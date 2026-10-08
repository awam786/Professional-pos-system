from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InventoryLocationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None


class InventoryLocationResponse(
    InventoryLocationCreate
):
    id: UUID
    shop_id: UUID
    created_at: datetime


class ProductBatchCreate(BaseModel):
    product_id: UUID
    batch_number: str = Field(
        min_length=1,
        max_length=100,
    )
    expiry_date: Optional[date] = None
    manufacturing_date: Optional[date] = None
    quantity: Decimal = Field(default=0, ge=0)
    purchase_price: Decimal = Field(default=0, ge=0)


class ProductBatchResponse(ProductBatchCreate):
    id: UUID
    created_at: datetime


class StockAdjustmentRequest(BaseModel):
    product_id: UUID
    quantity: Decimal
    movement_type: str = Field(
        min_length=1,
        max_length=50,
    )
    location_id: Optional[UUID] = None
    batch_id: Optional[UUID] = None
    note: Optional[str] = None


class StockMovementResponse(BaseModel):
    id: UUID
    shop_id: UUID
    product_id: UUID
    location_id: Optional[UUID]
    batch_id: Optional[UUID]
    quantity: Decimal
    stock_before: Decimal
    stock_after: Decimal
    movement_type: str
    reference_type: Optional[str]
    reference_id: Optional[str]
    note: Optional[str]
    created_by: Optional[UUID]
    created_at: datetime
