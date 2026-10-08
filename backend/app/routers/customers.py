from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Shop
from app.models.customer import (
    Customer,
    WhitelistCustomer,
)
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    VIPCustomerResponse,
    WhitelistCreate,
    WhitelistResponse,
    WhitelistUpdate,
)
from app.services.customer import get_vip_customer

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


async def get_default_shop_id(
    db: AsyncSession,
) -> UUID:
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
    "",
    response_model=CustomerResponse,
)
async def create_customer(
    payload: CustomerCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    if payload.customer_code:
        existing = await db.execute(
            select(Customer.id).where(
                Customer.shop_id == shop_id,
                Customer.customer_code
                == payload.customer_code,
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="Customer code already exists",
            )

    customer = Customer(
        shop_id=shop_id,
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        address=payload.address,
        customer_code=payload.customer_code,
        credit_limit=payload.credit_limit,
        notes=payload.notes,
    )

    db.add(customer)

    await db.commit()
    await db.refresh(customer)

    return customer


@router.get(
    "",
    response_model=list[CustomerResponse],
)
async def list_customers(
    search: str | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    query = select(Customer).where(
        Customer.shop_id == shop_id,
    )

    if active_only:
        query = query.where(
            Customer.is_active.is_(True)
        )

    if search:
        query = query.where(
            or_(
                Customer.name.ilike(
                    f"%{search}%"
                ),
                Customer.phone.ilike(
                    f"%{search}%"
                ),
                Customer.customer_code.ilike(
                    f"%{search}%"
                ),
            )
        )

    query = query.order_by(Customer.name)

    result = await db.execute(query)

    return result.scalars().all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.shop_id == shop_id,
        )
    )

    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.shop_id == shop_id,
        )
    )

    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    data = payload.model_dump(
        exclude_unset=True,
    )

    if "customer_code" in data:
        existing = await db.execute(
            select(Customer.id).where(
                Customer.shop_id == shop_id,
                Customer.customer_code
                == data["customer_code"],
                Customer.id != customer_id,
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="Customer code already exists",
            )

    for key, value in data.items():
        setattr(customer, key, value)

    await db.commit()
    await db.refresh(customer)

    return customer


@router.post(
    "/whitelist",
    response_model=WhitelistResponse,
)
async def add_whitelist_customer(
    payload: WhitelistCreate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    customer_result = await db.execute(
        select(Customer).where(
            Customer.id == payload.customer_id,
            Customer.shop_id == shop_id,
        )
    )

    customer = customer_result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    existing = await db.execute(
        select(WhitelistCustomer).where(
            WhitelistCustomer.customer_id
            == payload.customer_id,
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Customer is already on whitelist",
        )

    code_exists = await db.execute(
        select(WhitelistCustomer.id).where(
            WhitelistCustomer.shop_id == shop_id,
            WhitelistCustomer.owner_code
            == payload.owner_code,
        )
    )

    if code_exists.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Owner code already exists",
        )

    whitelist = WhitelistCustomer(
        shop_id=shop_id,
        customer_id=payload.customer_id,
        owner_code=payload.owner_code,
    )

    db.add(whitelist)

    await db.commit()
    await db.refresh(whitelist)

    return whitelist


@router.get(
    "/whitelist/all",
    response_model=list[WhitelistResponse],
)
async def list_whitelist_customers(
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(WhitelistCustomer)
        .where(
            WhitelistCustomer.shop_id == shop_id
        )
        .order_by(
            WhitelistCustomer.created_at.desc()
        )
    )

    return result.scalars().all()


@router.patch(
    "/whitelist/{whitelist_id}",
    response_model=WhitelistResponse,
)
async def update_whitelist_customer(
    whitelist_id: UUID,
    payload: WhitelistUpdate,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    result = await db.execute(
        select(WhitelistCustomer).where(
            WhitelistCustomer.id == whitelist_id,
            WhitelistCustomer.shop_id == shop_id,
        )
    )

    whitelist = result.scalar_one_or_none()

    if whitelist is None:
        raise HTTPException(
            status_code=404,
            detail="Whitelist customer not found",
        )

    data = payload.model_dump(
        exclude_unset=True,
    )

    if "owner_code" in data:
        existing = await db.execute(
            select(WhitelistCustomer.id).where(
                WhitelistCustomer.shop_id == shop_id,
                WhitelistCustomer.owner_code
                == data["owner_code"],
                WhitelistCustomer.id
                != whitelist_id,
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="Owner code already exists",
            )

    for key, value in data.items():
        setattr(whitelist, key, value)

    await db.commit()
    await db.refresh(whitelist)

    return whitelist


@router.get(
    "/vip/lookup/{search}",
    response_model=VIPCustomerResponse,
)
async def lookup_vip_customer(
    search: str,
    db: AsyncSession = Depends(get_db),
):
    shop_id = await get_default_shop_id(db)

    customer, whitelist = await get_vip_customer(
        db,
        shop_id,
        search,
    )

    if customer is None or whitelist is None:
        raise HTTPException(
            status_code=404,
            detail="VIP customer not found",
        )

    return VIPCustomerResponse(
        is_vip=True,
        customer_id=customer.id,
        name=customer.name,
        phone=customer.phone,
        customer_code=customer.customer_code,
        owner_code=whitelist.owner_code,
        status="Active",
    )
