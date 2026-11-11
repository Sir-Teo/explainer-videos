from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, STAGE_COLOR,
                                  STAGES, YES, PipeChart, box, fmt, load, mono)


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
        il = load("ironlaw")
        law = MathTex(r"T = N \times \text{CPI} \times t_{\text{clk}}", font_size=40, color=HEAD)
        st = load("stages")["stages"]
        bars = VGroup(*[Rectangle(width=0.5, height=1.8 * st[s]["ps"] / 1130, stroke_width=0,
                                  fill_color=STAGE_COLOR[s], fill_opacity=0.8) for s in STAGES]).arrange(
            RIGHT, buff=0.12, aligned_edge=DOWN)
        bars.add(*[label(s, font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.08) for s, b in zip(STAGES, bars)])
        pc = PipeChart(load("charts")["loaduse"], cycles=10, cw=0.3, ch=0.3, font_size=9, label_size=11,
                       label_width=1.6, max_rows=6)
        pc_all = VGroup(pc.heads, *pc.rows.values(), *pc.columns.values())
        fsm = VGroup(*[Circle(radius=0.3, color=c, stroke_width=3) for c in (NO, NO, YES, YES)]).arrange(RIGHT,
                                                                                                    buff=0.35)
        fsm.add(*[MathTex(t, font_size=22, color=GREY_A).move_to(c) for t, c in zip(("00", "01", "10", "11"), fsm)])
        fsm.add(*[Arrow(fsm[k].get_right(), fsm[k + 1].get_left(), buff=0.03, stroke_width=2, color=GREY_B,
                        max_tip_length_to_length_ratio=0.3) for k in range(3)])
        w = load("perceptron")["the Job, chapter 1"]["weights"]
        perc = VGroup(*[Rectangle(width=0.16, height=0.03 + 1.5 * abs(x) / 40, stroke_width=0,
                                  fill_color=YES if x > 0 else NO, fill_opacity=0.85) for x in w]).arrange(
            RIGHT, buff=0.05, aligned_edge=DOWN)
        d = load("depth")
        ax = Axes(x_range=[0, 60, 20], y_range=[0, 2700, 1000], x_length=3.0, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        curve = VGroup(ax, VMobject(color=CLOCK, stroke_width=3).set_points_as_corners(
            [ax.c2p(k, t) for k, t in zip(d["k"], d["time_ps"]) if k <= 60]))
        job = load("job")
        led = ledger_table(job["ledger"], font_size=18, row_h=0.4, label_width=1.8, bar_width=3.0)
        tiles = Group(
            tile(law, rf"the iron law: \ {il['speedup']:.2f}$\times$", HEAD),
            tile(bars, r"five stages, \ one clock", DATA),
            tile(pc_all, r"hazards, \ stalls, \ forwarding", FUNC),
            tile(fsm, r"two-bit counters", CTRL),
            tile(perc, r"a perceptron, \ predicting", YES),
            tile(led, r"the Job: \ ledger row 1", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Pipelines", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built: the performance equation; a five-stage functional pipeline; and an explicitly assumed "
            "clock budget. We visualized hazards, forwarding, load-use stalls, and precise architectural exceptions, "
            "with finite emulator comparisons. We measured counter, TAGE and perceptron implementations on specified "
            "traces, without claiming an absolute prediction limit. Short Job passages were simulated cycle by cycle; "
            "the full-corpus ledger row is a fitted projection, nearly twice as fast under its assumptions. Multiple "
            "instructions overlap, while this one-wide pipeline retires them in order."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            ('overlapping instructions, one-wide in-order retirement: the next limit', [8]),
            (r"the 1000 ps memory stages \ $\to$ \ caches", [9]),
            (r"the power wall \ $\to$ \ multicore and SIMD", [10]),
            (r"the load-use bubble \ $\to$ \ instruction scheduling", [13]),
            (r"speculation, \ and the traces it leaves: \ Spectre", [8, 55]),
            (r"Amdahl's law, \ for parallel programs and for whole systems", [10, 39, 48]),
        ], font_size=26)
        with self.voiceover(
            'Where this comes back. Our pipeline overlaps instructions but retires at most one per cycle in order; '
            "Part 8 lets independent instructions execute out of order. The assumed memory delays lead to Part 9's "
            'caches. Power constraints motivate multicore and SIMD. Instruction scheduling can hide some load-use '
            "bubbles when movement is safe. Speculation's microarchitectural traces connect to Spectre, and Amdahl's "
            'fixed-work accounting returns in parallel and distributed systems.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"\texttt{perf stat}", r"cycles, \ instructions, \ IPC, \ branch-misses: \ the iron law, \ measured on "
                                    r"your own program"),
            (r"profilers", r"\texttt{perf record}, \ VTune, \ Instruments: \ find the $p$ of Amdahl's law first"),
            ('hot-loop choices', r"\texttt{cmov}, \ \texttt{csel}; \ \texttt{\_\_builtin\_expect}; \ sorting or "
                                  r"partitioning data before a hot loop"),
            (r"microarchitecture docs", r"Agner Fog's tables, \ uops.info, \ vendor optimization manuals: \ "
                                        r"pipeline depths and penalties"),
            (r"processor design", r"open RISC-V cores \ (Rocket, \ BOOM, \ CVA6) \ and their branch predictors, \ "
                                  r"readable on GitHub"),
        ])
        with self.voiceover(
            "In practice, measure first. Linux perf stat can report supported cycle, instruction and branch events "
            "when permissions allow; results depend on the processor and operating system. Profilers help find "
            "baseline time shares, and wall time differs from processor time. Conditional moves, safe if-conversion "
            "and data reordering can help hot loops, but measure their extra work too. Vendor manuals and Agner Fog's "
            "tables provide useful measured and documented costs, not every core's complete internal pipeline. "
            "Open-source Rocket and BOOM offer concrete predictor implementations to inspect."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Draw the pipeline chart for \ \texttt{lw t0, 0(a0)}; \ \texttt{add t1, t0, t0}; \ "
            r"\texttt{sw t1, 4(a0)} \ with forwarding. \ Where is the bubble, \ and which paths carry values?",
            r"20\% of instructions are branches, \ 60\% of them taken. \ Predict-not-taken costs 2 cycles per taken "
            r"branch; \ a predictor that is 95\% right costs 2 per mistake. \ What CPI does each give?",
            r"Minimize $T(k) = (t/k + o)\,(1 + b\,(k - 1))$ \ to show $k^* = \sqrt{t(1-b)/(b\,o)}$. \ With "
            r"$t = 2560$ ps \ and $o = 70$ ps, \ what is $k^*$ for $b = 0.01$ \ and for $b = 0.1$?",
            r"80\% of a program can run in parallel. \ What speedup do 4, \ 16 and infinitely many processors give? "
            r"\ What if the problem grows so the serial time stays fixed \ (Gustafson)?",
            '\\textit{Build.} Schedule the Job scan loop to hide a load-use bubble. \\\\ First prove any hoisted load is safe in this layout; \\\\ then measure cycles, CPI and output on chapter 1.',
            '$\\bigstar$ \\textit{Research.} Design a predictor with at most 64 KiB of total state. \\\\ Fix train/tune/heldout chapters; exclude future test labels. \\\\ Report heldout accuracy, full bit accounting and remaining errors.',
        ], font_size=22)
        with self.voiceover(
            "Six problems are in the notes. The fifth schedules the Job's loop, with a required proof that a hoisted "
            "load is safe under this memory layout. The starred exercise designs a predictor within sixty-four "
            "kibibytes of fully accounted state. Choose training and tuning chapters first, then evaluate untouched "
            "chapters with no encoded future outcomes. A known trace can be memorized, so replay accuracy alone is not "
            "the research question. Report the protocol, remaining misses and what generalizes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 8, \ Out of Order", font_size=42).to_edge(UP, buff=0.6)
        order = VGroup(*[box(1.9, 0.7, t, c, 22) for t, c in ((r"\texttt{lw a0}", DATA), (r"\texttt{add a1, a0}", INF),
                                                              (r"\texttt{addi t0}", YES), (r"\texttt{xor t1}", YES))])
        order.arrange(RIGHT, buff=0.25).move_to(UP * 0.4)
        slots = [m.get_center() for m in order]
        q = label(r"if one instruction waits, \ why should the ones after it?", font_size=30, color=HEAD).to_edge(
            DOWN, buff=0.8)
        with self.voiceover(
            "Next time: our pipeline overlaps instructions, but executes and retires in order. When an older operation "
            "blocks progress, independent younger work may still be ready. Part 8 studies scheduling that work with "
            "register renaming and a reorder buffer to preserve precise architectural state. Modern cores can keep "
            "many instructions in flight. The 2018 Spectre disclosures also showed how some speculative activity can "
            "leak information through microarchitectural effects, under specific attack conditions."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in order], lag_ratio=0.2))
            self.play(order[2].animate(path_arc=-PI / 2).move_to(slots[0]),
                      order[3].animate(path_arc=-PI / 2).move_to(slots[1]),
                      order[0].animate.move_to(slots[2]).set_opacity(0.45),
                      order[1].animate.move_to(slots[3]).set_opacity(0.45), run_time=1.5)
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hennessy and Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed., ch. 1, 3, App. C",
             r"Patterson and Hennessy, \textit{Computer Organization and Design, RISC-V Edition}, ch. 1 and 4",
             r"Shen and Lipasti, \textit{Modern Processor Design}, ch. 2 and 9",
             r"Harris and Harris, \textit{Digital Design and Computer Architecture}, ch. 7",
             r"Fog, \textit{The microarchitecture of Intel, AMD and VIA CPUs} (updated yearly)"],
            [r"Amdahl, ``Validity of the single processor approach'', AFIPS (1967)",
             r"Smith, ``A study of branch prediction strategies'', ISCA (1981)",
             r"Yeh and Patt, ``Two-level adaptive training branch prediction'', MICRO (1991)",
             r"McFarling, ``Combining branch predictors'', DEC WRL TN-36 (1993)",
             r"Jim\'enez and Lin, ``Dynamic branch prediction with perceptrons'', HPCA (2001)",
             r"Seznec and Michaud, ``A case for (partially) tagged geometric history length branch prediction'' (2006)",
             r"Chen, Coffey and Mudge, ``Analysis of branch prediction via data compression'', ASPLOS (1996)",
             r"Zangeneh, Pruett, Lym and Patt, ``BranchNet'', MICRO (2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
