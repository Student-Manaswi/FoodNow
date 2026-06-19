import { useEffect, useMemo, useState } from "react";
import { useApp } from "@/contexts/AppContext";
import api from "@/services/api";
import { CATEGORIES, type Dish } from "@/lib/spice-types";
import DishCard, { DishCardSkeleton } from "./DishCard";
import OrderTracker from "./OrderTracker";
import { toast } from "sonner";

export default function CustomerApp() {
  const {
    user,
    logout,
    cart,
    cartCount,
    cartTotal,
    addItem,
    updateQty,
    clearCart,
    setActiveOrder,
    activeOrder,
  } = useApp();
  const [dishes, setDishes] = useState<Dish[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<string>("All");
  const [aiMode, setAiMode] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);
  const [recommendation, setRecommendation] = useState<string | null>(null);

  // initial load
  useEffect(() => {
    void fetchDishes("");
  }, []);

  // debounced search
  useEffect(() => {
    const t = setTimeout(() => {
      void fetchDishes(query);
    }, 500);
    return () => clearTimeout(t);
  }, [query]);

  const fetchDishes = async (q: string) => {
    setLoading(true);
    setAiMode(q.trim().length > 0);
    try {
      const res = await api.get("/api/search", { params: { query: q } });

      // Clean fallback array checks
      const rawData = res.data?.results || res.data || [];

      const data: Dish[] = rawData.map((d: any) => ({
        dish_id: String(d.dish_id || d.id || d._id || ""),
        name: d.name || "Unnamed",
        description: d.description || "",
        category: d.category || "Mains",
        price: Number(d.price ?? 0),
        tags: d.tags || d.dietary_tags || [],
        is_available: d.is_available !== false,
      }));
      setDishes(data);
    } catch (err) {
      console.error("❌ Frontend fetch alignment failure:", err);
      setDishes([]);
    } finally {
      setLoading(false);
    }
  };

  // cross-sell on cart change
  useEffect(() => {
    if (cart.length === 0) {
      setRecommendation(null);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const res = await api.post(
          "/api/cart/recommend",
          cart.map((i) => ({ dish_id: i.dish_id, name: i.name, dietary_tags: i.tags || [] })),
        );
        if (!cancelled)
          setRecommendation(
            res.data?.recommendation_text || res.data?.recommendation || res.data?.message || null,
          );
      } catch {
        /* silent fallback */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [cart]);

  const filtered = useMemo(() => {
    if (category === "All") return dishes;
    return dishes.filter((d) => (d.category || "").toLowerCase() === category.toLowerCase());
  }, [dishes, category]);

  const placeOrder = async () => {
    if (cart.length === 0) return;
    try {
      const res = await api.post("/api/orders", {
        customer_name: user?.name || "Guest",
        phone: user?.phone || "+91-0000000000",
        items: cart.map((i) => ({
          dish_id: i.dish_id,
          dish_name: i.name,
          quantity: i.quantity,
          unit_price: i.price,
        })),
      });
      const orderId = res.data?.order_id || res.data?._id || res.data?.id || "demo-order";
      setActiveOrder({ order_id: orderId, status: "Placed" });
      clearCart();
      setCartOpen(false);
      toast.success("Order placed!");
    } catch {
      toast.error("Could not place order. Try again.");
    }
  };

  return (
    <div className="min-h-screen bg-surface">
      {/* NAVBAR */}
      <header className="sticky top-0 z-30 border-b border-brandborder bg-card/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
          <h1 className="text-xl font-bold text-primary shrink-0">SpiceRoute</h1>
          <div className="flex-1 max-w-xl">
            <div className="relative">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="🔍 Try 'something light and not fried'"
                className="w-full rounded-full border border-brandborder bg-surface px-4 py-2 text-sm outline-none focus:border-primary"
              />
              {query && (
                <button
                  onClick={() => setQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-textsecondary hover:text-primary"
                >
                  x
                </button>
              )}
            </div>
          </div>
          <button
            onClick={() => setCartOpen((v) => !v)}
            className="relative rounded-full bg-primary-light p-2.5 text-primary hover:bg-primary hover:text-white transition lg:hidden"
          >
            🛒
            {cartCount > 0 && (
              <span className="animate-badge-pop absolute -top-1 -right-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-[10px] font-bold text-white">
                {cartCount}
              </span>
            )}
          </button>
          <div className="hidden md:flex items-center gap-2 rounded-full bg-primary-light px-3 py-1.5 text-sm">
            <span className="font-semibold text-primary">Hi, {user?.name}</span>
            <button onClick={logout} className="text-xs text-textsecondary hover:text-primary">
              Logout
            </button>
          </div>
        </div>
        {/* CATEGORY TABS */}
        <div className="mx-auto max-w-7xl overflow-x-auto px-4 pb-2">
          <div className="flex gap-1">
            {CATEGORIES.map((c) => (
              <button
                key={c}
                onClick={() => setCategory(c)}
                className={`whitespace-nowrap px-4 py-2 text-sm font-medium transition border-b-2 ${category === c ? "border-primary text-primary" : "border-transparent text-textsecondary hover:text-textprimary"}`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* MAIN GRID + CART */}
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6">
        <main className="flex-1">
          {loading ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 6 }).map((_, i) => (
                <DishCardSkeleton key={i} />
              ))}
            </div>
          ) : filtered.length === 0 ? (
            <EmptyState
              icon="🍽️"
              title="No dishes found"
              sub="Try a different search or category."
            />
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((d) => {
                const qty = cart.find((i) => i.dish_id === d.dish_id)?.quantity ?? 0;
                return (
                  <DishCard
                    key={d.dish_id}
                    dish={d}
                    inCartQty={qty}
                    onAdd={() => addItem(d)}
                    onInc={() => updateQty(d.dish_id, qty + 1)}
                    onDec={() => updateQty(d.dish_id, qty - 1)}
                    aiMatch={aiMode}
                  />
                );
              })}
            </div>
          )}
        </main>

        {/* Desktop cart */}
        <aside className="hidden lg:block w-80 shrink-0">
          <CartPanel
            recommendation={recommendation}
            onDismissRec={() => setRecommendation(null)}
            onPlaceOrder={placeOrder}
          />
        </aside>
      </div>

      {/* Mobile cart drawer */}
      {cartOpen && (
        <div className="fixed inset-0 z-40 lg:hidden" onClick={() => setCartOpen(false)}>
          <div className="absolute inset-0 bg-black/40" />
          <div
            onClick={(e) => e.stopPropagation()}
            className="absolute bottom-0 left-0 right-0 max-h-[85vh] overflow-y-auto rounded-t-2xl bg-card p-4 animate-slide-in-right"
          >
            <CartPanel
              recommendation={recommendation}
              onDismissRec={() => setRecommendation(null)}
              onPlaceOrder={placeOrder}
            />
          </div>
        </div>
      )}

      {activeOrder && <OrderTracker />}
    </div>
  );
}

function CartPanel({
  recommendation,
  onDismissRec,
  onPlaceOrder,
}: {
  recommendation: string | null;
  onDismissRec: () => void;
  onPlaceOrder: () => void;
}) {
  const { cart, cartTotal, cartCount, updateQty } = useApp();
  return (
    <div className="rounded-xl border border-brandborder bg-card p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-textprimary">Your Order</h3>
        <span className="text-xs text-textsecondary">
          {cartCount} item{cartCount !== 1 ? "s" : ""}
        </span>
      </div>
      {cart.length === 0 ? (
        <p className="mt-6 text-center text-sm text-textsecondary">Your cart is empty.</p>
      ) : (
        <>
          <ul className="mt-4 space-y-3">
            {cart.map((i) => (
              <li key={i.dish_id} className="flex items-center gap-2 text-sm">
                <span className="flex-1 truncate font-medium text-textprimary">{i.name}</span>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => updateQty(i.dish_id, i.quantity - 1)}
                    className="h-6 w-6 rounded bg-primary-light font-bold text-primary"
                  >
                    −
                  </button>
                  <span className="w-6 text-center">{i.quantity}</span>
                  <button
                    onClick={() => updateQty(i.dish_id, i.quantity + 1)}
                    className="h-6 w-6 rounded bg-primary-light font-bold text-primary"
                  >
                    +
                  </button>
                </div>
                <span className="w-14 text-right font-semibold text-primary">
                  ₹{i.price * i.quantity}
                </span>
              </li>
            ))}
          </ul>
          <hr className="my-4 border-brandborder" />
          <div className="flex justify-between text-sm text-textsecondary">
            <span>Subtotal</span>
            <span>₹{cartTotal}</span>
          </div>
          <div className="mt-1 flex justify-between text-base font-bold text-textprimary">
            <span>Total</span>
            <span>₹{cartTotal}</span>
          </div>

          {recommendation && (
            <div className="mt-4 flex items-start gap-2 rounded-lg border-l-4 border-primary bg-primary-light p-3 text-sm">
              <span className="text-lg">🌶️</span>
              <p className="flex-1 text-textprimary">{recommendation}</p>
              <button onClick={onDismissRec} className="text-textsecondary hover:text-textprimary">
                ×
              </button>
            </div>
          )}

          <button
            onClick={onPlaceOrder}
            className="mt-4 w-full rounded-lg bg-primary py-2.5 font-semibold text-white transition hover:bg-primary-dark"
          >
            Place Order
          </button>
        </>
      )}
    </div>
  );
}

function EmptyState({ icon, title, sub }: { icon: string; title: string; sub: string }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-brandborder bg-card py-16 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-light text-2xl">
        {icon}
      </div>
      <h3 className="mt-4 font-semibold text-textprimary">{title}</h3>
      <p className="mt-1 text-sm text-textsecondary">{sub}</p>
    </div>
  );
}
