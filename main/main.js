// const { app, BrowserWindow, ipcMain, Notification } = require('electron');
// const path = require('path');
// const { session } = require('electron');
// const express = require('express');
// const http = require('http');
// const WebSocket = require('ws');
// const qrcode = require('qrcode');
// const { v4: uuidv4 } = require('uuid');
// const crypto = require('crypto');
// const axios = require('axios');
// const os = require('os');
// const { exec } = require('child_process');
// const fs = require('fs');

// // Cấu hình API server
// const API_SERVER = process.env.API_SERVER || 'http://localhost:8000';

// // Lưu trữ thông tin phiên
// const sessions = {};
// let mainWindow;

// // Đường dẫn đến script Python và file lưu IP
// const pythonScript = path.join(app.getAppPath(), '..', 'get_ip.py');
// const ipFilePath = path.join(app.getAppPath(), '..', 'public', 'ip.txt');

// // Hàm chạy script Python để lấy IP
// function runPythonIPScript() {
//   return new Promise((resolve, reject) => {
//     console.log(`Executing Python script to get IP: ${pythonScript}`);
    
//     // Chạy Python script
//     exec(`python "${pythonScript}"`, (error, stdout, stderr) => {
//       if (error) {
//         console.error(`Error executing Python script: ${error}`);
//         reject(error);
//         return;
//       }
      
//       if (stderr) {
//         console.error(`Python script stderr: ${stderr}`);
//       }
      
//       console.log(`Python script output: ${stdout}`);
      
//       // Kiểm tra xem file có tồn tại không
//       if (fs.existsSync(ipFilePath)) {
//         // Đọc IP từ file
//         fs.readFile(ipFilePath, 'utf8', (err, data) => {
//           if (err) {
//             console.error(`Error reading IP file: ${err}`);
//             reject(err);
//             return;
//           }
          
//           const ip = data.trim();
//           console.log(`Successfully retrieved IP from Python script: ${ip}`);
//           console.log(`IP file path: ${ipFilePath}`);
//           resolve(ip);
//         });
//       } else {
//         console.error(`IP file not found at: ${ipFilePath}`);
//         console.log(`Falling back to OS-based IP detection...`);
//         // Nếu file không tồn tại, dùng hàm getIPv4 làm fallback
//         const fallbackIP = getIPv4();
//         console.log(`Fallback IP from OS: ${fallbackIP}`);
//         resolve(fallbackIP);
//       }
//     });
//   });
// }

// // Hàm lấy địa chỉ IPv4 local
// function getIPv4() {
//   const networkInterfaces = os.networkInterfaces();
//   for (const interfaceName in networkInterfaces) {
//     const addresses = networkInterfaces[interfaceName];
//     for (const address of addresses) {
//       if (address.family === 'IPv4' && !address.internal) {
//         return address.address;
//       }
//     }
//   }
//   return '127.0.0.1';
// }

// // Khởi tạo IP khi chạy ứng dụng và cache lại
// let cachedIP = null;

// // Hàm kết hợp lấy IP từ file Python hoặc từ OS
// async function getIP() {
//   // Nếu đã có IP trong cache, trả về luôn
//   if (cachedIP) {
//     return cachedIP;
//   }
  
//   try {
//     // Thử lấy IP từ script Python
//     const ip = await runPythonIPScript();
//     cachedIP = ip;
//     return ip;
//   } catch (error) {
//     console.error('Error getting IP from Python script, falling back to getIPv4():', error);
//     // Fallback về hàm getIPv4 nếu có lỗi
//     const ip = getIPv4();
//     cachedIP = ip;
//     return ip;
//   }
// }

// console.log('Getting IPv4 Address...');
// // Khởi tạo IP khi bắt đầu ứng dụng
// getIP().then(ip => {
//   console.log('IPv4 Address:', ip);
// });

// function createWindow() {
//   const win = new BrowserWindow({
//     width: 800,
//     height: 600,
//     icon: path.join(__dirname, '../app_icon.ico'),
//     webPreferences: {
//       contextIsolation: true,
//       nodeIntegration: false,
//       enableRemoteModule: false,
//       preload: path.join(__dirname, 'preload.js')
//     },
//     autoHideMenuBar: true,
//   });

//   // For development, use localhost
//   // win.loadURL('http://localhost:3000');
//   win.loadURL(`file://${path.join(__dirname, 'ipv4-qr-test.html')}`);
//   mainWindow = win;
// }

// // Tạo WebSocket client kết nối đến FastAPI server
// let wsClient = null;

// function connectToFastAPIWebsocket() {
//   const wsUrl = `ws://localhost:8000/ws/relay`;
  
//   console.log(`Connecting to FastAPI WebSocket at ${wsUrl}`);
//   wsClient = new WebSocket(wsUrl);
  
//   wsClient.on('open', () => {
//     console.log('Connected to FastAPI WebSocket server');
//   });
  
//   wsClient.on('message', (data) => {
//     try {
//       const message = JSON.parse(data);
//       console.log('Received from FastAPI:', message);
      
//       // Xử lý tin nhắn từ server
//       if (message.type === 'auth-request') {
//         if (mainWindow) {
//           mainWindow.webContents.send('auth-request', {
//             sessionId: message.session_id,
//             deviceInfo: message.device_info
//           });
//         }
//       }
//     } catch (error) {
//       console.error('Error processing WebSocket message:', error);
//     }
//   });
  
//   wsClient.on('error', (error) => {
//     console.error('WebSocket error:', error);
//     // Thử kết nối lại sau 5 giây
//     setTimeout(connectToFastAPIWebsocket, 5000);
//   });
  
//   wsClient.on('close', () => {
//     console.log('WebSocket connection closed');
//     // Thử kết nối lại sau 5 giây
//     setTimeout(connectToFastAPIWebsocket, 5000);
//   });
// }

// // Khởi tạo phiên QR mới bằng cách gọi API của FastAPI
// async function createQRSession() {
//   try {
//     // Lấy địa chỉ IP local bằng hàm getIP
//     const localIP = await getIP();
    
//     // Tạo dữ liệu cho request
//     const sessionData = {
//       app_id: "electron-app",
//       device_info: {
//         type: "desktop",
//         name: "Electron App",
//         ip: localIP
//       },
//       ttl: 300 // 5 phút
//     };
    
//     // Gọi API của FastAPI để tạo session
//     const response = await axios.post(`${API_SERVER}/api/qr-auth/session`, sessionData);
    
//     // Lưu session vào local
//     const qrSession = response.data;
//     sessions[qrSession.session_id] = {
//       ...qrSession,
//       createdAt: Date.now()
//     };
    
//     // Thông báo kết nối với server qua WebSocket
//     if (wsClient && wsClient.readyState === WebSocket.OPEN) {
//       wsClient.send(JSON.stringify({
//         type: 'register-desktop',
//         session_id: qrSession.session_id,
//         device_info: sessionData.device_info
//       }));
//     }
    
//     return qrSession;
//   } catch (error) {
//     console.error('Error creating QR session:', error);
//     throw error;
//   }
// }

// function showNotification(title, body) {
//   if (!Notification.isSupported()) {
//     return;
//   }

//   const notification = new Notification({
//     title,
//     body,
//     icon: '../src/assets/image/logo.png',
//   });

//   notification.show();

//   // Send to renderer process to update Redux store
//   mainWindow.webContents.send('new-notification', {
//     id: Date.now(),
//     title,
//     message: body,
//     date: new Date().toISOString().split('T')[0],
//     isRead: false,
//   });
// }

// // IPC handlers cho QR authentication
// ipcMain.handle('generate-qr-session', async () => {
//   const session = await createQRSession();
//   return session;
// });

// ipcMain.handle('get-qr-url', async (event, sessionId) => {
//   if (!sessionId || !sessions[sessionId]) {
//     throw new Error('Invalid session');
//   }
  
//   // Trả về URL ảnh QR từ session data
//   return sessions[sessionId].qr_image;
// });

// // Thêm handler để lấy địa chỉ IPv4 từ script Python
// ipcMain.handle('get-ipv4', async () => {
//   return await getIP();
// });

// // Thêm handler để tạo URL QR có chứa địa chỉ IPv4 và port
// ipcMain.handle('generate-ipv4-qr', async (event, { path, port = '3000' }) => {
//   const ipv4 = await getIP();
//   const url = `http://${ipv4}:${port}${path || '/login'}`;
  
//   try {
//     // Tạo mã QR từ URL
//     const qrImageData = await qrcode.toDataURL(url);
//     return {
//       url,
//       ipv4,
//       qrImage: qrImageData
//     };
//   } catch (error) {
//     console.error('Error generating QR code:', error);
//     throw error;
//   }
// });

// ipcMain.on('auth-response', (event, { sessionId, approved, user }) => {
//   console.log(`Responding to auth request: ${approved ? 'APPROVED' : 'REJECTED'}`);
  
//   // Gửi phản hồi xác thực qua WebSocket tới FastAPI
//   if (wsClient && wsClient.readyState === WebSocket.OPEN) {
//     wsClient.send(JSON.stringify({
//       type: 'auth-response',
//       session_id: sessionId,
//       approved: approved,
//       user_data: user
//     }));
//   }
  
//   // Xóa phiên sau khi xử lý
//   setTimeout(() => {
//     delete sessions[sessionId];
//   }, 5000);
  
//   // Thông báo xác thực thành công
//   if (approved) {
//     showNotification(
//       'Xác thực thành công', 
//       `${user.name} đã đăng nhập từ thiết bị di động`
//     );
//   }
// });

// // Listen for new notifications from renderer process
// ipcMain.on('send-notification', (event, { title, body }) => {
//   showNotification(title, body);
// });

// // Thêm IPC handler để kiểm tra kết nối server
// ipcMain.handle('check-server-connection', async () => {
//   try {
//     await axios.get(`${API_SERVER}/api/health`);
//     return true;
//   } catch (error) {
//     console.error('Server connection check failed:', error);
//     return false;
//   }
// });

// app.whenReady().then(() => {
//   createWindow();
//   connectToFastAPIWebsocket();
  
//   // Chạy script Python để cập nhật IP khi khởi động ứng dụng
//   getIP().then(ip => {
//     console.log('Application started with IP:', ip);
//   }).catch(err => {
//     console.error('Failed to get IP at startup:', err);
//   });
// });

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