from __future__ import annotations

import numpy as np
from scipy.stats import levy_stable

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, MART, P_C, PART, Q_C, load, real_data


class Stable(VoiceoverScene):
    def construct(self):
        s = load("stable")
        self.card()
        self.laws()
        self.estimate(s)
        self.scaling(s)

    def card(self):
        c = chapter_card(7, r"Heavy tails as stable laws", r"What shape survives adding up?", lit=(1963,), part=PART)
        with self.voiceover("Chapter seven. Heavy tails, as stable laws."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def laws(self):
        x = np.linspace(-6, 6, 241)
        g = axes([-6, 6], [-4, 0], x_length=7.2, y_length=4.4, xlabel=r"$x$", ylabel=r"density (log scale)",
                 xticks=[-6, -3, 0, 3, 6], yticks=[-4, -3, -2, -1, 0], yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1",
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        alphas = [(2.0, MART), (1.7, P_C), (1.4, Q_C), (1.0, LOSS)]
        curves = VGroup()
        for a, c in alphas:
            y = np.log10(np.maximum(levy_stable.pdf(x, a, 0.0), 1e-4))
            curves.add(curve(ax, x, y, c, stroke_width=3))
        leg = legend([(MART, r"$\alpha = 2$: Gaussian"), (P_C, r"$\alpha = 1.7$"), (Q_C, r"$\alpha = 1.4$"),
                      (LOSS, r"$\alpha = 1$: Cauchy")], font_size=21).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
        side = VGroup(
            wrapped_label(r"stable: a sum of independent copies has the same shape, rescaled by $n^{1/\alpha}$ "
                          r"(L\'evy, 1925)", 4.6, 22, GREY_A),
            wrapped_label(r"for $\alpha < 2$ the tails fall like $|x|^{-1-\alpha}$ and the variance is infinite", 4.6, 22,
                          GREY_A),
            wrapped_label(r"Mandelbrot (1963): cotton prices, $\alpha \approx 1.7$; Fama (1965): the thirty Dow stocks, "
                          r"$\alpha$ below 2", 4.6, 22, P_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(leg, side).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Part one measured how heavy the tails of returns are. Here is the family of distributions Benoit "
            "Mandelbrot proposed for them. The central limit theorem says that sums of many small independent pieces "
            "look Gaussian. Paul Lévy asked, in the 1920s, which shapes survive being added up at all: if you sum "
            "independent copies, you get the same shape, only wider. <bookmark mark='a'/> The answer is the stable "
            "family, indexed by alpha between zero and two. Alpha equal to two is the Gaussian. Below two, the tails "
            "fall like a power of x, so slowly that the variance is infinite. Alpha equal to one is the Cauchy. "
            "<bookmark mark='b'/> In 1963 Mandelbrot fitted cotton prices with alpha near one point seven, and in "
            "1965 Eugene Fama's thesis found alphas below two for the thirty stocks of the Dow. If they were right, "
            "volatility would not exist as a number, and the whole of option pricing would need rebuilding."
        ) as vo:
            self.play(FadeIn(g), Create(curves[0]), FadeIn(leg[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.3), FadeIn(leg[1:]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def estimate(self, s):
        dec = s["decades"]
        keys = sorted(dec)
        g = axes([0, len(keys) + 1.5], [1.0, 2.0], x_length=7.4, y_length=4.2, ylabel=r"McCulloch's $\hat\alpha$, daily returns",
                 xticks=[], yticks=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0], yfmt=lambda u: f"{u:.1f}", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        w = ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0]
        bars, xl = VGroup(), VGroup()
        for i, k in enumerate(keys):
            top, bot = ax.c2p(i + 0.5, dec[k]), ax.c2p(i + 0.5, 1.0)
            bars.add(Rectangle(width=w, height=top[1] - bot[1], stroke_width=0, fill_color=P_C, fill_opacity=0.85).move_to(
                (top + bot) / 2))
            xl.add(label(f"{k}s", font_size=16, color=GREY_B).next_to(bot, DOWN, buff=0.1))
        i = len(keys) + 0.6
        top, bot = ax.c2p(i, s["btc"]["alpha"]), ax.c2p(i, 1.0)
        bb = Rectangle(width=w, height=top[1] - bot[1], stroke_width=0, fill_color=Q_C, fill_opacity=0.85).move_to((top + bot) / 2)
        bl = label(r"BTC", font_size=16, color=Q_C).next_to(bot, DOWN, buff=0.1)
        two = DashedLine(ax.c2p(0, 2.0), ax.c2p(len(keys) + 1.5, 2.0), color=MART, stroke_width=2)
        side = VGroup(
            MathTex(rf"\text{{US, 1926--2020: }} \hat\alpha = {s['full']['alpha']:.2f}", font_size=30, color=P_C),
            MathTex(rf"\text{{Bitcoin, 2017--2020: }} {s['btc']['alpha']:.2f}", font_size=30, color=Q_C),
            wrapped_label(r"estimated from five quantiles of the distribution (McCulloch 1986), which is robust to the "
                          r"extreme days", 4.4, 20, GREY_B),
            wrapped_label(r"Mantegna and Stanley (1995), the S\&P 500 by the minute, 1984--89: $\alpha = 1.40$", 4.4, 21,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Kenneth French's daily US market; Binance BTCUSDT daily; the House's \texttt{stable\_mcculloch}")
        with self.voiceover(
            "Measure it. The House fits a stable law to daily returns from five quantiles, a method published by "
            "J. Huston McCulloch in 1986 that ignores the most extreme days. <bookmark mark='a'/> The American "
            "market, decade by decade: alpha between one point four and one point six, never near two. Over the whole "
            "sample, one point four. Bitcoin, lower still: one point two seven. <bookmark mark='b'/> In 1995 Rosario "
            "Mantegna and Eugene Stanley found the same one point four in the S and P 500 minute by minute. By this "
            "measure, the center of the return distribution is shaped like a stable law."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(two))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(xl), FadeIn(side[0]),
                      FadeIn(side[2]))
            self.play(GrowFromEdge(bb, DOWN), FadeIn(bl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def scaling(self, s):
        ms, msb, msg, ms62 = s["ms"], s["ms_btc"], s["ms_gauss"], s["ms_6286"]
        g = axes([0, np.log10(64) + 0.1], [-0.2, 1.4], x_length=6.6, y_length=4.4,
                 xlabel=r"horizon $h$, days (log scale)", ylabel=r"how many times smaller $P_h(0)$ is than $P_1(0)$ (log scale)",
                 xticks=list(np.log10([1, 2, 4, 8, 16, 32, 64])), xfmt=lambda u: f"{10 ** u:.0f}",
                 yticks=[0, 0.5, 1.0], yfmt=lambda u: {0: "1", 0.5: "3.2", 1.0: "10"}[round(u, 1)], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax

        def pts(m, col):
            h, p = np.log10(np.asarray(m["h"])), np.log10(np.asarray(m["p0"]))
            p0 = p[0]
            p = p0 - p  # falling probability of return, flipped so the lines rise
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=col) for a, b in zip(h, p)])
            fit = m["slope"] * h + m["intercept"] / np.log(10)  # the least-squares line, in log10 units
            line = curve(ax, h, p0 - fit, col, stroke_width=2.5)
            return VGroup(line, dots)

        gs, us, u62, bt = pts(msg, MART), pts(ms, P_C), pts(ms62, QC.GAIN), pts(msb, Q_C)
        leg = legend([(MART, rf"Gaussian: slope {-msg['slope']:.2f}, $\alpha = {msg['alpha']:.2f}$"),
                      (P_C, rf"US 1926--2020: {-ms['slope']:.2f}, $\alpha = {ms['alpha']:.2f}$"),
                      (QC.GAIN, rf"US 1962--86: {-ms62['slope']:.2f}, $\alpha = {ms62['alpha']:.2f}$"),
                      (Q_C, rf"Bitcoin: {-msb['slope']:.2f}, $\alpha = {msb['alpha']:.2f}$")], font_size=20)
        side = VGroup(
            leg,
            MathTex(r"P_h(0) \propto h^{-1/\alpha}", font_size=34),
            wrapped_label(r"the chance a sum over $h$ days lands near zero falls like $h^{-1/\alpha}$: a slope of one half "
                          r"for a Gaussian, more for a stable law", 4.8, 20, GREY_A),
            wrapped_label(r"but Part 1's tails have $\alpha \approx 3$ and a finite variance; the shape is a truncated "
                          r"L\'evy law, or a Gaussian whose volatility changes: Parts 7 and 13", 4.8, 20, LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Mantegna and Stanley's test of stability is elegant. Add up returns over h days, and measure the chance "
            "that the sum lands near zero. For a stable law that chance shrinks like h to the minus one over alpha. "
            "<bookmark mark='a'/> A Gaussian gives a slope of a half on these axes, and simulated Gaussian returns "
            "land on it. <bookmark mark='b'/> The American market falls faster: a slope near point six, an alpha of "
            "one point six seven. Between 1962 and 1986 the alpha is one point four four, Mantegna and Stanley's "
            "number. Bitcoin is close to the full American sample. <bookmark mark='c'/> So is variance infinite? No. "
            "Part one's tail exponent was near three, which means a finite variance, and the far tails fall faster "
            "than any stable law allows. The center looks stable, the tails are truncated: Mantegna and Stanley "
            "called it a truncated Lévy flight. And much of the shape comes from volatility that changes over time, "
            "the subject of Parts seven and thirteen. The variance exists, but it moves."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(FadeIn(gs), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(us), FadeIn(leg[1]))
            self.play(FadeIn(u62), FadeIn(leg[2]))
            self.play(FadeIn(bt), FadeIn(leg[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
