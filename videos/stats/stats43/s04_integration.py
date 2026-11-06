from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class Integration(VoiceoverScene):
    def construct(self):
        self.card()
        self.layer_cake()
        self.theorems()
        self.bumps()
        self.typewriter()
        self.ui()
        self.estimator()

    def card(self):
        card = chapter_card(3, r"Integration", r"When can a limit pass inside an expectation?", part=PART)
        with self.voiceover("Chapter three. Integration, and when a limit can pass inside an expectation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def layer_cake(self):
        A = axes([0, 4], [0, 1.2], x_length=5.4, y_length=3.6, xlabel=r"$x$", ylabel=r"$f(x)$", xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 0.5, 1], center=[-3.4, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0, 4, 400)
        f = np.exp(-(xs - 1.4) ** 2) + 0.15 * np.sin(5 * xs) ** 2
        cf = curve(ax, xs, f, LAWC, 4)
        vert = VGroup()
        for x in np.linspace(0.1, 3.9, 20):
            fx = float(np.interp(x, xs, f))
            p0, p1 = ax.c2p(x - 0.09, 0), ax.c2p(x + 0.09, fx)
            vert.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GREY_B, fill_opacity=0.35)
                     .move_to((p0 + p1) / 2))
        horiz = VGroup()
        for t in np.linspace(0.03, 1.0, 16):
            above = xs[f > t]
            if len(above) == 0:
                continue
            # the set {f > t} may be several intervals
            idx = np.flatnonzero(f > t)
            runs = np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)
            for r in runs:
                p0, p1 = ax.c2p(xs[r[0]], t - 0.03), ax.c2p(xs[r[-1]], t + 0.03)
                horiz.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=WASC, fill_opacity=0.6)
                          .move_to((p0 + p1) / 2))
        side = fit_rows(VGroup(
            label(r"Riemann: \ slice the $x$-axis", font_size=24, color=GREY_A),
            label(r"Lebesgue: \ slice the values", font_size=24, color=WASC),
            label(r"$\int f \, d\mu = \int_0^\infty \mu\{f > t\} \, dt$", font_size=26, color=WASC),
            label(r"for $X \ge 0$: \ $E X = \int_0^\infty P(X > t)\, dt$", font_size=24, color=S.ACCENT),
            label(r"(Part 40's RMST is this integral)", font_size=20, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Riemann integrates by slicing the horizontal axis into strips. <bookmark mark='b'/> "
            "Lebesgue slices the values instead: for each height t, measure the set where the function exceeds t, and add "
            "up those measures over t. <bookmark mark='c'/> It is the layer-cake formula, and it needs only that the sets "
            "where f exceeds t can be measured, which is exactly what measurability provides. <bookmark mark='d'/> For a "
            "non-negative random variable it says the expectation is the integral of the tail probability, <bookmark "
            "mark='e'/> the identity behind Part forty's restricted mean survival time."
        ) as vo:
            self.play(FadeIn(A), Create(cf))
            vo.wait_until("a")
            self.play(FadeIn(vert), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeOut(vert), FadeIn(horiz), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def theorems(self):
        rows = [
            cmath(r"\text{MCT}", r":", r"0 \le X_n \uparrow X \ \Rightarrow \ E X_n \uparrow E X", font_size=34),
            cmath(r"\text{Fatou}", r":", r"X_n \ge 0 \ \Rightarrow \ E \liminf X_n \le \liminf E X_n", font_size=34),
            cmath(r"\text{DCT}", r":", r"X_n \to X \text{ a.s.}, \ |X_n| \le Y, \ E Y < \infty \ \Rightarrow \ E X_n \to E X", font_size=32),
            cmath(r"\text{proofs}", r":", r"\text{simple functions} \to \text{MCT} \to \text{Fatou} \to \text{DCT}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"monotone convergence"), why(r"mass can only be lost"), why(r"dominated convergence"), why(r"a chain")]
        with self.voiceover(
            "<bookmark mark='a'/> Three theorems govern limits under the integral. Monotone convergence: if non-negative "
            "variables increase to a limit, their expectations increase to its expectation. <bookmark mark='b'/> Fatou's "
            "lemma: for non-negative variables, the expectation of the lower limit is at most the lower limit of the "
            "expectations. Mass can be lost in the limit, never gained. <bookmark mark='c'/> Dominated convergence: if the "
            "variables converge almost surely and are all bounded by one integrable variable, their expectations converge. "
            "<bookmark mark='d'/> Each proves the next: monotone convergence from simple functions, Fatou from monotone "
            "convergence, and dominated convergence by applying Fatou to Y plus X n and to Y minus X n. Every exchange of a "
            "limit and an expectation in this course, from the score's mean of zero to the delta method, used one of them."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bumps(self):
        A = axes([0, 1], [0, 34], x_length=5.4, y_length=3.8, xlabel=r"$\omega$", ylabel=r"$X_n(\omega) = n \, 1(\omega \le 1/n)$",
                 xticks=[0, 0.5, 1], yticks=[0, 8, 16, 32], center=[-3.4, 0.2, 0])
        ax = A.ax
        cols = [GREY_B, LAWC, S.ALT, S.ACCENT]
        bars = VGroup()
        for n, c in zip([2, 4, 8, 32], cols):
            p0, p1 = ax.c2p(0, 0), ax.c2p(1 / n, n)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=c, stroke_width=3, fill_color=c,
                               fill_opacity=0.25).move_to((p0 + p1) / 2))
        side = fit_rows(VGroup(
            label(r"$E X_n = n \times \tfrac1n = 1$ \ for every $n$", font_size=24, color=LAWC),
            label(r"$X_n(\omega) \to 0$ \ for every $\omega > 0$", font_size=24, color=GREY_A),
            label(r"so $E \lim X_n = 0 < 1 = \lim E X_n$", font_size=24, color=BADC),
            label(r"no integrable $Y$ dominates: \ $\sup_n X_n \approx 1/\omega$", font_size=24, color=BADC),
            label(r"Fatou's inequality, \ strict", font_size=24, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The conditions matter. On the unit interval, let X n be n on the first n-th of the "
            "interval and zero elsewhere: a bump that grows taller and thinner. <bookmark mark='b'/> Its expectation is n "
            "times one over n: one, for every n. <bookmark mark='c'/> But at every point except zero, the bump eventually "
            "passes by, and X n converges to zero. <bookmark mark='d'/> The limit has expectation zero, the expectations "
            "have limit one: the mass escaped to a point. <bookmark mark='e'/> Dominated convergence fails because nothing "
            "integrable bounds all the bumps: their supremum behaves like one over omega, whose integral is infinite. "
            "Fatou's inequality holds, strictly."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.5), run_time=3.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def typewriter(self):
        d = load("integral")
        blocks = d["typewriter"][:15]
        A = axes([0, 15], [0, 1], x_length=8.6, y_length=3.2, xlabel=r"$n$", ylabel=r"$\omega$", xticks=[1, 3, 7, 15], yticks=[0, 0.5, 1],
                 center=[-1.8, 0.75, 0])
        ax = A.ax
        cells = VGroup()
        for n, (k, j, a, b) in enumerate(blocks):
            p0, p1 = ax.c2p(n + 0.1, a), ax.c2p(n + 0.9, b)
            cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=LAWC, fill_opacity=0.85).move_to((p0 + p1) / 2))
        w = DashedLine(ax.c2p(0, 0.3), ax.c2p(15, 0.3), color=S.ACCENT, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"the typewriter: \ indicators sweeping $[0, 1)$ in halves, \ quarters, \ eighths, ...", font_size=24),
            label(r"$E X_n \to 0$: \ in $L^1$, \ and in probability", font_size=24, color=GOODC),
            label(r"but each $\omega$ is hit once in every sweep: \ $X_n(\omega) \to 0$ for no $\omega$", font_size=24, color=BADC),
            label(r"in probability $\not\Rightarrow$ almost surely; \ a subsequence always does", font_size=24, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.65, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The opposite failure. Let X n be the indicator of an interval that sweeps across the unit "
            "interval, first in halves, then quarters, then eighths, like a typewriter carriage. <bookmark mark='b'/> The "
            "intervals shrink, so the expectations tend to zero: convergence in mean and in probability. <bookmark "
            "mark='c'/> But follow any single point, the gold line: every sweep passes over it once, so X n of omega is one "
            "infinitely often and converges for no omega at all. <bookmark mark='d'/> Convergence in probability does not "
            "imply almost sure convergence, as Part six warned. What is true, and is the workhorse of many proofs, is that "
            "a subsequence converges almost surely: here, the first interval of each sweep."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(w), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def ui(self):
        rows = [
            cmath(r"\text{UI}", r":", r"\lim_{K \to \infty} \sup_n E\big[|X_n|\, 1(|X_n| > K)\big] = 0", font_size=34),
            cmath(r"\text{Vitali}", r":", r"X_n \to X \text{ in probability and UI} \iff E|X_n - X| \to 0", font_size=32),
            cmath(r"\text{enough}", r":", r"\sup_n E|X_n|^{1 + \delta} < \infty \ \text{ for some } \delta > 0", font_size=32),
            cmath(r"X_n = n \text{ w.p. } \tfrac1n", r":", r"E[X_n 1(X_n > K)] = 1 \text{ for } n > K: \ \text{not UI}", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"uniform integrability"), why(r"the exact condition"), why(r"a usable test"), why(r"the bump, as a random variable")]
        with self.voiceover(
            "<bookmark mark='a'/> The exact condition is uniform integrability: the tails beyond K carry a share of the "
            "expectation that goes to zero uniformly in n. <bookmark mark='b'/> Vitali's convergence theorem: convergence "
            "in probability plus uniform integrability is equivalent to convergence in mean. <bookmark mark='c'/> A handy "
            "sufficient condition is a uniformly bounded moment of order a little above one. <bookmark mark='d'/> The "
            "bump, written as a random variable that equals n with probability one over n, fails it: beyond any K, its "
            "tail carries the whole expectation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimator(self):
        rows = fit_rows(VGroup(
            label(r"Poisson counts, \ $\hat\theta = 1/\bar X$ \ estimates $1/\lambda$", font_size=26),
            label(r"$\bar X \to \lambda$ almost surely, \ so $\hat\theta \to 1/\lambda$: \ consistent", font_size=26, color=GOODC),
            label(r"but $P(\bar X = 0) = e^{-n\lambda} > 0$, \ so $E\hat\theta = \infty$ \ for every $n$", font_size=26, color=BADC),
            label(r"consistency is about probability; \ bias and MSE need uniform integrability", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A statistician meets this every day. Estimate one over a Poisson mean by one over the "
            "sample mean. <bookmark mark='b'/> By the strong law the sample mean converges, so the estimate converges to the "
            "truth: it is consistent. <bookmark mark='c'/> But there is always a positive chance that every count is zero, "
            "and then the estimate is infinite; its expectation is infinite for every sample size, and its bias and mean "
            "squared error do not even exist. <bookmark mark='d'/> Consistency is a statement about probabilities; "
            "statements about expectations, like asymptotic bias, need uniform integrability, which is why careful "
            "asymptotics, from Part forty-seven on, speaks of limiting distributions rather than limiting moments."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
