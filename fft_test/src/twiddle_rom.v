// Author: LR
// Description: Parameterized Twiddle Factor ROM for Multi-Point FFT
//              Stores W_N^k = exp(-j*2*pi*k/N) for N up to MAX_N.
//              Initialized from external hex files at synthesis time.
//              Output in Q15 fixed-point format (16-bit signed).

module twiddle_rom #(
    parameter MAX_N      = 2048,   // Maximum FFT size (power of 2)
    parameter DATA_WIDTH = 16      // Must be 16 for Q15
) (
    input                   clk,
    input      [10:0]       addr,  // Address: 0 to MAX_N/2 - 1
    output reg [DATA_WIDTH-1:0] data_re,
    output reg [DATA_WIDTH-1:0] data_im
);

    // Memory depth = MAX_N / 2 (due to symmetry)
    reg [DATA_WIDTH-1:0] rom_re [0:(MAX_N/2)-1];
    reg [DATA_WIDTH-1:0] rom_im [0:(MAX_N/2)-1];

    // Load from hex files (place in project root)
    initial begin
        $readmemh("twiddle_2048_re.hex", rom_re);
        $readmemh("twiddle_2048_im.hex", rom_im);
    end

    // Synchronous read for BRAM inference
    always @(posedge clk) begin
        data_re <= rom_re[addr];
        data_im <= rom_im[addr];
    end

endmodule