from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


class Interpret(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimands()
        self.pdp()
        self.twin()
        self.extrapolate()
        self.loco()
        self.shapley()
        self.shap_bars()
        self.inference()
        self.lesson()

    def card(self):
        card = chapter_card(11, r"Interpretation as estimation", r"What does an explanation estimate?", lit=(2017,), part=PART)
        with self.voiceover("Chapter eleven. Interpretation as estimation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimands(self):
        rows = [
            cmath(r"\text{partial dependence}", r":", r"\bar f_j(v) = E_X\big[\hat f(v, X_{-j})\big]", font_size=30),
            cmath(r"\text{permutation}", r":", r"E\,L\big(Y, \hat f(X_j^{\pi}, X_{-j})\big) - E\,L\big(Y, \hat f(X)\big)", font_size=28),
            cmath(r"\text{LOCO}", r":", r"E\,L\big(Y, \hat f_{-j}(X_{-j})\big) - E\,L\big(Y, \hat f(X)\big)", font_size=28),
            cmath(r"\text{all three}", r":", r"\text{functionals of } \hat f \text{ and } P", font_size=30),
        ]
        rows[3][-1].set_color(CALC)
        whys = [why(r"Friedman (2001)"), why(r"Breiman (2001): \ scramble $x_j$"),
                why(r"leave covariate out: \ Lei et al. (2018)"), why(r"so each estimates something")]
        with self.voiceover(
            "<bookmark mark='a'/> Statisticians are used to asking what an estimator estimates. Interpretation methods "
            "deserve the same question. Friedman's partial dependence of the fitted function on feature j sets that feature "
            "to v for everyone, and averages the predictions over the other features. <bookmark mark='b'/> Breiman's "
            "permutation importance is the increase in loss when feature j is scrambled. <bookmark mark='c'/> Leave one "
            "covariate out, LOCO, refits the model without feature j, and measures how much the loss rises. <bookmark "
            "mark='d'/> Each is a functional of the fitted model and of the population. They are different functionals, "
            "and they answer different questions."
        ) as vo:
            intro=label('Interpretation methods target distinct model and population functionals',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pdp(self):
        d = load("interp")
        g = np.asarray(d["grid"], float)
        panels = VGroup()
        curves = []
        for k, (j, name, lo, hi) in enumerate([("3", r"$x_4$: \ the truth is $10 x_4$", 6, 22), ("2", r"$x_3$: \ the truth is $20(x_3 - \frac12)^2$", 10, 18)]):
            A = axes([0, 1], [lo, hi], x_length=5.0, y_length=3.8, xlabel=r"value", ylabel=r"average prediction",
                     xticks=[0, 0.5, 1], yticks=[lo, (lo + hi) // 2, hi], center=[-3.4 + 6.4 * k, 0.4, 0])
            t = label(name, font_size=22, color=GREY_A).next_to(A, UP, buff=0.15)
            tr = polyline(A.ax, g, d["true_pdp"][j], TRUEC, 3)
            fo = polyline(A.ax, g, d["pdp"][j], TREEC, 3.5)
            panels.add(VGroup(A, t))
            curves.append((tr, fo))
        foot = fit_rows(VGroup(
            label(r"gold: \ the truth's partial dependence; \ blue: \ the forest's", font_size=22),
            label(r"the forest's curves are flatter: \ partial dependence of $\hat f$, \ not of $\mu$", font_size=22, color=CALC),
        ), 12.0, 0.25, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A forest of two hundred trees on five hundred points from Friedman's function. On the "
            "left, its partial dependence on x four, whose true effect is a straight line, ten times x four. <bookmark "
            "mark='b'/> The forest's curve has the right slope in the middle and flattens at the ends, the edge bias of "
            "averaging over leaves that we saw in chapter two. <bookmark mark='c'/> On the right, x three, whose true "
            "effect is a deep parabola. The forest only half finds it: a shallow dish, rising at the ends, because a "
            "curve in a weaker feature is hard for splits to capture while stronger features compete for them. <bookmark mark='d'/> So partial "
            "dependence is an honest summary of the fitted model. Whether it describes nature depends on how good the "
            "model is, and, as the next example shows, on the other features."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(panels[0]), Create(curves[0][0]))
            vo.wait_until("b")
            self.play(Create(curves[0][1]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1]), Create(curves[1][0]), Create(curves[1][1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def twin(self):
        d = load("interp")
        perm, loco = np.asarray(d["perm"], float), np.asarray(d["loco"], float)
        idx = [0, 10, 1, 2, 3, 4, 5]
        names = [r"$x_1$", r"$x_1'$ (twin)", r"$x_2$", r"$x_3$", r"$x_4$", r"$x_5$", r"$x_6$ (noise)"]
        top = max(perm[idx].max(), loco[idx].max())
        A = axes([0, 7], [min(0,float(perm[idx].min()),float(loco[idx].min()))*1.1, top * 1.1], x_length=7.6, y_length=4.2, xlabel=r"", ylabel=r"rise in test MSE",
                 xticks=[], yticks=[0, round(top / 2), round(top)], center=[-1.8, 0.5, 0])
        ax = A.ax
        bp = bars_at(ax, np.arange(7) + 0.32, perm[idx], 0.34, CALC)
        bl = bars_at(ax, np.arange(7) + 0.68, loco[idx], 0.34, BOOSTC)
        labs = VGroup(*[label(n, font_size=18, color=MISSC if i == 1 else GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.2)
                        for i, n in enumerate(names)])
        side = fit_rows(VGroup(
            label(r"$x_1'$: \ a noisy copy of $x_1$, \ correlation about 0.97", font_size=20),
            label(r"gold: \ permutation importance", font_size=20, color=CALC),
            label(rf"$x_1$: \ {perm[0]:.1f}; \ its twin: \ {perm[10]:.1f}", font_size=20, color=CALC),
            label(r"purple: \ LOCO, \ refitting without each", font_size=20, color=BOOSTC),
            label(rf"$x_1$: \ {loco[0]:.1f}; \ its twin: \ {loco[10]:.1f}", font_size=20, color=BOOSTC),
        ), 3.8, 0.38, [5.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now give the forest a twin: an eleventh feature that is x one plus a little noise, "
            "correlated about point nine seven with it, and carrying no additional outcome information once the original "
            "feature is known. <bookmark mark='b'/> Permutation importance, <bookmark mark='c'/> computed on fresh "
            "test data, credits both: x one with " + say(perm[0], 1) +
            " and the twin with " + say(perm[10], 1) + ". <bookmark mark='d'/> LOCO, which refits the forest without each feature in turn, tells a different "
            "story: <bookmark mark='e'/> without x one the twin stands in for it, and the loss barely rises, and the "
            "same is true the other way round. These fitted-model loss differences are small. The original still has "
            "information missing from its noisy twin; finite-model LOCO need not equal the oracle population "
            "importance."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bp], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bl], lag_ratio=0.1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def extrapolate(self):
        rows = fit_rows(VGroup(
            label(r"permuting $x_1$ alone creates cases with $x_1 = 0.9$ and its twin $= 0.1$", font_size=26),
            label(r"such mismatched pairs are extremely rare under this design", font_size=26, color=MISSC),
            label(r"permutation importance measures the model's behaviour off the data", font_size=26, color=CALC),
            label(r"Hooker, \ Mentch \& Zhou (2021): \ `permute-and-predict' forces extrapolation", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why does permutation give the twin so much credit? Scrambling x one alone creates "
            "artificial cases in which x one is point nine and its twin point one. <bookmark mark='b'/> Such cases "
            "are extremely rare under this noisy-twin distribution, so the forest has little training support there; "
            "its predictions there are arbitrary. <bookmark mark='c'/> So permutation importance partly measures how "
            "the model behaves away from the data, which is a property of the model, not of the world. <bookmark "
            "mark='d'/> Giles Hooker, Lucas Mentch and Siyu Zhou made this argument in 2021 under the heading: please"
            " stop permuting features. Partial dependence plots extrapolate in exactly the same way when features are"
            " correlated."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def loco(self):
        rows = [
            cmath(r"\psi_j", r"=", r"E\big[(Y - \mu_{-j}(X_{-j}))^2\big] - E\big[(Y - \mu(X))^2\big]", font_size=28),
            cmath(r"", r"=", r"E\big[\big(\mu(X) - E[\mu(X) \mid X_{-j}]\big)^2\big]", font_size=30),
            cmath(r"\psi_j = 0", r"\iff", r"x_j \text{ adds nothing given the others}", font_size=30),
            cmath(r"\text{estimate}", r":", r"\text{split, \ refit, \ a CI for } \psi_j", font_size=30),
        ]
        rows[1][-1].set_color(BOOSTC)
        whys = [why(r"a population quantity"), why(r"the variance of $\mu$ not explained without $x_j$"),
                why(r"conditional importance"), why(r"Williamson, \ Gilbert, \ Simon \& Carone (2021)")]
        with self.voiceover(
            "<bookmark mark='a'/> LOCO's target can be written without any model at all. Its population version is the "
            "increase in the best possible mean squared error when feature j is withheld. <bookmark mark='b'/> It equals "
            "the expected squared difference between the regression function and its conditional mean given the other "
            "features. <bookmark mark='c'/> It is zero exactly when feature j adds nothing to the others: a conditional "
            "importance, which is why the twins both scored near zero. <bookmark mark='d'/> Being a population quantity, "
            "it can be estimated with a confidence interval, by sample splitting and refitting; Brian Williamson, Peter "
            "Gilbert, Noah Simon and Marco Carone showed in 2021 how to do so efficiently, with any machine-learning "
            "method inside."
        ) as vo:
            intro=label('Oracle LOCO measures additional conditional-mean information',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def shapley(self):
        rows = [
            cmath(r"v(S)", r"=", r"E\big[\hat f(x_S, X_{-S})\big]", font_size=32),
            cmath(r"\phi_j", r"=", r"\textstyle\sum_{S \not\ni j} \dfrac{|S|!\,(m - |S| - 1)!}{m!}\big(v(S \cup j) - v(S)\big)", font_size=28),
            cmath(r"\textstyle\sum_j \phi_j", r"=", r"\hat f(x) - E\,\hat f(X)", font_size=32),
            cmath(r"\text{cost}", r":", r"2^m \text{ coalitions: \ approximate}", font_size=32),
        ]
        rows[1][-1].set_color(CALC)
        whys = [why(r"the coalition $S$ fixed at $x$'s values"), why(r"Shapley (1953): \ average marginal contribution"),
                why(r"efficiency: \ the prediction is shared out"), why(r"Lundberg \& Lee (2017): \ SHAP")]
        with self.voiceover(
            "<bookmark mark='a'/> For a single prediction, the most popular explanation borrows from game theory. "
            "Treat the features as players. The value of a coalition S is the average prediction when the features in"
            " S are fixed at this case's values and the others are drawn from the population. <bookmark mark='b'/> "
            "Lloyd Shapley showed in 1953 that only one way of sharing out a game's value is symmetric, additive and "
            "gives nothing to a player who contributes nothing: with the efficiency axiom as well, each player’s "
            "average marginal contribution over all orders of joining. <bookmark mark='c'/> The shares add up exactly"
            " to this prediction minus the average prediction. <bookmark mark='d'/> With m features there are two to "
            "the m coalitions, so in practice they are approximated; Scott Lundberg and Su-In Lee's SHAP of 2017 made"
            " that fast, especially for trees."
        ) as vo:
            intro=label('Shapley efficiency allocates the value of a specified coalition game',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def shap_bars(self):
        d = load("interp")
        phi = np.asarray(d["phi"], float)
        x = d["x"]
        lo = min((np.cumsum(phi) + d["v0"]).min(), d["v0"]) - 3
        hi = max((np.cumsum(phi) + d["v0"]).max(), d["v0"]) + 2
        A = axes([0, 6], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"", ylabel=r"prediction",
                 xticks=[], yticks=[round(lo), round(d["v0"]), round(hi)], center=[-2.0, 0.3, 0])
        ax = A.ax
        base = DashedLine(ax.c2p(0, d["v0"]), ax.c2p(6, d["v0"]), color=GREY_B, stroke_width=2)
        cur = d["v0"]
        bars = VGroup()
        labs = VGroup()
        for k, p in enumerate(phi):
            y0, y1 = cur, cur + p
            r = Rectangle(width=0.7 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=max(abs(ax.c2p(0, y1)[1] - ax.c2p(0, y0)[1]), 0.02),
                          stroke_width=0, fill_color=BANDC if p > 0 else MISSC, fill_opacity=0.8)
            r.move_to(ax.c2p(k + 0.5, (y0 + y1) / 2))
            bars.add(r)
            labs.add(label(rf"$x_{{{k + 1}}} = {x[k]:.1f}$", font_size=18, color=GREY_A).next_to(ax.c2p(k + 0.5, lo), DOWN, buff=0.15))
            cur = y1
        endl = DashedLine(ax.c2p(0, cur), ax.c2p(6, cur), color=TREEC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"average prediction: \ {d['v0']:.1f}", font_size=22, color=GREY_B),
            label(rf"this case's five values: \ {d['vall']:.1f}", font_size=22, color=TREEC),
            label(rf"$\phi$: \ " + r", \ ".join(f"{p:+.1f}" for p in phi), font_size=22, color=CALC),
            label(r"exact: \ all 32 coalitions of the first five features", font_size=20, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Exact Shapley values for one case, over the first five features as players, computing all "
            "thirty-two coalitions with the forest. The average prediction over the chosen 120-case background is "
            + say(d["v0"], 1) + ". <bookmark mark='b'/> Each feature's share is a step up or down. This case has a large x "
            "four, which pushes the prediction up most, then x two and x one, through the sine of their product; x three, "
            "near the high end of its parabola, adds a little; x five, near its average, a small contribution. <bookmark mark='c'/> The "
            "steps end exactly at the prediction for this case's five values, " + say(d["vall"], 1) + ": the shares account for the whole difference for this five-player game; the other features, including "
            "the twin, are averaged over the background rather than fixed at the full case. <bookmark mark='d'/> Like"
            " partial dependence, the coalition values fill in the missing features independently of the ones fixed, "
            "so with correlated features they too ask the model about combinations that are very rare under their "
            "joint distribution."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), Create(base), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.4), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(endl), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def inference(self):
        rows = fit_rows(VGroup(
            label(r"an explanation of $\hat f$ is an estimate with its own sampling error", font_size=26),
            label(r"retrain on a bootstrap sample: \ the importances move (chapter one's Rashomon)", font_size=26, color=TREEC),
            label(r"estimands of the model or of nature? \ say which", font_size=26, color=CALC),
            label(r"of nature: \ LOCO and its relatives, \ with intervals", font_size=26, color=BOOSTC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So an explanation is an estimate, and has a sampling distribution. <bookmark mark='b'/> "
            "Retrain on a bootstrap sample and the importances move, as the trees' root splits moved in chapter one. "
            "<bookmark mark='c'/> Before reporting one, say whether it describes the model, which is fine for debugging the "
            "model, or nature, which is what a scientist wants. <bookmark mark='d'/> For nature, population quantities such "
            "as LOCO's, estimated with intervals, are the honest choice."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"and none of them is causal", font_size=28, color=MISSC),
            label(r"`the model uses $x_j$' \ $\neq$ \ `changing $x_j$ changes $y$'", font_size=28),
            label(r"next: \ the outro, \ and a model that told doctors asthma protects you", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And none of them is causal. <bookmark mark='b'/> That the model leans on a feature does "
            "not mean that changing the feature would change the outcome. <bookmark mark='c'/> The outro tells the story of "
            "a model that concluded asthma protects you from dying of pneumonia, and was right about the data."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
