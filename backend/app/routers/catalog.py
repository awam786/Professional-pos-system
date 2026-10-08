from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.catalog import (
    Brand,
    Category,
    Product,
    ProductBarcode,
    Unit,
)
from app.schemas.catalog import (
    BarcodeResponse,
    BrandCreate,
    BrandResponse,
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductResponse,
    UnitCreate,
    UnitResponse,
)
from app.services.product import barcode_exists

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


# ---------------------------------------------------------
# Temporary shop resolver for Batch 2.
# Authentication middleware will replace this in Batch 3.
# ---------------------------------------------------------

async def get_default_shop_id(
    db: AsyncSession,
) -> UUID:
    from app.models import Shop

    result = await db.execute(
        select(Shop.id)
        .where(Shop.is_active.is_(True))
        .limit(1)
    )

    shop_id = result.scalar_one_or_none()

    if shop_id is None:
        raise HTTPException(
            status_code=404,
            detail="No active shop configured",
        )

    return shop_id


@router.post(
    "/categories",
    response_model=CategoryResponse,
)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    category = Category(
        shop_id=shop_id,
        name=payload.name,
        parent_id=payload.parent_id,
        description=payload.description,
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
)
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Category)
        .where(Category.shop_id == shop_id)
        .order_by(Category.name)
    )

    return result.scalars().all()


@router.post(
    "/brands",
    response_model=BrandResponse,
)
async def create_brand(
    payload: BrandCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    brand = Brand(
        shop_id=shop_id,
        name=payload.name,
        description=payload.description,
    )

    db.add(brand)
    await db.commit()
    await db.refresh(brand)

    return brand


@router.get(
    "/brands",
    response_model=list[BrandResponse],
)
async def list_brands(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Brand)
        .where(Brand.shop_id == shop_id)
        .order_by(Brand.name)
    )

    return result.scalars().all()


@router.post(
    "/units",
    response_model=UnitResponse,
)
async def create_unit(
    payload: UnitCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    unit = Unit(
        shop_id=shop_id,
        name=payload.name,
        symbol=payload.symbol,
        unit_type=payload.unit_type,
        allows_decimal=payload.allows_decimal,
    )

    db.add(unit)
    await db.commit()
    await db.refresh(unit)

    return unit


@router.get(
    "/units",
    response_model=list[UnitResponse],
)
async def list_units(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Unit)
        .where(Unit.shop_id == shop_id)
        .order_by(Unit.name)
    )

    return result.scalars().all()


@router.post(
    "/products",
    response_model=ProductResponse,
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    for barcode in payload.barcodes:
        if await barcode_exists(db, barcode.code):
            raise HTTPException(
                status_code=409,
                detail=f"Barcode already exists: {barcode.code}",
            )

    product = Product(
        shop_id=shop_id,
        category_id=payload.category_id,
        brand_id=payload.brand_id,
        unit_id=payload.unit_id,
        name=payload.name,
        sku=payload.sku,
        description=payload.description,
        image_url=payload.image_url,
        purchase_price=payload.purchase_price,
        selling_price=payload.selling_price,
        wholesale_price=payload.wholesale_price,
        minimum_price=payload.minimum_price,
        current_stock=payload.current_stock,
        minimum_stock=payload.minimum_stock,
        maximum_stock=payload.maximum_stock,
        track_batch=payload.track_batch,
        track_expiry=payload.track_expiry,
        track_serial=payload.track_serial,
        track_warranty=payload.track_warranty,
        location=payload.location,
        weight=payload.weight,
        size=payload.size,
        color=payload.color,
    )

    db.add(product)

    await db.flush()

    for barcode_data in payload.barcodes:
        product.barcodes.append(
            ProductBarcode(
                code=barcode_data.code,
                symbology=barcode_data.symbology,
                is_primary=barcode_data.is_primary,
            )
        )

    await db.commit()
    await db.refresh(product)

    return product


@router.get(
    "/products",
    response_model=list[ProductResponse],
)
async def list_products(
    search: str | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    query = select(Product).where(
        Product.shop_id == shop_id,
    )

    if active_only:
        query = query.where(
            Product.is_active.is_(True)
        )

    if search:
        query = query.where(
            Product.name.ilike(f"%{search}%")
            | Product.sku.ilike(f"%{search}%")
        )

    query = query.order_by(Product.name)

    result = await db.execute(query)

    return result.scalars().unique().all()


@router.get(
    "/products/barcode/{code}",
    response_model=ProductResponse,
)
async def product_by_barcode(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Product)
        .join(
            ProductBarcode,
            ProductBarcode.product_id == Product.id,
        )
        .where(
            Product.shop_id == shop_id,
            ProductBarcode.code == code,
            ProductBarcode.is_active.is_(True),
            Product.is_active.is_(True),
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Barcode not found",
        )

    return product
