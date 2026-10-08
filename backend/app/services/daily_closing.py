from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Product
from app.models.daily_closing import DailyClosing
from app.models.expense import Expense
from app.models.purchase import Purchase
from app.models.return_model import SaleReturn
from app.models.sale import Sale


async def build_daily_summary(
    db: AsyncSession,
    shop_id: int,
    target_date: date,
):
    start = datetime.combine(
        target_date,
        datetime.min.time(),
    )

    end = start + timedelta(days=1)

    sales = await db.scalar(
        select(
            func.coalesce(
                func.sum(Sale.total_amount),
                0,
            )
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
            Sale.status.in_(
                ["completed", "credit"]
            ),
        )
    )

    purchases = await db.scalar(
        select(
            func.coalesce(
                func.sum(Purchase.total_amount),
                0,
            )
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.created_at >= start,
            Purchase.created_at < end,
        )
    )

    expenses = await db.scalar(
        select(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        ).where(
            Expense.shop_id == shop_id,
            Expense.expense_date >= start,
            Expense.expense_date < end,
        )
    )

    returns = await db.scalar(
        select(
            func.coalesce(
                func.sum(SaleReturn.total_amount),
                0,
            )
        ).where(
            SaleReturn.shop_id == shop_id,
            SaleReturn.created_at >= start,
            SaleReturn.created_at < end,
        )
    )

    clients = await db.scalar(
        select(
            func.count(
                func.distinct(Sale.customer_id)
            )
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
            Sale.customer_id.is_not(None),
        )
    )

    stock_value = await db.scalar(
        select(
            func.coalesce(
                func.sum(
                    Product.current_stock
                    * Product.purchase_price
                ),
                0,
            )
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
        )
    )

    sales_value = Decimal(str(sales or 0))
    purchase_value = Decimal(str(purchases or 0))
    expense_value = Decimal(str(expenses or 0))
    return_value = Decimal(str(returns or 0))

    profit = (
        sales_value
        - purchase_value
        - expense_value
        - return_value
    )

    return {
        "date": target_date,
        "total_sale": sales_value,
        "total_clients": int(clients or 0),
        "total_profit": profit,
        "total_purchase": purchase_value,
        "stock_value": Decimal(
            str(stock_value or 0)
        ),
        "total_expenses": expense_value,
        "total_returns": return_value,
    }


async def close_daily_day(
    db: AsyncSession,
    shop_id: int,
    user_id: int | None,
    target_date: date,
    opening_cash: Decimal = Decimal("0"),
    closing_cash: Decimal = Decimal("0"),
    register_id: int | None = None,
    notes: str | None = None,
):
    existing = await db.scalar(
        select(DailyClosing).where(
            DailyClosing.shop_id == shop_id,
            DailyClosing.closing_date == target_date,
        )
    )

    if existing:
        raise ValueError(
            "This day has already been closed."
        )

    summary = await build_daily_summary(
        db,
        shop_id,
        target_date,
    )

    closing = DailyClosing(
        shop_id=shop_id,
        register_id=register_id,
        closed_by=user_id,
        closing_date=target_date,
        total_sales=summary["total_sale"],
        total_purchases=summary["total_purchase"],
        total_profit=summary["total_profit"],
        total_expenses=summary["total_expenses"],
        total_returns=summary["total_returns"],
        total_clients=summary["total_clients"],
        stock_value=summary["stock_value"],
        opening_cash=opening_cash,
        closing_cash=closing_cash,
        cash_difference=(
            closing_cash - opening_cash
        ),
        status="closed",
        notes=notes,
    )

    db.add(closing)

    await db.commit()
    await db.refresh(closing)

    return closing


async def get_daily_closing(
    db: AsyncSession,
    shop_id: int,
    target_date: date,
):
    return await db.scalar(
        select(DailyClosing).where(
            DailyClosing.shop_id == shop_id,
            DailyClosing.closing_date == target_date,
        )
    )
