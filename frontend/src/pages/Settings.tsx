import {
  useState,
} from "react";

import {
  Building2,
  Database,
  Save,
  ShieldCheck,
} from "lucide-react";

export default function SettingsPage() {
  const [
    shopName,
    setShopName,
  ] = useState(
    localStorage.getItem(
      "pos_shop_name",
    ) ||
      "My General Store",
  );

  const [
    phone,
    setPhone,
  ] = useState(
    localStorage.getItem(
      "pos_shop_phone",
    ) || "",
  );

  const [
    address,
    setAddress,
  ] = useState(
    localStorage.getItem(
      "pos_shop_address",
    ) || "",
  );

  function save() {
    localStorage.setItem(
      "pos_shop_name",
      shopName,
    );

    localStorage.setItem(
      "pos_shop_phone",
      phone,
    );

    localStorage.setItem(
      "pos_shop_address",
      address,
    );

    alert(
      "Shop settings saved.",
    );
  }

  return (
    <div>
      <div className="page-heading">
        <div>
          <h1>Settings</h1>
          <p>
            Configure your store and POS environment.
          </p>
        </div>
      </div>

      <div className="settings-grid">
        <section className="panel settings-section">
          <div className="settings-title">
            <Building2 size={19} />
            <div>
              <h2>Shop Information</h2>
              <p>
                Details shown on receipts.
              </p>
            </div>
          </div>

          <label>
            Shop Name
            <input
              value={shopName}
              onChange={(event) =>
                setShopName(
                  event.target.value,
                )
              }
            />
          </label>

          <label>
            Phone
            <input
              value={phone}
              onChange={(event) =>
                setPhone(
                  event.target.value,
                )
              }
            />
          </label>

          <label>
            Address
            <textarea
              value={address}
              onChange={(event) =>
                setAddress(
                  event.target.value,
                )
              }
            />
          </label>

          <button
            className="primary-button"
            onClick={save}
          >
            <Save size={17} />
            Save Settings
          </button>
        </section>

        <section className="panel settings-section">
          <div className="settings-title">
            <Database size={19} />
            <div>
              <h2>System</h2>
              <p>
                POS environment information.
              </p>
            </div>
          </div>

          <div className="setting-row">
            <span>Currency</span>
            <strong>PKR</strong>
          </div>

          <div className="setting-row">
            <span>Timezone</span>
            <strong>
              Asia/Karachi
            </strong>
          </div>

          <div className="setting-row">
            <span>Tax System</span>
            <strong>Disabled</strong>
          </div>

          <div className="setting-row">
            <span>Offline Mode</span>
            <strong className="text-success">
              Enabled
            </strong>
          </div>
        </section>

        <section className="panel settings-section">
          <div className="settings-title">
            <ShieldCheck size={19} />
            <div>
              <h2>Security</h2>
              <p>
                Account and permission controls.
              </p>
            </div>
          </div>

          <div className="setting-row">
            <span>Current Role</span>
            <strong>Owner</strong>
          </div>

          <div className="setting-row">
            <span>Audit Logging</span>
            <strong className="text-success">
              Enabled
            </strong>
          </div>

          <div className="setting-row">
            <span>Database</span>
            <strong>
              Railway PostgreSQL
            </strong>
          </div>
        </section>
      </div>
    </div>
  );
}
