from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class SBI(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Simulation-based inference, and posteriors that are too sure of themselves.", 10,
                            r"Simulation-based inference", r"When the likelihood is a simulator")
        self.setting()
        self.amortized()
        self.crisis()
        self.toy()
        self.chart()
        self.sbc()

    def setting(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Much of science now has a simulator instead of a likelihood: particle collisions, "
            "galaxy formation, epidemics, neurons. <bookmark mark='b'/> Given parameters, the simulator produces data; the "
            "probability of the data cannot be written down. <bookmark mark='c'/> Part twenty-seven's approximate Bayesian "
            "computation was the first answer: simulate, and keep the parameters whose output looks like the data. "
            "<bookmark mark='d'/> Neural networks gave a second: train a network on many simulated pairs to output the "
            "posterior directly, neural posterior estimation, which Kyle Cranmer, Johann Brehmer and Gilles Louppe surveyed "
            "in 2020.",
            [(r"\text{simulator}", r":", r"\theta \mapsto x, \ \ p(x \mid \theta) \text{ unknown}", 40),
             (r"\text{ABC}", r":", r"\text{keep } \theta \text{ whose } x \text{ is close}", 40),
             (r"\text{neural}", r":", r"q_\phi(\theta \mid x) \ \text{trained on } (\theta_i, x_i)", 40),
             (r"\text{amortized}", r":", r"\text{train once, \ apply to any } x", 40)],
            [r"likelihood-free", r"Part 27", r"neural posterior estimation", r"Cranmer, \ Brehmer \& Louppe (2020)"],
            colors=[(2, JUDGEC)])

    def amortized(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The training objective is honest in principle. <bookmark mark='b'/> Draw theta from the "
            "prior and x from the simulator, and maximize the average log of q of theta given x. <bookmark mark='c'/> The "
            "expected objective is maximized by the true posterior: it is a proper scoring rule, Part twenty-four's log "
            "score, averaged over the prior predictive. <bookmark mark='d'/> But with a finite number of simulations and a "
            "flexible network, the fit can overfit, and an overfitted density estimator can be too narrow: it has learned the "
            "training simulations' noise as signal.",
            [(r"\text{objective}", r":", r"\max_\phi \ \frac1N \sum_i \log q_\phi(\theta_i \mid x_i)", 40),
             (r"\text{population optimum}", r":", r"q = p(\theta \mid x)", 40),
             (r"\text{why}", r":", r"\text{the log score is proper}", 40),
             (r"\text{finite } N", r":", r"\text{overfit } \Rightarrow \text{ too narrow}", 40)],
            [r"simulate and fit", r"in the limit", r"Part 24", r"Part 19's overfitting"],
            colors=[(3, NAIVEC)])

    def crisis(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Joeri Hermans and colleagues checked, in 2022, under the title A Trust Crisis in "
            "Simulation-Based Inference? <bookmark mark='b'/> Across benchmark problems and methods, many posterior "
            "approximations were overconfident: their ninety percent credible regions contained the true parameter "
            "less than ninety percent of the time. <bookmark mark='c'/> They recommended checking coverage routinely, and "
            "preferring conservative methods, such as ensembles of estimators. <bookmark mark='d'/> Coverage is checkable "
            "because the simulator is available: simulate new pairs, and see how often the credible region contains the "
            "parameter that generated the data.",
            [(r"\text{audit}", r":", r"\text{Hermans et al. (2022)}", 40),
             (r"\text{found}", r":", r"\text{overconfident posteriors}", 40),
             (r"\text{advice}", r":", r"\text{check coverage; \ prefer conservative}", 40),
             (r"\text{possible because}", r":", r"\text{fresh simulations}", 40)],
            [r"TMLR (2022)", r"under-coverage", r"ensembles", r"Part 26's SBC"],
            colors=[(1, NAIVEC)])

    def toy(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A toy version, where the truth is known. <bookmark mark='b'/> Theta is standard normal, "
            "and the data are ten draws from a normal with mean theta; the true posterior is normal, with a simple "
            "formula. <bookmark mark='c'/> The approximation: regress theta on an eighth-degree polynomial of the sample "
            "mean, fitted on N simulations, and report a normal posterior with the regression's prediction as its mean and "
            "its residual variance as its variance. <bookmark mark='d'/> Two versions: the residual variance measured on "
            "the training simulations, and on a second, held-out set.",
            [(r"\theta", r"\sim", r"N(0, 1), \ \ x_{1:10} \mid \theta \sim N(\theta, 1)", 40),
             (r"q(\theta \mid x)", r"=", r"N(\hat m(\bar x), \ \hat s^2)", 40),
             (r"\hat m", r":", r"\text{degree-8 polynomial regression on } N \text{ simulations}", 38),
             (r"\hat s^2", r":", r"\text{in-sample, \ or held-out residuals}", 40)],
            [r"a conjugate truth", r"a Gaussian approximation", r"flexible", r"the one difference"],
            colors=[(3, HONC)])

    def chart(self):
        d = load("sbi")
        rows = d["rows"]
        lx = np.log10([r["n_sim"] for r in rows])
        A = axes([1.4, 3.7], [0.6, 1.0], x_length=7.2, y_length=4.4, xlabel=r"simulations $N$ (log scale)",
                 ylabel=r"coverage of the 90\% credible interval", xticks=list(np.log10([30, 120, 500, 4000])),
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[0.6, 0.7, 0.8, 0.9, 1.0], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 center=[-2.4, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(1.4, 0.9), ax.c2p(3.7, 0.9), color=GREY_B, stroke_width=2)

        def line(key, color):
            ys = [r[key] for r in rows]
            return VGroup(polyline(ax, lx, ys, color, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(lx, ys)])
        ins, ho = line("insample", NAIVEC), line("heldout", HONC)
        r0 = rows[0]
        side = side_groups([
            [(r"grey dashes: \ the promised 90\%", GREY_B), (r"20 fits $\times$ 2{,}000 tests per $N$", GREY_A)],
            [(rf"red: \ in-sample variance", NAIVEC), (rf"{100 * r0['insample']:.0f}\% at $N = {r0['n_sim']}$", NAIVEC)],
            [(rf"green: \ held-out RMS heuristic", HONC), (rf"{100 * r0['heldout']:.0f}\%: \ conservative", HONC)],
            [(r"both reach 90\% as $N$ grows", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Coverage of the ninety percent credible interval, against the number of training simulations, over fresh parameters and data. <bookmark mark='b'/> With the in-sample residual variance, the posterior is overconfident when simulations are scarce: {100 * r0['insample']:.0f} percent coverage with {r0['n_sim']} simulations. <bookmark mark='c'/> With the variance measured on held-out simulations, coverage is {100 * r0['heldout']:.0f} percent: above nominal in this experiment. Both versions now share the same fitted mean and test draws; only the residual-variance sample differs. Held-out RMS residuals do not guarantee a calibrated conditional posterior or conservative coverage in every problem. <bookmark mark='d'/> Both converge to ninety percent as the simulations grow. This toy isolates one training-error mechanism; it does not explain every failure in the cited SBI study. Coverage here averages over the prior predictive, rather than being guaranteed at each fixed parameter."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ins[0]), FadeIn(VGroup(*ins[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ho[0]), FadeIn(VGroup(*ho[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def sbc(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The general check is Part twenty-six's simulation-based calibration. <bookmark mark='b'/> Draw theta from the prior, simulate x, compute the approximate posterior, and record the rank of the true theta among posterior draws. <bookmark mark='c'/> Correct posterior draws give uniform ranks under the SBC experiment. U shapes, humps and slopes can suggest spread or bias errors, but do not uniquely diagnose them. Uniform ranks are necessary and not sufficient: returning the prior while ignoring data can also pass basic SBC. <bookmark mark='d'/> And when the simulator itself is wrong about the world, no calibration on simulations can reveal it: Part twenty-eight's model checking against real data is still required.",
            [(r"\text{SBC}", r":", r"\text{rank of the true } \theta \text{ among draws}", 40),
             (r"\text{calibrated}", r":", r"\text{uniform ranks}", 40),
             (r"\text{shapes}", r":", r"\text{U: \ overconfident; \ hump: \ under}", 40),
             (r"\text{misspecified simulator}", r":", r"\text{invisible to SBC}", 40)],
            [r"Talts et al. (2018)", r"Part 26", r"diagnosis", r"Part 28"],
            colors=[(3, NAIVEC)])
