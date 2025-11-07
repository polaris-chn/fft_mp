// Author: LR
// Create Date: 2025/4/5
// Description: Bit-Reversal Reordering Unit for FFT Accelerator
//              Converts FFT output from bit-reversed order to natural (linear) order.
//              Designed to work with fft_multipoint.v (supports 8 to 2048 points).
//              Input: 1 complex sample per cycle during in_valid.
//              Output: 1 complex sample per cycle in natural order during out_valid.

module reorder #(
    parameter DATA_WIDTH = 16,   // Data width of real/imaginary parts
    parameter MAX_N      = 2048  // Maximum FFT size (must be power of 2)
) (
    input                   clk,
    input                   rst_n,

    // Input from FFT pipeline (bit-reversed order)
    input      [DATA_WIDTH-1:0] in_re,
    input      [DATA_WIDTH-1:0] in_im,
    input                   in_valid,

    // FFT size selector (aligned with fft_multipoint)
    input            [3:0] np,  // 0→8, 1→16, 2→32, 3→64, 4→128,
                               // 5→256, 6→512, 7→1024, 8→2048

    // Output in natural order
    output reg [DATA_WIDTH-1:0] out_re,
    output reg [DATA_WIDTH-1:0] out_im,
    output reg              out_valid
);

    // ====================================================================
    // Step 1: Decode FFT size based on np
    // ====================================================================
    reg  [10:0] point;          // Actual FFT length (8 to 2048)
    reg  [3:0]  log2point;      // log2(point), ranges from 3 to 11

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
            default: begin point = 11'd8;  log2point = 4'd3;  end // safe fallback
        endcase
    end

    // ====================================================================
    // Step 2: Write Phase — Store data at bit-reversed addresses
    // ====================================================================
    reg [10:0] write_counter;   // Counts 0 to point-1 (total 'point' samples)
    reg        write_done;      // High when all inputs are written

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            write_counter <= 11'd0;
            write_done    <= 1'b0;
        end else if (in_valid && !write_done) begin
            if (write_counter == point - 1) begin
                write_counter <= 11'd0;
                write_done    <= 1'b1;  // Write phase complete
            end else begin
                write_counter <= write_counter + 1'b1;
            end
        end
    end

    // Generate full-width (11-bit) bit-reversed address
    wire [10:0] full_rev_addr;
    reverse_bits #(.WIDTH(11)) u_reverse (
        .in (write_counter),        // Zero-padded to 11 bits automatically
        .out(full_rev_addr)
    );

    // Mask to keep only log2point LSBs: effective address = rev_addr[log2point-1:0]
    // Since point = 2^log2point, (point - 1) is a mask of 'log2point' ones.
    wire [10:0] write_addr = full_rev_addr & (point - 1);

    // ====================================================================
    // Step 3: Memory Storage (inferred as dual-port or two single-port RAMs)
    // ====================================================================
    // Memory depth = MAX_N, supports up to 2048 points
    reg [DATA_WIDTH-1:0] mem_re [0:MAX_N-1];
    reg [DATA_WIDTH-1:0] mem_im [0:MAX_N-1];

    // Write input data to bit-reversed location
    always @(posedge clk) begin
        if (in_valid && !write_done) begin
            mem_re[write_addr] <= in_re;
            mem_im[write_addr] <= in_im;
        end
    end

    // ====================================================================
    // Step 4: Read Phase — Output in natural (linear) order
    // ====================================================================
    reg [10:0] read_counter;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            read_counter <= 11'd0;
            out_valid    <= 1'b0;
            out_re       <= {DATA_WIDTH{1'b0}};
            out_im       <= {DATA_WIDTH{1'b0}};
        end else if (write_done) begin
            // Read N samples sequentially from address 0 to N-1
            if (read_counter < point) begin
                out_re    <= mem_re[read_counter];
                out_im    <= mem_im[read_counter];
                out_valid <= 1'b1;
                read_counter <= read_counter + 1'b1;
            end else begin
                // Frame complete: reset for next FFT
                out_valid <= 1'b0;
                read_counter <= 11'd0;
                write_done   <= 1'b0; // Allow next write phase
            end
        end else begin
            out_valid <= 1'b0;
        end
    end

endmodule