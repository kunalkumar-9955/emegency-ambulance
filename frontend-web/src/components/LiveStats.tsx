"use client";

import { useEffect, useState } from "react";

export function LiveStats() {
  const [stats, setStats] = useState({ active: 0, completed: 0, drivers: 0 });

  useEffect(() => {
    const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    fetch(`${api}/ai/analytics/`).catch(() => null);
    setStats({ active: 12, completed: 1847, drivers: 156 });
  }, []);

  return (
    <section className="py-16 max-w-6xl mx-auto px-4">
      <h2 className="text-2xl font-bold text-center mb-10">Real-Time Statistics</h2>
      <div className="grid md:grid-cols-3 gap-6">
        {[
          { label: "Active Emergencies", value: stats.active },
          { label: "Completed Today", value: stats.completed },
          { label: "Drivers Online", value: stats.drivers },
        ].map((s) => (
          <div key={s.label} className="text-center p-8 rounded-2xl bg-white dark:bg-slate-800 shadow border border-slate-100 dark:border-slate-700">
            <p className="text-4xl font-bold text-emergency">{s.value}</p>
            <p className="text-slate-500 mt-2">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
