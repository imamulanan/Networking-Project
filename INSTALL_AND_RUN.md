# 🚀 COMPLETE INSTALLATION & RUN GUIDE

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install flask flask-socketio flask-cors pillow opencv-python
```

### Step 2: Start Web Server
```bash
python WebServer.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

**Then use the web interface to control everything!** 🎉

---

## 📋 Detailed Installation Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Internet connection (for package download)

### Verify Python Installation
```bash
python --version
# Should show: Python 3.7.x or higher

pip --version
# Should show pip version
```

### Install All Dependencies
```bash
# Navigate to project directory
cd "e:\Academic\5th Semester\Computer Network(CIT-313)\anan"

# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install flask==3.0.0
pip install flask-socketio==5.3.5
pip install flask-cors==4.0.0
pip install pillow==10.1.0
pip install opencv-python==4.8.1.78
```

### Verify Installation
```bash
# Test Flask
python -c "import flask; print(flask.__version__)"
# Should print: 3.0.0

# Test Flask-SocketIO
python -c "import flask_socketio; print(flask_socketio.__version__)"
# Should print: 5.3.5

# Test Flask-CORS
python -c "import flask_cors; print(flask_cors.__version__)"
# Should print: 4.0.0

# Test Pillow
python -c "import PIL; print(PIL.__version__)"
# Should print: 10.1.0

# Test OpenCV
python -c "import cv2; print(cv2.__version__)"
# Should print: 4.8.1.78
```

---

## 🎮 Running the System

### Method 1: One-Command Startup (Recommended) ⭐

```bash
# Step 1: Start Web Server (only command needed!)
python WebServer.py

# You should see:
# ============================================================
#   RTSP/RTP Video Streaming - Web Browser Version
# ============================================================
# 
# [WebServer] Starting web server...
# [WebServer] Open your browser and go to: http://localhost:5000
# [WebServer] Use the web interface to control the RTSP server
# [WebServer] Press Ctrl+C to stop
```

```bash
# Step 2: Open browser
# Go to: http://localhost:5000
```

```bash
# Step 3: Use Web Interface
# 1. Click "Start Server" button (wait for green status 🟢)
# 2. Click "Setup" button
# 3. Click "Play" button
# 4. Watch the video! 🎥
```

### Method 2: Pre-Started Server (Alternative)

If you want to run Server.py separately:

**Terminal 1:**
```bash
python Server.py

# You should see:
# ============================================================
#   RTSP/RTP Video Streaming Server
# ============================================================
# [Server] RTSP server listening on port 8554...
```

**Terminal 2:**
```bash
python WebServer.py

# You should see web server starting message
```

**Browser:**
```
http://localhost:5000
# Skip "Start Server" step
# Go directly to Setup → Play
```

---

## 🔧 Troubleshooting

### Problem: "Import flask could not be resolved"

**Solution:**
```bash
# Reinstall Flask
pip uninstall flask
pip install flask==3.0.0

# Or upgrade pip first
python -m pip install --upgrade pip
pip install flask==3.0.0
```

### Problem: "Port 5000 already in use"

**Solution Option 1 - Kill Process:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution Option 2 - Change Port:**
Edit `WebServer.py`, line ~480:
```python
# Change from:
socketio.run(app, host='0.0.0.0', port=5000, debug=False)

# To:
socketio.run(app, host='0.0.0.0', port=5001, debug=False)
```

Then open browser to: `http://localhost:5001`

### Problem: "Port 8554 already in use"

**Solution:**
```bash
# Find and kill process using port 8554
netstat -ano | findstr :8554
taskkill /PID <PID> /F

# Or kill all Python processes
Get-Process python | Stop-Process -Force

# Then restart WebServer.py
python WebServer.py
```

### Problem: "Server won't start" (clicking Start Server button does nothing)

**Diagnosis:**
1. Check Activity Log in web interface for errors
2. Check terminal where WebServer.py is running for error messages

**Solutions:**

**If Server.py file not found:**
```bash
# Make sure you're in the correct directory
cd "e:\Academic\5th Semester\Computer Network(CIT-313)\anan"

# Verify Server.py exists
dir Server.py
```

**If Python not found:**
```bash
# Make sure Python is in PATH
python --version

# If not working, use full path in WebServer.py
# Edit line with subprocess.Popen to use:
# 'C:\\Python39\\python.exe' instead of sys.executable
```

### Problem: "Video not playing"

**Checklist:**
- [ ] Is Server status showing "Running" 🟢?
- [ ] Did you click "Setup" first?
- [ ] Is "Play" button enabled?
- [ ] Does `video/movie.Mjpeg` file exist?

**Solutions:**

**Check video file:**
```bash
dir video\movie.Mjpeg
```

**If video file missing, create it:**
```bash
python VideoPrep.py
# Choose option 2: "Generate test video"
```

**Check Activity Log:**
- Look for error messages in red
- Common issues: Connection refused, Timeout, File not found

### Problem: "WebSocket connection failed"

**Solution:**
```bash
# Refresh browser page
# Press F5 or Ctrl+R

# Or close and reopen browser

# If still failing, restart WebServer.py
# Ctrl+C in terminal
python WebServer.py
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt

# Or install missing module specifically
pip install <module_name>
```

---

## 🎯 Verification Tests

### Test 1: Basic Startup
```bash
# Run
python WebServer.py

# Expected Output:
# ============================================================
#   RTSP/RTP Video Streaming - Web Browser Version
# ============================================================
# [WebServer] Starting web server...
# [WebServer] Open your browser and go to: http://localhost:5000

# Result: ✅ Web server starts without errors
```

### Test 2: Web Interface Loads
```bash
# Open browser: http://localhost:5000

# Expected:
# - Page loads with title "RTSP/RTP Video Streaming System"
# - Server Control panel visible
# - Video display area visible
# - Control buttons visible
# - Statistics panel visible
# - Activity log visible

# Result: ✅ Web interface displays correctly
```

### Test 3: Server Start
```bash
# In browser:
# 1. Click "Start Server" button

# Expected in Terminal:
# [WebServer] RTSP Server started successfully

# Expected in Browser:
# - Server status changes to "Running" 🟢
# - Activity log shows: "Server started"
# - "Start Server" button disabled
# - "Stop Server" button enabled

# Result: ✅ Server starts successfully
```

### Test 4: Video Streaming
```bash
# In browser:
# 1. Ensure server is running (🟢)
# 2. Click "Setup" button
# 3. Wait for "Play" button to enable
# 4. Click "Play" button

# Expected:
# - Video frames appear in video display area
# - Frame number increases
# - Packets number increases
# - Data rate shows value (~250 kbps)
# - FPS shows value (~20)

# Result: ✅ Video streams successfully
```

### Test 5: Complete Workflow
```bash
# Full test sequence:
# 1. Start Server → 🟢 Running
# 2. Setup → Session established
# 3. Play → Video streaming
# 4. Pause → Video paused
# 5. Play → Video resumes
# 6. Teardown → Session ended
# 7. Stop Server → 🔴 Stopped

# Result: ✅ All controls work correctly
```

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10 or higher
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 2 GB
- **Storage**: 100 MB free space
- **Python**: 3.7 or higher
- **Network**: Localhost (127.0.0.1)

### Recommended Requirements
- **OS**: Windows 10/11
- **CPU**: Quad-core 2.5 GHz
- **RAM**: 4 GB or more
- **Storage**: 500 MB free space
- **Python**: 3.9 or higher
- **Network**: Gigabit Ethernet or WiFi

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+ (macOS)
- ⚠️ Internet Explorer (NOT supported)

---

## 🌐 Network Configuration

### Local Access (Same Computer)
```
URL: http://localhost:5000
No configuration needed
```

### Same Network Access (Other Devices)

**Step 1: Find Your IP Address**
```bash
ipconfig
# Look for "IPv4 Address"
# Example: 192.168.1.100
```

**Step 2: Allow Firewall**
```bash
# Windows Firewall - Allow ports:
# - Port 5000 (Web Server)
# - Port 8554 (RTSP Server)
# - Ports 25000-26000 (RTP)
```

**Step 3: Access from Other Device**
```
From other device's browser:
http://192.168.1.100:5000

In web interface:
Change "Server Address" from "localhost" to "192.168.1.100"
```

---

## 🎓 For Academic Demonstration

### Pre-Presentation Setup (15 minutes before class)

**1. Verify Installation:**
```bash
python --version
pip list | findstr flask
```

**2. Test Run:**
```bash
python WebServer.py
# Test in browser
# Verify all buttons work
# Close when done (Ctrl+C)
```

**3. Prepare Browser:**
```
- Open Chrome/Firefox
- Bookmark: http://localhost:5000
- Close unnecessary tabs
- Zoom to comfortable level (Ctrl+0)
```

**4. Have Backup Ready:**
```
- Print QUICK_REFERENCE.md
- Open documentation files
- Note down any issues
```

### During Presentation (5 minutes)

**Script:**

```
[Terminal - 30 seconds]
"Let me start the system with one command:"
> python WebServer.py
[Wait for startup message]

[Browser - 30 seconds]
"Opening the web interface:"
[Type: http://localhost:5000]
[Show the interface]

[Explain UI - 1 minute]
"Here we have:
- Server control panel to start the RTSP server
- Video display area for live streaming
- Control buttons for RTSP operations
- Real-time statistics
- Activity log showing all events"

[Demo - 2 minutes]
"Let me demonstrate:"
[Click Start Server] "Starting the RTSP/RTP server"
[Point to green status] "Server is now running"
[Click Setup] "Establishing RTSP connection"
[Click Play] "Starting video stream using RTP protocol"
[Point to video] "Here's the live video"
[Point to statistics] "Real-time statistics updating"
[Point to log] "Activity log showing RTSP operations"
[Click Pause] "Pause the stream"
[Click Play] "Resume playback"
[Click Teardown] "End the session"
[Click Stop Server] "Stop the server"

[Conclusion - 1 minute]
"This system demonstrates:
- Complete RTSP/1.0 protocol implementation
- RTP (RFC 3550) for real-time media transport
- Modern web interface with Flask and WebSocket
- Real-time video streaming
- Professional UI with complete control
- All from a web browser!"
```

---

## 💾 Backup & Recovery

### Backup Before Presentation
```bash
# Create backup of entire project
cd "e:\Academic\5th Semester\Computer Network(CIT-313)"
xcopy anan anan_backup /E /I /H

# Or use 7-Zip/WinRAR to create archive
```

### Quick Recovery
```bash
# If something breaks, restore backup
cd "e:\Academic\5th Semester\Computer Network(CIT-313)"
xcopy anan_backup anan /E /I /H /Y
```

---

## 📝 Checklist for Successful Run

### Before Running (One-Time Setup)
- [ ] Python 3.7+ installed
- [ ] pip working
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Test video file exists (`video/movie.Mjpeg`)
- [ ] All project files present (24 files)
- [ ] Ports 5000 and 8554 available

### Before Each Run
- [ ] Close any previous Python processes
- [ ] No other programs using port 5000
- [ ] No other programs using port 8554
- [ ] Browser ready (Chrome/Firefox recommended)
- [ ] Documentation files accessible

### During Run
- [ ] WebServer.py starts without errors
- [ ] Browser loads web interface
- [ ] "Start Server" button works
- [ ] Server status shows 🟢 Running
- [ ] Setup button establishes connection
- [ ] Play button starts streaming
- [ ] Video displays in browser
- [ ] Statistics update in real-time

### After Successful Demo
- [ ] Teardown session
- [ ] Stop server
- [ ] Close browser
- [ ] Stop WebServer.py (Ctrl+C)
- [ ] Backup successful configuration

---

## 🆘 Emergency Procedures

### If System Freezes
```bash
# Ctrl+C in WebServer terminal
# If not responding:
Get-Process python | Stop-Process -Force

# Restart:
python WebServer.py
```

### If Browser Won't Load
```bash
# Clear browser cache
# Ctrl+Shift+Delete

# Try incognito mode
# Ctrl+Shift+N (Chrome)

# Try different browser
```

### If Demo Computer Crashes
```bash
# Have backup computer ready with:
# - Same project folder
# - Dependencies pre-installed
# - Quick test done

# Or have video recording of working demo
```

---

## 📞 Quick Help Reference

### Commands Summary
```bash
# Install
pip install -r requirements.txt

# Run
python WebServer.py

# Test
http://localhost:5000

# Kill processes
Get-Process python | Stop-Process -Force

# Check ports
netstat -ano | findstr :5000
netstat -ano | findstr :8554
```

### File Locations
```
Project: e:\Academic\5th Semester\Computer Network(CIT-313)\anan
Main:    WebServer.py
Server:  Server.py
Video:   video\movie.Mjpeg
Docs:    QUICK_REFERENCE.md, WEB_CONTROL_GUIDE.md
```

### Key URLs
```
Web Interface: http://localhost:5000
Documentation: file:///e:/Academic/5th%20Semester/Computer%20Network(CIT-313)/anan/WEB_CONTROL_GUIDE.md
```

---

## ✅ Success Indicators

You know it's working when:
- ✅ Terminal shows "Starting web server..."
- ✅ Browser loads beautiful interface
- ✅ Server status button changes color
- ✅ Video frames appear and update
- ✅ Statistics show increasing numbers
- ✅ Activity log shows events
- ✅ No red error messages

---

## 🎉 You're Ready!

Follow this guide and you'll have a smooth, successful demonstration!

**Key Reminder**: Just one command: `python WebServer.py` and then control everything from the browser! 🚀

**Good luck with your presentation!** 💪🎓

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Tested On**: Windows 10/11, Python 3.9+
