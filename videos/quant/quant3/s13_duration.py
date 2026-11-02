from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, PART, VALUE, load, real_data

C_ = {r"P": VALUE, r"D_1": CASH, r"r": QC.IMPLIED, r"g": CASH, r"D": DEBT}


class Duration(VoiceoverScene):
    def construct(self):
        d = load("duration")
        self.card()
        self.derive()
        self.fulcrum()
        self.sensitivity()
        self.measured(d)

    def card(self):
        c = chapter_card(2, r"The duration of equity", r"How long is a stock?", lit=(1938,), part=PART)
        with self.voiceover("Chapter two. The duration of equity."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [
            cmath(r"\ln P", r"=", r"\ln D_1 - \ln(r - g)", colors=C_, font_size=42),
            cmath(r"-\frac{\partial \ln P}{\partial r}", r"=", r"\frac{1}{r - g}", colors=C_, font_size=42),
            cmath(r"\text{Macaulay}", r"=", r"\sum_{t \ge 1} t\, w_t", r"=", r"\frac{1 + r}{r - g}", colors=C_,
                  font_size=42),
            cmath(r"r = 8\%,\ g = 5\%", r":", r"\ 33\ \text{years (modified)},\ \ 36\ \text{(Macaulay)}", font_size=36),
        ]
        whys = [why(r"take logs of Gordon's $P = D_1/(r - g)$"),
                why(r"differentiate in $r$: the modified duration, the percentage price change per unit of rate"),
                why(r"$w_t$: the share of value paid in year $t$, $(1 - q)q^{t-1}$ with $q = (1+g)/(1+r)$; "
                    r"sum $t\,w_t$ (differentiate the geometric series)"),
                why(r"a stock growing at 5\% behaves like a bond of more than thirty years")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.62, edge=6.9)
        with self.voiceover(
            "Frederick Macaulay defined the duration of a bond in 1938: the average date of its payments, each weighted by its "
            "share of the value. A stock has a duration too. Take logs of Gordon's formula. <bookmark mark='a'/> Differentiate "
            "with respect to the discount rate: the price falls by one over r minus g percent for each point the rate rises, the "
            "modified duration. <bookmark mark='b'/> Weight each year by its share of the value, a geometric sequence, and sum "
            "year times share: one plus r over r minus g. <bookmark mark='c'/> At an eight percent rate and five percent growth, "
            "thirty-three years modified, thirty-six Macaulay. On paper, a growing stock is a very long bond."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def fulcrum(self):
        H = 60
        g = axes([0, H], [0, 0.085], x_length=11.0, y_length=3.6, xlabel=r"year $t$",
                 ylabel=r"share of today's value paid in year $t$", xticks=[0, 10, 20, 30, 40, 50, 60],
                 yticks=[0, 0.04, 0.08], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).move_to(DOWN * 0.1)
        ax = g.ax
        gt = ValueTracker(0.0)
        r = 0.08
        bw = _bw = ax.c2p(0.8, 0)[0] - ax.c2p(0, 0)[0]
        bond = _bond_w(r, 30)

        def bars():
            w = valuation.pv_weights(r, gt.get_value(), H)
            out = VGroup()
            for t, v in enumerate(w, 1):
                h = ax.c2p(0, min(v, 0.085))[1] - ax.c2p(0, 0)[1]
                out.add(Rectangle(width=bw, height=max(h, 0.003), stroke_width=0, fill_color=VALUE,
                                  fill_opacity=0.8).move_to(ax.c2p(t, 0), aligned_edge=DOWN))
            return out

        def pivot():
            D = valuation.gordon_duration(r, gt.get_value())["macaulay"]
            x = ax.c2p(min(D, H + 2), 0)
            tri = Triangle(color=QC.HOUSE, fill_opacity=1, stroke_width=0).scale(0.16).move_to(x + DOWN * 0.18)
            lab = MathTex(rf"D = {D:.0f}\ \text{{years}}", font_size=28, color=QC.HOUSE).next_to(tri, DOWN, buff=0.12)
            gl = MathTex(rf"g = {100 * gt.get_value():.1f}\%", font_size=30, color=CASH).to_corner(UR, buff=0.5)
            return VGroup(tri, lab, gl)

        bondbars = VGroup()
        for t, v in enumerate(bond, 1):
            h = ax.c2p(0, min(v, 0.085))[1] - ax.c2p(0, 0)[1]
            bondbars.add(Rectangle(width=bw * 0.35, height=max(h, 0.003), stroke_width=0, fill_color=DEBT,
                                   fill_opacity=0.9).move_to(ax.c2p(t, 0), aligned_edge=DOWN))
        bl = label(r"a 30-year 5\% bond at 8\% (the spike: its principal)", font_size=20, color=DEBT)
        bl.to_corner(UL, buff=0.4).shift(DOWN * 0.4)
        sl = label(r"a stock growing at $g$, discounted at 8\%", font_size=20, color=VALUE).next_to(bl, DOWN, buff=0.1)
        sl.align_to(bl, LEFT)
        st = always_redraw(bars)
        pv = always_redraw(pivot)
        with self.voiceover(
            "Here are those weights as a picture: each bar the share of a stock's value paid in one year, at an eight percent "
            "rate, and the orange triangle the balance point, the duration. With no growth it balances at about thirteen and a "
            "half years. <bookmark mark='a'/> For scale, a thirty-year bond: coupons, and a spike of principal. "
            "<bookmark mark='b'/> Now let growth rise towards the rate. The mass slides right, the tail fattens, and the balance "
            "point runs towards the horizon: at seven percent growth, more than a century. <bookmark mark='c'/> Most of a growth "
            "stock's value is cash nobody alive will see paid, which is why it is so sensitive to the rate."
        ) as vo:
            self.play(FadeIn(g), FadeIn(sl))
            self.add(st, pv)
            vo.wait_until("a")
            self.play(FadeIn(bondbars), FadeIn(bl))
            vo.wait_until("b")
            self.play(gt.animate.set_value(0.07), run_time=7, rate_func=smooth)
            vo.wait_until("c")
            self.play(Indicate(pv[1] if len(pv) > 1 else pv, color=QC.HOUSE))
        st.clear_updaters()
        pv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def sensitivity(self):
        rs = np.linspace(0.04, 0.12, 161)
        V = 5 / (rs - 0.03)
        g = axes([0.04, 0.12], [0, 520], x_length=7.6, y_length=4.4, xlabel=r"discount rate $r$",
                 ylabel=r"value of a dividend of 5 growing at 3\%", xticks=[0.05, 0.08, 0.11],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yticks=[0, 100, 200, 300, 400, 500], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, rs, np.clip(V, 0, 519), VALUE, stroke_width=3.5)
        dots = VGroup(*[Dot(ax.c2p(r, 5 / (r - 0.03)), radius=0.08, color=QC.IMPLIED) for r in (0.08, 0.07, 0.05)])
        labs = VGroup(*[MathTex(rf"r = {int(100 * r)}\%:\ {5 / (r - 0.03):.0f}", font_size=28, color=QC.IMPLIED)
                        for r in (0.08, 0.07, 0.05)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lesson = wrapped_label(r"one point off the rate: $+25\%$ at $r - g = 5\%$, $+100\%$ at $r - g = 2\%$; the "
                               r"modified duration $1/(r-g)$ in action", 4.4, 23, GREY_A)
        side = VGroup(labs, lesson).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        with self.voiceover(
            "In numbers: five growing at three percent, discounted at eight, is worth a hundred. <bookmark mark='a'/> At seven, a "
            "hundred and twenty-five; at five, two hundred and fifty. <bookmark mark='b'/> The closer the rate to growth, the "
            "steeper the curve: one answer to Shiller's puzzle."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2)
            self.play(FadeIn(dots[0]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labs[1]))
            self.play(FadeIn(dots[2]), FadeIn(labs[2]))
            vo.wait_until("b")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def measured(self, d):
        b = np.asarray(d["beta"])
        se = np.asarray(d["se"])
        lo_i, hi_i = d["deciles"].index("Lo 10"), d["deciles"].index("Hi 10")
        growth, value = 100 * b[lo_i], 100 * b[hi_i]
        pred = -100 * d["gordon_mod"] * 0.01
        g = axes([0, 3], [-4, 0.5], x_length=6.0, y_length=4.4, ylabel=r"return per point rise in the 10-year yield",
                 xticks=[], yticks=[-4, -3, -2, -1, 0], yfmt=lambda v: f"{v:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bw = ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0]

        def bar(x, v, col):
            top, bot = ax.c2p(x, 0), ax.c2p(x, v)
            return Rectangle(width=bw, height=abs(top[1] - bot[1]), stroke_width=0, fill_color=col,
                             fill_opacity=0.85).move_to((top + bot) / 2)

        bars = VGroup(bar(0.9, growth, VALUE), bar(2.1, value, CASH))
        errs = VGroup(*[Line(ax.c2p(x, v - 196 * s_), ax.c2p(x, v + 196 * s_), color=WHITE, stroke_width=2)
                        for x, v, s_ in ((0.9, growth, se[lo_i]), (2.1, value, se[hi_i]))])
        names = VGroup(label(r"growth (lowest B/M)", font_size=19, color=VALUE).next_to(ax.c2p(0.9, 0), UP, buff=0.12),
                       label(r"value (highest B/M)", font_size=19, color=CASH).next_to(ax.c2p(2.1, 0), UP, buff=0.12))
        nums = VGroup(MathTex(rf"{growth:.2f}\%", font_size=26, color=VALUE).next_to(bars[0], RIGHT, buff=0.1),
                      MathTex(rf"{value:.2f}\%", font_size=26, color=CASH).next_to(bars[1], RIGHT, buff=0.1))
        ordered = growth < value
        side = VGroup(
            label(r"monthly returns on the month's change in the 10-year yield", font_size=20, color=GREY_A),
            label(rf"July 1963 -- December 2020, {d['n']} months; bars $\pm$1.96 s.e.\ (Newey--West)", font_size=18,
                  color=GREY_B),
            MathTex(rf"\text{{Gordon at }} r - g = 3\%:\ {pred:.0f}\%", font_size=32, color=QC.LOSS),
            wrapped_label(r"the order is right" if ordered else r"even the order is wrong", 4.4, 24,
                          QC.GAIN if ordered else QC.LOSS),
            wrapped_label(r"the size is off by more than ten times: when yields rise on inflation, expected dividends "
                          r"rise too, and $g$ moves with $r$", 4.6, 21, GREY_A),
            wrapped_label(r"Dechow, Sloan and Soliman (2004) estimate implied equity durations of about 15 years",
                          4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's book-to-market deciles (value-weighted); Shiller's GS10")
        order_line = ("The order is what duration predicts: growth, the longer asset, is more sensitive. " if ordered
                      else "Even the order is wrong: value moved more than growth. ")
        pp = desk_question(r"Pause and predict: Gordon says a one-point rise in yields should cut a growth stock by a "
                           r"third. What did the data say?", width=6.0, font_size=21).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Does the market price stocks like long bonds? Pause and predict: Gordon says a one-point rise in yields should cut "
            "such a stock by a third. <bookmark mark='a'/> Measured on French's portfolios since 1963, against the monthly change "
            f"in the ten-year yield: growth stocks lost {abs(growth):.1f} percent per point, value stocks {abs(value):.1f}. "
            f"<bookmark mark='b'/> {order_line}But the size is off more than tenfold. <bookmark mark='c'/> When yields rise "
            "with inflation, expected dividends rise too, so g moves with r. Dechow, Sloan and Soliman measured implied durations "
            "of about fifteen years."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(side[:2]))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_ in bars], lag_ratio=0.4), FadeIn(names), FadeIn(nums),
                      Create(errs))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()


def _bond_w(y, n, c=0.05):
    cf = np.full(n, c * 100.0)
    cf[-1] += 100
    pv = cf / (1 + y) ** np.arange(1, n + 1)
    return pv / pv.sum()
