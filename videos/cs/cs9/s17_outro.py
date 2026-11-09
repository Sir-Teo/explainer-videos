from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, Shelves,
                                  address_bits, box, fmt, load, mono, plot_range)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        bits = address_bits(0x0A4C, 6, 4, 6, cell=0.3)
        sh = Shelves(4, 2, w=0.9, h=0.3, set_labels=False)
        for s in range(4):
            for k in range(2):
                if (s + k) % 3:
                    sh.add(sh.put(s, k, "", [DATA, CTRL][k]))
        st = load("staircase")["points"]
        ymax, ystep = plot_range(p["ns"] for p in st)
        ax = Axes(x_range=[12, 29, 4], y_range=[0, ymax, ystep], x_length=3.2, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        stairs = VGroup(ax, VMobject(color=HEAD, stroke_width=3).set_points_as_corners(
            [ax.c2p(np.log2(p["bytes"]), p["ns"]) for p in st]))
        m = load("matmul")["gflops"]
        sizes = ["256", "512", "1024", "2048"]
        ymax, ystep = plot_range(v for k in ("ijk", "ikj", "tiled") for v in m[k].values())
        ax2 = Axes(x_range=[0, 3, 1], y_range=[0, ymax, ystep], x_length=3.0, y_length=2.0, tips=False,
                   axis_config={"color": GREY_D})
        mm = VGroup(ax2, *[VMobject(color=c, stroke_width=3).set_points_as_corners(
            [ax2.c2p(k, m[key][s]) for k, s in enumerate(sizes) if s in m[key]])
            for key, c in (("ijk", NO), ("ikj", DATA), ("tiled", YES))])
        bound = MathTex(r"Q \ge \frac{2n^3}{\sqrt{M}} - 2M", font_size=40, color=HEAD)
        led = ledger_table(load("job")["ledger"], font_size=18, row_h=0.4, label_width=1.8, bar_width=3.0)
        tiles = Group(
            tile(bits, r"tag, \ index, \ offset", DATA),
            tile(sh, r"sets and ways", CTRL),
            tile(stairs, r"this machine's staircase", HEAD),
            tile(mm, r"programming for caches", YES),
            tile(bound, r"the red-blue pebble game", HEAD),
            tile(led, r"the Job: \ ledger row 3", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ The Memory Hierarchy", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "We built cache lookup and replacement models, examined signed miss-accounting comparisons, and measured "
            "this host's dependent-access times and sequential throughput. Loop ordering and tiling changed data "
            "reuse, while recursive layouts illustrated cache-oblivious ideas under explicit assumptions. The "
            "red-blue pebble example now checks its fast-memory occupancy, and the classical multiplication "
            "comparison counts fills and dirty write-backs. The Job's ledger combines a relocated abstract event "
            "model with short core benchmarks and assumed clocks. Its small projected overhead belongs to those "
            "assumptions; the billions of table-line visits are not billions of physical DRAM misses. These "
            "distinctions let us connect a visualization to a calculation without claiming more than either "
            "establishes."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"many cores sharing caches \ $\to$ \ coherence", [10]),
            (r"the TLB and page tables", [32]),
            (r"B-trees, \ external sorting, \ column stores", [17, 34, 35]),
            (r"the Job reads too much \ $\to$ \ better algorithms", [16, 17]),
            (r"caches across machines: \ CDNs, \ Memcached", [39, 45]),
            (r"memory traffic on accelerators", [60]),
        ], font_size=25)
        with self.voiceover(
            "These ideas return in several layers of the course. Coherence in Part 10 controls how cached copies "
            "interact across cores; it is separate from the memory-ordering model. Part 32 develops virtual "
            "addressing and translation caches. B-trees, external sorting and column-oriented layouts reappear with "
            "their own storage and update assumptions. Later Job algorithms reduce the amount of searching rather "
            "than only its per-access cost. Distributed caching adds network latency, consistency and eviction "
            "choices across machines. Accelerator design adds arithmetic intensity, local storage and transfer "
            "scheduling. At every layer, specify the event being counted, the resource limit and the observations "
            "needed to test the model."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"game engines", r"data-oriented design: \ structs of arrays, \ hot and cold data split"),
            (r"databases", r"B-trees sized to pages, \ column stores, \ cache-conscious hash joins"),
            (r"HPC and AI", r"tiled kernels in BLAS and cuDNN; \ the roofline model; \ HBM bandwidth"),
            (r"servers", r"NUMA placement, \ huge pages for the TLB, \ \texttt{perf} cache-miss counters"),
            (r"system design", r"the latency numbers every programmer should know, \ from L1 to a disk to another "
                               r"continent"),
        ])
        with self.voiceover(
            "Practical optimization starts with a representative workload and a controlled measurement. Compare "
            "useful layout variants, inspect compiler and library settings, and check correctness before attributing "
            "a speedup. Distinguish dependent latency from throughput and logical bytes processed from actual memory "
            "traffic. Roofline reasoning needs the relevant memory boundary and arithmetic intensity. Huge-page "
            "advice, NUMA placement and prefetch hints require verification under the operating system and hardware "
            "in use. Cache simulators can isolate mechanisms under chosen rules; hardware counters and repeated "
            "benchmarks help test whether those mechanisms explain a real application. Record uncertainty and setup "
            "so someone else can reproduce the result."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"A 32 KiB, 8-way cache with 64-byte lines and 48-bit addresses: \ how many bits of tag, \ index and offset? "
            r"\ Which set does address \texttt{0x7f3a12345678} use?",
            r"Serial lookups: L1 4 cycles, 5\% misses; L2 adds 12 cycles, 20\% conditional misses; memory adds 200. What is "
            r"the AMAT? \ What miss rate in L1 would double it?",
            r"A cold fully associative cache has $C\ge2$ lines and forced insertion. For a repeated $(C+1)$-line "
            r"cycle, compare LRU, seeded random and MIN, including startup versus steady state.",
            r"For classical multiplication, state the fast-data budget and output conditions. Count read fills, "
            r"dirty evictions and final writes of tiled schedules; compare their movement with $\Omega(n^3/\sqrt M)$.",
            r"\textit{Build.} \ Add bimodal insertion to \texttt{cache.py} \ and run the Job's scaled scans: \ do you "
            r"reproduce 47\%? \ What insertion probability is best?",
            r"$\bigstar$ \textit{Research.} \ For the table-length prefix stream, pin $C-1$ front lines and use one "
            r"transient slot. Bound or compute MIN under the same rules, then evaluate a past-only policy on heldout scans.",
        ], font_size=22)
        with self.voiceover(
            "The exercises distinguish address arithmetic, serial access expectations, replacement policies and "
            "movement bounds. State the cache's initial state and insertion rules before comparing a cyclic scan "
            "with MIN. Keep read-only counts separate from total read-plus-write transfers, and include "
            "output-buffer space in external-memory examples. The build problem asks you to implement and evaluate "
            "insertion variants with explicit seeds and event definitions. For the research problem, use a feasible "
            "same-capacity comparator, separate training from heldout evaluation, and never encode future trace "
            "outcomes in an online predictor. A proof for a structured trace and an empirical result on a sampled "
            "workload are different deliverables."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 10, \ Parallel Machines", font_size=42).to_edge(UP, buff=0.6)
        cores = VGroup(*[box(1.6, 1.0, rf"\text{{core {k}}}", [DATA, YES, CTRL, INF][k], 22) for k in range(4)]).arrange(
            RIGHT, buff=0.4).move_to(UP * 0.4)
        shared = box(7.6, 0.6, r"\text{shared cache and memory}", HEAD, 22).next_to(cores, DOWN, buff=0.5)
        lines = VGroup(*[Line(c.get_bottom(), shared.get_top(), color=GREY_C) for c in cores])
        q = label("power and scaling constraints: \\ parallelism brings new trade-offs", font_size=30, color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next, parallel machines. Power and scaling constraints slowed the earlier pace of clock-frequency "
            "growth, while multicore designs and vector units became increasingly important. Part 10 studies SIMD, "
            "shared-memory execution, coherence and GPU organization, and evaluates parallel versions of the Job "
            "under stated workloads and resource limits. More cores do not automatically remove dependencies, serial "
            "work, communication or bandwidth bottlenecks. The memory models from this part give us a starting point "
            "for measuring those tradeoffs."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(c) for c in cores], lag_ratio=0.2), FadeIn(shared),
                      Create(lines))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hennessy and Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed., ch. 2, App. B",
             r"Bryant and O'Hallaron, \textit{Computer Systems: A Programmer's Perspective}, ch. 6",
             r"Jacob, Ng and Wang, \textit{Memory Systems: Cache, DRAM, Disk} (2008)",
             r"Drepper, ``What every programmer should know about memory'' (2007)"],
            [r"Belady, ``A study of replacement algorithms for a virtual-storage computer'', IBM Sys. J. (1966)",
             r"Mattson, Gecsei, Slutz and Traiger, ``Evaluation techniques for storage hierarchies'' (1970)",
             r"Hong and Kung, ``I/O complexity: the red-blue pebble game'', STOC (1981)",
             r"Hill, ``Aspects of cache memory and instruction buffer performance'', PhD thesis (1987)",
             r"Aggarwal and Vitter, ``The input/output complexity of sorting and related problems'' (1988)",
             r"Wulf and McKee, ``Hitting the memory wall'' (1995)",
             r"Frigo, Leiserson, Prokop and Ramachandran, ``Cache-oblivious algorithms'', FOCS (1999)",
             r"Qureshi et al., ``Adaptive insertion policies for high performance caching'', ISCA (2007)",
             r"Jain and Lin, ``Back to the future: leveraging Belady's algorithm'', ISCA (2016)",
             r"Shi et al., ``Applying deep learning to the cache replacement problem'', MICRO (2019)",
             r"Smith et al., ``A tight I/O lower bound for matrix multiplication'', arXiv v2 (2019)",
             r"Shah, Jain and Lin, ``Effective mimicry of Belady's MIN policy'', HPCA (2022)",
             r"Duong and Lin, ``Streamlined on-chip temporal prefetching'', HPCA (2026)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The books and papers this part follows are on screen and in the notes. Thank you for watching."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
