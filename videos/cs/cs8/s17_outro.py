from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, RobRing, box,
                                  dag_figure, fmt, load, mono)


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
        df = load("dataflow")
        g = dag_figure(df, dx=1.0, dy=0.5, font_size=12)
        dag = VGroup(g.edge_group, g.node_group, g.critical)
        rat = VGroup(*[VGroup(Text(a, font="DejaVu Sans Mono", font_size=20, color=CODE),
                              Text(p, font="DejaVu Sans Mono", font_size=20, color=HEAD)).arrange(RIGHT, buff=0.3)
                       for a, p in (("a0", "p22"), ("a1", "p24"), ("a2", "p23"))]).arrange(DOWN, buff=0.12)
        ring = RobRing(16, inner=0.7, outer=1.1)
        for i in range(10):
            ring.slots[i].set_fill([CTRL, FUNC, DATA][i % 3], opacity=0.8)
        L = load("limits")
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 32, 8], x_length=3.0, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        curve = VGroup(ax, VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [ax.c2p(k, v) for k, v in enumerate(L["curves"]["inf"])]),
                       VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(k, v) for k, v in enumerate(L["perfect_branches"]["2048"])]))
        r = load("spectre")["rounds"][0]
        k80 = int(np.argmin(r))
        probe = VGroup(VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [[k * 0.012, v * 0.025, 0] for k, v in enumerate(r)]), Dot([k80 * 0.012, r[k80] * 0.025, 0], radius=0.07,
                                                                         color=YES))
        job = load("job")
        led = ledger_table(job["ledger"], font_size=18, row_h=0.4, label_width=1.8, bar_width=3.0)
        tiles = Group(
            tile(dag, r"the dataflow limit", HEAD),
            tile(rat, r"renaming", CTRL),
            tile(ring, r"the reorder buffer", DATA),
            tile(curve, r"the ILP wall: \ branches", NO),
            tile(probe, r"Spectre, \ on our core", INF),
            tile(led, rf"the Job: \ ledger row 2", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Out of Order", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "This part connected dependency graphs to scheduling under stated latencies and resources, then "
            "separated register-name hazards from real value dependencies. We followed scoreboards, producer tags "
            "and precise architectural retirement, and checked a functional out-of-order model against the emulator "
            "on finite tests. Trace-oracle studies exposed the importance of their own knowledge, resource and "
            "ordering assumptions. A simulated Spectre gadget showed that squashed architectural work can leave "
            "observable cache effects, while two mitigations stopped that supplied witness under the model's rules. "
            "Finally, passage simulations supported a fitted full-corpus ledger projection at an assumed clock. "
            "Each conclusion travels with that evidence and scope."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"a window big enough to hide a miss \ $\to$ \ caches", [9]),
            (r"the ILP wall, \ and power \ $\to$ \ many cores, \ vectors", [10]),
            (r"static scheduling, \ software pipelining", [13]),
            (r"the length test no predictor can learn \ $\to$ \ better algorithms", [16, 17]),
            (r"loads and stores in a different order \ $\to$ \ memory models", [33]),
            (r"Spectre, \ Meltdown, \ side channels", [31, 32, 55]),
            (r"VLIW's second life", [60]),
        ], font_size=25)
        with self.voiceover(
            "These ideas return in several later parts. Larger windows interact with cache misses and memory-level "
            "parallelism in Part 9. Width, energy and multiple cores interact in Part 10. Static scheduling and "
            "software pipelining return with compiler transformations. The Job's repeated length checks motivate "
            "different data structures and algorithms; a measured predictor's difficulty does not prove a branch "
            "unlearnable. Reordering loads and stores connects to concurrency and memory models, where "
            "single-thread correctness and inter-thread visibility are different questions. The simulated security "
            "example leads into threat models and operating-system defenses, and static scheduling reappears in "
            "specialized hardware. The common habit is to connect a mechanism to a measured workload and explicit "
            "assumptions."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"CPU design teams", r"Apple, \ Arm, \ AMD, \ Intel, \ Qualcomm: \ predictors, \ schedulers and "
                                  r"windows, \ tuned on simulators like ours, \ at scale"),
            (r"performance tuning", r"\texttt{perf stat}: \ IPC, \ branch-misses, \ machine clears; \ "
                                    r"top-down analysis of where slots go"),
            (r"Spectre mitigations", r"\texttt{array\_index\_nospec}, \ retpolines, \ KPTI in kernels; \ site "
                                     r"isolation in browsers; \ SMT policy in clouds"),
            (r"open cores", r"BOOM and XiangShan: \ out-of-order RISC-V cores you can read and run"),
            (r"simulators", r"gem5, \ ChampSim: \ the tools architecture research uses"),
        ])
        with self.voiceover(
            "In practice, use implementation manuals and measurements together. Linux perf and top-down analysis "
            "expose supported event categories when hardware and permissions allow, but event meanings differ "
            "across cores. Production processors combine related scheduling ideas with many details omitted by "
            "Pebble. BOOM and other open designs let you inspect an implementation, while gem5 and trace simulators "
            "answer different modeling questions. Compiler and kernel hardening can mitigate particular speculative "
            "attacks under specified conditions; their names are not blanket security guarantees. When a counter, "
            "simulator or diagram supports a claim, state what it measures and what assumptions connect that "
            "measurement to the question."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Draw the dataflow graph of \ \texttt{lw a0, 0(s0)}; \ \texttt{lw a1, 4(s0)}; \ \texttt{add a2, a0, a1}; \ "
            r"\texttt{mul a3, a2, a2}; \ \texttt{add a4, a0, a3} \ (load 2, \ mul 3, \ add 1). \ Find $N$, $A$ and $L$. Compare start-slot schedules with "
            r"$\max(\lceil N/W\rceil,L)\le T_W$; separately test Graham\textquotesingle s weighted-work bound.",
            r"Rename the textbook example of chapters 3 and 4 into physical registers \ \texttt{p10, p11, \dots}. \ "
            r"Which dependences survive?",
            r"A core mispredicts once every 40 instructions, \ has CPI 0.3 with perfect prediction \ and a 15-cycle "
            r"penalty in a defined accounting model. What is its CPI? Can this alone determine ROB occupancy?",
            r"For unsigned $x$ and a nonempty array of size $2^k$, compare the dependency mask with "
            r"\texttt{x \& (size - 1)}. Which indices reach memory, and how does each handle invalid requests?",
            r"\textit{Build.} \ Part 7's problem 5 hoisted one load to hide a bubble, \ saving 4.4\% on the pipeline. \ "
            r"Make the same change and run chapter 1 on our core. \ What does it save now, \ and why?",
            r"$\bigstar$ \textit{Research.} \ Our control-shadow rule blocks this decoder, costing 3.5\% on chapter 1. Does it block "
            r"every speculative leak through the cache in our model? \ Find a program where it costs over 30\%, \ "
            r"and a rule that blocks the same leaks for less.",
        ], font_size=22)
        with self.voiceover(
            "The exercises ask you to build dependency schedules, distinguish instruction-count start limits from "
            "weighted processing-work bounds, and rename live register versions. Treat the CPI penalty calculation "
            "as a defined accounting model rather than a universal causal law. Before hoisting a load, prove its "
            "address and exception safety. For the research exercise, define protected data, public inputs, "
            "permitted observations and a non-speculative baseline, then search for a counterexample to our "
            "control-shadow rule. A finite successful test and a general security proof are different deliverables."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 9, \ The Memory Hierarchy", font_size=42).to_edge(UP, buff=0.6)
        bars = VGroup(*[Rectangle(width=0.9, height=h, stroke_width=0, fill_color=c, fill_opacity=0.8)
                        for h, c in ((0.15, YES), (0.4, DATA), (1.1, CTRL), (3.2, NO))]).arrange(RIGHT, buff=0.5,
                                                                                               aligned_edge=DOWN)
        names = VGroup(*[label(t, font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.12) for t, b in
                         zip((r"L1", r"L2", r"L3", r"DRAM"), bars)])
        fig = VGroup(bars, names).move_to(DOWN * 0.2)
        q = label("illustrative latency hierarchy; \\ core-cycle costs depend on the system", font_size=28,
                  color=HEAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Next, the memory hierarchy. Part 7 assigned illustrative memory delays; physical DRAM latency in core "
            "cycles depends on clock, configuration and access pattern. Part 9 studies caches, locality and the "
            "Job's miss-rate curves, and measures a latency staircase on this host. It also develops data-movement "
            "bounds for classical matrix multiplication under a specified computation model and limited fast "
            "memory. Those assumptions matter: a bound for one algorithmic model is not automatically a theorem "
            "about every possible matrix multiplication algorithm."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(names))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hennessy and Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed., ch. 3",
             r"Shen and Lipasti, \textit{Modern Processor Design}, ch. 4 to 9",
             r"Thornton, \textit{Design of a Computer: The Control Data 6600} (1970)",
             r"Fog, \textit{The microarchitecture of Intel, AMD and VIA CPUs} (updated yearly)"],
            [r"Tomasulo, ``An efficient algorithm for exploiting multiple arithmetic units'', IBM J. R\&D (1967)",
             r"Smith and Pleszkun, ``Implementation of precise interrupts in pipelined processors'', ISCA (1985)",
             r"Wall, ``Limits of instruction-level parallelism'', ASPLOS (1991)",
             r"Patterson and Ditzel, ``The case for the reduced instruction set computer'' (1980)",
             r"Fisher, ``Trace scheduling'' (1981); \ Lam, ``Software pipelining'', PLDI (1988)",
             r"Tullsen, Eggers and Levy, ``Simultaneous multithreading'', ISCA (1995)",
             r"Chrysos and Emer, ``Memory dependence prediction using store sets'', ISCA (1998)",
             r"Kocher et al., ``Spectre attacks'', S\&P (2019); \ Lipp et al., ``Meltdown'', USENIX Security (2018)",
             r"Lipasti, Wilkerson and Shen, ``Value locality and load value prediction'', ASPLOS (1996)",
             r"Yu et al., ``Speculative taint tracking'', MICRO (2019); \ Guarnieri et al., ``Spectector'', S\&P (2020)",
             "Loughlin et al., ``Dolma: Securing speculation with the principle of transient non-observability'', USENIX Security (2021)",
             "Daniel et al., ``ProSpeCT: Provably secure speculation for the constant-time policy'', USENIX Security (2023)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
