from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    shop_id: Mapped[int] = mapped_column(
        ForeignKey("shops.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    adjustment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    previous_stock: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    new_stock: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    reference: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
