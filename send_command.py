#!/usr/bin/env python3
"""
Send Command to Bot - Gửi lệnh đến Bot từ command line
"""

import requests
import json
import sys
import time
from datetime import datetime

class C2CommandSender:
    def __init__(self, server_url="http://192.168.1.5:5000"):
        self.server_url = server_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
    
    def get_system_status(self):
        """Lấy trạng thái hệ thống"""
        try:
            response = self.session.get(f"{self.server_url}/api/system-status")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Lỗi khi lấy trạng thái: {e}")
            return None
    
    def get_bots_list(self):
        """Lấy danh sách bot"""
        try:
            response = self.session.get(f"{self.server_url}/api/bots")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách bot: {e}")
            return None
    
    def send_command_to_all(self, command):
        """Gửi lệnh đến tất cả bot"""
        try:
            print(f"📡 Gửi lệnh đến tất cả bot: {command}")
            
            data = {'command': command}
            response = self.session.post(f"{self.server_url}/bot/command_all", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print(f"✅ Lệnh đã được gửi thành công!")
                    print(f"🆔 Command ID: {result.get('command_id', 'N/A')}")
                    return True
                else:
                    print(f"❌ Lỗi: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi gửi lệnh: {e}")
            return False
    
    def send_command_to_bot(self, bot_id, command):
        """Gửi lệnh đến bot cụ thể"""
        try:
            print(f"📡 Gửi lệnh đến bot {bot_id}: {command}")
            
            data = {
                'bot_id': bot_id,
                'command': command
            }
            response = self.session.post(f"{self.server_url}/bot/command", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print(f"✅ Lệnh đã được gửi thành công!")
                    print(f"🆔 Command ID: {result.get('command_id', 'N/A')}")
                    return True
                else:
                    print(f"❌ Lỗi: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi gửi lệnh: {e}")
            return False
    
    def show_status(self):
        """Hiển thị trạng thái hệ thống"""
        print("📊 Trạng thái hệ thống:")
        print("=" * 40)
        
        status = self.get_system_status()
        if status and status.get('status') == 'success':
            data = status.get('data', {})
            print(f"🖥️  Server: {data.get('server_status', 'Unknown')}")
            print(f"🤖 Bot Online: {data.get('online_bots', 0)}")
            print(f"📝 Tổng lệnh: {data.get('total_commands', 0)}")
            print(f"✅ Tỷ lệ thành công: {data.get('success_rate', 0)}%")
            print(f"⚡ CPU Usage: {data.get('cpu_usage', 0)}%")
            print(f"💾 Memory Usage: {data.get('memory_usage', 0)}%")
        else:
            print("❌ Không thể lấy trạng thái hệ thống")
    
    def show_bots(self):
        """Hiển thị danh sách bot"""
        print("\n🤖 Danh sách Bot:")
        print("=" * 40)
        
        bots = self.get_bots_list()
        if bots and bots.get('status') == 'success':
            bot_list = bots.get('bots', [])
            if bot_list:
                for i, bot in enumerate(bot_list, 1):
                    print(f"{i}. ID: {bot.get('bot_id', 'N/A')}")
                    print(f"   Tên: {bot.get('name', 'N/A')}")
                    print(f"   OS: {bot.get('os_info', 'N/A')}")
                    print(f"   Trạng thái: {bot.get('status', 'N/A')}")
                    print(f"   Health: {bot.get('health_score', 'N/A')}%")
                    print(f"   Cuối cùng: {bot.get('last_seen', 'N/A')}")
                    print()
            else:
                print("❌ Không có bot nào online")
        else:
            print("❌ Không thể lấy danh sách bot")
    
    def interactive_mode(self):
        """Chế độ tương tác"""
        print("🚀 C2 Server Command Interface")
        print("=" * 40)
        print("💡 Sử dụng 'help' để xem các lệnh có sẵn")
        print("💡 Sử dụng 'quit' để thoát")
        print()
        
        while True:
            try:
                command = input("🤖 C2> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("👋 Tạm biệt!")
                    break
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower() == 'status':
                    self.show_status()
                
                elif command.lower() == 'bots':
                    self.show_bots()
                
                elif command.lower() == 'send-all':
                    cmd = input("📝 Nhập lệnh cần gửi đến tất cả bot: ").strip()
                    if cmd:
                        self.send_command_to_all(cmd)
                    else:
                        print("❌ Lệnh không được để trống")
                
                elif command.lower() == 'send-bot':
                    self.show_bots()
                    bot_id = input("🆔 Nhập Bot ID: ").strip()
                    if bot_id:
                        cmd = input("📝 Nhập lệnh cần gửi: ").strip()
                        if cmd:
                            self.send_command_to_bot(bot_id, cmd)
                        else:
                            print("❌ Lệnh không được để trống")
                    else:
                        print("❌ Bot ID không được để trống")
                
                elif command.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("🚀 C2 Server Command Interface")
                    print("=" * 40)
                
                else:
                    print("❌ Lệnh không hợp lệ. Sử dụng 'help' để xem các lệnh có sẵn")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")
    
    def show_help(self):
        """Hiển thị trợ giúp"""
        print("\n📖 Trợ giúp - Các lệnh có sẵn:")
        print("=" * 40)
        print("help          - Hiển thị trợ giúp này")
        print("status        - Hiển thị trạng thái hệ thống")
        print("bots          - Hiển thị danh sách bot")
        print("send-all      - Gửi lệnh đến tất cả bot")
        print("send-bot      - Gửi lệnh đến bot cụ thể")
        print("clear         - Xóa màn hình")
        print("quit/exit/q   - Thoát chương trình")
        print()

def main():
    if len(sys.argv) < 2:
        # Interactive mode
        sender = C2CommandSender()
        sender.interactive_mode()
    else:
        # Command line mode
        if len(sys.argv) < 3:
            print("Usage:")
            print("  python send_command.py                    # Interactive mode")
            print("  python send_command.py all <command>      # Send to all bots")
            print("  python send_command.py bot <bot_id> <command>  # Send to specific bot")
            sys.exit(1)
        
        sender = C2CommandSender()
        
        if sys.argv[1] == 'all':
            command = ' '.join(sys.argv[2:])
            sender.send_command_to_all(command)
        
        elif sys.argv[1] == 'bot':
            if len(sys.argv) < 4:
                print("❌ Thiếu tham số: python send_command.py bot <bot_id> <command>")
                sys.exit(1)
            bot_id = sys.argv[2]
            command = ' '.join(sys.argv[3:])
            sender.send_command_to_bot(bot_id, command)
        
        else:
            print("❌ Lệnh không hợp lệ. Sử dụng 'all' hoặc 'bot'")

if __name__ == "__main__":
    main()
