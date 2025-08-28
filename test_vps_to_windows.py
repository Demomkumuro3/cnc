#!/usr/bin/env python3
"""
Test VPS to Windows Connection - Test kết nối từ VPS đến Windows C2 Server
"""
import requests
import socket
import time
import sys

def test_connection(windows_ip, windows_port):
    """Test kết nối đến Windows C2 Server"""
    print(f"🔍 Testing Connection to Windows C2 Server...")
    print(f"🎯 Target: {windows_ip}:{windows_port}")
    print("=" * 50)
    
    # Test 1: Ping
    print("🏓 Test 1: Ping...")
    try:
        import subprocess
        if sys.platform == "win32":
            result = subprocess.run(["ping", "-n", "1", windows_ip], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(["ping", "-c", "1", windows_ip], 
                                  capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Ping successful")
        else:
            print("   ❌ Ping failed")
    except Exception as e:
        print(f"   ❌ Ping test failed: {e}")
    
    # Test 2: Port check
    print(f"🔌 Test 2: Port {windows_port} check...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((windows_ip, int(windows_port)))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port {windows_port} is open")
        else:
            print(f"   ❌ Port {windows_port} is closed")
            return False
    except Exception as e:
        print(f"   ❌ Port test failed: {e}")
        return False
    
    # Test 3: HTTP connection
    print(f"🌐 Test 3: HTTP connection...")
    try:
        response = requests.get(f"http://{windows_ip}:{windows_port}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ HTTP connection successful")
        else:
            print(f"   ❌ HTTP status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ HTTP test failed: {e}")
        return False
    
    # Test 4: API endpoint
    print(f"🔧 Test 4: API endpoint...")
    try:
        response = requests.get(f"http://{windows_ip}:{windows_port}/api/bots", timeout=10)
        if response.status_code == 200:
            print("   ✅ API endpoint accessible")
            bots = response.json()
            print(f"   🤖 Online bots: {len(bots)}")
        else:
            print(f"   ❌ API endpoint error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False
    
    # Test 5: System status
    print(f"📊 Test 5: System status...")
    try:
        response = requests.get(f"http://{windows_ip}:{windows_port}/api/system-status", timeout=10)
        if response.status_code == 200:
            print("   ✅ System status accessible")
            status = response.json()
            print(f"   🖥️  Server: {status.get('server_status', 'Unknown')}")
        else:
            print(f"   ❌ System status error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ System status test failed: {e}")
    
    return True

def show_diagnostic_info(windows_ip, windows_port):
    """Hiển thị thông tin diagnostic"""
    print(f"\n🔧 Diagnostic Information:")
    print("=" * 50)
    
    print(f"📍 Windows IP: {windows_ip}")
    print(f"🔌 Port: {windows_port}")
    print(f"🌐 URLs to test:")
    print(f"   - Main: http://{windows_ip}:{windows_port}")
    print(f"   - API: http://{windows_ip}:{windows_port}/api/bots")
    print(f"   - Status: http://{windows_ip}:{windows_port}/api/system-status")
    
    print(f"\n💡 Common Issues & Solutions:")
    print("1. ❌ Port closed:")
    print("   - Check Windows firewall")
    print("   - Run: powershell -ExecutionPolicy Bypass -File windows_firewall_setup.ps1")
    
    print("2. ❌ C2 Server not running:")
    print("   - Start: python c2_server_auto.py")
    
    print("3. ❌ Network inaccessible:")
    print("   - Check router port forwarding")
    print("   - Check Windows network settings")
    
    print("4. ❌ Firewall blocking:")
    print("   - Run Windows firewall script as Administrator")
    print("   - Check antivirus settings")

def main():
    """Main function"""
    print("🔍 Test VPS to Windows Connection")
    print("=" * 50)
    
    # Lấy thông tin
    windows_ip = input("🏠 Nhập IP của máy Windows (mặc định 192.168.1.5): ").strip() or "192.168.1.5"
    windows_port = input("🔌 Nhập port của C2 Server (mặc định 5000): ").strip() or "5000"
    
    print(f"\n🎯 Testing connection to {windows_ip}:{windows_port}")
    
    # Test kết nối
    if test_connection(windows_ip, windows_port):
        print(f"\n🎉 Connection test successful!")
        print(f"✅ Windows C2 Server is accessible from this location")
        print(f"🌐 You can now run bot worker on VPS:")
        print(f"   python3 bot_worker_auto.py --server http://{windows_ip}:{windows_port}")
    else:
        print(f"\n❌ Connection test failed!")
        print(f"💡 Windows C2 Server is not accessible")
        
        # Hiển thị diagnostic info
        show_diagnostic_info(windows_ip, windows_port)

if __name__ == "__main__":
    main()
