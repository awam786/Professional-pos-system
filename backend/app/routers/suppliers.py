from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.services.supplier import (
    create_supplier,
    get_supplier,
    list_suppliers,
    supplier_statement,
)


router = APIRouter(
    prefix="/api/suppliers",
    tags=["Suppliers"],
)


async def current_shop_id() -> int:
    return 1


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_supplier(
    data: SupplierCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_supplier(
            db=db,
            shop_id=await current_shop_id(),
            data=data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[SupplierResponse],
)
async def get_suppliers(
    search: str | None = Query(
        default=None
    ),
    db: AsyncSession = Depends(get_db),
):
    return await list_suppliers(
        db=db,
        shop_id=await current_shop_id(),
        search=search,
    )


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
async def get_supplier_by_id(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
):
    supplier = await get_supplier(
        db=db,
        shop_id=await current_shop_id(),
        supplier_id=supplier_id,
    )

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found.",
        )

    return supplier


@router.get(
    "/{supplier_id}/statement",
)
async def get_supplier_statement(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await supplier_statement(
            db=db,
            shop_id=await current_shop_id(),
            supplier_id=supplier_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
