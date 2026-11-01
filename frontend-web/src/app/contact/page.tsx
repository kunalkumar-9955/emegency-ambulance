export default function ContactPage() {
  return (
    <div className="max-w-xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-6">Contact Us</h1>
      <p className="mb-4">Email: support@emergencyambulance.com</p>
      <p className="mb-8">Emergency: 108 / 102 (India)</p>
      <form className="space-y-4">
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Your name" />
        <input className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" placeholder="Email" />
        <textarea className="w-full border rounded-lg px-4 py-3 dark:bg-slate-800" rows={4} placeholder="Message" />
        <button type="button" className="bg-medical text-white px-6 py-3 rounded-lg font-semibold w-full">Send</button>
      </form>
    </div>
  );
}
