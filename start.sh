#!/bin/bash

# Start Xvfb (Virtual framebuffer)
echo "🖥️ Starting virtual display..."
Xvfb :99 -screen 0 ${SCREEN_WIDTH}x${SCREEN_HEIGHT}x${SCREEN_DEPTH} -ac +extension GLX +render -noreset &
XVFB_PID=$!

# Wait for Xvfb to be ready
echo "⏳ Waiting for X server to be ready..."
timeout=30
counter=0
while [ $counter -lt $timeout ]; do
    if xdpyinfo -display :99 >/dev/null 2>&1; then
        echo "✅ X server is ready!"
        break
    fi
    sleep 1
    counter=$((counter + 1))
done

if [ $counter -eq $timeout ]; then
    echo "❌ X server failed to start within $timeout seconds"
    exit 1
fi

# Start window manager
echo "🪟 Starting window manager..."
DISPLAY=:99 fluxbox &
sleep 2

# Start VNC server
echo "🔗 Starting VNC server on :5900..."
x11vnc -display :99 -nopw -shared -forever -xkb -ncache 10 -ncache_cr -rfbport 5900 &
VNC_PID=$!
sleep 2

# Start noVNC for browser access
echo "🌐 Starting noVNC web interface on :6080..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &
NOVNC_PID=$!

# Wait a moment for services to start
sleep 3

echo "✅ VNC Server started!"
echo "📺 Connect via VNC: localhost:5900 (password: secret)"
echo "🌐 Connect via browser: http://localhost:6080"

# Start the Flask API for evaluation
echo "🚀 Starting Flask API on port 5000 (internal)..."
python api.py &
FLASK_PID=$!

echo "🔥 Flask API started!"
echo "🌐 API available at: http://localhost:${API_PORT:-5001}"
echo "📋 Health check: http://localhost:${API_PORT:-5001}/health"
echo "🚢 Track booking: POST http://localhost:${API_PORT:-5001}/track"

# Wait a moment for API to start
sleep 2

# Start the visual automation for students to see
echo "🎬 Starting visual automation demo..."
python main-simple-test.py &
DEMO_PID=$!

echo "✅ All services started!"
echo "🎯 Students can see browser automation on VNC"
echo "🤖 Evaluation container can call API endpoints"
echo ""
echo "=== CONNECTION INFO ==="
echo "📺 VNC Viewer: localhost:5900"  
echo "🌐 Web VNC: http://localhost:6080"
echo "🔗 API: http://localhost:${API_PORT:-5001}"

# Keep container running - wait for all background processes
echo ""
echo "🔄 All services running. Container will stay alive."
wait 