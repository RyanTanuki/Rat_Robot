# coding:utf-8
"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2---OpenCV识别相关功能
作者:liuviking
版权所有:小R科技(深圳市小二极客科技有限公司www.xiao-r.com) WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
商务合作微信:18126008008
联系电话:0755-28915204
@version: python3.7
@Author  : liuviking
@Time    :2023/05/07
"""
from builtins import range, len, int
import os
from subprocess import call
import time
import math
import pyzbar.pyzbar as pyzbar
import urllib.request
import numpy as np
import xr_config as cfg
from XRColorRec import XRColorRec
from XRFaceRec import XRFaceRec
from XRQRCodeRec import XRQRCodeRec
from xr_motor import RobotDirection

go = RobotDirection()
import cv2

from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()

from flask import Flask, Response

class Camera(object):
    def __init__(self):
        # 打开opencv视频流
        self.cap = cv2.VideoCapture(0)

        self.qrRec = XRQRCodeRec()
        self.colorRec = XRColorRec()
        self.faceRec = XRFaceRec()
         # flask推流处理
        self.app = Flask(__name__)

        @self.app.route('/', methods=['get'])  # 这个地址返回视频流响应
        def video_feed():
            return Response(self.backgroundTask(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def backgroundTask(self):
        frame_count = 0
        last_time = time.time()
        
        try:
            while True:
                current_time = time.time()
                ret, image = self.cap.read()
                
                if ret:
                    frame_count += 1
                    # Print stats every 30 frames
                    if frame_count % 30 == 0:
                        elapsed = current_time - last_time
                        fps = 30 / elapsed
                        print(f"Camera FPS: {fps:.2f}")
                        last_time = current_time
                        frame_count = 0  # Reset counter
                        
                    if cfg.CAMERA_MOD == 0:
                        pass
                    elif cfg.CAMERA_MOD == 2:
                        image =  self.faceRec.decodeImage(image)
                    elif cfg.CAMERA_MOD == 3:
                        image =  self.colorRec.decodeImage(image)
                    elif cfg.CAMERA_MOD == 4:
                        image =  self.qrRec.decodeImage(image)
                        
                    ret, buffer = cv2.imencode('.jpg', image)
                    res = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + res + b'\r\n\r\n')
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            print("ctrl + c, stop video stream")


    def run(self):
        """
        Start the camera server
        """
        try:
            print("Starting camera server on port 8080...")  # Add debug print
            self.app.run("0.0.0.0", 8080, debug=False, threaded=True)
        except Exception as e:
            print(f"Camera server error: {e}")  # Add error logging
        
    def __del__(self):
        """Destructor to ensure camera resources are released"""
        if hasattr(self, 'cap'):
            self.cap.release()
        
