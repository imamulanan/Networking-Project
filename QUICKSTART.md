# Quick Start Guide - Video Streaming with RTSP/RTP

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies (1 minute)
```powershell
pip install -r requirements.txt
```

### Step 2: Create Test Video (1 minute)
```powershell
python VideoPrep.py test video/movie.Mjpeg 10 20
```
This creates a 10-second test video with animated colored frames.

### Step 3: Start Server (10 seconds)
Open a terminal:
```powershell
python Server.py
```
You should see:
```
[Server] RTSP Server started on port 8554
[Server] Waiting for clients...
```

### Step 4: Start Client (10 seconds)
Open a NEW terminal:
```powershell
python Client.py localhost 8554 25000 video/movie.Mjpeg
```

### Step 5: Play Video (30 seconds)
In the client window:
1. Click **"Setup"** → Wait for "Setup successful!" message
2. Click **"Play"** → Video starts playing
3. Click **"Pause"** → Video pauses
4. Click **"Play"** again → Video resumes
5. Click **"Teardown"** → Close connection

## 🎯 What You Should See

### Server Terminal
```
[Server] RTSP Server started on port 8554
[Server] Waiting for clients...
[Server] Connection from ('127.0.0.1', 54321)
[Server] Received from ('127.0.0.1', 54321):
SETUP video/movie.Mjpeg RTSP/1.0
CSeq: 1
Transport: RTP/AVP;unicast;client_port=25000

[Server] SETUP completed. Session: 1732367890, RTP port: 25000
[Server] PLAY started for session 1732367890
[Server] Starting RTP stream to 127.0.0.1:25000
```

### Client Window
- **Video Display**: Colored animated frames with frame numbers
- **Control Buttons**: Setup, Play, Pause, Teardown
- **Statistics**: 
  ```
  Frame: 150 | Packets: 150 | Data Rate: 245.67 kbps | FPS: 19.85
  ```

## 🔧 Troubleshooting

### Problem: "pip: command not found"
**Solution**: Use `python -m pip install -r requirements.txt`

### Problem: "Port 8554 already in use"
**Solution**: Use different port
```powershell
python Server.py 9000
python Client.py localhost 9000 25000 video/movie.Mjpeg
```

### Problem: "No module named 'cv2'"
**Solution**: Reinstall OpenCV
```powershell
pip install opencv-python --upgrade
```

### Problem: "No module named 'PIL'"
**Solution**: Install Pillow
```powershell
pip install Pillow
```

### Problem: Client shows black screen
**Solution**: 
1. Make sure you clicked "Setup" first
2. Then click "Play"
3. Check that video file exists: `video/movie.Mjpeg`

### Problem: "Address already in use" (Client)
**Solution**: Use different RTP port
```powershell
python Client.py localhost 8554 25001 video/movie.Mjpeg
```

## 📹 Using Your Own Videos

### Convert MP4 to MJPEG
```powershell
python VideoPrep.py convert myvideo.mp4 video/myvideo.Mjpeg 20
```

### Then stream it
```powershell
# Server (Terminal 1)
python Server.py

# Client (Terminal 2)
python Client.py localhost 8554 25000 video/myvideo.Mjpeg
```

## 🧪 Testing Multiple Clients

Want to test multiple clients simultaneously?

**Terminal 1 (Server)**:
```powershell
python Server.py
```

**Terminal 2 (Client 1)**:
```powershell
python Client.py localhost 8554 25000 video/movie.Mjpeg
```

**Terminal 3 (Client 2)**:
```powershell
python Client.py localhost 8554 25002 video/movie.Mjpeg
```

**Terminal 4 (Client 3)**:
```powershell
python Client.py localhost 8554 25004 video/movie.Mjpeg
```

Note: Each client needs a unique RTP port!

## 📊 Understanding the Statistics

```
Frame: 150 | Packets: 150 | Data Rate: 245.67 kbps | FPS: 19.85
```

- **Frame**: Current frame number
- **Packets**: Total RTP packets received
- **Data Rate**: Network bandwidth usage in kilobits per second
- **FPS**: Actual frames per second being displayed

## 🎓 Educational Experiments

### Experiment 1: Frame Rate Impact
Test different frame rates:
```powershell
python VideoPrep.py test video/test10.Mjpeg 10 10
python VideoPrep.py test video/test20.Mjpeg 10 20
python VideoPrep.py test video/test30.Mjpeg 10 30
```
Compare the data rates!

### Experiment 2: Network Simulation
On the same computer:
- Server on localhost → Low latency
- Try different RTP ports → Observe behavior

### Experiment 3: Session Control
Try this sequence:
1. Setup → Play → Pause (wait 5s) → Play → Watch seamless resume
2. Setup → Play → Teardown → Setup again → Play → New session!

## 📝 Key Concepts Demonstrated

1. **RTSP (TCP)**: Reliable session control
   - SETUP establishes connection
   - PLAY/PAUSE control stream
   - TEARDOWN closes session

2. **RTP (UDP)**: Fast video delivery
   - No retransmission
   - Real-time priority
   - Sequence numbers for ordering

3. **Client-Server Model**:
   - Server handles multiple clients
   - Each client has independent session
   - Concurrent streaming

4. **Multimedia Streaming**:
   - Frame packetization
   - Timing control (20 FPS)
   - MJPEG encoding

## ⏭️ Next Steps

1. ✅ Complete basic streaming
2. 📚 Read the full README.md
3. 🔬 Experiment with different videos
4. 💡 Understand RTSP/RTP protocols
5. 🚀 Try optional enhancements:
   - Add video quality selection
   - Implement RTCP feedback
   - Add bandwidth adaptation

## 💬 Common Questions

**Q: Why MJPEG instead of H.264?**  
A: MJPEG is simpler to implement and doesn't require complex encoding/decoding libraries. Perfect for learning!

**Q: Can I stream to remote computers?**  
A: Yes! Replace `localhost` with the server's IP address. Make sure firewall allows the ports.

**Q: Why does video loop?**  
A: By design! Server automatically restarts video when it ends. Check `Server.py` line with `videoStream.reset()`.

**Q: Can I change video resolution?**  
A: Yes! Edit `Client.py` around line 250 where it resizes to (640, 480).

---

**Happy Streaming! 🎬**
