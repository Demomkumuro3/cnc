@echo off
echo Downloading ngrok...
echo.

REM Download ngrok
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo Download completed!
echo.

REM Extract ngrok
echo Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo.
echo Ngrok ready to use!
echo.
echo Next steps:
echo 1. Sign up at https://ngrok.com/signup
echo 2. Get your authtoken from dashboard
echo 3. Run: ngrok config add-authtoken YOUR_TOKEN
echo 4. Run: ngrok http 5000
echo.
pause
