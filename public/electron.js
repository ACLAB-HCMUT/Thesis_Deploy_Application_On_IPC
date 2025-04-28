const { app, BrowserWindow, ipcMain, Notification } = require('electron');
const path = require('path');
const { session } = require('electron');
const { spawn } = require('child_process');
const fs = require('fs');
const { exec } = require('child_process');
const os = require('os');
const qrcode = require('qrcode');

// Global variables
let mainWindow;
let cachedIP = null;

// Đường dẫn đến script Python để lấy IP
const pythonScriptPath = path.join(app.getAppPath(), 'get_ip.py');

// Hàm chạy script Python để lấy IPv4 trực tiếp
function runPythonScriptDirect() {
  return new Promise((resolve, reject) => {
    console.log('===== Lấy IP trực tiếp từ script Python =====');
    console.log(`Script path: ${pythonScriptPath}`);
    
    // Thực thi script Python và lấy output trực tiếp
    exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error.message}`);
        reject(error);
        return;
      }
      
      if (stderr) {
        console.warn(`Python script stderr: ${stderr}`);
      }
      
      // Lấy IP trực tiếp từ stdout
      const ip = stdout.trim();
      console.log(`IP lấy trực tiếp từ Python: ${ip}`);
      
      if (!ip || ip === '') {
        console.error('IP không hợp lệ từ Python script');
        reject(new Error('Invalid IP from Python script'));
        return;
      }
      
      resolve(ip);
    });
  });
}

// Hàm lấy IP từ OS (dùng làm fallback)
function getLocalIPFromOS() {
  try {
    console.log('Getting IP from OS network interfaces...');
    const interfaces = os.networkInterfaces();
    for (const interfaceName in interfaces) {
      const iface = interfaces[interfaceName];
      for (const alias of iface) {
        if (alias.family === 'IPv4' && !alias.internal) {
          console.log(`Found IP from OS: ${alias.address}`);
          return alias.address;
        }
      }
    }
    console.log('No suitable IP found, returning localhost');
    return '127.0.0.1';
  } catch (error) {
    console.error(`Error getting IP from OS: ${error.message}`);
    return '127.0.0.1';
  }
}

// Hàm kết hợp lấy IP từ Python hoặc OS
async function getIPv4() {
  if (cachedIP) {
    console.log(`Using cached IP: ${cachedIP}`);
    return cachedIP;
  }
  
  try {
    // Lấy IP trực tiếp từ script Python
    const ip = await runPythonScriptDirect();
    cachedIP = ip;
    console.log(`IP đã được set: ${ip}`);
    return ip;
  } catch (error) {
    console.error('Failed to get IP from Python script:', error);
    // Fallback to OS method
    const ip = getLocalIPFromOS();
    cachedIP = ip;
    return ip;
  }
}

function getLocalIP() {
  return new Promise((resolve, reject) => {
    // Đường dẫn đến file Python (điều chỉnh theo cấu trúc dự án của bạn)
    const pythonPath = path.join(__dirname, 'src', 'get_ip.py');
    
    // Chạy script Python
    const pythonProcess = spawn('python', [pythonPath]);
    
    let output = '';
    
    // Lấy output từ script Python
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    // Xử lý lỗi
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python error: ${data}`);
      reject(`Python error: ${data}`);
    });
    
    // Khi process kết thúc
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python process exited with code ${code}`);
      } else {
        // Trả về IP (loại bỏ khoảng trắng và ký tự xuống dòng)
        resolve(output.trim());
      }
    });
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, '../app_icon.ico'),
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
      preload: path.join(app.getAppPath(), 'src', 'preload.tsx')
    },
    autoHideMenuBar: true,
  });

  // For development, use localhost
  win.loadURL('http://localhost:3000');
  
  // Lưu trữ window reference
  mainWindow = win;
  
  // Optional: Open DevTools in development
  win.webContents.openDevTools();
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

// IPC Handlers
ipcMain.handle('get-ipv4', async () => {
  const ip = await getIPv4();
  console.log(`IPC: Returning IP: ${ip}`);
  return ip;
});

// Handler để tạo QR code với IP và port
ipcMain.handle('generate-ipv4-qr', async (event, { path: urlPath = '/login', port = '3000' }) => {
  try {
    const ip = await getIPv4();
    const url = `http://${ip}:${port}${urlPath}`;
    console.log(`Generating QR code for URL: ${url}`);
    
    // Tạo QR code image
    const qrImage = await qrcode.toDataURL(url);
    
    return {
      url,
      ipv4: ip,
      qrImage
    };
  } catch (error) {
    console.error('Error generating QR code:', error);
    throw error;
  }
});

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