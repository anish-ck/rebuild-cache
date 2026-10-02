'use client';

export default function StorageStats({
  hot,
  warm,
  cold
}: {
  hot: number;
  warm: number;
  cold: number;
}) {
  const total = hot + warm + cold || 1; // Prevent division by zero
  const hotPct = (hot / total) * 100;
  const warmPct = (warm / total) * 100;
  const coldPct = (cold / total) * 100;

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
      <h3 className="text-sm font-semibold mb-4 text-gray-300">Storage Tiers Distribution</h3>
      
      {/* Visual Bar */}
      <div className="h-4 w-full bg-gray-800 rounded-full flex overflow-hidden mb-4">
        <div style={{ width: `${hotPct}%` }} className="bg-red-500 transition-all duration-500" />
        <div style={{ width: `${warmPct}%` }} className="bg-yellow-500 transition-all duration-500" />
        <div style={{ width: `${coldPct}%` }} className="bg-blue-500 transition-all duration-500" />
      </div>
      
      {/* Legend & Stats */}
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse-dot" />
            <span className="text-sm text-gray-300">HOT (Redis)</span>
          </div>
          <span className="font-mono text-sm">{hot.toLocaleString()}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span className="text-sm text-gray-300">WARM (SSD)</span>
          </div>
          <span className="font-mono text-sm">{warm.toLocaleString()}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span className="text-sm text-gray-300">COLD (HDD)</span>
          </div>
          <span className="font-mono text-sm">{cold.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
}
