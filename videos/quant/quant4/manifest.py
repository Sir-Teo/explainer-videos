"""Scene order for the final cut: (module, Scene class, chapter title).

Kept chapters keep their module and class names (the narration and render caches are keyed by them); the chapters
added in the expansion have new modules (``s02b_``, ``s03b_`` ...), so file order and chapter order differ."""

TITLE = "Quant, Built: Part 4, Martingales and Measure"

SCENES = [
    ("s01_hook", "Hook", "Can you beat a fair game?"),
    ("s02_information", "Information", "1. Information: σ-algebras and filtrations"),
    ("s02b_projection", "Projection", "2. Conditional expectation is a projection"),
    ("s03_martingales", "Martingales", "3. Martingales: Ville's fair games"),
    ("s03b_system", "System", "4. You can't beat the system"),
    ("s03c_stopping", "Stopping", "5. Stopping times, and the walk that always wins"),
    ("s03d_optional", "Optional", "6. Optional stopping, proved"),
    ("s03e_doubling", "Doubling", "7. Doubling and admissible strategies"),
    ("s05_barings", "Barings", "8. Doubling down: Barings, 1995"),
    ("s04_ruin", "Ruin", "9. Gambler's ruin and bold play"),
    ("s04b_convergence", "Convergence", "10. Martingales converge"),
    ("s06_doob", "Doob", "11. Doob's decomposition"),
    ("s07_measure", "Measure", "12. Change of measure"),
    ("s07b_radon", "Radon", "13. Radon–Nikodym, and the singular infinite"),
    ("s08_stable", "Stable", "14. Heavy tails as stable laws"),
    ("s09_betting", "Betting", "15. Ville's inequality and testing by betting"),
    ("s10_house", "House", "16. Learning to bet"),
    ("s10b_industry", "Industry", "17. The house, the book and the market"),
    ("s10c_frontier", "Frontier", "18. Frontier: anytime-valid inference, 2023–2026"),
    ("s11_outro", "Outro", "Recap, desk questions, problems"),
]
