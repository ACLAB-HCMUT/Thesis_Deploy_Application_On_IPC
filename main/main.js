// const { app, BrowserWindow } = require('electron');
// const path = require('path');
// const { getLocalIP } = require('./utils/network');

// function createWindow() {
//   const win = new BrowserWindow({
//     width: 800,
//     height: 600,
//     icon: path.join(__dirname, '../app_icon.ico'),
//     webPreferences: {
//       contextIsolation: true,
//       enableRemoteModule: false,
//     },
//     autoHideMenuBar: true,
//   });

//   const localIP = getLocalIP();
//   win.loadURL(`http://${localIP}:3000`);
// }

// app.whenReady().then(createWindow);

// app.on('window-all-closed', () => {
//   if (process.platform !== 'darwin') {
//     app.quit();
//   }
// });

// app.on('activate', () => {
//   if (BrowserWindow.getAllWindows().length === 0) {
//     createWindow();
//   }
// });
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { session } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        icon: path.join(__dirname, '../app_icon.ico'),
        webPreferences: {
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js') // Recommended for contextIsolation
        },
        autoHideMenuBar: true,
    });

    // For development, use localhost
    win.loadURL('http://localhost:3000');

    // Optional: Open DevTools in development
    // win.webContents.openDevTools();
}




app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});



app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});


function showNotification(title, body) {
    if (!Notification.isSupported()) {
      return;
    }
  
    const notification = new Notification({
      title,
      body,
      icon: '../src/assets/image/logo.png', // Add your app icon path
    });
  
    notification.show();
  
    // Send to renderer process to update Redux store
    mainWindow.webContents.send('new-notification', {
      id: Date.now(),
      title,
      message: body,
      date: new Date().toISOString().split('T')[0],
      isRead: false,
    });
  }
  
  // Listen for new notifications from renderer process
  ipcMain.on('send-notification', (event, { title, body }) => {
    showNotification(title, body);
  });