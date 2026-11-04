"""Scene order for the final cut: (module, Scene class, chapter title).

Kept chapters keep their module and class names (the narration and render caches are keyed by them); the chapters
added in the expansion are s10-s22, so file order and chapter order differ."""

TITLE = "Quant, Built: Part 12, The Volatility Surface"

SCENES = [
    ("s01_hook", "Hook", "The shape of fear"),
    ("s02_smile", "Smile", "1. The smile, read"),
    ("s10_dynamics", "Dynamics", "2. How the surface moves"),
    ("s11_arbitrage", "Arbitrage", "3. Static arbitrage: impossible shapes"),
    ("s12_svi", "SVI", "4. SVI: a smile in five numbers"),
    ("s13_ssvi", "SSVI", "5. SSVI: the whole surface in one formula"),
    ("s03_localvol", "LocalVol", "6. Dupire's local volatility, derived"),
    ("s14_gyongy", "Gyongy", "7. Gyöngy: every model has a local-volatility twin"),
    ("s15_forward", "Forward", "8. Local volatility's future"),
    ("s04_varswap", "VarSwap", "9. Variance swaps: buying volatility itself"),
    ("s16_replicate", "Replicate", "10. Replicating on real Bitcoin; volatility swaps"),
    ("s17_vix", "VIX", "11. The VIX, and our own"),
    ("s05_vrp", "VRP", "12. The variance risk premium, measured"),
    ("s18_moments", "Moments", "13. What option prices say about the future"),
    ("s19_etp", "ETP", "14. VIX futures, the roll and short-volatility notes"),
    ("s06_volmageddon", "Volmageddon", "15. Volmageddon, 5 February 2018"),
    ("s20_gamma", "Gamma", "16. Dealer gamma and same-day options"),
    ("s07_learning", "Learning", "17. Learning surfaces"),
    ("s21_industry", "Industry", "18. Who builds surfaces, and who sells them"),
    ("s22_frontier", "Frontier", "19. Frontier, 2023–2026"),
    ("s23_research", "Research", "For the researcher: reading the density from noisy prices"),
    ("s09_outro", "Outro", "Recap, desk questions, problems"),
]
