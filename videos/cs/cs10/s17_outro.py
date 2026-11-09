from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, COST, CTRL, DATA, FUNC, HEAD, NO, PART, STATE_COLOR, YES,
                                   box, load, wire_diagram)


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
        eq = MathTex(r"P = \alpha C V^2 f", font_size=44, color=NO)
        mesi = VGroup(*[VGroup(Circle(radius=0.4, stroke_color=STATE_COLOR[s], fill_color=STATE_COLOR[s],
                                      fill_opacity=0.2), Text(s, font="DejaVu Sans Mono", font_size=26,
                                                              color=STATE_COLOR[s])) for s in "MESI"])
        for m in mesi:
            m[1].move_to(m[0])
        mesi.arrange_in_grid(2, 2, buff=0.5)
        fs = load("falseshare")["rows"]
        ax = Axes(x_range=[0.5, 4.5, 1], y_range=[0, 90, 30], x_length=3.0, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        fsg = VGroup(ax, VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["threads"], r["same"]) for r in fs]), VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["threads"], r["padded"]) for r in fs]))
        brent = MathTex(r"T_p \le \frac{T_1}{p} + T_\infty", font_size=44, color=HEAD)
        sn = load("sortnet")["bitonic8"]
        net = wire_diagram(8, [[tuple(c) for c in l] for l in sn["layers"]], dy=0.3, dx=0.2, gap=0.15)
        led = ledger_table(load("split")["ledger"], font_size=18, row_h=0.4, label_width=1.8, bar_width=3.0)
        tiles = Group(
            tile(eq, r"the power wall", NO),
            tile(mesi, r"MESI coherence", DATA),
            tile(fsg, r"false sharing, \ measured", CTRL),
            tile(brent, r"Brent's theorem", HEAD),
            tile(net, r"sorting networks", YES),
            tile(led, r"the Job: \ ledger row 4", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Parallel Machines", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            "We connected three levels of parallel-machine reasoning. At the physical level, voltage and power "
            "budgets constrain frequency scaling. At the shared-memory level, MESI tracks permissions, "
            "false-sharing measurements show the cost of poor placement, and defined atomic litmus tests separate "
            "coherence from ordering. At the algorithm level, work and span give bounds, scans turn dependencies "
            "into parallel structure, and the zero-one principle verifies our small sorting networks. The "
            "four-core Job estimate improves partly through parallel execution and partly through less dictionary "
            "work, with several machine costs still omitted. Host C timings are separate measurements. Knowing "
            "which kind of evidence supports each number is part of understanding the machine."
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"locks, \ lock-free structures, \ the memory model in depth", [33]),
            (r"the Job's algorithm: \ sort, \ then count; \ a hash table", [16, 17]),
            (r"a SIMD tokenizer and a Swiss table: \ ledger row 10", [24]),
            (r"threads and the scheduler inside an operating system", [31]),
            (r"agreement between machines that can fail", [38, 59]),
            (r"MapReduce, \ shuffles, \ clusters", [39, 45]),
            (r"accelerators: \ the end of general-purpose speedups", [60]),
        ], font_size=25)
        with self.voiceover(
            "Where this comes back. Locks, lock-free data structures and the memory model in depth are Part 33. The "
            "Job's real fix, a better algorithm, is Parts 16 and 17, and a vectorized tokenizer gives ledger row ten "
            "in Part 24. Threads and their scheduling inside an operating system are Part 31. Consensus between "
            "machines that can crash, Herlihy's question at the scale of a data centre, is Parts 38 and 59. The "
            "partitioned merge grows into MapReduce and the shuffle in Parts 39 and 45. And specialized hardware, "
            "the answer to dark silicon, is Part 60."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"servers", r"a thread pool per core, \ per-core counters, \ no shared hot lines"),
            (r"libraries", r"OpenMP, \ Intel TBB, \ Rust's Rayon, \ Java's fork/join: \ work stealing inside"),
            (r"SIMD", r"intrinsics, \ \texttt{std::simd}, \ and compilers' auto-vectorization reports"),
            (r"GPUs", r"CUDA and its kernels: \ coalesced loads, \ no divergence, \ scans everywhere"),
            (r"HPC", r"MPI collectives, \ weak scaling, \ and the bisection of the network"),
            (r"debugging", r"ThreadSanitizer for races, \ \texttt{perf c2c} for false sharing"),
        ])
        with self.voiceover(
            (
            "In practice. Servers give each core its own thread pool and its own counters, and keep hot data out "
            "of shared lines. Parallel libraries offer several scheduling policies. oneTBB, Rayon and Java "
            "fork-join use forms of work stealing; OpenMP scheduling depends on the runtime and chosen construct. "
            "SIMD code is written with intrinsics or portable vector types, and compilers report which loops they "
            "vectorized. GPU kernels are written to keep loads coalesced and warps undivided. Supercomputer codes "
            "live by MPI collectives and weak scaling. And the tools of the trade are ThreadSanitizer, which can "
            "detect many data races, and perf c2c, which helps investigate cache-line contention when the host "
            "and permissions support its counters. Neither is a complete proof of correctness or performance."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Under Dennard scaling by $\kappa$, \ how does power per area change if the voltage stays fixed while the "
            r"clock still rises by $\kappa$? \ And if the clock stays fixed too?",
            r"Four MESI caches, \ all Invalid. \ Core 0 reads, \ core 1 writes, \ core 0 reads, \ core 1 writes. \ "
            r"Give every state after each step, \ and count the invalidations.",
            r"Under TSO, \ put a fence in thread 0 of the store-buffering test only. \ Can both threads still read 0? "
            r"\ Why?",
            r"Show that the Hillis--Steele scan does $n \log_2 n - n + 1$ additions, \ and Blelloch's $2(n - 1)$.",
            r"\textit{Build.} \ Cut the Job's text into 64 pieces, \ each counted in its own table, \ and let 4 cores "
            r"take them as they come free: \ how close to perfect balance, \ and what does the merge cost now?",
            r"$\bigstar$ \textit{Research.} \ Our work-stealing runs stay within $T_1/p + 1.6\,T_\infty$. \ What is "
            r"the tight constant for randomized stealing on balanced fork-join trees, \ and what does choosing "
            r"victims by locality change?",
        ], font_size=22)
        with self.voiceover(
            "The notes give six exercises and worked guidance. The fifth changes the Job from four large shards to sixty-four smaller pieces; compare both scheduling balance and the changed amount of dictionary work. The last is a research exercise on scheduler constants and locality. Specify the computation and scheduler before investigating a bound: a finite simulation does not establish a universal constant."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 11, \ The Running Program", font_size=42).to_edge(UP, buff=0.6)
        layers = VGroup(*[box(5.2, 0.62, rf"\text{{{t}}}", c, 22) for t, c in (
            ("source code", YES), ("compiler", DATA), ("assembler", CTRL), ("linker", FUNC), ("loader", HEAD),
            ("a running process", NO))]).arrange(DOWN, buff=0.12).move_to(DOWN * 0.2)
        q = label(r"Act III: \ speaking to the machine", font_size=30, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That ends Act Two. Next comes Act Three, Speaking to the Machine, and Part 11 follows one program from "
            "source code to a running process: how its data becomes bytes, its calls a stack, and its names "
            "addresses; how the linker and loader bring it to life; and how one unchecked copy can make it do "
            "something its author never wrote."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(l) for l in layers], lag_ratio=0.25))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hennessy and Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed., ch. 4, 5",
             r"Sorin, Hill and Wood, \textit{A Primer on Memory Consistency and Cache Coherence}, 2nd ed. (2020)",
             r"Herlihy, Shavit, Luchangco and Spear, \textit{The Art of Multiprocessor Programming}, 2nd ed. (2020)",
             r"Leighton, \textit{Introduction to Parallel Algorithms and Architectures} (1992)",
             r"Knuth, \textit{The Art of Computer Programming}, vol. 3, \S 5.3.4"],
            [r"Dennard et al., ``Design of ion-implanted MOSFETs with very small physical dimensions'' (1974)",
             r"Amdahl (1967); \ Gustafson, ``Reevaluating Amdahl's law'' (1988)",
             r"Lamport, ``How to make a multiprocessor computer that correctly executes multiprocess programs'' (1979)",
             r"Papamarcos and Patel, ``A low-overhead coherence solution for multiprocessors'' (1984)",
             r"Brent, ``The parallel evaluation of general arithmetic expressions'' (1974)",
             r"Batcher, ``Sorting networks and their applications'' (1968)",
             r"Ehlers and M\"uller, ``New bounds on optimal sorting networks'' (2015), arXiv:1501.06946",
             r"Blelloch, ``Prefix sums and their applications'' (1990); \ Valiant, ``A bridging model'' (1990)",
             r"Herlihy, ``Wait-free synchronization'' (1991)",
             r"Blumofe and Leiserson, ``Scheduling multithreaded computations by work stealing'' (1999)",
             r"Esmaeilzadeh et al., ``Dark silicon and the end of multicore scaling'' (2011)",
             r"Batty et al., ``Mathematizing C++ concurrency'' (2011); \ Kang et al., ``A promising semantics'' (2017)",
             r"Stern et al., ``How to avoid OOTA without really trying'' (2025), WG21 P3692R3 (proposal)",
             r"Landauer, ``Irreversibility and heat generation in the computing process'' (1961)",
             r"Rupp, \textit{Microprocessor Trend Data} (CC BY 4.0)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
