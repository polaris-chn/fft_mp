
def binary_twos_complement_to_decimal(binary_str, integer_bits=1, fraction_bits=7):
    """
    将带符号的二进制补码数转换为十进制

    参数:
    binary_str: 二进制字符串，如"10100101"
    integer_bits: 整数部分的位数（包括符号位）
    fraction_bits: 小数部分的位数

    返回:
    十进制数值
    """
    # 检查输入长度是否正确
    if len(binary_str) != integer_bits + fraction_bits:
        raise ValueError(f"输入二进制字符串长度应为{integer_bits + fraction_bits}位")

    # 如果是负数（符号位为1），需要转换为补码
    if binary_str[0] == '1':
        # 取反加1得到原码
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        # 加1（从小数部分开始）
        carry = 1
        result_bits = list(inverted)
        for i in range(len(result_bits)-1, -1, -1):
            if result_bits[i] == '0' and carry == 1:
                result_bits[i] = '1'
                carry = 0
            elif result_bits[i] == '1' and carry == 1:
                result_bits[i] = '0'
                carry = 1

        # 符号位保持为1
        result_bits[0] = '1'
        original_binary = ''.join(result_bits)

        # 计算数值部分（小数）
        decimal_value = 0.0
        for i, bit in enumerate(original_binary[1:]):
            if bit == '1':
                decimal_value += 2 ** -(i+1)  # 2的负幂次方，表示小数位

        # 由于是负数，结果取负
        decimal_value = -decimal_value
    else:
        # 正数直接计算
        decimal_value = 0.0
        for i, bit in enumerate(binary_str[1:]):
            if bit == '1':
                decimal_value += 2 ** -(i+1)  # 2的负幂次方，表示小数位

    return decimal_value

# 测试
binary_str = "10100101"
result = binary_twos_complement_to_decimal(binary_str, 1, 7)
print(f"二进制数 {binary_str} (带符号，7位小数位，补码表示) 的十进制值为: {result}")
