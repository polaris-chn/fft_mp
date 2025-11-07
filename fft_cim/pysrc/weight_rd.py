import pandas as pd
import numpy as np
import time
import copy


#数据格式：[OC][kw][1][IC]
def read_excel_data(file_path, row_index, accept_weight1):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 获取第 row_index 行的数据（行号从 1 开始）
    row_data = df.iloc[row_index]  # 转换为从 0 开始的索引
    
    # 提取数据并传递给 read_weight 函数
    base_line = row_data['base_line']
    row_begin = row_data['row_begin']
    row_end = row_data['row_end']
    col_begin = row_data['col_begin']
    col_end = row_data['col_end']
    line_num = row_data['line_num']
    data_name = row_data['data_name']
    # 假设 ICn, OCn, weight 是其他函数需要的额外数据，这里先传递空值作为占位
    ICn = 16  # 可以根据实际需要修改
    OCn = 16  # 可以根据实际需要修改
    load_file_name = f'权重/{data_name}.npz'
    print(load_file_name)
    fixed_point_dict = np.load(load_file_name)
    weight = fixed_point_dict["weight_bits"]


    # 调用 read_weight 函数，将数据传递给它
    accept_weight1.read_weight(base_line, row_begin, row_end, col_begin, col_end, line_num, ICn, OCn, weight)

def read_weight():
    accept_weight1 = accept_weight(16,16,96,4,4)
    #读取conv层权重
    for i in range(16):
        read_excel_data('weight.xlsx', i, accept_weight1)
    #读取FC层权重
    load_file_name = f'权重/fc_fixed_point.npz'
    print(load_file_name)
    fixed_point_dict = np.load(load_file_name)
    weight = fixed_point_dict["weight_bits"]
    for m in range(0,4):
            for n in range(0,4):
                for i in range(82,82+2):
                    for j in range(16):
                        for k in range(16):
                            accept_weight1.weight_data[m][n][i][j][k] = copy.deepcopy(weight[(k + n*16)+(i-82)*64][(j + m*16)].tolist())
    #返回权重数据
    return accept_weight1.weight_data



class accept_weight:
    def __init__(self, ICn, OCn, lines, num_array_rows, num_array_cols):
        self.weight_data = [[[[[[0] * 8 for _ in range(OCn)] for _ in range(ICn)] for _ in range(lines)] for _ in range(num_array_cols)] for _ in range(num_array_rows)]

    def read_weight(
        self,
        base_line, 
        row_begin, 
        row_end, 
        col_begin, 
        col_end, 
        line_num,
        ICn,
        OCn,
        weight
    ):
        for m in range(row_begin, (row_end+1)):
            for n in range(col_begin, (col_end+1)):
                for i in range(base_line, base_line + line_num):
                    for j in range(ICn):
                        for k in range(OCn):
                            #print(f"Accessing weight with indices: {k + (n-col_begin)*OCn}, {i-base_line}, 0, {j + (m-row_begin)*ICn}")

                            self.weight_data[m][n][i][j][k] = weight[k + (n-col_begin)*OCn][i-base_line][0][j + (m-row_begin)*ICn].tolist()


#main
weight_data = read_weight()

'''
测试
weight_data = read_weight()
for i in range(3):
    for j in range(4):
        for k in range(16):
            print(f"第{j}行，第{i}个权重的第一个oc通道是{weight_data[j][3][i+9][k][0]}")

print("##############################################")
print("##############################################")
print("##############################################")

load_file_name = f'TCResNet14_model_weight/conv0_0_fixed_point.npz'
fixed_point_dict = np.load(load_file_name)
weight = fixed_point_dict["weight_bits"]
np.set_printoptions(threshold=np.inf)
print(weight[0])
'''

#20250509 lxr

# weight_data = np.swapaxes(weight_data,2,3)
weight_data = np.transpose(weight_data, axes=(0, 1, 3, 5, 4, 2))
weight_data = weight_data.reshape(4, 4, 16, 8*16, 96)
reshaped_Columns = []
print("Total Weight Array shape:\n", np.array(weight_data).shape)
with open('weight_rom_final.txt', 'w') as file:
    for Arr_row in weight_data:
        for Arr_col in Arr_row:
            for IC in Arr_col:
                for Column in IC : #Column:一个Cell 96*1
                        reshaped_lines = np.array(Column).reshape(16,6, order='F')
                        reshaped_Columns.append(reshaped_lines)
                        # for row in reshaped_lines:
                        #     # 将每行的6个元素转换为字符串并用制表符分隔
                        #     line = '\t'.join(map(str, row))
                        #     file.write(line + '\n')
                IC_data = np.hstack(reshaped_Columns)
                for row in IC_data:
                    # 将每行的6*8*16个元素转换为字符串并用空格分隔（可以根据需要调整分隔符）
                    line = ' '.join(map(str, row))
                    file.write(line + '\n')
            file.write("one array finished\n")
            file.write("\n")
        file.write("new array row\n")
        file.write("\n")


'''
def extract_content_after_marker(input_file, output_file, marker):
 
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
 
    extracted_content = []
 
    # 遍历每一行
    for i in range(len(lines)):
        if marker in lines[i]:  # 检查是否包含需要查找的内容
            extracted_content.append(lines[i])  # 添加到输出列表
 
    # 将提取的内容写入新的文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(extracted_content)
 
 
input_file = "E:\\UE5\\TestC\\Saved\\Logs\\TestC.log"  # "填写被提取的文件名"
output_file = "提取后的文件.txt"                        # "填写提取后输出文件名"
marker = "Couldn't find file for package"              # "填写需要查找的内容"
 
extract_content_after_marker(input_file, output_file, marker)
'''
# 读取原始文件
with open('weight_rom_final.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 根据"one array finished"分割文本
parts = content.split('one array finished')

# 去除空行，确保每部分有内容
parts = [part.strip() for part in parts if part.strip()]

# 将每部分写入不同的文件
for i, part in enumerate(parts):
    with open(f'output_{i+1}.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(part)