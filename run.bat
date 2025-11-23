@echo off
REM Quick Test Script for RTSP/RTP Video Streaming
REM This script helps you quickly test the video streaming system

echo.
echo ========================================
echo  RTSP/RTP Video Streaming - Quick Test
echo ========================================
echo.

:menu
echo Please select an option:
echo.
echo 1. Install dependencies
echo 2. Create test video
echo 3. Start RTSP/RTP server
echo 4. Start desktop client
echo 5. Start web server (BROWSER VERSION)
echo 6. Get video info
echo 7. Convert video to MJPEG
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto createvideo
if "%choice%"=="3" goto server
if "%choice%"=="4" goto client
if "%choice%"=="5" goto webserver
if "%choice%"=="6" goto videoinfo
if "%choice%"=="7" goto convert
if "%choice%"=="8" goto end
goto menu

:install
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Dependencies installed!
pause
goto menu

:createvideo
echo.
set /p duration="Enter video duration in seconds (default: 10): "
if "%duration%"=="" set duration=10
set /p fps="Enter FPS (default: 20): "
if "%fps%"=="" set fps=20
echo.
echo Creating test video: video/movie.Mjpeg (%duration%s at %fps% FPS)...
python VideoPrep.py test video/movie.Mjpeg %duration% %fps%
echo.
echo Test video created!
pause
goto menu

:server
echo.
echo Starting RTSP/RTP Server...
echo Press Ctrl+C to stop the server
echo.
python Server.py
pause
goto menu

:client
echo.
echo Client Configuration:
set /p serveraddr="Server address (default: localhost): "
if "%serveraddr%"=="" set serveraddr=localhost
set /p serverport="Server port (default: 8554): "
if "%serverport%"=="" set serverport=8554
set /p rtpport="RTP port (default: 25000): "
if "%rtpport%"=="" set rtpport=25000
set /p videofile="Video file (default: video/movie.Mjpeg): "
if "%videofile%"=="" set videofile=video/movie.Mjpeg
echo.
echo Starting desktop client...
echo Server: %serveraddr%:%serverport%
echo RTP Port: %rtpport%
echo Video: %videofile%
echo.
python Client.py %serveraddr% %serverport% %rtpport% %videofile%
pause
goto menu

:webserver
echo.
echo ========================================
echo  STARTING WEB SERVER (BROWSER VERSION)
echo ========================================
echo.
echo The web server will start on http://localhost:5000
echo.
echo IMPORTANT: Make sure the RTSP/RTP server is running first!
echo            (Option 3 from main menu)
echo.
echo After starting, open your browser and go to:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the web server
echo.
pause
python WebServer.py
pause
goto menu

:videoinfo
echo.
set /p mjpegfile="Enter MJPEG file path (default: video/movie.Mjpeg): "
if "%mjpegfile%"=="" set mjpegfile=video/movie.Mjpeg
echo.
python VideoPrep.py info %mjpegfile%
echo.
pause
goto menu

:convert
echo.
set /p inputfile="Enter input video file path: "
set /p outputfile="Enter output MJPEG file path (default: video/converted.Mjpeg): "
if "%outputfile%"=="" set outputfile=video/converted.Mjpeg
set /p fps="Enter target FPS (default: 20): "
if "%fps%"=="" set fps=20
echo.
echo Converting video...
python VideoPrep.py convert "%inputfile%" "%outputfile%" %fps%
echo.
echo Conversion complete!
pause
goto menu

:end
echo.
echo Thank you for using RTSP/RTP Video Streaming!
echo.
exit /b 0
