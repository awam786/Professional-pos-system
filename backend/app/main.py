from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_database

from app.routers.catalog import router as catalog_router
from app.routers.inventory import router as inventory_router
from app.routers.customers import router as customers_router
from app.routers.pos import router as pos_router

from app.routers.sales import router as sales_router
from app.routers.payments import router as payments_router
from app.routers.returns import router as returns_router
from app.routers.receipts import router as receipts_router

from app.routers.purchases import router as purchases_router
from app.routers.suppliers import router as suppliers_router

from app.routers.cash_register import (
    router as cash_register_router,
)

from app.routers.daily_closing import (
    router as daily_closing_router,
)

from app.routers.reports import (
    router as reports_router,
)

from app.routers.exports import (
    router as exports_router,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    await init_database()
    yield


app = FastAPI(
    title="Professional General Store POS",
    version="1.0.0",
    description=(
        "Production-ready General Store POS "
        "with inventory, sales, purchases, "
        "reports and offline synchronization."
    ),
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=[
        "*",
    ],
    allow_headers=[
        "*",
    ],
)


app.include_router(
    catalog_router,
)

app.include_router(
    inventory_router,
)

app.include_router(
    customers_router,
)

app.include_router(
    pos_router,
)

app.include_router(
    sales_router,
)

app.include_router(
    payments_router,
)

app.include_router(
    returns_router,
)

app.include_router(
    receipts_router,
)

app.include_router(
    purchases_router,
)

app.include_router(
    suppliers_router,
)

app.include_router(
    cash_register_router,
)

app.include_router(
    daily_closing_router,
)

app.include_router(
    reports_router,
)

app.include_router(
    exports_router,
)


@app.get("/")
async def root():
    return {
        "name":
            "Professional General Store POS",
        "version":
            "1.0.0",
        "status":
            "online",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected",
    }


@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "service":
            "professional-pos",
    }
