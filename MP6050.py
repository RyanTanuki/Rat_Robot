import smbus
import math
import time


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    # math.sqrt(x) 方法返回数字x的平方根。
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    # math.atan2(y, x) 返回给定的 X 及 Y 坐标值的反正切值。
    radians = math.atan2(x, dist(y, z))
    # math.degrees(x) 将弧度x转换为角度。
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


# 创建一个smbus实例
bus = smbus.SMBus(1)
# 这是通过i2cdetect -y 1命令读取的地址值
address = 0x68

# 调用write_byte_data函数传入0x6b唤醒6050
bus.write_byte_data(address, 0x6b, 0)

while True:
    time.sleep(0.1)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print("gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131))  # 倍率：±250°/s
    print("gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131))
    print("gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131))

    # 加速度
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0  # 倍率：±2g
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
    print("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
    print("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)

    # 转动度数
    print("x rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))

    time.sleep(0.5)