from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class DailyClosingResponse(BaseModel):
    id: int
    closing_date: date
    total_sales: Decimal
    total_purchases: Decimal
    total_profit: Decimal
    total_expenses: Decimal
    total_returns: Decimal
    total_clients: int
    stock_value: Decimal
    opening_cash: Decimal
    closing_cash: Decimal
    cash_difference: Decimal
    status: str
    report_path: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
