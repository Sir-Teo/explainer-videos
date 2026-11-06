from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats44.common import *  # noqa: F403


class MartingaleCLT(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.ar1()
        self.score()
        self.hist()
        self.board()

    def card(self):
        card = chapter_card(7, r"The martingale CLT", r"Normal limits for dependent sums", lit=(1974,), part=PART)
        with self.voiceover("Chapter seven. The martingale central limit theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        rows = [
            cmath(r"\xi_{n,k}", r":", r"\text{martingale differences: } E[\xi_{n,k} \mid \mathcal F_{n,k-1}] = 0", font_size=32),
            cmath(r"\textstyle\sum_k E[\xi_{n,k}^2 \mid \mathcal F_{n,k-1}]", r"\to", r"1 \ \text{in probability}", font_size=32),
            cmath(r"\textstyle\sum_k E[\xi_{n,k}^2 1(|\xi_{n,k}| > \varepsilon) \mid \mathcal F_{n,k-1}]", r"\to", r"0 \ \text{in probability}", font_size=28),
            cmath(r"\Rightarrow", r"\;", r"\textstyle\sum_k \xi_{n,k} \Rightarrow N(0, 1)", font_size=36),
        ]
        rows[3][-1].set_color(MARTC)
        whys = [why(r"steps with conditional mean 0"), why(r"the conditional variances settle"), why(r"conditional Lindeberg"), why(r"McLeish (1974); \ Hall \& Heyde (1980)")]
        with self.voiceover(
            "<bookmark mark='a'/> Lindeberg's theorem has a martingale version. Take a triangular array of martingale "
            "differences: each step has conditional mean zero given the past. <bookmark mark='b'/> Suppose the sum of the "
            "conditional variances converges in probability to one, <bookmark mark='c'/> and a conditional Lindeberg "
            "condition holds, so no single step matters. <bookmark mark='d'/> Then the sum is asymptotically standard "
            "normal. Don McLeish gave a short proof in 1974, and Peter Hall and Christopher Heyde's book of 1980 made it "
            "the standard tool. The first condition is the crucial one: the information collected must become predictable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ar1(self):
        rows = [
            cmath(r"y_t", r"=", r"\phi y_{t-1} + e_t, \ \ e_t \text{ i.i.d.}, \ (0, \sigma^2)", font_size=34),
            cmath(r"\hat\phi - \phi", r"=", r"\frac{\sum_t y_{t-1} e_t}{\sum_t y_{t-1}^2}: \ \text{the numerator is a martingale}", font_size=32),
            cmath(r"\tfrac1n \textstyle\sum y_{t-1}^2 e_t^2", r"\to", r"\sigma^4 / (1 - \phi^2) \ \ \text{(ergodic theorem, } |\phi| < 1)", font_size=30),
            cmath(r"\sqrt n (\hat\phi - \phi)", r"\Rightarrow", r"N(0, \ 1 - \phi^2)", font_size=36),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 17's AR(1)"), why(r"$E[y_{t-1} e_t \mid \mathcal F_{t-1}] = 0$"), why(r"the conditional variances settle"), why(r"the familiar SE, \ justified")]
        with self.voiceover(
            "<bookmark mark='a'/> Its most common use is invisible: every time-series standard error. Take Part seventeen's "
            "first-order autoregression. <bookmark mark='b'/> The least-squares error is a ratio whose numerator, the sum of "
            "y t minus one times e t, is a martingale, because each new shock is unpredictable from the past. The terms are "
            "not independent: y t minus one is built from earlier shocks. <bookmark mark='c'/> The conditional variances add "
            "up to sigma squared times the sum of squared lags, which settles, divided by n, by the ergodic theorem, when phi "
            "is below one in absolute value. <bookmark mark='d'/> So root n times the error is normal with variance one minus "
            "phi squared, and the textbook standard error is justified."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hist(self):
        d = load("mclt")
        panels = VGroup()
        for i, (k, ttl, c) in enumerate([("0.5", r"$\phi = 0.5$, \ $n = 200$", GOODC), ("0.98", r"$\phi = 0.98$, \ $n = 100$", BADC)]):
            r = d[k]
            e = np.asarray(r["edges"])
            A = axes([-5, 3], [0, 0.6], x_length=5.4, y_length=3.4, xlabel=r"$\sqrt n (\hat\phi - \phi) / \sqrt{1 - \phi^2}$",
                     ylabel=r"density", xticks=[-4, -2, 0, 2], yticks=[0, 0.3, 0.6], center=[-3.5 + 6.8 * i, 0.8, 0])
            bars = bars_at(A.ax, (e[:-1] + e[1:]) / 2, np.minimum(r["hist"], 0.6), e[1] - e[0], c, opacity=0.7)
            xs = np.linspace(-5, 3, 200)
            nc = curve(A.ax, xs, stats.norm.pdf(xs), LIMC, 3)
            cap = label(rf"{ttl}: \ skewness ${r['skew']:.2f}$, \ mean $\hat\phi = {r['mean']:.3f}$", font_size=20, color=c).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, bars, nc, cap))
        side = fit_rows(VGroup(
            label(r"20,000 simulated series each, \ fitted with an intercept", font_size=22, color=GREY_A),
            label(r"near a unit root the conditional variances do not settle: \ $\sum y_{t-1}^2 / n$ keeps growing", font_size=22, color=BADC),
            label(r"the limit there is Dickey and Fuller's, \ not the normal: \ chapter 11", font_size=22, color=S.ACCENT),
        ), 12.4, 0.28, [0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Twenty thousand simulated series, fitted as practice fits them, with an intercept. With phi "
            f"a half and two hundred observations, the standardized estimate is close to normal. <bookmark mark='b'/> With phi "
            f"point nine eight and a hundred observations, it is skewed to the left and biased: the mean estimate is "
            f"{say(d['0.98']['mean'], 3)}. Near a unit root, the sum of squared lags over n does not settle, the first "
            f"condition fails, <bookmark mark='c'/> and the limit is not normal: at phi equal to one it is Dickey and Fuller's "
            f"functional of Brownian motion, chapter eleven's subject."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def board(self):
        show_board(self, board_rows("AR(1)"),
                   "<bookmark mark='a'/> The Board, for nominal ninety percent intervals for phi from least squares with an "
                   "intercept. At phi a half with two hundred observations, coverage is ninety percent: kept. <bookmark "
                   "mark='b'/> At phi point nine eight with a hundred, it is seventy: broken, because the martingale central "
                   "limit theorem's first condition has failed.",
                   [("a", [0]), ("b", [1])])

    def score(self):
        rows = [
            cmath(r"U_n(\theta)", r"=", r"\textstyle\sum_{i \le n} \partial_\theta \log f_\theta(X_i \mid X_1, \ldots, X_{i-1})", font_size=30),
            cmath(r"E_\theta[\text{step} \mid \text{past}]", r"=", r"0: \ \text{the score is a martingale, \ even for dependent data}", font_size=30),
            cmath(r"\langle U \rangle_n", r"=", r"\textstyle\sum_i \text{Var}[\text{step} \mid \text{past}] \ \text{(the conditional information)}", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"U_n / \sqrt{\langle U \rangle_n} \Rightarrow N(0, 1) \ \Rightarrow \ \text{the MLE is asymptotically normal}", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the likelihood of a process"), why(r"Part 22's mean-zero score"), why(r"observed vs expected information"), why(r"Part 47, \ for dependent data")]
        with self.voiceover(
            "<bookmark mark='a'/> The same theorem covers every likelihood for dependent data. The score of a process is "
            "a sum over observations of the derivative of each conditional log-density given the past. <bookmark mark='b'/> "
            "Each term has conditional mean zero, by Part twenty-two's argument applied conditionally, so the score is a "
            "martingale. <bookmark mark='c'/> Its predictable variation is the conditional information, the sum of the "
            "conditional variances. <bookmark mark='d'/> If that settles after scaling, the martingale central limit "
            "theorem makes the standardized score normal, and the usual Taylor argument makes the maximum likelihood "
            "estimate normal: for Markov chains, time series and branching processes alike, as Part forty-seven proves."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
