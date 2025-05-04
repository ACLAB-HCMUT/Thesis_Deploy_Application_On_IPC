import socket
import os
import json
import subprocess
import platform

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_wifi_name():
    system = platform.system()
    wifi_name = "Unknown"
    
    try:
        if system == "Windows":
            # Windows command to get SSID
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8')
            for line in output.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    wifi_name = line.split(':')[1].strip()
                    break
        
        elif system == "Darwin":  # macOS
            # macOS command to get SSID
            output = subprocess.check_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I", shell=True).decode('utf-8')
            for line in output.split('\n'):
                if " SSID: " in line:
                    wifi_name = line.split(':')[1].strip()
                    break
        
        elif system == "Linux":
            # Linux command to get SSID
            output = subprocess.check_output("iwgetid -r", shell=True).decode('utf-8')
            wifi_name = output.strip()
    
    except (subprocess.SubprocessError, UnicodeDecodeError, IndexError):
        wifi_name = "Không thể lấy tên WiFi"
    
    return wifi_name

if __name__ == "__main__":
    ip = get_local_ip()
    wifi_name = get_wifi_name()
    
    # Tạo JSON object với IP và tên WiFi
    ip_data = {
        "ipAddress": ip,
        "wifiName": wifi_name
    }
    
    # Đường dẫn cho file JSON
    ip_file_path = "./src/pages/authentication/ip.json"
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(ip_file_path), exist_ok=True)
    
    # Ghi JSON vào file
    with open(ip_file_path, "w") as f:
        json.dump(ip_data, f)
    
    # In thông tin ra stdout
    print(f"{ip},{wifi_name}")