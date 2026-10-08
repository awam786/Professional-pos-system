from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

    phone: Optional[str] = Field(
        default=None,
        max_length=50,
    )

    email: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    company: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    address: Optional[str] = None

    supplier_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    opening_balance: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    notes: Optional[str] = None


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    supplier_code: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    company: Optional[str]
    address: Optional[str]
    supplier_code: Optional[str]
    opening_balance: Decimal
    current_balance: Decimal
    notes: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
