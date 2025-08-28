# 🚀 HƯỚNG DẪN SỬ DỤNG C2 CNC - TẤT CẢ CÁC CÁCH

## 📋 **Tổng quan các cách làm C2 CNC:**

### **1. 🌐 Ngrok Tunnel (Đơn giản nhất)**
### **2. 🏠 VPS làm C2 Server (Ổn định nhất)**
### **3. 🔥 Public IP Windows (Đã thử - có vấn đề firewall)**

---

## 🌐 **CÁCH 1: NGROK TUNNEL (Khuyến nghị cho người mới)**

### **Bước 1: Tạo scripts**
```bash
python setup_ngrok_simple.py
```

### **Bước 2: Download ngrok**
```bash
# Windows
download_ngrok.bat

# Linux/Mac
chmod +x download_ngrok.sh
./download_ngrok.sh
```

### **Bước 3: Đăng ký tài khoản ngrok**
1. Truy cập: https://ngrok.com/signup
2. Tạo tài khoản miễn phí
3. Lấy authtoken từ dashboard

### **Bước 4: Cấu hình ngrok**
```bash
# Thêm authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE

# Test ngrok
ngrok version
```

### **Bước 5: Khởi động C2 Server**
```bash
python c2_server_auto.py
```

### **Bước 6: Tạo ngrok tunnel**
```bash
# Mở terminal mới
start_ngrok.bat
```

**Kết quả sẽ hiển thị:**
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```

### **Bước 7: Sử dụng trên VPS**
```bash
# Trên VPS, kết nối bot worker
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

---

## 🏠 **CÁCH 2: VPS LÀM C2 SERVER (Khuyến nghị cho dài hạn)**

### **Bước 1: Tạo scripts**
```bash
python setup_vps_c2_server.py
```

### **Bước 2: Upload lên VPS**
```bash
# Upload setup_vps_c2_server.sh lên VPS
# Sử dụng SCP, SFTP, hoặc copy-paste
```

### **Bước 3: Setup trên VPS**
```bash
# Trên VPS (Google Cloud)
chmod +x setup_vps_c2_server.sh
./setup_vps_c2_server.sh
```

### **Bước 4: Kiểm tra C2 Server**
```bash
# Trên VPS
systemctl status c2-server
curl http://localhost:5000/api/bots
```

### **Bước 5: Lấy VPS IP**
```bash
# Trên VPS
curl -s https://api.ipify.org
```

### **Bước 6: Kết nối từ Windows**
```bash
# Trên Windows
start_bot_worker_windows.bat
# Nhập VPS IP khi được yêu cầu
```

---

## 🔥 **CÁCH 3: PUBLIC IP WINDOWS (Đã thử - có vấn đề)**

### **Vấn đề hiện tại:**
- Windows Firewall không cho phép kết nối ngoài
- Cần quyền Administrator để mở port
- Có thể bị ISP chặn

### **Nếu muốn thử lại:**
```bash
# Chạy script setup public IP
python setup_public_ip_c2.py

# Force mở port (cần Administrator)
force_open_port.bat

# Test kết nối
test_connection_quick.bat
```

---

## 📊 **SO SÁNH CÁC CÁCH:**

| Tiêu chí | Ngrok | VPS C2 Server | Public IP Windows |
|----------|-------|---------------|-------------------|
| **Độ khó** | ⭐ Dễ | ⭐⭐ Trung bình | ⭐⭐⭐ Khó |
| **Tốc độ** | ⭐⭐⭐ Nhanh | ⭐⭐⭐ Nhanh | ⭐⭐ Chậm |
| **Ổn định** | ⭐⭐ Tạm | ⭐⭐⭐ Rất ổn | ⭐ Không ổn |
| **Chi phí** | ⭐⭐⭐ Miễn phí | ⭐⭐ Có phí | ⭐⭐⭐ Miễn phí |
| **Bảo mật** | ⭐⭐ Tạm | ⭐⭐⭐ Tốt | ⭐⭐ Tạm |

---

## 🎯 **KHUYẾN NGHỊ:**

### **Cho người mới bắt đầu:**
**Chọn NGROK** - Đơn giản, nhanh, không cần VPS

### **Cho dự án dài hạn:**
**Chọn VPS C2 Server** - Ổn định, chuyên nghiệp, IP cố định

### **Tránh xa:**
**Public IP Windows** - Nhiều vấn đề firewall, không ổn định

---

## 🚀 **BẮT ĐẦU NGAY:**

### **Cách 1: Ngrok (Đơn giản)**
```bash
python setup_ngrok_simple.py
```

### **Cách 2: VPS C2 Server (Ổn định)**
```bash
python setup_vps_c2_server.py
```

---

## ❓ **CÂU HỎI THƯỜNG GẶP:**

### **Q: Ngrok có an toàn không?**
**A:** Có, nhưng URL thay đổi mỗi lần restart. Tốt cho test, không tốt cho production.

### **Q: VPS có đắt không?**
**A:** Google Cloud có free tier, AWS có free tier. Chi phí thấp: $5-10/tháng.

### **Q: Có thể dùng cả hai không?**
**A:** Có! Dùng Ngrok để test, VPS để production.

---

## 📞 **HỖ TRỢ:**

Nếu gặp vấn đề:
1. Kiểm tra logs
2. Chạy test scripts
3. Đọc hướng dẫn chi tiết
4. Thử cách khác

**Chúc bạn thành công! 🎉**
