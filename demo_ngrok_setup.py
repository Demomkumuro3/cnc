#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Ngrok Setup - Script demo để test ngrok setup một cách trực quan
"""
import os
import subprocess
import sys
import time
import requests

def check_ngrok_installed():
    """Kiểm tra ngrok đã được cài đặt chưa"""
    print("🔍 Kiểm tra ngrok...")
    
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ngrok đã cài đặt: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ngrok chưa cài đặt hoặc có lỗi")
            return False
    except FileNotFoundError:
        print("❌ Ngrok chưa được cài đặt")
        return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra ngrok: {e}")
        return False

def check_ngrok_config():
    """Kiểm tra cấu hình ngrok"""
    print("\n🔍 Kiểm tra cấu hình ngrok...")
    
    try:
        result = subprocess.run(['ngrok', 'config', 'check'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Cấu hình ngrok OK")
            print(result.stdout)
            return True
        else:
            print("❌ Cấu hình ngrok chưa hoàn chỉnh")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra cấu hình: {e}")
        return False

def check_c2_server():
    """Kiểm tra C2 Server có đang chạy không"""
    print("\n🔍 Kiểm tra C2 Server...")
    
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("✅ C2 Server đang chạy trên port 5000")
            return True
        else:
            print(f"❌ C2 Server trả về status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ C2 Server không chạy hoặc không thể kết nối")
        return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra C2 Server: {e}")
        return False

def start_ngrok_tunnel():
    """Khởi động ngrok tunnel"""
    print("\n🚀 Khởi động ngrok tunnel...")
    
    try:
        # Khởi động ngrok trong background
        process = subprocess.Popen(['ngrok', 'http', '5000'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Đợi một chút để ngrok khởi động
        time.sleep(3)
        
        # Kiểm tra ngrok có đang chạy không
        if process.poll() is None:
            print("✅ Ngrok tunnel đang chạy")
            print("📋 Lưu ý: Giữ terminal này mở để duy trì tunnel")
            return process
        else:
            print("❌ Ngrok tunnel không thể khởi động")
            return None
            
    except Exception as e:
        print(f"❌ Lỗi khi khởi động ngrok: {e}")
        return None

def get_ngrok_url():
    """Lấy URL ngrok từ API"""
    print("\n🔍 Lấy URL ngrok...")
    
    try:
        # Đợi ngrok khởi động hoàn toàn
        time.sleep(5)
        
        response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            if tunnels:
                public_url = tunnels[0]['public_url']
                print(f"✅ URL ngrok: {public_url}")
                return public_url
            else:
                print("❌ Không tìm thấy tunnel nào")
                return None
        else:
            print(f"❌ Không thể lấy thông tin tunnel: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi khi lấy URL ngrok: {e}")
        return None

def test_ngrok_connection(url):
    """Test kết nối ngrok"""
    print(f"\n🧪 Test kết nối ngrok: {url}")
    
    try:
        response = requests.get(f"{url}/api/bots", timeout=10)
        if response.status_code == 200:
            print("✅ Kết nối ngrok thành công!")
            print("🌐 VPS có thể kết nối đến Windows C2 Server!")
            return True
        else:
            print(f"❌ Kết nối ngrok thất bại: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi test kết nối: {e}")
        return False

def show_usage_instructions(url):
    """Hiển thị hướng dẫn sử dụng"""
    print("\n" + "="*60)
    print("🎉 SETUP NGROK THÀNH CÔNG!")
    print("="*60)
    
    print(f"\n🌐 URL ngrok của bạn: {url}")
    print("\n📋 Hướng dẫn sử dụng:")
    print("1. Giữ terminal ngrok mở để duy trì tunnel")
    print("2. Trên VPS, kết nối bot worker:")
    print(f"   python3 bot_worker_auto.py --server {url}")
    print("3. Bot worker sẽ hiển thị trong giao diện web")
    print("4. Gửi lệnh qua http://localhost:5000")
    
    print("\n⚠️  Lưu ý quan trọng:")
    print("- URL ngrok thay đổi mỗi lần restart")
    print("- Cần copy URL mới mỗi lần")
    print("- Bot worker cần kết nối lại với URL mới")
    
    print("\n🚀 Bạn đã sẵn sàng sử dụng C2 CNC qua ngrok!")

def main():
    """Main function"""
    print("🌐 DEMO NGROK SETUP - C2 CNC")
    print("="*50)
    
    # Bước 1: Kiểm tra ngrok
    if not check_ngrok_installed():
        print("\n❌ Vui lòng cài đặt ngrok trước:")
        print("1. Chạy: python setup_ngrok_simple.py")
        print("2. Chạy: download_ngrok.bat")
        print("3. Đăng ký tại: https://ngrok.com/signup")
        print("4. Cấu hình authtoken")
        return
    
    # Bước 2: Kiểm tra cấu hình
    if not check_ngrok_config():
        print("\n❌ Vui lòng cấu hình ngrok authtoken:")
        print("ngrok config add-authtoken YOUR_TOKEN")
        return
    
    # Bước 3: Kiểm tra C2 Server
    if not check_c2_server():
        print("\n❌ Vui lòng khởi động C2 Server trước:")
        print("python c2_server_auto.py")
        return
    
    # Bước 4: Khởi động ngrok tunnel
    ngrok_process = start_ngrok_tunnel()
    if not ngrok_process:
        return
    
    try:
        # Bước 5: Lấy URL ngrok
        url = get_ngrok_url()
        if not url:
            print("❌ Không thể lấy URL ngrok")
            return
        
        # Bước 6: Test kết nối
        if test_ngrok_connection(url):
            # Bước 7: Hiển thị hướng dẫn
            show_usage_instructions(url)
        else:
            print("❌ Kết nối ngrok không hoạt động")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Dừng ngrok tunnel...")
    finally:
        if ngrok_process:
            ngrok_process.terminate()
            print("✅ Ngrok tunnel đã dừng")

if __name__ == "__main__":
    main()
