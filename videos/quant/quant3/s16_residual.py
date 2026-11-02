from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, EQUITY, PART, VALUE, load

C_ = {r"P_0": VALUE, r"B_0": EQUITY, r"r": QC.IMPLIED}


class ResidualIncome(VoiceoverScene, ThreeDScene):
    def construct(self):
        ri = load("ri")
        self.card()
        self.derive()
        self.surface(ri)
        self.fade(ri)

    def card(self):
        c = chapter_card(8, r"Residual income and price-to-book", r"What is a firm worth beyond its books?",
                         part=PART)
        with self.voiceover("Chapter eight. Residual income, and price-to-book."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [
            cmath(r"P_0", r"=", r"\sum_{t \ge 1} \frac{D_t}{(1+r)^t}", colors=C_, font_size=38),
            cmath(r"D_t", r"=", r"E_t - (B_t - B_{t-1})", colors=C_, font_size=38),
            cmath(r"P_0", r"=", r"\sum_{t \ge 1} \frac{E_t - r B_{t-1}}{(1+r)^t} + \sum_{t \ge 1}"
                  r"\Big(\frac{B_{t-1}}{(1+r)^{t-1}} - \frac{B_t}{(1+r)^t}\Big)", colors=C_, font_size=34),
            cmath(r"P_0", r"=", r"B_0 + \sum_{t \ge 1} \frac{(\text{ROE}_t - r)\,B_{t-1}}{(1+r)^t}", colors=C_,
                  font_size=38),
            cmath(r"\frac{P}{B}", r"=", r"1 + \frac{\text{ROE} - r}{r - g}", colors=C_, font_size=42),
        ]
        whys = [why(r"a share is worth its discounted dividends"),
                why(r"clean surplus: book equity changes only by earnings and payouts"),
                why(r"substitute, then add and subtract $r B_{t-1}$: the second sum telescopes"),
                why(r"it collapses to $B_0$ when book grows slower than $1+r$ (no bubble): Ohlson (1995)"),
                why(r"constant ROE, book growing at $g$: the residual incomes are a Gordon series")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "In 1995 James Ohlson rewrote the dividend discount model in the language of the balance sheet. Start from the "
            "dividends. <bookmark mark='a'/> Clean surplus says book equity changes only through earnings and payouts, so each "
            "dividend is earnings minus the growth in book. <bookmark mark='b'/> Substitute, then add and subtract r times last "
            "year's book. One sum is earnings in excess of a normal return on book; the other telescopes, each year's book "
            "cancelling the next. <bookmark mark='c'/> What is left is today's book plus the present value of residual income: "
            "return on equity minus the cost of equity, times the book that earned it. Accounting choices that shift earnings "
            "between years shift book too, and the value does not change. <bookmark mark='d'/> With a constant return and book "
            "growing at g, price-to-book is one plus the spread of ROE over r, divided by r minus g."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def surface(self, ri):
        ax = ThreeDAxes(x_range=[0.0, 0.24, 0.04], y_range=[0.0, 0.06, 0.02], z_range=[0, 5, 1], x_length=7.0,
                        y_length=4.6, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6 + RIGHT * 0.4)

        def f(roe, g):
            return float(np.clip(valuation.pb_steady(roe, 0.08, g), 0, 5))

        surf = loss_surface(ax, f, (0.0, 0.24), (0.0, 0.06), resolution=(24, 12), z_lo=0, z_hi=5)
        one = Surface(lambda u, v: ax.c2p(u, v, 1.0), u_range=[0, 0.24], v_range=[0, 0.06], resolution=(4, 2),
                      fill_opacity=0.35, stroke_width=0.5, stroke_color=GREY_B, checkerboard_colors=[GREY_C, GREY_C])
        seam = Line(ax.c2p(0.08, 0, 1), ax.c2p(0.08, 0.06, 1), color=QC.HOUSE, stroke_width=7)
        hint = VGroup(label(r"return on equity: 0 to 24\%", font_size=22, color=VALUE),
                      label(r"growth of book $g$: 0 to 6\%", font_size=22, color=CASH),
                      label(r"price-to-book, at $r = 8\%$; grey plane: $P/B = 1$", font_size=22, color=GREY_A))
        hint.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        rd = VGroup(MathTex(r"\text{ROE} = r:\ P/B = 1\ \text{for every } g", font_size=30, color=QC.HOUSE),
                    MathTex(r"\text{ROE} = 12\%,\ g = 4\%:\ P/B = 2", font_size=30, color=WHITE))
        rd.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
        dot = Dot3D(ax.c2p(0.12, 0.04, 2.0), radius=0.1, color=WHITE)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-115 * DEGREES, zoom=0.8)
        self.add_fixed_in_frame_mobjects(hint, rd)
        self.remove(hint, rd)
        with self.voiceover(
            "Draw that formula as a surface: return on equity across, growth of book running back, price-to-book as the height, "
            "at an eight percent cost of equity. <bookmark mark='a'/> The grey plane is a price-to-book of one, and the surface "
            "cuts it along a single line, where ROE equals the cost of equity, for every growth rate. <bookmark mark='b'/> Fly "
            "along the seam. On one side profitable growth lifts the multiple; on the other, growth only digs the hole deeper: "
            "chapter six's ridge in the accountant's language. <bookmark mark='c'/> A firm earning twelve percent on a book that "
            "grows at four sits at a price-to-book of two."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(one), Create(seam), FadeIn(rd[0]))
            vo.wait_until("b")
            self.move_camera(theta=-175 * DEGREES, phi=78 * DEGREES, run_time=4)
            vo.wait_until("c")
            self.move_camera(theta=-120 * DEGREES, phi=66 * DEGREES, run_time=2, added_anims=[FadeIn(dot), FadeIn(rd[1])])
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, one, seam, dot)),
                                                                  FadeOut(hint), FadeOut(rd)], run_time=1.5)
        self.clear_scene()

    def fade(self, ri):
        roe, res = np.asarray(ri["fade_roe"]), np.asarray(ri["fade_ri"])
        disc = 1.08 ** -np.arange(1, 11)
        g = axes([0, 11], [0, 1.3], x_length=7.2, y_length=4.4, ylabel=r"value per 100 of book", xticks=[],
                 yticks=[0, 0.5, 1.0], yfmt=lambda v: f"{100 * v:.0f}", font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        bw = ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0]
        book = Rectangle(width=bw, height=ax.c2p(0, 1.0)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=EQUITY,
                         fill_opacity=0.85).move_to(ax.c2p(0.5, 0), aligned_edge=DOWN)
        bl = label(r"book", font_size=18, color=EQUITY).next_to(book, DOWN, buff=0.1)
        bars, cum = VGroup(), 1.0
        for k, (v, d_) in enumerate(zip(res, disc), 1):
            h = v * d_ / 100
            r_ = Rectangle(width=bw, height=max(abs(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]), 0.004), stroke_width=0,
                           fill_color=VALUE, fill_opacity=0.85)
            r_.move_to(ax.c2p(k + 0.5, cum), aligned_edge=DOWN)
            cum += h
            bars.add(r_)
        yl = VGroup(*[MathTex(str(k), font_size=18, color=GREY_B).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.1)
                      for k in range(1, 11)])
        side = VGroup(
            label(r"ROE fades from 15\% to the 8\% cost of equity", font_size=21, color=GREY_A),
            label(r"each bar: that year's residual income, discounted", font_size=21, color=VALUE),
            MathTex(rf"P/B = {ri['fade_value'] / 100:.2f}", font_size=36, color=VALUE),
            label(r"the toy firm, 40 quarters, through the House's code:", font_size=20, color=GREY_A),
            MathTex(rf"|V_{{RI}} - V_{{DDM}}| = {ri['check_gap']:.0e}", font_size=30, color=QC.GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        pp = desk_question(r"Pause and predict: a firm's ROE equals its cost of equity. What is its P/B, whatever its "
                           r"growth?", width=5.6, font_size=21).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now one firm, year by year. Its value starts with its book, the blue block, and each year adds a bar: ROE above eight "
            "percent, times book, discounted. <bookmark mark='a'/> This firm earns fifteen percent now, and competition pulls it "
            "towards its cost of equity, so the bars shrink twice over, by the fading spread and by discounting. "
            f"<bookmark mark='b'/> Stack them: a price-to-book of {ri['fade_value'] / 100:.2f}. <bookmark mark='c'/> The identity "
            "is exact: run the toy firm's forty quarters through both formulas and they agree to the last digit a computer keeps. "
            "<bookmark mark='d'/> Pause and predict: a firm's ROE equals its cost of equity. What is its price-to-book, whatever "
            "its growth? One. AQR's quality factor, in chapter seventeen, starts here."
        ) as vo:
            self.play(FadeIn(g), GrowFromEdge(book, DOWN), FadeIn(bl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25, run_time=4), FadeIn(yl),
                      FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()
