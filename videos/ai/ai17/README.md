# AI, Built — Part 17: Silicon

Part 17 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). Why AI runs on GPUs: the end of Dennard scaling, the GPU from graphics to CUDA,
SIMT and latency hiding, AlexNet, matrix multiplication as the workload, tiling and arithmetic intensity, the memory
hierarchy, the roofline, systolic arrays and tensor cores, number formats from FP32 to FP4, interconnects and the α–β
model of collectives, writing a kernel, the trends in FLOPs, dollars and watts, other accelerators, and the frontier
in late 2026. Wherever it can, the part measures the computer that renders it: its matrix-product speed against size,
its memory bandwidth and latency at every cache level, a cache-blocking speed-up in C, its processes passing messages.
Everything about GPUs and other chips is from vendors' datasheets and papers, cited on screen.

* **Eighty million times the arithmetic.** AlexNet (2012) on two GeForce GTX 580s against Llama 3.1 405B (2024) on
  16,384 H100s: 4.7 × 10¹⁷ against 3.8 × 10²⁵ FLOP (Epoch AI). The same training, at the best matrix-product speed
  measured on this computer: days for AlexNet, millions of years for Llama.
* **1. The power wall.** Moore (1965, 1975); fifty years of microprocessors (K. Rupp's data, CC BY 4.0): transistors
  doubling every 2.0 years (fit); Dennard scaling (1974) derived: P = CV²f, power density constant under scaling by κ;
  why it broke (the 60 mV/decade subthreshold swing, leakage); clock speed doubling every 2.4 years to 2003, flat
  since; single-thread speed's slowdown; cores; Intel's 2004 turn to dual core; Sutter's "The free lunch is over"
  (2005); P ∝ f³ and why parallel wins; Amdahl's law (1967).
* **2. From pixels to GPGPU.** A shader per pixel, 124 million a second at 1080p60; GeForce 256 (1999), programmable
  shaders (2001); CPU and GPU dies compared (this computer's cores and vector width; an H100's 132 SMs × 128 lanes);
  Little's law (1961) for memory: bytes in flight = bandwidth × latency, for an H800 (Luo et al. 2024) and for one
  core of this computer (measured); Brook (Buck et al. 2004), Oh & Jung (2004, 20× on a GPU), CUDA (announced
  November 2006, released 2007), Raina, Madhavan & Ng (2009, up to 70×).
* **3. Warps, divergence and latency.** A CUDA kernel, grids, blocks and warps; SIMT; branch divergence simulated
  (random data against sorted); a warp scheduler hiding a 479-cycle load (simulated, greedy-then-oldest) against
  Little's law; an H100 SM's 4 schedulers and 64 warps; coalesced loads.
* **4. AlexNet: the moment.** ImageNet (Deng et al. 2009); ILSVRC 2012, 15.3% against 26.2% top-5 error; the network
  split across two 3 GB cards; cuda-convnet; the arithmetic (1.2 M × 90 × 0.75 G × 2 × 3 against the published
  4.7 × 10¹⁷), about 31% of two GTX 580s for 5.5 days; cuDNN (2014), DGX-1 (2016), "AI and Compute" (2018, a 3.4-month
  doubling), the hardware lottery (Hooker 2020).
* **5. Matrix multiply is the workload.** GPT-3's forward pass per token: weight matrices, attention's products and
  everything else (computed from its published shape); 6ND = 3.15 × 10²³ against the published 3.14 × 10²³; 2MNK
  derived; arithmetic intensity, naive (¼ FLOP/byte) and best (n/6); tiling animated, b/4 FLOP/byte, 3b² ≤ M;
  Hong & Kung's lower bound (1981); measured in C at n = 1,024: the textbook loop, loops reordered, tiled for tile
  sizes 8 to 512, and BLAS.
* **6. The memory hierarchy.** An H100 zoomed from HBM3 (80 GB, 3.35 TB/s) through the 50 MB L2 to an SM's shared
  memory and registers, with Luo et al.'s measured latencies (41, 263 and 479 cycles); this computer's bandwidth and
  random-read latency for data from 4 KiB to 256 MiB (measured, with the cache sizes it reports); energy per operation
  at 45 nm (Horowitz 2014): a DRAM read costs about 170 floating-point multiplies.
* **7. The roofline.** speed ≤ min(P, βI) derived (Williams, Waterman & Patterson 2009); this computer's single-core
  roofline (STREAM triad, best matrix product), matrix-vector products on the slope, matrix products climbing with n;
  the textbook loop, reordered, tiled and BLAS at the same intensity; four threads (measured, on a shared machine); an
  H100's roofline, its ridge at 295 FLOP/byte (n ≈ 890 in BF16), decoding at about 1 FLOP/byte (0.3% of peak); the
  TPU paper's ridges (1,350; K80 9; Haswell 13).
* **8. Tensor cores and systolic arrays.** Kung & Leiserson (1978), Kung (1982); a 4 × 4 output-stationary array
  computing C = AB cycle by cycle (simulated, checked against numpy); K + 2n − 2 cycles and 2/n reads per operation
  derived; the TPU v1 (Jouppi et al. 2017): 256 × 256 8-bit MACs at 700 MHz, 92 TOPS, deployed 2015, ran AlphaGo;
  padding utilization of a 256 × 256 array (computed); Volta's tensor cores (4 × 4 × 4 per clock, 640 × 64 × 2 ×
  1.53 GHz ≈ 125 TFLOP/s) and their successors.
* **9. Number formats in hardware.** π in FP32, TF32, BF16, FP16, FP8 E4M3 and E5M2, FP4 E2M1 (computed bits); unit
  roundoff 2^−(M+1) and the largest value (448 for E4M3) derived; relative RMS rounding error on 10⁶ Gaussian samples
  against the prediction 2^−M √(ln 2 / 18); block scaling (OCP MX 2023; NVFP4 2025) on real weights; H100 and
  Blackwell throughput by format; this CPU's bfloat16 matrix product, without bfloat16 units (measured); IEEE 754
  (1985), bfloat16 (TPU v2), FP8 (Micikevicius et al. 2022), MX (Rouhani et al. 2023).
* **10. Interconnect and collectives.** Llama 3.1's memory needs; HBM, NVLink and InfiniBand bandwidths; NVLink
  generations (160 GB/s to 3 TB/s); NVL72 (130 TB/s; 216 TB/s for Rubin); switches, fat trees (Leiserson 1985), 3D
  tori (TPU v4, optical switches); T = α + n/β (Hockney 1994) fitted to messages between processes on this computer;
  ring all-reduce animated and derived (Patarasuk & Yuan 2009); ring against tree in the α–β model for 8, 64 and 512
  devices, with the crossover; both timed on this computer's four processes.
* **11. Writing a kernel.** A tiled CUDA matmul with shared memory and `__syncthreads`, T/4 FLOP/byte; occupancy on an
  H100 against registers per thread (NVIDIA's limits, computed); Volkov (2010); Triton (Tillet, Kung & Cox 2019;
  OpenAI 2021), CUTLASS, Pallas, `torch.compile`; FlashAttention (Dao et al. 2022), its HBM traffic Θ(T²d²/M).
* **12. FLOPs, dollars and watts.** Twenty flagship accelerators 2017–2026 (Epoch AI): 16-bit tensor FLOP/s and
  memory bandwidth doubling times (fitted), Epoch's (2.3 and 4 years) and Gholami et al.'s memory wall; the ridge by
  generation and format (V100 to Rubin); FLOP/s per watt; pJ per FLOP, GTX 580 against H100; data centres' electricity
  (IEA 2025: 415 TWh in 2024, about 945 TWh projected for 2030), Llama 3.1's cluster, a 100 MW Rubin "AI factory".
* **13. Beyond the GPU.** TPU v1 to TPU 8t (2015–2026); Trainium3; Cerebras WSE-3 (one chip per wafer, 44 GB of
  SRAM); Groq's LPU, NVIDIA's licence (December 2025) and Groq 3 LPX (2026); analog in-memory computing (IBM, Nature
  2023) and neuromorphic chips (TrueNorth, Loihi, Hala Point).
* **14. The frontier, late 2026.** Blackwell (two dies, 208 billion transistors, FP4), GB200 and GB300 NVL72; Vera
  Rubin NVL72 (288 GB of HBM4 at 19.2 TB/s per GPU, NVLink 6 at 3 TB/s, 100 MW factories); domain sizes from 8 GPUs to
  9,600-chip TPU superpods; prefill and decode on different silicon (Rubin CPX, Groq 3 LPX, TPU 8i).
* **Recap**, where it comes back (Parts 18, 19, 15, 16), the problem set, Part 18's teaser, references.

Run from the repo root:

```
python tools/make.py ai17                           # everything: the computations, then English and Chinese
python -m videos.ai.ai17.compute                    # all the computations, resuming (each item cached when done)
python -m videos.ai.ai17.compute matmul_mt --force  # every core at once: short, best when the machine is idle
python tools/build.py ai17                          # English
python tools/build.py ai17 --lang zh                # Chinese
```

`compute.py` measures the computer it runs on, so the numbers in the video are that computer's, whatever it is: an
Intel or AMD machine on Linux, or a Mac (the processor's name from `sysctl` on macOS, `/proc/cpuinfo` on Linux; cache
sizes from `sysctl` or `/sys`). Each item records the load average it saw; a busy machine measures slower, and its
multi-thread numbers can collapse, which the narration then says. Every measurement runs one thread unless it says
otherwise (numpy's BLAS, whether OpenBLAS, MKL or Apple's Accelerate, is held to one thread). `kernels.c` is compiled
at compute time by `native.py` with `$CC` or the system's `cc` (gcc on Linux, Apple clang on macOS, from the Xcode
command line tools), `-O3 -march=native` (`-mcpu=native` on Apple Silicon) or plain `-O3`; without a compiler the
blocking item runs the same three loop orders in Python with numpy doing the innermost loop, the hierarchy item uses
numpy, and the narration says so. `comm.py` runs the message-passing measurements (four processes, started with
`spawn`); `specs.py` holds every published number, with its source. The formats item rounds the series' own model
(`explainer/ai/novels.py`; `make.py` trains it first) if it exists, else the narrator's Qwen3-TTS weights if they are
in the Hugging Face cache, else Gaussian samples only, and the narration names which. Everything random is seeded.
`data/` holds K. Rupp's microprocessor trend data (CC BY 4.0) and a column subset of Epoch AI's ML hardware database
(CC BY).

References: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed. (2017); Kirk, Hwu & El
Hajj, *Programming Massively Parallel Processors*, 4th ed. (2022); Sze, Chen, Yang & Emer, *Efficient Processing of
Deep Neural Networks* (2020); Moore (1965); Dennard et al. (1974); Amdahl (1967); Little (1961); Sutter (2005);
Esmaeilzadeh et al. (2011); Kung & Leiserson (1978); Kung (1982); Hong & Kung (1981); Buck et al., Brook (2004); Oh &
Jung (2004); Lindholm et al. (2008); Raina, Madhavan & Ng (2009); Deng et al. (2009); Krizhevsky, Sutskever & Hinton
(2012); Chetlur et al., cuDNN (2014); Amodei & Hernandez (2018); Hooker (2020); Brown et al. (2020); Kaplan et al.
(2020); Williams, Waterman & Patterson (2009); Jouppi et al. (2017, 2020, 2023); Horowitz (2014); Han et al., EIE
(2016); Micikevicius et al. (2022); Rouhani et al., Microscaling (2023); NVIDIA, NVFP4 (2025); Hockney (1994); Thakur,
Rabenseifner & Gropp (2005); Patarasuk & Yuan (2009); Leiserson (1985); Volkov (2010); Tillet, Kung & Cox (2019); Dao
et al., FlashAttention (2022); Luo et al. (2024); Hobbhahn, Heim & Aydos, Epoch AI (2023); Gholami et al. (2024); IEA,
*Energy and AI* (2025); Ambrogio et al. (2023); Merolla et al. (2014); NVIDIA H100, A100, V100, P100 datasheets, GB200,
GB300 and Vera Rubin NVL72 pages, NVLink page, Blackwell architecture page, technical blog on Groq 3 LPX (2026); Google
(Ironwood, 2025; TPU 8t and 8i, 2026); AWS Neuron documentation (Trainium3); Cerebras (WSE-3, 2024); Intel (Hala
Point, 2024); K. Rupp, microprocessor trend data; Epoch AI, notable AI models and ML hardware databases.

## Problems, with solutions

**1. Intensity of a matrix product.** For C = AB with A of size m × k and B of size k × n, stored in s-byte numbers,
each matrix moved once, show that I = 2mnk / (s(mk + kn + mn)). What happens when m = 1?

*Solution.* The product does mn dot products of length k, 2mnk operations; it reads mk + kn numbers and writes mn,
s bytes each. With m = 1 (one token at a time), I = 2nk / (s(k + kn + n)) → 2/s as k and n grow: two operations per
weight read, one per byte in 16 bits, half in FP32. That is on the slope of every roofline in this part, whatever the
chip.

**2. How much tiling saves.** Multiply n × n matrices in b × b tiles, with a fast memory of M numbers (3b² ≤ M). Show
that about 2n³/b numbers move, about 2√3 n³/√M.

*Solution.* There are (n/b)² tiles of C, and each takes n/b steps, each loading one b × b tile of A and one of B:
(n/b)³ · 2b² = 2n³/b numbers, plus n² to write C. The largest tiles that fit have b = √(M/3), so the traffic is
2n³√3/√M. Hong and Kung (1981) showed that no order of the operations moves fewer than order n³/√M, so tiling is
optimal up to a constant.

**3. Reaching the roof.** An H100 does 989 TFLOP/s in BF16 (dense) and reads 3.35 TB/s. Which square BF16 products
can reach the roof? Repeat for a Rubin GPU in NVFP4: 35 PFLOP/s (dense), 19.2 TB/s, half a byte per number.

*Solution.* The ridge is 989 × 10¹²/3.35 × 10¹² ≈ 295 FLOP/byte. With each matrix moved once, I = 2n³/(3n² · 2) = n/3,
so n ≥ 886. For Rubin, the ridge is 35 × 10¹⁵/19.2 × 10¹² ≈ 1,823 FLOP/byte, and I = 2n³/(3n² · 0.5) = 4n/3, so
n ≥ 1,368 (ignoring the block scales, which add 1/16 of a byte per number for NVFP4). Smaller products, and every
matrix-vector product, are memory-bound.

**4. Ring against tree.** Derive T_ring = 2(p − 1)α + 2((p − 1)/p)(n/β) and T_tree = 2 log₂p (α + n/β). For p = 8,
where do they cross?

*Solution.* The ring's reduce-scatter takes p − 1 steps; in each, every device sends one chunk of n/p bytes to its
neighbour and adds the one it receives; the all-gather passes the finished chunks around in p − 1 more steps. Each
step costs α + n/(pβ), which gives T_ring. The binomial tree reduces in log₂p steps of whole messages and broadcasts
in log₂p more: T_tree. For p = 8: 14α + 1.75 n/β = 6α + 6 n/β gives n = 8αβ/4.25 ≈ 1.9 αβ. Below that the tree is
faster, above it the ring; the ring's bandwidth term stays below 2n/β however large p is, which is the lower bound
for all-reduce (Patarasuk & Yuan 2009).

**5. Rounding and range.** Show that rounding to nearest in a binary floating-point format with M mantissa bits has
relative error at most 2^−(M+1) for normal numbers, and find the largest finite FP16, E4M3 and E5M2 numbers.

*Solution.* In [2^e, 2^(e+1)) the representable numbers are 2^(e−M) apart; rounding to nearest moves x by at most
half of that, 2^(e−M−1) ≤ 2^−(M+1)|x|. The largest finite number is the largest mantissa times the largest exponent:
FP16 (bias 15, exponent field 30 at most) gives (2 − 2^−10) · 2^15 = 65,504; E5M2 (IEEE-like) gives 1.75 · 2^15 =
57,344; E4M3 (bias 7) keeps only the all-ones pattern for NaN, so exponent field 15 is usable and the largest mantissa
there is 1.75: 1.75 · 2^8 = 448.

**6. Latency to hide.** Memory 3.35 TB/s away by about 273 ns (479 cycles at 1.755 GHz, Luo et al.'s measurement on
an H800), 132 SMs, loads of 128 bytes. How many loads must each SM keep in flight? Can 64 warps, one load each, do it?

*Solution.* By Little's law the bytes in flight are 3.35 × 10¹² × 273 × 10⁻⁹ ≈ 915 KB, about 6.9 KB per SM, or 54
loads of 128 bytes. Sixty-four warps with one load each can cover it, but only near full occupancy and only if every
warp is always waiting on a load; real kernels keep several loads in flight per warp (wider loads, unrolled loops,
asynchronous copies), which is what lets a kernel with fewer warps, but more registers per thread, keep up.

## 习题与解答

**1. 矩阵乘积的算术强度。** 对 C = AB，A 为 m × k，B 为 k × n，每个数占 s 字节，每个矩阵只搬运一次。证明
I = 2mnk / (s(mk + kn + mn))。m = 1 时会怎样？

*解答。* 乘积要做 mn 个长度为 k 的点积，共 2mnk 次运算；读入 mk + kn 个数，写出 mn 个，每个 s 字节。m = 1（一次生成一个
词元）时，I = 2nk / (s(k + kn + n))，当 k、n 增大时趋于 2/s：每读一个权重做两次运算，16位数下每字节一次，FP32 下每字节半次。
不论哪块芯片，这都落在本部分每条屋顶线的斜坡上。

**2. 分块省下多少。** 用 b × b 的块计算 n × n 矩阵乘法，快速存储能放 M 个数（3b² ≤ M）。证明大约要搬运 2n³/b 个数，
也就是约 2√3 n³/√M。

*解答。* C 有 (n/b)² 个块，每块要走 n/b 步，每步读入 A 的一个 b × b 块和 B 的一个：(n/b)³ · 2b² = 2n³/b 个数，再加上写出 C
的 n² 个。能放下的最大的块是 b = √(M/3)，所以搬运量为 2√3 n³/√M。洪加威和孔祥重（1981）证明，任何运算顺序的搬运量都不会
少于 n³/√M 的量级，所以分块在常数倍之内是最优的。

**3. 碰到屋顶。** H100 的 BF16 算力是每秒 989 万亿次（稠密），内存带宽 3.35 TB/s。多大的 BF16 方阵乘积能达到屋顶？再对
Rubin GPU 的 NVFP4 算一次：35 PFLOP/s（稠密），19.2 TB/s，每个数半个字节。

*解答。* 拐点是 989 × 10¹²/3.35 × 10¹² ≈ 295 次运算每字节。每个矩阵只搬运一次时，I = 2n³/(3n² · 2) = n/3，所以 n ≥ 886。
Rubin 的拐点是 35 × 10¹⁵/19.2 × 10¹² ≈ 1823 次运算每字节，I = 2n³/(3n² · 0.5) = 4n/3，所以 n ≥ 1368（忽略分块缩放因子；
NVFP4 的缩放因子每个数再加十六分之一字节）。更小的乘积，以及所有矩阵乘向量，都受内存限制。

**4. 环形与树形。** 推导 T_ring = 2(p − 1)α + 2((p − 1)/p)(n/β) 和 T_tree = 2 log₂p (α + n/β)。p = 8 时，两者在哪里相交？

*解答。* 环形算法的规约-分散阶段有 p − 1 步：每一步每台设备把一块 n/p 字节发给邻居，并把收到的那块加到自己的上面；全收集阶段
再用 p − 1 步把算完的块传一圈。每一步花 α + n/(pβ)，于是得到 T_ring。二叉树用 log₂p 步传整条消息完成规约，再用 log₂p 步
广播：得到 T_tree。p = 8 时，14α + 1.75 n/β = 6α + 6 n/β，得 n = 8αβ/4.25 ≈ 1.9 αβ。比它小，树更快；比它大，环更快。环形的
带宽项无论 p 多大都小于 2n/β，这正是全规约的下界（Patarasuk 和 Yuan，2009）。

**5. 舍入与范围。** 证明：在有 M 个尾数位的二进制浮点格式中，对规格化数就近舍入的相对误差至多为 2^−(M+1)；并求出 FP16、
E4M3 和 E5M2 能表示的最大有限数。

*解答。* 在 [2^e, 2^(e+1)) 中，可表示的数相隔 2^(e−M)；就近舍入最多把 x 移动这个间隔的一半，2^(e−M−1) ≤ 2^−(M+1)|x|。最大
有限数是最大尾数乘以最大指数：FP16（偏置 15，指数字段至多 30）得 (2 − 2^−10) · 2^15 = 65504；E5M2（类似 IEEE）得
1.75 · 2^15 = 57344；E4M3（偏置 7）只把全 1 的那个位模式留作 NaN，所以指数字段 15 可用，那里的最大尾数是 1.75：
1.75 · 2^8 = 448。

**6. 要隐藏的延迟。** 内存带宽 3.35 TB/s，延迟约 273 纳秒（Luo 等人在 H800 上测得：1.755 GHz 下 479 个周期），132 个 SM，每次
读取 128 字节。每个 SM 要同时保持多少个读取在路上？64 个线程束、每个一个读取，够不够？

*解答。* 由利特尔定律，在路上的字节数是 3.35 × 10¹² × 273 × 10⁻⁹ ≈ 915 KB，每个 SM 约 6.9 KB，也就是 54 个 128 字节的读取。
64 个线程束、每个一个读取，刚好能覆盖，但要接近满占用，而且每个线程束都得一直在等一个读取；真实的内核让每个线程束同时有好几个
读取在路上（更宽的读取、展开的循环、异步拷贝），这也是为什么线程束更少、但每个线程寄存器更多的内核，依然能跟得上。

## Glossary (for AI_ZH_GUIDE.md)

| English | 中文 |
|---|---|
| silicon, chip, die, wafer | 硅，芯片，裸片，晶圆 |
| transistor | 晶体管 |
| Moore's law | 摩尔定律 |
| Dennard scaling | 登纳德缩放 |
| the power wall | 功耗墙 |
| clock speed, frequency | 时钟频率 |
| leakage, threshold voltage | 漏电，阈值电压 |
| single-thread performance | 单线程性能 |
| core, multicore | 核心，多核 |
| Amdahl's law | 阿姆达尔定律 |
| GPU (graphics processing unit) | GPU（图形处理器） |
| shader | 着色器 |
| GPGPU (general-purpose computing on GPUs) | GPGPU（GPU通用计算） |
| CUDA, kernel | CUDA，内核（核函数） |
| thread, thread block, grid | 线程，线程块，网格 |
| warp | 线程束 |
| SIMT (single instruction, multiple threads) | SIMT（单指令多线程） |
| streaming multiprocessor (SM) | 流式多处理器（SM） |
| lane | 通道 |
| branch divergence | 分支发散 |
| latency hiding | 延迟隐藏 |
| Little's law | 利特尔定律 |
| bytes in flight | 在途字节 |
| memory coalescing | 访存合并 |
| occupancy | 占用率 |
| register, register file | 寄存器，寄存器堆 |
| shared memory | 共享内存 |
| cache, cache line, L1 / L2 / L3 | 缓存，缓存行，一级/二级/三级缓存 |
| SRAM, DRAM, HBM (high-bandwidth memory) | SRAM，DRAM，HBM（高带宽内存） |
| memory hierarchy | 存储层次 |
| bandwidth, latency | 带宽，延迟 |
| pointer chasing | 指针追逐 |
| prefetcher | 预取器 |
| huge pages, TLB | 大页，TLB（地址转换缓存） |
| matrix multiplication (GEMM), matrix-vector product (GEMV) | 矩阵乘法（GEMM），矩阵乘向量（GEMV） |
| FLOP, FLOP/s | 浮点运算次数，每秒浮点运算次数 |
| arithmetic intensity | 算术强度 |
| tiling, cache blocking, tile | 分块，缓存分块，块（瓦片） |
| BLAS | BLAS（基础线性代数库） |
| the roofline model, ridge point | 屋顶线模型，拐点 |
| compute-bound, memory-bound | 受算力限制，受内存限制 |
| STREAM triad | STREAM三元组测试 |
| systolic array, processing element (PE) | 脉动阵列，处理单元 |
| output-stationary, weight-stationary | 输出驻留，权重驻留 |
| wavefront | 波前 |
| TPU (Tensor Processing Unit) | TPU（张量处理器） |
| tensor core | 张量核心 |
| multiply-accumulate (MAC), fused multiply-add (FMA) | 乘加 |
| floating point: sign, exponent, mantissa, bias | 浮点数：符号位，指数，尾数，偏置 |
| unit roundoff, round to nearest | 单位舍入误差，就近舍入 |
| subnormal, saturate | 次正规数，饱和 |
| FP32, TF32, BF16 (bfloat16), FP16, FP8, FP4 | FP32，TF32，BF16，FP16，FP8，FP4 |
| microscaling (MX), block scale, shared exponent | 微缩放（MX），块缩放因子，共享指数 |
| interconnect, link | 互连，链路 |
| NVLink, NVSwitch, InfiniBand | NVLink，NVSwitch，InfiniBand |
| scale-up, scale-out | 纵向扩展，横向扩展 |
| topology: switch, fat tree, torus | 拓扑：交换机，胖树，环面 |
| optical circuit switch | 光路交换机 |
| collective, all-reduce, reduce-scatter, all-gather, broadcast | 集合通信，全规约，规约-分散，全收集，广播 |
| ring all-reduce, tree all-reduce | 环形全规约，树形全规约 |
| the α–β model (latency–bandwidth) | α–β模型（延迟–带宽模型） |
| Triton, CUTLASS | Triton，CUTLASS |
| FlashAttention, IO-aware | FlashAttention，IO感知 |
| price-performance, energy efficiency | 性价比，能效 |
| the memory wall | 内存墙 |
| data centre, AI factory | 数据中心，AI工厂 |
| rack, pod, superpod | 机柜，集群（pod），超级集群 |
| wafer-scale engine | 晶圆级引擎 |
| LPU | LPU（语言处理单元） |
| through-silicon via (TSV), silicon interposer | 硅通孔，硅中介层 |
| prefill, decode | 预填充，解码 |
| skew (of a systolic array) | （脉动阵列的）错位 |
| inference | 推断 |
| multi-thread, single-thread | 多线程，单线程 |
| load average | 平均负载 |
| analog in-memory computing, phase-change memory | 模拟存内计算，相变存储器 |
| neuromorphic computing, spiking neuron | 类脑计算，脉冲神经元 |
| prefill, decode | 预填充，解码 |
| the hardware lottery | 硬件彩票 |

Names: Gordon Moore → 戈登·摩尔; Robert Dennard → 罗伯特·登纳德; H. T. Kung → 孔祥重; Charles Leiserson → 查尔斯·雷瑟尔森;
Hong Jia-Wei → 洪加威; Ian Buck → 伊恩·巴克; John Nickolls → 约翰·尼科尔斯; Alex Krizhevsky → 亚历克斯·克里热夫斯基; Ilya
Sutskever → 伊利亚·苏茨克维; Geoffrey Hinton → 杰弗里·辛顿; Fei-Fei Li → 李飞飞; Jensen Huang → 黄仁勋; Sara Hooker → 萨拉·胡克;
Samuel Williams, Andrew Waterman, David Patterson → 塞缪尔·威廉斯、安德鲁·沃特曼、大卫·帕特森; Philippe Tillet → 菲利普·蒂莱;
Tri Dao → Tri Dao; Vasily Volkov → 瓦西里·沃尔科夫; Herb Sutter → 赫伯·萨特; Gene Amdahl → 吉恩·阿姆达尔; John Little →
约翰·利特尔; Mark Horowitz → 马克·霍洛维茨; William Kahan → 威廉·卡亨; Jonathan Ross → 乔纳森·罗斯. Products stay in Latin script
(GeForce, CUDA, H100, Blackwell, Rubin, NVLink, TPU, Ironwood, Trainium, Cerebras, Groq, TrueNorth, Loihi, Hala Point).
