"use client";

import Link from "next/link";
import { Ambulance, Moon, Sun } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [dark, setDark] = useState(false);

  const toggle = () => {
    setDark(!dark);
    document.documentElement.classList.toggle("dark");
  };

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-900/90 backdrop-blur">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <Ambulance className="text-emergency" />
          <span>Emergency<span className="text-medical">Ambulance</span></span>
        </Link>
        <nav className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/book">Book Emergency</Link>
          <Link href="/hospitals">Hospitals</Link>
          <Link href="/drivers">Become a Driver</Link>
          <Link href="/stats">Live Stats</Link>
          <Link href="/contact">Contact</Link>
        </nav>
        <div className="flex items-center gap-3">
          <button onClick={toggle} aria-label="Toggle theme" className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <Link href="/book" className="bg-emergency text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-emergency-dark">
            SOS
          </Link>
        </div>
      </div>
    </header>
  );
}
