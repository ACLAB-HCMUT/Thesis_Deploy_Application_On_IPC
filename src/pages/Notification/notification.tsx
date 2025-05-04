import React, { useState, useEffect, useRef } from 'react';
import { Calendar, Search, Trash2, Bell, Check, Menu, AlertCircle } from 'lucide-react';
// Import các utilities
import { 
  showGlobalNotification, 
  showStandardNotification, 
  showPredictionNotification, 
  showAlertNotification, 
  markNotificationAsRead 
} from '../../utils/NotificationUtils.tsx';
// Thêm interface Alert vào đầu file, dưới interface Prediction
interface Alert {
  issue: string;
  severity: string;
  recommendation: string;
  device: string;
}

interface Prediction {
  harvest_date?: string;
  confidence?: number;
  days_remaining?: number;
  crop_health?: string;
  crop_type?: string;
  care_recommendation?: string;
  develop_stage?: string;    // Thêm trường mới
  risk?: string;             // Thêm trường mới
  symptom?: string;          // Thêm trường mới
  device_id?: string;        // Thêm trường từ ai_simulator_controller
  sensor_data?: any;         // Thêm trường từ ai_simulator_controller
  timestamp?: string;        // Thêm trường từ ai_simulator_controller
  estimated_yield?: string;  // Thêm trường từ ai_simulator_controller
  health_issues?: string[];  // Thêm trường từ ai_simulator_controller
  recommendations?: string[]; // Thêm trường từ ai_simulator_controller       
}

interface Notification {
  id: number;
  title: string;
  message: string;
  date: string;
  isRead: boolean;
  prediction?: Prediction;
  alert?: Alert;
  type?: string; 
}

const NotificationPage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([
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
    }
  ]);

  const [searchQuery, setSearchQuery] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [newNotification, setNewNotification] = useState<Notification | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const notificationTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  // State cho widget dự đoán AI
  const [aiPredictions, setAiPredictions] = useState<Prediction[]>([]);
  const [latestPrediction, setLatestPrediction] = useState<Prediction | null>(null); 
  const [isAIPredictionExpanded, setIsAIPredictionExpanded] = useState(true);
  
  // State cho phân trang
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(5);

  // Cải thiện: Function cập nhật số lượng thông báo chưa đọc
  const updateUnreadCount = (count: number) => {
    console.log("Broadcasting notification update with count:", count);
    
    // Tạo và dispatch custom event với unread count
    const event = new CustomEvent('notificationUpdate', {
      detail: { unreadCount: count }
    });
    
    // Đảm bảo event được gửi đi
    window.dispatchEvent(event);
  };
  
  // Hàm xử lý thay đổi số lượng thông báo mỗi trang
  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newItemsPerPage = parseInt(e.target.value, 10);
    setItemsPerPage(newItemsPerPage);
    // Reset về trang đầu tiên khi thay đổi số lượng item mỗi trang
    setCurrentPage(1);
  };

  // Hàm định dạng thời gian Việt Nam
  const formatVietnameseDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('vi-VN', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch (error) {
      console.error('Error formatting date:', error);
      return dateString;
    }
  };

  // Cập nhật unreadCount ngay khi component mount
  useEffect(() => {
    const unreadCount = notifications.filter(n => !n.isRead).length;
    updateUnreadCount(unreadCount);
    console.log("Initial unread count:", unreadCount);
  }, []);

  // Kết nối WebSocket
  useEffect(() => {
    console.log("Connecting to WebSocket...");
    
    // Tạo kết nối WebSocket
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws/relay');
      wsRef.current = ws;
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
      };
      
      ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);
        try {
          const message = JSON.parse(event.data);
          
          // Xử lý thông báo dự đoán AI tự động
          if (message.type === 'ai_prediction') {
            console.log('AI prediction received:', message);
            
            if (message.prediction) {
              // Cập nhật state cho dự đoán mới nhất
              setLatestPrediction(message.prediction);
              
              // Thêm vào danh sách dự đoán
              setAiPredictions(prev => {
                // Giới hạn chỉ giữ 5 dự đoán gần nhất
                const newPredictions = [message.prediction, ...prev].slice(0, 5);
                return newPredictions;
              });
              
              // Tạo và hiển thị thông báo dự đoán
              const notificationId = showPredictionNotification(
                'Dự đoán thu hoạch AI',
                message.message || 'Hệ thống đã tạo dự đoán thu hoạch mới',
                message.prediction
              );
              
              // Thêm vào danh sách thông báo trong trang notification
              const newNotification: Notification = {
                id: notificationId,
                title: 'Dự đoán thu hoạch AI',
                message: message.message || 'Hệ thống đã tạo dự đoán thu hoạch mới',
                date: new Date().toISOString().split('T')[0],
                isRead: false,
                prediction: message.prediction,
                type: 'prediction'
              };
              
              // Hiển thị thông báo tạm thời trong trang notification
              setNewNotification(newNotification);
              
              if (notificationTimeoutRef.current) {
                clearTimeout(notificationTimeoutRef.current);
              }
              
              notificationTimeoutRef.current = setTimeout(() => {
                setNewNotification(null);
              }, 5000);
              
              // Thêm vào danh sách thông báo
              setNotifications(prev => {
                const updatedNotifications = [newNotification, ...prev];
                const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
                updateUnreadCount(newUnreadCount);
                return updatedNotifications;
              });
            }
          }
          // Xử lý cho thông báo cảnh báo AI
          else if (message.type === 'ai_alert') {
            console.log('AI alert received:', message);
            
            // Tạo và hiển thị thông báo cảnh báo
            const notificationId = showAlertNotification(
              'Cảnh báo từ thiết bị',
              message.message || 'Hệ thống phát hiện vấn đề cần chú ý',
              message.alert
            );
            
            // Tạo thông báo cảnh báo mới cho trang notification
            const newNotification: Notification = {
              id: notificationId,
              title: 'Cảnh báo từ thiết bị',
              message: message.message || 'Hệ thống phát hiện vấn đề cần chú ý',
              date: new Date().toISOString().split('T')[0],
              isRead: false,
              alert: message.alert,
              type: 'alert'
            };
            
            // Thêm vào danh sách thông báo
            setNotifications(prev => {
              const updatedNotifications = [newNotification, ...prev];
              const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
              updateUnreadCount(newUnreadCount);
              return updatedNotifications;
            });
            
            // Hiển thị thông báo tạm thời
            setNewNotification(newNotification);
            
            if (notificationTimeoutRef.current) {
              clearTimeout(notificationTimeoutRef.current);
            }
            
            notificationTimeoutRef.current = setTimeout(() => {
              setNewNotification(null);
            }, 5000);
          }
          // Xử lý thông báo thông thường
          else if (message.type === 'notification') {
            // Tạo và hiển thị thông báo tiêu chuẩn
            const notificationId = showStandardNotification(
              message.title || 'Thông báo mới',
              message.message || ''
            );
            
            // Tạo thông báo mới cho trang notification
            const newNotification: Notification = {
              id: notificationId,
              title: message.title || 'Thông báo mới',
              message: message.message || '',
              date: new Date().toISOString().split('T')[0],
              isRead: false,
              type: 'standard'
            };
            
            // Thêm vào danh sách thông báo
            setNotifications(prev => {
              const updatedNotifications = [newNotification, ...prev];
              const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
              updateUnreadCount(newUnreadCount);
              return updatedNotifications;
            });
            
            // Hiển thị thông báo tạm thời
            setNewNotification(newNotification);
            
            if (notificationTimeoutRef.current) {
              clearTimeout(notificationTimeoutRef.current);
            }
            
            notificationTimeoutRef.current = setTimeout(() => {
              setNewNotification(null);
            }, 5000);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        
        // Thử kết nối lại sau 5 giây
        setTimeout(connectWebSocket, 5000);
      };
    };
    
    // Khởi tạo kết nối
    connectWebSocket();
    
    // Dọn dẹp khi component unmount
    return () => {
      console.log('Closing WebSocket connection');
      if (wsRef.current) {
        wsRef.current.close();
      }
      
      if (notificationTimeoutRef.current) {
        clearTimeout(notificationTimeoutRef.current);
      }
    };
  }, []);

  // Đảm bảo luôn cập nhật unreadCount khi notifications thay đổi
  useEffect(() => {
    const unreadCount = notifications.filter(n => !n.isRead).length;
    updateUnreadCount(unreadCount);
    console.log("Updated unread count:", unreadCount);
  }, [notifications]);

  // Hàm gửi yêu cầu dự đoán thủ công
const handlePredict = async () => {
  console.log("Sending prediction request...");
  try {
    // Cập nhật URL để sử dụng endpoint mới
    const response = await fetch('http://localhost:8000/api/ai-simulator/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 1,
        // Các trường mới (không bao gồm ngày thu hoạch và ngày còn lại)
        care_recommendation: "Tăng cường Nito", 
        develop_stage: "Phát triển",
        risk: "Dễ bị bệnh",
        symptom: "lá héo",
        // Dữ liệu về cây trồng
        crop_type: "Cà chua",
        crop_health: "Trung bình",
        // Message hiển thị trên thông báo
        message: "Phát hiện tình trạng thiếu dưỡng chất trên cây Cà chua"
      }),
    });
    
    const data = await response.json();
    console.log('Prediction response:', data);
    
    if (!response.ok) {
      throw new Error(data.message || 'Prediction failed');
    }
    
    // Xử lý thông báo từ response
    if (data.success && data.prediction) {
      // Tạo và hiển thị thông báo dự đoán sử dụng GlobalNotification
      const notificationId = showPredictionNotification(
        'Dự đoán phân tích cây trồng',
        data.message || 'Hệ thống đã phân tích tình trạng cây trồng của bạn',
        data.prediction
      );
      
      const newNotification: Notification = {
        id: notificationId,
        title: 'Phân tích cây trồng',
        message: data.message || 'Hệ thống đã phân tích tình trạng cây trồng của bạn',
        date: new Date().toISOString().split('T')[0],
        isRead: false,
        prediction: data.prediction,
        type: 'prediction'
      };
      
      // Cập nhật state
      setNotifications(prev => {
        const updatedNotifications = [newNotification, ...prev];
        const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
        updateUnreadCount(newUnreadCount);
        return updatedNotifications;
      });
    }
  } catch (error) {
    console.error('Error:', error);
    alert(`Lỗi khi gửi yêu cầu dự đoán: ${error.message}`);
  }
};

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
      const filtered = notifs.filter(n => 
        n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.message.toLowerCase().includes(searchQuery.toLowerCase())
      );
      if (filtered.length > 0) {
        acc[date] = filtered;
      }
      return acc;
    }, {}
  );

  // Xử lý đánh dấu đã đọc cho một thông báo
  const handleMarkAsRead = (id: number) => {
    // Sử dụng hàm utility để đánh dấu thông báo đã đọc
    markNotificationAsRead(id);
    
    // Cập nhật state trong trang notification
    setNotifications(prevNotifications => {
      const updatedNotifications = prevNotifications.map(notification => {
        if (notification.id === id) {
          return { ...notification, isRead: true };
        }
        return notification;
      });
      
      // Cập nhật số lượng thông báo chưa đọc
      const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
      updateUnreadCount(newUnreadCount);
      
      return updatedNotifications;
    });
  };

  // Xử lý đánh dấu tất cả đã đọc
  const handleMarkAllAsRead = () => {
    // Đánh dấu từng thông báo là đã đọc
    notifications.forEach(notification => {
      if (!notification.isRead) {
        markNotificationAsRead(notification.id);
      }
    });
    
    // Cập nhật state trong trang notification
    setNotifications(prevNotifications => {
      const updatedNotifications = prevNotifications.map(notification => ({
        ...notification,
        isRead: true
      }));
      
      // Cập nhật số lượng thông báo chưa đọc (sẽ là 0)
      updateUnreadCount(0);
      
      return updatedNotifications;
    });
  };

  // Xử lý xóa một thông báo
  const handleDeleteNotification = (id: number) => {
    setNotifications(prevNotifications => {
      const updatedNotifications = prevNotifications.filter(notification => notification.id !== id);
      
      // Cập nhật số lượng thông báo chưa đọc
      const newUnreadCount = updatedNotifications.filter(n => !n.isRead).length;
      updateUnreadCount(newUnreadCount);
      
      return updatedNotifications;
    });
  };

  // Hàm hiển thị chi tiết dự đoán
  // Hàm hiển thị chi tiết dự đoán - Đã loại bỏ ngày thu hoạch và ngày còn lại
const renderPredictionDetails = (prediction: Prediction) => {
  return (
    <div className="mt-2 bg-blue-50 p-3 rounded-lg">
      <h4 className="font-medium text-blue-800 mb-2">Chi tiết phân tích:</h4>
      <div className="grid grid-cols-2 gap-2 text-sm">
        {prediction.crop_type && (
          <div>
            <span className="font-medium">Loại cây trồng:</span> {prediction.crop_type}
          </div>
        )}
        
        {prediction.develop_stage && (
          <div>
            <span className="font-medium">Giai đoạn:</span> {prediction.develop_stage}
          </div>
        )}
        
        {prediction.crop_health && (
          <div>
            <span className="font-medium">Tình trạng cây:</span> {prediction.crop_health}
          </div>
        )}
        
        {prediction.symptom && (
          <div>
            <span className="font-medium">Triệu chứng:</span> {prediction.symptom}
          </div>
        )}
        
        {prediction.risk && (
          <div>
            <span className="font-medium">Rủi ro:</span> {prediction.risk}
          </div>
        )}
        
        {prediction.estimated_yield && (
          <div>
            <span className="font-medium">Năng suất dự kiến:</span> {prediction.estimated_yield}
          </div>
        )}
        
        {prediction.care_recommendation && (
          <div className="col-span-2">
            <span className="font-medium">Khuyến nghị chăm sóc:</span> {prediction.care_recommendation}
          </div>
        )}
        
        {prediction.recommendations && prediction.recommendations.length > 0 && (
          <div className="col-span-2">
            <span className="font-medium">Khuyến nghị:</span>
            <ul className="list-disc pl-5 mt-1">
              {prediction.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
        
        {prediction.health_issues && prediction.health_issues.length > 0 && (
          <div className="col-span-2">
            <span className="font-medium">Vấn đề sức khỏe:</span>
            <ul className="list-disc pl-5 mt-1">
              {prediction.health_issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}
        
        {prediction.device_id && (
          <div>
            <span className="font-medium">Thiết bị:</span> {prediction.device_id}
          </div>
        )}
      </div>
      
      {prediction.sensor_data && (
        <div className="mt-3">
          <h5 className="font-medium text-blue-800 mb-1">Dữ liệu cảm biến:</h5>
          <div className="grid grid-cols-3 gap-2 text-xs">
            {Object.entries(prediction.sensor_data).map(([key, value]) => (
              <div key={key} className="bg-white p-1 rounded">
                <span className="font-medium">{key}:</span> {value}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

  // Hàm hiển thị chi tiết cảnh báo
  const renderAlertDetails = (alert: Alert) => {
    return (
      <div className="mt-2 bg-red-50 p-3 rounded-lg">
        <h4 className="font-medium text-red-800 mb-2">Chi tiết cảnh báo:</h4>
        <div className="grid grid-cols-1 gap-2 text-sm">
          <div>
            <span className="font-medium">Vấn đề:</span> {alert.issue}
          </div>
          <div>
            <span className="font-medium">Mức độ nghiêm trọng:</span> {alert.severity}
          </div>
          <div>
            <span className="font-medium">Thiết bị:</span> {alert.device}
          </div>
          <div>
            <span className="font-medium">Khuyến nghị:</span> {alert.recommendation}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 lg:hidden"
              >
                <Menu className="h-6 w-6" />
              </button>
              <h1 className="text-xl font-semibold text-gray-900 ml-2">Thông báo</h1>
            </div>
            
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-500">
                {isConnected ? 'Đã kết nối' : 'Mất kết nối'}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main content */}
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {/* Thông báo tạm thời */}
        {newNotification && (
          <div className="fixed top-20 right-4 w-80 bg-white shadow-lg rounded-lg overflow-hidden transition-all duration-300 z-50 border-l-4 border-blue-500">
            <div className="p-4">
              <div className="flex items-center justify-between">
                <h3 className="text-base font-medium text-gray-900">{newNotification.title}</h3>
                <button 
                  onClick={() => setNewNotification(null)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  &times;
                </button>
              </div>
              <p className="mt-1 text-sm text-gray-600">{newNotification.message}</p>
              
              {newNotification.prediction && renderPredictionDetails(newNotification.prediction)}
              {newNotification.alert && renderAlertDetails(newNotification.alert)}
              
              <div className="mt-3 flex justify-between">
                <button 
                  onClick={() => {
                    handleMarkAsRead(newNotification.id);
                    setNewNotification(null);
                  }}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Đánh dấu đã đọc
                </button>
                <span className="text-xs text-gray-500">Vừa xong</span>
              </div>
            </div>
          </div>
        )}
      
        {/* Search and Controls */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="p-4">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div className="relative flex-1">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Tìm kiếm thông báo..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={handleMarkAllAsRead}
                  className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <Check className="h-4 w-4 mr-1" />
                  Đọc tất cả
                </button>
                
                <button
                  onClick={handlePredict}
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <Calendar className="h-4 w-4 mr-1" />
                  Dự đoán
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Widget AI Prediction */}
        {latestPrediction && (
          <div className="bg-white shadow rounded-lg mb-6 overflow-hidden">
            <div 
              className="bg-indigo-600 px-4 py-3 flex justify-between items-center cursor-pointer"
              onClick={() => setIsAIPredictionExpanded(!isAIPredictionExpanded)}
            >
              <h3 className="text-white font-medium flex items-center">
                <Calendar className="h-5 w-5 mr-2" />
                Phân tích cây trồng mới nhất
              </h3>
              <button className="text-white">
                {isAIPredictionExpanded ? '−' : '+'}
              </button>
            </div>
            
            {isAIPredictionExpanded && (
              <div className="p-4">
                <div className="flex flex-col sm:flex-row justify-between mb-4">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">
                      {latestPrediction.crop_type ? 
                        `${latestPrediction.crop_type.charAt(0).toUpperCase() + latestPrediction.crop_type.slice(1)}` : 
                        'Cây trồng'}
                    </h4>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {latestPrediction.develop_stage && (
                        <p className="text-sm bg-gray-100 rounded-full px-2 py-1">
                          Giai đoạn: {latestPrediction.develop_stage}
                        </p>
                      )}
                      {latestPrediction.crop_health && (
                        <p className="text-sm bg-green-100 rounded-full px-2 py-1">
                          Tình trạng: {latestPrediction.crop_health}
                        </p>
                      )}
                      {latestPrediction.symptom && (
                        <p className="text-sm bg-amber-100 rounded-full px-2 py-1">
                          Triệu chứng: {latestPrediction.symptom}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  {latestPrediction.care_recommendation && (
                    <div className="bg-green-50 p-3 rounded-lg">
                      <div className="text-green-800 text-xs uppercase font-medium mb-1">Khuyến nghị</div>
                      <div className="text-lg font-semibold">
                        {latestPrediction.care_recommendation}
                      </div>
                    </div>
                  )}
                  
                  {latestPrediction.risk && (
                    <div className="bg-red-50 p-3 rounded-lg">
                      <div className="text-red-800 text-xs uppercase font-medium mb-1">Rủi ro</div>
                      <div className="text-lg font-semibold">{latestPrediction.risk}</div>
                    </div>
                  )}
                </div>
                
                {latestPrediction.sensor_data && (
                  <div className="mt-4 border-t pt-3">
                    <h5 className="text-sm font-medium text-gray-700 mb-2">Dữ liệu cảm biến:</h5>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                      {Object.entries(latestPrediction.sensor_data).map(([key, value]) => (
                        <div key={key} className="bg-gray-50 p-2 rounded text-center">
                          <div className="text-xs text-gray-500 uppercase">{key}</div>
                          <div className="font-medium">{value}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
        
        {/* Notifications List */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Danh sách thông báo
            </h3>
            
            {Object.keys(filteredGroups).length === 0 ? (
              <div className="text-center py-10">
                <Bell className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Không có thông báo</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {searchQuery ? 'Không tìm thấy thông báo nào khớp với tìm kiếm của bạn.' : 'Bạn chưa có thông báo nào.'}
                </p>
              </div>
            ) : (
              <>
                {(() => {
                   // Xử lý phân trang dữ liệu
  const sortedGroupEntries = Object.entries(filteredGroups)
  .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime());

// Làm phẳng danh sách thông báo đã được nhóm và sắp xếp
const allNotifications = sortedGroupEntries.flatMap(([date, notifs]) => 
  notifs.map(notif => ({ ...notif, date }))
);

// Tính vị trí bắt đầu và kết thúc dựa trên trang hiện tại
const startIndex = (currentPage - 1) * itemsPerPage;
const endIndex = Math.min(startIndex + itemsPerPage, allNotifications.length);

// Lấy thông báo cho trang hiện tại
const paginatedNotifications = allNotifications.slice(startIndex, endIndex);

// Nhóm lại thông báo theo ngày cho trang hiện tại
const paginatedGroups: Record<string, Notification[]> = paginatedNotifications.reduce((groups: Record<string, Notification[]>, notif) => {
  const date = notif.date;
  if (!groups[date]) {
    groups[date] = [];
  }
  groups[date].push(notif);
  return groups;
}, {});
                  return Object.entries(paginatedGroups)
                    .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime())
                    .map(([date, notifs]) => (
                      <div key={date} className="mb-6">
                        <h4 className="text-sm font-medium text-gray-500 mb-3">
                          {formatVietnameseDate(date)}
                        </h4>
                        
                        <div className="space-y-3">
                          {notifs.map((notification) => (
                            <div 
                              key={notification.id}
                              className={`p-4 rounded-lg border ${notification.isRead ? 'bg-white border-gray-200' : 'bg-blue-50 border-blue-200'}`}
                            >
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center">
                                    {notification.type === 'alert' && (
                                      <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                                    )}
                                    {notification.type === 'prediction' && (
                                      <Calendar className="h-5 w-5 text-blue-500 mr-2" />
                                    )}
                                    {(!notification.type || notification.type === 'standard') && (
                                      <Bell className="h-5 w-5 text-gray-500 mr-2" />
                                    )}
                                    <h4 className="text-base font-medium text-gray-900">
                                      {notification.title}
                                    </h4>
                                    {!notification.isRead && (
                                      <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                        Mới
                                      </span>
                                    )}
                                  </div>
                                  <p className="mt-1 text-sm text-gray-600">{notification.message}</p>
                                  
                                  {notification.prediction && renderPredictionDetails(notification.prediction)}
                                  {notification.alert && renderAlertDetails(notification.alert)}
                                </div>
                                
                                <div className="flex items-center ml-4">
                                  {!notification.isRead && (
                                    <button
                                      onClick={() => handleMarkAsRead(notification.id)}
                                      className="p-1 text-blue-600 hover:text-blue-800 mr-2"
                                      title="Đánh dấu đã đọc"
                                    >
                                      <Check className="h-5 w-5" />
                                    </button>
                                  )}
                                  <button
                                    onClick={() => handleDeleteNotification(notification.id)}
                                    className="p-1 text-red-600 hover:text-red-800"
                                    title="Xóa thông báo"
                                  >
                                    <Trash2 className="h-5 w-5" />
                                  </button>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ));
                })()}
              </>
            )}
          </div>
        </div>
        
        {/* Pagination */}
        {Object.keys(filteredGroups).length > 0 && (
          <div className="mt-4 flex justify-between items-center">
            <div className="flex items-center text-sm text-gray-500">
              <span className="mr-2">Hiển thị:</span>
              <select 
                value={itemsPerPage}
                onChange={handleItemsPerPageChange}
                className="form-select rounded border-gray-300 text-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
              </select>
              <span className="ml-2">thông báo mỗi trang</span>
            </div>
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button 
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${currentPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-500 hover:bg-gray-50'}`}
              >
                <span className="sr-only">Previous</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              
              {Array.from({ length: Math.ceil(Object.values(filteredGroups).flat().length / itemsPerPage) }, (_, i) => (
                <button 
                  key={i + 1}
                  onClick={() => setCurrentPage(i + 1)}
                  className={`relative inline-flex items-center px-4 py-2 border ${currentPage === i + 1 ? 'bg-blue-50 border-blue-500 text-blue-600 z-10' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'}`}
                >
                  {i + 1}
                </button>
              ))}
              
              <button 
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, Math.ceil(Object.values(filteredGroups).flat().length / itemsPerPage)))}
                disabled={currentPage === Math.ceil(Object.values(filteredGroups).flat().length / itemsPerPage)}
                className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${currentPage === Math.ceil(Object.values(filteredGroups).flat().length / itemsPerPage) ? 'text-gray-300 cursor-not-allowed' : 'text-gray-500 hover:bg-gray-50'}`}
              >
                <span className="sr-only">Next</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        )}
        
        {/* Test Controls - Chỉ hiển thị trong môi trường phát triển */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mt-6 p-4 bg-gray-100 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Test Controls</h3>
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  // Gửi một thông báo test
                  const testNotification: Notification = {
                    id: Date.now(),
                    title: 'Thông báo test',
                    message: 'Đây là một thông báo test được tạo thủ công.',
                    date: new Date().toISOString().split('T')[0],
                    isRead: false,
                    type: 'standard'
                  };
                  setNotifications(prev => [testNotification, ...prev]);
                  // Cập nhật số lượng thông báo chưa đọc
                  updateUnreadCount(notifications.filter(n => !n.isRead).length + 1);
                }}
                className="px-3 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Thêm thông báo test
              </button>
              
              <button
                onClick={() => {
                  // Test phân tích cây trồng với thông tin mới (đã loại bỏ ngày thu hoạch)
                  const testPrediction: Prediction = {
                    confidence: 85,
                    crop_health: 'Trung bình',
                    crop_type: 'cà chua',
                    care_recommendation: 'Tăng cường Nito và phân bón lân',
                    develop_stage: 'Phát triển',
                    risk: 'Dễ bị bệnh',
                    symptom: 'Lá héo nhẹ',
                    // Dữ liệu cảm biến mẫu
                    device_id: 'device_123',
                    sensor_data: {
                      temperature: 29.5,
                      humidity: 75.2,
                      soil_moisture: 42.3,
                      light_intensity: 8500,
                      pH: 6.4
                    }
                  };
                  
                  // Cập nhật dự đoán mới nhất
                  setLatestPrediction(testPrediction);
                  
                  // Thêm thông báo mới
                  const testNotification: Notification = {
                    id: Date.now(),
                    title: 'Phân tích cây trồng mới',
                    message: `Phân tích: Cây ${testPrediction.crop_type} (${testPrediction.develop_stage}) của bạn có tình trạng: ${testPrediction.crop_health}, triệu chứng: ${testPrediction.symptom}. Khuyến nghị: ${testPrediction.care_recommendation}.`,
                    date: new Date().toISOString().split('T')[0],
                    isRead: false,
                    prediction: testPrediction,
                    type: 'prediction'
                  };
                  
                  setNotifications(prev => [testNotification, ...prev]);
                  setNewNotification(testNotification);
                  // Cập nhật số lượng thông báo chưa đọc
                  updateUnreadCount(notifications.filter(n => !n.isRead).length + 1);
                }}
                className="px-3 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600"
              >
                Test phân tích
              </button>
              
              <button
                onClick={() => {
                  // Test cảnh báo
                  const testAlert: Alert = {
                    issue: 'Nhiệt độ cao bất thường',
                    severity: 'Cao',
                    recommendation: 'Kiểm tra hệ thống tưới và bón phân.',
                    device: 'Cảm biến nhiệt độ #12'
                  };
                  
                  // Thêm thông báo cảnh báo
                  const testNotification: Notification = {
                    id: Date.now(),
                    title: 'Cảnh báo nhiệt độ cao',
                    message: 'Phát hiện nhiệt độ cao bất thường tại khu vực trồng.',
                    date: new Date().toISOString().split('T')[0],
                    isRead: false,
                    alert: testAlert,
                    type: 'alert'
                  };
                  
                  setNotifications(prev => [testNotification, ...prev]);
                  setNewNotification(testNotification);
                  // Cập nhật số lượng thông báo chưa đọc
                  updateUnreadCount(notifications.filter(n => !n.isRead).length + 1);
                }}
                className="px-3 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600"
              >
                Test cảnh báo
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationPage;