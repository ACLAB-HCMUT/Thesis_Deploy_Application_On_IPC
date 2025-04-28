const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  generateQRSession: () => ipcRenderer.invoke('generate-qr-session'),
  getQRImageUrl: (sessionId, serverIp) => ipcRenderer.invoke('get-qr-url', sessionId),
  onAuthRequest: (callback) => ipcRenderer.on('auth-request', (_, data) => callback(data)),
  onQRSessionExpired: (callback) => ipcRenderer.on('qr-session-expired', (_, data) => callback(data)),
  onDeviceDisconnected: (callback) => ipcRenderer.on('device-disconnected', (_, data) => callback(data)),
  sendAuthResponse: (sessionId, approved, user) => ipcRenderer.send('auth-response', { sessionId, approved, user }),
  
  // API mới để lấy IPv4 từ script Python
  getLocalIpAddress: () => ipcRenderer.invoke('get-ipv4'),
  
  // API để tạo QR URL với IPv4 và port
  generateIPv4QR: (params) => ipcRenderer.invoke('generate-ipv4-qr', params),
  
  // API để kiểm tra kết nối server
  checkServerConnection: () => ipcRenderer.invoke('check-server-connection'),
  
  // API cho thông báo
  sendNotification: (notification) => ipcRenderer.send('send-notification', notification),
  onNewNotification: (callback) => ipcRenderer.on('new-notification', (_, notification) => callback(notification))
});