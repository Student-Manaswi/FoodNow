import { createFileRoute } from "@tanstack/react-router";
import { Toaster } from "sonner";
import { AppProvider, useApp } from "@/contexts/AppContext";
import Landing from "@/components/spice/Landing";
import AuthScreen from "@/components/spice/AuthScreen";
import CustomerApp from "@/components/spice/CustomerApp";
import AdminApp from "@/components/spice/AdminApp";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SpiceRoute — Order Food the Way You Think About It" },
      { name: "description", content: "AI-powered restaurant ordering with real-time tracking and smart recommendations." },
      { property: "og:title", content: "SpiceRoute" },
      { property: "og:description", content: "Type what you're craving — our AI finds the perfect dish." },
    ],
  }),
  component: Page,
});

function Page() {
  return (
    <AppProvider>
      <ScreenSwitch />
      <Toaster position="bottom-right" richColors closeButton />
    </AppProvider>
  );
}

function ScreenSwitch() {
  const { screen } = useApp();
  return (
    <div key={screen} className="animate-fade-in">
      {screen === "landing" && <Landing />}
      {screen === "auth" && <AuthScreen />}
      {screen === "customer" && <CustomerApp />}
      {screen === "admin" && <AdminApp />}
    </div>
  );
}
