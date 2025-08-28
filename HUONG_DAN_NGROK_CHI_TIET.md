# 🌐 HƯỚNG DẪN CHI TIẾT SETUP NGROK CHO C2 CNC

## 📋 **Tổng quan**

Ngrok là cách **đơn giản nhất** để VPS kết nối đến Windows C2 Server mà không cần mở port hay cấu hình firewall.

---

## 🎯 **Kết quả mong đợi**

Sau khi setup xong:
- ✅ VPS có thể kết nối đến Windows C2 Server
- ✅ Không cần mở port Windows
- ✅ Không cần quyền router
- ✅ Tự động HTTPS
- ✅ Hoạt động ngay lập tức

---

## 🚀 **BƯỚC 1: TẠO SCRIPTS NGROK**

### **1.1 Chạy script setup:**
```bash
python setup_ngrok_simple.py
```

### **1.2 Kiểm tra files đã tạo:**
- ✅ `download_ngrok.bat` - Download ngrok cho Windows
- ✅ `start_ngrok.bat` - Khởi động ngrok tunnel
- ✅ `test_ngrok_from_vps.sh` - Test từ VPS
- ✅ `NGROK_GUIDE.md` - Hướng dẫn ngrok

---

## 📥 **BƯỚC 2: DOWNLOAD NGROK**

### **2.1 Chạy script download:**
```bash
# Windows
download_ngrok.bat
```

### **2.2 Kết quả mong đợi:**
```
Downloading ngrok...
Download completed!

Extracting ngrok...
Ngrok ready to use!

Next steps:
1. Sign up at https://ngrok.com/signup
2. Get your authtoken from dashboard
3. Run: ngrok config add-authtoken YOUR_TOKEN
4. Run: ngrok http 5000
```

### **2.3 Kiểm tra ngrok:**
```bash
ngrok version
```

**Kết quả mong đợi:**
```
ngrok version 3.x.x
```

---

## 🔐 **BƯỚC 3: ĐĂNG KÝ TÀI KHOẢN NGROK**

### **3.1 Truy cập website:**
```
https://ngrok.com/signup
```

### **3.2 Tạo tài khoản:**
- Nhập email
- Nhập mật khẩu
- Xác nhận email
- Đăng nhập

### **3.3 Lấy authtoken:**
1. Đăng nhập vào dashboard
2. Vào menu "Your Authtoken"
3. Copy authtoken (dạng: `2abc123def456ghi789jkl`)

---

## ⚙️ **BƯỚC 4: CẤU HÌNH NGROK**

### **4.1 Thêm authtoken:**
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

**Ví dụ:**
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl
```

### **4.2 Kiểm tra cấu hình:**
```bash
ngrok config check
```

**Kết quả mong đợi:**
```
✓ authtoken from command line: 2abc123def456ghi789jkl
✓ authtoken from environment variable: 
✓ authtoken from config file: 2abc123def456ghi789jkl
```

---

## 🖥️ **BƯỚC 5: KHỞI ĐỘNG C2 SERVER**

### **5.1 Mở terminal mới:**
```bash
python c2_server_auto.py
```

### **5.2 Kết quả mong đợi:**
```
C2 Server starting...
C2 Server running on http://0.0.0.0:5000
```

### **5.3 Kiểm tra C2 Server:**
Mở trình duyệt: `http://localhost:5000`

**Kết quả mong đợi:** Hiển thị giao diện C2 Server

---

## 🌐 **BƯỚC 6: TẠO NGROK TUNNEL**

### **6.1 Mở terminal mới (giữ C2 Server chạy):**
```bash
start_ngrok.bat
```

### **6.2 Kết quả mong đợi:**
```
Starting Ngrok Tunnel for C2 Server...

Make sure C2 Server is running on port 5000 first!

Starting ngrok...
```

**Sau đó hiển thị:**
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                       United States (us)
Latency                      21ms
Web Interface                http://127.0.0.1:4040
Forwarding                   https://abc123.ngrok.io -> http://localhost:5000
```

### **6.3 Copy URL ngrok:**
**Quan trọng:** Copy URL `https://abc123.ngrok.io` (URL sẽ khác mỗi lần)

---

## 🧪 **BƯỚC 7: TEST TỪ VPS**

### **7.1 Upload test script lên VPS:**
```bash
# Trên VPS
chmod +x test_ngrok_from_vps.sh
./test_ngrok_from_vps.sh
```

### **7.2 Nhập URL ngrok khi được yêu cầu:**
```
Enter ngrok URL (e.g., https://abc123.ngrok.io): https://abc123.ngrok.io
```

### **7.3 Kết quả mong đợi:**
```
Testing Ngrok Tunnel...
================================
Testing connection to: https://abc123.ngrok.io

Ngrok tunnel is working!
C2 Server accessible via: https://abc123.ngrok.io

Now you can start bot worker:
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

---

## 🤖 **BƯỚC 8: KẾT NỐI BOT WORKER**

### **8.1 Trên VPS, kết nối bot worker:**
```bash
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

### **8.2 Kết quả mong đợi:**
```
Bot Worker starting...
Connecting to C2 Server: https://abc123.ngrok.io
Registration successful!
Bot ID: bot_12345
Status: Online
```

---

## 🌐 **BƯỚC 9: KIỂM TRA KẾT NỐI**

### **9.1 Trên Windows, mở giao diện web:**
```
http://localhost:5000
```

### **9.2 Kiểm tra danh sách bots:**
- Bot từ VPS sẽ hiển thị trong danh sách
- Status: Online
- IP: IP của VPS

### **9.3 Gửi lệnh test:**
```
ping google.com
```

**Kết quả mong đợi:** Bot thực thi lệnh và trả về kết quả

---

## ❌ **XỬ LÝ LỖI THƯỜNG GẶP**

### **Lỗi 1: "ngrok command not found"**
**Nguyên nhân:** Ngrok chưa được download hoặc PATH chưa đúng
**Giải pháp:** Chạy lại `download_ngrok.bat`

### **Lỗi 2: "authtoken invalid"**
**Nguyên nhân:** Authtoken sai hoặc hết hạn
**Giải pháp:** Lấy lại authtoken từ dashboard ngrok

### **Lỗi 3: "tunnel already in use"**
**Nguyên nhân:** Ngrok đang chạy ở nơi khác
**Giải pháp:** Dừng tất cả ngrok và chạy lại

### **Lỗi 4: "C2 Server not accessible"**
**Nguyên nhân:** C2 Server chưa chạy hoặc sai port
**Giải pháp:** Kiểm tra C2 Server có đang chạy trên port 5000 không

---

## 🔄 **SỬ DỤNG HÀNG NGÀY**

### **Mỗi lần sử dụng:**
1. Khởi động C2 Server: `python c2_server_auto.py`
2. Tạo ngrok tunnel: `start_ngrok.bat`
3. Copy URL ngrok mới
4. Kết nối bot worker với URL mới

### **Lưu ý quan trọng:**
- ⚠️ URL ngrok thay đổi mỗi lần restart
- ⚠️ Cần copy URL mới mỗi lần
- ⚠️ Bot worker cần kết nối lại với URL mới

---

## 📊 **SO SÁNH VỚI CÁC CÁCH KHÁC**

| Tiêu chí | Ngrok | VPS C2 Server | Public IP Windows |
|----------|-------|---------------|-------------------|
| **Độ khó** | ⭐ Dễ | ⭐⭐ Trung bình | ⭐⭐⭐ Khó |
| **Tốc độ** | ⭐⭐⭐ Nhanh | ⭐⭐⭐ Nhanh | ⭐⭐ Chậm |
| **Ổn định** | ⭐⭐ Tạm | ⭐⭐⭐ Rất ổn | ⭐ Không ổn |
| **Chi phí** | ⭐⭐⭐ Miễn phí | ⭐⭐ Có phí | ⭐⭐⭐ Miễn phí |

---

## 🎯 **KHUYẾN NGHỊ**

### **Sử dụng Ngrok khi:**
- ✅ Test và demo
- ✅ Sử dụng tạm thời
- ✅ Không có VPS
- ✅ Muốn setup nhanh

### **Chuyển sang VPS khi:**
- 🔄 Cần ổn định dài hạn
- 🔄 Không muốn URL thay đổi
- 🔄 Có ngân sách cho VPS
- 🔄 Cần bảo mật cao

---

## 🚀 **BƯỚC TIẾP THEO**

Sau khi setup Ngrok thành công:

1. **Test kết nối** từ VPS
2. **Kết nối bot worker** với URL ngrok
3. **Gửi lệnh test** qua giao diện web
4. **Sử dụng thực tế** cho dự án

---

## 📞 **HỖ TRỢ**

Nếu gặp vấn đề:
1. Kiểm tra từng bước trên
2. Xem logs ngrok và C2 Server
3. Test kết nối từng bước
4. Thử restart ngrok và C2 Server

---

## 🎉 **CHÚC MỪNG!**

Bạn đã setup thành công Ngrok cho C2 CNC! 

**VPS giờ đây có thể kết nối trực tiếp đến Windows C2 Server mà không cần mở port hay firewall!**

**Happy Hacking! 🚀**
