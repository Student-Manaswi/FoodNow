import { useApp } from "@/contexts/AppContext";

export default function Landing() {
  const { setScreen } = useApp();
  return (
    <div className="min-h-screen bg-surface">
      {/* HERO */}
      <section className="relative bg-darkbg text-white">
        <div className="absolute inset-0 dot-grid opacity-60" />
        <div className="relative mx-auto max-w-5xl px-6 py-24 md:py-32 flex flex-col items-center text-center">
          <span className="animate-fade-in inline-flex items-center gap-2 rounded-full border border-primary px-4 py-1.5 text-sm text-primary">
            🍽 Introducing SpiceRoute
          </span>
          <h1 className="animate-fade-in mt-6 text-4xl md:text-6xl font-bold leading-tight" style={{ animationDelay: "150ms" }}>
            Order Food the Way<br />
            You <span className="text-primary">Think About It.</span>
          </h1>
          <p className="animate-fade-in mt-6 max-w-xl text-base md:text-lg text-textsecondary" style={{ animationDelay: "300ms" }}>
            Type exactly what you're craving — "something light and not fried" — and our AI finds the perfect dish for you.
          </p>
          <div className="animate-fade-in mt-8 flex flex-wrap items-center justify-center gap-3" style={{ animationDelay: "450ms" }}>
            <button onClick={() => setScreen("auth")} className="rounded-lg bg-primary px-6 py-3 font-semibold text-white transition hover:bg-primary-dark">
              Get Started
            </button>
            <a href="#features" className="rounded-lg border border-primary px-6 py-3 font-semibold text-primary transition hover:bg-primary hover:text-white">
              See How It Works
            </a>
          </div>
          <p className="animate-fade-in mt-6 text-sm text-textsecondary" style={{ animationDelay: "600ms" }}>
            AI-powered search · Real-time order tracking · Smart recommendations
          </p>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="bg-card py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-6 md:grid-cols-3">
            {[
              { icon: "🔍", bg: "bg-primary-light", iconColor: "text-primary", title: "Talk to the Menu",
                body: "Type natural language like 'spicy non-veg under ₹250'. Our AI understands what you mean, not just what you type." },
              { icon: "🌶️", bg: "bg-orange-100", iconColor: "text-orange-600", title: "Smart Pairings",
                body: "Added something spicy? We'll suggest a cooling drink before you even think to look for one." },
              { icon: "📍", bg: "bg-green-100", iconColor: "text-success", title: "Track Every Step",
                body: "Watch your order move from kitchen to table in real time — no guessing, no refreshing." },
            ].map((f) => (
              <div key={f.title} className="rounded-xl border border-brandborder bg-card p-6 shadow-sm">
                <div className={`${f.bg} ${f.iconColor} mb-4 inline-flex h-12 w-12 items-center justify-center rounded-full text-2xl`}>{f.icon}</div>
                <h3 className="text-lg font-bold text-textprimary">{f.title}</h3>
                <p className="mt-2 text-sm text-textsecondary">{f.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="bg-surface py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-center text-3xl font-bold text-textprimary">How It Works</h2>
          <div className="mt-12 flex flex-col items-center gap-8 md:flex-row md:justify-between">
            {[
              { n: "1", t: "Search with AI", d: "Tell us what you're craving." },
              { n: "2", t: "Add to Cart", d: "Pick your favorites in seconds." },
              { n: "3", t: "Track & Enjoy", d: "Watch it arrive in real time." },
            ].map((s, i) => (
              <div key={s.n} className="flex items-center gap-6">
                <div className="text-center">
                  <div className="text-5xl font-bold text-primary">{s.n}</div>
                  <div className="mt-2 font-semibold text-textprimary">{s.t}</div>
                  <div className="mt-1 text-sm text-textsecondary">{s.d}</div>
                </div>
                {i < 2 && <div className="hidden md:block text-3xl text-primary">→</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="bg-darkbg py-20 text-center text-white">
        <h2 className="text-3xl md:text-4xl font-bold">Ready to order smarter?</h2>
        <button onClick={() => setScreen("auth")} className="mt-8 rounded-lg bg-primary px-8 py-3 font-semibold text-white transition hover:bg-primary-dark">
          Order Now
        </button>
        <p className="mt-4 text-sm text-textsecondary">No account needed for demo · Switch between Customer & Admin views</p>
      </section>
    </div>
  );
}
