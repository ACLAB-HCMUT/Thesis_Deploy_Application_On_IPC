import React, { useState } from "react";
import { Link } from 'react-router-dom';
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { 
  House,
  TabletSmartphone, 
  Bell, 
  ShieldCheck, 
  Settings as SettingsIcon,
  Menu,
  User,
  Globe,
  Bell as BellIcon,
  Wifi,
  Database,
  HardDrive,
  Save,
  RefreshCw,Thermometer
} from 'lucide-react';
import { Card, CardContent } from '../../components/ui/card.tsx';

// Settings interface definitions
interface SystemSettings {
  language: string;
  darkMode: boolean;
  notifications: boolean;
  dataRefreshRate: number; // in minutes
  autoUpdate: boolean;
}

interface NetworkSettings {
  serverAddress: string;
  serverPort: string;
  connectionTimeout: number; // in seconds
  useSSL: boolean;
}

interface SensorSettings {
  tempAlertThreshold: number;
  humidityAlertThreshold: number;
  soilMoistureThreshold: number;
  readingInterval: number; // in minutes
}

interface StorageSettings {
  localStorageDuration: number; // in days
  cloudBackup: boolean;
  backupFrequency: number; // in days
  dataCompressionLevel: number; // 0-9
}

export default function Settings() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('system');
  
  // State for different settings categories
  const [systemSettings, setSystemSettings] = useState<SystemSettings>({
    language: 'English',
    darkMode: false,
    notifications: true,
    dataRefreshRate: 15,
    autoUpdate: true
  });
  
  const [networkSettings, setNetworkSettings] = useState<NetworkSettings>({
    serverAddress: '176.23.43.54',
    serverPort: '5000',
    connectionTimeout: 30,
    useSSL: true
  });
  
  const [sensorSettings, setSensorSettings] = useState<SensorSettings>({
    tempAlertThreshold: 30,
    humidityAlertThreshold: 85,
    soilMoistureThreshold: 40,
    readingInterval: 60
  });
  
  const [storageSettings, setStorageSettings] = useState<StorageSettings>({
    localStorageDuration: 30,
    cloudBackup: true,
    backupFrequency: 7,
    dataCompressionLevel: 6
  });
  
  // Handlers for settings changes
  const handleSystemSettingChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setSystemSettings({
      ...systemSettings,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleNetworkSettingChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setNetworkSettings({
      ...networkSettings,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleSensorSettingChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    setSensorSettings({
      ...sensorSettings,
      [name]: Number(value)
    });
  };
  
  const handleStorageSettingChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setStorageSettings({
      ...storageSettings,
      [name]: type === 'checkbox' ? checked : Number(value)
    });
  };
  
  const saveSettings = () => {
    // Here you would implement saving to localStorage, a database, or an API
    console.log('Saving settings:', {
      systemSettings,
      networkSettings,
      sensorSettings,
      storageSettings
    });
    
    // Show a success message
    alert('Settings saved successfully!');
  };
  
  const resetSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to default values?')) {
      // Reset to default values
      setSystemSettings({
        language: 'English',
        darkMode: false,
        notifications: true,
        dataRefreshRate: 15,
        autoUpdate: true
      });
      
      setNetworkSettings({
        serverAddress: '176.23.43.54',
        serverPort: '5000',
        connectionTimeout: 30,
        useSSL: true
      });
      
      setSensorSettings({
        tempAlertThreshold: 30,
        humidityAlertThreshold: 85,
        soilMoistureThreshold: 40,
        readingInterval: 60
      });
      
      setStorageSettings({
        localStorageDuration: 30,
        cloudBackup: true,
        backupFrequency: 7,
        dataCompressionLevel: 6
      });
    }
  };

  // Render the appropriate settings panel based on active tab
  const renderSettingsPanel = () => {
    switch (activeTab) {
      case 'system':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-800">System Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
                <select 
                  name="language"
                  value={systemSettings.language}
                  onChange={handleSystemSettingChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="English">English</option>
                  <option value="Vietnamese">Vietnamese</option>
                  <option value="French">French</option>
                  <option value="Spanish">Spanish</option>
                </select>
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="darkMode"
                  name="darkMode"
                  checked={systemSettings.darkMode}
                  onChange={handleSystemSettingChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="darkMode" className="text-sm font-medium text-gray-700">Dark Mode</label>
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="notifications"
                  name="notifications"
                  checked={systemSettings.notifications}
                  onChange={handleSystemSettingChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="notifications" className="text-sm font-medium text-gray-700">Enable Notifications</label>
              </div>
              
              <div>
                <label htmlFor="dataRefreshRate" className="block text-sm font-medium text-gray-700 mb-1">
                  Data Refresh Rate (minutes)
                </label>
                <input
                  type="number"
                  id="dataRefreshRate"
                  name="dataRefreshRate"
                  value={systemSettings.dataRefreshRate}
                  onChange={handleSystemSettingChange}
                  min="1"
                  max="60"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="autoUpdate"
                  name="autoUpdate"
                  checked={systemSettings.autoUpdate}
                  onChange={handleSystemSettingChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="autoUpdate" className="text-sm font-medium text-gray-700">Auto Update Application</label>
              </div>
            </div>
          </div>
        );
        
      case 'network':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-800">Network Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="serverAddress" className="block text-sm font-medium text-gray-700 mb-1">
                  Server Address
                </label>
                <input
                  type="text"
                  id="serverAddress"
                  name="serverAddress"
                  value={networkSettings.serverAddress}
                  onChange={handleNetworkSettingChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="serverPort" className="block text-sm font-medium text-gray-700 mb-1">
                  Server Port
                </label>
                <input
                  type="text"
                  id="serverPort"
                  name="serverPort"
                  value={networkSettings.serverPort}
                  onChange={handleNetworkSettingChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="connectionTimeout" className="block text-sm font-medium text-gray-700 mb-1">
                  Connection Timeout (seconds)
                </label>
                <input
                  type="number"
                  id="connectionTimeout"
                  name="connectionTimeout"
                  value={networkSettings.connectionTimeout}
                  onChange={handleNetworkSettingChange}
                  min="5"
                  max="120"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="useSSL"
                  name="useSSL"
                  checked={networkSettings.useSSL}
                  onChange={handleNetworkSettingChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="useSSL" className="text-sm font-medium text-gray-700">Use SSL Encryption</label>
              </div>
            </div>
          </div>
        );
        
      case 'sensors':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-800">Sensor Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="tempAlertThreshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Temperature Alert Threshold (°C)
                </label>
                <input
                  type="number"
                  id="tempAlertThreshold"
                  name="tempAlertThreshold"
                  value={sensorSettings.tempAlertThreshold}
                  onChange={handleSensorSettingChange}
                  min="0"
                  max="50"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="humidityAlertThreshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Humidity Alert Threshold (%)
                </label>
                <input
                  type="number"
                  id="humidityAlertThreshold"
                  name="humidityAlertThreshold"
                  value={sensorSettings.humidityAlertThreshold}
                  onChange={handleSensorSettingChange}
                  min="0"
                  max="100"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="soilMoistureThreshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Soil Moisture Threshold (%)
                </label>
                <input
                  type="number"
                  id="soilMoistureThreshold"
                  name="soilMoistureThreshold"
                  value={sensorSettings.soilMoistureThreshold}
                  onChange={handleSensorSettingChange}
                  min="0"
                  max="100"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="readingInterval" className="block text-sm font-medium text-gray-700 mb-1">
                  Sensor Reading Interval (minutes)
                </label>
                <input
                  type="number"
                  id="readingInterval"
                  name="readingInterval"
                  value={sensorSettings.readingInterval}
                  onChange={handleSensorSettingChange}
                  min="1"
                  max="1440"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        );
        
      case 'storage':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-800">Storage Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="localStorageDuration" className="block text-sm font-medium text-gray-700 mb-1">
                  Local Storage Duration (days)
                </label>
                <input
                  type="number"
                  id="localStorageDuration"
                  name="localStorageDuration"
                  value={storageSettings.localStorageDuration}
                  onChange={handleStorageSettingChange}
                  min="1"
                  max="365"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="cloudBackup"
                  name="cloudBackup"
                  checked={storageSettings.cloudBackup}
                  onChange={handleStorageSettingChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="cloudBackup" className="text-sm font-medium text-gray-700">Enable Cloud Backup</label>
              </div>
              
              <div>
                <label htmlFor="backupFrequency" className="block text-sm font-medium text-gray-700 mb-1">
                  Backup Frequency (days)
                </label>
                <input
                  type="number"
                  id="backupFrequency"
                  name="backupFrequency"
                  value={storageSettings.backupFrequency}
                  onChange={handleStorageSettingChange}
                  min="1"
                  max="30"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="dataCompressionLevel" className="block text-sm font-medium text-gray-700 mb-1">
                  Data Compression Level (0-9)
                </label>
                <input
                  type="range"
                  id="dataCompressionLevel"
                  name="dataCompressionLevel"
                  value={storageSettings.dataCompressionLevel}
                  onChange={handleStorageSettingChange}
                  min="0"
                  max="9"
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-right text-sm text-gray-600">
                  {storageSettings.dataCompressionLevel} ({storageSettings.dataCompressionLevel === 0 ? 'No Compression' : 
                    storageSettings.dataCompressionLevel < 3 ? 'Low' : 
                    storageSettings.dataCompressionLevel < 7 ? 'Medium' : 'High'})
                </div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
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
          icon={<SettingsIcon size={20} />} 
          text="Settings" 
          alert={false} 
          active={true}
          to="/settings"
        />
        <SidebarItem 
          icon={<ShieldCheck size={20} />} 
          text="Authenticate" 
          alert={false} 
          active={false}
          to="/auth"
        />
      </Sidebar>

      {/* Main content */}
      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <Card className="w-full">
          <CardContent className="p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">Settings</h1>
            
            {/* Settings Tabs */}
            <div className="flex flex-wrap gap-2 mb-6">
              <button
                onClick={() => setActiveTab('system')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md ${
                  activeTab === 'system' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <User size={18} />
                <span>System</span>
              </button>
              
              <button
                onClick={() => setActiveTab('network')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md ${
                  activeTab === 'network' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Wifi size={18} />
                <span>Network</span>
              </button>
              
              <button
                onClick={() => setActiveTab('sensors')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md ${
                  activeTab === 'sensors' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Thermometer size={18} />
                <span>Sensors</span>
              </button>
              
              <button
                onClick={() => setActiveTab('storage')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md ${
                  activeTab === 'storage' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Database size={18} />
                <span>Storage</span>
              </button>
            </div>
            
            {/* Settings Content */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              {renderSettingsPanel()}
              
              {/* Action buttons */}
              <div className="mt-8 flex flex-wrap gap-4">
                <button
                  onClick={saveSettings}
                  className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  <Save size={18} />
                  <span>Save Settings</span>
                </button>
                
                <button
                  onClick={resetSettings}
                  className="flex items-center gap-2 px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
                >
                  <RefreshCw size={18} />
                  <span>Reset to Defaults</span>
                </button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}