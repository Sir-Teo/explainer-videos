from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats11.common import *  # noqa: F403


class Simultaneous(VoiceoverScene):
    def construct(self):
        self.card()
        self.joint()
        self.bonferroni()
        self.joint_sim()
        self.scheffe()
        self.dkw()
        self.band_vs_points()

    def card(self):
        card = chapter_card(8, r"Simultaneous intervals", r"When several promises must hold at once", part=PART)
        with self.voiceover("Chapter eight. Simultaneous intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def joint(self):
        rows = [
            cmath(r"P(\text{all } k \text{ cover})", r"=", r"0.95^k \quad\text{if independent}", font_size=34),
            cmath(r"k = 10", r":", r"0.95^{10} = 0.60", font_size=34),
        ]
        rows[1][2].set_color(MISS)
        whys = [why(r"Part 10's family-wise error, \ for intervals"), why(r"ten 95\% intervals: \ all right only 60\% of the time")]
        intro = label('Several individual promises versus one joint promise', font_size=36)
        with self.voiceover(
            "Part 10's multiple-testing problem has an interval version. <bookmark mark='a'/> If you report k intervals, "
            "each at ninety-five percent, the chance that all of them cover their targets is ninety-five percent to the "
            "k, if they're independent. <bookmark mark='b'/> With ten, sixty percent. If a conclusion depends on all the "
            "intervals being right at once, the individual promises aren't enough."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=1.6, x=-0.4, buff=1.0, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def bonferroni(self):
        k = 5
        z1, zb = stats.norm.ppf(0.975), stats.norm.ppf(1 - 0.025 / k)
        rows = [
            cmath(r"P(\text{some interval misses})", r"\le", r"\sum_{j=1}^k P(\text{interval } j \text{ misses}) = k\,\frac{\alpha}{k} = \alpha", font_size=30),
            cmath(r"k = 5:\ \ z_{1 - \alpha/(2k)}", r"=", rf"{zb:.2f}\quad\text{{instead of}}\ {z1:.2f}", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"each at level $1 - \alpha/k$: \ the union bound, \ any dependence"), why(rf"each interval {zb / z1:.2f} times wider")]
        with self.voiceover(
            "<bookmark mark='a'/> The Bonferroni fix works for intervals as for tests: make each one at level one minus "
            "alpha over k, and the union bound guarantees that all k hold together with probability at least one minus "
            "alpha, however they're related. <bookmark mark='b'/> For five intervals, the multiplier rises from one point "
            "nine six to two point five eight: each interval is about a third wider."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=1.6, x=0.6, buff=1.0, edge=6.9)
            for kk, m_ in enumerate("ab"):
                vo.wait_until(m_)
                step(kk, transform=False)
        self.clear_scene()

    def scheffe(self):
        hc = history_card(1953, r"Henry Scheff\'e, \ \emph{Biometrika} 40", r"intervals for \emph{every} contrast among $k$ means at once, \ "
                          r"including ones chosen after looking at the data; \ independent normal errors, common variance", color=OBS, width=8.4, font_size=24).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\sum_j c_j\bar x_j \pm \sqrt{(k - 1)\,F_{k-1,\,\nu,\,0.95}}\ \ \widehat{\mathrm{SE}}\Big(\sum_j c_j\bar x_j\Big),\qquad \sum_j c_j = 0",
                    font_size=30),
            label(r"infinitely many intervals, \ one 95\% guarantee: \ the price of fishing, \ paid in advance", font_size=24, color=OBS),
            label(r"Tukey (1953) for all pairwise differences; \ Working--Hotelling bands for a regression line (Part 12)", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.36, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the independent normal common-variance model, Henry Scheffé went further in 1953. His intervals cover every contrast among k group "
            "means simultaneously, infinitely many of them, including contrasts you only thought of after looking at "
            "the data. <bookmark mark='b'/> The multiplier comes from the F distribution, square root of k minus one times "
            "an F quantile. <bookmark mark='c'/> It's the price of fishing, paid in advance: wider intervals, but a "
            "promise that survives any amount of looking. <bookmark mark='d'/> John Tukey's method does the same for all "
            "pairwise differences, and the Working–Hotelling band of Part 12 does it for every point on a regression "
            "line."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def dkw(self):
        d = load("simultaneous")
        x, lo, hi = np.asarray(d["x"]), np.asarray(d["lo"]), np.asarray(d["hi"])
        grid, Ft = np.asarray(d["grid"]), np.asarray(d["Ftrue"])
        A = axes([155, 197], [0, 1], x_length=8.0, y_length=4.6, xlabel=r"height (cm), \ 100 of the World's men", ylabel=r"$F(t)$",
                 xticks=[160, 170, 176, 180, 190], yticks=[0, 0.5, 1], center=[-1.8, -0.3, 0])
        ax = A.ax

        def steps(xs, ys, color, sw, initial=0.0):
            # Include the pre-first-observation band and geometrically clip the viewport.
            pts = [(min(155.0, float(xs[0])), initial)]
            previous = initial
            for value, height in zip(xs, ys):
                pts.extend([(float(value), previous), (float(value), float(height))])
                previous = float(height)
            pts.append((max(197.0, float(xs[-1])), previous))
            coordinates = np.asarray(pts)
            return polyline(ax, coordinates[:, 0], coordinates[:, 1], color, sw)

        f = np.arange(1, len(x) + 1) / len(x)
        ec = steps(x, f, DATA, 3)
        band = VGroup(steps(x, hi, OBS, 1.8, initial=d["eps"]), steps(x, lo, OBS, 1.8))
        true = polyline(ax, grid, Ft, EXACT, 2.5)
        rows = fit_rows(VGroup(
            MathTex(r"P\Big(\sup_t |\hat F_n(t) - F(t)| > \varepsilon\Big) \le 2e^{-2n\varepsilon^2}", font_size=28),
            MathTex(rf"\varepsilon = \sqrt{{\frac{{\log(2/\alpha)}}{{2n}}}} = {d['eps']:.3f}", font_size=30, color=OBS),
            label(r"Dvoretzky, \ Kiefer \& Wolfowitz (1956); \ Massart's constant (1990)", font_size=22, color=GREY_A),
            label(r"a 95\% band for the whole curve, \ for any $F$", font_size=24, color=OBS),
        ), 5.0, 0.36, [4.4, -0.3, 0])
        tag = simulated_tag(r"the World: \ heights", corner=UR)
        with self.voiceover(
            "The most beautiful simultaneous interval is a band around a whole distribution. <bookmark mark='a'/> Here's "
            "the empirical distribution function of a hundred of the World's men, Part 1's staircase. "
            "<bookmark mark='b'/> The Dvoretzky–Kiefer–Wolfowitz inequality, from 1956, with the sharp constant Pascal "
            "Massart proved in 1990, says the chance that the staircase strays more than epsilon from the true curve, "
            "anywhere at all, is at most two e to the minus two n epsilon squared. <bookmark mark='c'/> Solve for "
            "epsilon at five percent: point one three six for a hundred observations. <bookmark mark='d'/> So this band, "
            "the staircase plus and minus point one three six, contains the entire true distribution function with "
            "probability at least ninety-five percent, whatever that distribution is. <bookmark mark='e'/> Here's the "
            "truth, in green, inside it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ec), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(Create(band), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(true))
        self.clear_scene()

    def band_vs_points(self):
        d = load("simultaneous")
        bars = VGroup()
        specs = [(r"DKW band", d["band_cov"], OBS), (r"nominal Wald intervals: \ all 200 grid points", d["point_cov"], MISS)]
        for i, (t, v, c) in enumerate(specs):
            y = 1.0 - 1.4 * i
            bars.add(VGroup(label(t, font_size=26, color=c).move_to([-3.8, y, 0]),
                            Rectangle(width=6.0 * v + 0.01, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([0, y, 0], aligned_edge=LEFT),
                            MathTex(rf"{100 * v:.1f}\%", font_size=32, color=c).move_to([6.4, y, 0])))
        for b in bars:
            if b[0].width > 4.4:
                b[0].width = 4.4
            b[0].align_to([-0.4, 0, 0], RIGHT)
        head = label(r"joint coverage in 2,000 IID samples of 100", font_size=26).to_edge(UP, buff=0.8)
        foot = label(r"Wald intervals also fail individually near the tails; \ DKW controls the whole CDF", font_size=26, color=OBS).to_edge(DOWN, buff=1.0)
        tag = simulated_tag(r"simulated: \ the World", corner=DR)
        with self.voiceover(
            "How much does the simultaneity matter? <bookmark mark='a'/> Over two thousand samples of a hundred men, the "
            "band contains the whole true curve ninety-five point eight five percent of the time, checking both limits at all CDF jumps. "
            "<bookmark mark='b'/> Now try the naive alternative: a separate nominal ninety-five percent Wald interval for the "
            "distribution function at each of two hundred points, and ask how often all of them hold together. Less "
            "than one percent of the time. <bookmark mark='c'/> These Wald intervals also undercover individually near the tails, so this comparison combines poor marginal calibration with multiplicity. It does not isolate simultaneity alone. The band was built for the joint promise, and Part 48 shows where its shape comes "
            "from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(bars[k][0]), GrowFromEdge(bars[k][1], LEFT), FadeIn(bars[k][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def joint_sim(self):
        from scipy import stats as st
        g = np.random.Generator(np.random.PCG64(1961))
        R, k, n = 10000, 10, 15
        x = g.normal(0, 1, (R, k, n))
        m, s = x.mean(2), x.std(2, ddof=1)
        t95, tb = st.t.ppf(0.975, n - 1), st.t.ppf(1 - 0.025 / k, n - 1)
        all95 = np.mean(np.all(np.abs(m) <= t95 * s / np.sqrt(n), 1))
        allb = np.mean(np.all(np.abs(m) <= tb * s / np.sqrt(n), 1))
        bars = VGroup()
        for i, (t, v, c) in enumerate(((r"ten separate 95\% intervals", all95, MISS), (r"ten Bonferroni intervals (99.5\% each)", allb, HIT))):
            y = 0.8 - 1.4 * i
            bars.add(VGroup(label(t, font_size=24, color=c).move_to([-3.8, y, 0]),
                            Rectangle(width=6.0 * v + 0.01, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([-0.6, y, 0], aligned_edge=LEFT),
                            MathTex(rf"{100 * v:.1f}\%", font_size=32, color=c).move_to([6.2, y, 0])))
        for b in bars:
            if b[0].width > 4.4:
                b[0].width = 4.4
            b[0].align_to([-0.8, 0, 0], RIGHT)
        head = label(r"how often all ten intervals hold at once", font_size=28).to_edge(UP, buff=0.8)
        foot = label(rf"the price: \ $t$ multiplier {tb:.2f} instead of {t95:.2f}", font_size=24, color=GREY_A).to_edge(DOWN, buff=1.0)
        tag = simulated_tag(r"simulated: \ 10,000 sets of ten $t$-intervals, \ $n = 15$", corner=DR)
        with self.voiceover(
            "A simulation makes it concrete. Ten independent means, each with a t-interval from fifteen observations. "
            "<bookmark mark='a'/> Each interval keeps its promise, but all ten hold together only sixty percent of the "
            "time, just as point nine five to the tenth predicts. <bookmark mark='b'/> With Bonferroni's adjustment, each "
            "interval at ninety-nine and a half percent, all ten hold together ninety-five percent of the time. "
            "<bookmark mark='c'/> The price is a multiplier of three point three instead of two point one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for kk, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(bars[kk][0]), GrowFromEdge(bars[kk][1], LEFT), FadeIn(bars[kk][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
