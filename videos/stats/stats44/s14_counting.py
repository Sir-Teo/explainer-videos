from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.compensator()
        self.picture()
        self.aalen()
        self.logrank()
        self.rebolledo()

    def card(self):
        card = chapter_card(13, r"Counting processes", r"The martingales inside survival analysis", lit=(1978,), part=PART)
        with self.voiceover("Chapter thirteen. Counting processes: the martingales inside survival analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def compensator(self):
        rows = [
            cmath(r"N(t)", r":", r"\text{the number of events by } t: \ \text{a counting process}", font_size=32),
            cmath(r"\Lambda(t)", r"=", r"\textstyle\int_0^t Y(s)\, \lambda(s)\, ds: \ \text{at risk } \times \text{ hazard, \ predictable}", font_size=30),
            cmath(r"M(t)", r"=", r"N(t) - \Lambda(t) \ \text{is a martingale}, \ \ \langle M \rangle(t) = \Lambda(t)", font_size=32),
            cmath(r"\text{Doob--Meyer}", r":", r"\text{every counting process} = \text{a martingale} + \text{its compensator}", font_size=30),
        ]
        rows[2][-1].set_color(MARTC)
        whys = [why(r"events in time"), why(r"the compensator"), why(r"Aalen (1978)"), why(r"chapter 2's decomposition, \ in continuous time")]
        with self.voiceover(
            "<bookmark mark='a'/> A counting process counts events as they happen: deaths in a cohort, relapses in a trial. "
            "<bookmark mark='b'/> Its compensator is the integral of the number at risk times the hazard: the expected count "
            "given the past, accumulated continuously, and known an instant ahead. <bookmark mark='c'/> The difference, "
            "counts minus compensator, is a martingale, and its predictable variation is the compensator itself. Odd Aalen's "
            "1978 thesis made this the foundation of survival analysis. <bookmark mark='d'/> It is chapter two's Doob "
            "decomposition in continuous time, the Doob–Meyer decomposition."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("counting")
        g = np.asarray(d["grid"])
        A = axes([0, 2.5], [0, 130], x_length=5.4, y_length=3.4, xlabel=r"$t$", ylabel=r"count", xticks=[0, 1, 2], yticks=[0, 60, 120],
                 center=[-3.5, 0.9, 0])
        B = axes([0, 2.5], [-20, 20], x_length=5.4, y_length=3.4, xlabel=r"$t$", ylabel=r"$M(t) = N(t) - \Lambda(t)$", xticks=[0, 1, 2],
                 yticks=[-20, 0, 20], center=[3.3, 0.9, 0])
        N = VMobject(stroke_color=CHAINC, stroke_width=3)
        N.set_points_as_corners([A.ax.c2p(a, b) for a, b in zip(g, d["N"])])
        L = polyline(A.ax, g, d["Lam"], LIMC, 3)
        M = polyline(B.ax, g, d["M"], MARTC, 3)
        band = VGroup(polyline(B.ax, g, 2 * np.sqrt(np.asarray(d["Lam"])), GREY_B, 2), polyline(B.ax, g, -2 * np.sqrt(np.asarray(d["Lam"])), GREY_B, 2))
        side = fit_rows(VGroup(
            label(rf"{d['n']} lifetimes, \ hazard 1, \ censored at random: \ {d['events']} events", font_size=22),
            label(r"blue: \ $N(t)$; \ gold: \ its compensator $\Lambda(t)$", font_size=22, color=CHAINC),
            label(r"right: \ the martingale, \ inside $\pm 2\sqrt{\Lambda(t)}$", font_size=22, color=MARTC),
        ), 12.4, 0.28, [0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two hundred simulated lifetimes with hazard one, censored at random times: "
            f"{d['events']} events. <bookmark mark='b'/> In blue the count of events, in gold its compensator, the integral "
            f"of the number still at risk. The two climb together. <bookmark mark='c'/> On the right, their difference, the "
            f"martingale. It wanders around zero inside plus or minus two times the root of the compensator, its predictable "
            f"standard deviation, and ends at {say(d['M'][-1], 1)} after more than a hundred events."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(exact_tag(r"simulated: 200 lifetimes")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(N), Create(L), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(M), Create(band), FadeIn(side[2]), run_time=2.0)
        self.clear_scene()

    def aalen(self):
        d = load("counting")
        t = np.asarray(d["na_t"], float)
        na, se = np.asarray(d["na"]), np.asarray(d["na_se"])
        A = axes([0, 24], [0, 6], x_length=7.4, y_length=4.4, xlabel=r"weeks", ylabel=r"cumulative hazard $\hat H(t)$",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 2, 4, 6], center=[-2.5, 0.2, 0])
        ax = A.ax
        pts, lo, hi = [], [], []
        prev, pl, ph = 0.0, 0.0, 0.0
        tt = [0.0]
        for a, h, s in zip(t, na, se):
            pts += [(a, prev), (a, h)]
            prev = h
        pts.append((23, prev))
        st = VMobject(stroke_color=CHAINC, stroke_width=4)
        st.set_points_as_corners([ax.c2p(a, min(b, 6)) for a, b in pts])
        bnd = band(ax, t, np.maximum(na - 1.96 * se, 0), np.minimum(na + 1.96 * se, 6), CHAINC, 0.25)
        side = fit_rows(VGroup(
            label(r"the 6-MP trial's placebo arm \ (21 children)", font_size=22),
            label(r"Nelson--Aalen: \ $\hat H(t) = \sum_{t_j \le t} d_j / Y(t_j)$", font_size=22, color=CHAINC),
            label(r"$\hat H - H$: \ a martingale integral, \ var $\sum d_j / Y_j^2$", font_size=22, color=MARTC),
            label(rf"at 23 weeks: \ $\hat H = {na[-1]:.2f}$, \ SE {se[-1]:.2f}", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The payoff is in Part forty's methods. Here is the placebo arm of the 6-MP trial. <bookmark "
            f"mark='b'/> The Nelson–Aalen estimator adds, at each event time, the number of events over the number at risk. "
            f"<bookmark mark='c'/> Its error, Nelson–Aalen minus the true cumulative hazard, is a stochastic integral against "
            f"the counting-process martingale, so its variance is the integrated predictable variation: the sum of the "
            f"events over the number at risk squared. <bookmark mark='d'/> That gives the band, and a cumulative hazard of "
            f"{say(na[-1], 2)} at twenty-three weeks, with standard error {say(se[-1], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Freireich et al. (1963), \ via Gehan (1965)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(st), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bnd), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def rebolledo(self):
        rows = fit_rows(VGroup(
            label(r"Rebolledo (1980): \ a martingale CLT for counting processes", font_size=26),
            label(r"if $\langle M_n \rangle(t) \to V(t)$ and the jumps vanish, \ $M_n \Rightarrow$ a Gaussian martingale", font_size=26, color=MARTC),
            label(r"so: \ Greenwood's formula, \ the log-rank test, \ Cox's partial likelihood: \ all asymptotically normal", font_size=26, color=GOODC),
            label(r"Andersen, \ Borgan, \ Gill \& Keiding, \ \emph{Statistical Models Based on Counting Processes} (1993)", font_size=22, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Rolando Rebolledo's central limit theorem for counting-process martingales completes the "
            "picture. <bookmark mark='b'/> If the predictable variations converge and the jumps become small, the "
            "martingales converge to a Gaussian martingale. <bookmark mark='c'/> Applied to stochastic integrals, it makes "
            "Greenwood's formula, the log-rank test and Cox's partial likelihood asymptotically normal, with censoring and "
            "delayed entry handled for free, because the at-risk process is predictable. <bookmark mark='d'/> The theory is "
            "set out in the book by Andersen, Borgan, Gill and Keiding. Every standard error in Part forty was, underneath, "
            "a martingale calculation."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def logrank(self):
        rows = [
            cmath(r"N_1, N_0", r":", r"\text{counting processes of two groups, \ at risk } Y_1, Y_0", font_size=32),
            cmath(r"U", r"=", r"\textstyle\int_0^\tau \frac{Y_0}{Y_1 + Y_0}\, dN_1 - \frac{Y_1}{Y_1 + Y_0}\, dN_0: \ \text{observed minus expected}", font_size=28),
            cmath(r"H_0: \lambda_1 = \lambda_0", r"\Rightarrow", r"U = \textstyle\int \frac{Y_0}{Y} dM_1 - \frac{Y_1}{Y} dM_0: \ \text{a martingale integral}", font_size=28),
            cmath(r"\text{Var}", r"=", r"\textstyle\int \frac{Y_1 Y_0}{Y^2}\, dN: \ \text{the log-rank variance, \ by } \langle M \rangle", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 40's two arms"), why(r"the log-rank statistic"), why(r"the compensators cancel"), why(r"Rebolledo makes it normal")]
        with self.voiceover(
            "<bookmark mark='a'/> The log-rank test of Part forty is a stochastic integral too. Take the counting "
            "processes of two groups with their numbers at risk. <bookmark mark='b'/> The log-rank statistic integrates, "
            "over time, the events in group one weighted by the share at risk in group zero, minus the reverse: observed "
            "minus expected. <bookmark mark='c'/> Under the null of equal hazards the compensators cancel exactly, and what "
            "is left is an integral of predictable weights against the two martingales. <bookmark mark='d'/> Its variance "
            "is the integrated predictable variation, the familiar log-rank variance, and Rebolledo's theorem, next, makes "
            "it normal."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
