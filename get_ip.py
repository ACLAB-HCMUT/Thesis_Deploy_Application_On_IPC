import socket
import os

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

if __name__ == "__main__":
    ip = get_local_ip()
    
    # Đổi đường dẫn từ public/ip.txt sang src/ip.txt
    ip_file_path = "src/ip.txt"
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(ip_file_path), exist_ok=True)
    
    # Ghi vào file trong thư mục src
    with open(ip_file_path, "w") as f:
        f.write(ip)
    
    # In trực tiếp ra stdout để Electron đọc
    print(ip)  # Đảm bảo đây là output duy nhất từ script