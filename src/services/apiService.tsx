// src/services/apiService.ts

// API base URL - Thay đổi tùy theo môi trường
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

/**
 * Hàm tạo một QR session mới
 * @param deviceInfo Thông tin thiết bị
 * @returns Dữ liệu session QR
 */
export const createQRSession = async (deviceInfo: any) => {
  try {
    console.log('Creating QR session with device info:', deviceInfo);
    
    const response = await fetch(`${API_BASE_URL}/api/qr-auth/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        app_id: 'web-app',
        device_info: deviceInfo,
        ttl: 300 // 5 phút
      })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`Server returned ${response.status}: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('QR session created:', data);
    return data;
  } catch (error) {
    console.error('Error creating QR session:', error);
    throw error;
  }
};

/**
 * Hàm lấy thông tin phiên QR
 * @param sessionId ID phiên
 * @returns Thông tin phiên
 */
export const getQRSession = async (sessionId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/qr-auth/session/${sessionId}`);
    
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting QR session:', error);
    throw error;
  }
};

/**
 * Hàm kiểm tra trạng thái kết nối tới server
 * @returns { connected: boolean, message?: string }
 */
export const checkServerConnection = async (): Promise<{ connected: boolean, message?: string, error?: string }> => {
  try {
    const response = await fetch(`${API_BASE_URL}/ping`);
    
    if (!response.ok) {
      return { connected: false, error: `Server returned ${response.status}` };
    }
    
    const data = await response.json();
    return { connected: true, message: data.message };
  } catch (error) {
    console.error('Error checking server connection:', error);
    return { connected: false, error: error.message };
  }
};

/**
 * Tạo kết nối WebSocket tới server
 * @param sessionId ID phiên QR
 * @param messageHandler Hàm xử lý tin nhắn
 * @param onOpen Callback khi kết nối được thiết lập
 * @param onError Callback khi có lỗi
 * @param onClose Callback khi kết nối bị đóng
 * @returns WebSocket object
 */
export const createWebSocketConnection = (
  sessionId: string,
  messageHandler: (data: any) => void,
  onOpen?: () => void,
  onError?: (error: Event) => void,
  onClose?: (event: CloseEvent) => void
): WebSocket => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const wsUrl = `${protocol}//${host}/${sessionId}`;
  
  console.log(`Creating WebSocket connection to ${wsUrl}`);
  
  const socket = new WebSocket(wsUrl);
  
  socket.onopen = () => {
    console.log('WebSocket connection established');
    if (onOpen) onOpen();
    
    // Gửi thông tin thiết bị
    const initMessage = {
      device_type: "desktop",
      device_info: {
        name: "Web Browser",
        userAgent: navigator.userAgent
      }
    };
    
    socket.send(JSON.stringify(initMessage));
  };
  
  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      messageHandler(data);
    } catch (error) {
      console.error('Error processing WebSocket message:', error);
    }
  };
  
  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
    if (onError) onError(error);
  };
  
  socket.onclose = (event) => {
    console.log(`WebSocket connection closed with code ${event.code}`);
    if (onClose) onClose(event);
  };
  
  return socket;
};