import {
  useEffect,
  useState,
} from "react";

import {
  Search,
  Star,
  UserPlus,
} from "lucide-react";

import { api } from "../api/client";
import type {
  Customer,
} from "../types";

export default function Customers() {
  const [
    customers,
    setCustomers,
  ] = useState<Customer[]>([]);

  const [
    search,
    setSearch,
  ] = useState("");

  useEffect(() => {
    const load =
      async () => {
        try {
          const result =
            await api.get<any>(
              "/customers",
              "customers",
            );

          setCustomers(
            Array.isArray(result)
              ? result
              : result.items || [],
          );
        } catch {
          // Offline-safe.
        }
      };

    void load();
  }, []);

  const filtered =
    customers.filter(
      (customer) =>
        customer.name
          .toLowerCase()
          .includes(
            search.toLowerCase(),
          ) ||
        customer.phone
          ?.includes(search) ||
        customer.customer_code
          ?.toLowerCase()
          .includes(
            search.toLowerCase(),
          ),
    );

  return (
    <div>
      <div className="page-heading">
        <div>
          <h1>Customers</h1>
          <p>
            Manage regular and VIP customers.
          </p>
        </div>

        <button className="primary-button">
          <UserPlus size={17} />
          Add Customer
        </button>
      </div>

      <div className="panel">
        <div className="table-toolbar">
          <div className="search-box">
            <Search size={17} />

            <input
              value={search}
              onChange={(event) =>
                setSearch(
                  event.target.value,
                )
              }
              placeholder="Search name, phone or customer code..."
            />
          </div>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Customer Code</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map(
                (customer) => (
                  <tr key={customer.id}>
                    <td>
                      <strong>
                        {customer.name}
                      </strong>
                    </td>

                    <td>
                      {customer.phone ||
                        "—"}
                    </td>

                    <td>
                      {customer.customer_code ? (
                        <span className="customer-code">
                          {customer.customer_code}
                        </span>
                      ) : (
                        "—"
                      )}
                    </td>

                    <td>
                      {customer.customer_code ? (
                        <span className="badge vip">
                          <Star
                            size={12}
                          />
                          VIP
                        </span>
                      ) : (
                        <span className="badge success">
                          Active
                        </span>
                      )}
                    </td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
