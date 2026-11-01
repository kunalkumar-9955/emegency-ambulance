export default function HospitalsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-6">Hospital Partnership</h1>
      <ul className="space-y-4 text-slate-600 dark:text-slate-300 list-disc pl-6">
        <li>Ambulance fleet management dashboard</li>
        <li>ICU and bed availability APIs</li>
        <li>Patient arrival tracking with live ETA</li>
        <li>Staff management and emergency analytics</li>
        <li>Encrypted pre-arrival health data sharing</li>
      </ul>
      <form className="mt-10 space-y-4">
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Hospital name" />
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Contact email" />
        <button type="button" className="bg-medical text-white px-6 py-3 rounded-lg font-semibold">Request Partnership</button>
      </form>
    </div>
  );
}
