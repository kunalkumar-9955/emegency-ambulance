import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../api";

export default function System() {
  const [health, setHealth] = useState<Record<string, unknown>>({});

  useEffect(() => {
    apiGet("/admin-panel/system/health/").then(setHealth).catch(() => setHealth({ database: "unknown" }));
  }, []);

  const backup = async () => {
    const r = await apiPost("/admin-panel/backup/trigger/", {});
    alert(`Backup queued: ${r.task_id}`);
  };

  return (
    <div>
      <h1>System Monitoring</h1>
      <div className="grid" style={{ marginTop: "1.5rem" }}>
        <div className="card">
          <p>Database</p>
          <p className="stat" style={{ color: health.database === "ok" ? "#4ade80" : "#f87171" }}>
            {String(health.database || "—")}
          </p>
        </div>
        <div className="card">
          <p>Audit Logs (24h)</p>
          <p className="stat">{String(health.audit_logs_24h ?? "—")}</p>
        </div>
      </div>
      <div className="card" style={{ marginTop: "1.5rem" }}>
        <h3>Backup & Recovery</h3>
        <button style={{ marginTop: "1rem" }} onClick={backup}>Trigger Backup</button>
      </div>
      <div className="card" style={{ marginTop: "1rem" }}>
        <h3>Crash Monitoring</h3>
        <p style={{ marginTop: "0.5rem", color: "#94a3b8" }}>Integrate Sentry DSN and Firebase Crashlytics in production.</p>
      </div>
    </div>
  );
}
