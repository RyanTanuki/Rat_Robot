"""
XiaoRGEEK Motor Control Module
-----------------------------
High-level motor control interface for the XiaoRGEEK robot platform.
Provides movement functions used by the test suite and main robot control.

Related Test Files:
- test_gpio.py: Tests the basic motor functions defined here
- test_movement.py: Uses these movement functions for full robot control
- test_command.py: Movement commands map to these functions

Features:
- Individual motor control (M1/M2 and M3/M4)
- Speed control for left and right sides
- Movement functions (forward, back, left, right)
- LED status indication during movement

Dependencies:
- xr_gpio: Low-level GPIO control
- xr_config: Robot configuration settings
"""

from builtins import float, object

import os
import xr_gpio as gpio
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class RobotDirection(object):
	def __init__(self):
		pass

	def set_speed(self, num, speed):
		"""
		设置电机速度，num表示左侧还是右侧，等于1表示左侧，等于右侧，speed表示设定的速度值（0-100）
		"""
		#print(speed)
		if num == 1:  # 调节左侧
			gpio.ena_pwm(speed)
		elif num == 2:  # 调节右侧
			gpio.enb_pwm(speed)

	def motor_init(self):
		"""
		获取机器人存储的速度
		"""
		print("获取机器人存储的速度")
		speed = cfgparser.get_data('motor', 'speed')
		cfg.LEFT_SPEED = speed[0]
		cfg.RIGHT_SPEED = speed[1]
		print(speed[0])
		print(speed[1])

	def save_speed(self):
		speed = [0, 0]
		speed[0] = cfg.LEFT_SPEED
		speed[1] = cfg.RIGHT_SPEED
		cfgparser.save_data('motor', 'speed', speed)

	def m1m2_forward(self):
		# 设置电机组M1、M2正转
		gpio.digital_write(gpio.IN1_GPIO, True)
		gpio.digital_write(gpio.IN2_GPIO, False)

	def m1m2_reverse(self):
		# 设置电机组M1、M2反转
		gpio.digital_write(gpio.IN1_GPIO, False)
		gpio.digital_write(gpio.IN2_GPIO, True)

	def m1m2_stop(self):
		# 设置电机组M1、M2停止
		gpio.digital_write(gpio.IN1_GPIO, False)
		gpio.digital_write(gpio.IN2_GPIO, False)

	def m3m4_forward(self):
		# 设置电机组M3、M4正转
		gpio.digital_write(gpio.IN3_GPIO, True)
		gpio.digital_write(gpio.IN4_GPIO, False)

	def m3m4_reverse(self):
		# 设置电机组M3、M4反转
		gpio.digital_write(gpio.IN3_GPIO, False)
		gpio.digital_write(gpio.IN4_GPIO, True)

	def m3m4_stop(self):
		# 设置电机组M3、M4停止
		gpio.digital_write(gpio.IN3_GPIO, False)
		gpio.digital_write(gpio.IN4_GPIO, False)

	def forward(self):
		"""
		设置机器人运动方向为前进
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_forward()
		gpio.digital_write(gpio.LED0_GPIO, False)#点亮LED

	def back(self):
		"""
		#设置机器人运动方向为后退
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_reverse()
		gpio.digital_write(gpio.LED1_GPIO, False)

	def left(self):
		"""
		#设置机器人运动方向为左转
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_forward()
		gpio.digital_write(gpio.LED1_GPIO, True)
		gpio.digital_write(gpio.LED2_GPIO, False)

	def right(self):
		"""
		#设置机器人运动方向为右转
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_reverse()
		gpio.digital_write(gpio.LED1_GPIO, False)
		gpio.digital_write(gpio.LED2_GPIO, True)

	def stop(self):
		"""
		#设置机器人运动方向为停止
		"""
		self.set_speed(1, 0)
		self.set_speed(2, 0)
		self.m1m2_stop()
		self.m3m4_stop()
		gpio.digital_write(gpio.LED0_GPIO, True)
		gpio.digital_write(gpio.LED1_GPIO, True)
		gpio.digital_write(gpio.LED2_GPIO, True)


