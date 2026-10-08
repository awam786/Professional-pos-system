import {
  useEffect,
  useState,
} from "react";

import {
  ArrowDownRight,
  ArrowUpRight,
  Box,
  CreditCard,
  DollarSign,
  Package,
  ShoppingCart,
  Users,
} from "lucide-react";

import { api } from "../api/client";
import type {
  DashboardData,
} from "../types";

function money(value: number) {
  return `PKR ${Number(value || 0).toLocaleString(
    "en-PK",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  )}`;
}

export default function Dashboard() {
  const [
    data,
    setData,
  ] = useState<DashboardData>({
    total_sales: 0,
    total_purchases: 0,
    total_profit: 0,
    stock_value: 0,
    total_customers: 0,
    low_stock_products: 0,
    today_transactions: 0,
  });

  useEffect(() => {
    const load =
      async () => {
        try {
          const today =
            new Date()
              .toISOString()
              .slice(0, 10);

          const [sales, purchases, inventory] =
            await Promise.all([
              api.get<any>(
                `/reports/sales?start_date=${today}&end_date=${today}`,
              ),
              api.get<any>(
                `/reports/purchases?start_date=${today}&end_date=${today}`,
              ),
              api.get<any>(
                `/reports/inventory`,
                "inventory-report",
              ),
            ]);

          setData({
            total_sales:
              sales.total_sales || 0,

            total_purchases:
              purchases.total_purchases ||
              0,

            total_profit:
              sales.total_profit || 0,

            stock_value:
              inventory.total_stock_cost_value ||
              0,

            total_customers:
              sales.total_clients || 0,

            low_stock_products:
              inventory.low_stock_products ||
              0,

            today_transactions:
              sales.total_transactions ||
              0,
          });
        } catch {
          // Offline mode may not have report data yet.
        }
      };

    void load();
  }, []);

  const cards = [
    {
      title: "Today's Sales",
      value: money(data.total_sales),
      icon: DollarSign,
      trend: "Sales today",
      positive: true,
    },
    {
      title: "Today's Profit",
      value: money(data.total_profit),
      icon: ArrowUpRight,
      trend: "Estimated net profit",
      positive: true,
    },
    {
      title: "Today's Purchases",
      value: money(data.total_purchases),
      icon: CreditCard,
      trend: "Purchase value",
      positive: false,
    },
    {
      title: "Stock Value",
      value: money(data.stock_value),
      icon: Package,
      trend: "Current cost value",
      positive: true,
    },
  ];

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <h1>Good morning, Administrator</h1>
          <p>
            Here's your store overview for today.
          </p>
        </div>

        <div className="date-badge">
          {new Date().toLocaleDateString(
            "en-PK",
            {
              weekday: "long",
              day: "2-digit",
              month: "long",
              year: "numeric",
            },
          )}
        </div>
      </div>

      <div className="stat-grid">
        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div
              className="stat-card"
              key={card.title}
            >
              <div className="stat-card-top">
                <div className="stat-icon">
                  <Icon size={20} />
                </div>

                {card.positive ? (
                  <ArrowUpRight
                    size={16}
                  />
                ) : (
                  <ArrowDownRight
                    size={16}
                  />
                )}
              </div>

              <span className="stat-label">
                {card.title}
              </span>

              <strong className="stat-value">
                {card.value}
              </strong>

              <span className="stat-description">
                {card.trend}
              </span>
            </div>
          );
        })}
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Today's Activity</h2>
              <p>
                Quick operational overview
              </p>
            </div>
          </div>

          <div className="activity-grid">
            <div className="activity-item">
              <ShoppingCart size={20} />
              <strong>
                {data.today_transactions}
              </strong>
              <span>Transactions</span>
            </div>

            <div className="activity-item">
              <Users size={20} />
              <strong>
                {data.total_customers}
              </strong>
              <span>Customers</span>
            </div>

            <div className="activity-item warning">
              <Box size={20} />
              <strong>
                {data.low_stock_products}
              </strong>
              <span>Low Stock</span>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Quick Actions</h2>
              <p>
                Common tasks
              </p>
            </div>
          </div>

          <div className="quick-actions">
            <button
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent(
                    "open-pos",
                  ),
                )
              }
            >
              <ShoppingCart size={19} />
              New Sale
            </button>

            <button>
              <Package size={19} />
              Add Product
            </button>

            <button>
              <Users size={19} />
              Add Customer
            </button>

            <button>
              <CreditCard size={19} />
              Cash Register
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}
