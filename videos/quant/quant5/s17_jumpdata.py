from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data


class JumpData(VoiceoverScene):
    def construct(self):
        j = load("jumps")
        jh = load("jump_hedge")
        self.card()
        self.bipower()
        self.bitcoin(j)
        self.hedge(jh)

    def card(self):
        c = chapter_card(13, r"Jumps in data, and the hedge they break", r"Are there jumps in real prices, and what do "
                         r"they cost a hedger?", part=PART)
        with self.voiceover("Chapter thirteen. Jumps in real prices, and the hedge they break."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bipower(self):
        rows = [cmath(r"RV", r"=", r"\sum_k r_k^2 \;\to\; \int_0^T \sigma_t^2\,dt + \sum_{s \le T} J_s^2", font_size=34,
                      colors={r"\sum_{s \le T} J_s^2": JUMP}),
                cmath(r"BV", r"=", r"\tfrac{\pi}{2}\sum_k |r_k|\,|r_{k-1}| \;\to\; \int_0^T \sigma_t^2\,dt", font_size=34,
                      colors={r"\int_0^T \sigma_t^2\,dt": ITO}),
                cmath(r"RV - BV", r"\to", r"\sum_{s \le T} J_s^2", font_size=34, colors={r"\sum_{s \le T} J_s^2": JUMP})]
        whys = [why(r"quadratic variation counts every jump's square, as in chapter 12 ($[\widetilde N] = N$)"),
                why(r"$\mathbb{E}|Z| = \sqrt{2/\pi}$; a jump touches a product only next to a neighbour of size "
                    r"$O(\sqrt{\Delta t})$, so it vanishes"),
                why(r"the difference isolates the jumps (Barndorff-Nielsen and Shephard 2004)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "Do real prices jump? Quadratic variation sees diffusion and jumps alike: the sum of squared returns "
            "converges to the integrated variance plus the sum of the squared jumps. <bookmark mark='a'/> Ole "
            "Barndorff-Nielsen and Neil Shephard found a sum that ignores the jumps: products of neighbouring absolute "
            "returns, scaled by pi over two. A jump appears in only two products, each time beside a small diffusive "
            "return, so its contribution vanishes as the sampling gets finer. <bookmark mark='b'/> The difference "
            "between the two measures the jumps, and dividing returns by bipower volatility makes jumps stand out."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
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
            wrapped_label(r"scale: bipower variation over the past week, known before the hour", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT one-hour candles, January 2018 -- December 2020")
        with self.voiceover(
            "Take Bitcoin's hourly returns for three years and divide each by the bipower volatility of the week "
            "before it, which a single jump barely moves. <bookmark mark='a'/> If the hours were Gaussian, the "
            f"histogram would follow the green curve, and you would expect {j['gauss_expected']:.3f} hours beyond five "
            f"standard deviations in three years. <bookmark mark='b'/> There were {j['n_jumps']}, about "
            f"{j['n_jumps'] / 3:.0f} a year, spread evenly across the three years, and those hours alone carry "
            f"{100 * j['share_of_variance']:.0f} percent of all the variance. The jumps are not rare accidents; they "
            "are a structural part of how this market moves, and a model without them misprices every option whose "
            "payoff cares about the tails."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01, run_time=2))
            vo.wait_until("a")
            self.play(Create(gl), Create(cut), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def hedge(self, jh):
        rows_ = jh["rows"]
        x = np.log10([r["n"] for r in rows_])
        yg = np.log10([r["gbm"] for r in rows_])
        yj = np.log10([r["jump"] for r in rows_])
        g = axes([1.0, 3.75], [-1.1, 0.7], x_length=6.6, y_length=4.2, xlabel=r"rebalances a year (log scale)",
                 ylabel=r"spread of the hedge error, dollars (log scale)", xticks=list(np.log10([13, 52, 252, 1000, 4000])),
                 xfmt=lambda u: f"{round(10 ** u):,}".replace(",", "{,}"), yticks=[-1, 0],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dg = [Dot(ax.c2p(a, b), radius=0.07, color=BM) for a, b in zip(x, yg)]
        dj = [Dot(ax.c2p(a, b), radius=0.07, color=JUMP) for a, b in zip(x, yj)]
        lg, lj = curve(ax, x, yg, BM, stroke_width=3), curve(ax, x, yj, JUMP, stroke_width=3)
        leg = legend([(BM, rf"no jumps: slope {jh['slope_gbm']:.2f}"), (JUMP, r"Merton jumps: a floor")],
                     font_size=21).to_corner(UR, buff=0.4)
        rows = [cmath(r"\Delta V - \Delta\cdot\Delta S", r"=", r"\tfrac12 \Gamma S^2 J^2 + O(J^3)", font_size=30,
                      colors={r"\tfrac12 \Gamma S^2 J^2 + O(J^3)": JUMP})]
        w0 = why(r"at a jump of relative size $J$: one instrument cannot offset jumps of two different sizes", 19)
        VGroup(rows[0], w0).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        if w0.width > 5.6:
            w0.scale_to_fit_width(5.6)
        es = theorem_card(r"Esscher (1932)", r"With jumps the risk-neutral measure is not unique: the Esscher transform "
                          r"$dQ/dP \propto e^{\theta X_T}$ is one choice among infinitely many (Part 13).", color=JUMP,
                          width=5.6, font_size=18, kind=r"Note")
        es.next_to(VGroup(rows[0], w0), DOWN, buff=0.3).align_to(leg, LEFT)
        pc, ans = pause(r"Rebalance every second. Does the jump error vanish?", r"No: a jump happens between two trades "
                        r"however close they are.", width=5.6, font_size=20)
        pc.to_corner(DR, buff=0.3)
        ans.next_to(pc, UP, buff=0.1).align_to(pc, LEFT)
        flat = jh["rows"][-1]["jump"] > 0.8 * jh["rows"][2]["jump"]
        verdict = ("barely moves" if flat else "keeps falling, more slowly")
        with self.voiceover(
            "What do jumps do to a hedge? Sell a three-month at-the-money call and delta-hedge it, thirteen to four "
            "thousand times a year, on ten thousand paths. <bookmark mark='a'/> Without jumps, the error's spread "
            f"falls like one over root n. <bookmark mark='b'/> With Merton's jumps, six a year, it {verdict}: at four "
            f"thousand rebalances it is {jh['floor_ratio']:.0f} times the jump-free error. <bookmark mark='c'/> At a "
            "jump the hedged book gains or loses half gamma times the squared jump, and no position in the stock "
            "offsets jumps of different sizes. The market is incomplete, and the risk-neutral measure is not unique. "
            "<bookmark mark='d'/> A pause: rebalance every second, and does the jump error vanish? No: a jump happens "
            "between two trades. Part eleven hedges with options."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dg], lag_ratio=0.3), Create(lg), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dj], lag_ratio=0.3), Create(lj), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(w0))
            self.play(FadeIn(es))
            vo.wait_until("d")
            self.play(FadeIn(pc), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
