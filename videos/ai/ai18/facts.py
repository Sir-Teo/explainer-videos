"""Published numbers used in Part 18 ("Pretraining at Scale"), each with its source.

Checked against the primary reports (arXiv papers, technical reports, model cards, vendor pages) on 23 October 2026.
Anything derived from these numbers (MFU, MTBF, memory, the cost of a run) is computed in ``compute.py``.
"""

# ---------------------------------------------------------------------------
# Frontier runs
# ---------------------------------------------------------------------------
LLAMA3 = dict(
    params=405e9, tokens=15.6e12, flops=3.8e25, gpus=16384, gpu="H100", peak_bf16=989e12,
    # Table 4: GPUs, TP, CP, PP, DP, sequence, batch per DP group, tokens per batch, TFLOP/s per GPU, MFU (%)
    table4=[(8192, 8, 1, 16, 64, 8192, 32, 16e6, 430, 43), (16384, 8, 1, 16, 128, 8192, 16, 16e6, 400, 41),
            (16384, 8, 16, 16, 8, 131072, 16, 16e6, 380, 38)],
    order=("TP", "CP", "PP", "DP"),
    days=54, interruptions=466, planned=47, unexpected=419, hardware_share=78, manual=3, effective=90,
    # Table 5: the largest root causes of the 419 unexpected interruptions (counts)
    causes=[("faulty GPU", 148), ("GPU HBM3 memory", 72), ("software bug", 54), ("network switch or cable", 35),
            ("host maintenance", 32)],
    ckpt_per_gpu=(1e6, 4e9), tectonic_bw=2e12, tectonic_peak=7e12, diurnal=(1, 2),
    batch_schedule=[(0, 4e6, 4096), (252e6, 8e6, 8192), (2.87e12, 16e6, 8192)], lr=8e-5,
    anneal_tokens=40e6, long_stages=6, long_tokens=800e9, ctx=(8192, 131072),
    src="Llama Team, The Llama 3 Herd of Models (arXiv 2407.21783, 2024), Secs. 3.3-3.4, Tables 4-5")

DSV3 = dict(
    total=671e9, active=37e9, tokens=14.8e12, gpus=2048, gpu="H800",
    hours_pre=2.664e6, hours_ctx=0.119e6, hours_post=0.005e6, hours=2.788e6, rate=2.0,
    hours_per_T=180e3, days_per_T=3.7,
    nvlink=160e9, ib=50e9, comm_sms=20, sms=132,
    tile_act=128, block_w=128, nc=128, accum_bits=14, accum_err=2.0, loss_err=0.25,
    pp=16, ep=64, nodes=8, max_nodes=4,
    mtp_depth=1, mtp_lambda=(0.3, 0.1), mtp_switch=10e12, mtp_accept=(85, 90), mtp_tps=1.8,
    lr_peak=2.2e-4, lr_end=2.2e-5, lr_tail=(2.2e-5, 333e9, 7.3e-6, 167e9), lr_const_until=10e12, lr_decay_tokens=4.3e12,
    warmup_steps=2000, batch=(3072, 15360), batch_ramp=469e9, seq=4096,
    fim=0.1, yarn=[(4096, 32768, 1000), (32768, 131072, 1000)],
    src="DeepSeek-AI, DeepSeek-V3 Technical Report (arXiv 2412.19437, 2024)")

DSV4 = dict(
    date="2026-04-24", pro=(1.6e12, 49e9, 33e12, 94.4e6), flash=(284e9, 13e9, 32e12, 75.5e6),
    ns_iters=10, ns_coeffs=[(3.4445, -4.7750, 2.0315), (2.0, -1.5, 0.5)], rms=0.18, mtp_lambda=(0.3, 0.1),
    seq=(4096, 16384, 65536, 1048576), routing_overhead=20,
    src="DeepSeek-AI, DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence (arXiv 2606.19348, "
        "2026), Secs. 2.4, 4.2")

KIMIK2 = dict(total=1.04e12, active=32e9, tokens=15.5e12, tau=100, heads_clipped=12.7, clip_steps=70000,
              rephrase=[("raw text, 10 epochs", 23.76), ("rephrased once, 10 epochs", 27.39),
                        ("rephrased 10 times, 1 epoch", 28.94)],
              src="Kimi Team, Kimi K2: Open Agentic Intelligence (arXiv 2507.20534, 2025), Secs. 2.1-2.2, Table 1")
MOONLIGHT = dict(efficiency=2.0, tokens=5.7e12, src="Liu et al., Muon is Scalable for LLM Training (arXiv 2502.16982, 2025)")
GLM45 = dict(tokens=23e12, ctx=(4096, 32768, 131072), muon_rms=0.2,
             src="GLM-4.5 Team, GLM-4.5 (arXiv 2508.06471, 2025), Sec. 2")
QWEN3 = dict(s1=30e12, s2=5e12, seq=4096, s3_seq=32768, rope=(10_000, 1_000_000), languages=119,
             src="Qwen Team, Qwen3 Technical Report (arXiv 2505.09388, 2025), Sec. 3.2")
OLMO3 = dict(pre=5.9e12, mid=100e9, long=(50e9, 100e9), ctx=65536, gpus=1024, mfu=(43, 41), tps=(7700, 1960),
             exact=67, fuzzy=23, substring=14, docs=(38.7e9, 12.8e9, 9.8e9, 9.7e9),
             src="Team OLMo, Olmo 3 (arXiv 2512.13961, 2025), Secs. 3.4-3.6, 4")
OLMO2 = dict(mid_share=(5, 10), microanneals=19, microanneal_tokens=130e9,
             src="Team OLMo, 2 OLMo 2 Furious (arXiv 2501.00656, 2025), Secs. 2.1, 4")
SMOLLM3 = dict(params=3e9, tokens=11.2e12, gpus=384, days=24,
               stages=[(0, 8e12, 85, 12, 3), (8e12, 10e12, 75, 15, 10), (10e12, 11.1e12, 63, 24, 13)],
               long=[(4096, 32768, 1.5e6), (32768, 65536, 5e6)], decay=10,
               src="Hugging Face, SmolLM3: smol, multilingual, long-context reasoner (blog, 8 July 2025)")
LLAMA4 = dict(gpus=32000, tflops=390, tokens=30e12, src="Meta AI, The Llama 4 herd (blog, 5 April 2025)")
NEMOTRON3 = dict(total=120e9, active=12e9, tokens=25e12, phases=(20e12, 5e12),
                 src="NVIDIA, Nemotron 3 Super technical report (March 2026)")
NVFP4 = dict(params=12e9, tokens=10e12, mmlu_pro=(62.58, 62.62), bf16_share=16, block=16,
             src="NVIDIA, Pretraining Large Language Models with NVFP4 (arXiv 2509.25149, 2025)")
MXFP8 = dict(params=8e9, tokens=15e12, block=32, src="Mishra et al., Recipes for Pre-training LLMs with MXFP8 (arXiv 2506.08027, 2025)")
KIMIK3 = dict(date="2026-07-16", total=2.8e12, active=104e9, quant="MXFP4 weights, MXFP8 activations (QAT)",
              src="Moonshot AI, Kimi K3 model card (2026)")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
FINEWEB = dict(tokens=15e12, snapshots=96, lid=0.65, shingle=5, hashes=112, bands=14, rows=8, target=0.75,
               global_tokens=4e12, per_snapshot_tokens=20e12, kept_share=10,
               src="Penedo et al., The FineWeb Datasets (arXiv 2406.17557, 2024), Secs. 3.2-3.4, App. E")
FINEWEB_EDU = dict(annotated=460_000, train=410_000, valid=50_000, threshold=3, f1=82, tokens=1.3e12,
                   gpu_hours=6000, model=1.71e9, ablation_tokens=350e9, mmlu=(33, 37), arc=(46, 57),
                   annotator="Llama-3-70B-Instruct", embedder="Snowflake-arctic-embed-m",
                   src="Penedo et al. (2024), Sec. 4")
DCLM = dict(pool=240e12, baseline=3.8e12, params=7e9, tokens=2.6e12, mmlu=64, lift=3.5,
            src="Li et al., DataComp-LM (arXiv 2406.11794, 2024)")
DOREMI = dict(proxy=280e6, target=8e9, gain=6.5, speedup=2.6,
              src="Xie et al., DoReMi (arXiv 2305.10429, NeurIPS 2023)")
REGMIX = dict(models=512, params=1e6, tokens=1e9, big=1e9, big_tokens=25e9, candidates=64, compute_share=10,
              src="Liu et al., RegMix (arXiv 2407.01492, ICLR 2025)")
WRAP = dict(speedup=3, ppl=10, src="Maini et al., Rephrasing the Web (arXiv 2401.16380, ACL 2024)")
COLLAPSE = dict(src="Shumailov et al., AI models collapse when trained on recursively generated data (Nature 631, 2024)")
ACCUMULATE = dict(src="Gerstgrasser et al., Is Model Collapse Inevitable? (arXiv 2404.01413, 2024)")
REPEAT = dict(epochs=4, src="Muennighoff et al., Scaling Data-Constrained Language Models (NeurIPS 2023)")
GPT3_CONTAM = dict(ngram=13, src="Brown et al., Language Models are Few-Shot Learners (2020), App. C")

# ---------------------------------------------------------------------------
# Objectives, schedules
# ---------------------------------------------------------------------------
FIM = dict(rate=0.5, src="Bavarian et al., Efficient Training of Language Models to Fill in the Middle (arXiv 2207.14255, 2022)")
T5 = dict(noise=0.15, span=3, src="Raffel et al., T5 (JMLR 2020)")
BERT = dict(mask=0.15, split=(80, 10, 10), src="Devlin et al., BERT (2019)")
WSD = dict(src="Hu et al., MiniCPM (arXiv 2404.06395, 2024); Hägele et al. (arXiv 2405.18392, 2024)")

# ---------------------------------------------------------------------------
# Systems
# ---------------------------------------------------------------------------
ZERO = dict(psi=7.5e9, nd=64, k=12, mem=(120, 31.4, 16.6, 1.9), comm=(2, 2, 3),
            src="Rajbhandari et al., ZeRO (arXiv 1910.02054, SC 2020), Fig. 1, Secs. 5, 7")
MEGATRON = dict(params=8.3e9, gpus=512, pflops=15.1, scaling=76, tp=8,
                src="Shoeybi et al., Megatron-LM (arXiv 1909.08053, 2019)")
MEGATRON2 = dict(params=1e12, gpus=3072, pflops=502, peak=52,
                 src="Narayanan et al., Efficient Large-Scale Language Model Training on GPU Clusters (SC 2021)")
KORTHIKANTI = dict(src="Korthikanti et al., Reducing Activation Recomputation in Large Transformer Models (2022)")
GPIPE = dict(rule=4, src="Huang et al., GPipe (NeurIPS 2019)")
ZB = dict(gain=(23, 31), src="Qi et al., Zero Bubble Pipeline Parallelism (ICLR 2024)")
PALM = dict(params=540e9, chips=6144, mfu=46.2, mfu_noattn=45.7, tps=238.3e3, peak=275e12, spikes=20,
            back=100, skip=(200, 500), zloss=1e-4, src="Chowdhery et al., PaLM (arXiv 2204.02311, 2022)")
MEGASCALE = dict(params=175e9, gpus=12288, mfu=55.2, src="Jiang et al., MegaScale (NSDI 2024)")
WORTSMAN = dict(zloss=1e-4, src="Wortsman et al., Small-scale proxies for large-scale Transformer training "
                                "instabilities (ICLR 2024)")
PATARASUK = dict(src="Patarasuk \\& Yuan, Bandwidth optimal all-reduce algorithms for clusters of workstations "
                     "(JPDC 2009)")
YOUNG = dict(src="Young, A first order approximation to the optimum checkpoint interval (CACM 1974)")
MIXED = dict(src="Micikevicius et al., Mixed Precision Training (ICLR 2018)")
FP8 = dict(src="Micikevicius et al., FP8 Formats for Deep Learning (2022)")
MTP = dict(params=13e9, humaneval=12, mbpp=17, speed=3,
           src="Gloeckle et al., Better & Faster Large Language Models via Multi-token Prediction (ICML 2024)")
FSDP = dict(src="Zhao et al., PyTorch FSDP (VLDB 2023)")
RING_ATTN = dict(src="Liu, Zaharia \\& Abbeel, Ring Attention (2023)")

# Formats: (exponent bits, mantissa bits, largest finite, smallest normal, smallest subnormal)
FORMATS = {
    "FP32": (8, 23, 3.4028235e38, 2.0 ** -126, 2.0 ** -149),
    "BF16": (8, 7, 3.3895314e38, 2.0 ** -126, 2.0 ** -133),
    "FP16": (5, 10, 65504.0, 2.0 ** -14, 2.0 ** -24),
    "E4M3": (4, 3, 448.0, 2.0 ** -6, 2.0 ** -9),
    "E5M2": (5, 2, 57344.0, 2.0 ** -14, 2.0 ** -16),
}
