from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.purchase import (
    PurchaseCreate,
    PurchasePaymentCreate,
    PurchaseResponse,
)
from app.services.purchase import (
    add_purchase_payment,
    create_purchase,
)


router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"],
)


async def current_shop_id() -> int:
    return 1


async def current_user_id() -> int:
    return 1


@router.post(
    "",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_purchase(
    data: PurchaseCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_purchase(
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
    "/{purchase_id}/payments",
)
async def create_purchase_payment(
    purchase_id: int,
    data: PurchasePaymentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        payment = await add_purchase_payment(
            db=db,
            shop_id=await current_shop_id(),
            purchase_id=purchase_id,
            data=data,
        )

        return {
            "success": True,
            "payment_id": payment.id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
