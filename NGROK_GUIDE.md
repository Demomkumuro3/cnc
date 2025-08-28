
NGROK TUNNEL - Cach don gian nhat de VPS ket noi Windows

Buoc 1: Download ngrok
# Windows
download_ngrok.bat

# Linux/Mac
chmod +x download_ngrok.sh
./download_ngrok.sh

Buoc 2: Dang ky tai khoan ngrok (mien phi)
1. Truy cap: https://ngrok.com/signup
2. Tao tai khoan mien phi
3. Lay authtoken tu dashboard

Buoc 3: Cau hinh ngrok
# Them authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE

# Test ngrok
ngrok version

Buoc 4: Tao tunnel den C2 Server
# Tren Windows, mo terminal moi
start_ngrok.bat

# Ket qua se hien thi:
# Forwarding    https://abc123.ngrok.io -> http://localhost:5000

Buoc 5: Su dung URL ngrok tren VPS
# Tren VPS, ket noi bot worker
python3 bot_worker_auto.py --server https://abc123.ngrok.io

Uu diem:
- Khong can mo port Windows
- Khong can quyen router
- Hoat dong ngay lap tuc
- Tu dong HTTPS

Nhuoc diem:
- URL thay doi moi lan restart
- Gioi han 1 tunnel (mien phi)
