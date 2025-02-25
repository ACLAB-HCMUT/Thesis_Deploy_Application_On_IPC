import React from "react";
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { House, TabletSmartphone, Bell, ShieldCheck, Monitor, Settings, Clock } from "lucide-react";

const Devices: React.FC = () => {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
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

      {/* Main Content */}
      <main className="flex-1 p-6 bg-gray-50">
        <h1 className="text-2xl font-bold mb-6">My Devices</h1>

        {/* Device Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-4 bg-white rounded-lg shadow-md text-center">
            <h2 className="font-medium text-lg">Relay 1</h2>
            <button className="mt-4 px-4 py-2 bg-indigo-500 text-white rounded-lg">ON</button>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-md text-center">
            <h2 className="font-medium text-lg">Relay 2</h2>
            <button className="mt-4 px-4 py-2 bg-indigo-500 text-white rounded-lg">ON</button>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-md text-center">
            <h2 className="font-medium text-lg">Relay 3</h2>
            <button className="mt-4 px-4 py-2 bg-indigo-500 text-white rounded-lg">ON</button>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-md text-center">
            <h2 className="font-medium text-lg">Relay 4</h2>
            <button className="mt-4 px-4 py-2 bg-indigo-500 text-white rounded-lg">ON</button>
          </div>
        </div>

        {/* Logs Section */}
        <div className="mt-8">
          <h3 className="text-xl font-medium mb-4">Device Logs</h3>
          <table className="w-full table-auto bg-white rounded-lg shadow-md">
            <thead className="bg-indigo-100">
              <tr>
                <th className="px-4 py-2 text-left">Device</th>
                <th className="px-4 py-2 text-left">Status</th>
                <th className="px-4 py-2 text-left">Time Start</th>
                <th className="px-4 py-2 text-left">Time End</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border-t px-4 py-2">Relay 1</td>
                <td className="border-t px-4 py-2">ON</td>
                <td className="border-t px-4 py-2">13/11/2024 12:23:20</td>
                <td className="border-t px-4 py-2">13/11/2024 12:23:20</td>
              </tr>
              <tr>
                <td className="border-t px-4 py-2">Relay 1</td>
                <td className="border-t px-4 py-2">OFF</td>
                <td className="border-t px-4 py-2">13/11/2024 12:23:20</td>
                <td className="border-t px-4 py-2">13/11/2024 14:23:20</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Schedule Form */}
        <div className="mt-8">
          <h3 className="text-xl font-medium mb-4">Schedule Relay</h3>
          <form className="bg-white p-6 rounded-lg shadow-md">
            <div className="mb-4">
              <label className="block font-medium mb-2">Start Time</label>
              <input type="datetime-local" className="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div className="mb-4">
              <label className="block font-medium mb-2">End Time</label>
              <input type="datetime-local" className="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div className="flex justify-end gap-4">
              <button type="submit" className="px-4 py-2 bg-indigo-500 text-white rounded-lg">
                Save
              </button>
              <button type="reset" className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default Devices;
