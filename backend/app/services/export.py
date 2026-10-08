import csv
import io
from datetime import date
from decimal import Decimal


def decimal_to_string(value):
    if isinstance(value, Decimal):
        return f"{value:.2f}"

    return str(value)


def report_to_csv(
    report: dict,
):
    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(
        ["Field", "Value"]
    )

    for key, value in report.items():
        if isinstance(value, (list, dict)):
            value = str(value)

        writer.writerow(
            [
                key.replace("_", " ").title(),
                decimal_to_string(value),
            ]
        )

    return output.getvalue()


def daily_summary_to_csv(
    rows: list[dict],
):
    output = io.StringIO()

    if not rows:
        return ""

    fieldnames = list(rows[0].keys())

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for row in rows:
        writer.writerow(
            {
                key: decimal_to_string(
                    value
                )
                for key, value in row.items()
            }
        )

    return output.getvalue()


def build_excel_rows(
    report: dict,
):
    rows = []

    for key, value in report.items():
        rows.append(
            {
                "Field": key.replace(
                    "_",
                    " ",
                ).title(),
                "Value": decimal_to_string(
                    value
                ),
            }
        )

    return rows
