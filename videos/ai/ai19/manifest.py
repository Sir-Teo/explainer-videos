"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "AI, Built: Part 19, Inference"

SCENES = [
    ("s01_hook", "Hook", "One token at a time"),
    ("s02_phases", "Phases", "1. Prefill and decode"),
    ("s03_kvcache", "KVCache", "2. The key-value cache, priced"),
    ("s04_batching", "Batching", "3. Batching: speed against cost"),
    ("s05_scheduling", "Scheduling", "4. Continuous batching"),
    ("s06_paging", "Paging", "5. Pages and shared prefixes"),
    ("s07_exact", "Exact", "6. Guess ahead, check at once"),
    ("s08_drafters", "Drafters", "7. Drafters"),
    ("s09_rounding", "Rounding", "8. Rounding error"),
    ("s10_outliers", "Outliers", "9. Outliers and SmoothQuant"),
    ("s11_gptq", "GPTQ", "10. GPTQ, from Optimal Brain Surgeon"),
    ("s12_rotation", "Rotation", "11. Rotations: QuaRot and SpinQuant"),
    ("s13_formats", "Formats", "12. Four-bit floats: MXFP4 and NVFP4"),
    ("s14_kvquant", "KVQuant", "13. The cache in fewer bits"),
    ("s15_flash", "Flash", "14. FlashAttention"),
    ("s16_serveattn", "ServeAttention", "15. Attention at serve time"),
    ("s17_grammar", "Grammar", "16. Constrained decoding"),
    ("s18_frontier", "Frontier", "17. The frontier, late 2026"),
    ("s19_outro", "Outro", "Recap, problems, and what comes next"),
]
