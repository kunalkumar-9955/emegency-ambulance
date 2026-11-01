import { useState } from "react";
import { apiPost } from "../api";

export default function OTA() {
  const [msg, setMsg] = useState("");

  const push = async () => {
    try {
      await apiPost("/ota/push/", {
        app_name: "patient",
        version: "1.0.1",
        build_number: 101,
        platform: "android",
        update_type: "recommended",
        download_url: "https://example.com/app.apk",
        changelog: "Bug fixes and performance improvements",
      });
      setMsg("OTA update pushed successfully.");
    } catch {
      setMsg("Failed — check admin key and super admin login.");
    }
  };

  return (
    <div>
      <h1>OTA Update Management</h1>
      <p style={{ margin: "1rem 0", color: "#94a3b8" }}>Push instant updates, force critical updates, and rollback versions.</p>
      <div className="card" style={{ maxWidth: 480 }}>
        <button onClick={push}>Push Sample Update (Patient Android)</button>
        <p style={{ marginTop: "1rem" }}>{msg}</p>
      </div>
    </div>
  );
}
