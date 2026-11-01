export default function DriversPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-6">Become an Ambulance Driver</h1>
      <p className="text-slate-600 dark:text-slate-300 mb-8">
        Join our network. Accept emergencies, navigate with AI routes, track earnings, and save lives.
      </p>
      <form className="space-y-4">
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Full name" />
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Phone" />
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="License number" />
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="City" />
        <button type="button" className="bg-emergency text-white px-6 py-3 rounded-lg font-semibold w-full">
          Apply Now
        </button>
      </form>
    </div>
  );
}
