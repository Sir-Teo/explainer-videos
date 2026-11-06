from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Knockoffs(VoiceoverScene):
    def construct(self):
        self.card()
        self.fixed_x()
        self.model_x()
        self.flip()
        self.compare_x()
        self.martingale()
        self.chart()
        self.robust()

    def card(self):
        card = chapter_card(6, r"Knockoff theory", r"Fake variables that keep the selection honest", lit=(2015,), part=PART)
        with self.voiceover("Chapter six. Knockoff theory: fake variables that keep the selection honest."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fixed_x(self):
        rows = [
            cmath(r"\text{the goal}", r":", r"\text{FDR} \le q \text{ in finite samples}", font_size=36),
            cmath(r"\tilde X", r":", r"\tilde X'\tilde X = X'X, \ \ X'\tilde X = X'X - \mathrm{diag}(s)", font_size=30),
            cmath(r"W_j", r"=", r"|\hat\beta_j| - |\hat\beta_{\tilde j}| \ \text{ from one lasso on } [X, \tilde X]", font_size=34),
            cmath(r"\hat S", r"=", r"\{j: W_j \ge T\}, \ \ T = \min\Big\{t: \frac{1 + \#\{W_j \le -t\}}{\#\{W_j \ge t\} \vee 1} \le q\Big\}", font_size=30),
        ]
        rows[1][-1].set_color(SPLITC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"Barber \& Cand\`es (2015)"), why(r"same geometry, \ no signal"), why(r"a contest: \ original vs fake"), why(r"knockoff$+$")]
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-three met knockoffs as a method; here is why they work. Rina Foygel Barber and "
            "Emmanuel Candès wanted variable selection with false discovery rate control in finite samples. <bookmark "
            "mark='b'/> Their idea: build a fake copy of every variable, a knockoff, whose correlations with everything "
            "mimic the original's, but which has no effect on the outcome. <bookmark mark='c'/> Fit one lasso on originals "
            "and knockoffs together, and score each variable by how much larger its coefficient is than its knockoff's. "
            "<bookmark mark='d'/> Select the variables whose score exceeds a threshold T, chosen as the smallest t at which "
            "the estimated false discovery proportion, one plus the number of scores below minus t, over the number above "
            "t, is at most q."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def model_x(self):
        rows = [
            cmath(r"\text{model-X}", r":", r"(X, \tilde X)_{\text{swap}(S)} \overset{d}{=} (X, \tilde X) \ \text{ for every } S, \ \ \tilde X \perp Y \mid X", font_size=30),
            cmath(r"\text{assumes}", r":", r"\text{the law of } X \text{ is known; \ nothing about } Y \mid X", font_size=34),
            cmath(r"\text{Gaussian } X", r":", r"\tilde X \mid X \sim N\big(X - X\Sigma^{-1}D, \ 2D - D\Sigma^{-1}D\big)", font_size=32),
            cmath(r"\text{so}", r":", r"\text{any } n, \ p > n \text{ allowed, \ any model for } Y", font_size=34),
        ]
        rows[0][-1].set_color(SPLITC)
        whys = [why(r"Cand\`es, \ Fan, \ Janson \& Lv (2018)"), why(r"the burden moves to $X$"), why(r"Part 33's construction"), why(r"the trade")]
        with self.voiceover(
            "<bookmark mark='a'/> Candès, Yingying Fan, Lucas Janson and Jinchi Lv's model-X knockoffs turn the requirement "
            "into a distributional one: swapping any set of variables with their knockoffs leaves the joint law of the "
            "pair unchanged, and the knockoffs are generated without looking at Y. <bookmark mark='b'/> That needs the law of "
            "the covariates to be known, but nothing at all about how Y depends on them. <bookmark mark='c'/> For Gaussian "
            "covariates, the knockoffs are drawn from a conditional normal, the construction of Part thirty-three. <bookmark "
            "mark='d'/> Any sample size, more variables than observations, and any model for the outcome are allowed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def flip(self):
        rows = [
            cmath(r"\text{swap a null } j", r":", r"X_j \leftrightarrow \tilde X_j \ \Rightarrow \ W_j \to -W_j, \ \text{others unchanged}", font_size=32),
            cmath(r"\text{exchangeability}", r"\Rightarrow", r"\text{null signs: \ fair coins, \ given } |W|", font_size=32),
            cmath(r"\#\{\text{null } W_j \ge t\}", r"\approx", r"\#\{\text{null } W_j \le -t\} \le \#\{W_j \le -t\}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{the numerator of } T\text{'s ratio estimates the false discoveries}", font_size=32),
        ]
        rows[1][-1].set_color(SPLITC)
        whys = [why(r"the antisymmetry of $W$"), why(r"the sign-flip property"), why(r"negatives mirror false positives"), why(r"conservatively")]
        with self.voiceover(
            "<bookmark mark='a'/> The key property. Swapping a null variable with its knockoff simply flips the sign of its "
            "score and leaves every other score alone. <bookmark mark='b'/> Since the swap leaves the joint law unchanged, "
            "the signs of the null scores are independent fair coins, given their magnitudes. <bookmark mark='c'/> So the "
            "number of null scores above t is matched, on average, by the number below minus t, and that is at most the "
            "number of all scores below minus t. <bookmark mark='d'/> The numerator of the threshold's ratio is therefore a "
            "conservative estimate of the number of false discoveries."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare_x(self):
        rows = [
            cmath(r"\text{fixed-X}", r":", r"\text{no model for } X; \ \text{Gaussian linear model for } Y; \ n \ge 2p", font_size=32),
            cmath(r"\text{model-X}", r":", r"\text{the law of } X \text{ known; \ any model for } Y; \ \text{any } n", font_size=34),
            cmath(r"\text{statistics } W", r":", r"\text{anything antisymmetric}", font_size=32),
            cmath(r"\text{power}", r":", r"\text{depends on } s \text{ in } \tilde X: \ \text{knockoffs far from the originals help}", font_size=32),
        ]
        rows[3][-1].set_color(SPLITC)
        whys = [why(r"Barber \& Cand\`es (2015)"), why(r"Cand\`es et al. (2018)"), why(r"the flexibility"), why(r"equicorrelated or SDP")]
        with self.voiceover(
            "<bookmark mark='a'/> The two frameworks trade assumptions. Fixed-X knockoffs need no model for the "
            "covariates, but a Gaussian linear model for the response and at least twice as many observations as "
            "variables. <bookmark mark='b'/> Model-X knockoffs need the covariates' law, but nothing about the "
            "response, and any sample size. <bookmark mark='c'/> In both, the score can be anything antisymmetric in "
            "an original and its knockoff: lasso coefficients, random-forest importances, or a neural network's. "
            "<bookmark mark='d'/> Power depends on how different the knockoffs are from the originals, set by the "
            "constant s, chosen to be as large as the covariance allows."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def martingale(self):
        rows = [
            cmath(r"M(t)", r"=", r"\frac{V^+(t)}{1 + V^-(t)}, \ \ V^\pm(t) = \#\{\text{null } j: \pm W_j \ge t\}", font_size=34),
            cmath(r"\text{as } t \text{ grows}", r":", r"M \text{ is a supermartingale}", font_size=32),
            cmath(r"T \text{ a stopping time}", r"\Rightarrow", r"E\,M(T) \le E\,M(0) \le 1", font_size=36),
            cmath(r"\text{FDR}", r"=", r"E\Big[\frac{V^+(T)}{\#\{W \ge T\} \vee 1}\Big] \le q\,E\,M(T) \le q \qquad \blacksquare", font_size=32),
        ]
        rows[1][-1].set_color(SPLITC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"false positives over (one plus) mirrors"), why(r"a hypergeometric calculation"), why(r"optional stopping, \ Part 44"), why(r"by the definition of $T$")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof that the false discovery rate is at most q is a martingale argument. Let M of t be "
            "the number of null scores above t, divided by one plus the number below minus t. <bookmark mark='b'/> As t "
            "increases, null scores drop out one at a time, each from a side chosen by a fair coin, and a short calculation "
            "shows M is a supermartingale. <bookmark mark='c'/> The threshold T is a stopping time for this process, so by "
            "optional stopping, the expected value of M at T is at most its starting value, which is at most one: problem two "
            "of the qualifying exam, now doing real work. <bookmark mark='d'/> And by the definition of T, the false "
            "discovery proportion at T is at most q times M of T. Taking expectations, the rate is at most q."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("knockoffs")
        fdp = np.asarray(d["fdp"])
        bins = np.linspace(0, 0.4, 9)
        h, _ = np.histogram(fdp, bins)
        A = axes([0, 0.4], [0, max(h) + 2], x_length=7.4, y_length=4.4, xlabel=r"false discovery proportion of one run", ylabel=r"runs",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 10, 20], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(b1, 0)[0] - ax.c2p(b0, 0)[0] - 0.04, height=max(ax.c2p(0, c)[1] - ax.c2p(0, 0)[1], 0.001),
                                  stroke_width=0, fill_color=SPLITC, fill_opacity=0.8).move_to([(ax.c2p(b0, 0)[0] + ax.c2p(b1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, c)[1]) / 2, 0])
                        for b0, b1, c in zip(bins[:-1], bins[1:], h)])
        q = DashedLine(ax.c2p(d["q"], 0), ax.c2p(d["q"], max(h) + 2), color=HYBC, stroke_width=3)
        m = DashedLine(ax.c2p(d["fdr"], 0), ax.c2p(d["fdr"], max(h) + 2), color=SELC, stroke_width=3)
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ $p = {d['p']}$ AR(1) Gaussian covariates, \ {d['k']} real", font_size=22),
            label(rf"teal: \ 40 runs of model-X knockoff$+$, \ $q = {d['q']:g}$", font_size=22, color=SPLITC),
            label(rf"gold: \ the average, \ the FDR: \ {d['fdr']:.3f}", font_size=22, color=SELC),
            label(rf"power: \ {100 * d['power']:.0f}\% of the real variables found", font_size=22, color=HYBC),
            label(rf"$M(T)$ averaged {d['ratio']:.2f}: \ at most 1, \ as proved", font_size=22, color=PROOFC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A check: three hundred observations of a hundred correlated Gaussian covariates, fifteen "
            f"with real effects. <bookmark mark='b'/> The histogram shows the false discovery proportion of each of forty "
            f"runs of model-X knockoff plus at q equal to a tenth: many runs have none, a few have more than a tenth. "
            f"<bookmark mark='c'/> Their average, the false discovery rate, is {say(d['fdr'], 3)}. <bookmark mark='d'/> And "
            f"{100 * d['power']:.0f} percent of the real variables are found. <bookmark mark='e'/> The supermartingale at the "
            f"stopping time averaged {say(d['ratio'], 2)}, at most one, as the proof requires."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), Create(q), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(m), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def robust(self):
        rows = [
            cmath(r"\text{the catch}", r":", r"\text{the law of } X \text{ is rarely known exactly}", font_size=34),
            cmath(r"\text{robustness}", r":", r"\text{FDR} \le q\,e^{\varepsilon} + P\big(\max_j \widehat{\mathrm{KL}}_j > \varepsilon\big)", font_size=34),
            cmath(r"\text{in practice}", r":", r"\text{estimate } \Sigma \text{ from unlabelled } X\text{'s}", font_size=32),
            cmath(r"\text{and}", r":", r"\text{derandomize with e-values}", font_size=32),
        ]
        rows[1][-1].set_color(SPLITC)
        whys = [why(r"model-X's assumption"), why(r"Barber, \ Cand\`es \& Samworth (2020)"), why(r"a large reference panel"), why(r"Ren \& Barber (2024)")]
        with self.voiceover(
            "<bookmark mark='a'/> The catch in model-X is that the law of the covariates is rarely known exactly. <bookmark "
            "mark='b'/> Barber, Candès and Richard Samworth showed the guarantee degrades gracefully: the rate is at most q "
            "times e to the epsilon, plus the chance that the knockoff construction's estimated Kullback–Leibler error exceeds "
            "epsilon for some variable. <bookmark mark='c'/> In practice the covariate law is estimated from many unlabelled "
            "observations, such as a genotype reference panel. <bookmark mark='d'/> And because a single knockoff draw is "
            "random, Zhimei Ren and Barber derandomized the procedure by aggregating many draws through e-values, the subject "
            "of Part fifty-eight."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
