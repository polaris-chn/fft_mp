
`timescale 1ns / 1ps

module test_tb();

    // 输入信号
    reg clk;
    reg rstn;

    // 输出信号
    wire [3:0] count;

    // 实例化被测试模块
    test uut (
        .clk(clk),
        .rstn(rstn),
        .count(count)
    );

    // 生成时钟信号
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 10ns周期，100MHz时钟
    end

    // 测试过程
    initial begin
        // 初始化输入
        rstn = 0;
        $display("=== 仿真开始 ===");
        $display("Time = %0t: 初始化 - 复位激活", $time);

        // 等待几个时钟周期
        #10;

        // 释放复位
        rstn = 1;
        $display("Time = %0t: 释放复位，计数器开始工作", $time);

        // 观察计数器计数过程
        $display("=== 计数器计数过程 ===");
        repeat(20) begin
            @(posedge clk);
            $display("Time = %0t: 计数值 = %d", $time, count);
        end

        // 让计数器运行足够长的时间以观察多个计数周期
        #200;

        // 再次测试复位功能
        $display("=== 测试复位功能 ===");
        $display("Time = %0t: 再次激活复位", $time);
        rstn = 0;
        repeat(3) @(posedge clk);
        $display("Time = %0t: 复位期间计数值 = %d", $time, count);
        rstn = 1;
        $display("Time = %0t: 释放复位", $time);
        repeat(10) begin
            @(posedge clk);
            $display("Time = %0t: 计数值 = %d", $time, count);
        end

        // 结束仿真
        $display("=== 仿真结束 ===");
        $finish;
    end

    // 使用预编译选项生成FSDB波形文件
    `ifdef FSDB
        initial begin
            $fsdbDumpfile("test.fsdb");
            $fsdbDumpvars(0, test_tb);
        end
    `endif

endmodule
