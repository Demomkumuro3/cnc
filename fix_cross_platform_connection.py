#!/usr/bin/env python3
"""
Fix Cross-Platform Connection - Bot Worker trên Codespaces kết nối đến C2 Server trên Google Cloud VPS
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
    
    # Lấy IP public của Codespaces
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        codespaces_public_ip = response.text
        print(f"   🌐 Codespaces Public IP: {codespaces_public_ip}")
    except:
        codespaces_public_ip = "unknown"
        print("   ❌ Cannot get Codespaces public IP")
    
    # Lấy IP local của Codespaces
    try:
        hostname = socket.gethostname()
        codespaces_local_ip = socket.gethostbyname(hostname)
        print(f"   🏠 Codespaces Local IP: {codespaces_local_ip}")
    except:
        codespaces_local_ip = "127.0.0.1"
        print("   ❌ Cannot get Codespaces local IP")
    
    # Lấy thông tin VPS
    vps_ip = input("🌐 Nhập IP của Google Cloud VPS: ").strip()
    vps_port = input("🔌 Nhập port của C2 Server (mặc định 5000): ").strip() or "5000"
    
    return {
        'codespaces_public_ip': codespaces_public_ip,
        'codespaces_local_ip': codespaces_local_ip,
        'vps_ip': vps_ip,
        'vps_port': vps_port
    }

def check_vps_connectivity(vps_ip, vps_port):
    """Kiểm tra kết nối đến VPS"""
    print(f"\n🔌 Testing VPS Connection...")
    print(f"🎯 Target: {vps_ip}:{vps_port}")
    
    # Test ping
    print("🏓 Testing ping...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["ping", "-n", "1", vps_ip], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(["ping", "-c", "1", vps_ip], 
                                  capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Ping successful")
        else:
            print("   ❌ Ping failed")
    except:
        print("   ❌ Ping test failed")
    
    # Test port
    print(f"🔌 Testing port {vps_port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((vps_ip, int(vps_port)))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port {vps_port} is open")
        else:
            print(f"   ❌ Port {vps_port} is closed")
            return False
    except Exception as e:
        print(f"   ❌ Port test failed: {e}")
        return False
    
    # Test HTTP connection
    print(f"🌐 Testing HTTP connection...")
    try:
        response = requests.get(f"http://{vps_ip}:{vps_port}/api/bots", timeout=10)
        if response.status_code == 200:
            print("   ✅ HTTP connection successful")
            return True
        else:
            print(f"   ❌ HTTP status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ HTTP test failed: {e}")
        return False

def setup_firewall_bypass(vps_ip, vps_port):
    """Setup firewall bypass cho VPS"""
    print(f"\n🛡️ Setting up Firewall Bypass for VPS...")
    
    # Tạo script firewall bypass
    firewall_script = f"""#!/bin/bash
# Firewall Bypass Script for Google Cloud VPS
# Run this on your VPS with root privileges

echo "🛡️ Setting up firewall bypass for C2 Server..."

# Allow port {vps_port}
if command -v ufw &> /dev/null; then
    echo "🔧 Using UFW firewall..."
    ufw allow {vps_port}/tcp
    ufw reload
elif command -v firewall-cmd &> /dev/null; then
    echo "🔧 Using firewalld..."
    firewall-cmd --permanent --add-port={vps_port}/tcp
    firewall-cmd --reload
elif command -v iptables &> /dev/null; then
    echo "🔧 Using iptables..."
    iptables -A INPUT -p tcp --dport {vps_port} -j ACCEPT
    iptables-save > /etc/iptables/rules.v4
else
    echo "❌ No firewall manager found"
fi

# Check if port is open
echo "🔍 Checking if port {vps_port} is open..."
if netstat -tuln | grep ":{vps_port} "; then
    echo "✅ Port {vps_port} is now open"
else
    echo "❌ Port {vps_port} is still closed"
fi

echo "🛡️ Firewall setup completed!"
"""
    
    # Lưu script
    script_path = "firewall_bypass_vps.sh"
    with open(script_path, "w") as f:
        f.write(firewall_script)
    
    print(f"   📝 Firewall bypass script created: {script_path}")
    print(f"   💡 Upload and run this script on your VPS:")
    print(f"      scp {script_path} root@{vps_ip}:/tmp/")
    print(f"      ssh root@{vps_ip} 'chmod +x /tmp/{script_path} && /tmp/{script_path}'")

def test_bot_worker_connection(vps_ip, vps_port):
    """Test kết nối bot worker đến VPS"""
    print(f"\n🤖 Testing Bot Worker Connection to VPS...")
    
    # Test kết nối trước
    try:
        response = requests.get(f"http://{vps_ip}:{vps_port}/api/bots", timeout=10)
        if response.status_code != 200:
            print(f"   ❌ VPS not accessible: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ VPS not accessible: {e}")
        return False
    
    # Khởi động bot worker
    print(f"   🚀 Starting bot worker with VPS: {vps_ip}:{vps_port}")
    try:
        process = subprocess.Popen([
            sys.executable, "bot_worker_auto.py",
            "--server", f"http://{vps_ip}:{vps_port}"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đợi kết nối
        time.sleep(10)
        
        if process.poll() is None:
            print("   ✅ Bot Worker started successfully")
            print(f"   🌐 Connected to VPS: {vps_ip}:{vps_port}")
            return process
        else:
            stdout, stderr = process.communicate()
            if "Successfully registered" in stdout:
                print("   ✅ Bot Worker connected successfully to VPS!")
                return True
            else:
                print("   ❌ Bot Worker failed to connect to VPS")
                print(f"   📝 Error: {stderr[:300]}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error starting bot worker: {e}")
        return False

def create_vps_setup_guide(vps_ip, vps_port):
    """Tạo hướng dẫn setup VPS"""
    print(f"\n📋 VPS Setup Guide - Hướng dẫn setup VPS:")
    print("=" * 60)
    
    guide = f"""
🚀 **Setup C2 Server trên Google Cloud VPS**

### **Bước 1: Kết nối đến VPS**
```bash
ssh root@{vps_ip}
```

### **Bước 2: Cài đặt dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Python và pip
apt install -y python3 python3-pip

# Install required packages
pip3 install flask flask-socketio psutil requests
```

### **Bước 3: Upload C2 Server files**
```bash
# Tạo thư mục
mkdir -p /opt/c2-server
cd /opt/c2-server

# Upload files từ máy local
scp c2_server_auto.py root@{vps_ip}:/opt/c2-server/
scp requirements.txt root@{vps_ip}:/opt/c2-server/
```

### **Bước 4: Setup firewall**
```bash
# Chạy script firewall bypass
chmod +x firewall_bypass_vps.sh
./firewall_bypass_vps.sh
```

### **Bước 5: Khởi động C2 Server**
```bash
cd /opt/c2-server
python3 c2_server_auto.py
```

### **Bước 6: Test kết nối**
```bash
# Test từ VPS
curl http://localhost:{vps_port}/api/bots

# Test từ Codespaces
curl http://{vps_ip}:{vps_port}/api/bots
```

### **Bước 7: Kết nối Bot Worker từ Codespaces**
```bash
python3 bot_worker_auto.py --server http://{vps_ip}:{vps_port}
```

### **🌐 URLs:**
- **VPS Local**: http://localhost:{vps_port}
- **VPS Public**: http://{vps_ip}:{vps_port}
- **Codespaces Bot**: http://{vps_ip}:{vps_port}

### **⚠️ Lưu ý quan trọng:**
1. **VPS phải có public IP** và port {vps_port} mở
2. **Firewall phải allow** port {vps_port}
3. **C2 Server phải bind** trên 0.0.0.0:{vps_port}
4. **Google Cloud VPC rules** phải allow port {vps_port}
"""
    
    # Lưu guide
    guide_path = f"VPS_SETUP_GUIDE_{vps_ip}.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"   📝 VPS setup guide created: {guide_path}")
    print(f"   💡 Follow this guide to setup your VPS")

def show_quick_fix():
    """Hiển thị quick fix"""
    print(f"\n🔧 Quick Fix - Sửa lỗi nhanh:")
    print("=" * 50)
    
    print("1. 🚀 **Trên VPS (Google Cloud):**")
    print("   # Mở port 5000")
    print("   ufw allow 5000/tcp")
    print("   ufw reload")
    print("")
    print("   # Khởi động C2 Server")
    print("   python3 c2_server_auto.py")
    print("")
    
    print("2. 🤖 **Trên Codespaces:**")
    print("   # Kết nối bot worker")
    print("   python3 bot_worker_auto.py --server http://<VPS_IP>:5000")
    print("")
    
    print("3. 🔍 **Test kết nối:**")
    print("   # Test từ Codespaces")
    print("   curl http://<VPS_IP>:5000/api/bots")
    print("")

def main():
    """Main function"""
    print("🚀 Fix Cross-Platform Connection - Bot Worker trên Codespaces → C2 Server trên Google Cloud VPS")
    print("=" * 80)
    
    # Kiểm tra OS
    if platform.system() != "Linux":
        print("❌ This script is designed for Linux (Codespaces)")
        print("💡 For Windows, use: python c2_server_auto.py")
        return
    
    # Lấy thông tin network
    network_info = get_network_info()
    
    # Kiểm tra kết nối VPS
    if not check_vps_connectivity(network_info['vps_ip'], network_info['vps_port']):
        print(f"\n❌ VPS {network_info['vps_ip']}:{network_info['vps_port']} không accessible!")
        print("💡 Hãy kiểm tra:")
        print("   1. VPS có đang chạy không")
        print("   2. Port có mở không")
        print("   3. Firewall có chặn không")
        print("   4. Google Cloud VPC rules")
        
        # Tạo firewall bypass script
        setup_firewall_bypass(network_info['vps_ip'], network_info['vps_port'])
        
        # Tạo setup guide
        create_vps_setup_guide(network_info['vps_ip'], network_info['vps_port'])
        
        # Hiển thị quick fix
        show_quick_fix()
        
        return
    
    # Test bot worker connection
    bot_process = test_bot_worker_connection(network_info['vps_ip'], network_info['vps_port'])
    
    if bot_process:
        print(f"\n🎉 Bot Worker đã kết nối thành công đến VPS!")
        print(f"📍 VPS: {network_info['vps_ip']}:{network_info['vps_port']}")
        print(f"🌐 Web UI: http://{network_info['vps_ip']}:{network_info['vps_port']}")
        print(f"🤖 Bot ID: AutoBot-codespaces")
        
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
        print(f"\n❌ Không thể kết nối Bot Worker đến VPS")
        print("💡 Hãy kiểm tra VPS setup trước")

if __name__ == "__main__":
    main()
