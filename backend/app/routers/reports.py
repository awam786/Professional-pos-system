from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.reports import (
    inventory_report,
    purchase_report,
    sales_report,
)


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


async def current_shop_id() -> int:
    return 1


@router.get("/sales")
async def get_sales_report(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
):
    return await sales_report(
        db=db,
        shop_id=await current_shop_id(),
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/purchases")
async def get_purchase_report(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
):
    return await purchase_report(
        db=db,
        shop_id=await current_shop_id(),
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/inventory")
async def get_inventory_report(
    db: AsyncSession = Depends(get_db),
):
    return await inventory_report(
        db=db,
        shop_id=await current_shop_id(),
    )
