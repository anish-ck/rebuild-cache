'use client';

import { SystemEvent } from '../lib/types';
import { formatTimeAgo } from '../lib/utils';
import { useEffect, useRef } from 'react';

export default function EventLog({ events }: { events: SystemEvent[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to top when new events arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = 0;
    }
  }, [events]);

  const getEventColor = (type: string) => {
    if (type.includes('HIT')) return 'text-green-400 bg-green-500/10 border-green-500/20';
    if (type.includes('MISS')) return 'text-red-400 bg-red-500/10 border-red-500/20';
    if (type.includes('QUERY')) return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
    if (type.includes('SET')) return 'text-purple-400 bg-purple-500/10 border-purple-500/20';
    if (type.includes('PREFETCH')) return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
    if (type.includes('COLD')) return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20';
    if (type.includes('HOT')) return 'text-orange-400 bg-orange-500/10 border-orange-500/20';
    return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
  };

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 flex flex-col h-full overflow-hidden">
      <div className="p-3 border-b border-gray-800 flex justify-between items-center bg-gray-900">
        <h3 className="text-sm font-semibold text-gray-300">Live System Events</h3>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-dot" />
          <span className="text-xs text-gray-500">Live</span>
        </div>
      </div>
      
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 space-y-2">
        {events.length === 0 ? (
          <div className="text-center text-sm text-gray-500 py-4">No events yet</div>
        ) : (
          events.slice(0, 50).map((event, i) => (
            <div key={`${event.timestamp}-${i}`} className="text-xs font-mono animate-fade-in">
              <div className="flex items-start gap-2">
                <span className="text-gray-500 w-16 flex-shrink-0">
                  {new Date(event.timestamp).toLocaleTimeString([], { hour12: false, second: '2-digit' })}
                </span>
                <span className={`px-1.5 py-0.5 rounded border text-[10px] whitespace-nowrap ${getEventColor(event.event_type)}`}>
                  {event.event_type}
                </span>
              </div>
              <div className="text-gray-400 ml-18 mt-1 pl-18 break-words border-l border-gray-800 ml-4 pl-3 py-1">
                {event.details}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
