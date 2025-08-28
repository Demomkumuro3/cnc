#!/usr/bin/env python3
"""
Setup C2 Server on GitHub Codespaces
"""
import os
import sys
import subprocess
import platform
import time
import requests
import json

def get_codespaces_info():
    """Lấy thông tin Codespaces"""
    print("🔍 Getting Codespaces Information...")
    
    # Lấy IP public
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        public_ip = response.text
        print(f"   🌐 Public IP: {public_ip}")
    except:
        public_ip = "unknown"
        print("   ❌ Cannot get public IP")
    
    # Lấy IP local
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"   🏠 Local IP: {local_ip}")
    except:
        local_ip = "127.0.0.1"
        print("   ❌ Cannot get local IP")
    
    # Lấy port
    port = 5000
    print(f"   🔌 Port: {port}")
    
    return {
        'public_ip': public_ip,
        'local_ip': local_ip,
        'port': port,
        'hostname': hostname if 'hostname' in locals() else 'codespaces'
    }

def check_dependencies():
    """Kiểm tra dependencies"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = ['flask', 'flask_socketio', 'psutil', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("   ✅ Packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install packages: {e}")
            return False
    
    return True

def setup_c2_server():
    """Setup C2 Server"""
    print("\n🚀 Setting up C2 Server...")
    
    # Kiểm tra xem C2 server có đang chạy không
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ C2 Server already running")
            return True
    except:
        pass
    
    # Khởi động C2 server
    print("   🔧 Starting C2 Server...")
    try:
        # Chạy C2 server trong background
        process = subprocess.Popen([
            sys.executable, "c2_server_auto.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đợi server khởi động
        time.sleep(5)
        
        # Kiểm tra kết nối
        for i in range(10):
            try:
                response = requests.get("http://localhost:5000/api/bots", timeout=5)
                if response.status_code == 200:
                    print("   ✅ C2 Server started successfully")
                    return True
            except:
                time.sleep(1)
        
        print("   ❌ C2 Server failed to start")
        return False
        
    except Exception as e:
        print(f"   ❌ Error starting C2 Server: {e}")
        return False

def test_connectivity():
    """Test kết nối"""
    print("\n🔌 Testing Connectivity...")
    
    codespaces_info = get_codespaces_info()
    
    # Test localhost
    print("📍 Testing localhost:5000...")
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ localhost:5000 - OK")
        else:
            print(f"   ❌ localhost:5000 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ localhost:5000 - Error: {e}")
    
    # Test local IP
    print(f"📍 Testing {codespaces_info['local_ip']}:5000...")
    try:
        response = requests.get(f"http://{codespaces_info['local_ip']}:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ {codespaces_info['local_ip']}:5000 - OK")
        else:
            print(f"   ❌ {codespaces_info['local_ip']}:5000 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {codespaces_info['local_ip']}:5000 - Error: {e}")

def start_bot_worker():
    """Khởi động Bot Worker"""
    print("\n🤖 Starting Bot Worker...")
    
    codespaces_info = get_codespaces_info()
    
    # Thử kết nối với localhost trước
    print("   📍 Trying localhost:5000...")
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ localhost:5000 accessible")
            server_url = "http://localhost:5000"
        else:
            raise Exception("Server not accessible")
    except:
        # Thử local IP
        print(f"   📍 Trying {codespaces_info['local_ip']}:5000...")
        try:
            response = requests.get(f"http://{codespaces_info['local_ip']}:5000/api/bots", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {codespaces_info['local_ip']}:5000 accessible")
                server_url = f"http://{codespaces_info['local_ip']}:5000"
            else:
                raise Exception("Server not accessible")
        except:
            print("   ❌ No accessible server found")
            return False
    
    # Khởi động bot worker
    print(f"   🚀 Starting bot worker with {server_url}")
    try:
        process = subprocess.Popen([
            sys.executable, "bot_worker_auto.py",
            "--server", server_url
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đợi một chút
        time.sleep(5)
        
        if process.poll() is None:
            print("   ✅ Bot Worker started successfully")
            print(f"   🌐 Server: {server_url}")
            print(f"   🤖 Bot ID: AutoBot-codespaces")
            return True
        else:
            stdout, stderr = process.communicate()
            if "Successfully registered" in stdout:
                print("   ✅ Bot Worker connected successfully")
                return True
            else:
                print("   ❌ Bot Worker failed to connect")
                print(f"   📝 Error: {stderr[:200]}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error starting bot worker: {e}")
        return False

def show_instructions():
    """Hiển thị hướng dẫn"""
    print("\n📋 Instructions - Hướng dẫn sử dụng:")
    print("=" * 60)
    
    codespaces_info = get_codespaces_info()
    
    print("1. 🚀 C2 Server đang chạy trên Codespaces")
    print(f"   📍 Local: http://localhost:5000")
    print(f"   📍 Local IP: http://{codespaces_info['local_ip']}:5000")
    
    print("\n2. 🤖 Bot Worker đã kết nối thành công")
    print("   📍 Server: http://localhost:5000")
    
    print("\n3. 🌐 Web Interface:")
    print("   📍 http://localhost:5000")
    print("   📍 http://" + codespaces_info['local_ip'] + ":5000")
    
    print("\n4. 📱 Command Interface:")
    print("   📍 python send_command.py")
    
    print("\n5. 🔍 Test Connection:")
    print("   📍 curl http://localhost:5000/api/bots")
    
    print(f"\n⚠️  Lưu ý: Codespaces chỉ accessible từ localhost")
    print(f"   Không thể kết nối từ máy Windows local (192.168.1.5)")

def main():
    """Main function"""
    print("🚀 Setup C2 Server on GitHub Codespaces")
    print("=" * 60)
    
    # Kiểm tra OS
    if platform.system() != "Linux":
        print("❌ This script is designed for Linux (Codespaces)")
        print("💡 For Windows, use: python c2_server_auto.py")
        return
    
    # Kiểm tra dependencies
    if not check_dependencies():
        print("❌ Dependencies check failed")
        return
    
    # Setup C2 server
    if not setup_c2_server():
        print("❌ C2 Server setup failed")
        return
    
    # Test connectivity
    test_connectivity()
    
    # Start bot worker
    if not start_bot_worker():
        print("❌ Bot Worker setup failed")
        return
    
    # Show instructions
    show_instructions()
    
    print("\n🎉 Setup completed successfully!")
    print("💡 Your C2 Server is now running on Codespaces")

if __name__ == "__main__":
    main()
