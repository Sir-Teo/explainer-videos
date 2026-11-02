from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import BTC, LOSS, PART, load, real_data, ts_date

C_ = {r"P": BTC, r"P_0": BTC, r"L": QC.HOUSE, r"m": LOSS}


def row(*parts, fs=40):
    return cmath(*parts, colors=C_, font_size=fs)


LCOL = {"2": QC.GAIN, "3": QC.IDEA, "10": LOSS}


class Margin(VoiceoverScene):
    def construct(self):
        m = load("margin")
        f = load("funding")
        self.card()
        self.mechanics()
        self.formula()
        self.crash(m)
        self.funding(f)

    def card(self):
        c = chapter_card(4, r"Margin and leverage", r"When does a leveraged position get closed for you?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter four. Margin and leverage."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        d1 = definition_card(r"Initial margin", r"The collateral posted to open a position: notional divided by the "
                             r"leverage allowed.", width=4.2, color=QC.HOUSE, font_size=22)
        d2 = definition_card(r"Variation margin", r"Every day (or every second, on crypto exchanges) gains are paid "
                             r"in and losses paid out: the position is marked to market.", width=4.2, color=BTC,
                             font_size=22)
        d3 = definition_card(r"Maintenance margin", r"The minimum the account must keep. Below it: a margin call, or, "
                             r"on most exchanges, liquidation on the spot.", width=4.2, color=LOSS, font_size=22)
        row_ = VGroup(d1, d2, d3).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.6)
        foot = wrapped_label(r"a future's losses are settled every day, so a position can be right in the end and still "
                             r"be closed out along the way", 11.0, 24, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A future or a perpetual swap costs nothing to enter, but the exchange wants collateral. The initial "
            "margin: the position's size divided by the leverage allowed. <bookmark mark='a'/> Then the position is "
            "marked to market: every day, and on crypto exchanges every second, gains are paid in and losses paid "
            "out. <bookmark mark='b'/> If the account falls below the maintenance margin, the trader gets a margin "
            "call, or, on most crypto exchanges, is liquidated on the spot. <bookmark mark='c'/> This is the "
            "difference between a future and a share bought with cash: a futures position can be right in the end "
            "and still be closed out along the way."
        ) as vo:
            self.play(FadeIn(d1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(d2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(d3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def formula(self):
        rows = [
            row(r"\text{equity}", r"=", r"\frac{P_0}{L}", r"+", r"(P - P_0)"),
            row(r"\frac{P_0}{L} + P - P_0", r"=", r"m", r"P"),
            row(r"P_{\text{liq}}", r"=", r"P_0\,\frac{1 - 1/L}{1 - m}"),
        ]
        whys = [why(r"one coin long, opened at $P_0$ with margin $P_0/L$"),
                why(r"liquidated when equity falls to the maintenance level $m$ of the position"),
                why(r"10x: a 9.5\% fall; 3x: 33\%; 2x: 50\% (with $m = 0.5\%$)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "How far can the price fall before the exchange steps in? Hold one coin, opened at P nought with a "
            "margin of P nought over L. The account's equity is that margin plus the gain or loss. "
            "<bookmark mark='a'/> Liquidation comes when equity falls to the maintenance level, a small fraction m "
            "of the position's value. <bookmark mark='b'/> Solve for the price. With a maintenance margin of half "
            "a percent: at ten times leverage, a fall of nine and a half percent ends the position. At three times, "
            "a third. At two times, a half. Leverage doesn't change where the market goes. It changes how far it may "
            "go before you are no longer in it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def crash(self, m):
        t = np.asarray(m["t"])
        p = np.asarray(m["price"])
        days = (t - t[0]) / 86400
        g = axes([0, 19], [3500, 9500], x_length=7.2, y_length=4.6, xlabel=r"March 2020 (UTC)",
                 ylabel=r"BTC perpetual, Binance, hourly close", xticks=[0, 5, 10, 15],
                 xfmt=lambda v: f"{int(v) + 1}", yticks=[4000, 6000, 8000],
                 yfmt=lambda v: rf"\${v / 1000:.0f}\text{{k}}", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, days, p, BTC, stroke_width=2.5)
        marks = VGroup()
        rows = VGroup()
        for L in ("10", "3", "2"):
            r_ = m["runs"][L]
            col = LCOL[L]
            lp = r_["liq_price_formula"]
            hl = DashedLine(ax.c2p(0, lp), ax.c2p(19, lp), color=col, stroke_width=1.8, dash_length=0.08)
            marks.add(hl)
            if r_["liq_index"] >= 0:
                i = r_["liq_index"]
                dot = VGroup(Cross(scale_factor=0.14, stroke_color=col, stroke_width=5).move_to(ax.c2p(days[i], p[i])))
                marks.add(dot)
            rows.add(VGroup(MathTex(rf"{L}\times", font_size=32, color=col),
                            label(rf"margin \${r_['margin']:,.0f}: liquidated ".replace(",", "{,}") +
                                  ts_date(r_["liq_time"], "%d %b, %H:00"), font_size=22)).arrange(RIGHT, buff=0.2))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        res = VGroup(
            MathTex(rf"\text{{1 March}}\ \${m['entry']:,.0f}\ \to\ \text{{13 March}}\ \${m['min_price']:,.0f}".replace(",", "{,}"),
                    font_size=28, color=BTC),
            MathTex(rf"{100 * m['fall']:.0f}\%", font_size=44, color=LOSS),
            wrapped_label(rf"the 2x account ended \${-m['runs']['2']['left']:.0f} below zero: a loss the exchange's "
                          r"insurance fund absorbs", 5.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        src = real_data(r"Binance USD-M BTCUSDT perpetual, hourly closes, with its 8-hourly funding; maintenance "
                        r"margin 0.5\%, a typical rule")
        with self.voiceover(
            "Now a real test. On the first of March 2020 Bitcoin traded at about "
            f"{m['entry']:,.0f} dollars. Three traders open long positions of one coin each on a perpetual swap: at "
            "ten times, three times and two times leverage. The dashed lines are their liquidation prices. "
            "<bookmark mark='a'/> On the ninth of March the price slips under the first line, and the ten-times "
            "trader is gone, nine and a half percent down. <bookmark mark='b'/> Then the twelfth of March, Part one's "
            "crisis. The three-times trader is liquidated that evening. And in the early hours of the thirteenth, "
            f"with Bitcoin at {m['min_price']:,.0f}, {abs(100 * m['fall']):.0f} percent below where it started, "
            "even the two-times trader is closed out, and the account ends below zero: a hole the exchange's "
            "insurance fund has to fill. <bookmark mark='c'/> Within weeks, Bitcoin was back above seven thousand "
            "dollars. None of the three was there to see it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(Create(line), run_time=3)
            self.play(LaggedStart(*[Create(x) for x in marks if isinstance(x, DashedLine)], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[3]), FadeIn(rows[1]))
            self.play(FadeIn(marks[5]), FadeIn(rows[2]))
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.4)
        self.clear_scene()

    def funding(self, f):
        t = np.asarray(f["time"])
        rate = np.asarray(f["rate"])
        days = (t - t[0]) / 86400
        g = axes([0, 366], [-0.0032, 0.0032], x_length=7.4, y_length=3.6, ylabel=r"funding rate, every 8 hours",
                 xticks=[0, 91, 182, 274, 365], xfmt=lambda v: ["Jan", "Apr", "Jul", "Oct", "Dec"][[0, 91, 182, 274, 365].index(int(v))],
                 yticks=[-0.003, 0, 0.003], yfmt=lambda v: f"{100 * v:+.1f}\\%" if v else "0",
                 font_size=18).to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(d, 0), ax.c2p(d, r), stroke_width=1.2, color=QC.GAIN if r > 0 else LOSS)
                        for d, r in zip(days, rate)])
        d = definition_card(r"Funding", r"A perpetual swap never expires. To keep its price near the spot price, "
                            r"longs pay shorts a funding rate every 8 hours when the swap trades above spot, and "
                            r"shorts pay longs when it trades below.", width=4.6, color=BTC, font_size=21)
        d.to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        res = VGroup(
            MathTex(rf"\text{{2020 average:}}\ {100 * f['annualized']:.1f}\%\ \text{{a year}}", font_size=30, color=BTC),
            MathTex(rf"\text{{longs paid in}}\ {100 * f['share_positive']:.0f}\%\ \text{{of settlements}}", font_size=28),
            MathTex(rf"\text{{one coin held long all year: \$}}{f['paid_total']:,.0f}".replace(",", "{,}"), font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g, DOWN, buff=0.45).align_to(g, LEFT)
        with self.voiceover(
            "One more cost. The perpetual swap, crypto's most traded contract, never expires. To keep its price tied "
            "to the coin's, every eight hours one side pays the other a funding rate: longs pay shorts when the "
            "swap trades above the coin, shorts pay longs when it trades below. <bookmark mark='a'/> Through 2020, "
            f"longs paid in {100 * f['share_positive']:.0f} percent of the settlements, about "
            f"{100 * f['annualized']:.0f} percent a year on average: holding one coin long on the swap all year cost "
            f"{f['paid_total']:,.0f} dollars. That is the price of leverage in this market, and it is a trade of its "
            "own: Part thirty-nine harvests it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(d))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.002, run_time=3))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
