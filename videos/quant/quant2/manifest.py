"""Scene order for the final cut: (module, Scene class, chapter title).

Modules keep the names they had in the first cut (narration and render caches are keyed by them); the chapters the
expansion added have new modules, so the file numbers no longer follow the order: this list does."""

TITLE = "Quant, Built: Part 2, The Machinery of Markets"

SCENES = [
    ("s01_hook", "Hook", "What happens when you press buy?"),
    ("s02_instruments", "Instruments", "1. Instruments and how they are quoted"),
    ("s13_futures", "Futures", "2. Futures: carry, basis and the hedge"),
    ("s03_orders", "Orders", "3. The order book"),
    ("s14_auction", "Auction", "4. Auctions: one price for everyone"),
    ("s15_dealers", "Dealers", "5. Dealers, RFQ and wholesalers"),
    ("s04_clearing", "Clearing", "6. Clearing: novation, netting, the waterfall"),
    ("s16_settlement", "Settlement", "7. Settlement and the deposit"),
    ("s05_margin", "Margin", "8. Margin and liquidation"),
    ("s17_imodel", "MarginModel", "9. How much margin?"),
    ("s06_short", "Short", "10. Short selling and the squeeze"),
    ("s07_repo", "Repo", "11. Repo, lending and specials"),
    ("s08_crisis", "Crisis", "12. The day repo broke"),
    ("s18_prime", "Prime", "13. Prime brokers and the race to sell"),
    ("s09_business", "Business", "14. Who earns what"),
    ("s19_index", "Index", "15. Benchmarks and indices"),
    ("s10_world", "World", "16. Markets around the world"),
    ("s20_industry", "Industry", "17. Industry: who runs the machine"),
    ("s21_frontier", "Frontier", "18. Frontier, 2023 to 2026"),
    ("s12_outro", "Outro", "The funding desk; recap, desk questions, problems"),
]
