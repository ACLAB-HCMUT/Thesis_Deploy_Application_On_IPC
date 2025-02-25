import React, { useState } from 'react';
import { Search, Trash2, Bell, Check, Menu, House, TabletSmartphone, ShieldCheck, Settings } from 'lucide-react';
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";

interface Notification {
    id: number;
    title: string;
    message: string;
    date: string;
    isRead: boolean;
  }

const NotificationPage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      title: "Canh bao do am dat",
      message: "Do am am trung binh ngay hom nay la",
      date: "2024-11-10",
      isRead: false,
    },
    {
      id: 2,
      title: "Canh bao nhiet do",
      message: "Nhiet do cao bat thuong",
      date: "2024-11-10",
      isRead: true,
    },
    {
      id: 3,
      title: "Canh bao nhiet do",
      message: "Nhiet do cao bat thuong",
      date: "2024-11-10",
      isRead: false,
    },
    {
      id: 4,
      title: "Canh bao nhiet do",
      message: "Nhiet do cao bat thuong",
      date: "2024-11-09",
      isRead: true,
    },
    {
      id: 5,
      title: "Cap nhat he thong",
      message: "He thong vua duoc cap nhat",
      date: "2024-11-09",
      isRead: false,
    }
  ]);

  const [searchQuery, setSearchQuery] = useState('');

  // Group notifications by date
  const groupedNotifications: { [key: string]: Notification[] } = notifications.reduce(
    (groups: { [key: string]: Notification[] }, notification) => {
      const date = notification.date;
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(notification);
      return groups;
    }, {}
  );

  
  // Filter notifications based on search query
const filteredGroups: { [key: string]: Notification[] } = Object.entries(groupedNotifications).reduce(
    (acc: { [key: string]: Notification[] }, [date, notifs]) => {
      const filtered = (notifs as Notification[]).filter(n => 
        n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.message.toLowerCase().includes(searchQuery.toLowerCase())
      );
      if (filtered.length > 0) {
        acc[date] = filtered;
      }
      return acc;
    }, {}
  );
  

  const toggleRead = (id) => {
    setNotifications(notifications.map(notification =>
      notification.id === id
        ? { ...notification, isRead: !notification.isRead }
        : notification
    ));
  };

  const deleteNotification = (id) => {
    setNotifications(notifications.filter(notification => notification.id !== id));
  };

  return (
    <main className="flex min-h-screen bg-gray-50">
      {/* Mobile menu button */}
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-md"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        <Menu size={24} />
      </button>

      {/* Sidebar with responsive visibility */}
      <div className={`
        fixed inset-y-0 left-0 transform lg:relative lg:translate-x-0 transition duration-200 ease-in-out z-40
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:block
      `}>
        <Sidebar>
        <SidebarItem 
          icon={<House size={20} />} 
          text="Home" 
          alert={false} 
          active={location.pathname === '/home'}
          to="/home"
        />
        <SidebarItem 
          icon={<TabletSmartphone size={20} />} 
          text="Devices" 
          alert={false} 
          active={location.pathname === '/devices'}
          to="/devices"
        />
        <SidebarItem 
          icon={<Bell size={20} />} 
          text="Notification" 
          alert={false} 
          active={location.pathname === '/notifications'}
          to="/notifications"
        />
        <SidebarItem 
          icon={<Settings size={20} />} 
          text="Settings" 
          alert={false} 
          active={location.pathname === '/settings'}
          to="/settings"
        />
        <SidebarItem 
          icon={<ShieldCheck size={20} />} 
          text="Authenticate" 
          alert={false} 
          active={location.pathname === '/auth'}
          to="/auth"
        />
      </Sidebar>
      </div>

      {/* Main content */}
      <div className="flex-1 p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 ml-0 lg:ml-0">
        <h1 className="text-2xl font-bold mb-6">Notifications</h1>
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="Search notifications..."
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
            </div>
          </div>

          {Object.entries(filteredGroups).map(([date, notifications]) => (
            <div key={date} className="mb-6">
              <h2 className="text-lg font-semibold mb-3">
                {new Date(date).toLocaleDateString('vi-VN', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </h2>
              
              <div className="space-y-3">
                {notifications.map(notification => (
                  <div 
                    key={notification.id}
                    className={`rounded-lg border shadow-sm transition-colors duration-200 ${
                      notification.isRead ? 'bg-gray-50' : 'bg-white'
                    }`}
                  >
                    <div className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3">
                          <div className={`mt-1 ${notification.isRead ? 'text-gray-400' : 'text-green-500'}`}>
                            <Bell size={20} />
                          </div>
                          <div>
                            <h3 className="font-medium">{notification.title}</h3>
                            <p className="text-gray-600 text-sm mt-1">{notification.message}</p>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => toggleRead(notification.id)}
                            className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-150"
                          >
                            <Check 
                              size={18} 
                              className={notification.isRead ? 'text-green-500' : 'text-gray-400'} 
                            />
                          </button>
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-150 text-red-500"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {Object.keys(filteredGroups).length === 0 && (
            <div className="text-center py-10 text-gray-500">
              No notifications found
            </div>
          )}
        </div>
      </div>
    </main>
  );
};

export default NotificationPage;