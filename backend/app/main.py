from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .config import settings
from .database import AsyncSessionLocal, init_database
from .routers import catalog, inventory
from .schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Professional General Store POS API",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    catalog.router,
    prefix=settings.api_prefix,
)

app.include_router(
    inventory.router,
    prefix=settings.api_prefix,
)


@app.get("/", tags=["System"])
async def root():
    return {
        "application": settings.app_name,
        "status": "online",
        "version": "1.0.0",
    }


@app.get(
    f"{settings.api_prefix}/health",
    response_model=HealthResponse,
    tags=["System"],
)
async def health_check():
    database_status = "disconnected"

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return HealthResponse(
        status=(
            "healthy"
            if database_status == "connected"
            else "degraded"
        ),
        database=database_status,
        application=settings.app_name,
    )
