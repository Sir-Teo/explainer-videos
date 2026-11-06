"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "Computer Science, Built: Part 32, Virtual Memory"

SCENES = [
    ("s01_hook", "Hook", "Two programs, one address"),
    ("s02_problem", "Problem", "1. Protection and relocation"),
    ("s03_segments", "Segments", "2. Base and bounds, and segments"),
    ("s04_paging", "Paging", "3. Paging"),
    ("s05_tables", "Tables", "4. Multi-level page tables"),
    ("s06_tlb", "Tlb", "5. The TLB"),
    ("s07_faults", "Faults", "6. Page faults"),
    ("s08_replacement", "Replacement", "7. Which page to evict"),
    ("s09_curves", "Curves", "8. Working sets and thrashing"),
    ("s10_cow", "Cow", "9. Copy-on-write, zero pages and mmap"),
    ("s11_kernelmap", "KernelMap", "10. The kernel's own mapping"),
    ("s12_alloc", "Alloc", "11. Kernel allocators"),
    ("s13_virt", "Virt", "12. Virtual machines"),
    ("s14_containers", "Containers", "13. Containers"),
    ("s15_pebblevm", "PebbleVM", "14. PebbleOS gains virtual memory"),
    ("s16_frontier", "Frontier", "15. Frontier: translation reach and memory tiers"),
    ("s17_outro", "Outro", "Recap, problems, and where this comes back"),
]
