from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, OPT, PART, RV, SPOT, VAR, load, real_data


def _yr(ts):
    return 1970 + np.asarray(ts, float) / (365.2425 * 86400)


class Moves(VoiceoverScene):
    def construct(self):
        f = load("facts")
        self.card()
        self.series(f)
        self.leverage(f)
        self.mixing()

    def card(self):
        c = chapter_card(1, r"Why volatility must move", r"What does a constant volatility leave out?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter one. Why volatility must move."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, f):
        t = _yr(f["t"])
        rv = np.asarray(f["rv30"])
        td = _yr(f["dvol_t"])
        dv = np.asarray(f["dvol"])
        g = axes([2021.25, 2026], [0, 1.4], x_length=8.2, y_length=4.2, ylabel=r"bitcoin volatility, annualized",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0, 0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lr = curve(ax, t, np.clip(rv, 0, 1.4), RV, stroke_width=2.2)
        ld = curve(ax, td, np.clip(dv, 0, 1.4), IV, stroke_width=2.2)
        leg = legend([(RV, r"realized over the past 30 days"), (IV, r"DVOL: implied, 30 days ahead")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"{100 * f['rv_min']:.0f}\% \ \text{{to}}\ {100 * f['rv_max']:.0f}\%", font_size=34, color=RV),
            wrapped_label(r"the range of 30-day realized volatility, April 2021 to November 2025: Black and Scholes "
                          r"assumed one number", 4.0, 20, GREY_A),
            MathTex(rf"\text{{vol of vol}} \approx {100 * f['volvol']:.0f}\%", font_size=32, color=VAR),
            wrapped_label(r"the annualized volatility of DVOL's own daily log changes: volatility is itself a risky "
                          r"asset, and options on it trade", 4.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT daily; Deribit DVOL daily")
        with self.voiceover(
            "Black, Scholes and Merton assumed one volatility, fixed for the life of the option. Here is Bitcoin's. "
            "In green, the volatility it actually realized over each past thirty days. <bookmark mark='a'/> It "
            f"ranged from {100 * f['rv_min']:.0f} percent to {100 * f['rv_max']:.0f} percent a year. "
            "<bookmark mark='b'/> In orange, DVOL, the market's thirty-day implied volatility, read from options. It "
            "moves too. Measured the same way as a price, the volatility of volatility is about "
            f"{100 * f['volvol']:.0f} percent a year. Volatility is not a parameter. It is a second random process, a "
            "second river running beside the price, and an option is a bet on both."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(lr), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(ld), FadeIn(side[2]), FadeIn(side[3]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def leverage(self, f):
        yrs = sorted(f["by_year"])
        vals = [f["by_year"][y] for y in yrs]
        g = axes([-0.5, len(yrs) - 0.5], [-0.7, 0.4], x_length=5.6, y_length=3.8, ylabel=r"corr(return, change in DVOL)",
                 xticks=list(range(len(yrs))), xfmt=lambda u: str(yrs[int(round(u))]), yticks=[-0.6, -0.3, 0, 0.3],
                 font_size=17).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.55, height=abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                                  fill_opacity=0.85, fill_color=BAD if v < 0 else RV)
                        .move_to(ax.c2p(i, v / 2)) for i, v in enumerate(vals)])
        side = VGroup(
            label(r"on days bitcoin fell more than 5\%:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{DVOL}}\ +{f['dvol_change_down5']:.1f}\%", font_size=34, color=BAD),
            label(r"on days it rose more than 5\%:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{DVOL}}\ {f['dvol_change_up5']:+.1f}\%", font_size=34, color=RV),
            wrapped_label(r"Black (1976) called it the leverage effect: as equity falls, firms grow more levered and "
                          r"riskier. Bitcoin has no debt, yet volatility still rises in its falls; in the 2023 rally the "
                          r"sign flipped, as calls were bid on the way up", 5.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5)
        src = real_data(rf"{f['n']} daily pairs, 2021--2025; average change in log DVOL, in percent")
        with self.voiceover(
            "And the two rivers are tied together. On the days Bitcoin fell more than five percent, DVOL rose by "
            f"{f['dvol_change_down5']:.0f} percent on average. On days it rose that much, DVOL barely moved. "
            "<bookmark mark='a'/> Year by year, the correlation between the day's return and the change in implied "
            "volatility was negative in most years, strongly so in 2022. Fischer Black named this in 1976, the "
            "leverage effect: a falling stock makes its firm more levered and riskier. Bitcoin has no debt, and the "
            "effect is still there. In 2023's rally it even flipped sign, as traders bid up calls on the way up. "
            "That correlation is what tilts the smile into a skew."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, UP if v < 0 else DOWN) for b, v in zip(bars, vals)],
                                             lag_ratio=0.2, run_time=2.5), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def mixing(self):
        hist = history_card(1987, r"19 October 1987, and after", r"The Dow fell 22.6\% and the S\&P 500 20.5\% in a day. Before the crash, "
                            r"index options traded close to one flat volatility; ever since, out-of-the-money puts have "
                            r"been dear: the skew (Rubinstein 1994; Bates 2000). Markets learned that volatility jumps "
                            r"when prices fall.", color=QC.CRISIS, width=5.6)
        rows = [cmath(r"C_{\text{HW}}", r"=", r"\mathbb{E}\Big[\,C_{\text{BS}}\big(\bar\sigma^2_T\big)\Big],\quad "
                      r"\bar\sigma^2_T = \tfrac1T\!\int_0^T\!\sigma_t^2\,dt", font_size=32, colors={r"C_{\text{HW}}": OPT}),
                cmath(r"\rho < 0", r"\Rightarrow", r"\text{skew};\quad \text{vol of vol} \Rightarrow \text{curvature}",
                      font_size=32, colors={r"\rho < 0": BAD})]
        whys = [why(r"Hull and White (1987): if volatility moves independently of the price, an option is worth the "
                    r"Black--Scholes price averaged over the variance the path will realize; averaging a curved function "
                    r"lifts both wings: a symmetric smile"),
                why(r"correlate the two rivers and the smile tilts: falling prices with rising volatility make "
                    r"downside strikes dear. The rest of this part is about models that get both right")]
        hist.move_to(ORIGIN)
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.0, buff=1.0, edge=6.9)
        with self.voiceover(
            "The market learned this the hard way. On the nineteenth of October 1987 the S&P 500 fell twenty percent "
            "in a day. Before it, index options traded close to one flat volatility. Ever since, out-of-the-money "
            "puts have been dear. <bookmark mark='a'/> Why does moving volatility make a smile? John Hull and Alan "
            "White showed in 1987 that if volatility moves independently of the price, an option is worth the "
            "Black–Scholes price averaged over the variance the path will realize. Averaging a curved function lifts "
            "both wings: a symmetric smile. <bookmark mark='b'/> Tie the rivers together, so volatility rises as the "
            "price falls, and the smile tilts into the skew. The models of this part are ways of saying exactly how."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hist))
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.4)
        self.clear_scene()
