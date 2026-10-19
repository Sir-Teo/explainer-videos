"""Published numbers Part 17 quotes, each with its source (checked against the primary document, October 2026).

Scenes import these; nothing here is computed.  "dense" means without 2:4 structured sparsity (vendors often quote
the sparse figure, twice the dense one).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Accelerators: peak dense tensor throughput (FLOP/s), memory (bytes), memory bandwidth (B/s), scale-up link (B/s,
# bidirectional), power (W)
# ---------------------------------------------------------------------------
GPUS = {
    # NVIDIA GeForce GTX 580 (Nov 2010): 512 CUDA cores at 1,544 MHz, 1.5 GB GDDR5 (AlexNet used the 3 GB card),
    # 192.4 GB/s, 244 W, $499 at launch.  FP32 = 2 x 512 x 1.544 GHz.  Epoch AI ML hardware database; TechPowerUp.
    "GTX 580": dict(year=2010, fp32=1.581e12, bw=192.4e9, mem=1.5e9, watts=244, price=499),
    # NVIDIA Tesla P100 SXM2 datasheet: 21.2 TFLOPS FP16, 10.6 FP32, 16 GB HBM2 at 732 GB/s, NVLink 160 GB/s, 300 W
    "P100": dict(year=2016, tensor=21.2e12, fp32=10.6e12, bw=732e9, mem=16e9, link=160e9, watts=300),
    # NVIDIA V100 SXM2 datasheet: 640 tensor cores, 125 TFLOPS tensor, 15.7 FP32, 900 GB/s, NVLink 300 GB/s, 300 W
    "V100": dict(year=2017, tensor=125e12, fp32=15.7e12, bw=900e9, mem=32e9, link=300e9, watts=300),
    # NVIDIA A100 80GB SXM: BF16 312 TFLOPS dense (624 sparse), FP32 19.5, 2,039 GB/s, NVLink 600 GB/s, 400 W
    "A100": dict(year=2020, tensor=312e12, fp32=19.5e12, bw=2.039e12, mem=80e9, link=600e9, watts=400),
    # NVIDIA H100 SXM: BF16 1,979 TFLOPS with sparsity (989 dense), FP8 3,958 sparse (1,979 dense), FP32 67,
    # 80 GB at 3.35 TB/s, NVLink 900 GB/s, up to 700 W
    "H100": dict(year=2022, tensor=989e12, fp8=1979e12, fp32=67e12, bw=3.35e12, mem=80e9, link=900e9, watts=700),
    # NVIDIA GB200 NVL72 page, superchip of 2 GPUs: FP16/BF16 10 PFLOPS sparse, FP8 20 sparse, NVFP4 40 | 20
    # sparse | dense ("dense is one-half sparse"), 372 GB HBM3E at 16 TB/s, NVLink 3.6 TB/s; per GPU, half of that.
    # Power: Epoch AI's database (1,200 W)
    "GB200": dict(year=2024, tensor=2.5e15, fp8=5e15, fp4=10e15, bw=8e12, mem=186e9, link=1.8e12, watts=1200),
    # NVIDIA Vera Rubin NVL72 page (Oct 2026), per Rubin GPU: FP16/BF16 4 PFLOPS dense, FP8 17.5 dense, NVFP4
    # training 35 dense (inference 50, sparse), 288 GB HBM4 at 19.2 TB/s, NVLink 6 3 TB/s
    "Rubin": dict(year=2026, tensor=4e15, fp8=17.5e15, fp4=35e15, bw=19.2e12, mem=288e9, link=3e12),
}

# Racks and pods
NVL72_GB200 = dict(gpus=72, nvlink=130e12, hbm=13.4e12, hbm_bw=576e12)  # GB200 NVL72 page
NVL72_GB300 = dict(gpus=72, nvlink=130e12, hbm=20e12, hbm_bw=576e12)  # GB300 NVL72 page (Blackwell Ultra)
NVL72_RUBIN = dict(gpus=72, nvlink=216e12, hbm=20.7e12, hbm_bw=1400e12, nvfp4_train=2520e15, bf16=288e15,
                   factory_gpus=40_000, factory_mw=100)  # Vera Rubin NVL72 page: "100 MW AI factory: 40K GPUs"
IRONWOOD = dict(year=2025, fp8=4614e12, mem=192e9, bw=7.37e12, ici=1.2e12, pod=9216, pod_eflops=42.5)  # Google, Apr 2025
TPU8T = dict(year=2026, fp4=12.6e15, mem=216e9, sram=128e6, bw=6.528e12, pod=9600, pod_eflops=121)  # Google, Apr 2026
TPU8I = dict(year=2026, fp4=10.1e15, mem=288e9, sram=384e6, bw=8.601e12, pod=1024)  # Google Cloud blog, 22 Apr 2026
TRAINIUM3 = dict(year=2025, fp8=2.517e15, bf16=671e12, mem=144 * 2**30, bw=4.9e12, link=2.56e12)  # AWS Neuron docs
WSE3 = dict(year=2024, transistors=4e12, cores=900_000, sram=44e9, peak=125e15)  # Cerebras, 13 Mar 2024
GROQ3_LPX = dict(year=2026, lpus=256, sram_per_lpu=500e6, sram_bw=40e15, flops=315e15)  # NVIDIA tech blog, 16 Mar 2026
TPU1 = dict(year=2015, macs=256 * 256, mhz=700, tops=92, sram_mib=28, ub_mib=24, ddr_bw=34e9, tdp=75, busy_w=40,
            ridge=1350, ridge_haswell=13, ridge_k80=9)  # Jouppi et al., ISCA 2017

# Interconnect generations, bidirectional per GPU (NVIDIA NVLink page; P100/V100/A100 datasheets)
NVLINK = [(2016, "NVLink 1 (P100)", 160e9), (2017, "NVLink 2 (V100)", 300e9), (2020, "NVLink 3 (A100)", 600e9),
          (2022, "NVLink 4 (H100)", 900e9), (2024, "NVLink 5 (Blackwell)", 1.8e12), (2026, "NVLink 6 (Rubin)", 3e12)]
IB_NDR = 400e9 / 8  # InfiniBand NDR: 400 Gb/s per port, one direction (bytes/s)

# ---------------------------------------------------------------------------
# H100 limits for the occupancy calculator: NVIDIA Hopper tuning guide (compute capability 9.0)
# ---------------------------------------------------------------------------
CC90 = dict(warps=64, blocks=32, regs=65536, max_regs_thread=255, smem=228 * 1024, smem_block=227 * 1024,
            smem_reserved=1024, reg_unit=256, sms=132, l2=50e6)

# Measured latencies on an H800 PCIe (Luo et al. 2024, "Benchmarking and dissecting the Nvidia Hopper GPU
# architecture", Tables III-IV): clock cycles at up to 1,755 MHz; memory 2,039 GB/s
H800_LAT = dict(l1=40.7, shared=29.0, l2=263.0, glob=478.8, mhz=1755, bw=2039e9)

# ---------------------------------------------------------------------------
# Energy per operation, 45 nm (Horowitz, ISSCC 2014, as tabulated by Han et al. 2016, Table I), picojoules
# ---------------------------------------------------------------------------
ENERGY_PJ = [("32-bit int add", 0.1), ("32-bit float add", 0.9), ("32-bit int multiply", 3.1),
             ("32-bit float multiply", 3.7), ("32-bit read, 32 KB SRAM", 5.0), ("32-bit read, DRAM", 640.0)]

# ---------------------------------------------------------------------------
# Training compute (Epoch AI, notable AI models database, accessed Oct 2026)
# ---------------------------------------------------------------------------
ALEXNET_FLOP = 4.7e17  # 1.2M images x 90 epochs x 0.75 GFLOP x 2 x 3 (OpenAI, "AI and Compute", 2018)
ALEXNET_DAYS = (5, 6)  # "between five and six days on two GTX 580 3GB GPUs" (Krizhevsky et al. 2012)
LLAMA31_FLOP = 3.8e25  # Llama 3.1 405B: 16,384 H100s (Meta 2024; Epoch: confident)
LLAMA31_GPUS = 16384
LLAMA31_MW = 22.6  # Epoch's estimate of the training cluster's power draw, megawatts
GPT3_FLOP = 3.14e23  # GPT-3 175B (Brown et al. 2020, Table D.1)
GPT3_CFG = dict(d=12288, layers=96, ctx=2048, params=175e9)  # Brown et al. 2020, Table 2.1

# Trends (Epoch AI, "Trends in machine learning hardware", Hobbhahn, Heim & Aydos, Nov 2023: 47 accelerators)
EPOCH_TRENDS = dict(flops_doubling=2.3, price_perf_doubling=2.1, energy_doubling=3.0, bw_doubling=4.0, mem_doubling=4.0)
MEMORY_WALL = dict(flops=3.0, dram=1.6, interconnect=1.4)  # Gholami et al. 2024: growth per two years, 20 years
AI_AND_COMPUTE = dict(doubling_months=3.4, growth=300_000)  # Amodei & Hernandez, OpenAI 2018 (2012-2018)
IEA = dict(twh_2024=415, share_2024=1.5, twh_2030=945)  # IEA, Energy and AI (April 2025)
