// GlobalNotification.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Check, AlertCircle, Calendar, Bell } from 'lucide-react';

// Types to match your existing notification types
interface Prediction {
  harvest_date: string;
  confidence: number;
  days_remaining: number;
  crop_health: string;
  crop_type: string;
  care_recommendation?: string;
}

interface Alert {
  issue: string;
  severity: string;
  recommendation: string;
  device: string;
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

const GlobalNotification: React.FC = () => {
  const [newNotification, setNewNotification] = useState<Notification | null>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Render prediction details
  const renderPredictionDetails = (prediction: Prediction) => {
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

    return (
      <div className="mt-2 bg-blue-50 p-3 rounded-lg">
        <h4 className="font-medium text-blue-800 mb-2">Chi tiết dự đoán:</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="font-medium">Loại cây trồng:</span> {prediction.crop_type}
          </div>
          <div>
            <span className="font-medium">Ngày thu hoạch:</span> {formatVietnameseDate(prediction.harvest_date)}
          </div>
          <div>
            <span className="font-medium">Còn lại:</span> {prediction.days_remaining} ngày
          </div>
          <div>
            <span className="font-medium">Tình trạng cây:</span> {prediction.crop_health}
          </div>
          <div className="col-span-2">
            <span className="font-medium">Khuyến nghị chăm sóc:</span> {prediction.care_recommendation}
          </div>
        </div>
      </div>
    );
  };

  // Render alert details
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

  // Get icon based on notification type
  const getNotificationIcon = (type?: string) => {
    switch (type) {
      case 'alert':
        return <AlertCircle className="h-5 w-5 text-red-500 mr-2" />;
      case 'prediction':
        return <Calendar className="h-5 w-5 text-blue-500 mr-2" />;
      default:
        return <Bell className="h-5 w-5 text-gray-500 mr-2" />;
    }
  };

  // Xác định border color dựa trên loại thông báo
  const getBorderColor = (type?: string) => {
    switch (type) {
      case 'alert':
        return 'border-red-500';
      case 'prediction':
        return 'border-blue-500';
      default:
        return 'border-gray-500';
    }
  };

  // Handle notification events
  useEffect(() => {
    const handleNotificationEvent = (e: Event) => {
      const event = e as CustomEvent<Notification>;
      console.log("Global notification received:", event.detail);
      
      // Xóa timeout cũ nếu có
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      
      // Show the notification
      setNewNotification(event.detail);

      // Auto-hide after 5 seconds
      timeoutRef.current = setTimeout(() => {
        setNewNotification(null);
      }, 5000);
    };

    // Handle marking notification as read
    const handleMarkNotificationAsRead = (e: Event) => {
      const event = e as CustomEvent<{id: number}>;
      
      // Hide the current notification if it matches the ID
      if (newNotification && newNotification.id === event.detail.id) {
        setNewNotification(null);
      }
    };

    // Add event listeners
    window.addEventListener('showGlobalNotification', handleNotificationEvent as EventListener);
    window.addEventListener('markNotificationAsRead', handleMarkNotificationAsRead as EventListener);

    // Cleanup
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      window.removeEventListener('showGlobalNotification', handleNotificationEvent as EventListener);
      window.removeEventListener('markNotificationAsRead', handleMarkNotificationAsRead as EventListener);
    };
  }, [newNotification]);

  // If no notification, return null
  if (!newNotification) return null;

  return (
    <div className={`fixed top-4 right-4 w-80 bg-white shadow-lg rounded-lg overflow-hidden transition-all duration-300 z-50 border-l-4 ${getBorderColor(newNotification.type)}`}>
      <div className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {getNotificationIcon(newNotification.type)}
            <h3 className="text-base font-medium text-gray-900">{newNotification.title}</h3>
          </div>
          <button 
            onClick={() => setNewNotification(null)}
            className="text-gray-400 hover:text-gray-500"
            aria-label="Đóng thông báo"
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
              // Dispatch a mark as read event
              const event = new CustomEvent('markNotificationAsRead', { 
                detail: { id: newNotification.id } 
              });
              window.dispatchEvent(event);
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
  );
};

export default GlobalNotification;