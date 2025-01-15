# -*- coding:utf-8 -*-
"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2-Opencv颜色识别并跟随旋转云台
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
from XRPid import PID
import cv2
import numpy as np
from XRConfig import colorDist
from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()
import math
import xr_config as cfg

class XRColorRec():
    def __init__(self) -> None:
        self.colorDist = colorDist
        self.isRec = False
        self.color = ""
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

        self.angle_X = 90
        self.angle_Y = 10

    def decodeImage(self, image):
        """解析图片数据

        Args:
            image ([type]): 原视频流数据

        Returns:
            [type]: 返回识别结果与视频流
        """   
        if cfg.COLOR_INDEX == cfg.COLOR_FOLLOW_SET['none']: #如果没有选择颜色，则什么都不做，直接返回视频流即可
            cv2.putText(image, "Please select a color in APP", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)
            return image

        frame = image
        res = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsv, self.colorDist[cfg.COLOR_FOLLOW_INDEX[cfg.COLOR_INDEX]]["Lower"], self.colorDist[cfg.COLOR_FOLLOW_INDEX[cfg.COLOR_INDEX]]["Upper"])
        
        #print(self.colorDist[cfg.COLOR_FOLLOW_INDEX[cfg.COLOR_INDEX]])

        mask = cv2.erode(mask, None, iterations=2)
        # 膨胀
        mask = cv2.dilate(mask, None, iterations=2)
        # 查找轮廓
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0 :
            c = max(cnts, key=cv2.contourArea)
            # 求出最小外接圆  原点坐标x, y  和半径
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius >= 5:  # 半径大于70才算，然后在屏幕画圆
                cv2.circle(res, (int(x), int(y)),
                            int(radius), (0, 255, 255), 2)
                x_middle = x      #x轴中心
                y_middle = y      #y轴中心

                self.xPid .update(x_middle)      #将X轴数据放入pid中计算输出值
                self.yPid .update(y_middle)      #将Y轴数据放入pid中计算输出值

                self.angle_X = math.ceil(self.angle_X + 0.3 * self.xPid .output)     #更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                self.angle_Y = math.ceil(self.angle_Y + 0.2 * self.yPid .output)   #更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度

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

                self.isRec = True  # 设置检测的标志位，交由后台线程做操作
            else:

                self.isRec = False
            #text = "color: {}".format(i)
            #cv2.putText(res, text, (int(x), int(y - 10)),
                        #cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)
        return res

if __name__ == "__main__":
    colorRec = XRColorRec()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 10)
    try:
        while True:
            ret, image = cap.read()
            if ret:
                image = colorRec.decodeImage(image)
                cv2.imshow("qrcode", image)
                cv2.waitKey(1)
    except Exception as e:
        print(e)
    cv2.destroyAllWindows()
    cap.release()
