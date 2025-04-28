// utils/NotificationUtils.ts

// Types
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
  
  /**
   * Hiển thị thông báo toàn cục
   * @param notification Thông báo cần hiển thị
   */
  export const showGlobalNotification = (notification: Notification) => {
    console.log("Broadcasting global notification:", notification);
    
    // Đảm bảo thông báo có id
    if (!notification.id) {
      notification.id = Date.now();
    }
    
    // Đảm bảo thông báo có date
    if (!notification.date) {
      notification.date = new Date().toISOString().split('T')[0];
    }
    
    // Tạo và dispatch custom event với notification
    const event = new CustomEvent('showGlobalNotification', {
      detail: notification
    });
    
    // Gửi event đến window để các component khác có thể lắng nghe
    window.dispatchEvent(event);
  };
  
  /**
   * Tạo và hiển thị thông báo tiêu chuẩn
   * @param title Tiêu đề thông báo
   * @param message Nội dung thông báo
   * @returns ID của thông báo
   */
  export const showStandardNotification = (title: string, message: string): number => {
    const notification: Notification = {
      id: Date.now(),
      title,
      message,
      date: new Date().toISOString().split('T')[0],
      isRead: false,
      type: 'standard'
    };
    
    showGlobalNotification(notification);
    return notification.id;
  };
  
  /**
   * Tạo và hiển thị thông báo dự đoán AI
   * @param title Tiêu đề thông báo
   * @param message Nội dung thông báo
   * @param prediction Dữ liệu dự đoán
   * @returns ID của thông báo
   */
  export const showPredictionNotification = (
    title: string, 
    message: string, 
    prediction: Prediction
  ): number => {
    const notification: Notification = {
      id: Date.now(),
      title,
      message,
      date: new Date().toISOString().split('T')[0],
      isRead: false,
      prediction,
      type: 'prediction'
    };
    
    showGlobalNotification(notification);
    return notification.id;
  };
  
  /**
   * Tạo và hiển thị thông báo cảnh báo
   * @param title Tiêu đề thông báo
   * @param message Nội dung thông báo
   * @param alert Dữ liệu cảnh báo
   * @returns ID của thông báo
   */
  export const showAlertNotification = (
    title: string, 
    message: string, 
    alert: Alert
  ): number => {
    const notification: Notification = {
      id: Date.now(),
      title,
      message,
      date: new Date().toISOString().split('T')[0],
      isRead: false,
      alert,
      type: 'alert'
    };
    
    showGlobalNotification(notification);
    return notification.id;
  };
  
  /**
   * Đánh dấu thông báo đã đọc
   * @param id ID của thông báo
   */
  export const markNotificationAsRead = (id: number): void => {
    const event = new CustomEvent('markNotificationAsRead', { 
      detail: { id }
    });
    window.dispatchEvent(event);
  };