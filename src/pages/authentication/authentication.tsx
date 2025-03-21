import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

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
      

      {/* Main content */}
      <div className="flex-1 mt-16 p-4 sm:p-6 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <h1 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6">Authentication</h1>
        <Card className="w-full">
          <CardContent className="p-0">
            {/* Server Info */}
            <div className="flex flex-col items-center justify-center py-6 sm:py-8 border-b border-gray-200">
              <div className="flex mb-4">
                <div className="w-10 h-10 sm:w-12 sm:h-12  bg-blue-900 rounded flex items-center justify-center">
                  <div className="w-3 h-3 sm:w-4 sm:h-4 bg-white rounded"></div>
                </div>
                <div className="flex flex-col ml-2">
                  <div className="w-6 h-2 sm:w-8 sm:h-2 bg-blue-900 rounded mb-1"></div>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-900 rounded"></div>
                    <div className="w-3 h-2 sm:w-4 sm:h-2 bg-blue-900 rounded"></div>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <p className="text-sm sm:text-sm text-gray-800">IP Server: 176.23.43.54</p>
                <p className="text-sm sm:text-sm text-gray-800">Port:5000</p>
              </div>
            </div>

            {/* User Table */}
            <div className="overflow-x-auto">
              <table className="w-full hidden sm:table">
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
              {/* List cho mobile */}
              <div className="sm:hidden divide-y divide-gray-200">
                {users.map((user) => (
                  <div key={user.id} className="p-4 flex flex-col space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center flex-shrink-0 ">
                        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                          {user.name.charAt(0)}
                        </div>
                        <span className="font-medium text-gray-900">
                          {user.name}
                        </span>
                      </div>
                      <button
                        className="bg-red-500 hover:bg-red-600 text-white py-1 px-2  rounded text-xs flex-shrink-0 ml-2" style={{ minWidth: "50px" }}
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        Delete
                      </button>
                    </div>
                    <div className="mt-2 text-sm text-gray-900">
                      <p>IP: {user.ip}</p>
                      <p>Port: {user.port}</p>
                      <p>
                        Status:{" "}
                        <span
                          className={`inline-flex text-xs font-semibold ${
                            user.status === "ON"
                              ? "text-green-800"
                              : "text-red-800"
                          }`}
                        >
                          {user.status}
                        </span>
                      </p>
                      <p>Last Active: {user.lastActive}</p>
                      <p>Last Connected: {user.lastConnected || "N/A"}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}