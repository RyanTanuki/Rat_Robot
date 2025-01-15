"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2-Opencv人脸识别并跟随旋转云台
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

import cv2

from XRPid import PID
import math
from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()

class XRFaceRec():
    def __init__(self) -> None:
        # 实例化一个X轴坐标的PID算法PID参数：第一个代表pid的P值，二代表I值,三代表D值
        self.xPid = PID(0.035, 0.008, 0.0005)
        # 设置PID算法的周期
        self.xPid.setSampleTime(0.005)
        # 设置PID算法的预值点，即目标值，这里160指的是屏幕框的x轴中心点，x轴的像素是480，一半是160
        self.xPid.setPoint(320)
       
        self.yPid = PID(0.035, 0.004, 0.005)
        self.yPid.setSampleTime(0.005)
        self.yPid.setPoint(240)

        self.servo_X = 7    #设置x轴舵机号
        self.servo_Y = 8 

        self.faceCascade = cv2.CascadeClassifier(
            '/home/pi/work/python_src/face.xml')
        self.angle_X = 90
        self.angle_Y = 10


    def decodeImage(self, image):
        """解析图片数据

        Args:
            image ([type]): 视频流数据

        Returns:
            [type]: 需要转动的X和Y的舵机角度以及处理过后的图片数据
        """
        res = image
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray)  # 查找人脸
        if len(faces)>0 and len(faces)<2:        #当视频中有人脸轮廓时
            #print('face found!')
            for (x,y,w,h) in faces:
                #参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
                cv2.rectangle(res,(x,y),(x+h,y+w),(0,255,0),2)

                result = (x,y,w,h)

                x_middle = result[0] + w/2      #x轴中心
                y_middle = result[1] + h / 2    #y轴中心

                #print("x_middle==%d"%x_middle)  
                #print("y_middle==%d"%y_middle)  

                self.xPid .update(x_middle)      #将X轴数据放入pid中计算输出值
                self.yPid .update(y_middle)      #将Y轴数据放入pid中计算输出值
                #print("X_pid.output==%d"%X_pid.output)     #打印X输出
                #print("Y_pid.output==%d"%Y_pid.output)     #打印Y输出
                self.angle_X = math.ceil(self.angle_X + 0.3 * self.xPid .output)     #更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                self.angle_Y = math.ceil(self.angle_Y + 0.2 * self.yPid .output)   #更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                #print("angle_X-----%d" % angle_X)  #打印X轴舵机角度
                #print("angle_Y-----%d" % angle_Y)  #打印Y轴舵机角度
                if self.angle_X > 170:       #限制X轴最大角度
                    self.angle_X = 170
                if self.angle_X < 10:         #限制X轴最小角度
                    self.angle_X = 10
                if self.angle_Y > 130:       #限制Y轴最大角度
                    self.angle_Y = 130
                if self.angle_Y < 5:         #限制Y轴最小角度
                    self.angle_Y = 5

                Servo.XiaoRGEEK_SetServoAngle(self.servo_X, self.angle_X)
                Servo.XiaoRGEEK_SetServoAngle(self.servo_Y, self.angle_Y)
        return res


if __name__ == "__main__":
    qrRec = XRFaceRec()
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, image = cap.read()
            if ret:
                # image = image.resize()
                image = qrRec.decodeImage(image)
                cv2.imshow("qrcode", image)
                cv2.waitKey(1)
    except Exception as e:
        print(e)
    cv2.destroyAllWindows()
    cap.release()
