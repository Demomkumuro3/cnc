
Setup C2 Server tren Public IP de VPS ket noi truc tiep

Thong tin hien tai:
- Windows Public IP: 118.68.51.42
- C2 Server Port: 5000
- Target URL: http://118.68.51.42:5000

Buoc 1: Mo Windows Firewall
# Chay voi quyen Administrator
setup_public_ip_firewall.bat

Buoc 2: Khoi dong C2 Server tren Public IP
# Terminal 1: Khoi dong C2 Server
start_c2_public_ip.bat

Buoc 3: Test ket noi local
# Test tu Windows local
curl http://localhost:5000/api/bots
curl http://118.68.51.42:5000/api/bots

Buoc 4: Test tu VPS
# Upload script len VPS
scp test_public_ip_from_vps.sh root@<VPS_IP>:/tmp/

# Chay test tren VPS
chmod +x /tmp/test_public_ip_from_vps.sh
/tmp/test_public_ip_from_vps.sh

Buoc 5: Ket noi Bot Worker
# Tren VPS, ket noi bot worker
python3 bot_worker_auto.py --server http://118.68.51.42:5000

URLs sau khi setup:
- Windows Local: http://localhost:5000
- Windows Public: http://118.68.51.42:5000
- VPS Bot: http://118.68.51.42:5000

Luu y quan trong:
1. C2 Server phai bind tren 0.0.0.0:5000 (khong phai 127.0.0.1:5000)
2. Windows Firewall phai allow port 5000
3. C2 Server phai chay truoc khi test tu VPS
4. Public IP phai on dinh (khong thay doi thuong xuyen)

Troubleshooting:
- Neu VPS khong ket noi duoc: Kiem tra Windows firewall va C2 Server binding
- Neu port 5000 bi chan: Thay doi port trong c2_server_auto.py
- Neu public IP thay doi: Cap nhat URL tren VPS
