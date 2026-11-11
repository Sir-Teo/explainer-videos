from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import (
    BAD,
    ES_C,
    GOOD,
    HURDLE,
    PART,
    TAIL_C,
    VAR_C,
    load,
)

NAMES = {"normal": r"normal, 500 days", "hs": r"historical simulation", "ewma": r"RiskMetrics (EWMA)",
         "fhs": r"filtered HS (EWMA)", "gjr_fhs": r"filtered HS (GJR-GARCH)", "evt": r"GJR + EVT"}


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        self.card()
        self.scores()
        self.pinball_lemma()
        self.osband()
        self.es_not()
        self.check_level(r)
        self.ru()
        self.fz()
        self.fz_proof()
        self.check_grid(r)
        self.check_rank(r)
        self.check_power(r)
        self.comparative()
        self.expectiles()
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"What can be backtested?", r"Which risk measures can be checked against outcomes, and how?",
                          part=PART)
        with self.voiceover('For the researcher: scoring, calibration and backtesting are different tasks. A quantile with a unique appropriate cutoff is elicitable; integrated-tail ES is not elicitable alone on a rich convex distribution class, while the VaR--ES pair is jointly elicitable under stated conditions. Non-elicitability does not prohibit model-verification tests. We prove the convex-level-set obstruction, derive score derivatives, and distinguish illustrative numerical evidence from a proof or a fully past-measurable historical forecast.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def scores(self):
        rows = [cmath(r"S(x, y)", r":", r"\text{the score of forecast } x \text{ when } y \text{ happens}", font_size=36),
                cmath(r"\mathbb E_F\,S(T(F), Y)", r"\le", r"\mathbb E_F\,S(x, Y)\quad \forall x", font_size=38,
                      colors={r"\le": HURDLE}),
                cmath(r"T \text{ elicitable}", r"\iff", r"\exists\ S \text{ strictly consistent for } T", font_size=36,
                      colors={r"T \text{ elicitable}": VAR_C})]
        whys = [why(r"a scoring function: lower is better, one number per day"),
                why(r"consistency: under the true distribution, the true value of the functional $T$ scores best on "
                    r"average; strictly, if nothing else ties"),
                why(r"Gneiting (2011): a functional is elicitable if some score makes it the unique best forecast; then "
                    r"forecasters can be ranked by their average scores")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A scoring function maps a point forecast and outcome to a loss, with lower better. <bookmark mark='a'/> Fix both a distribution class and an action domain, and require the expected scores used in the comparison to exist. <bookmark mark='b'/> Consistency means the target minimizes expected loss; strict consistency requires the minimizer to be unique on that class. <bookmark mark='c'/> Elicitability supports truthful score-based forecast comparison. It does not say that other model-verification tests are impossible, that every consistent score gives the same finite-sample ranking, or that a score alone establishes calibration."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def pinball_lemma(self):
        rows = [cmath(r"\mathbb E\,\ell_\tau(q, Y)", r"=", r"\int (\mathbf 1\{y < q\} - \tau)(q - y)\,dF(y)", font_size=38),
                cmath(r"\frac{\partial}{\partial q}", r"=", r"F(q) - \tau", font_size=42, colors={r"F(q) - \tau": VAR_C}),
                cmath(r"\Rightarrow", r"\ ", r"q^* = F^{-1}(\tau),\ \text{a minimum (convex)}", font_size=38)]
        whys = [why(r"the expected pinball loss of a quantile forecast $q$"),
                why('at continuity points slope is F(q)-tau; at atoms use left/right derivatives and the quantile set'),
                why('so the expected loss is convex in $q$ and minimized on the tau-quantile set; uniqueness is needed for a strictly consistent point target')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The pinball expectation is convex in q when the first moment is finite. <bookmark mark='a'/> At a continuous point its derivative is F of q minus tau. <bookmark mark='b'/> At an atom the left and right derivatives are F of q-minus minus tau and F of q minus tau. The minimizing condition is that tau lies between those two probabilities. <bookmark mark='c'/> A unique quantile gives strict consistency on the chosen class; otherwise the score elicits the quantile set. This statement avoids assuming every generalized quantile is a unique zero of a smooth derivative."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def osband(self):
        rows = [cmath(r"T(F_0) = T(F_1) = t", r"\Rightarrow", r"T\bigl(\lambda F_1 + (1 - \lambda)F_0\bigr) = t", font_size=36,
                      colors={r"\Rightarrow": HURDLE}),
                cmath(r"\mathbb E_{F_\lambda}S(x, Y)", r"=", r"\lambda\,\mathbb E_{F_1}S(x, Y) + (1 - \lambda)\,\mathbb E_{F_0}S(x, Y)",
                      font_size=34),
                cmath(r"", r"\ge", r"\lambda\,\mathbb E_{F_1}S(t, Y) + (1 - \lambda)\,\mathbb E_{F_0}S(t, Y) = \mathbb E_{F_\lambda}S(t, Y)",
                      font_size=32)]
        whys = [why(r"Lemma two (Osband 1985): an elicitable functional has convex level sets"),
                why(r"proof: an expected score under a mixture is the mixture of the expected scores"),
                why(r"each is minimised at $t$, so their mixture is too; strict consistency makes $t$ the unique minimiser, "
                    r"so $T(F_\lambda) = t$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Lemma two, a necessary condition due to Kent Osband. <bookmark mark='a'/> If two distributions have the same "
            "value of an elicitable functional, so does every mixture of them. <bookmark mark='b'/> The proof: an "
            "expected score under a mixture is the mixture of the expected scores. <bookmark mark='c'/> Each is minimised "
            "at t, so their mixture is too, and strict consistency makes t the only minimiser. Elicitable functionals "
            "have convex level sets."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def es_not(self):
        st = VGroup(MathTex(r"F_0 = \delta_1,\quad F_1 = 0.95\,\delta_0 + 0.05\,\delta_2,\quad \alpha = 90\%", font_size=32),
                    MathTex(r"\text{ES}(F_0) = \text{ES}(F_1) = 1,\qquad \text{ES}\bigl(\tfrac12 F_0 + \tfrac12 F_1\bigr) = 1.25",
                            font_size=32),
                    wrapped_label("expected shortfall's level sets are not convex, so by Lemma 2 no strictly consistent scalar ES score on a convex class containing these distributions; this does not prohibit calibration backtests",
                                  9.8, 20)).arrange(DOWN, buff=0.3)
        card = theorem_card(r"Expected shortfall is not elicitable (Gneiting 2011)", st, r"this part's counterexample",
                            width=11.8, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> Take a sure loss of one, and a loss of two with probability five percent, "
            "nothing otherwise. At ninety percent both have an expected shortfall of exactly one. <bookmark mark='b'/> "
            "Mix them half and half: the worst ten percent now holds two and a half percent of twos and seven and a half "
            "of ones, a shortfall of one and a quarter. The level set is not convex, so by lemma two no score of any form "
            "elicits expected shortfall."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=BAD, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def check_level(self, r):
        mv, me = r["mixV"], r["mixE"]
        hx = [-3.4, -0.4, 2.0, 4.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"", r"$F_0$", r"$F_1$", r"mixture")])
        rows = [(r"VaR, first pair (99\%)", mv["var"], VAR_C), (r"ES, second pair (90\%)", me["es"], ES_C)]
        tab = VGroup(head)
        for nm, vals, col in rows:
            tab.add(VGroup(label(nm, font_size=18, color=col), *[MathTex(f"{v:.2f}", font_size=28) for v in vals]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 1.0 * j, 0])
        foot = wrapped_label(r"computed by the House's \texttt{mixture\_var\_es}, splitting the atom at the quantile as "
                             r"Acerbi and Tasche prescribe", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Check one: the level sets, computed. <bookmark mark='a'/> Two distributions with the same ninety-nine "
            f"percent VaR, {mv['var'][0]:.0f}, and their mixture: the same VaR again. <bookmark mark='b'/> The theorem's "
            f"pair, with the same shortfall, {me['es'][0]:.2f}, and their mixture: {me['es'][2]:.2f}."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), Indicate(tab[2][3], color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def ru(self):
        rows = [cmath(r"\text{ES}_\alpha(L)", r"=", r"\min_v \Bigl\{v + \tfrac{1}{1 - \alpha}\,\mathbb E(L - v)^+\Bigr\}", font_size=38,
                      colors={r"\text{ES}_\alpha(L)": ES_C}),
                cmath(r"\frac{\partial}{\partial v}", r"=", r"1 - \frac{P(L > v)}{1 - \alpha} = 0 \iff v = \text{VaR}_\alpha", font_size=36,
                      colors={r"v = \text{VaR}_\alpha": VAR_C})]
        whys = [why(r"Rockafellar and Uryasev (2000), Part 30's CVaR optimisation: ES is the minimum of a function whose "
                    r"minimiser is VaR"),
                why(r"so ES is a second-order quantity of the quantile: it is not elicitable alone, but it may be "
                    r"together with VaR")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Rockafellar and Uryasev give a variational representation for integrable losses: minimize v plus expected positive excess above v divided by one minus alpha. <bookmark mark='a'/> At continuity points its derivative is one minus the exceedance probability divided by the tail mass. <bookmark mark='b'/> With atoms, the subgradient condition is F of v-minus at most alpha at most F of v. The minimum value is integrated-tail ES, and the minimizers form the quantile set. This representation does not make the minimum value elicitable alone; it motivates adding the quantile as another action."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def fz(self):
        st = VGroup(MathTex(r"S(v, e; r) = -\frac{\mathbf 1\{r \le v\}(v - r)}{\tau\,e} + \frac{v}{e} + \log(-e) - 1,\qquad e < v < 0",
                            font_size=30),
                    wrapped_label(r"for the return quantile $v$ and shortfall $e$ at level $\tau$ (both negative), this "
                                  r"score is strictly consistent for the pair: (VaR, ES) is jointly elicitable, though ES "
                                  r"alone is not", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Fissler and Ziegel (2016); the FZ0 form of Patton, Ziegel and Chen (2019)", st,
                            r"stated; checked numerically below", width=11.8, font_size=21)
        with self.voiceover(
            "Fissler and Ziegel characterize strictly consistent scores for the pair under suitable distribution and action-domain conditions. <bookmark mark='a'/> This FZ-zero version uses lower-tail return quantile v and ES e on the domain e less than v less than zero. Assume a unique continuous tau quantile, finite first moment, negative true ES, and finite expected score. <bookmark mark='b'/> Rescaling all returns and forecasts by a positive constant adds log of that constant to FZ zero. Score differences are unchanged, but the score level itself is not literally unit free. Joint scoring does not remove model uncertainty or guarantee identical rankings across every consistent score."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.02))
        self.wait(0.5)
        self.clear_scene()

    def fz_proof(self):
        rows=[
            cmath(r"\partial_v\mathbb E S(v,e;R)",r"=",r"\frac{F(v)-\tau}{-\tau e}",font_size=38),
            cmath(r"A(v)",r"=",r"v-\tau^{-1}\mathbb E(v-R)^+",font_size=37),
            cmath(r"\partial_e\mathbb E S(v,e;R)",r"=",r"\frac{e-A(v)}{e^2}",font_size=38),
            cmath(r"v=q_\tau,\quad A(v)=e_\tau",r"\Rightarrow",r"(v,e)=(q_\tau,e_\tau)",font_size=34),
        ]
        whys=[why(r"continuous unique quantile, finite first moment, e<0: sign is F(v)-tau"),
              why(r"at the true continuous cutoff, A is the lower-tail ES"),
              why('at $v=q$, derivative changes from negative to positive at $e=e_\\tau$'),
              why(r"first minimize v at fixed e, then e at v=q; pair in the stated action domain")]
        step=ladder(self,rows,whys,keep=4,top=2.8,x=-0.3,buff=0.5,edge=6.9)
        with self.voiceover("Both parts of the joint argument. <bookmark mark='a'/> For fixed negative e, the v derivative has the sign of F of v minus tau, so a unique continuous quantile minimizes the score in v. <bookmark mark='b'/> Define A of v as v minus the expected lower partial excess divided by tau. At the true cutoff this equals lower-tail ES. <bookmark mark='c'/> The e derivative is e minus A, divided by e squared. At the true cutoff it changes from negative to positive at the true ES, giving a global minimum within the negative domain. <bookmark mark='d'/> Minimizing v first and e second proves the pair result for the stated domain and integrability assumptions, not just a stationary point. Atoms and nonunique cutoffs require the more general theorem.") as vo:
            step(0)
            for i,mark in [(1,"b"),(2,"c"),(3,"d")]:
                vo.wait_until(mark)
                step(i)
        self.clear_scene()

    def check_grid(self, r):
        f = r["fz"]
        G = np.asarray(f["G"], float)
        vs = np.asarray(f["vs"], float)
        es = np.asarray(f["es"], float)
        sub = slice(0, None, 2)
        Gs = G[sub, sub]
        vmin, vmax = np.nanmin(Gs), np.nanpercentile(Gs, 85)
        n_e, n_v = Gs.shape
        size = 0.2
        cells = VGroup()
        for i in range(n_e):
            for j in range(n_v):
                val = Gs[i, j]
                if not np.isfinite(val):
                    continue
                t = min(max((val - vmin) / (vmax - vmin), 0), 1)
                col = interpolate_color(ManimColor(HURDLE), ManimColor("#1b2233"), t)
                cells.add(Square(side_length=size, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
                    [(j - n_v / 2) * size - 1.6, (i - n_e / 2) * size - 0.2, 0]))
        jt = int(np.argmin(np.abs(vs[sub] - f["v_true"])))
        it = int(np.argmin(np.abs(es[sub] - f["e_true"])))
        star = Star(n=5, outer_radius=0.16, color=BAD, fill_opacity=1).move_to(
            [(jt - n_v / 2) * size - 1.6, (it - n_e / 2) * size - 0.2, 0])
        xl = label(r"VaR forecast, from 0.6 to 1.4 times the truth", font_size=16, color=GREY_A).next_to(cells, DOWN, buff=0.25)
        yl = label(r"ES forecast", font_size=16, color=GREY_A).rotate(PI / 2).next_to(cells, LEFT, buff=0.25)
        side = VGroup(label(rf"true VaR, ES: {100 * f['v_true']:.2f}\%, {100 * f['e_true']:.2f}\%", font_size=18, color=BAD),
                      label(rf"grid minimum: {100 * f['v_hat']:.2f}\%, {100 * f['e_hat']:.2f}\%", font_size=18, color=HURDLE),
                      label(r"400,000 draws of a Student-$t_4$ day, $\tau = 2.5\%$", font_size=16, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        with self.voiceover(
            f"Check two is finite simulation evidence, not proof. <bookmark mark='a'/> Four hundred thousand Student-t-four draws generate average FZ-zero scores on an admissible grid around the truth, with brighter cells indicating smaller scores. The plotted heatmap uses every second grid point, while the reported minimum uses the full grid. <bookmark mark='b'/> Its minimum is {100*f['v_hat']:.2f} and {100*f['e_hat']:.2f} percent, compared with the separately displayed population values. Sampling and grid discretization can move a minimum; agreement at this resolution does not establish exact population equality."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(star), FadeIn(side[:2]))
        self.wait(0.4)
        self.clear_scene()

    def check_rank(self, r):
        hx = [-3.6, -0.6, 1.8, 4.4]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"97.5\% forecasts, 1928--2020", r"mean FZ0",
                                                                         r"exceeded", r"DM $t$ against the best")])
        tab = VGroup(head)
        best = r["best"]
        for x in r["rank"]:
            m = x["method"]
            tstat = r["dm"][m]["t"] if m in r["dm"] else None
            tab.add(VGroup(label(NAMES[m], font_size=18, color=GOOD if m == best else WHITE),
                           MathTex(f"{x['fz0']:.3f}", font_size=26, color=GOOD if m == best else WHITE),
                           MathTex(rf"{100 * x['rate']:.1f}\%", font_size=24),
                           MathTex(f"{tstat:.1f}" if tstat is not None else r"\text{--}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.72 * j, 0])
        worst = r["rank"][-1]["method"]
        worst_name = {"normal": "normal", "hs": "historical simulation", "ewma": "RiskMetrics", "fhs": "EWMA filter",
                      "gjr_fhs": "GJR filter", "evt": "EVT forecast"}[worst]
        tmin = min(v["t"] for v in r["dm"].values())
        tmax = max(v["t"] for v in r["dm"].values())
        with self.voiceover(
            "Check three: ranking the forecasters of Chapter three by FZ zero, at ninety-seven and a half percent, every "
            "day from nineteen twenty-eight. <bookmark mark='a'/> The GARCH-filtered historical simulation scores best. "
            f"<bookmark mark='b'/> Every other forecaster is worse, by Diebold-Mariano statistics from {tmin:.1f} to "
            f"{tmax:.1f}, and the {worst_name} last. The joint score orders them as the backtests did, but with one number "
            "each, and with a test of the difference."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def check_power(self, r):
        p = r["power"]
        rows = [cmath(r"\text{true}", r":", r"t_3;\quad \text{forecast: a normal with the same 99\% VaR}", font_size=34),
                cmath(r"\text{ES}", r":", rf"{p['es_normal']:.2f}\ \text{{forecast against}}\ {p['es_true']:.2f}\ "
                      r"\text{true}", font_size=36, colors={r"\text{ES}": ES_C}),
                cmath(r"\text{Kupiec rejects}", r":", rf"{100 * p['kupiec']:.1f}\%", font_size=38, colors={r"\text{Kupiec rejects}": VAR_C}),
                cmath(r"Z_2 \text{ rejects}", r":", rf"{100 * p['z2']:.1f}\%", font_size=38, colors={r"Z_2 \text{ rejects}": GOOD})]
        whys = [why(rf"{p['T']:,} days of a Student $t_3$, forecast by a normal tuned to get VaR exactly right; "
                    r"t and normal distributions differ broadly; only the selected VaR is matched"),
                why(r"the forecast shortfall is a quarter too small"),
                why(r"a test of VaR alone rejects at its size: it cannot see the error"),
                why(rf"Z$_2$, at its simulated 5\% critical value of {p['crit']:.2f}, catches it a third of the time")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"Check four holds one quantile fixed while changing the distribution. <bookmark mark='a'/> Each of two thousand replications has {p['T']} iid Student-t-three observations. A normal forecast is scaled to match its ninety-nine percent VaR, though the body and tail both differ. <bookmark mark='b'/> Forecast ES is {p['es_normal']:.2f} versus true {p['es_true']:.2f}. <bookmark mark='c'/> Kupiec rejects {100*p['kupiec']:.1f} percent: hits have the null one-percent probability, so the count does not identify the severity error. <bookmark mark='d'/> Z two rejects {100*p['z2']:.1f} percent using a critical value calibrated on the chosen normal null. These Monte Carlo rates and that calibration are specific to the sample length and alternative, not a universal power guarantee or proof that only the tail changed."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def comparative(self):
        cards = VGroup(
            desk_question(r"traditional backtests", r"ask whether a model can be rejected: a weak test, as Chapter 3 and "
                          r"check four show", width=12.4, font_size=19),
            desk_question(r"comparative backtests", r"Fissler, Ziegel and Gneiting (2016) and Nolde and Ziegel (2017): "
                          r"ask whether the bank's model scores worse than a standard one, with the burden of proof on "
                          r"the model", width=12.4, font_size=19),
            desk_question(r"a score-based traffic light", r"green if the model's FZ score is significantly better than "
                          r"the benchmark's, red if significantly worse: possible because the pair is elicitable",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this changes. <bookmark mark='a'/> A traditional backtest asks whether a model can be rejected, a weak "
            "question. <bookmark mark='b'/> Fissler, Ziegel and Gneiting, and Natalia Nolde with Ziegel, proposed "
            "comparative backtests: is the bank's model worse than a standard one, by the joint score? "
            "<bookmark mark='c'/> A traffic light built on score differences, possible only because the pair is "
            "elicitable."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def expectiles(self):
        rows = [cmath(r"e_\tau", r"=", r"\arg\min_x \mathbb E\,\bigl|\tau - \mathbf 1\{Y < x\}\bigr|\,(Y - x)^2", font_size=38,
                      colors={r"e_\tau": TAIL_C}),
                cmath(r"\text{coherent} \cap \text{elicitable}", r"=", r"\{-e_\tau(X),\ 0<\tau\le\tfrac12\}", font_size=36,
                      colors={r"\{-e_\tau(X),\ 0<\tau\le\tfrac12\}": HURDLE})]
        whys = [why(r"the expectile: an asymmetric least-squares analogue of the quantile, elicitable by construction"),
                why('Ziegel (2016) and Bellini and Bignozzi (2015): classification on an atomless rich bounded-return space with the required regularity; risk is minus a lower expectile')]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "An expectile minimizes an asymmetric squared loss when the needed second moment exists. <bookmark mark='a'/> For return X, a coherent monetary risk convention is minus its lower expectile, with tau at most one half; for losses use an upper expectile with the opposite tail orientation. <bookmark mark='b'/> Classification results for law-invariant coherent elicitable risks require an atomless rich function space and regularity; they are not an unqualified identity for every domain. The mean is included at tau one half. State the sign, space and integrability before applying that result."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"the theory", r"Osband (1985); Gneiting (2011); Fissler and Ziegel (2016); Ziegel (2016); "
                          r"Bellini and Bignozzi (2015)", width=12.4, font_size=19),
            desk_question(r"the practice", r"Patton, Ziegel and Chen (2019) on dynamic ES models; Acerbi and Székely "
                          r"(2014) on ES backtests; Nolde and Ziegel (2017) on comparative backtests", width=12.4,
                          font_size=19),
            desk_question(r"the series", 'QLIKE targets an appropriate conditional second-moment proxy under moment assumptions; squared error elicits the mean, and normalized R-squared summarizes a fixed-benchmark comparison', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The theory links Osband's convex-level-set condition, Gneiting's scoring framework and Fissler and Ziegel's joint elicitability. <bookmark mark='a'/> Patton, Ziegel and Chen develop dynamic joint-score models; Acerbi and Szekely study calibration diagnostics, and Nolde and Ziegel compare forecasting procedures. <bookmark mark='b'/> QLIKE can consistently score an appropriate conditional second moment or unbiased proxy under its assumptions; it does not elicit unconditional variance with an unknown mean from a single raw observation. Squared error elicits a mean. Out-of-sample R squared is a normalized fixed-benchmark loss comparison, not itself a universal standalone proper score. Those distinctions reconcile the next variance counterexample."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(('a','b')[k-1])
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"power in small samples", r"tests of ES that reject a wrong tail in a year or two of data, "
                          r"without strong distributional assumptions", width=12.4, font_size=19),
            desk_question(r"systemic measures", r"which systemic risk measures, such as CoVaR (Part 41), are elicitable, "
                          r"and with which scores", width=12.4, font_size=19),
            desk_question(r"scores that matter", r"among the many consistent scores for the pair, which one ranks models "
                          r"by what a bank actually loses when they are wrong", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Tests of expected shortfall with power in a year or two of data, "
            "without strong assumptions. <bookmark mark='b'/> Which systemic measures, such as Part forty-one's CoVaR, "
            "are elicitable, and by which scores. <bookmark mark='c'/> And among the many consistent scores for the pair, "
            "which one ranks models by what a bank actually loses when they are wrong."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the mean is elicited by squared error. Is the variance elicitable on its own? Use Lemma 2 with "
                       r"two point masses.")
        with self.voiceover(
            "Pause and predict. The mean is elicited by squared error. Is the variance elicitable on its own? Try lemma "
            "two with two point masses."
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
