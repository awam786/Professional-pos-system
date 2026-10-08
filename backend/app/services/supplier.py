from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.purchase import Purchase
from app.models.supplier import Supplier


async def create_supplier(
    db: AsyncSession,
    shop_id: int,
    data,
) -> Supplier:
    if data.supplier_code:
        existing = await db.scalar(
            select(Supplier).where(
                Supplier.shop_id == shop_id,
                Supplier.supplier_code
                == data.supplier_code,
            )
        )

        if existing:
            raise ValueError(
                "Supplier code already exists."
            )

    supplier = Supplier(
        shop_id=shop_id,
        name=data.name.strip(),
        phone=data.phone,
        email=data.email,
        company=data.company,
        address=data.address,
        supplier_code=data.supplier_code,
        opening_balance=data.opening_balance,
        current_balance=data.opening_balance,
        notes=data.notes,
        is_active=True,
    )

    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)

    return supplier


async def list_suppliers(
    db: AsyncSession,
    shop_id: int,
    search: str | None = None,
):
    query = select(Supplier).where(
        Supplier.shop_id == shop_id
    )

    if search:
        term = f"%{search.strip()}%"

        query = query.where(
            or_(
                Supplier.name.ilike(term),
                Supplier.phone.ilike(term),
                Supplier.company.ilike(term),
                Supplier.supplier_code.ilike(term),
            )
        )

    query = query.order_by(
        Supplier.name.asc()
    )

    result = await db.scalars(query)

    return list(result.all())


async def get_supplier(
    db: AsyncSession,
    shop_id: int,
    supplier_id: int,
):
    return await db.scalar(
        select(Supplier).where(
            Supplier.id == supplier_id,
            Supplier.shop_id == shop_id,
        )
    )


async def supplier_statement(
    db: AsyncSession,
    shop_id: int,
    supplier_id: int,
):
    supplier = await get_supplier(
        db,
        shop_id,
        supplier_id,
    )

    if not supplier:
        raise ValueError(
            "Supplier not found."
        )

    purchases_total = await db.scalar(
        select(
            func.coalesce(
                func.sum(Purchase.total_amount),
                0,
            )
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.supplier_id == supplier_id,
        )
    )

    paid_total = await db.scalar(
        select(
            func.coalesce(
                func.sum(Purchase.paid_amount),
                0,
            )
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.supplier_id == supplier_id,
        )
    )

    return {
        "supplier_id": supplier.id,
        "supplier_name": supplier.name,
        "opening_balance": Decimal(
            str(supplier.opening_balance)
        ),
        "purchases": Decimal(
            str(purchases_total or 0)
        ),
        "payments": Decimal(
            str(paid_total or 0)
        ),
        "current_balance": Decimal(
            str(supplier.current_balance)
        ),
    }
