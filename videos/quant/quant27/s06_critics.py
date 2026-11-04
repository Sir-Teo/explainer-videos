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
                why(r"Nagel (2025): when the kernel matrix is close to the identity, the forecast is a similarity-weighted "
                    r"average of the last twelve months' returns, scaled by their volatility: a kind of momentum")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "In 2025 Stefan Nagel reread the experiment. <bookmark mark='a'/> Write the forecast in its dual form: the "
            "next return is a combination of the twelve training returns, weighted through the inner products of the "
            "random features. <bookmark mark='b'/> With infinitely many features, those inner products become a kernel: "
            "a measure of how similar two months' predictors are. <bookmark mark='c'/> And with twelve observations in "
            "fifteen standardised dimensions, almost no two months are similar, so the kernel matrix is close to the "
            "identity, and the forecast is a similarity-weighted average of the last twelve months' returns, each "
            "divided by its volatility. That is not a discovery about dividend yields and credit spreads. It is a "
            "volatility-timed momentum strategy."
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
                 xticks=[], yticks=[], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, v in enumerate(sims):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(Rectangle(width=0.4, height=max(y1 - y0, 0.01), stroke_width=0, fill_color=COMPLEX,
                               fill_opacity=0.8).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]))
        side = VGroup(
            MathTex(rf"\text{{exact kernel, median}}:\ {sci(n['exact_median'], 1)}", font_size=24, color=COMPLEX),
            wrapped_label(r"with 12,000 random features the inner products between this month's predictors and the twelve "
                          r"training months' are almost all tiny: in fifteen standardised dimensions, no two months look "
                          r"alike, and the exact Gaussian kernel is nearly zero off the diagonal".replace("12,000", "12{,}000"),
                          3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Look inside. <bookmark mark='a'/> For each forecast, take the inner products between the current month's "
            "twelve thousand features and those of the twelve training months. They are all tiny. In fifteen "
            "standardised dimensions no two months look alike: the exact kernel between them is, in the median, "
            "essentially zero. So the forecast is mostly made of the training returns themselves, mixed by small and "
            "partly random weights."
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
            b = Rectangle(width=v * 9.0, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-1.2 + v * 4.5, 1.0 - 0.8 * i, 0])
            g.add(VGroup(label(nm, font_size=18, color=c).next_to([-1.3, 1.0 - 0.8 * i, 0], LEFT, buff=0.15), b,
                         MathTex(f"{v:.2f}", font_size=24).next_to(b, RIGHT, buff=0.12)))
        head = label(r"market timing, 1931--2020: Sharpe ratio", font_size=26).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"the complex forecast's correlation with the simple twelve-month average is "
                             rf"{n['corr_mom12']:.2f}. The simple strategy, with no predictors, no features and no "
                             r"tuning, does at least as well", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So compare the complex timer with the simple thing it resembles. <bookmark mark='a'/> Twelve thousand "
            "random features: a Sharpe ratio of point three three. The plain average of the last twelve months' "
            "volatility-scaled returns, no predictors, no features, no tuning: point four. Last month's return alone: "
            "point one three. The complex model's forecast is correlated with the simple average, and it does no "
            "better."
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
            g.add(VGroup(label(nm, font_size=19, color=c).move_to([-4.6, -0.4 - 0.85 * i, 0]), b,
                         MathTex(f"{v:+.2f}", font_size=26).next_to(b, RIGHT if v > 0 else LEFT, buff=0.12)))
        axis = Line([0, 0.1, 0], [0, -2.3, 0], color=GREY_C, stroke_width=1.5)
        foot = wrapped_label(rf"Sharpe ratios. Nagel's test: the complex model's forecast still correlates "
                             rf"{rv['corr_lag1']:+.2f} with last month's return, as if the world had momentum. It does "
                             r"not learn the structure of the data; it imposes one", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Nagel's decisive test. <bookmark mark='a'/> Keep the real predictors, but replace the returns with an "
            "artificial world in which they reverse: a good month tends to be followed by a bad one. "
            "<bookmark mark='b'/> A one-line reversal rule earns a Sharpe ratio above one. The twelve-thousand-feature "
            "model loses money, and its forecast still leans in the direction of last month's return. A model that "
            "learned from the data would have learned the reversal. This one did not learn; it imposed momentum, which "
            "happened to suit the real history."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(Create(axis), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
        self.add(illustration(r"simulated returns, the real Welch--Goyal predictors; the House's \texttt{ml.kmz\_timing}"))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self):
        cards = VGroup(
            desk_question(r"what survives", r"complexity is not automatically overfitting: the theory of benign "
                          r"overfitting is real, and the ridge keeps a huge model's forecasts small and stable", width=12.2,
                          font_size=20),
            desk_question(r"what does not", r"`more parameters than observations beats the simple models' is not "
                          r"established for market timing: here the gains are a simple strategy in disguise", width=12.2,
                          font_size=20),
            desk_question(r"the method", r"always ask what simple strategy a complex model's forecasts most resemble, "
                          r"and test the complex one against it, and in a world where it should fail", width=12.2,
                          font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where does that leave the virtue of complexity? <bookmark mark='a'/> Something survives: a huge model is "
            "not automatically overfitted, and the ridge keeps its forecasts small and stable, which is the real "
            "content of the theory. <bookmark mark='b'/> What does not survive, here, is the claim that more parameters "
            "than observations beat simple models at timing the market; the gains are a simple strategy in disguise. "
            "Other critiques followed, and the authors have replied. <bookmark mark='c'/> The method is the lasting "
            "lesson: ask what simple strategy a complex model most resembles, test it against that, and test it in a "
            "world where it ought to fail."
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
