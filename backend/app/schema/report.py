from datetime import date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


class ReportFilter(BaseModel):
    start_date: date
    end_date: date


class SalesReport(BaseModel):
    start_date: date
    end_date: date
    total_sales: Decimal
    total_paid: Decimal
    total_credit: Decimal
    total_discount: Decimal
    total_returns: Decimal
    total_transactions: int
    total_clients: int
    total_profit: Decimal


class PurchaseReport(BaseModel):
    start_date: date
    end_date: date
    total_purchases: Decimal
    total_paid: Decimal
    total_payable: Decimal
    total_transactions: int


class InventoryReport(BaseModel):
    total_products: int
    total_stock_quantity: Decimal
    total_stock_cost_value: Decimal
    total_stock_selling_value: Decimal
    low_stock_products: int
    out_of_stock_products: int


class DailySummary(BaseModel):
    date: date
    total_sale: Decimal
    total_clients: int
    total_profit: Decimal
    total_purchase: Decimal
    stock_value: Decimal
    total_expenses: Decimal
    total_returns: Decimal


class ExportResponse(BaseModel):
    report_type: str
    export_format: str
    file_name: str
    content_type: str
    data: Any
    file_path: Optional[str] = None
