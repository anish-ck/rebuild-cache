'use client';

import { useInfiniteQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';
import { fetchReels, reportClientStats } from '../lib/api';
import { LRUCache } from '../lib/lru-cache';
import { ReelListResponse } from '../lib/types';

// Global cache instance for reels
export const reelCache = new LRUCache<string, ReelListResponse>(40);

export function useReels() {
  const queryClient = useQueryClient();
  const reportTimerRef = useRef<NodeJS.Timeout | null>(null);

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ['reels'],
    queryFn: async ({ pageParam }) => {
      const cacheKey = pageParam || 'initial';
      
      // Check client LRU cache first
      const cached = reelCache.get(cacheKey);
      if (cached) {
        return cached;
      }
      
      const response = await fetchReels(pageParam as string | undefined);
      
      // Store in LRU cache
      reelCache.set(cacheKey, response);
      
      return response;
    },
    getNextPageParam: (lastPage) => lastPage.has_more ? lastPage.next_cursor : undefined,
    initialPageParam: undefined as string | undefined,
  });

  // Report stats periodically
  useEffect(() => {
    reportTimerRef.current = setInterval(() => {
      const stats = reelCache.getStats();
      reportClientStats({
        hits: stats.hits,
        misses: stats.misses,
        evictions: stats.evictions
      }).catch(console.error);
    }, 5000);

    return () => {
      if (reportTimerRef.current) clearInterval(reportTimerRef.current);
    };
  }, []);

  const reels = data?.pages.flatMap((page) => page.items) || [];
  
  return {
    reels,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    cacheStats: reelCache.getStats()
  };
}
