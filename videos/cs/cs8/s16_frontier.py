from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
                                  load, mono)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): can a machine beat the dataflow limit by predicting values,
    and can speculation be made safe, and at what cost?"""

    def construct(self):
        self.card()
        self.values()
        self.verdict_vp()
        self.secure()
        self.now()

    def card(self):
        card = chapter_card(15, r"Frontier: \ past the dataflow limit, \ safely",
                            r"Can a machine guess values, \ and can guessing be made safe?", lit=(1996, 2014, 2019),
                            extra=((1996, r"Lipasti: \ value prediction"), (2014, r"Perais and Seznec"),
                                   (2019, r"STT, \ NDA")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: past the dataflow limit, safely."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def values(self):
        d = load("frontier")
        head = label(r"Value prediction: \ guess what a load will return", font_size=34).to_edge(UP, buff=0.3)
        idea = VGroup(
            label(r"the critical path runs through loads: \ \texttt{lw t1} \ $\to$ \ \texttt{bne}", font_size=24,
                  color=GREY_A),
            label(r"guess the value, \ start the users now, \ check when the load arrives", font_size=24, color=HEAD),
            label(r"(Lipasti, \ Wilkerson and Shen, \ 1996: \ many loads return the same value as last time)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.35)
        th = d["thresholds"]
        base = d["vp"]["8/256"]["base"]
        oracle = d["vp"]["8/256"]["oracle"]
        keys = ["1", "2", "4", "8", "15"]
        ax = Axes(x_range=[0, 5, 1], y_range=[2.6, 4.2, 0.4], x_length=7.0, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.0 + DOWN * 1.6)
        ax.y_axis.add_numbers([2.6, 3.0, 3.4, 3.8], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(k, font_size=18, color=GREY_B).next_to(ax.c2p(i + 0.5, 2.6), DOWN, buff=0.12)
                      for i, k in enumerate(keys)])
        xl = note(r"confidence needed before guessing \ (correct in a row)", font_size=18).next_to(xt, DOWN, buff=0.1)
        bl = DashedLine(ax.c2p(0, base), ax.c2p(5, base), color=GREY_B, stroke_width=2)
        blt = label(rf"no prediction: \ {base:.2f}", font_size=18, color=GREY_B).next_to(bl, RIGHT, buff=0.1)
        ol = DashedLine(ax.c2p(0, oracle), ax.c2p(5, oracle), color=YES, stroke_width=2)
        olt = label(rf"every load guessed right: \ {oracle:.2f}", font_size=18, color=YES).next_to(ol, RIGHT, buff=0.1)
        pts = VGroup(*[Dot(ax.c2p(i + 0.5, th[k]["ipc"]), radius=0.08, color=NO) for i, k in enumerate(keys)])
        curve = VMobject(color=NO, stroke_width=3).set_points_as_corners([p.get_center() for p in pts])
        acc = VGroup(*[label(rf"{100 * th[k]['correct'] / th[k]['predicted']:.0f}\%", font_size=16, color=NO).next_to(
            pts[i], DOWN, buff=0.1) for i, k in enumerate(keys)])
        side = note("trace oracle: 8 starts/cycle; start distance 256; modeled control barriers \\\\ per-load stride predictions; red: IPC and conditional accuracy", font_size=17).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        with self.voiceover(
            "Value prediction changes the dependency model by guessing a load's result before it is verified. "
            "<bookmark mark='a'/> Dependents can tentatively use a predicted value, then correctness requires "
            "validation and recovery if it was wrong. This can pass a dependency bound derived for waiting on "
            "actual values because the assumptions changed. <bookmark mark='b'/> Here a per-load-PC stride "
            "predictor learns from the recorded trace, with a confidence threshold. It is an offline scheduling "
            "study, including trace-supplied inputs, not an implemented functional value-predicting core. <bookmark "
            "mark='c'/> At eight start slots, the no-value-prediction baseline is about three point three four IPC; "
            "an oracle that guesses every load correctly reaches about three point nine eight under the other "
            "retained assumptions. <bookmark mark='d'/> The real heuristic predicts only a subset and makes "
            "mistakes, so its schedules are slower than the baseline at the shown thresholds. Correctness, "
            "coverage, prediction availability, I/O ordering and recovery cost must all be addressed before "
            "translating this exercise into hardware."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(i) for i in idea], lag_ratio=0.4))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(side))
            vo.wait_until("c")
            self.play(Create(bl), FadeIn(blt), Create(ol), FadeIn(olt))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.2), Create(curve), FadeIn(acc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict_vp(self):
        d = load("frontier")
        head = label(r"What it would take", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label("benefit depends on accuracy, coverage, timing and recovery cost", font_size=26, color=HEAD),
            label("high-confidence prediction and recovery are design choices, \\ not a universal threshold", font_size=24,
                  color=GREY_A),
            label("this 8-slot trace study: \\ oracle value guesses improve IPC by 19\\%", font_size=24,
                  color=NO),
            label(r"open: \ which programs have values worth guessing, \ and can a core find them cheaply?",
                  font_size=26, color=YES),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Accuracy alone does not determine whether value prediction pays. <bookmark mark='a'/> Benefit depends "
            "on which loads are covered, when predictions arrive, how much dependent work they unlock, and the cost "
            "of validation and mistakes. There is no universal ninety-nine-percent threshold. <bookmark mark='b'/> "
            "High-confidence value-prediction work, including Perais and Seznec's 2014 research, studies particular "
            "mechanisms and recovery choices. Our simple scheduler is not a reproduction of those designs. "
            "<bookmark mark='c'/> In the shown eight-slot configuration, perfect load guesses improve this trace "
            "schedule by about nineteen percent, while the simple stride heuristic loses performance. Both "
            "statements are conditional on the rest of the scheduler's assumptions, including its prediction "
            "barriers and idealized memory information. <bookmark mark='d'/> A useful research question is which "
            "workload, coverage and recovery policy produces net benefit under a realistic functional model."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def secure(self):
        d = load("frontier")["secure"]
        sp = load("spectre")["mitigations"]
        head = label(r"Can speculation be made safe?", font_size=36).to_edge(UP, buff=0.35)
        rule = VGroup(
            label(r"a rule for our core \ (in the spirit of STT and NDA, \ 2019):", font_size=24, color=GREY_A),
            label(r"a load that completes in the shadow of an unresolved branch \\ keeps its value to itself until "
                  r"every older branch has executed", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.4)
        res = VGroup(
            label(r"supplied Spectre gadget: \ " + (r"no fast tested nonzero line" if all(
                x == 1 for x in sp["secure"]["output"]) else r"decoder still distinguishes a value"), font_size=26, color=YES),
            label(rf"chapter 1: \ IPC {d['plain_ipc']:.3f} \ $\to$ \ {d['secure_ipc']:.3f}: \ "
                  rf"{100 * d['cost']:.1f}\% slower", font_size=26, color=COST),
            label("other data sources and channels still need analysis; \\ no general proof here", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.8)
        with self.voiceover(
            "Our optional rule delays broadcasting a completed load's value while an older branch or indirect jump "
            "remains unresolved. <bookmark mark='a'/> That prevents dependent operations from using that value "
            "during the unresolved control speculation in this model. It is inspired by information-flow defenses, "
            "but does not implement complete STT or NDA algorithms. <bookmark mark='b'/> In the supplied Spectre "
            "experiment, the tested nonzero probe lines no longer reveal PEBBLE. This is a finite gadget result, "
            "not a proof of noninterference for every program or channel. <bookmark mark='c'/> On the Job chapter, "
            "model cycles increase from four hundred thirty-seven thousand five hundred eighty to four hundred "
            "fifty-three thousand one hundred twelve, about three point five percent. That cost is specific to this "
            "trace and implementation. <bookmark mark='d'/> Fault speculation, memory-alias speculation, "
            "preexisting register secrets, stores and other channels require separate analysis. We must state the "
            "attacker, permitted observations and protected data before making a security guarantee."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rule))
            vo.wait_until("a")
            for mk, r in zip("bcd", res):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def now(self):
        head = label(r"Open questions", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label("ProSpeCT (2023): \\ formal constant-time-policy result and RISC-V prototype", font_size=23, color=YES),
            label("Dolma (2021): \\ transient non-observability; \\ threat-model-specific cost",
                  font_size=23, color=COST),
            label(r"other channels: \ not only the cache, \ but ports, \ predictors, \ power", font_size=23,
                  color=NO),
            label("the 2400-IPC oracle supplies future information; \\ hardware feasibility is separate", font_size=23, color=HEAD),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Secure speculation is an active research area with formal results under explicit models. <bookmark "
            "mark='a'/> ProSpeCT, published in 2023, gives a formal processor model and a constant-time-policy "
            "security proof, plus a RISC-V hardware prototype. Its theorem has specified program and observation "
            "assumptions; it is not a proof that arbitrary physical systems have no side channels. <bookmark "
            "mark='b'/> Dolma's 2021 transient-non-observability design examines broader data sources and "
            "store-related attacks, with overheads measured on its chosen workloads and threat models. Such papers "
            "show why a successful gadget test is weaker than a stated security theorem. <bookmark mark='c'/> "
            "Compare like observations, attacker powers, protected inputs and baseline behavior before comparing "
            "guarantees or costs. There is no single minimum security overhead without those definitions. <bookmark "
            "mark='d'/> Likewise, the earlier oracle IPC is a trace-and-assumption result, not an implementation "
            "target guaranteed by a universal parallelism theorem. Good research turns an explicit model into a "
            "precise claim, then tests where that claim stops applying."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
