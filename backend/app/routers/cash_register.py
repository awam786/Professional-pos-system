from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.cash_register import (
    CashMovementCreate,
    CashRegisterClose,
    CashRegisterOpen,
    CashRegisterResponse,
)
from app.services.cash_register import (
    add_cash_movement,
    close_register,
    get_open_register,
    open_register,
)


router = APIRouter(
    prefix="/api/cash-register",
    tags=["Cash Register"],
)


async def current_shop_id() -> int:
    return 1


async def current_user_id() -> int:
    return 1


@router.get(
    "/current",
    response_model=CashRegisterResponse | None,
)
async def current_register(
    db: AsyncSession = Depends(get_db),
):
    return await get_open_register(
        db=db,
        shop_id=await current_shop_id(),
    )


@router.post(
    "/open",
    response_model=CashRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def open_cash_register(
    data: CashRegisterOpen,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await open_register(
            db=db,
            shop_id=await current_shop_id(),
            user_id=await current_user_id(),
            data=data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/movement",
)
async def create_cash_movement(
    data: CashMovementCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        movement = await add_cash_movement(
            db=db,
            shop_id=await current_shop_id(),
            user_id=await current_user_id(),
            data=data,
        )

        return movement

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/close",
    response_model=CashRegisterResponse,
)
async def close_cash_register(
    data: CashRegisterClose,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await close_register(
            db=db,
            shop_id=await current_shop_id(),
            actual_cash=data.actual_cash,
            notes=data.notes,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
