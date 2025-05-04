import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import {
  House, TabletSmartphone, Bell, ShieldCheck,
  Settings, Menu, Check, X, Trash2, RefreshCw, Wifi
} from 'lucide-react';
import { Card, CardContent } from '../../components/ui/card.tsx';
import { QRCodeSVG } from 'qrcode.react';

// Import file JSON (React hỗ trợ sẵn import JSON)
import ipData from './ip.json';

export default function Authentication() {
  // Lấy IP và tên WiFi từ file JSON
  const ipAddress = ipData.ipAddress;
  const wifiName = ipData.wifiName || "Không xác định";
  
  // State để lưu token ngẫu nhiên và thời gian còn lại
  const [token, setToken] = useState<string>(generateRandomToken());
  const [timeLeft, setTimeLeft] = useState<number>(300); // 300 giây = 5 phút
  
  // Tạo URL kèm theo port 3000 và token
  const fullUrl = `http://${ipAddress}:3000?token=${token}`;
  
  // Hàm tạo token ngẫu nhiên
  function generateRandomToken(): string {
    return Math.random().toString(36).substring(2, 15);
  }
  
  // Hàm làm mới token
  function refreshToken() {
    setToken(generateRandomToken());
    setTimeLeft(300); // Reset thời gian về 5 phút
  }
  
  // Effect để làm mới token mỗi 5 phút
  useEffect(() => {
    // Tạo interval làm mới token mỗi 5 phút
    const tokenInterval = setInterval(() => {
      refreshToken();
    }, 5 * 60 * 1000); // 5 phút = 5 * 60 * 1000 mili giây
    
    // Tạo interval để đếm ngược thời gian
    const timerInterval = setInterval(() => {
      setTimeLeft(prevTime => {
        if (prevTime <= 1) {
          return 300; // Sẽ được reset bởi refreshToken() khi hết thời gian
        }
        return prevTime - 1;
      });
    }, 1000); // Mỗi giây
    
    // Cleanup các interval khi component unmount
    return () => {
      clearInterval(tokenInterval);
      clearInterval(timerInterval);
    };
  }, []);
  
  // Định dạng thời gian còn lại thành phút:giây
  const formatTimeLeft = (): string => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
  };
  
  return (
    <main className="flex min-h-screen bg-gray-50">
      {/* Main content */}
      <div className="flex-1 mt-16 p-4 sm:p-6 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <h1 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6">Authentication</h1>
        
        {/* IP Address & QR Code Card */}
        <Card className="w-full mb-6">
          <CardContent className="p-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Thông tin mạng</h2>
              <button 
                onClick={refreshToken}
                className="flex items-center px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md transition-colors"
              >
                <RefreshCw className="w-4 h-4 mr-1" />
                <span>Làm mới</span>
              </button>
            </div>
            
            <div className="mb-4">
              {/* <h1 className="text-xl font-bold text-blue-600">{ipAddress}:3000</h1> */}
              <div className="flex items-center mt-1 text-gray-600">
                <Wifi className="w-4 h-4 mr-1" />
                <span className="text-base font-medium">WiFi: {wifiName}</span>
              </div>
            </div>
            
            <div className="flex flex-col items-center mt-6">
              <h3 className="text-md font-medium mb-3">Quét mã QR để truy cập</h3>
              
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <QRCodeSVG
                  value={fullUrl}
                  size={200}
                  bgColor={"#ffffff"}
                  fgColor={"#000000"}
                  level={"L"}
                  includeMargin={false}
                />
              </div>
              
              <div className="mt-3">
                <span className="text-sm font-medium text-orange-600">
                  Làm mới sau: {formatTimeLeft()}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}