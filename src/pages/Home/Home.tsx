import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
// import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
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
import Header from "../../components/common/Header.tsx";
import axios from 'axios';
import { app_id, city_id } from '../../config/env.tsx';

const API_URL = "http://localhost:8000/api/sensors/latest/vinhnguyenkhac20@gmail.com";
const WEATHER_URL = `https://api.openweathermap.org/data/2.5/weather?id=${city_id}&appid=${app_id}&units=metric`; 
const HOURLY_FORECAST = `https://pro.openweathermap.org/data/2.5/forecast?id=${city_id}&appid=${app_id}&units=metric`;
const CHART_MONTH = "http://localhost:8000/api/sensors/all/month/vinhnguyenkhac20@gmail.com";

const powerData = [
  { month: 'Ja', value: 25 },
  { month: 'Fe', value: 35 },
  { month: 'Ma', value: 30 },
  { month: 'Ap', value: 45 },
  { month: 'Ma', value: 40 },
  { month: 'Jun', value: 55 },
  { month: 'Jul', value: 73 }
];
// Định nghĩa kiểu dữ liệu cho Forecast
interface ForecastItem {
  dt: number;
  main: {
    temp_min: number;
    temp_max: number;
  };
  weather: {
    main: string;
    icon: string;
  }[];
}

const WeatherCard = ({ title, value, unit, icon: Icon }: { title: string; value: number; unit: string; icon: any })  => (
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

const PowerChart = ({title, data} : { title: string; data: { month: string; value: number }[] }) => (
  <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
    <CardContent className="p-3 sm:p-6">
      <div className="flex justify-between items-center mb-4 sm:mb-6">
        <h3 className="text-sm sm:text-base text-gray-800 font-semibold">{title}</h3>
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
        {/* <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
          <span className="w-2 h-2 sm:w-3 sm:h-3 bg-red-500 rounded-full"></span>
          <span className="text-gray-200 text-xs sm:text-sm font-medium">Electricity</span>
          <span className="text-red-400 ml-auto text-xs sm:text-sm font-semibold">73%</span>
        </div> */}
        
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={data}>
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

const WeatherForecast = ({ day, icon: Icon, temp, lowTemp }: { day: string; icon: any; temp: number; lowTemp: number }) => (
  <div className="flex justify-between items-center py-2 sm:py-3 px-3 sm:px-4 hover:bg-gray-50 rounded-lg transition-colors">
    <span className="text-gray-700 text-sm sm:text-base font-medium">{day}</span>
    <Icon className="text-yellow-500 w-5 h-5 sm:w-6 sm:h-6" />
    <span className="text-gray-900 text-sm sm:text-base font-semibold">
      {temp}°<span className="text-gray-400">/{lowTemp}°</span>
    </span>
  </div>
);

const HourlyForecast = ({ time, icon, temp }: { time: string; icon: string; temp: string | number }) => (
  <div className="bg-gray-900 text-white rounded-xl p-2 sm:p-4 text-center">
    <p className="text-xs sm:text-sm font-medium mb-1 sm:mb-2">{time}</p>
    {/* <Icon className="mx-auto mb-1 sm:mb-2 w-5 h-5 sm:w-7 sm:h-7" /> */}
    <img src={`https://openweathermap.org/img/wn/${icon}@2x.png`} alt="Weather icon" className="mx-auto" />
    <p className="text-sm sm:text-lg font-semibold">{temp}°C</p>
  </div>
);

export default function Home() {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(true);
  const [data, setData] = useState<{ temperature: number; humidity: number }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [weatherData, setWeatherData] = useState<{ name: string; main: { temp: number }; weather: { description: string, icon: string }[] } | null>(null);
  const [tempChart, setTempChart] = useState<{ month: string; value: number }[]>([]);
  const [humidityChart, setHumidityChart] = useState<{ month: string; value: number }[]>([]);
  const [soilTempChart, setSoilTempChart] = useState<{ month: string; value: number }[]>([]);
  const [soilHumidityChart, setSoilHumidityChart] = useState<{ month: string; value: number }[]>([]); 
  const [forecast, setForecast] = useState<ForecastItem[]>([]);
  // const [tempChart, setTempChart] = useState([]);
  // const [humidityChart, setHumidityChart] = useState([]);
  // const [soilTempChart, setSoilTempChart] = useState([]);
  // const [soilHumidityChart, setSoilHumidityChart] = useState([]);

  // Hourly forecast
  const [weather, setWeather] = useState({
    morning: { temp: "--", icon: "01d" },
    afternoon: { temp: "--", icon: "01d" },
    evening: { temp: "--", icon: "01d" }
  });

  const weatherIcons = {
    "Clear": Sun,
    "Clouds": Cloud,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(API_URL);
        setData(response.data.data.sensor_data || []);
        // console.log(response.data.data.sensor_data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    const fetchWeather = async () => {
      try {
        const response = await axios.get(WEATHER_URL);
        setWeatherData(response.data);
        console.log(response.data);
      } catch (err) {
        
      } finally {
        
      }
    };

    const fetchHourlyWeather = async () => {
      try {
        const response = await axios.get(HOURLY_FORECAST);
        // const data = await response.json();

        setWeather({
          morning: {
            temp: response.data.list[0].main.temp,
            icon: response.data.list[0].weather[0].icon
          },
          afternoon: {
            temp: response.data.list[4].main.temp,
            icon: response.data.list[4].weather[0].icon
          },
          evening: {
            temp: response.data.list[8].main.temp,
            icon: response.data.list[8].weather[0].icon
          }
        });
      } catch (error) {
        console.error("Error fetching weather:", error);
      }
    };
    
    const fetchChartData = async () => {
      const response = await axios.get(CHART_MONTH);
      console.log(response.data.data.sensor_data);
      const sensorData = response.data.data.sensor_data;
     
      setTempChart(
        sensorData.map(item => ({ month: item.month, value: item.temperature }))
      );

      setHumidityChart(
        sensorData.map(item => ({ month: item.month, value: item.humidity }))
      );

      setSoilTempChart(
        sensorData.map(item => ({ month: item.month, value: item.temperature }))
      );

      setSoilHumidityChart(
        sensorData.map(item => ({ month: item.month, value: item.humidity }))
      );

      console.log(tempChart);
    };

    const weatherForecast = async () => {
      try {
        const response = await axios.get(HOURLY_FORECAST);
        const dailyData = response.data.list.filter((item: any, index: number) => index % 8 === 0); // Lấy dữ liệu mỗi 24h
        setForecast(dailyData);
      } catch (error) {
        console.error("Lỗi khi lấy dữ liệu thời tiết:", error);
      }
    };


    fetchData();
    fetchWeather();
    fetchHourlyWeather();
    fetchChartData();
    weatherForecast();
    
    const interval = setInterval(fetchData, 30000); // Gọi API mỗi 30s
    const intervalWeather = setInterval(fetchWeather, 600000); // Gọi API mỗi 10p

    return () => {
      clearInterval(interval);
      clearInterval(intervalWeather);
    };
  }, []);  

  const capitalizeFirstLetter = (string: string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  return (    
    <main className="flex min-h-screen bg-gray-50">

      {/* Main content */}
      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        {/* Power Charts Grid */}
        <h1 className="text-2xl font-bold mb-6">Home</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
          {/* {[1, 2, 3, 4].map((index) => (
            <PowerChart key={index} data={tempChart} />
          ))} */}
          <PowerChart key="tempChart" title="Temperature" data={tempChart} />
          <PowerChart key="humidityChart" title="Humidity" data={humidityChart} />
          <PowerChart key="soilTempChart" title="Soil Temperature" data={soilTempChart} />
          <PowerChart key="soilhumidityChart" title="Soil Humidity" data={soilHumidityChart} />
        </div>

        {/* Weather Stats */}
        {data.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
            <WeatherCard 
              title="Temperature Air" 
              value={data[0].temperature}
              unit="°C" 
              icon={Thermometer}
            />
            <WeatherCard 
              title="Humidity Air" 
              value={data[0].humidity} 
              unit="%" 
              icon={Droplets}
            />
            <WeatherCard 
              title="Temperature Soil" 
              value={data[0].temperature}
              unit="°C" 
              icon={Thermometer}
            />
            <WeatherCard 
              title="Humidity Soil" 
              value={data[0].humidity}  
              unit="%" 
              icon={Droplets}
            />
          </div>
        )}

        {/* Weather Forecast */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100">
          <CardContent className="p-4 sm:p-6 lg:p-8">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-8 mb-6 sm:mb-8">
              <div className="p-3 sm:p-4 rounded-xl">
                {/* <Sun className="text-yellow-500 w-8 h-8 sm:w-12 sm:h-12" /> */}
                <img src={`https://openweathermap.org/img/wn/${weatherData?.weather[0].icon}@2x.png`} alt="Weather icon" className="mx-auto" />
              </div>
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-gray-800">{weatherData?.weather[0].description && capitalizeFirstLetter(weatherData.weather[0].description)}</h3>
                <p className="text-sm sm:text-base text-gray-500 mb-1 sm:mb-2">{weatherData?.name}</p>
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">{weatherData?.main.temp}°C</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 sm:gap-6 mb-6 sm:mb-8">
              <HourlyForecast time="Morning" icon={weather.morning.icon} temp={weather.morning.temp} />
              <HourlyForecast time="Afternoon" icon={weather.afternoon.icon} temp={weather.afternoon.temp} />
              <HourlyForecast time="Evening" icon={weather.evening.icon} temp={weather.evening.temp} />
            </div>

            {/* <div className="space-y-1">
              <WeatherForecast day="Monday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Tuesday" icon={Cloud} temp="21" lowTemp="19" />
              <WeatherForecast day="Wednesday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Thursday" icon={Sun} temp="32" lowTemp="24" />
              <WeatherForecast day="Friday" icon={Sun} temp="32" lowTemp="24" />
            </div> */}

            <div className="space-y-1">
              {forecast.map((item, index) => {
                const date = new Date(item.dt * 1000);
                const day = date.toLocaleDateString("en-US", { weekday: "long" });
                const weatherType = item.weather[0].main;
                const Icon = weatherIcons[weatherType] || Sun;

                return (
                  <WeatherForecast
                    key={index}
                    day={day}
                    icon={Icon}
                    temp={Math.round(item.main.temp_max)}
                    lowTemp={Math.round(item.main.temp_min)}
                  />
                );
              })}
            </div>
          </CardContent>
        </div>
      </div>
    </main>
  );
}