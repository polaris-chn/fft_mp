
import numpy as np
import cmath

def bit_reverse(x, n):
    """执行位反转操作，用于重排输入数据"""
    j = 0
    for i in range(1, n):
        bit = n >> 1
        j ^= bit
        if i < bit:
            bit >>= 1
        else:
            while bit & j:
                j ^= bit
                bit >>= 1
    return j

def fft_8point(x):
    """
    实现8点基2FFT算法
    x: 输入信号，长度为8的复数列表
    返回: FFT结果，长度为8的复数列表
    """
    N = len(x)
    if N != 8:
        raise ValueError("此函数仅适用于8点FFT")

    # 第一步：位反转重排
    x = [x[bit_reverse(i, 3)] for i in range(8)]

    # 第二步：执行3级蝶形运算
    # 第1级：蝶形间距=1，共4个蝶形单元
    for i in range(0, 8, 2):
        # 蝶形运算
        temp = x[i]
        x[i] = temp + x[i+1]
        x[i+1] = temp - x[i+1]

    # 第2级：蝶形间距=2，共2个蝶形单元
    for i in range(0, 4, 2):
        for j in range(i, i+2):
            # 蝶形运算，带旋转因子
            temp = x[j]
            twiddle = cmath.exp(-2j * cmath.pi * (j-i) / 8)
            x[j] = temp + x[j+2] * twiddle
            x[j+2] = temp - x[j+2] * twiddle

    # 第3级：蝶形间距=4，1个蝶形单元
    for i in range(0, 2):
        for j in range(i, i+4, 2):
            # 蝶形运算，带旋转因子
            temp = x[j]
            twiddle1 = cmath.exp(-2j * cmath.pi * (j-i) / 8)
            twiddle2 = cmath.exp(-2j * cmath.pi * (j-i+1) / 8)
            x[j] = temp + x[j+4] * twiddle1
            x[j+4] = temp - x[j+4] * twiddle1
            temp = x[j+1]
            x[j+1] = temp + x[j+5] * twiddle2
            x[j+5] = temp - x[j+5] * twiddle2

    return x

# 测试代码
if __name__ == "__main__":
    # 创建一个8点测试信号
    x = [complex(i, 0) for i in range(8)]  # [0, 1, 2, 3, 4, 5, 6, 7]

    print("输入信号:")
    print(x)

    # 计算FFT
    fft_result = fft_8point(x)

    print("\nFFT结果:")
    for i, val in enumerate(fft_result):
        print(f"X[{i}] = {val:.2f}")

    # 使用numpy的FFT进行验证
    numpy_fft = np.fft.fft(x)
    print("\nNumPy FFT结果 (用于验证):")
    for i, val in enumerate(numpy_fft):
        print(f"X[{i}] = {val:.2f}")
