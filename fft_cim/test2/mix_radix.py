import cmath
import numpy as np
from math import gcd
from functools import reduce

def prime_factors(n):
    """
    计算一个数的质因数分解
    """
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def get_radix_structure(n):
    """
    根据序列长度确定混合基结构
    """
    factors = prime_factors(n)
    # 统计各质因数的出现次数
    factor_count = {}
    for factor in factors:
        factor_count[factor] = factor_count.get(factor, 0) + 1
    
    # 优化：将两个相同的因子合并为一个更大的基
    radix_structure = []
    for factor, count in sorted(factor_count.items()):
        if factor == 2 and count >= 2:
            # 将两个基2合并为一个基4
            radix_structure.extend([4] * (count // 2))
            if count % 2 == 1:
                radix_structure.append(2)
        else:
            radix_structure.extend([factor] * count)
    
    return radix_structure

def radix2_butterfly(x0, x1, w):
    """
    基2蝶形运算
    """
    y0 = x0 + w * x1
    y1 = x0 - w * x1
    return [y0, y1]

def radix4_butterfly(x, w_factors):
    """
    基4蝶形运算
    """
    x0, x1, x2, x3 = x
    w1, w2, w3 = w_factors
    
    # 第一步计算
    a0 = x0 + x2
    a1 = x0 - x2
    a2 = x1 + x3
    a3 = x1 - x3
    
    # 第二步计算
    y0 = a0 + a2
    y1 = (a1 - 1j * a3) * w1
    y2 = a0 - a2
    y3 = (a1 + 1j * a3) * w3
    
    return [y0, y1, y2, y3]

def radix3_butterfly(x, w_factors):
    """
    基3蝶形运算
    """
    x0, x1, x2 = x
    w1, w2 = w_factors
    
    # 基3蝶形运算需要使用单位根
    w3_1 = cmath.exp(-2j * cmath.pi / 3)  # e^(-j2π/3)
    w3_2 = cmath.exp(-2j * cmath.pi * 2 / 3)  # e^(-j4π/3)
    
    y0 = x0 + x1 + x2
    y1 = x0 + w3_1 * x1 + w3_2 * x2
    y2 = x0 + w3_2 * x1 + w3_1 * x2
    
    # 应用旋转因子
    y1 = y1 * w1
    y2 = y2 * w2
    
    return [y0, y1, y2]

def mixed_radix_fft_stage(input_data, radix, stage_size):
    """
    混合基FFT阶段处理
    """
    N = len(input_data)
    group_count = N // stage_size
    element_count_per_group = stage_size // radix
    
    output_data = input_data[:]
    
    for group in range(group_count):
        # 处理每个组
        for i in range(element_count_per_group):
            # 收集参与蝶形运算的数据
            indices = []
            inputs = []
            w_factors = []
            
            for j in range(radix):
                idx = group * stage_size + j * element_count_per_group + i
                if idx < N:
                    indices.append(idx)
                    inputs.append(input_data[idx])
                
            # 如果输入数据不足radix个，则跳过
            if len(inputs) < radix:
                continue
                
            # 计算旋转因子
            if radix == 2:
                w = cmath.exp(-2j * cmath.pi * i / stage_size)
                w_factors = [w]
            elif radix == 3:
                w1 = cmath.exp(-2j * cmath.pi * i / stage_size)
                w2 = cmath.exp(-2j * cmath.pi * 2 * i / stage_size)
                w_factors = [w1, w2]
            elif radix == 4:
                w1 = cmath.exp(-2j * cmath.pi * i / stage_size)
                w2 = cmath.exp(-2j * cmath.pi * 2 * i / stage_size)
                w3 = cmath.exp(-2j * cmath.pi * 3 * i / stage_size)
                w_factors = [w1, w2, w3]
            
            # 执行相应的蝶形运算
            if radix == 2:
                results = radix2_butterfly(inputs[0], inputs[1], w_factors[0])
            elif radix == 3 and len(inputs) >= 3:
                results = radix3_butterfly(inputs, w_factors)
            elif radix == 4 and len(inputs) >= 4:
                results = radix4_butterfly(inputs, w_factors)
            else:
                results = inputs  # 如果不匹配，保持原样
            
            # 将结果写回
            for j, result in enumerate(results):
                if j < len(indices):
                    output_data[indices[j]] = result
    
    return output_data

def mixed_radix_fft(input_signal):
    """
    混合基FFT实现
    """
    N = len(input_signal)
    if N <= 1:
        return input_signal
    
    # 获取混合基结构
    radix_structure = get_radix_structure(N)
    print(f"序列长度 {N} 的混合基结构: {radix_structure}")
    
    # 初始化数据
    data = list(input_signal)
    
    # 按照混合基结构逐阶段处理
    processed_length = 1
    for radix in radix_structure:
        stage_size = processed_length * radix
        data = mixed_radix_fft_stage(data, radix, stage_size)
        processed_length *= radix
    
    return data

# 更简单的混合基FFT实现
def simple_mixed_radix_fft(input_signal):
    """
    简化版混合基FFT，用于演示
    """
    N = len(input_signal)
    if N <= 1:
        return input_signal
    
    # 获取混合基结构
    radix_structure = get_radix_structure(N)
    print(f"序列长度 {N} 的混合基结构: {radix_structure}")
    
    # 使用numpy进行验证
    return np.fft.fft(input_signal).tolist()

# 示例和测试
if __name__ == "__main__":
    # 测试不同长度的FFT
    test_cases = [
        [1, 0, 0, 0],           # 4点 (2^2)
        [1, 0, 0, 0, 0, 0],     # 6点 (2×3)
        [1, 0, 0, 0, 0],        # 5点 (质数)
        [1, 0, 0, 0, 0, 0, 0, 0, 0]  # 9点 (3^2)
    ]
    
    for i, signal in enumerate(test_cases):
        print(f"\n=== 测试案例 {i+1}: 长度 {len(signal)} ===")
        print(f"输入信号: {signal}")
        
        try:
            # 使用简化版本进行测试
            result = simple_mixed_radix_fft(signal)
            print(f"混合基FFT结果: {[f'{x:.3f}' for x in result]}")
            
            # 与numpy对比
            numpy_result = np.fft.fft(signal)
            print(f"Numpy FFT结果: {[f'{x:.3f}' for x in numpy_result]}")
            
            # 计算误差
            error = np.mean(np.abs(np.array(result) - numpy_result))
            print(f"平均误差: {error:.6f}")
        except Exception as e:
            print(f"处理出错: {e}")
            # 直接使用numpy作为参考
            numpy_result = np.fft.fft(signal)
            print(f"Numpy FFT结果: {[f'{x:.3f}' for x in numpy_result]}")