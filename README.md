# Professional POS System

A production-ready General Store Point of Sale (POS) system designed for Pakistan-based retail businesses.

## Core Features

- Professional dark POS interface
- PKR currency
- Asia/Karachi timezone
- PostgreSQL database
- Product and inventory management
- Barcode and QR scanning
- Customers and VIP/Whitelist customers
- Sales and purchases
- Supplier management
- Customer credit
- Supplier payable accounts
- Cash register
- Expenses
- Returns and refunds
- Daily closing
- Profit and inventory reports
- PDF, CSV and Excel exports
- Receipt printing
- User roles and permissions
- Audit logging
- Offline-capable PWA workflow
- Railway PostgreSQL support
- Multi-shop data isolation

## Technology

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT authentication
- Uvicorn

### Frontend

- React
- TypeScript
- Vite
- PWA
- IndexedDB

## Currency

PKR

## Timezone

Asia/Karachi

## Development

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
