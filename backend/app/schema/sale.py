from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0)


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None

    items: List[SaleItemCreate] = Field(min_length=1)

    discount_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    notes: Optional[str] = None

    is_vip: bool = False

    vip_discount: bool = False


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    sku: Optional[str]
    quantity: Decimal
    unit_price: Decimal
    cost_price: Decimal
    discount_amount: Decimal
    total_amount: Decimal

    model_config = {
        "from_attributes": True
    }


class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: Optional[int]
    subtotal: Decimal
    discount_amount: Decimal
    discount_type: str
    discount_label: str
    total_amount: Decimal
    paid_amount: Decimal
    credit_amount: Decimal
    change_amount: Decimal
    status: str
    notes: Optional[str]
    is_vip: bool
    receipt_stars: int
    created_at: datetime
    items: List[SaleItemResponse] = []

    model_config = {
        "from_attributes": True,
    }
