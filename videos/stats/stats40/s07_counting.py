from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.path()
        self.martingale()
        self.many()
        self.payoff()

    def card(self):
        card = chapter_card(6, r"Counting processes", r"Events minus their compensator", lit=(1978,), part=PART)
        with self.voiceover("Chapter six. Counting processes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"N(t)", r"=", r"\#\{\text{events observed by } t\}", font_size=32),
            cmath(r"Y(t)", r"=", r"\#\{\text{at risk just before } t\}", font_size=32),
            cmath(r"\Lambda(t)", r"=", r"\textstyle\int_0^t Y(s)\, h(s)\, ds", font_size=32),
            cmath(r"M(t)", r"=", r"N(t) - \Lambda(t): \ \text{a martingale}", font_size=32),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"a step function, \ jumps of 1"), why(r"the risk set's size"), why(r"the compensator: \ expected events"),
                why(r"Aalen (1978)")]
        with self.voiceover(
            "<bookmark mark='a'/> Odd Aalen's 1978 counting-process work recast the whole subject in terms of "
            "counting. N of t counts the events observed by time t. <bookmark mark='b'/> Y of t counts those still at"
            " risk. <bookmark mark='c'/> The compensator integrates the hazard over the risk set: the accumulated "
            "predictable event intensity, based on who has been at risk. <bookmark mark='d'/> The difference, "
            "observed minus expected, is a martingale: its expected future change, given the past, is zero, provided "
            "the specified intensity remains valid in the observed-data filtration and censoring does not reveal "
            "additional future event risk."
        ) as vo:
            heading = label('Observed events minus integrated intensity form a martingale', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def path(self):
        d = load("counting")
        grid = np.asarray(d["grid"], float)
        N, Lam, Y = (np.asarray(d[k], float) for k in ("N", "Lam", "Y"))
        A = axes([0, 2.5], [0, 40], x_length=7.4, y_length=4.2, xlabel=r"time", ylabel=r"count",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5], yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        cN = VMobject(stroke_color=EVTC, stroke_width=3)
        pts = []
        for i in range(len(grid)):
            if i:
                pts.append(ax.c2p(grid[i], N[i - 1]))
            pts.append(ax.c2p(grid[i], N[i]))
        cN.set_points_as_corners(pts)
        cL = polyline(ax, grid, Lam, TAUC, 3)
        cY = polyline(ax, grid, Y * 40 / 50, CENSC, 2, 0.6)
        side = fit_rows(VGroup(
            label(rf"{d['n']} exponential(1) lifetimes, \ random censoring", font_size=22),
            label(r"red: \ $N(t)$, \ events so far", font_size=22, color=EVTC),
            label(r"gold: \ $\Lambda(t)$, \ expected so far", font_size=22, color=TAUC),
            label(r"grey: \ $Y(t)$, \ at risk \ (scaled)", font_size=22, color=CENSC),
            label(r"the gold curve flattens as the risk set empties", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One path. Fifty lifetimes with hazard one, randomly censored. <bookmark mark='b'/> The "
            "count of events climbs in unit steps. <bookmark mark='c'/> The compensator climbs smoothly, at a rate equal to "
            "the hazard times the number at risk, <bookmark mark='d'/> so it slows as deaths and censoring empty the risk "
            "set. <bookmark mark='e'/> The two stay close: the red steps scatter around the gold curve."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cN), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(cL), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cY), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def martingale(self):
        rows = [
            cmath(r"E[dM(t) \mid \mathcal F_{t-}]", r"=", r"0", font_size=32),
            cmath(r"\langle M \rangle(t)", r"=", r"\Lambda(t): \ \ \text{Var}\, M(t) = E\Lambda(t)", font_size=32),
            cmath(r"\textstyle\int H(s)\, dM(s)", r":", r"\text{again a martingale, \ for predictable } H", font_size=30),
            cmath(r"\text{Rebolledo}", r":", r"\text{a martingale CLT: \ sums of small jumps are normal}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"no drift, \ given the past"), why(r"the predictable variation"), why(r"stochastic integrals"),
                why(r"Rebolledo (1980); \ Part 44")]
        with self.voiceover(
            "<bookmark mark='a'/> Martingales have no drift: given everything up to just before t, the expected "
            "increment is zero. <bookmark mark='b'/> Their predictable variation is the compensator itself, so the "
            "variance of M is the expected number of events. <bookmark mark='c'/> With suitable integrability, "
            "weighting the increments by a predictable process known just before each time gives another martingale. "
            "<bookmark mark='d'/> And Rolando Rebolledo's central limit theorem says a normal limit follows when jump"
            " sizes are negligible and predictable variance converges appropriately. Part forty-four proves it."
        ) as vo:
            heading = label('Martingale limits require variance and jump-size conditions', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def many(self):
        d = load("counting")
        h = np.asarray(d["hist"], float)
        edges = np.arange(-20.5, 21.5, 1.0)
        dens = h / 4000
        A = axes([-20.5, 20.5], [0, 0.1], x_length=7.4, y_length=4.0, xlabel=r"$M(1) = N(1) - \Lambda(1)$", ylabel=r"share of 4,000 paths",
                 xticks=[-20, -10, 0, 10, 20], yticks=[0, 0.05, 0.1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, dens, TAUC)
        xs = np.linspace(-20, 20, 200)
        sd = np.sqrt(d["Lam_mean"])
        nc = polyline(ax, xs, np.exp(-xs ** 2 / (2 * sd ** 2)) / (sd * np.sqrt(2 * np.pi)), SURVC, 3)
        side = fit_rows(VGroup(
            label(r"4,000 paths of 50 lifetimes", font_size=22),
            label(rf"mean of $M(1)$: \ {d['M_mean']:.2f}", font_size=22, color=TAUC),
            label(rf"variance: \ {d['M_var']:.1f}; \ $E\Lambda(1)$ = {d['Lam_mean']:.1f}", font_size=22, color=TAUC),
            label(r"blue: a normal approximation", font_size=22, color=SURVC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Check it on four thousand such paths. <bookmark mark='b'/> Observed minus expected events "
            "by time one averages " + say(d["M_mean"], 2) + ", zero up to simulation noise, <bookmark mark='c'/> and its "
            "variance is " + say(d["M_var"], 1) + ", against an expected compensator of " + say(d["Lam_mean"], 1) + ". <bookmark mark='d'/> And the histogram is close to a normal reference; the martingale central limit "
            "theorem explains the approximation under its conditions."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(nc), FadeIn(side[3]))
        self.clear_scene()

    def payoff(self):
        rows = fit_rows(VGroup(
            label(r"Nelson--Aalen: $\hat H-\int 1\{Y>0\}h\,dt=\int 1\{Y>0\}\,dM/Y$", font_size=26, color=HAZC),
            label(r"Kaplan--Meier: \ $\hat S / S - 1 = -\int (\hat S_- / S)\, dM / Y$: \ Greenwood's formula falls out", font_size=26, color=SURVC),
            label(r"log-rank: \ a weighted integral of $dM$ \ (chapter 7)", font_size=26, color=TAUC),
            label(r"Cox's score: \ a sum of martingale increments \ (chapter 8; \ Andersen \& Gill 1982)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why bother? Because every estimator in this part is an integral against M. The "
            "Nelson-Aalen error is the martingale integral of dM over Y, for the cumulative hazard stopped when the "
            "risk set becomes empty. This qualification matters: the estimator is not exactly unbiased for "
            "unrestricted H after the last person leaves. Its variance estimator follows at once. <bookmark "
            "mark='b'/> The Kaplan-Meier error has the same form, and Greenwood's formula drops out. <bookmark "
            "mark='c'/> The log-rank statistic is a weighted integral of dM, <bookmark mark='d'/> and so is Cox's "
            "score. Per Kragh Andersen and Richard Gill used this in 1982 to give Cox's model its large-sample "
            "theory, including covariates that change over time."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
