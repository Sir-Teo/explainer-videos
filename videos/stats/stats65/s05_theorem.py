from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class Theorem(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. The conjecture becomes a theorem, and here is its proof.", 4, r"A theorem",
                            r"Proved on screen")
        self.statement()
        self.step1()
        self.step2()
        self.step3()
        self.corollary()
        self.example()
        self.upper()
        self.kl()
        self.remarks()

    def statement(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Theorem. <bookmark mark='b'/> Suppose the calibration pairs are independent draws from P, "
            "the test pair is drawn from Q, independent of them, and both share the conditional law of Y given X. "
            "<bookmark mark='c'/> Let w hat be a fixed positive weight function, independent of the calibration data, with "
            "finite mean under P. <bookmark mark='d'/> Then the weighted split-conformal set built with w hat satisfies: "
            "coverage under Q is at least one minus alpha minus the total variation distance between P sub w hat and the "
            "covariate law of Q.",
            [(r"(X_i, Y_i)_{i \le n}", r"\overset{\text{iid}}{\sim}", r"P, \ \ (X, Y) \sim Q, \ \ P_{Y \mid X} = Q_{Y \mid X}", 38),
             (r"\hat w", r":", r"\text{fixed, \ positive, \ } E_P \hat w < \infty", 40),
             (r"\Rightarrow", r"\ ", r"Q(Y \in \hat C_{\hat w}(X)) \ge 1 - \alpha - \mathrm{TV}(P_{\hat w}, Q_X)", 40),
             (r"\text{proof}", r":", r"\text{three steps}", 40)],
            [r"the setting", r"split sample", r"the claim", r"next"],
            colors=[(2, THESISC)])

    def step1(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Step one: the method is exact for the reweighted source. <bookmark mark='b'/> Define P "
            "sub w hat by its density, w hat of x over the mean of w hat, relative to P. <bookmark mark='c'/> Then w hat is, "
            "up to a constant that the weighted quantile ignores, exactly the likelihood ratio of P sub w hat to P. "
            "<bookmark mark='d'/> So by Tibshirani and colleagues' theorem, applied with P sub w hat as the target, a test "
            "pair whose covariate is drawn from P sub w hat, with the common conditional law of Y, is covered with "
            "probability at least one minus alpha.",
            [(r"\frac{dP_{\hat w}}{dP}(x)", r"=", r"\frac{\hat w(x)}{E_P \hat w}", 40),
             (r"\text{so}", r":", r"\hat w \propto dP_{\hat w}/dP \ \text{exactly}", 40),
             (r"\text{constants}", r":", r"\text{cancel in the weighted quantile}", 40),
             (r"\tilde Q = P_{\hat w} \otimes P_{Y \mid X}", r":", r"\tilde Q(Y \in \hat C(X)) \ge 1 - \alpha", 40)],
            [r"a definition", r"a likelihood ratio", r"normalization", r"Tibshirani et al. (2019)"],
            colors=[(3, HONC)])

    def step2(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Step two: condition on the calibration data. <bookmark mark='b'/> Given the n calibration "
            "pairs, the conformal set is a fixed function of x, so the event that the test pair is covered is a fixed set "
            "A of pairs x, y. <bookmark mark='c'/> Its probability under Q and under Q tilde differ by at most the total "
            "variation between the two joint laws. <bookmark mark='d'/> And because both share the conditional law of Y "
            "given X, that joint distance equals the distance between their covariate laws: the conditional part cancels "
            "inside the integral.",
            [(r"\text{given } D_n", r":", r"A = \{(x, y): y \in \hat C(x)\} \ \text{fixed}", 40),
             (r"|Q(A) - \tilde Q(A)|", r"\le", r"\mathrm{TV}(Q, \tilde Q)", 40),
             (r"\mathrm{TV}(Q, \tilde Q)", r"=", r"\tfrac12 \int |q_X - p_{\hat w}| \, dx \int p(y \mid x) \, dy", 40),
             (r"", r"=", r"\mathrm{TV}(Q_X, P_{\hat w})", 40)],
            [r"independence", r"Part 43's TV", r"common conditional", r"the covariates only"],
            colors=[(3, HONC)])

    def step3(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Step three: average. <bookmark mark='b'/> For every calibration sample, coverage under Q "
            "is at least coverage under Q tilde minus the distance. <bookmark mark='c'/> Take expectations over the "
            "calibration sample; the distance does not depend on it, because w hat was fixed in advance. <bookmark "
            "mark='d'/> Step one bounds the expected coverage under Q tilde below by one minus alpha. So coverage under Q is "
            "at least one minus alpha minus the distance. That completes the proof.",
            [(r"Q(A \mid D_n)", r"\ge", r"\tilde Q(A \mid D_n) - \mathrm{TV}(Q_X, P_{\hat w})", 40),
             (r"E_{D_n}", r":", r"\mathrm{TV} \text{ is constant, \ as } \hat w \text{ is fixed}", 40),
             (r"E\,\tilde Q(A \mid D_n)", r"\ge", r"1 - \alpha", 40),
             (r"Q(Y \in \hat C(X))", r"\ge", r"1 - \alpha - \mathrm{TV}(Q_X, P_{\hat w}) \quad \blacksquare", 40)],
            [r"pointwise", r"why splitting matters", r"step one", r"proved"],
            colors=[(3, THESISC)])

    def corollary(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two corollaries, both used in the study. <bookmark mark='b'/> Tempered Gaussian-tilt "
            "weights: the bound of chapter three, exactly. <bookmark mark='c'/> A logistic classifier on x, under a Gaussian "
            "mean shift, estimates the log ratio as a line with slope b hat; reweighting N of zero and one by it gives N of "
            "b hat and one, so the bound is one minus alpha minus two Phi of the absolute difference of b hat and mu over two, "
            "plus one. <bookmark mark='d'/> Consistency follows: if b hat tends to mu, coverage tends to at least one minus "
            "alpha, at the rate at which b hat converges.",
            [(r"\hat w = w^\lambda", r":", r"1 - \alpha - (2\Phi(|1 - \lambda||\mu|/2) - 1)", 40),
             (r"\text{logistic, \ slope } \hat b", r":", r"1 - \alpha - (2\Phi(|\hat b - \mu|/2) - 1)", 40),
             (r"\hat b \to \mu", r"\Rightarrow", r"\liminf \text{coverage} \ge 1 - \alpha", 40),
             (r"\text{rate}", r":", r"\text{loss} \approx |\hat b - \mu| \, \phi(0) = O_P(n^{-1/2})", 40)],
            [r"chapter 3's formula", r"the estimated case", r"consistency", r"a root-n loss"],
            colors=[(1, ESTC)])

    def remarks(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What the theorem does not say. <bookmark mark='b'/> It needs the weights fixed in "
            "advance. Estimating them on the calibration data itself, or cross-fitting, couples the weights to the scores; "
            "that case is not covered here. <bookmark mark='c'/> It is a lower bound only, and the doubts of chapter three "
            "suggest it may be far from tight. <bookmark mark='d'/> And it is close to known results: Barber and colleagues' "
            "2023 bounds for weighted methods, under any departure from exchangeability, are of the same kind. The contribution is the clean statement with one computable "
            "distance, and what the study shows about its tightness. Saying so is part of the work.",
            [(r"\text{needs}", r":", r"\hat w \text{ independent of calibration}", 40),
             (r"\text{only}", r":", r"\text{a lower bound}", 40),
             (r"\text{prior art}", r":", r"\text{close to Barber et al. (2023)}", 40),
             (r"\text{contribution}", r":", r"\text{one distance, \ and its tightness}", 40)],
            [r"cross-fitting: \ open", r"chapter 5", r"credit where due", r"honest scope"],
            colors=[(2, NAIVEC)])

    def example(self):
        st = {(x["mu"], x["gamma"], x["method"]): x for x in load("study")["rows"]}
        t = st[(1.0, 1.0, "tempered")]
        self.lad_voiceover(
            f"<bookmark mark='a'/> A worked number, to make the theorem concrete. <bookmark mark='b'/> A shift of one "
            f"standard deviation, and weights at half strength. The reweighted source is N of a half and one, the target N "
            f"of one and one. <bookmark mark='c'/> Their total variation is two Phi of a quarter, minus one: about "
            f"{0.9 - t['bound']:.3f}. So the guarantee is ninety percent minus that, "
            f"{100 * t['bound']:.1f} percent. <bookmark mark='d'/> The study, with noise strongly dependent on x, found "
            f"{100 * t['coverage']:.1f} percent. True, and pessimistic by {100 * (t['coverage'] - t['bound']):.0f} points.",
            [(r"\mu = 1, \ \lambda = 0.5", r":", r"P_{\hat w} = N(0.5, 1), \ \ Q = N(1, 1)", 40),
             (r"\mathrm{TV}", r"=", rf"2\Phi(0.25) - 1 = {0.9 - t['bound']:.3f}", 40),
             (r"\text{guarantee}", r":", rf"{100 * t['bound']:.1f}\%", 40),
             (r"\text{observed}", r":", rf"{100 * t['coverage']:.1f}\% \ \ (\gamma = 1)", 40)],
            [r"the setting", r"the distance", r"the bound", r"chapter 5"],
            colors=[(2, BOUNDC), (3, HONC)])

    def upper(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A lower bound alone is half a story. <bookmark mark='b'/> The same argument, run the "
            "other way, bounds coverage above: at most the reweighted source's coverage plus the distance. <bookmark "
            "mark='c'/> But the reweighted source's coverage can itself be far above one minus alpha, when a test point's "
            "weight is large enough to make the interval infinite, as chapter five will show. <bookmark mark='d'/> So the "
            "two-sided statement needs a bound on the largest normalized weight, the same overlap condition that Part "
            "thirty-six's propensity weights need. That refinement is left for the discussion.",
            [(r"\text{upper}", r":", r"\text{coverage} \le \tilde Q(\text{cover}) + \mathrm{TV}", 40),
             (r"\tilde Q(\text{cover})", r":", r"\text{can exceed } 1 - \alpha \text{ a lot}", 40),
             (r"\text{needs}", r":", r"\text{a bound on the largest weight}", 40),
             (r"\text{overlap}", r":", r"\text{Part 36's condition again}", 40)],
            [r"symmetry", r"infinite intervals", r"a refinement", r"Part 36"],
            colors=[(2, NAIVEC)])

    def kl(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A practical variant. Total variation is hard to estimate from samples; the "
            "Kullback-Leibler divergence often is not. <bookmark mark='b'/> Pinsker's inequality, from Part fifty, bounds "
            "total variation by the square root of half the KL divergence. <bookmark mark='c'/> So coverage is at least one "
            "minus alpha minus the square root of KL over two. <bookmark mark='d'/> For the tempered Gaussian weights, the "
            "KL divergence between N of lambda mu and N of mu is one minus lambda squared times mu squared over two, so the "
            "loss is at most the absolute value of one minus lambda times mu, over two: a line, a little looser than the "
            "exact curve, and easy to remember.",
            [(r"\text{Pinsker}", r":", r"\mathrm{TV} \le \sqrt{\mathrm{KL}/2}", 40),
             (r"\text{so}", r":", r"\text{coverage} \ge 1 - \alpha - \sqrt{\mathrm{KL}(Q_X \| P_{\hat w})/2}", 40),
             (r"\mathrm{KL}(N(\mu,1) \| N(\lambda\mu, 1))", r"=", r"(1 - \lambda)^2\mu^2/2", 40),
             (r"\text{loss}", r"\le", r"|1 - \lambda||\mu|/2", 40)],
            [r"estimable", r"Part 50", r"a KL corollary", r"easy to remember"],
            colors=[(3, BOUNDC)])
