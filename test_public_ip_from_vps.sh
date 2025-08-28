#!/bin/bash
# Test Connection to Windows C2 Server on Public IP
# Run this on your VPS

echo "Testing Connection to Windows C2 Server..."
echo "=============================================="
echo "Target: 118.68.51.42:5000"
echo ""

# Test 1: Ping
echo "Test 1: Ping..."
if ping -c 1 118.68.51.42 > /dev/null 2>&1; then
    echo "   Ping successful"
else
    echo "   Ping failed (this is normal for some ISPs)"
fi

# Test 2: Port check
echo "Test 2: Port 5000 check..."
if nc -z -w5 118.68.51.42 5000 2>/dev/null; then
    echo "   Port 5000 is open"
else
    echo "   Port 5000 is closed"
    echo "   Check if C2 Server is running on Windows"
    exit 1
fi

# Test 3: HTTP connection
echo "Test 3: HTTP connection..."
if curl -s --connect-timeout 10 "http://118.68.51.42:5000/api/bots" > /dev/null; then
    echo "   HTTP connection successful!"
    echo "   C2 Server is accessible from VPS!"
    echo ""
    echo "SUCCESS! Now you can connect bot worker:"
    echo "python3 bot_worker_auto.py --server http://118.68.51.42:5000"
else
    echo "   HTTP connection failed"
    echo "   Check if:"
    echo "      1. C2 Server is running on Windows"
    echo "      2. Windows firewall allows port 5000"
    echo "      3. C2 Server binds on 0.0.0.0:5000"
    exit 1
fi

echo ""
echo "Test completed!"
