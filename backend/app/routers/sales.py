from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale import create_sale, get_sale


router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"],
)


async def current_shop_id() -> int:
    return 1


async def current_user_id() -> int:
    return 1


@router.post(
    "",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_sale(
    data: SaleCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        sale = await create_sale(
            db=db,
            shop_id=await current_shop_id(),
            user_id=await current_user_id(),
            data=data,
        )

        return sale

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
async def read_sale(
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

    return sale
