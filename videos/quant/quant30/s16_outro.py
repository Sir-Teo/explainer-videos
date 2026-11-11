from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant30.common import (BAD, EST_C, EW_C, GOOD, HRP_C, HURDLE, PART, REAL_C, RMT_C, RP_C, SHRINK_C,
                                         TRUE_C, comma, load)

DESK = [('Why can an optimizer select flattering errors?', 'adaptive weights exploit estimated inputs; inspect objective, sign normalisation, covariance loss and evaluation; no one-error explanation identifies a causal effect'), ('A 49-asset, 60-month backtest reports 3\\% volatility. Is its true risk known?', 'no: Gaussian ratios are model references, not conditional certainty; inspect timing, assumptions and independently measured risk'), ('Does the Jagannathan--Ma identity guarantee future improvement?', 'no: it identifies an equivalent adjusted unit-budget quadratic; population misspecification and costs still matter'), ('Black--Litterman with no views gives which weights?', 'mean stays Pi; unchanged Sigma recovers benchmark risky demand, predictive Sigma scales it by 1/(1+tau), absent other constraints'), ('Does estimated Kelly imply a universal half-Kelly rule?', 'no: the displayed fraction needs fixed true strength, known variance and an unbiased independent mean estimate in a quadratic growth model'), ('An unchanged 1/N target has zero target changes. Zero trades?', 'no: relative returns drift holdings; maintaining the target requires trades from pretrade weights, with fee and financing conventions specified')]

PROBLEMS = ['Two uncorrelated assets have annual volatilities 10\\% and 20\\%. Derive unit-budget GMV weights and volatility.', 'For the same chosen covariance, derive positive equal-risk-contribution weights and volatility; compare equal money.', 'Compute the Marchenko--Pastur null support at N=49,T=60. State why it is not a finite-sample test of economic noise.', 'For fixed target F and unbiased S, derive the Frobenius-optimal linear intensity, clipped to [0,1]. What changes if F is estimated from S?', 'Black--Litterman with no views: give the posterior mean and risky demands under unchanged versus predictive covariance, with no budget constraint.', 'In a known-parameter diffusion, market excess drift is 6\\%, volatility16\\%. Compute Kelly leverage and quadratic excess growth at twice Kelly.', "For two assets derive Cover's continuous-uniform per-period bound; separately derive the M-component uniform finite-mixture bound. Distinguish their hindsight comparison classes.", 'Five equally likely losses are -2,0,1,5,10. Compute exact expected shortfall at 80\\% and60\\%, accounting for quantile mass.', 'Two scenarios have returns -10\\% and+10\\% and positive equal prior weights. Impose a+5\\% mean and solve the entropy-pooling probabilities.', 'In the IID Gaussian GMV model with K=100,T=250, compute exact expected in/out ratios, their ratio, and the gamma=.4 limiting ratio. Distinguish ratio of expectations from expected ratio.', '(qual) Prove the inverse-Wishart quadratic chi-square lemma using a Schur complement. Derive the GMV out-risk F law via Gaussian regression, its mean conditions, concentration limits and ensemble bias correction.', "(qual) With S positive definite, prove long-only GMV equivalence for adjusted S-1/2(lambda1'+1lambda'). Use zero-budget directions to explain why full-space positive definiteness of the adjusted matrix is unnecessary."]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("michaud"), load("rolling"), load("spectrum"), load("shrink"), load("constraints"), load("bl"),
                   load("riskparity"), load("cvar"), load("growth"), load("views"), load("e2e"),
                   load("theory"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, m, ro, sp, sh, co, bl, rp, cv, gr, vw, e2, th):
        pts = np.median(np.asarray(m["sims"]["60"]["pts"], float), axis=0)
        r120, y19, s60 = ro["res"]["120"], sp["years"]["2019"], sh["sims"]["60"]
        groups = [
            [(rf"Gaussian model: median reported monthly vol {100*pts[2]:.1f}\%, true {100*pts[0]:.1f}\%", EST_C),
             (rf"research Sharpe: 1/N {r120['1/N']['sharpe']:.2f}; shrunk GMV {r120['LW const-corr GMV']['sharpe']:.2f}", EW_C),
             (rf"MP null benchmark: {y19['n_above']} eigenvalues above edge; no bulk/noise identification", RMT_C),
             (rf"fixed Gaussian sample-GMV risk ratio {s60['sample']['gmv']:.1f}; nonlinear {s60['nonlinear']['gmv']:.2f}", SHRINK_C),
             (r"constraints: unit-budget quadratic identity, not a future dominance guarantee", SHRINK_C),
             (r"Black--Litterman: prior, view errors and covariance convention all matter", TRUE_C),
             (r"ERC and HRP differ; no inverse does not mean no estimation risk", RP_C)],
            [(r"CVaR: precise tail mass and historical scenario fitting", BAD),
             (r"Kelly: specified diffusion; Cover: continuous theorem versus finite grid", GOOD),
             (rf"entropy: {vw['ens']:.0f} effective scenarios; fixed-centre moment stress", HURDLE),
             (rf"end-to-end diagnostic: train {e2['train']['e2e']:.2f}, validation {e2['valid']['e2e']:.2f}; leaked scaling", BAD),
             (rf"protocol and fixed arithmetic; existing registrations {comma(pit.trials_upto(PART))}", QC.HOUSE),
             (r"Rule 30: audit information, estimation, holdings, costs and evaluation", QC.HOUSE),
             (r"research: exact Gaussian laws, ensemble bias and conditional limits", REAL_C)]]
        head, rows = self._rows(list(enumerate(groups[0], 1)), r"Part 30: estimation and allocation")
        with self.voiceover("The first seven lessons. Gaussian simulations separate fitted promises from population evaluation. Retrospective rolling comparisons do not prove universal failure of means. Random-matrix support is a null benchmark, not a noise classifier. Shrinkage depends on its target and loss. Constraints have an exact unit-budget identity, without guaranteed future improvement. Black-Litterman depends on prior and covariance conventions. ERC and HRP need different interpretations and still face estimation risk."):
            self.play(FadeIn(head), FadeIn(rows))
        self.clear_scene()
        head, rows = self._rows(list(enumerate(groups[1], 8)), r"Part 30: evaluation and limits")
        with self.voiceover("The remaining lessons. CVaR requires a discrete tail convention and enough relevant scenarios. Kelly needs a stated model, and a finite portfolio grid differs from Cover's continuous theorem. Entropy pooling reweights supplied scenarios. The saved network has a validation-scaling leak. Evaluation protocol and fixed arithmetic replace a strategy verdict. The research proof gives exact Gaussian sampling laws and ensemble bias, not a guarantee that every realised report understates risk."):
            self.play(FadeIn(head), FadeIn(rows))
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards=VGroup(*[desk_question(q,a,width=12.4,font_size=20)for q,a in qs]).arrange(DOWN,buff=.25)
            if cards.height>6.6:cards.scale_to_fit_height(6.6)
            return cards
        cards=page(DESK[:3])
        with self.voiceover("Six desk checks. Ask how an objective selects flattering errors. <bookmark mark='a'/> A low reported variance does not identify its true risk without assumptions. <bookmark mark='b'/> A constraint identity does not guarantee better future performance.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards=page(DESK[3:])
        with self.voiceover("Without views, Black-Litterman's weights depend on the covariance convention. <bookmark mark='a'/> Fractional Kelly is a model calculation, not a universal half-bet rule. <bookmark mark='b'/> An unchanged equal-weight target can still require trading because holdings drift. Full solutions are in the bilingual notes.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def problems(self):
        def page(start,end,title):
            ps=problem_set(PROBLEMS[start:end],font_size=25,title=title)
            for number,row in enumerate(ps.rows,start+1):
                old=row[0]
                new=label(rf"{number}.",font_size=25,color=old.get_color())
                new.match_height(old).move_to(old).align_to(old,RIGHT)
                old.become(new)
            self.play(FadeIn(ps.head),FadeIn(ps.rows))
        with self.voiceover("Twelve problems in three groups. The first six derive fixed-covariance weights, the MP null benchmark, fixed-target shrinkage, no-view Black-Litterman and diffusion Kelly. <bookmark mark='a'/> Problems seven through ten separate continuous and finite-mixture bounds, calculate discrete tail risk and entropy probabilities, and compare exact Gaussian expectations with high-dimensional limits. <bookmark mark='b'/> Two qualifying problems prove the Wishart and F sampling laws with their conditions, then establish Jagannathan-Ma on the unit-budget affine set. Complete English and Chinese solutions are in the notes.") as vo:
            page(0,6,r"Problems 1--6")
            vo.wait_until("a")
            self.clear_scene()
            page(6,10,r"Problems 7--10")
            vo.wait_until("b")
            self.clear_scene()
            page(10,12,r"Problems 11--12: qualifying")
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"factor risk models, costs and trading through time", [31]),
            (r"risk parity in macro: trend and alternative premia", [32]),
            (r"measuring risk: VaR, CVaR, coherence", [40]),
            (r"the finale: every optimizer's row, deflated", [43]),
        ])
        with self.voiceover(
            'These questions return later. Part thirty-one studies factor risk models, costs and decisions through time. Part thirty-two considers macro allocation. Part forty develops risk measures and expected shortfall. The finale reviews the full record and evaluation policy; a bookkeeping or statistical correction alone does not certify a selected strategy.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Meucci, \textit{Risk and Asset Allocation} (2005); Grinold and Kahn, \textit{Active Portfolio Management}, "
             r"ch.\ 14--15; Paleologo, \textit{Advanced Portfolio Management} (2021); Chincarini and Kim, "
             r"\textit{Quantitative Equity Portfolio Management}; Muirhead, \textit{Aspects of Multivariate Statistical "
             r"Theory} (1982)"],
            [r"Markowitz (1952); Kelly (1956); Breiman (1961); Marchenko and Pastur (1967); Merton (1972); Michaud (1989); "
             r"Best and Grauer (1991); Cover (1991); Black and Litterman (1992); Chopra and Ziemba (1993); He and "
             r"Litterman (1999); Laloux, Cizeau, Bouchaud and Potters (1999); Rockafellar and Uryasev (2000); Fernholz "
             r"(2002); Goldfarb and Iyengar (2003); Jagannathan and Ma (2003); Ledoit and Wolf (2003, 2004a, 2004b, "
             r"2017, 2020)",
             r"Kempf and Memmel (2006); Ceria and Stubbs (2006); Meucci (2008); DeMiguel, Garlappi and Uppal (2009); Bai, "
             r"Liu and Wong (2009); El Karoui (2010); Maillard, Roncalli and Te\"iletche (2010); Spinu (2013); "
             r"L\'opez de Prado (2016); Bun, Bouchaud and Potters (2017); Bodnar, Parolya and Schmid (2018); Zhang, "
             r"Zohren and Roberts (2020). Data: Kenneth French's data library"])
        with self.voiceover(
            'The notes identify the textbooks and papers for each method, from Markowitz to nonlinear shrinkage and decision-focused learning. Measured quantities come from audited ordinary originals; population simulations and fixed arithmetic have explicit labels. Paper claims remain attributed, and the sealed strategy experiment is excluded.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 31, Risk Models, Costs and Trading Through Time", font_size=30, color=QC.IDEA
                    ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a portfolio desk: estimators that know their noise, rules that need fewer estimates, and a "
            "duty to report risk on data the weights never saw. <bookmark mark='a'/> Next, Part thirty-one: risk models, "
            "costs and trading through time. The fundamental law of active management, derived; factor risk models; and "
            "how to trade toward a moving target when every trade costs money."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
