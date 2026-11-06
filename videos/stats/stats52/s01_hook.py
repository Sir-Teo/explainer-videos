from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.spectrum()
        self.scree()
        self.loadings()
        self.question()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1967,)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"a thousand people, \ five hundred measurements each, \ all pure noise", font_size=28),
            label(r"every variable independent, \ variance 1: \ no structure at all", font_size=26, color=GREY_A),
            label(r"run PCA: \ the top component's variance is 2.92, \ the bottom's 0.09", font_size=26, color=SPIKEC),
            label(r"a naive reading: \ a strong first factor, \ and near-collinear directions", font_size=26, color=BADC),
            label(r"both are artefacts of $p/n = 1/2$", font_size=26, color=BULKC),
        ), 12.4, 0.55, [0, -0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Take a thousand people and measure five hundred things about each, but make every "
            "measurement pure noise. <bookmark mark='b'/> Every variable is independent of every other, with variance one: "
            "there is no structure at all. <bookmark mark='c'/> Now run principal components. The top component has a variance "
            "of two point nine two, nearly three times what any direction truly has, and the bottom one a variance of point "
            "zero nine. <bookmark mark='d'/> A naive reading finds a strong first factor and a set of nearly collinear "
            "directions. <bookmark mark='e'/> Both are artefacts of having half as many variables as observations, and the "
            "Marchenko–Pastur law of Part fifty-one predicts them exactly."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def spectrum(self):
        d = load("hook")
        A = axes([0, 3.2], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of the sample covariance", ylabel=r"density",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lab = SpectrumBulk(ax)
        bars = lab.bars(d["edges"], d["hist"], color=BULKC)
        law = lab.law(d["x"], d["pdf"], color=TRUEC)
        one = lab.edge(1.0, 1.0, color=SPIKEC)
        lo, hi = d["mp"]
        e1, e2 = lab.edge(lo, 0.6, color=BADC), lab.edge(hi, 0.6, color=BADC)
        side = fit_rows(VGroup(
            label(r"$n = 1{,}000$, \ $p = 500$, \ $\Sigma = I$", font_size=22),
            label(r"gold: \ the truth, \ every eigenvalue 1", font_size=22, color=SPIKEC),
            label(rf"teal: \ the sample's 500, \ {d['ev_min']:.3f} to {d['ev_max']:.2f}", font_size=22, color=BULKC),
            label(rf"white: \ Marchenko--Pastur; \ red: \ edges {lo:.3f}, \ {hi:.3f}", font_size=22, color=TRUEC),
            label(r"the bulk is predicted, \ edge to edge", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The spectrum, drawn with this part's random-matrix lab, the SpectrumBulk. <bookmark "
            f"mark='b'/> The truth: all five hundred eigenvalues are exactly one. <bookmark mark='c'/> The sample's "
            f"five hundred eigenvalues spread from {say(d['ev_min'], 3)} to {say(d['ev_max'], 2)}. <bookmark mark='d'/> The "
            f"Marchenko–Pastur density, with edges at one minus root a half, squared, and one plus root a half, squared, "
            f"traces the histogram and predicts both extremes to two decimal places. <bookmark mark='e'/> Any analysis in high "
            f"dimension has to begin by knowing what noise alone does to a spectrum."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ the law exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(law), Create(e1), Create(e2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def scree(self):
        d = load("hook")
        rows = [[r"component"] + [str(k) for k in range(1, 6)],
                [r"sample variance"] + [f"{v:.2f}" for v in d["top5"]],
                [r"true variance"] + ["1.00"] * 5,
                [r"share of total, \ sample"] + [f"{100 * v / 500:.2f}\\%" for v in d["top5"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.4, colors=[GREY_B, SPIKEC, TRUEC, GREY_A])
        tab.move_to([0, 0.9, 0])
        foot = label(rf"the first component ``explains'' {100 * d['share_top']:.2f}\% \ against a true 0.20\%: \ {d['share_top'] / d['share_true']:.1f} times", font_size=24, color=BADC).move_to([0, -1.2, 0])
        foot2 = label(r"and its loadings point in a uniformly random direction", font_size=24, color=GREY_A).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The scree table a careless analyst would report. The first five components have sample "
            f"variances from {say(d['top5'][0], 2)} down to {say(d['top5'][4], 2)}, when every true variance is one. "
            f"<bookmark mark='b'/> The first component appears to explain {say(100 * d['share_top'], 2)} percent of the "
            f"variance, against a true share of point two percent, about {d['share_top'] / d['share_true']:.0f} times too "
            f"much. <bookmark mark='c'/> And its loadings point in a uniformly random direction: interpret them, and you are "
            f"interpreting noise."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def loadings(self):
        import numpy as np

        r = np.random.default_rng(5201)
        X = r.standard_normal((1000, 500))
        w, V = np.linalg.eigh(X.T @ X / 1000)
        v = V[:, -1] * np.sign(V[:, -1].sum())
        A = axes([0, 41], [-0.16, 0.16], x_length=7.4, y_length=4.4, xlabel=r"variable (the first 40 of 500)", ylabel=r"loading on component 1",
                 xticks=[1, 10, 20, 30, 40], yticks=[-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(j + 1, 0), ax.c2p(j + 1, v[j]), color=SPIKEC if abs(v[j]) > 0.09 else BULKC, stroke_width=6) for j in range(40)])
        sd = 1 / np.sqrt(500)
        b1 = DashedLine(ax.c2p(0, 2 * sd), ax.c2p(41, 2 * sd), color=TRUEC, stroke_width=2)
        b2 = DashedLine(ax.c2p(0, -2 * sd), ax.c2p(41, -2 * sd), color=TRUEC, stroke_width=2)
        big = int(np.sum(np.abs(v) > 0.09))
        top = np.argsort(-np.abs(v))[:3] + 1
        side = fit_rows(VGroup(
            label(r"the top eigenvector of the noise covariance", font_size=22),
            label(r"white: \ $\pm 2/\sqrt p$, \ a random unit vector's spread", font_size=22, color=TRUEC),
            label(rf"gold: \ {big} of 500 loadings above 0.09", font_size=22, color=SPIKEC),
            label(rf"``the factor is driven by'' variables {top[0]}, \ {top[1]}, \ {top[2]}", font_size=22, color=BADC),
            label(r"a uniformly random direction: \ nothing to interpret", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> And the loadings: the top eigenvector's entries for the first forty of the five hundred "
            f"variables. <bookmark mark='b'/> The white lines mark plus and minus two over root p, the spread of a uniformly "
            f"random unit vector's coordinates. <bookmark mark='c'/> The loadings scatter inside them, with {big} of the five "
            f"hundred above point oh nine. <bookmark mark='d'/> A report might say the first factor is driven by variables "
            f"{top[0]}, {top[1]} and {top[2]}. <bookmark mark='e'/> But this direction is uniformly random: by symmetry, "
            f"pure noise has no preferred direction, so the leading eigenvector is drawn from the whole sphere."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(b1), Create(b2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"so, \ when parameters outnumber observations:", font_size=28, color=GREY_A),
            label(r"how fast can a sparse regression be estimated? \ which variables can be found?", font_size=26, color=LASSOC),
            label(r"how well can a covariance matrix, \ or a low-rank matrix, \ be recovered?", font_size=26, color=BULKC),
            label(r"when is a spike in a spectrum visible at all?", font_size=26, color=SPIKEC),
            label(r"and how do you put an interval on anything?", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The questions of this part, for problems in which parameters outnumber observations. "
            "<bookmark mark='b'/> How fast can a sparse regression be estimated, and which of its variables can be found? "
            "<bookmark mark='c'/> How well can a covariance matrix, or a low-rank matrix with most entries missing, be "
            "recovered? <bookmark mark='d'/> When is a real spike in a spectrum visible at all? <bookmark mark='e'/> And how "
            "do you put a confidence interval on anything, after all that selection?"
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(32, r"the lasso finds sparse signals; \ cross-validation tunes it", r"that it works, \ by experiment",
                         r"chapters 1--3: \ oracle inequalities and support recovery, \ proved"),
            upgrade_card(31, r"PCA finds the directions of largest variance", r"$p$ fixed, \ $n \to \infty$",
                         r"chapters 6--10: \ spectra when $p/n$ is fixed: \ the BBP transition"),
            upgrade_card(51, r"concentration, \ random matrices, \ Gaussian widths", r"probability, \ with no model",
                         r"the tools behind every theorem here"),
        ]
        for c in cards:
            c.scale(0.86)
        stack = VGroup(*cards).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises come due. Part thirty-two showed the lasso finding sparse signals, but only "
            "by experiment; chapters one to three prove when and how fast it works. <bookmark mark='b'/> Part thirty-one's "
            "principal components assumed few variables and many observations; chapters six to ten study spectra when the "
            "ratio is fixed, and find a sharp threshold below which a signal is invisible. <bookmark mark='c'/> And Part "
            "fifty-one built the probability; here it becomes the proofs."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(stack[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 52", font_size=34, color=GREY_B), label(r"High-Dimensional Statistics", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the lasso's oracle inequality; \ restricted eigenvalues; \ support recovery and the primal--dual witness",
            r"decomposable regularizers; \ low-rank recovery and matrix completion; \ covariance estimation",
            r"Davis--Kahan; \ the Stieltjes transform and the semicircle; \ spikes, \ BBP, \ Tracy--Widom",
            r"sparse PCA and graphs; \ the debiased lasso, \ on real data",
        ], color=SPIKEC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 31, \ 32, \ 51").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.hdstat}, \ the random-matrix lab").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-two: high-dimensional statistics. <bookmark mark='b'/> We'll prove the lasso's "
            "oracle inequality under restricted eigenvalues, and find when it recovers the right variables; unify sparse, "
            "group and low-rank problems with decomposable regularizers; complete matrices and estimate covariances; bound "
            "eigenvector errors with Davis and Kahan; derive random-matrix laws from the Stieltjes transform; find the BBP "
            "transition for spikes and the Tracy–Widom law for the largest eigenvalue; meet sparse PCA and graphical models; "
            "and end with confidence intervals from the debiased lasso, on real data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
