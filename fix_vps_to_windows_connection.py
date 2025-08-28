#!/usr/bin/env python3
"""
Fix VPS to Windows Connection - Bot Worker trên Google Cloud VPS kết nối đến C2 Server trên Windows Local
"""
import os
import sys
import subprocess
import platform
import time
import requests
import json
import socket
import threading

def get_network_info():
    """Lấy thông tin network"""
    print("🔍 Getting Network Information...")
    
    # Lấy IP public của Codespaces (nếu đang chạy trên Codespaces)
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        current_public_ip = response.text
        print(f"   🌐 Current Public IP: {current_public_ip}")
    except:
        current_public_ip = "unknown"
        print("   ❌ Cannot get current public IP")
    
    # Lấy thông tin Windows local
    windows_ip = input("🏠 Nhập IP của máy Windows local (mặc định 192.168.1.5): ").strip() or "192.168.1.5"
    windows_port = input("🔌 Nhập port của C2 Server (mặc định 5000): ").strip() or "5000"
    
    # Lấy thông tin VPS
    vps_ip = input("🌐 Nhập IP của Google Cloud VPS: ").strip()
    
    return {
        'current_public_ip': current_public_ip,
        'windows_ip': windows_ip,
        'windows_port': windows_port,
        'vps_ip': vps_ip
    }

def check_windows_connectivity(windows_ip, windows_port):
    """Kiểm tra kết nối đến Windows local"""
    print(f"\n🔌 Testing Windows Local Connection...")
    print(f"🎯 Target: {windows_ip}:{windows_port}")
    
    # Test ping
    print("🏓 Testing ping...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["ping", "-n", "1", windows_ip], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(["ping", "-c", "1", windows_ip], 
                                  capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Ping successful")
        else:
            print("   ❌ Ping failed")
    except:
        print("   ❌ Ping test failed")
    
    # Test port
    print(f"🔌 Testing port {windows_port}...")
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
    
    # Test HTTP connection
    print(f"🌐 Testing HTTP connection...")
    try:
        response = requests.get(f"http://{windows_ip}:{windows_port}/api/bots", timeout=10)
        if response.status_code == 200:
            print("   ✅ HTTP connection successful")
            return True
        else:
            print(f"   ❌ HTTP status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ HTTP test failed: {e}")
        return False

def create_windows_firewall_script(windows_ip, windows_port):
    """Tạo script mở firewall trên Windows"""
    print(f"\n🛡️ Creating Windows Firewall Script...")
    
    # Tạo PowerShell script
    powershell_script = f"""# Windows Firewall Script for C2 Server
# Run this on Windows with Administrator privileges

Write-Host "🛡️ Setting up Windows Firewall for C2 Server..." -ForegroundColor Green

# Allow inbound connection on port {windows_port}
Write-Host "🔧 Adding inbound firewall rule..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="C2 Server Inbound" dir=in action=allow protocol=TCP localport={windows_port}

# Allow outbound connection on port {windows_port}
Write-Host "🔧 Adding outbound firewall rule..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="C2 Server Outbound" dir=out action=allow protocol=TCP localport={windows_port}

# Check if rules were added
Write-Host "🔍 Checking firewall rules..." -ForegroundColor Yellow
netsh advfirewall firewall show rule name="C2 Server*"

Write-Host "✅ Windows Firewall setup completed!" -ForegroundColor Green
Write-Host "💡 C2 Server should now be accessible from external IPs" -ForegroundColor Cyan
"""
    
    # Lưu script
    script_path = "windows_firewall_setup.ps1"
    with open(script_path, "w") as f:
        f.write(powershell_script)
    
    print(f"   📝 Windows firewall script created: {script_path}")
    print(f"   💡 Run this script on Windows with Administrator privileges:")
    print(f"      powershell -ExecutionPolicy Bypass -File {script_path}")

def create_vps_bot_worker_script(windows_ip, windows_port, vps_ip):
    """Tạo script chạy bot worker trên VPS"""
    print(f"\n🤖 Creating VPS Bot Worker Script...")
    
    # Tạo bash script
    bash_script = f"""#!/bin/bash
# Bot Worker Script for Google Cloud VPS
# Run this on your VPS

echo "🤖 Setting up Bot Worker on VPS..."

# Update system
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python and dependencies..."
apt install -y python3 python3-pip
pip3 install flask flask-socketio psutil requests

# Create directory
echo "📁 Creating C2 directory..."
mkdir -p /opt/c2-bot
cd /opt/c2-bot

# Download bot worker (if not exists)
if [ ! -f "bot_worker_auto.py" ]; then
    echo "📥 Downloading bot worker..."
    # You can upload this file manually or download from your repository
    echo "⚠️  Please upload bot_worker_auto.py to /opt/c2-bot/"
fi

# Test connection to Windows
echo "🔍 Testing connection to Windows C2 Server..."
if curl -s http://{windows_ip}:{windows_port}/api/bots > /dev/null; then
    echo "✅ Connection to Windows C2 Server successful!"
else
    echo "❌ Cannot connect to Windows C2 Server"
    echo "💡 Check if:"
    echo "   1. Windows C2 Server is running"
    echo "   2. Windows firewall allows port {windows_port}"
    echo "   3. Windows is accessible from VPS"
    exit 1
fi

# Start bot worker
echo "🚀 Starting Bot Worker..."
python3 bot_worker_auto.py --server http://{windows_ip}:{windows_port}

echo "🤖 Bot Worker setup completed!"
"""
    
    # Lưu script
    script_path = "vps_bot_worker_setup.sh"
    with open(script_path, "w") as f:
        f.write(bash_script)
    
    print(f"   📝 VPS bot worker script created: {script_path}")
    print(f"   💡 Upload and run this script on your VPS:")
    print(f"      scp {script_path} root@{vps_ip}:/tmp/")
    print(f"      ssh root@{vps_ip} 'chmod +x /tmp/{script_path} && /tmp/{script_path}'")

def create_windows_setup_guide(windows_ip, windows_port):
    """Tạo hướng dẫn setup Windows"""
    print(f"\n📋 Windows Setup Guide - Hướng dẫn setup Windows:")
    print("=" * 60)
    
    guide = f"""
🚀 **Setup C2 Server trên Windows Local**

### **Bước 1: Mở PowerShell với quyền Administrator**
```
Click chuột phải vào PowerShell → "Run as Administrator"
```

### **Bước 2: Chạy script firewall**
```powershell
# Chạy script firewall
powershell -ExecutionPolicy Bypass -File windows_firewall_setup.ps1
```

### **Bước 3: Khởi động C2 Server**
```cmd
# Terminal 1: Khởi động C2 Server
python c2_server_auto.py
```

### **Bước 4: Test kết nối local**
```cmd
# Test từ Windows local
curl http://localhost:{windows_port}/api/bots
```

### **Bước 5: Test kết nối từ VPS**
```bash
# Test từ VPS (Google Cloud)
curl http://{windows_ip}:{windows_port}/api/bots
```

### **Bước 6: Khởi động Bot Worker trên VPS**
```bash
# Trên VPS
python3 bot_worker_auto.py --server http://{windows_ip}:{windows_port}
```

### **🌐 URLs:**
- **Windows Local**: http://localhost:{windows_port}
- **Windows Network**: http://{windows_ip}:{windows_port}
- **VPS Bot**: http://{windows_ip}:{windows_port}

### **⚠️ Lưu ý quan trọng:**
1. **Windows Firewall** phải allow port {windows_port}
2. **C2 Server phải bind** trên 0.0.0.0:{windows_port}
3. **Windows và VPS** phải cùng network hoặc accessible
4. **Port forwarding** có thể cần thiết nếu Windows ở sau router
"""
    
    # Lưu guide
    guide_path = f"WINDOWS_SETUP_GUIDE_{windows_ip}.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"   📝 Windows setup guide created: {guide_path}")
    print(f"   💡 Follow this guide to setup Windows")

def show_quick_fix(windows_ip, windows_port):
    """Hiển thị quick fix"""
    print(f"\n🔧 Quick Fix - Sửa lỗi nhanh:")
    print("=" * 50)
    
    print("1. 🚀 **Trên Windows (Local):**")
    print("   # Mở PowerShell với quyền Administrator")
    print("   # Chạy script firewall")
    print("   powershell -ExecutionPolicy Bypass -File windows_firewall_setup.ps1")
    print("")
    print("   # Khởi động C2 Server")
    print("   python c2_server_auto.py")
    print("")
    
    print("2. 🤖 **Trên VPS (Google Cloud):**")
    print("   # Kết nối bot worker")
    print(f"   python3 bot_worker_auto.py --server http://{windows_ip}:{windows_port}")
    print("")
    
    print("3. 🔍 **Test kết nối:**")
    print("   # Test từ VPS")
    print(f"   curl http://{windows_ip}:{windows_port}/api/bots")
    print("")

def test_current_connection(windows_ip, windows_port):
    """Test kết nối hiện tại"""
    print(f"\n🔍 Testing Current Connection...")
    
    try:
        response = requests.get(f"http://{windows_ip}:{windows_port}/api/bots", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Windows C2 Server accessible from current location")
            return True
        else:
            print(f"   ❌ Windows C2 Server error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to Windows C2 Server: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Fix VPS to Windows Connection - Bot Worker trên Google Cloud VPS → C2 Server trên Windows Local")
    print("=" * 80)
    
    # Lấy thông tin network
    network_info = get_network_info()
    
    print(f"\n📍 Network Configuration:")
    print(f"   🏠 Windows Local: {network_info['windows_ip']}:{network_info['windows_port']}")
    print(f"   🌐 Google Cloud VPS: {network_info['vps_ip']}")
    print(f"   📍 Current Location: {network_info['current_public_ip']}")
    
    # Kiểm tra kết nối Windows
    if not check_windows_connectivity(network_info['windows_ip'], network_info['windows_port']):
        print(f"\n❌ Windows C2 Server {network_info['windows_ip']}:{network_info['windows_port']} không accessible!")
        print("💡 Hãy kiểm tra:")
        print("   1. Windows C2 Server có đang chạy không")
        print("   2. Windows firewall có chặn port không")
        print("   3. Windows có accessible từ network không")
        
        # Tạo scripts và guides
        create_windows_firewall_script(network_info['windows_ip'], network_info['windows_port'])
        create_vps_bot_worker_script(network_info['windows_ip'], network_info['windows_port'], network_info['vps_ip'])
        create_windows_setup_guide(network_info['windows_ip'], network_info['windows_port'])
        
        # Hiển thị quick fix
        show_quick_fix(network_info['windows_ip'], network_info['windows_port'])
        
        return
    
    # Test kết nối hiện tại
    if test_current_connection(network_info['windows_ip'], network_info['windows_port']):
        print(f"\n🎉 Windows C2 Server accessible!")
        print(f"📍 Windows: {network_info['windows_ip']}:{network_info['windows_port']}")
        print(f"🌐 Web UI: http://{network_info['windows_ip']}:{network_info['windows_port']}")
        
        # Tạo scripts cho VPS
        create_vps_bot_worker_script(network_info['windows_ip'], network_info['windows_port'], network_info['vps_ip'])
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Upload bot_worker_auto.py to VPS")
        print(f"   2. Run vps_bot_worker_setup.sh on VPS")
        print(f"   3. Bot worker sẽ kết nối đến Windows C2 Server")
        
    else:
        print(f"\n❌ Windows C2 Server không accessible từ vị trí hiện tại")
        print("💡 Hãy setup Windows trước")

if __name__ == "__main__":
    main()
