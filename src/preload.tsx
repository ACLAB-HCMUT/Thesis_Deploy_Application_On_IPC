const { contextBridge, ipcRenderer } = require('electron');
const os = require('os');

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const interfaceName in interfaces) {
    const iface = interfaces[interfaceName];
    for (const alias of iface) {
      if (alias.family === 'IPv4' && !alias.internal) {
        return alias.address;
      }
    }
  }
  return 'localhost';
}

contextBridge.exposeInMainWorld('electronAPI', {
  // getLocalIP: () => getLocalIP(),
  getLocalIpAddress: () => ipcRenderer.invoke('get-ipv4'),
  
  // Tạo QR code với IP và port
  generateIPv4QR: (params) => ipcRenderer.invoke('generate-ipv4-qr', params),
  
  // Các API khác từ preload cũ
  getLocalIP: () => {
    return ipcRenderer.invoke('get-ipv4');
  },
  // APIs cho QR Authentication
  generateQRSession: () => ipcRenderer.invoke('generate-qr-session'),
  getQRImageUrl: (sessionId, serverIp) => ipcRenderer.invoke('get-qr-url', sessionId, serverIp),
  onAuthRequest: (callback) => ipcRenderer.on('auth-request', (_, data) => callback(data)),
  onQRSessionExpired: (callback) => ipcRenderer.on('qr-session-expired', (_, data) => callback(data)),
  onDeviceDisconnected: (callback) => ipcRenderer.on('device-disconnected', (_, data) => callback(data)),
  sendAuthResponse: (sessionId, approved, user) => ipcRenderer.send('auth-response', { sessionId, approved, user }),
  
  // APIs cho notification
  sendNotification: (notification) => ipcRenderer.send('send-notification', notification),
  onNewNotification: (callback) => ipcRenderer.on('new-notification', (_, notification) => callback(notification))
});

