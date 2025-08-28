@echo off
echo Starting C2 Server on Public IP...
echo.
echo This will make C2 Server accessible from internet!
echo.
echo Starting C2 Server on 0.0.0.0:5000...
python c2_server_auto.py
echo.
echo C2 Server stopped.
pause
