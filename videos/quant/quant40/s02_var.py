from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import (
    BAD,
    DATA_C,
    ES_C,
    GOOD,
    MODEL_C,
    PART,
    TAIL_C,
    VAR_C,
    load,
)


class VaR(VoiceoverScene):
    def construct(self):
        v = load("var3")
        s = load("sqrt")
        self.card()
        self.definition()
        self.picture()
        self.riskmetrics()
        self.three_ways()
        self.table(v["2007"], "the end of 2007")
        self.october(v["2008"])
        self.sqrt_rule(s)
        self.decades(s)
        self.options(load("options"))
        self.what_var_says()
        self.question()

    def card(self):
        c = chapter_card(1, r"Value at risk, three ways", r"What does a single risk number promise, and how is it made?",
                         part=PART)
        with self.voiceover("Chapter one. Since the nineteen nineties, banks have summarised market risk in one number: "
                            "the loss they do not expect to exceed, on a given day, with a given confidence. This chapter "
                            "defines it, estimates it three ways, and shows where the estimates disagree."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        rows = [cmath(r"L", r"=", r"-r", font_size=44),
                cmath(r"\text{VaR}_\alpha", r"=", r"\inf\{\ell : P(L > \ell) \le 1 - \alpha\}", font_size=40,
                      colors={r"\text{VaR}_\alpha": VAR_C}),
                cmath(r"\text{ES}_\alpha", r"=", r"\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u(L)\,du", font_size=40,
                      colors={r"\text{ES}_\alpha": ES_C}),
                cmath(r"\alpha = 99\%", r":", '\\text{continuous model: }1\\%\\text{ exceedance probability}', font_size=38)]
        whys = [why(r"work in losses: a loss is a negative return, so the left tail of returns is the right tail of $L$"),
                why('value at risk: the $\\alpha$-quantile of the loss, a threshold with strict exceedance probability at most $1 - \\alpha$'),
                why('integrated-tail ES; equals a conditional tail mean for a continuous distribution; split the quantile atom otherwise'),
                why('continuous calibrated model: frequency is probabilistic, not a guaranteed count; ES concerns severity')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The definitions. <bookmark mark='a'/> Work in losses, L equals minus the modeled return, or a dollar loss after valuation. <bookmark mark='b'/> VaR is the generalized alpha quantile, with strict exceedance probability at most one minus alpha. Equality needs appropriate continuity. <bookmark mark='c'/> Expected shortfall averages upper-tail quantiles. For continuous losses it equals the tail conditional mean; at an atom one takes only the probability mass needed to complete the tail. <bookmark mark='d'/> Thus a correct continuous ninety-nine percent VaR has one percent exceedance probability, not a guaranteed calendar count."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def picture(self):
        xs = np.linspace(-6, 6, 300)
        nu = 4.0
        pdf = stats.t.pdf(xs, nu)
        g = axes([-6, 6], [0, 0.42], x_length=8.4, y_length=4.0, xlabel='loss, Student-t scale units', ylabel=r"density",
                 xticks=[-4, -2, 0, 2, 4], yticks=[], font_size=16).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, xs, pdf, DATA_C, stroke_width=3)
        v = stats.t.ppf(0.99, nu)
        tx = np.linspace(v, 6, 120)
        tail = band(ax, tx, np.zeros(len(tx)), stats.t.pdf(tx, nu), ES_C, opacity=0.6)  # Axes.get_area breaks on 2D axes
        vl = DashedLine(ax.c2p(v, 0), ax.c2p(v, 0.3), color=VAR_C, stroke_width=3)
        q = stats.t.ppf(0.99, nu)
        es = (nu + q ** 2) / (nu - 1) * stats.t.pdf(q, nu) / 0.01
        el = DashedLine(ax.c2p(es, 0), ax.c2p(es, 0.2), color=ES_C, stroke_width=3)
        lv = label(rf"VaR$_{{99\%}}$ = {v:.2f}", font_size=20, color=VAR_C).next_to(ax.c2p(v, 0.3), UP, buff=0.1)
        le = label(rf"ES$_{{99\%}}$ = {es:.2f}", font_size=20, color=ES_C).next_to(ax.c2p(es, 0.2), UP, buff=0.1)
        with self.voiceover(
            f"A Student t illustration with four degrees of freedom and unit scale; its standard deviation is root two, not one. <bookmark mark='a'/> The ninety-nine percent quantile is {v:.2f}. The axis shows a finite range, so the shading displays only the visible part of an unbounded tail. <bookmark mark='b'/> Expected shortfall of the complete modeled tail is {es:.2f}; it is not the center of mass of just the truncated shaded segment. The location can change with tail shape even when the selected quantile is held fixed."
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(Create(vl), FadeIn(lv))
            vo.wait_until("b")
            self.play(FadeIn(tail), Create(el), FadeIn(le))
        self.wait(0.4)
        self.clear_scene()

    def riskmetrics(self):
        rows = [cmath(r"\sigma_t^2", r"=", r"\lambda\,\sigma_{t-1}^2 + (1 - \lambda)\,r_{t-1}^2,\quad \lambda = 0.94",
                      font_size=36, colors={r"\sigma_t^2": MODEL_C}),
                cmath(r"\text{VaR}_{99\%}", r"=", r"2.33\,\sigma_t \times \text{position}", font_size=38,
                      colors={r"\text{VaR}_{99\%}": VAR_C}),
                cmath('\\text{historical risk reporting}', r":", r"\text{one number, every evening}", font_size=36)]
        whys = [why(r"J.P. Morgan's RiskMetrics (1994, published 1996): an exponentially weighted variance, Part 7's "
                    r"EWMA"),
                why(r"with normal returns, the 99\% quantile is 2.33 standard deviations"),
                why('RiskMetrics launched in 1994; the 1996 technical document describes its methods. Historical Basel model approval had additional conditions.')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "RiskMetrics launched in nineteen ninety-four, with a J.P. Morgan and Reuters technical document in nineteen ninety-six. <bookmark mark='a'/> Its daily EWMA variance illustration uses lambda nought point nine four and yesterday's squared return. <bookmark mark='b'/> With a zero-mean normal return and a compatible linear dollar exposure, ninety-nine percent loss VaR is about two point three three standard deviations times position. <bookmark mark='c'/> A nonzero mean adds a separate location term. The historical Basel market-risk framework allowed eligible internal models under additional approval, testing and capital conditions; this formula alone does not establish compliance."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def three_ways(self):
        cards = VGroup(
            desk_question(r"parametric", r"assume a distribution, normal or Student-t, estimate its parameters, read off "
                          r"the quantile: quick, and wrong in exactly the way the assumption is wrong", width=12.4,
                          font_size=19),
            desk_question(r"historical simulation", "replay the last 500 days' returns on today's position and take the interpolated sample quantile: the empirical distribution is the model, with a chosen finite window", width=12.4,
                          font_size=19),
            desk_question(r"Monte Carlo", r"simulate the position's value under a fitted model, as many times as needed: "
                          r"necessary for options and paths, only as good as the model", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three estimators. <bookmark mark='a'/> A parametric model fits a distribution and reads its quantile. <bookmark mark='b'/> Historical simulation applies a selected window of returns to today's exposure and interpolates a sample quantile; it is not literally the fifth worst observation here. Its empirical distribution and window are assumptions. <bookmark mark='c'/> Monte Carlo approximates a model's loss distribution, useful for nonlinear valuation, but neither simulation nor a larger draw count removes model error."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def _table(self, x, when):
        hx = [-3.4, 0.4, 3.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (rf"\$100m in the US market, {when}",
                                                                         r"VaR 99\%, \$m", r"ES 99\%, \$m")])
        tab = VGroup(head)
        for nm, key, col in ((r"normal, 500 days", "normal", MODEL_C), (r"historical simulation", "hs", DATA_C),
                             (rf"Student-$t$ ($\nu = {x['nu']:.1f}$)", "t", TAIL_C), (r"Monte Carlo, $t$", "mc", TAIL_C),
                             (r"RiskMetrics (EWMA)", "ewma", VAR_C)):
            v, e = x[key]
            tab.add(VGroup(label(nm, font_size=18, color=col), MathTex(f"{100 * v:.2f}", font_size=28),
                           MathTex(f"{100 * e:.2f}", font_size=28, color=ES_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.75 * j, 0])
        return tab

    def table(self, x, when):
        tab = self._table(x, when)
        with self.voiceover(
            "A hundred million dollars in the American stock market at the end of twenty oh seven, from the five hundred "
            f"days before. <bookmark mark='a'/> The normal says a VaR of {100 * x['normal'][0]:.1f} million; historical "
            f"simulation, {100 * x['hs'][0]:.1f}. <bookmark mark='b'/> A fitted Student t, whose degrees of freedom come "
            f"out near {x['nu']:.0f}, and its Monte Carlo agree on VaR with history but put expected shortfall far "
            f"higher, {100 * x['t'][1]:.1f} million. <bookmark mark='c'/> And RiskMetrics, reacting to the volatility "
            f"of that autumn, says {100 * x['ewma'][0]:.1f}. Five honest methods, and a spread of almost half the number."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(tab[5]))
        self.wait(0.4)
        self.clear_scene()

    def october(self, x):
        tab = self._table(x, r"15 Oct 2008")
        loss = -100 * x["next"]
        with self.voiceover(
            "The same position on the fifteenth of October twenty oh eight. <bookmark mark='a'/> The five-hundred-day "
            f"methods still see mostly calm: a normal VaR of {100 * x['normal'][0]:.1f} million, history "
            f"{100 * x['hs'][0]:.1f}. <bookmark mark='b'/> RiskMetrics, with volatility at {100 * x['sig_ann']:.0f} "
            f"percent a year, says {100 * x['ewma'][0]:.1f}. <bookmark mark='c'/> That day the market lost "
            f"{loss:.1f} percent: {loss:.1f} million on the position. Only the method that forgets the past quickly "
            "came close."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(Indicate(VGroup(tab[1], tab[2]), color=BAD, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Indicate(tab[5], color=GOOD, scale_factor=1.05))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def sqrt_rule(self, s):
        rows = [cmath(r"\text{VaR}_{10\text{d}}", r"\overset{?}{=}", r"\sqrt{10}\,\text{VaR}_{1\text{d}}", font_size=44,
                      colors={r"\text{VaR}_{10\text{d}}": VAR_C}),
                cmath(r"\text{1926--2020, history}", r":", rf"{100 * s['one_day']:.2f}\% \times \sqrt{{10}} = "
                      rf"{100 * s['scaled']:.2f}\%", font_size=36),
                cmath('\\text{overlapping 10-day arithmetic sums}', r":", rf"{100 * s['direct']:.2f}\%", font_size=38,
                      colors={rf"{100 * s['direct']:.2f}\%": BAD})]
        whys = [why('zero-mean iid Gaussian additive losses; nonzero mean scales linearly and volatility scales by the square root'),
                why(r"the one-day 99\% historical VaR of the US market, scaled"),
                why('quantile of sums of simple daily returns; larger here, without identifying the cause')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"The horizon exercise. <bookmark mark='a'/> Root-ten scaling is exact for zero-mean independent Gaussian additive daily losses with constant variance. With daily mean mu and standard deviation sigma, ten-day loss VaR is minus ten mu plus root ten times sigma times the normal quantile. <bookmark mark='b'/> The one-day empirical VaR is {100*s['one_day']:.2f} percent, whose root-ten scale is {100*s['scaled']:.2f}. <bookmark mark='c'/> The cached overlapping ten-day arithmetic-sum quantile is {100*s['direct']:.2f}. This omits compounding and uncertainty bands; the gap alone does not identify volatility clustering or a structural cause."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def decades(self, s):
        hx = [-3.4, -0.6, 2.0, 4.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"decade", r"$\sqrt{10}\times$ 1-day",
                                                                         r"10-day, direct", r"ratio")])
        tab = VGroup(head)
        for x in s["decades"]:
            ratio = x["direct"] / x["scaled"]
            tab.add(VGroup(MathTex(f"{x['decade']}s", font_size=24), MathTex(rf"{100 * x['scaled']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * x['direct']:.1f}\%", font_size=24),
                           MathTex(f"{ratio:.2f}", font_size=24, color=BAD if ratio > 1.05 else (GOOD if ratio < 0.95
                                                                                                 else GREY_A))))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.8 - 0.56 * j, 0])
        r70 = [x for x in s["decades"] if x["decade"] == 1970][0]
        r90 = [x for x in s["decades"] if x["decade"] == 1990][0]
        hi70 = r70["direct"] / r70["scaled"]
        lo90 = r90["direct"] / r90["scaled"]
        with self.voiceover(
            f"The ratio changes across selected decades. <bookmark mark='a'/> The nineteen-seventies arithmetic-sum quantile is {hi70:.2f} times its root-ten scale. <bookmark mark='b'/> The nineties ratio is {lo90:.2f}. These descriptive values mix sampling error, marginal tails and dependence. We have not computed an autocorrelation decomposition or a counterfactual that attributes the gap to rebounds or clustering. Root-time scaling can overstate as well as understate a chosen empirical horizon quantile."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def options(self, o):
        rows = [cmath(r"\text{delta-normal}", r":", rf"\${o['delta_normal']:,.0f}", font_size=40, colors={r"\text{delta-normal}": BAD}),
                cmath(r"\text{delta-gamma}", r":", rf"\${o['delta_gamma'][0]:,.0f}", font_size=40),
                cmath(r"\text{full revaluation}", r":", rf"\${o['full'][0]:,.0f}", font_size=40, colors={r"\text{full revaluation}": GOOD}),
                cmath(r"\text{plus a 5-point vol rise}", r":", rf"\${o['vol_shock'][0]:,.0f}", font_size=38,
                      colors={r"\text{plus a 5-point vol rise}": TAIL_C})]
        whys = [why(r"a book short 1,000 at-the-money one-month straddles, delta-hedged: its delta is zero, so the linear "
                    r"approximation sees no risk at all"),
                why('quadratic spot term only; theta is omitted, whereas full revaluation advances maturity by a day'),
                why('model-based full revaluation, including one day of decay; fixed implied volatility and static hedge'),
                why('chosen five-volatility-point shock on every simulated path, not only the worst spot paths; no calibrated joint volatility model')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"A chosen short-straddle example. <bookmark mark='a'/> One thousand at-the-money straddles are initially delta hedged, making the linear spot-only VaR zero. <bookmark mark='b'/> The quadratic spot term gives {o['delta_gamma'][0]:,.0f} dollars. <bookmark mark='c'/> Full Black--Scholes revaluation gives {o['full'][0]:,.0f}, but also includes a day of maturity decay that the quadratic approximation omits. Their difference is not solely a gamma-approximation error. <bookmark mark='d'/> Raising implied volatility by five points on every simulated path gives {o['vol_shock'][0]:,.0f}. This is a chosen stress, not a fitted joint spot-volatility forecast or an executable loss guarantee."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def what_var_says(self):
        cards = VGroup(
            desk_question(r"what it says", r"on 99 days in 100, under the model, the loss will be smaller than this", width=12.4,
                          font_size=19),
            desk_question(r"what it does not say", r"how large the other day's loss will be; whether the model is right; "
                          r"what happens if the position cannot be sold in a day", width=12.4, font_size=19),
            desk_question(r"why it lasted", r"one number that adds up across desks (almost), that a board can read, and "
                          r"that can be checked against the days that follow", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the number is. <bookmark mark='a'/> It says that on ninety-nine days in a hundred, under the model, the "
            "loss will be smaller. <bookmark mark='b'/> It does not say how large the hundredth day's loss will be, "
            "whether the model is right, or what happens if the position cannot be sold in a day. "
            "<bookmark mark='c'/> It lasted because it is one number that a board can read and that can be checked "
            "against the days that follow. The next two chapters ask whether it should be added up, and how to check it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two bonds each lose \$100 with probability 4\%, independently, and nothing otherwise. Each has a "
                       r"95\% VaR of zero. What is the 95\% VaR of holding both?")
        with self.voiceover(
            "Pause and predict. Two bonds each lose a hundred dollars with probability four percent, independently, and "
            "nothing otherwise. Each has a ninety-five percent VaR of zero. What is the ninety-five percent VaR of "
            "holding both?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
