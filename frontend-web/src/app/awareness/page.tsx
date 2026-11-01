export default function AwarenessPage() {
  const tips = [
    "Call SOS or 108 immediately in life-threatening situations.",
    "Keep medical history and allergies updated in the app.",
    "Share live location — do not hang up until help arrives.",
    "Learn basic CPR — crowd volunteers may be notified nearby.",
    "Keep emergency contacts updated for family alerts.",
  ];
  return (
    <div className="max-w-2xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Emergency Awareness</h1>
      <ol className="space-y-4 list-decimal pl-6">
        {tips.map((t) => (
          <li key={t} className="text-lg text-slate-700 dark:text-slate-300">{t}</li>
        ))}
      </ol>
    </div>
  );
}
