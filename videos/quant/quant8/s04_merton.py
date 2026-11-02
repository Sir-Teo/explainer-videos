from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, load, real_data


class Merton(VoiceoverScene):
    def construct(self):
        m = load("merton_us")
        self.card()
        self.fraction(m)

    def card(self):
        c = chapter_card(3, r"Merton's problem", r"How much of your wealth belongs in stocks?", lit=(1969,), part=PART)
        with self.voiceover("Chapter three. Merton's problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

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
            wrapped_label(r"the fraction is constant: sell after a rise, buy after a fall, to keep it; Merton (1969, "
                          r"1971) in continuous time, Samuelson (1969) in discrete", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French: US market excess return and T-bill, monthly, July 1926 -- December 2020")
        with self.voiceover(
            "In 1969 Robert Merton solved the HJB equation for an investor with constant relative risk aversion, "
            "choosing between a stock market with log-normal returns and a riskless bond. The answer is the formula "
            "of the last chapter: hold the fraction excess return over gamma times variance, always. To keep it "
            "constant you must sell after the market rises and buy after it falls. <bookmark mark='a'/> Put in "
            f"the American market's history: an excess return of {100 * m['excess']:.1f} percent a year over "
            f"Treasury bills, and a volatility of {100 * m['sigma']:.1f}. <bookmark mark='b'/> An investor with log "
            f"utility should hold {100 * f[0]:.0f} percent of wealth in stocks, borrowing to do it. With gamma "
            f"three, {100 * f[2]:.0f} percent; with gamma ten, {100 * f[-1]:.0f}. <bookmark mark='c'/> But the "
            "excess return is the least certain number in finance. After ninety-four years its standard error is "
            f"still {100 * m['se_excess']:.1f} percent a year, as Merton himself pointed out in 1980, and the bars "
            f"show what that does to the answer: for gamma three, anything from {100 * lo[2]:.0f} to "
            f"{100 * hi[2]:.0f} percent. The formula is exact; its inputs are not."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(ol), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b_) for b_ in band], lag_ratio=0.1), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
