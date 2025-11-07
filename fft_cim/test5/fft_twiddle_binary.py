import math
import cmath
import numpy as np

def float_to_binary_fixed_point(value, total_bits, fractional_bits):
    """
    将浮点数转换为定点二进制表示

    参数:
    value: 要转换的浮点数
    total_bits: 二进制数总位数
    fractional_bits: 小数部分位数

    返回:
    二进制字符串表示
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

def get_twiddle_factors(n):
    """
    生成N点FFT的所有旋转因子

    参数:
    n: FFT点数

    返回:
    旋转因子列表
    """
    factors = []
    for k in range(n):
        angle = -2 * math.pi * k / n
        real = math.cos(angle)
        imag = math.sin(angle)
        factors.append(complex(real, imag))
    return factors

def generate_twiddle_factors_binary(n, total_bits, fractional_bits):
    """
    生成N点FFT的所有旋转因子，并转换为二进制表示

    参数:
    n: FFT点数 (必须是2的幂)
    total_bits: 二进制数总位数
    fractional_bits: 小数部分位数

    返回:
    包含所有旋转因子二进制表示的列表
    """
    # 检查n是否为2的幂
    if not (n > 0 and (n & (n - 1)) == 0):
        print(f"错误: {n} 不是2的幂")
        return None

    # 生成旋转因子
    twiddle_factors = get_twiddle_factors(n)

    # 转换为二进制表示
    binary_factors = []
    for idx, factor in enumerate(twiddle_factors):
        real_binary = float_to_binary_fixed_point(factor.real, total_bits, fractional_bits)
        imag_binary = float_to_binary_fixed_point(factor.imag, total_bits, fractional_bits)

        binary_factors.append({
            'index': idx,
            'complex': factor,
            'real': factor.real,
            'imag': factor.imag,
            'real_binary': real_binary,
            'imag_binary': imag_binary,
            'magnitude': abs(factor),
            'phase': cmath.phase(factor)
        })

    return binary_factors

def print_twiddle_factors_by_stage(n, twiddle_factors):
    """
    按FFT阶段打印旋转因子的二进制表示

    参数:
    n: FFT点数
    twiddle_factors: 旋转因子二进制表示的列表
    """
    stages = int(math.log2(n))
    print(f"按FFT阶段显示旋转因子 (共{stages}级):")
    print("=" * 70)

    for stage in range(1, stages + 1):
        span = n // (2 ** stage)
        num_unique_factors = 2 ** (stage - 1)

        print(f"第{stage}级 (Stage {stage}):")
        print(f"  蝶形跨度: {span}")
        print(f"  不同旋转因子数量: {num_unique_factors}")
        print(f"  旋转因子 (实部, 虚部):")

        # 打印该级所有旋转因子
        factors_in_stage = []
        for k in range(num_unique_factors):
            factor = twiddle_factors[k]
            factors_in_stage.append(f"W({n},{k}):({factor['real_binary']},{factor['imag_binary']})")

        # 按行打印，每行最多2个因子
        for i in range(0, len(factors_in_stage), 2):
            print("    " + ", ".join(factors_in_stage[i:i+2]))
        print()

def print_all_twiddle_factors(n, twiddle_factors):
    """
    打印所有旋转因子的详细信息

    参数:
    n: FFT点数
    twiddle_factors: 旋转因子二进制表示的列表
    """
    print("所有旋转因子详细信息:")
    print("=" * 70)

    for factor in twiddle_factors:
        print(f"W({n},{factor['index']}):")
        print(f"  十进制: 实部={factor['real']:.6f}, 虚部={factor['imag']:.6f}")
        print(f"  二进制: 实部={factor['real_binary']}, 虚部={factor['imag_binary']}")
        print(f"  幅值: {factor['magnitude']:.6f}, 相位: {factor['phase']:.6f} 弧度")
        print()

def save_twiddle_factors_to_file(n, twiddle_factors, total_bits, fractional_bits, filename=None):
    """
    将旋转因子二进制表示保存到文件

    参数:
    n: FFT点数
    twiddle_factors: 旋转因子二进制表示的列表
    total_bits: 二进制总位数
    fractional_bits: 小数部分位数
    filename: 保存的文件名，如果为None则自动生成
    """
    if filename is None:
        filename = f"twiddle_factors_{n}_{total_bits}bits_{fractional_bits}frac.txt"

    with open(filename, 'w') as f:
        f.write(f"{n}点FFT旋转因子二进制表示\n")
        f.write(f"使用{total_bits}位二进制数表示，其中小数部分占{fractional_bits}位\n")
        f.write("=" * 70 + "\n\n")

        # 写入所有旋转因子
        for factor in twiddle_factors:
            f.write(f"W({n},{factor['index']}):\n")
            f.write(f"  十进制: 实部={factor['real']:.6f}, 虚部={factor['imag']:.6f}\n")
            f.write(f"  二进制: 实部={factor['real_binary']}, 虚部={factor['imag_binary']}\n")
            f.write(f"  幅值: {factor['magnitude']:.6f}, 相位: {factor['phase']:.6f} 弧度\n\n")

    print(f"结果已保存到 {filename}")

def main():
    print("FFT旋转因子二进制转换程序")
    print("=" * 70)

    # 获取用户输入
    try:
        n = int(input("请输入FFT点数(必须是2的幂): "))
        total_bits = int(input("请输入二进制总位数: "))
        fractional_bits = int(input("请输入小数部分位数: "))

        # 验证输入
        if total_bits < fractional_bits + 1:
            print("错误: 二进制总位数必须大于小数部分位数+1(至少需要1位符号位)")
            return

        # 生成旋转因子二进制表示
        twiddle_factors = generate_twiddle_factors_binary(n, total_bits, fractional_bits)

        if twiddle_factors:
            # 显示选项
            print("\n显示选项:")
            print("1. 按FFT阶段显示旋转因子")
            print("2. 显示所有旋转因子详细信息")
            print("3. 选项1和2都显示")
            print("4. 仅保存到文件")

            choice = input("请选择显示方式(1-4): ")

            if choice in ['1', '3']:
                print_twiddle_factors_by_stage(n, twiddle_factors)

            if choice in ['2', '3']:
                print_all_twiddle_factors(n, twiddle_factors)

            if choice in ['3', '4']:
                save_twiddle_factors_to_file(n, twiddle_factors, total_bits, fractional_bits)
            elif choice not in ['1', '2']:
                print("无效的选择")

    except ValueError:
        print("错误: 请输入有效的整数")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
