import type { ReactNode } from 'react';
import Sidebar from './nav/Sidebar';
import BottomBar from './nav/BottomBar';
import OfflineBanner from './OfflineBanner';

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-full flex-col md:flex-row">
      <Sidebar />
      {/* isolate: los z-index internos de Leaflet no se salen de esta caja */}
      <div className="relative isolate flex min-h-0 min-w-0 flex-1 flex-col">
        <OfflineBanner />
        <div className="min-h-0 flex-1">{children}</div>
      </div>
      <BottomBar />
    </div>
  );
}