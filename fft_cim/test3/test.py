import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

# 设置中文字体和解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def fft_radix2_butterfly(x):
    """
    使用基2蝶形运算计算FFT
    """
    N = len(x)
    
    # 检查长度是否为2的幂次
    if N & (N - 1) != 0:
        raise ValueError("长度必须是2的幂次")
    
    # 位反转置换
    x_reordered = bit_reverse_order(x)
    
    # 按级进行蝶形运算
    num_stages = int(math.log2(N))
    
    for stage in range(num_stages):
        # 当前阶段的块大小
        block_size = 2 ** (stage + 1)
        # 当前阶段的旋转因子步长
        twiddle_step = N // block_size
        
        # 处理每个块
        for block in range(N // block_size):
            # 处理块内的每对元素
            for i in range(block_size // 2):
                # 计算输入索引
                idx1 = block * block_size + i
                idx2 = block * block_size + i + block_size // 2
                
                # 获取输入值
                a = x_reordered[idx1]
                b = x_reordered[idx2]
                
                # 计算旋转因子 W_N^(twiddle_step * i)
                k = twiddle_step * i
                W = np.exp(-2j * np.pi * k / N)
                
                # 蝶形运算
                temp1 = a + W * b
                temp2 = a - W * b
                
                # 存储结果
                x_reordered[idx1] = temp1
                x_reordered[idx2] = temp2
    
    return x_reordered

def bit_reverse_order(x):
    """
    位反转排序
    """
    N = len(x)
    num_bits = int(math.log2(N))
    x_reordered = [0] * N
    
    for i in range(N):
        # 计算位反转索引
        reversed_i = 0
        for j in range(num_bits):
            if (i >> j) & 1:
                reversed_i |= 1 << (num_bits - 1 - j)
        x_reordered[reversed_i] = x[i]
    
    return x_reordered

def print_input_signal(x):
    """
    打印输入信号
    """
    print("输入信号 (32点):")
    print("=" * 30)
    for i in range(len(x)):
        real, imag = x[i].real, x[i].imag
        if abs(real) < 1e-10: real = 0
        if abs(imag) < 1e-10: imag = 0
        print(f"  [{i:2d}] = {real:6.2f} {imag:+6.2f}j")

# 示例：计算32点FFT
if __name__ == "__main__":
    N = 32
    
    # 创建测试信号 (简单的正弦波)
    x = np.zeros(N, dtype=complex)
    for n in range(N):
        # 频率成分: 直流分量 + 3Hz正弦波 + 7Hz正弦波
        x[n] = np.sin(2 * np.pi * 3 * n / N) + 0.5 * np.sin(2 * np.pi * 7 * n / N)
    
    print_input_signal(x)

    # 创建时域信号图形
    plt.figure(figsize=(15, 10))

    # 子图1: 实部时域波形
    plt.subplot(3, 3, 1)
    n_indices = np.arange(N)
    line1, = plt.plot(n_indices, x.real, 'b-o', linewidth=2, markersize=4, label='实部')
    plt.xlabel('样本点 n')
    plt.ylabel('幅度')
    plt.title('输入信号实部 (时域波形)')
    plt.grid(True, alpha=0.3)
    plt.legend([line1], ['实部'])

    # 子图2: 虚部时域波形
    plt.subplot(3, 3, 2)
    line2, = plt.plot(n_indices, x.imag, 'r-o', linewidth=2, markersize=4, label='虚部')
    plt.xlabel('样本点 n')
    plt.ylabel('幅度')
    plt.title('输入信号虚部 (时域波形)')
    plt.grid(True, alpha=0.3)
    plt.legend([line2], ['虚部'])

    # 子图3: 信号幅度
    plt.subplot(3, 3, 3)
    magnitude = np.abs(x)
    line3, = plt.plot(n_indices, magnitude, 'g-o', linewidth=2, markersize=4, label='幅度')
    plt.xlabel('样本点 n')
    plt.ylabel('幅度')
    plt.title('输入信号幅度')
    plt.grid(True, alpha=0.3)
    plt.legend([line3], ['幅度'])

    # 计算FFT
    X = fft_radix2_butterfly(x.copy())
    
    # 与NumPy结果比较
    X_numpy = np.fft.fft(x)
    
    # 绘制频域结果
    freq_bins = np.arange(N)
    
    # 子图4: FFT结果实部
    plt.subplot(3, 3, 4)
    line4, = plt.plot(freq_bins, X_numpy.real, 'b-o', linewidth=2, markersize=4, label='NumPy')
    line5, = plt.plot(freq_bins, np.array([Xi.real for Xi in X]), 'r--', linewidth=1, markersize=3, label='自实现')
    plt.xlabel('频率 bin')
    plt.ylabel('实部')
    plt.title('FFT结果实部')
    plt.legend([line4, line5], ['NumPy', '自实现'])
    plt.grid(True, alpha=0.3)

    # 子图5: FFT结果虚部
    plt.subplot(3, 3, 5)
    line6, = plt.plot(freq_bins, X_numpy.imag, 'b-o', linewidth=2, markersize=4, label='NumPy')
    line7, = plt.plot(freq_bins, np.array([Xi.imag for Xi in X]), 'r--', linewidth=1, markersize=3, label='自实现')
    plt.xlabel('频率 bin')
    plt.ylabel('虚部')
    plt.title('FFT结果虚部')
    plt.legend([line6, line7], ['NumPy', '自实现'])
    plt.grid(True, alpha=0.3)

    # 子图6: FFT幅度谱
    plt.subplot(3, 3, 6)
    magnitude_spectrum = np.abs(X_numpy)
    magnitude_spectrum_custom = np.abs(X)
    line8, = plt.plot(freq_bins, magnitude_spectrum, 'b-o', linewidth=2, markersize=4, label='NumPy')
    line9, = plt.plot(freq_bins, magnitude_spectrum_custom, 'r--', linewidth=1, markersize=3, label='自实现')
    plt.xlabel('频率 bin')
    plt.ylabel('幅度')
    plt.title('FFT幅度谱')
    plt.legend([line8, line9], ['NumPy', '自实现'])
    plt.grid(True, alpha=0.3)

    # 子图7: FFT相位谱
    plt.subplot(3, 3, 7)
    phase_spectrum = np.angle(X_numpy)
    phase_spectrum_custom = np.angle(X)
    line10, = plt.plot(freq_bins, phase_spectrum, 'b-o', linewidth=2, markersize=4, label='NumPy')
    line11, = plt.plot(freq_bins, phase_spectrum_custom, 'r--', linewidth=1, markersize=3, label='自实现')
    plt.xlabel('频率 bin')
    plt.ylabel('相位 (弧度)')
    plt.title('FFT相位谱')
    plt.legend([line10, line11], ['NumPy', '自实现'])
    plt.grid(True, alpha=0.3)

    # 子图8: FFT幅度谱(仅正频率部分)
    plt.subplot(3, 3, 8)
    # 对于实信号，只显示前N/2+1个点
    positive_freqs = freq_bins[:N//2 + 1]
    magnitude_positive = magnitude_spectrum[:N//2 + 1]
    line12, = plt.plot(positive_freqs, magnitude_positive, 'b-o', linewidth=2, markersize=5, label='幅度')
    plt.xlabel('频率 bin')
    plt.ylabel('幅度')
    plt.title('FFT幅度谱 (正频率部分)')
    plt.legend([line12], ['幅度'])
    plt.grid(True, alpha=0.3)
    
    # 标注主要频率成分
    plt.annotate('f=3', xy=(3, magnitude_positive[3]), xytext=(5, magnitude_positive[3]+2),
                arrowprops=dict(arrowstyle='->'), fontsize=10, color='red')
    plt.annotate('f=7', xy=(7, magnitude_positive[7]), xytext=(9, magnitude_positive[7]+2),
                arrowprops=dict(arrowstyle='->'), fontsize=10, color='red')

    # 子图9: 对数幅度谱(仅正频率部分)
    plt.subplot(3, 3, 9)
    log_magnitude = 20 * np.log10(magnitude_positive + 1e-10)  # 避免log(0)
    line13, = plt.plot(positive_freqs, log_magnitude, 'g-o', linewidth=2, markersize=5, label='dB幅度')
    plt.xlabel('频率 bin')
    plt.ylabel('幅度 (dB)')
    plt.title('FFT对数幅度谱 (正频率部分)')
    plt.legend([line13], ['dB幅度'])
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 打印FFT结果的主要频率成分
    print("\nFFT幅度谱主要峰值:")
    print("=" * 30)
    magnitude_spectrum = np.abs(X)
    for i in range(N):
        if magnitude_spectrum[i] > 1.0:  # 只显示幅度大于1的频率成分
            print(f"频率 bin {i:2d}: 幅度 = {magnitude_spectrum[i]:.4f}")

    # 验证结果准确性
    total_error = 0
    for i in range(N):
        error = abs(X[i] - X_numpy[i])
        total_error += error
    
    print(f"\n平均误差: {total_error/N:.6f}")