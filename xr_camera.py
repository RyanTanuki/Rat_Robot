"""
Robot Camera Control Module
-------------------------
Handles the robot's camera operations including initialization, 
streaming, and frame processing.

This module provides the interface between the physical camera
hardware and the web streaming service.

Dependencies:
- OpenCV (cv2)
- numpy
- threading
"""

import cv2
import numpy as np
import threading
import time

class Camera:
    """
    Camera control class for robot video streaming.
    
    Handles camera initialization, frame capture, and processing
    for the web interface video stream.
    """

    def __init__(self):
        """
        Initialize camera controller.
        Sets up camera parameters and initializes frame buffer.
        """
        self.frame = None
        self.last_access = 0
        self.is_running = False
        self.thread = None
        self.camera = None

    def initialize(self):
        """
        Initialize camera hardware and start capture thread.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False

    def get_frame(self):
        """
        Retrieve the latest frame from the camera.
        
        Returns:
            numpy.ndarray: Current camera frame or None if no frame available
        """
        self.last_access = time.time()
        return self.frame

    def capture_loop(self):
        """
        Main capture loop that continuously reads frames from the camera.
        Runs in a separate thread to maintain smooth frame capture.
        """
        while self.is_running:
            try:
                _, self.frame = self.camera.read()
                time.sleep(0.01)  # Small delay to prevent CPU overload
            except Exception as e:
                print(f"Frame capture error: {e}")
                break

    def start(self):
        """
        Start the camera capture thread.
        
        Returns:
            bool: True if camera started successfully, False otherwise
        """
        if self.initialize():
            self.is_running = True
            self.thread = threading.Thread(target=self.capture_loop)
            self.thread.start()
            return True
        return False

    def stop(self):
        """
        Stop the camera capture and release resources.
        """
        self.is_running = False
        if self.thread:
            self.thread.join()
        if self.camera:
            self.camera.release()

    def __del__(self):
        """
        Cleanup method to ensure camera resources are released.
        """
        self.stop() 