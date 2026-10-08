from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    category: str = Field(
        min_length=1,
        max_length=100,
    )

    description: Optional[str] = None

    amount: Decimal = Field(gt=0)

    payment_method: str = Field(
        default="cash",
        min_length=2,
        max_length=30,
    )

    reference: Optional[str] = None

    expense_date: Optional[datetime] = None


class ExpenseResponse(BaseModel):
    id: int
    category: str
    description: Optional[str]
    amount: Decimal
    payment_method: str
    reference: Optional[str]
    expense_date: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
