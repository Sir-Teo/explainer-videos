from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
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
            f"""Chapter five. These are different descriptive questions. In the selected market's worst five-percent days, other-finance returns average a {100 * abs(f['Fin']['mes']):.1f}-percent loss and insurers a {100 * abs(f['Insur']['mes']):.1f}-percent loss. Fitted delta CoVaR instead compares the system quantile at an industry's tail and median state, and gives a different ranking. Exposure and conditional association are distinct; neither industry regression identifies a causal contribution to a crisis."""
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
                why("the fitted conditional-quantile change between the institution's median and tail state; not a causal contribution")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "CoVaR, after Adrian and Brunnermeier. <bookmark mark='a'/> In a correctly specified continuous conditional model, it is the system-return quantile at a chosen institution-return state. Conditioning on an exact return is defined through that conditional distribution, not by selecting observations equal to one number. <bookmark mark='b'/> Here a linear quantile regression is approximated by finite iteratively reweighted least squares. Specification and numerical error remain. <bookmark mark='c'/> Delta CoVaR is the fitted difference between institution tail and median states. It is a conditional association, not an identified causal effect."
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
            f"""Retrospective daily data from nineteen ninety to twenty twenty, with industry portfolios standing in for firms. <bookmark mark='a'/> The fitted market five-percent quantile difference is {100 * s['full']['Banks']['dcovar']:.2f} percentage points for banks, {100 * s['full']['Insur']['dcovar']:.2f} for insurers and {100 * s['full']['Fin']['dcovar']:.2f} for other finance. <bookmark mark='b'/> MES instead averages each industry's return on the market's worst days. These rankings differ because the conditioning questions differ. The estimates have sampling and specification uncertainty and are not causal effects of putting an institution into distress."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(VGroup(tab[1][0], tab[1][1], tab[1][2])), FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(VGroup(tab[1][0], tab[1][1], tab[1][2]), color=HURDLE), LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[2:]], lag_ratio=0.3))
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
            dc = 100 * np.asarray(s["series"][k]["dcovar"], float)
            lines.add(curve(ax, yrs, dc, cols[k], stroke_width=3))
        leg = legend([(cols[k], NM[k]) for k in ("Banks", "Insur", "Fin")], font_size=18).to_corner(DR, buff=0.6)
        worst = min(min(s["series"][k]["dcovar"]) for k in ("Banks", "Insur", "Fin"))
        with self.voiceover(
            "Over time, in two-year windows. <bookmark mark='a'/> All three are quiet in calm years and plunge together "
            f"in the crises: the deepest reading, {100 * worst:.1f} percent, comes in the window around twenty oh eight. "
            "<bookmark mark='b'/> A systemic measure built from market prices sees the crisis as it arrives, which makes "
            "it a thermometer more than a forecast."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lines))
            vo.wait_until("a")
            self.play(Indicate(lines, color=HURDLE), run_time=1.2)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def mes_def(self):
        rows = [cmath(r"\text{MES}_i", r"=", r"\mathbb E\bigl[r_i \mid r_{sys} \le \text{VaR}_{5\%}(r_{sys})\bigr]", font_size=38,
                      colors={r"\text{MES}_i": FUND_C}),
                cmath(r"\text{LRMES}", r"\approx", r"1 - e^{-18\,m},\quad m=-\text{MES}_{\rm return}>0", font_size=42),
                cmath(r"m = 3\%", r"\Rightarrow", r"\text{LRMES} \approx 42\%", font_size=40)]
        whys = [why(r"Acharya, Pedersen, Philippon and Richardson (2017): an institution's average return on the system's "
                    r"worst days, Part 40's Euler contribution to ES"),
                why('a heuristic six-month loss mapping commonly motivated by 2\\%-tail daily MES; this chapter instead inserts its 5\\%-tail industry proxy'),
                why('chosen positive loss input $m=3\\%$ gives $1-e^{-18m}\\approx42\\%$; this is a model mapping, not a validated firm forecast')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Exposure is a different question. <bookmark mark='a'/> This chapter defines MES as average institution return on the market's worst five percent of days, usually a negative number. Its connection to a portfolio ES contribution needs suitable linear-loss and smooth-tail conditions. <bookmark mark='b'/> For the long-run heuristic, switch signs to a positive loss m, then use one minus exp of minus eighteen m. The customary motivation uses a two-percent daily tail; our unchanged illustration feeds it a five-percent industry proxy. <bookmark mark='c'/> A chosen three-percent positive loss maps to roughly forty-two percent. It does not validate a firm-specific six-month crisis forecast."
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
                why('a chosen 8\\% prudential ratio for this illustration, not a universal current regulatory requirement'),
                why('system shortfall aggregates positive parts; one firm surplus does not automatically recapitalize another')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "SRISK, after Brownlees and Engle. <bookmark mark='a'/> For debt D, market equity E and a crisis loss fraction L, shortfall is k D minus one minus k times one minus L times E. The one-minus-k factor is essential. <bookmark mark='b'/> We choose k equal to eight percent; that is a modeling parameter here, not a certification of current capital requirements. <bookmark mark='c'/> For aggregate capital need, sum positive shortfalls rather than netting surpluses across firms. The debt, equity and crisis-loss inputs must match the intended model."
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
                why('heuristic loss from a 5\\%-tail industry proxy; not a fitted Lehman return model'),
                why('illustrative proxy: book equity replaces market capitalization, so this is not a standard firm-specific SRISK estimate')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""An explicitly approximate Lehman illustration. <bookmark mark='a'/> Its reported fiscal year-end balance sheet has six hundred ninety-one billion dollars of assets and twenty-two point five billion of book equity. <bookmark mark='b'/> We use other-finance industry returns on the market's worst five percent of two thousand seven days, a positive loss input of {100 * r['mes']:.1f} percent. <bookmark mark='c'/> The heuristic maps this to {100 * r['lrmes']:.0f} percent. <bookmark mark='d'/> Inserting it and book equity gives {r['srisk']:.0f} billion dollars. Because both industry MES and book equity replace firm-specific market inputs, this is not standard estimated Lehman SRISK or a validated advance capital forecast."""
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
            desk_question(r"the regulators' list", 'since 2011 the Financial Stability Board names global systemically important banks each year, from five indicator categories: size, interconnectedness, substitutability, complexity and cross-border activity', width=12.4, font_size=19),
            desk_question(r"and charges them", r"each bucket adds a capital surcharge of 1 to 3.5 percentage points; "
                          r"stress tests and resolution plans come with it", width=12.4, font_size=19),
            desk_question(r"published market measures", r"SRISK estimates for listed firms are published and updated, "
                          r"as by NYU's Volatility Laboratory: a public check on the official list", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In the historical policy framework. <bookmark mark='a'/> Since twenty eleven the Financial Stability Board has published an annual list of global systemically important banks using five indicator categories: size, interconnectedness, substitutability, complexity and cross-border activity. These are categories containing multiple indicators, not just five measured variables. <bookmark mark='b'/> The Basel bucket framework specifies additional capital surcharges, including levels from one to three and a half percentage points; implementation and occupied buckets are separate questions. <bookmark mark='c'/> Published market measures such as SRISK offer another perspective for listed firms, under their own model and data assumptions."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question('timing must be evaluated', 'these retrospective windows describe realized stress; predictive content requires a separate past-measurable out-of-sample design', width=12.4, font_size=19),
            desk_question(r"correlation, not cause", r"a high $\Delta$CoVaR can mean a firm spreads distress or only "
                          r"shares exposures with the system", width=12.4, font_size=19),
            desk_question(r"the measured are listed", 'many funds have prices, but valuations, coverage and bilateral exposures can be incomplete or delayed, especially outside listed banks', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Limits of these measurements. <bookmark mark='a'/> Our full-sample and two-year windows describe realized stress. Establishing advance predictive information would require a separate past-measurable out-of-sample design; market prices are not inherently devoid of forward-looking information. <bookmark mark='b'/> A high delta CoVaR may reflect transmission or shared exposures; this regression alone cannot separate them. <bookmark mark='c'/> Many funds have observable prices, but coverage, valuation frequency and financing exposures differ. Missing bilateral data and delayed marks remain substantial limits."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('in early 1998 a hedge fund held about \\$125bn of assets on \\$4.7bn of capital, mostly in trades betting that spreads would narrow. Under a fixed-debt, uniform asset-value-loss approximation, what percentage fall exhausts equity? A spread-basis-point answer additionally needs sensitivities.')
        with self.voiceover(
            "Pause and predict. In early nineteen ninety-eight a hedge fund held about a hundred and twenty-five billion "
            "dollars of assets on four point seven billion of capital, mostly in trades betting that spreads would narrow. "
            "What move would have wiped it out, and who would have had to sell?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
