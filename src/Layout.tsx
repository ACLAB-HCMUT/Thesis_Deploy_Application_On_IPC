// Layout.tsx
import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar, { SidebarItem } from "./components/common/Sidebar.tsx";
import { House, TabletSmartphone, Bell, ShieldCheck, Settings } from "lucide-react";
import GlobalNotification from "./components/common/GlobalNotification.tsx";

const Layout = () => {
    const location = useLocation(); // Sử dụng useLocation hook để lấy đường dẫn hiện tại
    
    return (
        <div className="flex">
            <Sidebar>
                <SidebarItem icon={<House size={20} />} text="Home" alert={false} active={location.pathname === "/home"} to="/home" />
                <SidebarItem icon={<TabletSmartphone size={20} />} text="Devices" alert={false} active={location.pathname === "/devices"} to="/devices" />
                <SidebarItem icon={<Bell size={20} />} text="Notification" alert={false} active={location.pathname === "/notifications"} to="/notifications" />
                <SidebarItem icon={<Settings size={20} />} text="Settings" alert={false} active={location.pathname === "/settings"} to="/settings" />
                <SidebarItem icon={<ShieldCheck size={20} />} text="Authenticate" alert={false} active={location.pathname === "/auth"} to="/auth" />
            </Sidebar>
            <main className="flex-1">
                <GlobalNotification />
                <Outlet /> {/* Các page sẽ render ở đây */}
            </main>
        </div>
    );
};

export default Layout;