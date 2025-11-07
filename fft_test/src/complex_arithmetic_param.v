module complex_mult #(
    parameter integer DATA_WIDTH = 16
) (
    input  signed [DATA_WIDTH-1:0] x0_re,
    input  signed [DATA_WIDTH-1:0] x0_im,
    input  signed [DATA_WIDTH-1:0] x1_re,
    input  signed [DATA_WIDTH-1:0] x1_im,
    output signed [DATA_WIDTH-1:0] res_re,
    output signed [DATA_WIDTH-1:0] res_im
);

    // 饱和函数 - 固定为16位
    function automatic signed [15:0] saturate_16bit;
        input signed [18:0] val;  // 16+3=19位输入
        begin
            // 16位饱和界限: 32767 和 -32768
            localparam signed [18:0] UPPER = 19'd32767;
            localparam signed [18:0] LOWER = -19'd32768;
            
            if (val > UPPER) begin
                saturate_16bit = 16'h7FFF;  // 32767
            end else if (val < LOWER) begin
                saturate_16bit = 16'h8000;  // -32768
            end else begin
                saturate_16bit = val[15:0];
            end
        end
    endfunction

    // Product terms: each is 32-bit wide (Q31)
    wire signed [31:0] ac = x0_re * x1_re;
    wire signed [31:0] bd = x0_im * x1_im;
    wire signed [31:0] ad = x0_re * x1_im;
    wire signed [31:0] bc = x0_im * x1_re;

    // Real part: ac - bd
    wire signed [32:0] real_ext = {ac[31], ac} - {bd[31], bd};

    // Imag part: ad + bc
    wire signed [32:0] imag_ext = {ad[31], ad} + {bc[31], bc};

    // Right arithmetic shift by 15 to convert from Q31 to Q15
    wire signed [16:0] real_shifted = real_ext >>> 15;
    wire signed [16:0] imag_shifted = imag_ext >>> 15;

    // Apply saturation to final result
    assign res_re = saturate_16bit({2'b0, real_shifted}); // 扩展到19位
    assign res_im = saturate_16bit({2'b0, imag_shifted});

endmodule

// =============================================================================
// Module: complex_add
// =============================================================================
module complex_add #(
    parameter integer DATA_WIDTH = 16
) (
    input  signed [DATA_WIDTH-1:0] x0_re,
    input  signed [DATA_WIDTH-1:0] x0_im,
    input  signed [DATA_WIDTH-1:0] x1_re,
    input  signed [DATA_WIDTH-1:0] x1_im,
    output signed [DATA_WIDTH-1:0] res_re,
    output signed [DATA_WIDTH-1:0] res_im
);

    // 饱和函数 - 固定为16位
    function automatic signed [15:0] saturate_16bit;
        input signed [18:0] val;
        begin
            localparam signed [18:0] UPPER = 19'd32767;
            localparam signed [18:0] LOWER = -19'd32768;
            
            if (val > UPPER) begin
                saturate_16bit = 16'h7FFF;
            end else if (val < LOWER) begin
                saturate_16bit = 16'h8000;
            end else begin
                saturate_16bit = val[15:0];
            end
        end
    endfunction

    // Sign-extend to 17 bits to capture overflow
    wire signed [16:0] sum_re = {x0_re[15], x0_re} + {x1_re[15], x1_re};
    wire signed [16:0] sum_im = {x0_im[15], x0_im} + {x1_im[15], x1_im};

    // Saturate to 16 bits
    assign res_re = saturate_16bit({2'b0, sum_re}); // 扩展到19位
    assign res_im = saturate_16bit({2'b0, sum_im});

endmodule

// =============================================================================
// Module: complex_sub
// =============================================================================
module complex_sub #(
    parameter integer DATA_WIDTH = 16
) (
    input  signed [DATA_WIDTH-1:0] x0_re,
    input  signed [DATA_WIDTH-1:0] x0_im,
    input  signed [DATA_WIDTH-1:0] x1_re,
    input  signed [DATA_WIDTH-1:0] x1_im,
    output signed [DATA_WIDTH-1:0] res_re,
    output signed [DATA_WIDTH-1:0] res_im
);

    // 饱和函数 - 固定为16位
    function automatic signed [15:0] saturate_16bit;
        input signed [18:0] val;
        begin
            localparam signed [18:0] UPPER = 19'd32767;
            localparam signed [18:0] LOWER = -19'd32768;
            
            if (val > UPPER) begin
                saturate_16bit = 16'h7FFF;
            end else if (val < LOWER) begin
                saturate_16bit = 16'h8000;
            end else begin
                saturate_16bit = val[15:0];
            end
        end
    endfunction

    // Sign-extend to 17 bits
    wire signed [16:0] diff_re = {x0_re[15], x0_re} - {x1_re[15], x1_re};
    wire signed [16:0] diff_im = {x0_im[15], x0_im} - {x1_im[15], x1_im};

    // Saturate to 16 bits
    assign res_re = saturate_16bit({2'b0, diff_re});
    assign res_im = saturate_16bit({2'b0, diff_im});

endmodule