import { useEffect, useState } from "react";
import { apiGet } from "../api";

type Emergency = {
  id: string;
  status: string;
  priority: string;
  is_sos: boolean;
  patient: string;
  fraud_flagged: boolean;
};

export default function Emergencies() {
  const [list, setList] = useState<Emergency[]>([]);

  useEffect(() => {
    const load = () => apiGet("/admin-panel/emergencies/live/").then(setList).catch(() => setList([]));
    load();
    const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  return (
    <div>
      <h1>Emergency Monitoring</h1>
      <table style={{ width: "100%", marginTop: "1rem", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #334155" }}>
            <th style={{ padding: "0.5rem" }}>ID</th>
            <th>Status</th>
            <th>Priority</th>
            <th>SOS</th>
            <th>Fraud</th>
            <th>Patient</th>
          </tr>
        </thead>
        <tbody>
          {list.map((e) => (
            <tr key={e.id} style={{ borderBottom: "1px solid #1e293b" }}>
              <td style={{ padding: "0.5rem", fontFamily: "monospace" }}>{e.id.slice(0, 8)}</td>
              <td>{e.status}</td>
              <td>{e.priority}</td>
              <td>{e.is_sos ? "YES" : "—"}</td>
              <td style={{ color: e.fraud_flagged ? "#f87171" : "#4ade80" }}>{e.fraud_flagged ? "FLAGGED" : "OK"}</td>
              <td>{e.patient}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {list.length === 0 && <p style={{ marginTop: "1rem", color: "#64748b" }}>No active emergencies or API not connected.</p>}
    </div>
  );
}
