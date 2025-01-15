import smbus
import time
from datetime import datetime

# MPU6050设备地址
MPU6050_ADDR = 0x68

# 寄存器地址
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

bus = smbus.SMBus(1)

def read_i2c_word(register):
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register + 1)
    value = (high << 8) + low
    if value > 32767:
        value -= 65536
    return value

def setup():
    # 唤醒MPU6050
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

try:
    setup()
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        accel_x = read_i2c_word(ACCEL_XOUT_H)
        accel_y = read_i2c_word(ACCEL_YOUT_H)
        accel_z = read_i2c_word(ACCEL_ZOUT_H)
        gyro_x = read_i2c_word(GYRO_XOUT_H)
        gyro_y = read_i2c_word(GYRO_YOUT_H)
        gyro_z = read_i2c_word(GYRO_ZOUT_H)

        print(f"{now} Accel: X={accel_x}, Y={accel_y}, Z={accel_z} Gyro: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
        time.sleep(1)
except KeyboardInterrupt:
    print("程序停止")
