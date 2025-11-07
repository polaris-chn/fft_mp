import pandas as pd
import numpy as np
import time
def generate_netlist(input_filename,i_arr):
    #读取仅包含0和1的txt文件，并转换为二维列表
    weights = []
    with open(input_filename, 'r') as file:
        for line in file:
            # 去除行末换行符，并将每行转换为整数列表
            row = [int(char) for char in line.strip()]
            weights.append(row)

    # 生成网表文件
    with open('array_netlist_front.txt', 'r', encoding='utf-8') as file1:
        content1 = file1.read()
    with open('array_netlist_back.txt', 'r', encoding='utf-8') as file3:
        content3 = file3.read()
    
    with open(f'./Array_netlists_40n/Array{i_arr}', 'w', encoding='utf-8') as output_file:

        output_file.write(content1)
        output_file.write(f'************************************************************************\n')
        output_file.write(f'************************************************************************\n')

        for w in range(16): #OC
            # with open(f'./8bCols_netlists/8Cols_arr{i_arr}_oc{k}', 'w', encoding='utf-8') as output_file:
            for j in range(8): #8bit   msb-lsb j=0->msb,j=7->lsb
                for i in range(16):  #IC
                    w_cell = [row[w*8+j] for row in weights[i*96:(i+1)*96]] #第w*8+j列 第0-15行，中括号左闭右开，行列索引从0开始
                    
                    output_file.write(f"****Sub-Circuit for Cell_arr{i_arr}_ic{i}_col{7-j}_oc{w}, May 12 2025*****\n")
                    output_file.write(f".SUBCKT Cell_arr{i_arr}_ic{i}_col{7-j}_oc{w} Cell_out IN<0:15> \n+ RSTN VDD VSS \n+ row_2level<0:5> \n+ row_en<0:15>\n")
                    output_file.write(f'*.PININFO IN<0:15>:I Reset_:I VDD:I VSS:I row_2level<0>:I row_2level<1>:I\n')
                    output_file.write(f'*.PININFO row_2level<2>:I row_2level<3>:I row_2level<4>:I row_2level<5>:I\n')
                    output_file.write(f'*.PININFO row_en<0>:I row_en<1>:I row_en<2>:I row_en<3>:I row_en<4>:I\n')
                    output_file.write(f'*.PININFO row_en<5>:I row_en<6>:I row_en<7>:I row_en<8>:I row_en<9>:I\n')
                    output_file.write(f'*.PININFO row_en<10>:I row_en<11>:I row_en<12>:I row_en<13>:I row_en<14>:I\n')
                    output_file.write(f'*.PININFO row_en<15>:I Cell_out:O\n')
                    for k in range(96):
                        if w_cell[k]==1:
                            output_file.write(f'MNM{k} mid_out{k//16} row_en<{k%16}> IN<{k%16}> VSS nhvt09_ckt m=1 l=40n w=100n\n')
                        elif w_cell[k]==0 :
                            output_file.write(f'MNM{k} net{k} row_en<{k%16}> IN<{k%16}> VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    
                    output_file.write(f'MPM1 Cell_out RSTN VDD VDD plvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM96 Cell_out row_2level<0> mid_out0 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM97 Cell_out row_2level<1> mid_out1 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM98 Cell_out row_2level<2> mid_out2 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM99 Cell_out row_2level<3> mid_out3 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM100 Cell_out row_2level<4> mid_out4 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'MNM101 Cell_out row_2level<5> mid_out5 VSS nhvt09_ckt m=1 l=40n w=100n\n')
                    output_file.write(f'.ENDS\n')
                if j==0:
                    output_file.write(f'************************************************************************\n')
                    output_file.write(f'.SUBCKT Col{7-j}_arr{i_arr}_oc{w} OUT<0:5> IN<0:255>\n')
                    output_file.write(f'+ RSTN VDD VSS row_2level<0:5> row_en<0:15> sign_inv<0:15>\n')
                    output_file.write(f'*.PININFO IN<0:255>:I RSTN:I VDD:I VSS:I row_2level<0:5>:I row_en<0:15>:I sign_inv<0:15>:I\n')
                    output_file.write(f'*.PININFO OUT<0:5>:O\n')
                    output_file.write(f'XI0 Cell_out<0> IN<0:15> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic0_col{7-j}_oc{w}\n')
                    output_file.write(f'XI1 Cell_out<1> IN<16:31> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic1_col{7-j}_oc{w}\n')
                    output_file.write(f'XI2 Cell_out<2> IN<32:47> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic2_col{7-j}_oc{w}\n')
                    output_file.write(f'XI3 Cell_out<3> IN<48:63> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic3_col{7-j}_oc{w}\n')
                    output_file.write(f'XI4 Cell_out<4> IN<64:79> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic4_col{7-j}_oc{w}\n')
                    output_file.write(f'XI5 Cell_out<5> IN<80:95> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic5_col{7-j}_oc{w}\n')
                    output_file.write(f'XI6 Cell_out<6> IN<96:111> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic6_col{7-j}_oc{w}\n')
                    output_file.write(f'XI7 Cell_out<7> IN<112:127> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic7_col{7-j}_oc{w}\n')
                    output_file.write(f'XI8 Cell_out<8> IN<128:143> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic8_col{7-j}_oc{w}\n')
                    output_file.write(f'XI9 Cell_out<9> IN<144:159> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic9_col{7-j}_oc{w}\n')
                    output_file.write(f'XI10 Cell_out<10> IN<160:175> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic10_col{7-j}_oc{w}\n')
                    output_file.write(f'XI11 Cell_out<11> IN<176:191> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic11_col{7-j}_oc{w}\n')
                    output_file.write(f'XI12 Cell_out<12> IN<192:207> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic12_col{7-j}_oc{w}\n')
                    output_file.write(f'XI13 Cell_out<13> IN<208:223> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic13_col{7-j}_oc{w}\n')
                    output_file.write(f'XI14 Cell_out<14> IN<224:239> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic14_col{7-j}_oc{w}\n')
                    output_file.write(f'XI15 Cell_out<15> IN<240:255> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic15_col{7-j}_oc{w}\n')
                    output_file.write(f'XI16 OUT<0:5> Cell_out<0:15> VDD VSS sign_inv<0:15> / AdderTree_sign_domino\n')
                    output_file.write(f'.ENDS\n')
                else :
                    output_file.write(f'************************************************************************\n')
                    output_file.write(f'.SUBCKT Col{7-j}_arr{i_arr}_oc{w} OUT<0:4> IN<0:255>\n')
                    output_file.write(f'+ RSTN VDD VSS row_2level<0:5> row_en<0:15> sign_inv<0:15>\n')
                    output_file.write(f'*.PININFO IN<0:255>:I RSTN:I VDD:I VSS:I row_2level<0:5>:I row_en<0:15>:I sign_inv<0:15>:I\n')
                    output_file.write(f'*.PININFO OUT<0:4>:O\n')
                    output_file.write(f'XI0 Cell_out<0> IN<0:15> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic0_col{7-j}_oc{w}\n')
                    output_file.write(f'XI1 Cell_out<1> IN<16:31> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic1_col{7-j}_oc{w}\n')
                    output_file.write(f'XI2 Cell_out<2> IN<32:47> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic2_col{7-j}_oc{w}\n')
                    output_file.write(f'XI3 Cell_out<3> IN<48:63> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic3_col{7-j}_oc{w}\n')
                    output_file.write(f'XI4 Cell_out<4> IN<64:79> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic4_col{7-j}_oc{w}\n')
                    output_file.write(f'XI5 Cell_out<5> IN<80:95> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic5_col{7-j}_oc{w}\n')
                    output_file.write(f'XI6 Cell_out<6> IN<96:111> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic6_col{7-j}_oc{w}\n')
                    output_file.write(f'XI7 Cell_out<7> IN<112:127> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic7_col{7-j}_oc{w}\n')
                    output_file.write(f'XI8 Cell_out<8> IN<128:143> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic8_col{7-j}_oc{w}\n')
                    output_file.write(f'XI9 Cell_out<9> IN<144:159> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic9_col{7-j}_oc{w}\n')
                    output_file.write(f'XI10 Cell_out<10> IN<160:175> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic10_col{7-j}_oc{w}\n')
                    output_file.write(f'XI11 Cell_out<11> IN<176:191> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic11_col{7-j}_oc{w}\n')
                    output_file.write(f'XI12 Cell_out<12> IN<192:207> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic12_col{7-j}_oc{w}\n')
                    output_file.write(f'XI13 Cell_out<13> IN<208:223> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic13_col{7-j}_oc{w}\n')
                    output_file.write(f'XI14 Cell_out<14> IN<224:239> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic14_col{7-j}_oc{w}\n')
                    output_file.write(f'XI15 Cell_out<15> IN<240:255> RSTN VDD VSS row_2level<0:5> row_en<0:15> / Cell_arr{i_arr}_ic15_col{7-j}_oc{w}\n')
                    output_file.write(f'XI16 OUT<0:4> Cell_out<0:15> VDD VSS sign_inv<0:15> / AdderTree_domino\n')
                    output_file.write(f'.ENDS\n')
            output_file.write(f'************************************************************************\n')
            output_file.write(f'.SUBCKT 8Cols_arr{i_arr}_oc{w} SUM<0:12> IN<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS\n')
            output_file.write(f'*.PININFO IN<0:255>:I RSTN:I VDD:I VSS:I row_en2<0:5>:I row_en1<0:15>:I sign_inv<0:15>:I SUM<0:12>:O\n')
            output_file.write(f'XI0 SUM<0>,b0<1:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col0_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI1 b1<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col1_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI2 b2<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col2_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI3 b3<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col3_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI4 b4<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col4_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI5 b5<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col5_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI6 b6<0:4> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col6_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI7 b7<0:5> IN<0:255> RSTN VDD VSS row_en2<0:5> row_en1<0:15> sign_inv<0:15> / Col7_arr{i_arr}_oc{w}\n')
            output_file.write(f'XI8 SUM<1:12> b0<1:4> b1<0:4> b2<0:4> b3<0:4> b4<0:4> b5<0:4> b6<0:4> b7<0:5> VDD VSS / Bit_shifter_full\n')
            output_file.write(f'.ENDS\n')
        output_file.write(f'************************************************************************\n')
        output_file.write(f'.SUBCKT Arr{i_arr} SUM<0:207> IN<0:15> RSTN row_en1<0:15> row_en2<0:5> cnt_b7 VDD VSS\n')
        output_file.write(f'*.PININFO IN<0:15>:I RSTN:I VDD:I VSS:I row_en2<0:5>:I row_en1<0:15>:I cnt_b7:I SUM<0:207>:O\n')
        output_file.write(f'XI0 SUM<0:12> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc0\n')
        output_file.write(f'XI1 SUM<13:25> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc1\n')
        output_file.write(f'XI2 SUM<26:38> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc2\n')
        output_file.write(f'XI3 SUM<39:51> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc3\n')
        output_file.write(f'XI4 SUM<52:64> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc4\n')
        output_file.write(f'XI5 SUM<65:77> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc5\n')
        output_file.write(f'XI6 SUM<78:90> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc6\n')
        output_file.write(f'XI7 SUM<91:103> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc7\n')
        output_file.write(f'XI8 SUM<104:116> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc8\n')
        output_file.write(f'XI9 SUM<117:129> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc9\n')
        output_file.write(f'XI10 SUM<130:142> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc10\n')
        output_file.write(f'XI11 SUM<143:155> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc11\n')
        output_file.write(f'XI12 SUM<156:168> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc12\n')
        output_file.write(f'XI13 SUM<169:181> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc13\n')
        output_file.write(f'XI14 SUM<182:194> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc14\n')
        output_file.write(f'XI15 SUM<195:207> IN_N_BUF<0:255> RSTN row_en1<0:15> row_en2<0:5> sign_inv<0:15> VDD VSS / 8Cols_arr{i_arr}_oc15\n')
        # output_file.write(f'XI18<0> in_buf<0> IN_N_BUF<0:255> VDD VSS row_en1<0:15> / IN_gate\n')
        # output_file.write(f'XI18<1> in_buf<1> IN_N_BUF<0:255> VDD VSS row_en1<0:15> / IN_gate\n')
        # output_file.write(f'XI38<0:15> IN<0:15> cnt_msb VDD VDD VSS VSS sign_inv<0:15> / AND2V1_140P7T40H\n')
        # output_file.write(f'XI26<0:15> IN<0:15> VDD VDD VSS VSS IN_N<0:15> / INV1_140P7T40H\n')
        # output_file.write(f'XI20<0:15> IN_N<0:15> VDD VDD VSS VSS in_buf<0:15> / BUFV16_140P7T40H\n')

                
        output_file.write(f'************************************************************************\n')
        output_file.write(f'************************************************************************\n')
        output_file.write(content3)



# main
for i in range(1,17):
    input_filename = f'output_{i}.txt'
    generate_netlist(input_filename,i)


with open(f'./Array_netlists_40n/Array_all', 'w', encoding='utf-8') as outfile:
    for i in range(1,17):
        with open(f'./Array_netlists_40n/Array{i}', 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())  # 直接写入全部内容