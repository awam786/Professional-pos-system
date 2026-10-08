from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Product
from app.models.expense import Expense
from app.models.purchase import Purchase
from app.models.return_model import SaleReturn
from app.models.sale import Sale, SaleItem


async def sales_report(
    db: AsyncSession,
    shop_id: int,
    start_date: date,
    end_date: date,
):
    start = datetime.combine(
        start_date,
        datetime.min.time(),
    )

    end = datetime.combine(
        end_date + timedelta(days=1),
        datetime.min.time(),
    )

    total_sales = await db.scalar(
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

    total_paid = await db.scalar(
        select(
            func.coalesce(
                func.sum(Sale.paid_amount),
                0,
            )
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
        )
    )

    total_credit = await db.scalar(
        select(
            func.coalesce(
                func.sum(Sale.credit_amount),
                0,
            )
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
        )
    )

    total_discount = await db.scalar(
        select(
            func.coalesce(
                func.sum(Sale.discount_amount),
                0,
            )
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
        )
    )

    total_returns = await db.scalar(
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

    transactions = await db.scalar(
        select(
            func.count(Sale.id)
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
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

    cost = await db.scalar(
        select(
            func.coalesce(
                func.sum(
                    SaleItem.quantity
                    * SaleItem.cost_price
                ),
                0,
            )
        ).join(
            Sale,
            Sale.id == SaleItem.sale_id,
        ).where(
            Sale.shop_id == shop_id,
            Sale.created_at >= start,
            Sale.created_at < end,
        )
    )

    sales_value = Decimal(str(total_sales or 0))
    cost_value = Decimal(str(cost or 0))
    returns_value = Decimal(
        str(total_returns or 0)
    )

    profit = (
        sales_value
        - cost_value
        - returns_value
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": sales_value,
        "total_paid": Decimal(
            str(total_paid or 0)
        ),
        "total_credit": Decimal(
            str(total_credit or 0)
        ),
        "total_discount": Decimal(
            str(total_discount or 0)
        ),
        "total_returns": returns_value,
        "total_transactions": int(
            transactions or 0
        ),
        "total_clients": int(
            clients or 0
        ),
        "total_profit": profit,
    }


async def purchase_report(
    db: AsyncSession,
    shop_id: int,
    start_date: date,
    end_date: date,
):
    start = datetime.combine(
        start_date,
        datetime.min.time(),
    )

    end = datetime.combine(
        end_date + timedelta(days=1),
        datetime.min.time(),
    )

    total = await db.scalar(
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

    paid = await db.scalar(
        select(
            func.coalesce(
                func.sum(Purchase.paid_amount),
                0,
            )
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.created_at >= start,
            Purchase.created_at < end,
        )
    )

    payable = await db.scalar(
        select(
            func.coalesce(
                func.sum(Purchase.payable_amount),
                0,
            )
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.created_at >= start,
            Purchase.created_at < end,
        )
    )

    transactions = await db.scalar(
        select(
            func.count(Purchase.id)
        ).where(
            Purchase.shop_id == shop_id,
            Purchase.created_at >= start,
            Purchase.created_at < end,
        )
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_purchases": Decimal(
            str(total or 0)
        ),
        "total_paid": Decimal(
            str(paid or 0)
        ),
        "total_payable": Decimal(
            str(payable or 0)
        ),
        "total_transactions": int(
            transactions or 0
        ),
    }


async def inventory_report(
    db: AsyncSession,
    shop_id: int,
):
    total_products = await db.scalar(
        select(
            func.count(Product.id)
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
        )
    )

    total_quantity = await db.scalar(
        select(
            func.coalesce(
                func.sum(Product.current_stock),
                0,
            )
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
        )
    )

    cost_value = await db.scalar(
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

    selling_value = await db.scalar(
        select(
            func.coalesce(
                func.sum(
                    Product.current_stock
                    * Product.selling_price
                ),
                0,
            )
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
        )
    )

    low_stock = await db.scalar(
        select(
            func.count(Product.id)
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
            Product.current_stock
            <= Product.min_stock,
            Product.current_stock > 0,
        )
    )

    out_of_stock = await db.scalar(
        select(
            func.count(Product.id)
        ).where(
            Product.shop_id == shop_id,
            Product.is_active.is_(True),
            Product.current_stock <= 0,
        )
    )

    return {
        "total_products": int(
            total_products or 0
        ),
        "total_stock_quantity": Decimal(
            str(total_quantity or 0)
        ),
        "total_stock_cost_value": Decimal(
            str(cost_value or 0)
        ),
        "total_stock_selling_value": Decimal(
            str(selling_value or 0)
        ),
        "low_stock_products": int(
            low_stock or 0
        ),
        "out_of_stock_products": int(
            out_of_stock or 0
        ),
    }
