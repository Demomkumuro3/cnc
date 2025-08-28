@echo off
echo Force Opening Port 5000 for C2 Server...
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - OK
) else (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo Step 1: Removing all existing C2 Server rules...
netsh advfirewall firewall delete rule name="C2 Server*" 2>nul
netsh advfirewall firewall delete rule name="C2 Server Public IP*" 2>nul
netsh advfirewall firewall delete rule name="C2 Server Inbound" 2>nul
netsh advfirewall firewall delete rule name="C2 Server Outbound" 2>nul

echo.
echo Step 2: Adding new firewall rules...
echo Adding inbound rule for port 5000...
netsh advfirewall firewall add rule name="C2 Server Port 5000 Inbound" dir=in action=allow protocol=TCP localport=5000 enable=yes

echo Adding outbound rule for port 5000...
netsh advfirewall firewall add rule name="C2 Server Port 5000 Outbound" dir=out action=allow protocol=TCP localport=5000 enable=yes

echo Adding general inbound rule for C2 Server...
netsh advfirewall firewall add rule name="C2 Server General Inbound" dir=in action=allow protocol=TCP localport=5000 enable=yes

echo Adding general outbound rule for C2 Server...
netsh advfirewall firewall add rule name="C2 Server General Outbound" dir=out action=allow protocol=TCP localport=5000 enable=yes

echo.
echo Step 3: Checking firewall rules...
netsh advfirewall firewall show rule name="C2 Server*"

echo.
echo Step 4: Testing port accessibility...
echo Testing if port 5000 is accessible...
netstat -an | findstr :5000

echo.
echo Step 5: Windows Firewall setup completed!
echo.
echo If still not working, try these additional steps:
echo 1. Check Windows Defender Firewall settings
echo 2. Check antivirus software firewall settings
echo 3. Check router port forwarding
echo.
pause
