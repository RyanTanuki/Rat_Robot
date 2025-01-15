"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2-Opencv二维码识别并跟随旋转云台
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
import pyzbar.pyzbar as pyzbar
import cv2
from xr_motor import RobotDirection
go = RobotDirection()
import time

class XRQRCodeRec():

    def __init__(self):
        self.BARCODE_DATE = None  # 二维码识别数据
        self.BARCODE_TYPE = None  # 二维码识别数据类型
        self.isRec = False  # 识别到二维码的标志位

    def decodeImage(self, image):
        """图像数据解码

        Args:
            image ([type]): 图像

        Returns:
            [type]: 二维码识别结果
        """
        barcodes = pyzbar.decode(image)
        if barcodes == []:
            self.isRec = False
            self.BARCODE_DATE = None
            self.BARCODE_TYPE = None
            go.stop()
        else:
            for barcode in barcodes:
                if self.isRec == False:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    self.BARCODE_DATE = barcode.data.decode("utf-8")
                    self.BARCODE_TYPE = barcode.type
                    text = "{} ({})".format(self.BARCODE_DATE, self.BARCODE_TYPE)
                    cv2.putText(image, text, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)
                    if self.BARCODE_DATE =="forward":
                        go.forward()
                    elif self.BARCODE_DATE =="back":
                        go.back()
                    elif self.BARCODE_DATE =="left":
                        go.left()
                    elif self.BARCODE_DATE =="right":
                        go.right()
                    self.isRec = True
        return image


if __name__ == "__main__":
    qrRec = XRQRCodeRec()
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, image = cap.read()
            if ret:
                image = qrRec.decodeImage(image)
                cv2.imshow("qrcode", image)
                cv2.waitKey(1)
    except Exception as e:
        print(e)
    cv2.destroyAllWindows()
    cap.release()

