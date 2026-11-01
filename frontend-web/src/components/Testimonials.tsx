const items = [
  { name: "Priya S.", text: "Ambulance arrived in 6 minutes. Live tracking kept my family calm.", city: "Mumbai" },
  { name: "Rajesh K.", text: "Driver was professional. Hospital was already alerted before arrival.", city: "Delhi" },
  { name: "Anita M.", text: "SOS button is large and easy — my mother used it without help.", city: "Bangalore" },
];

export function Testimonials() {
  return (
    <section className="py-16 bg-slate-50 dark:bg-slate-800/50">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-2xl font-bold text-center mb-10">Trusted in Emergencies</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {items.map((t) => (
            <blockquote key={t.name} className="p-6 bg-white dark:bg-slate-800 rounded-2xl shadow-sm">
              <p className="text-slate-600 dark:text-slate-300 mb-4">&ldquo;{t.text}&rdquo;</p>
              <footer className="font-semibold">{t.name} — {t.city}</footer>
            </blockquote>
          ))}
        </div>
      </div>
    </section>
  );
}
