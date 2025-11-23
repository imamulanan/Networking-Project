"""
RTSP/RTP Video Streaming Client
GUI-based client for streaming video with RTSP/RTP
"""

import sys
import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io
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


class Client:
    """RTSP Client with GUI"""
    
    def __init__(self, master, serverAddr, serverPort, rtpPort, videoFile):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.master.title("RTSP Video Streaming Client")
        
        # Server information
        self.serverAddr = serverAddr
        self.serverPort = int(serverPort)
        self.rtpPort = int(rtpPort)
        self.videoFile = videoFile
        self.fileName = videoFile
        
        # RTSP/RTP parameters
        self.rtspSocket = None
        self.rtpSocket = None
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = INIT
        self.state = INIT
        self.teardownAcked = 0
        
        # Statistics
        self.frameNum = 0
        self.packetsReceived = 0
        self.bytesReceived = 0
        self.startTime = 0
        
        # Threading
        self.rtpThread = None
        self.stopEvent = threading.Event()
        
        # Create GUI
        self.createWidgets()
    
    def createWidgets(self):
        """Create GUI widgets"""
        # Video display
        self.label = Label(self.master, height=19, bg='black')
        self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5)
        
        # Control buttons
        self.setup = Button(self.master, width=20, padx=3, pady=3)
        self.setup["text"] = "Setup"
        self.setup["command"] = self.setupMovie
        self.setup.grid(row=1, column=0, padx=2, pady=2)
        
        self.start = Button(self.master, width=20, padx=3, pady=3)
        self.start["text"] = "Play"
        self.start["command"] = self.playMovie
        self.start.grid(row=1, column=1, padx=2, pady=2)
        
        self.pause = Button(self.master, width=20, padx=3, pady=3)
        self.pause["text"] = "Pause"
        self.pause["command"] = self.pauseMovie
        self.pause.grid(row=1, column=2, padx=2, pady=2)
        
        self.teardown = Button(self.master, width=20, padx=3, pady=3)
        self.teardown["text"] = "Teardown"
        self.teardown["command"] = self.exitClient
        self.teardown.grid(row=1, column=3, padx=2, pady=2)
        
        # Statistics display
        self.statsLabel = Label(self.master, text="Statistics: ", anchor=W, justify=LEFT)
        self.statsLabel.grid(row=2, column=0, columnspan=4, sticky=W, padx=5, pady=5)
    
    def setupMovie(self):
        """Send SETUP request"""
        if self.state == INIT:
            try:
                # Create RTSP socket
                self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.rtspSocket.connect((self.serverAddr, self.serverPort))
                
                # Create RTP socket
                self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.rtpSocket.settimeout(0.5)
                self.rtpSocket.bind(('', self.rtpPort))
                
                # Send SETUP request
                self.rtspSeq += 1
                request = f"{SETUP} {self.fileName} RTSP/1.0\n"
                request += f"CSeq: {self.rtspSeq}\n"
                request += f"Transport: RTP/AVP;unicast;client_port={self.rtpPort}\n"
                
                self.rtspSocket.send(request.encode('utf-8'))
                self.requestSent = SETUP
                
                print(f"[Client] SETUP request sent:\n{request}")
                
                # Receive reply
                reply = self.rtspSocket.recv(1024).decode('utf-8')
                print(f"[Client] SETUP reply:\n{reply}")
                
                # Parse reply
                lines = reply.split('\n')
                seqNum = int(lines[1].split(' ')[1])
                
                if seqNum == self.rtspSeq:
                    self.sessionId = int(lines[2].split(' ')[1])
                    self.state = READY
                    messagebox.showinfo("Setup", "Setup successful!")
                    print(f"[Client] Session {self.sessionId} established")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Setup failed: {e}")
                print(f"[Client] Setup error: {e}")
    
    def playMovie(self):
        """Send PLAY request"""
        if self.state == READY:
            try:
                # Send PLAY request
                self.rtspSeq += 1
                request = f"{PLAY} {self.fileName} RTSP/1.0\n"
                request += f"CSeq: {self.rtspSeq}\n"
                request += f"Session: {self.sessionId}\n"
                
                self.rtspSocket.send(request.encode('utf-8'))
                self.requestSent = PLAY
                
                print(f"[Client] PLAY request sent:\n{request}")
                
                # Receive reply
                reply = self.rtspSocket.recv(1024).decode('utf-8')
                print(f"[Client] PLAY reply:\n{reply}")
                
                # Parse reply
                lines = reply.split('\n')
                seqNum = int(lines[1].split(' ')[1])
                
                if seqNum == self.rtspSeq:
                    self.state = PLAYING
                    self.startTime = time.time()
                    
                    # Start RTP receiving thread
                    self.stopEvent.clear()
                    self.rtpThread = threading.Thread(target=self.listenRtp)
                    self.rtpThread.start()
                    
                    print("[Client] Playing...")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Play failed: {e}")
                print(f"[Client] Play error: {e}")
    
    def pauseMovie(self):
        """Send PAUSE request"""
        if self.state == PLAYING:
            try:
                # Send PAUSE request
                self.rtspSeq += 1
                request = f"{PAUSE} {self.fileName} RTSP/1.0\n"
                request += f"CSeq: {self.rtspSeq}\n"
                request += f"Session: {self.sessionId}\n"
                
                self.rtspSocket.send(request.encode('utf-8'))
                self.requestSent = PAUSE
                
                print(f"[Client] PAUSE request sent:\n{request}")
                
                # Receive reply
                reply = self.rtspSocket.recv(1024).decode('utf-8')
                print(f"[Client] PAUSE reply:\n{reply}")
                
                # Parse reply
                lines = reply.split('\n')
                seqNum = int(lines[1].split(' ')[1])
                
                if seqNum == self.rtspSeq:
                    self.state = READY
                    
                    # Stop RTP thread
                    self.stopEvent.set()
                    if self.rtpThread:
                        self.rtpThread.join()
                    
                    print("[Client] Paused")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Pause failed: {e}")
                print(f"[Client] Pause error: {e}")
    
    def exitClient(self):
        """Send TEARDOWN request and exit"""
        try:
            # Send TEARDOWN request
            self.rtspSeq += 1
            request = f"{TEARDOWN} {self.fileName} RTSP/1.0\n"
            request += f"CSeq: {self.rtspSeq}\n"
            request += f"Session: {self.sessionId}\n"
            
            if self.rtspSocket:
                self.rtspSocket.send(request.encode('utf-8'))
                self.requestSent = TEARDOWN
                
                print(f"[Client] TEARDOWN request sent:\n{request}")
                
                # Receive reply
                try:
                    reply = self.rtspSocket.recv(1024).decode('utf-8')
                    print(f"[Client] TEARDOWN reply:\n{reply}")
                except:
                    pass
            
            # Stop RTP thread
            self.stopEvent.set()
            if self.rtpThread:
                self.rtpThread.join()
            
            # Close sockets
            if self.rtpSocket:
                self.rtpSocket.close()
            if self.rtspSocket:
                self.rtspSocket.close()
            
            print("[Client] Session closed")
            
        except Exception as e:
            print(f"[Client] Teardown error: {e}")
        finally:
            self.master.destroy()
    
    def listenRtp(self):
        """Listen for RTP packets"""
        print("[Client] Listening for RTP packets...")
        
        while not self.stopEvent.is_set():
            try:
                # Receive RTP packet
                data, addr = self.rtpSocket.recvfrom(20480)
                
                if data:
                    # Decode RTP packet
                    rtpPacket = RtpPacket()
                    rtpPacket.decode(data)
                    
                    # Update statistics
                    self.packetsReceived += 1
                    self.bytesReceived += len(data)
                    self.frameNum = rtpPacket.getSeqNum()
                    
                    # Update statistics display
                    self.updateStats()
                    
                    # Get frame data
                    payload = rtpPacket.getPayload()
                    
                    # Display frame
                    self.displayFrame(payload)
                    
            except socket.timeout:
                continue
            except Exception as e:
                if not self.stopEvent.is_set():
                    print(f"[Client] Error receiving RTP: {e}")
                break
    
    def displayFrame(self, data):
        """Display video frame"""
        try:
            # Convert JPEG data to image
            image = Image.open(io.BytesIO(data))
            
            # Resize to fit display
            image = image.resize((640, 480), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update label
            self.label.configure(image=photo)
            self.label.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"[Client] Error displaying frame: {e}")
    
    def updateStats(self):
        """Update statistics display"""
        if self.startTime > 0:
            elapsed = time.time() - self.startTime
            dataRate = (self.bytesReceived * 8) / (elapsed * 1000)  # kbps
            fps = self.packetsReceived / elapsed if elapsed > 0 else 0
            
            stats = f"Statistics:\n"
            stats += f"Frame: {self.frameNum} | "
            stats += f"Packets: {self.packetsReceived} | "
            stats += f"Data Rate: {dataRate:.2f} kbps | "
            stats += f"FPS: {fps:.2f}"
            
            self.statsLabel.config(text=stats)
    
    def handler(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.exitClient()


def main():
    """Main function"""
    if len(sys.argv) < 5:
        print("Usage: python Client.py <server_addr> <server_port> <rtp_port> <video_file>")
        print("Example: python Client.py localhost 8554 25000 video/movie.Mjpeg")
        sys.exit(1)
    
    serverAddr = sys.argv[1]
    serverPort = sys.argv[2]
    rtpPort = sys.argv[3]
    videoFile = sys.argv[4]
    
    # Create GUI
    root = Tk()
    app = Client(root, serverAddr, serverPort, rtpPort, videoFile)
    root.mainloop()


if __name__ == '__main__':
    main()
