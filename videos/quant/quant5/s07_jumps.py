from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, real_data


class Jumps(VoiceoverScene):
    def construct(self):
        j = load("jumps")
        h = load("hawkes")
        self.card()
        self.levy(j)
        self.bitcoin(j)
        self.hawkes(h)

    def card(self):
        c = chapter_card(6, r"Jumps, and jumps that cause jumps", r"What if prices don't move continuously?", part=PART)
        with self.voiceover("Chapter six. Jumps, and jumps that cause jumps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def levy(self, j):
        P = np.asarray(j["merton_paths"])
        n = P.shape[1]
        g = axes([0, 1], [0.3, 1.9], x_length=5.6, y_length=4.2, xlabel=r"time (years)", ylabel=r"price",
                 xticks=[0, 0.5, 1], yticks=[0.5, 1.0, 1.5], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        t = np.linspace(0, 1, n)
        cols = color_gradient([BM, STRAT], len(P))
        paths = VGroup(*[curve(ax, t, np.clip(p, 0.3, 1.9), c, stroke_width=2.2) for p, c in zip(P, cols)])
        rows = VGroup(
            MathTex(r"X_t = b\,t + \sigma W_t + \sum_{s \le t} \Delta X_s", font_size=32),
            label(r"L\'evy--It\^o: drift, plus Brownian motion, plus jumps (compensated when small)", font_size=20,
                  color=GREY_A),
            MathTex(r"df(X_t) = f'\,dX^c_t + \tfrac12 f''\,d\langle X^c\rangle_t + \big[f(X_t) - f(X_{t-})\big]",
                    font_size=28, color=ITO),
            label(r"It\^o for jumps: the continuous part as before, plus each jump's full change", font_size=20,
                  color=GREY_A),
            label(r"Merton (1976): GBM plus Poisson jumps, here 6 a year, mean $-5\%$", font_size=20, color=STRAT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if rows.width > 6.6:
            rows.scale_to_fit_width(6.6)
        rows.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Brownian paths are continuous. Prices are not always: news arrives in lumps, and a price can gap. The "
            "simplest model adds a Poisson clock that rings at random times, and a random jump each time it rings. "
            "<bookmark mark='a'/> Robert Merton proposed exactly this in 1976. <bookmark mark='b'/> More generally, "
            "the Lévy-Itô decomposition says that any process with independent, stationary increments is a drift, "
            "plus a Brownian motion, plus jumps. And Itô's lemma extends: the continuous part behaves as before, and "
            "each jump contributes its full change. <bookmark mark='c'/> What disappears is completeness. A jump of "
            "random size can't be hedged with the stock alone, which is why Part eleven needs options to hedge "
            "options."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3, run_time=4), FadeIn(rows[4]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def bitcoin(self, j):
        edges = np.asarray(j["z_edges"])
        h = np.asarray(j["z_hist"], float)
        mid = (edges[:-1] + edges[1:]) / 2
        w = edges[1] - edges[0]
        N = j["n_hours"]
        gauss = N * (norm.cdf(edges[1:]) - norm.cdf(edges[:-1]))
        g = axes([-12, 12], [-1, 4.2], x_length=7.2, y_length=4.4, xlabel=r"hourly return / local volatility (bipower)",
                 ylabel=r"hours (log scale)", xticks=[-10, -5, 0, 5, 10], yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for m_, c in zip(mid, h):
            if c <= 0:
                continue
            top, bot = ax.c2p(m_, np.log10(c)), ax.c2p(m_, -1)
            col = JUMP if abs(m_) > 5 else BM
            bars.add(Rectangle(width=ax.c2p(w * 0.9, 0)[0] - ax.c2p(0, 0)[0], height=top[1] - bot[1], stroke_width=0,
                               fill_color=col, fill_opacity=0.85).move_to((top + bot) / 2))
        gl = curve(ax, mid, np.log10(np.maximum(gauss, 0.1)), DRIFT, stroke_width=3)
        cut = VGroup(DashedLine(ax.c2p(5, -1), ax.c2p(5, 4.2), color=JUMP, stroke_width=1.5),
                     DashedLine(ax.c2p(-5, -1), ax.c2p(-5, 4.2), color=JUMP, stroke_width=1.5))
        py = j["per_year"]
        side = VGroup(
            label(r"Bitcoin, hourly, 2018--2020", font_size=22, color=GREY_A),
            MathTex(rf"\text{{beyond 5 local sd: }} {j['n_jumps']} \text{{ hours}}", font_size=30, color=JUMP),
            MathTex(rf"\text{{a Gaussian would give }} {j['gauss_expected']:.3f}", font_size=30, color=DRIFT),
            label(rf"by year: {py['2018']}, {py['2019']}, {py['2020']}", font_size=21, color=GREY_A),
            MathTex(rf"\text{{share of all variance: }} {100 * j['share_of_variance']:.0f}\%", font_size=30, color=JUMP),
            wrapped_label(r"scale: bipower variation over the past week, $\tfrac{\pi}{2} \sum |r_t|\,|r_{t-1}|$, which a "
                          r"single jump barely moves (Barndorff-Nielsen and Shephard 2004)", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT one-hour candles, January 2018 -- December 2020")
        with self.voiceover(
            "Are there jumps in real prices? Take Bitcoin's hourly returns for three years and divide each by a local "
            "volatility measured in a way a single jump barely moves: bipower variation, the sum of products of "
            "neighbouring absolute returns. <bookmark mark='a'/> If the hours were Gaussian, the histogram would follow "
            "the green curve, and you would expect one hour in about two hundred years beyond five standard deviations. "
            f"<bookmark mark='b'/> There were {j['n_jumps']}, about seventy a year, and those hours alone carry a "
            f"{100 * j['share_of_variance']:.0f} percent share of all the variance. The jumps are not rare accidents; "
            "they are a structural part of how this market moves."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01, run_time=2))
            vo.wait_until("a")
            self.play(Create(gl), Create(cut), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def hawkes(self, h):
        f = h["fit"]
        grid, lam = np.asarray(h["grid"]), np.asarray(h["lam"])
        ev = np.asarray(h["events"])
        T = h["T"]
        g = axes([0, T], [0, 3.4], x_length=8.0, y_length=3.6, xlabel=r"days since 1 January 2018",
                 ylabel=r"fitted intensity, large moves a day", xticks=[0, 365, 730, 1095], yticks=[0, 1, 2, 3],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        line = curve(ax, grid, np.clip(lam, 0, 3.4), JUMP, stroke_width=2)
        ticks = VGroup(*[Line(ax.c2p(e, 0), ax.c2p(e, 0.25), stroke_width=1.2, color=BM) for e in ev])
        base = DashedLine(ax.c2p(0, f["mu"]), ax.c2p(T, f["mu"]), color=DRIFT, stroke_width=2)
        eq = MathTex(r"\lambda_t = \mu + \sum_{t_i < t} \alpha\,e^{-\beta (t - t_i)}", font_size=34, color=JUMP)
        eq.to_corner(UL, buff=0.5)
        side = VGroup(
            MathTex(rf"\text{{branching ratio }} \alpha/\beta = {f['branching']:.2f}", font_size=30, color=JUMP),
            label(rf"each large move triggers {f['branching']:.2f} more, on average", font_size=21, color=GREY_A),
            label(rf"the excitement halves in {h['half_life_hours']:.1f} hours", font_size=21, color=GREY_A),
            label(rf"log-likelihood {f['loglik']:.0f}, against {f['loglik_poisson']:.0f} for a Poisson clock",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        how = label(r"events: hours with $|r| > 4\times$ the past month's volatility; fitted by maximum likelihood",
                    font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Big moves also come in clusters: one large move makes another more likely soon after. Alan Hawkes wrote "
            "down a point process with that property in 1971. Its intensity, the rate of events, jumps up by alpha "
            "after every event and decays at rate beta back toward a base rate. <bookmark mark='a'/> Fit it to the "
            f"{f['n']} hours since 2018 when Bitcoin moved more than four times its recent volatility. The fitted "
            "intensity spikes after each event and relaxes. <bookmark mark='b'/> The branching ratio, alpha over "
            f"beta, is {f['branching']:.2f}: each large move triggers about a third of another, and the excitement "
            f"halves in about {h['half_life_hours']:.0f} hours. The self-exciting model beats a plain Poisson clock "
            "by a wide margin. Hawkes processes come back in Part fourteen, in rough volatility, and in Part "
            "thirty-six, in the order book, where orders trigger orders."
        ) as vo:
            self.play(FadeIn(g), FadeIn(eq), FadeIn(how))
            vo.wait_until("a")
            self.play(FadeIn(ticks), Create(base))
            self.play(Create(line), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()
