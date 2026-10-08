from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=50,
    )

    email: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    address: Optional[str] = None

    customer_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    credit_limit: Decimal = Field(
        default=0,
        ge=0,
    )

    notes: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=50,
    )

    email: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    address: Optional[str] = None

    customer_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    credit_limit: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    notes: Optional[str] = None

    is_active: Optional[bool] = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    shop_id: UUID
    name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    customer_code: Optional[str]
    credit_limit: Decimal
    current_balance: Decimal
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class WhitelistCreate(BaseModel):
    customer_id: UUID

    owner_code: str = Field(
        min_length=1,
        max_length=100,
    )


class WhitelistUpdate(BaseModel):
    owner_code: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    is_active: Optional[bool] = None


class WhitelistResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    shop_id: UUID
    customer_id: UUID
    owner_code: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class VIPCustomerResponse(BaseModel):
    is_vip: bool
    customer_id: UUID
    name: str
    phone: Optional[str]
    customer_code: Optional[str]
    owner_code: Optional[str]
    status: str
