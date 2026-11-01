import { LiveStats } from "@/components/LiveStats";

export default function StatsPage() {
  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold text-center mb-4">Live Emergency Statistics</h1>
      <LiveStats />
    </div>
  );
}
