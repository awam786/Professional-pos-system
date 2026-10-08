from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.receipt import build_receipt_data
from app.services.sale import get_sale


router = APIRouter(
    prefix="/api/receipts",
    tags=["Receipts"],
)


async def current_shop_id() -> int:
    return 1


@router.get("/{sale_id}")
async def get_receipt(
    sale_id: int,
    db: AsyncSession = Depends(get_db),
):
    sale = await get_sale(
        db=db,
        shop_id=await current_shop_id(),
        sale_id=sale_id,
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found.",
        )

    return build_receipt_data(sale)
