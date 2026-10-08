from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.models.sale import Sale


ALLOWED_PAYMENT_METHODS = {
    "cash",
    "bank",
    "card",
    "other",
}


async def add_payment(
    db: AsyncSession,
    shop_id: int,
    sale_id: int,
    data,
) -> Payment:
    sale = await db.scalar(
        select(Sale).where(
            Sale.id == sale_id,
            Sale.shop_id == shop_id,
        )
    )

    if not sale:
        raise ValueError("Sale not found.")

    method = data.payment_method.lower().strip()

    if method not in ALLOWED_PAYMENT_METHODS:
        raise ValueError(
            "Invalid payment method."
        )

    amount = Decimal(str(data.amount))

    if amount <= 0:
        raise ValueError(
            "Payment amount must be greater than zero."
        )

    remaining = (
        Decimal(str(sale.total_amount))
        - Decimal(str(sale.paid_amount))
    )

    if remaining <= 0:
        raise ValueError(
            "This sale is already fully paid."
        )

    payment_amount = min(amount, remaining)
    change = max(amount - remaining, Decimal("0"))

    payment = Payment(
        shop_id=shop_id,
        sale_id=sale.id,
        payment_method=method,
        amount=payment_amount,
        reference=data.reference,
        notes=data.notes,
    )

    db.add(payment)

    sale.paid_amount = (
        Decimal(str(sale.paid_amount))
        + payment_amount
    )

    sale.credit_amount = max(
        Decimal(str(sale.total_amount))
        - Decimal(str(sale.paid_amount)),
        Decimal("0"),
    )

    sale.change_amount = (
        Decimal(str(sale.change_amount))
        + change
    )

    if sale.credit_amount == 0:
        sale.status = "completed"
    else:
        sale.status = "credit"

    await db.commit()
    await db.refresh(payment)

    return payment
