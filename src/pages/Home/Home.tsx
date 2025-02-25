// import React from "react";
// import Link from 'react-router-dom'
// import Sidebar from "../../components/common/Sidebar.tsx"
// import { SidebarItem } from "../../components/common/Sidebar.tsx"
// import {
//   House,
//   TabletSmartphone,
//   Bell,
//   ShieldCheck,
//   Settings
// } from 'lucide-react'

// export default function Home() {
//   return (
//     <main>
//       <Sidebar>
//         <SidebarItem icon={<House size={20} />} text="Home" alert={false} active={true}/>
//         <SidebarItem icon={<TabletSmartphone size={20} />} text="Devices" alert={false} active={undefined}/>
//         <SidebarItem icon={<Bell size={20} />} text="Notification" alert={false} active={undefined}/>
//         <SidebarItem icon={<Settings size={20} />} text="Settings" alert={false} active={undefined}/>
//         <SidebarItem icon={<ShieldCheck size={20} />} text="Authenticate" alert={false} active={undefined}/>
//       </Sidebar>
//     </main>
//   );
// }
import React from "react";
import { Link } from 'react-router-dom';
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer  } from 'recharts';
import { 
  House,
  TabletSmartphone, 
  Bell, 
  ShieldCheck, 
  Settings,
  Sun, 
  
  Cloud, 
  Droplets, 
  Thermometer, Menu
} from 'lucide-react';
import { Card, CardContent } from '../../components/ui/card.tsx';

const powerData = [
  { month: 'Ja', value: 25 },
  { month: 'Fe', value: 35 },
  { month: 'Ma', value: 30 },
  { month: 'Ap', value: 45 },
  { month: 'Ma', value: 40 },
  { month: 'Jun', value: 55 },
  { month: 'Jul', value: 73 },
  { month: 'Au', value: 65 }
];

const WeatherCard = ({ title, value, unit, icon: Icon }) => (
  <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-3 sm:p-6 shadow-lg border border-gray-100">
    <div className="flex items-center gap-2 sm:gap-3">
      <div className="p-2 sm:p-3 bg-blue-50 rounded-lg">
        <Icon className="text-blue-500 w-4 h-4 sm:w-6 sm:h-6" />
      </div>
      <div>
        <p className="text-gray-500 text-xs sm:text-sm font-medium">{title}</p>
        <p className="text-lg sm:text-2xl font-bold text-gray-800">{value}{unit}</p>
      </div>
    </div>
  </div>
);

const PowerChart = () => (
  <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
    <CardContent className="p-3 sm:p-6">
      <div className="flex justify-between items-center mb-4 sm:mb-6">
        <h3 className="text-sm sm:text-base text-gray-800 font-semibold">Power Consumed</h3>
        <div className="flex items-center gap-2">
          <select className="bg-gray-900 text-white px-2 sm:px-4 py-1 sm:py-2 rounded-lg text-xs sm:text-sm font-medium">
            <option>Month</option>
          </select>
          <button className="bg-gray-900 text-white p-1 sm:p-2 rounded-lg hover:bg-gray-800 transition-colors">
            &gt;
          </button>
        </div>
      </div>
      
      <div className="bg-gray-900 rounded-xl p-3 sm:p-6">
        <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
          <span className="w-2 h-2 sm:w-3 sm:h-3 bg-red-500 rounded-full"></span>
          <span className="text-gray-200 text-xs sm:text-sm font-medium">Electricity</span>
          <span className="text-red-400 ml-auto text-xs sm:text-sm font-semibold">73%</span>
        </div>
        
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={powerData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="month" stroke="#9CA3AF" tick={{ fontSize: 12 }} />
            <YAxis stroke="#9CA3AF" tick={{ fontSize: 12 }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
              labelStyle={{ color: '#fff', fontSize: 12 }}
            />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke="#EF4444" 
              strokeWidth={2}
              dot={{ stroke: '#EF4444', strokeWidth: 2, fill: '#1F2937' }}
              activeDot={{ r: 6, stroke: '#EF4444', strokeWidth: 2, fill: '#FEE2E2' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </CardContent>
  </div>
);

const WeatherForecast = ({ day, icon: Icon, temp, lowTemp }) => (
  <div className="flex justify-between items-center py-2 sm:py-3 px-3 sm:px-4 hover:bg-gray-50 rounded-lg transition-colors">
    <span className="text-gray-700 text-sm sm:text-base font-medium">{day}</span>
    <Icon className="text-yellow-500 w-5 h-5 sm:w-6 sm:h-6" />
    <span className="text-gray-900 text-sm sm:text-base font-semibold">
      {temp}°<span className="text-gray-400">/{lowTemp}°</span>
    </span>
  </div>
);

const HourlyForecast = ({ time, icon: Icon, temp }) => (
  <div className="bg-gray-900 text-white rounded-xl p-2 sm:p-4 text-center">
    <p className="text-xs sm:text-sm font-medium mb-1 sm:mb-2">{time}</p>
    <Icon className="mx-auto mb-1 sm:mb-2 w-5 h-5 sm:w-7 sm:h-7" />
    <p className="text-sm sm:text-lg font-semibold">{temp}°C</p>
  </div>
);

export default function Home() {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

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
        {/* Power Charts Grid */}
        <h1 className="text-2xl font-bold mb-6">Home</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
          {[1, 2, 3, 4].map((index) => (
            <PowerChart key={index} />
          ))}
        </div>

        {/* Weather Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
          <WeatherCard 
            title="Temperature Air" 
            value="21" 
            unit="°C" 
            icon={Thermometer}
          />
          <WeatherCard 
            title="Humidity Air" 
            value="21" 
            unit="%" 
            icon={Droplets}
          />
          <WeatherCard 
            title="Temperature Soil" 
            value="21" 
            unit="°C" 
            icon={Thermometer}
          />
          <WeatherCard 
            title="Humidity Soil" 
            value="21" 
            unit="%" 
            icon={Droplets}
          />
        </div>

        {/* Weather Forecast */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100">
          <CardContent className="p-4 sm:p-6 lg:p-8">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-8 mb-6 sm:mb-8">
              <div className="p-3 sm:p-4 bg-yellow-50 rounded-xl">
                <Sun className="text-yellow-500 w-8 h-8 sm:w-12 sm:h-12" />
              </div>
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-gray-800">Sunny Day</h3>
                <p className="text-sm sm:text-base text-gray-500 mb-1 sm:mb-2">Time in Hưng Yên</p>
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">21°C</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 sm:gap-6 mb-6 sm:mb-8">
              <HourlyForecast time="Morning" icon={Sun} temp="31" />
              <HourlyForecast time="Afternoon" icon={Sun} temp="31" />
              <HourlyForecast time="Evening" icon={Sun} temp="31" />
            </div>

            <div className="space-y-1">
              <WeatherForecast day="Monday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Tuesday" icon={Cloud} temp="21" lowTemp="19" />
              <WeatherForecast day="Wednesday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Thursday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Friday" icon={Sun} temp="32" lowTemp="24" />
            </div>
          </CardContent>
        </div>
      </div>
    </main>
  );
}