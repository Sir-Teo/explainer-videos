from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, fit_right, load


class DeepSDF(VoiceoverScene):
    def construct(self):
        s = load("sdf")
        self.card()
        self.moments()
        self.tangency()
        self.game()
        self.result(s)
        self.diagnosis(s)
        self.question()

    def card(self):
        c = chapter_card(8, r"Deep SDFs with adversarial moments", r"Can a network learn the discount factor that "
                         r"prices every coin?", part=PART)
        with self.voiceover('Chapter eight. Learn a restricted return-span discount-factor projection, and distinguish its training objective from a positive arbitrage-free pricing certificate.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def moments(self):
        rows = [cmath(r"\mathbb E_t\big[M_{t+1} R^e_{i,t+1}\big]", r"=", r"0\quad \text{for every asset } i", font_size=32,
                      colors={r"\mathbb E_t\big[M_{t+1} R^e_{i,t+1}\big]": HURDLE}),
                cmath(r"M_{t+1}", r"=", r"1 - \textstyle\sum_i w(z_{i,t})\, R^e_{i,t+1}", font_size=32,
                      colors={r"M_{t+1}": NET}),
                cmath(r"\mathbb E\big[M_{t+1} R^e_{i,t+1}\, g(\mathcal I_t)\big]", r"=", r"0\quad \text{for every function } g",
                      font_size=32, colors={r"\mathbb E\big[M_{t+1} R^e_{i,t+1}\, g(\mathcal I_t)\big]": HURDLE})]
        whys = [why('Ideal conditional pricing under suitable no-arbitrage assumptions. The linear return-span projection below can be negative and need not satisfy all conditions.'),
                why(r"the SDF as a portfolio: its weights a network of each coin's characteristics (Chen, Pelger and Zhu "
                    r"2024)"),
                why(r"a conditional expectation is zero exactly when the unconditional one is zero against every function "
                    r"of the conditioning information: infinitely many moment conditions")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "The ideal pricing condition and the fitted approximation differ. <bookmark mark='a'/> Under suitable no-arbitrage conditions, a positive stochastic discount factor prices excess returns. <bookmark mark='b'/> A linear return-span projection of the form one minus portfolio return can satisfy unconditional moments while taking negative values; positivity is not imposed here. <bookmark mark='c'/> Conditional moments are equivalent to suitable unconditional tests against all measurable conditioning functions. A finite adversarial function class only checks selected moments, not all functions and every asset's pricing error."
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

    def tangency(self):
        rows = [cmath(r"\mathbb E[MR^e]", r"=", r"0\ \Rightarrow\ \mu = \mathbb E[R^e R^{e\top}]\,w", font_size=32,
                      colors={r"\mathbb E[MR^e]": HURDLE}),
                cmath(r"w", r"=", r"(\Sigma + \mu\mu^{\top})^{-1}\mu = \frac{\Sigma^{-1}\mu}{1 + \mu^{\top}\Sigma^{-1}\mu}",
                      font_size=32, colors={r"w": NET}),
                cmath(r"\frac{\sigma(M)}{\mathbb E[M]}", r"\ge", r"\max_p |SR_p| = \sqrt{\mu^{\top}\Sigma^{-1}\mu}",
                      font_size=32, colors={r"\frac{\sigma(M)}{\mathbb E[M]}": GOOD})]
        whys = [why(r"substitute $M = 1 - w^{\top}R^e$: the pricing conditions are linear in $w$"),
                why('Canonical unconditional projection: positive-definite covariance and unrestricted weights. Network constraints and conditional weighting change the optimisation.'),
                why('Hansen--Jagannathan uses standard deviation divided by positive mean. A single learned portfolio Sharpe is not a certificate of all pricing conditions.')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "State an unconditional finite-moment calculation with positive-definite return covariance. <bookmark mark='a'/> Substitution gives mean returns equal to the return second-moment matrix times the weights. <bookmark mark='b'/> Sherman--Morrison gives covariance-inverse mean divided by one plus squared tangency Sharpe. These are canonical unrestricted projection weights; network and normalisation constraints change the problem. <bookmark mark='c'/> The Hansen--Jagannathan bound uses discount-factor standard deviation divided by its positive mean. A learned portfolio's Sharpe alone cannot certify positivity, all conditional moments or maximum-Sharpe optimality."
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

    def game(self):
        eq = MathTex(r"\min_{w}\ \max_{g}\ \sum_{j}\Big(\tfrac1T\textstyle\sum_t \tfrac{1}{N_t}\sum_i M_{t+1}\, R^e_{i,t+1}\, "
                     r"g_j(z_{i,t})\Big)^2", font_size=34).to_edge(UP, buff=0.5)
        w_box = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.15, stroke_color=NET, fill_color=NET,
                                        fill_opacity=0.15),
                       Tex(r"SDF network $w(z)$\\prices the moments", font_size=24)).move_to(LEFT * 3.2 + DOWN * 0.3)
        w_box[1].move_to(w_box[0])
        g_box = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.15, stroke_color=BAD, fill_color=BAD,
                                        fill_opacity=0.15),
                       Tex(r"adversary $g(z)$\\finds the worst-priced\\test portfolios", font_size=24)).move_to(
            RIGHT * 3.2 + DOWN * 0.3)
        g_box[1].move_to(g_box[0])
        a1 = CurvedArrow(w_box.get_top() + RIGHT * 0.6, g_box.get_top() + LEFT * 0.6, angle=-TAU / 6, color=GREY_B)
        a2 = CurvedArrow(g_box.get_bottom() + LEFT * 0.6, w_box.get_bottom() + RIGHT * 0.6, angle=-TAU / 6, color=GREY_B)
        foot = wrapped_label('Finite pooled moments; L1-normalised portfolio weights; constant plus four learned test channels; three alternating rounds. No individual-moment, positivity or convergence certificate.', 12.0, 23, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House implementation uses a finite adversarial game. <bookmark mark='a'/> Its portfolio weights are normalised by their absolute sum. It averages moments across assets within each week and then across weeks, using winsorised log-return training targets. <bookmark mark='b'/> The adversary supplies a finite function family plus a constant channel over three alternating rounds. That channel adds a pooled unconditional target; it does not enforce each individual asset moment. No positivity, convergence or exact pricing certificate follows from this finite objective."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(w_box))
            vo.wait_until("b")
            self.play(FadeIn(g_box), Create(a1), Create(a2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def result(self, s):
        weeks = np.asarray(s["weeks"])
        n = len(weeks)
        ca, cl = np.asarray(s["cum_adv"]), np.asarray(s["cum_lin"])
        lo, hi = min(ca.min(), cl.min(), 0) - 0.1, max(ca.max(), cl.max(), 0.2) + 0.1
        g = axes([0, n - 1], [lo, hi], x_length=7.6, y_length=4.0, xlabel=r"week of 2020",
                 ylabel=r"cumulative return of the SDF portfolio (sum of weekly)", xticks=[0,(n-1)//2,n-1], yticks=list(np.linspace(lo,hi,5)), yfmt=lambda v:f"{v:.2f}", font_size=17).move_to(
            LEFT * 1.8 + DOWN * 0.3)
        ax = g.ax
        la = curve(ax, np.arange(n), ca, NET, stroke_width=3)
        ll = curve(ax, np.arange(n), cl, LINEAR, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n - 1, 0), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{adversarial}}:\ SR = {s['sr_adv']:.2f}", font_size=24, color=NET),
            MathTex(rf"\text{{linear SDF}}:\ SR = {s['sr_lin']:.2f}", font_size=24, color=LINEAR),
            MathTex(rf"\text{{holding every coin}}:\ SR = {s['sr_ew']:.2f}", font_size=24, color=MKT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(side)
        with self.voiceover(
            f"The saved evaluation reports gross simple-return portfolios, although training uses winsorised log-return targets. <bookmark mark='a'/> The linear managed-portfolio comparator has Sharpe {s['sr_lin']:.3f}. <bookmark mark='b'/> The adversarial portfolio has {s['sr_adv']:.3f}, compared with {s['sr_ew']:.3f} for the equal-weight market. Different constraints and parameterisations prevent interpreting this as an isolated architecture ablation. Costs and short feasibility remain unmodelled."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(ll), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(side[0]), FadeIn(side[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def diagnosis(self, s):
        rows = VGroup(
            MathTex(rf"\text{{the coin market, 2018--19}}:\ {100 * s['train_mkt']:.0f}\%\ \text{{a year}}", font_size=30,
                    color=BAD),
            MathTex(rf"\text{{the coin market, 2020}}:\ +{100 * s['test_mkt']:.0f}\%\ \text{{a year}}", font_size=30,
                    color=GOOD),
            MathTex(rf"\operatorname{{corr}}(\text{{SDF portfolio}},\ \text{{market}})_{{2020}} = {s['corr_mkt_adv']:.3f}",
                    font_size=30, color=NET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.9)
        lesson = wrapped_label('The observed market correlation diagnoses exposure. It does not prove exact training pricing, an identified premia mechanism, positivity or global optimality.', 11.4, 25,
                               QC.HOUSE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"A descriptive exposure diagnostic helps interpret the saved path. <bookmark mark='a'/> Annualised arithmetic market means are {100*s['train_mkt']:.1f} percent in the training-era sample and {100*s['test_mkt']:.1f} percent in the later research sample. These are not compounded annual returns. <bookmark mark='b'/> The adversarial portfolio's market correlation is {s['corr_mkt_adv']:.3f}. <bookmark mark='c'/> This can diagnose substantial signed market exposure, but does not establish why optimisation chose it, exact training-moment pricing, or a uniquely identified premia mechanism. A richer exposure analysis and matched restrictions would be needed for causal conclusions."
        ) as vo:
            self.add(rows[0],rows[1])
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask('Propose an explicit market-exposure bound for a learned discount-factor portfolio. What estimation and normalisation does it require, what opportunities does it exclude, and what does it fail to certify?')
        with self.voiceover(
            'Pause and predict. Propose an explicit market-exposure bound for a learned discount-factor portfolio. State the estimation and normalisation choices, the opportunities it excludes, and why the bound does not certify every pricing moment.'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
