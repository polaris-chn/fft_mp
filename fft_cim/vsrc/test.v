module test (
    input clk,
    input rstn,
    output [3:0] count
);

    reg [3:0] count_tmp;
    always @(posedge clk or negedge rstn) begin
        if(!rstn) 
            count_tmp <= 4'b0;
        else 
            count_tmp <= count_tmp + 1'b1;
    end

    assign count = count_tmp;
    
endmodule