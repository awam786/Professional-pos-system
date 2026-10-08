import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  BarChart3,
  Boxes,
  Calculator,
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  CreditCard,
  FileBarChart,
  LayoutDashboard,
  Menu,
  Package,
  Settings,
  ShoppingCart,
  Store,
  Users,
  WalletCards,
  X,
} from "lucide-react";

import OfflineIndicator from "./components/OfflineIndicator";
import SyncStatus from "./components/SyncStatus";

import Dashboard from "./pages/Dashboard";
import POS from "./pages/POS";
import Products from "./pages/Products";
import Customers from "./pages/Customers";
import Reports from "./pages/Reports";
import DailyClosing from "./pages/DailyClosing";
import SettingsPage from "./pages/Settings";

import { startSyncEngine } from "./offline/sync";

type Page =
  | "dashboard"
  | "pos"
  | "products"
  | "customers"
  | "reports"
  | "closing"
  | "settings";

const navigation: {
  id: Page;
  label: string;
  icon: typeof LayoutDashboard;
}[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    id: "pos",
    label: "Point of Sale",
    icon: ShoppingCart,
  },
  {
    id: "products",
    label: "Products & Stock",
    icon: Package,
  },
  {
    id: "customers",
    label: "Customers",
    icon: Users,
  },
  {
    id: "reports",
    label: "Reports",
    icon: BarChart3,
  },
  {
    id: "closing",
    label: "Daily Closing",
    icon: WalletCards,
  },
  {
    id: "settings",
    label: "Settings",
    icon: Settings,
  },
];

function App() {
  const [page, setPage] =
    useState<Page>("dashboard");

  const [
    sidebarCollapsed,
    setSidebarCollapsed,
  ] = useState(false);

  const [
    mobileMenu,
    setMobileMenu,
  ] = useState(false);

  useEffect(() => {
    const stop =
      startSyncEngine();

    return stop;
  }, []);

  const content = useMemo(() => {
    switch (page) {
      case "pos":
        return <POS />;

      case "products":
        return <Products />;

      case "customers":
        return <Customers />;

      case "reports":
        return <Reports />;

      case "closing":
        return <DailyClosing />;

      case "settings":
        return <SettingsPage />;

      default:
        return <Dashboard />;
    }
  }, [page]);

  return (
    <div className="app-shell">
      <aside
        className={[
          "sidebar",
          sidebarCollapsed
            ? "sidebar-collapsed"
            : "",
          mobileMenu
            ? "sidebar-mobile-open"
            : "",
        ].join(" ")}
      >
        <div className="brand">
          <div className="brand-mark">
            <Store size={21} />
          </div>

          {!sidebarCollapsed && (
            <div>
              <strong>GENERAL POS</strong>
              <span>Professional Edition</span>
            </div>
          )}

          <button
            className="mobile-close"
            onClick={() =>
              setMobileMenu(false)
            }
          >
            <X size={20} />
          </button>
        </div>

        <nav className="main-nav">
          <div className="nav-section-title">
            OPERATIONS
          </div>

          {navigation
            .slice(0, 4)
            .map((item) => {
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  className={
                    page === item.id
                      ? "nav-item active"
                      : "nav-item"
                  }
                  onClick={() => {
                    setPage(item.id);
                    setMobileMenu(false);
                  }}
                  title={item.label}
                >
                  <Icon size={19} />
                  {!sidebarCollapsed && (
                    <span>
                      {item.label}
                    </span>
                  )}
                </button>
              );
            })}

          <div className="nav-section-title">
            MANAGEMENT
          </div>

          {navigation
            .slice(4)
            .map((item) => {
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  className={
                    page === item.id
                      ? "nav-item active"
                      : "nav-item"
                  }
                  onClick={() => {
                    setPage(item.id);
                    setMobileMenu(false);
                  }}
                  title={item.label}
                >
                  <Icon size={19} />
                  {!sidebarCollapsed && (
                    <span>
                      {item.label}
                    </span>
                  )}
                </button>
              );
            })}
        </nav>

        <div className="sidebar-bottom">
          <div className="register-mini">
            <Calculator size={17} />

            {!sidebarCollapsed && (
              <div>
                <span>Register</span>
                <strong>Ready</strong>
              </div>
            )}
          </div>

          <button
            className="collapse-button"
            onClick={() =>
              setSidebarCollapsed(
                (value) => !value,
              )
            }
          >
            {sidebarCollapsed ? (
              <ChevronRight size={18} />
            ) : (
              <ChevronLeft size={18} />
            )}

            {!sidebarCollapsed && (
              <span>Collapse menu</span>
            )}
          </button>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button
            className="mobile-menu-button"
            onClick={() =>
              setMobileMenu(true)
            }
          >
            <Menu size={21} />
          </button>

          <div className="breadcrumb">
            <span>POS</span>
            <ChevronRight size={14} />
            <strong>
              {
                navigation.find(
                  (item) =>
                    item.id === page,
                )?.label
              }
            </strong>
          </div>

          <div className="topbar-actions">
            <SyncStatus />

            <div className="user-chip">
              <div className="user-avatar">
                A
              </div>

              <div>
                <strong>Administrator</strong>
                <span>Owner</span>
              </div>
            </div>
          </div>
        </header>

        <section className="page-content">
          {content}
        </section>
      </main>

      <OfflineIndicator />
    </div>
  );
}

export default App;
