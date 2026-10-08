from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Product
from app.models.stock_adjustment import StockAdjustment


ALLOWED_TYPES = {
    "increase",
    "decrease",
    "set",
}


async def create_stock_adjustment(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
) -> StockAdjustment:
    adjustment_type = (
        data.adjustment_type.lower().strip()
    )

    if adjustment_type not in ALLOWED_TYPES:
        raise ValueError(
            "Adjustment type must be increase, decrease, or set."
        )

    product = await db.scalar(
        select(Product).where(
            Product.id == data.product_id,
            Product.shop_id == shop_id,
        )
    )

    if not product:
        raise ValueError(
            "Product not found."
        )

    quantity = Decimal(str(data.quantity))

    if quantity <= 0:
        raise ValueError(
            "Adjustment quantity must be greater than zero."
        )

    previous_stock = Decimal(
        str(product.current_stock)
    )

    if adjustment_type == "increase":
        new_stock = (
            previous_stock + quantity
        )

    elif adjustment_type == "decrease":
        new_stock = (
            previous_stock - quantity
        )

        if new_stock < 0:
            raise ValueError(
                "Stock cannot become negative."
            )

    else:
        new_stock = quantity

    product.current_stock = new_stock

    adjustment = StockAdjustment(
        shop_id=shop_id,
        product_id=product.id,
        user_id=user_id,
        adjustment_type=adjustment_type,
        quantity=quantity,
        previous_stock=previous_stock,
        new_stock=new_stock,
        reason=data.reason,
        reference=data.reference,
    )

    db.add(adjustment)

    await db.commit()
    await db.refresh(adjustment)

    return adjustment


async def list_stock_adjustments(
    db: AsyncSession,
    shop_id: int,
    product_id: int | None = None,
):
    query = select(
        StockAdjustment
    ).where(
        StockAdjustment.shop_id == shop_id
    )

    if product_id:
        query = query.where(
            StockAdjustment.product_id
            == product_id
        )

    query = query.order_by(
        StockAdjustment.created_at.desc()
    )

    result = await db.scalars(query)

    return list(result.all())
