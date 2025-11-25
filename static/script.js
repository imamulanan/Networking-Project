// WebSocket connection
let socket = null;
let isConnected = false;

// Initialize WebSocket connection
function initializeSocket() {
    socket = io();

    socket.on('connect', () => {
        isConnected = true;
        updateStatus('connected', 'Connected to WebSocket');
        addLog('Connected to web server', 'success');
        
        // Check server status on connect
        socket.emit('check_server_status');
    });

    socket.on('disconnect', () => {
        isConnected = false;
        updateStatus('disconnected', 'Disconnected');
        addLog('Disconnected from web server', 'error');
        disableAllButtons();
    });

    socket.on('video_frame', (data) => {
        displayFrame(data);
    });

    socket.on('setup_response', (response) => {
        handleSetupResponse(response);
    });

    socket.on('play_response', (response) => {
        handlePlayResponse(response);
    });

    socket.on('pause_response', (response) => {
        handlePauseResponse(response);
    });

    socket.on('teardown_response', (response) => {
        handleTeardownResponse(response);
    });

    socket.on('rtsp_server_status', (data) => {
        updateServerStatus(data.running, data.message);
    });

    socket.on('server_output', (data) => {
        addLog('Server: ' + data.message, data.success ? 'success' : 'error');
    });
}

// Server Control Functions
function startRtspServer() {
    if (!isConnected) {
        addLog('Not connected to web server', 'error');
        return;
    }

    addLog('Starting RTSP/RTP Server...', 'info');
    socket.emit('start_server');
    document.getElementById('startServerBtn').disabled = true;
}

function stopRtspServer() {
    if (!isConnected) {
        addLog('Not connected to web server', 'error');
        return;
    }

    addLog('Stopping RTSP/RTP Server...', 'info');
    socket.emit('stop_server');
    document.getElementById('stopServerBtn').disabled = true;
}

function updateServerStatus(isRunning, message = '') {
    const statusText = document.getElementById('rtspServerStatus');
    const statusDot = document.getElementById('rtspServerDot');
    const startBtn = document.getElementById('startServerBtn');
    const stopBtn = document.getElementById('stopServerBtn');
    
    if (isRunning) {
        statusText.textContent = 'Running';
        statusDot.classList.add('running');
        startBtn.disabled = true;
        stopBtn.disabled = false;
        if (message) addLog(message, 'success');
    } else {
        statusText.textContent = 'Stopped';
        statusDot.classList.remove('running');
        startBtn.disabled = false;
        stopBtn.disabled = true;
        if (message) addLog(message, 'info');
    }
}

// Update connection status
function updateStatus(status, text) {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    
    statusDot.className = 'status-dot ' + (status === 'connected' ? 'connected' : '');
    statusText.textContent = text;
}

// Button handlers
function setup() {
    if (!isConnected) {
        addLog('Not connected to web server', 'error');
        return;
    }

    const serverAddr = document.getElementById('serverAddr').value;
    const serverPort = document.getElementById('serverPort').value;
    const videoFile = document.getElementById('videoFile').value;

    addLog(`Sending SETUP request to ${serverAddr}:${serverPort}`, 'info');

    socket.emit('setup', {
        server_addr: serverAddr,
        server_port: parseInt(serverPort),
        video_file: videoFile
    });

    document.getElementById('setupBtn').disabled = true;
}

function play() {
    addLog('Sending PLAY request', 'info');
    socket.emit('play');
    document.getElementById('playBtn').disabled = true;
}

function pause() {
    addLog('Sending PAUSE request', 'info');
    socket.emit('pause');
    document.getElementById('pauseBtn').disabled = true;
}

function teardown() {
    addLog('Sending TEARDOWN request', 'info');
    socket.emit('teardown');
    document.getElementById('teardownBtn').disabled = true;
}

// Response handlers
function handleSetupResponse(response) {
    if (response.success) {
        addLog(`Setup successful! Session ID: ${response.session_id}`, 'success');
        document.getElementById('playBtn').disabled = false;
        document.getElementById('teardownBtn').disabled = false;
        updateStatus('connected', 'Ready to Play');
    } else {
        addLog(`Setup failed: ${response.message}`, 'error');
        document.getElementById('setupBtn').disabled = false;
    }
}

function handlePlayResponse(response) {
    if (response.success) {
        addLog('Playback started', 'success');
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('teardownBtn').disabled = false;
        updateStatus('connected', 'Playing');
    } else {
        addLog(`Play failed: ${response.message}`, 'error');
        document.getElementById('playBtn').disabled = false;
    }
}

function handlePauseResponse(response) {
    if (response.success) {
        addLog('Playback paused', 'success');
        document.getElementById('playBtn').disabled = false;
        document.getElementById('teardownBtn').disabled = false;
        updateStatus('connected', 'Paused');
    } else {
        addLog(`Pause failed: ${response.message}`, 'error');
        document.getElementById('pauseBtn').disabled = false;
    }
}

function handleTeardownResponse(response) {
    if (response.success) {
        addLog('Session terminated', 'success');
        resetUI();
        updateStatus('connected', 'Session Closed');
    } else {
        addLog(`Teardown failed: ${response.message}`, 'error');
    }
}

// Display video frame
function displayFrame(data) {
    const img = document.getElementById('videoFrame');
    img.src = 'data:image/jpeg;base64,' + data.frame;

    // Update statistics
    document.getElementById('frameNum').textContent = data.frame_num;
    document.getElementById('packets').textContent = data.packets;
    document.getElementById('dataRate').textContent = data.data_rate + ' kbps';
    document.getElementById('fps').textContent = data.fps;
}

// Add log entry
function addLog(message, type = 'info') {
    const logContent = document.getElementById('logContent');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.innerHTML = `<span class="log-time">[${timestamp}]</span>${message}`;
    
    logContent.appendChild(logEntry);
    logContent.scrollTop = logContent.scrollHeight;
}

// Clear log
function clearLog() {
    document.getElementById('logContent').innerHTML = '';
    addLog('Log cleared', 'info');
}

// Reset UI
function resetUI() {
    document.getElementById('setupBtn').disabled = false;
    document.getElementById('playBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('teardownBtn').disabled = true;
    
    // Reset statistics
    document.getElementById('frameNum').textContent = '0';
    document.getElementById('packets').textContent = '0';
    document.getElementById('dataRate').textContent = '0.00 kbps';
    document.getElementById('fps').textContent = '0.00';
    
    // Reset video frame
    const img = document.getElementById('videoFrame');
    img.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 480'%3E%3Crect width='640' height='480' fill='%23000'/%3E%3Ctext x='50%25' y='50%25' font-size='24' fill='%23fff' text-anchor='middle' dominant-baseline='middle'%3EClick Setup to Start%3C/text%3E%3C/svg%3E";
}

// Disable all buttons
function disableAllButtons() {
    document.getElementById('setupBtn').disabled = true;
    document.getElementById('playBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('teardownBtn').disabled = true;
}

// Load configuration on page load
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        document.getElementById('serverAddr').value = config.server_addr;
        document.getElementById('serverPort').value = config.server_port;
        document.getElementById('videoFile').value = config.video_file;
    } catch (error) {
        console.error('Error loading config:', error);
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    addLog('Web client initialized', 'info');
    loadConfig();
    initializeSocket();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (socket) {
        socket.disconnect();
    }
});
