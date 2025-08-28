#!/usr/bin/env python3
"""
One-Click C2 Setup - Setup hoàn chỉnh C2 Server với một lần click
"""

import os
import sys
import subprocess
import platform
import time
import requests
import json
from datetime import datetime

class OneClickC2Setup:
    def __init__(self):
        self.os_type = platform.system()
        self.setup_steps = []
        self.bypass_methods = []
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command, description, shell=True, timeout=60):
        self.log(f"🔧 {description}...")
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                self.log(f"   ✅ {description} successful", "SUCCESS")
                return True
            else:
                self.log(f"   ❌ {description} failed", "ERROR")
                return False
        except Exception as e:
            self.log(f"   ❌ {description} error: {e}", "ERROR")
            return False
    
    def check_admin_privileges(self):
        """Kiểm tra quyền Administrator"""
        self.log("🔐 Checking administrator privileges...")
        
        if self.os_type == "Windows":
            try:
                test_file = "C:\\Windows\\test_admin.tmp"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.log("   ✅ Administrator privileges confirmed", "SUCCESS")
                return True
            except:
                self.log("   ❌ Administrator privileges required!", "ERROR")
                return False
        else:
            if os.geteuid() == 0:
                self.log("   ✅ Root privileges confirmed", "SUCCESS")
                return True
            else:
                self.log("   ❌ Root privileges required!", "ERROR")
                return False
    
    def phase_1_system_preparation(self):
        """Phase 1: Chuẩn bị hệ thống"""
        self.log("🚀 Phase 1: System Preparation")
        self.log("=" * 50)
        
        # Step 1: Update system
        self.log("📦 Updating system...")
        if self.os_type == "Windows":
            self.run_command('wuauclt /detectnow', "Windows Update")
        else:
            if os.path.exists('/etc/debian_version'):
                self.run_command('apt-get update && apt-get upgrade -y', "System Update")
            elif os.path.exists('/etc/redhat-release'):
                self.run_command('yum update -y', "System Update")
        
        # Step 2: Install dependencies
        self.log("📚 Installing dependencies...")
        if self.os_type == "Windows":
            # Check Python
            if not self.run_command('python --version', "Check Python"):
                self.run_command('winget install Python.Python.3.11', "Install Python")
            
            # Install packages
            packages = ['flask', 'flask-socketio', 'psutil', 'requests']
            for package in packages:
                self.run_command(f'pip install {package}', f"Install {package}")
        else:
            # Linux packages
            if os.path.exists('/etc/debian_version'):
                packages = ['python3', 'python3-pip', 'python3-venv', 'git', 'curl', 'wget']
                self.run_command(f'apt-get install -y {" ".join(packages)}', "Install packages")
            elif os.path.exists('/etc/redhat-release'):
                packages = ['python3', 'python3-pip', 'git', 'curl', 'wget']
                self.run_command(f'yum install -y {" ".join(packages)}', "Install packages")
            
            # Python packages
            packages = ['flask', 'flask-socketio', 'psutil', 'requests']
            for package in packages:
                self.run_command(f'pip3 install {package}', f"Install {package}")
        
        self.setup_steps.append("System Prepared")
        return True
    
    def phase_2_firewall_bypass(self):
        """Phase 2: Bypass Firewall"""
        self.log("🛡️ Phase 2: Firewall Bypass")
        self.log("=" * 50)
        
        # Method 1: Standard firewall rules
        self.log("🛡️ Method 1: Standard Firewall Rules")
        if self.os_type == "Windows":
            commands = [
                'netsh advfirewall firewall add rule name="C2 Server In" dir=in action=allow protocol=TCP localport=5000',
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
            if self.run_command(cmd, "Firewall rule"):
                success = True
            else:
                success = False
        
        if success:
            self.bypass_methods.append("Standard Firewall")
        
        # Method 2: Port forwarding
        self.log("🔄 Method 2: Port Forwarding")
        if self.os_type == "Windows":
            cmd = 'netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=127.0.0.1'
            if self.run_command(cmd, "Port forwarding"):
                self.bypass_methods.append("Port Forwarding")
        else:
            cmd = 'iptables -t nat -A PREROUTING -p tcp --dport 5000 -j DNAT --to-destination 127.0.0.1:5000'
            if self.run_command(cmd, "Port forwarding"):
                self.bypass_methods.append("Port Forwarding")
        
        # Method 3: VPN tunnel (if available)
        self.log("🔒 Method 3: VPN Tunnel")
        if self.os_type == "Windows":
            result = subprocess.run('where openvpn', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("   ✅ OpenVPN found", "INFO")
                self.bypass_methods.append("VPN Tunnel")
        else:
            if self.run_command('apt-get install -y openvpn', "Install OpenVPN"):
                self.bypass_methods.append("VPN Tunnel")
        
        self.setup_steps.append("Firewall Bypassed")
        return True
    
    def phase_3_c2_server_setup(self):
        """Phase 3: Setup C2 Server"""
        self.log("🤖 Phase 3: C2 Server Setup")
        self.log("=" * 50)
        
        # Create C2 server directory
        if not os.path.exists('c2_server'):
            os.makedirs('c2_server')
        
        # Copy existing files
        files_to_copy = ['c2_server_auto.py', 'bot_worker_auto.py', 'requirements.txt']
        for file in files_to_copy:
            if os.path.exists(file):
                import shutil
                shutil.copy2(file, f'c2_server/{file}')
                self.log(f"   ✅ Copied {file}", "SUCCESS")
        
        # Create startup scripts
        self.log("🚀 Creating startup scripts...")
        if self.os_type == "Windows":
            # Windows batch script
            batch_content = '''@echo off
echo 🚀 Starting C2 Server...
cd /d %~dp0c2_server
python c2_server_auto.py
pause
'''
            with open('start_c2_server.bat', 'w') as f:
                f.write(batch_content)
            
            # Windows service
            service_content = '''@echo off
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
            startup_content = '''#!/bin/bash
echo "🚀 Starting C2 Server..."
cd "$(dirname "$0")/c2_server"
python3 c2_server_auto.py
'''
            with open('start_c2_server.sh', 'w') as f:
                f.write(startup_content)
            os.chmod('start_c2_server.sh', 0o755)
            
            # Linux systemd service
            service_content = '''[Unit]
Description=C2 Server Auto System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/c2_server
ExecStart=/usr/bin/python3 c2_server_auto.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
            with open('c2-server.service', 'w') as f:
                f.write(service_content)
        
        self.setup_steps.append("C2 Server Setup")
        return True
    
    def phase_4_start_services(self):
        """Phase 4: Khởi động services"""
        self.log("🚀 Phase 4: Starting Services")
        self.log("=" * 50)
        
        # Change to C2 server directory
        os.chdir('c2_server')
        
        # Start C2 server
        if self.os_type == "Windows":
            self.run_command('start "C2 Server" python c2_server_auto.py', "Start C2 Server")
        else:
            self.run_command('nohup python3 c2_server_auto.py > c2_server.log 2>&1 &', "Start C2 Server")
        
        # Wait for server to start
        self.log("   ⏳ Waiting for server to start...", "INFO")
        time.sleep(15)
        
        # Test server
        try:
            response = requests.get("http://localhost:5000/", timeout=10)
            if response.status_code == 200:
                self.log("   ✅ C2 Server is running", "SUCCESS")
                self.setup_steps.append("Services Started")
                return True
            else:
                self.log(f"   ❌ C2 Server status: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"   ❌ C2 Server test failed: {e}", "ERROR")
        
        return False
    
    def phase_5_test_connectivity(self):
        """Phase 5: Test kết nối"""
        self.log("🔍 Phase 5: Testing Connectivity")
        self.log("=" * 50)
        
        # Test local connection
        try:
            response = requests.get("http://localhost:5000/", timeout=10)
            if response.status_code == 200:
                self.log("   ✅ Local connection: OK", "SUCCESS")
            else:
                self.log(f"   ❌ Local connection failed: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"   ❌ Local connection error: {e}", "ERROR")
        
        # Test API endpoints
        endpoints = ['/api/bots', '/api/system-status']
        for endpoint in endpoints:
            try:
                response = requests.get(f"http://localhost:5000{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.log(f"   ✅ {endpoint}: OK", "SUCCESS")
                else:
                    self.log(f"   ❌ {endpoint}: {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"   ❌ {endpoint} error: {e}", "ERROR")
        
        # Test bot worker connection
        self.log("🤖 Testing bot worker connection...")
        try:
            from bot_worker_auto import AutoBotWorker
            bot = AutoBotWorker('http://localhost:5000', 'TestBot')
            if bot.register_with_server():
                self.log("   ✅ Bot worker connection: OK", "SUCCESS")
                bot.send_heartbeat()
                bot.disconnect_from_server()
            else:
                self.log("   ❌ Bot worker connection failed", "ERROR")
        except Exception as e:
            self.log(f"   ❌ Bot worker test error: {e}", "ERROR")
        
        self.setup_steps.append("Connectivity Tested")
        return True
    
    def run_complete_setup(self):
        """Chạy setup hoàn chỉnh"""
        self.log("🚀 Starting One-Click C2 Setup...")
        self.log(f"🖥️  OS: {self.os_type}")
        self.log("=" * 60)
        
        # Check admin privileges
        if not self.check_admin_privileges():
            self.log("❌ Cannot proceed without administrator privileges!", "ERROR")
            return False
        
        # Run all phases
        phases = [
            self.phase_1_system_preparation,
            self.phase_2_firewall_bypass,
            self.phase_3_c2_server_setup,
            self.phase_4_start_services,
            self.phase_5_test_connectivity
        ]
        
        for i, phase in enumerate(phases, 1):
            self.log(f"\n📋 Running Phase {i}/{len(phases)}...")
            if not phase():
                self.log(f"❌ Phase {i} failed!", "ERROR")
                return False
            time.sleep(3)
        
        # Setup summary
        self.log("\n🎉 One-Click C2 Setup Completed Successfully!")
        self.log("=" * 60)
        for step in self.setup_steps:
            self.log(f"✅ {step}")
        
        self.log(f"\n🚀 C2 Server is now running on localhost:5000")
        self.log("🌐 Access Web UI: http://localhost:5000")
        self.log("🤖 Bot workers can connect to: http://localhost:5000")
        self.log(f"🛡️ Firewall bypass methods: {', '.join(self.bypass_methods)}")
        
        return True

def main():
    setup = OneClickC2Setup()
    
    try:
        if setup.run_complete_setup():
            print("\n🎉 Setup completed successfully!")
            print("🚀 Your C2 Server is ready to use!")
            print("\n💡 Next steps:")
            print("   1. Open http://localhost:5000 in your browser")
            print("   2. Run bot workers: python bot_worker_auto.py")
            print("   3. Use command interface: python send_command.py")
        else:
            print("\n❌ Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
