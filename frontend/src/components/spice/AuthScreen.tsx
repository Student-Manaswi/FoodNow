import { useState } from "react";
import { useApp } from "@/contexts/AppContext";
import api from "@/services/api";

export default function AuthScreen() {
  const { login, setScreen } = useApp();
  const [tab, setTab] = useState<"login" | "signup">("login");

  // login state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginErr, setLoginErr] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  // signup state
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [sEmail, setSEmail] = useState("");
  const [sPass, setSPass] = useState("");
  const [sConfirm, setSConfirm] = useState("");
  const [sRole, setSRole] = useState<"customer" | "admin">("customer");
  const [sErr, setSErr] = useState("");
  const [sLoading, setSLoading] = useState(false);

  const submitLogin = async (role: "customer" | "admin") => {
    if (!email.trim() || !password.trim()) {
      setLoginErr("Please fill in all fields.");
      return;
    }
    setLoginErr("");
    setLoginLoading(true);
    try {
      const res = await api.post("/api/auth/login", { email, password });
      const { access_token, role: serverRole } = res.data;
      // store token for all future requests
      localStorage.setItem("token", access_token);
      api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
      const displayName = email.split("@")[0];
      login({
        name: displayName.charAt(0).toUpperCase() + displayName.slice(1),
        email,
        role: serverRole || role,
      });
    } catch (err: any) {
      const msg = err?.response?.data?.detail || "Invalid email or password.";
      setLoginErr(msg);
    } finally {
      setLoginLoading(false);
    }
  };

  const submitSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !sEmail || !sPass || !sConfirm) {
      setSErr("Please fill in all fields.");
      return;
    }
    if (sPass !== sConfirm) {
      setSErr("Passwords do not match.");
      return;
    }
    setSErr("");
    setSLoading(true);
    try {
      await api.post("/api/auth/register", {
        name,
        email: sEmail,
        password: sPass,
        phone: phone || "+91-0000000000",
        role: sRole,
      });
      // after register, auto login
      const res = await api.post("/api/auth/login", { email: sEmail, password: sPass });
      const { access_token, role: serverRole } = res.data;
      localStorage.setItem("token", access_token);
      api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
      login({ name, email: sEmail, role: serverRole || sRole });
    } catch (err: any) {
      const msg = err?.response?.data?.detail || "Registration failed. Try again.";
      setSErr(msg);
    } finally {
      setSLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center bg-darkbg px-4 py-10">
      <div className="absolute inset-0 dot-grid opacity-50" />
      <div className="relative w-full max-w-md animate-fade-in rounded-2xl bg-card p-8 shadow-xl">
        <button
          onClick={() => setScreen("landing")}
          className="text-xs text-textsecondary hover:text-primary mb-4"
        >
          ← Back to home
        </button>
        <h1 className="text-center text-2xl font-bold text-primary">SpiceRoute</h1>

        <div className="mt-6 flex border-b border-brandborder">
          {(["login", "signup"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-sm font-medium transition ${tab === t ? "border-b-2 border-primary text-primary" : "text-textsecondary"}`}
            >
              {t === "login" ? "Login" : "Sign Up"}
            </button>
          ))}
        </div>

        {tab === "login" ? (
          <div className="mt-6 space-y-4">
            <input
              type="email"
              placeholder="you@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <input
              type="password"
              placeholder="Your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            {loginErr && <p className="text-sm text-red-500">{loginErr}</p>}
            <button
              onClick={() => submitLogin("customer")}
              disabled={loginLoading}
              className="w-full rounded-lg bg-primary py-2.5 font-semibold text-white transition hover:bg-primary-dark disabled:opacity-60"
            >
              {loginLoading ? "Logging in..." : "Login as Customer"}
            </button>
            <button
              onClick={() => submitLogin("admin")}
              disabled={loginLoading}
              className="w-full rounded-lg border border-primary py-2.5 font-semibold text-primary transition hover:bg-primary-light disabled:opacity-60"
            >
              {loginLoading ? "Logging in..." : "Login as Admin"}
            </button>
          </div>
        ) : (
          <form onSubmit={submitSignup} className="mt-6 space-y-4">
            <input
              placeholder="Your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <input
              type="email"
              placeholder="you@email.com"
              value={sEmail}
              onChange={(e) => setSEmail(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <input
              placeholder="Phone (optional)"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <input
              type="password"
              placeholder="Password"
              value={sPass}
              onChange={(e) => setSPass(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <input
              type="password"
              placeholder="Confirm password"
              value={sConfirm}
              onChange={(e) => setSConfirm(e.target.value)}
              className="w-full rounded-lg border border-brandborder bg-card px-4 py-2.5 text-sm outline-none focus:border-primary"
            />
            <div className="flex gap-4 text-sm">
              {(["customer", "admin"] as const).map((r) => (
                <label key={r} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="role"
                    checked={sRole === r}
                    onChange={() => setSRole(r)}
                    className="accent-[#E85D24]"
                  />
                  I'm a {r === "customer" ? "Customer" : "Admin"}
                </label>
              ))}
            </div>
            {sErr && <p className="text-sm text-red-500">{sErr}</p>}
            <button
              type="submit"
              disabled={sLoading}
              className="w-full rounded-lg bg-primary py-2.5 font-semibold text-white transition hover:bg-primary-dark disabled:opacity-60"
            >
              {sLoading ? "Creating account..." : "Create Account"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
