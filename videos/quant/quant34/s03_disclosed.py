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
        self.add(c)
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
        self.add(card)
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
                why(r"the Gaussian-implied daily ratio is about 3.2; $\sqrt{252}$ annualization also requires iid stable "
                    r"daily variance"),
                why(r"one-sided 95\% binomial bound assumes iid loss indicators; translating it requires the Gaussian model")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Condition on a Gaussian daily profit distribution. <bookmark mark='a'/> Its loss probability is Phi of minus the daily mean-to-standard-deviation ratio. <bookmark mark='b'/> Plugging in the reported frequency gives {v['normal']:.2f}. Multiplication by root two hundred and fifty-two gives about {v['annual']:.0f} only under the daily independence and variance assumptions. <bookmark mark='c'/> The original one-sided binomial upper confidence bound is {v['p_upper']:.4f}; under iid Bernoulli loss indicators and the same Gaussian model it gives a lower daily ratio {v['normal_lower']:.2f}. These are model-conditional calculations from a selected disclosure, not measured investable annual returns."""
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
        rows = [cmath(r"\text{specified location-scale families}", r":", rf"s_N={v['normal']:.2f},\ s_{{t_4}}={v['t4']:.2f},\ s_{{t_3}}={v['t3']:.2f}", font_size=30),
                cmath(r"\Pr(X=-2000)=1/1238", r",", r"\Pr(X=1)=1237/1238", font_size=30),
                cmath(r"\mathbb E[X]", r"=", r"(1237-2000)/1238 < 0", font_size=34)]
        whys = [why(r"these three chosen families give different implied ratios at the same loss probability"),
                why(r"a stipulated two-point counterexample: the same rare-loss probability, very different magnitudes"),
                why(r"loss frequency alone identifies neither the mean nor the mean-to-standard-deviation ratio")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(f"Distributional shape matters. <bookmark mark='a'/> In the specified finite-variance Student-t location-scale families, the same loss probability maps to daily ratios {v['t4']:.2f} and {v['t3']:.2f}. That comparison does not make the Gaussian answer a universal lower bound. <bookmark mark='b'/> Stipulate a payoff of plus one most days, and minus two thousand with probability one over twelve hundred and thirty-eight. <bookmark mark='c'/> Its mean is negative despite the same rare-loss probability. This is a mathematical counterexample, not a description of Virtu's returns. We need loss magnitudes and a distributional model.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
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
        self.add(g, st, dots[0], lab[0])
        with self.voiceover(
            f"""A possible aggregation model, not an inference about the firm. <bookmark mark='a'/> Each independent trade has edge divided by noise point zero one. An even-money coin with that ratio has win probability approximately fifty point five percent; the cached simulation instead uses Normal aggregate profits. <bookmark mark='b'/> In its twenty thousand simulated days, a hundred trades lose on {ys[0]:.0f} percent of days, ten thousand on {ys[2]:.0f} percent, and a hundred thousand on {ys[3]:.2f} percent. These frequencies have Monte Carlo variation. For independent equal-risk trades, the aggregate ratio is the per-trade ratio times root N. A disclosure does not establish those assumptions or reveal the actual firm's strategy."""
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
                             r"with positive net covariance require more for the same ratio; negative covariance can reduce variance", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            "Under the independent equal-risk model, solve N equals the daily ratio over the per-trade ratio, squared. <bookmark mark='a'/> At per-trade ratio point zero five the target needs about four thousand trades; at point zero one, about a hundred thousand. Positive net covariance raises aggregate variance and increases the required count at fixed edge. Negative covariance can lower it. Heterogeneous risk, costs, dependence and capacity can all change the calculation; this table does not estimate actual independent trades at a firm."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def compare(self, v):
        fl = v["fund_lose"]
        cards = VGroup(
            desk_question(r"Gaussian/iid comparison", rf"under Gaussian iid daily returns, annual Sharpe 2 loses on {100 * fl['2']:.0f}\% of days, and of 3 on "
                          rf"{100 * fl['3']:.0f}\%: from the inside, even an excellent fund feels like a coin toss",
                          width=12.4, font_size=26),
            desk_question(r"why the ratio does not scale", r"market making's capacity is the flow that arrives: doubling "
                          r"capital does not double the trades, so the dollar profit is limited, whatever the ratio",
                          width=12.4, font_size=26),
            desk_question(r"before fixed costs", r"a trading day's P\&L excludes the salaries, data, exchange "
                          r"memberships and technology that must be paid every day, good or bad", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            f"""The comparison also needs a model. <bookmark mark='a'/> Under iid Gaussian daily returns with annual Sharpe two, about {100*fl['2']:.0f} percent of days lose. The annual Sharpe alone does not imply that frequency without the distribution and time assumptions. <bookmark mark='b'/> Trading capacity and order flow limit dollar profit; doubling capital need not double opportunities. <bookmark mark='c'/> Definitions of trading profit, operating costs and investor returns differ. Read the filing's accounting scope before comparing a market maker with a fund."""
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
        self.add(card)
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
        self.add(card)
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
                why('a different reported statistic: reconciliation requires annual returns, fee history, fee bases, high-water marks and timing')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Use a stipulated single-period fee example. <bookmark mark='a'/> Charge management fee m on capital, then performance fee p on the remaining positive profit. <bookmark mark='b'/> At gross sixty-six percent, m five percent and p forty-four percent, net is {100*net:.2f} percent. <bookmark mark='c'/> That arithmetic does not reproduce or validate the reported thirty-nine percent historical average. Reconciliation needs year-by-year returns, fees, timing and high-water-mark conventions. With constant affine positive-profit fees, averaging itself commutes with the formula; historical fee changes and nonlinear rules need separate data."""
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
                          r"loss rate or a capacity, and what sample it came from", width=12.4, font_size=26),
            desk_question(r"ask what is excluded", r"fixed costs, fees, the years before the record began, and the "
                          r"funds that closed and stopped reporting (Part 26's survivorship)", width=12.4, font_size=26),
            desk_question(r"separate the firm from the fund", r"the firm's profit includes fees; the investor's return is "
                          r"after them; a firm can prosper on a fund that only matches its benchmark", width=12.4,
                          font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
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
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('\\hat p=5/1250,\\quad s=-\\Phi^{-1}(\\hat p),\\quad S_{\\rm ann}=\\sqrt{252}\\,s', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Gaussian daily location-scale model. Annualization additionally assumes iid stable daily variance; loss counts alone do not identify return magnitudes.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. A firm reports five losing days in twelve hundred and fifty. Under a Gaussian daily model, compute the implied daily mean-to-standard-deviation ratio and its iid annualization. What can the count alone not tell us?'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
