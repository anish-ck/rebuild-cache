'use client';

import { Reel } from '../lib/types';
import { formatTimeAgo } from '../lib/utils';

export default function ReelCard({ reel }: { reel: Reel }) {
  const formatCount = (count: number) => {
    if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M';
    if (count >= 1000) return (count / 1000).toFixed(1) + 'K';
    return count.toString();
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'HOT': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'WARM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      case 'COLD': return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/50';
    }
  };

  const gradients = [
    'from-red-500 to-orange-500',
    'from-blue-500 to-cyan-500',
    'from-green-500 to-emerald-500',
    'from-purple-500 to-pink-500',
    'from-yellow-400 to-orange-500',
    'from-indigo-500 to-purple-500',
    'from-pink-500 to-rose-500',
    'from-teal-400 to-emerald-500',
    'from-cyan-500 to-blue-500',
    'from-fuchsia-500 to-pink-500',
  ];
  const bgGradient = gradients[reel.id % gradients.length];

  return (
    <div className="bg-gray-900 rounded-xl overflow-hidden border border-gray-800 shadow-lg group hover:scale-[1.02] transition-transform duration-200">
      <div className={`h-48 w-full bg-gradient-to-br ${bgGradient} relative flex items-center justify-center`}>
        {/* Play Icon Placeholder */}
        <div className="w-12 h-12 rounded-full bg-black/40 flex items-center justify-center backdrop-blur-sm border border-white/10 group-hover:bg-black/60 transition-colors">
          <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
        
        {/* Tier Badge */}
        <div className={`absolute top-3 right-3 px-2 py-1 rounded text-xs font-bold border backdrop-blur-md ${getTierColor(reel.storage_tier)}`}>
          {reel.storage_tier}
        </div>
        
        {/* Views */}
        <div className="absolute bottom-3 left-3 flex items-center text-white/90 text-sm font-medium drop-shadow-md">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          {formatCount(reel.view_count)}
        </div>
      </div>
      
      <div className="p-4">
        <p className="text-sm text-gray-200 line-clamp-2 mb-2">
          {reel.caption}
        </p>
        <div className="flex justify-between items-center text-xs text-gray-500 mt-3 pt-3 border-t border-gray-800">
          <span>{formatTimeAgo(reel.created_at)}</span>
          <span className="font-mono bg-gray-950 px-2 py-1 rounded text-gray-400">#{reel.id}</span>
        </div>
      </div>
    </div>
  );
}
