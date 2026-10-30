from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import BAD, GOOD, HIST, HL, chapter, load, plot

FOREST = C.INTERVAL
RHO_COL = {"0.0": C.REWARD, "0.2": C.MODEL_Q, "0.5": C.ADVANTAGE, "0.8": C.PENALTY}
MF_COL = {"mf70": C.PENALTY, "mf8": C.INTERVAL, "mf2": C.MODEL_Q}


class Forests(VoiceoverScene):
    def construct(self):
        chapter(self, 13, r"Bagging and random forests", r"Why does a crowd of trees beat one?",
                "Chapter thirteen. Bagging and random forests.", lit=(1979, 1996, 2001))
        self.formula()
        self.decorrelate()
        self.forest()

    # ------------------------------------------------------------------
    def formula(self):
        b = load("bagging")
        colors = {r"\rho": HL}
        rows = [
            cmath(r"\operatorname{Var}\Big(\frac1B\sum_b T_b\Big)", "=", r"\frac{1}{B^2}\sum_{b,c}\operatorname{Cov}(T_b, T_c)",
                  font_size=32, colors=colors),
            cmath(r"\operatorname{Var}\Big(\frac1B\sum_b T_b\Big)", "=", r"\frac{1}{B^2}\Big(B\sigma^2 + B(B-1)\,\rho\sigma^2\Big)",
                  font_size=32, colors=colors),
            cmath(r"\operatorname{Var}\Big(\frac1B\sum_b T_b\Big)", "=", r"\rho\sigma^2 + \frac{1 - \rho}{B}\,\sigma^2",
                  font_size=32, colors=colors),
        ]
        whys = [why(r"every pair of trees", font_size=20), why(r"$B$ variances, \\ $B(B-1)$ covariances", font_size=20),
                why(r"a floor, \ and a part \\ that averages away", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-1.2, buff=0.35, edge=6.8)
        Bs = np.asarray(b["syn_B"], float)
        lb = np.log10(Bs)
        g = plot([0, 2, 1], [0, 1.05, 0.5], x_length=6.0, y_length=3.0, xticks=[0, 1, 2], yticks=[0, 0.5, 1],
                 xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)], center=[-2.2, -2.1, 0],
                 xlabel=r"trees averaged, \ $B$", ylabel=r"variance of the average \ ($\sigma^2 = 1$)")
        ax = g.ax
        art = VGroup()
        for rho, vals in b["syn"].items():
            r = float(rho)
            col = RHO_COL[rho]
            th = curve(ax, np.linspace(0, 2, 60), [r + (1 - r) / 10 ** v for v in np.linspace(0, 2, 60)], col,
                       stroke_width=2.5, smooth=True)
            pts = VGroup(*[Dot(ax.c2p(a, v), radius=0.045, color=col) for a, v in zip(lb, vals)])
            art.add(VGroup(th, pts, label(rf"$\rho = {r:g}$", font_size=20, color=col).next_to(ax.c2p(2, r + (1 - r) / 100), RIGHT, buff=0.1)))
        tag = note(r"lines: \ the formula; \ dots: \ $20{,}000$ simulated averages of correlated bells").next_to(g, RIGHT, buff=0.3)
        tag.align_to(g, DOWN)
        rr = b["syn"]["0.5"]
        with self.voiceover(
            "Why does averaging trees help? Write the variance of an average of B trees, each with variance sigma "
            "squared, and every pair correlated by rho. <bookmark mark='a'/> It's the sum over every pair of their "
            "covariance: <bookmark mark='b'/> B variances, and B times B minus one covariances. <bookmark mark='c'/> "
            "So: rho sigma squared, plus the rest divided by B. More trees remove the second part, but never the "
            "first: correlation sets a floor. <bookmark mark='d'/> Check it by simulation: with rho a half, a "
            f"{Bs[-1]:.0f} averaged copies keep {rr[-1]:.3f} of the variance, against the formula's {0.5 + 0.5 / Bs[-1]:.3f}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=HL))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(g), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(a_) for a_ in art], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decorrelate(self):
        b = load("bagging")
        Bm = np.asarray(b["Bm"], float)
        lb = np.log10(Bm)
        top = max(max(b[k]["meas"]) for k in MF_COL) * 1.1
        g = plot([0, math.log10(Bm[-1]) + 0.05, 1], [0, top, 0.05], x_length=6.4, y_length=4.0, xticks=[0, 1],
                 yticks=[0, 0.05, 0.1, 0.15], xfmt=lambda v: {0: "1", 1: "10"}[int(v)], center=[-2.4, -0.5, 0],
                 xlabel=r"trees averaged, \ $B$", ylabel=r"variance of the vote at a held-out page, \ over training sets")
        ax = g.ax
        art, rows = VGroup(), VGroup()
        names = {"mf70": r"bagging: \ all $70$ words at each question", "mf8": r"random forest: \ $8$ random words",
                 "mf2": r"random forest: \ $2$ random words"}
        for k, col in MF_COL.items():
            r_, s2 = b[k]["rho"], b[k]["s2"]
            xs = np.linspace(0, lb[-1], 60)
            th = curve(ax, xs, [r_ * s2 + (1 - r_) * s2 / 10 ** v for v in xs], col, stroke_width=2.5, smooth=True)
            pts = VGroup(*[Dot(ax.c2p(a, v), radius=0.05, color=col) for a, v in zip(lb, b[k]["meas"])])
            art.add(VGroup(th, pts))
            rows.add(VGroup(label(names[k], font_size=22, color=col),
                            label(rf"$\rho = {r_:.3f}$, \ $\sigma^2 = {s2:.3f}$", font_size=22, color=GREY_A))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.6, 0])
        how = note(rf"${b['Rs']}$ training sets of ${b['m']}$ pages, \ ${b['T']}$ trees each; \ lines: \ the formula "
                   r"with the measured $\rho$ and $\sigma^2$").to_edge(DOWN, buff=0.15)
        bag, rf8 = b["mf70"], b["mf8"]
        dev = max(abs(v - (b[k]["rho"] * b[k]["s2"] + (1 - b[k]["rho"]) * b[k]["s2"] / B_)) /
                  (b[k]["rho"] * b[k]["s2"] + (1 - b[k]["rho"]) * b[k]["s2"] / B_)
                  for k in MF_COL for B_, v in zip(Bm, b[k]["meas"]))
        lower = rf8["rho"] < bag["rho"]
        with self.voiceover(
            "On the pages, the trees' correlation comes from sharing the same training pages. Draw "
            f"{b['Rs']} training sets of {b['m']} pages, grow {b['T']} trees on resamples of each, and measure sigma "
            "squared and rho at the held-out pages. "
            f"<bookmark mark='a'/> Bagged trees, Breiman's 1996 recipe, are correlated: rho is {bag['rho']:.3f}, and "
            "that floor stops the averaging. <bookmark mark='b'/> Breiman's 2001 twist lets each question choose among "
            "only a few random words. "
            + (f"The trees disagree more: rho falls to {rf8['rho']:.3f} with eight words, and the floor nearly vanishes, "
               f"although each tree on its own is noisier, sigma squared {rf8['s2']:.3f} against {bag['s2']:.3f}. "
               if lower else f"Here rho doesn't fall: {rf8['rho']:.3f}. ")
            + "<bookmark mark='c'/> "
            + (f"The measured variances sit on the formula's curves, within {100 * dev:.0f} percent everywhere."
               if dev < 0.2 else f"The measured variances follow the formula's curves loosely: the largest gap is "
               f"{100 * dev:.0f} percent, from only {b['Rs']} training sets.")
        ) as vo:
            self.play(FadeIn(g), FadeIn(how))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(art[0][0]), FadeIn(art[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(art[1][0]), FadeIn(art[1][1]))
            self.play(FadeIn(rows[2]), Create(art[2][0]), FadeIn(art[2][1]))
            vo.wait_until("c")
            self.play(*[Indicate(a_[1], color=WHITE, scale_factor=1.1) for a_ in art])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forest(self):
        b = load("bagging")
        fa, fo, ba = np.asarray(b["forest_acc"]), np.asarray(b["forest_oob"]), np.asarray(b["bag_acc"])
        n = len(fa)
        lo = 0.8
        g = plot([0, n, 50], [lo, 1.0, 0.05], x_length=7.4, y_length=4.2, xticks=[0, 100, 200, 300],
                 yticks=[0.8, 0.85, 0.9, 0.95, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.0, -0.4, 0],
                 xlabel=r"trees in the forest \ (all $70$ rates)", ylabel=r"pages right")
        ax = g.ax
        one = DashedLine(ax.c2p(0, b["one_tree"]), ax.c2p(n, b["one_tree"]), color=GREY_B, stroke_width=2)
        cf = curve(ax, np.arange(1, n + 1), np.clip(fa, lo, 1), FOREST, stroke_width=4)
        co = curve(ax, np.arange(1, n + 1), np.clip(fo, lo, 1), GOOD, stroke_width=3)
        cb = curve(ax, np.arange(1, len(ba) + 1), np.clip(ba, lo, 1), BAD, stroke_width=3)
        key = VGroup(label(rf"one full tree: \ ${100 * b['one_tree']:.1f}\%$", font_size=22, color=GREY_B),
                     label(rf"bagging, ${len(ba)}$ trees: \ ${100 * ba[-1]:.1f}\%$", font_size=22, color=BAD),
                     label(rf"random forest, ${n}$: \ ${100 * fa[-1]:.1f}\%$", font_size=22, color=FOREST),
                     label(rf"out-of-bag estimate: \ ${100 * fo[-1]:.1f}\%$", font_size=22, color=GOOD))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, 0.4, 0])
        oob = note(r"out of bag: \ each training page judged only by the trees \\ whose resample left it out").next_to(
            key, DOWN, buff=0.35).align_to(key, LEFT)
        hist = history_card(2001, r"Leo Breiman", r"random forests, \ after Ho's random decision forests (1995) "
                            r"and his own bagging (1996)", color=HIST, width=5.2).to_corner(UL, buff=0.2)
        n_te = int(np.asarray(load("pages")["test"], bool).sum())
        with self.voiceover(
            f"Grow a forest of {n} on all the training pages. <bookmark mark='a'/> One full tree gets "
            f"{100 * b['one_tree']:.0f} percent of the held-out pages right. <bookmark mark='b'/> The forest climbs "
            f"to {100 * fa[-1]:.1f}: {round(fa[-1] * n_te)} of {n_te}. <bookmark mark='c'/> And it grades itself for "
            "free: each training page left out of a tree's resample is a test page for that tree. That out-of-bag "
            f"estimate says {100 * fo[-1]:.0f} percent, without touching the held-out pages."
        ) as vo:
            self.play(FadeIn(g), FadeIn(hist, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Create(one), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(key[1]), run_time=1.5)
            self.play(Create(cf), FadeIn(key[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(co), FadeIn(key[3]), FadeIn(oob), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
