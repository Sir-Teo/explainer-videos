from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403

EST = (("no controls", GREY_B), ("linear controls", JUDGE), ("plug-in ML", NAIVE), ("double ML", CAUSE))


class DML(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Double machine learning", r"Can a flexible learner control for confounders without "
             r"biasing the effect?", "Chapter five. Double machine learning.", lit={1988: r"Robinson",
                                                                                    2018: r"Chernozhukov et al."},
             scale=("person", "nation"), horizon=("a year",))
        self.model()
        self.strips()
        self.why()

    def model(self):
        eq = VGroup(label(r"$y = \theta\, d + g(X) + \varepsilon$", font_size=38),
                    label(r"$d = m(X) + v$", font_size=38)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"$\theta$: \ the effect wanted \ (here 1)", font_size=23, color=CAUSE),
            label(r"$g$ and $m$: \ how five background variables move the outcome and the treatment \ "
                  r"(nonlinear, \ shared)", font_size=23, color=WHITE),
            label(r"entered linearly, \ the controls miss the curves, \ and the bias stays", font_size=23,
                  color=JUDGE),
            label(r"plugged in naively, \ a learner's own errors leak into $\hat\theta$", font_size=23, color=NAIVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Chernozhukov, \ Chetverikov, \ Demirer, \ Duflo, \ Hansen, \ Newey and Robins, \ "
                            r"Econometrics Journal 21(1) (2018); \ Robinson, \ Econometrica 56(4) (1988)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Machine learning predicts; most of economics wants a causal effect. Can the two be combined? Take the "
            "partially linear model. <bookmark mark='a'/> The outcome is theta times a treatment, plus some function "
            "g of background variables; and the treatment itself depends on those variables through another "
            "function, m. <bookmark mark='b'/> Theta, here one, is what we want. g and m are nuisances: we do not "
            "care about them, but we must get them right enough. On the Island they are curved, with "
            "interactions and thresholds, and they share variables, so the treatment is confounded. <bookmark "
            "mark='c'/> Ordinary least squares with the controls entered linearly misses the curves, and the bias "
            "stays. <bookmark mark='d'/> Replacing g with a machine-learning fit, and regressing what is left of y "
            "on d, sounds like the fix. It is not, because the learner's own errors are correlated with d."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.1))
                if k == 0:
                    self.play(FadeIn(rows[1], shift=RIGHT * 0.1))
        self.clear_scene()

    def strips(self):
        D = load("dml")
        ax = plane([0.8, 1.7], [-0.5, 3.5], center=RIGHT * 0.6 + DOWN * 0.2, x_length=7.6, y_length=4.8,
                   xticks=[0.8, 1.0, 1.2, 1.4, 1.6], yticks=[], xlabel=r"the estimate of $\theta$ \ (the truth is 1)",
                   xfmt=lambda v: f"{v:.1f}", font_size=15)
        truth = vline(ax, 1.0, -0.5, 3.5, TRUTHC)
        rows = VGroup()
        names = VGroup()
        rng = np.random.default_rng(64)
        for r, (k, c) in enumerate(EST):
            y0 = 3 - r
            draws = np.array(D[k]["draws"])
            rows.add(VGroup(*[dot(ax, x, y0 + rng.uniform(-0.25, 0.25), c, 0.045) for x in draws]))
            names.add(label(rf"{k}: \ {D[k]['mean']:.2f}", font_size=17, color=c).next_to(ax.ax.c2p(0.8, y0), LEFT,
                                                                                            buff=0.15))
        side = label(rf"double ML's 90\% intervals \\ cover the truth {100 * D['coverage']:.0f}\% of the time",
                     font_size=19, color=CAUSE).to_corner(DR, buff=0.5)
        tag = island_tag(rf"the Island: \ {D['reps']} samples of {D['n']:,}; \ gradient boosting; \ "
                         r"agora.learn.dml\_study".replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            f"Draw {D['reps']} samples of {D['n']:,} from the Island and estimate theta four ways. Each dot is one "
            f"sample. <bookmark mark='a'/> With no controls: about {D['no controls']['mean']:.2f}, the "
            f"confounding unchecked. <bookmark mark='b'/> With the controls entered linearly: "
            f"{D['linear controls']['mean']:.2f}, hardly better. <bookmark mark='c'/> With a machine-learning fit "
            f"plugged in naively: {D['plug-in ML']['mean']:.2f}, closer, and still clearly wrong. <bookmark "
            f"mark='d'/> With double machine learning: {D['double ML']['mean']:.2f}, centred on the truth, and its "
            f"ninety percent intervals cover the truth in {100 * D['coverage']:.0f} percent of samples."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(truth), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rows[k]], lag_ratio=0.01), FadeIn(names[k]),
                          run_time=1.2)
            self.play(FadeIn(side))
        self.clear_scene()

    def why(self):
        eq = label(r"$\hat\theta = \dfrac{\sum_i \big(d_i - \hat m(X_i)\big)\big(y_i - \hat\ell(X_i)\big)}"
                   r"{\sum_i \big(d_i - \hat m(X_i)\big)^2}, \qquad \ell(X) = E[y \mid X]$", font_size=32)
        eq.to_edge(UP, buff=0.8)
        cards = point_cards([
            (r"orthogonality", r"partial the controls out of both $y$ and $d$, \ as Robinson did in 1988: \ errors in "
             r"$\hat m$ and $\hat\ell$ then enter only as a product, \ so small errors stay small", CAUSE),
            (r"cross-fitting", r"fit the learners on one part of the sample and use them on another, \ then swap: \ "
             r"the learner never grades its own homework", ALGO),
            (r"what it buys", r"any learner fast enough \ (forests, \ boosting, \ the lasso, \ networks) \ for the "
             r"nuisances, \ and an ordinary standard error for $\theta$", TRUTHC),
            (r"what it does not", r"no design: \ if a confounder is unmeasured, \ double ML is as biased as OLS",
             HOLD),
        ], cols=2, width=12.8, font_size=19).next_to(eq, DOWN, buff=0.55)
        with self.voiceover(
            "Two ideas make it work. <bookmark mark='a'/> First, orthogonality. Partial the controls out of both "
            "the outcome and the treatment, then regress residual on residual, as Peter Robinson did for kernel "
            "estimators in 1988. The learners' errors then enter only as a product, so modest errors in each "
            "become a negligible error in theta. <bookmark mark='b'/> Second, cross-fitting: fit the learners on one "
            "part of the sample and use them on another, then swap, so a learner never grades its own homework. "
            "<bookmark mark='c'/> What it buys: any reasonably accurate learner for the nuisances, forests, "
            "boosting, the lasso or a network, and an ordinary standard error for theta. <bookmark mark='d'/> What "
            "it does not buy is a design. If a confounder is missing from X, double machine learning is exactly as "
            "biased as least squares."
        ) as vo:
            self.play(FadeIn(eq))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
