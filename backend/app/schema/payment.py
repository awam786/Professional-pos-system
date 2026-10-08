from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    payment_method: str = Field(
        min_length=2,
        max_length=30,
    )

    amount: Decimal = Field(gt=0)

    reference: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    sale_id: int
    payment_method: str
    amount: Decimal
    reference: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
