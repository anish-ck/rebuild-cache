import { ReelListResponse, Stats, SystemEvent } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchReels(cursor?: string | null, limit: number = 20): Promise<ReelListResponse> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (cursor) params.set('cursor', cursor);
  const res = await fetch(`${API_URL}/api/reels?${params}`);
  if (!res.ok) throw new Error('Failed to fetch reels');
  return res.json();
}

export async function fetchProfile(): Promise<{ username: string; total_reels: number; avatar_url: string | null }> {
  const res = await fetch(`${API_URL}/api/profile`);
  if (!res.ok) throw new Error('Failed to fetch profile');
  return res.json();
}

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${API_URL}/api/stats`);
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}

export async function fetchEvents(): Promise<SystemEvent[]> {
  const res = await fetch(`${API_URL}/api/events`);
  if (!res.ok) throw new Error('Failed to fetch events');
  return res.json();
}

export async function resetSystem(): Promise<void> {
  await fetch(`${API_URL}/api/reset`, { method: 'POST' });
}

export async function reportClientStats(stats: { hits: number; misses: number; evictions: number }): Promise<void> {
  await fetch(`${API_URL}/api/stats/client`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(stats),
  });
}
