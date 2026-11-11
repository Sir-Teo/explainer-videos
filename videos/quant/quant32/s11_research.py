from __future__ import annotations

import math
import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import GOOD, HURDLE, PART, TREND_C
from videos.quant.quant32.illustrations import gaussian_trend_theory, trend_paths


class Research(VoiceoverScene):
    def construct(self):
        t = gaussian_trend_theory()
        self.card()
        self.setup_()
        self.identity()
        self.mean(t)
        self.moments()
        self.third()
        self.diagonalise()
        self.finite(t)
        self.limit_proof()
        self.scope()
        self.diversify()
        self.filters()
        self.open_problems()
        self.question()

    def steps(self, rows, whys, top=2.5):
        return ladder(self, rows, [why(w) for w in whys], keep=len(rows), top=top,
                      x=-0.3, align_index=None, buff=0.62, edge=6.9)

    def card(self):
        c = research_card(r"Linear trend: identity, moments and limits",
                          r"Which conclusions are pathwise, and which need a probability model?", part=PART)
        with self.voiceover(
            "For the researcher. We can prove a useful shape of the linear trend rule without "
            "claiming a profitable trading strategy. The identity is pathwise. Its mean needs "
            "a model for dependence and drift. The exact finite-block distribution below needs "
            "independent, zero-mean Gaussian increments. Keeping these layers separate prevents "
            "an attractive quadratic picture from becoming an unsupported performance claim."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"x_t", r"=", r"\sum_{s<t}r_s,\qquad x_1=0", font_size=38),
                cmath(r"P", r"=", r"\sum_{t=1}^n x_t r_t", font_size=38),
                cmath(r"S", r"=", r"\sum_t r_t,\qquad Q=\sum_t r_t^2", font_size=36)]
        step = self.steps(rows, [
            r"one fixed block; reset to zero at its start; no forecast uses the current increment",
            r"position-times-increment profit, in squared increment units",
            r"arithmetic sum and raw sum of squares; no wealth compounding or demeaned variance"])
        with self.voiceover(
            "Start with a block of n scalar increments. Position at time t is the sum of "
            "earlier increments, with the first position zero. <bookmark mark='a'/> Profit "
            "is the sum of position times the next increment. Its units are squared increment "
            "units, unless a separate contract and capital normalisation are supplied. "
            "<bookmark mark='b'/> S is the arithmetic sum and Q the raw sum of squares. Q is "
            "not a sample variance with its mean subtracted. Resetting at every block, ignoring "
            "costs and using this unbounded linear position are essential to this exact object."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def identity(self):
        rows = [cmath(r"P", r"=", r"\sum_{s<t}r_s r_t", font_size=38),
                cmath(r"S^2", r"=", r"Q+2\sum_{s<t}r_s r_t", font_size=36),
                cmath(r"P", r"=", r"\tfrac12(S^2-Q)", font_size=44, colors={r"P": GOOD})]
        step = self.steps(rows, [
            r"substitute the lagged position: each unordered pair appears once",
            r"expand the square; this is algebra for every finite path",
            r"quadratic dependence conditional on Q; Q itself changes with the path"])
        with self.voiceover(
            "Substitute the position and every earlier increment multiplies every later one "
            "exactly once. <bookmark mark='a'/> Expanding S squared gives Q plus twice those "
            "cross products. <bookmark mark='b'/> Therefore P is half S squared minus half Q, "
            "for every finite path. No normality, independence or stationarity has entered. "
            "But this is not a vanilla straddle payoff, which is piecewise linear in its "
            "terminal underlying. Nor is Q a fixed premium paid at inception. The four unit "
            "rises and the single final jump both have S equal to four, yet their profits "
            "are six and zero because their Q values are four and sixteen."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def mean(self, t):
        rows = [cmath(r"\mathbb E P", r"=", r"\binom n2\mu^2+\sum_{k=1}^{n-1}(n-k)\gamma_k",
                      font_size=36),
                cmath(r"n=4,\ \gamma_k=\rho^k", r":",
                      r"6\mu^2+3\rho+2\rho^2+\rho^3", font_size=34),
                label(r"chosen (mu,rho): (0,0) -> 0; (0,.2) -> .688; (0,-.2) -> -.528",
                      font_size=22)]
        step = self.steps(rows, [
            r"stationary finite-second-moment increments; mean $\mu$ and autocovariance $\gamma_k$",
            r"chosen unit marginal variance and feasible AR(1) covariance",
            r"at mu=.1, rho=.2 the mean is .748; drift is not automatically negligible"])
        with self.voiceover(
            "For stationary increments with finite second moments, each cross product has "
            "expectation mu squared plus the autocovariance at its lag. Count n minus k "
            "pairs at lag k. <bookmark mark='a'/> The mean is the sum of those covariance "
            "terms plus n choose two times mu squared. Independent increments with nonzero "
            "drift therefore need not have zero expected profit. <bookmark mark='b'/> For a "
            "chosen four-period unit-variance AR one covariance, correlation parameter point "
            "two gives point six eight eight; minus point two gives minus point five two eight. "
            "Adding mean point one to the first case raises it to point seven four eight. "
            "These stipulated moments are not fitted market evidence."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def moments(self):
        rows = [cmath(r"r_t", r"=", r"\sigma z_t,\quad z_t\ {\rm iid}\ N(0,1)", font_size=36),
                cmath(r"Y=P/\sigma^2", r"=", r"\sum_{s<t}z_s z_t,\quad \mathbb EY=0", font_size=36),
                cmath(r"\mathbb E Y^2", r"=", r"\binom n2", font_size=40)]
        step = self.steps(rows, [
            r"now impose independence, zero mean and Gaussianity; n at least two",
            r"every product has zero mean; symmetry of individual increments is not symmetry of profit",
            r"in the squared sum only identical edges survive: each contributes $\mathbb E[z_s^2z_t^2]=1$"])
        with self.voiceover(
            "Now impose independent, zero-mean Gaussian increments with variance sigma squared. "
            "Normalise profit by sigma squared and call it Y. <bookmark mark='a'/> Every "
            "cross product has mean zero. To find its variance, expand Y squared. If two "
            "different edges share one endpoint, their other endpoints still appear once "
            "and the expectation vanishes. Disjoint edges vanish as well. "
            "<bookmark mark='b'/> Only the same edge paired with itself survives, with "
            "expectation one. There are n choose two edges. This counting proof also works "
            "for independent zero-mean unit-variance increments without Gaussianity."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def third(self):
        rows = [cmath(r"\mathbb E Y^3", r"=", r"6\binom n3=n(n-1)(n-2)", font_size=38),
                cmath(r"{\rm skew}(P)", r"=", r"\frac{2^{3/2}(n-2)}{\sqrt{n(n-1)}}", font_size=40),
                label(r"n=2: skew 0; n grows: skew approaches 2 sqrt(2), while E[P]=0",
                      font_size=24)]
        step = self.steps(rows, [
            r"under the Gaussian model, surviving triples of edges form triangles",
            r"divide the third central moment by variance to the power three-halves",
            r"positive skew and expected return answer different questions"])
        with self.voiceover(
            "In Y cubed, Gaussian odd moments vanish. A surviving triple of distinct "
            "edges forms a triangle: each of three vertices appears twice. There are "
            "six orders for each chosen triangle. <bookmark mark='a'/> This gives "
            "n times n minus one times n minus two. Divide by the variance to the "
            "three-halves power to obtain the displayed skewness. <bookmark mark='b'/> "
            "At two periods the skewness is zero. At large n it approaches two root two, "
            "despite zero mean profit at every n. More generally, non-Gaussian third "
            "moments can add repeated-edge terms, so the Gaussian formula must not be "
            "quoted as a universal consequence of independent returns."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def diagonalise(self):
        rows = [cmath(r"A", r"=", r"\tfrac12(\mathbf1\mathbf1^\top-I),\quad Y=z^\top A z", font_size=34),
                cmath(r"\operatorname{eig}(A)", r"=", r"(n-1)/2,\quad\underbrace{-1/2,\ldots,-1/2}_{n-1}", font_size=32),
                cmath(r"Y", r"\overset d=", r"\tfrac12[(n-1)U-V]", font_size=40)]
        step = self.steps(rows, [
            r"the matrix has zero diagonal and one-half off the diagonal",
            r"the all-ones direction and its orthogonal complement diagonalise A",
            r"U ~ chi-square(1), V ~ chi-square(n-1), independent under Gaussianity"])
        with self.voiceover(
            "An exact distribution follows by diagonalising the quadratic form. A is "
            "half the all-ones outer product minus half the identity. Its eigenvalue "
            "along the all-ones direction is n minus one over two. "
            "<bookmark mark='a'/> All n minus one orthogonal directions have eigenvalue "
            "minus one half. An orthogonal rotation preserves independent standard "
            "Gaussian coordinates. <bookmark mark='b'/> Thus Y equals in distribution "
            "half of n minus one times a one-degree chi-square, minus an independent "
            "n minus one degree chi-square. The random negative term matters at finite "
            "n. This is a distributional statement, not a traded option replication."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def finite(self, t):
        rows = VGroup()
        for q in t["rows"]:
            rows.add(label(rf"n={q['n']}: skew={q['skew']:.3f}; Pr(P>0)={100*q['win_probability']:.2f}\%",
                           font_size=25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        head = label(r"Exact analytic Gaussian reference; no simulated or fitted sample", font_size=27).to_edge(UP)
        formula = cmath(r"\Pr(P>0)", r"=", r"\Pr(F_{1,n-1}>1)", font_size=32).to_edge(DOWN)
        self.play(FadeIn(head), FadeIn(rows[0]))
        with self.voiceover(
            "The exact finite-block win probability is the upper tail of an F distribution "
            "with one and n minus one degrees of freedom, evaluated at one. "
            "<bookmark mark='a'/> The table evaluates that analytic expression and the "
            "skewness formula, from two through two hundred fifty-two periods. At two "
            "periods the win probability is one half. It falls toward thirty-one point "
            "seven percent as the block grows. <bookmark mark='b'/> No Monte Carlo "
            "experiment or market fit produced this table. A low winning fraction is "
            "compatible with zero mean because winning blocks can be larger. It does "
            "not establish a positive net edge after fees."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(formula))
        self.clear_scene()

    def limit_proof(self):
        rows = [cmath(r"\frac{P}{n\sigma^2}", r"=",
                      r"\tfrac12[(S/(\sigma\sqrt n))^2-Q/(n\sigma^2)]", font_size=34),
                cmath(r"S/(\sigma\sqrt n)", r"\Rightarrow", r"Z,\qquad Q/(n\sigma^2)\to_p1", font_size=36),
                cmath(r"P/(n\sigma^2)", r"\Rightarrow", r"\tfrac12(Z^2-1)", font_size=40)]
        step = self.steps(rows, [
            r"iid zero-mean increments with finite nonzero variance suffice for this weak limit",
            r"central limit theorem for S; law of large numbers for squared increments",
            r"continuous mapping and Slutsky; the limiting law has no atom at zero"])
        with self.voiceover(
            "The weak limit needs less than Gaussianity: independent, identically "
            "distributed, zero-mean increments with finite nonzero variance suffice. "
            "Divide the identity by n sigma squared. <bookmark mark='a'/> The central "
            "limit theorem sends S over sigma root n to a standard normal. The law "
            "of large numbers sends Q over n sigma squared to one. "
            "<bookmark mark='b'/> Continuous mapping and Slutsky give half of Z squared "
            "minus one. Because that limiting variable has no atom at zero, the win "
            "probability tends to the probability that absolute Z exceeds one. "
            "That is about thirty-one point seven three percent. Weak convergence "
            "alone does not guarantee convergence of third moments or skewness."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def scope(self):
        cards = VGroup(
            desk_question(r"moment existence", r"fat tails can leave profit's third moment undefined; a finite sample "
                          r"skewness does not establish that population moment", width=12.4, font_size=20),
            desk_question(r"implementation", r"signs, clipping, volatility forecasts, overlapping windows and transaction "
                          r"costs change the solved object", width=12.4, font_size=20),
            desk_question(r"observations", r"dropping missing days compresses time; pooling correlated markets does "
                          r"not create independent blocks", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Three limits matter in applications. Heavy-tailed increments can make "
            "the profit's third moment fail to exist, even when a computer reports "
            "a finite sample skewness. <bookmark mark='a'/> A sign rule, clipped "
            "position, volatility forecast or cost model changes the solved payoff. "
            "The theorem cannot simply be transferred to every trend fund. "
            "<bookmark mark='b'/> Missing observations also need a clock convention: "
            "dropping days makes a block count observations rather than calendar days. "
            "And pooling related markets does not turn their blocks into independent "
            "replications. These are model and inference questions, not cosmetic "
            "choices in plotting an empirical smile."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def diversify(self):
        rows = [cmath(r"{\rm skew}\left(\sum_{j=1}^K P_j\right)", r"=",
                      r"\frac{{\rm skew}(P_1)}{\sqrt K}", font_size=36),
                label(r"only for independent identically distributed profits with finite third moments",
                      font_size=22),
                label(r"chosen n=63, K=23: individual skew 2.761; equal-book skew about .576",
                      font_size=25)]
        step = self.steps(rows, [
            r"independent zero-mean profits: variances and third central moments add",
            r"cross third moments survive under dependence; zero correlation is insufficient",
            r"this mathematical aggregation is not an empirical multi-market result"])
        with self.voiceover(
            "For K independent identically distributed profits with finite third "
            "moments, variance grows like K and the third central moment also grows "
            "like K. <bookmark mark='a'/> Standardisation therefore reduces skewness "
            "by root K. Independence is stronger than zero correlation: mixed third "
            "moments can remain in an uncorrelated book. <bookmark mark='b'/> With "
            "the chosen Gaussian block length sixty-three and twenty-three independent "
            "copies, the analytic individual skewness is about two point seven six "
            "and the equal-book skewness about point five eight. This is a model "
            "calculation. It does not describe twenty-three actual markets or their "
            "crisis dependence."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def filters(self):
        rows = [cmath(r"P_w", r"=", r"\sum_{s<t}w_{t-s}r_s r_t", font_size=36),
                cmath(r"\mathbb E P_w", r"=", r"\sum_{k=1}^{n-1}(n-k)w_k(\gamma_k+\mu^2)",
                      font_size=34),
                cmath(r"{\rm Var}_0(P_w)", r"=", r"\sigma^4\sum_{k=1}^{n-1}(n-k)w_k^2", font_size=34)]
        step = self.steps(rows, [
            r"fixed deterministic lag filter; no estimated weights using the same observations",
            r"stationary finite-second-moment model for the expectation",
            r"variance reference: independent zero-mean increments; correlated alternatives have extra terms"])
        with self.voiceover(
            "A deterministic lag filter replaces equal weights by w at each lag. "
            "Stationarity gives its mean by weighting gamma k plus mu squared. "
            "<bookmark mark='a'/> Under an independent zero-mean variance reference, "
            "the same surviving-edge argument gives sigma to the fourth times "
            "the sum of n minus k times w k squared. <bookmark mark='b'/> For a "
            "zero-mean local alternative with specified autocovariances, maximising "
            "the mean divided by this reference standard deviation yields w k "
            "proportional to gamma k, by weighted Cauchy-Schwarz. This is a matched "
            "filter against a stated alternative. It is not a universal optimum "
            "under the alternative's full covariance, costs or estimation error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"which payoff after constraints?", r"Potters--Bouchaud (2005), Fung--Hsieh (2001): "
                          r"compare a prespecified constrained filter with its convexity benchmark", width=12.4, font_size=19),
            desk_question(r"which dependence survives costs?", r"Moskowitz--Ooi--Pedersen (2012), "
                          r"Lemperiere et al. (2014): estimate stable lags with selection and overlap accounted for",
                          width=12.4, font_size=19),
            desk_question(r"which crisis protection transfers?", r"Hurst--Ooi--Pedersen (2017): "
                          r"separate horizon, executable exposure and joint tail dependence", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Three research questions remain. First, how much of the quadratic "
            "payoff survives realistic constraints and a specified filter? The "
            "trend and lookback-option literature frames useful benchmarks, "
            "without identifying all implementations. <bookmark mark='a'/> Second, "
            "which dependence estimates survive costs and selection across horizons? "
            "A prespecified test and uncertainty for overlapping observations "
            "would make that question measurable. <bookmark mark='b'/> Third, when "
            "does protection transfer to a portfolio's crisis horizon? Long-run "
            "trend evidence motivates the question, but exposure timing and joint "
            "tails decide it. Each proposal needs evidence beyond this algebra."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('\\mathbb E[P]=0,\\quad {\\rm skew}(P)>0,\\quad n>2', font_size=34),
            MathTex('C\\geq0:\\quad \\mathbb E[P-C]=-\\mathbb E[C]\\leq0', font_size=34),
            MathTex('\\mu\\neq0,\\ {\\rm iid}:\\quad\\mathbb E[P]=\\binom n2\\mu^2', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Under iid zero-mean Gaussian increments, positive skew but E[P]=0: "
                       r"does convexity alone pay fees? What changes if mu is nonzero?")
        self.play(FadeIn(q))
        with self.voiceover(
            "Pause and predict. Independent zero-mean Gaussian increments give "
            "positive skew for blocks longer than two periods, yet expected gross "
            "profit is zero. Does convexity alone pay trading fees? No: a "
            "nonnegative fee reduces that expectation. With independent nonzero "
            "drift, the mean instead includes n choose two times mu squared. "
            "State the assumptions before naming the source of return."
        ):
            self.wait(0.2)
        self.clear_scene()
