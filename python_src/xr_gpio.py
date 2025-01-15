# coding:utf-8
"""
小R科技树莓派5 WiFi无线视频小车机器人驱动源码V2---GPIO管脚定义
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

from gpiozero import LED as GPIO
from gpiozero import PWMLED as PWM
from gpiozero import DigitalInputDevice as INPUT_GPIO
import time

# LED灯引脚
LED0 = 10
LED1 = 9
LED2 = 25

# 设置电机引脚
ENA = 13  	# //L298使能A
ENB = 20  	# //L298使能B
IN1 = 19  	# //电机接口1
IN2 = 16  	# //电机接口2
IN3 = 21  	# //电机接口3
IN4 = 26  	# //电机接口4

# 设置超声波引脚
ECHO = 5  	# 超声波接收脚位
TRIG = 17  	# 超声波发射脚位

# 设置红外引脚
IR_R = 18  	# 小车右侧巡线红外
IR_L = 27  	# 小车左侧巡线红外
IR_M = 22  	# 小车中间避障红外
IRF_R = 23  # 小车跟随右侧红外
IRF_L = 24  # 小车跟随左侧红外

# 引脚初始化使能，并全部拉低电平
IN1_GPIO = GPIO(IN1)
IN1_GPIO.off()

IN2_GPIO = GPIO(IN2)
IN2_GPIO.off()

IN3_GPIO = GPIO(IN3)
IN3_GPIO.off()

IN4_GPIO = GPIO(IN4)
IN4_GPIO.off()

ENA_pwm = PWM(ENA, active_high=True, initial_value=0, frequency=100, pin_factory=None)
ENA_pwm.value = 0 #默认PWM最低，范围是0-1；

ENB_pwm = PWM(ENB, active_high=True, initial_value=0, frequency=100, pin_factory=None)
ENB_pwm.value = 0 #默认PWM最低，范围是0-1；

# 红外引脚初始化使能
IR_R_GPIO = INPUT_GPIO(IR_R)

IR_L_GPIO = INPUT_GPIO(IR_L)

IR_M_GPIO = INPUT_GPIO(IR_M)

IRF_R_GPIO = INPUT_GPIO(IRF_R)

IRF_L_GPIO = INPUT_GPIO(IRF_L)

# 超声波脚初始化使能
TRIG_GPIO = GPIO(TRIG)
TRIG_GPIO.off()

ECHO_GPIO = INPUT_GPIO(ECHO)

# LED脚初始化使能
LED0_GPIO = GPIO(LED0)
LED0_GPIO.off()
LED1_GPIO = GPIO(LED1)
LED1_GPIO.off()
LED2_GPIO = GPIO(LED2)
LED2_GPIO.off()

def LED_flash():
	for i in range(10):
		LED0_GPIO.on()
		LED1_GPIO.on()
		LED2_GPIO.on()
		time.sleep(0.3)
		LED0_GPIO.off()
		LED1_GPIO.off()
		LED2_GPIO.off()
		time.sleep(0.3)

def digital_write(gpio, status):
	"""
	设置gpio端口为电平
	参数：gpio为设置的端口，status为状态值只能为True(高电平)，False(低电平)
	"""
	if status == True:
		gpio.on()
		#print(gpio,"is on!")
	else:
		gpio.off()
		#print(gpio,"is off!")

def digital_read(gpio):
	"""
	读取gpio端口的电平
	"""
	return gpio.value  

def ena_pwm(pwm):
	"""
	设置电机调速端口ena的pwm
	"""
	pwm = pwm / 100
	#print("ena pwm:",pwm)
	ENA_pwm.value = pwm

	

def enb_pwm(pwm):
	"""
	设置电机调速端口enb的pwm
	"""
	pwm = pwm / 100
	#print("enb pwm:",pwm)
	ENB_pwm.value = pwm
