"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "How Frontier AI Models Are Trained, End to End"

SCENES = [
    ("s01_hook", "Hook", "One of the largest computations ever run"),
    ("s02_raw_web", "RawWeb", "Part 1: The raw web"),
    ("s03_filtering", "Filtering", "Filtering: the FineWeb recipe"),
    ("s04_dedup", "Dedup", "Deduplication with MinHash"),
    ("s05_quality", "Quality", "Quality, mixtures, and tokens"),
    ("s06_scaling", "ScalingLaws", "Part 2: How big? Scaling laws"),
    ("s07_architecture", "Architecture", "Architecture and mixture of experts"),
    ("s08_optimizer", "Optimizer", "The optimizer: AdamW and Muon"),
    ("s09_schedule", "Schedule", "Learning-rate schedules"),
    ("s10_precision", "Precision", "Fewer bits: FP8 and FP4"),
    ("s11_stability", "Stability", "Loss spikes and stability"),
    ("s12_memory", "Memory", "Part 3: Memory and data parallelism"),
    ("s13_parallelism", "Parallelism", "Tensor, pipeline, expert parallelism"),
    ("s14_operations", "Operations", "Keeping the run alive"),
    ("s15_sft", "SFT", "Part 4: Supervised fine-tuning"),
    ("s16_preferences", "Preferences", "Learning from preferences"),
    ("s17_rl", "RL", "Reinforcement learning and reasoning"),
    ("s18_outro", "Outro", "The whole pipeline"),
]
