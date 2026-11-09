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
        head = label('One trace: empirical accuracy versus nominal table payload', font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-1, 3, 1], y_range=[91, 98, 1], x_length=7.4, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax.y_axis.add_numbers(list(range(92, 99, 2)), font_size=18, num_decimal_places=0)
        xt = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(ax.c2p(k, 91), DOWN, buff=0.15)
                      for k, t in zip(range(-1, 4), (r"0.1", r"1", r"10", r"100", r"1000"))])
        xl = note('nominal table payload, KiB (log scale)', font_size=20).next_to(xt, DOWN, buff=0.12)
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
        ppml = label(rf"growing context tables, max $h=64$ (PPM): \ {top:.1f}\%", font_size=20, color=HEAD).next_to(
            ax.c2p(3, top), UP, buff=0.1).align_to(ax.c2p(3, top), RIGHT)
        side = VGroup(
            label('table payload estimates exclude history, \\\\ validity and implementation overhead',
                  font_size=20, color=GREY_A),
            label(rf"the Job: \ {100 * (1 - two):.1f}\% wrong $\to$ {100 * (1 - tage[2]['accuracy']):.1f}\% "
                  rf"$\to$ {100 - top:.1f}\%", font_size=20, color=COST),
            label('this tested perceptron plateaus; \\\\ size alone does not establish its cause', font_size=20, color=FUNC),
            label('one trace, online training; \\\\ compare algorithms, not an absolute ceiling', font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        with self.voiceover(
            "What do these experiments establish? This is an empirical comparison on one trace, not a prediction "
            "limit. <bookmark mark='a'/> The Job chapter supplies about a quarter-million branch outcomes. The two-bit "
            "table is our baseline. <bookmark mark='b'/> Our simplified TAGE improves as its arrays grow. The "
            "horizontal axis estimates nominal packed table payload, excluding history, validity and implementation "
            "overhead; it is not Python memory or a complete hardware budget. <bookmark mark='c'/> The perceptron "
            "changes little over the tested sizes. A plateau alone does not prove a representation ceiling. <bookmark "
            "mark='d'/> The dashed PPM result uses a different algorithm with unbounded context-table growth but a "
            "bounded set of history lengths. Its advantage cannot be assigned entirely to storage, and its remaining "
            "errors are not proved impossible. Compare algorithms under a defined training protocol before drawing "
            "stronger conclusions."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
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
        head = label('History length and online learning on this trace', font_size=36).to_edge(UP, buff=0.3)
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
        hil = label('hindsight majority: offline oracle for these features', font_size=18, color=GREY_B).next_to(
            ax.c2p(32, 100 * sg[-1]["hindsight"]), LEFT, buff=0.15).shift(UP * 0.25)
        ppm = 100 * d["ppm"]["accuracy"]
        tage = 100 * d["tage"][2]["accuracy"]
        lines = VGroup(DashedLine(ax.c2p(0, ppm), ax.c2p(32, ppm), color=HEAD, stroke_width=2),
                       DashedLine(ax.c2p(0, tage), ax.c2p(32, tage), color=YES, stroke_width=2))
        ll = VGroup(label(rf"PPM, \ configured lengths up to 64: \ {ppm:.1f}\%", font_size=18, color=HEAD).next_to(
            lines[0], UP, buff=0.05),
            label(rf"TAGE, \ nominal 9 KiB: \ {tage:.1f}\%", font_size=18, color=YES).next_to(lines[1], UP, buff=0.05))
        side = VGroup(
            label(r"long histories see sharper patterns \\ but must learn each context from scratch", font_size=20,
                  color=GREY_A),
            label('PPM-style backoff among configured lengths, \\\\ up to 64 outcomes; context tables may grow', font_size=20, color=HEAD),
            label('probabilistic prediction relates to code length; \\\\ entropy is not directly an accuracy ceiling', font_size=20, color=YES),
            label(rf"{fmt(d['ppm']['contexts'])} contexts stored, \ no aliasing", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.1)
        with self.voiceover(
            "Try a table for each chosen history length. <bookmark mark='a'/> Predict before updating on each outcome. "
            "In this run, online accuracy peaks near twelve outcomes of history, then falls as contexts recur less "
            "often. This is an observed learning trade-off, not a universal optimum. <bookmark mark='b'/> The dashed "
            "curve instead uses each context's majority label from the entire evaluated trace. That is an offline "
            "oracle for this feature class; it uses future labels and is not a deployable online predictor. It is "
            "bounded by one hundred percent. <bookmark mark='c'/> Our PPM-style model backs off among its configured "
            "lengths, up to sixty-four outcomes, and stores the shown number of contexts. <bookmark mark='d'/> Partial "
            "matching links prediction and compression, but entropy and code length concern probabilities and log "
            "loss. They do not directly give a branch-accuracy ceiling. TAGE shares some ideas while imposing finite "
            "hashed tables."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
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
        head = label('XOR: no perfect fixed affine separator of two bits', font_size=36).to_edge(UP, buff=0.3)
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
        # A shifted affine line gets three uniform XOR cases right, never all four.
        lines.append(Line(ax.c2p(-1.6, 0.6), ax.c2p(0.6, -1.6), color=HEAD, stroke_width=2.5))
        line = lines[0].copy()
        rule = MathTex(r"B = A \oplus C", font_size=34, color=HEAD).next_to(ax, UP, buff=0.25)
        cap = label('no fixed affine separator classifies all four; \\\\ best fixed line: 3/4 for uniform cases', font_size=20,
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
            label("piecewise-linear: path-selected functions; \\\\ multiperspective: hashed history features (Jim\\'enez, 2005, 2016)", font_size=20, color=GREY_A),
            label('TAGE-SC-L (Seznec, 2016): TAGE + statistical corrector + loop predictor; \\\\ components, not necessarily three serial hardware stages', font_size=20, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A small example gives a precise representational result. <bookmark mark='a'/> Let branch B equal the "
            "exclusive-or of two earlier bits, A and C. The taken cases lie on opposite corners. <bookmark mark='b'/> "
            "No fixed affine line separates all four labels. With only these two features, a perceptron cannot "
            "classify XOR perfectly; a best line can still get three of four equally likely cases right. Thus fifty "
            "percent is not the mathematical ceiling. <bookmark mark='c'/> Our online parity run happens to give this "
            "perceptron about forty-nine percent. Other histories, initialization and learning rules can change that "
            "empirical result; it does not explain the entire Job plateau. <bookmark mark='d'/> Research expands "
            "features and combines predictors: piecewise-linear methods select functions by path; multiperspective "
            "predictors hash several history features. TAGE-SC-L combines TAGE, a statistical corrector and a loop "
            "predictor, not necessarily three serial hardware stages."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(axl))
            self.play(FadeIn(pts), Write(rule))
            vo.wait_until("b")
            self.play(Create(line))
            for ln in lines[1:]:
                self.play(Transform(line, ln), run_time=0.8)
            self.play(FadeIn(cap))
            wrong = SurroundingRectangle(pts[3], buff=0.08, color=HEAD)
            three = label(r"3/4 right: one wrong corner", font_size=18, color=HEAD).next_to(ax, DOWN, buff=0.15)
            self.play(Create(wrong), FadeIn(three), run_time=0.6)
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
            label('\\textbf{offline learning.} BranchNet (2020): convolutional models for selected hard branches; \\\\ evaluate on unseen inputs; combine with a runtime predictor.', font_size=21, color=DATA),
            label('\\textbf{front-end capacity.} Large code footprints pressure fetch and predictor storage; \\\\ capacity and accuracy both matter, depending on workload.', font_size=21, color=CTRL),
            label('\\textbf{evaluation protocol.} Fix features, all state bits, training and heldout chapters; \\\\ never encode future test labels in initial state or design.', font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        with self.voiceover(
            "Research starts by defining the information and evaluation protocol. <bookmark mark='a'/> Profile which "
            "static branches cause errors on the chosen workload. Independent unseen random data would defeat a "
            "history-only guess, but our fixed traces do not prove such independence. <bookmark mark='b'/> BranchNet, "
            "published in 2020, trains convolutional models offline and combines predictions for selected hard "
            "branches with a runtime predictor. Its paper evaluates unseen inputs; that is research evidence for "
            "specified workloads, not a claim that arbitrary branches become predictable. <bookmark mark='c'/> Large "
            "code footprints also pressure instruction fetch and prediction capacity. Accuracy and capacity both "
            "matter, depending on the application. <bookmark mark='d'/> A fair next experiment fixes allowed features, "
            "all state bits, training data and heldout chapters. Keep test labels out of design and initial state. "
            "That makes improved accuracy evidence of generalization, rather than memorization of a known trace."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
