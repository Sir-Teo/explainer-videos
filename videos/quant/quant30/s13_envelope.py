"""Evaluation protocol and fixed arithmetic; never load the strategy experiment."""
from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant30.common import PART, comma


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.accounting()
        self.fixed_weights()
        self.drift()
        self.costs()
        self.inference()
        self.question()

    def card(self):
        c = chapter_card(12, r"Evaluating portfolio rules", r"What must be fixed before a future comparison means anything?", part=PART)
        with self.voiceover("Chapter twelve. Evaluation protocol and fixed arithmetic. This chapter uses no sealed strategy result. A portfolio comparison needs a complete information, allocation, execution and reporting policy before its performance can be interpreted."):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.clear_scene()

    def protocol(self):
        cards = VGroup(
            desk_question(r"freeze the entire procedure", r"data vintage, membership, release time, estimation window, preprocessing, covariance and mean estimators, constraints, solver, hyperparameters and stopping", width=12.2, font_size=19),
            desk_question(r"specify attainable trades", r"decision and fill times, drifted holdings, leverage, cash, financing, borrow, fees, impact and unavailable prices", width=12.2, font_size=19),
            desk_question(r"pre-specify the comparison", r"benchmark, risk goal, horizon, dependence-aware inference, multiplicity, reporting and what a subsequent revision counts as", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Freeze more than a covariance formula. <bookmark mark='a'/> Fix data timing, preprocessing, estimation, constraints and tuning. <bookmark mark='b'/> Define trades from actual drifted holdings, with cash, financing and costs. <bookmark mark='c'/> State the benchmark, risk goal and inferential policy. Equal weights, minimum variance and HRP answer different objectives; a single Sharpe ranking does not resolve all of them.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def accounting(self):
        before, after = pit.trials_upto(29), pit.trials_upto(30)
        card = VGroup(label(r"Existing registration metadata", font_size=30),
                      MathTex(rf"{comma(before)} + {after-before} = {comma(after)}", font_size=38, color=QC.HOUSE),
                      wrapped_label(r"Bookkeeping of prior registrations; no new trial, opening, strategy score or statistical verdict", 11.0, 21, GREY_A)).arrange(DOWN, buff=0.4)
        with self.voiceover(f"Existing metadata counts {before:,} registrations through Part twenty-nine and {after:,} through Part thirty, an increment of {after-before}. These are historical bookkeeping totals, not independent statistical tests. Restoring ordinary calculations creates no new registration. The strategy experiment remains excluded; no performance, significance or power conclusion is supplied."):
            self.play(FadeIn(card))
        self.clear_scene()

    def fixed_weights(self):
        v_gmv, v_ew, v_erc = math.sqrt(.008), math.sqrt(.0125), math.sqrt(2 * (.1 * 2/3)**2)
        head = MathTex(r"\Sigma=\operatorname{diag}(0.1^2,0.2^2),\quad \rho=0", font_size=32).to_edge(UP, buff=.45)
        # portfolio volatility against the weight in the calmer asset: one curve, three named points on it
        g = axes([0, 1], [8, 20.5], x_length=6.4, y_length=3.7, xticks=[0, .25, .5, .75, 1], yticks=[10, 15, 20],
                 yfmt=lambda v: rf"{v:g}\%", xlabel=r"weight in the 10\% asset", font_size=18).move_to(LEFT * 2.9 + DOWN * .25)
        ax = g.ax
        w = np.linspace(0, 1, 101)
        vol = 100 * np.sqrt((w * .1) ** 2 + ((1 - w) * .2) ** 2)
        line = curve(ax, w, vol, QC.SPOT, stroke_width=4)
        pts = [(.8, 100 * v_gmv, QC.GAIN), (2 / 3, 100 * v_erc, QC.P), (.5, 100 * v_ew, QC.OPTION)]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=.09, color=c) for x, y, c in pts])
        drops = VGroup(*[DashedLine(ax.c2p(x, 8), ax.c2p(x, y), color=c, stroke_width=2, dash_length=.07) for x, y, c in pts])
        rows = VGroup(
            MathTex(rf"w_{{\rm GMV}}=(0.8,0.2),\quad \sigma_{{\rm GMV}}={100*v_gmv:.3f}\%", font_size=28, color=QC.GAIN),
            MathTex(rf"w_{{\rm ERC}}=(2/3,1/3),\quad \sigma_{{\rm ERC}}={100*v_erc:.3f}\%", font_size=28, color=QC.P),
            MathTex(rf"w_{{1/N}}=(0.5,0.5),\quad \sigma_{{1/N}}={100*v_ew:.3f}\%", font_size=28, color=QC.OPTION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.45).next_to(g, RIGHT, buff=.6).shift(UP * .3)
        foot = wrapped_label(r"Fixed chosen annual covariance, known exactly; no assets, historical sample or expected-return comparison", 11.2, 19, GREY_A).to_edge(DOWN, buff=.35)
        with self.voiceover(f"A fixed two-asset covariance toy. <bookmark mark='a'/> Choose uncorrelated annual volatilities ten and twenty percent, known exactly. Minimum variance gives eighty and twenty percent weights and volatility {100*v_gmv:.3f} percent. <bookmark mark='b'/> Equal risk contributions give two thirds and one third, with {100*v_erc:.3f} percent volatility. Equal money gives {100*v_ew:.3f} percent. This shows that equal money, equal risk and minimum variance differ; it does not compare returns or estimation performance.") as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(foot))
            self.play(Create(line), run_time=2)
            vo.wait_until("a")
            self.play(Create(drops[0]), FadeIn(dots[0], scale=1.6), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(drops[1]), FadeIn(dots[1], scale=1.6), FadeIn(rows[1]))
            self.play(Create(drops[2]), FadeIn(dots[2], scale=1.6), FadeIn(rows[2]))
        self.clear_scene()

    def drift(self):
        rows = VGroup(
            MathTex(r"w_0=(1/2,1/2),\quad r=(10\%,0),\quad V_0=1", font_size=32),
            MathTex(r"V^-=(0.55,0.50),\quad V^-_{\rm total}=1.05", font_size=32),
            MathTex(r"w^-=(11/21,10/21)\ne(1/2,1/2)", font_size=32),
            MathTex(r"\text{target-weight change}=0,\quad \text{sell }0.025,\ \text{buy }0.025", font_size=28),
            wrapped_label(r"Fixed one-period simple-return toy; rebalance trades are before fees, measured in initial-dollar units", 11.2, 19, GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover("A second fixed toy shows why target-weight turnover misses trades. <bookmark mark='a'/> Start with half a dollar in each asset. Choose a ten-percent return for the first and zero for the second. Values become fifty-five and fifty cents, so pretrade weights are eleven twenty-firsts and ten twenty-firsts. <bookmark mark='b'/> To return to equal weights before fees, sell two and a half cents of the first and buy the same amount of the second. The target never changed, but trading was required.") as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[-1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def costs(self):
        traded, rate = .05, .0005
        cost_bp = traded * rate * 10000
        card = VGroup(MathTex(r"\text{gross traded}=0.025+0.025=0.05", font_size=32),
                      MathTex(rf"\text{{fee}}=0.05\times5\ \text{{bp}}={cost_bp:.2f}\ \text{{bp of initial wealth}}", font_size=30),
                      wrapped_label(r"Fixed fee arithmetic only; fees paid separately. Financing, slippage, impact and a self-financing post-fee rebalance are not modelled", 11.2, 20, GREY_A)).arrange(DOWN, buff=0.5)
        with self.voiceover(f"Under a chosen five-basis-point fee per dollar traded, five cents of gross trades cost {cost_bp:.2f} basis points of initial wealth. The fee denominator is traded dollars; the reported cost denominator is initial wealth. This arithmetic pays fees separately and does not solve a self-financing post-fee rebalance. It supplies no historical net performance or complete implementation model."):
            self.play(FadeIn(card))
        self.clear_scene()

    def inference(self):
        cards = VGroup(
            desk_question(r"compare paired outcomes", r"use common periods and denominators, account for serial dependence and overlapping training windows, and define the loss before selection", width=12.2, font_size=19),
            desk_question(r"separate uncertainty from a verdict", r"a noisy difference can be consistent with several economically different effects; lack of rejection does not establish equivalence", width=12.2, font_size=19),
            desk_question(r"keep the audit trail", r"retain every candidate, data vintage, failed run and revision; one fresh period alone does not fix leakage, selection, costs or low power", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Inference needs a defined comparison. <bookmark mark='a'/> Use paired observations and a method appropriate to dependence and the selected loss. <bookmark mark='b'/> A wide uncertainty interval is not proof of equality, and a variance objective is not an expected-return objective. <bookmark mark='c'/> Preserve selection and revision history. No test statistic or strategy verdict is computed in this chapter.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        card = pause_card(r"A fixed 1/N target has zero target-weight changes. Why can maintaining it still require trading?")
        with self.voiceover("Pause and predict. Why can an unchanged equal-weight target still require trades, and which denominator converts a per-dollar-traded fee into portfolio cost?"):
            self.play(FadeIn(card))
        self.clear_scene()
