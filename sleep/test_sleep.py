import time
import subprocess
import os
import win32gui
import win32con
import win32api
import win32gui_struct
import threading


def monitor_power_events(proc):
    hwnd = win32gui.CreateWindow("STATIC", "PowerEventMonitor", 0, 0, 0, 0, 0, 0, 0, 0, None)

    def wnd_proc(hwnd, msg, wparam, lparam):
        if msg == win32con.WM_POWERBROADCAST and wparam == win32con.PBT_APMSUSPEND:
            print("System is going to sleep. Terminating subprocess.")
            proc.terminate()
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, wnd_proc)
    while True:
        win32gui.PumpMessages()

def main():
    proc = subprocess.Popen(["python", "hello.py"])

    threading.Thread(target = monitor_power_events, args=(proc,),daemon=True).start()

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("Terminating subprocess manually...")
        proc.terminate()

# def monitor_sleep(start):
#     """
#     Giám sát trạng thái sleep và hiển thị trạng thái hoạt động.
#     """
#     print("Chương trình đang theo dõi trạng thái máy...")
#     last_time = time.time()

#     while True:
#         try:
#             # Đợi một khoảng thời gian ngắn để kiểm tra
#             time.sleep(2)
#             current_time = time.time()
            
#             # Kiểm tra khoảng thời gian gián đoạn (lớn hơn 5 giây nghĩa là máy đã sleep)
#             if current_time - last_time > 5 or start == 0:
#                 try:
#                     print(">>> Máy vừa vào trạng thái sleep. Đang chạy hello.py...")
#                     subprocess.run(["python", "D:\HCMUT\Do_an_KTMT\connect_device\sleep\hello.py"], check=True)
#                     print(">>> Đã chạy hello.py thành công!")
#                 except subprocess.CalledProcessError as e:
#                     print(">>> Lỗi khi chạy hello.py:", e)
#             else:
#                 print("Máy đang hoạt động bình thường.")
            
#             # Cập nhật thời gian lần cuối
#             last_time = current_time
#             start = start + 1

#         except KeyboardInterrupt:
#             print("Dừng theo dõi.")
#             break

if __name__ == "__main__":
    # start = 0
    # monitor_sleep(start)
    main()


