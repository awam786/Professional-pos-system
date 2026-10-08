import {
  useState,
} from "react";

import {
  BarChart3,
  Download,
  FileText,
} from "lucide-react";

import { api } from "../api/client";

function today() {
  return new Date()
    .toISOString()
    .slice(0, 10);
}

export default function Reports() {
  const [
    startDate,
    setStartDate,
  ] = useState(today());

  const [
    endDate,
    setEndDate,
  ] = useState(today());

  const [
    report,
    setReport,
  ] = useState<any>(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  async function loadReport() {
    setLoading(true);

    try {
      const data =
        await api.get<any>(
          `/reports/sales?start_date=${startDate}&end_date=${endDate}`,
        );

      setReport(data);
    } finally {
      setLoading(false);
    }
  }

  function downloadCsv() {
    window.open(
      `${
        import.meta.env
          .VITE_API_URL ||
        "http://localhost:8000/api"
      }/exports/sales.csv?start_date=${startDate}&end_date=${endDate}`,
      "_blank",
    );
  }

  return (
    <div>
      <div className="page-heading">
        <div>
          <h1>Reports</h1>
          <p>
            Analyze sales, profit and transactions.
          </p>
        </div>
      </div>

      <div className="panel report-controls">
        <div>
          <label>From</label>
          <input
            type="date"
            value={startDate}
            onChange={(event) =>
              setStartDate(
                event.target.value,
              )
            }
          />
        </div>

        <div>
          <label>To</label>
          <input
            type="date"
            value={endDate}
            onChange={(event) =>
              setEndDate(
                event.target.value,
              )
            }
          />
        </div>

        <button
          className="primary-button"
          onClick={() =>
            void loadReport()
          }
        >
          <BarChart3 size={17} />
          {loading
            ? "Loading..."
            : "Generate Report"}
        </button>

        <button
          className="secondary-button"
          onClick={downloadCsv}
        >
          <Download size={17} />
          CSV
        </button>
      </div>

      {report && (
        <div className="report-grid">
          <ReportCard
            title="Total Sales"
            value={report.total_sales}
          />

          <ReportCard
            title="Total Profit"
            value={report.total_profit}
          />

          <ReportCard
            title="Transactions"
            value={
              report.total_transactions
            }
            plain
          />

          <ReportCard
            title="Customers"
            value={
              report.total_clients
            }
            plain
          />

          <ReportCard
            title="Discount"
            value={
              report.total_discount
            }
          />

          <ReportCard
            title="Returns"
            value={
              report.total_returns
            }
          />
        </div>
      )}

      {!report && (
        <div className="empty-report panel">
          <FileText size={40} />
          <strong>
            No report generated
          </strong>
          <span>
            Select your date range and
            generate a report.
          </span>
        </div>
      )}
    </div>
  );
}

function ReportCard({
  title,
  value,
  plain = false,
}: {
  title: string;
  value: number;
  plain?: boolean;
}) {
  return (
    <div className="report-card">
      <span>{title}</span>

      <strong>
        {plain
          ? Number(
              value || 0,
            ).toLocaleString()
          : `PKR ${Number(
              value || 0,
            ).toLocaleString(
              "en-PK",
              {
                minimumFractionDigits: 2,
              },
            )}`}
      </strong>
    </div>
  );
}
