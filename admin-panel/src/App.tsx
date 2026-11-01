import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import { useState } from "react";
import { login } from "./api";
import Dashboard from "./pages/Dashboard";
import Emergencies from "./pages/Emergencies";
import OTA from "./pages/OTA";
import System from "./pages/System";

function Login({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("admin@emergency.local");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      onLogin();
    } catch {
      setErr("Login failed. Use super admin credentials.");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "4rem auto", padding: "2rem" }} className="card">
      <h1 style={{ marginBottom: "0.5rem" }}>Super Admin</h1>
      <p className="warn">Localhost only. Encrypted admin access required.</p>
      <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Secure Login</button>
      </form>
      {err && <p style={{ color: "#f87171", marginTop: "0.5rem" }}>{err}</p>}
    </div>
  );
}

export default function App() {
  const [authed, setAuthed] = useState(!!localStorage.getItem("access_token"));

  if (!authed) return <Login onLogin={() => setAuthed(true)} />;

  return (
    <BrowserRouter>
      <div className="layout">
        <aside className="sidebar">
          <h2 style={{ fontSize: "1rem", marginBottom: "1.5rem", color: "#f87171" }}>Emergency Admin</h2>
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/emergencies">Live Emergencies</NavLink>
          <NavLink to="/ota">OTA Updates</NavLink>
          <NavLink to="/system">System & Backup</NavLink>
        </aside>
        <main className="main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/emergencies" element={<Emergencies />} />
            <Route path="/ota" element={<OTA />} />
            <Route path="/system" element={<System />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
