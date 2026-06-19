import { useEffect, useState } from "react";
import { useApp } from "@/contexts/AppContext";
import api from "@/services/api";
import { ORDER_STATUSES } from "@/lib/spice-types";
import { toast } from "sonner";

export default function OrderTracker() {
  const { activeOrder, setActiveOrder } = useApp();
  const [status, setStatus] = useState(activeOrder?.status || "Placed");
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!activeOrder) return;
    let cancelled = false;
    const tick = async () => {
      try {
        const res = await api.get(`/api/orders/${activeOrder.order_id}`);
        if (cancelled) return;
        const s = res.data?.status || status;
        setStatus(s);
        if (s === "Picked Up") setDone(true);
      } catch { /* ignore polling errors */ }
    };
    tick();
    const id = setInterval(tick, 5000);
    return () => { cancelled = true; clearInterval(id); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeOrder?.order_id]);

  if (!activeOrder) return null;
  const idx = ORDER_STATUSES.indexOf(status as any);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/50 p-4 backdrop-blur-sm">
      <div className="my-8 w-full max-w-2xl animate-fade-in rounded-2xl bg-card p-6 shadow-xl md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold text-textprimary">Order #{activeOrder.order_id.slice(0, 8).toUpperCase()}</h2>
            <p className="text-sm text-textsecondary">Live status updates every 5 seconds.</p>
          </div>
          <button onClick={() => setActiveOrder(null)} className="text-2xl leading-none text-textsecondary hover:text-textprimary">×</button>
        </div>

        <div className="mt-8 flex items-center justify-between gap-2">
          {ORDER_STATUSES.map((s, i) => {
            const completed = i < idx;
            const active = i === idx;
            return (
              <div key={s} className="flex flex-1 flex-col items-center text-center">
                <div className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold transition
                  ${completed ? "bg-success text-white" : active ? "bg-primary text-white animate-pulse-ring" : "border-2 border-brandborder bg-card text-textsecondary"}`}>
                  {completed ? "✓" : i + 1}
                </div>
                <span className={`mt-2 text-[11px] font-medium ${active || completed ? "text-textprimary" : "text-textsecondary"}`}>{s}</span>
                {i < ORDER_STATUSES.length - 1 && (
                  <div className={`absolute h-0.5 ${completed ? "bg-success" : "bg-brandborder"}`} style={{ display: "none" }} />
                )}
              </div>
            );
          })}
        </div>

        {done && <FeedbackForm orderId={activeOrder.order_id} />}
      </div>
    </div>
  );
}

function FeedbackForm({ orderId }: { orderId: string }) {
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [submitted, setSubmitted] = useState(false);

  const submit = async () => {
    if (rating === 0) { toast.error("Please give a rating."); return; }
    try {
      await api.post("/api/feedback", { order_id: orderId, rating, comment, photo_urls: [] });
      setSubmitted(true);
      toast.success("Feedback submitted!");
    } catch {
      toast.error("Could not submit feedback.");
    }
  };

  if (submitted) return <div className="mt-8 rounded-xl bg-primary-light p-6 text-center text-lg font-semibold text-primary">Thank you! 🎉</div>;

  return (
    <div className="mt-8 rounded-xl border border-brandborder p-5">
      <h3 className="font-bold text-textprimary">How was your meal?</h3>
      <div className="mt-3 flex gap-1">
        {[1, 2, 3, 4, 5].map((n) => (
          <button key={n} onClick={() => setRating(n)} className="text-2xl transition">
            <span className={n <= rating ? "text-primary" : "text-gray-300"}>★</span>
          </button>
        ))}
      </div>
      <textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Tell us about your experience..."
        className="mt-3 w-full rounded-lg border border-brandborder px-3 py-2 text-sm outline-none focus:border-primary" rows={3} />
      <input type="file" multiple accept="image/*" onChange={(e) => setFiles(Array.from(e.target.files || []))}
        className="mt-3 block w-full text-sm" />
      {files.length > 0 && (
        <div className="mt-2 flex gap-2 overflow-x-auto">
          {files.map((f, i) => <img key={i} src={URL.createObjectURL(f)} alt="" className="h-16 w-16 rounded-lg object-cover" />)}
        </div>
      )}
      <button onClick={submit} className="mt-4 w-full rounded-lg bg-primary py-2 font-semibold text-white hover:bg-primary-dark">
        Submit Feedback
      </button>
    </div>
  );
}
