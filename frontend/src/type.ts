export interface Product {
  id: number;
  name: string;
  sku?: string;
  selling_price: number;
  purchase_price: number;
  current_stock: number;
  min_stock: number;
  unit?: string;
  is_active: boolean;
}

export interface Customer {
  id: number;
  name: string;
  phone?: string;
  customer_code?: string;
  current_balance?: number;
  is_active: boolean;
}

export interface SaleItem {
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  discount: number;
  total: number;
}

export interface CartItem {
  product: Product;
  quantity: number;
  discount: number;
}

export interface DashboardData {
  total_sales: number;
  total_purchases: number;
  total_profit: number;
  stock_value: number;
  total_customers: number;
  low_stock_products: number;
  today_transactions: number;
}

export interface DailySummary {
  date: string;
  total_sale: number;
  total_clients: number;
  total_profit: number;
  total_purchase: number;
  stock_value: number;
  total_expenses: number;
  total_returns: number;
}
