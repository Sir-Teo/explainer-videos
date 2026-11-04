from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats6.common import *  # noqa: F403


class Using(VoiceoverScene):
    def construct(self):
        self.card()
        self.demoivre()
        self.local()
        self.continuity()
        self.rare()

    def card(self):
        card = chapter_card(6, r"Using it", r"The normal approximation, \ and how to apply it well", lit=(1733,), part=PART)
        with self.voiceover("Chapter six. Using the normal approximation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def demoivre(self):
        tl = timeline(lit=(1733,)).to_edge(UP, buff=0.35)
        hc = history_card(1733, r"Abraham de Moivre, \ \emph{Approximatio ad summam terminorum binomii $(a+b)^n$}",
                          r"a seven-page Latin pamphlet, \ printed privately on 12 November 1733: \ the binomial's terms, for "
                          r"large $n$, \ follow the curve $e^{-2x^2/n}$", color=S.MUSEUM, width=8.4, font_size=24).move_to([0, 0.9, 0])
        rows = VGroup(label(r"a Huguenot refugee in London, \ who made his living tutoring mathematics and advising gamblers",
                            font_size=24, color=GREY_A),
                      label(r"with James Stirling's $\sqrt{2\pi}$, \ the first appearance of the normal curve", font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "The first central limit theorem was a theorem about coins. <bookmark mark='a'/> In November 1733 Abraham "
            "de Moivre, a French Protestant refugee living in London, printed a seven-page pamphlet in Latin for his "
            "friends. He wanted the sum of the middle terms of the binomial for large n, too many to add by hand. "
            "<bookmark mark='b'/> He made his living tutoring mathematics and advising gamblers, and he had worked on "
            "the problem for twelve years. <bookmark mark='c'/> With the constant root two pi, which his friend James "
            "Stirling supplied, he found that the binomial terms fall away from the middle like e to the minus two x "
            "squared over n: the first appearance of the normal curve."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def local(self):
        d = load("demoivre")
        k, pmf = np.asarray(d["k"]), np.asarray(d["pmf"])
        A = axes([29.5, 70.5], [0, 0.09], x_length=6.8, y_length=4.2, xlabel=r"heads in 100 fair tosses", xticks=[30, 40, 50, 60, 70],
                 yticks=[0, 0.04, 0.08], center=[-3.0, -0.6, 0])
        ax = A.ax
        bars = pmf_bars(ax, k, pmf, SIM, width=0.85)
        xs = np.linspace(29.5, 70.5, 300)
        nrm = curve(ax, xs, normal_pdf(xs, 50, 5), EXACT, 3)
        rows = [
            cmath(r"\binom{n}{k} p^k q^{n-k}", r"\approx", r"\frac{1}{\sqrt{2\pi npq}}\, e^{-(k - np)^2/2npq}", font_size=30),
            cmath(r"P(S = 50)", r"=", rf"{d['exact_eq']:.4f}", r"\ \ \text{vs}\ \ ", rf"\tfrac{{1}}{{5\sqrt{{2\pi}}}} = {d['approx_eq']:.4f}",
                  font_size=30),
        ]
        rows[0][2].set_color(EXACT)
        whys = [why(r"de Moivre--Laplace: \ Stirling's formula for the factorials, \ then $\log(1 + x) \approx x - x^2/2$"),
                why(r"the local version: \ the height of one bar")]
        with self.voiceover(
            "Here's what he found, for a hundred fair tosses. <bookmark mark='a'/> The blue bars are the exact "
            "binomial probabilities. <bookmark mark='b'/> The gold curve is the normal density with the same mean, "
            "fifty, and the same standard deviation, five. <bookmark mark='c'/> De Moivre's approximation: put "
            "Stirling's formula into each factorial, expand the logarithm to second order, and the binomial term "
            "becomes the normal density at k. <bookmark mark='d'/> At the centre the exact chance of fifty heads is "
            f"{d['exact_eq']:.4f}; the curve's height is {d['approx_eq']:.4f}. Laplace extended the result to any p in "
            "1812, which is why it's called the de Moivre–Laplace theorem."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.02))
            vo.wait_until("b")
            self.play(Create(nrm))
            step = ladder(self, rows, whys, keep=2, top=2.6, x=3.6, buff=1.3, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1, transform=False)
        self.clear_scene()

    def continuity(self):
        d = load("demoivre")
        k, pmf = np.asarray(d["k"]), np.asarray(d["pmf"])
        A = axes([49.5, 70.5], [0, 0.085], x_length=7.0, y_length=4.4, xlabel=r"heads in 100 fair tosses", xticks=[50, 55, 60, 65, 70],
                 yticks=[0, 0.04, 0.08], center=[-2.8, -0.6, 0])
        ax = A.ax
        keep = k >= 50
        bars = pmf_bars(ax, k[keep], pmf[keep], GREY_C, width=0.95, opacity=0.5)
        hi = pmf_bars(ax, k[k >= 60], pmf[k >= 60], SIM, width=0.95, opacity=0.9)
        xs = np.linspace(49.5, 70.5, 300)
        nrm = curve(ax, xs, normal_pdf(xs, 50, 5), EXACT, 3)
        a60 = band(ax, np.linspace(60, 70.5, 80), 0 * np.linspace(60, 70.5, 80), normal_pdf(np.linspace(60, 70.5, 80), 50, 5),
                   BOUND, 0.35)
        a595 = band(ax, np.linspace(59.5, 70.5, 80), 0 * np.linspace(59.5, 70.5, 80),
                    normal_pdf(np.linspace(59.5, 70.5, 80), 50, 5), S.LIK, 0.35)
        rows = VGroup(
            MathTex(rf"P(S \ge 60) = {d['exact']:.4f}", r"\quad \text{exact}", font_size=30, color=SIM),
            MathTex(rf"1 - \Phi\big(\tfrac{{60 - 50}}{{5}}\big) = {d['plain']:.4f}", r"\quad \text{area from } 60", font_size=30,
                    color=BOUND),
            MathTex(rf"1 - \Phi\big(\tfrac{{59.5 - 50}}{{5}}\big) = {d['cc']:.4f}", r"\quad \text{from } 59.5", font_size=30,
                    color=S.LIK),
            label(r"each bar covers $k \pm \tfrac12$: \ the continuity correction", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        for r in rows:
            if r.width > 5.6:
                r.width = 5.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.9, 0.6, 0])
        with self.voiceover(
            "Now a tail probability: sixty heads or more. <bookmark mark='a'/> Exactly, adding the bars, it's "
            f"{d['exact']:.4f}, about one chance in thirty-five. <bookmark mark='b'/> The naive approximation takes the "
            "area under the curve from sixty upwards: two standard deviations, "
            f"{d['plain']:.4f}, twenty percent too small. <bookmark mark='c'/> The fault is ours, not the theorem's. "
            "Each bar is one unit wide and centred on its integer, so the bar for sixty starts at fifty-nine and a "
            "half. Take the area from there and you get "
            f"{d['cc']:.4f}, within one percent. <bookmark mark='d'/> That's the continuity correction: when a "
            "continuous curve stands in for a discrete distribution, match the bars, not their labels."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bars), Create(nrm))
            vo.wait_until("a")
            self.play(FadeIn(hi), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(a60), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(a60), FadeIn(a595), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rare(self):
        n, p = 100, 0.03
        k = np.arange(0, 13)
        A = axes([-0.6, 12.6], [0, 0.25], x_length=7.0, y_length=4.2, xlabel=r"successes in 100 trials, \ $p = 0.03$",
                 xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 0.1, 0.2], center=[-2.8, -0.6, 0])
        ax = A.ax
        bars = pmf_bars(ax, k, st.binom.pmf(k, n, p), SIM, width=0.8)
        xs = np.linspace(-0.6, 12.6, 200)
        sd = np.sqrt(n * p * (1 - p))
        nrm = curve(ax, xs, normal_pdf(xs, n * p, sd), EXACT, 3)
        poi = VGroup(*[Dot(ax.c2p(kk, st.poisson.pmf(kk, 3)), radius=0.07, color=S.LIK) for kk in k])
        ex, nc, po = st.binom.sf(5, n, p), st.norm.sf((5.5 - 3) / sd), st.poisson.sf(5, 3)
        rows = VGroup(
            MathTex(rf"P(S \ge 6) = {ex:.3f}", r"\quad \text{exact}", font_size=28, color=SIM),
            MathTex(rf"\text{{normal (corrected): }} {nc:.3f}", font_size=28, color=EXACT),
            MathTex(rf"\text{{Poisson}}(3):\ {po:.3f}", font_size=28, color=S.LIK),
            MathTex(r"\text{skewness} = \frac{1 - 2p}{\sqrt{npq}} = " + f"{(1 - 2 * p) / sd:.2f}", font_size=28, color=GREY_A),
            label(r"rule of thumb: \ trust the normal when $npq \gtrsim 10$;", font_size=24, color=S.ACCENT),
            label(r"for rare events, \ Part 3's Poisson", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r in rows:
            if r.width > 5.6:
                r.width = 5.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 0.5, 0])
        with self.voiceover(
            "The approximation has limits. <bookmark mark='a'/> A hundred trials, each succeeding with chance three "
            "percent: the expected count is only three, and the distribution is visibly skewed. <bookmark mark='b'/> "
            "The normal curve spills below zero and misses the shape. <bookmark mark='c'/> For six or more "
            f"successes, the corrected normal gives {nc:.3f} against an exact {ex:.3f}, while Part 3's Poisson "
            f"approximation, the green dots, gives {po:.3f}. <bookmark mark='d'/> The skewness, one minus two p over "
            "root n p q, tells you how far you are from the bell. A common rule of thumb asks for n p q of ten or "
            "more; for rare events, use the Poisson."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Create(nrm))
            vo.wait_until("c")
            self.play(FadeIn(poi), FadeIn(rows[:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()
