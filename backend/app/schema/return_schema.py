from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class SaleReturnItemCreate(BaseModel):
    sale_item_id: int
    quantity: Decimal = Field(gt=0)


class SaleReturnCreate(BaseModel):
    sale_id: int

    items: List[SaleReturnItemCreate] = Field(
        min_length=1
    )

    refund_method: str = Field(
        default="cash",
        min_length=2,
        max_length=30,
    )

    reason: Optional[str] = None


class SaleReturnItemResponse(BaseModel):
    id: int
    sale_item_id: int
    product_id: int
    product_name: str
    quantity: Decimal
    unit_price: Decimal
    total_amount: Decimal

    model_config = {
        "from_attributes": True,
    }


class SaleReturnResponse(BaseModel):
    id: int
    return_number: str
    sale_id: int
    customer_id: Optional[int]
    total_amount: Decimal
    refund_method: str
    reason: Optional[str]
    status: str
    created_at: datetime
    items: List[SaleReturnItemResponse] = []

    model_config = {
        "from_attributes": True,
    }
