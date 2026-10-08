from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cash_register import (
    CashMovement,
    CashRegister,
)


VALID_MOVEMENT_TYPES = {
    "cash_in",
    "cash_out",
}


async def get_open_register(
    db: AsyncSession,
    shop_id: int,
):
    return await db.scalar(
        select(CashRegister)
        .options(
            selectinload(
                CashRegister.movements
            )
        )
        .where(
            CashRegister.shop_id == shop_id,
            CashRegister.status == "open",
        )
        .order_by(
            CashRegister.opened_at.desc()
        )
    )


async def open_register(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
):
    existing = await get_open_register(
        db,
        shop_id,
    )

    if existing:
        raise ValueError(
            "A cash register is already open."
        )

    register = CashRegister(
        shop_id=shop_id,
        user_id=user_id,
        opening_amount=data.opening_amount,
        expected_cash=data.opening_amount,
        status="open",
        notes=data.notes,
    )

    db.add(register)

    await db.commit()
    await db.refresh(register)

    return register


async def add_cash_movement(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    data,
):
    register = await get_open_register(
        db,
        shop_id,
    )

    if not register:
        raise ValueError(
            "No open cash register."
        )

    movement_type = (
        data.movement_type.lower().strip()
    )

    if movement_type not in VALID_MOVEMENT_TYPES:
        raise ValueError(
            "Movement type must be cash_in or cash_out."
        )

    amount = Decimal(str(data.amount))

    movement = CashMovement(
        register_id=register.id,
        shop_id=shop_id,
        user_id=user_id,
        movement_type=movement_type,
        amount=amount,
        reason=data.reason,
        reference=data.reference,
    )

    db.add(movement)

    if movement_type == "cash_in":
        register.cash_in = (
            Decimal(str(register.cash_in))
            + amount
        )
        register.expected_cash = (
            Decimal(str(register.expected_cash))
            + amount
        )

    else:
        available = Decimal(
            str(register.expected_cash)
        )

        if amount > available:
            raise ValueError(
                "Cash out cannot exceed expected cash."
            )

        register.cash_out = (
            Decimal(str(register.cash_out))
            + amount
        )

        register.expected_cash = (
            Decimal(str(register.expected_cash))
            - amount
        )

    await db.commit()
    await db.refresh(movement)

    return movement


async def close_register(
    db: AsyncSession,
    shop_id: int,
    actual_cash: Decimal,
    notes: str | None = None,
):
    register = await get_open_register(
        db,
        shop_id,
    )

    if not register:
        raise ValueError(
            "No open cash register."
        )

    actual_cash = Decimal(str(actual_cash))

    expected_cash = Decimal(
        str(register.expected_cash)
    )

    difference = (
        actual_cash - expected_cash
    )

    register.actual_cash = actual_cash
    register.difference = difference
    register.closed_at = (
        __import__("datetime")
        .datetime.utcnow()
    )
    register.status = "closed"

    if notes:
        register.notes = notes

    await db.commit()
    await db.refresh(register)

    return register
