from __future__ import annotations

import numpy as np
from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import GOOD, NET, PART, REF, axes, data_range


class Generator(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.gaussian_reverse()
        self.signature_scope()
        self.validation()

    def card(self):
        c = chapter_card(16, r"Market generators", r"What can an invented path establish?", lit=(2020,), part=PART)
        with self.voiceover("Chapter sixteen. Market generators. This chapter uses an analytical Gaussian illustration; it does not train on or inspect the sealed BTC window."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"x_t", r"=", r"\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\varepsilon,\quad\varepsilon\sim N(0,I)", font_size=33),
                cmath(r"\bar\alpha_t", r"=", r"\prod_{s=1}^t(1-\beta_s)", font_size=36),
                cmath(r"\min_\theta", r"\ ", r"\mathbb E\|\varepsilon-\varepsilon_\theta(x_t,t)\|^2", font_size=36),
                cmath(r"\varepsilon_{\rm opt}(x_t,t)", r"=", r"\mathbb E[\varepsilon\mid x_t,t]", font_size=34)]
        whys = [why(r"the forward marginal of a noisy 32-component return window"),
                why(r"200 steps, $\beta=10^{-4}$ to $0.02$: $\bar\alpha_{200}\approx0.132$, so signal amplitude is about $0.364$, not zero"),
                why(r"squared loss learns a conditional mean, not each window's exact hidden noise"),
                why(r"a Gaussian start approximates the terminal forward law only when the schedule makes that approximation adequate")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.5, buff=0.65, edge=6.9)
        with self.voiceover("A diffusion model adds Gaussian noise to a return window, then learns a reverse model. The forward marginal is one blend of data and noise. <bookmark mark='a'/> Its cumulative alpha is a product. In the legacy two-hundred-step schedule, that product is about 0.132: the original window still has amplitude 0.364. It has not become exactly pure noise. <bookmark mark='b'/> Squared noise-prediction loss is minimized by a conditional mean, not by reconstructing the particular hidden noise perfectly. <bookmark mark='c'/> A standard Gaussian start can therefore introduce a terminal-law approximation. Finite network error and reverse discretization add other errors. Ho, Jain and Abbeel's framework supplies a method, not a guarantee that a small trained network reproduces financial tails.") as vo:
            step(0)
            vo.wait_until("a"); step(1)
            vo.wait_until("b"); step(2)
            vo.wait_until("c"); step(3)
        self.wait(0.5)
        self.clear_scene()

    def gaussian_reverse(self):
        # Exact stationary-Gaussian conditional dynamics; no fitted market data.
        beta = np.linspace(1e-4, 0.02, 200)
        rng = np.random.default_rng(17016)
        x = rng.standard_normal((24, 32))
        snaps = {200: x.copy()}
        stages = [200, 150, 100, 60, 30, 10, 0]
        for t in range(199, -1, -1):
            x = np.sqrt(1 - beta[t]) * x + np.sqrt(beta[t]) * rng.standard_normal(x.shape)
            if t in stages:
                snaps[t] = x.copy()
        paths = {t: np.c_[np.zeros(24), np.cumsum(v, axis=1)] for t, v in snaps.items()}
        g = axes([0, 32], data_range(*paths.values(), zero=True), x_length=10.4, y_length=3.8,
                 xlabel=r"component / day", ylabel=r"cumulative standardized return", xticks=[0, 16, 32], yticks=[], font_size=16)
        g.shift(DOWN * 0.45)
        title = label(r"Exact reverse example: independent Gaussian windows", font_size=29).to_edge(UP, buff=0.35)
        eq = MathTex(r"x_{t-1}\mid x_t\sim N(\sqrt{\alpha_t}x_t,\,\beta_t I)", font_size=32).next_to(title, DOWN, buff=0.3)
        foot = wrapped_label(r"24 fixed-seed illustration paths; all saved values shown. No neural fit, BTC data or market-validation score.", 12.2, 20, GREY_A).to_edge(DOWN, buff=0.3)
        def fan(t):
            return VGroup(*[curve(g.ax, np.arange(33), p, NET, stroke_width=1.4).set_stroke(opacity=0.65) for p in paths[t]])
        lines = fan(200)
        badge = label(r"step 200", font_size=22, color=REF).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        with self.voiceover("Here is a reverse process we can justify exactly. Suppose the original window has thirty-two independent standard Gaussian coordinates. Every forward marginal is then standard Gaussian. Gaussian conditioning gives the reverse law shown above, so no fitted denoiser is needed. <bookmark mark='a'/> The twenty-four paths change as we step backward, but their marginal distribution stays Gaussian throughout. The fixed seed makes this illustration reproducible; no path is selected for looking realistic. <bookmark mark='b'/> At step zero these are still independent Gaussian returns. Attractive pictures cannot establish clustering, leverage, crash dependence or useful hedge performance. A generator can produce plausible-looking paths and still miss the features that matter to a particular book.") as vo:
            self.play(FadeIn(title), FadeIn(eq), FadeIn(g), FadeIn(lines), FadeIn(badge), FadeIn(foot))
            vo.wait_until("a")
            for t in stages[1:]:
                self.play(Transform(lines, fan(t)), Transform(badge, label(rf"step {t}", font_size=22, color=REF).move_to(badge)), run_time=1.4)
            vo.wait_until("b")
            self.play(Indicate(eq))
        self.wait(0.5)
        self.clear_scene()

    def signature_scope(self):
        rows = [cmath(r"\phi_m(X)", r"=", r"S_{\le m}(\operatorname{augment}(X))", font_size=36),
                cmath(r"d_m(P,Q)", r"=", r"\|\mathbb E_P\phi_m-\mathbb E_Q\phi_m\|", font_size=36),
                cmath(r"d_m(P,Q)=0", r"\not\Rightarrow", r"P=Q\quad(m<\infty)", font_size=38)]
        whys = [why(r"specify time, level, running variance or lead--lag augmentation"),
                why(r"empirical means are noisy; overlapping windows are dependent; tail clipping changes the law being compared"),
                why(r"identification results require the full suitable normalized signature and stated path-space assumptions; depth four is a finite feature diagnostic")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.5, buff=0.95, edge=6.9)
        with self.voiceover("Signatures offer another way to compare generated paths. First specify the augmentation: time, cumulative returns and running variance, or a lead-lag path. <bookmark mark='a'/> A finite-depth distance compares expected feature vectors. The empirical version contains sampling error, and overlapping windows are not independent replications. Winsorizing returns stabilizes a score, but compares transformed laws and can conceal tail mistakes. <bookmark mark='b'/> Identification theorems for a full appropriately normalized signature do not say that depth four identifies a path law. Different distributions can match finitely many expectations. Use signatures alongside tail behavior, volatility persistence, leverage, stress dependence and downstream losses; choose those diagnostics before seeing the test set.") as vo:
            step(0)
            vo.wait_until("a"); step(1)
            vo.wait_until("b"); step(2)
        self.wait(0.5)
        self.clear_scene()

    def validation(self):
        items = [(r"Fit and tune", r"research-window training data; separate chronological validation; train-only scaling"),
                 (r"Test once", r"a disjoint registered window; no overlapping fitted windows; dependence-aware uncertainty"),
                 (r"Stress the book", r"multiple generators, common payoff and costs, and declared tail scenarios"),
                 (r"This pass", r"BTC-through-2025 generator, reverse and cross-generator jobs were not executed; no scores presented")]
        cards = VGroup(*[desk_question(q, a, width=12.2, font_size=23) for q, a in items]).arrange(DOWN, buff=0.3)
        if cards.height > 7.2:
            cards.scale_to_fit_height(7.2)
        with self.voiceover("A useful evaluation separates fitting, tuning and a final chronological test. Scaling and clipping thresholds come from training alone. Overlapping windows require dependence-aware uncertainty. Choosing a generator after inspecting a test score turns that score into validation data. <bookmark mark='a'/> Test a hedger on the same payoff and costs across more than one generator and disjoint historical windows, with predeclared stress scenarios. Agreement on a few moments cannot certify the next crisis. <bookmark mark='b'/> The legacy jobs use BTC history through 2025; their cross-generator replay overlaps fitted history. They were not executed in this pass, and their scores are not presented. This analytical example preserves the series' sealed investing window. Next come production controls and the validation design.") as vo:
            self.play(FadeIn(cards[0]), FadeIn(cards[1]))
            vo.wait_until("a"); self.play(FadeIn(cards[2]))
            vo.wait_until("b"); self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
