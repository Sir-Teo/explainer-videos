from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, RP_C, SHRINK_C, TRUE_C, fit_right, load


class Growth(VoiceoverScene):
    def construct(self):
        g = load("growth")
        self.card()
        self.kelly(g)
        self.curve_(g)
        self.cover_math()
        self.cover(g)
        self.fernholz(g)
        self.question()

    def card(self):
        c = chapter_card(9, r"Kelly, Cover and Fernholz", r"What if the goal is not the best trade-off between mean and "
                         r"variance, but the fastest growth of wealth?", part=PART)
        with self.voiceover("Chapter nine. Mean-variance is a one-period idea. An investor who reinvests for decades cares "
                            "about something else: how fast wealth compounds. Three answers, from three traditions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kelly(self, g):
        rows = [cmath(r"g(w)", r"=", r"r + w^\top\mu - \tfrac12 w^\top\Sigma w", font_size=34, colors={r"g(w)": TRUE_C}),
                cmath(r"w^*", r"=", r"\Sigma^{-1}\mu", font_size=36, colors={r"w^*": TRUE_C}),
                cmath(r"f^*_{\text{market}}", r"=", rf"\frac{{\mu_m}}{{\sigma_m^2}} = \frac{{{100 * g['mu']:.1f}\%}}"
                      rf"{{{100 * g['s2']:.2f}\%}} = {g['kelly']:.2f}", font_size=30, colors={r"f^*_{\text{market}}": HURDLE})]
        whys = [why(r"the expected log growth rate of a constantly rebalanced portfolio in continuous time "
                    r"($\mu$: excess returns)"),
                why(r"Kelly (1956), Breiman (1961): maximising it gives the portfolio that, with probability one, "
                    r"eventually outgrows any other; it is mean-variance with risk aversion one (Part 8)"),
                why(r"the US market, 1970--2020: the growth-optimal investor would have held the market levered "
                    r"almost three times")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The first answer is Kelly's, which Part eight derived for one bet. <bookmark mark='a'/> The expected log "
            "growth of a constantly rebalanced portfolio is the mean minus half the variance. <bookmark mark='b'/> Its "
            "maximiser is the inverse covariance times the excess returns: mean-variance with a risk aversion of exactly "
            "one, and, with probability one, the portfolio that eventually outgrows every other. "
            f"<bookmark mark='c'/> For the American market from 1970 to 2020 that means a leverage of {g['kelly']:.2f}: "
            "the growth-optimal investor would have borrowed almost two dollars for each one invested."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def curve_(self, g):
        fs = np.asarray(g["fs"], float)
        th = 100 * np.asarray(g["g_theory"], float)
        em = 100 * np.asarray(g["g_emp"], float)
        lo = float(np.floor(np.nanmin(np.r_[th, em]) / 5) * 5)
        hi = float(np.ceil(np.nanmax(np.r_[th, em]) / 5) * 5)
        gr = axes([0, 4], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"fraction of wealth in the market (leverage)",
                  ylabel=r"growth rate of wealth, \% a year", xticks=[0, 1, 2, 3, 4], yticks=[lo, 0, hi], font_size=15
                  ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        lt, le = curve(ax, fs, th, TRUE_C, stroke_width=3), curve(ax, fs, em, REAL_C, stroke_width=3)
        k = float(g["kelly"])
        kl = DashedLine(ax.c2p(k, lo), ax.c2p(k, hi), color=HURDLE, stroke_width=2)
        leg = legend([(TRUE_C, r"$r + f\mu - f^2\sigma^2/2$"), (REAL_C, r"the actual monthly path, rebalanced")],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"past the peak, more leverage means less growth; at twice Kelly, the growth rate is back to "
                             r"the risk-free rate. Practitioners bet a fraction of Kelly, because $\mu$ is estimated",
                             3.4, 15, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        i_emp = int(np.nanargmax(em))
        f_emp = fs[i_emp]
        with self.voiceover(
            "Draw the growth rate against leverage. <bookmark mark='a'/> The formula is a parabola, peaking at the Kelly "
            f"fraction. <bookmark mark='b'/> The actual path of the market, rebalanced monthly, peaks at {f_emp:.2f}, "
            "close by. Past the peak, more leverage means less growth, and at twice Kelly the growth falls back to the "
            "risk-free rate while the risk keeps rising. And the peak depends on an estimated mean: which is why careful "
            "practitioners bet half of Kelly or less."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lt), Create(kl))
            vo.wait_until("b")
            self.play(Create(le), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def cover_math(self):
        rows = [cmath(r"S_n(b)", r"=", r"\textstyle\prod_{t \le n} b^\top x_t", font_size=34, colors={r"S_n(b)": RP_C}),
                cmath(r"\hat b_{n+1}", r"=", r"\frac{\int b\,S_n(b)\,db}{\int S_n(b)\,db}", font_size=34,
                      colors={r"\hat b_{n+1}": RP_C}),
                cmath(r"\frac{\max_b S_n(b)}{\hat S_n}", r"\le", r"(n + 1)^{m - 1}", font_size=34,
                      colors={r"\frac{\max_b S_n(b)}{\hat S_n}": HURDLE})]
        whys = [why(r"the wealth of the constant-rebalanced portfolio $b$ on the price relatives $x_t$"),
                why(r"Cover (1991): hold the performance-weighted average of all of them, which needs no model at all"),
                why(r"for $m$ assets the universal portfolio's wealth trails the best rebalanced portfolio, chosen in "
                    r"hindsight, by at most a polynomial factor: the same exponential growth rate")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The second answer needs no model at all. <bookmark mark='a'/> Consider every constant-rebalanced mix of the "
            "assets, and its wealth so far. <bookmark mark='b'/> Thomas Cover's universal portfolio of 1991 holds their "
            "average, weighted by how well each has done. <bookmark mark='c'/> And he proved that its wealth trails the "
            "best mix chosen in hindsight by at most a polynomial factor in time: it grows at the same exponential rate "
            "as the best constant mix, whatever the market does."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def cover(self, g):
        cv = g["cover"]
        b = np.asarray(cv["b"], float)
        W = np.log(np.asarray(cv["wealth"], float))
        lo, hi = float(np.floor(W.min())), float(np.ceil(W.max()))
        gr = axes([0, 1], [lo, hi], x_length=7.0, y_length=4.2, xlabel=rf"share in {cv['pair'][0]}, the rest in "
                  rf"{cv['pair'][1]}, rebalanced monthly", ylabel=r"log of final wealth, 1970--2020",
                  xticks=[0, 0.5, 1], yticks=[lo, hi], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        line = curve(ax, b, W, RP_C, stroke_width=3)
        uni = DashedLine(ax.c2p(0, math.log(cv["uni"][-1])), ax.c2p(1, math.log(cv["uni"][-1])), color=GOOD, stroke_width=2)
        ratio = cv["best"][-1] / cv["uni"][-1]
        side = VGroup(MathTex(rf"\text{{best mix}}: b = {cv['b_best']:.2f},\ \times{cv['best'][-1]:.0f}", font_size=22,
                              color=RP_C),
                      MathTex(rf"\text{{universal}}: \times{cv['uni'][-1]:.0f}", font_size=22, color=GOOD),
                      MathTex(rf"\text{{ratio}}\ {ratio:.2f} \le {cv['bound']}", font_size=22, color=HURDLE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            f"Two industries that rarely move together, {cv['pair'][0]} and {cv['pair'][1]}, monthly from 1970. "
            "<bookmark mark='a'/> Each point of the curve is a constant mix, rebalanced every month, and its final "
            f"wealth. The best, in hindsight, puts {100 * cv['b_best']:.0f} percent in gold and multiplies wealth "
            f"{cv['best'][-1]:.0f} times. <bookmark mark='b'/> The universal portfolio, which knew nothing in advance, "
            f"multiplied it {cv['uni'][-1]:.0f} times: a ratio of {ratio:.2f}, far inside Cover's bound of "
            f"{cv['bound']}. Notice also that the best mix beats both industries held alone: rebalancing between "
            "volatile assets earns their diversification return."
        ) as vo:
            self.play(FadeIn(gr))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Create(uni), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def fernholz(self, g):
        sp = g["spt"]
        d = np.asarray(sp["dates"], float)
        x = d // 100 + ((d % 100) - 0.5) / 12
        rel = 100 * (np.asarray(sp["cum_div"]) - np.asarray(sp["cum_mkt"]))
        lo, hi = float(np.floor(min(rel.min(), 0) / 5) * 5), float(np.ceil(max(rel.max(), 0) / 5) * 5)
        gr = axes([x[0], x[-1]], [lo, hi], x_length=8.6, y_length=3.8, xlabel=r"",
                  ylabel=r"diversity-weighted minus cap-weighted, cumulative log return, \%", xticks=[1970, 1990, 2010, 2020],
                  yticks=[lo, 0, hi], xfmt=lambda v: f"{v:.0f}", font_size=14).move_to(LEFT * 0.6 + DOWN * 0.5)
        ax = gr.ax
        line = curve(ax, x, rel, SHRINK_C, stroke_width=3)
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_B, stroke_width=1.2)
        eq = MathTex(r"w_i \propto \mu_i^{\,p},\ p = \tfrac12;\qquad \log\frac{V_{\text{div}}}{V_{\text{mkt}}} = "
                     r"\log\frac{D_p(\mu_T)}{D_p(\mu_0)} + (1 - p)\int_0^T\gamma^*_t\,dt", font_size=26).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The third answer is Robert Fernholz's stochastic portfolio theory, which asks when a portfolio beats the "
            "market without forecasting anything. <bookmark mark='a'/> Weight each asset by its market weight raised to "
            "a power p below one, which tilts toward the small. Fernholz's master equation splits its return relative to "
            "the market into a bounded term, the change in the market's diversity, and a term that only accumulates: "
            "the excess growth rate, which is positive whenever assets move apart. <bookmark mark='b'/> On the "
            "forty-nine industries, the diversity-weighted portfolio gained about "
            f"{100 * sp['excess']:.1f} percent a year on the cap-weighted one: small, because industries are few and "
            "broad, and in the long run positive, as the theory says it must be if diversity does not collapse."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(gr), Create(zero))
            vo.wait_until("b")
            self.play(Create(line), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an investor bets twice the Kelly fraction. What is the growth rate relative to the risk-free "
                       r"rate, and why?")
        with self.voiceover(
            "Pause and predict. An investor bets twice the Kelly fraction. What is the growth rate, and why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
