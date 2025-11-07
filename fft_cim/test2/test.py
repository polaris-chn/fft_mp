import numpy as np
import matplotlib.pyplot as plt

# 随机生成64个在0和1之间的数据
np.random.seed(42)  # 设置随机种子以确保结果可重复
y = np.random.random(64)
x = np.arange(64)  # 时域索引
print(y)

# 创建图形，包含两个子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# 绘制时域图
ax1.plot(x, y, 'b-o', linewidth=1, markersize=4)
ax1.set_xlabel('样本点')
ax1.set_ylabel('幅度')
ax1.set_title('随机数据时域图')
ax1.grid(True, alpha=0.3)

# 进行傅里叶变换
fft_result = np.fft.fft(y)
print(fft_result)
# 计算频率轴
freqs = np.fft.fftfreq(len(y), d=1)  # 由于是离散数据，采样间隔设为1

# 计算幅度谱（取绝对值）
magnitude = np.abs(fft_result)

# 绘制频域图（只显示正频率部分）
positive_freq_idx = freqs >= 0  # 包含直流分量
ax2.plot(freqs[positive_freq_idx], magnitude[positive_freq_idx], 'r-o', linewidth=1, markersize=4)
ax2.set_xlabel('频率 (Hz)')
ax2.set_ylabel('幅度')
ax2.set_title('随机数据频域图 (FFT)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印一些关键信息
print(f"采样点数: {len(y)}")
print(f"采样间隔: {1}")
print(f"频率分辨率: {freqs[1]-freqs[0]:.4f}")