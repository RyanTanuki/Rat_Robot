import os  
  
def get_raspberry_pi_model():  
    # 读取/proc/cpuinfo文件  
    with open('/proc/cpuinfo', 'r') as file:  
        cpuinfo = file.read()  
  
    # 查找包含模型名称的行  
    model_line = next((line for line in cpuinfo.splitlines() if 'Model' in line), None)  
  
    if model_line:  
        # 提取模型名称并去除前后的空白字符  
        model_name = model_line.split(':', 1)[1].strip()  
        return model_name  
    else:  
        return "无法获取树莓派型号"  
  
# 调用函数并打印结果  
model = get_raspberry_pi_model()  
print("树莓派型号:", model)