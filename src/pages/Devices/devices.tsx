import React from "react";
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { SwitchToggle } from "../../components/common/Switch.tsx";
import { House, TabletSmartphone, Bell, ShieldCheck, Monitor, Settings, Clock, Lamp, Microwave, RadioReceiver, MonitorSpeaker } from "lucide-react";

const DeviceCard = ({ title, icon: Icon }) => (
  <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-3 sm:p-6 shadow-lg border border-gray-100">
    <div className="flex items-center gap-2 sm:gap-3 justify-between">
      
      <div className="flex flex-col items-center">
        <div className="p-2 sm:p-3 bg-blue-50 rounded-lg ">
          <Icon className="text-blue-500 w-4 h-4 sm:w-6 sm:h-6" />
        </div>
        <p className="text-gray-500 text-xs sm:text-sm font-medium pt-1">{title}</p>
        
      </div>
      <SwitchToggle/>
    </div>
  </div>
);

const Devices: React.FC = () => {
  return (
    <main className="flex min-h-screen bg-gray-50">
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

      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        {/* Device cards */}
        <div className="grid grid:cols-1 sm:grid-cols-2 md:grid-cols-2 xl:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
          <DeviceCard 
            title="Relay 1" 
            icon={Lamp}
          />
          <DeviceCard 
            title="Relay 2"
            icon={RadioReceiver}
          />
          <DeviceCard 
            title="Relay 3" 
            icon={MonitorSpeaker}
          />
          <DeviceCard 
            title="Relay 4"
            icon={Microwave}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 lg:grid-cols-4 gap-6 mt-5">
          {/* Logs Section */}
          <div className="rounded-lg col-span-1 md:col-span-3 lg:col-span-3">
            <div className="w-full bg-white rounded-lg shadow-md overflow-hidden">
              <div className="max-h-64 overflow-y-auto">
                <table className="w-full table-auto">
                  <thead className="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400 sticky top-0">
                    <tr>
                      <th className="px-4 py-2 text-left">Device</th>
                      <th className="px-4 py-2 text-left">Status</th>
                      <th className="px-4 py-2 text-left">Time Start</th>
                      <th className="px-4 py-2 text-left">Time End</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm">
                    {[...Array(20)].map((_, index) => (
                      <tr key={index} className="border-t">
                        <td className="px-4 py-2">Relay {index + 1}</td>
                        <td className="px-4 py-2">{index % 2 === 0 ? "ON" : "OFF"}</td>
                        <td className="px-4 py-2">13/11/2024 12:23:20</td>
                        <td className="px-4 py-2">13/11/2024 14:23:20</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Schedule Form */}
          <div className="bg-slate-200 rounded-lg col-span-1 md:col-span-2 lg:col-span-1">
            {/* <h2 className="text-2xl font-bold pt-3 pl-3">Schedule Relay</h2> */}
            <form className="bg-white max-h-64 p-6 rounded-lg shadow-md">
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
        </div>

        <div className="mt-6 rounded-lg col-span-1 md:col-span-3 lg:col-span-3">
          <div className="w-full bg-white rounded-lg shadow-md overflow-hidden">
            <div className="max-h-64 overflow-y-auto">
              <table className="w-full table-auto">
                <thead className="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400 sticky top-0">
                  <tr>
                    <th className="px-4 py-2 text-left">Device</th>
                    <th className="px-4 py-2 text-left">User</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Time</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {[...Array(20)].map((_, index) => (
                    <tr key={index} className="border-t">
                      <td className="px-4 py-2">Relay {index + 1}</td>
                      <td className="px-4 py-2">Vinh Nguyen</td>
                      <td className="px-4 py-2">{index % 2 === 0 ? "ON" : "OFF"}</td>
                      <td className="px-4 py-2">13/11/2024 14:23:20</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Devices;
