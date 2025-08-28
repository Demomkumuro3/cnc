#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start All C2 Methods - Script tổng hợp để dễ dàng chọn cách làm C2 CNC
"""
import os
import platform
import subprocess
import sys

def show_menu():
    """Hiển thị menu chọn cách"""
    print("🚀 C2 CNC - TẤT CẢ CÁC CÁCH LÀM")
    print("=" * 50)
    print("1. 🌐 Ngrok Tunnel (Đơn giản nhất - Khuyến nghị)")
    print("2. 🏠 VPS làm C2 Server (Ổn định nhất)")
    print("3. 🔥 Public IP Windows (Đã thử - có vấn đề)")
    print("4. 📖 Xem hướng dẫn chi tiết")
    print("5. 🧹 Dọn dẹp file không cần thiết")
    print("6. ❌ Thoát")
    print("=" * 50)

def setup_ngrok():
    """Setup Ngrok"""
    print("\n🌐 Đang setup Ngrok...")
    try:
        subprocess.run([sys.executable, "setup_ngrok_simple.py"], check=True)
        print("\n✅ Ngrok setup hoàn thành!")
        print("\n📋 Hướng dẫn sử dụng:")
        print("1. Chạy: download_ngrok.bat")
        print("2. Đăng ký tại: https://ngrok.com/signup")
        print("3. Lấy authtoken và cấu hình")
        print("4. Khởi động C2 Server: python c2_server_auto.py")
        print("5. Tạo tunnel: start_ngrok.bat")
        print("6. Copy URL ngrok và sử dụng trên VPS")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi setup Ngrok")

def setup_vps_c2():
    """Setup VPS C2 Server"""
    print("\n🏠 Đang setup VPS C2 Server...")
    try:
        subprocess.run([sys.executable, "setup_vps_c2_server.py"], check=True)
        print("\n✅ VPS C2 Server setup hoàn thành!")
        print("\n📋 Hướng dẫn sử dụng:")
        print("1. Upload setup_vps_c2_server.sh lên VPS")
        print("2. Chạy: chmod +x setup_vps_c2_server.sh && ./setup_vps_c2_server.sh")
        print("3. Lấy VPS IP: curl -s https://api.ipify.org")
        print("4. Trên Windows: start_bot_worker_windows.bat")
        print("5. Nhập VPS IP khi được yêu cầu")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi setup VPS C2 Server")

def setup_public_ip():
    """Setup Public IP Windows"""
    print("\n🔥 Đang setup Public IP Windows...")
    try:
        subprocess.run([sys.executable, "setup_public_ip_c2.py"], check=True)
        print("\n✅ Public IP Windows setup hoàn thành!")
        print("\n⚠️  CẢNH BÁO: Cách này có vấn đề firewall!")
        print("\n📋 Hướng dẫn sử dụng:")
        print("1. Chạy: setup_public_ip_firewall.bat (Administrator)")
        print("2. Khởi động C2 Server: start_c2_public_ip.bat")
        print("3. Test từ VPS: test_public_ip_from_vps.sh")
        print("4. Kết nối bot worker đến public IP")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi setup Public IP Windows")

def show_guide():
    """Hiển thị hướng dẫn"""
    print("\n📖 Hướng dẫn chi tiết:")
    print("=" * 50)
    
    if os.path.exists("HUONG_DAN_SU_DUNG_C2_CNC.md"):
        try:
            with open("HUONG_DAN_SU_DUNG_C2_CNC.md", "r", encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"❌ Lỗi khi đọc file hướng dẫn: {e}")
    else:
        print("❌ File hướng dẫn không tồn tại")
        print("Hãy chạy option 1 hoặc 2 trước để tạo hướng dẫn")

def cleanup_files():
    """Dọn dẹp file không cần thiết"""
    print("\n🧹 Đang dọn dẹp file không cần thiết...")
    
    files_to_keep = [
        "c2_server_auto.py",
        "bot_worker_auto.py",
        "command_interface.html",
        "send_command.py",
        "setup_ngrok_simple.py",
        "setup_vps_c2_server.py",
        "setup_public_ip_c2.py",
        "HUONG_DAN_SU_DUNG_C2_CNC.md",
        "start_all_c2_methods.py"
    ]
    
    current_files = [f for f in os.listdir(".") if os.path.isfile(f)]
    
    for file in current_files:
        if file not in files_to_keep and not file.endswith(('.py', '.md', '.html')):
            try:
                os.remove(file)
                print(f"🗑️  Đã xóa: {file}")
            except Exception as e:
                print(f"❌ Không thể xóa {file}: {e}")
    
    print("✅ Dọn dẹp hoàn thành!")

def main():
    """Main function"""
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Chọn cách (1-6): ").strip()
            
            if choice == "1":
                setup_ngrok()
            elif choice == "2":
                setup_vps_c2()
            elif choice == "3":
                setup_public_ip()
            elif choice == "4":
                show_guide()
            elif choice == "5":
                cleanup_files()
            elif choice == "6":
                print("\n👋 Tạm biệt! Chúc bạn thành công!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1-6.")
            
            if choice in ["1", "2", "3", "5"]:
                input("\n⏸️  Nhấn Enter để tiếp tục...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! Chúc bạn thành công!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            input("\n⏸️  Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
