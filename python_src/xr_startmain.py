# coding:utf-8
"""
XiaoRGEEK Robot Main Control Module
----------------------------------
Main control module for the XiaoRGEEK robot platform.
Initializes and manages all robot subsystems.

Related Test Files:
- test_server.py: Tests the command server implemented here
- test_command.py: Tests command handling
- test_camera.py: Tests camera service management
- test_movement.py: Tests movement control interface
- test_gpio.py: Tests underlying GPIO functionality

Features:
- Robot service initialization
- Command server (TCP/IP)
- Movement control
- Camera streaming
- Servo control
- System monitoring

Dependencies:
- All XR modules (gpio, motor, camera, etc)
- Socket programming for command interface
- Threading for concurrent operations
"""
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
@Explain :主线程
@Time    :2023/05/07
@File    :xr_startmain.py
"""
from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call
import xr_gpio as gpio

import xr_config as cfg
from xr_motor import RobotDirection
go = RobotDirection()
from socket import socket as socketlib, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from xr_socket import Socket
robot_socket = Socket()
from xr_infrared import Infrared
infrared = Infrared()
from xr_ultrasonic import Ultrasonic
ultrasonic = Ultrasonic()
from xr_camera import Camera
camera = Camera()
from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()
import json
import cv2
from flask import Flask, Response
import sys
import socket  # Add this line

class CommandHandler:
	"""
	Command processing class for robot control.
	
	Handles commands tested by:
	- test_command.py: Basic command processing
	- test_movement.py: Movement commands
	- test_gpio.py: Motor control commands
	"""
	def __init__(self):
		self.go = go
		self.servo = Servo
		
	def handle_command(self, command_str):
		try:
			print(f"Received command: {command_str}")  # Debug print
			command = json.loads(command_str)
			cmd_type = command.get('type')
			
			if cmd_type == 'motor':
				print(f"Processing motor command: {command}")  # Debug print
				return self.handle_motor(command)
			elif cmd_type == 'servo':
				print(f"Processing servo command: {command}")  # Debug print
				return self.handle_servo(command)
			else:
				return json.dumps({"status": "error", "message": "Unknown command type"})
				
		except Exception as e:
			print(f"Command error: {e}")  # Debug print
			return json.dumps({"status": "error", "message": str(e)})
		
	def handle_motor(self, command):
		try:
			left = command.get('left', 0)
			right = command.get('right', 0)
			direction = command.get('direction', 'stop')
			
			# Set speeds
			self.go.set_speed(1, left)
			self.go.set_speed(2, right)
			
			# Set direction
			if direction == 'forward':
				self.go.forward()
			elif direction == 'backward':
				self.go.back()
			elif direction == 'left':
				self.go.left()
			elif direction == 'right':
				self.go.right()
			else:
				self.go.stop()
				
			return json.dumps({"status": "success"})
		except Exception as e:
			return json.dumps({"status": "error", "message": str(e)})
		
	def handle_servo(self, command):
		try:
			servo_id = command.get('id')
			angle = command.get('angle')
			
			if 1 <= servo_id <= 8:
				self.servo.XiaoRGEEK_SetServoAngle(servo_id, angle)
				return json.dumps({"status": "success"})
			else:
				return json.dumps({"status": "error", "message": "Invalid servo ID"})
		except Exception as e:
			return json.dumps({"status": "error", "message": str(e)})

def command_server(handler):
	"""
	TCP server for robot control commands.
	
	Tested by:
	- test_server.py: Server initialization
	- test_command.py: Command processing
	"""
	"""TCP server to handle commands from web interface"""
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	try:
		server_socket.bind(('0.0.0.0', 2001))
		print("Command server listening on port 2001")
		server_socket.listen(1)
		
		while True:
			try:
				client_socket, address = server_socket.accept()
				print(f"Received connection from {address}")
				data = client_socket.recv(1024).decode()
				print(f"Received data: {data}")  # Debug print
				
				if data:
					response = handler.handle_command(data)
					print(f"Sending response: {response}")  # Debug print
					client_socket.send(response.encode())
					
			except Exception as e:
				print(f"Error handling client: {e}")
			finally:
				client_socket.close()
				
	except Exception as e:
		print(f"Server error: {e}")
	finally:
		server_socket.close()

def cruising_mode():
	"""
	模式切换函数
	:return:none
	"""
	# print('pre_CRUISING_FLAG：{}'.format(cfg.PRE_CRUISING_FLAG))
	time.sleep(0.001)
	if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_FLAG:  # 如果循环模式改变
		cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # 在切换其他模式的时候,恢复上次保存的速度值
		cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
		if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_SET['normal']:	 # 如果循环模式改变，且上次的模式不是正常模式
			go.stop()	  # 先停止小车
		cfg.PRE_CRUISING_FLAG = cfg.CRUISING_FLAG	 # 重新赋值上次模式标志位

	if cfg.CRUISING_FLAG == cfg.CRUISING_SET['irfollow']:  # 进入红外跟随模式
		# print("Infrared.irfollow")
		infrared.irfollow()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['trackline']:  # 进入红外巡线模式
		# print("Infrared.trackline")
		infrared.trackline()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoiddrop']:  # 进入红外防掉落模式
		# print("Infrared.avoiddrop")
		infrared.avoiddrop()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoidbyragar']:  # 进入超声波避障模式
		# print("Ultrasonic.avoidbyragar")
		ultrasonic.avoidbyragar()
		time.sleep(0.5)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['send_distance']:  # 进入超声波测距模式
		# print("Ultrasonic.send_distance")
		ultrasonic.send_distance()
		time.sleep(1)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['maze']:  # 进入超声波走迷宫模式
		# print("Ultrasonic.maze")
		ultrasonic.maze()
		time.sleep(0.05)

	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_normal']:  # 进入调试模式
		time.sleep(2)
		print("CRUISING_FLAG == 7")
		cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']
	elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
		pass
	else:
		time.sleep(0.001)



if __name__ == '__main__':
	try:
		print("Starting robot service...")
		
		# Initialize GPIO
		print("Initializing GPIO...")
		if not gpio.init_gpio():
			raise Exception("Failed to initialize GPIO")
			
		# Setup Bluetooth
		print("Setting up Bluetooth...")
		try:
			os.system("sudo hciconfig hci0 name XiaoRGEEK")
			time.sleep(0.1)
			os.system("sudo hciconfig hci0 reset")
			time.sleep(0.3)
			os.system("sudo hciconfig hci0 piscan")
			time.sleep(0.2)
			print("Bluetooth setup complete")
		except Exception as e:
			print(f"Bluetooth setup failed: {e}")
			# Continue even if Bluetooth fails

		# Initialize servos
		print("Initializing servos...")
		try:
			Servo.XiaoRGEEK_ReSetServo()
			time.sleep(0.1)
			print("Servos initialized")
		except Exception as e:
			print(f"Servo initialization failed: {e}")
			raise

		print("Creating threads...")
		threads = []
		
		try:
			# Camera thread
			t1 = threading.Thread(target=camera.run, args=())
			threads.append(t1)
			
			# # Bluetooth thread
			# t2 = threading.Thread(target=robot_socket.bluetooth_server, args=())
			# threads.append(t2)
			
			# # TCP thread
			# t3 = threading.Thread(target=robot_socket.tcp_server, args=())
			# threads.append(t3)
			
			# Command handler
			# cmd_handler = CommandHandler()
			# t4 = threading.Thread(target=command_server, args=(cmd_handler,))
			# threads.append(t4)

			# Start all threads
			for t in threads:
				print(f"Starting thread: {t}")
				t.setDaemon(True)
				t.start()
				time.sleep(0.05)

			print("All threads started")
			
		except Exception as e:
			print(f"Thread creation/startup failed: {e}")
			raise

		# Initialize motors
		print("Initializing motors...")
		try:
			go.motor_init()
			print("Motors initialized")
		except Exception as e:
			print(f"Motor initialization failed: {e}")
			raise
		
		print("Startup complete, flashing LED...")
		gpio.LED_flash()
		
		while True:
			try:
				cruising_mode()
			except Exception as e:
				print(f'cruising_mode error: {e}')
				time.sleep(0.1)
				
	except Exception as e:
		print(f"Fatal error: {e}")
		import traceback
		traceback.print_exc()
		sys.exit(1)

