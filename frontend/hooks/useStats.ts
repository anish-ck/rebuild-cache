'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchStats, fetchEvents, resetSystem } from '../lib/api';

export function useStats() {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: fetchStats,
    refetchInterval: 2000,
  });

  const { data: events } = useQuery({
    queryKey: ['events'],
    queryFn: fetchEvents,
    refetchInterval: 2000,
  });

  return {
    stats,
    events: events || [],
    resetSystem,
  };
}
