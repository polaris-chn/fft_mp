// Author: LR  (updated from brimonzzy)
// Description: N-stage synchronous shift register, WIDTHidth WIDTH
// Note: N must be >= 1

module shiftreg #(
    parameter WIDTH = 16,
    parameter DEPTH = 8  // N >= 1
) (
    input             clk,
    input             rst_n,
    input  [WIDTH-1:0]    d_in,
    output [WIDTH-1:0]    d_out
);

    reg [WIDTH-1:0] shift_reg [0:DEPTH-1]; // clearer indexing

    integer i;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < DEPTH; i = i + 1) begin
                shift_reg[i] <= {WIDTH{1'b0}};
            end
        end else begin
            shift_reg[0] <= d_in;
            for (i = 1; i < DEPTH; i = i + 1) begin
                shift_reg[i] <= shift_reg[i-1];
            end
        end
    end

    assign d_out = shift_reg[DEPTH-1];

endmodule