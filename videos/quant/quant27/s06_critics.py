from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COMPLEX, GOOD, HURDLE, MOM, PART, ask, fit_right, illustration, load, sci


class Critics(VoiceoverScene):
    def construct(self):
        n = load("nagel")
        self.card()
        self.claim()
        self.kernel(n)
        self.compare(n)
        self.reversal(n)
        self.verdict()
        self.question()

    def card(self):
        c = chapter_card(5, r"The critics", r"What did the complex model actually learn?", lit=(2025,), part=PART)
        with self.voiceover("Chapter five. The critics, and what twelve thousand random features turn out to be doing."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def claim(self):
        rows = [cmath(r"\hat r_{t}", r"=", r"z(x_{t-1})^{\top}\,Z^{\top}\big(ZZ^{\top} + \lambda T I\big)^{-1} r", font_size=36,
                      colors={r"\hat r_{t}": COMPLEX}),
                cmath(r"\hat r_{t}", r"\xrightarrow[P \to \infty]{}", r"k(x_{t-1}, X)^{\top}\big(K + \lambda T I\big)^{-1} r",
                      font_size=36, colors={r"\hat r_{t}": COMPLEX}),
                cmath(r"\hat r_{t}", r"\approx", r"\tfrac{1}{1 + \lambda T}\textstyle\sum_{s=t-12}^{t-1} k(x_{t-1}, x_{s-1})\, r_s",
                      font_size=36, colors={r"\hat r_{t}": MOM})]
        whys = [why(r"the random-feature ridge forecast in its dual form: the next return is a combination of the 12 "
                    r"training returns, weighted through the features' inner products"),
                why(r"with infinitely many features the inner products become a kernel, here the Gaussian "
                    r"$k(x, y) = e^{-\gamma^2|x - y|^2/2}$: nothing but how similar two months' predictors are"),
                why('If the training Gram is approximately identity, the dual forecast simplifies to small similarity-weighted training returns. This does not imply equal positive momentum weights.')]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "Nagel's critique motivates inspecting the dual forecast. <bookmark mark='a'/> Random-feature ridge combines training outcomes through feature inner products and a regularised Gram inverse. <bookmark mark='b'/> With a fixed finite input set and a positive penalty, Gaussian feature inner products converge to their kernel and so does the ridge forecast. <bookmark mark='c'/> A near-identity training Gram simplifies that inverse. Tiny test similarities then imply small similarity-weighted forecasts; they do not by themselves imply equal positive momentum weights. Finite-feature randomness, scaling and the information set still matter."
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

    def kernel(self, n):
        sims = np.asarray(n["sims_mean"])
        g = axes([-0.6, 11.6], [0, max(sims.max() * 1.3, 0.02)], x_length=7.2, y_length=4.0,
                 xlabel=r"training month, oldest to most recent", ylabel=r"average $|$feature inner product$|$",
                 xticks=[0,3,6,9,11], yticks=list(np.linspace(0,max(sims.max()*1.3,.02),5)), yfmt=lambda v:f"{v:.3f}", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, v in enumerate(sims):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(Rectangle(width=0.4, height=max(y1 - y0, 0.01), stroke_width=0, fill_color=COMPLEX,
                               fill_opacity=0.8).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]))
        side = VGroup(
            MathTex(rf"\text{{exact kernel, median}}:\ {sci(n['exact_median'], 1)}", font_size=24, color=COMPLEX),
            wrapped_label('Saved absolute-inner-product averages by training lag. The exact-kernel median is small, but the maximum is not zero; a median does not describe every pair.'.replace("12,000", "12{,}000"),
                          3.6, 23, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The saved diagnostic averages absolute feature inner products by training lag. <bookmark mark='a'/> The exact Gaussian test-kernel median is {n['exact_median']:.6g}, while its maximum is {n['exact_max']:.3f}. A small median does not mean that every pair is dissimilar. Absolute averages also discard signs. These summaries diagnose a selected implementation and do not identify a universal momentum mechanism."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def compare(self, n):
        items = [(r"12,000 random features".replace("12,000", "12{,}000"), n["sr_rff"], COMPLEX),
                 (r"average of the last 12 months' scaled returns", n["sr_mom12"], MOM),
                 (r"last month's scaled return", n["sr_lag1"], HURDLE)]
        g = VGroup()
        for i, (nm, v, c) in enumerate(items):
            b = Rectangle(width=max(abs(v)*9.0,.01), height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-1.2 + v * 4.5, 1.0 - 0.8 * i, 0])
            g.add(VGroup(label(nm, font_size=22, color=c).next_to([-1.3, 1.0 - 0.8 * i, 0], LEFT, buff=0.15), b,
                         MathTex(f"{v:.2f}", font_size=24).next_to(b, RIGHT, buff=0.12)))
        head = label(r"market timing, 1931--2020: Sharpe ratio", font_size=34).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"the complex forecast's correlation with the simple twelve-month average is "
                             rf"{n['corr_mom12']:.2f}. The simple strategy, with no predictors, no features and no "
                             r"tuning in this implementation; a descriptive research comparison", 12.0, 24, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"Compare selected gross research strategies. <bookmark mark='a'/> The random-feature timer's Sharpe is {n['sr_rff']:.3f}, the twelve-month scaled-return average has {n['sr_mom12']:.3f}, and the one-month rule has {n['sr_lag1']:.3f}. The complex forecast's correlation with the twelve-month rule is {n['corr_mom12']:.3f}. These are different selected models, not proof of equivalence. A fair deployment comparison also requires matched tuning effort, information, position scaling and costs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reversal(self, n):
        rv = n["rev"]
        rows = VGroup(
            MathTex(rf"r_t = {rv['phi']:+.1f}\,r_{{t-1}} + \varepsilon_t", font_size=36, color=BAD),
            label(r"an artificial world in which returns reverse, with the real predictors unchanged", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.7)
        items = [(r"the reversal rule, $-r_{t-1}$", rv["sr_reversal"], GOOD),
                 (r"12,000 random features".replace("12,000", "12{,}000"), rv["sr_rff"], COMPLEX)]
        g = VGroup()
        for i, (nm, v, c) in enumerate(items):
            b = Rectangle(width=abs(v) * 4.0, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([v * 2.0, -0.4 - 0.85 * i, 0])
            g.add(VGroup(label(nm, font_size=22, color=c).move_to([-4.6, -0.4 - 0.85 * i, 0]), b,
                         MathTex(f"{v:+.2f}", font_size=26).next_to(b, RIGHT if v > 0 else LEFT, buff=0.12)))
        axis = Line([0, 0.1, 0], [0, -2.3, 0], color=GREY_C, stroke_width=1.5)
        foot = wrapped_label(rf"Fixed artificial example. The feature forecast correlates "
                             rf"{rv['corr_lag1']:+.2f} with last month's return, as if the world had momentum. It does "
                             r"not identify a learning failure: the reversal baseline receives a different artificial lagged input", 12.0, 24, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Now a fixed-seed artificial stress example. <bookmark mark='a'/> The target follows an autoregression with coefficient {rv['phi']:.1f}, while the feature model retains the real financial predictors. The reversal baseline directly receives the artificial target's lag, which is not among those predictors. <bookmark mark='b'/> Its saved Sharpe is {rv['sr_reversal']:.3f}, compared with {rv['sr_rff']:.3f} for the random-feature model. This mismatched information set prevents the conclusion that any successful learner should have discovered reversal. It is an illustration, not a decisive replication of the paper or a test of all high-dimensional learning."
        ) as vo:
            self.add(rows)
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(Create(axis), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
        self.add(illustration(r"simulated returns, the real Welch--Goyal predictors; the House's \texttt{ml.kmz\_timing}"))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self):
        cards = VGroup(
            desk_question(r"what survives", 'High dimension alone is inconclusive. Benign-overfitting and ridge results require stated distribution, scaling and signal assumptions.', width=12.2,
                          font_size=27),
            desk_question(r"what does not", 'A selected timing comparison and mismatched synthetic inputs cannot reject high-dimensional learning generally.', width=12.2,
                          font_size=27),
            desk_question(r"the method", r"always ask what simple strategy a complex model's forecasts most resemble, "
                          r"and test the complex one against it, and in a world where it should fail", width=12.2,
                          font_size=27),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Separate theory from this diagnostic. <bookmark mark='a'/> Large models are not automatically useless; risk depends on regularisation, scaling, signal and noise. <bookmark mark='b'/> A selected gross timing comparison and a mismatched synthetic baseline do not establish that all complexity gains are disguised momentum or that learning failed. <bookmark mark='c'/> The useful research question is which simple model captures a complex forecast's behaviour. Compare them at matched information and tuning budgets, then evaluate on genuinely independent data. No additional market strategy is run here."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a deep network's daily stock forecasts have a correlation of 0.8 with a one-month reversal signal. "
                r"Before paying for the network, what two tests would you run?")
        with self.voiceover(
            "Pause and predict. A deep network's daily stock forecasts have a correlation of point eight with a "
            "one-month reversal signal. Before paying for the network, what two tests would you run?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
