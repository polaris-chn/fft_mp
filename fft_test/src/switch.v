// Author: LR
// Create Date: 2025/2/13
// Modified:    2025/4/5
// Description: Complex Data Switch for FFT Pipeline
//              A 2x2 configurable crossbar that either passes through or swaps
//              two complex inputs based on a control signal.
//              Used in radix-2 FFT pipeline stages to implement bit-reversal
//              data routing (e.g., in MDC or SDF architectures).
//              Fully compatible with fft_multipoint.v (supports 8~2048-point FFT).

module switch (
    input                   sel,        // Control: 0 = pass-through, 1 = swap
    input      signed [15:0] x0_re,     // Input complex sample 0 (real part)
    input      signed [15:0] x0_im,     // Input complex sample 0 (imaginary part)
    input      signed [15:0] x1_re,     // Input complex sample 1 (real part)
    input      signed [15:0] x1_im,     // Input complex sample 1 (imaginary part)
    output reg signed [15:0] y0_re,     // Output sample 0 (real)
    output reg signed [15:0] y0_im,     // Output sample 0 (imaginary)
    output reg signed [15:0] y1_re,     // Output sample 1 (real)
    output reg signed [15:0] y1_im      // Output sample 1 (imaginary)
);

    // Combinational logic: no clock, no reset
    // When sel=0: y0 <= x0, y1 <= x1  (no swap)
    // When sel=1: y0 <= x1, y1 <= x0  (swap inputs)
    always @(*) begin
        if (sel) begin
            y0_re = x1_re;
            y0_im = x1_im;
            y1_re = x0_re;
            y1_im = x0_im;
        end else begin
            y0_re = x0_re;
            y0_im = x0_im;
            y1_re = x1_re;
            y1_im = x1_im;
        end
    end

endmodule