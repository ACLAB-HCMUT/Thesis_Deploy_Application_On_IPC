import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { 
  House,
  TabletSmartphone, 
  Bell, 
  ShieldCheck, 
  Settings,
  Menu,
  Check,
  X,
  Trash2
} from 'lucide-react';
import { Card, CardContent } from '../../components/ui/card.tsx';

interface User {
  id: string;
  name: string;
  ip: string;
  port: string;
  status: "ON" | "OFF";
  lastActive: string;
  lastConnected?: string;
}

export default function Authentication() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [users, setUsers] = useState<User[]>([
    {
      id: "1",
      name: "Brad Simmons",
      ip: "176.12.23.45",
      port: "5000",
      status: "ON",
      lastActive: "13/11/2024 20:03:30",
      lastConnected: "13/11/2024 20:05:30"
    },
    {
      id: "2",
      name: "Jessie Clarcson",
      ip: "176.12.23.45",
      port: "5000",
      status: "OFF",
      lastActive: "13/11/2024 20:03:30"
    },
    {
      id: "3",
      name: "Lebron Wayde",
      ip: "176.12.23.45",
      port: "5000",
      status: "OFF",
      lastActive: "13/11/2024 20:03:30"
    },
    {
      id: "4",
      name: "Natali Trump",
      ip: "176.12.23.45",
      port: "5000",
      status: "OFF",
      lastActive: "13/11/2024 20:03:30"
    }
  ]);

  const handleDeleteUser = (userId: string) => {
    setUsers(users.filter(user => user.id !== userId));
  };

  return (
    <main className="flex min-h-screen bg-gray-50">
      {/* Sidebar with responsive visibility */}
      <Sidebar>
        <SidebarItem 
          icon={<House size={20} />} 
          text="Home" 
          alert={false} 
          active={false}
          to="/home"
        />
        <SidebarItem 
          icon={<TabletSmartphone size={20} />} 
          text="Devices" 
          alert={false} 
          active={false}
          to="/devices"
        />
        <SidebarItem 
          icon={<Bell size={20} />} 
          text="Notification" 
          alert={false} 
          active={false}
          to="/notifications"
        />
        <SidebarItem 
          icon={<Settings size={20} />} 
          text="Settings" 
          alert={false} 
          active={false}
          to="/settings"
        />
        <SidebarItem 
          icon={<ShieldCheck size={20} />} 
          text="Authenticate" 
          alert={false} 
          active={true}
          to="/auth"
        />
      </Sidebar>

      {/* Main content */}
      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <h1 className="text-2xl font-bold mb-6">Authentication</h1>
        <Card className="w-full">
          <CardContent className="p-0">
            {/* Server Info */}
            <div className="flex flex-col items-center justify-center py-8 border-b border-gray-200">
              <div className="flex mb-4">
                <div className="w-12 h-12 bg-blue-900 rounded flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded"></div>
                </div>
                <div className="flex flex-col ml-2">
                  <div className="w-8 h-2 bg-blue-900 rounded mb-1"></div>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-900 rounded"></div>
                    <div className="w-4 h-2 bg-blue-900 rounded"></div>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-800">IP Server: 176.23.43.54</p>
                <p className="text-sm text-gray-800">Port:5000</p>
              </div>
            </div>

            {/* User Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Address IP</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rating</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {users.map(user => (
                    <tr key={user.id}>
                      <td className="py-3 px-4">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                            {user.name.charAt(0)}
                          </div>
                          <span className="font-medium text-gray-900">{user.name}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm text-gray-900">{user.ip}</div>
                        <div className="text-xs text-gray-500">{user.port}</div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          user.status === "ON" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                        }`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm text-gray-900">{user.lastActive}</div>
                        <div className="text-xs text-gray-500">{user.lastConnected || "N/A"}</div>
                      </td>
                      <td className="py-3 px-4">
                        <button 
                          className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded text-sm"
                          onClick={() => handleDeleteUser(user.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}