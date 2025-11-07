import numpy as np
import math

def fft_radix2_butterfly(x):
    """
    使用基2蝶形运算计算8点FFT
    """
    N = len(x)
    if N != 8:
        raise ValueError("This implementation is for 8-point FFT only")
    
    # 位反转排序
    def bit_reverse_order(x):
        # 8点FFT的位反转索引: 0,1,2,3,4,5,6,7 -> 0,4,2,6,1,5,3,7
        bit_rev_indices = [0, 4, 2, 6, 1, 5, 3, 7]
        return [x[i] for i in bit_rev_indices]
    
    # 蝶形运算函数
    def butterfly(a, b, w):
        """
        执行蝶形运算
        """
        t = w * b
        return a + t, a - t
    
    # 初始化
    x_reordered = bit_reverse_order(x)
    
    # 转换为复数数组
    X = [complex(val) for val in x_reordered]
    
    # 第一级蝶形运算 (4组，每组2点)
    for i in range(0, 8, 2):
        X[i], X[i+1] = butterfly(X[i], X[i+1], complex(1, 0))
    
    # 第二级蝶形运算 (2组，每组4点)
    for i in range(0, 8, 4):
        # 第一个蝶形
        X[i], X[i+2] = butterfly(X[i], X[i+2], complex(1, 0))
        # 第二个蝶形
        X[i+1], X[i+3] = butterfly(X[i+1], X[i+3], complex(0, -1))
    
    # 第三级蝶形运算 (1组，8点)
    # 前4个点与后4个点之间的蝶形运算
    W_N = [complex(math.cos(2*math.pi*k/8), -math.sin(2*math.pi*k/8)) for k in range(4)]
    
    for i in range(4):
        X[i], X[i+4] = butterfly(X[i], X[i+4], W_N[i])
    
    return X

def fft_radix2_butterfly_detailed(x):
    """
    使用基2蝶形运算计算8点FFT - 详细版本，展示每一级的计算过程
    """
    N = len(x)
    if N != 8:
        raise ValueError("This implementation is for 8-point FFT only")
    
    # 位反转排序
    def bit_reverse_order(x):
        bit_rev_indices = [0, 4, 2, 6, 1, 5, 3, 7]
        return [x[i] for i in bit_rev_indices]
    
    # 蝶形运算函数
    def butterfly(a, b, w):
        t = w * b
        return a + t, a - t
    
    print("Input sequence:", x)
    
    # 初始化
    x_reordered = bit_reverse_order(x)
    print("Bit-reversed order:", x_reordered)
    
    # 转换为复数数组
    X = [complex(val) for val in x_reordered]
    
    print("\n--- Stage 1 (N/2 groups of 2 points) ---")
    # 第一级蝶形运算 (4组，每组2点)
    for i in range(0, 8, 2):
        X[i], X[i+1] = butterfly(X[i], X[i+1], complex(1, 0))
        print(f"Butterfly {i//2+1}: X[{i}] = {X[i]:.3f}, X[{i+1}] = {X[i+1]:.3f}")
    
    print("\n--- Stage 2 (N/4 groups of 4 points) ---")
    # 第二级蝶形运算 (2组，每组4点)
    for i in range(0, 8, 4):
        # 第一个蝶形
        X[i], X[i+2] = butterfly(X[i], X[i+2], complex(1, 0))
        print(f"Butterfly 1 in group {(i//4)+1}: X[{i}] = {X[i]:.3f}, X[{i+2}] = {X[i+2]:.3f}")
        # 第二个蝶形
        X[i+1], X[i+3] = butterfly(X[i+1], X[i+3], complex(0, -1))
        print(f"Butterfly 2 in group {(i//4)+1}: X[{i+1}] = {X[i+1]:.3f}, X[{i+3}] = {X[i+3]:.3f}")
    
    print("\n--- Stage 3 (1 group of 8 points) ---")
    # 第三级蝶形运算 (1组，8点)
    W_N = [complex(math.cos(2*math.pi*k/8), -math.sin(2*math.pi*k/8)) for k in range(4)]
    print("Twiddle factors:", [f"{w:.3f}" for w in W_N])
    
    for i in range(4):
        X[i], X[i+4] = butterfly(X[i], X[i+4], W_N[i])
        print(f"Butterfly {i+1}: X[{i}] = {X[i]:.3f}, X[{i+4}] = {X[i+4]:.3f}")
    
    return X

# 示例使用
if __name__ == "__main__":
    # 测试序列
    x = [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0]
    
    print("8-point FFT using Radix-2 Butterfly Operations")
    print("=" * 50)
    
    # 简单版本
    result = fft_radix2_butterfly(x)
    print("FFT Result (simple):")
    for i, val in enumerate(result):
        print(f"X[{i}] = {val:.3f}")
    
    print("\n" + "=" * 50)
    
    # 详细版本
    result_detailed = fft_radix2_butterfly_detailed(x)
    print("\nFFT Result (detailed):")
    for i, val in enumerate(result_detailed):
        print(f"X[{i}] = {val:.3f}")
    
    # 验证结果
    print("\n" + "=" * 50)
    print("Verification with NumPy FFT:")
    numpy_result = np.fft.fft(x)
    for i, val in enumerate(numpy_result):
        print(f"NumPy X[{i}] = {val:.3f}")