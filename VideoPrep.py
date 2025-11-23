"""
Video Preparation Utility
Convert video files to MJPEG format for streaming
"""

import sys
import cv2
import os


def video_to_mjpeg(input_file, output_file, fps=20):
    """
    Convert a video file to MJPEG format
    
    Args:
        input_file: Input video file path
        output_file: Output MJPEG file path
        fps: Target frames per second (default: 20)
    """
    try:
        # Open video file
        cap = cv2.VideoCapture(input_file)
        
        if not cap.isOpened():
            print(f"Error: Cannot open video file {input_file}")
            return False
        
        # Get video properties
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Input video: {input_file}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {original_fps}")
        print(f"Total frames: {frame_count}")
        print(f"Target FPS: {fps}")
        
        # Calculate frame skip for target FPS
        frame_skip = max(1, int(original_fps / fps))
        
        # Open output file
        with open(output_file, 'wb') as outfile:
            frame_num = 0
            written_frames = 0
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Skip frames to achieve target FPS
                if frame_num % frame_skip == 0:
                    # Encode frame as JPEG
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                    
                    if result:
                        # Get frame data
                        frame_data = encoded_frame.tobytes()
                        frame_length = len(frame_data)
                        
                        # Write frame length (5 bytes) followed by frame data
                        outfile.write(str(frame_length).zfill(5).encode())
                        outfile.write(frame_data)
                        
                        written_frames += 1
                        
                        if written_frames % 10 == 0:
                            print(f"Processed {written_frames} frames...", end='\r')
                
                frame_num += 1
            
            print(f"\nConversion complete!")
            print(f"Written {written_frames} frames to {output_file}")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"Error converting video: {e}")
        return False


def create_test_video(output_file, duration=10, fps=20, width=640, height=480):
    """
    Create a test video with colored frames
    
    Args:
        output_file: Output MJPEG file path
        duration: Video duration in seconds
        fps: Frames per second
        width: Frame width
        height: Frame height
    """
    try:
        import numpy as np
        
        print(f"Creating test video: {output_file}")
        print(f"Duration: {duration}s, FPS: {fps}, Resolution: {width}x{height}")
        
        total_frames = duration * fps
        
        with open(output_file, 'wb') as outfile:
            for i in range(total_frames):
                # Create colored frame (cycling through colors)
                hue = int((i / total_frames) * 180)
                frame = np.ones((height, width, 3), dtype=np.uint8)
                frame[:, :] = cv2.cvtColor(
                    np.array([[[hue, 255, 255]]], dtype=np.uint8),
                    cv2.COLOR_HSV2BGR
                )[0][0]
                
                # Add frame number text
                text = f"Frame {i+1}/{total_frames}"
                cv2.putText(frame, text, (50, height//2),
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                
                # Encode as JPEG
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                
                if result:
                    frame_data = encoded_frame.tobytes()
                    frame_length = len(frame_data)
                    
                    # Write frame
                    outfile.write(str(frame_length).zfill(5).encode())
                    outfile.write(frame_data)
                    
                    if (i + 1) % 10 == 0:
                        print(f"Created {i+1}/{total_frames} frames...", end='\r')
            
            print(f"\nTest video created successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error creating test video: {e}")
        return False


def get_video_info(mjpeg_file):
    """
    Display information about an MJPEG file
    
    Args:
        mjpeg_file: MJPEG file path
    """
    try:
        with open(mjpeg_file, 'rb') as infile:
            frame_count = 0
            total_size = 0
            
            while True:
                # Read frame length
                length_data = infile.read(5)
                if not length_data or len(length_data) < 5:
                    break
                
                frame_length = int(length_data)
                
                # Skip frame data
                infile.seek(frame_length, 1)
                
                frame_count += 1
                total_size += frame_length
            
            print(f"\nMJPEG File Info: {mjpeg_file}")
            print(f"Total frames: {frame_count}")
            print(f"Total size: {total_size / 1024:.2f} KB")
            print(f"Average frame size: {total_size / frame_count if frame_count > 0 else 0:.2f} bytes")
        
    except Exception as e:
        print(f"Error reading MJPEG file: {e}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Video Preparation Utility for RTSP/RTP Streaming")
        print("\nUsage:")
        print("  Convert video:")
        print("    python VideoPrep.py convert <input_video> <output_mjpeg> [fps]")
        print("    Example: python VideoPrep.py convert sample.mp4 video/movie.Mjpeg 20")
        print("\n  Create test video:")
        print("    python VideoPrep.py test <output_mjpeg> [duration] [fps]")
        print("    Example: python VideoPrep.py test video/test.Mjpeg 10 20")
        print("\n  Get video info:")
        print("    python VideoPrep.py info <mjpeg_file>")
        print("    Example: python VideoPrep.py info video/movie.Mjpeg")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'convert':
        if len(sys.argv) < 4:
            print("Error: Missing arguments for convert command")
            print("Usage: python VideoPrep.py convert <input_video> <output_mjpeg> [fps]")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        fps = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found")
            sys.exit(1)
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        video_to_mjpeg(input_file, output_file, fps)
    
    elif command == 'test':
        if len(sys.argv) < 3:
            print("Error: Missing arguments for test command")
            print("Usage: python VideoPrep.py test <output_mjpeg> [duration] [fps]")
            sys.exit(1)
        
        output_file = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        fps = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        create_test_video(output_file, duration, fps)
    
    elif command == 'info':
        if len(sys.argv) < 3:
            print("Error: Missing arguments for info command")
            print("Usage: python VideoPrep.py info <mjpeg_file>")
            sys.exit(1)
        
        mjpeg_file = sys.argv[2]
        
        if not os.path.exists(mjpeg_file):
            print(f"Error: File {mjpeg_file} not found")
            sys.exit(1)
        
        get_video_info(mjpeg_file)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Valid commands: convert, test, info")
        sys.exit(1)


if __name__ == '__main__':
    main()
