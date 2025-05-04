const { app, BrowserWindow, ipcMain, Notification } = require('electron');
const path = require('path');
const { session } = require('electron');
const { spawn } = require('child_process');
const fs = require('fs');
const { exec } = require('child_process');
const os = require('os');
// const qrcode = require('qrcode');

// Global variables
let mainWindow;

// Thêm các log để debug trong hàm createWindow của electron.js
function createWindow() {
  console.log('Creating window...');
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, '../app_icon.ico'),
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js') // Đảm bảo đường dẫn đúng
    },
    autoHideMenuBar: true,
  });

  // For development, use localhost
  win.loadURL('http://localhost:3000');
  
  // Lưu trữ window reference
  mainWindow = win;
  
  // Mở DevTools để debug
  win.webContents.openDevTools();

  // Không cần đọc file IP.txt nữa vì React sẽ import trực tiếp từ JSON
  // Tuy nhiên, vẫn nên chạy script Python để tạo file IP.json
  
  // Chạy script Python để cập nhật IP
  exec('python get_ip.py', (error, stdout, stderr) => {
    if (error) {
      console.error('Error executing Python script:', error);
      return;
    }
    
    if (stderr) {
      console.error('Python script stderr:', stderr);
    }
    
    const ip = stdout.trim();
    console.log('IP obtained from Python script:', ip);
    
    // Kiểm tra xem file JSON đã được tạo chưa
    const ipJsonPath = path.join(__dirname, '../src/pages/authentication/ip.json');
    console.log('Path to IP JSON file:', ipJsonPath);
    
    fs.access(ipJsonPath, fs.constants.F_OK, (err) => {
      if (err) {
        console.error('IP JSON file was not created by Python script:', err);
        
        // Tạo file JSON với IP từ output của script nếu file không tồn tại
        const jsonData = JSON.stringify({ ipAddress: ip || '127.0.0.1' });
        
        fs.writeFile(ipJsonPath, jsonData, (writeErr) => {
          if (writeErr) {
            console.error('Failed to create IP JSON file:', writeErr);
          } else {
            console.log('Created IP JSON file with IP:', ip);
          }
        });
      } else {
        console.log('IP JSON file exists (created by Python script)');
      }
    });
  });
}

function showNotification(title, body) {
  if (!Notification.isSupported() || !mainWindow) {
    return;
  }

  const notification = new Notification({
    title,
    body,
    icon: path.join(app.getAppPath(), 'src', 'assets', 'image', 'logo.png'),
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

// Xử lý các thông báo
ipcMain.on('send-notification', (event, { title, body }) => {
  showNotification(title, body);
});

// Khởi tạo ứng dụng
app.whenReady().then(async () => {
  console.log('===== Electron Application Starting =====');
  
  // Lấy IP khi ứng dụng khởi động
  try {
    const ip = await getIPv4();
    console.log(`===== Application started with IP: ${ip} =====`);
  } catch (error) {
    console.error('Failed to get IP at startup:', error);
  }
  
  createWindow();
});

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