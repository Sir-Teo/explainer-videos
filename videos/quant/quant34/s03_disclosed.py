from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PLAT_C, PM_C, PNL_C, comma, fit_right, load


class Disclosed(VoiceoverScene):
    def construct(self):
        v = load("virtu")
        self.card()
        self.filing()
        self.implied(v)
        self.tails(v)
        self.lln(v)
        self.trades(v)
        self.compare(v)
        self.revenue()
        self.medallion()
        self.fees()
        self.reading()
        self.question()

    def card(self):
        c = chapter_card(2, r"What the firms have disclosed", r"What can a single number from a filing tell us?",
                         part=PART)
        with self.voiceover("Chapter two. Quant firms are private about their methods, but not silent: listed firms "
                            "file accounts, private ones borrow money and must show lenders their numbers, and books and "
                            "court cases fill in the rest. One number from a filing can say a lot."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def filing(self):
        card = firm_card(r"Virtu Financial, Form S-1 (2014)", r"the registration statement for its listing reported that "
                         r"from January 2009 to December 2013 the firm had a losing trading day once, on one of 1{,}238 "
                         r"trading days, and attributed it to its risk management and its technology",
                         numbers=((r"1 / 1{,}238", r"losing days, as disclosed"),), kind=r"The filing", width=10.6,
                         font_size=22).move_to(UP * 0.4)
        with self.voiceover(
            "The number. <bookmark mark='a'/> In 2014 the market maker Virtu Financial filed to list its shares. Its "
            "registration statement reported that from 2009 to 2013 it had lost money on one trading day out of one "
            "thousand two hundred and thirty-eight, and credited its risk management and technology. The press "
            "treated it as a sensation. What does it actually imply?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def implied(self, v):
        rows = [cmath(r"\Pr(\text{loss})", r"=", r"\Phi(-s) = 1/1238", font_size=38),
                cmath(r"s", r"=", rf"{v['normal']:.2f}\ \text{{a day}}\ \approx\ {v['annual']:.0f}\ \text{{a year}}",
                      font_size=36, colors={r"s": GOOD}),
                cmath(r"\Pr(\text{loss}) \le", rf"{1000 * v['p_upper']:.2f}\times 10^{{-3}}", r"\Rightarrow\ s \ge "
                      rf"{v['normal_lower']:.2f}\ \ (\ge {v['annual_lower']:.0f}\ \text{{a year}})", font_size=32)]
        whys = [why(r"if daily P\&L were normal with mean $\mu$ and volatility $\sigma$, the losing share is "
                    r"$\Phi(-\mu/\sigma)$"),
                why(r"so the daily Sharpe ratio is about 3.2, and with $\sqrt{252}$, about 50 a year: thirty times a good "
                    r"fund's"),
                why(r"one loss is a small sample: the 95\% upper bound on the loss rate still implies more than 40 a year")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Read it as a Sharpe ratio. <bookmark mark='a'/> If daily profit and loss were normal, the share of losing "
            "days would be the normal tail at minus the daily Sharpe ratio. <bookmark mark='b'/> One in twelve hundred "
            f"and thirty-eight gives a daily ratio of {v['normal']:.2f}, about {v['annual']:.0f} a year. "
            "<bookmark mark='c'/> One loss is a small sample, so take the upper confidence bound on the loss rate: it "
            f"still implies more than {v['annual_lower']:.0f} a year. A good fund runs at one or two."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def tails(self, v):
        rows = [cmath(r"t_4", r":", rf"s = {v['t4']:.2f}\ \text{{a day}}", font_size=36),
                cmath(r"t_3", r":", rf"s = {v['t3']:.2f}\ \text{{a day}}", font_size=36),
                cmath(r"\text{fat tails}", r"\Rightarrow", r"\text{a higher } s \text{ for the same loss rate}", font_size=32,
                      colors={r"\text{fat tails}": BAD})]
        whys = [why(r"with Student-$t$ daily P\&L of four degrees of freedom, scaled to the same volatility"),
                why(r"and three: rare days are larger, so a given share of losing days needs a larger mean"),
                why(r"the normal reading is the conservative one; whatever the shape, the daily ratio is above three")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And if the daily profit has fat tails? <bookmark mark='a'/> With a Student-t of four degrees of freedom, "
            f"the same loss rate needs a daily ratio of {v['t4']:.1f}. <bookmark mark='b'/> With three, "
            f"{v['t3']:.1f}. <bookmark mark='c'/> Fat tails make a large deviation more likely, so the same rare loss "
            "needs a larger mean, and the implied ratio rises. The normal reading is the conservative one: whatever the shape, the daily ratio is above "
            "three."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lln(self, v):
        sims = v["sims"]
        xs = np.log10([s["n"] for s in sims])
        ys = [100 * s["lose"] for s in sims]
        g = axes([1.5, 5.5], [0, 50], x_length=7.4, y_length=4.4, xlabel=r"independent trades a day",
                 ylabel=r"losing days, \%", xticks=[2, 3, 4, 5], yticks=[0, 25, 50],
                 xfmt=lambda u: f"10^{{{int(u)}}}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=PNL_C) for a, b in zip(xs, ys)])
        lab = VGroup(*[MathTex(rf"{b:.1f}\%", font_size=22).next_to(d_, UR, buff=0.08) for d_, b in zip(dots, ys)])
        line = curve(ax, xs, ys, PNL_C, stroke_width=2)
        st = wrapped_label(r"each trade earns a hundredth of its own standard deviation: edge/noise $= 0.01$", 3.8, 16,
                           GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "Where such a ratio comes from. <bookmark mark='a'/> Give every trade a tiny edge, a hundredth of its own "
            "standard deviation: a coin that lands heads fifty point four percent of the time. "
            f"<bookmark mark='b'/> With a hundred independent trades a day, {ys[0]:.0f} percent of days lose. With ten "
            f"thousand, {ys[2]:.0f} percent. With a hundred thousand, {ys[3]:.2f} percent, about one day in two thousand. "
            "The firm's daily Sharpe ratio is the trade's ratio times the root of the number of trades. That is the "
            "whole secret of the statistic, and also its limit: it needs a vast number of small, nearly independent bets."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), FadeIn(lab))
        self.wait(0.4)
        self.clear_scene()

    def trades(self, v):
        tr = v["trades"]
        hx = [-2.4, 2.4]
        head = VGroup(label(r"edge/noise per trade", font_size=18, color=GREY_B),
                      label(r"independent trades a day for $s = 3.15$", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for k in ("0.05", "0.02", "0.01", "0.005"):
            tab.add(VGroup(MathTex(k, font_size=28), MathTex(comma(tr[k]), font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(r"$N = (s/r)^2$ for a daily ratio $s$ from $N$ independent trades of ratio $r$; real trades "
                             r"are correlated, which needs more of them", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Turn it around. <bookmark mark='a'/> The number of independent trades a day needed for a daily ratio of "
            "three point one five is that ratio over the per-trade ratio, squared. At five hundredths, about four "
            "thousand trades; at one hundredth, about a hundred thousand. Real trades are correlated, so a firm needs "
            "even more of them. A market maker's edge is not a forecast; it is a factory."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def compare(self, v):
        fl = v["fund_lose"]
        cards = VGroup(
            desk_question(r"a good fund's days", rf"a Sharpe ratio of 2 loses on {100 * fl['2']:.0f}\% of days, and of 3 on "
                          rf"{100 * fl['3']:.0f}\%: from the inside, even an excellent fund feels like a coin toss",
                          width=12.4, font_size=19),
            desk_question(r"why the ratio does not scale", r"market making's capacity is the flow that arrives: doubling "
                          r"capital does not double the trades, so the dollar profit is limited, whatever the ratio",
                          width=12.4, font_size=19),
            desk_question(r"before fixed costs", r"a trading day's P\&L excludes the salaries, data, exchange "
                          r"memberships and technology that must be paid every day, good or bad", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the number does not mean. <bookmark mark='a'/> A fund with a Sharpe ratio of two loses on "
            f"{100 * fl['2']:.0f} percent of its days: from the inside, an excellent fund feels like a coin toss. The "
            "two businesses are not comparable on this statistic. <bookmark mark='b'/> A market maker's capacity is the "
            "flow that arrives; doubling its capital does not double the trades. <bookmark mark='c'/> And a day's "
            "trading profit is before the fixed costs, salaries, data, memberships and machines, that are paid every day."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def revenue(self):
        card = firm_card(r"Jane Street, as reported", r"Bloomberg reported in 2024 that documents prepared for a bond sale "
                         r"showed net trading revenue of about \$10.6 billion for 2023, and later reports put 2024 near "
                         r"\$20 billion; the firm is private and these are the press's readings of offering documents",
                         kind=r"The record", width=10.6, font_size=22).move_to(UP * 0.4)
        with self.voiceover(
            "A private firm's numbers reach the public when it borrows. <bookmark mark='a'/> Bloomberg reported in 2024 "
            "that documents prepared for a Jane Street bond sale showed net trading revenue of about ten point six "
            "billion dollars for 2023, and later reports put 2024 near twenty billion. These are the press's readings of "
            "offering documents, and the firm is private; they show the scale of the business of selling immediacy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def medallion(self):
        card = firm_card(r"Medallion, as reported", r"Gregory Zuckerman's \textit{The Man Who Solved the Market} (2019) "
                         r"reported average annual returns of about 66\% before fees and 39\% after them, 1988--2018; "
                         r"arithmetic averages of yearly returns, on a fund kept small and, since the mid-2000s, open "
                         r"only to the firm's employees",
                         numbers=((r"66\% / 39\%", r"gross / net, as reported"),), kind=r"The record", width=10.6,
                         font_size=22).move_to(UP * 0.4)
        with self.voiceover(
            "And the most famous number. <bookmark mark='a'/> Gregory Zuckerman's book on Renaissance reported that the "
            "Medallion fund averaged about sixty-six percent a year before fees and thirty-nine percent after them, "
            "from 1988 to 2018. Those are arithmetic averages of yearly returns, on a fund that was kept small and, "
            "since the mid-2000s, open only to the firm's own employees: Part thirty-one's capacity, chosen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def fees(self):
        g, mf, pf = 0.66, 0.05, 0.44
        net = g - mf - pf * (g - mf)
        rows = [cmath(r"\text{net}", r"=", r"g - m - p\,(g - m)", font_size=38, colors={r"\text{net}": PNL_C}),
                cmath(r"g = 66\%,\ m = 5\%,\ p = 44\%", r"\Rightarrow", rf"\text{{net}} = {100 * net:.1f}\%", font_size=34),
                cmath(r"\text{reported}", r"=", r"39\%", font_size=36, colors={r"\text{reported}": GOOD})]
        whys = [why(r"a management fee $m$ on assets and a performance fee $p$ on the profit after it"),
                why(r"at the fees reported for Medallion's later years, applied to the reported average"),
                why(r"close to the reported net: the fees were lower in the early years, and averages of yearly returns "
                    r"do not compound exactly")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Check the two numbers against each other. <bookmark mark='a'/> Net return is gross, less the management "
            "fee, less the performance fee on what is left. <bookmark mark='b'/> With the fees reported for later "
            f"years, five percent and forty-four percent, sixty-six percent gross gives {100 * net:.0f} percent net. "
            "<bookmark mark='c'/> The reported thirty-nine is close: the fees were lower in the early years, and "
            "averages of yearly returns do not compound exactly. The two reported numbers are consistent with each other."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"read a disclosed number as a statistic", r"ask what model turns it into a Sharpe ratio, a "
                          r"loss rate or a capacity, and what sample it came from", width=12.4, font_size=19),
            desk_question(r"ask what is excluded", r"fixed costs, fees, the years before the record began, and the "
                          r"funds that closed and stopped reporting (Part 26's survivorship)", width=12.4, font_size=19),
            desk_question(r"separate the firm from the fund", r"the firm's profit includes fees; the investor's return is "
                          r"after them; a firm can prosper on a fund that only matches its benchmark", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How to read the public record. <bookmark mark='a'/> Turn each disclosed number into a statistic, with a "
            "model and a sample. <bookmark mark='b'/> Ask what it excludes: fixed costs, fees, the years before the "
            "record, and the funds that closed. <bookmark mark='c'/> And separate the firm from the fund: the firm's "
            "profit includes its fees, the investor's return is after them."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a firm has 5 losing days in 1{,}250. Under a normal model, what daily and annual Sharpe ratios "
                       r"does that imply?")
        with self.voiceover(
            "Pause and predict. A firm has five losing days in one thousand two hundred and fifty. Under a normal model, "
            "what daily and annual Sharpe ratios does that imply?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
