from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Lepski(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.tests()
        self.chart()
        self.table()
        self.mcycle()
        self.price()

    def card(self):
        card = chapter_card(7, r"Adaptation", r"Lepski's method: \ let the data choose the smoothing", lit=(1990,), part=PART)
        with self.voiceover("Chapter seven. Adaptation: Lepski's method lets the data choose the smoothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def method(self):
        rows = [
            cmath(r"h_1 < h_2 < \dots < h_J", r":", r"\text{bandwidths: \ } \hat f_j(x_0) \text{ with SD } \sigma_j \downarrow", font_size=32),
            cmath(r"\text{bias}", r"\uparrow, \ \ \text{variance} \downarrow", r":", font_size=34),
            cmath(r"\hat j", r"=", r"\max\{j : |\hat f_j - \hat f_i| \le \kappa\, \sigma_i \ \ \forall i < j\}", font_size=34),
            cmath(r"\text{idea}", r":", r"\text{grow } h \text{ until finer estimates disagree}", font_size=34),
        ]
        rows[2][-1].set_color(ADAPTC)
        whys = [why(r"a grid of smoothing levels"), why(r"the usual trade-off"), why(r"Lepski (1990)"), why(r"no knowledge of $s$")]
        with self.voiceover(
            "<bookmark mark='a'/> Oleg Lepski's method, of 1990, chooses a bandwidth at a point without knowing the "
            "smoothness. Compute the estimate at a grid of bandwidths, from small to large. <bookmark mark='b'/> Small "
            "bandwidths have little bias and much noise; large ones the reverse. <bookmark mark='c'/> Choose the largest "
            "bandwidth whose estimate agrees with every smaller-bandwidth estimate to within a few of that estimate's "
            "standard deviations. <bookmark mark='d'/> The idea: keep smoothing more, until the estimate starts to disagree "
            "with a noisier but less biased one. The disagreement is the bias showing itself."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tests(self):
        rows = [
            cmath(r"\text{step } j", r":", r"\text{test } H_0: \text{bias}(h_j) \text{ is small, \ against every finer } h_i", font_size=32),
            cmath(r"\kappa", r"\asymp", r"\sqrt{\log n}: \ \text{a Bonferroni correction over the grid}", font_size=34),
            cmath(r"\text{too-large } h", r":", r"\text{rejected with high probability, \ once its bias exceeds } \kappa\,\sigma", font_size=32),
            cmath(r"\text{Goldenshluger \& Lepski (2011)}", r":", r"\text{the same idea for whole functions, \ many dimensions}", font_size=30),
        ]
        rows[1][-1].set_color(HYPC)
        whys = [why(r"a sequence of tests"), why(r"Part 33's multiplicity"), why(r"bias reveals itself"), why(r"the modern form")]
        with self.voiceover(
            "<bookmark mark='a'/> Lepski's rule is a sequence of tests. At each step it tests whether the current bandwidth's "
            "bias is still small, by comparing its estimate with every finer one. <bookmark mark='b'/> The constant kappa must "
            "grow like the root of log n, a Bonferroni correction over the grid of bandwidths, Part thirty-three's "
            "multiplicity in a new place. That correction is the source of the log factor in the adaptive rate. <bookmark "
            "mark='c'/> A bandwidth whose bias exceeds kappa standard deviations is rejected with high probability, so the "
            "rule stops near the oracle. <bookmark mark='d'/> Alexander Goldenshluger and Lepski extended the idea in 2011 to "
            "whole functions in several dimensions, comparing estimators through a common smoother."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("lepski")
        lh = np.log10(d["hs"])
        A = axes([-2.7, -0.4], [-3.6, 0.3], x_length=7.4, y_length=4.4, xlabel=r"bandwidth $h$ \ (log scale)", ylabel=r"$\log_{10}$ MSE at $x_0$",
                 xticks=[np.log10(0.005), np.log10(0.02), np.log10(0.08), np.log10(0.32)], xfmt=lambda v: f"{10 ** v:.3f}", yticks=[-3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cs = VGroup(polyline(ax, lh, np.log10(d["smooth"]["risk_by_h"]), UPC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=UPC) for a, b in zip(lh, np.log10(d["smooth"]["risk_by_h"]))])
        ck = VGroup(polyline(ax, lh, np.log10(d["kink"]["risk_by_h"]), HYPC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=HYPC) for a, b in zip(lh, np.log10(d["kink"]["risk_by_h"]))])
        ls = DashedLine(ax.c2p(-2.7, np.log10(d["smooth"]["lepski"])), ax.c2p(-0.4, np.log10(d["smooth"]["lepski"])), color=UPC, stroke_width=2)
        lk = DashedLine(ax.c2p(-2.7, np.log10(d["kink"]["lepski"])), ax.c2p(-0.4, np.log10(d["kink"]["lepski"])), color=HYPC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"regression, \ $n = {d['n']:,}$, \ box kernel at $x_0$", font_size=22),
            label(r"blue: \ $\sin 2\pi x$ at its peak: \ smooth", font_size=22, color=UPC),
            label(r"gold: \ $3|x - \tfrac12|^{1/2}$ at its cusp: \ rough", font_size=22, color=HYPC),
            label(r"each curve's minimum: \ the oracle bandwidth", font_size=22, color=GREY_A),
            label(r"dashed: \ Lepski's MSE, \ told neither", font_size=22, color=ADAPTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two regression functions, four thousand observations, the value at one point. <bookmark "
            "mark='b'/> A smooth one, a sine at its peak, whose mean squared error is smallest at a large bandwidth. "
            "<bookmark mark='c'/> And a rough one, a square-root cusp, whose error is smallest at a small bandwidth. "
            "<bookmark mark='d'/> No single bandwidth is good for both. <bookmark mark='e'/> The dashed lines are Lepski's "
            "error, choosing its own bandwidth each time: in both cases a modest factor above the best possible, without "
            "being told which function it faces."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 1,500 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ck), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(ls), Create(lk), FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("lepski")
        rows = [[r"function", r"oracle MSE", r"fixed $h = 0.04$", r"Lepski", r"Lepski / oracle"]]
        for k, nm in (("smooth", r"$\sin 2\pi x$, \ smooth"), ("kink", r"$|x - \tfrac12|^{1/2}$, \ rough")):
            r = d[k]
            rows.append([nm, f"{r['oracle']:.4f}", f"{r['fixed']:.4f}", f"{r['lepski']:.4f}", f"{r['lepski'] / r['oracle']:.1f}"])
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.45, colors=[GREY_B, UPC, HYPC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.9, 0])
        s, k = d["smooth"], d["kink"]
        foot = label(rf"the fixed bandwidth is {k['fixed'] / k['oracle']:.1f} times the oracle on the rough function; \ Lepski is within {max(s['lepski'] / s['oracle'], k['lepski'] / k['oracle']):.1f} on both", font_size=24, color=ADAPTC).move_to([0, -1.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> In numbers. A fixed bandwidth of point oh four is the oracle choice for the smooth "
            f"function but costs a factor of {say(k['fixed'] / k['oracle'], 1)} on the rough one. Lepski's choice costs a factor "
            f"of {say(s['lepski'] / s['oracle'], 1)} and {say(k['lepski'] / k['oracle'], 1)}: never the best, never bad. "
            f"<bookmark mark='b'/> That uniformity across classes is what adaptation means."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def mcycle(self):
        d = load("mcycle")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"time after impact (ms)", ylabel=r"head acceleration (g)",
                 xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[-100, 0, 50], center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=GREY_B) for a, b in zip(x, y)])
        marks = VGroup()
        for p in d["points"]:
            seg = Line(ax.c2p(p["x0"] - p["h"], p["est"]), ax.c2p(p["x0"] + p["h"], p["est"]), color=ADAPTC, stroke_width=6)
            marks.add(VGroup(seg, Dot(ax.c2p(p["x0"], p["est"]), radius=0.08, color=ADAPTC)))
        P = d["points"]
        side = fit_rows(VGroup(
            label(r"the motorcycle crash: \ 133 readings", font_size=22),
            label(r"green bars: \ Lepski's window at three times", font_size=22, color=ADAPTC),
            label(rf"14 ms and 22 ms: \ $h$ = {P[0]['h']:.0f}, \ {P[1]['h']:.0f}: \ the signal moves fast", font_size=22, color=ADAPTC),
            label(rf"40 ms: \ $h$ = {P[2]['h']:.0f}: \ it is flat, \ so average widely", font_size=22, color=ADAPTC),
            label(r"local smoothing chosen by the data, \ point by point", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The motorcycle crash data from Part twenty-nine: head acceleration after a simulated "
            f"impact, a curve that is flat, then plunges, then rebounds. <bookmark mark='b'/> Lepski's method picks a window "
            f"at each point separately. <bookmark mark='c'/> At fourteen and twenty-two milliseconds, where the curve moves "
            f"fast, it picks half-widths of {P[0]['h']:.0f} and {P[1]['h']:.0f} milliseconds. <bookmark mark='d'/> At forty, "
            f"where it has settled, {P[2]['h']:.0f}. <bookmark mark='e'/> The smoothing adapts to the local roughness, which "
            f"a single global bandwidth cannot do."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), FadeIn(museum_tag(r"Silverman (1985); \ Schmidt, \ Mattern \& Schüler (1981)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(marks[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def price(self):
        rows = [
            cmath(r"\text{known } s", r":", r"\inf \sup E(\hat f(x_0) - f(x_0))^2 \asymp n^{-2s/(2s+1)}", font_size=32),
            cmath(r"\text{unknown } s, \ \text{pointwise}", r":", r"\text{the best adaptive rate is } (n/\log n)^{-2s/(2s+1)}", font_size=32),
            cmath(r"\text{the price}", r":", r"\text{a log factor, \ and it cannot be avoided}", font_size=34),
            cmath(r"\text{global } L_2 \text{ loss}", r":", r"\text{no price: \ adaptation is free \ (block JS, \ chapter 6)}", font_size=32),
        ]
        rows[1][-1].set_color(ADAPTC)
        rows[2][-1].set_color(LOWC)
        rows[3][-1].set_color(UPC)
        whys = [why(r"Farrell, \ Stone"), why(r"Lepski (1990, \ 1991)"), why(r"Brown \& Low (1996)"), why(r"Efromovich \& Pinsker")]
        with self.voiceover(
            "<bookmark mark='a'/> How much does not knowing the smoothness cost? With s known, the pointwise rate is n to the "
            "minus two s over two s plus one. <bookmark mark='b'/> With s unknown, Lepski showed the best rate any adaptive "
            "estimator can achieve at a point is the same with n replaced by n over log n. <bookmark mark='c'/> That log "
            "factor is a genuine price, and Lawrence Brown and Mark Low proved it cannot be avoided. <bookmark mark='d'/> For "
            "the global squared-error loss, by contrast, there is no price at all: blockwise James–Stein adapts exactly. "
            "Whether adaptation is free depends on the loss."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
