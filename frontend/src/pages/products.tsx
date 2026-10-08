import {
  useEffect,
  useState,
} from "react";

import {
  Package,
  Plus,
  Search,
  TriangleAlert,
} from "lucide-react";

import { api } from "../api/client";
import type {
  Product,
} from "../types";

function money(value: number) {
  return `PKR ${Number(value || 0).toLocaleString(
    "en-PK",
    {
      minimumFractionDigits: 2,
    },
  )}`;
}

export default function Products() {
  const [
    products,
    setProducts,
  ] = useState<Product[]>([]);

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
              "/products",
              "products",
            );

          setProducts(
            Array.isArray(result)
              ? result
              : result.items || [],
          );
        } catch {
          // Offline cache.
        }
      };

    void load();
  }, []);

  const filtered =
    products.filter(
      (product) =>
        product.name
          .toLowerCase()
          .includes(
            search.toLowerCase(),
          ) ||
        product.sku
          ?.toLowerCase()
          .includes(
            search.toLowerCase(),
          ),
    );

  return (
    <div>
      <div className="page-heading">
        <div>
          <h1>Products & Stock</h1>
          <p>
            Manage products, prices and inventory.
          </p>
        </div>

        <button className="primary-button">
          <Plus size={17} />
          Add Product
        </button>
      </div>

      <div className="panel">
        <div className="table-toolbar">
          <div className="search-box">
            <Search size={17} />

            <input
              placeholder="Search products..."
              value={search}
              onChange={(event) =>
                setSearch(
                  event.target.value,
                )
              }
            />
          </div>

          <span className="table-count">
            {filtered.length} products
          </span>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>SKU</th>
                <th>Purchase</th>
                <th>Selling</th>
                <th>Stock</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map(
                (product) => (
                  <tr key={product.id}>
                    <td>
                      <div className="table-product">
                        <div className="mini-icon">
                          <Package
                            size={16}
                          />
                        </div>

                        <strong>
                          {product.name}
                        </strong>
                      </div>
                    </td>

                    <td>
                      {product.sku ||
                        "—"}
                    </td>

                    <td>
                      {money(
                        product.purchase_price,
                      )}
                    </td>

                    <td>
                      {money(
                        product.selling_price,
                      )}
                    </td>

                    <td>
                      {product.current_stock}
                      {" "}
                      {product.unit ||
                        "pcs"}
                    </td>

                    <td>
                      {product.current_stock <=
                      product.min_stock ? (
                        <span className="badge warning">
                          <TriangleAlert
                            size={12}
                          />
                          Low Stock
                        </span>
                      ) : (
                        <span className="badge success">
                          In Stock
                        </span>
                      )}
                    </td>
                  </tr>
                ),
              )}
            </tbody>
          </table>

          {!filtered.length && (
            <div className="empty-state">
              No products available.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
