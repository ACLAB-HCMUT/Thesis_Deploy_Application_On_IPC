  import React, { useState, useEffect, useRef } from 'react';
  import { Calendar, Search, Trash2, Bell, Check, Menu, AlertCircle } from 'lucide-react';

  // Thêm interface Alert vào đầu file, dưới interface Prediction
interface Alert {
  issue: string;
  severity: string;
  recommendation: string;
  device: string;
}

  interface Prediction {
    harvest_date: string;
    confidence: number;
    days_remaining: number;
    crop_health: string;
    estimated_yield: string;
    crop_type: string;
  }

  interface Notification {
    id: number;
    title: string;
    message: string;
    date: string;
    isRead: boolean;
    prediction?: Prediction;
    alert?: Alert;  // Thêm trường này
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
      },
      {
        id: 3,
        title: "Canh bao nhiet do",
        message: "Nhiet do cao bat thuong",
        date: "2024-11-10",
        isRead: false,
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
              }
              
              // Hiển thị thông báo tạm thời
              const newNotification: Notification = {
                id: Date.now(),
                title: 'Dự đoán thu hoạch AI',
                message: message.message,
                date: new Date().toISOString().split('T')[0],
                isRead: false,
                prediction: message.prediction,
                type: 'prediction'
              };
              
              setNewNotification(newNotification);
              
              if (notificationTimeoutRef.current) {
                clearTimeout(notificationTimeoutRef.current);
              }
              
              notificationTimeoutRef.current = setTimeout(() => {
                setNewNotification(null);
              }, 5000);
              
              // Thêm vào danh sách thông báo
              setNotifications(prev => [newNotification, ...prev]);
            }
            // Thêm xử lý cho thông báo cảnh báo AI
            else if (message.type === 'ai_alert') {
              console.log('AI alert received:', message);
              
              // Tạo thông báo cảnh báo mới
              const newNotification: Notification = {
                id: Date.now(),
                title: 'Cảnh báo từ thiết bị',
                message: message.message,
                date: new Date().toISOString().split('T')[0],
                isRead: false,
                alert: message.alert,
                type: 'alert'
              };
              
              // Thêm vào danh sách thông báo
              setNotifications(prev => [newNotification, ...prev]);
              
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
              // Code xử lý thông báo thông thường (không cần thay đổi)
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

    // Hàm gửi yêu cầu dự đoán thủ công
    const handlePredict = async () => {
      console.log("Sending prediction request...");
      try {
        const response = await fetch('http://localhost:8000/api/notifications/predict_harvest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: 1,
            input_data: {
              crop_type: "tomato",
              planting_date: new Date().toISOString().split('T')[0]
            }
          }),
        });
        
        const data = await response.json();
        console.log('Prediction response:', data);
        
        if (!response.ok) {
          throw new Error(data.message || 'Prediction failed');
        }
        
        // Thêm thông báo trực tiếp từ response nếu không nhận được qua WebSocket
        if (data.success && data.notification) {
          const newNotification: Notification = {
            id: Date.now(),
            title: 'Dự đoán thu hoạch',
            message: data.notification.message,
            date: new Date().toISOString().split('T')[0],
            isRead: false,
            prediction: data.prediction
          };
          setNotifications(prev => [newNotification, ...prev]);
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
        const filtered = (notifs as Notification[]).filter(n => 
          n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          n.message.toLowerCase().includes(searchQuery.toLowerCase())
        );
        if (filtered.length > 0) {
          acc[date] = filtered;
        }
        return acc;
      }, {}
    );
    
    // Đếm số thông báo chưa đọc
    const unreadCount = notifications.filter(n => !n.isRead).length;

    const toggleRead = (id: number) => {
      setNotifications(notifications.map(notification =>
        notification.id === id
          ? { ...notification, isRead: !notification.isRead }
          : notification
      ));
    };

    const deleteNotification = (id: number) => {
      setNotifications(notifications.filter(notification => notification.id !== id));
    };

    return (
      <main className="flex min-h-screen bg-gray-50">
        {/* Mobile menu button */}
        <button
          className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-md"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        >
          <Menu size={24} />
        </button>

        {/* Main content */}
        <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold mb-6">Notifications</h1>
            <div className="flex items-center">
              {isConnected ? (
                <span className="flex items-center text-green-500 text-sm">
                  <span className="relative flex h-3 w-3 mr-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                  </span>
                  Kết nối máy chủ thành công
                </span>
              ) : (
                <span className="flex items-center text-red-500 text-sm">
                  <span className="relative flex h-3 w-3 mr-2">
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                  </span>
                  Mất kết nối máy chủ
                </span>
              )}
              
              {unreadCount > 0 && (
                <span className="ml-4 bg-green-500 text-white px-2 py-1 rounded-full text-xs">
                  {unreadCount} mới
                </span>
              )}
            </div>
          </div>
          
          {/* Pop-up thông báo mới */}
          {newNotification && (
            <div className="fixed top-5 right-5 max-w-md w-full bg-white rounded-lg shadow-lg p-4 border-l-4 border-green-500 transform transition-transform duration-300 z-50 animate-bounce">
              <div className="flex items-start">
                <div className="flex-shrink-0 text-green-500">
                  <AlertCircle size={24} />
                </div>
                <div className="ml-3 w-0 flex-1">
                  <p className="font-medium text-gray-900">{newNotification.title}</p>
                  <p className="mt-1 text-sm text-gray-500">{newNotification.message}</p>
                </div>
                <button 
                  className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-500"
                  onClick={() => setNewNotification(null)}
                >
                  <span className="sr-only">Đóng</span>
                  <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          )}
          
          
          
          <div className="max-w-4xl mx-auto">
            <div className="mb-6">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search notifications..."
                  className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
              </div>
            </div>

            {Object.entries(filteredGroups).map(([date, notifications]) => (
              <div key={date} className="mb-6">
                <h2 className="text-lg font-semibold mb-3">
                  {formatVietnameseDate(date)}
                </h2>
                
                <div className="space-y-3">
                  {notifications.map(notification => (
                    <div 
                      key={notification.id}
                      className={`rounded-lg border shadow-sm transition-colors duration-200 ${
                        notification.isRead ? 'bg-gray-50' : 'bg-white border-l-4 border-green-500'
                      }`}
                    >
                      <div className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3">
                            <div className={`mt-1 ${notification.isRead ? 'text-gray-400' : 'text-green-500'}`}>
                              <Bell size={20} />
                            </div>
                            <div>
                              <h3 className="font-medium">{notification.title}</h3>
                              <p className="text-gray-600 text-sm mt-1">{notification.message}</p>
                              
                              {/* Hiển thị chi tiết dự đoán nếu có */}
                              {notification.prediction && (
                                <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
                                  <div className="grid grid-cols-2 gap-2">
                                    <div>
                                      <span className="font-medium">Ngày thu hoạch:</span> {notification.prediction.harvest_date}
                                    </div>
                                    <div>
                                      <span className="font-medium">Còn lại:</span> {notification.prediction.days_remaining} ngày
                                    </div>
                                    <div>
                                      <span className="font-medium">Sức khỏe cây:</span> {notification.prediction.crop_health}
                                    </div>
                                    <div>
                                      <span className="font-medium">Loại cây:</span> {notification.prediction.crop_type}
                                    </div>
                                  </div>
                                </div>
                              )}
                              {/* Thêm phần hiển thị thông tin cảnh báo */}
{notification.alert && (
  <div className="mt-2 p-2 bg-red-50 rounded text-sm border-l-2 border-red-500">
    <div className="grid grid-cols-2 gap-2">
      <div>
        <span className="font-medium">Thiết bị:</span> {notification.alert.device || 'Không xác định'}
      </div>
      <div>
        <span className="font-medium">Mức độ:</span> <span className={
          notification.alert.severity === 'Cao' || notification.alert.severity === 'Nghiêm trọng' 
            ? 'text-red-600 font-medium' 
            : 'text-orange-500'
        }>{notification.alert.severity}</span>
      </div>
      <div>
        <span className="font-medium">Vấn đề:</span> {notification.alert.issue}
      </div>
      <div>
        <span className="font-medium">Đề xuất:</span> {notification.alert.recommendation}
      </div>
    </div>
  </div>
)}
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => toggleRead(notification.id)}
                              className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-150"
                            >
                              <Check 
                                size={18} 
                                className={notification.isRead ? 'text-green-500' : 'text-gray-400'} 
                              />
                            </button>
                            <button
                              onClick={() => deleteNotification(notification.id)}
                              className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-150 text-red-500"
                            >
                              <Trash2 size={18} />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}

            {Object.keys(filteredGroups).length === 0 && (
              <div className="text-center py-10 text-gray-500">
                No notifications found
              </div>
            )}
          </div>
        </div>
      </main>
    );
  };

  export default NotificationPage;