from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    unit_cost: Decimal = Field(ge=0)
    selling_price: Optional[Decimal] = Field(default=None, ge=0)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0)


class PurchaseCreate(BaseModel):
    supplier_id: Optional[int] = None
    supplier_invoice_number: Optional[str] = None

    items: List[PurchaseItemCreate] = Field(
        min_length=1
    )

    discount_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    notes: Optional[str] = None


class PurchasePaymentCreate(BaseModel):
    payment_method: str = Field(
        min_length=2,
        max_length=30,
    )

    amount: Decimal = Field(gt=0)

    reference: Optional[str] = None
    notes: Optional[str] = None


class PurchaseReturnItemCreate(BaseModel):
    purchase_item_id: int
    quantity: Decimal = Field(gt=0)


class PurchaseReturnCreate(BaseModel):
    purchase_id: int

    items: List[PurchaseReturnItemCreate] = Field(
        min_length=1
    )

    reason: Optional[str] = None


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: Decimal
    unit_cost: Decimal
    selling_price: Optional[Decimal]
    discount_amount: Decimal
    total_amount: Decimal

    model_config = {
        "from_attributes": True,
    }


class PurchaseResponse(BaseModel):
    id: int
    invoice_number: str
    supplier_id: Optional[int]
    supplier_invoice_number: Optional[str]
    subtotal: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    payable_amount: Decimal
    status: str
    notes: Optional[str]
    created_at: datetime
    items: List[PurchaseItemResponse] = []

    model_config = {
        "from_attributes": True,
    }
