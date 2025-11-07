import cmath
import numpy as np

def butterfly_operation(a, b, w):
    """
    执行基本的蝶形运算
    
    参数:
    a: 第一个输入值（复数）
    b: 第二个输入值（复数）
    w: 加权因子（复数旋转因子）
    
    返回:
    (a_prime, b_prime): 蝶形运算后的输出值对
    """
    a_prime = a + w * b
    b_prime = a - w * b
    return (a_prime, b_prime)

def radix2_butterfly(input_array):
    """
    对长度为2的数组执行基-2蝶形运算
    
    参数:
    input_array: 包含两个复数的数组 [x0, x1]
    
    返回:
    输出数组 [X0, X1]
    """
    if len(input_array) != 2:
        raise ValueError("输入数组长度必须为2")
    
    x0, x1 = input_array[0], input_array[1]
    # 对于2点FFT，旋转因子W(2,0) = 1
    w = 1
    
    X0 = x0 + w * x1
    X1 = x0 - w * x1
    
    return [X0, X1]

def fft_butterfly_stage(input_data, stage_index, N):
    """
    执行FFT的一个蝶形运算阶段
    
    参数:
    input_data: 输入数据数组
    stage_index: 阶段索引
    N: 数据总长度
    
    返回:
    该阶段处理后的数据
    """
    output_data = [0] * N
    num_groups = 2 ** stage_index
    group_size = N // num_groups
    
    for group in range(num_groups):
        for i in range(group_size // 2):
            # 计算旋转因子
            k = group * group_size + i
            j = k + group_size // 2
            
            # 计算旋转因子 W_N^(k*(group_size/2))
            w_exp = (group_size // 2) * (k % num_groups)
            w = cmath.exp(-2j * cmath.pi * w_exp / N)
            
            # 蝶形运算
            output_data[k] = input_data[k] + w * input_data[j]
            output_data[j] = input_data[k] - w * input_data[j]
    
    return output_data

def simple_fft_4point(input_signal):
    """
    使用蝶形运算实现4点FFT
    
    参数:
    input_signal: 长度为4的输入信号数组
    
    返回:
    FFT结果
    """
    if len(input_signal) != 4:
        raise ValueError("输入信号长度必须为4")
    
    # 第一阶段：按位反转顺序
    x = [input_signal[i] for i in [0, 2, 1, 3]]
    
    # 第二阶段：第一级蝶形运算（2个2点FFT）
    stage1 = [0+0j] * 4
    # 第一组 (0,1)
    stage1[0] = x[0] + x[1]
    stage1[1] = x[0] - x[1]
    # 第二组 (2,3)
    stage1[2] = x[2] + x[3]
    stage1[3] = x[2] - x[3]
    
    # 第三阶段：第二级蝶形运算
    stage2 = [0+0j] * 4
    # 第一组 (0,2)
    w0 = cmath.exp(-2j * cmath.pi * 0 / 4)  # W_4^0 = 1
    stage2[0] = stage1[0] + w0 * stage1[2]
    stage2[2] = stage1[0] - w0 * stage1[2]
    # 第二组 (1,3)
    w1 = cmath.exp(-2j * cmath.pi * 1 / 4)  # W_4^1 = -j
    stage2[1] = stage1[1] + w1 * stage1[3]
    stage2[3] = stage1[1] - w1 * stage1[3]
    
    return stage2

# 示例和测试
if __name__ == "__main__":
    # 在现有代码的最后添加以下验证代码

    print("\n=== 额外验证 ===")
    
    # 验证 butterfly_operation 函数
    print("\n1. 验证 butterfly_operation 函数:")
    a = 2 + 3j
    b = 1 - 1j
    w = cmath.exp(-2j * cmath.pi * 1 / 4)  # W_4^1 = -j
    result = butterfly_operation(a, b, w)
    print(f"   输入: a={a}, b={b}, w={w:.3f}")
    print(f"   输出: a'={result[0]:.3f}, b'={result[1]:.3f}")
    
    # 验证 radix2_butterfly 函数
    print("\n2. 验证 radix2_butterfly 函数:")
    test_input = [1+2j, 3+1j]
    result = radix2_butterfly(test_input)
    numpy_result = np.fft.fft(test_input)
    print(f"   输入: {test_input}")
    print(f"   我们的结果: [{result[0]:.3f}, {result[1]:.3f}]")
    print(f"   Numpy的结果: [{numpy_result[0]:.3f}, {numpy_result[1]:.3f}]")
    error = np.mean(np.abs(np.array(result) - numpy_result))
    print(f"   平均误差: {error:.6f}")
    
    # 验证 simple_fft_4point 函数与numpy的一致性
    print("\n3. 验证 simple_fft_4point 函数:")
    test_signal = [1+0j, 1+1j, 0+1j, 1+0j]
    our_result = simple_fft_4point(test_signal)
    numpy_result = np.fft.fft(test_signal)
    print(f"   输入信号: {[f'{x:.3f}' for x in test_signal]}")
    print(f"   我们的结果: {[f'{x:.3f}' for x in our_result]}")
    print(f"   Numpy结果: {[f'{x:.3f}' for x in numpy_result]}")
    error = np.mean(np.abs(np.array(our_result) - numpy_result))
    print(f"   平均误差: {error:.6f}")
    
    # 验证不同输入信号
    print("\n4. 测试不同输入信号:")
    test_cases = [
        [1, 1, 1, 1],      # 常数信号
        [1, 0, 0, 0],      # 单位脉冲
        [0, 1, 0, 0],      # 时移脉冲
        [1, -1, 1, -1]     # 交替信号
    ]
    
    for i, signal in enumerate(test_cases):
        complex_signal = [complex(x) for x in signal]
        our_result = simple_fft_4point(complex_signal)
        numpy_result = np.fft.fft(complex_signal)
        error = np.mean(np.abs(np.array(our_result) - numpy_result))
        print(f"   测试 {i+1}: 信号 {signal} -> 误差: {error:.6f}")
    
    print("\n=== 验证完成 ===")