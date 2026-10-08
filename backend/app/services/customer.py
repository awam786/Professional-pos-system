from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import (
    Customer,
    WhitelistCustomer,
)


async def find_customer(
    db: AsyncSession,
    shop_id: UUID,
    search: str,
) -> Customer | None:
    result = await db.execute(
        select(Customer).where(
            Customer.shop_id == shop_id,
            Customer.is_active.is_(True),
            or_(
                Customer.phone == search,
                Customer.customer_code == search,
            ),
        )
    )

    return result.scalar_one_or_none()


async def get_vip_customer(
    db: AsyncSession,
    shop_id: UUID,
    search: str,
) -> tuple[Customer | None, WhitelistCustomer | None]:
    result = await db.execute(
        select(Customer, WhitelistCustomer)
        .join(
            WhitelistCustomer,
            WhitelistCustomer.customer_id == Customer.id,
        )
        .where(
            Customer.shop_id == shop_id,
            Customer.is_active.is_(True),
            WhitelistCustomer.is_active.is_(True),
            or_(
                Customer.phone == search,
                Customer.customer_code == search,
                WhitelistCustomer.owner_code == search,
            ),
        )
    )

    row = result.first()

    if row is None:
        return None, None

    return row[0], row[1]


async def is_vip_customer(
    db: AsyncSession,
    shop_id: UUID,
    customer_id: UUID,
) -> bool:
    result = await db.execute(
        select(WhitelistCustomer.id).where(
            WhitelistCustomer.shop_id == shop_id,
            WhitelistCustomer.customer_id == customer_id,
            WhitelistCustomer.is_active.is_(True),
        )
    )

    return result.scalar_one_or_none() is not None
