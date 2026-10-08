from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CashRegisterOpen(BaseModel):
    opening_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    notes: Optional[str] = None


class CashMovementCreate(BaseModel):
    movement_type: str = Field(
        min_length=2,
        max_length=30,
    )

    amount: Decimal = Field(gt=0)

    reason: Optional[str] = None

    reference: Optional[str] = None


class CashRegisterClose(BaseModel):
    actual_cash: Decimal = Field(ge=0)

    notes: Optional[str] = None


class CashMovementResponse(BaseModel):
    id: int
    movement_type: str
    amount: Decimal
    reason: Optional[str]
    reference: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class CashRegisterResponse(BaseModel):
    id: int
    opening_amount: Decimal
    cash_in: Decimal
    cash_out: Decimal
    cash_sales: Decimal
    expected_cash: Decimal
    actual_cash: Optional[Decimal]
    difference: Optional[Decimal]
    status: str
    opened_at: datetime
    closed_at: Optional[datetime]
    notes: Optional[str]
    movements: list[CashMovementResponse] = []

    model_config = {
        "from_attributes": True,
    }
