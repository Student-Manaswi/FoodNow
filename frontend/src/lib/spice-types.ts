export type Role = "customer" | "admin";
export type Screen = "landing" | "auth" | "customer" | "admin";

export interface User {
  name: string;
  email: string;
  phone?: string;
  role: Role;
}

export interface Dish {
  dish_id: string;
  name: string;
  description?: string;
  category?: string;
  price: number;
  tags?: string[];
  is_available?: boolean;
}

export interface CartItem {
  dish_id: string;
  name: string;
  price: number;
  quantity: number;
  tags?: string[];
}

export interface ActiveOrder {
  order_id: string;
  status: string;
}

export interface DashboardData {
  total_revenue: number;
  active_orders: number;
  popular_items: Array<{ name: string; count?: number; orders?: number }>;
  avg_rating: number;
}

export interface OrderData {
  order_id?: string;
  _id?: string;
  id?: string;
  customer_name: string;
  phone?: string;
  items: Array<{
    dish_id?: string;
    name?: string;
    dish_name?: string;
    quantity: number;
    price?: number;
    unit_price?: number;
  }>;
  total_price: number;
  status: string;
}

export interface FeedbackItem {
  order_id: string;
  rating: number;
  comment: string;
  created_at?: string;
  timestamp?: string;
  photo_urls?: string[];
}

export const CATEGORIES = ["All", "Appetizers", "Mains", "Desserts", "Beverages"] as const;
export const TAG_OPTIONS = [
  "vegetarian",
  "non-vegetarian",
  "spicy",
  "healthy",
  "vegan",
  "light",
  "heavy",
] as const;
export const ORDER_STATUSES = ["Placed", "Confirmed", "Preparing", "Ready", "Picked Up"] as const;
