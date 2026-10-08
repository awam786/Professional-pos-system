from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.return_schema import (
    SaleReturnCreate,
    SaleReturnResponse,
)
from app.services.return_service import create_sale_return


router = APIRouter(
    prefix="/api/returns",
    tags=["Returns"],
)


async def current_shop_id() -> int:
    return 1


async def current_user_id() -> int:
    return 1


@router.post(
    "",
    response_model=SaleReturnResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_return(
    data: SaleReturnCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_sale_return(
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
