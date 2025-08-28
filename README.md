# 🚀 **C2 Server - Auto System Hoàn Chỉnh**

## 🎯 **Mô tả hệ thống:**

Hệ thống C2 Server tự động hoàn chỉnh với khả năng auto-bypass firewall và auto-setup VPS.

## 📁 **Cấu trúc file:**

### **🤖 Core Files:**
- `c2_server_auto.py` - C2 Server chính với auto-recovery, auto-scaling, auto-monitoring
- `bot_worker_auto.py` - Bot worker tự động kết nối đến C2 Server

### **🛡️ Auto-Bypass Firewall:**
- `auto_bypass_firewall.py` - Tự động bypass firewall với 7 phương pháp
- `auto_setup_vps.py` - Tự động setup VPS hoàn chỉnh
- `one_click_setup.py` - Setup hoàn chỉnh với 1 lần click

### **💻 Command Interface:**
- `send_command.py` - Gửi lệnh từ command line
- `command_interface.html` - Giao diện web để gửi lệnh

### **📚 Documentation:**
- `UPGRADE_GUIDE.md` - Hướng dẫn sử dụng chi tiết
- `requirements.txt` - Dependencies cần thiết

## 🚀 **Cách sử dụng:**

### **1. Setup hoàn chỉnh (Khuyến nghị):**
```bash
python one_click_setup.py
```

### **2. Bypass firewall:**
```bash
python auto_bypass_firewall.py <TARGET_IP>
```

### **3. Setup VPS:**
```bash
python auto_setup_vps.py <VPS_IP>
```

### **4. Chạy C2 Server:**
```bash
python c2_server_auto.py
```

### **5. Chạy Bot Worker:**
```bash
python bot_worker_auto.py --server <C2_SERVER_URL>
```

### **6. Gửi lệnh:**
```bash
python send_command.py
```

## 🛡️ **Tính năng chính:**

✅ **Auto-Bypass Firewall** - 7 phương pháp tự động  
✅ **Auto-Setup VPS** - 7 bước setup tự động  
✅ **One-Click Setup** - Setup hoàn chỉnh 1 lần click  
✅ **Multi-OS Support** - Windows & Linux  
✅ **Auto-Recovery** - Tự động khôi phục  
✅ **Auto-Monitoring** - Giám sát tự động  
✅ **Web Interface** - Giao diện web đẹp mắt  
✅ **Command Line** - Giao diện command line  

## 🔧 **Yêu cầu hệ thống:**

- **Python**: 3.7+
- **RAM**: Tối thiểu 1GB
- **Storage**: Tối thiểu 10GB
- **OS**: Windows 10+ hoặc Linux (Ubuntu 18.04+)
- **Quyền**: Administrator (Windows) hoặc Root (Linux)

## 📦 **Cài đặt dependencies:**

```bash
pip install -r requirements.txt
```

## 🌐 **Truy cập:**

- **Web UI**: http://localhost:5000
- **Command Interface**: http://localhost:5000/command
- **API Status**: http://localhost:5000/api/system-status
- **Bot List**: http://localhost:5000/api/bots

## 🎉 **Kết quả:**

Hệ thống C2 Server hoàn chỉnh với khả năng tự động bypass firewall và setup trên bất kỳ VPS nào chỉ với 1 lệnh!

---

**Tác giả**: Auto System  
**Phiên bản**: 2.0 - Auto-Bypass & Auto-Setup  
**Ngày cập nhật**: 28/08/2025
