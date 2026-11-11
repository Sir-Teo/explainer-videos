from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, COST_C, GOOD, GP_C, HURDLE, IC_C, MYO_C, PART, fit_right, load


class Capacity(VoiceoverScene):
    def construct(self):
        g = load("gp")
        self.card()
        self.turnover(g)
        self.optimum()
        self.picture()
        self.berk_green()
        self.fee()
        self.evidence()
        self.question()

    def card(self):
        c = chapter_card(8, r"Decay, capacity and Berk--Green", r"How large should a strategy be, and who keeps the "
                         r"skill?", part=PART)
        with self.voiceover("Chapter eight. A signal's speed sets its turnover, its turnover sets its costs, and its costs "
                            "set how much money it can manage. Then the question is who keeps the profits."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def turnover(self, g):
        ph = g["phi"]
        ts, tf = math.sqrt(2 * ph["slow"]), math.sqrt(2 * ph["fast"])
        rows = [cmath(r"h_t", r"\propto", r"z_t,\qquad \operatorname{Corr}(z_t, z_{t-1}) = 1 - \phi", font_size=34),
                cmath(r"\operatorname{Var}(z_t - z_{t-1})", r"=", r"2(1 - \operatorname{Corr}) = 2\phi", font_size=34),
                cmath(r"\text{RMS score change}", r"=", r"\sqrt{2\phi}", font_size=36),
                cmath(r"\text{calm, reversal}", r":", rf"\sqrt{{2\phi}} = {ts:.2f},\ \ {tf:.2f}", font_size=34)]
        whys = [why(r"holdings proportional to standardised scores whose day-to-day autocorrelation is $1-\phi$"),
                why(r"each day's change in the scores, for unit-variance scores"),
                why(r"absolute turnover has this scaling only with a fixed increment distribution, normalisation and universe"),
                why(r"Chapter 5's empirical persistence proxies do not directly measure book turnover")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            f"""Relate persistence to score changes carefully. <bookmark mark='a'/> For a stationary matched pair of unit-variance scores with correlation one minus phi, <bookmark mark='b'/> the difference has variance two phi. <bookmark mark='c'/> Its root-mean-square change is square root of two phi. Expected absolute change has proportional scaling only with a fixed increment distribution; portfolio turnover also depends on normalisation, universe and drift. <bookmark mark='d'/> The two saved persistence proxies give {ts:.2f} and {tf:.2f}. Their ratio is a score-change illustration, not measured turnover of the two books."""
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def optimum(self):
        rows = [cmath(r"\Pi(A)", r"=", r"g\,A - c\,A^{3/2}", font_size=40, colors={r"c\,A^{3/2}": COST_C}),
                cmath(r"A_0", r"=", r"(g/c)^2", font_size=36, colors={r"A_0": BAD}),
                cmath(r"A^*", r"=", r"\big(\tfrac{2g}{3c}\big)^2 = \tfrac49\,A_0", font_size=36, colors={r"A^*": GOOD}),
                cmath(r"\frac{\Pi(A^*)}{A^*}", r"=", r"\frac{g}{3}", font_size=36)]
        whys = [why(r"dollar profit of a strategy with gross return $g$ per dollar, run at size $A$, with square-root "
                    r"impact: costs per dollar grow like $\sqrt A$"),
                why(r"the break-even size: there the net return is zero"),
                why(r"the size that maximises dollar profit: less than half the break-even size"),
                why(r"at this unconstrained fixed-$g,c$ profit optimum, net return before manager fees is $g/3$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Choose an objective for size. <bookmark mark='a'/> Assume fixed positive gross return g and coefficient c, with dollar profit g A minus c A to the three-halves power, and no other costs, constraints or risk objective. <bookmark mark='b'/> Break-even size is g over c squared. <bookmark mark='c'/> Differentiating dollar profit gives an optimum of four ninths of break-even. <bookmark mark='d'/> Net return there is g over three before manager fees. This identity belongs to this fixed-input model, not a universal definition of capacity."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def picture(self):
        gr, cc = 1.0, 1.0
        A = np.linspace(0, 1.1, 120)
        prof = gr * A - cc * A ** 1.5
        net = gr - cc * np.sqrt(A)
        g = axes([0, 1.1], [-0.25, 1.05], x_length=7.4, y_length=4.4, xlabel=r"size, as a fraction of break-even",
                 ylabel=r"dimensionless normalised values", xticks=[0, 4 / 9, 1], yticks=[0, 1 / 3, 1], xfmt=lambda v: {0: "0", 1: "1"}.get(v, r"4/9"),
                 yfmt=lambda v: {0: "0", 1: "1"}.get(v, r"1/3"), font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_net = curve(ax, A, net, HURDLE, stroke_width=3)
        c_pr = curve(ax, A, prof * 4, GOOD, stroke_width=4)
        star = Dot(ax.c2p(4 / 9, 4 * (4 / 9 - (4 / 9) ** 1.5)), radius=0.08, color=GOOD)
        vline = DashedLine(ax.c2p(4 / 9, -0.25), ax.c2p(4 / 9, 1.0), color=GREY_C, stroke_width=1.5)
        leg = legend([(HURDLE, r"net return divided by $g$"), (GOOD, r"$4\Pi/(g A_0)$")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        fit_right(leg)
        with self.voiceover(
            "The same dimensionless fixed-input toy. <bookmark mark='a'/> Net return divided by g falls as square root of relative size. <bookmark mark='b'/> Profit divided by g times break-even size is multiplied by four for visibility. The full curve, including its negative tail, is shown. Profit peaks at four ninths. A fee contract can change incentives; the next model specifies one rather than assuming every manager wants unlimited assets."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c_net))
            vo.wait_until("b")
            self.play(Create(c_pr), Create(vline), FadeIn(star))
        self.wait(0.4)
        self.clear_scene()

    def berk_green(self):
        rows = [cmath(r"\alpha^{\text{inv}}(q)", r"=", r"a - c(q) - f", font_size=38, colors={r"\alpha^{\text{inv}}(q)": IC_C}),
                cmath(r"\text{flows}", r":", r"q \uparrow\ \text{while}\ \alpha^{\text{inv}} > 0", font_size=34),
                cmath(r"\alpha^{\text{inv}}(q^*)", r"=", r"0\quad\Rightarrow\quad f\,q^* = (a - c(q^*))\,q^*", font_size=34,
                      colors={r"\alpha^{\text{inv}}(q^*)": BAD}),
                cmath(r"\text{past returns}", r"\to", r"\text{beliefs about } a \to \text{flows, not future alpha}",
                      font_size=30)]
        whys = [why(r"Berk and Green (2004): a manager's skill $a$, costs $c(q)$ rising with the assets $q$, and a fee $f$"),
                why(r"rational investors add money as long as the expected net alpha is positive"),
                why(r"in the ideal flow equilibrium, expected risk-adjusted net alpha is zero; fees capture skill rents after trading costs"),
                why(r"so the absence of persistence in fund returns is not evidence that skill is absent")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Berk and Green model rational fund flows with decreasing returns to scale. <bookmark mark='a'/> Expected risk-adjusted alpha before fees is skill minus size-dependent costs. <bookmark mark='b'/> Ideal rational flows expand the fund while expected net alpha is positive. <bookmark mark='c'/> In equilibrium expected net alpha is zero; realised returns and total expected returns need not be zero. Manager fees collect the remaining rent after trading costs. <bookmark mark='d'/> In this model, past returns update beliefs and move assets, so weak return persistence can coexist with skill. This is a model implication, not proof that every observed flow is rational."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def fee(self):
        rows = [cmath(r"\alpha^{\text{inv}}", r"=", r"a - c\sqrt q - f = 0\ \Rightarrow\ q^*(f) = \Big(\frac{a - f}{c}\Big)^2",
                      font_size=32),
                cmath(r"\max_f\ f\,q^*(f)", r":", r"(a - f)^2 - 2f(a - f) = 0\ \Rightarrow\ f^* = \frac a3", font_size=32,
                      colors={r"f^* = \frac a3": GOOD}),
                cmath(r"q^*", r"=", r"\Big(\frac{2a}{3c}\Big)^2 = \tfrac49\,\Big(\frac ac\Big)^2", font_size=34,
                      colors={r"q^*": HURDLE})]
        whys = [why(r"Berk and Green with the square-root law: costs per dollar $c\sqrt q$; investors fund the manager "
                    r"until their alpha is zero"),
                why(r"a manager choosing the fee to maximise revenue charges a third of the skill"),
                why(r"and runs exactly the profit-maximising size of the earlier slide: four ninths of break-even")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Consider a particular known-skill square-root-cost extension. <bookmark mark='a'/> Let skill a and c be positive and restrict the fee between zero and a. The zero-expected-net-alpha flow condition determines size. <bookmark mark='b'/> Maximising fee revenue gives a divided by three. <bookmark mark='c'/> The resulting size is four ninths of the no-fee break-even size, matching the earlier profit optimum under these assumptions. Other technologies, uncertainty or contracts need not give the same fee or size."
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

    def evidence(self):
        cards = VGroup(
            desk_question(r"skill in dollars", r"Berk and van Binsbergen (2015): value added and persistence in their fund sample, conditional on their benchmarks and assumptions", width=12.4, font_size=19),
            desk_question(r"why the best funds close", r"capacity incentives can contribute; fund closures also have operational, contractual and other causes", width=12.4, font_size=19),
            desk_question(r"the House's rule", r"report size sensitivity, cost assumptions and the chosen capacity objective; $g/3$ is a fixed-input illustration", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Empirical evidence is more qualified. <bookmark mark='a'/> Berk and van Binsbergen report value-added patterns in their fund sample; those measurements depend on their benchmark and assumptions. <bookmark mark='b'/> Capacity incentives are one possible reason to restrict outside money, not an identified explanation of every closure. <bookmark mark='c'/> A desk should state the capacity objective and show sensitivity to costs and size. The one-third-edge rule is the preceding toy's result, not a general capital-allocation rule."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a strategy breaks even at \$900 million. At what size does it make the most money, and what is "
                       r"its net return there, as a share of the gross?")
        with self.voiceover(
            "Pause and predict. A strategy breaks even at nine hundred million dollars. At what size does it make the "
            "most money, and what share of its gross return do investors keep there?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
