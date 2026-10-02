'use client';

import { useStats } from '../hooks/useStats';
import { useReels } from '../hooks/useReels';
import CacheStats from './CacheStats';
import StorageStats from './StorageStats';
import EventLog from './EventLog';

export default function SystemMonitor() {
  const { stats, events } = useStats();
  const { reels, cacheStats: clientCacheStats } = useReels();

  if (!stats) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        <div className="animate-pulse">Loading system monitor...</div>
      </div>
    );
  }

  const redisHitRate = stats.redis_hits + stats.redis_misses > 0 
    ? ((stats.redis_hits / (stats.redis_hits + stats.redis_misses)) * 100).toFixed(1) + '%' 
    : '0%';

  return (
    <div className="flex flex-col gap-4 h-full">
      <div className="bg-gray-900 rounded-xl p-4 border border-gray-800 shadow-lg">
        <div className="flex items-center gap-2 mb-2">
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <h2 className="text-lg font-bold">System Monitor</h2>
        </div>
        <p className="text-xs text-gray-500">Real-time architecture telemetry</p>
      </div>

      <CacheStats 
        title="Client Cache (LRU)" 
        colorTheme="purple"
        stats={[
          { label: 'Capacity', value: `${clientCacheStats.size} / ${clientCacheStats.maxSize}` },
          { label: 'Evictions', value: clientCacheStats.evictions },
          { label: 'Hits', value: clientCacheStats.hits },
          { label: 'Misses', value: clientCacheStats.misses },
        ]} 
      />

      <CacheStats 
        title="Backend Redis Cache" 
        colorTheme="blue"
        stats={[
          { label: 'Hit Rate', value: redisHitRate },
          { label: 'Sets', value: stats.redis_sets },
          { label: 'Hits', value: stats.redis_hits },
          { label: 'Misses', value: stats.redis_misses },
        ]} 
      />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h3 className="text-sm font-semibold mb-2 text-gray-300">Database</h3>
          <div className="text-2xl font-bold">{stats.db_queries.toLocaleString()}</div>
          <div className="text-xs text-gray-500">Queries executed</div>
          
          <div className="mt-3 text-sm font-medium text-blue-400">
            {stats.avg_db_latency_ms.toFixed(1)}ms avg latency
          </div>
        </div>
        
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h3 className="text-sm font-semibold mb-2 text-gray-300">Prefetcher</h3>
          <div className="text-2xl font-bold text-yellow-500">{stats.prefetch_requests.toLocaleString()}</div>
          <div className="text-xs text-gray-500">Background loads</div>
        </div>
      </div>

      <StorageStats 
        hot={stats.hot_storage_requests} 
        warm={stats.warm_storage_requests} 
        cold={stats.cold_storage_requests} 
      />

      <div className="flex-1 min-h-[250px]">
        <EventLog events={events} />
      </div>
    </div>
  );
}
