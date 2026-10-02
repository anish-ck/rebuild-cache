'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchProfile, resetSystem } from '../lib/api';
import { useState } from 'react';

export default function ProfileHeader() {
  const { data, refetch } = useQuery({
    queryKey: ['profile'],
    queryFn: fetchProfile,
  });
  
  const [isResetting, setIsResetting] = useState(false);

  const handleReset = async () => {
    setIsResetting(true);
    try {
      await resetSystem();
      await refetch();
      // Optionally trigger reload for reels if needed
      window.location.reload();
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 flex items-center justify-between shadow-lg">
      <div className="flex items-center gap-6">
        <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 flex items-center justify-center text-3xl font-bold border-4 border-gray-950">
          {data?.username?.charAt(0).toUpperCase() || 'T'}
        </div>
        
        <div>
          <h1 className="text-2xl font-bold">{data?.username || 'Loading...'}</h1>
          <div className="flex gap-6 mt-3 text-sm text-gray-400">
            <div className="flex flex-col">
              <span className="text-white font-semibold text-lg">{data?.total_reels ? data.total_reels.toLocaleString() : '0'}</span>
              <span>Posts</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white font-semibold text-lg">1.2M</span>
              <span>Followers</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white font-semibold text-lg">342</span>
              <span>Following</span>
            </div>
          </div>
        </div>
      </div>
      
      <button 
        onClick={handleReset}
        disabled={isResetting}
        className="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/20 rounded-lg transition-colors font-medium disabled:opacity-50"
      >
        {isResetting ? 'Resetting...' : 'Reset System'}
      </button>
    </div>
  );
}
