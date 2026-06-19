import type { Dish, CartItem } from "@/lib/spice-types";

const GRADIENTS = [
  "from-orange-400 to-pink-500",
  "from-amber-400 to-red-500",
  "from-red-400 to-orange-600",
  "from-yellow-400 to-orange-500",
  "from-pink-400 to-purple-500",
  "from-emerald-400 to-teal-500",
];

export function dishGradient(name: string) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
  return GRADIENTS[h % GRADIENTS.length];
}

const TAG_STYLES: Record<string, string> = {
  vegetarian: "bg-green-100 text-green-700",
  "veg": "bg-green-100 text-green-700",
  "non-vegetarian": "bg-red-100 text-red-700",
  "non-veg": "bg-red-100 text-red-700",
  spicy: "bg-orange-100 text-orange-700",
  healthy: "bg-teal-100 text-teal-700",
  vegan: "bg-purple-100 text-purple-700",
  light: "bg-sky-100 text-sky-700",
  heavy: "bg-stone-200 text-stone-700",
};

export function TagPill({ tag }: { tag: string }) {
  const cls = TAG_STYLES[tag.toLowerCase()] || "bg-gray-100 text-gray-700";
  return <span className={`${cls} rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide`}>{tag}</span>;
}

interface Props {
  dish: Dish;
  inCartQty: number;
  onAdd: () => void;
  onInc: () => void;
  onDec: () => void;
  aiMatch?: boolean;
}

export default function DishCard({ dish, inCartQty, onAdd, onInc, onDec, aiMatch }: Props) {
  const available = dish.is_available !== false;
  const letter = (dish.name?.[0] || "?").toUpperCase();
  return (
    <div className={`relative overflow-hidden rounded-xl border border-brandborder bg-card shadow-sm transition hover:shadow-md ${!available ? "opacity-70" : ""}`}>
      <div className={`relative h-36 bg-gradient-to-br ${dishGradient(dish.name)} flex items-center justify-center`}>
        <span className="text-5xl font-bold text-white drop-shadow">{letter}</span>
        {aiMatch && (
          <span className="absolute top-2 left-2 rounded-full bg-primary px-2 py-0.5 text-[10px] font-bold text-white shadow">
            AI Match
          </span>
        )}
        {!available && (
          <span className="absolute top-2 right-2 rounded-full bg-gray-800 px-2 py-0.5 text-[10px] font-bold text-white">
            Unavailable
          </span>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-textprimary line-clamp-1">{dish.name}</h3>
          <span className="font-bold text-primary">₹{dish.price}</span>
        </div>
        <p className="mt-1 text-xs text-textsecondary line-clamp-2 min-h-[2.5rem]">{dish.description || "—"}</p>
        {dish.tags && dish.tags.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {dish.tags.slice(0, 4).map((t) => <TagPill key={t} tag={t} />)}
          </div>
        )}
        <div className="mt-3">
          {!available ? (
            <button disabled className="w-full rounded-lg bg-gray-200 py-2 text-sm font-semibold text-gray-500">Unavailable</button>
          ) : inCartQty === 0 ? (
            <button onClick={onAdd} className="w-full rounded-lg bg-primary py-2 text-sm font-semibold text-white transition hover:bg-primary-dark">
              Add to Cart
            </button>
          ) : (
            <div className="flex items-center justify-between rounded-lg border border-primary">
              <button onClick={onDec} className="px-4 py-1.5 font-bold text-primary hover:bg-primary-light">−</button>
              <span className="font-semibold text-textprimary">{inCartQty}</span>
              <button onClick={onInc} className="px-4 py-1.5 font-bold text-primary hover:bg-primary-light">+</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function DishCardSkeleton() {
  return (
    <div className="overflow-hidden rounded-xl border border-brandborder bg-card">
      <div className="h-36 animate-pulse bg-gray-200" />
      <div className="space-y-3 p-4">
        <div className="h-4 w-3/4 animate-pulse rounded bg-gray-200" />
        <div className="h-3 w-full animate-pulse rounded bg-gray-200" />
        <div className="h-8 w-full animate-pulse rounded bg-gray-200" />
      </div>
    </div>
  );
}

export type { CartItem };
