from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.catalog import Product
from app.models.purchase import (
    Purchase,
    PurchaseItem,
    PurchasePayment,
)
from app.models.supplier import Supplier


async def create_purchase(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
) -> Purchase:
    if not data.items:
        raise ValueError(
            "Purchase must contain at least one item."
        )

    if data.supplier_id:
        supplier = await db.scalar(
            select(Supplier).where(
                Supplier.id == data.supplier_id,
                Supplier.shop_id == shop_id,
            )
        )

        if not supplier:
            raise ValueError(
                "Supplier not found."
            )

    subtotal = Decimal("0")
    purchase_items = []

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

        line_total = (
            item.unit_cost * item.quantity
        ) - item.discount_amount

        if line_total < 0:
            raise ValueError(
                f"Invalid discount for {product.name}."
            )

        subtotal += line_total

        purchase_items.append(
            (
                product,
                item,
                line_total,
            )
        )

    discount = Decimal(
        str(data.discount_amount)
    )

    if discount > subtotal:
        raise ValueError(
            "Purchase discount cannot exceed subtotal."
        )

    total = subtotal - discount

    purchase = Purchase(
        shop_id=shop_id,
        supplier_id=data.supplier_id,
        user_id=user_id,
        invoice_number=(
            f"PUR-{uuid4().hex[:10].upper()}"
        ),
        supplier_invoice_number=(
            data.supplier_invoice_number
        ),
        subtotal=subtotal,
        discount_amount=discount,
        total_amount=total,
        paid_amount=Decimal("0"),
        payable_amount=total,
        status="credit" if total > 0 else "completed",
        notes=data.notes,
    )

    db.add(purchase)
    await db.flush()

    for product, item, line_total in purchase_items:
        db.add(
            PurchaseItem(
                purchase_id=purchase.id,
                product_id=product.id,
                product_name=product.name,
                quantity=item.quantity,
                unit_cost=item.unit_cost,
                selling_price=item.selling_price,
                discount_amount=item.discount_amount,
                total_amount=line_total,
            )
        )

        product.current_stock = (
            Decimal(str(product.current_stock))
            + item.quantity
        )

        product.purchase_price = item.unit_cost

        if item.selling_price is not None:
            product.selling_price = item.selling_price

    if data.supplier_id:
        supplier = await db.scalar(
            select(Supplier).where(
                Supplier.id == data.supplier_id
            )
        )

        if supplier:
            supplier.current_balance = (
                Decimal(str(supplier.current_balance))
                + total
            )

    await db.commit()

    result = await db.scalar(
        select(Purchase)
        .options(selectinload(Purchase.items))
        .where(Purchase.id == purchase.id)
    )

    return result


async def add_purchase_payment(
    db: AsyncSession,
    shop_id: int,
    purchase_id: int,
    data,
) -> PurchasePayment:
    purchase = await db.scalar(
        select(Purchase).where(
            Purchase.id == purchase_id,
            Purchase.shop_id == shop_id,
        )
    )

    if not purchase:
        raise ValueError(
            "Purchase not found."
        )

    amount = Decimal(str(data.amount))

    if amount <= 0:
        raise ValueError(
            "Payment must be greater than zero."
        )

    remaining = (
        Decimal(str(purchase.total_amount))
        - Decimal(str(purchase.paid_amount))
    )

    if remaining <= 0:
        raise ValueError(
            "Purchase is already fully paid."
        )

    payment_amount = min(
        amount,
        remaining,
    )

    payment = PurchasePayment(
        shop_id=shop_id,
        purchase_id=purchase.id,
        payment_method=data.payment_method.lower(),
        amount=payment_amount,
        reference=data.reference,
        notes=data.notes,
    )

    db.add(payment)

    purchase.paid_amount = (
        Decimal(str(purchase.paid_amount))
        + payment_amount
    )

    purchase.payable_amount = max(
        Decimal(str(purchase.total_amount))
        - Decimal(str(purchase.paid_amount)),
        Decimal("0"),
    )

    purchase.status = (
        "completed"
        if purchase.payable_amount == 0
        else "credit"
    )

    if purchase.supplier_id:
        supplier = await db.scalar(
            select(Supplier).where(
                Supplier.id == purchase.supplier_id
            )
        )

        if supplier:
            supplier.current_balance = max(
                Decimal(str(supplier.current_balance))
                - payment_amount,
                Decimal("0"),
            )

    await db.commit()
    await db.refresh(payment)

    return payment
