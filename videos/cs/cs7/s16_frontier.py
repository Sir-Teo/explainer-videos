from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): how close do predictors come to the limit of what history can
    tell them, and what can a perceptron never learn?"""

    def construct(self):
        self.card()
        self.storage()
        self.mixing()
        self.xor()
        self.now()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the limits of prediction", r"How good could a branch predictor be?",
                            lit=(1991, 1996, 2016, 2020), extra=((1991, r"Wall's limits of ILP"), (1996, r"prediction as compression"), (2016, r"TAGE-SC-L"), (2020, r"BranchNet")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: the limits of prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def storage(self):
        d = load("frontier")
        two = load("predictors")["table"]["the Job, chapter 1"]["rows"]["2-bit"]["accuracy"]
        head = label(r"A limit study: \ accuracy against storage", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-1, 3, 1], y_range=[91, 98, 1], x_length=7.4, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax.y_axis.add_numbers(list(range(92, 99, 2)), font_size=18, num_decimal_places=0)
        xt = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(ax.c2p(k, 91), DOWN, buff=0.15)
                      for k, t in zip(range(-1, 4), (r"0.1", r"1", r"10", r"100", r"1000"))])
        xl = note(r"storage, \ kilobytes \ (log scale)", font_size=20).next_to(xt, DOWN, buff=0.12)
        yl = note(r"the Job's branches predicted right, \ \%", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax,
                                                                                                          LEFT)
        lg = np.log10
        tage = d["tage"]
        tpts = [ax.c2p(lg(r["kb"]), 100 * r["accuracy"]) for r in tage]
        tline = VMobject(color=YES, stroke_width=3).set_points_as_corners(tpts)
        tdots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in tpts])
        tl = label(r"TAGE \ (ours, simplified)", font_size=20, color=YES).next_to(tpts[3], UP + LEFT, buff=0.1)
        per = d["perceptron"]
        ppts = [ax.c2p(lg(r["kb"]), 100 * r["accuracy"]) for r in per]
        pline = VMobject(color=FUNC, stroke_width=3).set_points_as_corners(ppts)
        pdots = VGroup(*[Dot(p, radius=0.06, color=FUNC) for p in ppts])
        pl = label(r"perceptron", font_size=20, color=FUNC).next_to(ppts[-1], DOWN, buff=0.15)
        tb = Dot(ax.c2p(lg(0.25), 100 * two), radius=0.07, color=GREY_A)
        tbl = label(r"2-bit", font_size=18, color=GREY_A).next_to(tb, UP, buff=0.1)
        top = 100 * d["ppm"]["accuracy"]
        ppm = DashedLine(ax.c2p(-1, top), ax.c2p(3, top), color=HEAD, stroke_width=2.5)
        ppml = label(rf"unlimited storage \ (PPM): \ {top:.1f}\%", font_size=20, color=HEAD).next_to(
            ax.c2p(3, top), UP, buff=0.1).align_to(ax.c2p(3, top), RIGHT)
        side = VGroup(
            label(r"a limit study removes one constraint \\ and measures what is left \ (Wall, \ 1991)",
                  font_size=20, color=GREY_A),
            label(rf"the Job: \ {100 * (1 - two):.1f}\% wrong $\to$ {100 * (1 - tage[2]['accuracy']):.1f}\% "
                  rf"$\to$ {100 - top:.1f}\%", font_size=20, color=COST),
            label(r"the perceptron stops at 92.5\%: \\ more weights do not help it", font_size=20, color=FUNC),
            label(r"the Championship Branch Prediction \\ has an unlimited track too", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        with self.voiceover(
            "The research question behind this part is simple to state: how good could branch prediction be? "
            "Architects answer such questions with a limit study, an idea David Wall made famous in 1991: take away one "
            "constraint, here the size of the predictor, and measure how much is left to gain. <bookmark mark='a'/> "
            "Here is the Job's first chapter, a quarter of a million branches. A table of two-bit counters, a quarter "
            "of a kilobyte, gets ninety-one percent right. <bookmark mark='b'/> Our TAGE climbs as it is given more "
            "storage: ninety-four percent at nine kilobytes, ninety-six at half a megabyte. <bookmark mark='c'/> The "
            "perceptron does not climb. More tables, more weights, the same ninety-two and a half percent: whatever "
            "it cannot learn is not a matter of size. <bookmark mark='d'/> And the dashed line is a predictor with no "
            "storage limit at all, which we will meet in a moment: ninety-seven and a half percent. On this program, "
            "more than half of TAGE's remaining mistakes at nine kilobytes are the price of its budget; the rest are "
            "beyond this kind of predictor altogether. The Championship Branch Prediction, held every few years, has "
            "a track for exactly this question, with no storage limit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(tb), FadeIn(tbl))
            vo.wait_until("b")
            self.play(Create(tline), FadeIn(tdots), FadeIn(tl), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(pline), FadeIn(pdots), FadeIn(pl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ppm), FadeIn(ppml))
            self.play(FadeIn(side[1]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mixing(self):
        d = load("frontier")
        head = label(r"No single history length is enough", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 32, 8], y_range=[91, 98, 1], x_length=6.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(
            LEFT * 2.6 + DOWN * 0.4)
        xl = note(r"history length $h$", font_size=20).next_to(ax, DOWN, buff=0.35)
        yl = note(r"\% right", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        sg = d["single"]
        on = VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["h"], 100 * r["online"]) for r in sg])
        hi = DashedVMobject(VMobject(color=GREY_B, stroke_width=2).set_points_as_corners(
            [ax.c2p(r["h"], 100 * r["hindsight"]) for r in sg]), num_dashes=40)
        best = max(sg, key=lambda r: r["online"])
        bd = Dot(ax.c2p(best["h"], 100 * best["online"]), color=DATA, radius=0.08)
        onl = label(rf"one unlimited table per length: \ best {100 * best['online']:.1f}\% at $h = {best['h']}$",
                    font_size=18, color=DATA).move_to(ax.c2p(16, 91.5))
        hil = label(r"with hindsight: \ meaningless", font_size=18, color=GREY_B).next_to(
            ax.c2p(32, 100 * sg[-1]["hindsight"]), LEFT, buff=0.15).shift(UP * 0.25)
        ppm = 100 * d["ppm"]["accuracy"]
        tage = 100 * d["tage"][2]["accuracy"]
        lines = VGroup(DashedLine(ax.c2p(0, ppm), ax.c2p(32, ppm), color=HEAD, stroke_width=2),
                       DashedLine(ax.c2p(0, tage), ax.c2p(32, tage), color=YES, stroke_width=2))
        ll = VGroup(label(rf"PPM, \ every length at once: \ {ppm:.1f}\%", font_size=18, color=HEAD).next_to(
            lines[0], UP, buff=0.05),
            label(rf"TAGE, \ 9 KB: \ {tage:.1f}\%", font_size=18, color=YES).next_to(lines[1], UP, buff=0.05))
        side = VGroup(
            label(r"long histories see sharper patterns \\ but must learn each context from scratch", font_size=20,
                  color=GREY_A),
            label(r"PPM \ (Cleary and Witten, 1984): \\ use the longest context seen before, \\ fall back to shorter "
                  r"ones", font_size=20, color=HEAD),
            label(r"predicting a branch is compressing its outcomes \\ (Chen, Coffey and Mudge, 1996); \\ TAGE is a "
                  r"PPM that fits in a chip", font_size=20, color=YES),
            label(rf"{fmt(d['ppm']['contexts'])} contexts stored, \ no aliasing", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.1)
        with self.voiceover(
            "Storage is not the whole story. Try the obvious ideal first: one table, as large as it needs to be, with a "
            "counter for every branch and every pattern of the last h outcomes. <bookmark mark='a'/> Its "
            "accuracy rises with h, peaks at about ninety-two point seven percent for twelve branches of history, and "
            "falls. A longer history sees sharper patterns, but each pattern is a new context that has to be learned "
            "from scratch, and most of them are seen only a few times. It is the trade-off between bias and variance, "
            "inside a processor. <bookmark mark='b'/> The dashed grey curve is the same table judged with hindsight, "
            "each context predicted by its majority over the whole trace. It rises forever, because with enough "
            "history every context is unique. Limit studies must be causal, or they measure nothing. "
            "<bookmark mark='c'/> The winner uses every length at once: look up the longest context that has been seen "
            "before, and fall back to shorter ones when it has not. That is prediction by partial matching, an "
            "algorithm from data compression, and in 1996 Chen, Coffey and Mudge showed that predicting branches and "
            "compressing their outcomes are the same problem. <bookmark mark='d'/> TAGE, with its geometric history "
            "lengths, is a partial-matching predictor small enough to build."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(on), FadeIn(onl), run_time=2.0)
            self.play(FadeIn(bd), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(hil), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[0]), FadeIn(ll[0]), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(lines[1]), FadeIn(ll[1]), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def xor(self):
        d = load("frontier")
        head = label(r"What a perceptron cannot learn", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1], x_length=3.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C}).move_to(LEFT * 4.3 + UP * 0.3)
        axl = VGroup(label(r"A", font_size=22, color=GREY_B).next_to(ax.x_axis.get_right(), DOWN, buff=0.12),
                     label(r"C", font_size=22, color=GREY_B).next_to(ax.y_axis.get_top(), LEFT, buff=0.12))
        pts = VGroup()
        for a in (-1, 1):
            for c in (-1, 1):
                taken = a != c
                pts.add(Dot(ax.c2p(a, c), radius=0.14, color=YES if taken else NO))
        lines = [Line(ax.c2p(-1.6, -1.6 + 3.2 * t), ax.c2p(1.6, 1.6 - 3.2 * t), color=FUNC, stroke_width=2.5)
                 for t in (0.1, 0.5, 0.9)]
        line = lines[0].copy()
        rule = MathTex(r"B = A \oplus C", font_size=34, color=HEAD).next_to(ax, UP, buff=0.25)
        cap = label(r"no line puts the green points on one side \\ (Minsky and Papert, \ 1969)", font_size=20,
                    color=FUNC).next_to(ax, DOWN, buff=0.55)
        names = [("2-bit", GREY_B), ("perceptron", FUNC), ("gshare", DATA), ("TAGE", YES),
                 ("PPM, unlimited", HEAD)]
        bars = VGroup()
        for k, (n, c) in enumerate(names):
            v = d["parity"][n]
            y = 1.6 - 0.62 * k
            r = Rectangle(width=4.0 * v, height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.7).move_to(
                [0.9 + 2.0 * v, y, 0])
            nl = label(n, font_size=20, color=c).next_to([0.8, y, 0], LEFT, buff=0.1)
            vl = label(rf"{100 * v:.0f}\%", font_size=20, color=GREY_A).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(nl, r, vl))
        bh = label(r"branch B of the parity benchmark, \% right", font_size=20, color=GREY_A).next_to(
            bars, UP, buff=0.25)
        fix = VGroup(
            label(r"piecewise-linear and multiperspective perceptrons \ (Jim\'enez, \ 2005, \ 2016): "
                  r"\ many perceptrons per branch, \ chosen by path", font_size=20, color=GREY_A),
            label(r"TAGE-SC-L \ (Seznec, \ 2016): \ TAGE, \ then a perceptron-like corrector, \ then a loop "
                  r"predictor; \ each catches what the others miss", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The perceptron's plateau has a precise cause, the oldest theorem about neural networks. "
            "<bookmark mark='a'/> Here is a branch B whose outcome is the exclusive-or of two earlier branches, A and C. "
            "Draw the four cases with A across and C up: B is taken on one diagonal and not taken on the other. "
            "<bookmark mark='b'/> A perceptron predicts with the sign of a weighted sum, which is a straight line "
            "through this square, and no line puts both green points on one side and both red ones on the other. "
            "Minsky and Papert proved this in 1969, and the result is often blamed for a decade-long chill in neural "
            "network research. "
            "<bookmark mark='c'/> So we built the branch. In the parity benchmark the perceptron gets B right forty-"
            "nine percent of the time, no better than a two-bit counter or a coin, and its weights stay near zero, "
            "while gshare and TAGE, whose tables can hold any function of the history, get about ninety, and the "
            "unlimited predictor all but a few. <bookmark mark='d'/> Research since has combined the two kinds. "
            "Jiménez's piecewise-linear and multiperspective perceptrons give each branch many perceptrons, chosen by "
            "the path taken to reach it. Seznec's TAGE-SC-L, a winner of the 2016 championship, runs TAGE, then a "
            "perceptron-like statistical corrector, then a loop predictor, each catching what the others miss."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(axl))
            vo.wait_until("a")
            self.play(FadeIn(pts), Write(rule))
            vo.wait_until("b")
            self.play(Create(line))
            for ln in lines[1:]:
                self.play(Transform(line, ln), run_time=0.8)
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(bh), LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                                for b in bars], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(fix[0]))
            self.play(FadeIn(fix[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def now(self):
        head = label(r"Open questions", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{hard-to-predict branches.} \ A few static branches cause most of the remaining misses; "
                  r"\\ many depend on data, \ like the threshold loop.", font_size=21, color=GREY_A),
            label(r"\textbf{offline learning.} \ BranchNet \ (Zangeneh, Pruett, Lym and Patt, \ 2020) \ trains small "
                  r"convolutional networks \\ on a program's traces before it ships, \ for the branches TAGE cannot "
                  r"learn online.", font_size=21, color=DATA),
            label(r"\textbf{the front end at scale.} \ Data-centre programs have code footprints that overflow the "
                  r"predictor and the target buffer \\ (Kanev et al., \ 2015): \ the frontier is now capacity, \ not "
                  r"accuracy.", font_size=21, color=CTRL),
            label(r"\textbf{the true limit is unknown.} \ It is the entropy rate of a program's branch stream, \ given "
                  r"everything the machine could know: \\ every limit study, \ ours included, \ only bounds it from "
                  r"one side.", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        with self.voiceover(
            "Where the research stands. <bookmark mark='a'/> In modern predictors, a handful of static branches cause "
            "most of the remaining mistakes, and many of them depend on data, like the threshold loop of chapter "
            "fourteen. History cannot predict a coin. <bookmark mark='b'/> One line of work trains models offline: "
            "BranchNet, from Yale Patt's group in 2020, trains small convolutional networks on a program's traces before "
            "it ships, for exactly the branches TAGE cannot learn as it runs. <bookmark mark='c'/> Another is "
            "capacity. Data-centre programs have so much code that it overflows the predictor tables and the target "
            "buffer, and Google's profile of its own fleet in 2015 found the front end a major bottleneck. "
            "<bookmark mark='d'/> And the real limit is unknown. It is the entropy rate of the branch stream, given "
            "everything the machine could know, and every limit study, ours included, bounds it from one side only. "
            "The research problem in this part's set starts here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
