"""Published numbers Part 19 quotes, each with its source, checked against the primary document on 24 October 2026.

Scenes import these; nothing here is computed.  Chip figures (H100 and the rest) are Part 17's (``videos/ai/ai17/
specs.py``), imported where needed.  Anything derived from these (bytes per token, costs, bounds) is computed in
``compute.py``.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Model configurations (attention and size): what the key-value cache costs
#   layers, query heads, key-value heads, head dim; MLA: compressed dim d_c and decoupled RoPE dim
# ---------------------------------------------------------------------------
LLAMA31_70B = dict(params=70.6e9, layers=80, d=8192, heads=64, kv_heads=8, head_dim=128,
                   src="Llama Team, The Llama 3 Herd of Models (arXiv 2407.21783, 2024), Table 3")
LLAMA31_8B = dict(params=8.03e9, layers=32, d=4096, heads=32, kv_heads=8, head_dim=128,
                  src="Llama Team (2024), Table 3")
DSV3 = dict(total=671e9, active=37e9, layers=61, heads=128, kv_lora_rank=512, rope_dim=64, nope_dim=128, v_dim=128,
            mtp_accept=(85, 90), mtp_tps=1.8, prefill_unit=(4, 32), decode_unit=(40, 320),
            src="DeepSeek-AI, DeepSeek-V3 Technical Report (arXiv 2412.19437, 2024), config.json, Secs. 3.4, 5.4.3")
DSV2 = dict(kv_cut=93.3, throughput=5.76, groups=2.25,
            src="DeepSeek-AI, DeepSeek-V2 (arXiv 2405.04434, 2024), abstract and Table 1")
DSV32 = dict(topk=2048, gpu_hour=2.0, date="2025-12",
             src="DeepSeek-AI, DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models (arXiv 2512.02556, "
                 "2025): DSA selects 2,048 key-value tokens per query; costs at 2 USD per H800 GPU-hour")
GPT_OSS_120B = dict(total=116.83e9, active=5.13e9, mlp=114.71e9, attn=0.96e9, embed=1.16e9, ckpt_gib=60.8, layers=36,
                    heads=64, kv_heads=8, head_dim=64, window=128, experts=128, top_k=4, mxfp4_bits=4.25, fits_gb=80,
                    date="2025-08",
                    src="OpenAI, gpt-oss-120b & gpt-oss-20b Model Card (arXiv 2508.10925, 2025), Table 1, Sec. 2; "
                        "config.json")
GPT_OSS_20B = dict(total=20.91e9, active=3.61e9, mlp=19.12e9, layers=24, experts=32, fits_gb=16, ckpt_gib=12.8,
                   src="OpenAI (2025), Table 1")
GEMMA3 = dict(local=5, glob=1, window=1024, ctx=128_000,
              src="Gemma Team, Gemma 3 Technical Report (arXiv 2503.19786, 2025), Sec. 2")
APPLE_ON_DEVICE = dict(params=3e9, bits=2, emb_bits=4, kv_bits=8, kv_share=37.5, server_bits=3.56,
                       src="Apple, Apple Intelligence Foundation Language Models Tech Report 2025 (arXiv 2507.13575)")

# ---------------------------------------------------------------------------
# Memory bandwidth of the machines a model can run on (bytes a second)
# ---------------------------------------------------------------------------
DEVICES = [  # name, bandwidth, memory, source
    ("Apple M5", 153e9, 32e9, "Apple newsroom, 15 October 2025"),
    ("Apple M5 Max", 614e9, 128e9, "Apple newsroom, 3 March 2026"),
    ("NVIDIA H100", 3.35e12, 80e9, "NVIDIA H100 datasheet (Part 17)"),
]

# ---------------------------------------------------------------------------
# Serving systems
# ---------------------------------------------------------------------------
ORCA = dict(gain=36.9, model="GPT-3 175B",
            src="G.-I. Yu et al., Orca: A Distributed Serving System for Transformer-Based Generative Models (OSDI 2022)")
VLLM = dict(used=(20.4, 38.2), block=16, gain=(2, 4),
            src="W. Kwon et al., Efficient Memory Management for LLM Serving with PagedAttention (SOSP 2023)")
SGLANG = dict(gain=6.4, src="L. Zheng et al., SGLang: Efficient Execution of Structured LM Programs (arXiv 2312.07104)")
SARATHI = dict(gain=(2.6, 3.7), src="A. Agrawal et al., Taming Throughput-Latency Tradeoff in LLM Inference with "
                                    "Sarathi-Serve (OSDI 2024)")
DISTSERVE = dict(requests=7.4, slo=12.6, src="Y. Zhong et al., DistServe (OSDI 2024)")
SPLITWISE = dict(throughput=1.4, cost=20, src="P. Patel et al., Splitwise (ISCA 2024)")
MOONCAKE = dict(requests=75, src="R. Qin et al., Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving "
                                 "(arXiv 2407.00079, 2024)")
POPE = dict(latency_ms=29, mfu=76, model="PaLM 540B", ctx=2048,
            src="R. Pope et al., Efficiently Scaling Transformer Inference (arXiv 2211.05102, 2022)")
RUBIN_CPX = dict(date="2025-09-09", mem=128e9, nvfp4=30e15,
                 src="NVIDIA newsroom, NVIDIA Unveils Rubin CPX (9 September 2025)")

# ---------------------------------------------------------------------------
# Attention
# ---------------------------------------------------------------------------
MQA = dict(year=2019, src="N. Shazeer, Fast Transformer Decoding: One Write-Head is All You Need (arXiv 1911.02150)")
GQA = dict(year=2023, uptrain=5, src="J. Ainslie et al., GQA (arXiv 2305.13245, 2023)")
FLASH1 = dict(year=2022, bert=15, gpt2=3.0, lra=2.4,
              src="T. Dao, D. Y. Fu, S. Ermon, A. Rudra & C. Re, FlashAttention (NeurIPS 2022), Thm. 2, Prop. 3")
FLASH2 = dict(year=2023, gain=2.0, util=(50, 73), src="T. Dao, FlashAttention-2 (arXiv 2307.08691, 2023)")
FLASH3 = dict(year=2024, bf16=740e12, util=75, fp8=1.2e15, fa2_util=35, err=2.6,
              src="J. Shah et al., FlashAttention-3 (arXiv 2407.08608, 2024)")
FLASHDEC = dict(year=2023, gain=8, sms_a100=108,
                src="T. Dao, D. Haziza, F. Massa & G. Sizov, Flash-Decoding for long-context inference (October 2023)")
ONLINE_SOFTMAX = dict(year=2018, src="M. Milakov & N. Gimelshein, Online normalizer calculation for softmax (2018)")
H100_SMEM = 228 * 1024  # bytes of shared memory per SM (Part 17's specs, CC90)
H100_SMS = 132

# ---------------------------------------------------------------------------
# Speculative decoding
# ---------------------------------------------------------------------------
BLOCKWISE = dict(year=2018, iters=2, wall=4,
                 src="M. Stern, N. Shazeer & J. Uszkoreit, Blockwise Parallel Decoding (NeurIPS 2018)")
LEVIATHAN = dict(year=2022, gain=(2, 3), model="T5-XXL",
                 src="Y. Leviathan, M. Kalman & Y. Matias, Fast Inference from Transformers via Speculative Decoding "
                     "(ICML 2023; arXiv November 2022)")
CHEN = dict(year=2023, gain=(2, 2.5), model="Chinchilla 70B",
            src="C. Chen et al., Accelerating LLM Decoding with Speculative Sampling (arXiv 2302.01318, 2023)")
MEDUSA = dict(year=2024, gain1=2.2, gain2=(2.3, 3.6), src="T. Cai et al., Medusa (arXiv 2401.10774, 2024)")
EAGLE = dict(year=2024, gain=(2.7, 3.5), model="LLaMA2-Chat 70B", src="Y. Li et al., EAGLE (ICML 2024)")
EAGLE3 = dict(year=2025, gain=6.5, src="Y. Li et al., EAGLE-3 (arXiv 2503.01840, 2025)")

# ---------------------------------------------------------------------------
# Quantization
# ---------------------------------------------------------------------------
OBD = dict(year=1990, src="Y. LeCun, J. Denker & S. Solla, Optimal Brain Damage (NIPS 1989, published 1990)")
OBS = dict(year=1993, src="B. Hassibi & D. Stork, Second Order Derivatives for Network Pruning: Optimal Brain Surgeon "
                          "(NIPS 1992, published 1993)")
OBQ = dict(year=2022, src="E. Frantar & D. Alistarh, Optimal Brain Compression (NeurIPS 2022)")
LLM_INT8 = dict(year=2022, scale=6.7e9, mag=20, share=0.1, threshold=6.0, int8=99.9,
                src="T. Dettmers et al., LLM.int8() (NeurIPS 2022)")
GPTQ = dict(year=2022, params=175e9, hours=4, bits=(3, 4), a100=3.25,
            src="E. Frantar, S. Ashkboos, T. Hoefler & D. Alistarh, GPTQ (ICLR 2023; arXiv October 2022)")
SMOOTHQUANT = dict(year=2022, speed=1.56, mem=2, alpha=0.5, params=530e9,
                   src="G. Xiao et al., SmoothQuant (ICML 2023; arXiv November 2022)")
AWQ = dict(year=2023, salient=1, src="J. Lin et al., AWQ (MLSys 2024, best paper; arXiv June 2023)")
QUAROT = dict(year=2024, ppl=0.47, kept=99, model="LLaMA2-70B",
              src="S. Ashkboos et al., QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs (NeurIPS 2024)")
SPINQUANT = dict(year=2024, spread=13, gap=2.9, model="LLaMA-2 7B",
                 src="Z. Liu et al., SpinQuant: LLM quantization with learned rotations (ICLR 2025)")
KIVI = dict(year=2024, bits=2, mem=2.6, batch=4, tput=(2.35, 3.47),
            src="Z. Liu et al., KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache (ICML 2024)")
MX = dict(year=2023, block=32, src="B. D. Rouhani et al., Microscaling Data Formats for Deep Learning (arXiv 2310.10537, "
                                   "2023); OCP Microscaling Formats (MX) Specification v1.0 (2023)")
NVFP4 = dict(year=2025, block=16, bits=4.5, vs_fp16=3.5, vs_fp8=1.8, r1_drop=1,
             src="NVIDIA, Introducing NVFP4 for Efficient and Accurate Low-Precision Inference (24 June 2025)")
LLAMA_CPP = dict(date="2023-03-10", src="G. Gerganov, llama.cpp (github.com/ggml-org/llama.cpp, March 2023)")
KIMIK3 = dict(date="2026-07-16", total=2.8e12, active=104e9, src="Moonshot AI, Kimi K3 model card (2026), as in Part 18")

# ---------------------------------------------------------------------------
# Constrained decoding
# ---------------------------------------------------------------------------
OUTLINES = dict(year=2023, src="B. T. Willard & R. Louf, Efficient Guided Generation for Large Language Models "
                               "(arXiv 2307.09702, 2023)")
XGRAMMAR = dict(year=2024, gain=100, src="Y. Dong et al., XGrammar (MLSys 2025; arXiv November 2024)")
GAD = dict(year=2024, src="K. Park et al., Grammar-Aligned Decoding (NeurIPS 2024)")

# ---------------------------------------------------------------------------
# Prices and thinking budgets
# ---------------------------------------------------------------------------
# OpenAI API list prices per million tokens, for a model at least as capable as the original GPT-3 (davinci)
PRICES = [  # (year as a decimal, model, USD per million input tokens, source)
    (2021.0, "GPT-3 davinci", 60.0, "OpenAI API pricing, 2021 (USD 0.06 per 1K tokens)"),
    (2022.67, "davinci, cut", 20.0, "OpenAI, price cut effective 1 September 2022"),
    (2023.17, "gpt-3.5-turbo", 2.0, "OpenAI, Introducing ChatGPT and Whisper APIs (1 March 2023)"),
    (2024.55, "GPT-4o mini", 0.15, "OpenAI, GPT-4o mini (18 July 2024): USD 0.15 in, 0.60 out per million"),
]
EPOCH_PRICES = dict(lo=9, hi=900, gpqa=40, date="2025-03-12",
                    src="B. Cottier et al., LLM inference prices have fallen rapidly but unequally across tasks "
                        "(Epoch AI, 12 March 2025)")
R1_0528 = dict(tokens_old=12_000, tokens_new=23_000, acc_old=70.0, acc_new=87.5, max_len=32_768,
               src="DeepSeek-AI, DeepSeek-R1-0528 model card (May 2025): average tokens per AIME question")
