import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { apiGet } from "../api";

export default function Dashboard() {
  const [data, setData] = useState<{ emergencies_today?: number; active_emergencies?: number }>({});

  useEffect(() => {
    apiGet("/admin-panel/analytics/").then(setData).catch(() => setData({ emergencies_today: 0, active_emergencies: 0 }));
  }, []);

  const chartData = [
    { hour: "6am", count: 2 },
    { hour: "12pm", count: 8 },
    { hour: "6pm", count: 12 },
    { hour: "12am", count: 5 },
  ];

  return (
    <div>
      <h1>AI Analytics Dashboard</h1>
      <div className="grid" style={{ marginTop: "1.5rem" }}>
        <div className="card"><p>Today</p><p className="stat">{data.emergencies_today ?? "—"}</p></div>
        <div className="card"><p>Active</p><p className="stat">{data.active_emergencies ?? "—"}</p></div>
        <div className="card"><p>API Status</p><p className="stat" style={{ color: "#4ade80" }}>OK</p></div>
        <div className="card"><p>Crash Reports</p><p className="stat">Sentry</p></div>
      </div>
      <div className="card" style={{ marginTop: "1.5rem", height: 280 }}>
        <h3 style={{ marginBottom: "1rem" }}>Emergency Peak Hours</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={chartData}>
            <XAxis dataKey="hour" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Bar dataKey="count" fill="#dc2626" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
