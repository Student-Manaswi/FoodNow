import { useEffect, useState } from "react";
import { useApp } from "@/contexts/AppContext";
import api from "@/services/api";
import {
  CATEGORIES,
  ORDER_STATUSES,
  TAG_OPTIONS,
  type Dish,
  type DashboardData,
  type OrderData,
  type FeedbackItem,
} from "@/lib/spice-types";
import { toast } from "sonner";

type Section = "dashboard" | "menu" | "orders" | "feedback";

export default function AdminApp() {
  const { user, logout, setScreen } = useApp();
  const [section, setSection] = useState<Section>("dashboard");

  const nav: { key: Section; label: string; icon: string }[] = [
    { key: "dashboard", label: "Dashboard", icon: "📊" },
    { key: "menu", label: "Menu", icon: "🍽️" },
    { key: "orders", label: "Orders", icon: "📦" },
    { key: "feedback", label: "Feedback", icon: "💬" },
  ];

  return (
    <div className="min-h-screen bg-surface">
      <header className="border-b border-brandborder bg-card">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <h1 className="font-bold text-textprimary">
            Admin Panel · <span className="text-primary">SpiceRoute</span>
          </h1>
          <div className="flex items-center gap-4 text-sm">
            <button
              onClick={() => setScreen("customer")}
              className="text-textsecondary hover:text-primary"
            >
              Switch to Customer View
            </button>
            <span className="text-textsecondary">Hi, {user?.name}</span>
            <button onClick={logout} className="text-primary hover:underline">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl flex-col md:flex-row">
        {/* Sidebar (desktop) */}
        <aside className="hidden md:block w-56 shrink-0 border-r border-brandborder bg-card p-3">
          {nav.map((n) => (
            <button
              key={n.key}
              onClick={() => setSection(n.key)}
              className={`flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition
                ${section === n.key ? "bg-primary-light text-primary" : "text-textsecondary hover:bg-primary-light/50"}`}
            >
              <span>{n.icon}</span>
              {n.label}
            </button>
          ))}
        </aside>

        <main className="flex-1 p-4 md:p-6 pb-24 md:pb-6">
          {section === "dashboard" && <Dashboard />}
          {section === "menu" && <MenuManagement />}
          {section === "orders" && <OrdersAdmin />}
          {section === "feedback" && <FeedbackWall />}
        </main>
      </div>

      {/* Mobile bottom tab bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-30 flex border-t border-brandborder bg-card md:hidden">
        {nav.map((n) => (
          <button
            key={n.key}
            onClick={() => setSection(n.key)}
            className={`flex flex-1 flex-col items-center py-2 text-xs font-medium transition
              ${section === n.key ? "text-primary" : "text-textsecondary"}`}
          >
            <span className="text-lg">{n.icon}</span>
            {n.label}
          </button>
        ))}
      </nav>
    </div>
  );
}

/* ------------------ DASHBOARD ------------------ */
function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/api/admin/dashboard");
        setData(res.data || {});
      } catch {
        setData(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const cards = [
    { icon: "💰", label: "Revenue", value: data ? `₹${data.total_revenue ?? 0}` : "—" },
    { icon: "📦", label: "Active Orders", value: data?.active_orders ?? 0 },
    {
      icon: "🔥",
      label: "Top Dish",
      value: data?.popular_items?.[0]?.name ?? "—",
      sub: data?.popular_items?.[0]
        ? `${data.popular_items[0].count ?? data.popular_items[0].orders ?? ""} orders`
        : "",
    },
    {
      icon: "⭐",
      label: "Avg Rating",
      value: data?.avg_rating != null ? `${Number(data.avg_rating).toFixed(1)} / 5` : "—",
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-textprimary">Dashboard</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {loading
          ? Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-32 animate-pulse rounded-xl bg-gray-200" />
            ))
          : cards.map((c) => (
              <div
                key={c.label}
                className="rounded-xl border-t-4 border-primary bg-card p-5 shadow-sm"
              >
                <div className="text-2xl">{c.icon}</div>
                <div className="mt-2 text-xs uppercase tracking-wide text-textsecondary">
                  {c.label}
                </div>
                <div className="mt-1 text-2xl font-bold text-textprimary">{c.value}</div>
                {c.sub && <div className="text-xs text-textsecondary">{c.sub}</div>}
              </div>
            ))}
      </div>
    </div>
  );
}

/* ------------------ MENU MANAGEMENT ------------------ */
function MenuManagement() {
  const [dishes, setDishes] = useState<Dish[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState<Dish | null>(null);
  const [creating, setCreating] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/search", { params: { query: "" } });
      const data: Dish[] = (res.data?.results || res.data || []).map(
        (d: Record<string, unknown>) => ({
          dish_id: d.dish_id || d._id || d.id,
          name: d.name,
          description: d.description,
          category: d.category,
          price: Number(d.price ?? 0),
          tags: d.tags || [],
          is_available: d.is_available !== false,
        }),
      );
      setDishes(data);
    } catch {
      setDishes([]);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    void load();
  }, []);

  const toggleAvail = async (d: Dish) => {
    try {
      await api.patch(`/api/admin/dishes/${d.dish_id}`, { is_available: !d.is_available });
      setDishes((ds) =>
        ds.map((x) => (x.dish_id === d.dish_id ? { ...x, is_available: !x.is_available } : x)),
      );
    } catch {
      toast.error("Could not update.");
    }
  };

  const remove = async (d: Dish) => {
    if (!confirm(`Delete "${d.name}"?`)) return;
    try {
      await api.delete(`/api/admin/dishes/${d.dish_id}`);
      setDishes((ds) => ds.filter((x) => x.dish_id !== d.dish_id));
      toast.success("Dish deleted.");
    } catch {
      toast.error("Delete failed.");
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-textprimary">Menu Management</h2>
        <button
          onClick={() => setCreating(true)}
          className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
        >
          + Add New Dish
        </button>
      </div>

      <div className="mt-6 overflow-x-auto rounded-xl border border-brandborder bg-card shadow-sm">
        <table className="w-full text-sm">
          <thead className="bg-primary-light text-left text-xs uppercase tracking-wide text-primary">
            <tr>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Price</th>
              <th className="px-4 py-3">Tags</th>
              <th className="px-4 py-3">Available</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array.from({ length: 4 }).map((_, i) => (
                <tr key={i} className="border-t border-brandborder">
                  {Array.from({ length: 6 }).map((__, j) => (
                    <td key={j} className="px-4 py-3">
                      <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
                    </td>
                  ))}
                </tr>
              ))
            ) : dishes.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-12 text-center text-textsecondary">
                  No dishes yet. Add your first dish.
                </td>
              </tr>
            ) : (
              dishes.map((d) => (
                <tr key={d.dish_id} className="border-t border-brandborder">
                  <td className="px-4 py-3 font-medium text-textprimary">{d.name}</td>
                  <td className="px-4 py-3 text-textsecondary">{d.category || "—"}</td>
                  <td className="px-4 py-3 font-semibold text-primary">₹{d.price}</td>
                  <td className="px-4 py-3 text-xs text-textsecondary">
                    {(d.tags || []).join(", ")}
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => toggleAvail(d)}
                      aria-label={`Toggle ${d.name} availability`}
                      className={`relative h-6 w-11 rounded-full transition ${d.is_available ? "bg-success" : "bg-gray-300"}`}
                    >
                      <span
                        className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition ${d.is_available ? "left-5" : "left-0.5"}`}
                      />
                    </button>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <button
                        onClick={() => setEditing(d)}
                        className="rounded border border-brandborder px-2 py-1 text-xs hover:bg-primary-light hover:text-primary"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => remove(d)}
                        className="rounded border border-danger px-2 py-1 text-xs text-danger hover:bg-danger hover:text-white"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {(editing || creating) && (
        <DishModal
          initial={editing || undefined}
          onClose={() => {
            setEditing(null);
            setCreating(false);
          }}
          onSaved={() => {
            setEditing(null);
            setCreating(false);
            void load();
          }}
        />
      )}
    </div>
  );
}

function DishModal({
  initial,
  onClose,
  onSaved,
}: {
  initial?: Dish;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [name, setName] = useState(initial?.name || "");
  const [description, setDescription] = useState(initial?.description || "");
  const [category, setCategory] = useState(initial?.category || "Mains");
  const [price, setPrice] = useState<number>(initial?.price || 0);
  const [tags, setTags] = useState<string[]>(initial?.tags || []);
  const [isAvailable, setIsAvailable] = useState(initial?.is_available !== false);
  const [saving, setSaving] = useState(false);

  const toggleTag = (t: string) =>
    setTags((ts) => (ts.includes(t) ? ts.filter((x) => x !== t) : [...ts, t]));

  const save = async () => {
    if (!name.trim()) {
      toast.error("Name is required.");
      return;
    }
    setSaving(true);
    const payload = {
      name,
      description,
      category,
      price: Number(price),
      tags,
      is_available: isAvailable,
    };
    try {
      if (initial) await api.patch(`/api/admin/dishes/${initial.dish_id}`, payload);
      else await api.post(`/api/admin/dishes`, payload);
      toast.success("Saved!");
      onSaved();
    } catch {
      toast.error("Save failed.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl bg-card p-6 shadow-xl animate-fade-in">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-textprimary">
            {initial ? "Edit Dish" : "Add New Dish"}
          </h3>
          <button onClick={onClose} className="text-2xl leading-none text-textsecondary">
            ×
          </button>
        </div>
        <div className="mt-4 space-y-3">
          <Field label="Name">
            <input
              placeholder="Dish name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
            />
          </Field>
          <Field label="Description">
            <textarea
              placeholder="Dish description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="input"
            />
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="Category">
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                aria-label="Select dish category"
                className="input"
              >
                {CATEGORIES.filter((c) => c !== "All").map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </Field>
            <Field label="Price (₹)">
              <input
                type="number"
                min={0}
                placeholder="0"
                value={price}
                onChange={(e) => setPrice(Number(e.target.value))}
                className="input"
              />
            </Field>
          </div>
          <Field label="Tags">
            <div className="flex flex-wrap gap-2">
              {TAG_OPTIONS.map((t) => (
                <label
                  key={t}
                  className={`cursor-pointer rounded-full border px-3 py-1 text-xs ${tags.includes(t) ? "border-primary bg-primary text-white" : "border-brandborder text-textsecondary"}`}
                >
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={tags.includes(t)}
                    onChange={() => toggleTag(t)}
                  />
                  {t}
                </label>
              ))}
            </div>
          </Field>
          <label className="flex items-center gap-3 text-sm">
            <input
              type="checkbox"
              checked={isAvailable}
              onChange={(e) => setIsAvailable(e.target.checked)}
              className="accent-[#E85D24]"
            />
            Is Available
          </label>
        </div>
        <div className="mt-6 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="rounded-lg border border-brandborder px-4 py-2 text-sm"
          >
            Cancel
          </button>
          <button
            onClick={save}
            disabled={saving}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-60"
          >
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
        <style>{`.input{width:100%;border:1px solid #F0E6DF;border-radius:0.5rem;padding:0.5rem 0.75rem;font-size:0.875rem;outline:none;background:#fff} .input:focus{border-color:#E85D24}`}</style>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="mb-1 block text-xs font-medium text-textsecondary">{label}</label>
      {children}
    </div>
  );
}

/* ------------------ ORDERS ------------------ */
function OrdersAdmin() {
  const [orders, setOrders] = useState<OrderData[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/api/orders");
        setOrders(Array.isArray(res.data) ? res.data : res.data?.results || []);
      } catch {
        setOrders(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const statusColor = (s: string) =>
    (
      ({
        Placed: "bg-gray-200 text-gray-700",
        Confirmed: "bg-blue-100 text-info",
        Preparing: "bg-amber-100 text-warning",
        Ready: "bg-green-100 text-success",
        "Picked Up": "bg-gray-800 text-white",
      }) as Record<string, string>
    )[s] || "bg-gray-100";

  const updateStatus = async (orderId: string, status: string) => {
    if (!confirm(`Set order to "${status}"?`)) return;
    try {
      await api.patch(`/api/orders/${orderId}/status`, { status });
      setOrders(
        (os) =>
          os?.map((o) => ((o.order_id || o._id || o.id) === orderId ? { ...o, status } : o)) || [],
      );
      toast.success("Status updated.");
    } catch {
      toast.error("Update failed.");
    }
  };

  if (loading)
    return (
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-14 animate-pulse rounded-xl bg-gray-200" />
        ))}
      </div>
    );
  if (!orders || orders.length === 0)
    return (
      <div>
        <h2 className="text-2xl font-bold text-textprimary">Orders</h2>
        <div className="mt-6 rounded-xl border border-brandborder bg-card py-16 text-center">
          <div className="text-3xl">📦</div>
          <p className="mt-2 text-textsecondary">
            No orders yet. Orders placed by customers will appear here.
          </p>
        </div>
      </div>
    );

  return (
    <div>
      <h2 className="text-2xl font-bold text-textprimary">Orders</h2>
      <div className="mt-6 overflow-x-auto rounded-xl border border-brandborder bg-card shadow-sm">
        <table className="w-full text-sm">
          <thead className="bg-primary-light text-left text-xs uppercase tracking-wide text-primary">
            <tr>
              <th className="px-4 py-3">Order</th>
              <th className="px-4 py-3">Customer</th>
              <th className="px-4 py-3">Items</th>
              <th className="px-4 py-3">Total</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Update</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => {
              const id = o.order_id || o._id || o.id;
              return (
                <tr key={id} className="border-t border-brandborder">
                  <td className="px-4 py-3 font-mono text-xs">{String(id).slice(0, 8)}</td>
                  <td className="px-4 py-3">{o.customer_name}</td>
                  <td className="px-4 py-3">{o.items?.length ?? 0}</td>
                  <td className="px-4 py-3 font-semibold text-primary">₹{o.total_price}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-semibold ${statusColor(o.status)}`}
                    >
                      {o.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <select
                      defaultValue={o.status}
                      onChange={(e) => updateStatus(id as string, e.target.value || o.status)}
                      aria-label="Update order status"
                      className="rounded-lg border border-brandborder bg-card px-2 py-1 text-xs"
                    >
                      {ORDER_STATUSES.map((s) => (
                        <option key={s}>{s}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ------------------ FEEDBACK WALL ------------------ */
function FeedbackWall() {
  const [items, setItems] = useState<FeedbackItem[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/api/feedback");
        setItems(Array.isArray(res.data) ? res.data : res.data?.results || []);
      } catch {
        setItems([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const relative = (ts?: string) => {
    if (!ts) return "";
    const d = new Date(ts).getTime();
    const diff = Math.max(0, Date.now() - d);
    const m = Math.floor(diff / 60000);
    if (m < 1) return "just now";
    if (m < 60) return `${m}m ago`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-textprimary">Feedback Wall</h2>
      {loading ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-32 animate-pulse rounded-xl bg-gray-200" />
          ))}
        </div>
      ) : items && items.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((f, i) => (
            <div key={i} className="rounded-xl border border-brandborder bg-card p-4 shadow-sm">
              <div className="flex">
                {[1, 2, 3, 4, 5].map((n) => (
                  <span key={n} className={n <= (f.rating ?? 0) ? "text-primary" : "text-gray-300"}>
                    ★
                  </span>
                ))}
              </div>
              <p className="mt-2 text-sm text-textprimary">{f.comment || "—"}</p>
              <p className="mt-3 text-xs text-textsecondary">
                {relative(f.created_at || f.timestamp)}
              </p>
              {Array.isArray(f.photo_urls) && f.photo_urls.length > 0 && (
                <div className="mt-3 flex gap-2 overflow-x-auto">
                  {f.photo_urls.map((u: string, i: number) => (
                    <img key={i} src={u} className="h-16 w-16 rounded-lg object-cover" alt="" />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-6 rounded-xl border border-brandborder bg-card py-16 text-center">
          <div className="text-3xl">💬</div>
          <p className="mt-2 text-textsecondary">No feedback yet.</p>
        </div>
      )}
    </div>
  );
}
