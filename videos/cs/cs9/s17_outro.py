from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, Shelves,
                                  address_bits, box, fmt, load, mono)


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
        ax = Axes(x_range=[12, 29, 4], y_range=[0, 350, 100], x_length=3.2, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        stairs = VGroup(ax, VMobject(color=HEAD, stroke_width=3).set_points_as_corners(
            [ax.c2p(np.log2(p["bytes"]), p["ns"]) for p in st]))
        m = load("matmul")["gflops"]
        sizes = ["256", "512", "1024", "2048"]
        ax2 = Axes(x_range=[0, 3, 1], y_range=[0, 4.5, 1], x_length=3.0, y_length=2.0, tips=False,
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
            "What we built in this part. Caches from nothing: an address cut into tag, index and offset; sets and "
            "ways; replacement and write policies; and the three kinds of miss, measured on the Job. This computer's "
            "memory, measured: a staircase from one and a half nanoseconds to three hundred, and the bandwidth at each "
            "step. Programs that respect the hierarchy, and algorithms that respect every level at once without "
            "knowing its size. A theorem about pebbles that says how much data any matrix multiply must move. And the "
            "Job, which turned out to hide its three billion cache misses almost completely."
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
            "Where this comes back. When several cores share memory, their caches must agree: Part 10's coherence. "
            "Address translation and its cache, the TLB, are Part 32. B-trees, external sorting and column stores "
            "return in Parts 17, 34 and 35. The Job's real problem, reading three billion lines to count four and a "
            "half million words, is solved by better algorithms in Parts 16 and 17. Caching across whole machines, "
            "with content delivery networks and Memcached, is Parts 39 and 45. And memory traffic is the limit of "
            "the accelerators in Part 60."
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
            "In practice. Game engines lay out data for the cache, splitting hot fields from cold. Databases size "
            "their B-tree nodes to pages and store columns separately. Numerical libraries and AI frameworks are built "
            "from tiled kernels, and judge themselves on the roofline model, arithmetic against memory bandwidth. "
            "Servers place memory near the core that uses it and use huge pages to spare the TLB. And every system "
            "design starts from the same table of latencies this part measured, extended to disks and networks."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"A 32 KB, 8-way cache with 64-byte lines and 48-bit addresses: \ how many bits of tag, \ index and offset? "
            r"\ Which set does address \texttt{0x7f3a12345678} use?",
            r"L1: \ 4 cycles, \ 5\% misses; \ L2: \ 12 cycles, \ 20\% of those miss; \ DRAM: \ 200 cycles. \ What is "
            r"the AMAT? \ What miss rate in L1 would double it?",
            r"Explain why random replacement beats LRU on a loop over $C + 1$ lines in a cache of $C$ lines. \ What "
            r"does Belady's policy do?",
            r"Show that a tiled multiply with $3T^2 \le M$ moves $O(n^3/T)$ words. \ How close to the pebble bound "
            r"$2n^3/\sqrt{M}$ can the best $T$ come?",
            r"\textit{Build.} \ Add bimodal insertion to \texttt{cache.py} \ and run the Job's scaled scans: \ do you "
            r"reproduce 47\%? \ What insertion probability is best?",
            r"$\bigstar$ \textit{Research.} \ On the Job's full scans, \ keeping the table's front misses 70\% at 32 KB "
            r"\ against LRU's 88\%. \ What is Belady's miss rate there, \ and how close can an online policy get?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add an insertion policy to our cache simulator and measure it on the Job's scans. The last, "
            "marked with a star, is a research problem: nobody knows its full answer, and the notes say where to "
            "start."
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
        q = label(r"the clock stopped getting faster in 2005: \ what then?", font_size=30, color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. Around 2005 the clock stopped getting faster, for reasons of power that Part 10 derives, and "
            "processors became many cores sharing caches and memory, with vector units in each. Part 10 builds them: "
            "SIMD, multicore, cache coherence, GPUs, and the Job on four cores."
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
             r"Shi et al., ``Applying deep learning to the cache replacement problem'', MICRO (2019)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
