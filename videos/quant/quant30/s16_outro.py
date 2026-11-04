from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import (BAD, EST_C, EW_C, GOOD, HRP_C, HURDLE, PART, REAL_C, RMT_C, RP_C, SHRINK_C,
                                         TRUE_C, comma, load)

DESK = [
    (r"Why does the optimizer love the asset with the most estimation error?",
     r"it maximises estimated return per unit of estimated risk, so it overweights assets whose mean is overestimated "
     r"and whose variance is underestimated: the largest positive errors (Michaud). Shrink the inputs, or use rules "
     r"that need fewer of them"),
    (r"Your 49-asset minimum-variance backtest on 5-year windows reports 3\% volatility. Believe it?",
     r"no: with $K/T \approx 0.8$ the true variance exceeds the reported one by $1/(1 - \gamma)^2$, roughly 30 times "
     r"under normality; here the data were worse still. Shrink, or lengthen the window, and report out-of-sample risk"),
    (r"A colleague adds a long-only constraint and the portfolio improves. Luck?",
     r"no: Jagannathan and Ma: the constraint shrinks exactly the covariances the optimizer would have exploited"),
    (r"Black--Litterman with no views gives which portfolio?",
     r"the market portfolio: the prior is the equilibrium that makes the market optimal. A view moves weights only along "
     r"the portfolios it mentions"),
    (r"Should a long-horizon investor hold the Kelly portfolio?",
     r"it maximises long-run growth, but with estimated means and a fat left tail, full Kelly is often ruinous in "
     r"practice; fractional Kelly trades a little growth for much less risk"),
    (r"HRP lost to 1/N on 2021--25. Drop it?",
     r"not on five years: the standard errors (about 0.45) exceed the difference; judge rules on their stated goal "
     r"(risk) and on long samples, and keep counting"),
]

PROBLEMS = [
    r"Two uncorrelated assets, volatilities 10\% and 20\%: the minimum-variance weights and volatility.",
    r"The same two assets: the equal-risk-contribution weights.",
    r"The Marchenko--Pastur edges for $N = 49$, $T = 60$.",
    r"Minimise $\mathbb E\|\delta F + (1 - \delta)S - \Sigma\|_F^2$ over $\delta$ for a fixed target $F$ with "
    r"$\mathbb E S = \Sigma$: the optimal intensity.",
    r"Black--Litterman with $P = 0$: the posterior mean and the portfolio.",
    r"Market excess return 6\%, volatility 16\%: the Kelly fraction, and the growth rate at twice it.",
    r"Cover's bound for two assets over $n$ periods: show the universal portfolio's growth rate per period approaches "
    r"the best constant mix's.",
    r"Five equally likely losses $-2, 0, 1, 5, 10$: CVaR at $\beta = 80\%$ and at $60\%$.",
    r"Two equally likely scenarios, returns $-10\%$ and $+10\%$; impose a mean of $+5\%$ by entropy pooling.",
    r"100 assets, 250 observations: by what factor does the sample GMV's true variance exceed what it reports, "
    r"asymptotically?",
    r"(qual) For $n\hat\Sigma \sim W_K(n, \Sigma)$, use $a^\top\Sigma^{-1}a / a^\top W^{-1}a \sim \chi^2_{n-K+1}$ to show "
    r"$\hat\sigma^2_{\text{in}}/\sigma^2_{\min} = \chi^2_{n-K+1}/n$; given the $F$ law of the out-of-sample excess, derive "
    r"$\mathbb E[\sigma^2_{\text{out}}/\sigma^2_{\min}] = (n - 1)/(n - K)$ and the limit of their ratio.",
    r"(qual) Prove Jagannathan and Ma's theorem: the long-only minimum-variance portfolio of $S$ is the unconstrained "
    r"one of $S - \frac12(\lambda 1^\top + 1\lambda^\top)$, $\lambda$ the KKT multipliers of $w \ge 0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("michaud"), load("rolling"), load("spectrum"), load("shrink"), load("constraints"), load("bl"),
                   load("riskparity"), load("cvar"), load("growth"), load("views"), load("e2e"), load("envelope"),
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

    def recap(self, m, ro, sp, sh, co, bl, rp, cv, gr, vw, e2, env, th):
        pts = np.median(np.asarray(m["sims"]["60"]["pts"], float), axis=0)
        r120 = ro["res"]["120"]
        y19 = sp["years"]["2019"]
        s60 = sh["sims"]["60"]
        lw = env["strats"]["lw_gmv_part30"]["row"]["holdout"]
        hp = env["strats"]["hrp_part30"]["row"]["holdout"]
        ew = env["strats"]["equal_weight_part30"]["row"]["holdout"]
        items = [
            (rf"error maximisation: promised {100 * pts[2]:.1f}\% volatility a month, delivered {100 * pts[0]:.1f}\%", EST_C),
            (rf"1/N against the optimizers: {r120['1/N']['sharpe']:.2f}; sample tangency {r120['sample tangency']['sharpe']:.2f}; "
             rf"shrunk GMV {r120['LW const-corr GMV']['sharpe']:.2f}", EW_C),
            (rf"Marchenko--Pastur: {y19['n_above']} of 49 eigenvalues above the noise edge; the market mode "
             rf"{100 * y19['share1']:.0f}\%", RMT_C),
            (rf"shrinkage: the sample GMV's true variance {s60['sample']['gmv']:.1f}$\times$ the minimum, shrunk "
             rf"{s60['nonlinear']['gmv']:.1f}$\times$", SHRINK_C),
            (rf"constraints as shrinkage: long only keeps {co['n_pos']} industries; Jagannathan--Ma, exactly", SHRINK_C),
            (r"Black--Litterman: equilibrium returns, and views relative to them", TRUE_C),
            (r"risk parity and HRP: equal risk, no inverted matrix", RP_C),
        ]
        items2 = [
            (r"robust optimisation and CVaR: the better risk measure needs more data", BAD),
            (rf"Kelly {gr['kelly']:.2f} on the market; Cover's universal portfolio; Fernholz's diversity", GOOD),
            (rf"entropy pooling: a banking crisis view, {vw['ens']:.0f} effective scenarios of {vw['J']}", HURDLE),
            (rf"end to end: {e2['train']['e2e']:.2f} in training, {e2['valid']['e2e']:.2f} out", BAD),
            (rf"2021--25: 1/N {ew['sharpe']:.2f}, HRP {hp['sharpe']:.2f}, shrunk GMV {lw['sharpe']:.2f}; counter "
             rf"{comma(env['trials'])}", QC.HOUSE),
            (r"Rule 30: shrink, report out-of-sample risk, compare with 1/N", QC.HOUSE),
            (rf"research: reported $\to (1 - \gamma)\sigma^2_{{\min}}$, true $\to \sigma^2_{{\min}}/(1 - \gamma)$", REAL_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 30 in fourteen lines")
        with self.voiceover(
            "Part thirty in fourteen lines. Fed with estimates, the optimizer promises a fraction of the risk it delivers, "
            "because it seeks out the most flattering errors. Against one over N, the rules that use estimated means lose, "
            "and the rules that minimise variance with a shrunk covariance win on risk. Random matrix theory says most of "
            "a covariance matrix's spectrum is indistinguishable from noise, apart from the market and a few sectors. "
            "Shrinkage toward a simple target, linear or eigenvalue by eigenvalue, cuts the damage several times over; a "
            "long-only constraint does the same in disguise. Black and Litterman start from the market. Risk parity and "
            "HRP avoid inverting the matrix at all."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 30 in fourteen lines")
        with self.voiceover(
            "Minimising tail risk needs more data than minimising variance. Growth has its own theory, from Kelly's "
            "leverage to Cover's universal portfolio and Fernholz's diversity. Entropy pooling imposes a view on a whole "
            "distribution, and chose the crises by itself. A network trained end to end learned its training years. On "
            "the sealed years one over N came first, by less than a standard error. And the research chapter proved that "
            "the sample minimum-variance portfolio always underestimates its own risk, by a factor it computed."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a_, width=12.4, font_size=20) for q, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Why does the optimizer love the asset with the most estimation error? Because it "
            "maximises estimated reward per estimated risk, and the most flattering estimates are the most wrong. "
            "<bookmark mark='a'/> A forty-nine-asset backtest on five-year windows reporting three percent volatility is "
            "reporting a fraction of its true variance. <bookmark mark='b'/> And a long-only constraint that improves a "
            "portfolio is not luck: it is shrinkage."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "Black-Litterman with no views returns the market. <bookmark mark='a'/> Full Kelly maximises long-run growth "
            "and is usually too much, because its inputs are estimates. <bookmark mark='b'/> And five years cannot rank "
            "two rules whose standard errors exceed their difference. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: a two-asset minimum-variance portfolio; its risk-parity cousin; the noise band for "
            "five-year windows; the optimal shrinkage intensity; Black-Litterman without views; Kelly and twice Kelly; "
            "Cover's bound; CVaR by hand; entropy pooling on two scenarios; and the risk illusion for a hundred assets. "
            "Then two qualifying-exam problems: the exact laws of the sample minimum-variance portfolio's risk, and "
            "Jagannathan and Ma's theorem. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"factor risk models, costs and trading through time", [31]),
            (r"risk parity in macro: trend and alternative premia", [32]),
            (r"measuring risk: VaR, CVaR, coherence", [40]),
            (r"the finale: every optimizer's row, deflated", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-one builds factor risk models, the structured covariance a real desk uses, "
            "and trades through time with costs. Part thirty-two puts risk parity to work across asset classes. Part forty "
            "measures risk properly, including CVaR's coherence. And the finale deflates these rows with everything else."
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
            "The textbooks this part follows, and the papers it draws on, from Markowitz in 1952 to nonlinear shrinkage "
            "in 2020. Every number on screen was computed by the House's code from Kenneth French's industry portfolios, "
            "with simulations labelled as such."
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
