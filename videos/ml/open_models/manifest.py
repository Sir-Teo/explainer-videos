"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "Inside the Open Frontier: The Architectures of MiMo-V2.6-Pro, GLM-5.3 and Kimi K3"

SCENES = [
    ("s01_hook", "Hook", "Three open frontier models"),
    ("s02_blueprint", "Blueprint", "The blueprint, and its two bills"),
    ("s03_experts", "Experts", "Mixture of experts"),
    ("s04_routing", "Routing", "Routing, and keeping the experts busy"),
    ("s05_long_context", "LongContext", "The million-token problem"),
    ("s06_sliding_window", "SlidingWindow", "MiMo: look nearby, mostly"),
    ("s07_sinks", "Sinks", "MiMo: permission to look at nothing"),
    ("s08_latent", "LatentAttention", "GLM: compress the memory"),
    ("s09_sparse", "SparseAttention", "GLM: read only what matters"),
    ("s10_linear", "LinearMemory", "Kimi: a memory that never grows"),
    ("s11_delta", "DeltaRule", "Kimi: the delta rule, and forgetting"),
    ("s12_hybrid", "Hybrid", "Kimi: three to one"),
    ("s13_depth", "AttentionResiduals", "Kimi: attention across depth"),
    ("s14_latent_moe", "LatentMoE", "Kimi: 896 experts, kept stable"),
    ("s15_side_by_side", "SideBySide", "Side by side"),
    ("s16_outro", "Outro", "Recap"),
]
