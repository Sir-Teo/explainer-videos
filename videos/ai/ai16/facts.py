"""Published facts Part 16 quotes, each with its source (checked against the primary document, October 2026; see the
README's fact-check notes).  Nothing here is computed; ``compute.py`` derives the rest (parameter counts from
configurations, active shares)."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Mixture-of-experts language models: (key, name, date, total, active, routed experts, chosen per token, shared,
# source).  Totals and active counts as each maker states them.
# ---------------------------------------------------------------------------
MODELS = [
    ("switch", "Switch-C", "2021-01", 1.571e12, None, 2048, 1, 0,
     "Fedus, Zoph & Shazeer, Switch Transformers (2021), Table 9"),
    ("glam", "GLaM", "2021-12", 1.2e12, 96.6e9, 64, 2, 0, "Du et al., GLaM (2021), Table 4"),
    ("mixtral", "Mixtral 8x7B", "2023-12", 46.7e9, 12.9e9, 8, 2, 0, "Jiang et al., Mixtral of Experts (2024)"),
    ("dsv2", "DeepSeek-V2", "2024-05", 236e9, 21e9, 160, 6, 2, "DeepSeek-AI, DeepSeek-V2 (2024), Sec. 3.1"),
    ("dsv3", "DeepSeek-V3", "2024-12", 671e9, 37e9, 256, 8, 1, "DeepSeek-AI, DeepSeek-V3 (2024), Sec. 4.2"),
    ("llama4", "Llama 4 Maverick", "2025-04", 400e9, 17e9, 128, 1, 1, "Meta AI blog, 5 April 2025"),
    ("qwen3", "Qwen3-235B-A22B", "2025-04", 235e9, 22e9, 128, 8, 0, "Qwen Team, Qwen3 Technical Report (2025)"),
    ("kimik2", "Kimi K2", "2025-07", 1.04e12, 32e9, 384, 8, 1, "Moonshot AI, Kimi-K2 model card"),
    ("glm45", "GLM-4.5", "2025-07", 355e9, 32e9, 160, 8, 1, "Zhipu AI, GLM-4.5 model card and configuration"),
    ("gptoss", "gpt-oss-120b", "2025-08", 116.8e9, 5.1e9, 128, 4, 0, "OpenAI, gpt-oss model card (2025)"),
    ("qwen3next", "Qwen3-Next-80B-A3B", "2025-09", 80e9, 3e9, 512, 10, 1, "Qwen, Qwen3-Next model card"),
    ("minimax", "MiniMax-M2", "2025-10", 230e9, 10e9, 256, 8, 0, "MiniMax, MiniMax-M2 model card and configuration"),
    ("glm5", "GLM-5", "2026-02", 744e9, 40e9, 256, 8, 1, "Zhipu AI, GLM-5 model card and configuration"),
    ("qwen35", "Qwen3.5-397B-A17B", "2026-02", 397e9, 17e9, 512, 10, 1, "Qwen, Qwen3.5-397B-A17B model card"),
    ("dsv4", "DeepSeek-V4-Pro", "2026-04", 1.6e12, 49e9, 384, 6, 1,
     "DeepSeek-AI, DeepSeek-V4 (arXiv 2606.19348, 2026), Table of hyperparameters"),
    ("kimik3", "Kimi K3", "2026-07", 2.8e12, 104e9, 896, 16, 2, "Moonshot AI, Kimi-K3 model card"),
    ("mistral4", "Mistral Large 4", "2026-10", 1.0e12, 52e9, 128, 4, 1, "Mistral AI, Mistral-Large-4-1T-A52B model card"),
]

# The configurations the parameter count is derived from (the models' published config.json files)
DSV3_CONFIG = dict(vocab=129280, d=7168, layers=61, dense_layers=3, ffn=18432, moe_ffn=2048, routed=256, shared=1,
                   k=8, heads=128, q_lora=1536, kv_lora=512, nope=128, rope=64, v=128, mtp_params=14e9,
                   src="deepseek-ai/DeepSeek-V3 config.json; DeepSeek-V3 Technical Report (2024)")
MIXTRAL_CONFIG = dict(vocab=32000, d=4096, layers=32, ffn=14336, experts=8, k=2, heads=32, kv_heads=8, head_dim=128,
                      src="mistralai/Mixtral-8x7B-v0.1 config.json; Jiang et al. (2024)")

# DeepSeek-V3's routing and its training (Technical Report, Secs. 2.1.2, 3.2, 4.2)
DSV3_ROUTING = dict(gamma=0.001, gamma_until=14.3e12, alpha_seq=0.0001, max_nodes=4, nodes=8, ep=64, no_drop=True,
                    nvlink=160e9, ib=50e9, fp8_dispatch=True, scaling=2.5)

# History (dates of first public release)
HISTORY = [
    (1991, "Jacobs, Jordan, Nowlan & Hinton", "Adaptive Mixtures of Local Experts (Neural Computation 3:79-87)"),
    (1994, "Jordan & Jacobs", "Hierarchical mixtures of experts and the EM algorithm"),
    (2017, "Shazeer et al.", "Outrageously Large Neural Networks: up to 137 billion parameters, noisy top-k gating"),
    (2020, "Lepikhin et al., GShard", "600 billion parameters, 2,048 TPU v3 chips, 4 days; 100 languages to English"),
    (2021, "Fedus, Zoph & Shazeer, Switch", "one expert per token; up to 7x faster pre-training at equal compute"),
    (2021, "Du et al., GLaM", "1.2 trillion parameters; a third of GPT-3's training energy, half its FLOPs per token"),
    (2022, "Zoph et al., ST-MoE", "the router z-loss"),
    (2023, "Jiang et al., Mixtral", "8 experts, 2 per token: the first strong open mixture"),
    (2024, "Dai et al., DeepSeekMoE", "fine-grained experts, shared experts"),
    (2024, "Wang et al.; DeepSeek-V3", "load balancing without an auxiliary loss"),
]
SHAZEER = dict(params=137e9, capacity=1000, src="Shazeer et al., ICLR 2017 (arXiv 1701.06538)")
GSHARD = dict(params=600e9, tpus=2048, days=4, languages=100, src="Lepikhin et al. (arXiv 2006.16668)")
SWITCH = dict(speedup=7, xxl_speedup=4, alpha=0.01, cf=(1.0, 1.25), params=1.571e12, experts=2048,
              src="Fedus, Zoph & Shazeer (arXiv 2101.03961)")
GLAM = dict(params=1.2e12, energy=1 / 3, flops=1 / 2, src="Du et al. (arXiv 2112.06905)")

# Upcycling, mixture-of-depths
UPCYCLE = dict(sunk=0.5, src="Komatsuzaki et al., Sparse Upcycling (arXiv 2212.05055, ICLR 2023)")
MOD = dict(cap=0.125, every=2, faster=0.5, predictor=0.99, src="Raposo et al., Mixture-of-Depths (arXiv 2404.02258)")

# Sparse attention
NSA = dict(cmp_block=32, stride=16, sel_block=64, n_sel=16, window=512, fwd=9.0, bwd=6.0, dec=11.6, ctx=65536,
           model=(27e9, 3e9), src="Yuan et al., Native Sparse Attention (arXiv 2502.11089, 2025), Secs. 4.1, 5")
DSA = dict(topk=2048, heads=64, dim=128, bits=8, src="DeepSeek-AI, DeepSeek-V3.2-Exp (2025) and its config.json")
GLM5_DSA = dict(topk=2048, heads=32, dim=128, src="zai-org/GLM-5 config.json")
DSV4_ATT = dict(m=4, m2=128, topk=(1024, 512), window=128, idx_heads=64, idx_dim=128, idx_bits=4, flops=0.27, kv=0.10,
                src="DeepSeek-AI, DeepSeek-V4 (arXiv 2606.19348, 2026)")

# Pruning and sparsity
LTH = dict(size=(0.1, 0.2), src="Frankle & Carbin, The Lottery Ticket Hypothesis (ICLR 2019)")
HAN = dict(alexnet=9, vgg=13, src="Han, Pool, Tran & Dally, Learning both Weights and Connections (NeurIPS 2015)")
SPARSEGPT = dict(sparsity=0.6, hours=4.5, src="Frantar & Alistarh, SparseGPT (arXiv 2301.00774)")
LAZY = dict(t5=0.030, vit=0.063, src="Li et al., The Lazy Neuron Phenomenon (ICLR 2023)")
TEAL = dict(sparsity=(0.4, 0.5), speed=(1.53, 1.8), src="Liu et al., TEAL (arXiv 2408.14690)")
