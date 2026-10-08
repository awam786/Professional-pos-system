from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    parent_id: Optional[UUID] = None
    description: Optional[str] = None


class CategoryResponse(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    shop_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BrandCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None


class BrandResponse(BrandCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    shop_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    symbol: str = Field(min_length=1, max_length=20)
    unit_type: str = Field(default="piece", max_length=30)
    allows_decimal: bool = False


class UnitResponse(UnitCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    shop_id: UUID
    is_active: bool
    created_at: datetime


class BarcodeCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    symbology: str = Field(default="custom", max_length=50)
    is_primary: bool = False


class BarcodeResponse(BarcodeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    is_active: bool
    created_at: datetime


class ProductVariantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    sku: Optional[str] = Field(default=None, max_length=100)
    purchase_price: Optional[Decimal] = Field(default=None, ge=0)
    selling_price: Optional[Decimal] = Field(default=None, ge=0)
    stock: Decimal = Field(default=0, ge=0)
    attributes: Optional[str] = None


class ProductVariantResponse(ProductVariantCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    is_active: bool
    created_at: datetime


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=250)
    sku: str = Field(min_length=1, max_length=100)

    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    unit_id: Optional[UUID] = None

    description: Optional[str] = None
    image_url: Optional[str] = None

    purchase_price: Decimal = Field(default=0, ge=0)
    selling_price: Decimal = Field(default=0, ge=0)
    wholesale_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )
    minimum_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    current_stock: Decimal = Field(default=0, ge=0)
    minimum_stock: Decimal = Field(default=0, ge=0)
    maximum_stock: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    track_batch: bool = False
    track_expiry: bool = False
    track_serial: bool = False
    track_warranty: bool = False

    location: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    weight: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    size: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    color: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    barcodes: list[BarcodeCreate] = Field(
        default_factory=list,
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=250,
    )

    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    unit_id: Optional[UUID] = None

    description: Optional[str] = None
    image_url: Optional[str] = None

    purchase_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    selling_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    wholesale_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    minimum_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    minimum_stock: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    maximum_stock: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    track_batch: Optional[bool] = None
    track_expiry: Optional[bool] = None
    track_serial: Optional[bool] = None
    track_warranty: Optional[bool] = None

    location: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    weight: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    size: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    color: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    shop_id: UUID
    category_id: Optional[UUID]
    brand_id: Optional[UUID]
    unit_id: Optional[UUID]

    name: str
    sku: str
    description: Optional[str]
    image_url: Optional[str]

    purchase_price: Decimal
    selling_price: Decimal
    wholesale_price: Optional[Decimal]
    minimum_price: Optional[Decimal]

    current_stock: Decimal
    minimum_stock: Decimal
    maximum_stock: Optional[Decimal]

    track_batch: bool
    track_expiry: bool
    track_serial: bool
    track_warranty: bool

    location: Optional[str]
    weight: Optional[Decimal]
    size: Optional[str]
    color: Optional[str]

    is_active: bool
    created_at: datetime
    updated_at: datetime

    barcodes: list[BarcodeResponse] = Field(
        default_factory=list,
    )
