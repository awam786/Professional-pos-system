from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.daily_closing import DailyClosingResponse
from app.services.daily_closing import (
    build_daily_summary,
    close_daily_day,
    get_daily_closing,
)


router = APIRouter(
    prefix="/api/daily-closing",
    tags=["Daily Closing"],
)


async def current_shop_id() -> int:
    return 1


async def current_user_id() -> int:
    return 1


@router.get(
    "/summary",
)
async def daily_summary(
    target_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await build_daily_summary(
        db=db,
        shop_id=await current_shop_id(),
        target_date=target_date,
    )


@router.post(
    "/close",
    response_model=DailyClosingResponse,
)
async def close_day(
    target_date: date,
    opening_cash: Decimal = Decimal("0"),
    closing_cash: Decimal = Decimal("0"),
    register_id: int | None = None,
    notes: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await close_daily_day(
            db=db,
            shop_id=await current_shop_id(),
            user_id=await current_user_id(),
            target_date=target_date,
            opening_cash=opening_cash,
            closing_cash=closing_cash,
            register_id=register_id,
            notes=notes,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{target_date}",
    response_model=DailyClosingResponse | None,
)
async def get_closed_day(
    target_date: date,
    db: AsyncSession = Depends(get_db),
):
    return await get_daily_closing(
        db=db,
        shop_id=await current_shop_id(),
        target_date=target_date,
    )
