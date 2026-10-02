'use client';

import ProfileHeader from '@/components/ProfileHeader';
import ReelFeed from '@/components/ReelFeed';
import SystemMonitor from '@/components/SystemMonitor';

export default function Home() {
  return (
    <main className="container mx-auto p-4 max-w-7xl flex flex-col lg:flex-row gap-6 h-screen overflow-hidden">
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        <ProfileHeader />
        <div className="flex-1 mt-6 min-h-0">
          <ReelFeed />
        </div>
      </div>
      <div className="w-full lg:w-96 flex-shrink-0 h-full overflow-y-auto pb-4">
        <SystemMonitor />
      </div>
    </main>
  );
}
