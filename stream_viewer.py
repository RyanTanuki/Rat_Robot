import cv2
import numpy as np
import urllib.request
import time

def view_stream(url="http://192.168.68.80:8080"):
    """
    Display video stream from the robot's camera
    
    Args:
        url (str): URL of the mjpg stream
    """
    stream_url = f"{url}/?action=stream"
    print(f"Connecting to stream at {stream_url}")
    
    try:
        while True:
            # Try to connect to stream
            try:
                stream = urllib.request.urlopen(stream_url)
                print("Successfully connected to stream")
                break
            except Exception as e:
                print(f"Connection failed: {e}")
                print("Retrying in 2 seconds...")
                time.sleep(2)
                continue
                
        bytes_buffer = b''
        
        while True:
            bytes_buffer += stream.read(1024)
            a = bytes_buffer.find(b'\xff\xd8')  # JPEG start
            b = bytes_buffer.find(b'\xff\xd9')  # JPEG end
            
            if a != -1 and b != -1:
                jpg = bytes_buffer[a:b+2]
                bytes_buffer = bytes_buffer[b+2:]
                
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if frame is None:
                    print("Failed to decode frame, skipping...")
                    continue
                
                cv2.imshow('Robot Camera Stream', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    print("Refreshing stream...")
                    stream = urllib.request.urlopen(stream_url)
                    bytes_buffer = b''
                    
    except Exception as e:
        print(f"Stream error: {e}")
        print("Try checking if:")
        print("1. The robot's camera service is running")
        print("2. The robot's IP and port are correct")
        print("3. You can access the stream URL in a web browser")
        print(f"4. Try accessing {url} directly in browser")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Starting stream viewer...")
    print("Press 'q' to quit, 'r' to refresh stream")
    
    try:
        view_stream()
    except KeyboardInterrupt:
        print("\nStream viewer stopped by user")
    finally:
        cv2.destroyAllWindows() 