#!/usr/bin/env python3
"""
Setup C2 Server trên Public IP - Giải pháp tốt nhất để VPS kết nối Windows
"""
import os
import sys
import subprocess
import platform
import time
import requests
import socket
import json

def get_public_ip():
    """Lấy public IP của Windows"""
    print("🔍 Getting Windows Public IP...")
    
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        public_ip = response.text
        print(f"   🌐 Windows Public IP: {public_ip}")
        return public_ip
    except Exception as e:
        print(f"   ❌ Cannot get public IP: {e}")
        return None

def check_c2_server_binding():
    """Kiểm tra C2 Server có bind trên 0.0.0.0 không"""
    print("\n🔍 Checking C2 Server Binding...")
    
    try:
        # Kiểm tra port 5000 có đang listen không
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("   ✅ Port 5000 is open (C2 Server might be running)")
            
            # Kiểm tra xem có bind trên 0.0.0.0 không
            try:
                response = requests.get("http://127.0.0.1:5000/api/bots", timeout=5)
                if response.status_code == 200:
                    print("   ✅ C2 Server is running on localhost")
                    return True
                else:
                    print(f"   ⚠️  C2 Server responded with status: {response.status_code}")
                    return False
            except:
                print("   ❌ C2 Server not responding on localhost")
                return False
        else:
            print("   ❌ Port 5000 is closed (C2 Server not running)")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking C2 Server: {e}")
        return False

def create_public_ip_c2_script():
    """Tạo script khởi động C2 Server trên public IP"""
    print("\n🚀 Creating Public IP C2 Server Script...")
    
    # Script khởi động C2 Server với bind trên 0.0.0.0
    c2_script = """@echo off
echo Starting C2 Server on Public IP...
echo.
echo This will make C2 Server accessible from internet!
echo.
echo Starting C2 Server on 0.0.0.0:5000...
python c2_server_auto.py
echo.
echo C2 Server stopped.
pause
"""
    
    with open("start_c2_public_ip.bat", "w") as f:
        f.write(c2_script)
    
    print("   📝 C2 Server script created: start_c2_public_ip.bat")

def create_vps_connection_script(public_ip):
    """Tạo script kết nối từ VPS"""
    print(f"\n🤖 Creating VPS Connection Script...")
    
    # Script test kết nối từ VPS
    vps_test_script = f"""#!/bin/bash
# Test Connection to Windows C2 Server on Public IP
# Run this on your VPS

echo "🔍 Testing Connection to Windows C2 Server..."
echo "=============================================="
echo "🌐 Target: {public_ip}:5000"
echo ""

# Test 1: Ping
echo "🏓 Test 1: Ping..."
if ping -c 1 {public_ip} > /dev/null 2>&1; then
    echo "   ✅ Ping successful"
else
    echo "   ❌ Ping failed (this is normal for some ISPs)"
fi

# Test 2: Port check
echo "🔌 Test 2: Port 5000 check..."
if nc -z -w5 {public_ip} 5000 2>/dev/null; then
    echo "   ✅ Port 5000 is open"
else
    echo "   ❌ Port 5000 is closed"
    echo "   💡 Check if C2 Server is running on Windows"
    exit 1
fi

# Test 3: HTTP connection
echo "🌐 Test 3: HTTP connection..."
if curl -s --connect-timeout 10 "http://{public_ip}:5000/api/bots" > /dev/null; then
    echo "   ✅ HTTP connection successful!"
    echo "   🌐 C2 Server is accessible from VPS!"
    echo ""
    echo "🎉 SUCCESS! Now you can connect bot worker:"
    echo "python3 bot_worker_auto.py --server http://{public_ip}:5000"
else
    echo "   ❌ HTTP connection failed"
    echo "   💡 Check if:"
    echo "      1. C2 Server is running on Windows"
    echo "      2. Windows firewall allows port 5000"
    echo "      3. C2 Server binds on 0.0.0.0:5000"
    exit 1
fi

echo ""
echo "🔍 Test completed!"
"""
    
    with open("test_public_ip_from_vps.sh", "w") as f:
        f.write(vps_test_script)
    
    print(f"   📝 VPS test script created: test_public_ip_from_vps.sh")

def create_windows_firewall_script():
    """Tạo script mở firewall Windows"""
    print(f"\n🛡️ Creating Windows Firewall Script...")
    
    firewall_script = """@echo off
echo Setting up Windows Firewall for Public IP C2 Server...
echo.
echo This will allow external connections to port 5000
echo.

REM Allow inbound connections on port 5000
echo Adding inbound firewall rule...
netsh advfirewall firewall add rule name="C2 Server Public IP Inbound" dir=in action=allow protocol=TCP localport=5000

REM Allow outbound connections on port 5000
echo Adding outbound firewall rule...
netsh advfirewall firewall add rule name="C2 Server Public IP Outbound" dir=out action=allow protocol=TCP localport=5000

REM Show the rules
echo.
echo Checking firewall rules...
netsh advfirewall firewall show rule name="C2 Server Public IP*"

echo.
echo ✅ Windows Firewall setup completed!
echo 💡 C2 Server should now be accessible from internet
echo.
pause
"""
    
    with open("setup_public_ip_firewall.bat", "w") as f:
        f.write(firewall_script)
    
    print(f"   📝 Firewall script created: setup_public_ip_firewall.bat")

def create_public_ip_guide(public_ip):
    """Tạo hướng dẫn setup public IP"""
    print(f"\n📋 Public IP C2 Server Setup Guide:")
    print("=" * 60)
    
    guide = f"""
🚀 **Setup C2 Server trên Public IP để VPS kết nối trực tiếp**

### **🌐 Thông tin hiện tại:**
- **Windows Public IP**: {public_ip}
- **C2 Server Port**: 5000
- **Target URL**: http://{public_ip}:5000

### **Bước 1: Mở Windows Firewall**
```cmd
# Chạy với quyền Administrator
setup_public_ip_firewall.bat
```

### **Bước 2: Khởi động C2 Server trên Public IP**
```cmd
# Terminal 1: Khởi động C2 Server
start_c2_public_ip.bat
```

### **Bước 3: Test kết nối local**
```cmd
# Test từ Windows local
curl http://localhost:5000/api/bots
curl http://{public_ip}:5000/api/bots
```

### **Bước 4: Test từ VPS**
```bash
# Upload script lên VPS
scp test_public_ip_from_vps.sh root@<VPS_IP>:/tmp/

# Chạy test trên VPS
chmod +x /tmp/test_public_ip_from_vps.sh
/tmp/test_public_ip_from_vps.sh
```

### **Bước 5: Kết nối Bot Worker**
```bash
# Trên VPS, kết nối bot worker
python3 bot_worker_auto.py --server http://{public_ip}:5000
```

### **🌐 URLs sau khi setup:**
- **Windows Local**: http://localhost:5000
- **Windows Public**: http://{public_ip}:5000
- **VPS Bot**: http://{public_ip}:5000

### **⚠️ Lưu ý quan trọng:**
1. **C2 Server phải bind** trên 0.0.0.0:5000 (không phải 127.0.0.1:5000)
2. **Windows Firewall** phải allow port 5000
3. **C2 Server phải chạy** trước khi test từ VPS
4. **Public IP phải ổn định** (không thay đổi thường xuyên)

### **🔧 Troubleshooting:**
- **Nếu VPS không kết nối được**: Kiểm tra Windows firewall và C2 Server binding
- **Nếu port 5000 bị chặn**: Thay đổi port trong c2_server_auto.py
- **Nếu public IP thay đổi**: Cập nhật URL trên VPS
"""
    
    # Lưu guide
    guide_path = f"PUBLIC_IP_C2_GUIDE_{public_ip}.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"   📝 Public IP guide created: {guide_path}")

def show_quick_setup(public_ip):
    """Hiển thị quick setup"""
    print(f"\n🚀 Quick Setup - Thiết lập nhanh:")
    print("=" * 50)
    
    print(f"1. 🛡️ **Mở Windows Firewall:**")
    print(f"   # Chạy với quyền Administrator")
    print(f"   setup_public_ip_firewall.bat")
    
    print(f"\n2. 🚀 **Khởi động C2 Server:**")
    print(f"   start_c2_public_ip.bat")
    
    print(f"\n3. 🔍 **Test từ VPS:**")
    print(f"   # Upload và chạy test script")
    print(f"   chmod +x test_public_ip_from_vps.sh")
    print(f"   ./test_public_ip_from_vps.sh")
    
    print(f"\n4. 🤖 **Kết nối Bot Worker:**")
    print(f"   python3 bot_worker_auto.py --server http://{public_ip}:5000")
    
    print(f"\n💡 **Ưu điểm của Public IP:**")
    print(f"   ✅ Không cần ngrok")
    print(f"   ✅ Không cần port forwarding")
    print(f"   ✅ Kết nối trực tiếp và ổn định")
    print(f"   ✅ URL không thay đổi")

def main():
    """Main function"""
    print("🚀 Setup C2 Server trên Public IP - Giải pháp tốt nhất VPS kết nối Windows")
    print("=" * 80)
    
    # Lấy public IP
    public_ip = get_public_ip()
    
    if not public_ip:
        print("\n❌ Không thể lấy public IP!")
        print("💡 Hãy kiểm tra kết nối internet và thử lại")
        return
    
    # Kiểm tra C2 Server
    print(f"\n🔍 Checking Current C2 Server Status...")
    c2_running = check_c2_server_binding()
    
    if c2_running:
        print(f"   ✅ C2 Server đang chạy")
    else:
        print(f"   ❌ C2 Server không chạy hoặc không bind đúng")
    
    # Tạo scripts và guides
    create_public_ip_c2_script()
    create_vps_connection_script(public_ip)
    create_windows_firewall_script()
    create_public_ip_guide(public_ip)
    
    # Hiển thị quick setup
    show_quick_setup(public_ip)
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Chạy setup_public_ip_firewall.bat (Administrator)")
    print(f"   2. Khởi động C2 Server với start_c2_public_ip.bat")
    print(f"   3. Test từ VPS với test_public_ip_from_vps.sh")
    print(f"   4. Kết nối bot worker đến http://{public_ip}:5000")
    
    print(f"\n🎯 **Kết quả mong đợi:**")
    print(f"   Bot worker trên VPS sẽ kết nối trực tiếp đến Windows C2 Server!")
    print(f"   Không cần ngrok, không cần port forwarding!")
    print(f"   URL ổn định: http://{public_ip}:5000")

if __name__ == "__main__":
    main()
