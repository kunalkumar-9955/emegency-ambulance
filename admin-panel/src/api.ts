const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";
const ADMIN_KEY = import.meta.env.VITE_ADMIN_PANEL_KEY || "local-admin-secret-change-me";

export function getHeaders(): HeadersInit {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    "X-Admin-Panel-Key": ADMIN_KEY,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function apiGet(path: string) {
  const res = await fetch(`${API}${path}`, { headers: getHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiPost(path: string, body: unknown) {
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${API.replace("/api/v1", "")}/api/v1/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  if (data.access) {
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
  }
  return data;
}
