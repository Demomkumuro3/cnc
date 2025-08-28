#!/usr/bin/env python3
"""
Auto-Setup VPS - Tự động setup C2 Server trên VPS
"""

import os
import sys
import subprocess
import platform
import time
import requests
import json
from datetime import datetime

class AutoVPSSetup:
    def __init__(self, vps_ip=None):
        self.vps_ip = vps_ip or self.get_local_ip()
        self.os_type = platform.system()
        self.setup_steps = []
        
    def get_local_ip(self):
        """Lấy IP local"""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command, description, shell=True):
        self.log(f"🔧 {description}...")
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.log(f"   ✅ {description} successful", "SUCCESS")
                return True
            else:
                self.log(f"   ❌ {description} failed", "ERROR")
                return False
        except Exception as e:
            self.log(f"   ❌ {description} error: {e}", "ERROR")
            return False
    
    def step_1_update_system(self):
        """Bước 1: Update hệ thống"""
        self.log("📦 Step 1: Updating system...")
        
        if self.os_type == "Windows":
            # Windows update
            if self.run_command('wuauclt /detectnow', "Windows Update"):
                self.setup_steps.append("System Updated")
                return True
        else:
            # Linux update
            if os.path.exists('/etc/debian_version'):
                commands = [
                    'apt-get update',
                    'apt-get upgrade -y',
                    'apt-get autoremove -y'
                ]
            elif os.path.exists('/etc/redhat-release'):
                commands = [
                    'yum update -y',
                    'yum upgrade -y'
                ]
            else:
                commands = ['pacman -Syu --noconfirm']
            
            success = True
            for cmd in commands:
                if not self.run_command(cmd, f"Update command"):
                    success = False
            
            if success:
                self.setup_steps.append("System Updated")
                return True
        
        return False
    
    def step_2_install_dependencies(self):
        """Bước 2: Cài đặt dependencies"""
        self.log("📚 Step 2: Installing dependencies...")
        
        if self.os_type == "Windows":
            # Windows - install Python and pip
            if not self.run_command('python --version', "Check Python"):
                self.log("   📥 Installing Python...", "INFO")
                # Download and install Python
                self.run_command('winget install Python.Python.3.11', "Install Python")
            
            # Install pip packages
            pip_packages = ['flask', 'flask-socketio', 'psutil', 'requests']
            for package in pip_packages:
                self.run_command(f'pip install {package}', f"Install {package}")
        else:
            # Linux - install packages
            if os.path.exists('/etc/debian_version'):
                packages = ['python3', 'python3-pip', 'python3-venv', 'git', 'curl', 'wget']
                install_cmd = f'apt-get install -y {" ".join(packages)}'
            elif os.path.exists('/etc/redhat-release'):
                packages = ['python3', 'python3-pip', 'git', 'curl', 'wget']
                install_cmd = f'yum install -y {" ".join(packages)}'
            else:
                packages = ['python', 'python-pip', 'git', 'curl', 'wget']
                install_cmd = f'pacman -S --noconfirm {" ".join(packages)}'
            
            if self.run_command(install_cmd, "Install system packages"):
                # Install Python packages
                pip_packages = ['flask', 'flask-socketio', 'psutil', 'requests']
                for package in pip_packages:
                    self.run_command(f'pip3 install {package}', f"Install {package}")
        
        self.setup_steps.append("Dependencies Installed")
        return True
    
    def step_3_configure_firewall(self):
        """Bước 3: Cấu hình firewall"""
        self.log("🛡️ Step 3: Configuring firewall...")
        
        if self.os_type == "Windows":
            commands = [
                'netsh advfirewall firewall add rule name="C2 Server" dir=in action=allow protocol=TCP localport=5000',
                'netsh advfirewall firewall add rule name="C2 Server Out" dir=out action=allow protocol=TCP localport=5000',
                'netsh advfirewall firewall add rule name="C2 Server All IPs" dir=in action=allow protocol=TCP localport=5000 remoteip=any'
            ]
        else:
            if os.path.exists('/etc/debian_version'):
                commands = [
                    'ufw allow 5000/tcp',
                    'ufw allow 22/tcp',
                    'ufw --force enable'
                ]
            elif os.path.exists('/etc/redhat-release'):
                commands = [
                    'firewall-cmd --permanent --add-port=5000/tcp',
                    'firewall-cmd --permanent --add-port=22/tcp',
                    'firewall-cmd --reload'
                ]
            else:
                commands = [
                    'iptables -A INPUT -p tcp --dport 5000 -j ACCEPT',
                    'iptables -A INPUT -p tcp --dport 22 -j ACCEPT'
                ]
        
        success = True
        for cmd in commands:
            if not self.run_command(cmd, f"Firewall rule"):
                success = False
        
        if success:
            self.setup_steps.append("Firewall Configured")
            return True
        return False
    
    def step_4_download_c2_server(self):
        """Bước 4: Download C2 Server"""
        self.log("📥 Step 4: Downloading C2 Server...")
        
        # Create directory
        if not os.path.exists('c2_server'):
            os.makedirs('c2_server')
        
        # Download files
        files_to_download = {
            'c2_server_auto.py': 'https://raw.githubusercontent.com/your-repo/c2_server_auto.py',
            'bot_worker_auto.py': 'https://raw.githubusercontent.com/your-repo/bot_worker_auto.py',
            'requirements.txt': 'https://raw.githubusercontent.com/your-repo/requirements.txt'
        }
        
        success = True
        for filename, url in files_to_download.items():
            if self.run_command(f'curl -L -o c2_server/{filename} {url}', f"Download {filename}"):
                self.log(f"   ✅ Downloaded {filename}", "SUCCESS")
            else:
                success = False
        
        if success:
            self.setup_steps.append("C2 Server Downloaded")
            return True
        return False
    
    def step_5_create_startup_scripts(self):
        """Bước 5: Tạo startup scripts"""
        self.log("🚀 Step 5: Creating startup scripts...")
        
        if self.os_type == "Windows":
            # Windows batch script
            batch_content = f'''@echo off
echo 🚀 Starting C2 Server on {self.vps_ip}...
cd /d %~dp0c2_server
python c2_server_auto.py
pause
'''
            with open('start_c2_server.bat', 'w') as f:
                f.write(batch_content)
            
            # Windows service script
            service_content = f'''@echo off
echo Installing C2 Server as Windows Service...
sc create "C2Server" binPath= "%~dp0c2_server\\c2_server_auto.py" start= auto
sc description "C2Server" "C2 Server Auto System"
sc start "C2Server"
echo C2 Server service installed and started!
pause
'''
            with open('install_c2_service.bat', 'w') as f:
                f.write(service_content)
            
        else:
            # Linux startup script
            startup_content = f'''#!/bin/bash
echo "🚀 Starting C2 Server on {self.vps_ip}..."
cd "$(dirname "$0")/c2_server"
python3 c2_server_auto.py
'''
            with open('start_c2_server.sh', 'w') as f:
                f.write(startup_content)
            
            # Make executable
            os.chmod('start_c2_server.sh', 0o755)
            
            # Linux systemd service
            service_content = f'''[Unit]
Description=C2 Server Auto System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={os.getcwd()}/c2_server
ExecStart=/usr/bin/python3 c2_server_auto.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
            with open('c2-server.service', 'w') as f:
                f.write(service_content)
        
        self.setup_steps.append("Startup Scripts Created")
        return True
    
    def step_6_test_installation(self):
        """Bước 6: Test cài đặt"""
        self.log("🧪 Step 6: Testing installation...")
        
        # Test Python
        if not self.run_command('python --version', "Test Python"):
            if not self.run_command('python3 --version', "Test Python3"):
                self.log("   ❌ Python not found", "ERROR")
                return False
        
        # Test required packages
        test_script = '''
import flask
import flask_socketio
import psutil
import requests
print("✅ All required packages are available")
'''
        
        with open('test_packages.py', 'w') as f:
            f.write(test_script)
        
        if self.run_command('python test_packages.py', "Test packages"):
            self.log("   ✅ All packages working", "SUCCESS")
            os.remove('test_packages.py')
            self.setup_steps.append("Installation Tested")
            return True
        
        return False
    
    def step_7_start_c2_server(self):
        """Bước 7: Khởi động C2 Server"""
        self.log("🚀 Step 7: Starting C2 Server...")
        
        # Change to C2 server directory
        os.chdir('c2_server')
        
        # Start C2 server in background
        if self.os_type == "Windows":
            if self.run_command('start "C2 Server" python c2_server_auto.py', "Start C2 Server"):
                self.log("   ✅ C2 Server started in background", "SUCCESS")
        else:
            if self.run_command('nohup python3 c2_server_auto.py > c2_server.log 2>&1 &', "Start C2 Server"):
                self.log("   ✅ C2 Server started in background", "SUCCESS")
        
        # Wait for server to start
        self.log("   ⏳ Waiting for server to start...", "INFO")
        time.sleep(10)
        
        # Test if server is running
        try:
            response = requests.get(f"http://{self.vps_ip}:5000/", timeout=10)
            if response.status_code == 200:
                self.log("   ✅ C2 Server is running and accessible", "SUCCESS")
                self.setup_steps.append("C2 Server Started")
                return True
            else:
                self.log(f"   ❌ C2 Server returned status: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"   ❌ C2 Server test failed: {e}", "ERROR")
        
        return False
    
    def run_complete_setup(self):
        """Chạy setup hoàn chỉnh"""
        self.log("🚀 Starting Auto VPS Setup...")
        self.log(f"🎯 VPS IP: {self.vps_ip}")
        self.log(f"🖥️  OS: {self.os_type}")
        self.log("=" * 60)
        
        # Check admin privileges
        if self.os_type == "Windows":
            try:
                test_file = "C:\\Windows\\test_admin.tmp"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.log("✅ Administrator privileges confirmed", "SUCCESS")
            except:
                self.log("❌ Administrator privileges required!", "ERROR")
                return False
        else:
            if os.geteuid() != 0:
                self.log("❌ Root privileges required!", "ERROR")
                return False
        
        # Run all setup steps
        steps = [
            self.step_1_update_system,
            self.step_2_install_dependencies,
            self.step_3_configure_firewall,
            self.step_4_download_c2_server,
            self.step_5_create_startup_scripts,
            self.step_6_test_installation,
            self.step_7_start_c2_server
        ]
        
        for i, step in enumerate(steps, 1):
            self.log(f"\n📋 Running Step {i}/{len(steps)}...")
            if not step():
                self.log(f"❌ Step {i} failed!", "ERROR")
                return False
            time.sleep(2)
        
        # Setup summary
        self.log("\n🎉 VPS Setup Completed Successfully!")
        self.log("=" * 60)
        for step in self.setup_steps:
            self.log(f"✅ {step}")
        
        self.log(f"\n🚀 C2 Server is now running on {self.vps_ip}:5000")
        self.log("🌐 Access Web UI: http://" + self.vps_ip + ":5000")
        self.log("🤖 Bot workers can connect to: http://" + self.vps_ip + ":5000")
        
        return True

def main():
    if len(sys.argv) > 1:
        vps_ip = sys.argv[1]
    else:
        vps_ip = None
    
    setup = AutoVPSSetup(vps_ip)
    
    try:
        if setup.run_complete_setup():
            print("\n🎉 VPS setup completed successfully!")
            print("🚀 Your C2 Server is ready to use!")
        else:
            print("\n❌ VPS setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
