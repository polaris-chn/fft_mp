import numpy as np

def print_8point_twiddle_factors():
    """
    输出8点基2 FFT的所有旋转因子
    """
    N = 8
    print(f"8点基2 FFT旋转因子表")
    print("=" * 50)
    
    # 基2 FFT有log2(8) = 3个阶段
    num_stages = int(np.log2(N))
    
    for stage in range(num_stages):
        # 每个阶段的旋转因子数量
        num_twiddles = 2 ** stage
        print(f"\n第 {stage+1} 阶段 (共 {num_twiddles} 个旋转因子):")
        print("-" * 30)
        
        for k in range(num_twiddles):
            # 计算旋转因子 W_N^k = e^(-j*2*pi*k/N)
            W = np.exp(-2j * np.pi * k / (2 ** stage)) if stage > 0 else 1.0
            
            # 以多种格式显示旋转因子
            real_part = W.real
            imag_part = W.imag
            magnitude = abs(W)
            
            # 格式化输出
            if abs(real_part) < 1e-10:
                real_part = 0.0
            if abs(imag_part) < 1e-10:
                imag_part = 0.0
                
            # 角度（弧度和度数）
            angle_rad = np.angle(W)
            angle_deg = np.degrees(angle_rad)
            
            print(f"W_{{{2**stage}}}^{{{k}}} = {real_part:8.4f} {imag_part:+8.4f}j  "
                  f"(幅度: {magnitude:.4f}, 角度: {angle_rad:8.4f} rad, {angle_deg:6.1f}°)")

def print_8point_twiddle_matrix():
    """
    以矩阵形式输出8点FFT旋转因子
    """
    N = 8
    print(f"\n\n8点FFT完整旋转因子矩阵 (W_8^{{nk}})")
    print("=" * 80)
    
    # 创建完整的旋转因子矩阵
    print("     ", end="")
    for k in range(N):
        print(f"{k:>9}", end="")
    print()
    
    for n in range(N):
        print(f"{n:>2} | ", end="")
        for k in range(N):
            # W_N^{nk} = e^(-j*2*pi*n*k/N)
            W = np.exp(-2j * np.pi * n * k / N)
            real = W.real
            imag = W.imag
            
            # 格式化显示
            if abs(real) < 1e-10:
                real = 0
            if abs(imag) < 1e-10:
                imag = 0
                
            if imag == 0:
                print(f"{real:9.3f}", end="")
            elif real == 0:
                print(f"{imag:+9.3f}j", end="")
            else:
                print(f"{real:6.2f}{imag:+6.2f}j", end="")
        print()

def print_8point_butterfly_twiddle_factors():
    """
    按蝶形运算详细显示8点FFT旋转因子
    """
    N = 8
    print(f"\n\n8点FFT按蝶形运算阶段显示旋转因子")
    print("=" * 50)
    
    num_stages = int(np.log2(N))
    
    for stage in range(num_stages):
        block_size = 2 ** (stage + 1)
        num_blocks = N // block_size
        
        print(f"\n第 {stage+1} 阶段 (蝶形运算):")
        print(f"  块大小: {block_size}, 块数量: {num_blocks}")
        print(f"  旋转因子:")
        
        # 显示该阶段使用的所有旋转因子
        for k in range(2**stage):
            W = np.exp(-2j * np.pi * k / block_size)
            real = W.real
            imag = W.imag
            if abs(real) < 1e-10:
                real = 0
            if abs(imag) < 1e-10:
                imag = 0
            
            magnitude = abs(W)
            angle_deg = np.degrees(np.angle(W))
            
            print(f"    W_{block_size}^{k} = {real:8.4f} {imag:+8.4f}j  "
                  f"(幅度: {magnitude:.4f}, 角度: {angle_deg:6.1f}°)")

def print_8point_unique_twiddle_factors():
    """
    输出8点FFT中所有唯一的旋转因子值
    """
    print(f"\n\n8点FFT中所有唯一的旋转因子值")
    print("=" * 50)
    
    unique_twiddles = set()
    
    # 收集所有可能的旋转因子
    for stage in range(int(np.log2(8))):
        block_size = 2 ** (stage + 1)
        for k in range(2**stage):
            W = np.exp(-2j * np.pi * k / block_size)
            # 四舍五入以避免浮点精度问题
            W_rounded = complex(round(W.real, 10), round(W.imag, 10))
            unique_twiddles.add(W_rounded)
    
    # 排序并显示
    sorted_twiddles = sorted(list(unique_twiddles), key=lambda x: (x.real, x.imag))
    
    print(f"共有 {len(sorted_twiddles)} 个唯一值:")
    for i, W in enumerate(sorted_twiddles):
        real = W.real
        imag = W.imag
        magnitude = abs(W)
        angle_deg = np.degrees(np.angle(W))
        
        if abs(real) < 1e-10:
            real = 0
        if abs(imag) < 1e-10:
            imag = 0
            
        if imag == 0:
            print(f"  [{i:2d}] {real:8.4f}           (幅度: {magnitude:.4f}, 角度: {angle_deg:6.1f}°)")
        else:
            print(f"  [{i:2d}] {real:8.4f} {imag:+8.4f}j (幅度: {magnitude:.4f}, 角度: {angle_deg:6.1f}°)")

# 运行所有函数
if __name__ == "__main__":
    print_8point_twiddle_factors()
    print_8point_twiddle_matrix()
    print_8point_butterfly_twiddle_factors()
    print_8point_unique_twiddle_factors()