import { createContext, useContext, useState, useCallback, useMemo, type ReactNode } from "react";
import type { User, Role, Screen, CartItem, ActiveOrder, Dish } from "@/lib/spice-types";

interface AppCtx {
  screen: Screen;
  setScreen: (s: Screen) => void;
  user: User | null;
  login: (u: User) => void;
  logout: () => void;

  cart: CartItem[];
  addItem: (d: Dish) => void;
  removeItem: (id: string) => void;
  updateQty: (id: string, q: number) => void;
  clearCart: () => void;
  cartTotal: number;
  cartCount: number;

  activeOrder: ActiveOrder | null;
  setActiveOrder: (o: ActiveOrder | null) => void;
}

const Ctx = createContext<AppCtx | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [screen, setScreen] = useState<Screen>("landing");
  const [user, setUser] = useState<User | null>(null);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [activeOrder, setActiveOrder] = useState<ActiveOrder | null>(null);

  const login = useCallback((u: User) => {
    setUser(u);
    setScreen(u.role === "admin" ? "admin" : "customer");
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setCart([]);
    setActiveOrder(null);
    setScreen("landing");
  }, []);

  const addItem = useCallback((d: Dish) => {
    setCart((c) => {
      const existing = c.find((i) => i.dish_id === d.dish_id);
      if (existing) return c.map((i) => i.dish_id === d.dish_id ? { ...i, quantity: i.quantity + 1 } : i);
      return [...c, { dish_id: d.dish_id, name: d.name, price: d.price, quantity: 1, tags: d.tags }];
    });
  }, []);

  const removeItem = useCallback((id: string) => setCart((c) => c.filter((i) => i.dish_id !== id)), []);
  const updateQty = useCallback((id: string, q: number) => {
    setCart((c) => q <= 0 ? c.filter((i) => i.dish_id !== id) : c.map((i) => i.dish_id === id ? { ...i, quantity: q } : i));
  }, []);
  const clearCart = useCallback(() => setCart([]), []);

  const cartTotal = useMemo(() => cart.reduce((s, i) => s + i.price * i.quantity, 0), [cart]);
  const cartCount = useMemo(() => cart.reduce((s, i) => s + i.quantity, 0), [cart]);

  const value: AppCtx = {
    screen, setScreen, user, login, logout,
    cart, addItem, removeItem, updateQty, clearCart, cartTotal, cartCount,
    activeOrder, setActiveOrder,
  };

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useApp() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
