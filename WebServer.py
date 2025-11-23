"""
Web-based RTSP/RTP Video Streaming Client
Uses Flask and WebSocket for browser-based video streaming
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import socket
import threading
import time
import base64
import subprocess
import sys
import os
from RtpPacket import RtpPacket
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'video-streaming-secret'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# RTSP States
INIT = 0
READY = 1
PLAYING = 2

# Active sessions storage
sessions = {}

# RTSP Server process
rtsp_server_process = None
server_running = False


class WebStreamingClient:
    """Web-based streaming client handler"""
    
    def __init__(self, client_id, server_addr, server_port, video_file):
        self.client_id = client_id
        self.server_addr = server_addr
        self.server_port = int(server_port)
        self.video_file = video_file
        
        # RTSP/RTP parameters
        self.rtsp_socket = None
        self.rtp_socket = None
        self.rtp_port = 25000 + (hash(client_id) % 1000)
        self.rtsp_seq = 0
        self.session_id = 0
        self.state = INIT
        
        # Statistics
        self.frame_num = 0
        self.packets_received = 0
        self.bytes_received = 0
        self.start_time = 0
        
        # Threading
        self.rtp_thread = None
        self.stop_event = threading.Event()
    
    def setup(self):
        """Send SETUP request"""
        try:
            # Create RTSP socket
            self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.rtsp_socket.connect((self.server_addr, self.server_port))
            
            # Create RTP socket
            self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.rtp_socket.settimeout(0.5)
            self.rtp_socket.bind(('', self.rtp_port))
            
            # Send SETUP request
            self.rtsp_seq += 1
            request = f"SETUP {self.video_file} RTSP/1.0\n"
            request += f"CSeq: {self.rtsp_seq}\n"
            request += f"Transport: RTP/AVP;unicast;client_port={self.rtp_port}\n"
            
            self.rtsp_socket.send(request.encode('utf-8'))
            
            # Receive reply
            reply = self.rtsp_socket.recv(1024).decode('utf-8')
            lines = reply.split('\n')
            
            # Parse session ID
            for line in lines:
                if line.startswith('Session:'):
                    self.session_id = int(line.split(' ')[1])
                    break
            
            self.state = READY
            
            return {
                'success': True,
                'message': 'Setup successful',
                'session_id': self.session_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Setup failed: {str(e)}'
            }
    
    def play(self):
        """Send PLAY request"""
        if self.state != READY:
            return {'success': False, 'message': 'Not in READY state'}
        
        try:
            # Send PLAY request
            self.rtsp_seq += 1
            request = f"PLAY {self.video_file} RTSP/1.0\n"
            request += f"CSeq: {self.rtsp_seq}\n"
            request += f"Session: {self.session_id}\n"
            
            self.rtsp_socket.send(request.encode('utf-8'))
            
            # Receive reply
            reply = self.rtsp_socket.recv(1024).decode('utf-8')
            
            self.state = PLAYING
            self.start_time = time.time()
            
            # Start RTP receiving thread
            self.stop_event.clear()
            self.rtp_thread = threading.Thread(target=self.listen_rtp)
            self.rtp_thread.start()
            
            return {'success': True, 'message': 'Playing'}
            
        except Exception as e:
            return {'success': False, 'message': f'Play failed: {str(e)}'}
    
    def pause(self):
        """Send PAUSE request"""
        if self.state != PLAYING:
            return {'success': False, 'message': 'Not playing'}
        
        try:
            # Send PAUSE request
            self.rtsp_seq += 1
            request = f"PAUSE {self.video_file} RTSP/1.0\n"
            request += f"CSeq: {self.rtsp_seq}\n"
            request += f"Session: {self.session_id}\n"
            
            self.rtsp_socket.send(request.encode('utf-8'))
            
            # Receive reply
            reply = self.rtsp_socket.recv(1024).decode('utf-8')
            
            self.state = READY
            
            # Stop RTP thread
            self.stop_event.set()
            if self.rtp_thread:
                self.rtp_thread.join()
            
            return {'success': True, 'message': 'Paused'}
            
        except Exception as e:
            return {'success': False, 'message': f'Pause failed: {str(e)}'}
    
    def teardown(self):
        """Send TEARDOWN request"""
        try:
            # Send TEARDOWN request
            self.rtsp_seq += 1
            request = f"TEARDOWN {self.video_file} RTSP/1.0\n"
            request += f"CSeq: {self.rtsp_seq}\n"
            request += f"Session: {self.session_id}\n"
            
            if self.rtsp_socket:
                self.rtsp_socket.send(request.encode('utf-8'))
                
                # Receive reply
                try:
                    reply = self.rtsp_socket.recv(1024).decode('utf-8')
                except:
                    pass
            
            # Stop RTP thread
            self.stop_event.set()
            if self.rtp_thread:
                self.rtp_thread.join()
            
            # Close sockets
            if self.rtp_socket:
                self.rtp_socket.close()
            if self.rtsp_socket:
                self.rtsp_socket.close()
            
            self.state = INIT
            
            return {'success': True, 'message': 'Teardown complete'}
            
        except Exception as e:
            return {'success': False, 'message': f'Teardown failed: {str(e)}'}
    
    def listen_rtp(self):
        """Listen for RTP packets and send to browser via WebSocket"""
        while not self.stop_event.is_set():
            try:
                # Receive RTP packet
                data, addr = self.rtp_socket.recvfrom(20480)
                
                if data:
                    # Decode RTP packet
                    rtp_packet = RtpPacket()
                    rtp_packet.decode(data)
                    
                    # Update statistics
                    self.packets_received += 1
                    self.bytes_received += len(data)
                    self.frame_num = rtp_packet.getSeqNum()
                    
                    # Get frame data
                    payload = rtp_packet.getPayload()
                    
                    # Convert to base64 for transmission to browser
                    frame_b64 = base64.b64encode(payload).decode('utf-8')
                    
                    # Calculate statistics
                    elapsed = time.time() - self.start_time if self.start_time > 0 else 1
                    data_rate = (self.bytes_received * 8) / (elapsed * 1000)
                    fps = self.packets_received / elapsed if elapsed > 0 else 0
                    
                    # Send frame to browser
                    socketio.emit('video_frame', {
                        'frame': frame_b64,
                        'frame_num': self.frame_num,
                        'packets': self.packets_received,
                        'data_rate': round(data_rate, 2),
                        'fps': round(fps, 2)
                    }, room=self.client_id)
                    
            except socket.timeout:
                continue
            except Exception as e:
                if not self.stop_event.is_set():
                    print(f"[WebClient] Error receiving RTP: {e}")
                break


# Flask routes
@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get default configuration"""
    return jsonify({
        'server_addr': 'localhost',
        'server_port': 8554,
        'video_file': 'video/movie.Mjpeg'
    })


# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"[WebServer] Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to streaming server'})
    
    # Send current server status
    emit('rtsp_server_status', {
        'running': server_running,
        'message': 'Server is running' if server_running else 'Server is stopped'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    client_id = request.sid
    print(f"[WebServer] Client disconnected: {client_id}")
    
    # Teardown session if exists
    if client_id in sessions:
        sessions[client_id].teardown()
        del sessions[client_id]


@socketio.on('check_server_status')
def handle_check_server_status():
    """Check if RTSP server is running"""
    emit('rtsp_server_status', {
        'running': server_running,
        'message': 'Server is running' if server_running else 'Server is stopped'
    })


@socketio.on('start_server')
def handle_start_server():
    """Start the RTSP/RTP Server"""
    global rtsp_server_process, server_running
    
    if server_running:
        emit('server_output', {
            'success': False,
            'message': 'RTSP Server is already running'
        })
        return
    
    try:
        # Start Server.py as a subprocess
        server_script = os.path.join(os.path.dirname(__file__), 'Server.py')
        rtsp_server_process = subprocess.Popen(
            [sys.executable, server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give server time to start
        time.sleep(2)
        
        # Check if server started successfully
        if rtsp_server_process.poll() is None:
            server_running = True
            socketio.emit('rtsp_server_status', {
                'running': True,
                'message': 'RTSP/RTP Server started successfully on port 8554'
            }, broadcast=True)
            print("[WebServer] RTSP Server started successfully")
        else:
            server_running = False
            socketio.emit('server_output', {
                'success': False,
                'message': 'Failed to start RTSP Server'
            })
            
    except Exception as e:
        server_running = False
        emit('server_output', {
            'success': False,
            'message': f'Error starting server: {str(e)}'
        })
        print(f"[WebServer] Error starting RTSP Server: {e}")


@socketio.on('stop_server')
def handle_stop_server():
    """Stop the RTSP/RTP Server"""
    global rtsp_server_process, server_running
    
    if not server_running:
        emit('server_output', {
            'success': False,
            'message': 'RTSP Server is not running'
        })
        return
    
    try:
        # Close all client sessions first
        for client_id in list(sessions.keys()):
            sessions[client_id].teardown()
            del sessions[client_id]
        
        # Terminate the server process
        if rtsp_server_process:
            rtsp_server_process.terminate()
            rtsp_server_process.wait(timeout=5)
            rtsp_server_process = None
        
        server_running = False
        socketio.emit('rtsp_server_status', {
            'running': False,
            'message': 'RTSP/RTP Server stopped'
        }, broadcast=True)
        print("[WebServer] RTSP Server stopped")
        
    except Exception as e:
        emit('server_output', {
            'success': False,
            'message': f'Error stopping server: {str(e)}'
        })
        print(f"[WebServer] Error stopping RTSP Server: {e}")


@socketio.on('setup')
def handle_setup(data):
    """Handle SETUP request from browser"""
    client_id = request.sid
    server_addr = data.get('server_addr', 'localhost')
    server_port = data.get('server_port', 8554)
    video_file = data.get('video_file', 'video/movie.Mjpeg')
    
    print(f"[WebServer] Setup request from {client_id}")
    
    # Create new session
    client = WebStreamingClient(client_id, server_addr, server_port, video_file)
    result = client.setup()
    
    if result['success']:
        sessions[client_id] = client
    
    emit('setup_response', result)


@socketio.on('play')
def handle_play():
    """Handle PLAY request from browser"""
    client_id = request.sid
    
    if client_id not in sessions:
        emit('play_response', {'success': False, 'message': 'No session found'})
        return
    
    print(f"[WebServer] Play request from {client_id}")
    result = sessions[client_id].play()
    emit('play_response', result)


@socketio.on('pause')
def handle_pause():
    """Handle PAUSE request from browser"""
    client_id = request.sid
    
    if client_id not in sessions:
        emit('pause_response', {'success': False, 'message': 'No session found'})
        return
    
    print(f"[WebServer] Pause request from {client_id}")
    result = sessions[client_id].pause()
    emit('pause_response', result)


@socketio.on('teardown')
def handle_teardown():
    """Handle TEARDOWN request from browser"""
    client_id = request.sid
    
    if client_id not in sessions:
        emit('teardown_response', {'success': False, 'message': 'No session found'})
        return
    
    print(f"[WebServer] Teardown request from {client_id}")
    result = sessions[client_id].teardown()
    
    if result['success']:
        del sessions[client_id]
    
    emit('teardown_response', result)


def main():
    """Main function"""
    global rtsp_server_process, server_running
    
    print("=" * 60)
    print("  RTSP/RTP Video Streaming - Web Browser Version")
    print("=" * 60)
    print("\n[WebServer] Starting web server...")
    print("[WebServer] Open your browser and go to: http://localhost:5000")
    print("[WebServer] Use the web interface to control the RTSP server")
    print("[WebServer] Press Ctrl+C to stop\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n[WebServer] Shutting down...")
        
        # Stop RTSP server if running
        if server_running and rtsp_server_process:
            print("[WebServer] Stopping RTSP Server...")
            rtsp_server_process.terminate()
            rtsp_server_process.wait(timeout=5)
        
        print("[WebServer] Shutdown complete")


if __name__ == '__main__':
    main()
