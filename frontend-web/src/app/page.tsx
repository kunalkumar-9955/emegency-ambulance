import Link from "next/link";
import { Activity, Clock, MapPin, Shield } from "lucide-react";
import { LiveStats } from "@/components/LiveStats";
import { Testimonials } from "@/components/Testimonials";

export default function HomePage() {
  return (
    <>
      <section className="relative overflow-hidden bg-gradient-to-br from-red-50 via-white to-sky-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 py-20">
        <div className="max-w-6xl mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <p className="text-medical font-semibold text-sm mb-2">AI-Powered Emergency Response</p>
            <h1 className="text-4xl md:text-5xl font-bold leading-tight mb-6">
              One tap. <span className="text-emergency">Nearest ambulance.</span> Live tracking.
            </h1>
            <p className="text-lg text-slate-600 dark:text-slate-300 mb-8">
              Smart dispatch, hospital coordination, encrypted medical communication, and real-time ETA — built for real emergencies.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                href="/book"
                className="sos-pulse bg-emergency text-white text-lg px-8 py-4 rounded-2xl font-bold shadow-lg hover:bg-emergency-dark"
              >
                Emergency SOS
              </Link>
              <Link href="/drivers" className="border-2 border-medical text-medical px-6 py-4 rounded-2xl font-semibold hover:bg-sky-50 dark:hover:bg-slate-800">
                Register as Driver
              </Link>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {[
              { icon: Clock, label: "Avg Response", value: "< 8 min" },
              { icon: MapPin, label: "Live Tracking", value: "Real-time" },
              { icon: Shield, label: "E2E Encrypted", value: "Medical data" },
              { icon: Activity, label: "AI Dispatch", value: "Smart match" },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} className="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700">
                <Icon className="text-medical mb-2" size={28} />
                <p className="text-2xl font-bold">{value}</p>
                <p className="text-sm text-slate-500">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <LiveStats />
      <Testimonials />

      <section className="py-16 bg-medical text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Hospital Partnership Program</h2>
          <p className="mb-6 opacity-90">Fleet management, ICU availability, patient arrival tracking, and AI analytics.</p>
          <Link href="/hospitals" className="inline-block bg-white text-medical px-8 py-3 rounded-full font-semibold">
            Partner With Us
          </Link>
        </div>
      </section>
    </>
  );
}
