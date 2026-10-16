"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "Building a Top-Tier Real-Time Trading System"

SCENES = [
    ("s01_hook", "Hook", "Two o'clock on Fed day"),
    ("s02_job", "TheJob", "Part 1: What a market maker does"),
    ("s03_exchange", "TheExchange", "Inside the exchange"),
    ("s04_feed", "TheFeed", "Part 2: The feed, byte by byte"),
    ("s05_book", "BuildingTheBook", "Rebuilding the order book"),
    ("s06_race", "TheRace", "Part 3: Why microseconds matter"),
    ("s07_light", "SpeedOfLight", "The speed of light"),
    ("s08_ladder", "LatencyLadder", "Inside the box: the latency ladder"),
    ("s09_software", "HotPath", "The hot path in software"),
    ("s10_fpga", "Hardware", "Hardware: deciding before the packet ends"),
    ("s11_fairvalue", "FairValue", "Part 4: Fair value"),
    ("s12_quoting", "Quoting", "Quoting: spread, skew, inventory"),
    ("s13_backtest", "Backtest", "Testing on real queues"),
    ("s14_risk", "Risk", "Part 5: Risk, and Knight Capital"),
    ("s15_research", "ResearchLoop", "Determinism and the research loop"),
    ("s16_outro", "Outro", "The whole machine"),
]
