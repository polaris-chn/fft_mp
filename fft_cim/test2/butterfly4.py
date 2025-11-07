import cmath
import numpy as np

def radix4_butterfly(x0, x1, x2, x3, w1, w2, w3):
    """
    基4蝶形运算
    
    参数:
    x0, x1, x2, x3: 四个输入值
    w1, w2, w3: 旋转因子 W^1, W^2, W^3
    
    返回:
    y0, y1, y2, y3: 四个输出值
    """
    # 第一步计算
    a0 = x0 + x2
    a1 = x0 - x2
    a2 = x1 + x3
    a3 = x1 - x3
    
    # 第二步计算
    y0 = a0 + a2
    y1 = a1 - 1j * a3  # 乘以 W^1 (对于基4，W^1 = -j)
    y2 = a0 - a2
    y3 = a1 + 1j * a3  # 乘以 W^3 (对于基4，W^3 = j)
    
    # 应用旋转因子
    y1 = y1 * w1
    y2 = y2 * w2
    y3 = y3 * w3
    
    return y0, y1, y2, y3

def radix4_fft_stage(input_data, N, stage):
    """
    基4 FFT单阶段处理
    
    参数:
    input_data: 输入数据
    N: 数据长度
    stage: 阶段数
    
    返回:
    该阶段处理后的数据
    """
    output_data = [0] * N
    group_count = 4 ** stage
    group_size = N // group_count
    
    for group in range(group_count):
        for i in range(group_size // 4):
            idx0 = group * group_size + i
            idx1 = idx0 + group_size // 4
            idx2 = idx1 + group_size // 4
            idx3 = idx2 + group_size // 4
            
            # 计算旋转因子
            w1 = cmath.exp(-2j * cmath.pi * (idx1 % group_size) / group_size)
            w2 = cmath.exp(-2j * cmath.pi * (idx2 % group_size) / group_size)
            w3 = cmath.exp(-2j * cmath.pi * (idx3 % group_size) / group_size)
            
            # 执行基4蝶形运算
            y0, y1, y2, y3 = radix4_butterfly(
                input_data[idx0], input_data[idx1], 
                input_data[idx2], input_data[idx3],
                w1, w2, w3
            )
            
            output_data[idx0] = y0
            output_data[idx1] = y1
            output_data[idx2] = y2
            output_data[idx3] = y3
    
    return output_data

def simple_radix4_fft_4point(input_signal):
    """
    简单的4点基4 FFT实现
    
    参数:
    input_signal: 长度为4的输入信号
    
    返回:
    FFT结果
    """
    if len(input_signal) != 4:
        raise ValueError("输入信号长度必须为4")
    
    # 对于4点FFT，只需要一级基4蝶形运算
    x0, x1, x2, x3 = input_signal
    
    # 计算旋转因子
    w0 = 1  # W^0
    w1 = cmath.exp(-2j * cmath.pi * 1 / 4)  # W^1 = -j
    w2 = cmath.exp(-2j * cmath.pi * 2 / 4)  # W^2 = -1
    w3 = cmath.exp(-2j * cmath.pi * 3 / 4)  # W^3 = j
    
    # 基4蝶形运算
    y0 = x0 + x1 + x2 + x3
    y1 = x0 + w1*x1 + w2*x2 + w3*x3
    y2 = x0 - x1 + x2 - x3
    y3 = x0 - w1*x1 + w2*x2 - w3*x3
    
    return [y0, y1, y2, y3]

# 示例测试
if __name__ == "__main__":
    # 测试基4蝶形运算
    print("=== 基4蝶形运算示例 ===")
    input_signal = [1+0j, 0+0j, 0+0j, 0+0j]
    result = simple_radix4_fft_4point(input_signal)
    print(f"输入: {input_signal}")
    print(f"输出: {[f'{x:.3f}' for x in result]}")
    
    # 与numpy FFT对比
    numpy_result = np.fft.fft(input_signal)
    print(f"Numpy FFT: {[f'{x:.3f}' for x in numpy_result]}")
    
    # 更复杂的信号测试
    print("\n=== 复杂信号测试 ===")
    complex_signal = [1+1j, 2+0j, 0+1j, 1-1j]
    our_result = simple_radix4_fft_4point(complex_signal)
    numpy_result = np.fft.fft(complex_signal)
    print(f"输入: {complex_signal}")
    print(f"我们的结果: {[f'{x:.3f}' for x in our_result]}")
    print(f"Numpy结果: {[f'{x:.3f}' for x in numpy_result]}")