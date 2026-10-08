import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Barcode,
  CreditCard,
  Minus,
  Plus,
  Search,
  ShoppingCart,
  Trash2,
  UserRound,
} from "lucide-react";

import { api } from "../api/client";
import type {
  CartItem,
  Customer,
  Product,
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

export default function POS() {
  const [
    products,
    setProducts,
  ] = useState<Product[]>([]);

  const [
    customers,
    setCustomers,
  ] = useState<Customer[]>([]);

  const [
    search,
    setSearch,
  ] = useState("");

  const [
    cart,
    setCart,
  ] = useState<CartItem[]>([]);

  const [
    selectedCustomer,
    setSelectedCustomer,
  ] = useState<Customer | null>(
    null,
  );

  const [
    discount,
    setDiscount,
  ] = useState(0);

  const [
    paymentMethod,
    setPaymentMethod,
  ] = useState("cash");

  const [
    cashReceived,
    setCashReceived,
  ] = useState(0);

  useEffect(() => {
    const load =
      async () => {
        try {
          const result =
            await api.get<any>(
              "/products",
              "products",
            );

          const list =
            Array.isArray(result)
              ? result
              : result.items || [];

          setProducts(list);
        } catch {
          // Cached/offline data may be unavailable initially.
        }

        try {
          const result =
            await api.get<any>(
              "/customers",
              "customers",
            );

          const list =
            Array.isArray(result)
              ? result
              : result.items || [];

          setCustomers(list);
        } catch {
          // Offline safe.
        }
      };

    void load();
  }, []);

  const filteredProducts =
    useMemo(
      () =>
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
        ),
      [products, search],
    );

  const subtotal =
    cart.reduce(
      (sum, item) =>
        sum +
        item.product.selling_price *
          item.quantity -
        item.discount,
      0,
    );

  const total = Math.max(
    0,
    subtotal - discount,
  );

  const change = Math.max(
    0,
    cashReceived - total,
  );

  function addProduct(
    product: Product,
  ) {
    setCart(
      (current) => {
        const existing =
          current.find(
            (item) =>
              item.product.id ===
              product.id,
          );

        if (existing) {
          return current.map(
            (item) =>
              item.product.id ===
              product.id
                ? {
                    ...item,
                    quantity:
                      item.quantity + 1,
                  }
                : item,
          );
        }

        return [
          ...current,
          {
            product,
            quantity: 1,
            discount: 0,
          },
        ];
      },
    );
  }

  function updateQuantity(
    productId: number,
    amount: number,
  ) {
    setCart(
      (current) =>
        current
          .map((item) =>
            item.product.id ===
            productId
              ? {
                  ...item,
                  quantity:
                    item.quantity +
                    amount,
                }
              : item,
          )
          .filter(
            (item) =>
              item.quantity > 0,
          ),
    );
  }

  async function completeSale() {
    if (!cart.length) {
      return;
    }

    const sale = {
      customer_id:
        selectedCustomer?.id ||
        null,

      discount_amount: discount,

      discount_type:
        discount > 0
          ? "fixed"
          : "none",

      items: cart.map(
        (item) => ({
          product_id:
            item.product.id,

          quantity:
            item.quantity,

          unit_price:
            item.product
              .selling_price,

          discount_amount:
            item.discount,
        }),
      ),

      payment: {
        method:
          paymentMethod,

        amount:
          paymentMethod === "cash"
            ? cashReceived
            : total,
      },
    };

    try {
      await api.post(
        "/sales",
        sale,
      );

      setCart([]);
      setDiscount(0);
      setCashReceived(0);
      setSelectedCustomer(null);

      alert(
        "Sale completed successfully.",
      );
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Sale could not be completed.",
      );
    }
  }

  return (
    <div className="pos-page">
      <div className="page-heading">
        <div>
          <h1>Point of Sale</h1>
          <p>
            Scan, search and complete
            transactions quickly.
          </p>
        </div>

        <div className="pos-status">
          <span className="status-dot" />
          Register Ready
        </div>
      </div>

      <div className="pos-layout">
        <section className="pos-products panel">
          <div className="search-row">
            <div className="search-box">
              <Search size={18} />

              <input
                value={search}
                onChange={(event) =>
                  setSearch(
                    event.target.value,
                  )
                }
                placeholder="Search product or SKU..."
              />
            </div>

            <button className="scan-button">
              <Barcode size={18} />
              Scan
            </button>
          </div>

          <div className="product-grid">
            {filteredProducts.map(
              (product) => (
                <button
                  className="product-card"
                  key={product.id}
                  onClick={() =>
                    addProduct(product)
                  }
                >
                  <div className="product-card-icon">
                    <PackageIcon />
                  </div>

                  <strong>
                    {product.name}
                  </strong>

                  <span>
                    {product.sku ||
                      "No SKU"}
                  </span>

                  <b>
                    {money(
                      product.selling_price,
                    )}
                  </b>

                  <small>
                    Stock:{" "}
                    {product.current_stock}
                  </small>
                </button>
              ),
            )}

            {!filteredProducts.length && (
              <div className="empty-state">
                No products found.
              </div>
            )}
          </div>
        </section>

        <section className="pos-cart panel">
          <div className="cart-heading">
            <div>
              <h2>
                <ShoppingCart
                  size={19}
                />
                Current Sale
              </h2>
              <span>
                {cart.length} items
              </span>
            </div>
          </div>

          <div className="customer-select">
            <UserRound size={17} />

            <select
              value={
                selectedCustomer?.id ||
                ""
              }
              onChange={(event) => {
                const customer =
                  customers.find(
                    (item) =>
                      item.id ===
                      Number(
                        event.target.value,
                      ),
                  );

                setSelectedCustomer(
                  customer || null,
                );
              }}
            >
              <option value="">
                Walk-in Customer
              </option>

              {customers.map(
                (customer) => (
                  <option
                    key={customer.id}
                    value={customer.id}
                  >
                    {customer.name}
                    {customer.customer_code
                      ? ` — ${customer.customer_code}`
                      : ""}
                  </option>
                ),
              )}
            </select>
          </div>

          {selectedCustomer?.customer_code && (
            <div className="vip-banner">
              ⭐ VIP CUSTOMER
              <span>
                {selectedCustomer.name}
                {" · "}
                {selectedCustomer.customer_code}
              </span>
            </div>
          )}

          <div className="cart-items">
            {cart.map((item) => (
              <div
                className="cart-item"
                key={item.product.id}
              >
                <div className="cart-item-info">
                  <strong>
                    {item.product.name}
                  </strong>

                  <span>
                    {money(
                      item.product
                        .selling_price,
                    )}
                  </span>
                </div>

                <div className="quantity-control">
                  <button
                    onClick={() =>
                      updateQuantity(
                        item.product.id,
                        -1,
                      )
                    }
                  >
                    <Minus size={13} />
                  </button>

                  <strong>
                    {item.quantity}
                  </strong>

                  <button
                    onClick={() =>
                      updateQuantity(
                        item.product.id,
                        1,
                      )
                    }
                  >
                    <Plus size={13} />
                  </button>
                </div>

                <strong className="item-total">
                  {money(
                    item.product
                      .selling_price *
                      item.quantity -
                      item.discount,
                  )}
                </strong>

                <button
                  className="icon-danger"
                  onClick={() =>
                    setCart(
                      (current) =>
                        current.filter(
                          (cartItem) =>
                            cartItem
                              .product
                              .id !==
                            item.product
                              .id,
                        ),
                    )
                  }
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))}

            {!cart.length && (
              <div className="cart-empty">
                <ShoppingCart
                  size={35}
                />
                <strong>
                  Cart is empty
                </strong>
                <span>
                  Select products to
                  start a sale.
                </span>
              </div>
            )}
          </div>

          <div className="cart-summary">
            <div>
              <span>Subtotal</span>
              <strong>
                {money(subtotal)}
              </strong>
            </div>

            <div className="discount-line">
              <span>
                {selectedCustomer
                  ? "VIP Discount"
                  : "Discount"}
              </span>

              <input
                type="number"
                min="0"
                value={discount}
                onChange={(event) =>
                  setDiscount(
                    Number(
                      event.target.value,
                    ),
                  )
                }
              />
            </div>

            <div className="total-line">
              <span>Total</span>
              <strong>
                {money(total)}
              </strong>
            </div>

            <div className="payment-methods">
              {[
                ["cash", "Cash"],
                ["card", "Card"],
                ["bank", "Bank"],
                ["other", "Other"],
              ].map(
                ([value, label]) => (
                  <button
                    key={value}
                    className={
                      paymentMethod ===
                      value
                        ? "payment active"
                        : "payment"
                    }
                    onClick={() =>
                      setPaymentMethod(
                        value,
                      )
                    }
                  >
                    <CreditCard
                      size={15}
                    />
                    {label}
                  </button>
                ),
              )}
            </div>

            {paymentMethod ===
              "cash" && (
              <div className="cash-input">
                <label>
                  Cash Received
                </label>

                <input
                  type="number"
                  min="0"
                  value={cashReceived}
                  onChange={(event) =>
                    setCashReceived(
                      Number(
                        event.target
                          .value,
                      ),
                    )
                  }
                />

                <span>
                  Change:{" "}
                  <strong>
                    {money(change)}
                  </strong>
                </span>
              </div>
            )}

            <button
              className="complete-sale"
              disabled={!cart.length}
              onClick={
                completeSale
              }
            >
              Complete Sale
              <span>
                {money(total)}
              </span>
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

function PackageIcon() {
  return (
    <Package
      size={25}
    />
  );
}
