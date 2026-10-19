"""Published facts for Part 14 ("The Language-Model Lineage"), each with its source.

Every published number the scenes show lives here, with the paper, technical report or model card it comes from
(checked against the primary source on 19 October 2026; see the README's fact-check notes).  ``compute.py`` derives
everything else from these (parameter counts from configurations, 6ND, tokens per parameter, cache sizes, growth
rates), and asserts that the derivations agree with what the papers report.

Dates are those of first public release (arXiv v1, or the announcement); the scenes show month and year.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Configurations, year by year.  None = not published (or not applicable).
#   arch: "encdec" | "encoder" | "decoder";  norm: post-LN, pre-LN, pre-RMS;  act: activation of the MLP;
#   pos: position encoding;  attn: attention variant;  bias: biases in the linear layers.
# ---------------------------------------------------------------------------
CONFIGS = [
    dict(key="transformer", name="Transformer (big)", org="Google", date="2017-06-12", arch="encdec",
         layers=12, layers_note="6 + 6", d=1024, heads=16, kv_heads=16, d_ff=4096, ctx=None, vocab=37000,
         params=213e6, active=None, tokens=None, norm="post-LN", act="ReLU", pos="sinusoidal", attn="MHA",
         bias=True, src="Vaswani et al., Attention Is All You Need (2017), Table 3"),
    dict(key="gpt1", name="GPT-1", org="OpenAI", date="2018-06-11", arch="decoder", layers=12, d=768, heads=12,
         kv_heads=12, d_ff=3072, ctx=512, vocab=40478, params=117e6, active=None, tokens=None, norm="post-LN",
         act="GELU", pos="learned", attn="MHA", bias=True,
         src="Radford et al., Improving Language Understanding by Generative Pre-Training (2018), Sec. 4.1"),
    dict(key="bert", name="BERT-Large", org="Google", date="2018-10-11", arch="encoder", layers=24, d=1024,
         heads=16, kv_heads=16, d_ff=4096, ctx=512, vocab=30522, params=340e6, active=None, tokens=None,
         norm="post-LN", act="GELU", pos="learned", attn="MHA", bias=True,
         src="Devlin et al., BERT (2018), Sec. 3; released configuration"),
    dict(key="gpt2", name="GPT-2", org="OpenAI", date="2019-02-14", arch="decoder", layers=48, d=1600, heads=25,
         kv_heads=25, d_ff=6400, ctx=1024, vocab=50257, params=1.5e9, active=None, tokens=None, norm="pre-LN",
         act="GELU", pos="learned", attn="MHA", bias=True,
         src="Radford et al., Language Models are Unsupervised Multitask Learners (2019), Table 2; released "
             "configuration (25 heads)"),
    dict(key="t5", name="T5-11B", org="Google", date="2019-10-23", arch="encdec", layers=48, layers_note="24 + 24",
         d=1024, heads=128, kv_heads=128, d_ff=65536, ctx=512, vocab=32000, params=11e9, active=None, tokens=1e12,
         norm="pre-RMS", act="ReLU", pos="relative", attn="MHA", bias=None,
         src="Raffel et al., T5 (2019), Secs. 3.1, 3.7; GPT-3 paper Table D.1 (tokens)"),
    dict(key="gpt3", name="GPT-3", org="OpenAI", date="2020-05-28", arch="decoder", layers=96, d=12288, heads=96,
         kv_heads=96, d_ff=49152, ctx=2048, vocab=50257, params=174.6e9, active=None, tokens=300e9,
         norm="pre-LN", act="GELU", pos="learned", attn="dense + sparse", bias=True,
         src="Brown et al., Language Models are Few-Shot Learners (2020), Table 2.1, Table D.1"),
    dict(key="palm", name="PaLM", org="Google", date="2022-04-04", arch="decoder", layers=118, d=18432, heads=48,
         kv_heads=1, d_ff=None, ctx=2048, vocab=256000, params=540.35e9, active=None, tokens=780e9,
         norm="pre-LN", act="SwiGLU", pos="RoPE", attn="MQA", bias=False,
         src="Chowdhery et al., PaLM (2022), Sec. 2, Table 1"),
    dict(key="llama", name="LLaMA-65B", org="Meta", date="2023-02-24", arch="decoder", layers=80, d=8192,
         heads=64, kv_heads=64, d_ff=22016, ctx=2048, vocab=32000, params=65.2e9, active=None, tokens=1.4e12,
         norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="MHA", bias=False,
         src="Touvron et al., LLaMA (2023), Table 2, Sec. 2.2"),
    dict(key="llama2", name="Llama 2 70B", org="Meta", date="2023-07-18", arch="decoder", layers=80, d=8192,
         heads=64, kv_heads=8, d_ff=28672, ctx=4096, vocab=32000, params=70e9, active=None, tokens=2e12,
         norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA", bias=False,
         src="Touvron et al., Llama 2 (2023), Table 1"),
    dict(key="mistral", name="Mistral 7B", org="Mistral AI", date="2023-09-27", arch="decoder", layers=32,
         d=4096, heads=32, kv_heads=8, d_ff=14336, ctx=8192, vocab=32000, params=7.3e9, active=None, tokens=None,
         norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA + window", bias=False,
         src="Jiang et al., Mistral 7B (2023), Table 1"),
    dict(key="llama3", name="Llama 3.1 405B", org="Meta", date="2024-07-23", arch="decoder", layers=126,
         d=16384, heads=128, kv_heads=8, d_ff=53248, ctx=131072, vocab=128256, params=405e9, active=None,
         tokens=15.6e12, norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA", bias=False,
         src="Llama Team, The Llama 3 Herd of Models (2024), Table 3, Sec. 3"),
    dict(key="dsv3", name="DeepSeek-V3", org="DeepSeek", date="2024-12-26", arch="decoder", layers=61, d=7168,
         heads=128, kv_heads=None, d_ff=2048, ctx=131072, vocab=129280, params=671e9, active=37e9,
         tokens=14.8e12, norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="MLA", bias=False, experts=256,
         active_experts=8, shared_experts=1,
         src="DeepSeek-AI, DeepSeek-V3 Technical Report (2024), Secs. 2, 4.2"),
    dict(key="qwen3", name="Qwen3-235B-A22B", org="Alibaba", date="2025-04-29", arch="decoder", layers=94,
         d=4096, heads=64, kv_heads=4, d_ff=1536, ctx=131072, vocab=151669, params=235e9, active=22e9,
         tokens=36e12, norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA + QK-norm", bias=False, experts=128,
         active_experts=8, shared_experts=0, src="Qwen Team, Qwen3 Technical Report (2025), Tables 1-2"),
    dict(key="kimik2", name="Kimi K2", org="Moonshot AI", date="2025-07-11", arch="decoder", layers=61, d=7168,
         heads=64, kv_heads=None, d_ff=2048, ctx=131072, vocab=163840, params=1.04e12, active=32.6e9,
         tokens=15.5e12, norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="MLA", bias=False, experts=384,
         active_experts=8, shared_experts=1, src="Kimi Team, Kimi K2 (2025), Table 2"),
    dict(key="glm45", name="GLM-4.5", org="Zhipu AI", date="2025-07-28", arch="decoder", layers=92, d=5120,
         heads=96, kv_heads=8, d_ff=1536, ctx=131072, vocab=None, params=355e9, active=32e9, tokens=23e12,
         norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA + QK-norm", bias=False, experts=160,
         active_experts=8, shared_experts=1, src="GLM-4.5 Team, GLM-4.5 (2025), Table 1"),
    dict(key="gptoss", name="gpt-oss-120b", org="OpenAI", date="2025-08-05", arch="decoder", layers=36, d=2880,
         heads=64, kv_heads=8, d_ff=2880, ctx=131072, vocab=201088, params=116.8e9, active=5.1e9, tokens=None,
         norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="GQA + window + sinks", bias=None, experts=128,
         active_experts=4, shared_experts=0, src="OpenAI, gpt-oss-120b & gpt-oss-20b Model Card (2025), Sec. 2"),
    dict(key="qwen35", name="Qwen3.5-397B-A17B", org="Alibaba", date="2026-02-16", arch="decoder", layers=60,
         d=4096, heads=32, kv_heads=2, d_ff=1024, ctx=262144, vocab=248320, params=397e9, active=17e9,
         tokens=None, norm="pre-RMS", act="SwiGLU", pos="RoPE", attn="hybrid: DeltaNet 3 : 1", bias=False,
         experts=512, active_experts=10, shared_experts=1, src="Qwen, Qwen3.5-397B-A17B model card (2026)"),
    dict(key="dsv4", name="DeepSeek-V4-Pro", org="DeepSeek", date="2026-04-24", arch="decoder", layers=None,
         d=None, heads=None, kv_heads=None, d_ff=None, ctx=1048576, vocab=None, params=1.6e12, active=49e9,
         tokens=32e12, tokens_note="more than", norm=None, act=None, pos=None, attn="compressed sparse",
         bias=None, src="DeepSeek-AI, DeepSeek-V4 model card (preview, 2026)"),
    dict(key="kimik3", name="Kimi K3", org="Moonshot AI", date="2026-07-16", arch="decoder", layers=93, d=7168,
         heads=96, kv_heads=None, d_ff=3072, ctx=1048576, vocab=160000, params=2.8e12, active=104e9, tokens=None,
         norm=None, act="SiTU-GLU", pos=None, attn="hybrid: KDA 69 + MLA 24", bias=None, experts=896,
         active_experts=16, shared_experts=2, src="Moonshot AI, Kimi K3 model card (2026), Sec. 2"),
]
CFG = {c["key"]: c for c in CONFIGS}

# the "convergence" columns of chapter 10, in the order they are switched on
RECIPE = [
    ("norm", "pre-RMS", r"pre-norm RMSNorm"),
    ("act", "SwiGLU", r"SwiGLU"),
    ("pos", "RoPE", r"RoPE"),
    ("attn", "GQA", r"grouped-query attention"),
    ("bias", False, r"no biases"),
]

# ---------------------------------------------------------------------------
# 2017: the Transformer (Vaswani et al., Table 2 and Secs. 5.2, 6.1)
# ---------------------------------------------------------------------------
TRANSFORMER = dict(
    bleu=[  # (system, EN-DE, EN-FR, training FLOPs EN-DE, EN-FR)
        ("GNMT + RL", 24.6, 39.92, 2.3e19, 1.4e20),
        ("ConvS2S", 25.16, 40.46, 9.6e18, 1.5e20),
        ("MoE", 26.03, 40.56, 2.0e19, 1.2e20),
        ("Transformer (base)", 27.3, 38.1, 3.3e18, 3.3e18),
        ("Transformer (big)", 28.4, 41.8, 2.3e19, 2.3e19),
    ],
    base=dict(N=6, d=512, d_ff=2048, h=8, d_k=64, params=65e6, steps=100_000, hours=12),
    big=dict(N=6, d=1024, d_ff=4096, h=16, d_k=64, params=213e6, steps=300_000, hours=84),
    gpus=8, gpu="P100", tflops=9.5,  # "we used ... 9.5 TFLOPS for ... P100" (Table 2, footnote)
    pairs_en_de=4.5e6, sentences_en_fr=36e6, batch_tokens=25000,
    authors=8,
    src="Vaswani et al., Attention Is All You Need, NeurIPS 2017 (arXiv 1706.03762)",
)

# ---------------------------------------------------------------------------
# 2018: pretrain, then fine-tune
# ---------------------------------------------------------------------------
ULMFIT = dict(date="2018-01-18", error_cut=(18, 24), labelled=100, equiv=100, pretrain="Wikitext-103",
              words=103e6, src="Howard & Ruder, ULMFiT (2018)")
ELMO = dict(date="2018-02-15", tasks=6, lstm_units=4096, proj=512, rel_err=20, src="Peters et al., ELMo (2018)")
GPT1 = dict(date="2018-06-11", books=7000, layers=12, d=768, heads=12, ctx=512, sota=9, tasks=12, epochs=100,
            src="Radford et al. (2018)")
BERT = dict(
    date="2018-10-11", mask=0.15, mask_split=(80, 10, 10), base_params=110e6, large_params=340e6,
    words_books=800e6, words_wiki=2500e6, glue_bert=80.5, glue_gpt=72.8, steps=1_000_000, batch_tokens=128000,
    tpu_days=4, chips_large=64,
    # Table 5: the same architecture pretrained left-to-right (like GPT) or masked, dev scores
    ablation=[("MNLI", 84.4, 82.1), ("QNLI", 88.4, 84.3), ("MRPC", 86.7, 77.5), ("SST-2", 92.7, 92.1),
              ("SQuAD", 88.5, 77.8)],
    src="Devlin et al., BERT (2018), Table 1, Table 5, App. A.2, C.1",
)
GLUE = dict(date="2018-04-20", tasks=9, src="Wang et al., GLUE (2018)")
SUPERGLUE = dict(date="2019-05-02", human=89.8, t5=88.9, src="Wang et al., SuperGLUE (2019); Raffel et al. (2019)")

# ---------------------------------------------------------------------------
# 2019: T5 (Raffel et al., Table 2: GLUE / CNNDM / SQuAD / SuperGLUE, dev, baseline-sized models)
# ---------------------------------------------------------------------------
T5 = dict(
    date="2019-10-23", c4_gb=750, params=11e9, corrupt=0.15, span=3, base_tokens=2**35,
    table=[  # (architecture, objective, GLUE, SQuAD, SuperGLUE)
        ("encoder-decoder", "denoising", 83.28, 80.88, 71.36),
        ("prefix LM", "denoising", 81.82, 78.94, 68.11),
        ("decoder-only LM", "denoising", 74.70, 61.14, 55.02),
        ("encoder-decoder", "LM", 79.56, 76.02, 64.29),
        ("prefix LM", "LM", 79.68, 76.87, 64.86),
        ("decoder-only LM", "LM", 73.78, 53.81, 56.51),
    ],
    src="Raffel et al., Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (2019), "
        "Table 2",
)
WANG2022 = dict(date="2022-04-12", params=5e9, tokens=170e9,
                src="Wang et al., What Language Model Architecture and Pretraining Objective Work Best for Zero-Shot "
                    "Generalization? (2022)")

# ---------------------------------------------------------------------------
# 2019: GPT-2 (Radford et al., Tables 2 and 3; the GPT-2 model card)
# ---------------------------------------------------------------------------
GPT2 = dict(
    date="2019-02-14", links=45e6, karma=3, docs=8e6, gb=40, ctx=1024, vocab=50257,
    sizes=[("117M", 12, 768), ("345M", 24, 1024), ("762M", 36, 1280), ("1542M", 48, 1600)],
    lambada_acc=[45.99, 55.48, 60.12, 63.24], lambada_sota=59.23,
    release=[("Feb 2019", "124M"), ("May 2019", "355M"), ("Aug 2019", "774M"), ("Nov 2019", "1.5B")],
    enwik8_bpb=0.93, sota_lm=7, lm_sets=8,
    src="Radford et al. (2019), Tables 2-3; openai/gpt-2 model card (Nov 2019)",
)

# ---------------------------------------------------------------------------
# 2020: scaling laws and GPT-3
# ---------------------------------------------------------------------------
KAPLAN = dict(date="2020-01-23", alpha_n=0.076, alpha_d=0.095, alpha_c=0.050, n_exp=0.73,
              src="Kaplan et al., Scaling Laws for Neural Language Models (2020), Eqs. 1.1-1.3, 1.7-1.8")
GPT3 = dict(
    date="2020-05-28", flops=3.14e23, pf_days=3.64e3, params_m=174_600,
    sizes=[("Small", 125e6), ("Medium", 350e6), ("Large", 760e6), ("XL", 1.3e9), ("2.7B", 2.7e9), ("6.7B", 6.7e9),
           ("13B", 13e9), ("175B", 175e9)],
    mix=[("Common Crawl (filtered)", 410e9, 60), ("WebText2", 19e9, 22), ("Books1", 12e9, 8), ("Books2", 55e9, 8),
         ("Wikipedia", 3e9, 3)],
    lambada=dict(zero=76.2, one=72.5, few=86.4, sota=68.0),
    triviaqa=dict(zero=64.3, one=68.0, few=71.2),
    src="Brown et al., Language Models are Few-Shot Learners (2020), Tables 2.1, 2.2, 3.2, 3.3, D.1",
)
CHINCHILLA = dict(date="2022-03-29", params=70e9, tokens=1.4e12, gopher_params=280e9, gopher_tokens=300e9,
                  mmlu=67.6, gopher_gain=7.6, flops=5.76e23, per_param=20,
                  src="Hoffmann et al., Training Compute-Optimal Large Language Models (2022), Tables 1, 3")

# ---------------------------------------------------------------------------
# 2021-22: code, instructions
# ---------------------------------------------------------------------------
CODEX = dict(date="2021-07-07", problems=164, pass1=28.8, pass100=70.2, gpt3=0.0, gptj=11.4, gb=159, repos=54e6,
             params=12e9, src="Chen et al., Evaluating Large Language Models Trained on Code (2021)")
FLAN = dict(date="2021-09-03", params=137e9, datasets=60, won=20, of=25,
            src="Wei et al., Finetuned Language Models Are Zero-Shot Learners (2021)")
T0 = dict(date="2021-10-15", params=11e9, won=9, of=11, smaller=16,
          src="Sanh et al., Multitask Prompted Training Enables Zero-Shot Task Generalization (2021)")
INSTRUCTGPT = dict(date="2022-03-04", small=1.3e9, big=175e9, sft=13_000, rm=33_000, ppo=31_000,
                   src="Ouyang et al., Training language models to follow instructions with human feedback (2022)")
CHATGPT = dict(date="2022-11-30", src="OpenAI, Introducing ChatGPT (30 November 2022)")

# ---------------------------------------------------------------------------
# 2023: GPT-4 and the closed era
# ---------------------------------------------------------------------------
GPT4 = dict(
    date="2023-03-14", bar="top 10%", mmlu=86.4, gpt35_mmlu=70.0, predicted_from=10_000, experts=50,
    quote=("Given both the competitive landscape and the safety implications of large-scale models like GPT-4, "
           "this report contains no further details about the architecture (including model size), hardware, "
           "training compute, dataset construction, training method, or similar."),
    src="OpenAI, GPT-4 Technical Report (2023), Secs. 2-3; GPT-4 System Card",
)

# ---------------------------------------------------------------------------
# 2023-26: open weights
# ---------------------------------------------------------------------------
LLAMA = dict(date="2023-02-24", sizes=[("7B", 6.7e9, 1.0e12), ("13B", 13.0e9, 1.0e12), ("33B", 32.5e9, 1.4e12),
                                       ("65B", 65.2e9, 1.4e12)], gpus=2048, days=21, tok_s_gpu=380,
             src="Touvron et al., LLaMA (2023), Table 2, Sec. 2.4")
LLAMA2 = dict(date="2023-07-18", tokens=2e12, ctx=4096, more=40, src="Touvron et al., Llama 2 (2023), Sec. 2")
MISTRAL = dict(date="2023-09-27", window=4096, src="Jiang et al., Mistral 7B (2023)")
MIXTRAL = dict(date="2023-12-11", experts=8, top=2, total=47e9, active=13e9, ctx=32768,
               src="Jiang et al., Mixtral of Experts (2024)")
LLAMA3 = dict(date="2024-07-23", flops=3.8e25, tokens=15.6e12, gpus=16384, mfu=38, interruptions=466, days=54,
              unexpected=419, src="Llama Team, The Llama 3 Herd of Models (2024), Secs. 1, 3.3")
DSV2 = dict(date="2024-05-07", total=236e9, active=21e9, tokens=8.1e12, kv_cut=93.3,
            src="DeepSeek-AI, DeepSeek-V2 (2024)")
DSV3 = dict(date="2024-12-26", gpu_hours=2.788e6, usd=5.576e6, rate=2.0, pre_hours=2.664e6,
            src="DeepSeek-AI, DeepSeek-V3 Technical Report (2024), Table 1")
R1 = dict(date="2025-01-20", aime_start=15.6, aime_zero=77.9, aime_r1=79.8, rl_usd=294e3,
          src="DeepSeek-AI, DeepSeek-R1 (2025; Nature 2025), Table 2, Sec. 2")
QWEN3 = dict(date="2025-04-29", tokens=36e12, languages=119, src="Qwen Team, Qwen3 Technical Report (2025)")
KIMIK2 = dict(date="2025-07-11", tokens=15.5e12, src="Kimi Team, Kimi K2 (2025)")
GLM45 = dict(date="2025-07-28", tokens=23e12, src="GLM-4.5 Team (2025)")
GPTOSS = dict(date="2025-08-05", h100_hours=2.1e6, bits=4.25, src="OpenAI, gpt-oss model card (2025)")
QWEN3NEXT = dict(date="2025-09-10", total=80e9, active=3e9, tokens=15e12,
                 src="Qwen, Qwen3-Next-80B-A3B model card (2025)")
KIMILINEAR = dict(date="2025-10-30", total=48e9, active=3e9, kv_cut=75, speed=6,
                  src="Kimi Team, Kimi Linear (2025)")
GLM5 = dict(date="2026-02-11", total=744e9, active=40e9, tokens=28.5e12,
            src="Zhipu AI, GLM-5 model card; GLM-5 (arXiv 2602.15763, 2026)")
DSV4 = dict(date="2026-04-24", total=1.6e12, active=49e9, flash_total=284e9, flash_active=13e9, flops_frac=27,
            kv_frac=10, tokens=32e12, src="DeepSeek-AI, DeepSeek-V4 model card (2026)")
KIMIK3 = dict(date="2026-07-16", total=2.8e12, active=104e9, kda=69, mla=24, experts=896, top=16,
              src="Moonshot AI, Kimi K3 model card (2026)")
MIMO26 = dict(date="2026-09-21", total=1.02e12, active=42e9, src="Xiaomi, MiMo-V2.6-Pro model card (2026)")

# hybrid attention, in order (linear-time memory layers mixed with a few full-attention layers)
HYBRIDS = [
    ("2024-03-28", "Jamba", r"Mamba + attention", "AI21 Labs", "Lieber et al. (2024)"),
    ("2025-01-14", "MiniMax-01", r"lightning attention", "MiniMax", "MiniMax (2025)"),
    ("2025-04-04", "Nemotron-H", r"Mamba-2 + attention", "NVIDIA", "NVIDIA (2025)"),
    ("2025-09-10", "Qwen3-Next", r"gated DeltaNet 3 : 1", "Alibaba", "Qwen3-Next model card"),
    ("2025-10-30", "Kimi Linear", r"KDA 3 : 1", "Moonshot AI", "Kimi Team (2025)"),
    ("2026-02-16", "Qwen3.5", r"gated DeltaNet 3 : 1", "Alibaba", "Qwen3.5 model card"),
    ("2026-07-16", "Kimi K3", r"KDA 69 : 24", "Moonshot AI", "Kimi K3 model card"),
]

# ---------------------------------------------------------------------------
# Trends (Epoch AI)
# ---------------------------------------------------------------------------
EPOCH = dict(
    growth_all=4.1, growth_frontier=5.3, growth_lm=9.5, growth_frontier_lm=5.0, headline=(4, 5),
    src="Sevilla & Roldan, Training Compute of Frontier AI Models Grows by 4-5x per Year (Epoch AI, May 2024)",
    cost_growth=2.4, gpt4_usd=40e6, gemini_usd=30e6, billion_by=2027,
    cost_src="Cottier et al., The Rising Costs of Training Frontier AI Models (Epoch AI, 2024)",
    data_src="Epoch AI, Notable AI Models database (downloaded 19 October 2026)",
)

# the models of the family tree: (key, label, year, branch, open weights?, parent key)
TREE = [
    ("transformer", r"Transformer", 2017.45, "encdec", True, None),
    ("gpt1", r"GPT-1", 2018.44, "decoder", True, "transformer"),
    ("bert", r"BERT", 2018.78, "encoder", True, "transformer"),
    ("gpt2", r"GPT-2", 2019.12, "decoder", True, "gpt1"),
    ("roberta", r"RoBERTa", 2019.57, "encoder", True, "bert"),
    ("t5", r"T5", 2019.81, "encdec", True, "transformer"),
    ("electra", r"ELECTRA", 2020.22, "encoder", True, "bert"),
    ("gpt3", r"GPT-3", 2020.41, "decoder", False, "gpt2"),
    ("codex", r"Codex", 2021.52, "decoder", False, "gpt3"),
    ("flan", r"FLAN, T0", 2021.75, "encdec", False, "t5"),
    ("instructgpt", r"InstructGPT", 2022.17, "decoder", False, "gpt3"),
    ("chatgpt", r"ChatGPT", 2022.91, "decoder", False, "instructgpt"),
    ("llama", r"LLaMA", 2023.15, "decoder", True, "gpt3"),
    ("gpt4", r"GPT-4", 2023.2, "decoder", False, "chatgpt"),
    ("llama2", r"Llama 2", 2023.54, "decoder", True, "llama"),
    ("mistral", r"Mistral 7B", 2023.74, "decoder", True, "llama"),
    ("mixtral", r"Mixtral", 2023.94, "decoder", True, "mistral"),
    ("llama3", r"Llama 3", 2024.3, "decoder", True, "llama2"),
    ("dsv3", r"DeepSeek-V3", 2024.98, "decoder", True, "llama"),
    ("r1", r"DeepSeek-R1", 2025.05, "decoder", True, "dsv3"),
    ("qwen3", r"Qwen3", 2025.32, "decoder", True, "llama"),
    ("kimik2", r"Kimi K2", 2025.52, "decoder", True, "dsv3"),
    ("gptoss", r"gpt-oss", 2025.59, "decoder", True, "gpt3"),
    ("qwen35", r"Qwen3.5", 2026.12, "decoder", True, "qwen3"),
    ("dsv4", r"DeepSeek-V4", 2026.31, "decoder", True, "dsv3"),
    ("kimik3", r"Kimi K3", 2026.54, "decoder", True, "kimik2"),
]
