import numpy as np
import math

def print_fft_stages_twiddle_factors(n=64):
    """
    打印N点基2 FFT每一级的旋转因子
    """
    stages = int(math.log2(n))
    print(f"{n}点FFT基2计算共有{stages}级")
    print("=" * 60)
    
    for stage in range(1, stages + 1):
        # 计算当前级的蝶形跨度
        span = n // (2 ** stage)
        # 计算当前级需要的不同旋转因子数量
        num_unique_factors = 2 ** (stage - 1)
        
        print(f"第{stage}级 (Stage {stage}):")
        print(f"  蝶形跨度: {span}")
        print(f"  不同旋转因子数量: {num_unique_factors}")
        print(f"  旋转因子:")
        
        # 打印该级所有旋转因子
        factors_in_stage = []
        for k in range(num_unique_factors):
            # 计算旋转因子 W_N^k
            angle = -2 * math.pi * k / n
            real = math.cos(angle)
            imag = math.sin(angle)
            
            # 格式化输出
            if abs(real) < 1e-10:
                real = 0.0
            if abs(imag) < 1e-10:
                imag = 0.0
                
            if imag == 0:
                factor_str = f"{real:.3f}"
            elif real == 0:
                factor_str = f"{imag:.3f}j"
            elif imag > 0:
                factor_str = f"{real:.3f}+{imag:.3f}j"
            else:
                factor_str = f"{real:.3f}{imag:.3f}j"
                
            factors_in_stage.append(f"W({n},{k})={factor_str}")
        
        # 按行打印，每行最多4个因子
        for i in range(0, len(factors_in_stage), 4):
            print("    " + ", ".join(factors_in_stage[i:i+4]))
        print()

# 执行程序
print_fft_stages_twiddle_factors(64)