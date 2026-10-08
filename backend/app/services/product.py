from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import (
    Product,
    ProductBarcode,
)


async def get_product_by_id(
    db: AsyncSession,
    shop_id: UUID,
    product_id: UUID,
) -> Product | None:
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.shop_id == shop_id,
        )
    )

    return result.scalar_one_or_none()


async def get_product_by_barcode(
    db: AsyncSession,
    shop_id: UUID,
    code: str,
) -> Product | None:
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

    return result.scalar_one_or_none()


async def barcode_exists(
    db: AsyncSession,
    code: str,
) -> bool:
    result = await db.execute(
        select(ProductBarcode.id).where(
            ProductBarcode.code == code,
        )
    )

    return result.scalar_one_or_none() is not None
