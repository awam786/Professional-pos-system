from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(
        gt=0,
    )

    unit_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    discount: Decimal = Field(
        default=0,
        ge=0,
    )

    note: Optional[str] = None


class CartItemResponse(BaseModel):
    product_id: UUID
    name: str
    sku: str
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal
    line_total: Decimal
    stock_available: Decimal


class CartCalculateRequest(BaseModel):
    items: list[CartItemCreate] = Field(
        default_factory=list,
    )

    customer_id: Optional[UUID] = None

    discount: Decimal = Field(
        default=0,
        ge=0,
    )

    notes: Optional[str] = None


class CartCalculateResponse(BaseModel):
    items: list[CartItemResponse]
    customer_id: Optional[UUID]
    is_vip: bool
    vip_customer_name: Optional[str]
    vip_customer_code: Optional[str]
    subtotal: Decimal
    discount: Decimal
    total: Decimal
    notes: Optional[str]


class HoldSaleRequest(BaseModel):
    items: list[CartItemCreate]

    customer_id: Optional[UUID] = None

    discount: Decimal = Field(
        default=0,
        ge=0,
    )

    notes: Optional[str] = None

    reference: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class HeldSaleResponse(BaseModel):
    id: UUID
    reference: str
    customer_id: Optional[UUID]
    subtotal: Decimal
    discount: Decimal
    total: Decimal
    notes: Optional[str]


class BarcodeLookupResponse(BaseModel):
    found: bool
    product_id: Optional[UUID]
    name: Optional[str]
    sku: Optional[str]
    selling_price: Optional[Decimal]
    current_stock: Optional[Decimal]
    barcode: str
