from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense


ALLOWED_PAYMENT_METHODS = {
    "cash",
    "bank",
    "card",
    "other",
}


async def create_expense(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
) -> Expense:
    amount = Decimal(str(data.amount))

    if amount <= 0:
        raise ValueError(
            "Expense amount must be greater than zero."
        )

    payment_method = (
        data.payment_method.lower().strip()
    )

    if payment_method not in ALLOWED_PAYMENT_METHODS:
        raise ValueError(
            "Invalid expense payment method."
        )

    expense = Expense(
        shop_id=shop_id,
        user_id=user_id,
        category=data.category.strip(),
        description=data.description,
        amount=amount,
        payment_method=payment_method,
        reference=data.reference,
        expense_date=(
            data.expense_date
            or datetime.utcnow()
        ),
    )

    db.add(expense)
    await db.commit()
    await db.refresh(expense)

    return expense


async def list_expenses(
    db: AsyncSession,
    shop_id: int,
):
    result = await db.scalars(
        select(Expense)
        .where(Expense.shop_id == shop_id)
        .order_by(
            Expense.expense_date.desc()
        )
    )

    return list(result.all())
