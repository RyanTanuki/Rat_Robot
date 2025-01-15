"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2--红外传感器相关功能
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
import xr_gpio as gpio
import xr_config as cfg

from xr_motor import RobotDirection

go = RobotDirection()


class Infrared(object):
	def __init__(self):
		pass

	def trackline(self):
		"""
		红外巡线
		"""
		cfg.LEFT_SPEED = 40
		cfg.RIGHT_SPEED = 40
		# print('ir_trackline run...')
		# 两边都没有检测到黑线
		if (gpio.digital_read(gpio.IR_L_GPIO) == 0) and (gpio.digital_read(gpio.IR_R_GPIO) == 0):  # 黑线为高，地面为低
			go.forward()
		# 右边红外传感器检测到黑线
		elif (gpio.digital_read(gpio.IR_L_GPIO) == 0) and (gpio.digital_read(gpio.IR_R_GPIO) == 1):
			go.left()
		# 左边传感器检测到黑线
		elif (gpio.digital_read(gpio.IR_L_GPIO) == 1) and (gpio.digital_read(gpio.IR_R_GPIO) == 0):
			go.right()
		# 两边同时检测到黑线
		elif (gpio.digital_read(gpio.IR_L_GPIO) == 1) and (gpio.digital_read(gpio.IR_R_GPIO) == 1):
			go.stop()

	def iravoid(self):
		"""
		红外避障
		"""
		if gpio.digital_read(gpio.IR_M_GPIO) == 0:		# 如果中间传感器校测到物体
			go.stop()
		# print("红外避障")

	def irfollow(self):
		"""
		红外跟随
		"""
		cfg.LEFT_SPEED = 50
		cfg.RIGHT_SPEED = 50
		if  (gpio.digital_read(gpio.IRF_L_GPIO) == 0 and gpio.digital_read(gpio.IRF_R_GPIO) == 0 and gpio.digital_read(gpio.IR_M_GPIO) == 1):
			go.stop()				# 停止：左右检测到障碍物或全都检测不到障碍物
		else:
			if gpio.digital_read(gpio.IRF_L_GPIO) == 1 and gpio.digital_read(gpio.IRF_R_GPIO) == 0:
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.right()			# 左边传感器未检测到障碍物+右边传感器检测到障碍物
			elif gpio.digital_read(gpio.IRF_L_GPIO) == 0 and gpio.digital_read(gpio.IRF_R_GPIO) == 1:
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.left()			# 左边传感器检测到障碍物+右边传感器未检测到障碍物
			elif (gpio.digital_read(gpio.IRF_L_GPIO) == 1 and gpio.digital_read(gpio.IRF_R_GPIO) == 1) or (gpio.digital_read(gpio.IRF_L_GPIO) == 1 and gpio.digital_read(gpio.IRF_R_GPIO) == 1):
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.forward()		# 前进：只有中间传感器检测到障碍物

	def avoiddrop(self):
		"""
		红外防跌落
		"""
		cfg.LEFT_SPEED = 40
		cfg.RIGHT_SPEED = 40
		if (gpio.digital_read(gpio.IR_L_GPIO) == 0) and (gpio.digital_read(gpio.IR_R_GPIO) == 0):  # 俩个红外传感器都探测到地面的时候
			cfg.AVOIDDROP_CHANGER = 1		# 标志位置1，串口解析中方向判断此标志
		else:
			if cfg.AVOIDDROP_CHANGER == 1: 	# 只有当上一次得到状态是正常状态时才会运行停止，避免重复执行停止无法再进行遥控
				go.stop()
				cfg.AVOIDDROP_CHANGER = 0
