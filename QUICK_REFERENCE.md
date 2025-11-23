# 🚀 QUICK REFERENCE - Web Control

## ⚡ Fastest Way to Start

```bash
python WebServer.py
```
Then open: **http://localhost:5000**

---

## 🎮 Button Controls

| Button | What It Does | When Available |
|--------|--------------|----------------|
| **▶️ Start Server** | Starts RTSP/RTP Server on port 8554 | When server is stopped |
| **⏹️ Stop Server** | Stops RTSP/RTP Server | When server is running |
| **⚙️ Setup** | Establish RTSP connection | When server is running |
| **▶️ Play** | Start video streaming | After successful setup |
| **⏸️ Pause** | Pause video streaming | During playback |
| **⏹️ Teardown** | End streaming session | After setup |

---

## 📊 Status Indicators

| Indicator | Meaning |
|-----------|---------|
| 🟢 **Green Dot** | Running / Connected |
| 🔴 **Red Dot** | Stopped / Disconnected |

---

## 🔄 Typical Workflow

```
1. Start Server     ▶️  (Wait for 🟢)
2. Setup           ⚙️  (Establish connection)
3. Play            ▶️  (Start streaming)
4. Pause/Resume    ⏸️▶️ (Control playback)
5. Teardown        ⏹️  (End session)
6. Stop Server     ⏹️  (Clean shutdown)
```

---

## 📁 Default Settings

```
Server Address:  localhost
Server Port:     8554
Video File:      video/movie.Mjpeg
Web Port:        5000
```

---

## 🐛 Quick Fixes

**Server won't start?**
```bash
Get-Process python | Stop-Process -Force
```

**WebSocket disconnected?**
```
Press F5 to refresh browser
```

**Port 5000 busy?**
```
Change port in WebServer.py line ~460:
socketio.run(app, host='0.0.0.0', port=5001)
```

---

## 🎯 Project Structure

```
Your Project/
├── Server.py           ← RTSP/RTP Server
├── WebServer.py        ← Flask Web Server (Run This!)
├── RtpPacket.py        ← RTP Protocol
├── templates/
│   └── index.html      ← Web UI
├── static/
│   ├── script.js       ← JavaScript Controls
│   └── style.css       ← Styling
└── video/
    └── movie.Mjpeg     ← Test Video
```

---

## 💻 Terminal Commands

### Start System
```bash
python WebServer.py
```

### Kill All Python Processes (Emergency)
```bash
Get-Process python | Stop-Process -Force
```

### Check What's Using Port 8554
```bash
netstat -ano | findstr :8554
```

### Check What's Using Port 5000
```bash
netstat -ano | findstr :5000
```

---

## 🌐 Access from Other Devices

1. Find your IP:
   ```bash
   ipconfig
   ```

2. On other device's browser:
   ```
   http://YOUR_IP:5000
   ```

3. In web interface, change **Server Address** to your IP

---

## 📈 Statistics Explained

| Stat | Description |
|------|-------------|
| **Frame** | Current frame number being displayed |
| **Packets** | Total RTP packets received |
| **Data Rate** | Streaming speed in kilobits per second |
| **FPS** | Frames Per Second (playback speed) |

---

## 🎨 Log Colors

- 🟢 **Green** = Success
- 🔴 **Red** = Error
- 🔵 **Blue** = Information

---

## ⚠️ Important Notes

1. **Must start Server before Setup**: Click "Start Server" first!
2. **Wait for status update**: Watch for 🟢 green dot
3. **One session at a time**: Teardown before new Setup
4. **Clean shutdown**: Stop Server before closing WebServer

---

## 📞 For Presentation

**Demo Flow**: Start Server → Setup → Play → Show Stats → Pause → Resume → Teardown → Stop

**Talking Points**:
- "Everything controlled from web browser"
- "Real-time statistics"
- "RTSP/RTP protocols"
- "Multi-client support"
- "Professional interface"

---

## 🔗 Full Documentation

- Complete Guide: `WEB_CONTROL_GUIDE.md`
- Technical Docs: `README.md`
- Web Features: `README_WEB.md`
- All Features: `PROJECT_COMPLETE.md`

---

**Quick Help**: Open `WEB_CONTROL_GUIDE.md` for detailed explanations!
