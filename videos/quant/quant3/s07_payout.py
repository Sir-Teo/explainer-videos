from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, PRICE, VALUE, load, real_data

F_, T_, SA, R_ = 80.0, 5.0, 0.25, 0.02


def stack(ops, cash, shares, title, color=VALUE):
    """A firm as a stacked bar: operations and cash, with the price per share."""
    unit = 0.0033
    o = Rectangle(width=1.5, height=ops * unit, stroke_width=0, fill_color=VALUE, fill_opacity=0.75)
    c = Rectangle(width=1.5, height=max(cash, 1e-3) * unit, stroke_width=0, fill_color=CASH, fill_opacity=0.8)
    bar = VGroup(c, o).arrange(DOWN, buff=0)
    if cash <= 0:
        c.set_opacity(0)
    ol = MathTex(rf"{ops:.0f}", font_size=24).move_to(o)
    cl = MathTex(rf"{cash:.0f}", font_size=22).move_to(c) if cash > 0 else VMobject()
    tl = label(title, font_size=21, color=GREY_A).next_to(bar, UP, buff=0.15)
    px = MathTex(rf"{shares:.0f}\ \text{{shares}} \times {(ops + cash) / shares:.0f}", font_size=26,
                 color=PRICE).next_to(bar, DOWN, buff=0.15)
    return VGroup(bar, ol, cl, tl, px)


class Payout(VoiceoverScene):
    def construct(self):
        s = load("shiller")
        self.card()
        self.irrelevance()
        self.yield_(s)
        self.merton()

    def card(self):
        c = chapter_card(6, r"Dividends, buybacks, and equity as an option", r"Does it matter how cash comes back?",
                         part=PART)
        with self.voiceover("Chapter six. Dividends, buybacks, and equity as an option."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def irrelevance(self):
        a = stack(900, 100, 100, r"before: operations 900, cash 100")
        b = stack(900, 0, 100, r"a dividend of 1 a share")
        c = stack(900, 0, 90, r"a buyback of 10 shares at 10")
        VGroup(a, b, c).arrange(RIGHT, buff=2.4, aligned_edge=DOWN).to_edge(UP, buff=0.7)
        bnote = wrapped_label(r"price 9, plus 1 in each owner's pocket: still 10", 3.2, 21, CASH).next_to(b, DOWN,
                                                                                                    buff=0.15)
        cnote = wrapped_label(r"price 10; the sellers got 10 in cash", 3.2, 21, CASH).next_to(c, DOWN, buff=0.15)
        b[4].become(MathTex(r"100\ \text{shares} \times 9", font_size=26, color=PRICE).move_to(b[4]))
        eps = VGroup(
            MathTex(r"\text{EPS: } \frac{90 + 2}{100} = 0.92 \;\to\; \frac{90}{90} = 1.00", font_size=32),
            label(r"earnings per share rise 9\%; the price does not move: the P/E falls from 10.9 to 10", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        foot = note(r"operations earn 90 a year; the cash earned 2\%", font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In 1961 Miller and Modigliani turned the same argument on payout. A firm owns operations worth nine "
            "hundred and a hundred in cash, and has a hundred shares, worth ten each. <bookmark mark='a'/> It pays "
            "a dividend of one a share. The cash leaves the firm, the shares fall to nine, and each owner holds nine "
            "in stock and one in cash: still ten. <bookmark mark='b'/> Or it buys back ten shares at ten. The "
            "sellers have their cash, the ninety remaining shares share the nine hundred of operations: still ten "
            "each. In a world without taxes and frictions, how cash comes back does not change what owners have. "
            "<bookmark mark='c'/> But watch the number that headlines report. The operations earn ninety a year "
            "and the cash earned two. Earnings per share were ninety-two cents, and after the buyback they are a "
            "dollar: nine percent higher, with the price unchanged. Earnings per share can be bought; value cannot."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("a")
            self.play(FadeIn(b), FadeIn(bnote))
            vo.wait_until("b")
            self.play(FadeIn(c), FadeIn(cnote))
            vo.wait_until("c")
            self.play(FadeIn(eps[0]), FadeIn(foot))
            self.play(FadeIn(eps[1]))
        self.wait(0.4)
        self.clear_scene()

    def yield_(self, s):
        t, dy = np.asarray(s["t"]), np.asarray(s["dy"])
        g = axes([1871, 2021], [0, 0.1], x_length=9.0, y_length=4.4, ylabel=r"S\&P dividend yield",
                 xticks=[1880, 1920, 1960, 2000], xfmt=lambda x: f"{int(x)}", yticks=[0, 0.02, 0.04, 0.06, 0.08, 0.10],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, dy, CASH, stroke_width=3)
        v82 = DashedLine(ax.c2p(1982.9, 0), ax.c2p(1982.9, 0.1), color=QC.HOUSE, stroke_width=2)
        v82l = label(r"Rule 10b-18, 1982", font_size=20, color=QC.HOUSE).next_to(ax.c2p(1982.9, 0.1), UP, buff=0.05)
        pre, post = dy[t < 1983].mean(), dy[t >= 1983].mean()
        side = VGroup(
            MathTex(rf"\text{{1871--1982: }}{100 * pre:.1f}\%", font_size=30, color=CASH),
            MathTex(rf"\text{{1983--2020: }}{100 * post:.1f}\%", font_size=30, color=CASH),
            wrapped_label(r"the same cash now comes back partly as buybacks, which a dividend yield does not count; "
                          r"a dividend-based valuation has to add them back", 3.6, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Shiller's data: next year's dividends over January's price")
        with self.voiceover(
            "Real-world payout did change. For a century, American firms paid out about five percent of their "
            "value each year in dividends. <bookmark mark='a'/> In November 1982 the SEC adopted Rule 10b-18, a "
            "safe harbour that protected companies buying back their own shares from charges of manipulating the "
            "price. Buybacks grew to rival dividends, and the dividend yield fell, to about one percent in 2000 and "
            "under two in 2020. <bookmark mark='b'/> That matters to anyone who reads valuation off dividends: a "
            "dividend yield that ignores buybacks makes the market look more expensive than it is, and a forecasting "
            "model fitted to dividends breaks in 1982."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(v82), FadeIn(v82l))
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def merton(self):
        A = np.linspace(1, 200, 200)
        m = valuation.merton_equity(A, F_, T_, SA, R_)
        g = axes([0, 200], [0, 200], x_length=6.0, y_length=4.8, xlabel=r"value of the firm's assets $A$",
                 ylabel=r"value of the claim", xticks=[0, 80, 200], yticks=[0, 80, 200], font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        pay = curve(ax, [0, F_, 200], [0, 0, 200 - F_], GREY_B, stroke_width=2.5)
        eq = curve(ax, A, m["equity"], EQUITY, stroke_width=4)
        dpay = curve(ax, [0, F_, 200], [0, F_, F_], GREY_C, stroke_width=2)
        dv = curve(ax, A, m["debt"], DEBT, stroke_width=3.5)
        leg = legend([(GREY_B, r"equity at the debt's maturity: $\max(A - F, 0)$"),
                      (EQUITY, r"equity now: a call on the assets"),
                      (DEBT, r"debt now: riskless debt minus a put")], font_size=21)
        rows = VGroup(
            cmath(r"E", r"=", r"C(A, F, T, \sigma_A)", font_size=36, colors={r"E": EQUITY}),
            cmath(r"D", r"=", r"F e^{-rT} - P(A, F, T, \sigma_A)", font_size=36, colors={r"D": DEBT}),
            label(rf"debt of {F_:.0f} due in {T_:.0f} years; asset volatility {100 * SA:.0f}\%", font_size=19,
                  color=GREY_B),
            wrapped_label(r"so owners gain when the firm takes more risk: the call is worth more, the debt less "
                          r"(asset substitution).  A project's option to wait or expand is a call too: a real option.",
                          5.4, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(leg, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "One more way to see a share. A firm has assets worth A and owes F, due in five years. When the debt "
            "comes due, the owners pay it if the assets are worth more, and keep the rest; if not, they hand the "
            "firm to the lenders and walk away, because their liability is limited. <bookmark mark='a'/> That "
            "payoff, the maximum of A minus F and zero, is a call option on the firm's assets, struck at the debt. "
            "Before maturity, equity is worth what a call is worth: Black and Scholes noticed this in 1973, and "
            "Robert Merton built a theory of corporate debt on it in 1974. <bookmark mark='b'/> And the debt is "
            "riskless debt minus a put: the lenders have sold the owners the right to default. "
            "<bookmark mark='c'/> It explains a conflict: a call is worth more when volatility rises, so owners of a "
            "struggling firm gain from risky bets that hurt the lenders. And it explains real options: a project "
            "that can be delayed or expanded is worth more than its NPV. Part ten prices the call, and Part twenty "
            "turns this into a model of default."
        ) as vo:
            self.play(FadeIn(g), Create(pay), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(eq), FadeIn(leg[1]), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(dpay), Create(dv), FadeIn(leg[2]), FadeIn(rows[1]), FadeIn(rows[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
