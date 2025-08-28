# 🚀 C2 CNC - HỆ THỐNG COMMAND & CONTROL

## 📋 **Tổng quan**

Hệ thống C2 CNC cho phép bạn quản lý và điều khiển các bot worker từ xa thông qua nhiều phương pháp kết nối khác nhau.

## 🌟 **Tính năng chính**

- ✅ **C2 Server**: Máy chủ trung tâm quản lý bots
- ✅ **Bot Worker**: Client kết nối và thực thi lệnh
- ✅ **Web Interface**: Giao diện web để gửi lệnh
- ✅ **Command Line**: Giao diện dòng lệnh
- ✅ **Auto-recovery**: Tự động khôi phục khi mất kết nối
- ✅ **Multi-VPS**: Hỗ trợ nhiều VPS cùng lúc
- ✅ **Real-time**: Giao tiếp thời gian thực

## 🚀 **Các cách kết nối**

### **1. 🌐 Ngrok Tunnel (Khuyến nghị cho người mới)**
- **Ưu điểm**: Đơn giản, nhanh, không cần mở port
- **Nhược điểm**: URL thay đổi, giới hạn miễn phí
- **Phù hợp**: Test, demo, sử dụng tạm thời

### **2. 🏠 VPS làm C2 Server (Khuyến nghị cho dài hạn)**
- **Ưu điểm**: Ổn định, IP cố định, chuyên nghiệp
- **Nhược điểm**: Cần VPS, có chi phí
- **Phù hợp**: Production, dự án dài hạn

### **3. 🔥 Public IP Windows (Không khuyến nghị)**
- **Ưu điểm**: Miễn phí, trực tiếp
- **Nhược điểm**: Nhiều vấn đề firewall, không ổn định
- **Phù hợp**: Chỉ dành cho người có kinh nghiệm

## 📁 **Cấu trúc file**

```
viper/
├── c2_server_auto.py          # C2 Server chính
├── bot_worker_auto.py         # Bot Worker
├── command_interface.html     # Giao diện web
├── send_command.py            # Giao diện dòng lệnh
├── setup_ngrok_simple.py      # Setup Ngrok
├── setup_vps_c2_server.py     # Setup VPS C2 Server
├── setup_public_ip_c2.py      # Setup Public IP Windows
├── start_all_c2_methods.py    # Script tổng hợp
├── HUONG_DAN_SU_DUNG_C2_CNC.md # Hướng dẫn chi tiết
└── README_C2_CNC.md           # File này
```

## 🚀 **Bắt đầu nhanh**

### **Cách đơn giản nhất (Ngrok):**

```bash
# 1. Chạy script tổng hợp
python start_all_c2_methods.py

# 2. Chọn option 1 (Ngrok)
# 3. Làm theo hướng dẫn
```

### **Cách ổn định nhất (VPS):**

```bash
# 1. Chạy script tổng hợp
python start_all_c2_methods.py

# 2. Chọn option 2 (VPS C2 Server)
# 3. Làm theo hướng dẫn
```

## 📖 **Hướng dẫn chi tiết**

Xem file `HUONG_DAN_SU_DUNG_C2_CNC.md` để có hướng dẫn chi tiết cho từng cách.

## 🔧 **Yêu cầu hệ thống**

- **Python 3.7+**
- **Windows/Linux/Mac**
- **Internet connection**
- **VPS (cho option 2)**

## 📦 **Cài đặt dependencies**

```bash
pip install flask flask-socketio psutil requests
```

## 🎯 **Sử dụng cơ bản**

### **1. Khởi động C2 Server:**
```bash
python c2_server_auto.py
```

### **2. Kết nối Bot Worker:**
```bash
python bot_worker_auto.py --server http://SERVER_IP:5000
```

### **3. Gửi lệnh qua Web:**
Mở `command_interface.html` trong trình duyệt

### **4. Gửi lệnh qua Command Line:**
```bash
python send_command.py
```

## 🌐 **Giao diện Web**

- **URL**: Mở `command_interface.html` trong trình duyệt
- **Chức năng**: Xem danh sách bots, gửi lệnh, theo dõi trạng thái
- **Tương thích**: Chrome, Firefox, Safari, Edge

## 📱 **Giao diện Command Line**

- **Script**: `send_command.py`
- **Chế độ**: Interactive và Direct
- **Lệnh**: Hỗ trợ tất cả lệnh hệ thống

## 🔒 **Bảo mật**

- **Authentication**: Có thể thêm xác thực
- **Encryption**: Hỗ trợ HTTPS qua Ngrok
- **Firewall**: Tự động cấu hình firewall
- **Logging**: Ghi log đầy đủ

## 🚨 **Xử lý lỗi**

### **Lỗi kết nối:**
1. Kiểm tra C2 Server có đang chạy không
2. Kiểm tra firewall
3. Thử cách kết nối khác

### **Lỗi lệnh:**
1. Kiểm tra quyền thực thi
2. Kiểm tra đường dẫn
3. Xem logs để debug

## 📞 **Hỗ trợ**

Nếu gặp vấn đề:
1. Đọc hướng dẫn chi tiết
2. Chạy test scripts
3. Kiểm tra logs
4. Thử cách kết nối khác

## 🔄 **Cập nhật**

Để cập nhật hệ thống:
1. Backup dữ liệu hiện tại
2. Download phiên bản mới
3. Chạy lại setup scripts
4. Kiểm tra tương thích

## 📄 **Giấy phép**

Dự án này được phát hành dưới giấy phép MIT.

## 🤝 **Đóng góp**

Mọi đóng góp đều được chào đón! Hãy:
1. Fork dự án
2. Tạo branch mới
3. Commit thay đổi
4. Tạo Pull Request

---

## 🎉 **Chúc bạn thành công!**

Hệ thống C2 CNC này được thiết kế để đơn giản, mạnh mẽ và dễ sử dụng. Hãy bắt đầu với Ngrok nếu bạn mới làm quen, và chuyển sang VPS khi cần ổn định hơn.

**Happy Hacking! 🚀**
