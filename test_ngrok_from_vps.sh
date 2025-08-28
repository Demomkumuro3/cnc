#!/bin/bash
# Test Ngrok Tunnel from VPS
# Run this on your VPS

echo "Testing Ngrok Tunnel..."
echo "========================"

# Get ngrok URL from user
read -p "Enter ngrok URL (e.g., https://abc123.ngrok.io): " NGROK_URL

if [ -z "$NGROK_URL" ]; then
    echo "No URL provided"
    exit 1
fi

echo "Testing connection to: $NGROK_URL"

# Test connection
if curl -s --connect-timeout 10 "$NGROK_URL/api/bots" > /dev/null; then
    echo "Ngrok tunnel is working!"
    echo "C2 Server accessible via: $NGROK_URL"
    echo ""
    echo "Now you can start bot worker:"
    echo "python3 bot_worker_auto.py --server $NGROK_URL"
else
    echo "Ngrok tunnel not accessible"
    echo "Check if:"
    echo "1. Ngrok is running on Windows"
    echo "2. C2 Server is running on port 5000"
    echo "3. URL is correct"
fi
