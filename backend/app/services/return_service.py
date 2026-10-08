from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.return_model import SaleReturn, SaleReturnItem
from app.models.sale import Sale, SaleItem
from app.models.catalog import Product


async def create_sale_return(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
) -> SaleReturn:
    sale = await db.scalar(
        select(Sale).where(
            Sale.id == data.sale_id,
            Sale.shop_id == shop_id,
        )
    )

    if not sale:
        raise ValueError("Sale not found.")

    total = Decimal("0")
    return_items = []

    for requested in data.items:
        sale_item = await db.scalar(
            select(SaleItem).where(
                SaleItem.id == requested.sale_item_id,
                SaleItem.sale_id == sale.id,
            )
        )

        if not sale_item:
            raise ValueError(
                "Sale item not found."
            )

        if requested.quantity > sale_item.quantity:
            raise ValueError(
                f"Cannot return more than sold quantity "
                f"for {sale_item.product_name}."
            )

        amount = (
            Decimal(str(sale_item.unit_price))
            * requested.quantity
        )

        total += amount

        return_items.append(
            (
                sale_item,
                requested.quantity,
                amount,
            )
        )

    sale_return = SaleReturn(
        shop_id=shop_id,
        sale_id=sale.id,
        customer_id=sale.customer_id,
        user_id=user_id,
        return_number=f"RET-{uuid4().hex[:10].upper()}",
        total_amount=total,
        refund_method=data.refund_method.lower(),
        reason=data.reason,
        status="completed",
    )

    db.add(sale_return)
    await db.flush()

    for sale_item, quantity, amount in return_items:
        product = await db.scalar(
            select(Product).where(
                Product.id == sale_item.product_id,
                Product.shop_id == shop_id,
            )
        )

        if not product:
            raise ValueError(
                f"Product {sale_item.product_name} not found."
            )

        product.current_stock = (
            Decimal(str(product.current_stock))
            + quantity
        )

        db.add(
            SaleReturnItem(
                return_id=sale_return.id,
                sale_item_id=sale_item.id,
                product_id=product.id,
                product_name=sale_item.product_name,
                quantity=quantity,
                unit_price=sale_item.unit_price,
                total_amount=amount,
            )
        )

    await db.commit()
    await db.refresh(sale_return)

    return sale_return
