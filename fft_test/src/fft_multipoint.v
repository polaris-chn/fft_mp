// Author: LR
// Description: Parameterized Multi-Point FFT Accelerator (FFT-only)
//              Supports FFT sizes: 8, 16, 32, ..., 2048 (2^3 to 2^11)
//              Uses a single twiddle ROM for MAX_N=2048, with address scaling
//              for smaller FFT sizes.
//              Input: 1 complex sample per cycle (with sop_in/stb)
//              Output: 1 complex sample per cycle in natural order

module fft_multipoint (
    input             clk,
    input             rst_n,
    input       [3:0] np,        // FFT size: 0→8, 1→16, ..., 8→2048
    input             stb,       // Input data valid
    input             sop_in,    // Start-of-packet (first valid input)
    input      [15:0] x_re,      // Input real part (Q15)
    input      [15:0] x_im,      // Input imaginary part (Q15)

    output            valid_out, // Output data valid
    output reg        sop_out,   // Start-of-packet for output
    output     [15:0] y_re,      // Output real part
    output     [15:0] y_im       // Output imaginary part
);

    // ==============================
    // Constant Parameters
    // ==============================
    localparam MAX_N      = 2048;          // Maximum supported FFT size
    localparam MAX_STAGE  = 11;            // log2(MAX_N)
    localparam STAGE_NUM  = MAX_STAGE - 1; // Number of stages with twiddle factors (0 to 9)

    // ==============================
    // Decode FFT Size
    // ==============================
    reg  [10:0] point;          // Actual FFT size (8 to 2048)
    reg  [3:0]  log2point;      // log2(point), 3 to 11

    always @(*) begin
        case(np)
            4'd0:  begin point = 11'd8;    log2point = 4'd3;  end
            4'd1:  begin point = 11'd16;   log2point = 4'd4;  end
            4'd2:  begin point = 11'd32;   log2point = 4'd5;  end
            4'd3:  begin point = 11'd64;   log2point = 4'd6;  end
            4'd4:  begin point = 11'd128;  log2point = 4'd7;  end
            4'd5:  begin point = 11'd256;  log2point = 4'd8;  end
            4'd6:  begin point = 11'd512;  log2point = 4'd9;  end
            4'd7:  begin point = 11'd1024; log2point = 4'd10; end
            4'd8:  begin point = 11'd2048; log2point = 4'd11; end
            default: begin point = 11'd8;  log2point = 4'd3;  end
        endcase
    end

    // ==============================
    // Frame Control Counter
    // ==============================
    // Total latency = 3*point/2 cycles
    reg [11:0] cnt;
    wire busy = (cnt != 12'd0);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 12'd0;
        end else if (sop_in && !busy) begin
            cnt <= 12'd1;
        end else if (stb || busy) begin
            if (cnt == (point * 3 / 2 - 1)) begin
                cnt <= 12'd0;
            end else begin
                cnt <= cnt + 1'b1;
            end
        end
    end

    // ==============================
    // Output Timing Control
    // ==============================
    // Output N samples: from cnt = point-1 to cnt = 2*point-2
    wire output_valid = (cnt >= (point - 1)) && (cnt < (2 * point - 1));

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sop_out <= 1'b0;
        end else begin
            sop_out <= (cnt == (point - 1)); // Assert on first output sample
        end
    end

    // ==============================
    // Data Path: Butterfly and Switch Arrays
    // ==============================
    // Butterfly I/O (stages 0 to STAGE_NUM-1)
    wire [15:0] bf_x0_re [0:STAGE_NUM-1];
    wire [15:0] bf_x0_im [0:STAGE_NUM-1];
    wire [15:0] bf_x1_re [0:STAGE_NUM-1];
    wire [15:0] bf_x1_im [0:STAGE_NUM-1];
    wire [15:0] bf_w_re  [0:STAGE_NUM-1];
    wire [15:0] bf_w_im  [0:STAGE_NUM-1];
    wire [15:0] bf_y0_re [0:STAGE_NUM-1];
    wire [15:0] bf_y0_im [0:STAGE_NUM-1];
    wire [15:0] bf_y1_re [0:STAGE_NUM-1];
    wire [15:0] bf_y1_im [0:STAGE_NUM-1];

    // Switch units
    wire        switch_sel [0:STAGE_NUM-1];
    wire [15:0] switch_x0_re [0:STAGE_NUM-1];
    wire [15:0] switch_x0_im [0:STAGE_NUM-1];
    wire [15:0] switch_x1_re [0:STAGE_NUM-1];
    wire [15:0] switch_x1_im [0:STAGE_NUM-1];
    wire [15:0] switch_y0_re [0:STAGE_NUM-1];
    wire [15:0] switch_y0_im [0:STAGE_NUM-1];
    wire [15:0] switch_y1_re [0:STAGE_NUM-1];
    wire [15:0] switch_y1_im [0:STAGE_NUM-1];

    // Final stage (no twiddle factor)
    wire [15:0] bf_noW_x0_re, bf_noW_x0_im;
    wire [15:0] bf_noW_x1_re, bf_noW_x1_im;
    wire [15:0] bf_noW_y0_re, bf_noW_y0_im;
    wire [15:0] bf_noW_y1_re, bf_noW_y1_im;

    // ==============================
    // Instantiate Stages with Correct Twiddle Addressing
    // ==============================
    genvar i;
    generate
        for (i = 0; i < STAGE_NUM; i = i + 1) begin : stage_gen

            // --- Butterfly ---
            bf_rdx2 bf_u (
                .x0_re(bf_x0_re[i]), .x0_im(bf_x0_im[i]),
                .x1_re(bf_x1_re[i]), .x1_im(bf_x1_im[i]),
                .w_re (bf_w_re[i]),  .w_im (bf_w_im[i]),
                .y0_re(bf_y0_re[i]), .y0_im(bf_y0_im[i]),
                .y1_re(bf_y1_re[i]), .y1_im(bf_y1_im[i])
            );

            // --- Switch ---
            switch switch_u (
                .sel(switch_sel[i]),
                .x0_re(switch_x0_re[i]), .x0_im(switch_x0_im[i]),
                .x1_re(switch_x1_re[i]), .x1_im(switch_x1_im[i]),
                .y0_re(switch_y0_re[i]), .y0_im(switch_y0_im[i]),
                .y1_re(switch_y1_re[i]), .y1_im(switch_y1_im[i])
            );

            // --- Twiddle Address Generation (Key Fix!) ---
            // Local twiddle index for this stage
            wire [10:0] k_local = (cnt >> (log2point - 1 - i)) & (point/2 - 1);
            // Scale to 2048-point ROM address: addr = k_local * (2048 / point)
            wire shift_bits = 11 - log2point; // because 2048 = 2^11
            wire [10:0] tw_addr = k_local << shift_bits;

            // --- Twiddle ROM (shared for all sizes) ---
            twiddle_rom #(.MAX_N(MAX_N)) tw_rom_u (
                .clk(clk),
                .addr(tw_addr),
                .data_re(bf_w_re[i]),
                .data_im(bf_w_im[i])
            );

            // --- Switch Control ---
            assign switch_sel[i] = cnt[log2point - 2 - i];
            assign switch_x0_re[i] = bf_y0_re[i];
            assign switch_x0_im[i] = bf_y0_im[i];
            assign switch_x1_re[i] = bf_y1_re[i];  
            assign switch_x1_im[i] = bf_y1_im[i];  

        end
    endgenerate

    // ==============================
    // Final Butterfly (Stage 10, No Twiddle)
    // ==============================
    bf_rdx2_noW bf_noW_u (
        .x0_re(bf_noW_x0_re), .x0_im(bf_noW_x0_im),
        .x1_re(bf_noW_x1_re), .x1_im(bf_noW_x1_im),
        .y0_re(bf_noW_y0_re), .y0_im(bf_noW_y0_im),
        .y1_re(bf_noW_y1_re), .y1_im(bf_noW_y1_im)
    );

    // ==============================
    // Data Routing and Bypass Logic
    // ==============================
    // Stage 0: always use full delay
    shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 1))) sr_in_re (
        .clk(clk), .rst_n(rst_n), .d_in(x_re), .d_out(bf_x0_re[0])
    );
    shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 1))) sr_in_im (
        .clk(clk), .rst_n(rst_n), .d_in(x_im), .d_out(bf_x0_im[0])
    );
    assign bf_x1_re[0] = x_re;
    assign bf_x1_im[0] = x_im;

    // Stages 1 to STAGE_NUM-1: with bypass for small FFTs
    generate
        for (i = 1; i < STAGE_NUM; i = i + 1) begin : bypass_gen
            wire bypass = (log2point <= (i + 2));
            assign bf_x1_re[i] = bypass ? x_re : switch_y1_re[i-1];
            assign bf_x1_im[i] = bypass ? x_im : switch_y1_im[i-1];

            wire [15:0] din_re = bypass ? x_re : switch_y0_re[i-1];
            wire [15:0] din_im = bypass ? x_im : switch_y0_im[i-1];

            shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 1 - i))) sr_re (
                .clk(clk), .rst_n(rst_n), .d_in(din_re), .d_out(bf_x0_re[i])
            );
            shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 1 - i))) sr_im (
                .clk(clk), .rst_n(rst_n), .d_in(din_im), .d_out(bf_x0_im[i])
            );
        end
    endgenerate

    // Final stage inputs
    assign bf_noW_x1_re = switch_y1_re[STAGE_NUM-1];
    assign bf_noW_x1_im = switch_y1_im[STAGE_NUM-1];

    shiftreg #(.WIDTH(16), .DEPTH(1)) sr_last_re (
        .clk(clk), .rst_n(rst_n), .d_in(switch_y0_re[STAGE_NUM-1]), .d_out(bf_noW_x0_re)
    );
    shiftreg #(.WIDTH(16), .DEPTH(1)) sr_last_im (
        .clk(clk), .rst_n(rst_n), .d_in(switch_y0_im[STAGE_NUM-1]), .d_out(bf_noW_x0_im)
    );

    // Output alignment delays
    generate
        for (i = 0; i < STAGE_NUM; i = i + 1) begin : output_delay
            shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 2 - i))) delay_re (
                .clk(clk), .rst_n(rst_n), .d_in(bf_y1_re[i]), .d_out(switch_x1_re[i])
            );
            shiftreg #(.WIDTH(16), .DEPTH(1 << (MAX_STAGE - 2 - i))) delay_im (
                .clk(clk), .rst_n(rst_n), .d_in(bf_y1_im[i]), .d_out(switch_x1_im[i])
            );
        end
    endgenerate

    // ==============================
    // Output Reordering
    // ==============================
    wire [15:0] reorder_out_re, reorder_out_im;
    wire        reorder_valid;

    // Note: This reorder module expects 1 complex input per cycle
    reorder #(.DATA_WIDTH(16), .MAX_N(MAX_N)) reorder_u (
        .clk(clk),
        .rst_n(rst_n),
        .in_re     (bf_noW_y0_re),
        .in_im     (bf_noW_y0_im),
        .in_valid  (output_valid),
        .np        (np),
        .out_re    (reorder_out_re),
        .out_im    (reorder_out_im),
        .out_valid (reorder_valid)
    );

    assign valid_out = reorder_valid;
    assign y_re      = reorder_out_re;
    assign y_im      = reorder_out_im;

endmodule