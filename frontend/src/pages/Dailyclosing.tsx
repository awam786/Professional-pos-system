import {
  useState,
} from "react";

import {
  CheckCircle2,
  LockKeyhole,
} from "lucide-react";

import { api } from "../api/client";
import type {
  DailySummary,
} from "../types";

function today() {
  return new Date()
    .toISOString()
    .slice(0, 10);
}

function money(value: number) {
  return `PKR ${Number(value || 0).toLocaleString(
    "en-PK",
    {
      minimumFractionDigits: 2,
    },
  )}`;
}

export default function DailyClosing() {
  const [
    date,
    setDate,
  ] = useState(today());

  const [
    summary,
    setSummary,
  ] = useState<DailySummary | null>(
    null,
  );

  const [
    openingCash,
    setOpeningCash,
  ] = useState(0);

  const [
    closingCash,
    setClosingCash,
  ] = useState(0);

  const [
    closed,
    setClosed,
  ] = useState(false);

  async function loadSummary() {
    try {
      const result =
        await api.get<DailySummary>(
          `/daily-closing/summary?target_date=${date}`,
        );

      setSummary(result);
    } catch {
      setSummary(null);
    }
  }

  async function closeDay() {
    const confirmed =
      window.confirm(
        "Close this business day? Normal transactions for this day should not be changed without authorization.",
      );

    if (!confirmed) {
      return;
    }

    try {
      await api.post(
        `/daily-closing/close?target_date=${date}&opening_cash=${openingCash}&closing_cash=${closingCash}`,
      );

      setClosed(true);
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Daily closing failed.",
      );
    }
  }

  return (
    <div>
      <div className="page-heading">
        <div>
          <h1>Daily Closing</h1>
          <p>
            Finalize the day's sales, purchases,
            profit and cash position.
          </p>
        </div>

        {closed && (
          <div className="closed-badge">
            <CheckCircle2 size={17} />
            Day Closed
          </div>
        )}
      </div>

      <div className="panel closing-controls">
        <div>
          <label>Business Date</label>

          <input
            type="date"
            value={date}
            onChange={(event) => {
              setDate(
                event.target.value,
              );
              setClosed(false);
            }}
          />
        </div>

        <button
          className="primary-button"
          onClick={() =>
            void loadSummary()
          }
        >
          Generate Summary
        </button>
      </div>

      {summary && (
        <>
          <div className="closing-summary">
            <Summary
              label="Today Total Sale"
              value={money(
                summary.total_sale,
              )}
            />

            <Summary
              label="Total Clients"
              value={summary.total_clients.toLocaleString()}
            />

            <Summary
              label="Total Profit"
              value={money(
                summary.total_profit,
              )}
            />

            <Summary
              label="Total Purchase"
              value={money(
                summary.total_purchase,
              )}
            />

            <Summary
              label="Stock Value"
              value={money(
                summary.stock_value,
              )}
            />

            <Summary
              label="Expenses"
              value={money(
                summary.total_expenses,
              )}
            />

            <Summary
              label="Returns"
              value={money(
                summary.total_returns,
              )}
            />
          </div>

          <div className="panel closing-cash">
            <div className="panel-heading">
              <div>
                <h2>
                  <LockKeyhole
                    size={19}
                  />
                  Cash Reconciliation
                </h2>

                <p>
                  Count the physical cash before
                  finalizing the day.
                </p>
              </div>
            </div>

            <div className="cash-grid">
              <div>
                <label>
                  Opening Cash
                </label>

                <input
                  type="number"
                  value={openingCash}
                  onChange={(event) =>
                    setOpeningCash(
                      Number(
                        event.target
                          .value,
                      ),
                    )
                  }
                />
              </div>

              <div>
                <label>
                  Actual Closing Cash
                </label>

                <input
                  type="number"
                  value={closingCash}
                  onChange={(event) =>
                    setClosingCash(
                      Number(
                        event.target
                          .value,
                      ),
                    )
                  }
                />
              </div>

              <div className="cash-difference">
                <span>
                  Difference
                </span>

                <strong>
                  {money(
                    closingCash -
                      openingCash,
                  )}
                </strong>
              </div>
            </div>

            <button
              className="close-day-button"
              onClick={() =>
                void closeDay()
              }
              disabled={closed}
            >
              <LockKeyhole size={17} />
              {closed
                ? "Day Already Closed"
                : "Close & Finalize Day"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

function Summary({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="closing-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
