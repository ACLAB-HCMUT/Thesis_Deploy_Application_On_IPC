import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import { 
  House,
  TabletSmartphone, Bell, ShieldCheck, Settings as SettingsIcon,
  Menu, User, Globe,
  Bell as BellIcon,
  Wifi, Database,
  HardDrive, Save,
  RefreshCw, Thermometer, Sun
} from 'lucide-react';
import { Card, CardContent } from '../../components/ui/card.tsx';
import axios from 'axios';

// Define API base URL
const API_BASE_URL = 'http://localhost:8000/api'; // Update with your actual server URL

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

// Update SensorSettings to match backend threshold fields
interface SensorSettings {
  temperature_threshold: number;
  humidity_threshold: number;
  humidity_soil_threshold: number;
  light_threshold: number;
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
  const [activeTab, setActiveTab] = useState('sensors'); // Default to sensors tab
  const [isLoading, setIsLoading] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState("");
  
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
  
  // Update sensor settings to match backend field names
  const [sensorSettings, setSensorSettings] = useState<SensorSettings>({
    temperature_threshold: 30,
    humidity_threshold: 85,
    humidity_soil_threshold: 40,
    light_threshold: 1000,
    readingInterval: 60
  });
  
  const [storageSettings, setStorageSettings] = useState<StorageSettings>({
    localStorageDuration: 30,
    cloudBackup: true,
    backupFrequency: 7,
    dataCompressionLevel: 6
  });

  // Fetch threshold settings from backend
  useEffect(() => {
    fetchThresholdSettings();
  }, []);

  // Function to show toast message temporarily
  const showToast = (success: boolean, message: string) => {
    if (success) {
      setSaveSuccess(true);
      setSaveError("");
      setTimeout(() => setSaveSuccess(false), 3000);
    } else {
      setSaveError(message);
      setTimeout(() => setSaveError(""), 3000);
    }
  };

  const fetchThresholdSettings = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/setup/threshold`);
      
      if (response.data && response.data.status === 200) {
        const thresholdData = response.data.data;
        
        // Update the sensor settings with data from backend
        setSensorSettings(prevSettings => ({
          ...prevSettings,
          temperature_threshold: thresholdData.temperature_threshold || prevSettings.temperature_threshold,
          humidity_threshold: thresholdData.humidity_threshold || prevSettings.humidity_threshold,
          humidity_soil_threshold: thresholdData.humidity_soil_threshold || prevSettings.humidity_soil_threshold,
          light_threshold: thresholdData.light_threshold || prevSettings.light_threshold
        }));
        
        showToast(true, "Threshold settings loaded successfully");
      } else {
        // Handle case where status is not 200
        console.warn("Unexpected response structure:", response.data);
        showToast(false, response.data?.message || "Error loading threshold settings");
      }
    } catch (error) {
      console.error("Error fetching threshold settings:", error);
      showToast(false, "Failed to load threshold settings. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Save threshold settings to backend
  const saveThresholdSettings = async () => {
    setIsLoading(true);
    try {
      const thresholdData = {
        temperature_threshold: sensorSettings.temperature_threshold,
        humidity_threshold: sensorSettings.humidity_threshold,
        humidity_soil_threshold: sensorSettings.humidity_soil_threshold,
        light_threshold: sensorSettings.light_threshold
      };
      
      const response = await axios.put(`${API_BASE_URL}/setup/threshold`, thresholdData);
      
      if (response.data && response.data.status === 200) {
        showToast(true, "Threshold settings saved successfully");
      } else {
        showToast(false, response.data?.message || "Unexpected response from server");
      }
    } catch (error) {
      console.error("Error saving threshold settings:", error);
      showToast(false, "Failed to save threshold settings. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Reset threshold settings to zero
  const resetThresholdSettings = async () => {
    if (window.confirm('Are you sure you want to reset all threshold settings to zero?')) {
      setIsLoading(true);
      try {
        const response = await axios.delete(`${API_BASE_URL}/setup/threshold`);
        
        if (response.data && response.data.status === 200) {
          // Reset local state as well
          setSensorSettings(prevSettings => ({
            ...prevSettings,
            temperature_threshold: 0,
            humidity_threshold: 0,
            humidity_soil_threshold: 0,
            light_threshold: 0
          }));
          showToast(true, "Threshold settings reset successfully");
        } else {
          showToast(false, response.data?.message || "Unexpected response from server");
        }
      } catch (error) {
        console.error("Error resetting threshold settings:", error);
        showToast(false, "Failed to reset threshold settings. Please try again.");
      } finally {
        setIsLoading(false);
      }
    }
  };
  
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
    // Different save actions based on active tab
    if (activeTab === 'sensors') {
      saveThresholdSettings();
    } else {
      // For other tabs, just show a mock success message
      console.log('Saving settings:', {
        systemSettings,
        networkSettings,
        sensorSettings,
        storageSettings
      });
      
      // Show a success message
      showToast(true, `${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} settings saved successfully!`);
    }
  };
  
  const resetSettings = () => {
    if (activeTab === 'sensors') {
      resetThresholdSettings();
    } else {
      if (window.confirm(`Are you sure you want to reset all ${activeTab} settings to default values?`)) {
        // Reset to default values based on active tab
        switch (activeTab) {
          case 'system':
            setSystemSettings({
              language: 'English',
              darkMode: false,
              notifications: true,
              dataRefreshRate: 15,
              autoUpdate: true
            });
            break;
          
          case 'network':
            setNetworkSettings({
              serverAddress: '176.23.43.54',
              serverPort: '5000',
              connectionTimeout: 30,
              useSSL: true
            });
            break;
          
          case 'storage':
            setStorageSettings({
              localStorageDuration: 30,
              cloudBackup: true,
              backupFrequency: 7,
              dataCompressionLevel: 6
            });
            break;
        }
        
        showToast(true, `${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} settings reset to defaults`);
      }
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
            <h2 className="text-xl font-bold text-gray-800">Sensor Thresholds</h2>
            <p className="text-sm text-gray-600 mb-4">
              Set threshold values for automated alerts and actions when sensor readings exceed these values.
            </p>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="temperature_threshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Temperature Threshold (°C)
                </label>
                <div className="flex items-center">
                  <input
                    type="number"
                    id="temperature_threshold"
                    name="temperature_threshold"
                    value={sensorSettings.temperature_threshold}
                    onChange={handleSensorSettingChange}
                    min="0"
                    max="50"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="ml-2">
                    <Thermometer size={20} className="text-red-500" />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  System will alert when temperature exceeds this value
                </p>
              </div>
              
              <div>
                <label htmlFor="humidity_threshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Air Humidity Threshold (%)
                </label>
                <div className="flex items-center">
                  <input
                    type="number"
                    id="humidity_threshold"
                    name="humidity_threshold"
                    value={sensorSettings.humidity_threshold}
                    onChange={handleSensorSettingChange}
                    min="0"
                    max="100"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="ml-2">
                    <Wifi size={20} className="text-blue-500" />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  System will alert when air humidity exceeds this percentage
                </p>
              </div>
              
              <div>
                <label htmlFor="humidity_soil_threshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Soil Moisture Threshold (%)
                </label>
                <div className="flex items-center">
                  <input
                    type="number"
                    id="humidity_soil_threshold"
                    name="humidity_soil_threshold"
                    value={sensorSettings.humidity_soil_threshold}
                    onChange={handleSensorSettingChange}
                    min="0"
                    max="100"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="ml-2">
                    <Database size={20} className="text-green-700" />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  System will trigger irrigation when soil moisture falls below this percentage
                </p>
              </div>
              
              <div>
                <label htmlFor="light_threshold" className="block text-sm font-medium text-gray-700 mb-1">
                  Light Intensity Threshold (lux)
                </label>
                <div className="flex items-center">
                  <input
                    type="number"
                    id="light_threshold"
                    name="light_threshold"
                    value={sensorSettings.light_threshold}
                    onChange={handleSensorSettingChange}
                    min="0"
                    max="100000"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="ml-2">
                    <Sun size={20} className="text-yellow-500" />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  System will adjust light sources based on this threshold
                </p>
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
      {/* Main content */}
      <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <Card className="w-full">
          <CardContent className="p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">Settings</h1>
            
            {/* Toast notifications */}
            {saveSuccess && (
              <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded relative">
                <span className="block sm:inline">Settings saved successfully!</span>
                <button 
                  className="absolute top-0 right-0 px-2 py-1" 
                  onClick={() => setSaveSuccess(false)}
                >
                  ×
                </button>
              </div>
            )}
            
            {saveError && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded relative">
                <span className="block sm:inline">{saveError}</span>
                <button 
                  className="absolute top-0 right-0 px-2 py-1" 
                  onClick={() => setSaveError("")}
                >
                  ×
                </button>
              </div>
            )}
            
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
              {isLoading ? (
                <div className="flex justify-center items-center h-40">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
                </div>
              ) : (
                renderSettingsPanel()
              )}
              
              {/* Action buttons */}
              <div className="mt-8 flex flex-wrap gap-4">
                <button
                  onClick={saveSettings}
                  disabled={isLoading}
                  className={`flex items-center gap-2 px-6 py-2 ${
                    isLoading 
                      ? 'bg-gray-400 cursor-not-allowed' 
                      : 'bg-blue-600 hover:bg-blue-700'
                  } text-white rounded-md transition-colors`}
                >
                  <Save size={18} />
                  <span>{isLoading ? 'Saving...' : 'Save Settings'}</span>
                </button>
                
                <button
                  onClick={resetSettings}
                  disabled={isLoading}
                  className={`flex items-center gap-2 px-6 py-2 ${
                    isLoading 
                      ? 'bg-gray-300 cursor-not-allowed' 
                      : 'bg-gray-200 hover:bg-gray-300'
                  } text-gray-700 rounded-md transition-colors`}
                >
                  <RefreshCw size={18} />
                  <span>{isLoading ? 'Resetting...' : 'Reset to Defaults'}</span>
                </button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}