from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load, real_data


def glass(share, color_top, label_text, x):
    """A glass of height 3: the stock layer (top colour) over the bond layer."""
    h, w = 3.0, 1.3
    frame = Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=2).move_to([x, -0.6, 0])
    bot = frame.get_bottom()
    bond = Rectangle(width=w, height=h * (1 - share), stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
    bond.move_to(bot + UP * h * (1 - share) / 2)
    stock = Rectangle(width=w, height=h * share, stroke_width=0, fill_color=color_top, fill_opacity=0.85)
    stock.move_to(bot + UP * (h * (1 - share) + h * share / 2))
    pct = MathTex(rf"{100 * share:.0f}\%", font_size=28, color=color_top).next_to(frame, UP, buff=0.1)
    lab = label(label_text, font_size=19, color=GREY_A).next_to(frame, DOWN, buff=0.15)
    return VGroup(bond, stock, frame, pct, lab)


class Merton(VoiceoverScene):
    def construct(self):
        m = load("merton_us")
        rb = load("rebalance_sim")
        self.card()
        self.rebalance(rb)
        self.funds()
        self.fraction(m)

    def card(self):
        c = chapter_card(5, r"Merton's problem", r"How much of your wealth belongs in stocks?", lit=(1969,), part=PART)
        with self.voiceover("Chapter five. Merton's problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rebalance(self, rb):
        pi = rb["pi"]
        pre, bh = np.asarray(rb["path_pre"]), np.asarray(rb["path_bh"])
        price = np.asarray(rb["path_price"])
        n = len(pre)
        g = axes([0, n], [0.6, 1.8], x_length=5.6, y_length=2.6, xlabel=r"months", ylabel=r"the stock",
                 xticks=[0, 20, 40, 60], yticks=[1.0, 1.5], font_size=16).to_edge(RIGHT, buff=0.5).to_edge(UP, buff=0.9)
        tk = ValueTracker(0.0)

        def share_mix(v):
            k = min(int(v), n - 1)
            fr = v - int(v)
            return pi + (pre[k] - pi) * (fr / 0.7 if fr < 0.7 else (1 - fr) / 0.3)

        def share_bh(v):
            return float(np.interp(v, np.arange(n + 1), bh))

        gm = always_redraw(lambda: glass(share_mix(tk.get_value()), KELLY, r"Merton: rebalance monthly", -5.2))
        gb = always_redraw(lambda: glass(share_bh(tk.get_value()), ALT, r"buy and hold", -2.9))
        path = always_redraw(lambda: curve(g.ax, np.arange(int(tk.get_value()) + 1),
                                           price[:int(tk.get_value()) + 1], VALUE, stroke_width=3))
        target = DashedLine([-5.85, -2.1 + 3.0 * pi, 0], [-4.55, -2.1 + 3.0 * pi, 0], color=WHITE, stroke_width=2)
        better = rb["ce_mix"] > rb["ce_bh"]
        side = VGroup(
            wrapped_label(r"stock up: sell some (back to the line); stock down: buy some. Buy-and-hold lets the mix "
                          r"drift with the market", 5.4, 19, GREY_A),
            MathTex(rf"\text{{certainty-equivalent growth, }}\gamma = 3:\ \ {100 * rb['ce_mix']:.2f}\%\ \text{{vs}}\ "
                    rf"{100 * rb['ce_bh']:.2f}\%", font_size=26),
            wrapped_label(rf"after 30 years, buy-and-hold's stock share is anywhere from {100 * rb['bh_frac_p10']:.0f}\% "
                          rf"to {100 * rb['bh_frac_p90']:.0f}\% (10th to 90th percentile)", 5.4, 19, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        src = illustration(rf"simulation: $\mu = 8\%$, $r = 2\%$, $\sigma = 18\%$; {rb['n']:,} thirty-year paths".replace(
            ",", "{,}"))
        q = pause_card(r"Stocks just fell 20\%. Does Merton buy or sell?", width=5.0, font_size=22).next_to(
            g, DOWN, buff=0.4).align_to(g, LEFT)
        with self.voiceover(
            f"The last two chapters found Merton's answer by two methods: hold a constant fraction, the excess return "
            f"over gamma times the variance, {100 * pi:.1f} percent in our market. What does constant mean in "
            "practice? <bookmark mark='a'/> Pause and predict: stocks just fell twenty percent. Does Merton buy or "
            "sell? <bookmark mark='b'/> Watch two glasses over five years of one simulated market, stock on top, "
            "bonds below. When the stock rises, its layer swells; Merton pours it back to the line by selling. When "
            "it falls, he buys. He buys after falls: a contrarian by arithmetic, not by opinion. The second glass "
            "buys and holds, and its mix drifts wherever the market takes it. <bookmark mark='c'/> Over twenty "
            "thousand thirty-year markets, for an investor with gamma three, "
            f"rebalancing comes out ahead, as it must, though only by {100 * (rb['ce_mix'] - rb['ce_bh']):.2f} "
            "percent a year in certainty-equivalent terms; the bigger difference is that buy-and-hold ends with a "
            "stock share that depends on luck."
            if better else
            f"The last two chapters found Merton's answer by two methods: hold a constant fraction, the excess return "
            f"over gamma times the variance, {100 * pi:.1f} percent in our market. What does constant mean in "
            "practice? <bookmark mark='a'/> Pause and predict: stocks just fell twenty percent. Does Merton buy or "
            "sell? <bookmark mark='b'/> Watch two glasses over five years of one simulated market, stock on top, "
            "bonds below. When the stock rises, its layer swells; Merton pours it back to the line by selling. When "
            "it falls, he buys. He buys after falls: a contrarian by arithmetic, not by opinion. The second glass "
            "buys and holds, and its mix drifts wherever the market takes it. <bookmark mark='c'/> Over twenty "
            "thousand thirty-year markets, for an investor with gamma three, "
            "buy-and-hold comes out ahead in this sample, which is simulation noise: the theory says it cannot be "
            "better; the bigger difference is that buy-and-hold ends with a stock share that depends on luck."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.add(gm, gb, path)
            self.play(Create(target))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(q), FadeIn(side[0]))
            self.play(tk.animate.set_value(n - 0.001), run_time=max(min(vo.remaining(10.0) - 6, 18), 8),
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        for mob in (gm, gb, path):
            mob.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def funds(self):
        rows = [cmath(r"\boldsymbol{\pi}^*", r"=", r"\frac{1}{\gamma}\,\Sigma^{-1}(\boldsymbol{\mu} - r\mathbf{1})",
                      font_size=40, colors={r"\boldsymbol{\pi}^*": KELLY}),
                cmath(r"\boldsymbol{\pi}^*", r"=", r"\frac{\mathbf{1}^\top\Sigma^{-1}(\boldsymbol{\mu} - r\mathbf{1})}"
                      r"{\gamma}\ \cdot\ \underbrace{\frac{\Sigma^{-1}(\boldsymbol{\mu} - r\mathbf{1})}{\mathbf{1}^\top"
                      r"\Sigma^{-1}(\boldsymbol{\mu} - r\mathbf{1})}}_{\text{the same risky fund for everyone}}",
                      font_size=34, colors={r"\boldsymbol{\pi}^*": KELLY})]
        whys = [why(r"many stocks: the same HJB, now a quadratic form in the vector $\boldsymbol\pi$; its vertex"),
                why(r"mutual-fund separation (Merton 1971; Tobin 1958): $\gamma$ sets only how much of one fund to hold, "
                    r"not what is in it; Part 30 builds that fund")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-1.0, buff=1.2, edge=6.9)
        with self.voiceover(
            "With many stocks the derivation is the same, with a vector of fractions and a covariance matrix. The "
            "parabola becomes a quadratic form, and its vertex is the inverse covariance matrix times the excess "
            "returns, over gamma. <bookmark mark='a'/> Factor it. The direction of that vector does not depend on "
            "gamma at all: every investor, cautious or bold, holds the same mix of risky assets, and risk aversion "
            "only decides how much of it to hold against the bond. That is Merton's mutual-fund theorem, the "
            "continuous-time cousin of Tobin's separation; Part thirty builds that fund from data."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def fraction(self, m):
        gam = np.asarray(m["gammas"])
        f, lo, hi = (np.asarray(m[k]) for k in ("fraction", "fraction_lo", "fraction_hi"))
        g = axes([0.5, 10.5], [0, 4], x_length=7.0, y_length=4.4, xlabel=r"relative risk aversion $\gamma$",
                 ylabel=r"fraction of wealth in US stocks", xticks=list(range(1, 11)), xfmt=lambda u: f"{int(u)}",
                 yticks=[0, 1, 2, 3, 4], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        one = DashedLine(ax.c2p(0.5, 1), ax.c2p(10.5, 1), color=GREY_B, stroke_width=2)
        ol = label(r"all in, no borrowing", font_size=18, color=GREY_B).next_to(ax.c2p(10.5, 1), UP, buff=0.05).shift(LEFT * 1.0)
        band = VGroup(*[Line(ax.c2p(x, min(a, 4)), ax.c2p(x, min(b, 4)), color=ALT, stroke_width=7).set_opacity(0.45)
                        for x, a, b in zip(gam, lo, hi)])
        dots = VGroup(*[Dot(ax.c2p(x, min(y, 4)), radius=0.07, color=KELLY) for x, y in zip(gam, f)])
        side = VGroup(
            MathTex(r"\pi^* = \frac{\mu - r}{\gamma\,\sigma^2}", font_size=40, color=KELLY),
            MathTex(rf"\mu - r = {100 * m['excess']:.1f}\%,\quad \sigma = {100 * m['sigma']:.1f}\%", font_size=28),
            MathTex(rf"\gamma = 1:\ {100 * f[0]:.0f}\%\qquad \gamma = 3:\ {100 * f[2]:.0f}\%", font_size=28, color=KELLY),
            wrapped_label(rf"bars: the premium $\pm$ 2 standard errors ({100 * m['se_excess']:.1f}\% a year, after "
                          rf"{m['n_months'] // 12} years); for $\gamma = 3$ anything from {100 * lo[2]:.0f}\% to "
                          rf"{100 * hi[2]:.0f}\%", 4.4, 20, ALT),
            wrapped_label(r"Merton (1980): the mean is the hard part; variances are estimated far better than means", 4.4,
                          20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French: US market excess return and T-bill, monthly, July 1926 -- December 2020")
        with self.voiceover(
            "Now put in the American market's history: an excess return of "
            f"{100 * m['excess']:.1f} percent a year over Treasury bills, and a volatility of {100 * m['sigma']:.1f}. "
            f"<bookmark mark='b'/> An investor with log utility should hold {100 * f[0]:.0f} percent of wealth in "
            f"stocks, borrowing to do it. With gamma three, {100 * f[2]:.0f} percent; with gamma ten, {100 * f[-1]:.0f}. "
            "<bookmark mark='c'/> But the excess return is the least certain number in finance. After ninety-four "
            f"years its standard error is still {100 * m['se_excess']:.1f} percent a year, as Merton himself pointed "
            "out in 1980, and the bars show what that does to the answer: for gamma three, anything from "
            f"{100 * lo[2]:.0f} to {100 * hi[2]:.0f} percent. The formula is exact; its inputs are not. Chapter "
            "thirteen meets an investor who takes that doubt seriously."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(ol), FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b_) for b_ in band], lag_ratio=0.1), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
