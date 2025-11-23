# Web Browser Version - Quick Start Guide

## 🌐 Running the Web Browser Client

This is the **easiest way** to use the video streaming system - no desktop client needed!

### Step 1: Install Dependencies (First Time Only)
```powershell
pip install -r requirements.txt
```

### Step 2: Start RTSP/RTP Server
Open **Terminal 1**:
```powershell
python Server.py
```

Wait for:
```
[Server] RTSP Server started on port 8554
[Server] Waiting for clients...
```

### Step 3: Start Web Server
Open **Terminal 2**:
```powershell
python WebServer.py
```

You'll see:
```
[WebServer] Starting web server...
[WebServer] Open your browser and go to: http://localhost:5000
```

### Step 4: Open Browser
1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Go to: **http://localhost:5000**
3. You'll see the video streaming interface!

### Step 5: Start Streaming
In the web interface:
1. **Click "Setup"** → Wait for "Setup successful!" in the log
2. **Click "Play"** → Video starts playing in the browser!
3. **Click "Pause"** → Pause the video
4. **Click "Play"** again → Resume
5. **Click "Teardown"** → End session

## 🎯 What You'll See

### Web Interface Features:
- **📡 Connection Settings** - Configure server address and video file
- **🎬 Video Player** - Real-time video display in browser
- **🎮 Control Buttons** - Setup, Play, Pause, Teardown controls
- **📊 Live Statistics** - Frame count, data rate, FPS
- **📝 Activity Log** - Real-time activity monitoring
- **🟢 Status Indicator** - Connection status display

### Browser Window:
```
┌──────────────────────────────────────────────┐
│  🎬 RTSP/RTP Video Streaming                 │
│     Web Browser Client                       │
├──────────────────────────────────────────────┤
│  📡 Connection Settings  │  🎬 Video Player  │
│  ┌──────────────────┐   │  ┌──────────────┐ │
│  │ Server: localhost│   │  │              │ │
│  │ Port: 8554       │   │  │    VIDEO     │ │
│  │ File: movie.Mjpeg│   │  │   DISPLAY    │ │
│  │ Status: Playing  │   │  │              │ │
│  └──────────────────┘   │  └──────────────┘ │
│                          │  [Setup] [Play]   │
│                          │  [Pause] [Stop]   │
│                          │  📊 Statistics     │
│                          │  Frame: 150       │
│                          │  FPS: 19.85       │
├──────────────────────────────────────────────┤
│  📝 Activity Log                             │
│  [10:30:15] Connected to web server          │
│  [10:30:20] Setup successful! Session: 1234  │
│  [10:30:25] Playback started                 │
└──────────────────────────────────────────────┘
```

## 🔧 Configuration

### Default Settings (can be changed in browser):
- **Server Address**: localhost
- **Server Port**: 8554
- **Video File**: video/movie.Mjpeg
- **Web Server Port**: 5000

### To Change Settings:
Just type in the input fields before clicking Setup!

## 🌍 Access from Other Devices

### On the Same Network:

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On another device (phone, tablet, laptop), open browser and go to:
   ```
   http://192.168.1.100:5000
   ```

3. In the web interface, update:
   - Server Address: `192.168.1.100`
   - Click Setup and Play!

## 📱 Mobile Browser Support

Works on:
- ✅ Chrome (Android/iOS)
- ✅ Safari (iOS)
- ✅ Firefox (Android)
- ✅ Edge (Android/iOS)

**Note**: Make sure your mobile device is on the same WiFi network!

## 🎨 Features

### Visual Interface:
- **Modern Design** - Clean, professional interface
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Live video and statistics
- **Color-coded Logs** - Easy to track activity
- **Status Indicators** - Visual connection status

### Technical Features:
- **WebSocket Communication** - Real-time bi-directional communication
- **Base64 Encoding** - JPEG frames transmitted efficiently
- **Automatic Reconnection** - Handles network interruptions
- **Session Management** - Multiple browser tabs supported
- **Live Statistics** - Frame rate, bandwidth monitoring

## 🆚 Desktop vs Web Client

| Feature | Desktop Client | Web Client |
|---------|---------------|------------|
| Installation | Tkinter required | Just a browser |
| Interface | Basic GUI | Modern web UI |
| Platform | Desktop only | Any device |
| Mobile Support | ❌ No | ✅ Yes |
| Remote Access | Manual setup | Easy |
| Multiple Clients | Different ports | Different tabs |
| Statistics | Basic | Enhanced |
| Activity Log | Console only | Web interface |

## 🔍 Troubleshooting

### Issue: "Cannot connect to web server"
**Solution**: Make sure `python WebServer.py` is running in Terminal 2

### Issue: "Setup failed: Connection refused"
**Solution**: Make sure `python Server.py` is running in Terminal 1

### Issue: "Video not loading"
**Solution**: 
1. Check that `video/movie.Mjpeg` exists
2. Clear browser cache (Ctrl+Shift+Delete)
3. Refresh the page (F5)

### Issue: "WebSocket disconnected"
**Solution**: 
1. Restart the web server
2. Refresh the browser page
3. Check firewall settings

### Issue: "Blank video screen"
**Solution**:
1. Make sure you clicked "Setup" first
2. Then click "Play"
3. Check browser console for errors (F12)

## 💡 Tips & Tricks

### Tip 1: Keep Both Terminals Open
- Terminal 1: RTSP/RTP Server (port 8554)
- Terminal 2: Web Server (port 5000)
- Both must be running!

### Tip 2: Multiple Browser Windows
You can open multiple browser windows/tabs and each will get its own session!

### Tip 3: Check the Activity Log
The activity log shows everything happening - great for debugging!

### Tip 4: Monitor Statistics
Watch the FPS and Data Rate to see streaming performance in real-time.

### Tip 5: Mobile Testing
Test on your phone for the full experience - it's responsive!

## 📊 Performance

### Expected Performance:
- **Latency**: ~100ms (local network)
- **Frame Rate**: 19-20 FPS
- **Bandwidth**: 250-300 kbps
- **Resolution**: 640x480
- **Browser Load**: Low CPU usage

### Optimized For:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🎓 How It Works

```
Browser ←→ WebSocket ←→ Web Server ←→ RTSP/RTP ←→ Video Server
   ↓            ↓            ↓            ↓            ↓
Display   Real-time   Flask App   Protocol   File Read
Frames    Transport   Bridge      Handler    (MJPEG)
```

1. **Browser** connects to Web Server via WebSocket
2. **Web Server** acts as RTSP/RTP client to Video Server
3. **RTP packets** are received and decoded
4. **JPEG frames** are base64-encoded
5. **WebSocket** sends frames to browser
6. **Browser** displays frames in real-time

## 🚀 Quick Commands Reference

```powershell
# Terminal 1 - Video Server
python Server.py

# Terminal 2 - Web Server
python WebServer.py

# Browser
http://localhost:5000

# Mobile/Remote (replace with your IP)
http://192.168.1.100:5000
```

## 📝 Complete Workflow

1. **Start Video Server** → Terminal 1
2. **Start Web Server** → Terminal 2
3. **Open Browser** → http://localhost:5000
4. **Click Setup** → Establishes connection
5. **Click Play** → Video streams to browser
6. **Enjoy!** → Watch, pause, resume
7. **Click Teardown** → Clean shutdown
8. **Close Browser** → Session ends
9. **Ctrl+C** → Stop servers (both terminals)

---

**That's it! You're now streaming video in your web browser! 🎉**

**Advantages of Web Version:**
- ✅ No desktop client installation
- ✅ Works on any device with a browser
- ✅ Mobile-friendly responsive design
- ✅ Modern, professional interface
- ✅ Easy remote access
- ✅ Real-time activity monitoring
- ✅ Better user experience

**Perfect for demonstrations and presentations!** 🎬
