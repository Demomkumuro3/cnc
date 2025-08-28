#!/usr/bin/env python3
"""
Auto-Bypass Firewall - Tự động bypass firewall với nhiều phương pháp
"""

import os
import sys
import subprocess
import platform
import time
import socket
import requests
import threading
from datetime import datetime

class AutoFirewallBypass:
    def __init__(self, target_ip, target_port=5000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.os_type = platform.system()
        self.bypass_methods = []
        self.success_methods = []
        
    def log(self, message, level="INFO"):
        """Log message với timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command, description, shell=True, timeout=30):
        """Chạy command và hiển thị kết quả"""
        self.log(f"🔧 {description}...")
        try:
            if shell:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            else:
                result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                self.log(f"   ✅ {description} successful", "SUCCESS")
                if result.stdout.strip():
                    self.log(f"      Output: {result.stdout.strip()}", "DEBUG")
                return True
            else:
                self.log(f"   ❌ {description} failed", "ERROR")
                if result.stderr.strip():
                    self.log(f"      Error: {result.stderr.strip()}", "ERROR")
                return False
        except Exception as e:
            self.log(f"   ❌ {description} error: {e}", "ERROR")
            return False
    
    def check_admin_privileges(self):
        """Kiểm tra quyền Administrator"""
        self.log("🔐 Checking administrator privileges...")
        
        if self.os_type == "Windows":
            try:
                # Try to create a file in C:\Windows (requires admin)
                test_file = "C:\\Windows\\test_admin.tmp"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.log("   ✅ Administrator privileges confirmed", "SUCCESS")
                return True
            except:
                self.log("   ❌ Administrator privileges required!", "ERROR")
                self.log("   💡 Please run as Administrator", "WARNING")
                return False
        else:
            # Linux - check if running as root
            if os.geteuid() == 0:
                self.log("   ✅ Root privileges confirmed", "SUCCESS")
                return True
            else:
                self.log("   ❌ Root privileges required!", "ERROR")
                self.log("   💡 Please run with: sudo python3 auto_bypass_firewall.py", "WARNING")
                return False
    
    def method_1_standard_firewall(self):
        """Phương pháp 1: Mở firewall tiêu chuẩn"""
        self.log("🛡️ Method 1: Standard Firewall Rules")
        
        if self.os_type == "Windows":
            commands = [
                f'netsh advfirewall firewall add rule name="C2 Server In" dir=in action=allow protocol=TCP localport={self.target_port}',
                f'netsh advfirewall firewall add rule name="C2 Server Out" dir=out action=allow protocol=TCP localport={self.target_port}',
                f'netsh advfirewall firewall add rule name="C2 Server All IPs" dir=in action=allow protocol=TCP localport={self.target_port} remoteip=any'
            ]
        else:
            if os.path.exists('/etc/debian_version'):
                commands = [
                    f'ufw allow {self.target_port}/tcp',
                    'ufw reload'
                ]
            elif os.path.exists('/etc/redhat-release'):
                commands = [
                    f'firewall-cmd --permanent --add-port={self.target_port}/tcp',
                    f'firewall-cmd --permanent --add-rich-rule=\'rule family="ipv4" port port="{self.target_port}" protocol="tcp" accept\'',
                    'firewall-cmd --reload'
                ]
            else:
                commands = [
                    f'iptables -A INPUT -p tcp --dport {self.target_port} -j ACCEPT',
                    f'iptables -A OUTPUT -p tcp --sport {self.target_port} -j ACCEPT'
                ]
        
        success = True
        for cmd in commands:
            if not self.run_command(cmd, f"Firewall command"):
                success = False
        
        if success:
            self.success_methods.append("Standard Firewall")
            return True
        return False
    
    def method_2_port_forwarding(self):
        """Phương pháp 2: Port Forwarding"""
        self.log("🔄 Method 2: Port Forwarding")
        
        try:
            # Test if port forwarding is possible
            if self.os_type == "Windows":
                # Windows port forwarding
                cmd = f'netsh interface portproxy add v4tov4 listenport={self.target_port} listenaddress=0.0.0.0 connectport={self.target_port} connectaddress={self.target_ip}'
                if self.run_command(cmd, "Port forwarding"):
                    self.success_methods.append("Port Forwarding")
                    return True
            else:
                # Linux port forwarding with iptables
                cmd = f'iptables -t nat -A PREROUTING -p tcp --dport {self.target_port} -j DNAT --to-destination {self.target_ip}:{self.target_port}'
                if self.run_command(cmd, "Port forwarding"):
                    self.success_methods.append("Port Forwarding")
                    return True
        except Exception as e:
            self.log(f"   ❌ Port forwarding failed: {e}", "ERROR")
        
        return False
    
    def method_3_vpn_tunnel(self):
        """Phương pháp 3: VPN Tunnel (OpenVPN)"""
        self.log("🔒 Method 3: VPN Tunnel Setup")
        
        try:
            # Check if OpenVPN is available
            if self.os_type == "Windows":
                # Windows - check OpenVPN
                result = subprocess.run('where openvpn', shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("   ✅ OpenVPN found, setting up tunnel...", "SUCCESS")
                    # Create basic OpenVPN config
                    config_content = f"""client
dev tun
proto udp
remote {self.target_ip} 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
remote-cert-tls server
cipher AES-256-CBC
verb 3
"""
                    with open('client.ovpn', 'w') as f:
                        f.write(config_content)
                    
                    self.log("   📁 OpenVPN config created: client.ovpn", "INFO")
                    self.success_methods.append("VPN Tunnel")
                    return True
                else:
                    self.log("   ❌ OpenVPN not found", "WARNING")
            else:
                # Linux - install and setup OpenVPN
                if self.run_command('apt-get update && apt-get install -y openvpn', "Installing OpenVPN"):
                    self.success_methods.append("VPN Tunnel")
                    return True
        except Exception as e:
            self.log(f"   ❌ VPN setup failed: {e}", "ERROR")
        
        return False
    
    def method_4_ssh_tunnel(self):
        """Phương pháp 4: SSH Tunnel"""
        self.log("🔑 Method 4: SSH Tunnel")
        
        try:
            # Create SSH tunnel
            ssh_cmd = f'ssh -L {self.target_port}:localhost:{self.target_port} -N -f user@{self.target_ip}'
            
            if self.run_command(ssh_cmd, "SSH tunnel setup"):
                self.success_methods.append("SSH Tunnel")
                return True
            else:
                self.log("   ❌ SSH tunnel failed - SSH key setup required", "WARNING")
        except Exception as e:
            self.log(f"   ❌ SSH tunnel error: {e}", "ERROR")
        
        return False
    
    def method_5_proxy_chain(self):
        """Phương pháp 5: Proxy Chain"""
        self.log("🔗 Method 5: Proxy Chain")
        
        try:
            if self.os_type == "Windows":
                # Windows proxy setup
                proxy_cmd = f'netsh winhttp set proxy proxy-server="{self.target_ip}:{self.target_port}" bypass-list="localhost"'
                if self.run_command(proxy_cmd, "Proxy setup"):
                    self.success_methods.append("Proxy Chain")
                    return True
            else:
                # Linux proxy setup
                proxy_cmd = f'export http_proxy=http://{self.target_ip}:{self.target_port} && export https_proxy=http://{self.target_ip}:{self.target_port}'
                if self.run_command(proxy_cmd, "Proxy setup"):
                    self.success_methods.append("Proxy Chain")
                    return True
        except Exception as e:
            self.log(f"   ❌ Proxy setup failed: {e}", "ERROR")
        
        return False
    
    def method_6_dns_tunnel(self):
        """Phương pháp 6: DNS Tunnel"""
        self.log("🌐 Method 6: DNS Tunnel")
        
        try:
            # Check if iodine is available
            if self.os_type == "Windows":
                # Windows - check iodine
                result = subprocess.run('where iodine', shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    dns_cmd = f'iodine -f {self.target_ip}'
                    if self.run_command(dns_cmd, "DNS tunnel setup"):
                        self.success_methods.append("DNS Tunnel")
                        return True
                else:
                    self.log("   ❌ Iodine not found", "WARNING")
            else:
                # Linux - install and setup iodine
                if self.run_command('apt-get update && apt-get install -y iodine', "Installing iodine"):
                    dns_cmd = f'iodine -f {self.target_ip}'
                    if self.run_command(dns_cmd, "DNS tunnel setup"):
                        self.success_methods.append("DNS Tunnel")
                        return True
        except Exception as e:
            self.log(f"   ❌ DNS tunnel failed: {e}", "ERROR")
        
        return False
    
    def method_7_icmp_tunnel(self):
        """Phương pháp 7: ICMP Tunnel"""
        self.log("📡 Method 7: ICMP Tunnel")
        
        try:
            # Check if ptunnel is available
            if self.os_type == "Windows":
                # Windows - check ptunnel
                result = subprocess.run('where ptunnel', shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    icmp_cmd = f'ptunnel -p {self.target_ip} -lp {self.target_port} -da 127.0.0.1 -dp {self.target_port}'
                    if self.run_command(icmp_cmd, "ICMP tunnel setup"):
                        self.success_methods.append("ICMP Tunnel")
                        return True
                else:
                    self.log("   ❌ Ptunnel not found", "WARNING")
            else:
                # Linux - install and setup ptunnel
                if self.run_command('apt-get update && apt-get install -y ptunnel', "Installing ptunnel"):
                    icmp_cmd = f'ptunnel -p {self.target_ip} -lp {self.target_port} -da 127.0.0.1 -dp {self.target_port}'
                    if self.run_command(icmp_cmd, "ICMP tunnel setup"):
                        self.success_methods.append("ICMP Tunnel")
                        return True
        except Exception as e:
            self.log(f"   ❌ ICMP tunnel failed: {e}", "ERROR")
        
        return False
    
    def test_connection(self):
        """Test kết nối sau khi bypass"""
        self.log(f"🧪 Testing connection to {self.target_ip}:{self.target_port}...")
        
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"http://{self.target_ip}:{self.target_port}/", timeout=10)
                if response.status_code == 200:
                    self.log("   ✅ Connection test successful!", "SUCCESS")
                    return True
                else:
                    self.log(f"   ⚠️ Attempt {attempt + 1}: Status {response.status_code}", "WARNING")
            except Exception as e:
                self.log(f"   ⚠️ Attempt {attempt + 1}: {e}", "WARNING")
            
            if attempt < max_attempts - 1:
                self.log("   ⏳ Waiting 5 seconds before retry...", "INFO")
                time.sleep(5)
        
        self.log("   ❌ All connection attempts failed", "ERROR")
        return False
    
    def run_all_methods(self):
        """Chạy tất cả các phương pháp bypass"""
        self.log("🚀 Starting Auto-Firewall Bypass...")
        self.log(f"🎯 Target: {self.target_ip}:{self.target_port}")
        self.log(f"🖥️  OS: {self.os_type}")
        self.log("=" * 60)
        
        # Check admin privileges first
        if not self.check_admin_privileges():
            self.log("❌ Cannot proceed without administrator privileges!", "ERROR")
            return False
        
        # Run all bypass methods
        methods = [
            self.method_1_standard_firewall,
            self.method_2_port_forwarding,
            self.method_3_vpn_tunnel,
            self.method_4_ssh_tunnel,
            self.method_5_proxy_chain,
            self.method_6_dns_tunnel,
            self.method_7_icmp_tunnel
        ]
        
        for method in methods:
            try:
                if method():
                    self.log(f"✅ Method successful: {method.__name__}", "SUCCESS")
                else:
                    self.log(f"❌ Method failed: {method.__name__}", "WARNING")
            except Exception as e:
                self.log(f"❌ Method error {method.__name__}: {e}", "ERROR")
            
            time.sleep(2)  # Wait between methods
        
        # Test connection
        self.log("\n🔍 Testing connection after bypass...")
        if self.test_connection():
            self.log("🎉 Firewall bypass successful!", "SUCCESS")
            self.log(f"✅ Successful methods: {', '.join(self.success_methods)}", "SUCCESS")
            return True
        else:
            self.log("❌ Firewall bypass failed", "ERROR")
            return False
    
    def cleanup(self):
        """Dọn dẹp sau khi bypass"""
        self.log("🧹 Cleaning up...")
        
        try:
            # Remove temporary files
            temp_files = ['client.ovpn']
            for file in temp_files:
                if os.path.exists(file):
                    os.remove(file)
                    self.log(f"   ✅ Removed {file}", "INFO")
            
            # Stop background processes
            if self.os_type == "Windows":
                self.run_command('taskkill /f /im openvpn.exe', "Stopping OpenVPN")
                self.run_command('taskkill /f /im iodine.exe', "Stopping Iodine")
                self.run_command('taskkill /f /im ptunnel.exe', "Stopping Ptunnel")
            else:
                self.run_command('pkill -f openvpn', "Stopping OpenVPN")
                self.run_command('pkill -f iodine', "Stopping Iodine")
                self.run_command('pkill -f ptunnel', "Stopping Ptunnel")
            
            self.log("✅ Cleanup completed", "SUCCESS")
        except Exception as e:
            self.log(f"❌ Cleanup error: {e}", "ERROR")

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_bypass_firewall.py <TARGET_IP>")
        print("Example: python auto_bypass_firewall.py 192.168.1.5")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = 5000
    
    bypass = AutoFirewallBypass(target_ip, target_port)
    
    try:
        if bypass.run_all_methods():
            print("\n🎉 Firewall bypass completed successfully!")
            print(f"✅ Target {target_ip}:{target_port} is now accessible")
            print("🚀 You can now run your C2 server or bot worker")
        else:
            print("\n❌ Firewall bypass failed!")
            print("💡 Manual intervention may be required")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    finally:
        bypass.cleanup()

if __name__ == "__main__":
    main()
