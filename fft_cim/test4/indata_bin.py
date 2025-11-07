import math
import random

def float_to_binary_fixed_point(value, total_bits, fractional_bits):
    """
    将浮点数转换为定点二进制表示
    """
    # 计算整数部分位数
    integer_bits = total_bits - fractional_bits - 1  # -1 for sign bit
    
    # 处理符号
    if value < 0:
        sign = 1
        value = abs(value)
    else:
        sign = 0
    
    # 将值缩放到整数范围
    scaled_value = value * (2 ** fractional_bits)
    integer_value = int(round(scaled_value))
    
    # 处理溢出
    max_value = (2 ** (total_bits - 1)) - 1
    if integer_value > max_value:
        integer_value = max_value
    
    # 转换为二进制（不包括符号位）
    binary_str = format(integer_value, f'0{total_bits-1}b')
    
    # 添加符号位
    binary_str = str(sign) + binary_str
    
    return binary_str

def binary_to_float_fixed_point(binary_str, fractional_bits):
    """
    将二进制定点数转换为浮点数
    """
    total_bits = len(binary_str)
    
    # 解析符号位
    sign = int(binary_str[0])
    
    # 解析数值部分
    value = int(binary_str[1:], 2)
    
    # 转换为浮点数
    float_value = value / (2 ** fractional_bits)
    
    # 应用符号
    if sign == 1:
        float_value = -float_value
        
    return float_value

def quantize_input_data(data, bit_width, fractional_bits):
    """
    对输入数据进行量化
    
    参数:
    data: 输入数据列表，每个元素为复数或实数
    bit_width: 二进制数总位数
    fractional_bits: 小数部分位数
    
    返回:
    量化后的数据列表和二进制表示列表
    """
    quantized_data = []
    binary_representations = []
    
    for i, value in enumerate(data):
        if isinstance(value, complex):
            # 处理复数
            real_part = value.real
            imag_part = value.imag
            
            # 量化实部和虚部
            real_binary = float_to_binary_fixed_point(real_part, bit_width, fractional_bits)
            imag_binary = float_to_binary_fixed_point(imag_part, bit_width, fractional_bits)
            
            # 转换回浮点数
            quantized_real = binary_to_float_fixed_point(real_binary, fractional_bits)
            quantized_imag = binary_to_float_fixed_point(imag_binary, fractional_bits)
            
            quantized_data.append(complex(quantized_real, quantized_imag))
            binary_representations.append(f"Index {i}: ({real_binary}, {imag_binary})")
        else:
            # 处理实数
            real_binary = float_to_binary_fixed_point(value, bit_width, fractional_bits)
            quantized_real = binary_to_float_fixed_point(real_binary, fractional_bits)
            
            quantized_data.append(quantized_real)
            binary_representations.append(f"Index {i}: {real_binary}")
    
    return quantized_data, binary_representations

def print_fft_stages_twiddle_factors_binary(n, bit_width, fractional_bits):
    """
    打印N点基2 FFT每一级的旋转因子（二进制形式）
    
    参数:
    n: FFT点数 (必须是2的幂)
    bit_width: 二进制数总位数
    fractional_bits: 小数部分位数
    """
    # 检查n是否为2的幂
    if not (n > 0 and (n & (n - 1)) == 0):
        print(f"错误: {n} 不是2的幂")
        return
    
    stages = int(math.log2(n))
    print(f"{n}点FFT基2计算共有{stages}级")
    print(f"使用{bit_width}位二进制数表示，其中小数部分占{fractional_bits}位")
    print("=" * 70)
    
    for stage in range(1, stages + 1):
        # 计算当前级的蝶形跨度
        span = n // (2 ** stage)
        # 计算当前级需要的不同旋转因子数量
        num_unique_factors = 2 ** (stage - 1)
        
        print(f"第{stage}级 (Stage {stage}):")
        print(f"  蝶形跨度: {span}")
        print(f"  不同旋转因子数量: {num_unique_factors}")
        print(f"  旋转因子 (实部, 虚部):")
        
        # 打印该级所有旋转因子
        factors_in_stage = []
        for k in range(num_unique_factors):
            # 计算旋转因子 W_N^k = e^(-j*2*pi*k/N)
            angle = -2 * math.pi * k / n
            real = math.cos(angle)
            imag = math.sin(angle)
            
            # 转换为二进制
            real_binary = float_to_binary_fixed_point(real, bit_width, fractional_bits)
            imag_binary = float_to_binary_fixed_point(imag, bit_width, fractional_bits)
            
            factors_in_stage.append(f"W({n},{k}):({real_binary},{imag_binary})")
        
        # 按行打印，每行最多2个因子
        for i in range(0, len(factors_in_stage), 2):
            print("    " + ", ".join(factors_in_stage[i:i+2]))
        print()

def generate_test_input_data(n, complex_data=True):
    """
    生成测试输入数据
    
    参数:
    n: 数据点数
    complex_data: 是否生成复数数据
    
    返回:
    输入数据列表
    """
    data = []
    for i in range(n):
        if complex_data:
            # 生成复数数据
            real_part = random.uniform(-1.0, 1.0)
            imag_part = random.uniform(-1.0, 1.0)
            data.append(complex(real_part, imag_part))
        else:
            # 生成实数数据
            data.append(random.uniform(-1.0, 1.0))
    return data

# 示例用法
if __name__ == "__main__":
    # FFT参数
    fft_points = 8
    binary_bits = 8
    fractional_bits = 7
    
    print(f"{fft_points}点FFT输入数据量化示例")
    print(f"使用{binary_bits}位二进制数表示，其中小数部分占{fractional_bits}位")
    print("=" * 70)
    
    # 生成测试数据
    input_data = generate_test_input_data(fft_points, complex_data=True)
    
    print("原始输入数据:")
    for i, value in enumerate(input_data):
        print(f"  Index {i}: {value}")
    
    print("\n量化后的数据:")
    quantized_data, binary_representations = quantize_input_data(
        input_data, binary_bits, fractional_bits)
    
    for i, (quantized_value, binary_repr) in enumerate(zip(quantized_data, binary_representations)):
        original = input_data[i]
        if isinstance(original, complex):
            print(f"  Index {i}:")
            print(f"    原始: {original}")
            print(f"    量化: {quantized_value}")
            print(f"    二进制: {binary_repr}")
        else:
            print(f"  Index {i}: 原始={original:.6f}, 量化={quantized_value:.6f}, 二进制={binary_repr}")
    
    print("\n" + "="*70 + "\n")
    
    # 显示旋转因子
    print_fft_stages_twiddle_factors_binary(fft_points, binary_bits, fractional_bits)