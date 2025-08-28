@echo off
echo Setting up Windows Firewall for Public IP C2 Server...
echo.
echo This will allow external connections to port 5000
echo.

REM Allow inbound connections on port 5000
echo Adding inbound firewall rule...
netsh advfirewall firewall add rule name="C2 Server Public IP Inbound" dir=in action=allow protocol=TCP localport=5000

REM Allow outbound connections on port 5000
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
