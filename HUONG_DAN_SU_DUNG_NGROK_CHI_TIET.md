# 🌐 HƯỚNG DẪN SỬ DỤNG NGROK CHI TIẾT - C2 CNC

## 📋 **Tổng quan**

Hướng dẫn này sẽ dạy bạn **từng bước cụ thể** cách setup và sử dụng Ngrok để VPS kết nối đến Windows C2 Server.

---

## 🎯 **Kết quả cuối cùng**

Sau khi làm theo hướng dẫn này:
- ✅ VPS có thể kết nối đến Windows C2 Server
- ✅ Không cần mở port Windows
- ✅ Không cần cấu hình firewall
- ✅ Hoạt động ngay lập tức

---

## 🚀 **BƯỚC 1: TẠO SCRIPTS NGROK**

### **1.1 Mở Command Prompt**
- Nhấn `Windows + R`
- Gõ `cmd` và nhấn Enter

### **1.2 Di chuyển đến thư mục dự án**
```cmd
cd C:\Users\cuten\Desktop\viper
```

### **1.3 Chạy script setup**
```cmd
python setup_ngrok_simple.py
```

### **1.4 Kết quả mong đợi:**
```
Creating Ngrok Download Script...
   Ngrok download script created: download_ngrok.bat

Creating Ngrok Start Script...
   Ngrok start script created: start_ngrok.bat

Creating VPS Ngrok Test Script...
   VPS ngrok test script created: test_ngrok_from_vps.sh

Creating Ngrok Guide...
   Ngrok guide created: NGROK_GUIDE.md

Ngrok setup completed!
```

### **1.5 Kiểm tra files đã tạo:**
```cmd
dir *.bat
dir *.sh
dir *.md
```

**Bạn sẽ thấy:**
- `download_ngrok.bat`
- `start_ngrok.bat`
- `test_ngrok_from_vps.sh`
- `NGROK_GUIDE.md`

---

## 📥 **BƯỚC 2: DOWNLOAD NGROK**

### **2.1 Chạy script download**
```cmd
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

### **2.3 Kiểm tra ngrok đã cài đặt**
```cmd
ngrok version
```

**Kết quả mong đợi:**
```
ngrok version 3.x.x
```

---

## 🔐 **BƯỚC 3: ĐĂNG KÝ TÀI KHOẢN NGROK**

### **3.1 Mở trình duyệt web**
- Mở Chrome, Firefox, hoặc Edge

### **3.2 Truy cập website ngrok**
```
https://ngrok.com/signup
```

### **3.3 Tạo tài khoản**
1. **Nhập email:** `your-email@example.com`
2. **Nhập mật khẩu:** `your-password-here`
3. **Click "Sign up for free"**
4. **Xác nhận email** (kiểm tra inbox)

### **3.4 Đăng nhập**
1. Quay lại: https://ngrok.com
2. Click **"Sign in"**
3. Nhập email và mật khẩu

---

## 🔑 **BƯỚC 4: LẤY AUTHTOKEN**

### **4.1 Vào dashboard**
Sau khi đăng nhập, bạn sẽ thấy dashboard

### **4.2 Tìm Your Authtoken**
**Cách 1: Menu bên trái**
- Nhìn menu bên trái
- Tìm **"Your Authtoken"**
- Click vào đó

**Cách 2: Menu dropdown**
- Click vào **tên/email** của bạn (góc trên bên phải)
- Chọn **"Your Authtoken"**

**Cách 3: Trực tiếp**
- Truy cập: https://dashboard.ngrok.com/get-started/your-authtoken

### **4.3 Copy authtoken**
- Bạn sẽ thấy chuỗi dài: `2abc123def456ghi789jkl0mnopqrstuvwxyz`
- Click **"Copy"** button
- **Lưu ý:** Đây là thông tin bảo mật, đừng chia sẻ!

---

## ⚙️ **BƯỚC 5: CẤU HÌNH NGROK**

### **5.1 Mở Command Prompt mới**
- Nhấn `Windows + R`
- Gõ `cmd` và nhấn Enter

### **5.2 Di chuyển đến thư mục dự án**
```cmd
cd C:\Users\cuten\Desktop\viper
```

### **5.3 Thêm authtoken**
```cmd
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

**Ví dụ:**
```cmd
ngrok config add-authtoken 2abc123def456ghi789jkl0mnopqrstuvwxyz
```

### **5.4 Kiểm tra cấu hình**
```cmd
ngrok config check
```

**Kết quả mong đợi:**
```
✓ authtoken from command line: 2abc123def456ghi789jkl0mnopqrstuvwxyz
✓ authtoken from environment variable: 
✓ authtoken from config file: 2abc123def456ghi789jkl0mnopqrstuvwxyz
```

---

## 🖥️ **BƯỚC 6: KHỞI ĐỘNG C2 SERVER**

### **6.1 Mở Command Prompt mới**
- Nhấn `Windows + R`
- Gõ `cmd` và nhấn Enter

### **6.2 Di chuyển đến thư mục dự án**
```cmd
cd C:\Users\cuten\Desktop\viper
```

### **6.3 Khởi động C2 Server**
```cmd
python c2_server_auto.py
```

### **6.4 Kết quả mong đợi:**
```
C2 Server starting...
C2 Server running on http://0.0.0.0:5000
```

### **6.5 Kiểm tra C2 Server**
- Mở trình duyệt mới
- Truy cập: `http://localhost:5000`
- **Giữ terminal C2 Server mở!**

---

## 🌐 **BƯỚC 7: TẠO NGROK TUNNEL**

### **7.1 Mở Command Prompt mới (giữ C2 Server chạy)**
- Nhấn `Windows + R`
- Gõ `cmd` và nhấn Enter

### **7.2 Di chuyển đến thư mục dự án**
```cmd
cd C:\Users\cuten\Desktop\viper
```

### **7.3 Tạo ngrok tunnel**
```cmd
start_ngrok.bat
```

### **7.4 Kết quả mong đợi:**
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

### **7.5 Copy URL ngrok**
**Quan trọng:** Copy URL `https://abc123.ngrok.io` (URL sẽ khác mỗi lần)

---

## 🧪 **BƯỚC 8: TEST TỪ VPS**

### **8.1 Upload test script lên VPS**
- Sử dụng SCP, SFTP, hoặc copy-paste
- Upload `test_ngrok_from_vps.sh` lên VPS

### **8.2 Trên VPS, chạy test script**
```bash
chmod +x test_ngrok_from_vps.sh
./test_ngrok_from_vps.sh
```

### **8.3 Nhập URL ngrok khi được yêu cầu**
```
Enter ngrok URL (e.g., https://abc123.ngrok.io): https://abc123.ngrok.io
```

### **8.4 Kết quả mong đợi:**
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

## 🤖 **BƯỚC 9: KẾT NỐI BOT WORKER**

### **9.1 Trên VPS, kết nối bot worker**
```bash
python3 bot_worker_auto.py --server https://abc123.ngrok.io
```

### **9.2 Kết quả mong đợi:**
```
Bot Worker starting...
Connecting to C2 Server: https://abc123.ngrok.io
Registration successful!
Bot ID: bot_12345
Status: Online
```

---

## 🌐 **BƯỚC 10: KIỂM TRA KẾT NỐI**

### **10.1 Trên Windows, mở giao diện web**
- Mở trình duyệt
- Truy cập: `http://localhost:5000`

### **10.2 Kiểm tra danh sách bots**
- Bot từ VPS sẽ hiển thị trong danh sách
- Status: Online
- IP: IP của VPS

### **10.3 Gửi lệnh test**
- Nhập lệnh: `ping google.com`
- Click "Send Command"
- Bot sẽ thực thi và trả về kết quả

---

## ❌ **XỬ LÝ LỖI THƯỜNG GẶP**

### **Lỗi 1: "ngrok command not found"**
**Nguyên nhân:** Ngrok chưa được download hoặc PATH chưa đúng
**Giải pháp:** 
1. Chạy lại `download_ngrok.bat`
2. Kiểm tra file `ngrok.exe` có trong thư mục không

### **Lỗi 2: "authtoken invalid"**
**Nguyên nhân:** Authtoken sai hoặc hết hạn
**Giải pháp:**
1. Vào dashboard ngrok
2. Lấy lại authtoken mới
3. Chạy: `ngrok config add-authtoken NEW_TOKEN`

### **Lỗi 3: "tunnel already in use"**
**Nguyên nhân:** Ngrok đang chạy ở nơi khác
**Giải pháp:**
1. Dừng tất cả ngrok
2. Chạy: `taskkill /f /im ngrok.exe`
3. Chạy lại `start_ngrok.bat`

### **Lỗi 4: "C2 Server not accessible"**
**Nguyên nhân:** C2 Server chưa chạy hoặc sai port
**Giải pháp:**
1. Kiểm tra C2 Server có đang chạy không
2. Kiểm tra port 5000 có bị chiếm không
3. Restart C2 Server

---

## 🔄 **SỬ DỤNG HÀNG NGÀY**

### **Mỗi lần sử dụng:**
1. **Khởi động C2 Server:**
   ```cmd
   python c2_server_auto.py
   ```

2. **Tạo ngrok tunnel:**
   ```cmd
   start_ngrok.bat
   ```

3. **Copy URL ngrok mới** (quan trọng!)

4. **Kết nối bot worker với URL mới:**
   ```bash
   python3 bot_worker_auto.py --server https://NEW_URL.ngrok.io
   ```

### **Lưu ý quan trọng:**
- ⚠️ **URL ngrok thay đổi mỗi lần restart**
- ⚠️ **Cần copy URL mới mỗi lần**
- ⚠️ **Bot worker cần kết nối lại với URL mới**

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
1. **Kiểm tra từng bước** trên
2. **Xem logs** ngrok và C2 Server
3. **Test kết nối** từng bước
4. **Thử restart** ngrok và C2 Server

---

## 🎉 **CHÚC MỪNG!**

Bạn đã setup thành công Ngrok cho C2 CNC! 

**VPS giờ đây có thể kết nối trực tiếp đến Windows C2 Server mà không cần mở port hay firewall!**

**Happy Hacking! 🚀**
