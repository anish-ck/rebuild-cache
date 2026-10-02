'use client';

export default function CacheStats({
  title,
  stats,
  colorTheme
}: {
  title: string;
  stats: { label: string; value: string | number; subValue?: string }[];
  colorTheme: 'blue' | 'purple' | 'green';
}) {
  const themes = {
    blue: 'border-blue-500/30 bg-blue-500/5',
    purple: 'border-purple-500/30 bg-purple-500/5',
    green: 'border-green-500/30 bg-green-500/5',
  };

  const headerColors = {
    blue: 'text-blue-400',
    purple: 'text-purple-400',
    green: 'text-green-400',
  };

  return (
    <div className={`rounded-xl border p-4 ${themes[colorTheme]}`}>
      <h3 className={`text-sm font-semibold mb-3 ${headerColors[colorTheme]}`}>{title}</h3>
      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat, i) => (
          <div key={i} className="bg-gray-900/50 rounded-lg p-2 border border-gray-800">
            <div className="text-xs text-gray-400 mb-1">{stat.label}</div>
            <div className="flex items-baseline gap-2">
              <span className="text-lg font-bold text-gray-100">
                {typeof stat.value === 'number' ? stat.value.toLocaleString() : stat.value}
              </span>
              {stat.subValue && (
                <span className="text-xs text-gray-500">{stat.subValue}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
