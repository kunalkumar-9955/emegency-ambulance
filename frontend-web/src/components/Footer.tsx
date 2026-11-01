import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-700 py-10 mt-16">
      <div className="max-w-6xl mx-auto px-4 grid md:grid-cols-3 gap-8 text-sm text-slate-600 dark:text-slate-400">
        <div>
          <p className="font-semibold text-slate-900 dark:text-white mb-2">Emergency Ambulance</p>
          <p>AI-powered emergency response for everyone.</p>
        </div>
        <div className="flex flex-col gap-2">
          <Link href="/awareness">Emergency Awareness</Link>
          <Link href="/hospitals">Hospital Partnership</Link>
          <Link href="/drivers">Driver Registration</Link>
        </div>
        <div>
          <p>24/7 Emergency Hotline</p>
          <p className="text-2xl font-bold text-emergency">108 / 102</p>
        </div>
      </div>
    </footer>
  );
}
