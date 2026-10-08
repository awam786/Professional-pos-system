from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    database: str
    application: str


class ShopCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=50)
    address: Optional[str] = None
    currency: str = Field(default="PKR", max_length=10)
    timezone: str = Field(default="Asia/Karachi", max_length=100)


class ShopResponse(ShopCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    logo_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    shop_id: UUID
    role_id: UUID
    username: str
    full_name: str
    phone: Optional[str]
    is_active: bool
    last_login_at: Optional[datetime]
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class CurrentUserResponse(UserResponse):
    role: str
    shop_name: str
