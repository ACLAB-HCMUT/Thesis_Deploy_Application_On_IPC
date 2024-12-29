const { app, BrowserWindow } = require('electron');
const path = require('path');
const { getLocalIP } = require('./utils/network');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, '../app_icon.ico'),
    webPreferences: {
      contextIsolation: true,
      enableRemoteModule: false,
    },
    autoHideMenuBar: true,
  });

  const localIP = getLocalIP();
  win.loadURL(`http://${localIP}:3000`);
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
