from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class StockAdjustmentCreate(BaseModel):
    product_id: int

    adjustment_type: str = Field(
        min_length=2,
        max_length=30,
    )

    quantity: Decimal = Field(
        gt=0
    )

    reason: Optional[str] = None

    reference: Optional[str] = None


class StockAdjustmentResponse(BaseModel):
    id: int
    product_id: int
    adjustment_type: str
    quantity: Decimal
    previous_stock: Decimal
    new_stock: Decimal
    reason: Optional[str]
    reference: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
