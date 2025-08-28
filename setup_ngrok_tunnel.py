#!/usr/bin/env python3
"""
Setup Ngrok Tunnel - Giải pháp nhanh để VPS kết nối Windows C2 Server
"""
import os
import sys
import subprocess
import platform
import time
import requests
import json

def download_ngrok():
    """Download ngrok"""
    print("📥 Downloading Ngrok...")
    
    if platform.system() == "Windows":
        download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        filename = "ngrok-windows.zip"
    else:
        download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        filename = "ngrok-linux.tgz"
    
    print(f"   🌐 Download URL: {download_url}")
    print(f"   📁 Filename: {filename}")
    
    # Tạo script download
    if platform.system() == "Windows":
        download_script = f"""@echo off
echo Downloading ngrok...
powershell -Command "Invoke-WebRequest -Uri '{download_url}' -OutFile '{filename}'"
echo Download completed!
echo Extracting...
powershell -Command "Expand-Archive -Path '{filename}' -DestinationPath '.' -Force"
echo Ngrok ready to use!
"""
        script_path = "download_ngrok.bat"
    else:
        download_script = f"""#!/bin/bash
echo "Downloading ngrok..."
curl -L {download_url} -o {filename}
echo "Download completed!"
echo "Extracting..."
tar -xzf {filename}
echo "Ngrok ready to use!"
"""
        script_path = "download_ngrok.sh"
    
    with open(script_path, "w") as f:
        f.write(download_script)
    
    print(f"   📝 Download script created: {script_path}")
    return script_path

def create_ngrok_setup_guide():
    """Tạo hướng dẫn setup ngrok"""
    print("\n📋 Ngrok Setup Guide - Hướng dẫn setup ngrok:")
    print("=" * 60)
    
    guide = """
🚀 **Setup Ngrok Tunnel để VPS kết nối Windows**

### **Bước 1: Download và cài đặt ngrok**
```bash
# Windows
download_ngrok.bat

# Linux/Mac
chmod +x download_ngrok.sh
./download_ngrok.sh
```

### **Bước 2: Đăng ký tài khoản ngrok (miễn phí)**
```
1. Truy cập: https://ngrok.com/signup
2. Tạo tài khoản miễn phí
3. Lấy authtoken từ dashboard
```

### **Bước 3: Cấu hình ngrok**
```bash
# Thêm authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE

# Test ngrok
ngrok version
```

### **Bước 4: Tạo tunnel đến C2 Server**
```bash
# Trên Windows, mở terminal mới
ngrok http 5000

# Kết quả sẽ hiển thị:
# Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```

### **Bước 5: Sử dụng URL ngrok trên VPS**
```bash
# Trên VPS, kết nối bot worker
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

### **🌐 URLs sau khi setup:**
- **Windows Local**: http://localhost:5000
- **Ngrok Public**: https://abc123.ngrok.io
- **VPS Bot**: https://abc123.ngrok.io

### **⚠️ Lưu ý quan trọng:**
1. **Ngrok miễn phí** có giới hạn 1 tunnel
2. **URL ngrok thay đổi** mỗi lần restart
3. **C2 Server phải chạy** trước khi tạo tunnel
4. **Sử dụng HTTPS** URL từ ngrok
"""
    
    # Lưu guide
    guide_path = "NGROK_SETUP_GUIDE.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"   📝 Ngrok setup guide created: {guide_path}")

def create_ngrok_scripts():
    """Tạo scripts ngrok"""
    print("\n🤖 Creating Ngrok Scripts...")
    
    # Script khởi động ngrok trên Windows
    windows_script = """@echo off
echo Starting Ngrok Tunnel for C2 Server...
echo.
echo Make sure C2 Server is running on port 5000 first!
echo.
echo Starting ngrok...
ngrok http 5000
echo.
echo Ngrok tunnel stopped.
pause
"""
    
    with open("start_ngrok_windows.bat", "w") as f:
        f.write(windows_script)
    
    # Script test ngrok từ VPS
    vps_test_script = """#!/bin/bash
# Test Ngrok Tunnel from VPS
# Run this on your VPS

echo "🔍 Testing Ngrok Tunnel..."
echo "=========================="

# Get ngrok URL from user
read -p "Enter ngrok URL (e.g., https://abc123.ngrok.io): " NGROK_URL

if [ -z "$NGROK_URL" ]; then
    echo "❌ No URL provided"
    exit 1
fi

echo "🌐 Testing connection to: $NGROK_URL"

# Test connection
if curl -s --connect-timeout 10 "$NGROK_URL/api/bots" > /dev/null; then
    echo "✅ Ngrok tunnel is working!"
    echo "🌐 C2 Server accessible via: $NGROK_URL"
    echo ""
    echo "🤖 Now you can start bot worker:"
    echo "python3 bot_worker_auto.py --server $NGROK_URL"
else
    echo "❌ Ngrok tunnel not accessible"
    echo "💡 Check if:"
    echo "   1. Ngrok is running on Windows"
    echo "   2. C2 Server is running on port 5000"
    echo "   3. URL is correct"
fi
"""
    
    with open("test_ngrok_from_vps.sh", "w") as f:
        f.write(vps_test_script)
    
    print("   📝 Ngrok scripts created:")
    print("      - start_ngrok_windows.bat (Windows)")
    print("      - test_ngrok_from_vps.sh (VPS)")

def create_quick_fix():
    """Tạo quick fix"""
    print("\n🔧 Quick Fix with Ngrok - Sửa lỗi nhanh:")
    print("=" * 50)
    
    quick_fix = """
🚀 **Quick Fix với Ngrok (5 phút):**

### **Trên Windows:**
1. **Download ngrok:**
   ```
   download_ngrok.bat
   ```

2. **Khởi động C2 Server:**
   ```
   python c2_server_auto.py
   ```

3. **Tạo ngrok tunnel:**
   ```
   start_ngrok_windows.bat
   ```

4. **Copy URL ngrok** (ví dụ: https://abc123.ngrok.io)

### **Trên VPS:**
1. **Test ngrok tunnel:**
   ```
   chmod +x test_ngrok_from_vps.sh
   ./test_ngrok_from_vps.sh
   ```

2. **Kết nối bot worker:**
   ```
   python3 bot_worker_auto.py --server https://abc123.ngrok.io
   ```

### **🎉 Kết quả:**
- Bot worker trên VPS sẽ kết nối thành công đến Windows C2 Server
- Không cần port forwarding
- Không cần quyền router
- Hoạt động ngay lập tức
"""
    
    # Lưu quick fix
    quick_fix_path = "NGROK_QUICK_FIX.md"
    with open(quick_fix_path, "w") as f:
        f.write(quick_fix)
    
    print(f"   📝 Quick fix guide created: {quick_fix_path}")

def show_immediate_steps():
    """Hiển thị các bước ngay lập tức"""
    print("\n🚀 Immediate Steps - Các bước ngay lập tức:")
    print("=" * 50)
    
    print("1. 📥 **Download ngrok trên Windows:**")
    print("   download_ngrok.bat")
    
    print("\n2. 🚀 **Khởi động C2 Server trên Windows:**")
    print("   python c2_server_auto.py")
    
    print("\n3. 🌐 **Tạo ngrok tunnel trên Windows:**")
    print("   start_ngrok_windows.bat")
    
    print("\n4. 📋 **Copy URL ngrok** (https://abc123.ngrok.io)")
    
    print("\n5. 🤖 **Kết nối bot worker trên VPS:**")
    print("   python3 bot_worker_auto.py --server https://abc123.ngrok.io")
    
    print("\n💡 **Ưu điểm của ngrok:**")
    print("   ✅ Không cần port forwarding")
    print("   ✅ Không cần quyền router")
    print("   ✅ Hoạt động ngay lập tức")
    print("   ✅ Tự động HTTPS")
    print("   ⚠️  URL thay đổi mỗi lần restart")

def main():
    """Main function"""
    print("🚀 Setup Ngrok Tunnel - Giải pháp nhanh VPS kết nối Windows")
    print("=" * 70)
    
    # Download ngrok
    download_script = download_ngrok()
    
    # Tạo guides và scripts
    create_ngrok_setup_guide()
    create_ngrok_scripts()
    create_quick_fix()
    
    # Hiển thị immediate steps
    show_immediate_steps()
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Chạy {download_script} trên Windows")
    print(f"   2. Khởi động C2 Server")
    print(f"   3. Tạo ngrok tunnel")
    print(f"   4. Kết nối bot worker từ VPS")
    
    print(f"\n🎯 **Kết quả mong đợi:**")
    print(f"   Bot worker trên VPS sẽ kết nối thành công đến Windows C2 Server!")
    print(f"   Không cần port forwarding, hoạt động ngay lập tức!")

if __name__ == "__main__":
    main()
