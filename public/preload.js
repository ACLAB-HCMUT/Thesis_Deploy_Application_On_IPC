const { contextBridge, ipcRenderer } = require('electron');

console.log('Preload script is running...');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
  'electron', {
    getIp: (callback) => {
      console.log('getIp method called from renderer');
      
      // Đăng ký lắng nghe sự kiện ip-ready
      ipcRenderer.on('ip-ready', (_event, ip) => {
        console.log('Received IP from main process:', ip);
        callback(ip);
      });
      
      // Thêm một phương thức trực tiếp để yêu cầu IP
      setTimeout(() => {
        console.log('Checking if IP was received...');
      }, 2000);
    }
  }
);

// Log khi preload script hoàn thành
console.log('Preload script completed');