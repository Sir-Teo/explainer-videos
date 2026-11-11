from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from explainer.quant.house import risk as R
from videos.quant.quant40.common import (
    BAD,
    DATA_C,
    ES_C,
    GOOD,
    HIT_C,
    HURDLE,
    MODEL_C,
    PART,
    VAR_C,
    load,
)

NAMES = {"normal": r"normal, 500 days", "hs": r"historical simulation", "ewma": r"RiskMetrics (EWMA)",
         "fhs": r"filtered HS (EWMA)", "gjr_fhs": r"filtered HS (GJR-GARCH)", "evt": r"GJR + EVT (McNeil--Frey)"}


class Backtest(VoiceoverScene):
    def construct(self):
        b = load("backtest")
        self.card()
        self.kupiec_()
        self.light()
        self.christoffersen_()
        self.table(b)
        self.crisis(b)
        self.bars(b)
        self.years(b)
        self.z2(b)
        self.lessons()
        self.question()

    def card(self):
        k = R.kupiec(np.r_[np.ones(7), np.zeros(243)].astype(int), 0.01)
        c = chapter_card(3, r"Backtesting", r"How do we know a risk number was right?", part=PART)
        with self.voiceover(
            'Chapter three. Seven exceptions in two hundred and fifty days place the historical Basel traffic light in yellow. A coverage likelihood ratio uses a chi-square approximation and can reject at five percent, but sparse counts make finite-sample calibration relevant. Non-rejection would not prove the model correct. We also inspect timing: a correct conditional continuous quantile implies unpredictable hits relative to the forecast information set, not merely an acceptable unconditional total.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kupiec_(self):
        rows = [cmath(r"I_t", r"=", r"\mathbf 1\{L_t > \text{VaR}_t\}", font_size=42, colors={r"I_t": HIT_C}),
                cmath(r"\text{H}_0", r":", r"I_t \sim \text{iid Bernoulli}(1 - \alpha)", font_size=40),
                cmath(r"\text{LR}_{uc}", r"=", r"-2\log\frac{p^x(1 - p)^{T - x}}{\hat p^x(1 - \hat p)^{T - x}} \sim \chi^2_1",
                      font_size=34, colors={r"\text{LR}_{uc}": VAR_C})]
        whys = [why(r"the hit sequence: one on each day the loss exceeded the forecast made the evening before"),
                why('under a correct continuous conditional quantile and its information set, hits have conditional probability p with probability $p = 1 - \\alpha$'),
                why('Kupiec (1995), with a chi-square asymptotic null: the likelihood ratio of the promised rate against the observed one, as in Parts 2 and 21')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A forecast can be checked. <bookmark mark='a'/> Each day the loss either exceeds the forecast made the "
            "evening before or it does not: the hit sequence. <bookmark mark='b'/> If the forecast is right, hits are "
            "independent coin flips with probability one minus alpha. <bookmark mark='c'/> Paul Kupiec's test compares "
            "the promised rate with the observed one by a likelihood ratio, as Parts two and twenty-one did."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def light(self):
        zones = [(r"green", r"0 to 4 exceptions", r"multiplier 3", GOOD),
                 (r"yellow", r"5 to 9", r"3.4 to 3.85", HURDLE),
                 (r"red", r"10 or more", r"4, and the model is reviewed", BAD)]
        rows = VGroup()
        for nm, cnt, mult, col in zones:
            box = RoundedRectangle(width=11.0, height=1.0, corner_radius=0.12, stroke_color=col, fill_color=col,
                                   fill_opacity=0.15)
            t = VGroup(label(nm, font_size=24, color=col), label(cnt, font_size=22), label(mult, font_size=20,
                                                                                         color=GREY_A))
            t.arrange(RIGHT, buff=1.2).move_to(box)
            rows.add(VGroup(box, t))
        rows.arrange(DOWN, buff=0.25).move_to(UP * 0.2)
        foot = wrapped_label(r"Basel's 1996 traffic light for a 99\% one-day VaR over 250 days: the capital multiplier "
                             r"on the model's VaR rises with the exceptions", 11.4, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Regulators turned the count into a traffic light. <bookmark mark='a'/> Over two hundred and fifty days, up "
            "to four exceptions is green, and capital is three times the model's VaR. <bookmark mark='b'/> Five to nine "
            "is yellow, with a rising multiplier. <bookmark mark='c'/> Ten or more is red: the multiplier is four and the "
            "model is reviewed."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def christoffersen_(self):
        rows = [cmath(r"\pi_{01}", r"=", r"P(I_t = 1 \mid I_{t-1} = 0)", font_size=40),
                cmath(r"\pi_{11}", r"=", r"P(I_t = 1 \mid I_{t-1} = 1)", font_size=40, colors={r"\pi_{11}": HIT_C}),
                cmath(r"\text{H}_0^{ind}", r":", r"\pi_{01} = \pi_{11}", font_size=40),
                cmath(r"\text{LR}_{cc}", r"=", r"\text{LR}_{uc} + \text{LR}_{ind} \sim \chi^2_2", font_size=40,
                      colors={r"\text{LR}_{cc}": VAR_C})]
        whys = [why(r"Christoffersen (1998): model the hits as a two-state Markov chain"),
                why(r"after an exception, how likely is another the next day?"),
                why(r"a correct forecast makes yesterday's hit irrelevant to today's"),
                why(r"conditional coverage tests the right count and the right timing together")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Peter Christoffersen added the timing. <bookmark mark='a'/> Treat the hits as a two-state Markov chain: the "
            "chance of an exception after a quiet day, <bookmark mark='b'/> and after an exception. "
            "<bookmark mark='c'/> A correct forecast makes them equal: yesterday's hit tells you nothing. "
            "<bookmark mark='d'/> Adding the two likelihood ratios tests the count and the timing together."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, b):
        hx = [-4.4, -1.4, 0.6, 2.6, 4.8]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"one-day 99\% forecaster, 1928--2020",
                                                                         r"exceptions", r"Kupiec $p$",
                                                                         r"$\pi_{11}$", r"independence $p$")])
        tab = VGroup(head)
        for m in ("normal", "hs", "ewma", "fhs", "gjr_fhs", "evt"):
            x = b["methods"][m]
            ok = x["kupiec_p"] > 0.05 and x["ind_p"] > 0.05
            tab.add(VGroup(label(NAMES[m], font_size=17, color=GOOD if ok else WHITE),
                           MathTex(rf"{100 * x['rate']:.2f}\%", font_size=24, color=HIT_C),
                           MathTex(f"{x['kupiec_p']:.3f}", font_size=24), MathTex(f"{x['p11']:.3f}", font_size=24),
                           MathTex(f"{x['ind_p']:.3f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.7 * j, 0])
        n, g = b["methods"]["normal"], b["methods"]["gjr_fhs"]
        e = b["methods"]["evt"]
        with self.voiceover(
            f"Six reported forecasters, with {n['T']:,} observations each. <bookmark mark='a'/> Normal exceptions are {100*n['rate']:.2f} percent and follow an exception {100*n['p11']:.0f} percent of the time; history and RiskMetrics also reject selected tests. <bookmark mark='b'/> GJR filtering reports {100*g['rate']:.2f} percent with neither coverage nor first-order independence rejected at five percent. This does not establish calibration at every horizon or independence beyond one lag. More importantly, the unchanged filter initializes each refit variance with a segment that includes some evaluation returns. These are descriptive implementation comparisons, not strictly past-measurable validation. <bookmark mark='c'/> EVT reports {100*e['rate']:.2f} percent, which the two-sided coverage test rejects on the conservative side."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), LaggedStart(*[FadeIn(r_) for r_ in tab[2:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
            vo.wait_until("c")
            self.play(FadeIn(tab[6]))
        self.wait(0.4)
        self.clear_scene()

    def crisis(self, b):
        y = b["y2008"]
        dd = np.asarray(y["d"], int)
        from datetime import date
        t = np.array([date(int(v//10000),int(v//100%100),int(v%100)).year +
                      (date(int(v//10000),int(v//100%100),int(v%100))-date(int(v//10000),1,1)).days /
                      (date(int(v//10000)+1,1,1)-date(int(v//10000),1,1)).days for v in dd])
        L = -100 * np.asarray(y["r"], float)
        g = axes([2008, 2010], [-6, 10], x_length=8.2, y_length=4.2, xlabel=r"2008--2009, daily",
                 ylabel=r"loss and 99\% VaR, \%", xticks=[2008, 2009, 2010], yticks=[-5, 0, 5, 10],
                 font_size=14).move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, max(min(l_, 10), -6)), stroke_width=1.6,
                             color=DATA_C, stroke_opacity=0.5) for x, l_ in zip(t, L)])
        cn = curve(ax, t, 100 * np.asarray(y["normal"], float), MODEL_C, stroke_width=2.5)
        cg = curve(ax, t, np.minimum(100 * np.asarray(y["gjr"], float), 10), VAR_C, stroke_width=2.5)
        hits_n = VGroup(*[Dot(ax.c2p(x, min(l_, 10)), radius=0.05, color=BAD) for x, l_, v in
                          zip(t, L, 100 * np.asarray(y["normal"], float)) if l_ > v])
        leg = legend([(MODEL_C, r"normal, 500 days"), (VAR_C, r"filtered HS (GJR)"), (BAD, r"exceptions of the normal")],
                     font_size=16).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Where the failures come from. <bookmark mark='a'/> Through twenty oh eight, the five-hundred-day normal VaR "
            "barely moves while the losses grow: its exceptions arrive in bunches, in September and October. "
            "<bookmark mark='b'/> The GARCH-filtered forecast rises with volatility within days, and the losses mostly "
            "stay under it. A risk number must forget the calm quickly enough to see the storm."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cn), FadeIn(hits_n))
            vo.wait_until("b")
            self.play(Create(cg))
        self.wait(0.4)
        self.clear_scene()

    def bars(self, b):
        yrs = np.asarray(b["years"], int)
        n = np.asarray(b["methods"]["normal"]["per_year"], float)
        g_ = np.asarray(b["methods"]["gjr_fhs"]["per_year"], float)
        top = float(max(n.max(), g_.max()) + 2)
        g = axes([1928, 2021], [0, top], x_length=9.6, y_length=3.8, xlabel=r"exceptions of a 99\% VaR per year",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 2.5, 10, 20, 30], font_size=14).move_to(DOWN * 0.3)
        ax = g.ax
        bn = VGroup(*[Rectangle(width=0.035, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                fill_color=MODEL_C, fill_opacity=0.75).move_to(ax.c2p(y - 0.2, 0), aligned_edge=DOWN)
                      for y, v in zip(yrs, n)])
        bg = VGroup(*[Rectangle(width=0.035, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                fill_color=VAR_C, fill_opacity=0.9).move_to(ax.c2p(y + 0.2, 0), aligned_edge=DOWN)
                      for y, v in zip(yrs, g_)])
        exp_ = DashedLine(ax.c2p(1928, 2.5), ax.c2p(2021, 2.5), color=GREY_B)
        red = DashedLine(ax.c2p(1928, 10), ax.c2p(2021, 10), color=BAD)
        leg = legend([(MODEL_C, r"normal, 500 days"), (VAR_C, r"filtered HS (GJR)"), (BAD, r"red zone, 10")], font_size=16)
        leg.to_corner(UR, buff=0.4)
        worst = int(yrs[int(np.argmax(n))])
        n_max = int(n.max())
        with self.voiceover(
            f"Calendar-year exception counts. <bookmark mark='a'/> The normal series peaks in {worst}, with {n_max} exceptions. <bookmark mark='b'/> The filtered series is smaller in many years, but the dashed two-and-a-half line is only the expectation for exactly two hundred and fifty trials. Calendar years and the first partial year have different lengths. Sparse yearly outcomes do not prove equal crisis and calm calibration, and the filter initialization caveat still applies."
        ) as vo:
            self.play(FadeIn(g), Create(exp_), Create(red), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in bn], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in bg], lag_ratio=0.01))
        self.wait(0.4)
        self.clear_scene()

    def years(self, b):
        hx = [-3.4, -0.6, 2.2, 4.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"forecaster", r"red years", r"yellow years",
                                                                         r"years")])
        tab = VGroup(head)
        ny = len(b["years"])
        for m in ("normal", "hs", "ewma", "fhs", "gjr_fhs", "evt"):
            x = b["methods"][m]
            tab.add(VGroup(label(NAMES[m], font_size=17), MathTex(str(x["red"]), font_size=26, color=BAD),
                           MathTex(str(x["yellow"]), font_size=26, color=HURDLE), MathTex(str(ny), font_size=22,
                                                                                         color=GREY_B)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.7 * j, 0])
        n, g = b["methods"]["normal"], b["methods"]["gjr_fhs"]
        with self.voiceover(
            f"The historical traffic-light thresholds applied descriptively to calendar years. <bookmark mark='a'/> Normal has {n['red']} red calendar years out of {ny}. <bookmark mark='b'/> GJR has {g['red']} red and {g['yellow']} yellow. These are not the regulatory rolling two-hundred-and-fifty-day windows. Their unequal lengths and the filter initialization prevent a regulatory pass claim or a direct probability statement about model luck."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), LaggedStart(*[FadeIn(r_) for r_ in tab[2:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def z2(self, b):
        cr = b["z2_crit"]
        c95 = cr["normal"]["q95"]
        c95t = cr["t4"]["q95"]
        rows = [cmath(r"Z_2", r"=", r"\frac{1}{T(1 - \alpha)}\sum_t \frac{L_t I_t}{\text{ES}_t} - 1", font_size=40,
                      colors={r"Z_2": ES_C}),
                cmath(r"Z_2^{5\%}", r"\approx", rf"{c95:.2f}\ \text{{(normal)}},\ {c95t:.2f}\ (t_4)", font_size=36)]
        whys = [why('Acerbi and Székely (2014): on the days beyond VaR, were the losses as large as the ES promised? zero in expectation under correct continuous conditional VaR and ES; positive flags underestimation or other misspecification'),
                why('its 5\\% critical value for this many days, simulated under a correct forecast: these two iid null examples only; not a distribution-free critical value for arbitrary dependent forecasts')]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.3, buff=0.6, edge=6.9)
        hx = [-2.6, 2.6]
        tab = VGroup()
        for j, m in enumerate(("normal", "hs", "ewma", "fhs", "gjr_fhs", "evt")):
            z = b["methods"][m]["z2"]
            tab.add(VGroup(label(NAMES[m], font_size=17).move_to([hx[0], 1.5 - 0.65 * j, 0]),
                           MathTex(f"{z:+.2f}", font_size=24, color=BAD if z > c95 else GOOD).move_to([hx[1], 1.5 - 0.65 * j, 0])))
        n = b["methods"]["normal"]["z2"]
        with self.voiceover(
            f"The shortfall diagnostic. <bookmark mark='a'/> Z two averages loss times the VaR-hit indicator divided by the ES forecast and tail probability, then subtracts one. Under correct continuous conditional VaR and ES, suitable integrability and a nonzero ES denominator, its expectation is zero. Realized values fluctuate; a positive statistic can reflect either quantile or tail-severity error. <bookmark mark='b'/> In this sample-size experiment, simulated iid normal and t-four null critical values are {c95:.2f} and {c95t:.2f}. Similar values in two models are not a distribution-free theorem. <bookmark mark='c'/> The normal statistic is {n:+.2f}; negative filtered statistics do not establish correctness or rule out overconservatism."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.clear_scene()
            head=label(r"Z2: separate reported statistics",font_size=30).to_edge(UP,buff=0.4)
            self.play(FadeIn(head),LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"backtests have little power", r"at 99\%, a year holds 2.5 expected exceptions: a model off by "
                          r"half is often green; decades of data are needed to separate good from bad", width=12.4,
                          font_size=19),
            desk_question(r"clustering is the tell", 'check clustering as well as coverage; neither rejection ordering nor test power is universal', width=12.4, font_size=19),
            desk_question(r"conservatism is not free", r"too many capital charges for too little risk is also a failed "
                          r"model: the EVT forecaster was rejected for being too cautious", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> At one percent, two hundred and fifty correctly calibrated continuous observations have two and a half expected exceptions, so sparse-count tests can have low power. The exact power depends on the alternative. <bookmark mark='b'/> Check dependence as well as coverage; first-order timing tests do not exhaust all serial patterns, and there is no universal ordering of which test rejects first. <bookmark mark='c'/> Two-sided tests can reject overconservative as well as aggressive quantiles. Capital cost and model calibration are related but distinct evaluation criteria."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the US market's worst day since 1926 was a loss of about 17\%. Under a normal distribution fitted "
                       r"to all those days, how often should a day like that happen?")
        with self.voiceover(
            "Pause and predict. The American market's worst day since nineteen twenty-six was a loss of about seventeen "
            "percent. Under a normal distribution fitted to all those days, how often should a day like that happen?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
