# 🚀 **C2 Server - Auto System Nâng Cấp Hoàn Chỉnh**

## 🎯 **Tính năng mới:**

### **🛡️ Auto-Bypass Firewall**
- **7 phương pháp bypass** tự động
- **Port forwarding** thông minh
- **VPN tunnel** tự động
- **SSH tunnel** tự động
- **Proxy chain** tự động
- **DNS tunnel** tự động
- **ICMP tunnel** tự động

### **🌐 Auto-Setup VPS**
- **7 bước setup** tự động hoàn chỉnh
- **Update hệ thống** tự động
- **Cài đặt dependencies** tự động
- **Cấu hình firewall** tự động
- **Download C2 Server** tự động
- **Tạo startup scripts** tự động
- **Test kết nối** tự động

### **🔧 One-Click Setup**
- **Setup hoàn chỉnh** với 1 lần click
- **5 phases** tự động
- **Test toàn bộ hệ thống** tự động
- **Báo cáo chi tiết** từng bước

---

## 🚀 **Cách sử dụng:**

### **1. Auto-Bypass Firewall**
```bash
# Bypass firewall cho IP cụ thể
python auto_bypass_firewall.py 192.168.1.5

# Tự động thử 7 phương pháp bypass
# ✅ Standard Firewall
# ✅ Port Forwarding  
# ✅ VPN Tunnel
# ✅ SSH Tunnel
# ✅ Proxy Chain
# ✅ DNS Tunnel
# ✅ ICMP Tunnel
```

### **2. Auto-Setup VPS**
```bash
# Setup VPS với IP cụ thể
python auto_setup_vps.py 192.168.1.5

# Hoặc setup VPS local
python auto_setup_vps.py

# Tự động thực hiện 7 bước:
# ✅ System Updated
# ✅ Dependencies Installed
# ✅ Firewall Configured
# ✅ C2 Server Downloaded
# ✅ Startup Scripts Created
# ✅ Installation Tested
# ✅ C2 Server Started
```

### **3. One-Click Setup (Khuyến nghị)**
```bash
# Setup hoàn chỉnh với 1 lần click
python one_click_setup.py

# Tự động thực hiện 5 phases:
# 🚀 Phase 1: System Preparation
# 🛡️ Phase 2: Firewall Bypass
# 🤖 Phase 3: C2 Server Setup
# 🚀 Phase 4: Starting Services
# 🔍 Phase 5: Testing Connectivity
```

---

## 🛡️ **Chi tiết Auto-Bypass Firewall:**

### **Method 1: Standard Firewall**
```bash
# Windows
netsh advfirewall firewall add rule name="C2 Server" dir=in action=allow protocol=TCP localport=5000

# Linux UFW
sudo ufw allow 5000/tcp

# Linux firewalld
sudo firewall-cmd --permanent --add-port=5000/tcp
```

### **Method 2: Port Forwarding**
```bash
# Windows
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=127.0.0.1

# Linux
iptables -t nat -A PREROUTING -p tcp --dport 5000 -j DNAT --to-destination 127.0.0.1:5000
```

### **Method 3: VPN Tunnel**
```bash
# OpenVPN config tự động
# Tạo file client.ovpn
# Kết nối VPN tunnel
```

### **Method 4: SSH Tunnel**
```bash
# SSH tunnel tự động
ssh -L 5000:localhost:5000 -N -f user@target_ip
```

### **Method 5: Proxy Chain**
```bash
# Windows proxy
netsh winhttp set proxy proxy-server="target_ip:5000"

# Linux proxy
export http_proxy=http://target_ip:5000
```

### **Method 6: DNS Tunnel**
```bash
# Iodine DNS tunnel
iodine -f target_ip
```

### **Method 7: ICMP Tunnel**
```bash
# Ptunnel ICMP tunnel
ptunnel -p target_ip -lp 5000 -da 127.0.0.1 -dp 5000
```

---

## 🌐 **Chi tiết Auto-Setup VPS:**

### **Step 1: Update System**
```bash
# Windows
wuauclt /detectnow

# Ubuntu/Debian
apt-get update && apt-get upgrade -y

# CentOS/RHEL
yum update -y
```

### **Step 2: Install Dependencies**
```bash
# Windows
winget install Python.Python.3.11
pip install flask flask-socketio psutil requests

# Ubuntu/Debian
apt-get install -y python3 python3-pip python3-venv git curl wget
pip3 install flask flask-socketio psutil requests

# CentOS/RHEL
yum install -y python3 python3-pip git curl wget
pip3 install flask flask-socketio psutil requests
```

### **Step 3: Configure Firewall**
```bash
# Windows
netsh advfirewall firewall add rule name="C2 Server" dir=in action=allow protocol=TCP localport=5000

# Ubuntu/Debian
ufw allow 5000/tcp
ufw allow 22/tcp
ufw --force enable

# CentOS/RHEL
firewall-cmd --permanent --add-port=5000/tcp
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --reload
```

### **Step 4: Download C2 Server**
```bash
# Tạo thư mục
mkdir c2_server

# Download files
curl -L -o c2_server/c2_server_auto.py https://raw.githubusercontent.com/your-repo/c2_server_auto.py
curl -L -o c2_server/bot_worker_auto.py https://raw.githubusercontent.com/your-repo/bot_worker_auto.py
curl -L -o c2_server/requirements.txt https://raw.githubusercontent.com/your-repo/requirements.txt
```

### **Step 5: Create Startup Scripts**
```bash
# Windows batch script
start_c2_server.bat

# Windows service
install_c2_service.bat

# Linux startup script
start_c2_server.sh

# Linux systemd service
c2-server.service
```

### **Step 6: Test Installation**
```bash
# Test Python
python --version

# Test packages
python -c "import flask, flask_socketio, psutil, requests; print('All packages working')"
```

### **Step 7: Start C2 Server**
```bash
# Windows
start "C2 Server" python c2_server_auto.py

# Linux
nohup python3 c2_server_auto.py > c2_server.log 2>&1 &
```

---

## 🔧 **Chi tiết One-Click Setup:**

### **Phase 1: System Preparation**
- Update hệ thống
- Cài đặt dependencies
- Kiểm tra Python

### **Phase 2: Firewall Bypass**
- Standard firewall rules
- Port forwarding
- VPN tunnel

### **Phase 3: C2 Server Setup**
- Tạo thư mục
- Copy files
- Tạo startup scripts

### **Phase 4: Starting Services**
- Khởi động C2 server
- Chờ server start
- Test server

### **Phase 5: Testing Connectivity**
- Test local connection
- Test API endpoints
- Test bot worker

---

## 📊 **Kết quả mong đợi:**

### **✅ Setup thành công:**
```
🎉 One-Click C2 Setup Completed Successfully!
============================================================
✅ System Prepared
✅ Firewall Bypassed
✅ C2 Server Setup
✅ Services Started
✅ Connectivity Tested

🚀 C2 Server is now running on localhost:5000
🌐 Access Web UI: http://localhost:5000
🤖 Bot workers can connect to: http://localhost:5000
🛡️ Firewall bypass methods: Standard Firewall, Port Forwarding, VPN Tunnel
```

### **🛡️ Firewall bypass thành công:**
```
🎉 Firewall bypass successful!
✅ Successful methods: Standard Firewall, Port Forwarding, VPN Tunnel
✅ Target 192.168.1.5:5000 is now accessible
🚀 You can now run your C2 server or bot worker
```

---

## 🚨 **Lưu ý quan trọng:**

### **1. Quyền Administrator/Root**
- **Windows**: Chạy PowerShell/CMD với quyền Administrator
- **Linux**: Sử dụng `sudo` hoặc chạy với quyền root

### **2. Network Security**
- Chỉ mở port cần thiết (5000)
- Sử dụng VPN tunnel nếu cần bảo mật cao
- Monitor firewall logs

### **3. VPS Requirements**
- **RAM**: Tối thiểu 1GB
- **Storage**: Tối thiểu 10GB
- **OS**: Windows 10+ hoặc Linux (Ubuntu 18.04+)

---

## 🔍 **Troubleshooting:**

### **Lỗi "Access Denied":**
```bash
# Windows: Chạy PowerShell với quyền Administrator
# Linux: Sử dụng sudo
sudo python3 auto_bypass_firewall.py 192.168.1.5
```

### **Lỗi "Port already in use":**
```bash
# Kiểm tra process đang sử dụng port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### **Lỗi "Connection refused":**
```bash
# Kiểm tra firewall
# Kiểm tra C2 server có đang chạy không
# Test kết nối local trước
```

---

## 🎯 **Kết luận:**

**Hệ thống C2 Server đã được nâng cấp hoàn chỉnh với:**

✅ **Auto-Bypass Firewall** - 7 phương pháp tự động  
✅ **Auto-Setup VPS** - 7 bước setup tự động  
✅ **One-Click Setup** - Setup hoàn chỉnh 1 lần click  
✅ **Multi-OS Support** - Windows & Linux  
✅ **Auto-Recovery** - Tự động khôi phục  
✅ **Auto-Monitoring** - Giám sát tự động  

**Bây giờ bạn có thể setup C2 Server trên bất kỳ VPS nào chỉ với 1 lệnh!** 🚀
