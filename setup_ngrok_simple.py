#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Ngrok - Cách đơn giản nhất để VPS kết nối Windows
"""
import os
import platform
import requests

def create_ngrok_download():
    """Tạo script download ngrok"""
    print("Creating Ngrok Download Script...")
    
    if platform.system() == "Windows":
        script = """@echo off
echo Downloading ngrok...
echo.

REM Download ngrok
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo Download completed!
echo.

REM Extract ngrok
echo Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo.
echo Ngrok ready to use!
echo.
echo Next steps:
echo 1. Sign up at https://ngrok.com/signup
echo 2. Get your authtoken from dashboard
echo 3. Run: ngrok config add-authtoken YOUR_TOKEN
echo 4. Run: ngrok http 5000
echo.
pause
"""
        filename = "download_ngrok.bat"
    else:
        script = """#!/bin/bash
echo "Downloading ngrok..."
echo ""

# Download ngrok
curl -L https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz

echo "Download completed!"
echo ""

# Extract ngrok
echo "Extracting ngrok..."
tar -xzf ngrok.tgz

echo ""
echo "Ngrok ready to use!"
echo ""
echo "Next steps:"
echo "1. Sign up at https://ngrok.com/signup"
echo "2. Get your authtoken from dashboard"
echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
echo "4. Run: ngrok http 5000"
echo ""
"""
        filename = "download_ngrok.sh"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(script)
    
    print(f"   Ngrok download script created: {filename}")

def create_ngrok_start():
    """Tạo script khởi động ngrok"""
    print("Creating Ngrok Start Script...")
    
    if platform.system() == "Windows":
        script = """@echo off
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
        filename = "start_ngrok.bat"
    else:
        script = """#!/bin/bash
echo "Starting Ngrok Tunnel for C2 Server..."
echo ""
echo "Make sure C2 Server is running on port 5000 first!"
echo ""
echo "Starting ngrok..."
ngrok http 5000
echo ""
echo "Ngrok tunnel stopped."
"""
        filename = "start_ngrok.sh"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(script)
    
    print(f"   Ngrok start script created: {filename}")

def create_vps_ngrok_test():
    """Tạo script test ngrok từ VPS"""
    print("Creating VPS Ngrok Test Script...")
    
    script = """#!/bin/bash
# Test Ngrok Tunnel from VPS
# Run this on your VPS

echo "Testing Ngrok Tunnel..."
echo "========================"

# Get ngrok URL from user
read -p "Enter ngrok URL (e.g., https://abc123.ngrok.io): " NGROK_URL

if [ -z "$NGROK_URL" ]; then
    echo "No URL provided"
    exit 1
fi

echo "Testing connection to: $NGROK_URL"

# Test connection
if curl -s --connect-timeout 10 "$NGROK_URL/api/bots" > /dev/null; then
    echo "Ngrok tunnel is working!"
    echo "C2 Server accessible via: $NGROK_URL"
    echo ""
    echo "Now you can start bot worker:"
    echo "python3 bot_worker_auto.py --server $NGROK_URL"
else
    echo "Ngrok tunnel not accessible"
    echo "Check if:"
    echo "1. Ngrok is running on Windows"
    echo "2. C2 Server is running on port 5000"
    echo "3. URL is correct"
fi
"""
    
    with open("test_ngrok_from_vps.sh", "w", encoding='utf-8') as f:
        f.write(script)
    
    print("   VPS ngrok test script created: test_ngrok_from_vps.sh")

def create_ngrok_guide():
    """Tạo hướng dẫn ngrok"""
    print("Creating Ngrok Guide...")
    
    guide = """
NGROK TUNNEL - Cach don gian nhat de VPS ket noi Windows

Buoc 1: Download ngrok
# Windows
download_ngrok.bat

# Linux/Mac
chmod +x download_ngrok.sh
./download_ngrok.sh

Buoc 2: Dang ky tai khoan ngrok (mien phi)
1. Truy cap: https://ngrok.com/signup
2. Tao tai khoan mien phi
3. Lay authtoken tu dashboard

Buoc 3: Cau hinh ngrok
# Them authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE

# Test ngrok
ngrok version

Buoc 4: Tao tunnel den C2 Server
# Tren Windows, mo terminal moi
start_ngrok.bat

# Ket qua se hien thi:
# Forwarding    https://abc123.ngrok.io -> http://localhost:5000

Buoc 5: Su dung URL ngrok tren VPS
# Tren VPS, ket noi bot worker
python3 bot_worker_auto.py --server https://abc123.ngrok.io

Uu diem:
- Khong can mo port Windows
- Khong can quyen router
- Hoat dong ngay lap tuc
- Tu dong HTTPS

Nhuoc diem:
- URL thay doi moi lan restart
- Gioi han 1 tunnel (mien phi)
"""
    
    with open("NGROK_GUIDE.md", "w", encoding='utf-8') as f:
        f.write(guide)
    
    print("   Ngrok guide created: NGROK_GUIDE.md")

def main():
    """Main function"""
    print("Setup Ngrok - Cach don gian nhat de VPS ket noi Windows")
    print("=" * 70)
    
    # Tạo scripts
    create_ngrok_download()
    create_ngrok_start()
    create_vps_ngrok_test()
    create_ngrok_guide()
    
    print("\nNgrok setup completed!")
    print("\nNext Steps:")
    print("1. Chay download_ngrok.bat de tai ngrok")
    print("2. Dang ky tai khoan tai https://ngrok.com/signup")
    print("3. Lay authtoken va cau hinh: ngrok config add-authtoken YOUR_TOKEN")
    print("4. Khoi dong C2 Server: python c2_server_auto.py")
    print("5. Tao ngrok tunnel: start_ngrok.bat")
    print("6. Copy URL ngrok va su dung tren VPS")
    
    print("\nKet qua mong doi:")
    print("Bot worker tren VPS se ket noi thanh cong den Windows C2 Server!")
    print("Khong can mo port, khong can quyen router!")

if __name__ == "__main__":
    main()
