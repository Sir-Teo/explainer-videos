from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
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
                cmath(r"\text{ES}_\alpha", r"=", r"\mathbb E[L \mid L \ge \text{VaR}_\alpha]", font_size=40,
                      colors={r"\text{ES}_\alpha": ES_C}),
                cmath(r"\alpha = 99\%", r":", r"\text{exceeded on one day in a hundred}", font_size=38)]
        whys = [why(r"work in losses: a loss is a negative return, so the left tail of returns is the right tail of $L$"),
                why(r"value at risk: the $\alpha$-quantile of the loss, the threshold exceeded with probability $1 - \alpha$"),
                why(r"expected shortfall: the average loss on the days beyond it (Acerbi and Tasche 2002)"),
                why(r"a promise about frequency only: VaR says nothing about how bad the bad days are; ES does")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The definitions. <bookmark mark='a'/> Work in losses: a loss is a negative return. <bookmark mark='b'/> "
            "Value at risk at confidence alpha is the alpha quantile of the loss, the threshold exceeded with "
            "probability one minus alpha. <bookmark mark='c'/> Expected shortfall is the average loss on the days "
            "beyond it. <bookmark mark='d'/> At ninety-nine percent, the VaR should be exceeded on one day in a hundred. "
            "That is a promise about how often, and says nothing about how much; expected shortfall says how much."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def picture(self):
        xs = np.linspace(-6, 6, 300)
        nu = 4.0
        pdf = stats.t.pdf(xs, nu)
        g = axes([-6, 6], [0, 0.42], x_length=8.4, y_length=4.0, xlabel=r"loss, in standard units", ylabel=r"density",
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
            "In a picture, for a Student t with four degrees of freedom. <bookmark mark='a'/> VaR is a line: one percent "
            f"of the mass lies beyond {v:.2f}. <bookmark mark='b'/> Expected shortfall is the shaded mass's centre of "
            f"gravity, at {es:.2f}: it moves when the tail grows fatter, even if the line stays where it is."
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
                cmath(r"\text{4.15 report}", r":", r"\text{one number, every evening}", font_size=36)]
        whys = [why(r"J.P. Morgan's RiskMetrics (1994, published 1996): an exponentially weighted variance, Part 7's "
                    r"EWMA"),
                why(r"with normal returns, the 99\% quantile is 2.33 standard deviations"),
                why(r"the firm-wide market risk on one page after the close, as reported; Basel's 1996 amendment then let "
                    r"banks use such models for capital")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Where the number came from. <bookmark mark='a'/> J.P. Morgan's RiskMetrics, published in nineteen ninety-six: "
            "an exponentially weighted variance with lambda nought point nine four, Part seven's EWMA. "
            "<bookmark mark='b'/> With normal returns, the ninety-nine percent VaR is two point three three standard "
            "deviations times the position. <bookmark mark='c'/> It was reported to have been delivered to the chairman "
            "at four fifteen every afternoon, and Basel's nineteen ninety-six amendment let banks base capital on such "
            "models."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def three_ways(self):
        cards = VGroup(
            desk_question(r"parametric", r"assume a distribution, normal or Student-t, estimate its parameters, read off "
                          r"the quantile: quick, and wrong in exactly the way the assumption is wrong", width=12.4,
                          font_size=19),
            desk_question(r"historical simulation", r"replay the last 500 days' returns on today's position and take the "
                          r"fifth-worst: no distribution assumed, but only the past window's tail", width=12.4,
                          font_size=19),
            desk_question(r"Monte Carlo", r"simulate the position's value under a fitted model, as many times as needed: "
                          r"necessary for options and paths, only as good as the model", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three ways to estimate it. <bookmark mark='a'/> Parametric: assume a distribution, estimate it, read off "
            "the quantile. <bookmark mark='b'/> Historical simulation: replay the last five hundred days' returns on "
            "today's position and take the fifth worst, assuming nothing but the window. <bookmark mark='c'/> And Monte "
            "Carlo: simulate the position under a fitted model, necessary when options make the loss non-linear."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
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
                cmath(r"\text{overlapping 10-day returns}", r":", rf"{100 * s['direct']:.2f}\%", font_size=38,
                      colors={rf"{100 * s['direct']:.2f}\%": BAD})]
        whys = [why(r"exact only for independent, identically distributed normal returns; Basel let banks scale this way"),
                why(r"the one-day 99\% historical VaR of the US market, scaled"),
                why(r"the quantile of actual ten-day losses: larger, because big days cluster and volatility persists")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The desk question's rule. <bookmark mark='a'/> Ten-day VaR as the square root of ten times one-day VaR: "
            "exact only for independent normal returns. <bookmark mark='b'/> On the American market from twenty-six to "
            f"twenty twenty, the one-day ninety-nine percent historical VaR of {100 * s['one_day']:.2f} percent scales to "
            f"{100 * s['scaled']:.2f}. <bookmark mark='c'/> The ten-day losses that actually happened put it at "
            f"{100 * s['direct']:.2f}: big days cluster, and the rule understates."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            "Decade by decade, the rule is neither safe nor conservative. <bookmark mark='a'/> In the nineteen seventies "
            f"the actual ten-day VaR was {hi70:.2f} times the scaled one: daily returns were positively autocorrelated, "
            "so bad days followed bad days. "
            f"<bookmark mark='b'/> In the nineties, {lo90:.2f}: bad days were followed by rebounds. The error depends on "
            "the dependence between days, which the rule assumes away."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.15))
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
                why(r"add Part 10's gamma: the loss is quadratic in the move, simulated"),
                why(r"reprice every option at every simulated spot: the honest number, 99\% over one day"),
                why(r"and options also lose when implied volatility rises, a risk factor the spot-only VaR never moves")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why Monte Carlo is needed for options. <bookmark mark='a'/> A book short a thousand at-the-money straddles, "
            "delta-hedged. Its delta is zero, so the linear, delta-normal VaR is zero. <bookmark mark='b'/> Adding gamma, "
            f"the loss becomes quadratic, and the VaR {o['delta_gamma'][0]:,.0f} dollars. <bookmark mark='c'/> Repricing "
            f"every option at every simulated price gives {o['full'][0]:,.0f}. <bookmark mark='d'/> And if implied "
            f"volatility rises five points at the same time, {o['vol_shock'][0]:,.0f}: a risk factor that a spot-only "
            "model never moves."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
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
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
