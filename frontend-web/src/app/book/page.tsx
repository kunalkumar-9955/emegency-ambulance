"use client";

import { useState } from "react";

export default function BookPage() {
  const [status, setStatus] = useState<string | null>(null);

  const handleSOS = async () => {
    setStatus("Requesting location...");
    if (!navigator.geolocation) {
      setStatus("Geolocation not supported. Call 108.");
      return;
    }
    navigator.geolocation.getCurrentPosition(async (pos) => {
      setStatus("Sending SOS...");
      const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch(`${api}/emergencies/sos/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify({
            pickup_latitude: pos.coords.latitude,
            pickup_longitude: pos.coords.longitude,
            is_sos: true,
            symptoms: "Web SOS",
          }),
        });
        if (res.ok) {
          const data = await res.json();
          setStatus(`Emergency created. ID: ${data.id?.slice(0, 8)}...`);
        } else {
          setStatus("Login required in mobile app for full SOS. Call 108 immediately.");
        }
      } catch {
        setStatus("Network error. Call 108 / 102 immediately.");
      }
    });
  };

  return (
    <div className="max-w-lg mx-auto px-4 py-20 text-center">
      <h1 className="text-3xl font-bold mb-4">Emergency Booking</h1>
      <p className="text-slate-600 dark:text-slate-300 mb-10">
        Press SOS to share your live location and dispatch the nearest ambulance.
      </p>
      <button
        onClick={handleSOS}
        className="sos-pulse w-48 h-48 rounded-full bg-emergency text-white text-2xl font-bold shadow-2xl mx-auto block hover:bg-emergency-dark"
      >
        SOS
      </button>
      {status && <p className="mt-8 text-medical font-medium">{status}</p>}
      <p className="mt-6 text-sm text-slate-500">For life-threatening emergencies, also call national helpline 108.</p>
    </div>
  );
}
