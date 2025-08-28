@echo off
echo Fixing Windows Firewall for C2 Server...
echo.

REM Remove existing rules if any
echo Removing existing C2 Server rules...
netsh advfirewall firewall delete rule name="C2 Server Public IP Inbound" 2>nul
netsh advfirewall firewall delete rule name="C2 Server Public IP Outbound" 2>nul

REM Add inbound rule
echo Adding inbound firewall rule...
netsh advfirewall firewall add rule name="C2 Server Public IP Inbound" dir=in action=allow protocol=TCP localport=5000

REM Add outbound rule
echo Adding outbound firewall rule...
netsh advfirewall firewall add rule name="C2 Server Public IP Outbound" dir=out action=allow protocol=TCP localport=5000

REM Show the rules
echo.
echo Checking firewall rules...
netsh advfirewall firewall show rule name="C2 Server Public IP*"

echo.
echo Windows Firewall setup completed!
echo C2 Server should now be accessible from internet
echo.
pause
