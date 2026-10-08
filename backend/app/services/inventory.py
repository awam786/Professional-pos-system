from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Product
from app.models.inventory import StockMovement


async def adjust_stock(
    db: AsyncSession,
    shop_id: UUID,
    product_id: UUID,
    quantity: Decimal,
    movement_type: str,
    user_id: UUID | None = None,
    location_id: UUID | None = None,
    batch_id: UUID | None = None,
    note: str | None = None,
) -> StockMovement:
    result = await db.execute(
        select(Product)
        .where(
            Product.id == product_id,
            Product.shop_id == shop_id,
        )
        .with_for_update()
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    stock_before = product.current_stock
    stock_after = stock_before + quantity

    if stock_after < 0:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock",
        )

    product.current_stock = stock_after

    movement = StockMovement(
        shop_id=shop_id,
        product_id=product_id,
        location_id=location_id,
        batch_id=batch_id,
        quantity=quantity,
        stock_before=stock_before,
        stock_after=stock_after,
        movement_type=movement_type,
        created_by=user_id,
        note=note,
    )

    db.add(movement)

    await db.flush()

    return movement
