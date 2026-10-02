'use client';

import { useEffect, useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { useReels } from '../hooks/useReels';
import ReelCard from './ReelCard';

export default function ReelFeed() {
  const { reels, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } = useReels();
  const parentRef = useRef<HTMLDivElement>(null);
  const observerTarget = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: reels.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 320, // Estimated height of ReelCard + gap
    overscan: 5,
  });

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);

  // Prefetch logic
  useEffect(() => {
    const lastRendered = virtualizer.getVirtualItems()[virtualizer.getVirtualItems().length - 1];
    if (lastRendered && reels.length - lastRendered.index <= 5 && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [virtualizer.getVirtualItems(), reels.length, hasNextPage, isFetchingNextPage, fetchNextPage]);

  if (isLoading && reels.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="bg-gray-900 rounded-t-xl p-3 border border-gray-800 border-b-0 text-sm text-gray-400 flex justify-between">
        <span>Loaded: {reels.length} reels</span>
        <span>Rendered: {virtualizer.getVirtualItems().length} items</span>
      </div>
      
      <div 
        ref={parentRef}
        className="flex-1 overflow-y-auto bg-gray-950 rounded-b-xl border border-gray-800 relative"
      >
        <div
          style={{
            height: `${virtualizer.getTotalSize()}px`,
            width: '100%',
            position: 'relative',
          }}
        >
          {virtualizer.getVirtualItems().map((virtualRow) => {
            const reel = reels[virtualRow.index];
            if (!reel) return null;
            
            return (
              <div
                key={virtualRow.index}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: `${virtualRow.size}px`,
                  transform: `translateY(${virtualRow.start}px)`,
                  padding: '12px',
                }}
              >
                <div className="max-w-md mx-auto">
                  <ReelCard reel={reel} />
                </div>
              </div>
            );
          })}
        </div>
        
        {/* Intersection Observer Target */}
        <div ref={observerTarget} className="h-10 w-full" />
        
        {isFetchingNextPage && (
          <div className="py-6 flex justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500"></div>
          </div>
        )}
      </div>
    </div>
  );
}
