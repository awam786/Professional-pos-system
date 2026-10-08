from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Shop
from app.models.inventory import (
    InventoryLocation,
    ProductBatch,
    StockMovement,
)
from app.schemas.inventory import (
    InventoryLocationCreate,
    InventoryLocationResponse,
    ProductBatchCreate,
    ProductBatchResponse,
    StockAdjustmentRequest,
    StockMovementResponse,
)
from app.services.inventory import adjust_stock

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
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
    "/locations",
    response_model=InventoryLocationResponse,
)
async def create_location(
    payload: InventoryLocationCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    location = InventoryLocation(
        shop_id=shop_id,
        name=payload.name,
        description=payload.description,
    )

    db.add(location)
    await db.commit()
    await db.refresh(location)

    return location


@router.get(
    "/locations",
    response_model=list[InventoryLocationResponse],
)
async def list_locations(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(InventoryLocation)
        .where(
            InventoryLocation.shop_id == shop_id
        )
        .order_by(InventoryLocation.name)
    )

    return result.scalars().all()


@router.post(
    "/batches",
    response_model=ProductBatchResponse,
)
async def create_batch(
    payload: ProductBatchCreate,
    db: AsyncSession = Depends(get_db),
):
    batch = ProductBatch(
        product_id=payload.product_id,
        batch_number=payload.batch_number,
        expiry_date=payload.expiry_date,
        manufacturing_date=payload.manufacturing_date,
        quantity=payload.quantity,
        purchase_price=payload.purchase_price,
    )

    db.add(batch)
    await db.commit()
    await db.refresh(batch)

    return batch


@router.post(
    "/adjust",
    response_model=StockMovementResponse,
)
async def stock_adjustment(
    payload: StockAdjustmentRequest,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    movement = await adjust_stock(
        db=db,
        shop_id=shop_id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        movement_type=payload.movement_type,
        location_id=payload.location_id,
        batch_id=payload.batch_id,
        note=payload.note,
    )

    await db.commit()
    await db.refresh(movement)

    return movement


@router.get(
    "/movements",
    response_model=list[StockMovementResponse],
)
async def list_stock_movements(
    product_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    query = select(StockMovement).where(
        StockMovement.shop_id == shop_id,
    )

    if product_id:
        query = query.where(
            StockMovement.product_id == product_id
        )

    query = query.order_by(
        StockMovement.created_at.desc()
    )

    result = await db.execute(query)

    return result.scalars().all()
