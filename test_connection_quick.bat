@echo off
echo Quick Test C2 Server Connection...
echo.

echo Step 1: Check if C2 Server is running...
netstat -an | findstr :5000
if %errorLevel% == 0 (
    echo C2 Server is running on port 5000
) else (
    echo ERROR: C2 Server is NOT running on port 5000
    echo Please start C2 Server first with: start_c2_public_ip.bat
    pause
    exit /b 1
)

echo.
echo Step 2: Test local connection...
curl -s http://localhost:5000/api/bots >nul 2>&1
if %errorLevel% == 0 (
    echo Local connection: SUCCESS
) else (
    echo Local connection: FAILED
)

echo.
echo Step 3: Test public IP connection...
curl -s http://118.68.51.42:5000/api/bots >nul 2>&1
if %errorLevel% == 0 (
    echo Public IP connection: SUCCESS
    echo VPS can now connect to: http://118.68.51.42:5000
) else (
    echo Public IP connection: FAILED
    echo This means VPS cannot connect from internet
    echo.
    echo Possible issues:
    echo 1. Windows Firewall blocking port 5000
    echo 2. Antivirus software blocking
    echo 3. Router not forwarding port 5000
    echo 4. ISP blocking incoming connections
)

echo.
echo Step 4: Check firewall rules...
netsh advfirewall firewall show rule name="C2 Server*"

echo.
echo Test completed!
pause
