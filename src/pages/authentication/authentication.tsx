import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import { 
  House, TabletSmartphone, Bell, ShieldCheck, 
  Settings, Menu, Check, X, Trash2
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
  
  // States cho IP và QR Code
  const [ipAddresses, setIpAddresses] = useState<string[]>([]);
  const [selectedIP, setSelectedIP] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [qrSize, setQrSize] = useState(200);
  const [showQRCode, setShowQRCode] = useState(false);
  
  // Function cập nhật để lấy IP từ nhiều nguồn
  useEffect(() => {
    const getIPAddresses = async () => {
      try {
        setLoading(true);
        const collectedIPs: string[] = [];
        let hasLocalIP = false;
        
        // 1. Phương pháp 1: Sử dụng WebRTC với nhiều STUN servers
        try {
          // Tạo một mảng các promises để chạy song song
          const stunServers = [
            'stun:stun.l.google.com:19302',
            'stun:stun1.l.google.com:19302',
            'stun:stun2.l.google.com:19302',
            'stun:stun.ekiga.net',
            'stun:stun.ideasip.com',
            'stun:stun.stunprotocol.org:3478',
            'stun:stun.voiparound.com',
            'stun:stun.voipbuster.com',
            'stun:stun.voxgratia.org'
          ];
          
          // Lấy một mẫu ngẫu nhiên từ danh sách STUN servers để giảm tải
          const sampleStunServers = stunServers.sort(() => 0.5 - Math.random()).slice(0, 4);
          
          // Sử dụng Promise.all đúng cách với mảng promises
          const promises: Promise<string | null>[] = [];
          for (const server of sampleStunServers) {
            promises.push(getIPFromWebRTC(server));
          }
          
          // Chạy song song các yêu cầu WebRTC
          const results = await Promise.all(promises);
          
          // Lọc các kết quả null và loại bỏ trùng lặp
          const validIPs = Array.from(new Set(results.filter((ip): ip is string => ip !== null)));
          if (validIPs.length > 0) {
            validIPs.forEach(ip => {
              if (ip && !collectedIPs.includes(ip)) {
                collectedIPs.push(ip);
                if (isLocalIP(ip)) hasLocalIP = true;
              }
            });
          }
        } catch (err) {
          console.error("Lỗi WebRTC:", err);
        }
        
        // 2. Phương pháp 2: Sử dụng RTCDataChannel theo cách khác
        if (!hasLocalIP) {
          try {
            const ip = await getIPWithDataChannel();
            if (ip && !collectedIPs.includes(ip)) {
              collectedIPs.push(ip);
              if (isLocalIP(ip)) hasLocalIP = true;
            }
          } catch (err) {
            console.error("Lỗi RTCDataChannel:", err);
          }
        }
        
        // 3. Phương pháp 3: Thử phương pháp WebRTC với config đặc biệt
        if (!hasLocalIP) {
          try {
            // Thử với config tùy chỉnh
            const ip = await getIPWithSpecialConfig();
            if (ip && !collectedIPs.includes(ip)) {
              collectedIPs.push(ip);
              if (isLocalIP(ip)) hasLocalIP = true;
            }
          } catch (err) {
            console.error("Lỗi với config đặc biệt:", err);
          }
        }
        
        // 4. Phương pháp cuối: API bên ngoài để lấy IP công cộng
        try {
          const response = await fetch('https://api.ipify.org?format=json');
          const data = await response.json();
          if (data.ip && !collectedIPs.includes(data.ip)) {
            collectedIPs.push(data.ip + ' (public)');
          }
        } catch (ipifyErr) {
          console.error("Lỗi ipify:", ipifyErr);
          
          // Thử lại với API dự phòng
          try {
            const response = await fetch('https://api.my-ip.io/ip.json');
            const data = await response.json();
            if (data.ip && !collectedIPs.includes(data.ip)) {
              collectedIPs.push(data.ip + ' (public)');
            }
          } catch (myipErr) {
            console.error("Lỗi my-ip.io:", myipErr);
            
            // Thử dùng dữ liệu mặc định nếu tất cả các phương pháp thất bại
            if (collectedIPs.length === 0) {
              collectedIPs.push('127.0.0.1 (localhost)');
            }
          }
        }
        
        if (collectedIPs.length > 0) {
          setIpAddresses(collectedIPs);
          // Ưu tiên địa chỉ IP nội bộ
          const localIPs = collectedIPs.filter(ip => isLocalIP(ip.split(' ')[0]));
          setSelectedIP(localIPs.length > 0 ? localIPs[0] : collectedIPs[0]);
        } else {
          throw new Error("Không thể lấy địa chỉ IP từ bất kỳ nguồn nào");
        }
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };
    
    getIPAddresses();
  }, []);
  
  // Hàm kiểm tra có phải IP nội bộ không
  const isLocalIP = (ip: string): boolean => {
    return ip.startsWith('192.168.') || 
           ip.startsWith('10.') || 
           (ip.startsWith('172.') && 
            parseInt(ip.split('.')[1]) >= 16 && 
            parseInt(ip.split('.')[1]) <= 31) ||
           ip === '127.0.0.1';
  };

  // Hàm lấy IP từ WebRTC với một STUN server cụ thể
  const getIPFromWebRTC = (stunServer: string): Promise<string | null> => {
    return new Promise((resolve) => {
      try {
        const pc = new RTCPeerConnection({
          iceServers: [{ urls: stunServer }]
        });
        
        pc.createDataChannel("findIP");
        
        // Đặt thời gian timeout cho mỗi request
        const timeoutId = setTimeout(() => {
          pc.close();
          resolve(null);
        }, 5000);
        
        pc.onicecandidate = (event) => {
          if (!event.candidate) return;
          
          // Regex để tìm địa chỉ IPv4
          const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
          const ipMatch = event.candidate.candidate.match(ipRegex);
          
          if (ipMatch && ipMatch[1]) {
            const ip = ipMatch[1];
            if (isLocalIP(ip) && ip !== '0.0.0.0') {
              clearTimeout(timeoutId);
              pc.close();
              resolve(ip);
            }
          }
        };
        
        pc.createOffer()
          .then(offer => pc.setLocalDescription(offer))
          .catch(err => {
            console.error("Lỗi createOffer:", err);
            clearTimeout(timeoutId);
            pc.close();
            resolve(null);
          });
      } catch (err) {
        console.error("Lỗi RTCPeerConnection:", err);
        resolve(null);
      }
    });
  };
  
  // Phương pháp thay thế sử dụng RTCDataChannel
  const getIPWithDataChannel = (): Promise<string | null> => {
    return new Promise((resolve) => {
      try {
        const pc = new RTCPeerConnection();
        
        // Khởi tạo data channel
        pc.createDataChannel("");
        
        // Thiết lập timeout
        const timeoutId = setTimeout(() => {
          pc.close();
          resolve(null);
        }, 5000);
        
        // Lắng nghe ice candidates
        pc.onicecandidate = (e) => {
          if (!e.candidate) return;
          
          const candidateStr = e.candidate.candidate;
          // Regex tìm địa chỉ IP
          const match = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(candidateStr);
          
          if (match) {
            const ip = match[1];
            if (isLocalIP(ip) && ip !== '0.0.0.0') {
              clearTimeout(timeoutId);
              pc.close();
              resolve(ip);
            }
          }
        };
        
        // Khởi tạo quá trình tạo ICE candidates
        pc.createOffer()
          .then(offer => pc.setLocalDescription(offer))
          .catch(err => {
            console.error("Lỗi setLocalDescription:", err);
            clearTimeout(timeoutId);
            pc.close();
            resolve(null);
          });
      } catch (err) {
        console.error("Lỗi tạo RTCDataChannel:", err);
        resolve(null);
      }
    });
  };
  
  // Phương pháp với cấu hình đặc biệt
  const getIPWithSpecialConfig = (): Promise<string | null> => {
    return new Promise((resolve) => {
      try {
        // Sử dụng nhiều servers và config đặc biệt
        const pc = new RTCPeerConnection({
          iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' }
          ],
          iceCandidatePoolSize: 10,
          iceTransportPolicy: 'all'
        });
        
        const dc = pc.createDataChannel("special-config-channel");
        
        // Thiết lập timeout
        const timeoutId = setTimeout(() => {
          pc.close();
          resolve(null);
        }, 5000);
        
        // Tìm kiếm trong SDP khi không có ICE candidates
        pc.onicegatheringstatechange = () => {
          if (pc.iceGatheringState === 'complete') {
            const sdp = pc.localDescription?.sdp || '';
            const matches = sdp.match(/c=IN IP4 ([0-9]{1,3}(\.[0-9]{1,3}){3})/g);
            
            if (matches) {
              for (const match of matches) {
                const ipMatch = match.match(/([0-9]{1,3}(\.[0-9]{1,3}){3})/);
                if (ipMatch && ipMatch[1]) {
                  const ip = ipMatch[1];
                  if (isLocalIP(ip) && ip !== '0.0.0.0') {
                    clearTimeout(timeoutId);
                    pc.close();
                    resolve(ip);
                    return;
                  }
                }
              }
            }
          }
        };
        
        // Phương pháp thông thường
        pc.onicecandidate = (e) => {
          if (!e.candidate) return;
          
          // Regex để tìm địa chỉ IPv4
          const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
          const ipMatch = e.candidate.candidate.match(ipRegex);
          
          if (ipMatch && ipMatch[1]) {
            const ip = ipMatch[1];
            if (isLocalIP(ip) && ip !== '0.0.0.0') {
              clearTimeout(timeoutId);
              pc.close();
              resolve(ip);
            }
          }
        };
        
        // Tạo offer và set local description
        pc.createOffer()
          .then(offer => pc.setLocalDescription(offer))
          .catch(err => {
            console.error("Lỗi createOffer trong config đặc biệt:", err);
            clearTimeout(timeoutId);
            pc.close();
            resolve(null);
          });
      } catch (err) {
        console.error("Lỗi cấu hình đặc biệt:", err);
        resolve(null);
      }
    });
  };
  
  // Tạo URL cho mã QR
  const getQRCodeUrl = () => {
    if (!selectedIP) return '';
    // Chỉ sử dụng phần IP, không bao gồm phần mô tả
    const ipPart = selectedIP.split(' ')[0];
    return `https://chart.googleapis.com/chart?cht=qr&chl=${encodeURIComponent(ipPart)}&chs=${qrSize}x${qrSize}&choe=UTF-8`;
  };
  
  const handleSizeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQrSize(parseInt(e.target.value, 10));
  };
  
  const handleIPChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedIP(e.target.value);
  };
  
  const copyToClipboard = () => {
    // Chỉ sao chép phần IP, không bao gồm phần mô tả
    const ipPart = selectedIP.split(' ')[0];
    navigator.clipboard.writeText(ipPart)
      .then(() => alert('Đã sao chép địa chỉ IP vào clipboard!'))
      .catch(err => console.error('Không thể sao chép:', err));
  };

  const handleDeleteUser = (userId: string) => {
    setUsers(users.filter(user => user.id !== userId));
  };

  return (
    <main className="flex min-h-screen bg-gray-50">
      {/* Main content */}
      <div className="flex-1 mt-16 p-4 sm:p-6 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
        <h1 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6">Authentication</h1>
        
        {/* IP Address & QR Code Card */}
        <Card className="w-full mb-6">
          <CardContent className="p-4">
            <h2 className="text-lg font-semibold mb-4">Địa chỉ IP của bạn</h2>
            
            {loading ? (
              <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                <span className="ml-3 text-gray-600">Đang lấy địa chỉ IP...</span>
              </div>
            ) : error ? (
              <div className="text-red-500 text-center py-4">{error}</div>
            ) : (
              <div className="space-y-4">
                {ipAddresses.length > 0 ? (
                  <>
                    <div className="flex flex-col space-y-2">
                      <div className="flex items-center justify-between">
                        <label htmlFor="ip-select" className="text-sm font-medium">Chọn địa chỉ IP:</label>
                        <div className="flex items-center">
                          <select 
                            id="ip-select"
                            value={selectedIP} 
                            onChange={handleIPChange}
                            className="p-2 border border-gray-300 rounded-l"
                          >
                            {ipAddresses.map((ip, index) => (
                              <option key={index} value={ip}>{ip}</option>
                            ))}
                          </select>
                          <button 
                            onClick={copyToClipboard}
                            className="p-2 bg-blue-500 text-white rounded-r hover:bg-blue-600"
                            title="Sao chép địa chỉ IP"
                          >
                            📋
                          </button>
                        </div>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <button
                          onClick={() => setShowQRCode(!showQRCode)}
                          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                          {showQRCode ? "Ẩn mã QR" : "Hiển thị mã QR"}
                        </button>
                        
                        {showQRCode && (
                          <div className="flex items-center">
                            <span className="text-sm mr-2">Kích thước: {qrSize}x{qrSize}</span>
                            <input
                              type="range"
                              min="128"
                              max="300"
                              step="10"
                              value={qrSize}
                              onChange={handleSizeChange}
                              className="w-32 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                            />
                          </div>
                        )}
                      </div>
                    </div>
                    
                    {showQRCode && selectedIP && (
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
                  </>
                ) : (
                  <div className="text-center text-red-500">
                    Không tìm thấy địa chỉ IP nào. Vui lòng thử lại sau.
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
        
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