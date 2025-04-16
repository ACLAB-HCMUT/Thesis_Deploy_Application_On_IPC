const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  sendNotification: (title, body) => {
    ipcRenderer.send('send-notification', { title, body });
  },
  onNewNotification: (callback) => {
    ipcRenderer.on('new-notification', (event, notification) => callback(notification));
  },
});