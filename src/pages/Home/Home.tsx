import React from "react";
import Link from 'react-router-dom'
import Sidebar from "../../components/common/Sidebar.tsx"
import { SidebarItem } from "../../components/common/Sidebar.tsx"
import {
  House,
  TabletSmartphone,
  Bell,
  ShieldCheck,
  Settings
} from 'lucide-react'

export default function Home() {
  return (
    <main>
      <Sidebar>
        <SidebarItem icon={<House size={20} />} text="Home" alert={false} active={true}/>
        <SidebarItem icon={<TabletSmartphone size={20} />} text="Devices" alert={false} active={undefined}/>
        <SidebarItem icon={<Bell size={20} />} text="Notification" alert={false} active={undefined}/>
        <SidebarItem icon={<Settings size={20} />} text="Settings" alert={false} active={undefined}/>
        <SidebarItem icon={<ShieldCheck size={20} />} text="Authenticate" alert={false} active={undefined}/>
      </Sidebar>
    </main>
  );
}