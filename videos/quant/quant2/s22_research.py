from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CCP, GAIN, LOSS, PART, RATE, load


def ask(text: str):
    """The pause-and-predict banner at the foot of the frame."""
    return wrapped_label(rf"Pause and predict: {text}", 12.4, 25, QC.IDEA).to_edge(DOWN, buff=0.3)


def fit_right(m, edge: float = 6.75):
    """Shift ``m`` left until its right edge is inside the frame."""
    m.shift(LEFT * max(0.0, m.get_right()[0] - edge))
    return m


EWMA, CONST = CCP, QC.REALIZED


class Research(VoiceoverScene):
    def construct(self):
        t = load("backtest_theory")
        self.card()
        self.wilks()
        self.discrete(t)
        self.markov()
        self.power(t)
        self.us(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Backtesting a margin model", r"What can a count of breaches prove, and what can it not?",
                          part=PART)
        with self.voiceover("For the researcher: backtesting Chapter 9's margin model. It promises one breach in a hundred days. Can "
                            "a count tell us whether it works?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def wilks(self):
        rows = [cmath(r"I_t", r"=", r"\mathbf 1\{r_t < -m_t\},\quad H_0:\ I_t \overset{\text{iid}}{\sim} \text{Bernoulli}(p)",
                      font_size=32, colors={r"I_t": LOSS}),
                cmath(r"\text{LR}_{uc}", r"=", r"-2\ln\frac{(1 - p)^{T - x}p^x}{(1 - \hat p)^{T - x}\hat p^x},\quad \hat p = "
                      r"\tfrac xT", font_size=32, colors={r"\text{LR}_{uc}": CCP}),
                cmath(r"\text{LR}_{uc}", r"=", r"\frac{(\hat p - p)^2}{p(1 - p)/T} + O_p(T^{-1/2})", font_size=32,
                      colors={r"\text{LR}_{uc}": CCP}),
                cmath(r"\text{LR}_{uc}", r"\Rightarrow", r"\chi^2_1", font_size=32, colors={r"\text{LR}_{uc}": CCP})]
        whys = [why(r"a breach indicator for each day; a correct model makes them independent coin flips with "
                    r"probability $p$ = 1\%"),
                why(r"Kupiec (1995): the likelihood ratio of the promised rate against the best-fitting one"),
                why(r"expand the log-likelihood to second order around $\hat p$: the ratio is the squared standardised "
                    r"error of the breach rate"),
                why(r"Wilks (1938): by the central limit theorem the standardised rate is $N(0, 1)$, so its square is "
                    r"$\chi^2$ with one degree of freedom; reject above 3.84 at 5\%")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The test is a likelihood ratio. <bookmark mark='a'/> Mark each day the margin was breached. If the model "
            "is right, the marks are independent coin flips that land heads one time in a hundred. <bookmark "
            "mark='b'/> Kupiec's statistic compares the likelihood of the promised rate with the likelihood of the "
            "rate observed. <bookmark mark='c'/> Expand it to second order and it is the squared standardised error "
            "of the breach rate. <bookmark mark='d'/> So by the central limit theorem it tends to a chi-squared with "
            "one degree of freedom: Wilks's theorem. Reject the model when it exceeds three point eight four."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def discrete(self, t):
        pmf = np.asarray(t["size"]["250"]["pmf"])
        n = len(pmf)
        g = axes([-0.6, n - 0.4], [0, 0.3], x_length=8.0, y_length=3.8, xlabel=r"breaches in 250 days, model correct",
                 ylabel=r"probability", xticks=[0, 2, 4, 6, 8, 10, 12, 14], yticks=[0, 0.1, 0.2, 0.3], font_size=13).move_to(
            LEFT * 1.6 + DOWN * 0.3)
        ax = g.ax
        from explainer.quant.house import funding
        bars = VGroup()
        for k, v in enumerate(pmf):
            lr = funding.kupiec(k, 250, 0.01)["LR"]
            col = LOSS if lr > 3.841 else (QC.DELTA if k >= 5 else GAIN)
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(Rectangle(width=0.6 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=max(y1 - y0, 0.005),
                               stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([ax.c2p(k, 0)[0], (y0 + y1) / 2, 0]))
        s250, s1000, tr = t["size"]["250"], t["size"]["1000"], t["traffic"]
        side = VGroup(
            MathTex(rf"\text{{nominal 5\%, actual}}:\ {100 * s250['exact']:.1f}\%", font_size=24, color=LOSS),
            MathTex(rf"x \in \{{0,\ldots,250\}}:\ {s250['count_support']}\ \text{{possible counts}}", font_size=22),
            MathTex(rf"T = 1{{,}}000:\ {100 * s1000['exact']:.1f}\%", font_size=22),
            MathTex(rf"\text{{Basel yellow or red}}:\ {100 * tr['p_yellow_or_worse']:.1f}\%", font_size=22, color=QC.DELTA),
            wrapped_label(r"red bars: counts the $\chi^2$ test rejects (0, and 7 or more); amber: the Basel traffic "
                          r"light's yellow zone (5 to 9 in 250 days). The probabilities are exact binomial ones", 3.4,
                          15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "But a year of trading is two hundred and fifty days, and a breach count is a small whole number. "
            "<bookmark mark='a'/> These are the exact chances of each count for a correct model. The chi-squared "
            "test rejects at zero breaches and at seven or more, and those counts together have probability nine and a "
            "half percent, almost twice the nominal five. There are two hundred and fifty-one possible counts, but "
            "most probability sits on just a few small ones. Discreteness still matters. At a thousand days the size "
            "is five and a half percent. <bookmark mark='b'/> The "
            "Basel traffic light, which counts breaches in a year, puts a correct model in its yellow zone or worse "
            "about one year in nine. That is a design choice, not an accident: a regulator prefers false alarms."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1:]], lag_ratio=0.05), FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(FadeIn(side[3:]))
        self.wait(0.4)
        self.clear_scene()

    def markov(self):
        rows = [cmath(r"\pi_{ij}", r"=", r"\Pr(I_t = j \mid I_{t-1} = i)", font_size=32, colors={r"\pi_{ij}": CONST}),
                cmath(r"\text{LR}_{ind}", r"=", r"-2\ln\frac{(1 - \hat\pi)^{n_{00} + n_{10}}\hat\pi^{n_{01} + n_{11}}}"
                      r"{(1 - \hat\pi_{01})^{n_{00}}\hat\pi_{01}^{n_{01}}(1 - \hat\pi_{11})^{n_{10}}\hat\pi_{11}^{n_{11}}}"
                      r"\ \Rightarrow\ \chi^2_1", font_size=28, colors={r"\text{LR}_{ind}": CONST}),
                cmath(r"\text{LR}_{cc}", r"=", r"\text{LR}_{uc} + \text{LR}_{ind}\ \Rightarrow\ \chi^2_2", font_size=32,
                      colors={r"\text{LR}_{cc}": QC.IDEA})]
        whys = [why(r"Christoffersen (1998): let breaches follow a two-state Markov chain; a correct model has "
                    r"$\pi_{01} = \pi_{11} = p$, so a breach yesterday says nothing about today"),
                why(r"the independence test: one transition probability against two, by counts $n_{ij}$ of each "
                    r"transition; Wilks again, one restriction"),
                why(r"conditional coverage: the right count and no memory; the two statistics are asymptotically "
                    r"independent, so their sum is $\chi^2_2$ (the House's \texttt{funding.christoffersen})")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "A count cannot see timing. A margin that is too thin in every crisis and too thick in every calm can "
            "have the right number of breaches, all in a few bad months. <bookmark mark='a'/> Christoffersen let the "
            "breaches follow a two-state Markov chain: the chance of a breach today given a breach yesterday, or "
            "given none. A correct model makes both equal to p. <bookmark mark='b'/> The independence test compares "
            "one transition probability with two, by counting each kind of transition: Wilks again, with one "
            "restriction. <bookmark mark='c'/> And the two tests add up to a test of conditional coverage, the right "
            "count with no memory, chi-squared with two degrees of freedom."
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

    def power(self, t):
        pw = t["power"]
        hx = [-3.6, 0.8, 3.0, 5.0]
        head = VGroup(label(r"rejected at 5\%, 1{,}000 days", font_size=18, color=GREY_B),
                      label(r"$\text{LR}_{uc}$", font_size=20), label(r"$\text{LR}_{ind}$", font_size=20),
                      label(r"$\text{LR}_{cc}$", font_size=20))
        rows_ = [(r"EWMA margin, $\lambda = 0.97$", pw["ewma"], EWMA),
                 (r"constant margin, the right long-run variance", pw["constant"], CONST)]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(nm, font_size=18, color=col),
                                                 *[MathTex(rf"{100 * d[k]:.0f}\%", font_size=26) for k in ("uc", "ind", "cc")])
                                          for nm, d, col in rows_]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.75 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.0, 0, 0]), LEFT)
            tab.add(row)
        extra = VGroup(
            MathTex(rf"\text{{breach rate}}:\ {100 * pw['ewma']['hits']:.2f}\%\ \text{{vs}}\ {100 * pw['constant']['hits']:.2f}\%",
                    font_size=24),
            MathTex(rf"\Pr(\text{{breach}} \mid \text{{breach yesterday}}):\ {100 * pw['ewma']['p11']:.1f}\%\ \text{{vs}}\ "
                    rf"{100 * pw['constant']['p11']:.1f}\%", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 1.2)
        g_ = t["garch"]
        foot = note(rf"2{{,}}000 simulated GARCH(1,1) paths, $(\omega, \alpha, \beta) = ({g_[0]:g}, {g_[1]}, {g_[2]})$, "
                    r"normal shocks; 99\% one-day margins", font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How well do the tests see? Simulate four years of daily returns with clustered volatility. <bookmark "
            "mark='a'/> The EWMA count test rejects about eight percent, above the nominal five. A constant margin with "
            "exactly the right long-run variance is breached one and a half percent of the time, because clustered "
            "volatility fattens the tails, and the count test catches it about half the time. <bookmark mark='b'/> "
            "But the independence test, built for exactly this failure, catches it only one time in four. A breach "
            "after a breach is six percent likely instead of one, and four years still hold too few breaches to "
            "show it. This low power is the test's well-known weakness."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(extra[0]))
            vo.wait_until("b")
            self.play(FadeIn(extra[1]))
        self.wait(0.4)
        self.clear_scene()

    def us(self, t):
        us = t["us"]
        decs = list(us["ewma"]["by_decade"].keys())
        n = len(decs)
        top = max(max(us[k]["by_decade"].values()) for k in us) * 1.1
        g = axes([-0.6, n - 0.4], [0, top], x_length=9.0, y_length=3.8, xlabel=r"decade", ylabel=r"breaches of a 99\% "
                 r"one-day margin", xticks=[], yticks=[0, 50, 100, 150, 200], font_size=13).move_to(LEFT * 1.2 + DOWN * 0.4)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, dc in enumerate(decs):
            for j, (k, col) in enumerate((("ewma", EWMA), ("constant", CONST))):
                v = us[k]["by_decade"][dc]
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=0.3 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=max(y1 - y0, 0.01),
                                   stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    [ax.c2p(i + (j - 0.5) * 0.34, 0)[0], (y0 + y1) / 2, 0]))
            labs.add(label(rf"{dc}s", font_size=14, color=GREY_B).next_to(ax.c2p(i, 0), DOWN, buff=0.12))
        side = VGroup(
            MathTex(rf"\text{{EWMA}}:\ {100 * us['ewma']['hits'] / t['us_T']:.1f}\%,\ \text{{LR}}_{{ind}} = {us['ewma']['LR_ind']:.0f}",
                    font_size=22, color=EWMA),
            MathTex(rf"\text{{constant}}:\ {100 * us['constant']['hits'] / t['us_T']:.1f}\%,\ \text{{LR}}_{{ind}} = "
                    rf"{us['constant']['LR_ind']:.0f}", font_size=22, color=CONST),
            wrapped_label(r"the US market's daily log return, 1926--2020, against Chapter 9's EWMA margin and a constant "
                          r"one at the full sample's volatility; both 99\%, normal quantile", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        fit_right(side)
        with self.voiceover(
            "Ninety-five years of the American market give a historical stress test. The constant margin uses the "
            "full sample's volatility, so it is a hindsight benchmark, not a tradable forecast. <bookmark mark='a'/> Its breaches "
            "pile into the 1930s and the 2000s: almost two hundred in one decade, six in another. <bookmark mark='b'/> "
            "EWMA reduces clustering, but the independence test still rejects. Both also fail "
            "the count: the EWMA margin is breached on two percent of days, not one, because a normal quantile is too "
            "thin for real tails, and breaches still cluster a little. The fix the industry uses is a fatter-tailed "
            "quantile or filtered historical simulation, and Part 40 returns to it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(side[1]),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1::2]], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(Indicate(bars[3], color=CONST))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[0::2]], lag_ratio=0.08), FadeIn(side[0]),
                      FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: power against realistic failures", r"first-order Markov tests miss breaches that "
                          r"cluster at longer lags; duration-based tests (Christoffersen and Pelletier 2004) and "
                          r"regression tests (Engle and Manganelli 2004) do better, but no test is uniformly most powerful",
                          width=12.4, font_size=18),
            desk_question(r"open: backtesting expected shortfall", r"ES is not elicitable on its own (Gneiting 2011), "
                          r"so it has no consistent scoring function; it is jointly elicitable with VaR (Fissler and "
                          r"Ziegel 2016), and how best to backtest it is still argued", width=12.4, font_size=18),
            desk_question(r"open: estimation error in the test", r"the margin's parameters are estimated, so the "
                          r"breaches are not exactly Bernoulli even under the model (Escanciano and Olmo 2010)",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> First-order Markov tests miss breaches that cluster at longer "
            "lags. Duration tests and regression tests do better, but no test is best against every failure. "
            "<bookmark mark='b'/> Regulators now ask for expected shortfall, the average loss beyond the quantile, "
            "and expected shortfall cannot be scored on its own: it has no consistent scoring function, only one "
            "jointly with the quantile. How best to backtest it is still argued. <bookmark mark='c'/> And the "
            "margin's own parameters are estimated, so even under the model the breaches are not exactly coin flips."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a 1\% margin model has breaches on days 40, 100, 101 and 102 of 250. Compute $\text{LR}_{uc}$ "
                r"and the transition counts $n_{ij}$. Which test, if any, rejects it?")
        q.move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. A one-percent margin model is breached on days forty, one hundred, one hundred and one, "
            "and one hundred and two, out of two hundred and fifty. Compute the count statistic and the transition "
            "counts. Which test, if any, rejects it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
        self.answer()

    def answer(self):
        from explainer.quant.house import funding

        hits = np.zeros(250, dtype=int)
        hits[[39, 99, 100, 101]] = 1
        result = funding.christoffersen(hits, 0.01)
        title = label(r"Same count, different timing", font_size=34, color=QC.IDEA).to_edge(UP, buff=0.35)
        # Magnify the cluster: the quiet days immediately before and after it matter too.
        dots = VGroup(*[Dot(radius=0.10, color=LOSS if day in (100, 101, 102) else GREY_C)
                        for day in range(98, 105)]).arrange(RIGHT, buff=0.65).move_to(UP * 1.9)
        days = VGroup(*[MathTex(str(day), font_size=20).next_to(dot, DOWN, buff=0.12)
                        for day, dot in zip(range(98, 105), dots)])
        zoom = label(r"zoom: days 98--104; the fourth breach is on day 40", font_size=18, color=GREY_A)
        zoom.next_to(dots, UP, buff=0.22)
        count = VGroup(
            label(r"Count: 4 in 250", font_size=25, color=CCP),
            MathTex(rf"\hat p = 0.016,\quad \text{{LR}}_{{uc}} = {result['LR_uc']:.2f}", font_size=27),
            label(r"below 3.84: do not reject at 5\%", font_size=20, color=GAIN),
        ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.3 + DOWN * 0.5)
        timing = VGroup(
            label(r"Timing: 249 transitions", font_size=25, color=CONST),
            MathTex(r"(n_{ij}) = \begin{pmatrix}243 & 2\\2 & 2\end{pmatrix}", font_size=31),
            MathTex(rf"\hat\pi_{{01}} = 2/245,\quad \hat\pi_{{11}} = 2/4", font_size=25),
            MathTex(rf"\text{{LR}}_{{ind}} = {result['LR_ind']:.2f} > 3.84", font_size=27, color=LOSS),
        ).arrange(DOWN, buff=0.20).move_to(RIGHT * 3.2 + DOWN * 0.55)
        caveat = wrapped_label(r"The asymptotic independence test rejects. With only four breaches, use a simulated "
                               r"null distribution to check the small-sample conclusion.", 11.8, 20, GREY_A)
        caveat.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The count is fine: four in two hundred and fifty gives a likelihood ratio of zero point seven seven. "
            "<bookmark mark='a'/> Of two hundred and forty-nine transitions, two enter a breach, two leave one, and "
            "two connect consecutive breaches. The next-day rate jumps from two in two hundred and forty-five to two "
            "in four. <bookmark mark='b'/> Independence rejects: twelve point two exceeds three point eight four. "
            "With four breaches, check against a simulated null distribution."
        ) as vo:
            self.play(FadeIn(title), FadeIn(dots), FadeIn(days), FadeIn(zoom), FadeIn(count))
            vo.wait_until("a")
            self.play(FadeIn(timing[:3]))
            vo.wait_until("b")
            self.play(FadeIn(timing[3]), FadeIn(caveat))
        self.wait(0.5)
        self.clear_scene()
