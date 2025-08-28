#!/usr/bin/env python3
"""
Test Connection Fix - Kiểm tra kết nối bot worker với C2 server
"""
import requests
import time
import subprocess
import sys
import os

def test_c2_server():
    """Test C2 server connection"""
    print("🔍 Testing C2 Server Connection...")
    print("=" * 50)
    
    # Test localhost
    print("📍 Testing localhost:5000...")
    try:
        response = requests.get("http://localhost:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ localhost:5000 - OK")
        else:
            print(f"   ❌ localhost:5000 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ localhost:5000 - Error: {e}")
    
    # Test 192.168.1.5
    print("📍 Testing 192.168.1.5:5000...")
    try:
        response = requests.get("http://192.168.1.5:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ 192.168.1.5:5000 - OK")
        else:
            print(f"   ❌ 192.168.1.5:5000 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 192.168.1.5:5000 - Error: {e}")
    
    # Test 127.0.0.1
    print("📍 Testing 127.0.0.1:5000...")
    try:
        response = requests.get("http://127.0.0.1:5000/api/bots", timeout=5)
        if response.status_code == 200:
            print("   ✅ 127.0.0.1:5000 - OK")
        else:
            print(f"   ❌ 127.0.0.1:5000 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 127.0.0.1:5000 - Error: {e}")

def test_bot_worker_connection():
    """Test bot worker connection"""
    print("\n🤖 Testing Bot Worker Connection...")
    print("=" * 50)
    
    # Test với localhost
    print("📍 Testing bot worker with localhost:5000...")
    try:
        result = subprocess.run([
            sys.executable, "bot_worker_auto.py", 
            "--server", "http://localhost:5000"
        ], capture_output=True, text=True, timeout=10)
        
        if "Successfully registered" in result.stdout:
            print("   ✅ localhost:5000 - Bot registered successfully")
        elif "Connection refused" in result.stderr or "No connection" in result.stderr:
            print("   ❌ localhost:5000 - Connection refused")
        else:
            print(f"   ⚠️ localhost:5000 - Output: {result.stdout[:100]}...")
    except subprocess.TimeoutExpired:
        print("   ⏱️ localhost:5000 - Timeout (expected)")
    except Exception as e:
        print(f"   ❌ localhost:5000 - Error: {e}")
    
    # Test với 192.168.1.5
    print("📍 Testing bot worker with 192.168.1.5:5000...")
    try:
        result = subprocess.run([
            sys.executable, "bot_worker_auto.py", 
            "--server", "http://192.168.1.5:5000"
        ], capture_output=True, text=True, timeout=10)
        
        if "Successfully registered" in result.stdout:
            print("   ✅ 192.168.1.5:5000 - Bot registered successfully")
        elif "Connection refused" in result.stderr or "No connection" in result.stderr:
            print("   ❌ 192.168.1.5:5000 - Connection refused")
        else:
            print(f"   ⚠️ 192.168.1.5:5000 - Output: {result.stdout[:100]}...")
    except subprocess.TimeoutExpired:
        print("   ⏱️ 192.168.1.5:5000 - Timeout (expected)")
    except Exception as e:
        print(f"   ❌ 192.168.1.5:5000 - Error: {e}")

def show_solution():
    """Show solution"""
    print("\n💡 Solution - Cách sửa:")
    print("=" * 50)
    print("1. 🚀 Start C2 Server:")
    print("   python c2_server_auto.py")
    print()
    print("2. 🤖 Start Bot Worker (Terminal mới):")
    print("   python bot_worker_auto.py --server http://192.168.1.5:5000")
    print()
    print("3. 🌐 Test Web Interface:")
    print("   http://192.168.1.5:5000")
    print()
    print("4. 📱 Test Command Interface:")
    print("   python send_command.py")
    print()
    print("⚠️  Lưu ý: Luôn dùng --server để chỉ định IP chính xác!")

def main():
    """Main function"""
    print("🔧 Test Connection Fix - Kiểm tra kết nối")
    print("=" * 60)
    
    # Test C2 server
    test_c2_server()
    
    # Test bot worker
    test_bot_worker_connection()
    
    # Show solution
    show_solution()

if __name__ == "__main__":
    main()
