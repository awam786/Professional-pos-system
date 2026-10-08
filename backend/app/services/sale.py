from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.catalog import Product
from app.models.customer import Customer
from app.models.sale import Sale, SaleItem


async def create_sale(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
) -> Sale:
    if not data.items:
        raise ValueError("Sale must contain at least one item.")

    customer = None

    if data.customer_id:
        customer = await db.scalar(
            select(Customer).where(
                Customer.id == data.customer_id,
                Customer.shop_id == shop_id,
            )
        )

        if not customer:
            raise ValueError("Customer not found.")

    subtotal = Decimal("0")
    sale_items = []

    for item in data.items:
        product = await db.scalar(
            select(Product).where(
                Product.id == item.product_id,
                Product.shop_id == shop_id,
                Product.is_active.is_(True),
            )
        )

        if not product:
            raise ValueError(
                f"Product {item.product_id} was not found."
            )

        if Decimal(str(product.current_stock)) < item.quantity:
            raise ValueError(
                f"Insufficient stock for {product.name}."
            )

        unit_price = (
            item.unit_price
            if item.unit_price is not None
            else Decimal(str(product.selling_price))
        )

        line_subtotal = unit_price * item.quantity
        line_total = line_subtotal - item.discount_amount

        if line_total < 0:
            raise ValueError(
                f"Invalid discount for {product.name}."
            )

        subtotal += line_total

        sale_items.append(
            {
                "product": product,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "discount_amount": item.discount_amount,
                "total_amount": line_total,
            }
        )

    discount = Decimal(str(data.discount_amount))

    if discount > subtotal:
        raise ValueError(
            "Sale discount cannot exceed subtotal."
        )

    total = subtotal - discount

    is_vip = bool(data.is_vip or data.vip_discount)

    discount_label = (
        "VIP Discount"
        if is_vip and discount > 0
        else "Discount"
    )

    discount_type = (
        "vip"
        if is_vip and discount > 0
        else "normal"
        if discount > 0
        else "none"
    )

    sale = Sale(
        shop_id=shop_id,
        customer_id=data.customer_id,
        user_id=user_id,
        invoice_number=f"INV-{uuid4().hex[:10].upper()}",
        sale_type="OUT",
        subtotal=subtotal,
        discount_amount=discount,
        discount_type=discount_type,
        discount_label=discount_label,
        total_amount=total,
        paid_amount=Decimal("0"),
        credit_amount=total,
        change_amount=Decimal("0"),
        status="pending",
        notes=data.notes,
        is_vip=is_vip,
        receipt_stars=1 if is_vip else 3,
    )

    db.add(sale)
    await db.flush()

    for entry in sale_items:
        product = entry["product"]

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            product_name=product.name,
            sku=product.sku,
            quantity=entry["quantity"],
            unit_price=entry["unit_price"],
            cost_price=product.purchase_price,
            discount_amount=entry["discount_amount"],
            total_amount=entry["total_amount"],
        )

        db.add(sale_item)

        product.current_stock = (
            Decimal(str(product.current_stock))
            - entry["quantity"]
        )

    await db.commit()

    result = await db.scalar(
        select(Sale)
        .options(selectinload(Sale.items))
        .where(Sale.id == sale.id)
    )

    return result


async def get_sale(
    db: AsyncSession,
    shop_id: int,
    sale_id: int,
) -> Sale | None:
    return await db.scalar(
        select(Sale)
        .options(selectinload(Sale.items))
        .where(
            Sale.id == sale_id,
            Sale.shop_id == shop_id,
        )
    )
