from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class Replica(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. The replica method: the physicists' predictions, and their proofs.", 7,
                            r"The replica method", r"Predictions first, \ proofs later", lit=(2019,))
        self.idea()
        self.formula()
        self.bayes_amp()
        self.denoiser_worked()
        self.chart()
        self.hard()
        self.proofs()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Statistical physicists study the average free energy, the log of a partition function, "
            "of systems with random interactions. <bookmark mark='b'/> The replica trick computes the average of the log "
            "through the average of the partition function to the power n, for integer n, and then lets n go to zero. "
            "<bookmark mark='c'/> It is not rigorous, but it makes exact predictions, under an assumption called replica "
            "symmetry. <bookmark mark='d'/> For a Bayesian inference problem, the free energy is the log of the evidence, "
            "Part twenty-eight's marginal likelihood, and its derivatives give the minimum mean squared error.",
            [(r"\text{free energy}", r":", r"\tfrac1p E\log Z, \ \ Z = \text{a partition function}", 40),
             (r"\text{replica trick}", r":", r"E\log Z = \lim_{n \to 0}\tfrac1n\log E Z^n", 40),
             (r"\text{assumption}", r":", r"\text{replica symmetry}", 40),
             (r"\text{in statistics}", r":", r"Z = \text{the evidence}; \ \text{derivatives give the MMSE}", 38)],
            [r"spin glasses", r"Parisi, \ M\'ezard, \ Virasoro", r"the heuristic", r"Part 28's evidence"],
            colors=[(1, AMPC)])

    def formula(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For sparse linear regression with an i.i.d. prior, the replica-symmetric prediction reduces "
            "to a scalar problem: <bookmark mark='b'/> observe one coordinate of the signal in Gaussian noise of variance "
            "tau squared, and compute its minimum mean squared error, mmse of tau. <bookmark mark='c'/> The effective noise "
            "satisfies tau squared equals sigma squared plus mmse of tau over delta, the fixed point of a state evolution "
            "with the Bayes-optimal denoiser in place of soft thresholding. <bookmark mark='d'/> When several fixed points "
            "exist, the true one minimizes a potential, the replica free energy.",
            [(r"\text{scalar channel}", r":", r"Y_0 = X + \tau Z", 40),
             (r"\mathrm{mmse}(\tau)", r"=", r"E\big[(E[X \mid Y_0] - X)^2\big]", 40),
             (r"\tau^2", r"=", r"\sigma^2 + \mathrm{mmse}(\tau)/\delta", 40),
             (r"\text{several fixed points}", r":", r"\text{the potential's minimum wins}", 40)],
            [r"one coordinate", r"the Bayes risk", r"Bayes-optimal SE", r"the replica potential"],
            colors=[(2, AMPC)])

    def bayes_amp(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Bayes-optimal AMP runs that state evolution as an algorithm: replace the soft threshold by "
            "the posterior mean of a coordinate given its pseudo-observation. <bookmark mark='b'/> For a signal that is zero "
            "with probability nine tenths and plus or minus one otherwise, the posterior mean is a ratio of three Gaussian "
            "densities. <bookmark mark='c'/> AMP then reaches the fixed point that state evolution reaches from an "
            "uninformative start. <bookmark mark='d'/> When that is the potential's global minimum, AMP is Bayes-optimal: it "
            "achieves the minimum mean squared error that any method could.",
            [(r"\eta_t(r)", r"=", r"E[X \mid X + \tau_t Z = r]", 40),
             (r"\text{prior}", r":", r"0.9\,\delta_0 + 0.05\,\delta_{+1} + 0.05\,\delta_{-1}", 40),
             (r"\text{AMP reaches}", r":", r"\text{the fixed point from an uninformative start}", 38),
             (r"\text{if it is the global one}", r":", r"\text{AMP is Bayes-optimal}", 40)],
            [r"the posterior mean", r"three Gaussians", r"a specific fixed point", r"no method does better"],
            colors=[(3, PROPC)])

    def chart(self):
        d = load("bayes")
        R = d["rows"]
        dl = np.array([r["delta"] for r in R])
        A = axes([0.1, 0.6], [0, 0.1], x_length=7.4, y_length=4.4, xlabel=r"undersampling $\delta = n/p$", ylabel=r"mean squared error per coordinate",
                 xticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.05, 0.1], center=[-2.5, 0.2, 0])
        ax = A.ax
        las = polyline(ax, dl, [min(r["lasso"], 0.1) for r in R], SIMC, 4)
        bay = polyline(ax, dl, [min(r["bayes"], 0.1) for r in R], AMPC, 4)
        dt = DashedLine(ax.c2p(d["dt_delta"], 0), ax.c2p(d["dt_delta"], 0.1), color=SIMC, stroke_width=2)
        jump = next(r["delta"] for r in R if r["bayes"] < 1e-3)
        ba = DashedLine(ax.c2p(jump, 0), ax.c2p(jump, 0.1), color=AMPC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"signal: \ {int(100 * d['eps'])}\% of coordinates $\pm 1$; \ noise $\sigma^2 = 10^{{-4}}$", font_size=22),
            label(r"blue: \ the lasso, \ best threshold, \ by state evolution", font_size=22, color=SIMC),
            label(r"gold: \ Bayes-optimal AMP, \ the replica prediction it attains", font_size=22, color=AMPC),
            label(rf"recovery: \ Bayes-AMP from $\delta \approx {jump:.2f}$, \ the lasso from {d['dt_delta']:.2f}", font_size=22, color=PROPC),
            label(r"the prior's discreteness is worth undersampling", font_size=22, color=GREY_A),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The two errors, as functions of the undersampling ratio, for a signal that is ten percent "
            f"plus or minus one, in tiny noise. <bookmark mark='b'/> The lasso, tuned at its best threshold, recovers the "
            f"signal only past delta {say(d['dt_delta'], 2)}, the Donoho–Tanner point. <bookmark mark='c'/> Bayes-optimal AMP "
            f"has lower error everywhere, <bookmark mark='d'/> and recovers from delta about {say(jump, 2)}. <bookmark "
            f"mark='e'/> Knowing that the nonzero values are exactly plus or minus one saves about a tenth of the measurements: "
            f"the lasso cannot use it, a Bayesian denoiser can."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"state evolution: \ exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(las), Create(dt), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(bay), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(ba), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hard(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The replica formula predicts the minimum mean squared error of any method, efficient or "
            "not. <bookmark mark='b'/> In some regions, AMP's fixed point from an uninformative start is not the potential's "
            "global minimum: the information is there, but AMP does not find it. <bookmark mark='c'/> Physicists call this the "
            "hard phase, and conjecture that no polynomial-time algorithm can do better there. <bookmark mark='d'/> Evidence "
            "for the conjecture comes from low-degree polynomials and other restricted models of computation; a proof is "
            "open, and it is chapter ten's first problem.",
            [(r"\text{replica MMSE}", r":", r"\text{the best error of any method}", 40),
             (r"\text{hard phase}", r":", r"\text{AMP's fixed point} \ne \text{the global minimum}", 40),
             (r"\text{conjecture}", r":", r"\text{no efficient algorithm does better there}", 40),
             (r"\text{evidence}", r":", r"\text{low-degree polynomials; \ no proof}", 40)],
            [r"information-theoretic", r"information without computation", r"statistical-computational gaps", r"chapter 10"],
            colors=[(1, CLASSC), (2, CLASSC)])

    def proofs(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The predictions came first; the proofs came decades later. <bookmark mark='b'/> Jean "
            "Barbier, Florent Krzakala, Nicolas Macris, Léo Miolane and Lenka Zdeborová proved in 2019 the replica formula for "
            "generalized linear models with i.i.d. Gaussian designs, <bookmark mark='c'/> by interpolation: deform the problem "
            "continuously into the scalar channel and control the change in free energy. <bookmark mark='d'/> Earlier proofs "
            "covered the linear model, by Reeves and Pfister and by Barbier and colleagues; all confirm the physicists' "
            "formulas.",
            [(r"\text{first}", r":", r"\text{predictions, \ 1980s onwards}", 40),
             (r"\text{Barbier et al. (2019)}", r":", r"\text{the replica formula for GLMs, \ proved}", 38),
             (r"\text{method}", r":", r"\text{interpolation to the scalar channel}", 40),
             (r"\text{also}", r":", r"\text{the linear model: \ Reeves \& Pfister; \ Barbier et al.}", 38)],
            [r"heuristics", r"\emph{PNAS}", r"Guerra's idea", r"the physicists were right"],
            colors=[(1, PROPC)])

    def denoiser_worked(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Bayes denoiser in numbers. With noise level a half, suppose the pseudo-observation is 0.5, halfway between zero and one. <bookmark mark='b'/> The prior gives zero nine times the weight of each nonzero value, and the likelihood of 0.5 is the same under zero and under one, and much smaller under minus one: weights nought point nine, nought point oh five, and nearly nothing. <bookmark mark='c'/> So the posterior mean is about 0.05, shrinking hard toward zero. <bookmark mark='d'/> At an observation of 1.0 it rises to about 0.29: a smooth, prior-aware shrinkage that soft thresholding cannot imitate.",
            [('\\tau = 0.5, \\ r = 0.5', ':', '\\text{halfway between } 0 \\text{ and } 1', 40),
             ('\\text{weights}', ':', '0.9\\,\\phi(1) \\ : \\ 0.05\\,\\phi(1) \\ : \\ 0.05\\,\\phi(3)', 38),
             ('E[X \\mid r = 0.5]', '\\approx', '0.05', 40),
             ('E[X \\mid r = 1]', '\\approx', '0.29', 40)],
            ['a hard case', 'prior times likelihood', 'strong shrinkage', 'smooth, \\ prior-aware'],
            colors=[(2, AMPC), (3, AMPC)])
