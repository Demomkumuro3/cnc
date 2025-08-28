#!/usr/bin/env python3
"""
Fix Bot Connection - Tự động sửa lỗi kết nối bot worker
"""
import subprocess
import sys
import time
import os
import signal
import threading

def get_local_ip():
    """Lấy IP local"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.5"  # Fallback IP

def start_c2_server():
    """Khởi động C2 Server"""
    print("🚀 Starting C2 Server...")
    try:
        # Kiểm tra xem C2 server có đang chạy không
        result = subprocess.run([
            "netstat", "-an"
        ], capture_output=True, text=True, timeout=5)
        
        if ":5000" in result.stdout:
            print("   ✅ C2 Server đang chạy trên port 5000")
            return True
        else:
            print("   ❌ C2 Server không chạy trên port 5000")
            return False
    except:
        return False

def start_bot_worker(server_ip):
    """Khởi động Bot Worker với IP chính xác"""
    print(f"🤖 Starting Bot Worker with server: {server_ip}")
    
    try:
        # Chạy bot worker với IP chính xác
        process = subprocess.Popen([
            sys.executable, "bot_worker_auto.py",
            "--server", f"http://{server_ip}:5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Đợi một chút để xem kết quả
        time.sleep(5)
        
        # Kiểm tra output
        if process.poll() is None:
            print("   ✅ Bot Worker đang chạy...")
            print("   📍 Server IP:", server_ip)
            print("   🌐 Web UI: http://" + server_ip + ":5000")
            return process
        else:
            stdout, stderr = process.communicate()
            if "Successfully registered" in stdout:
                print("   ✅ Bot Worker kết nối thành công!")
                return process
            else:
                print("   ❌ Bot Worker kết nối thất bại")
                print("   📝 Error:", stderr[:200])
                return None
                
    except Exception as e:
        print(f"   ❌ Error starting bot worker: {e}")
        return None

def show_status():
    """Hiển thị trạng thái hệ thống"""
    print("\n📊 System Status:")
    print("=" * 50)
    
    # Kiểm tra C2 server
    print("🔍 Checking C2 Server...")
    try:
        import requests
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ C2 Server: Running")
            bots = response.json()
            print(f"   🤖 Online Bots: {len(bots)}")
        else:
            print("   ❌ C2 Server: Error")
    except:
        print("   ❌ C2 Server: Not accessible")
    
    # Kiểm tra port 5000
    print("🔌 Checking Port 5000...")
    try:
        result = subprocess.run([
            "netstat", "-an"
        ], capture_output=True, text=True, timeout=5)
        
        if ":5000" in result.stdout:
            print("   ✅ Port 5000: Open")
        else:
            print("   ❌ Port 5000: Closed")
    except:
        print("   ❌ Port 5000: Unknown")

def main():
    """Main function"""
    print("🔧 Fix Bot Connection - Tự động sửa lỗi kết nối")
    print("=" * 60)
    
    # Lấy IP local
    local_ip = get_local_ip()
    print(f"📍 Local IP: {local_ip}")
    
    # Kiểm tra C2 server
    if not start_c2_server():
        print("\n💡 C2 Server chưa chạy. Hãy chạy:")
        print("   python c2_server_auto.py")
        print("\nSau đó chạy lại script này!")
        return
    
    # Khởi động bot worker
    print(f"\n🤖 Khởi động Bot Worker...")
    bot_process = start_bot_worker(local_ip)
    
    if bot_process:
        print(f"\n🎉 Bot Worker đã kết nối thành công!")
        print(f"📍 Server: http://{local_ip}:5000")
        print(f"🌐 Web UI: http://{local_ip}:5000")
        print(f"📱 Command: python send_command.py")
        
        # Hiển thị trạng thái
        show_status()
        
        print(f"\n💡 Để dừng Bot Worker, nhấn Ctrl+C")
        
        try:
            # Giữ script chạy
            while bot_process.poll() is None:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping Bot Worker...")
            bot_process.terminate()
            bot_process.wait()
            print("✅ Bot Worker stopped")
    else:
        print(f"\n❌ Không thể khởi động Bot Worker")
        print(f"💡 Hãy kiểm tra:")
        print(f"   1. C2 Server có đang chạy không")
        print(f"   2. Firewall có chặn port 5000 không")
        print(f"   3. Chạy: python bot_worker_auto.py --server http://{local_ip}:5000")

if __name__ == "__main__":
    main()
