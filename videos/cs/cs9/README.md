# Computer Science, Built — Part 9: The Memory Hierarchy

A cache earns its speed by exploiting a program's access history. This chapter builds the mechanisms,
measures a host, and asks which conclusions survive when the model changes. Seventeen scenes connect
address decoding, replacement, locality, data layout and communication bounds to the continuing Pebble Job.
See the [series plan](../README.md) and [syllabus](../SYLLABUS.md).

The visual spine moves from a latency scale and address-time scatter to moving cache lines, reuse-distance
curves, a pointer-chase staircase, matrix traversal, legal red-blue pebble moves and a conditional cost ledger.
English and Chinese narration share bookmark order; a local caption table translates explanatory labels.

## Follow the argument

1. **Hook / memory wall.** A second-per-cycle illustration uses an explicitly illustrative 2.8 GHz clock.
   Host footprint samples remain footprint samples, rather than guaranteed L1/L2/L3/DRAM identifications.
   Historical growth rates illustrate a dated trend; they are not a present-day forecast.
2. **Locality / direct mapping.** Watch the Job's table prefixes and letter addresses, then split an address
   into offset, set and tag. A reuse-distance miss curve assumes fully associative LRU and a specified line size.
3. **Associativity / the three Cs.** Compare LRU, tree PLRU, FIFO, random and offline MIN under matching cache
   rules. A signed set-associative-minus-fully-associative difference can be negative; it is not literally a
   negative number of physical conflict events. Writes require a separate allocation and propagation policy.
4. **AMAT.** Nest conditional miss rates with incremental service costs. Cumulative pointer-chase delays must
   first be differenced, with a nondecreasing envelope, before they can populate this serialized model.
5. **Measured host.** Random dependent loads measure latency-like costs; independent streams measure logical
   GB/s. Allocation advice does not prove that huge pages were used. A bend alone does not establish a cache
   boundary, TLB cause, physical miss count or number of outstanding hardware requests.
6. **Programming.** Compare row and column traversal, loop order, tiling and structs of arrays. C timings and
   a NumPy/BLAS result belong to their stated implementations/settings; the chart does not isolate vector width
   or thread count as a cause. Axes adapt to the cached measurements.
7. **Cache-oblivious algorithms.** Recursive transpose illustrates an ideal-cache argument under its cache and
   tall-cache assumptions. The plotted unit is allocation fills per data reference: 0.125 fills/reference
   equals 0.25 fills/output element because each output entails two references. Dirty writebacks are excluded
   from this particular plot. Balanced static van Emde Boas layout has an O(1 + log_B N) search bound in its model.
8. **Pebbles and matrix movement.** Every demonstrated compute move has red predecessors and enough red slots.
   With the stated place-new rule the tiny graph needs at least three red slots: M=2 is impossible, M=3 needs
   six transfers, and M=4 permits the displayed four-transfer schedule. Independent shortest paths verify this.
   The classical matrix bound requires its stated computation/output assumptions. Its comparison chart counts
   line fills, dirty evictions and the final output drain, reserving eight of 1,024 fast data words for scalars.
9. **External memory.** Scanning, comparison sorting and B-trees use item/block units. The sorting expression
   includes the small-input regime. A merge must reserve output space; fan-in is at most floor(M/B)-1 in the
   simple buffered implementation. Tree height also depends on occupancy and root conventions.
10. **Prefetch / DRAM.** The teaching hierarchy has immediate, uncharged prefetch, no queues or bandwidth limit,
    no coherence/translation, no inclusive back-invalidations and no propagated dirty-write timing. Its dramatic
    speedups are conditional. The DRAM diagram assigns eight banks and 8 KiB rows; it does not measure host banks.
    Activation restores charge, precharge prepares bitlines, and refresh/scheduling/interface details matter.
11. **Job / frontier / recap.** Exact table-prefix LRU counts coexist with a separate sampled cost projection.
    Learned replacement uses offline labels and online predictors with explicit state and generalization limits.
    Hawkeye, Glider, Mockingjay and Streamline illustrate different mechanisms; they are not interchangeable models.

## Reproduce the data and renders

Run from the repository root, using the project environment:

```bash
python -m videos.cs.cs9.compute                  # reuse current items; compute missing or legacy items
python -m videos.cs.cs9.compute scans pebbles job_memory job --force
python -m unittest tests.test_cs9_cache
python tools/build.py cs9 -q l                  # low-resolution build
python tools/build.py cs9                       # native production build
```

Explicit compute commands refresh legacy schemas. Ordinary scene loads reject a legacy scan, movement or
projection payload with a refresh command; reading does not silently rewrite evidence. Computations use
`explainer.paths` and `.cache/cs9/`. Host benchmarks and simulated microbenchmarks can take several minutes.
Changing a producer requires reviewing its downstream items as well as its own JSON. `--force` deliberately
replaces cached measurements, so do not use it during a frozen QA run.

This checkpoint's host reports **AMD EPYC 9V74 80-Core Processor** with no usable measured GHz field.
The 2.8 GHz comparison clock is illustrative; Pebble's approximately 885 MHz clock is a teaching assumption
inherited from its timing model. Host timings vary with scheduling, virtualization, allocation and workload.
Cache inventory reported by the OS does not prove how much capacity this process effectively receives.

## What the Job figures mean

The corpus has 4,609,954 words and 57,895 distinct entries in this cached run. A new word reads only existing
entries, then appends its own slot. The abstract trace includes the length field at byte offset four of each
12-byte entry. It contains one empty scan and **2,818,246,721 table-line visits**, not all loads/stores in the program.
A constant-space cached-prefix state computes exact fully associative LRU counts for this stream. Literal
cache simulations check small cases; an independent corpus calculation checks all nine capacity rows.

The green feasible comparator pins C-1 initial lines and discards a transient line after use. It obeys forced
insertion and upper-bounds MIN's misses; it does not compute exact MIN. For a loop over C+1 lines, MIN's steady
miss fraction is 1/C, not one miss per C+1-reference pass.

A different model samples four corpus windows, coalescing table events and first-letter pool events. The
abstract grown table and letter pool are relocated into disjoint regions. Later matching letters, target reads
and stores are omitted. Synthetic benchmarks on the functional core supply cost increments, and a fit weights
those increments by sampled fractions. It is not a full execution of the unchanged Pebble memory image.

The resulting row-3 projection is about **57.36 s** at the assumed clock, an approximately **0.0645%** increase;
turning off immediate free prefetch gives about **2.67%**. These values have no claimed physical runtime error
bound. They omit bandwidth, queues, prefetch lead time and complete writes. A serialized all-large-set waiting
budget is an illustration, not a measured no-cache run or a universal runtime bound.

## Problems and worked checks

1. **Address fields.** For a 32 KiB, eight-way cache with 64-byte lines and 48-bit byte addresses, find the fields
   and the set of `0x7f3a12345678`.

   There are 512 lines and 64 sets: six offset bits, six index bits and 36 tag bits. The example has offset 56,
   set 25 and tag `0x7f3a12345`.

2. **Serial AMAT.** L1 costs four cycles, with miss rate 0.05. L2 adds 12 cycles, and 0.2 of L2 accesses add a
   further 200 cycles. Compute AMAT and the L1 miss rate that doubles it.

   `4 + 0.05*(12 + 0.2*200) = 6.6` cycles. Doubling requires `m=(13.2-4)/52`, about 17.69%. This concerns the
   modeled average access cost; it does not by itself halve whole-program performance.

3. **A cyclic adversary.** In an initially empty, fully associative C-line cache (C >= 2), access C+1 distinct
   lines cyclically with forced insertion. Compare LRU and MIN, including startup.

   LRU misses every reference. After initially filling C slots, MIN evicts the resident line used farthest in
   the future. With R >= C references, its count is `C + ceil((R-C)/C)`, approaching miss fraction 1/C. A fixed
   pinned-front comparator is feasible but need not achieve this. Compare identical startup and insertion rules.

4. **Complete movement.** For classical n=64 multiplication and M=1,024 fast words, evaluate
   `2*n^3/sqrt(M)-2*M` under the all-output-in-slow-memory assumptions.

   The bound is 14,336 words. Our 127-line LRU plus eight scalar words moves 274,432 words for either untiled
   order, about 19.1 times the bound. T=16 moves 64,000 words, about 4.5 times. These totals include fills,
   dirty evictions and final dirty lines; the old fills-only comparison understated movement. A three-tile
   schedule with 3*T^2 <= M has O(n^3/T + n^2) movement. Tight leading constants require a schedule and storage
   proof; they do not follow merely from the asymptotic big-O expression.

5. **External merge.** Let N=10^10 records, B=10^5 records/block and M=10^9 records of fast storage. Reserve an
   output buffer. How many whole-file read/write passes does simple run generation plus merging need?

   Ten initial runs fit a fan-in of 9,999. One generation pass and one merge pass suffice: approximately
   `2*2*ceil(N/B)=400,000` block transfers, excluding metadata and temporary setup. M counts records, not bytes.

6. **Build and research.** Compare LRU, LIP/BIP and MIN on the scaled prefix trace. Then change the workload's
   phase or entry order. Keep capacities, warmup, insertion and random seeds comparable. Tune on one segment
   and evaluate on heldout segments; a fitted winner on a growing table need not track a changing working set.
   For the full prefix stream, distinguish a feasible upper-bound policy from exact offline MIN. Derive a
   compressed-state algorithm or validate a proposed bound against expanded small traces before scaling up.

## Sources and research scope

Canon: Belady (1966); Denning (1968); Mattson et al. (1970); Bayer and McCreight (1972); Hong and Kung (1981);
Aggarwal and Vitter (1988); Wulf and McKee (1995); Frigo et al., *Cache-Oblivious Algorithms* (1999).
Textbook context: Hennessy and Patterson, *Computer Architecture*; Bryant and O'Hallaron, *CS:APP*;
Jacob, Ng and Wang, *Memory Systems*. Qureshi et al. (ISCA 2007) motivates adaptive insertion.

Primary research checked for the repaired claims:

- [Smith et al., A Tight I/O Lower Bound for Matrix Multiplication](https://arxiv.org/pdf/1702.02017), v2 (2019):
  assumptions and distinct read/total-movement bounds. The chart uses complete output movement.
- [Jain and Lin, Hawkeye](https://www.cs.utexas.edu/~lin/papers/isca16.pdf), ISCA 2016: sampled OPTgen labels and
  online prediction.
- [Shi et al., Glider](https://www.cs.utexas.edu/~lin/papers/micro19c.pdf), MICRO 2019: offline attention-LSTM
  insights inform an online unordered load-PC-history predictor.
- [Shah et al., Mockingjay](https://www.cs.utexas.edu/~lin/papers/hpca22.pdf), HPCA 2022: reuse-distance classes
  and predicted reuse-time ordering.
- [Streamline](https://www.cs.utexas.edu/~lin/papers/hpca26.pdf), HPCA 2026: metadata-efficient temporal prefetching.

The evidence packet records which primary sections were actually read. Sampled preview QA is separate from
continuous listening, Chinese speech/listening, whole-video native production review and a runtime decision at
an approved narration pace. Those production release gates remain open.
