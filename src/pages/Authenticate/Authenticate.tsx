import React from "react";
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { House, TabletSmartphone, Bell, ShieldCheck, Settings } from "lucide-react";

const Authenticate: React.FC = () => {
  return (
    <main className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar>
          <SidebarItem icon={<House size={20} />} text="Home" alert={false} active={false} to="home"/>
          <SidebarItem icon={<TabletSmartphone size={20} />} text="Devices" alert={false} active={false} to="devices"/>
          <SidebarItem icon={<Bell size={20} />} text="Notification" alert={false} active={false} to="notification" />
          <SidebarItem icon={<Settings size={20} />} text="Settings" alert={false} active={false} to="settings" />
          <SidebarItem icon={<ShieldCheck size={20} />} text="Authenticate" alert={false} active={true} to="authenticate" />
      </Sidebar>

      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        
      </div>
    </main>
  );
};

export default Authenticate;
