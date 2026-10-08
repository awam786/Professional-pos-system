from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from app.services.payment import add_payment


router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"],
)


async def current_shop_id() -> int:
    return 1


@router.post(
    "/sales/{sale_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    sale_id: int,
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await add_payment(
            db=db,
            shop_id=await current_shop_id(),
            sale_id=sale_id,
            data=data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
