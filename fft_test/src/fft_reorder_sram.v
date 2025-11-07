// =============================================================================
// Module: fft_reorder_sram_sp
// Description: Parameterizable single-port synchronous SRAM for FFT bit-reversal
//              buffering. Fully synthesizable and technology-independent.
// =============================================================================
// Parameters:
//   ADDR_WIDTH : Width of address bus.
//                Determines memory depth = 2^ADDR_WIDTH words.
//                Example: ADDR_WIDTH=8 → 256-word depth.
//   DATA_WIDTH : Width of data bus (bits per word).
//                Example: DATA_WIDTH=16 → 16-bit words.
//                => Total SRAM size = (2^ADDR_WIDTH) × DATA_WIDTH bits.
// Interface:
//   clk : Clock (posedge active)
//   ce  : Chip enable (high-active)
//   we  : Write enable (high-active; 1=write, 0=read)
//   addr[ADDR_WIDTH-1:0] : Memory address
//   din[DATA_WIDTH-1:0]  : Data input
//   dout[DATA_WIDTH-1:0] : Registered data output (1-cycle read latency)
// =============================================================================

module fft_reorder_sram#(
    parameter ADDR_WIDTH = 8,   // Address width; memory depth = 2^ADDR_WIDTH (e.g., 8 → 256 words)
    parameter DATA_WIDTH = 16   // Data width per word in bits (e.g., 16 → 16-bit words)
) (
    input                    clk,
    input                    ce,
    input                    we,
    input      [ADDR_WIDTH-1:0] addr,
    input      [DATA_WIDTH-1:0] din,
    output reg [DATA_WIDTH-1:0] dout
);

// Total memory size: (2^ADDR_WIDTH) × DATA_WIDTH bits

localparam MEM_DEPTH = 1 << ADDR_WIDTH;

// Declare memory array
reg [DATA_WIDTH-1:0] mem [0 : MEM_DEPTH-1];

// Write operation (synchronous)
always @(posedge clk) begin
    if (ce && we) begin
        mem[addr] <= din;
    end
end

// Read operation (registered output, 1-cycle latency)
always @(posedge clk) begin
    if (ce && !we) begin
        dout <= mem[addr];
    end
    // else: hold previous value — no 'x', safe for synthesis
end

endmodule