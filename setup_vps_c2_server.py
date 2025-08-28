#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup C2 Server trên VPS - Cách thay thế cho Windows
"""
import os
import platform

def create_vps_c2_setup():
    """Tạo script setup C2 Server trên VPS"""
    print("Creating VPS C2 Server Setup Script...")
    
    script = """#!/bin/bash
# Setup C2 Server trên VPS (Google Cloud)
# Run this on your VPS

echo "Setting up C2 Server on VPS..."
echo "================================"

# Update system
echo "Updating system..."
apt update && apt upgrade -y

# Install Python and dependencies
echo "Installing Python and dependencies..."
apt install -y python3 python3-pip git

# Install Python packages
echo "Installing Python packages..."
pip3 install flask flask-socketio psutil requests

# Create directory
echo "Creating C2 directory..."
mkdir -p /opt/c2-server
cd /opt/c2-server

# Download C2 Server files
echo "Downloading C2 Server files..."
if [ ! -f "c2_server_auto.py" ]; then
    echo "Please upload c2_server_auto.py to /opt/c2-server/"
    echo "Or download from your repository"
fi

# Create startup script
echo "Creating startup script..."
cat > start_c2_server.sh << 'EOF'
#!/bin/bash
cd /opt/c2-server
python3 c2_server_auto.py
EOF

chmod +x start_c2_server.sh

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/c2-server.service << EOF
[Unit]
Description=C2 Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/c2-server
ExecStart=/opt/c2-server/start_c2_server.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "Enabling and starting C2 Server service..."
systemctl daemon-reload
systemctl enable c2-server
systemctl start c2-server

# Check status
echo "Checking C2 Server status..."
systemctl status c2-server

echo ""
echo "C2 Server setup completed!"
echo ""
echo "C2 Server is now running on: http://$(curl -s https://api.ipify.org):5000"
echo ""
echo "To manage C2 Server:"
echo "  Start:   systemctl start c2-server"
echo "  Stop:    systemctl stop c2-server"
echo "  Status:  systemctl status c2-server"
echo "  Logs:    journalctl -u c2-server -f"
echo ""
echo "Now you can connect bot workers to: http://$(curl -s https://api.ipify.org):5000"
"""
    
    with open("setup_vps_c2_server.sh", "w", encoding='utf-8') as f:
        f.write(script)
    
    print("   VPS C2 Server setup script created: setup_vps_c2_server.sh")

def create_windows_bot_worker():
    """Tạo script bot worker cho Windows"""
    print("Creating Windows Bot Worker Script...")
    
    script = """@echo off
echo Starting Bot Worker on Windows...
echo.

echo Bot Worker will connect to VPS C2 Server
echo.

REM Get VPS IP from user
set /p VPS_IP="Enter VPS IP address: "

if "%VPS_IP%"=="" (
    echo No IP provided
    pause
    exit /b 1
)

echo.
echo Connecting to VPS C2 Server: http://%VPS_IP%:5000
echo.

REM Start bot worker
python bot_worker_auto.py --server http://%VPS_IP%:5000

echo.
echo Bot Worker stopped.
pause
"""
    
    with open("start_bot_worker_windows.bat", "w", encoding='utf-8') as f:
        f.write(script)
    
    print("   Windows bot worker script created: start_bot_worker_windows.bat")

def create_vps_c2_guide():
    """Tạo hướng dẫn VPS C2 Server"""
    print("Creating VPS C2 Server Guide...")
    
    guide = """
VPS C2 SERVER - Cach thay the cho Windows

Buoc 1: Setup C2 Server tren VPS
# Tren VPS (Google Cloud)
chmod +x setup_vps_c2_server.sh
./setup_vps_c2_server.sh

Buoc 2: Kiem tra C2 Server
# Tren VPS
systemctl status c2-server
curl http://localhost:5000/api/bots

Buoc 3: Lay VPS IP
# Tren VPS
curl -s https://api.ipify.org

Buoc 4: Ket noi Bot Worker tu Windows
# Tren Windows
start_bot_worker_windows.bat
# Nhap VPS IP khi duoc yeu cau

Uu diem:
- Khong can mo port Windows
- Khong can firewall Windows
- C2 Server chay 24/7 tren VPS
- IP on dinh, khong thay doi
- Co the ket noi tu nhieu noi

Nhuoc diem:
- Can VPS (Google Cloud, AWS, etc.)
- Chi phi VPS
- Can upload file len VPS

Kien truc:
Windows Bot Worker -> VPS C2 Server
"""
    
    with open("VPS_C2_SERVER_GUIDE.md", "w", encoding='utf-8') as f:
        f.write(guide)
    
    print("   VPS C2 Server guide created: VPS_C2_SERVER_GUIDE.md")

def main():
    """Main function"""
    print("Setup VPS C2 Server - Cach thay the cho Windows")
    print("=" * 70)
    
    # Tạo scripts
    create_vps_c2_setup()
    create_windows_bot_worker()
    create_vps_c2_guide()
    
    print("\nVPS C2 Server setup completed!")
    print("\nNext Steps:")
    print("1. Upload setup_vps_c2_server.sh len VPS")
    print("2. Chay: chmod +x setup_vps_c2_server.sh && ./setup_vps_c2_server.sh")
    print("3. Lay VPS IP: curl -s https://api.ipify.org")
    print("4. Tren Windows, chay: start_bot_worker_windows.bat")
    print("5. Nhap VPS IP khi duoc yeu cau")
    
    print("\nKet qua mong doi:")
    print("Bot worker tren Windows se ket noi thanh cong den VPS C2 Server!")
    print("Khong can mo port Windows, khong can firewall!")

if __name__ == "__main__":
    main()
