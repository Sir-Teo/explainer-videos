from __future__ import annotations

import numpy as np

from videos.quant.quant26.common import *  # noqa: F403
from videos.quant.quant26.common import GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, fit_right, load

NAIVE = QC.LOSS
COND = QC.GAIN
HYB = QC.OPTION


def _pc(s: str) -> str:
    """A rule's label for TeX: its percent signs escaped."""
    return s.replace("%", r"\%")


def _ci(c, digits=2, capped=False):
    if capped:
        return rf"[\le {c[0]:.{digits}f},\ {c[1]:.{digits}f}]\ {{\scriptscriptstyle \text{{floor}}}}"
    return rf"[{c[0]:.{digits}f},\ {c[1]:.{digits}f}]"


class Research(VoiceoverScene):
    def construct(self):
        t = load("winners")
        self.card(t)
        self.curse()
        self.condition()
        self.invert()
        self.sim(t)
        self.picture(t)
        self.data(t)
        self.reading(t)
        self.open_problems()
        self.question()

    def card(self, t):
        w = t["data"]["1926-86"]
        c = research_card(r"Inference on the winner", rf"The best of 10{{,}}000 rules earned a Sharpe ratio of {w['x']:.2f}. "
                          r"What interval for its true Sharpe ratio is honest, given that it was picked for being best?",
                          part=PART)
        with self.voiceover("For the researcher: Chapters 3 and 8 deflated the best backtest against a hurdle, and asked "
                            "whether it beats noise. A sharper question: given that we picked it for being the best, what "
                            "is an honest estimate of how good it really is, with an interval that covers? Isaiah Andrews, "
                            "Toru Kitagawa and Adam McCloskey give exact results in a specified Gaussian model; the historical Sharpe application below is an approximation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curse(self):
        rows=[cmath(r"X",r"\sim",r"N(\mu,\Sigma),\quad\hat\jmath=\arg\max_jX_j",font_size=34,colors={r"X":RULE}),
              cmath(r"\mathbb E[X_{\hat\jmath}-\mu_{\hat\jmath}]",r"\ge",r"0",font_size=34,colors={r"\mathbb E[X_{\hat\jmath}-\mu_{\hat\jmath}]":NAIVE}),
              cmath(r"\Pr(0\in X_{\hat\jmath}\pm1.96)",r"=",r"\Phi(1.96)^J-\Phi(-1.96)^J\quad(\mu=0,\Sigma=I)",font_size=29,colors={r"\Pr(0\in X_{\hat\jmath}\pm1.96)":NAIVE})]
        whys=[why(r"a known-covariance jointly Gaussian estimation model; historical Sharpe estimates need an approximation and covariance estimation"),
              why(r"selection can create upward bias in the chosen estimate; strictness depends on nondegenerate selection, and bias alone does not imply universal undercoverage"),
              why(r"for independent standard-normal null estimates, coverage is about 95\% at $J=2$ but 28.2\% at $J=50$; repeated selection does not preserve a generic fixed-parameter interval")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=-.3,buff=.5,edge=6.9)
        with self.voiceover("Start with a statistical model. <bookmark mark='a'/> Estimates are jointly Gaussian with known covariance, and we select the largest. The later Sharpe-ratio application only approximates that model. <bookmark mark='b'/> Selection can bias the chosen estimate upward. Nonnegative bias does not by itself imply that every selected interval strictly undercovers. <bookmark mark='c'/> With independent standard-normal null estimates, coverage of the selected symmetric interval is Phi of one point nine six to the number of estimates, minus the opposite-tail probability to that same power. With two it is about ninety-five percent; with fifty it is about twenty-eight percent.") as vo:
            step(0);vo.wait_until('a');self.wait(.1);vo.wait_until('b');step(1);vo.wait_until('c');step(2)
        self.clear_scene()

    def condition(self):
        rows=[cmath(r"Z",r"=",r"X-{\Sigma_{\cdot j}\over\Sigma_{jj}}X_j\ \perp\ X_j,\quad a_k=1-{\Sigma_{kj}\over\Sigma_{jj}}",font_size=30,colors={r"Z":GREY_A}),
              cmath(r"L(Z),\ U(Z)",r"=",r"\max_{k:a_k>0}{Z_k\over a_k},\quad\min_{k:a_k<0}{Z_k\over a_k}",font_size=32,colors={r"L(Z),\ U(Z)":HURDLE}),
              cmath(r"X_j\mid\hat\jmath=j,Z",r"\sim",r"N(\mu_j,\Sigma_{jj})\text{ restricted to }[L,U]",font_size=30,colors={r"X_j\mid\hat\jmath=j,Z":COND})]
        whys=[why(r"joint Gaussian with known covariance and $\Sigma_{jj}>0$; residuals are independent of $X_j$"),
              why(r"winning requires $a_kX_j\ge Z_k$: lower bounds for $a_k>0$, upper bounds for $a_k<0$; if $a_k=0$, require $Z_k\le0$. Empty extrema are $-\infty,+\infty$"),
              why(r"conditional on a feasible selection event and residuals, only $\mu_j$ is unknown; the equal-variance nondegenerate examples have $a_k>0$and $U=+\infty$")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=-.3,buff=.5,edge=6.9)
        theorem=theorem_card(r"Known Gaussian model and numerical application",wrapped_label(r"Exact conditional coverage follows from exact truncated-normal inversion under the stated known-covariance model. The saved implementation uses finite search brackets; the hybrid uses a finite grid and simulated projection critical values. Historical Sharpe intervals are plug-in diagnostics.",9.6,22),r"Andrews, Kitagawa and McCloskey (2024),\textit{QJE}139; implementation qualifications",width=10.4,font_size=22)
        with self.voiceover("Condition on the winner and suitable residuals. <bookmark mark='a'/> Subtract the covariance projection of the winning estimate. Joint Gaussianity makes the residual vector independent of that estimate when the covariance is known. <bookmark mark='b'/> Each rival imposes a scaled inequality. A positive coefficient gives a lower bound, a negative coefficient gives an upper bound, and a zero coefficient imposes a residual feasibility condition. In the equal-variance examples the upper bound is infinite. <bookmark mark='c'/> Conditional on a feasible winning event and the residuals, the estimate has a truncated normal distribution. <bookmark mark='d'/> Exact inversion gives exact conditional coverage in this model. Finite search brackets, a gridded hybrid and simulated critical values introduce numerical approximations; estimated Sharpe covariances add further uncertainty.") as vo:
            step(0);vo.wait_until('a');self.wait(.1);vo.wait_until('b');step(1);vo.wait_until('c');step(2);vo.wait_until('d');self.play(FadeOut(Group(*self.mobjects)));self.play(FadeIn(theorem,shift=UP*.2))
        self.clear_scene()

    def invert(self):
        rows = [cmath(r"F(\mu)", r"=", r"\Pr_{\mu}\big(X_j \le x_j \mid L \le X_j \le U\big)\ \ \text{falls as } \mu \text{ rises}",
                      font_size=30, colors={r"F(\mu)": COND}),
                cmath(r"F(\hat\mu_{1/2})", r"=", r"\tfrac12,\qquad F(\mu_{\mathrm{lo}}) = 1 - \tfrac\alpha2,\quad F(\mu_{\mathrm{hi}}) = "
                      r"\tfrac\alpha2", font_size=30, colors={r"F(\hat\mu_{1/2})": COND}),
                cmath(r"\text{hybrid}", r":", r"\text{also truncate to } |X_j - \mu| \le c_\beta\sigma_j,\ \text{level } "
                      r"\tfrac{\alpha - \beta}{1 - \beta}", font_size=30, colors={r"\text{hybrid}": HYB})]
        whys = [why(r"the conditional cdf of the observed estimate, as a function of the unknown mean"),
                why(r"the median-unbiased estimate and the equal-tailed interval: exactly as for an ordinary normal, but on "
                    r"the truncated one. When $x_j$ is close to $L$, the interval becomes very wide"),
                why(r"$c_\beta$: the simultaneous (max-$|t|$) critical value at $\beta = 0.5\%$. The hybrid lies inside "
                    r"the projection interval in the ideal known-model theorem; this implementation uses finite grids and simulated critical values")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The theorem and its implementation have different precision. <bookmark mark='a'/> Under a known Gaussian model, the conditional distribution function falls as the candidate mean rises. <bookmark mark='b'/> Exact tail inversion defines conditional intervals and a median-unbiased estimator. The original numerical routine searches only sixty standard errors on either side of the observation and returns a boundary when no root is bracketed. A boundary is not an exact interval endpoint. <bookmark mark='c'/> The hybrid additionally uses a simultaneous projection event and an adjusted tail level. Its ideal coverage theorem requires a valid simultaneous critical value. Here the hybrid is approximated on eight hundred and one grid points, and the critical values are simulated or estimated. Neither numerical example is an exact historical coverage guarantee."
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

    def picture(self, t):
        w = t["data"]["1987-2003"]
        inv = t["inv"]
        mu = np.asarray(inv["mu"], float)
        g = axes([-3, 2], [0, 1], x_length=8.0, y_length=4.2, xlabel=r"candidate true Sharpe ratio $\mu$ of the "
                 r"1987--2003 winner", ylabel=r"$F(\mu)$: chance of an estimate at or below the one observed, given it won",
                 xticks=[-3, -2, -1, 0, 1, 2], yticks=[0, 0.5, 1], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        curves = {}
        for key, col in (("naive", NAIVE), ("cond", COND), ("hybrid", HYB)):
            y = np.asarray(inv[key], float)
            ok = np.isfinite(y)
            curves[key] = curve(ax, mu[ok], y[ok], col, stroke_width=3)
        levels = VGroup(*[DashedLine(ax.c2p(-3, v), ax.c2p(2, v), color=GREY_C, stroke_width=1.5) for v in (0.025, 0.5, 0.975)])
        dots = VGroup(Dot(ax.c2p(w["x"], 0.5), color=NAIVE), Dot(ax.c2p(w["med"], 0.5), color=COND),
                      Dot(ax.c2p(w["hyb_med"], 0.5), color=HYB))
        leg = legend([(NAIVE, r"naive: a plain normal"), (COND, r"conditional on winning"),
                      (HYB, r"hybrid: inside the simultaneous interval")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = wrapped_label(f"{_pc(w['label'])} won by {w['gap']:.2f} standard errors over {_pc(w['binding'])}. Estimates where each curve crosses $\\frac12$: {w['x']:.2f}, {w['med']:.2f}, {w['hyb_med']:.2f}; the conditional lower root is beyond the solver floor {w['cond'][0]:.1f}; the plot shows only part of the candidate-mean range", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"This plot shows only candidate means from minus three to two for the 1987 to 2003 winner. Its gap above the fitted selection boundary is {w['gap']:.2f} proxy standard errors. <bookmark mark='a'/> The naive curve crosses one half at {w['x']:.2f}. <bookmark mark='b'/> The conditional median root is {w['med']:.2f}. Crucially, its lower-tail root is not found within the finite bracket: the stored value {w['cond'][0]:.2f} is the sixty-standard-error solver floor, so the true model-based lower endpoint lies farther left. <bookmark mark='c'/> The gridded hybrid median is {w['hyb_med']:.2f}, with approximate grid bounds {w['hybrid'][0]:.2f} and {w['hybrid'][1]:.2f}. Estimated correlations and an IID Sharpe standard-error proxy add uncertainty beyond this numerical truncation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(levels), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(curves["naive"]), FadeIn(dots[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(curves["cond"]), FadeIn(dots[1]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(curves["hybrid"]), FadeIn(dots[2]), FadeIn(leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def sim(self, t):
        hx = [-4.6, -2.2, -0.6, 1.0, 2.6, 4.6]
        head = VGroup(label(r"true means", font_size=18, color=GREY_B), label(r"naive", font_size=19, color=NAIVE),
                      label(r"conditional", font_size=19, color=COND), label(r"hybrid", font_size=19, color=HYB),
                      label(r"projection", font_size=19, color=GREY_A), label(r"median bias: naive / $\hat\mu_{1/2}$",
                                                                              font_size=17, color=GREY_B))
        tab = VGroup(head)
        for name, s_ in t["sims"].items():
            cv, ln = s_["cover"], s_["length"]
            tab.add(VGroup(label(name, font_size=18),
                           *[MathTex(rf"{100 * cv[k]:.0f}\%\ ({ln[k]:.1f})", font_size=24) for k in ("naive", "cond", "hybrid", "proj")],
                           MathTex(rf"{s_['medbias_naive']:+.2f}\ /\ {s_['medbias_med']:+.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.8 * j, 0])
        foot = wrapped_label(rf"{t['J']} estimates with unit standard error, correlation {t['rho']:.1f} between every pair; "
                             rf"{t['reps']:,} draws per row; coverage of the winner's true mean by 95\% intervals, median "
                             r"length in brackets; projection: the simultaneous max-$|t|$ interval", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        z, c1 = t["sims"]["all zero"], t["sims"]["one clear winner"]
        with self.voiceover(
            f"These saved known-Gaussian simulations use {t['J']} estimates, pairwise correlation {t['rho']:.1f}, and {t['reps']:,} worlds per row. <bookmark mark='a'/> With all means zero, naive coverage is {100*z['cover']['naive']:.1f} percent; with one clear winner it is {100*c1['cover']['naive']:.1f} percent. Selection effects depend on the model and mean configuration. <bookmark mark='b'/> The table gives actual conditional and hybrid coverage frequencies, and median estimator bias. These are finite Monte Carlo results, with conditional root brackets and a gridded hybrid. <bookmark mark='c'/> The parenthesised quantities are median lengths. Simultaneous critical values were estimated from twenty thousand Gaussian draws. The ideal theorem does not turn those finite numerical frequencies into exact guarantees, and the hybrid need not be longer than naive in every sample."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[1]) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3], r_[5])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[4]) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        hx = [-4.9, -2.3, -0.2, 1.9, 4.6]
        head = VGroup(label(r"chosen on", font_size=18, color=GREY_B), label(r"naive", font_size=19, color=NAIVE),
                      label(r"conditional", font_size=19, color=COND), label(r"hybrid", font_size=19, color=HYB),
                      label(r"afterwards ($\pm 1.96$ s.e.)", font_size=18, color=OOS_C))
        tab = VGroup(head)
        for name, w in t["data"].items():
            after = rf"{w['first_out'] // 10000}\text{{--}}{w['last_out'] // 10000 % 100:02d}"
            tab.add(VGroup(VGroup(label(rf"{name}", font_size=20), label(_pc(w["label"]), font_size=15, color=GREY_A)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['x']:.2f}", font_size=26), MathTex(_ci(w["naive"]), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['med']:.2f}", font_size=26), MathTex(_ci(w["cond"], capped=bool(np.isclose(w['cond'][0],w['x']-60*w['s']))), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['hyb_med']:.2f}", font_size=26), MathTex(_ci(w["hybrid"]), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['out']:.2f}", font_size=26),
                                  MathTex(rf"\pm {1.96 * w['s_out']:.2f}\ \ ({after})", font_size=20)).arrange(DOWN, buff=0.08)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 1.2 * j, 0])
        foot = wrapped_label(r"annualised Sharpe ratios of the best of the 10{,}000 rules, chosen in each era; standard error "
                             r"$\sqrt{252/T}$ IID common-error proxy; estimated return correlations; finite 60-s.e. root brackets and 801-point hybrid grid; $c_\beta$ by a "
                             r"400-draw IID Gaussian multiplier calculation on all 10{,}000 rules; no exact time-series coverage claim", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.55)
        a_, b_ = t["data"]["1926-86"], t["data"]["1987-2003"]
        with self.voiceover(
            f"Apply the unchanged plug-in calculation to the two saved rule searches. <bookmark mark='a'/> The 1926 to 1986 winner has ratio {a_['x']:.2f}, a fitted gap of {a_['gap']:.1f} standard errors, and conditional roots {a_['cond'][0]:.2f} and {a_['cond'][1]:.2f}. Its later ratio is {a_['out']:.2f}. <bookmark mark='b'/> The 1987 to 2003 winner has ratio {b_['x']:.2f}, a gridded hybrid median {b_['hyb_med']:.2f}, and later ratio {b_['out']:.2f}. Its conditional lower endpoint is beyond the displayed solver floor. Common IID Sharpe errors, estimated return correlations and four hundred IID Gaussian multiplier draws make this historical analysis approximate. The later contrast identifies neither a unique causal explanation nor future performance."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def reading(self,t):
        a_,b_=t['data']['1926-86'],t['data']['1987-2003']
        cards=VGroup(
            desk_question(r"earlier winner: little correction in this proxy",rf"a {a_['gap']:.1f}-standard-error gap in the fitted model; historical collapse does not identify how much came from regime change, stale prices, selection or implementation",width=12.4,font_size=18),
            desk_question(r"later winner: substantial conditional adjustment",rf"{b_['n_close']} rules lie within two proxy standard errors; the gridded hybrid estimate is near zero. Later realised performance does not prove selection was the only cause",width=12.4,font_size=18),
            desk_question(r"what it estimates",r"a selected same-window mean under a specified model, not next decade's performance. Common IID standard errors, estimated return correlations and finite numerical search limit the historical inference",width=12.4,font_size=18),
        ).arrange(DOWN,buff=.22)
        with self.voiceover("Read the two historical examples cautiously. <bookmark mark='a'/> The earlier winner has a wide lead under the fitted common-error model, so that model makes little selection correction. Its later collapse does not identify a unique regime-change cause or eliminate other sources of bias. <bookmark mark='b'/> The later winner has many close rivals and receives a substantial conditional adjustment. Subsequent performance does not establish that selection explained all of its decline. <bookmark mark='c'/> These procedures concern a selected same-window mean under stated assumptions. Estimated correlations, an independent-return standard-error proxy and finite numerical search prevent an exact historical coverage claim or a forecast certificate.") as vo:
            for k,mk in enumerate(('a','b','c')):
                if k:vo.wait_until(mk)
                self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: non-normal, dependent returns", r"the theorem needs a normal estimate with known "
                          r"covariance; with fat tails and time-varying volatility it needs a justified asymptotic approximation and covariance estimate; how fast "
                          r"in Sharpe-ratio problems is not well charted", width=12.4, font_size=18),
            desk_question(r"open: adaptive research", r"real searches are sequential: each try depends on the last. "
                          r"Conditioning on a whole research path, not just one argmax, is largely open", width=12.4,
                          font_size=18),
            desk_question(r"open: winners in a changing world", r"combining selection-corrected inference with "
                          r"structural breaks, so that an interval covers next decade's Sharpe ratio, not last decade's", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three research questions remain. <bookmark mark='a'/> Known Gaussian covariance is a strong assumption. Dependent, heavy-tailed or nonstationary returns need a justified limiting distribution, covariance estimation and finite-sample assessment; a large sample alone is not sufficient. <bookmark mark='b'/> Real adaptive searches involve a whole history of choices. Conditioning only on one maximum does not account for that full path. <bookmark mark='c'/> Finally, selection-adjusted inference for a past-window mean is different from prediction through structural change. A future-performance interval needs a credible model of that change as well as selection."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two uncorrelated rules, both with standard error 0.2; estimates 1.0 and 0.98. Is the winner's "
                       r"conditional interval wide or narrow? And if the estimates were 1.0 and 0.2?")
        with self.voiceover(
            "Pause and predict. Two uncorrelated rules, each with standard error point two. Their estimates are one "
            "and point nine eight. Is the winner's conditional interval wide or narrow? And if the estimates were one "
            "and point two?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
