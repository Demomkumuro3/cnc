#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start Ngrok Demo - Script tổng hợp để dễ dàng chọn và sử dụng ngrok demo
"""
import os
import subprocess
import sys

def show_menu():
    """Hiển thị menu chọn cách"""
    print("🌐 NGROK DEMO - C2 CNC")
    print("=" * 50)
    print("1. 🚀 Setup Ngrok (Tạo scripts)")
    print("2. 📥 Download Ngrok")
    print("3. 🔐 Cấu hình Ngrok")
    print("4. 🖥️  Khởi động C2 Server")
    print("5. 🌐 Tạo Ngrok Tunnel")
    print("6. 🧪 Demo Test Ngrok")
    print("7. 📖 Xem hướng dẫn chi tiết")
    print("8. ❌ Thoát")
    print("=" * 50)

def setup_ngrok():
    """Setup Ngrok"""
    print("\n🚀 Đang setup Ngrok...")
    try:
        subprocess.run([sys.executable, "setup_ngrok_simple.py"], check=True)
        print("\n✅ Ngrok setup hoàn thành!")
        print("\n📋 Files đã tạo:")
        print("- download_ngrok.bat")
        print("- start_ngrok.bat")
        print("- test_ngrok_from_vps.sh")
        print("- NGROK_GUIDE.md")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi setup Ngrok")

def download_ngrok():
    """Download Ngrok"""
    print("\n📥 Đang download Ngrok...")
    if os.path.exists("download_ngrok.bat"):
        try:
            subprocess.run(["download_ngrok.bat"], check=True)
            print("\n✅ Ngrok download hoàn thành!")
        except subprocess.CalledProcessError:
            print("❌ Lỗi khi download Ngrok")
    else:
        print("❌ File download_ngrok.bat không tồn tại")
        print("Hãy chạy option 1 trước để tạo scripts")

def configure_ngrok():
    """Cấu hình Ngrok"""
    print("\n🔐 Cấu hình Ngrok...")
    print("\n📋 Hướng dẫn:")
    print("1. Đăng ký tại: https://ngrok.com/signup")
    print("2. Lấy authtoken từ dashboard")
    print("3. Chạy lệnh:")
    print("   ngrok config add-authtoken YOUR_TOKEN")
    print("4. Kiểm tra cấu hình:")
    print("   ngrok config check")
    
    token = input("\n👉 Nhập authtoken (hoặc Enter để bỏ qua): ").strip()
    if token:
        try:
            subprocess.run(["ngrok", "config", "add-authtoken", token], check=True)
            print("✅ Authtoken đã được thêm!")
            
            print("\n🔍 Kiểm tra cấu hình...")
            subprocess.run(["ngrok", "config", "check"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Lỗi khi thêm authtoken")

def start_c2_server():
    """Khởi động C2 Server"""
    print("\n🖥️  Khởi động C2 Server...")
    print("\n📋 Hướng dẫn:")
    print("1. Mở terminal mới")
    print("2. Chạy: python c2_server_auto.py")
    print("3. Giữ terminal mở")
    print("4. Mở trình duyệt: http://localhost:5000")
    
    choice = input("\n👉 Bạn có muốn khởi động C2 Server ngay bây giờ không? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            print("\n🚀 Khởi động C2 Server...")
            subprocess.Popen([sys.executable, "c2_server_auto.py"])
            print("✅ C2 Server đang khởi động...")
            print("📋 Mở trình duyệt: http://localhost:5000")
        except Exception as e:
            print(f"❌ Lỗi khi khởi động C2 Server: {e}")

def create_ngrok_tunnel():
    """Tạo Ngrok Tunnel"""
    print("\n🌐 Tạo Ngrok Tunnel...")
    if os.path.exists("start_ngrok.bat"):
        print("\n📋 Hướng dẫn:")
        print("1. Đảm bảo C2 Server đang chạy")
        print("2. Mở terminal mới")
        print("3. Chạy: start_ngrok.bat")
        print("4. Copy URL ngrok hiển thị")
        
        choice = input("\n👉 Bạn có muốn tạo ngrok tunnel ngay bây giờ không? (y/n): ").strip().lower()
        if choice == 'y':
            try:
                print("\n🚀 Khởi động ngrok tunnel...")
                subprocess.Popen(["start_ngrok.bat"])
                print("✅ Ngrok tunnel đang khởi động...")
                print("📋 Copy URL ngrok từ terminal mới")
            except Exception as e:
                print(f"❌ Lỗi khi khởi động ngrok: {e}")
    else:
        print("❌ File start_ngrok.bat không tồn tại")
        print("Hãy chạy option 1 trước để tạo scripts")

def demo_test_ngrok():
    """Demo test Ngrok"""
    print("\n🧪 Demo Test Ngrok...")
    if os.path.exists("demo_ngrok_setup.py"):
        try:
            print("\n🚀 Chạy demo ngrok...")
            subprocess.run([sys.executable, "demo_ngrok_setup.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Lỗi khi chạy demo")
    else:
        print("❌ File demo_ngrok_setup.py không tồn tại")
        print("Hãy chạy option 1 trước để tạo scripts")

def show_guide():
    """Hiển thị hướng dẫn"""
    print("\n📖 Hướng dẫn chi tiết:")
    print("=" * 50)
    
    if os.path.exists("HUONG_DAN_NGROK_CHI_TIET.md"):
        try:
            with open("HUONG_DAN_NGROK_CHI_TIET.md", "r", encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"❌ Lỗi khi đọc file hướng dẫn: {e}")
    else:
        print("❌ File hướng dẫn không tồn tại")
        print("Hãy chạy option 1 trước để tạo hướng dẫn")

def main():
    """Main function"""
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Chọn cách (1-8): ").strip()
            
            if choice == "1":
                setup_ngrok()
            elif choice == "2":
                download_ngrok()
            elif choice == "3":
                configure_ngrok()
            elif choice == "4":
                start_c2_server()
            elif choice == "5":
                create_ngrok_tunnel()
            elif choice == "6":
                demo_test_ngrok()
            elif choice == "7":
                show_guide()
            elif choice == "8":
                print("\n👋 Tạm biệt! Chúc bạn thành công!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1-8.")
            
            if choice in ["1", "2", "3", "4", "5", "6"]:
                input("\n⏸️  Nhấn Enter để tiếp tục...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! Chúc bạn thành công!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            input("\n⏸️  Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
