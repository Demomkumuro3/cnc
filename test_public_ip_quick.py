#!/usr/bin/env python3
"""
Quick Test Public IP C2 Server - Test nhanh C2 Server trên public IP
"""
import requests
import socket
import time
import sys

def test_public_ip_c2():
    """Test C2 Server trên public IP"""
    print("🔍 Quick Test: Public IP C2 Server")
    print("=" * 50)
    
    # Lấy public IP
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        public_ip = response.text
        print(f"🌐 Windows Public IP: {public_ip}")
    except:
        print("❌ Cannot get public IP")
        return False
    
    # Test 1: Local connection
    print(f"\n🏠 Test 1: Local Connection...")
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ Local C2 Server accessible")
        else:
            print(f"   ❌ Local C2 Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Local C2 Server not accessible: {e}")
        return False
    
    # Test 2: Public IP connection
    print(f"\n🌐 Test 2: Public IP Connection...")
    try:
        response = requests.get(f"http://{public_ip}:5000/api/bots", timeout=10)
        if response.status_code == 200:
            print("   ✅ Public IP C2 Server accessible!")
            print(f"   🎉 SUCCESS! VPS can connect to: http://{public_ip}:5000")
            return True
        else:
            print(f"   ❌ Public IP C2 Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Public IP C2 Server not accessible: {e}")
        print(f"   💡 This means VPS cannot connect directly")
        return False

def show_solution():
    """Hiển thị giải pháp"""
    print(f"\n🔧 Solution - Giải pháp:")
    print("=" * 40)
    
    print("1. 🛡️ **Mở Windows Firewall:**")
    print("   # Chạy với quyền Administrator")
    print("   setup_public_ip_firewall.bat")
    
    print(f"\n2. 🚀 **Khởi động C2 Server:**")
    print(f"   start_c2_public_ip.bat")
    
    print(f"\n3. 🔍 **Test lại:**")
    print(f"   python test_public_ip_quick.py")
    
    print(f"\n4. 🤖 **Kết nối từ VPS:**")
    print(f"   python3 bot_worker_auto.py --server http://<PUBLIC_IP>:5000")

def main():
    """Main function"""
    print("🚀 Quick Test Public IP C2 Server")
    print("=" * 50)
    
    # Test public IP
    if test_public_ip_c2():
        print(f"\n🎉 C2 Server is accessible via public IP!")
        print(f"💡 VPS can connect directly without ngrok or port forwarding!")
    else:
        print(f"\n❌ C2 Server not accessible via public IP")
        show_solution()

if __name__ == "__main__":
    main()
