
def binary_to_decimal(binary_str, integer_bits=1, fraction_bits=7):
    """
    将带符号的二进制数转换为十进制

    参数:
    binary_str: 二进制字符串，如"01011011"
    integer_bits: 整数部分的位数（包括符号位）
    fraction_bits: 小数部分的位数

    返回:
    十进制数值
    """
    # 检查输入长度是否正确
    if len(binary_str) != integer_bits + fraction_bits:
        raise ValueError(f"输入二进制字符串长度应为{integer_bits + fraction_bits}位")

    # 分离符号位和数值位
    sign_bit = binary_str[0]
    magnitude_bits = binary_str[1:]

    # 计算数值部分（小数）
    decimal_value = 0.0
    for i, bit in enumerate(magnitude_bits):
        if bit == '1':
            decimal_value += 2 ** -(i+1)  # 2的负幂次方，表示小数位

    # 处理符号
    if sign_bit == '1':
        decimal_value = -decimal_value

    return decimal_value

# 测试
binary_str = "01011011"
result = binary_to_decimal(binary_str, 1, 7)
print(f"二进制数 {binary_str} (带符号，7位小数位) 的十进制值为: {result}")
