# Computer Science, Built — Part 60: Domain-Specific Hardware

Part 60 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act XI, *The Research Frontier*. When Act II's free speedups ended,
the industry's answer was specialization: hardware that does one kind of work and spends almost nothing on organizing
it. We measure this machine's roofline, build H. T. Kung's systolic array out of Part 4's multipliers and simulate it
gate by gate, read the numbers in Google's TPU paper, and end by turning the Job itself into a four-stage circuit that
counts one byte every cycle.

The instruments are in `explainer/cs/hw/` (tested in `tests/test_cs60_hw.py`), built on Part 3's gates, Part 4's
adders and multipliers and Part 5's registers (`explainer/cs/pebble/`):
* `systolic.py`: a multiply-accumulate cell at gate level in two versions (a Dadda tree multiplier with a Kogge–Stone
  adder; an array multiplier with a ripple-carry adder), checked against s + ab; output-stationary and
  weight-stationary N × N grids of those cells, clocked by the HDL simulator, traced cycle by cycle and checked against
  NumPy's exact integer products; an integer model of both dataflows for grids up to 256 × 256, checked against the
  closed forms for cycles and utilization; symmetric per-tensor int8 quantization of a 256 × 256 product and of a
  linear classifier; Horowitz's energy and area per operation beside our multipliers' gate counts and the TPU's
  published figures.
* `roofline.py`: this machine's two roofs, measured on one thread (peak float64 FLOP/s from BLAS matrix products at
  four sizes; bandwidth from STREAM-style copy, add, daxpy and dot on 512 MB arrays, counted as STREAM counts); kernels
  placed under them with intensities from their compulsory traffic: axpy, dot, matrix–vector, matrix products at four
  sizes, a 5-point stencil, Part 52's three BLAS levels, and the Job in Python (four operations a byte, estimated);
  Horowitz's 45 nm table as data.
* `accel.py`: the Job as a netlist of four pipeline stages (classify a byte; hash the word, h ← 33h + code, in two
  Kogge–Stone adders; emit a k-bit index folded from the hash, with the whole hash as a tag; count, by reading a
  direct-mapped table, comparing tags at gate level and incrementing, with an overflow register for words that find
  their slot taken); gates, depth and clock per stage from the series' timing model; gate-level runs in parallel lanes
  checked against the software Job and against a functional model of the table; the thirty novels through that model
  for 1, 4, 16 and 64 lanes and six table sizes; ledger row 21.

## Chapters

* **Hook.** Energy per operation at 45 nm (Horowitz, approximate): an 8-bit add 0.03 pJ, a 32-bit add 0.1, an 8-bit
  multiply 0.2, a 32-bit float multiply 3.7; reading 64 bits from an 8 KB SRAM 10 pJ, from a 1 MB SRAM 100, from DRAM
  1,300–2,600, as much as 90,000 8-bit additions; Hameed et al.'s video encoder (2010), about 500 times less energy as
  a dedicated chip. A 4 × 4 output-stationary grid multiplies two matrices in a diagonal wave in 10 cycles, at gate
  level and checked. The plan: the Job as a circuit, ledger row 21, the thirty novels in about 31 ms.
* **1. The end of general-purpose scaling.** Part 10's trend data: the clock grew 33% a year in 1985–2004 and −0.7% a
  year in 2006–2021. The energy of an instruction against that of its operation: a 10 pJ fetch for a 0.1 pJ add
  leaves a useful share of at most 1%. One instruction driving k operations: 1% for a scalar add, 14% for a 16-wide
  vector add, 99.9% for the 65,536 8-bit multiply-adds of a 256 × 256 grid. Hennessy and Patterson's four reasons for
  domain-specific architecture (Turing lecture, June 2018). The price, Amdahl again: f = 0.9 and s = 50 give 8.5
  times, and no accelerator gives more than 10.
* **2. The roofline model.** T ≥ F/P and T ≥ Q/β, so F/T ≤ min(P, Iβ) with I = F/Q, derived. Intensities from
  compulsory traffic: axpy 0.083 (2 flops for 24 bytes), dot 0.125, matrix–vector 0.25, the stencil 0.25, a matrix
  product n/12, 171 at n = 2,048. This machine on one core: matrix products at 65, 69, 73 and 78 GFLOP/s for n = 256
  to 2,048; on 512 MB arrays copy 27, add 16, daxpy 28 and dot 18 GB/s; the ridge 78/28 ≈ 2.8 flops per byte
  (load average 0.7 when measured). Axpy at 93% of its roof, the stencil at 10% (NumPy's temporaries), matrix products
  at 91–95% of the peak, Part 52's kernels beside them, and the Job in Python about 600 times under its roof. TPU v1's
  ridge, about 2,700.
* **3. A systolic array.** C₀₀ = 70 + 104 + 156 + 15 = 345: N³ = 64 multiply-adds for 4 × 4. One cell: with the tree
  multiplier and Kogge–Stone adder 723 gates (1,923 as NAND gates), depth 29; with the array multiplier and ripple
  carry 461 gates (1,321), depth 61; 40 flip-flops; both checked on 4,096 random inputs. A_ik and B_kj meet in cell
  (i, j) at cycle i + j + k, so a product takes 3N − 2 cycles. The wave cycle by cycle (the corner cell 70, 174, 330,
  345). Grids of 2, 4 and 8 cells a side at gate level: 4, 10 and 22 cycles, 2,892, 11,568 and 46,272 gates (exactly
  N² × 723), 16 random products each, all exact.
* **4. Which number stays put.** Output-, weight- and input-stationary; Eyeriss's row-stationary mix (2016). A
  weight-stationary 4 × 4 grid at gate level with 6 input rows: 4 load cycles and 12 compute cycles. Utilization
  derived: N/(3N − 2) → 1/3 and M/(M + 3N − 2) → 1, checked against the simulations (0.40 and 0.375; 0.50 counting
  only compute cycles). Curves against grid size: weight-stationary with M = N tends to a quarter, with M = 16N stays
  above 80%. At N = 16, 64 and 256 every utilization equals its formula; at 256, 33.4% for one output-stationary
  product against 84.2% for a long weight-stationary stream. Holding weights costs 25 more gates per cell.
* **5. The TPU, and fewer bits.** The first TPU (in Google's data centres from 2015; Jouppi et al. 2017): a 256 × 256
  matrix unit, a 24 MiB unified buffer, 8 GiB of weight DRAM at 34 GB/s, 4 MiB of 32-bit accumulators. 65,536 cells ×
  2 × 700 MHz = 9.18 × 10¹³, the paper's 92 TOPS; its ridge about 2,700 operations per byte. Beside this machine: a
  flat roof about 1,200 times higher, bandwidth 1.2 times; most of the paper's networks were memory-bound; 15–30 times
  faster than a contemporary CPU and GPU on inference. Quantization: s = 1.95/127 = 0.01535, error at most half a
  step. Products below 2¹⁴, 256 of them below 2²²; measured, the largest accumulator was 56,572 (15 bits of headroom),
  and a 64 × 64 slice through chapter 4's model was exact in 254 cycles. Relative error of a 256 × 256 product against
  float64: float32 2.9 × 10⁻⁷, float16 inputs 2.9 × 10⁻⁴, int8 1.5 × 10⁻²; a 10-class classifier 75.54% in float32,
  75.52% in int8, the same answer on 99.6% of 5,000 points. An 8-bit multiply costs 0.2 pJ against 3.7 (about an
  eighteenth) and 420 gates against 3,790 (about a ninth).
* **6. GPUs revisited.** Warps of 32 sharing one instruction; divergence. A tensor core: D = AB + C on 4 × 4
  matrices, 64 multiply-adds per clock, 16-bit products and 32-bit sums (its wiring unpublished; drawn as a sketch).
  Multiply-adds per instruction: 1, 16, 32 and 4,096 (a 16 × 16 × 16 warp step). The V100 (datasheet): 15.7 TFLOP/s on
  its lanes, 125 on tensor cores, 900 GB/s, so the ridge moves from 17 to 139. Tiles: I = b/2 for 16-bit numbers, so
  b ≥ 278 to reach the tensor-core ridge, which is why kernels tile at every level at once.
* **7. Spatial machines: dataflow, CGRAs and FPGAs.** y_i = 3x_i + 2x_{i−1}: 8 instructions per result in time, one
  unit per operation in space. Dataflow firing on tokens: (5 + 3)(7 − 4) = 24 (Dennis and Misunas 1975; Part 8's
  out-of-order core as a hidden dataflow engine). The loop placed and routed on a 3 × 4 CGRA, with one element that
  only passes a value on; then one result per cycle after the pipeline fills (6, 7, 14, 17, 21, 16, 22, 15). A 4-input
  lookup table computing parity, then "at least two set"; the FPGA fabric; Kuon and Rose's gap (2007): around 35
  times the area and several times slower. The spectrum from CPU to ASIC; Catapult (2014), FPGAs to rent (2017),
  Plasticine (2017).
* **8. Computing near memory.** One byte: an 8-bit add 0.03 pJ; from an 8 KB SRAM 1.25 pJ, a 32 KB SRAM 2.5, a 1 MB
  SRAM 12.5, DRAM 162–325, the energy of 5,400–10,800 additions. Wire energy ½CV² with C ∝ length. HBM (a JEDEC
  standard since 2013): 1,024 data wires per stack, millimetres long, against a DDR channel's 64 across the board.
  Processing in memory: summing 2²⁸ four-byte numbers moves 1,073,741,824 bytes over the channel, or 128 bytes of
  partial sums from 16 banks, about 8 million times less (UPMEM; Samsung's HBM-PIM, 2021). An analog crossbar: Ohm
  and Kirchhoff give I = GᵀV in one step, here (7, 5, 3, 4); a few bits of precision.
* **9. Sparsity and approximation.** A pruned row: 16 multiplies, 11 of them by zero, against 5 skipped to the same
  sum (Han et al. 2015 pruned about nine in ten of AlexNet's weights; EIE). Compressed sparse rows: 24 bytes dense
  against 28 compressed for the example; with 8-bit values and 16-bit indices compression wins only below a third
  density. 2:4 structured sparsity (A100, 2020): 32 bits a group become 20, exactly half the multiplies. Stochastic
  rounding derived: E[r(x)] = x, variance at most Δ²/4; 24 quarter-step updates, round to nearest stuck at 0, one
  stochastic run ending at 6 as the exact sum does (Gupta et al. 2015). An approximate 8 × 8 multiplier dropping the 10
  partial products in the four lowest columns: error at most 49, under 0.08% of 255²; chapter 5's classifier, scores
  off by 0.9% and answers changed on 0.4% of points; loop perforation.
* **10. How hardware is designed.** RTL, synthesis, netlist, place and route, tape-out; Chisel (2012) beside this
  series' Python HDL. High-level synthesis of a pipelined dot product: 3 + 255 = 258 cycles for 256 iterations, the
  sum's recurrence the limit. Agile hardware (Lee et al. 2016) against the waterfall. Design-space exploration of
  chapter 3's two cells: periods 360 ps and 680 ps; gates × period 260,280 against 313,480, so the tree does 1.2 times
  the work per gate. Bits as the biggest knob: 420, 807 and 3,790 gates at 8, 11 and 24 bits, about 6.6 n² each;
  G(24)/G(8) = 9.02; depth 19, 23, 32. Co-design: 33h = (h ≪ 5) + h makes the hash stage two adders, 977 gates;
  quantization, 2:4 pruning, bfloat16, FlashAttention.
* **11. The Job in hardware.** Four stages: classify (23 gates, depth 9), hash (977, depth 25), emit (12, depth 1),
  count (749, depth 19); 1,761 gates and 141 flip-flops beside a 4,096 × 57-bit table (1,769 gates with the 2²⁰-entry
  table for the novels). The clock: 1,000 ps for the table read + 19 × 10 + 70 = 1,260 ps, about 794 MHz; the logic
  alone would take 320 ps (3.1 GHz). The opening of *Pride and Prejudice* cycle by cycle ("I" enters, code 9; the first
  count written at cycle 5). Chapter 1 of the novel (4,709 bytes) through 8 lanes at gate level in 598 cycles: every
  hash and every table as the software and the model say, the top twenty exact, 885 counted + 5 lost = 890 words, 4 of
  331 distinct words short. Table size swept from 4,096 to 4,194,304 entries on the thirty novels: lost occurrences
  from 1,185,921 to 2,747, words not counted exactly predicted by m(1 − e^{−n/m}) within a few percent (19,452
  against 19,450 at 2¹⁶; 1,581 against 1,569 at 2²⁰; 407 against 398 at 2²²); at 2²⁰ entries (7.1 MB) 18,362 of
  4,609,954 occurrences lost (0.4%), the top twenty exact from 16,384 entries up. Lanes: 31.46, 8.02, 2.27 and 1.06 ms
  for 1, 4, 16 and 64 (0.8 to 23.5 GB/s), merging costing more than streaming at 64 (453,234 cycles against 390,194),
  lost occurrences down to 3,937. Ledger row 21: about 31 ms at 794 MHz, one cycle a byte against about 29 for Part
  17's hash table on Pebble; the caveats (a byte every cycle, a 7 MB table in 1 ns).
* **12. Frontier: accelerators for language models.** A 2022 datacentre GPU (989 TFLOP/s dense 16-bit, 3.35 TB/s):
  ridge 295 flops per byte; decoding one token is about 1 flop per byte, 0.3% of the peak at batch 1; batches of 1,
  8, 64 and 512 on the roof; remedies (batching, quantized weights, speculative decoding, FlashAttention). Wafer
  scale (Cerebras, 2019), chiplets (AMD's server chips, 2017; UCIe, 2022), stacked memory. Four open problems and the
  ★ research problem (Hong and Kung's red–blue pebble game on a grid of cells).
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs60.compute
python -m unittest tests.test_cs60_hw
python tools/build.py cs60
```

## Problems, with solutions

1. **Tiled intensity.** Derive the arithmetic intensity of an n × n matrix product with b × b tiles in a fast memory
   of 3b² words, and the b that reaches this machine's ridge.

   *Solution.* Keep one b × b tile of C in fast memory, starting at zero. For each of the n/b steps along the inner
   index bring in one b × b tile of A and one of B (2b² words), and add their product, 2b³ flops, into the C tile;
   after the last step write the C tile out (b² words). The three tiles are the 3b² words. Over all (n/b)² tiles of C
   the flops are 2n³ and the words moved are (n/b)²((n/b)·2b² + b²) = 2n³/b + n². With 8-byte words,
   I = 2n³ / (8(2n³/b + n²)) = b / (8 + 4b/n), which is b/8 when b ≪ n; at b = n it is n/12, chapter 2's compulsory
   count, since then each matrix is touched once. Reuse grows linearly with the tile's side. This machine's ridge is
   P/β = 78.4/28.4 ≈ 2.76 flops per byte, so b/8 ≥ 2.76 needs b ≥ 22.1, and at n = 2,048 the correction term raises
   that to 22.2: b = 23, a fast memory of 3 · 23² = 1,587 words, about 12.4 KB. That is the least b that could reach
   the ridge; reaching the flat roof in practice also needs register tiling and a bandwidth as good as the best STREAM
   kernel.

2. **Systolic timing.** Show that an output-stationary N × N grid needs 3N − 2 cycles, and a weight-stationary one
   M + 2N − 2 after loading.

   *Solution.* Number the cycles from 0. Output-stationary: row i of A enters the west edge i cycles late, so A_ik is
   in column 0 at cycle i + k and, moving one cell east per cycle, in column j at i + j + k; column j of B enters the
   north edge j cycles late, so B_kj reaches row i at the same cycle i + j + k. Every product A_ik B_kj is therefore
   formed exactly once, in cell (i, j), at t = i + j + k. The first is at t = 0 and the last, with i = j = k = N − 1,
   at t = 3N − 3, so the product needs the 3N − 2 cycles 0, …, 3N − 3; cell (i, j) is busy for the N cycles from
   i + j. Weight-stationary: during loading one row of W enters the top of each column per cycle, last row first, so
   after N shifts row k of W sits in row k of the grid. Then X_rk enters row k at cycle r + k, moves east one cell per
   cycle, and reaches cell (k, j) at r + k + j, where it is multiplied by W_kj and added to the partial sum from cell
   (k − 1, j), formed there at r + (k − 1) + j and moved one row down: the timings agree, so Y_rj accumulates down
   column j and leaves the bottom row at cycle r + (N − 1) + j. The last output, r = M − 1 and j = N − 1, leaves at
   M + 2N − 3, so the stream needs M + 2N − 2 cycles. Dividing the multiply-adds by cells × cycles gives
   N/(3N − 2) → 1/3 and M/(M + 3N − 2) → 1, and the gate-level runs agree exactly (N = 4: 10 cycles; with M = 6,
   4 + 12).

3. **Accumulator width.** An int8 product of length K sums into 32 bits. How large can K be before the sum can
   overflow?

   *Solution.* A 32-bit two's-complement accumulator holds [−2³¹, 2³¹ − 1]. With chapter 5's symmetric quantization
   the integers lie in [−127, 127], so each product has |q r| ≤ 127² = 16,129 and a sum of K of them has magnitude at
   most 16,129 K. That is at most 2³¹ − 1 = 2,147,483,647 while K ≤ 133,144; at K = 133,145 inputs at the extremes
   can overflow. If −128 is allowed, the largest product is (−128)² = 2¹⁴, and K · 2¹⁴ ≤ 2³¹ − 1 gives
   K ≤ 2¹⁷ − 1 = 131,071 (the most negative product, −128 · 127, allows K ≤ 132,104, so the positive side binds).
   Either way K can be about 2¹⁷, over five hundred times the TPU's 256-long columns; in chapter 5's measured
   256 × 256 product the largest sum was only 56,572, because random terms cancel.

4. **Batch size.** Decoding one token reads every weight once. Find the batch size at which a chip with the roofline
   of chapter twelve becomes compute-bound.

   *Solution.* A model with P parameters in 16-bit weights reads 2P bytes per decoding step, however many sequences
   share the step. With B sequences in the batch each weight read serves B multiply-adds, 2PB flops, so the intensity
   is about B flops per byte. Chapter twelve's chip has ridge 989/3.35 ≈ 295.2 flops per byte, so it becomes
   compute-bound at B ≈ 296; at batch 1 it reaches 3.35/989 ≈ 0.34% of its peak. With 8-bit weights the bytes halve
   and so does the batch needed, to about 148; with 4-bit weights, about 74. The count leaves out attention's reads of
   each sequence's key–value cache: that cache serves only its own sequence, so its intensity stays near 1 whatever
   the batch, and with long contexts it keeps the overall intensity below B, and the break-even batch higher.

5. **Build.** Add linear probing to the word-counting unit, and measure its gates, its clock and the words it no
   longer loses.

   *Solution notes.* Start with the functional model: give `table_model` in `explainer/cs/hw/accel.py` a probe window
   of w slots, i, i + 1, …, i + w − 1 (mod 2^k), in which the first slot holding the word's tag or empty wins and a
   word that finds all w owned by other tags is lost to the overflow register. Run with the unit's own hash on the
   thirty novels, that model at 2²⁰ entries loses 133 distinct words (1,223 occurrences) with w = 2 and 4 words (35
   occurrences) with w = 4, against the direct-mapped 1,581 (18,362); unbounded probing loses none and never needs
   more than 9 probes. At 2¹⁶ entries (88% full) unbounded probing still loses none but needs up to 1,832 probes,
   while w = 4 loses 7,984 words. For one byte a cycle, read the window in parallel: interleave the table over w banks
   by the index's low bits, so that w consecutive slots lie in different banks and are read in the same access; give
   `count_stage` w tag comparators (each 32 XNOR gates and a tree of 31 AND gates, like the one it has), a priority
   encoder picking the first hit or the first empty slot, and w-to-1 multiplexers for the count and the bank; the
   unit's write port then takes a bank as well as an index. Measure the new stage with `timing` (gates from
   `c.size()`, depth from `c.depth()`): the comparators work in parallel, so the period grows only by the encoder and
   the multiplexers, a few gate delays beside the 1 ns table read. The alternative, one probe per cycle with the input
   stalled, keeps the gates down but needs a ready signal the unit does not have, and gives up one byte per cycle in the
   worst case. Check it as the instruments check the present unit: extend `run` so that each lane's table is compared
   with the probing model, keep `accounted` (counted plus lost equals words), make the lanes' merge probe too, and add
   tests beside `test_collisions_reported` in `tests/test_cs60_hw.py`. Words still end at least two cycles apart, so
   a read never sees a stale entry.

6. **★ Research.** The least data movement for a matrix product on a grid of small memories, with a matching
   dataflow.

   *Discussion.* Open in the form asked. Hong and Kung's red–blue pebble game (1981) bounds the words that any
   evaluation of the classical n³ product must move between a fast memory of M words and a slow one, Θ(n³/√M); Irony,
   Toledo and Tiskin (2004) proved the parallel analogue, Ω(n³/(P√M)) words for some one of P processors, and
   Cannon's algorithm on a 2D torus and the 2.5D algorithms of Solomonik and Demmel (2011) meet such bounds up to
   constants. Those models charge a word once, whatever distance it travels. On a systolic grid the cost is a word
   times the hops it makes between neighbours, the inputs enter only at the edges, and when n > N the product must be
   tiled through the grid, so the edge bandwidth and the traffic to memory off the grid count as well. Chapter 3's
   grid, with M = O(1) words a cell, makes Θ(1) hops per multiply-add; a cell holding a √M × √M block of C can bring
   that down to about 1/√M. A good partial answer would fix the model (an N × N mesh, M words a cell, edge input and
   output, cost in word-hops), prove a lower bound on total hops for n = N with the constant, and give a dataflow
   meeting it; then extend to n > N, where it would also have to say whether replicating data, as 2.5D algorithms do,
   pays when distance is charged.

## 习题与解答

1. **分块后的算术强度。** 推导 n × n 矩阵乘法在容量为 3b² 个字的快速存储中使用 b × b 分块时的算术强度，并求出达到本机拐点所需的 b。

   *解答。* 在快速存储中保留 C 的一个 b × b 块，初值为零。沿内层下标走 n/b 步，每步调入 A 的一个 b × b 块和 B 的一个 b × b 块
   （2b² 个字），把它们的乘积（2b³ 次浮点运算）累加进 C 块；最后一步之后把 C 块写回（b² 个字）。这三个块正好是 3b² 个字。对 C 的全部
   (n/b)² 个块，浮点运算共 2n³ 次，搬运的字数为 (n/b)²((n/b)·2b² + b²) = 2n³/b + n²。每字 8 字节时，
   I = 2n³ / (8(2n³/b + n²)) = b / (8 + 4b/n)，b ≪ n 时约为 b/8；b = n 时为 n/12，正是第 2 章按必经流量算出的值，因为此时每个矩阵只碰
   一次。复用随块的边长线性增长。本机的拐点是 P/β = 78.4/28.4 ≈ 2.76 次浮点运算每字节，所以 b/8 ≥ 2.76 要求 b ≥ 22.1；n = 2,048 时
   修正项把它抬到 22.2，于是 b = 23，快速存储为 3 · 23² = 1,587 个字，约 12.4 KB。这只是可能达到拐点的最小 b；实际要贴近平顶，还需要
   寄存器级分块，以及与最好的 STREAM 内核一样高的带宽。

2. **脉动阵列的时序。** 证明输出驻留的 N × N 阵列需要 3N − 2 个周期，权重驻留的阵列在装载之后需要 M + 2N − 2 个周期。

   *解答。* 周期从 0 计起。输出驻留：A 的第 i 行晚 i 个周期从西边进入，所以 A_ik 在周期 i + k 位于第 0 列，每周期向东移一格，在
   i + j + k 到达第 j 列；B 的第 j 列晚 j 个周期从北边进入，所以 B_kj 也在 i + j + k 到达第 i 行。因此每个乘积 A_ik B_kj 恰好形成一次，
   在单元 (i, j)、周期 t = i + j + k。第一个在 t = 0，最后一个（i = j = k = N − 1）在 t = 3N − 3，所以一次乘法需要 0, …, 3N − 3 这
   3N − 2 个周期；单元 (i, j) 从 i + j 起忙 N 个周期。权重驻留：装载时每周期把 W 的一行送入各列顶端，最后一行最先，所以移位 N 次后 W 的
   第 k 行停在阵列的第 k 行。之后 X_rk 在周期 r + k 进入第 k 行，每周期向东一格，在 r + k + j 到达单元 (k, j)，在那里乘以 W_kj，并加上
   从单元 (k − 1, j) 传下来的部分和；那个部分和在 r + (k − 1) + j 形成、再下移一行，时间正好对上，于是 Y_rj 沿第 j 列向下累加，在周期
   r + (N − 1) + j 离开最底行。最后一个输出（r = M − 1，j = N − 1）在 M + 2N − 3 离开，所以输入流需要 M + 2N − 2 个周期。乘加次数除以
   单元数 × 周期数，得到 N/(3N − 2) → 1/3 和 M/(M + 3N − 2) → 1，与门级模拟完全一致（N = 4 时 10 个周期；M = 6 时 4 + 12）。

3. **累加器的宽度。** 长度为 K 的 int8 点积累加到 32 位中。K 最大是多少，和才不可能溢出？

   *解答。* 32 位补码累加器能表示 [−2³¹, 2³¹ − 1]。按第 5 章的对称量化，整数落在 [−127, 127]，所以每个乘积 |q r| ≤ 127² = 16,129，
   K 个乘积之和的绝对值至多 16,129 K。只要 K ≤ 133,144，它就不超过 2³¹ − 1 = 2,147,483,647；K = 133,145 时，取极值的输入就可能溢出。
   若允许 −128，最大乘积为 (−128)² = 2¹⁴，由 K · 2¹⁴ ≤ 2³¹ − 1 得 K ≤ 2¹⁷ − 1 = 131,071（最负的乘积 −128 · 127 允许 K ≤ 132,104，
   所以起约束作用的是正的一侧）。两种情形下 K 都可以到约 2¹⁷，是 TPU 每列 256 项的五百多倍；第 5 章实测的 256 × 256 乘积中最大的和只有
   56,572，因为随机的项会互相抵消。

4. **批大小。** 解码一个词元要把每个权重读一遍。求批大小多大时，具有第十二章屋顶线的芯片转为受算力限制。

   *解答。* 参数量为 P、权重为 16 位的模型，每个解码步读 2P 字节，无论这一步由多少个序列共享。批中有 B 个序列时，每读一个权重就服务
   B 次乘加，共 2PB 次浮点运算，所以算术强度约为每字节 B 次。第十二章的芯片拐点为 989/3.35 ≈ 295.2 次每字节，所以在 B ≈ 296 时转为受
   算力限制；批大小为 1 时只能达到峰值的 3.35/989 ≈ 0.34%。权重为 8 位时字节数减半，所需的批也减半，约 148；4 位时约 74。这个算法没有
   计入注意力对各序列键值缓存的读取：这份缓存只服务它自己的序列，无论批多大，它的算术强度都在 1 左右；上下文很长时，它会把总体强度压到
   B 以下，使所需的批更大。

5. **动手。** 给词频计数单元加上线性探测，并测量它的门数、时钟，以及它不再丢失的词。

   *解答要点。* 先改功能模型：给 `explainer/cs/hw/accel.py` 中的 `table_model` 加一个 w 个槽位的探测窗口 i, i + 1, …, i + w − 1
   （mod 2^k），窗口中第一个存着该词标签或为空的槽位胜出；若 w 个槽位都被别的标签占着，这个词就丢失，记入溢出寄存器。用单元自己的哈希在
   三十部小说上运行，这个模型在 2²⁰ 个表项时，w = 2 丢 133 个不同的词（1,223 次出现），w = 4 丢 4 个词（35 次出现），而直接映射丢 1,581
   个（18,362 次）；不设上限的探测一个也不丢，最多只需 9 次探测。在 2¹⁶ 个表项（88% 已占用）时，不设上限的探测仍然不丢词，但最多要探测
   1,832 次，而 w = 4 丢 7,984 个词。要保持每周期一个字节，就并行地读整个窗口：按下标的低位把表交错分成 w 个存储体，使 w 个相邻槽位落在
   不同的存储体里、在同一次访问中读出；给 `count_stage` 配 w 个标签比较器（每个是 32 个 XNOR 门和一棵 31 个 AND 门的树，与现有的那个
   一样）、一个挑出第一个命中或第一个空槽的优先编码器，以及计数值和存储体的 w 选 1 多路选择器；单元的写端口除了下标还要接收存储体号。
   用 `timing` 测量新的一级（门数取自 `c.size()`，深度取自 `c.depth()`）：比较器并行工作，所以周期只因编码器和多路选择器增加几个门延迟，
   相对 1 ns 的读表时间很小。另一种做法是每周期探测一次、同时让输入停顿：门更少，但需要一个单元现在没有的就绪信号，并且在最坏情况下放弃
   每周期一个字节。照仪器检查现有单元的方式来检查它：扩展 `run`，把每条通道的表与探测模型比较，保持 `accounted`（计入加丢失等于词数），
   让通道之间的合并也做探测，并在 `tests/test_cs60_hw.py` 中 `test_collisions_reported` 旁边加上测试。相邻两个词的结束仍至少相隔两个周期，
   所以读表永远不会读到过时的表项。

6. **★ 研究。** 在由小存储组成的网格上做矩阵乘法所需的最少数据搬运，并给出相匹配的数据流。

   *讨论。* 按题目的提法尚未解决。Hong 与 Kung 的红蓝卵石游戏（1981）给出了：经典 n³ 矩阵乘法的任何计算顺序，在 M 个字的快速存储与慢速
   存储之间必须搬运 Θ(n³/√M) 个字；Irony、Toledo 与 Tiskin（2004）证明了并行版本：P 个处理器中必有一个要通信 Ω(n³/(P√M)) 个字；
   二维环面上的 Cannon 算法和 Solomonik 与 Demmel（2011）的 2.5D 算法在常数因子内达到这类下界。这些模型对一个字只计一次，不管它走多远。
   在脉动网格上，代价是字数乘以它在相邻单元之间走过的跳数，输入只能从边缘进入；n > N 时乘法必须分块穿过网格，于是边缘带宽和网格外存储的
   流量也要计入。第 3 章的网格每个单元 M = O(1) 个字，每次乘加 Θ(1) 跳；单元若保留 C 的一个 √M × √M 块，可以把它降到约 1/√M。好的部分
   结果应当先固定模型（N × N 网格，每单元 M 个字，边缘输入输出，代价按字·跳计），对 n = N 证明一个带常数的总跳数下界，并给出达到它的数据流；
   然后推广到 n > N，那时还要说明：在计入距离的情况下，像 2.5D 算法那样复制数据是否划算。

## Glossary additions

* **domain-specific architecture (DSA), accelerator, ASIC** — hardware built for one kind of work; a chip made for
  one design.
* **energy per operation, data movement** — the cost of an operation against the cost of fetching its operands
  (Horowitz's table).
* **the roofline model, arithmetic intensity, ridge point, compute-bound, memory-bound** — attainable speed
  min(P, Iβ); flops per byte moved; P/β; which roof a kernel sits under.
* **STREAM** — McCalpin's benchmark of sustained memory bandwidth on arrays larger than the caches.
* **systolic array, cell (processing element), wavefront, skew** — a grid of identical cells passing data to their
  neighbours each clock; the diagonal of active cells; the delay that lines the inputs up.
* **multiply-accumulate (MAC)** — s ← s + a · b, the operation of every cell.
* **output-, weight-, input- and row-stationary** — which of the three numbers in a multiply-add stays in the cell.
* **utilization** — multiply-adds done over cells × cycles.
* **TPU, matrix unit, unified buffer, accumulators** — Google's inference accelerator and its parts.
* **quantization, scale, symmetric per-tensor int8, headroom** — a real number as a scale times a small integer;
  the bits an accumulator has to spare.
* **SIMT, warp, divergence** — threads sharing one instruction stream in groups of 32; lanes idling at a branch they
  disagree on.
* **tensor core** — a small matrix multiply-accumulate unit in each GPU multiprocessor.
* **tiling (blocking)** — computing on a block that fits in fast memory so each fetched value is used many times.
* **the memory wall** — arithmetic outgrowing the bandwidth that feeds it.
* **dataflow machine, token, firing rule** — execution ordered by the arrival of operands rather than by a program
  counter.
* **CGRA, placement and routing** — a grid of word-wide configurable elements; assigning operations to elements and
  edges to wires.
* **FPGA, lookup table (LUT), hard blocks** — a fabric of small programmable truth tables, flip-flops, wires,
  multipliers and memories.
* **near-memory and in-memory computing (PIM), HBM, through-silicon via, interposer** — computing beside or inside
  the memory; stacked DRAM joined by vertical wires on a slab of silicon.
* **analog crossbar** — conductances at wire crossings computing a matrix-vector product by Ohm's and Kirchhoff's
  laws.
* **pruning, compressed sparse rows (CSR), 2:4 structured sparsity** — removing weights; storing values, columns
  and row starts; two nonzeros in every group of four.
* **stochastic rounding** — rounding up with probability equal to the fraction, unbiased in expectation.
* **approximate computing, loop perforation** — giving up accuracy on purpose, in circuits or by skipping
  iterations.
* **RTL, synthesis, netlist, place and route, tape-out** — the stages from a hardware description to a chip.
* **hardware generator (Chisel), high-level synthesis (HLS), initiation interval** — programs that produce
  circuits; compiling C to hardware; cycles between iterations of a pipelined loop.
* **agile hardware, design-space exploration, co-design** — iterating on working designs; searching among
  alternatives; choosing algorithm and hardware together.
* **bfloat16** — a 16-bit float with float32's exponent range.
* **direct-mapped table, tag, overflow, lanes** — one slot per index and no probing; the stored hash that identifies
  a word; the count of words lost; copies of the unit working on pieces of the text.
* **decoding, batching, speculative decoding, KV cache** — generating one token per step; sharing each weight read
  across sequences; guessing tokens with a small model and checking them with the large one; stored attention keys
  and values.
* **wafer-scale processor, chiplets, UCIe** — one processor the size of a wafer; several dies in one package; a
  standard for joining them.
* **red–blue pebble game, I/O complexity** — Hong and Kung's model of moving data between fast and slow memory.

## Sources

* J. Hennessy and D. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 7 ("Domain-specific
  architectures"); V. Sze, Y.-H. Chen, T.-J. Yang and J. Emer, *Efficient Processing of Deep Neural Networks*
  (Morgan & Claypool, 2020).
* J. Hennessy and D. Patterson, "A new golden age for computer architecture", Communications of the ACM 62(2), 2019
  (the 2018 Turing lecture).
* H. T. Kung and C. Leiserson, "Systolic arrays (for VLSI)", Sparse Matrix Proceedings 1978 (SIAM, 1979);
  H. T. Kung, "Why systolic architectures?", IEEE Computer 15(1), 1982.
* J.-W. Hong and H. T. Kung, "I/O complexity: the red-blue pebble game", STOC 1981; D. Irony, S. Toledo and
  A. Tiskin, "Communication lower bounds for distributed-memory matrix multiplication", J. Parallel Distrib. Comput.
  64(9), 2004; E. Solomonik and J. Demmel, "Communication-optimal parallel 2.5D matrix multiplication and LU
  factorization algorithms", Euro-Par 2011.
* S. Williams, A. Waterman and D. Patterson, "Roofline: an insightful visual performance model for multicore
  architectures", Communications of the ACM 52(4), 2009; J. McCalpin, "Memory bandwidth and machine balance in
  current high performance computers", IEEE TCCA Newsletter, December 1995.
* M. Horowitz, "Computing's energy problem (and what we can do about it)", ISSCC 2014; R. Hameed et al.,
  "Understanding sources of inefficiency in general-purpose chips", ISCA 2010; K. Rupp, *Microprocessor Trend Data*
  (CC BY 4.0).
* N. Jouppi et al., "In-datacenter performance analysis of a tensor processing unit", ISCA 2017; Y.-H. Chen, J. Emer
  and V. Sze, "Eyeriss: a spatial architecture for energy-efficient dataflow for convolutional neural networks", ISCA
  2016.
* NVIDIA, Tesla V100 datasheet (2017), A100 architecture whitepaper (2020) and H100 datasheet (2022); JEDEC JESD235,
  High Bandwidth Memory (2013).
* J. Dennis and D. Misunas, "A preliminary architecture for a basic data-flow processor", ISCA 1975; I. Kuon and
  J. Rose, "Measuring the gap between FPGAs and ASICs", IEEE Trans. CAD 26(2), 2007; A. Putnam et al., "A
  reconfigurable fabric for accelerating large-scale datacenter services", ISCA 2014; R. Prabhakar et al.,
  "Plasticine: a reconfigurable architecture for parallel patterns", ISCA 2017.
* S. Han, J. Pool, J. Tran and W. Dally, "Learning both weights and connections for efficient neural networks", NIPS
  2015; S. Han et al., "EIE: efficient inference engine on compressed deep neural network", ISCA 2016; S. Gupta,
  A. Agrawal, K. Gopalakrishnan and P. Narayanan, "Deep learning with limited numerical precision", ICML 2015;
  S. Sidiroglou-Douskos, S. Misailovic, H. Hoffmann and M. Rinard, "Managing performance vs. accuracy trade-offs with
  loop perforation", ESEC/FSE 2011.
* J. Bachrach et al., "Chisel: constructing hardware in a Scala embedded language", DAC 2012; Y. Lee et al., "An
  agile approach to building RISC-V microprocessors", IEEE Micro 36(2), 2016.
* T. Dao, D. Fu, S. Ermon, A. Rudra and C. Ré, "FlashAttention: fast and memory-efficient exact attention with
  IO-awareness", NeurIPS 2022.
