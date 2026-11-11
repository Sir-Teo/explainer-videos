"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "Computer Science, Built: Part 33, Concurrency"

SCENES = [
    ("s01_hook", "Hook", "Two threads, one counter"),
    ("s02_why", "Why", "1. Why concurrency"),
    ("s03_race", "Race", "2. The race"),
    ("s04_mutex", "Mutex", "3. Mutual exclusion from reads and writes"),
    ("s05_tso", "Tso", "4. Peterson meets the store buffer"),
    ("s06_locks", "Locks", "5. Hardware locks"),
    ("s07_sema", "Sema", "6. Semaphores"),
    ("s08_monitors", "Monitors", "7. Monitors and condition variables"),
    ("s09_deadlock", "Deadlock", "8. Deadlock"),
    ("s10_models", "Models", "9. Memory models"),
    ("s11_lin", "Lin", "10. Linearizability"),
    ("s12_lockfree", "LockFree", "11. Lock-free structures"),
    ("s13_consensus", "Consensus", "12. Consensus numbers"),
    ("s14_tm", "Tm", "13. Transactional memory, channels and actors"),
    ("s15_wild", "Wild", "14. Concurrency bugs in the wild"),
    ("s16_pebble", "PebbleThreads", "15. PebbleOS gains threads and CAS"),
    ("s17_frontier", "Frontier", "16. Frontier: checking concurrent programs"),
    ("s18_outro", "Outro", "Recap, problems, and where this comes back"),
]
