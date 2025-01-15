"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2
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
import numpy as np

# 颜色识别的识别的字典
colorDist = {
    'red': {'Lower': np.array([0,127,128]), 'Upper': np.array([10,255,255])},
    'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
    'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
}

# 要识别的颜色的键值
recColor = 'red'
recMode = 'default'
# AI功能模式
TYPE_QR_MODE = "qr"
TYPE_FACE_MODE = "face"
TYPE_COLOR_MODE = "color"
# socket server
SOCKET_HOST = "http://localhost:5051"

#动作组执行标志位，如果正在执行动作，则不能继续下发命令
ACTION_FINISHED_FLAG = True

timer_start = 0
timer_end = 0
