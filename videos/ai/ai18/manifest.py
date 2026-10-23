"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "AI, Built: Part 18, Pretraining at Scale"

SCENES = [
    ("s01_hook", "Hook", "Sixteen thousand GPUs, fifty-four days"),
    ("s02_anatomy", "Anatomy", "1. Anatomy of a frontier run"),
    ("s03_web", "Web", "2. From the web to text"),
    ("s04_dedup", "Dedup", "3. Near-duplicates: MinHash and LSH"),
    ("s05_quality", "Quality", "4. Quality, and keeping the test clean"),
    ("s06_mixture", "Mixture", "5. Mixtures, synthetic data and collapse"),
    ("s07_objectives", "Objectives", "6. What the model is asked to predict"),
    ("s08_curriculum", "Curriculum", "7. Annealing, mid-training, long context"),
    ("s09_accounting", "Accounting", "8. Counting FLOPs and bytes"),
    ("s10_dataparallel", "DataParallel", "9. Data parallelism and the all-reduce"),
    ("s11_zero", "ZeRO", "10. ZeRO and FSDP"),
    ("s12_tensor", "TensorParallel", "11. Tensor parallelism"),
    ("s13_pipeline", "Pipeline", "12. Pipeline parallelism"),
    ("s14_context", "Context", "13. Context, experts, and utilization"),
    ("s15_precision", "Precision", "14. Fewer bits"),
    ("s16_stability", "Stability", "15. Keeping the run stable"),
    ("s17_mtp", "MTP", "16. Predicting two tokens ahead"),
    ("s18_faults", "Faults", "17. When hardware fails"),
    ("s19_recipe", "Recipe", "18. Our own full recipe"),
    ("s20_outro", "Outro", "Recap, problems, and what comes next"),
]
