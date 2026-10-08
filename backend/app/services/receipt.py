from decimal import Decimal


def build_receipt_data(sale):
    items = []

    for item in sale.items:
        items.append(
            {
                "name": item.product_name,
                "sku": item.sku,
                "quantity": str(item.quantity),
                "unit_price": str(item.unit_price),
                "discount": str(item.discount_amount),
                "total": str(item.total_amount),
            }
        )

    return {
        "invoice_number": sale.invoice_number,
        "created_at": sale.created_at,
        "customer_id": sale.customer_id,
        "is_vip": sale.is_vip,
        "stars": sale.receipt_stars,
        "subtotal": str(
            Decimal(str(sale.subtotal))
        ),
        "discount": str(
            Decimal(str(sale.discount_amount))
        ),
        "discount_label": sale.discount_label,
        "total": str(
            Decimal(str(sale.total_amount))
        ),
        "paid": str(
            Decimal(str(sale.paid_amount))
        ),
        "credit": str(
            Decimal(str(sale.credit_amount))
        ),
        "change": str(
            Decimal(str(sale.change_amount))
        ),
        "items": items,
    }
