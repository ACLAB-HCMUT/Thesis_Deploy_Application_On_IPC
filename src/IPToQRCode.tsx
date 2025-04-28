import React, { useState, useEffect } from 'react';

const IPToQRCode = () => {
  const [ipAddress, setIpAddress] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [qrSize, setQrSize] = useState(256);
  
  useEffect(() => {
    const getIPAddress = async () => {
      try {
        setLoading(true);
        
        // Phương pháp 1: Sử dụng WebRTC để lấy địa chỉ IP nội bộ
        const getLocalIP = async () => {
          return new Promise((resolve, reject) => {
            // Tạo kết nối RTCPeerConnection
            const rtc = new RTCPeerConnection({
              iceServers: []
            });
            
            // Thêm một kênh dữ liệu trống (cần thiết để tạo ICE candidates)
            rtc.createDataChannel('');
            
            // Tạo một đề nghị và thiết lập description nội bộ
            rtc.createOffer()
              .then(offer => rtc.setLocalDescription(offer))
              .catch(reject);
            
            // Khi ICE candidate được tạo, tìm địa chỉ IPv4
            rtc.onicecandidate = (event) => {
              if (!event.candidate) return;
              
              // Regex để tìm địa chỉ IPv4
              const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
              const ipMatch = event.candidate.candidate.match(ipRegex);
              
              if (ipMatch && ipMatch[1]) {
                const ip = ipMatch[1];
                // Kiểm tra nếu là địa chỉ IP nội bộ
                if (
                  ip.startsWith('192.168.') || 
                  ip.startsWith('10.') || 
                  ip.startsWith('172.') ||
                  ip !== '0.0.0.0'
                ) {
                  resolve(ip);
                  rtc.close();
                }
              }
            };
            
            // Nếu không tìm thấy sau 5 giây, trả về lỗi
            setTimeout(() => {
              reject(new Error('Không thể tìm thấy địa chỉ IP trong thời gian chờ'));
              rtc.close();
            }, 5000);
          });
        };
      
        try {
          const ip = await getLocalIP();
          setIpAddress(ip as string);
        } catch (webrtcError) {
          console.error('Lỗi khi lấy IP qua WebRTC:', webrtcError);
          
          // Phương pháp dự phòng: Sử dụng API bên ngoài để lấy IP
          try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            setIpAddress(data.ip as string);
            console.log('Đã lấy IP công cộng:', data.ip);
          } catch (apiError) {
            throw new Error('Không thể lấy địa chỉ IP');
          }
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    getIPAddress();
  }, []);
  
  // Tạo URL cho mã QR
  const getQRCodeUrl = () => {
    if (!ipAddress) return '';
    
    // Sử dụng Google Chart API để tạo mã QR
    return `https://chart.googleapis.com/chart?cht=qr&chl=${encodeURIComponent(ipAddress)}&chs=${qrSize}x${qrSize}&choe=UTF-8`;
  };
  
  const handleSizeChange = (e) => {
    setQrSize(parseInt(e.target.value, 10));
  };
  
  const copyToClipboard = () => {
    navigator.clipboard.writeText(ipAddress)
      .then(() => alert('Đã sao chép địa chỉ IP vào clipboard!'))
      .catch(err => console.error('Không thể sao chép:', err));
  };
  
  return (
    <div className="flex flex-col items-center p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-6">
      <h1 className="text-2xl font-bold text-blue-600">IP to QR Code Generator</h1>
      
      {loading ? (
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Đang lấy địa chỉ IP...</span>
        </div>
      ) : error ? (
        <div className="text-red-500 text-center">{error}</div>
      ) : (
        <div className="w-full space-y-4">
          <div className="flex items-center justify-between">
            <div className="text-lg font-medium">Địa chỉ IP của bạn:</div>
            <div className="flex items-center">
              <span className="font-mono bg-gray-100 px-3 py-1 rounded">{ipAddress}</span>
              <button 
                onClick={copyToClipboard}
                className="ml-2 p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                title="Sao chép địa chỉ IP"
              >
                📋
              </button>
            </div>
          </div>
          
          <div className="flex flex-col items-center space-y-4">
            <div className="w-full">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Kích thước mã QR: {qrSize}x{qrSize}
              </label>
              <input
                type="range"
                min="128"
                max="512"
                step="32"
                value={qrSize}
                onChange={handleSizeChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            
            {ipAddress && (
              <div className="flex flex-col items-center p-4 border rounded-lg">
                <img
                  src={getQRCodeUrl()}
                  alt="QR Code for IP Address"
                  className="border rounded"
                />
                <p className="mt-2 text-sm text-gray-500">
                  Quét mã QR để lấy địa chỉ IP
                </p>
              </div>
            )}
            
            <div className="text-sm text-gray-500 text-center">
              <p>Mã QR này chứa địa chỉ IP của thiết bị của bạn.</p>
              <p>Quét mã này để dễ dàng kết nối với thiết bị của bạn trong mạng nội bộ.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IPToQRCode;