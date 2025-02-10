const { contextBridge } = require('electron');
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
  getLocalIP: () => getLocalIP()
});
