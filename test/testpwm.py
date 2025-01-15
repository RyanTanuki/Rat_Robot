from gpiozero import PWMLED as PWM
import time  
  
# 创建一个 PWMLED 实例，指定 GPIO 引脚号  
# 例如，如果你的舵机连接到 GPIO 引脚 17，则使用 '17'  
ena = PWM(20, active_high=True, initial_value=0, frequency=100, pin_factory=None)
while True:   
    for i in range(100):
        ena.value = i / 100
        time.sleep(0.1)  # 每次更改后等待 0.1 秒
        print(ena)
        
    for i in range(100,0,-1):
        ena.value = i / 100
        time.sleep(0.1)  # 每次更改后等待 0.1 秒  
    