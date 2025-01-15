from gpiozero import DigitalInputDevice as INPUT_GPIO
from gpiozero import LED as GPIO

import time  
  
TRIG = 17
ECHO = 5

TRIG_GPIO = GPIO(TRIG)
TRIG_GPIO.off()

ECHO_GPIO = INPUT_GPIO(ECHO)

def get_distance():
		"""
		获取超声波距离函数,有返回值distance，单位cm
		"""
		time_count = 0
		time.sleep(0.01)
		TRIG_GPIO.on()  # 拉高超声波Trig引脚
		time.sleep(0.000015)  # 发送10um以上高电平方波
		TRIG_GPIO.off() # 拉低
		while not ECHO_GPIO.value:  # 等待Echo引脚由低电平变成高电平
			pass
		t1 = time.time()  # 记录Echo引脚高电平开始时间点
		while ECHO_GPIO.value:  # 等待Echo引脚由低电平变成低电平
			if time_count < 2000:  # 超时检测，防止死循环
				time_count = time_count + 1
				time.sleep(0.000001)
				pass
			else:
				print("NO ECHO receive! Please check connection")
				break
		t2 = time.time()  # 记录Echo引脚高电平结束时间点
		distance = (t2 - t1) * 340 / 2 * 100  # Echo引脚高电平持续时间就是超声波由发射到返回的时间，即用时间x声波速度/2等于单程即超声波距物体距离值
		# t2-t1时间单位s,声波速度340m/s,x100将距离值单位m转换成cm
		print("distance is %d" % distance)  # 打印距离值
		if distance < 500:  # 正常检测距离值
			# print("distance is %d"%distance)
			DISTANCE = round(distance, 2)
			return DISTANCE
		else:
			# print("distance is 0")  # 如果距离值大于5m,超出检测范围
			DISTANCE = 0
			return 0

while True:
    get_distance()