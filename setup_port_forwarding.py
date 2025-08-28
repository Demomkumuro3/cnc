#!/usr/bin/env python3
"""
Setup Port Forwarding - Để VPS có thể kết nối đến Windows C2 Server
"""
import os
import sys
import subprocess
import platform
import time
import requests
import socket

def get_public_ip():
    """Lấy public IP của Windows"""
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        return response.text
    except:
        return None

def check_router_access():
    """Kiểm tra quyền truy cập router"""
    print("🔍 Checking Router Access...")
    
    # Kiểm tra các IP router phổ biến
    common_routers = [
        "192.168.1.1", "192.168.0.1", "192.168.2.1",
        "10.0.0.1", "10.0.1.1", "172.16.0.1"
    ]
    
    accessible_routers = []
    for router_ip in common_routers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((router_ip, 80))
            sock.close()
            
            if result == 0:
                accessible_routers.append(router_ip)
                print(f"   ✅ Router accessible: {router_ip}")
        except:
            pass
    
    return accessible_routers

def create_port_forwarding_guide():
    """Tạo hướng dẫn port forwarding"""
    print("\n📋 Port Forwarding Guide - Hướng dẫn mở port:")
    print("=" * 60)
    
    guide = """
🚀 **Setup Port Forwarding để VPS kết nối Windows**

### **Bước 1: Tìm Router IP**
```cmd
# Trên Windows, mở Command Prompt
ipconfig | findstr "Default Gateway"
```

### **Bước 2: Truy cập Router**
```
Mở trình duyệt và truy cập: http://192.168.1.1
Username: admin (hoặc để trống)
Password: admin, password, hoặc để trống
```

### **Bước 3: Tìm Port Forwarding**
```
Tìm menu: Port Forwarding, Virtual Server, hoặc NAT
Thường ở: Advanced → Port Forwarding
```

### **Bước 4: Thêm Port Forwarding Rule**
```
Service Name: C2 Server
Protocol: TCP
External Port: 5000
Internal Port: 5000
Internal IP: 192.168.1.5 (IP của Windows)
Status: Enabled
```

### **Bước 5: Lưu và Test**
```
Click Save/Apply
Test từ VPS: curl http://<PUBLIC_IP>:5000/api/bots
```

### **🌐 URLs sau khi setup:**
- **Windows Local**: http://192.168.1.5:5000
- **Windows Public**: http://<PUBLIC_IP>:5000
- **VPS Bot**: http://<PUBLIC_IP>:5000

### **⚠️ Lưu ý quan trọng:**
1. **Router phải hỗ trợ** port forwarding
2. **Windows IP** phải là static IP
3. **Firewall** phải allow port 5000
4. **C2 Server** phải bind trên 0.0.0.0:5000
"""
    
    # Lưu guide
    guide_path = "PORT_FORWARDING_GUIDE.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"   📝 Port forwarding guide created: {guide_path}")

def create_alternative_solutions():
    """Tạo giải pháp thay thế"""
    print("\n🔧 Alternative Solutions - Giải pháp thay thế:")
    print("=" * 60)
    
    solutions = """
💡 **Giải pháp thay thế nếu Port Forwarding không khả thi:**

### **Giải pháp 1: Ngrok Tunnel**
```bash
# Trên Windows, cài đặt ngrok
# Download từ: https://ngrok.com/download

# Tạo tunnel
ngrok http 5000

# Sử dụng URL ngrok trên VPS
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

### **Giải pháp 2: Cloudflare Tunnel**
```bash
# Cài đặt cloudflared
# Tạo tunnel đến localhost:5000
# Sử dụng tunnel URL trên VPS
```

### **Giải pháp 3: Reverse SSH Tunnel**
```bash
# Trên Windows (cần SSH server)
ssh -R 5000:localhost:5000 user@<VPS_IP>

# Trên VPS
python3 bot_worker_auto.py --server http://localhost:5000
```

### **Giải pháp 4: VPN Connection**
```bash
# Tạo VPN giữa VPS và Windows
# Sử dụng IP VPN thay vì public IP
```

### **Giải pháp 5: Public IP của Windows**
```bash
# Kiểm tra xem Windows có public IP không
# Nếu có, sử dụng trực tiếp public IP
```
"""
    
    # Lưu solutions
    solutions_path = "ALTERNATIVE_SOLUTIONS.md"
    with open(solutions_path, "w") as f:
        f.write(solutions)
    
    print(f"   📝 Alternative solutions created: {solutions_path}")

def create_quick_test_script():
    """Tạo script test nhanh"""
    print("\n🔍 Creating Quick Test Script...")
    
    test_script = """#!/bin/bash
# Quick Test Script for VPS to Windows Connection
# Run this on your VPS

echo "🔍 Quick Test: VPS to Windows Connection"
echo "=========================================="

# Get Windows public IP (if accessible)
echo "🌐 Getting Windows public IP..."
WINDOWS_PUBLIC_IP=$(curl -s https://api.ipify.org)
echo "   Windows Public IP: $WINDOWS_PUBLIC_IP"

# Test connection to Windows public IP
echo "🔌 Testing connection to Windows public IP..."
if curl -s --connect-timeout 10 http://$WINDOWS_PUBLIC_IP:5000/api/bots > /dev/null; then
    echo "   ✅ Windows C2 Server accessible via public IP!"
    echo "   🌐 Use this URL on VPS:"
    echo "      python3 bot_worker_auto.py --server http://$WINDOWS_PUBLIC_IP:5000"
else
    echo "   ❌ Windows C2 Server not accessible via public IP"
    echo "   💡 Try port forwarding or alternative solutions"
fi

# Test local Windows IP (will likely fail)
echo "🏠 Testing connection to local Windows IP..."
if curl -s --connect-timeout 10 http://192.168.1.5:5000/api/bots > /dev/null; then
    echo "   ✅ Windows C2 Server accessible via local IP!"
else
    echo "   ❌ Windows C2 Server not accessible via local IP (expected)"
    echo "   💡 This is normal - VPS cannot access local network IPs"
fi

echo "🔍 Test completed!"
"""
    
    # Lưu script
    script_path = "quick_test_vps_to_windows.sh"
    with open(script_path, "w") as f:
        f.write(test_script)
    
    print(f"   📝 Quick test script created: {script_path}")
    print(f"   💡 Upload and run on VPS:")
    print(f"      scp {script_path} root@<VPS_IP>:/tmp/")
    print(f"      ssh root@<VPS_IP> 'chmod +x /tmp/{script_path} && /tmp/{script_path}'")

def show_immediate_fix():
    """Hiển thị fix ngay lập tức"""
    print("\n🚀 Immediate Fix - Sửa lỗi ngay:")
    print("=" * 50)
    
    print("1. 🌐 **Kiểm tra Public IP của Windows:**")
    print("   # Trên Windows, mở trình duyệt")
    print("   # Truy cập: https://whatismyipaddress.com")
    print("   # Ghi nhớ public IP")
    
    print("\n2. 🔌 **Test kết nối từ VPS:**")
    print("   # Trên VPS, test public IP")
    print("   curl http://<WINDOWS_PUBLIC_IP>:5000/api/bots")
    
    print("\n3. 🤖 **Kết nối Bot Worker:**")
    print("   # Nếu public IP accessible:")
    print("   python3 bot_worker_auto.py --server http://<WINDOWS_PUBLIC_IP>:5000")
    
    print("\n4. 🛡️ **Nếu public IP không accessible:**")
    print("   # Setup port forwarding trên router")
    print("   # Hoặc sử dụng ngrok tunnel")

def main():
    """Main function"""
    print("🚀 Setup Port Forwarding - VPS kết nối Windows C2 Server")
    print("=" * 70)
    
    # Lấy public IP của Windows
    print("🔍 Getting Windows Public IP...")
    windows_public_ip = get_public_ip()
    
    if windows_public_ip:
        print(f"   🌐 Windows Public IP: {windows_public_ip}")
        print(f"   💡 Test từ VPS: curl http://{windows_public_ip}:5000/api/bots")
    else:
        print("   ❌ Cannot get Windows public IP")
    
    # Kiểm tra router access
    print("\n🔍 Checking Router Access...")
    accessible_routers = check_router_access()
    
    if accessible_routers:
        print(f"   ✅ Routers accessible: {', '.join(accessible_routers)}")
        print(f"   💡 Setup port forwarding on: http://{accessible_routers[0]}")
    else:
        print("   ❌ No routers accessible")
    
    # Tạo guides và scripts
    create_port_forwarding_guide()
    create_alternative_solutions()
    create_quick_test_script()
    
    # Hiển thị immediate fix
    show_immediate_fix()
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Test Windows public IP từ VPS")
    print(f"   2. Setup port forwarding nếu cần")
    print(f"   3. Sử dụng ngrok nếu không có quyền router")
    print(f"   4. Test kết nối và kết nối bot worker")

if __name__ == "__main__":
    main()
