from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Product
from app.models.customer import Customer
from app.schemas.pos import (
    CartCalculateRequest,
    CartCalculateResponse,
    CartItemResponse,
)
from app.services.customer import is_vip_customer


async def calculate_cart(
    db: AsyncSession,
    shop_id: UUID,
    payload: CartCalculateRequest,
) -> CartCalculateResponse:
    result_items: list[CartItemResponse] = []

    subtotal = Decimal("0")

    for item in payload.items:
        result = await db.execute(
            select(Product).where(
                Product.id == item.product_id,
                Product.shop_id == shop_id,
                Product.is_active.is_(True),
            )
        )

        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Product not found: "
                    f"{item.product_id}"
                ),
            )

        if product.current_stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient stock for "
                    f"{product.name}. "
                    f"Available: "
                    f"{product.current_stock}"
                ),
            )

        unit_price = (
            item.unit_price
            if item.unit_price is not None
            else product.selling_price
        )

        line_subtotal = unit_price * item.quantity
        line_total = line_subtotal - item.discount

        if line_total < 0:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Discount exceeds item value "
                    f"for {product.name}"
                ),
            )

        subtotal += line_total

        result_items.append(
            CartItemResponse(
                product_id=product.id,
                name=product.name,
                sku=product.sku,
                quantity=item.quantity,
                unit_price=unit_price,
                discount=item.discount,
                line_total=line_total,
                stock_available=product.current_stock,
            )
        )

    if payload.discount > subtotal:
        raise HTTPException(
            status_code=400,
            detail="Cart discount exceeds subtotal",
        )

    total = subtotal - payload.discount

    vip = False
    vip_name = None
    vip_code = None

    if payload.customer_id:
        vip = await is_vip_customer(
            db,
            shop_id,
            payload.customer_id,
        )

        customer_result = await db.execute(
            select(Customer).where(
                Customer.id == payload.customer_id,
                Customer.shop_id == shop_id,
            )
        )

        customer = customer_result.scalar_one_or_none()

        if customer:
            vip_name = customer.name
            vip_code = customer.customer_code

    return CartCalculateResponse(
        items=result_items,
        customer_id=payload.customer_id,
        is_vip=vip,
        vip_customer_name=vip_name,
        vip_customer_code=vip_code,
        subtotal=subtotal,
        discount=payload.discount,
        total=total,
        notes=payload.notes,
    )
