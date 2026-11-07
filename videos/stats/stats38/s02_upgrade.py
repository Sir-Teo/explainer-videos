from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


def mini(center, ys, color, title, y_range=None):
    ys = np.asarray(ys, float)
    lo, hi = (float(ys.min()), float(ys.max())) if y_range is None else y_range
    pad = 0.08 * (hi - lo + 1e-9)
    A = axes([0, len(ys)], [lo - pad, hi + pad], x_length=5.4, y_length=1.9, xlabel=r"", ylabel=r"", xticks=[], yticks=[],
             center=list(center))
    line = series_line(A.ax, np.arange(len(ys)), ys, color, 1.6)
    t = label(title, font_size=20, color=color).next_to(A, UP, buff=0.08)
    return VGroup(A, line, t)


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.recap()
        self.gallery()
        self.wold()
        self.ergodic()
        self.plan()

    def card(self):
        card = chapter_card(1, r"What Part 17 assumed", r"Stationary, \ short memory, \ constant variance, \ observed",
                            lit=(1927, 1938), part=PART)
        with self.voiceover("Chapter one. What Part seventeen assumed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def recap(self):
        card = upgrade_card(17, r"ARMA models: \ stationary, \ fitted by Yule--Walker and least squares, \ forecast with intervals",
                            r"a constant mean and variance, \ autocorrelations that die off fast, \ and a fully observed series",
                            r"Part 38: \ frequencies, \ unit roots, \ moving variance, \ long memory, \ hidden states, \ several series at once")
        with self.voiceover(
            "<bookmark mark='a'/> Part seventeen built autoregressive and moving-average models, fitted them by Yule-Walker "
            "and least squares, and forecast with intervals. <bookmark mark='b'/> It assumed a constant mean and variance, "
            "autocorrelations that die away quickly, and a series we observe directly. <bookmark mark='c'/> This part lets "
            "each assumption go in turn."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def gallery(self):
        d = load("gallery")
        p0 = mini([-3.4, 1.7, 0], d["ar"], Y0C, r"Part 17: \ an AR(1), \ $\phi = 0.6$")
        p1 = mini([3.4, 1.7, 0], d["rw"], MISSC, r"a random walk: \ no mean to return to")
        p2 = mini([-3.4, -1.3, 0], d["garch"], VOLC, r"GARCH: \ calm and storm")
        p3 = mini([3.4, -1.3, 0], d["lm"], LMC, r"ARFIMA, \ $d = 0.45$: \ long excursions")
        with self.voiceover(
            "<bookmark mark='a'/> Four seeded series. First, Part seventeen's world: an autoregression that forgets quickly "
            "and returns to its mean. <bookmark mark='b'/> A random walk: the same shocks, accumulated forever, so the series "
            "has no mean to return to and its variance grows without bound. Chapters three and four. <bookmark mark='c'/> A "
            "GARCH series: no correlation in the values at all, but calm stretches and storms, because the variance "
            "depends on recent shocks. Chapter five. <bookmark mark='d'/> And fractionally integrated noise: stationary, "
            "with a mean, but with excursions that last much longer than an autoregression's, the Nile's long memory. "
            "Chapter six."
        ) as vo:
            self.add(seeded_tag())
            for p, m_ in zip((p0, p1, p2, p3), "abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(p[0]), FadeIn(p[2]), Create(p[1]), run_time=2.0)
        self.clear_scene()

    def wold(self):
        rows = [
            cmath(r"X_t", r"=", r"\mu + \textstyle\sum_{j \ge 0} \psi_j \varepsilon_{t-j} \quad \text{(Wold, 1938)}", font_size=30),
            cmath(r"\text{unit root}", r":", r"\psi_j \not\to 0 \ \Rightarrow \ \text{not covariance-stationary}", font_size=30),
            cmath(r"\text{long memory}", r":", r"\psi_j \sim j^{d-1} \ \Rightarrow \ \textstyle\sum_h |\rho_h| = \infty", font_size=30),
            cmath(r"\text{GARCH}", r":", r"\varepsilon_t \text{ uncorrelated, \ but not independent}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"the purely nondeterministic stationary component"), why(r"shocks never fade"), why(r"shocks fade, \ slowly"),
                why(r"the variance has memory")]
        with self.voiceover(
            "<bookmark mark='a'/> Herman Wold proved in 1938 that every covariance-stationary square-integrable "
            "series, after removing its linearly deterministic part, is a moving average of past uncorrelated shocks,"
            " with weights that die away. <bookmark mark='b'/> A unit root is a series whose weights never die away: "
            "a shock today moves the series forever. <bookmark mark='c'/> Long memory has weights that do die away, "
            "but so slowly, like a power of the lag, that the autocorrelations cannot be added up. <bookmark "
            "mark='d'/> And GARCH keeps the shocks uncorrelated but not independent: their sizes are predictable even"
            " though their signs are not. Wold's theorem speaks only of correlations."
        ) as vo:
            intro=label('Wold represents the purely nondeterministic stationary component',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def plan(self):
        d = load("gallery")
        rows = fit_rows(VGroup(
            label(r"and a fifth departure: \ the series we care about may be hidden", font_size=26, color=STATEC),
            label(r"we see a noisy measurement; \ the state underneath must be inferred", font_size=26),
            label(r"the Kalman filter \ (chapters 7--9): \ Gaussian conditioning, \ one step at a time", font_size=26, color=TAUC),
            label(r"first: \ look at a series one frequency at a time", font_size=26, color=SPECC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There is a fifth departure. The series we care about may be hidden: a position, a level, "
            "a state of the economy. <bookmark mark='b'/> We see only noisy measurements, and the state underneath must be "
            "inferred. <bookmark mark='c'/> Kalman's filter, in chapters seven to nine, does that by Gaussian conditioning, "
            "one step at a time. <bookmark mark='d'/> But first, a different way to look at any stationary series: one "
            "frequency at a time."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ergodic(self):
        rows = fit_rows(VGroup(
            label(r"we see one realization: \ one Nile, \ one DAX, \ one history", font_size=26, color=GREY_A),
            label(r"ergodicity: \ time averages converge to the averages over realizations", font_size=26, color=TAUC),
            label(r"mixing can ensure ergodicity; covariance decay alone ensures mean convergence", font_size=26, color=MISSC),
            label(r"nonstationary models require their own limit conditions", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One thing every time-series method assumes quietly. We observe one realization: one"
            " Nile, one stock index, one history. Probability talks about averages over many possible histories. "
            "<bookmark mark='b'/> Ergodicity is the property that lets an average over time stand in for an average "
            "over realizations: the sample mean of one long series converges to the expected value. <bookmark "
            "mark='c'/> Stationarity with sufficient mixing is one route to ergodicity. Vanishing autocovariances "
            "suffice for mean convergence in mean square, but not for full ergodicity. Unit roots need different "
            "asymptotics, and long memory can make mean convergence very slow. <bookmark mark='d'/> Different methods"
            " in this part require different stationarity, ergodicity or nonstationary limit conditions. Leaving Part"
            " seventeen's world requires checking which conditions survive."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
