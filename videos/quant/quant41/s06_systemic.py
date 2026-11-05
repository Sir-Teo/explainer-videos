from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, NET_C, PART, PRICE_C, SPIRAL_C, load)

NM = {"Banks": r"banks", "Insur": r"insurers", "Fin": r"other finance"}


class Systemic(VoiceoverScene):
    def construct(self):
        s = load("systemic")
        self.card(s)
        self.covar_def()
        self.table(s)
        self.over_time(s)
        self.mes_def()
        self.srisk_def()
        self.lehman(s)
        self.gsib()
        self.limits()
        self.question()

    def card(self, s):
        f = s["full"]
        c = chapter_card(5, r"Measuring systemic risk", r"Which institutions matter most when everything falls?", part=PART)
        with self.voiceover(
            "Chapter five, and the answer to the pause: they are different questions. On the market's worst days, other "
            f"finance falls most, {100 * abs(f['Fin']['mes']):.1f} percent on average, and insurers least, "
            f"{100 * abs(f['Insur']['mes']):.1f}. But when insurers themselves are in distress, the market's own worst "
            "case worsens more than when banks are. Exposure to a crisis and contribution to one need two measures."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def covar_def(self):
        rows = [cmath(r"P\bigl(r_{sys} \le \text{CoVaR}_q \mid r_i = \text{VaR}_q(r_i)\bigr)", r"=", r"q", font_size=34,
                      colors={r"q": HURDLE}),
                cmath(r"Q_q(r_{sys} \mid r_i)", r"=", r"\alpha + \beta\,r_i", font_size=40),
                cmath(r"\Delta\text{CoVaR}_i", r"=", r"\beta\,\bigl(\text{VaR}_q(r_i) - \text{median}(r_i)\bigr)", font_size=36,
                      colors={r"\Delta\text{CoVaR}_i": SPIRAL_C})]
        whys = [why(r"Adrian and Brunnermeier (2016): the system's value at risk, given that an institution is in its own "
                    r"distress"),
                why(r"estimated by a quantile regression of the system's return on the institution's (Part 40's pinball "
                    r"loss)"),
                why(r"the change from the institution's normal state to its distressed one: its contribution to the "
                    r"system's tail")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Tobias Adrian and Markus Brunnermeier's CoVaR. <bookmark mark='a'/> The system's value at risk, given that an "
            "institution is in its own distress. <bookmark mark='b'/> It comes from a quantile regression of the system's "
            "return on the institution's, the pinball loss of Part forty. <bookmark mark='c'/> And delta CoVaR is the "
            "change from the institution's normal state to its distressed one: how much worse the system's tail gets when "
            "this institution is in trouble."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, s):
        hx = [-3.6, -0.8, 1.8, 4.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"industry, daily 1990--2020", r"$\beta$ at 5\%",
                                                                         r"$\Delta$CoVaR", r"MES")])
        tab = VGroup(head)
        for k in ("Banks", "Insur", "Fin"):
            x = s["full"][k]
            tab.add(VGroup(label(NM[k], font_size=20), MathTex(f"{x['beta']:.2f}", font_size=28),
                           MathTex(rf"{100 * x['dcovar']:.2f}\%", font_size=28, color=SPIRAL_C),
                           MathTex(rf"{100 * x['mes']:.2f}\%", font_size=28, color=FUND_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.9 * j, 0])
        foot = wrapped_label(r"the system is the US market; the institutions are Kenneth French's value-weighted industry "
                             r"portfolios, a stand-in for the individual firms the measures were built for", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "On thirty years of American data, with industries standing in for firms. <bookmark mark='a'/> Delta CoVaR: "
            f"distress in banks moves the market's five percent quantile by {100 * s['full']['Banks']['dcovar']:.2f} "
            f"percent, insurers {100 * s['full']['Insur']['dcovar']:.2f}, other finance "
            f"{100 * s['full']['Fin']['dcovar']:.2f}. <bookmark mark='b'/> And marginal expected shortfall, how much each "
            "falls on the market's worst days, ranks them differently: insurers fall least, yet their distress moves the "
            "market's tail more than banks' distress does."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def over_time(self, s):
        g = axes([1990, 2020], [-5, 0], x_length=7.6, y_length=4.2, xlabel=r"two-year windows",
                 ylabel=r"$\Delta$CoVaR, \%", xticks=[1990, 2000, 2008, 2020], yticks=[-4, -2, 0], font_size=16)
        g.move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        cols = {"Banks": LEV_C, "Insur": NET_C, "Fin": SPIRAL_C}
        lines = VGroup()
        for k in ("Banks", "Insur", "Fin"):
            yrs = np.asarray(s["series"][k]["year"], float)
            dc = np.clip(100 * np.asarray(s["series"][k]["dcovar"], float), -5, 0)
            lines.add(curve(ax, yrs, dc, cols[k], stroke_width=3))
        leg = legend([(cols[k], NM[k]) for k in ("Banks", "Insur", "Fin")], font_size=18).to_corner(DR, buff=0.6)
        worst = min(min(s["series"][k]["dcovar"]) for k in ("Banks", "Insur", "Fin"))
        with self.voiceover(
            "Over time, in two-year windows. <bookmark mark='a'/> All three are quiet in calm years and plunge together "
            f"in the crises: the deepest reading, {100 * worst:.1f} percent, comes in the window around twenty oh eight. "
            "<bookmark mark='b'/> A systemic measure built from market prices sees the crisis as it arrives, which makes "
            "it a thermometer more than a forecast."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def mes_def(self):
        rows = [cmath(r"\text{MES}_i", r"=", r"\mathbb E\bigl[r_i \mid r_{sys} \le \text{VaR}_{5\%}(r_{sys})\bigr]", font_size=38,
                      colors={r"\text{MES}_i": FUND_C}),
                cmath(r"\text{LRMES}", r"\approx", r"1 - e^{-18\,\text{MES}}", font_size=42),
                cmath(r"\text{MES} = 3\%", r"\Rightarrow", r"\text{LRMES} \approx 42\%", font_size=40)]
        whys = [why(r"Acharya, Pedersen, Philippon and Richardson (2017): an institution's average return on the system's "
                    r"worst days, Part 40's Euler contribution to ES"),
                why(r"the long-run version: its expected loss over six months in a 40\% market crash, by Acharya, Engle and "
                    r"Richardson's approximation"),
                why(r"a firm that loses 3\% on the market's bad days would lose about two-fifths in a crisis")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The other side: exposure. <bookmark mark='a'/> Marginal expected shortfall is an institution's average return "
            "on the system's worst days, Part forty's Euler contribution. <bookmark mark='b'/> Its long-run version "
            "approximates the loss over six months in a forty percent crash, one minus e to the minus eighteen MES. "
            "<bookmark mark='c'/> A firm that loses three percent on the market's bad days loses about two-fifths in a "
            "crisis."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def srisk_def(self):
        rows = [cmath(r"\text{SRISK}", r"=", r"k\,D - (1 - k)(1 - \text{LRMES})\,E", font_size=42, colors={r"\text{SRISK}": SPIRAL_C}),
                cmath(r"k", r"=", r"8\%", font_size=44),
                cmath(r"\text{SRISK} > 0", r":", r"\text{capital it would need, in a crisis}", font_size=38)]
        whys = [why(r"Brownlees and Engle (2017): the capital a firm would be short after a crisis, given its debt $D$, "
                    r"its market equity $E$ and its long-run MES"),
                why(r"the prudential capital ratio assumed: equity of at least 8\% of assets"),
                why(r"summed over firms, the capital the system would need when it can least raise it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Christian Brownlees and Robert Engle turned it into a capital number. <bookmark mark='a'/> SRISK is the "
            "capital a firm would be short after a crisis: eight percent of its debt, minus what its equity would be "
            "worth after the crisis. <bookmark mark='b'/> With an eight percent prudential ratio. <bookmark mark='c'/> "
            "Summed over firms, it is the capital the system would need at the moment it can least raise it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def lehman(self, s):
        r = s["srisk"]
        rows = [cmath(r"\text{assets, equity}", r":", r"\$691\text{bn},\ \$22.5\text{bn}\ (\text{30.7}\times)", font_size=36,
                      colors={r"\text{assets, equity}": LEV_C}),
                cmath(r"\text{MES, 2007}", r"=", rf"{100 * r['mes']:.2f}\%", font_size=40, colors={r"\text{MES, 2007}": FUND_C}),
                cmath(r"\text{LRMES}", r"=", rf"{100 * r['lrmes']:.0f}\%", font_size=40),
                cmath(r"\text{SRISK}", r"=", rf"0.08 \times {r['debt']:.0f} - 0.92 \times {1 - r['lrmes']:.2f} \times 22.5 = "
                      rf"\${r['srisk']:.0f}\text{{bn}}", font_size=32, colors={r"\text{SRISK}": SPIRAL_C})]
        whys = [why(r"Lehman Brothers at its fiscal year-end, 30 November 2007, as reported in its annual report"),
                why(r"other financial stocks' average return on the US market's worst 5\% of days in 2007, a stand-in for "
                    r"Lehman's own"),
                why(r"its implied loss in a crisis: about half its market value"),
                why(r"so ten months before it failed, by this measure, it would have needed about twice its equity in new "
                    r"capital")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Lehman Brothers, at the end of twenty oh seven. <bookmark mark='a'/> Six hundred and ninety-one billion "
            "dollars of assets on twenty-two and a half of equity, as reported: thirty-one times. <bookmark mark='b'/> "
            f"Financial stocks' MES that year, as a stand-in: {100 * r['mes']:.1f} percent. <bookmark mark='c'/> An implied "
            f"crisis loss of {100 * r['lrmes']:.0f} percent. <bookmark mark='d'/> And an SRISK of about "
            f"{r['srisk']:.0f} billion dollars: ten months before it failed, a capital shortfall of about twice its "
            "equity."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def gsib(self):
        cards = VGroup(
            desk_question(r"the regulators' list", r"since 2011 the Financial Stability Board names global systemically "
                          r"important banks each year, from five indicators: size, interconnectedness, substitutability, "
                          r"complexity and cross-border activity", width=12.4, font_size=19),
            desk_question(r"and charges them", r"each bucket adds a capital surcharge of 1 to 3.5 percentage points; "
                          r"stress tests and resolution plans come with it", width=12.4, font_size=19),
            desk_question(r"published market measures", r"SRISK estimates for listed firms are published and updated, "
                          r"as by NYU's Volatility Laboratory: a public check on the official list", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In policy. <bookmark mark='a'/> Since twenty eleven the Financial Stability Board names the global "
            "systemically important banks each year, from five indicators: size, interconnectedness, substitutability, "
            "complexity and cross-border activity. <bookmark mark='b'/> Each bucket adds a capital surcharge, from one to "
            "three and a half percentage points. <bookmark mark='c'/> And market measures like SRISK are published for "
            "listed firms, a public check on the official list."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"thermometers, not barometers", r"measures from market prices rise with the crisis, not before "
                          r"it; they say who is exposed, rarely when", width=12.4, font_size=19),
            desk_question(r"correlation, not cause", r"a high $\Delta$CoVaR can mean a firm spreads distress or only "
                          r"shares exposures with the system", width=12.4, font_size=19),
            desk_question(r"the measured are listed", r"funds, shadow banks and private credit have no daily prices: the "
                          r"blind spots of 2020 and 2023", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Their limits. <bookmark mark='a'/> Measures from market prices rise with the crisis, not before it: they say "
            "who is exposed, rarely when. <bookmark mark='b'/> A high delta CoVaR can mean a firm spreads distress, or only "
            "shares exposures with everyone else. <bookmark mark='c'/> And only listed firms are measured: funds, shadow "
            "banks and private credit have no daily prices, which were the blind spots of twenty twenty and twenty "
            "twenty-three."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in early 1998 a hedge fund held about \$125bn of assets on \$4.7bn of capital, mostly in trades "
                       r"betting that spreads would narrow. What spread move would have wiped it out, and who would have "
                       r"had to sell?")
        with self.voiceover(
            "Pause and predict. In early nineteen ninety-eight a hedge fund held about a hundred and twenty-five billion "
            "dollars of assets on four point seven billion of capital, mostly in trades betting that spreads would narrow. "
            "What move would have wiped it out, and who would have had to sell?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
