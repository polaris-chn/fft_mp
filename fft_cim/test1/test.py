import numpy as np
from decimal import Decimal

def generate_twiddle_factors(N):
  """
  生成长度为N的FFT旋转因子。

  Args:
    N: FFT的长度。

  Returns:
    一个包含旋转因子的NumPy数组，形状为(N//2, 1)。
  """
  return np.exp(-1j * 2 * np.pi * np.arange(N//2) / N)

def save_twiddle_factors_to_file(twiddle_factors, filename, format_type='complex'):
  """
  将旋转因子保存到文件中

  Args:
    twiddle_factors: 旋转因子数组
    filename: 保存的文件名
    format_type: 保存格式 ('complex', 'separate', 'magnitude_phase')
  """
  with open(filename, 'w') as f:
    f.write("# FFT Twiddle Factors\n")
    f.write(f"# Number of factors: {len(twiddle_factors)}\n")
    f.write("# Format: index, real, imaginary, magnitude, phase\n")
    f.write("#" + "-"*50 + "\n")
    
    for i, factor in enumerate(twiddle_factors):
      real = factor.real
      imag = factor.imag
      magnitude = abs(factor)
      phase = np.angle(factor)
      
      if format_type == 'complex':
        # 保存为复数形式
        f.write(f"{i}: {real:.6f}{imag:+.6f}j\n")
      elif format_type == 'separate':
        # 分别保存实部和虚部
        f.write(f"{i} {real:.6f} {imag:.6f}\n")
      elif format_type == 'magnitude_phase':
        # 保存为幅度和相位
        f.write(f"{i} {magnitude:.6f} {phase:.6f}\n")
      else:
        # 详细格式
        f.write(f"{i} {real:.6f} {imag:.6f} {magnitude:.6f} {phase:.6f}\n")

def save_twiddle_factors_binary(twiddle_factors, filename):
  """
  将旋转因子以二进制格式保存到文件中

  Args:
    twiddle_factors: 旋转因子数组
    filename: 保存的文件名
  """
  # 保存为.npy格式（NumPy二进制格式）
  np.save(filename, twiddle_factors)
  
  # 保存为.ram格式（原始二进制数据）
  with open(filename + '.ram', 'wb') as f:
    # 保存为连续的浮点数（实部,虚部交替）
    data = np.column_stack((twiddle_factors.real, twiddle_factors.imag)).flatten()
    data.tofile(f)
  
  # 或者保存为原始二进制数据
  with open(filename + '.raw', 'wb') as f:
    # 保存为连续的浮点数（实部,虚部交替）
    data = np.column_stack((twiddle_factors.real, twiddle_factors.imag)).flatten()
    data.tofile(f)

def read_ram_file_binary(filename):
  """
  直接以二进制格式读取.ram文件

  Args:
    filename: .ram文件名

  Returns:
    包含二进制数据的字节串
  """
  with open(filename, 'rb') as f:
    binary_data = f.read()
  return binary_data

def read_twiddle_factors_from_ram(filename, dtype=np.float64):
  """
  从.ram文件读取旋转因子

  Args:
    filename: .ram文件名
    dtype: 数据类型（默认为float64）

  Returns:
    重构的复数旋转因子数组
  """
  # 以二进制形式读取文件
  binary_data = read_ram_file_binary(filename)
  
  # 将二进制数据解释为浮点数数组
  float_data = np.frombuffer(binary_data, dtype=dtype)
  
  # 重构为复数形式（实部和虚部交替）
  real_parts = float_data[0::2]
  imag_parts = float_data[1::2]
  complex_data = real_parts + 1j * imag_parts
  
  return complex_data

def display_binary_content(binary_data, max_bytes=32):
  """
  显示二进制数据的内容

  Args:
    binary_data: 字节串
    max_bytes: 显示的最大字节数
  """
  print(f"二进制数据大小: {len(binary_data)} 字节")
  print("前{}字节的十六进制表示:".format(min(max_bytes, len(binary_data))))
  
  # 以十六进制格式显示
  hex_str = ' '.join(f'{b:02x}' for b in binary_data[:max_bytes])
  print(hex_str)
  
  if len(binary_data) > max_bytes:
      print("... (还有{}字节)".format(len(binary_data) - max_bytes))


if __name__ == '__main__':
  # 示例：生成长度为32的FFT的旋转因子
  N = 8
  
  twiddle_factors = generate_twiddle_factors(N)

  # 将旋转因子保存到不同格式的文件中
  save_twiddle_factors_to_file(twiddle_factors, 'twiddle_factors.txt', 'complex')
  save_twiddle_factors_to_file(twiddle_factors, 'twiddle_factors_detailed.txt', 'separate')
  save_twiddle_factors_to_file(twiddle_factors, 'twiddle_factors_polar.txt', 'magnitude_phase')

  # 保存为二进制格式
  save_twiddle_factors_binary(twiddle_factors, 'twiddle_factors.npy')

  print("旋转因子已保存到以下文件:")
  print("- twiddle_factors.txt (复数格式)")
  print("- twiddle_factors_detailed.txt (实部虚部分开)")
  print("- twiddle_factors_polar.txt (幅度相位格式)")
  print("- twiddle_factors.npy (NumPy二进制格式)")
  print("- twiddle_factors.npy.ram (RAM二进制格式)")
  print("- twiddle_factors.raw (原始二进制格式)")

  # 验证读取
  print("\n验证读取:")
  loaded_factors = np.load('twiddle_factors.npy')
  print("从.npy文件读取的因子[3]:", loaded_factors[3])
  print("与原因子匹配:", np.allclose(twiddle_factors, loaded_factors))

  # 直接以二进制格式读取.ram文件
  print("\n直接二进制读取.ram文件:")
  try:
      # 读取二进制内容
      binary_content = read_ram_file_binary('twiddle_factors.npy.ram')
      display_binary_content(binary_content, 64)
      
      # 从.ram文件重构旋转因子
      ram_factors = read_twiddle_factors_from_ram('twiddle_factors.npy.ram')
      print(f"\n从.ram文件重构的因子[3]: {ram_factors[3]}")
      print(f"与原始.npy文件数据匹配: {np.allclose(loaded_factors, ram_factors)}")
      print(f"与原始计算数据匹配: {np.allclose(twiddle_factors, ram_factors)}")
      
  except FileNotFoundError:
      print("未找到.ram文件")