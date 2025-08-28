@echo off
echo Starting Ngrok Tunnel for C2 Server...
echo.
echo Make sure C2 Server is running on port 5000 first!
echo.
echo Starting ngrok...
ngrok http 5000
echo.
echo Ngrok tunnel stopped.
pause
