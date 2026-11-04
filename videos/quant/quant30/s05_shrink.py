from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, RMT_C, SAMPLE_C, SHRINK_C, fit_right, load

EST_COL = {"sample": SAMPLE_C, "LW identity": QC.OPTION, "LW const-corr": SHRINK_C, "RMT clipped": RMT_C,
           "nonlinear": GOOD}


class Shrink(VoiceoverScene):
    def construct(self):
        s = load("shrink")
        self.card()
        self.linear()
        self.constcorr()
        self.nonlinear()
        self.horse(s)
        self.intensity(s)
        self.question()

    def card(self):
        c = chapter_card(4, r"Shrinkage: Ledoit and Wolf", r"If the sample covariance is too extreme, how far should we "
                         r"pull it back, and toward what?", part=PART)
        with self.voiceover("Chapter four. The sample covariance spreads its eigenvalues too far apart. How far should we "
                            "pull it back, and toward what?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def linear(self):
        rows = [cmath(r"\hat\Sigma_\delta", r"=", r"\delta F + (1 - \delta) S", font_size=36, colors={r"\hat\Sigma_\delta": SHRINK_C}),
                cmath(r"\delta^*", r"=", r"\arg\min_\delta \mathbb E\|\hat\Sigma_\delta - \Sigma\|_F^2 = "
                      r"\frac{\mathbb E\|S - \Sigma\|_F^2}{\mathbb E\|S - F\|_F^2}", font_size=30, colors={r"\delta^*": HURDLE}),
                cmath(r"F = m I", r":", r"\hat\delta = \frac{\hat b^2}{\hat d^2},\ \ \hat b^2 = \tfrac{1}{T^2}\textstyle\sum_t "
                      r"\|x_t x_t^\top - S\|^2,\ \ \hat d^2 = \|S - mI\|^2", font_size=28)]
        whys = [why(r"a weighted average of the sample matrix $S$ and a simple target $F$: less variance, some bias"),
                why(r"the best weight in squared error, when $F$ is fixed: the sample matrix's own noise over its distance "
                    r"from the target"),
                why(r"Ledoit and Wolf (2004a): with the scaled identity as target, both are estimable from the data, and "
                    r"the estimate converges to the optimum as $N, T \to \infty$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Shrinkage. <bookmark mark='a'/> Take a weighted average of the sample matrix and a simple target that "
            "cannot be badly wrong, because it has few parameters. <bookmark mark='b'/> The best weight, in squared error, "
            "is the sample matrix's own noise divided by its distance from the target: the noisier the sample, the more "
            "we shrink. <bookmark mark='c'/> Olivier Ledoit and Michael Wolf showed in 2004 that with a scaled identity "
            "as the target, both pieces can be estimated from the same data, and the estimated weight converges to the "
            "best one as both N and T grow."
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

    def constcorr(self):
        cards = VGroup(
            desk_question(r"the constant-correlation target", r"keep every variance, set every correlation to the "
                          r"average: Ledoit and Wolf's `Honey, I shrunk the sample covariance matrix' (2004b), with its own "
                          r"estimated intensity", width=12.4, font_size=19),
            desk_question(r"a factor-model target", r"the covariance implied by a one-factor (market) model, Ledoit and "
                          r"Wolf (2003): the target is itself a structured estimate", width=12.4, font_size=19),
            desk_question(r"why targets work", r"they have few parameters, so little noise; their bias is the price, "
                          r"and the optimal intensity buys exactly as much bias as the noise it removes is worth",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Other targets. <bookmark mark='a'/> Keep every variance and set every correlation to the average: the "
            "constant-correlation target, from Ledoit and Wolf's paper with the memorable title. <bookmark mark='b'/> Or "
            "the covariance a one-factor market model implies. <bookmark mark='c'/> Every good target has few "
            "parameters, so little noise; its bias is the price, and the optimal intensity buys exactly as much bias as "
            "the noise it removes is worth."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nonlinear(self):
        rows = [cmath(r"\hat\Sigma", r"=", r"U\,\operatorname{diag}(d_1, \dots, d_N)\,U^\top", font_size=34,
                      colors={r"\hat\Sigma": GOOD}),
                cmath(r"d_i^{\text{or}}", r"=", r"u_i^\top\Sigma u_i", font_size=34, colors={r"d_i^{\text{or}}": HURDLE}),
                cmath(r"d_i", r"=", r"\frac{\lambda_i}{\big(\pi q\lambda_i \hat f(\lambda_i)\big)^2 + \big(1 - q - \pi q "
                      r"\lambda_i \mathcal H\hat f(\lambda_i)\big)^2}", font_size=30, colors={r"d_i": GOOD})]
        whys = [why(r"keep the sample eigenvectors $U$, choose new eigenvalues: the rotation-equivariant estimators"),
                why(r"the best such choice, if we knew $\Sigma$: the true variance along each sample eigenvector"),
                why(r"Ledoit and Wolf (2020): the oracle in the large-dimensional limit, from a kernel estimate of the "
                    r"eigenvalues' density $\hat f$ and its Hilbert transform; each eigenvalue gets its own shrinkage")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Linear shrinkage moves every eigenvalue by the same rule. The best known refinement does not. "
            "<bookmark mark='a'/> Keep the sample eigenvectors, and choose new eigenvalues. <bookmark mark='b'/> If we "
            "knew the truth, the best choice along each eigenvector would be the true variance in that direction. "
            "<bookmark mark='c'/> Ledoit and Wolf's analytical nonlinear shrinkage, of 2020, estimates exactly that "
            "oracle from the sample eigenvalues themselves, using random matrix theory: each eigenvalue gets its own "
            "amount of shrinkage."
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

    def horse(self, s):
        est = s["estimators"]
        Ts = ["60", "120", "240"]
        hx = [-4.4, -1.6, 0.9, 3.4]
        head = VGroup(label(r"estimator", font_size=18, color=GREY_B),
                      *[label(rf"$T = {t}$ months", font_size=18, color=GREY_B) for t in Ts])
        tab = VGroup(head)
        for e in est:
            tab.add(VGroup(label(e, font_size=19, color=EST_COL[e]),
                           *[MathTex(rf"{s['sims'][t][e]['gmv']:.2f}", font_size=26) for t in Ts]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.1 - 0.7 * j, 0])
        foot = wrapped_label(r"the true variance of each estimator's minimum-variance portfolio, as a multiple of the "
                             r"lowest possible; the truth is the industries' 1970--2020 covariance, 100 simulated windows each",
                             11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        s60 = s["sims"]["60"]
        with self.voiceover(
            "A horse race, again against a known truth. <bookmark mark='a'/> For each estimator, build the minimum-variance "
            "portfolio and measure its true variance, as a multiple of the lowest possible. <bookmark mark='b'/> With "
            f"five years of data, the sample matrix's portfolio has {s60['sample']['gmv']:.1f} times the minimum "
            f"variance. Shrinkage brings it to about {s60['LW const-corr']['gmv']:.1f}; the nonlinear estimator to "
            f"{s60['nonlinear']['gmv']:.2f}. The gap narrows as the window grows, and the Ledoit-Wolf estimators never "
            "lose. Clipping can: with twenty years of data it does worse than the plain sample matrix, "
            f"{s['sims']['240']['RMT clipped']['gmv']:.2f} against {s['sims']['240']['sample']['gmv']:.2f}, because it "
            "throws away real structure inside the noise band."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def intensity(self, s):
        x = np.asarray(s["dates"], float)
        x = x // 100 + ((x % 100) - 0.5) / 12
        ki, kc = np.asarray(s["k_identity"]), np.asarray(s["k_constcorr"])
        g = axes([x[0], x[-1]], [0, 0.6], x_length=9.0, y_length=4.0, xlabel=r"", ylabel=r"estimated shrinkage intensity",
                 xticks=[1980, 2000, 2020], yticks=[0, 0.3, 0.6], xfmt=lambda v: f"{v:.0f}", font_size=15
                 ).move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        li, lc = curve(ax, x, ki, QC.OPTION, stroke_width=3), curve(ax, x, kc, SHRINK_C, stroke_width=3)
        leg = legend([(QC.OPTION, r"toward the scaled identity"), (SHRINK_C, r"toward constant correlation")],
                     font_size=15).to_corner(UR, buff=0.4)
        with self.voiceover(
            "On the real data, with ten-year windows. <bookmark mark='a'/> The estimated intensity toward constant "
            f"correlation ranges from {kc.min():.2f} to {kc.max():.2f}: often a quarter or more of the weight on the target. "
            "Toward the identity it stays below "
            f"{ki.max():.2f}, because the identity ignores the market mode that every industry shares, so it is a worse "
            "target here. A good target is one that is close to the truth."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lc), Create(li), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"if the true covariance really is a multiple of the identity, what shrinkage intensity is best, "
                       r"and what does the estimate converge to?")
        with self.voiceover(
            "Pause and predict. If the true covariance really were a multiple of the identity, what intensity would be "
            "best?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
