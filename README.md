# Video Streaming with RTSP and RTP Lab

A comprehensive Python implementation of a video streaming system using **RTSP (Real-Time Streaming Protocol)** for session control and **RTP (Real-Time Transport Protocol)** for transmitting video data.

## 📋 Project Overview

This project implements a complete video streaming solution with:
- **RTSP Server**: Handles session setup, control (play/pause), and teardown
- **RTP Server**: Transmits video frames in real-time using UDP
- **RTSP Client**: GUI-based client with video playback controls
- **RTP Client**: Receives and displays video frames in real-time
- **Video Preparation Tools**: Convert videos to MJPEG format for streaming

## 🏗️ Architecture

```
┌─────────────┐                    ┌─────────────┐
│   Client    │                    │   Server    │
│             │                    │             │
│ ┌─────────┐ │  RTSP (TCP 8554)   │ ┌─────────┐ │
│ │  RTSP   │◄├───────────────────►│ │  RTSP   │ │
│ │ Client  │ │                    │ │ Handler │ │
│ └────┬────┘ │                    │ └────┬────┘ │
│      │      │                    │      │      │
│ ┌────▼────┐ │  RTP (UDP 25000)   │ ┌────▼────┐ │
│ │   RTP   │◄├───────────────────►│ │   RTP   │ │
│ │ Receiver│ │                    │ │ Sender  │ │
│ └────┬────┘ │                    │ └────┬────┘ │
│      │      │                    │      │      │
│ ┌────▼────┐ │                    │ ┌────▼────┐ │
│ │   GUI   │ │                    │ │  Video  │ │
│ │ Display │ │                    │ │ Stream  │ │
│ └─────────┘ │                    │ └─────────┘ │
└─────────────┘                    └─────────────┘
```

## 📁 Project Structure

```
.
├── Server.py           # RTSP/RTP server implementation
├── Client.py           # RTSP/RTP client with GUI
├── RtpPacket.py        # RTP packet encoding/decoding
├── VideoPrep.py        # Video preparation utilities
├── requirements.txt    # Python dependencies
├── video/              # Directory for video files
│   └── movie.Mjpeg     # Sample video (MJPEG format)
└── README.md           # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

### Prepare Video Content

#### Option 1: Create a Test Video
```powershell
python VideoPrep.py test video/movie.Mjpeg 10 20
```
This creates a 10-second test video at 20 FPS with colored frames.

#### Option 2: Convert Existing Video
```powershell
python VideoPrep.py convert input.mp4 video/movie.Mjpeg 20
```
This converts any video file (MP4, AVI, MOV, etc.) to MJPEG format.

#### Option 3: Get Video Info
```powershell
python VideoPrep.py info video/movie.Mjpeg
```
Display information about an MJPEG file.

## 🎬 Running the Application

### Step 1: Start the Server

Open a terminal and run:
```powershell
python Server.py
```

The server will start on port **8554** by default. You can specify a different port:
```powershell
python Server.py 9000
```

### Step 2: Start the Client

Open another terminal and run:
```powershell
python Client.py localhost 8554 25000 video/movie.Mjpeg
```

**Parameters**:
- `localhost`: Server address
- `8554`: RTSP server port
- `25000`: RTP port for receiving video
- `video/movie.Mjpeg`: Video file to stream

### Step 3: Control Playback

In the client GUI:
1. Click **Setup** to establish connection
2. Click **Play** to start streaming
3. Click **Pause** to pause playback
4. Click **Teardown** to end session and close

## 🔧 Technical Details

### RTSP Protocol

The RTSP protocol handles session control with these methods:

- **SETUP**: Establishes session and negotiates transport parameters
- **PLAY**: Starts video streaming
- **PAUSE**: Pauses the stream
- **TEARDOWN**: Terminates the session

#### Sample RTSP Exchange

**Client → Server (SETUP)**:
```
SETUP video/movie.Mjpeg RTSP/1.0
CSeq: 1
Transport: RTP/AVP;unicast;client_port=25000
```

**Server → Client (Response)**:
```
RTSP/1.0 200 OK
CSeq: 1
Session: 1234567890
```

### RTP Protocol

RTP packets carry video frames with:
- **Version**: 2
- **Payload Type**: 26 (MJPEG)
- **Sequence Number**: Frame counter
- **Timestamp**: 90kHz clock
- **SSRC**: Session identifier
- **Payload**: JPEG frame data

#### RTP Packet Structure
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       sequence number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           synchronization source (SSRC) identifier            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Video Format

Videos must be in **MJPEG format** with this structure:
- Each frame is prefixed with 5-byte length indicator
- Frame data is JPEG-encoded
- Default streaming rate: 20 FPS

## 📊 Features

### Current Features
- ✅ RTSP session control (SETUP, PLAY, PAUSE, TEARDOWN)
- ✅ RTP real-time video transmission
- ✅ GUI-based video player
- ✅ Real-time statistics (frame count, data rate, FPS)
- ✅ Multi-threaded server supporting multiple clients
- ✅ Video format conversion utilities
- ✅ Loop playback (video restarts when finished)

### Optional Enhancements
- 🔲 Multiple simultaneous clients
- 🔲 Video quality selection
- 🔲 Adaptive streaming based on network conditions
- 🔲 RTCP (RTP Control Protocol) for feedback
- 🔲 Different video codecs (H.264, H.265)
- 🔲 Live video feed support

## 🛠️ Configuration

### Server Configuration
- **Port**: Default 8554 (configurable via command line)
- **Frame Rate**: 20 FPS (adjustable in `Server.py`)
- **Transport**: UDP for RTP packets

### Client Configuration
- **RTP Port**: Default 25000 (configurable via command line)
- **Timeout**: 0.5 seconds for RTP socket
- **Display Size**: 640x480 (adjustable in `Client.py`)

## 📝 Code Components

### RtpPacket.py
Implements RTP packet structure according to RFC 3550:
- `encode()`: Create RTP packet from header and payload
- `decode()`: Parse RTP packet from byte stream
- Getter/setter methods for all RTP header fields

### Server.py
Main server components:
- `Server`: Main RTSP server class
- `ServerWorker`: Handles individual client connections
- `VideoStream`: Reads MJPEG frames from file

### Client.py
Client components:
- `Client`: Main client class with GUI
- RTSP request handling
- RTP packet reception and decoding
- Video frame display
- Statistics tracking

### VideoPrep.py
Video preparation utilities:
- Convert videos to MJPEG format
- Create test videos
- Display video information

## 🔍 Troubleshooting

### Server Issues
- **Port already in use**: Change the server port
  ```powershell
  python Server.py 9000
  ```
- **Video file not found**: Ensure the video file path is correct

### Client Issues
- **Connection refused**: Ensure server is running first
- **No video display**: Check if video file exists and is in correct format
- **Port in use**: Change RTP port in client command
  ```powershell
  python Client.py localhost 8554 25001 video/movie.Mjpeg
  ```

### Video Issues
- **Conversion fails**: Ensure OpenCV is properly installed
  ```powershell
  pip install opencv-python --upgrade
  ```
- **Test video colors**: This is normal - test videos cycle through colors

## 📚 Learning Objectives

This project demonstrates:
1. **Network Protocols**: RTSP and RTP implementation
2. **Socket Programming**: TCP for RTSP, UDP for RTP
3. **Multithreading**: Concurrent client handling and packet transmission
4. **Video Processing**: MJPEG encoding/decoding
5. **GUI Development**: Tkinter for video player interface
6. **Real-time Systems**: Frame timing and synchronization

## 🔗 References

- [RFC 2326 - RTSP Protocol](https://tools.ietf.org/html/rfc2326)
- [RFC 3550 - RTP Protocol](https://tools.ietf.org/html/rfc3550)
- [MJPEG Format](https://en.wikipedia.org/wiki/Motion_JPEG)

## 📄 License

This is an educational project for Computer Network Lab (CIT-313).

## 👥 Author

Created for 5th Semester Computer Network Lab

## 🎓 Academic Notes

**Course**: Computer Network (CIT-313)  
**Topic**: Multimedia Streaming and Real-time Communication Protocols  
**Concepts Covered**:
- Application Layer Protocols (RTSP)
- Transport Layer Protocols (RTP, UDP, TCP)
- Client-Server Architecture
- Real-time Data Transmission
- Multimedia Streaming

---

**Enjoy streaming! 🎥✨**
