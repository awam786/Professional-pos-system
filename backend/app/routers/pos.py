import uuid
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Shop
from app.models.catalog import Product, ProductBarcode
from app.models.pos import HeldSale
from app.schemas.pos import (
    BarcodeLookupResponse,
    CartCalculateRequest,
    CartCalculateResponse,
    HeldSaleResponse,
    HoldSaleRequest,
)
from app.services.pos import calculate_cart

router = APIRouter(
    prefix="/pos",
    tags=["POS"],
)


async def get_default_shop_id(
    db: AsyncSession,
) -> UUID:
    result = await db.execute(
        select(Shop.id)
        .where(Shop.is_active.is_(True))
        .limit(1)
    )

    shop_id = result.scalar_one_or_none()

    if shop_id is None:
        raise HTTPException(
            status_code=404,
            detail="No active shop configured",
        )

    return shop_id


@router.post(
    "/cart/calculate",
    response_model=CartCalculateResponse,
)
async def calculate_pos_cart(
    payload: CartCalculateRequest,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    return await calculate_cart(
        db,
        shop_id,
        payload,
    )


@router.get(
    "/barcode/{code}",
    response_model=BarcodeLookupResponse,
)
async def lookup_barcode(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Product)
        .join(
            ProductBarcode,
            ProductBarcode.product_id == Product.id,
        )
        .where(
            Product.shop_id == shop_id,
            ProductBarcode.code == code,
            ProductBarcode.is_active.is_(True),
            Product.is_active.is_(True),
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        return BarcodeLookupResponse(
            found=False,
            product_id=None,
            name=None,
            sku=None,
            selling_price=None,
            current_stock=None,
            barcode=code,
        )

    return BarcodeLookupResponse(
        found=True,
        product_id=product.id,
        name=product.name,
        sku=product.sku,
        selling_price=product.selling_price,
        current_stock=product.current_stock,
        barcode=code,
    )


@router.post(
    "/hold",
    response_model=HeldSaleResponse,
)
async def hold_sale(
    payload: HoldSaleRequest,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    calculation = await calculate_cart(
        db,
        shop_id,
        CartCalculateRequest(
            items=payload.items,
            customer_id=payload.customer_id,
            discount=payload.discount,
            notes=payload.notes,
        ),
    )

    reference = payload.reference or (
        f"HOLD-{uuid.uuid4().hex[:10].upper()}"
    )

    cart_data = {
        "items": [
            item.model_dump(mode="json")
            for item in calculation.items
        ],
        "customer_id": (
            str(payload.customer_id)
            if payload.customer_id
            else None
        ),
    }

    # Batch 3 does not yet have the authenticated
    # user dependency. A system placeholder is used
    # temporarily and will be replaced in Batch 4.
    from app.models import User

    user_result = await db.execute(
        select(User.id)
        .where(
            User.shop_id == shop_id,
            User.is_active.is_(True),
        )
        .limit(1)
    )

    user_id = user_result.scalar_one_or_none()

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="No active user available",
        )

    held_sale = HeldSale(
        shop_id=shop_id,
        user_id=user_id,
        customer_id=payload.customer_id,
        reference=reference,
        cart_data=cart_data,
        subtotal=calculation.subtotal,
        discount=calculation.discount,
        total=calculation.total,
        notes=payload.notes,
    )

    db.add(held_sale)

    await db.commit()
    await db.refresh(held_sale)

    return HeldSaleResponse(
        id=held_sale.id,
        reference=held_sale.reference,
        customer_id=held_sale.customer_id,
        subtotal=held_sale.subtotal,
        discount=held_sale.discount,
        total=held_sale.total,
        notes=held_sale.notes,
    )


@router.get(
    "/held",
    response_model=list[HeldSaleResponse],
)
async def list_held_sales(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(HeldSale)
        .where(HeldSale.shop_id == shop_id)
        .order_by(HeldSale.created_at.desc())
    )

    return [
        HeldSaleResponse(
            id=item.id,
            reference=item.reference,
            customer_id=item.customer_id,
            subtotal=item.subtotal,
            discount=item.discount,
            total=item.total,
            notes=item.notes,
        )
        for item in result.scalars().all()
    ]


@router.delete(
    "/held/{held_sale_id}",
)
async def delete_held_sale(
    held_sale_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(HeldSale).where(
            HeldSale.id == held_sale_id,
            HeldSale.shop_id == shop_id,
        )
    )

    held_sale = result.scalar_one_or_none()

    if held_sale is None:
        raise HTTPException(
            status_code=404,
            detail="Held sale not found",
        )

    await db.delete(held_sale)
    await db.commit()

    return {
        "success": True,
        "message": "Held sale deleted",
    }
