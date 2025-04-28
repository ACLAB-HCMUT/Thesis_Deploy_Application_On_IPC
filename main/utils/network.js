// utils/network.js
const { networkInterfaces } = require('os');

/**
 * Lấy địa chỉ IPv4 local của máy tính
 * @returns {string} - Địa chỉ IP local hoặc '127.0.0.1' nếu không tìm thấy
 */

function getIPv4() {
  const networkInterfaces = os.networkInterfaces();
  for (const interfaceName in networkInterfaces) {
      const addresses = networkInterfaces[interfaceName];
      for (const address of addresses) {
          if (address.family === 'IPv4' && !address.internal) {
              return address.address;
          }
      }
  }
  return '127.0.0.1';
}

console.log('IPv4 Address:', getIPv4());

function getLocalIP() {
  const nets = networkInterfaces();
  const results = [];
  
  console.log('Bắt đầu lấy địa chỉ IP local');
  console.log('Giao diện mạng:', Object.keys(nets));

  // Lặp qua tất cả các giao diện mạng
  for (const name of Object.keys(nets)) {
    console.log(`Kiểm tra giao diện: ${name}`);
    for (const net of nets[name]) {
      console.log(`  - ${net.family} | ${net.address} | internal: ${net.internal}`);
      // Chỉ quan tâm đến địa chỉ IPv4 và không phải địa chỉ internal
      if (net.family === 'IPv4' && !net.internal) {
        results.push(net.address);
      }
    }
  }

  console.log('Các địa chỉ IP hợp lệ tìm thấy:', results);

  // Ưu tiên địa chỉ IP không phải localhost
  for (const ip of results) {
    if (!ip.startsWith('127.')) {
      console.log('Địa chỉ IP được chọn:', ip);
      return ip;
    }
  }

  // Nếu không tìm thấy IP không phải localhost, trả về localhost
  const finalIP = results.length > 0 ? results[0] : '127.0.0.1';
  console.log('Địa chỉ IP được chọn (fallback):', finalIP);
  return finalIP;
}

/**
 * Kiểm tra xem hai địa chỉ IP có cùng mạng không
 * @param {string} ip1 - Địa chỉ IP thứ nhất
 * @param {string} ip2 - Địa chỉ IP thứ hai
 * @returns {boolean} - True nếu cùng mạng, False nếu khác mạng
 */
function isSameNetwork(ip1, ip2) {
  if (!ip1 || !ip2) return false;
  
  // Phương pháp đơn giản: so sánh 3 octet đầu tiên
  const segments1 = ip1.split('.');
  const segments2 = ip2.split('.');
  
  if (segments1.length !== 4 || segments2.length !== 4) {
    return false;
  }
  
  // So sánh 3 octet đầu tiên
  return segments1[0] === segments2[0] && 
         segments1[1] === segments2[1] && 
         segments1[2] === segments2[2];
}

module.exports = {
  getLocalIP,
  isSameNetwork
};