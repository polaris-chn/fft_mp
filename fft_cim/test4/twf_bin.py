import math

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

# 示例用法
if __name__ == "__main__":
    # 8点FFT，8位二进制数，7位小数部分
    print("8点FFT，8位二进制表示（1位符号位+7位小数位）:")
    print_fft_stages_twiddle_factors_binary(8, 8, 7)
    
    # 16点FFT，16位二进制数，15位小数部分
    print("16点FFT，16位二进制表示（1位符号位+15位小数位）:")
    print_fft_stages_twiddle_factors_binary(16, 16, 15)
    
    print("\n" + "="*70 + "\n")
    
    # 32点FFT，8位二进制数，7位小数部分
    print("32点FFT，8位二进制表示（1位符号位+7位小数位）:")
    print_fft_stages_twiddle_factors_binary(32, 8, 7)
    
    print("\n" + "="*70 + "\n")
    
    # 128点FFT，12位二进制数，10位小数部分
    print("128点FFT，12位二进制表示（1位符号位+10位小数位）:")
    print_fft_stages_twiddle_factors_binary(128, 12, 10)