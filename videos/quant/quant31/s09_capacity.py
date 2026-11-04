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
                cmath(r"\text{turnover}", r"\propto", r"\sqrt{2\phi}", font_size=40, colors={r"\text{turnover}": COST_C}),
                cmath(r"\text{calm, reversal}", r":", rf"\sqrt{{2\phi}} = {ts:.2f},\ \ {tf:.2f}", font_size=34)]
        whys = [why(r"holdings proportional to standardised scores whose day-to-day autocorrelation is $1-\phi$"),
                why(r"each day's change in the scores, for unit-variance scores"),
                why(r"so the book's turnover grows with the square root of the signal's decay rate"),
                why(r"Chapter 5's two signals: the fast one trades four times as much as the slow one, for every dollar")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Decay and turnover first. <bookmark mark='a'/> Hold positions in proportion to scores whose day-to-day "
            "correlation is one minus phi. <bookmark mark='b'/> The change in the scores each day has variance two phi. "
            "<bookmark mark='c'/> So turnover grows with the square root of the decay rate. <bookmark mark='d'/> For "
            f"Chapter five's two signals, {ts:.2f} against {tf:.2f}: the reversal book trades about four times as much "
            "per dollar as the calm book, and under the square-root law it pays more than four times as much."
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
                why(r"at that size, investors earn a third of the gross return; the other two thirds pay for the trading")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "How large should a strategy be? <bookmark mark='a'/> A gross return g per dollar, at size A, with "
            "square-root impact: costs per dollar grow like the square root of size, so dollar costs grow like A to "
            "the three halves. <bookmark mark='b'/> The net return reaches zero at the break-even size, g over c, "
            "squared. <bookmark mark='c'/> Dollar profit peaks earlier: at four ninths of the break-even size. "
            "<bookmark mark='d'/> And there, the return per dollar is a third of the gross. Capacity is not the size at "
            "which a strategy stops working; it is a choice about how much of the edge to give to the market."
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
        g = axes([0, 1.1], [-0.2, 1.05], x_length=7.4, y_length=4.4, xlabel=r"size, as a fraction of break-even",
                 ylabel=r"per unit", xticks=[0, 4 / 9, 1], yticks=[0, 1 / 3, 1], xfmt=lambda v: {0: "0", 1: "1"}.get(v, r"4/9"),
                 yfmt=lambda v: {0: "0", 1: "g"}.get(v, r"g/3"), font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_net = curve(ax, A, net, HURDLE, stroke_width=3)
        c_pr = curve(ax, A, prof * 4, GOOD, stroke_width=4)
        star = Dot(ax.c2p(4 / 9, 4 * (4 / 9 - (4 / 9) ** 1.5)), radius=0.08, color=GOOD)
        vline = DashedLine(ax.c2p(4 / 9, -0.2), ax.c2p(4 / 9, 1.0), color=GREY_C, stroke_width=1.5)
        leg = legend([(HURDLE, r"net return per dollar"), (GOOD, r"dollar profit (scaled)")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        fit_right(leg)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> The net return per dollar falls from g, as the square root of size, and "
            "reaches zero at break-even. <bookmark mark='b'/> Dollar profit rises, peaks at four ninths, and falls back. "
            "A manager paid on assets wants to sit to the right of the peak; investors want the left. The tension "
            "between them is the next model."
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
                why(r"in equilibrium investors earn zero alpha; the manager collects the rent of the skill as fees on a "
                    r"larger fund"),
                why(r"so the absence of persistence in fund returns is not evidence that skill is absent")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Jonathan Berk and Richard Green wrote the model in 2004. <bookmark mark='a'/> A manager has skill a; costs "
            "rise with the size of the fund; the fee is f. Investors earn a minus costs minus fees. "
            "<bookmark mark='b'/> Rational investors keep adding money as long as that is positive. "
            "<bookmark mark='c'/> So in equilibrium they earn nothing above the benchmark, and the manager collects the "
            "whole value of the skill, as fees on a larger fund. <bookmark mark='d'/> Past returns move money, not future "
            "alpha. The famous lack of persistence in fund returns is what a world with skill and capacity predicts."
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
            "Put the square-root law into Berk and Green. <bookmark mark='a'/> Investors fund the manager until their "
            "alpha is zero, which fixes the fund's size for any fee. <bookmark mark='b'/> A manager who sets the fee to "
            "maximise revenue charges a third of the skill. <bookmark mark='c'/> And the fund then runs at exactly four "
            "ninths of its break-even size, the profit-maximising size from before. The manager who owns the strategy "
            "and the manager who sells it arrive at the same size; they differ only in who keeps the third."
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
            desk_question(r"skill in dollars", r"Berk and van Binsbergen (2015): measure value added as alpha times "
                          r"size; the average manager adds value, and the ranking persists, while investors' alphas are "
                          r"near zero", width=12.4, font_size=19),
            desk_question(r"why the best funds close", r"a manager who owns the strategy, not the fees, stops at the "
                          r"profit-maximising size, and returns outside money", width=12.4, font_size=19),
            desk_question(r"the House's rule", r"report each strategy's capacity at a third of its gross edge, from its "
                          r"measured turnover and the square-root law, before it is given capital", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The evidence. <bookmark mark='a'/> Jonathan Berk and Jules van Binsbergen measured skill as value added in "
            "dollars, alpha times size, and found that the average manager does add value and that the ranking "
            "persists, while investors' alphas are near zero, as the model predicts. <bookmark mark='b'/> It also "
            "explains why some of the most successful funds close to outside money: an owner of the strategy wants the "
            "profit-maximising size, not the largest. <bookmark mark='c'/> The House's rule: every strategy reports its "
            "capacity, from its measured turnover and the square-root law, before it gets capital."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
