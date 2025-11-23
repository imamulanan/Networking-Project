# Testing Instructions - RTSP/RTP Video Streaming Lab

## ✅ Pre-Test Checklist

- [x] Python 3.7+ installed
- [x] All dependencies installed (`pip install -r requirements.txt`)
- [x] Test video created (`video/movie.Mjpeg` - 200 frames, ~2.6 MB)
- [ ] Server ready to start
- [ ] Client ready to start

## 🧪 Test Plan

### Test 1: Basic Server Startup ✅

**Objective**: Verify server starts correctly

**Steps**:
```powershell
python Server.py
```

**Expected Output**:
```
[Server] RTSP Server started on port 8554
[Server] Waiting for clients...
```

**Result**: ☐ Pass ☐ Fail

---

### Test 2: Client Connection & SETUP ✅

**Objective**: Test RTSP SETUP method

**Steps**:
1. Keep server running
2. In new terminal:
   ```powershell
   python Client.py localhost 8554 25000 video/movie.Mjpeg
   ```
3. Click "Setup" button

**Expected Client Behavior**:
- GUI window appears
- Message box: "Setup successful!"

**Expected Server Output**:
```
[Server] Connection from ('127.0.0.1', XXXXX)
[Server] Received from ('127.0.0.1', XXXXX):
SETUP video/movie.Mjpeg RTSP/1.0
...
[Server] SETUP completed. Session: XXXXXXXXXX, RTP port: 25000
```

**Result**: ☐ Pass ☐ Fail

---

### Test 3: Video Streaming (PLAY) ✅

**Objective**: Test RTSP PLAY method and RTP streaming

**Steps**:
1. After successful SETUP
2. Click "Play" button

**Expected Client Behavior**:
- Video frames appear (colored with frame numbers)
- Statistics update continuously
- Smooth playback at ~20 FPS

**Expected Server Output**:
```
[Server] PLAY started for session XXXXXXXXXX
[Server] Starting RTP stream to 127.0.0.1:25000
```

**Verify Statistics**:
- Frame count increases
- FPS shows ~19-20
- Data rate shows ~200-300 kbps

**Result**: ☐ Pass ☐ Fail

---

### Test 4: Pause and Resume ✅

**Objective**: Test RTSP PAUSE method

**Steps**:
1. While video is playing
2. Click "Pause" button
3. Wait 5 seconds
4. Click "Play" button again

**Expected Behavior**:
- Video freezes on current frame
- Statistics stop updating
- After clicking Play, video resumes from paused frame
- Frame counter continues from where it stopped

**Expected Server Output**:
```
[Server] PAUSE for session XXXXXXXXXX
[Server] PLAY started for session XXXXXXXXXX
```

**Result**: ☐ Pass ☐ Fail

---

### Test 5: Session Teardown ✅

**Objective**: Test RTSP TEARDOWN method

**Steps**:
1. While video is playing or paused
2. Click "Teardown" button

**Expected Behavior**:
- Client window closes
- Server logs teardown

**Expected Server Output**:
```
[Server] TEARDOWN for session XXXXXXXXXX
[Server] Connection closed for ('127.0.0.1', XXXXX)
```

**Result**: ☐ Pass ☐ Fail

---

### Test 6: Multiple Sequential Sessions ✅

**Objective**: Test multiple session handling

**Steps**:
1. Complete a full cycle: Setup → Play → Teardown
2. Start client again
3. Repeat: Setup → Play → Teardown

**Expected Behavior**:
- Each session gets unique session ID
- No interference between sessions
- Server continues accepting new connections

**Result**: ☐ Pass ☐ Fail

---

### Test 7: Multiple Simultaneous Clients ✅

**Objective**: Test concurrent client handling

**Steps**:
1. Keep server running
2. Start 3 clients with different RTP ports:

**Terminal 2**:
```powershell
python Client.py localhost 8554 25000 video/movie.Mjpeg
```

**Terminal 3**:
```powershell
python Client.py localhost 8554 25002 video/movie.Mjpeg
```

**Terminal 4**:
```powershell
python Client.py localhost 8554 25004 video/movie.Mjpeg
```

3. Click Setup → Play on all clients

**Expected Behavior**:
- All clients receive video simultaneously
- Independent playback control for each client
- Server shows multiple active sessions

**Result**: ☐ Pass ☐ Fail

---

### Test 8: RTP Packet Analysis ✅

**Objective**: Verify RTP packet structure

**Method**: Check console output or add debug prints

**Verify RTP Headers**:
- Version = 2
- Payload Type = 26 (MJPEG)
- Sequence numbers increment correctly
- Timestamps are consistent
- SSRC matches session ID

**Result**: ☐ Pass ☐ Fail

---

### Test 9: Video Loop Behavior ✅

**Objective**: Test end-of-video handling

**Steps**:
1. Start playback
2. Wait for video to complete (~10 seconds)
3. Continue watching

**Expected Behavior**:
- Video automatically restarts from beginning
- No interruption or error messages
- Continuous loop playback

**Result**: ☐ Pass ☐ Fail

---

### Test 10: Error Handling ✅

**Objective**: Test error scenarios

#### Test 10a: Invalid Video File
**Steps**:
```powershell
python Client.py localhost 8554 25000 video/nonexistent.Mjpeg
```

**Expected**: Server returns error 404

**Result**: ☐ Pass ☐ Fail

#### Test 10b: Server Not Running
**Steps**:
1. Stop server
2. Try to start client and click Setup

**Expected**: Client shows connection error

**Result**: ☐ Pass ☐ Fail

#### Test 10c: Port Already in Use
**Steps**:
1. Start server on port 8554
2. Try starting another server on same port

**Expected**: Error message about port in use

**Result**: ☐ Pass ☐ Fail

---

## 📊 Performance Testing

### Network Statistics Analysis

**Collect Data**:
1. Play video for 30 seconds
2. Record statistics every 10 seconds

| Time (s) | Frames | Packets | Data Rate (kbps) | FPS |
|----------|--------|---------|------------------|-----|
| 10       |        |         |                  |     |
| 20       |        |         |                  |     |
| 30       |        |         |                  |     |

**Calculate**:
- Average FPS: ________
- Average Data Rate: ________ kbps
- Packet Loss: ________ packets (if any)

---

## 🔍 Protocol Verification

### RTSP Message Format Verification

**Check SETUP Request**:
```
SETUP video/movie.Mjpeg RTSP/1.0
CSeq: 1
Transport: RTP/AVP;unicast;client_port=25000
```
- ☐ Correct method name
- ☐ Valid file path
- ☐ RTSP version 1.0
- ☐ CSeq present
- ☐ Transport parameters correct

**Check SETUP Response**:
```
RTSP/1.0 200 OK
CSeq: 1
Session: XXXXXXXXXX
```
- ☐ Status code 200
- ☐ CSeq matches request
- ☐ Session ID provided

---

## 🎯 Advanced Testing (Optional)

### Test 11: Custom Frame Rate
**Steps**:
1. Create video with different FPS:
   ```powershell
   python VideoPrep.py test video/fast.Mjpeg 5 30
   ```
2. Stream and measure actual FPS

**Result**: ☐ Pass ☐ Fail

### Test 12: Video Conversion
**Steps**:
1. Get a sample MP4 file
2. Convert:
   ```powershell
   python VideoPrep.py convert sample.mp4 video/converted.Mjpeg 20
   ```
3. Stream converted video

**Result**: ☐ Pass ☐ Fail

### Test 13: Network Simulation
**Steps**:
1. Use different network configurations
2. Test on same machine vs different machines
3. Measure latency and jitter

**Result**: ☐ Pass ☐ Fail

---

## 📝 Test Report Template

**Date**: ________________

**Tester**: ________________

**Environment**:
- OS: Windows / Linux / macOS
- Python Version: ________
- Network: Local / Remote

**Test Results Summary**:
- Total Tests: 10
- Passed: ____
- Failed: ____
- Success Rate: ____%

**Issues Found**:
1. _______________________________________
2. _______________________________________
3. _______________________________________

**Observations**:
_______________________________________
_______________________________________
_______________________________________

**Recommendations**:
_______________________________________
_______________________________________
_______________________________________

---

## 🐛 Common Issues & Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Black screen in client | Forgot to click Setup | Click Setup first |
| No video after Play | Video file missing | Check video/movie.Mjpeg exists |
| Connection refused | Server not running | Start server first |
| Port error | Port in use | Use different port |
| Import error | Missing dependencies | `pip install -r requirements.txt` |
| Low FPS | System overload | Close other applications |

---

## ✨ Demonstration Checklist

For presenting to instructor:

- [ ] Clean server start
- [ ] Client connection established
- [ ] Video plays smoothly
- [ ] Pause/Resume works
- [ ] Multiple clients demonstration
- [ ] Statistics visible and updating
- [ ] Clean teardown
- [ ] Explain RTSP protocol
- [ ] Explain RTP packet structure
- [ ] Show video preparation tool

---

## 🎓 Understanding Questions

**After testing, you should be able to answer**:

1. What is the difference between RTSP and RTP?
2. Why is TCP used for RTSP and UDP for RTP?
3. What information is in an RTP packet header?
4. How does the server handle multiple clients?
5. What happens if RTP packets are lost?
6. How is frame rate controlled?
7. What is the MJPEG format?
8. How does session management work?

---

**Good luck with your testing! 🚀**
