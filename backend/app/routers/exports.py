from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.export import report_to_csv
from app.services.reports import (
    inventory_report,
    purchase_report,
    sales_report,
)


router = APIRouter(
    prefix="/api/exports",
    tags=["Exports"],
)


async def current_shop_id() -> int:
    return 1


@router.get("/sales.csv")
async def export_sales_csv(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
):
    report = await sales_report(
        db=db,
        shop_id=await current_shop_id(),
        start_date=start_date,
        end_date=end_date,
    )

    content = report_to_csv(report)

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="sales-report.csv"'
            )
        },
    )


@router.get("/purchases.csv")
async def export_purchases_csv(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
):
    report = await purchase_report(
        db=db,
        shop_id=await current_shop_id(),
        start_date=start_date,
        end_date=end_date,
    )

    content = report_to_csv(report)

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="purchase-report.csv"'
            )
        },
    )


@router.get("/inventory.csv")
async def export_inventory_csv(
    db: AsyncSession = Depends(get_db),
):
    report = await inventory_report(
        db=db,
        shop_id=await current_shop_id(),
    )

    content = report_to_csv(report)

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="inventory-report.csv"'
            )
        },
    )
