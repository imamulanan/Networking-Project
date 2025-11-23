"""
RTSP/RTP Video Streaming Server
Handles RTSP session control and RTP video streaming
"""

import sys
import socket
import threading
import time
from RtpPacket import RtpPacket

# RTSP States
INIT = 0
READY = 1
PLAYING = 2

# RTSP Methods
SETUP = 'SETUP'
PLAY = 'PLAY'
PAUSE = 'PAUSE'
TEARDOWN = 'TEARDOWN'


class ServerWorker:
    """Worker class to handle individual client connections"""
    
    def __init__(self, clientInfo):
        self.clientInfo = clientInfo
        self.clientSocket = clientInfo['socket']
        self.clientAddr = clientInfo['addr']
        self.rtspSeq = 0
        self.sessionId = 0
        self.clientRtpPort = 0
        self.clientRtcpPort = 0
        self.rtpSocket = None
        self.state = INIT
        self.videoStream = None
        self.frameNum = 0
        self.stopEvent = threading.Event()
        self.workerThread = None
        
    def run(self):
        """Main loop to handle RTSP requests"""
        print(f"[Server] Connection from {self.clientAddr}")
        
        while True:
            try:
                data = self.clientSocket.recv(1024)
                if not data:
                    break
                    
                request = data.decode('utf-8')
                print(f"[Server] Received from {self.clientAddr}:\n{request}")
                
                # Parse the RTSP request
                lines = request.split('\n')
                requestLine = lines[0].split(' ')
                
                if len(requestLine) >= 2:
                    requestType = requestLine[0]
                    
                    # Get CSeq
                    for line in lines:
                        if line.startswith('CSeq:'):
                            self.rtspSeq = int(line.split(' ')[1])
                    
                    # Handle different request types
                    if requestType == SETUP:
                        self.handleSetup(lines)
                    elif requestType == PLAY:
                        self.handlePlay()
                    elif requestType == PAUSE:
                        self.handlePause()
                    elif requestType == TEARDOWN:
                        self.handleTeardown()
                        break
                        
            except Exception as e:
                print(f"[Server] Error handling request: {e}")
                break
        
        # Cleanup
        self.cleanup()
    
    def handleSetup(self, lines):
        """Handle SETUP request"""
        if self.state == INIT:
            try:
                # Get video filename from request
                requestLine = lines[0].split(' ')
                filename = requestLine[1]
                
                # Open video file
                self.videoStream = VideoStream(filename)
                
                # Get RTP/RTCP port from request
                for line in lines:
                    if line.startswith('Transport:'):
                        transport = line.split(' ')[1]
                        # Parse client_port from Transport header
                        # Format: RTP/AVP;unicast;client_port=25000-25001
                        if 'client_port=' in transport:
                            ports = transport.split('client_port=')[1]
                            portRange = ports.split('-')
                            self.clientRtpPort = int(portRange[0])
                            if len(portRange) > 1:
                                self.clientRtcpPort = int(portRange[1])
                
                # Generate session ID
                self.sessionId = int(time.time())
                
                # Create RTP socket
                self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send RTSP reply
                self.state = READY
                self.sendRtspReply(200, self.rtspSeq, self.sessionId)
                
                print(f"[Server] SETUP completed. Session: {self.sessionId}, RTP port: {self.clientRtpPort}")
                
            except Exception as e:
                print(f"[Server] SETUP error: {e}")
                self.sendRtspReply(404, self.rtspSeq)
    
    def handlePlay(self):
        """Handle PLAY request"""
        if self.state == READY:
            self.state = PLAYING
            
            # Send RTSP reply
            self.sendRtspReply(200, self.rtspSeq, self.sessionId)
            
            # Start streaming in a new thread
            self.stopEvent.clear()
            self.workerThread = threading.Thread(target=self.sendRtp)
            self.workerThread.start()
            
            print(f"[Server] PLAY started for session {self.sessionId}")
    
    def handlePause(self):
        """Handle PAUSE request"""
        if self.state == PLAYING:
            self.state = READY
            
            # Stop the streaming thread
            self.stopEvent.set()
            if self.workerThread:
                self.workerThread.join()
            
            # Send RTSP reply
            self.sendRtspReply(200, self.rtspSeq, self.sessionId)
            
            print(f"[Server] PAUSE for session {self.sessionId}")
    
    def handleTeardown(self):
        """Handle TEARDOWN request"""
        # Stop streaming
        self.stopEvent.set()
        if self.workerThread:
            self.workerThread.join()
        
        # Send RTSP reply
        self.sendRtspReply(200, self.rtspSeq, self.sessionId)
        
        print(f"[Server] TEARDOWN for session {self.sessionId}")
    
    def sendRtp(self):
        """Send RTP packets to the client"""
        print(f"[Server] Starting RTP stream to {self.clientAddr[0]}:{self.clientRtpPort}")
        
        while not self.stopEvent.is_set():
            try:
                # Get next frame from video
                data = self.videoStream.nextFrame()
                if data:
                    frameNum = self.videoStream.frameNum()
                    
                    # Create RTP packet
                    rtpPacket = RtpPacket()
                    rtpPacket.setPayloadType(26)  # MJPEG
                    rtpPacket.setSeqNum(frameNum)
                    rtpPacket.setTimestamp(int(time.time() * 90000))  # 90kHz clock
                    rtpPacket.setSSRC(self.sessionId)
                    rtpPacket.setPayload(data)
                    
                    # Send packet
                    packet = rtpPacket.encode()
                    self.rtpSocket.sendto(packet, (self.clientAddr[0], self.clientRtpPort))
                    
                    # Control frame rate (20 FPS)
                    time.sleep(0.05)
                else:
                    # End of file, loop back
                    self.videoStream.reset()
                    
            except Exception as e:
                print(f"[Server] Error sending RTP: {e}")
                if self.stopEvent.is_set():
                    break
    
    def sendRtspReply(self, code, seq, session=None):
        """Send RTSP reply to the client"""
        if code == 200:
            reply = f'RTSP/1.0 200 OK\nCSeq: {seq}\n'
            if session:
                reply += f'Session: {session}\n'
        elif code == 404:
            reply = f'RTSP/1.0 404 Not Found\nCSeq: {seq}\n'
        else:
            reply = f'RTSP/1.0 {code}\nCSeq: {seq}\n'
        
        try:
            self.clientSocket.send(reply.encode('utf-8'))
        except Exception as e:
            print(f"[Server] Error sending RTSP reply: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self.stopEvent.set()
        
        if self.workerThread:
            self.workerThread.join()
        
        if self.rtpSocket:
            self.rtpSocket.close()
        
        if self.videoStream:
            self.videoStream.close()
        
        if self.clientSocket:
            self.clientSocket.close()
        
        print(f"[Server] Connection closed for {self.clientAddr}")


class VideoStream:
    """Video stream class to read MJPEG frames"""
    
    def __init__(self, filename):
        try:
            self.filename = filename
            self.file = open(filename, 'rb')
            self.currentFrame = 0
        except Exception as e:
            print(f"[VideoStream] Error opening file {filename}: {e}")
            raise
    
    def nextFrame(self):
        """Get the next frame"""
        try:
            # Read frame length (5 bytes)
            data = self.file.read(5)
            if not data or len(data) < 5:
                return None
            
            frameLength = int(data)
            
            # Read frame data
            frameData = self.file.read(frameLength)
            self.currentFrame += 1
            
            return frameData
        except Exception as e:
            print(f"[VideoStream] Error reading frame: {e}")
            return None
    
    def frameNum(self):
        """Get current frame number"""
        return self.currentFrame
    
    def reset(self):
        """Reset to beginning of file"""
        self.file.seek(0)
        self.currentFrame = 0
    
    def close(self):
        """Close the video file"""
        if self.file:
            self.file.close()


class Server:
    """Main RTSP server class"""
    
    def __init__(self, port=8554):
        self.port = port
        self.serverSocket = None
        self.clients = []
    
    def start(self):
        """Start the RTSP server"""
        try:
            # Create server socket
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind(('', self.port))
            self.serverSocket.listen(5)
            
            print(f"[Server] RTSP Server started on port {self.port}")
            print("[Server] Waiting for clients...")
            
            while True:
                clientSocket, addr = self.serverSocket.accept()
                
                # Create new client handler
                clientInfo = {
                    'socket': clientSocket,
                    'addr': addr
                }
                
                worker = ServerWorker(clientInfo)
                self.clients.append(worker)
                
                # Handle client in new thread
                clientThread = threading.Thread(target=worker.run)
                clientThread.start()
                
        except KeyboardInterrupt:
            print("\n[Server] Server interrupted by user")
        except Exception as e:
            print(f"[Server] Error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up server resources"""
        print("[Server] Shutting down...")
        
        if self.serverSocket:
            self.serverSocket.close()
        
        print("[Server] Server stopped")


def main():
    """Main function"""
    port = 8554
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8554")
    
    server = Server(port)
    server.start()


if __name__ == '__main__':
    main()
