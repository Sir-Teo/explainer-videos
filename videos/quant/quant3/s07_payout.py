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
        p = load("payout")
        self.proof()
        self.irrelevance()
        self.two_firms(p)
        self.yield_(s)
        self.issuance(p)

    def card(self):
        c = chapter_card(11, r"Payout: dividends, buybacks and issuance", r"Does it matter how cash comes back?",
                         part=PART)
        with self.voiceover("Chapter eleven. Payout: dividends, buybacks and issuance."):
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
            "In numbers. A firm owns operations worth nine "
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

    def proof(self):
        rows = [
            cmath(r"V_t", r"=", r"\frac{1}{1 + r}\Big[n_t D_{t+1} + n_{t+1} P_{t+1} - m_{t+1} P_{t+1}\Big]",
                  font_size=38, colors={r"V_t": VALUE}),
            cmath(r"n_t D_{t+1}", r"=", r"X_{t+1} - I_{t+1} + m_{t+1} P_{t+1}", font_size=38,
                  colors={r"n_t D_{t+1}": CASH}),
            cmath(r"V_t", r"=", r"\frac{X_{t+1} - I_{t+1} + V_{t+1}}{1 + r}", font_size=40, colors={r"V_t": VALUE}),
        ]
        whys = [why(r"today's owners get the dividend and the shares' value, less what the $m$ new shares are sold for"),
                why(r"the firm's cash: what it pays out is earnings $X$ less investment $I$, plus what it raises"),
                why(r"substitute: the dividend and the new shares cancel; value depends on investment, not on payout")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.8, buff=0.85, edge=6.9)
        with self.voiceover(
            "In 1961 Miller and Modigliani turned their argument on payout. The firm's value today is what its "
            "current owners will receive next period: the dividend on their shares, plus what their shares are worth, "
            "which is the whole firm's value less whatever new shares were sold to outsiders. "
            "<bookmark mark='a'/> But the dividend must be financed: by earnings, less investment, plus any new shares "
            "sold. <bookmark mark='b'/> Substitute, and the dividend cancels. Value depends on earnings and "
            "investment, the real decisions, and not at all on how the cash is returned. Pay a bigger dividend and "
            "you must sell more shares to invest the same amount; the owners end up exactly where they were."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def two_firms(self, p):
        tf = p["two_firms"]
        Wd, Wb = np.asarray(tf["div"]["wealth"]), np.asarray(tf["buy"]["wealth"])
        Ed, Eb = np.asarray(tf["div"]["eps"]), np.asarray(tf["buy"]["eps"])
        n = len(Wd)
        k = ValueTracker(0)
        unit = 0.17

        def draw():
            i = int(np.clip(round(k.get_value()), 0, n - 1))
            out = VGroup()
            for x, W, E, name, col in ((-4.2, Wd, Ed, r"pays dividends", CASH), (-1.6, Wb, Eb, r"buys back", PRICE)):
                bar = Rectangle(width=1.4, height=W[i] * unit, stroke_width=0, fill_color=QC.HOUSE, fill_opacity=0.85)
                bar.move_to([x, -2.6, 0], aligned_edge=DOWN)
                out.add(bar, MathTex(rf"{W[i]:.2f}", font_size=28, color=QC.HOUSE).next_to(bar, UP, buff=0.1),
                        label(name, font_size=22, color=col).move_to([x, -3.0, 0]),
                        MathTex(rf"\text{{EPS}}\ {E[i]:.2f}", font_size=26, color=col).move_to([x, 2.6, 0]))
            out.add(label(rf"year {i + 1}", font_size=26, color=GREY_B).move_to([-2.9, 3.3, 0]))
            return out

        dr = always_redraw(draw)
        side = VGroup(
            label(r"two identical firms: operations worth 1{,}000 earn 100 a year, all paid out", font_size=21,
                  color=GREY_A),
            label(r"one pays it as dividends (reinvested by the owner at the same 10\%);", font_size=21, color=CASH),
            label(r"the other buys back its shares", font_size=21, color=PRICE),
            label(r"gold: the wealth of an owner who started with one share", font_size=21, color=QC.HOUSE),
            wrapped_label(r"the buyback firm's EPS and price grow 10\% a year; the dividend payer's stay flat; "
                          r"the owners are equally rich", 5.4, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Run it. Two identical firms earn a hundred a year on operations worth a thousand and return all of it. "
            "One pays dividends; its owner reinvests them at the same ten percent. The other buys back its own "
            "shares. <bookmark mark='a'/> Watch the headline numbers diverge. The buyback firm's earnings per share "
            "and its share price climb ten percent a year, because the same earnings are spread over fewer shares. "
            "The dividend payer's stay flat. <bookmark mark='b'/> Now the gold bars, what an owner who started with "
            f"one share is worth. They rise together, to {Wd[-1]:.2f} and {Wb[-1]:.2f} after ten years. A rising "
            "EPS line is not, by itself, a reason to pay more."
        ) as vo:
            self.play(FadeIn(side[:3]))
            self.add(dr)
            vo.wait_until("a")
            self.play(k.animate.set_value(n - 1), run_time=8, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[3:]))
        dr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def issuance(self, p):
        ann = p["ni_annual"]
        cols = ["< 0", "ZERO", "Lo 10", "Dec 2", "Dec 3", "Dec 4", "Dec 5", "Dec 6", "Dec 7", "Dec 8", "Dec 9",
                "Hi 10"]
        names = [r"buy back", r"none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        g = axes([0, len(cols)], [0, 0.16], x_length=7.4, y_length=4.2, ylabel=r"average return a year, 1963--2020",
                 xticks=[], yticks=[0, 0.05, 0.10, 0.15], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bw = ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for i, c in enumerate(cols):
            v = ann[c]
            col = QC.GAIN if c == "< 0" else (QC.LOSS if c == "Hi 10" else GREY_B)
            r_ = Rectangle(width=bw, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                           fill_opacity=0.85).move_to(ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars.add(VGroup(r_, label(names[i], font_size=15, color=GREY_B).next_to(r_, DOWN, buff=0.08)))
        xl = label(r"net issuance over the past year: repurchasers, none, then deciles of issuers", font_size=18,
                   color=GREY_A).next_to(g, DOWN, buff=0.45)
        o = p["osap"]
        side = VGroup(
            MathTex(rf"\text{{repurchasers}}\ {100 * ann['< 0']:.1f}\%\ \text{{vs top issuers}}\ {100 * ann['Hi 10']:.1f}\%",
                    font_size=28),
            label(r"long-short portfolios, \% a month, in the original sample $\to$ after publication:", font_size=19,
                  color=GREY_A),
            MathTex(rf"\text{{net payout yield}}\ {o['NetPayoutYield']['in']:.2f} \to {o['NetPayoutYield']['post']:.2f}",
                    font_size=28, color=CASH),
            label(rf"Boudoukh et al.\ ({o['NetPayoutYield']['year']})", font_size=17, color=GREY_B),
            MathTex(rf"\text{{share issuance}}\ {o['ShareIss1Y']['in']:.2f} \to {o['ShareIss1Y']['post']:.2f}",
                    font_size=28, color=QC.LOSS),
            label(rf"Pontiff and Woodgate ({o['ShareIss1Y']['year']})", font_size=17, color=GREY_B),
            wrapped_label(r"payout does not create value; but the decision to issue or buy back carries managers' "
                          r"information about price (Ikenberry, Lakonishok and Vermaelen 1995)", 4.8, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's net-issuance sorts (value-weighted); Chen--Zimmermann long-shorts")
        with self.voiceover(
            "Irrelevance is a statement about mechanics. In the data, the choice to issue or to buy back still says "
            "something. Kenneth French sorts stocks every year on how many shares they issued. "
            f"<bookmark mark='a'/> Since 1963 the firms that bought back shares returned {100 * ann['< 0']:.1f} percent "
            f"a year; the tenth that issued the most returned {100 * ann['Hi 10']:.1f}. <bookmark mark='b'/> The "
            "published long-short versions, from Boudoukh and coauthors' net payout yield and Pontiff and Woodgate's "
            "share issuance, earned these returns a month in their papers' samples and these after publication. "
            "Managers seem to sell shares when they think them dear and buy when they think them cheap. The payout "
            "does not create value; the information in the decision does."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(xl))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(b[1]) for b in bars], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side[1:]], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()
