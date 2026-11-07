from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class Knockoffs(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.construct_()
        self.gaussian()
        self.fixedx()
        self.stats_()
        self.coin()
        self.bars()
        self.results()
        self.reach()

    def card(self):
        card = chapter_card(7, r"Knockoffs", r"Fake variables that catch false ones", lit=(2015,), part=PART)
        with self.voiceover("Chapter seven. Knockoffs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\text{regression}", r":", r"\text{which of } p \text{ variables matter, \ given the others?}", font_size=30),
            cmath(r"\text{lasso}", r":", r"\text{selects, \ but with no error control}", font_size=30),
            cmath(r"p\text{-values}", r":", r"\text{hard to get after selection, \ or when } p > n", font_size=30),
            cmath(r"\text{goal}", r":", r"\text{FDR control with valid knockoffs and flip-sign statistics}", font_size=30),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"conditional independence"), why(r"Part 32"), why(r"chapter ten of Part 32"),
                why(r"Barber \& Cand\`es (2015)")]
        with self.voiceover(
            "<bookmark mark='a'/> Testing variables in a regression is harder. We ask whether each variable matters given "
            "all the others. <bookmark mark='b'/> The lasso selects variables but promises nothing about errors. "
            "<bookmark mark='c'/> Valid p-values for each variable are hard to get after selection, and impossible by "
            "classical means when p exceeds n. <bookmark mark='d'/> Rina Foygel Barber and Emmanuel Candès found a way, in "
            "2015, to control the false discovery rate of a selection made by almost any method: knockoffs."
        ) as vo:
            intro=label('Variable selection asks about conditional association',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def construct_(self):
        rows = [
            cmath(r"\tilde X", r":", r"\text{a fake copy of every variable}", font_size=32),
            cmath(r"(X, \tilde X)_{\mathrm{swap}(S)}", r"\overset{d}{=}", r"(X, \tilde X) \ \ \text{for any set } S", font_size=30),
            cmath(r"\tilde X", r"\perp", r"y \mid X", font_size=34),
            cmath(r"\text{so}", r":", r"\text{each knockoff looks like its original, \ but is certainly null}", font_size=28),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"the knockoffs"), why(r"pairwise exchangeable"), why(r"made without looking at $y$"),
                why(r"a matched control for each variable")]
        with self.voiceover(
            "<bookmark mark='a'/> Construct a fake copy of every variable, a knockoff, with two properties. "
            "<bookmark mark='b'/> Swapping any set of variables with their knockoffs leaves the joint distribution of all of "
            "them unchanged: each knockoff relates to the other variables exactly as its original does. "
            "<bookmark mark='c'/> And the knockoffs are made without looking at the outcome, so they are independent of it "
            "given the real variables. <bookmark mark='d'/> Each knockoff is a perfect matched control: it looks like its "
            "original in every way, but is certainly null."
        ) as vo:
            intro=label('Model-X knockoffs require joint exchangeability and conditional independence',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gaussian(self):
        rows = [
            cmath(r"x", r"\sim", r"N(0, \Sigma)", font_size=34),
            cmath(r"\tilde x \mid x", r"\sim", r"N\big(x - D\Sigma^{-1}x, \ 2D - D\Sigma^{-1}D\big)", font_size=30),
            cmath(r"D", r"=", r"s I, \ s = \min(1, 2\lambda_{\min}(\Sigma))", font_size=32),
            cmath(r"\text{larger } s", r":", r"\text{knockoffs less like their originals: \ more power}", font_size=28),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"model-X: \ the design's law is known"), why(r"Cand\`es, Fan, Janson \& Lv (2018)"),
                why(r"equicorrelated knockoffs"), why(r"but still exchangeable")]
        with self.voiceover(
            "<bookmark mark='a'/> When the variables are multivariate normal with a known covariance, the model-X knockoffs "
            "of Candès, Yingying Fan, Lucas Janson and Jinchi Lv have a closed form: <bookmark mark='b'/> draw each knockoff "
            "row from a normal whose mean and covariance are set by sigma and a diagonal matrix D. <bookmark mark='c'/> The "
            "simplest choice makes D a multiple of the identity, as large as positive definiteness allows. "
            "<bookmark mark='d'/> The larger D, the less each knockoff resembles its original, and the easier it is to tell "
            "a real variable from its fake."
        ) as vo:
            intro=label('A known Gaussian design law gives a conditional sampling formula',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stats_(self):
        rows = [
            cmath(r"\text{lasso on}", r":", r"[X, \tilde X], \ 2p \text{ columns}", font_size=32),
            cmath(r"W_j", r"=", r"|\hat\beta_j| - |\hat\beta_{\tilde j}|", font_size=34),
            cmath(r"W_j > 0", r":", r"\text{the real variable beat its knockoff}", font_size=30),
            cmath(r"\text{any } W", r":", r"\text{that flips sign when } x_j \leftrightarrow \tilde x_j", font_size=30),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"fit both at once"), why(r"the coefficient difference"), why(r"evidence for $x_j$"),
                why(r"the antisymmetry that makes it work")]
        with self.voiceover(
            "<bookmark mark='a'/> Now fit any model to the real variables and their knockoffs together, for example a"
            " lasso on two p columns. <bookmark mark='b'/> For each variable, W j is the size of its coefficient "
            "minus the size of its knockoff's. <bookmark mark='c'/> A large positive W means the real variable "
            "clearly beat its fake. <bookmark mark='d'/> Any statistic works, provided the statistic obeys the joint "
            "flip-sign property: swapping a subset flips exactly those W signs and leaves the others unchanged."
        ) as vo:
            intro=label('Joint flip-sign statistics compare each variable with its matched knockoff',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coin(self):
        rows = [
            cmath(r"j \text{ null}", r"\Rightarrow", r"\mathrm{sign}(W_j) \text{ is a fair coin, \ independent of } |W_j|", font_size=28),
            cmath(r"\#\{\text{nulls with } W_j \ge t\}", r"\approx", r"\#\{j : W_j \le -t\}", font_size=30),
            cmath(r"\widehat{\mathrm{FDP}}(t)", r"=", r"\dfrac{1 + \#\{j : W_j \le -t\}}{\max(1, \#\{j : W_j \ge t\})}", font_size=30),
            cmath(r"\tau", r"=", r"\min\{t\in\{|W_j|:|W_j|>0\} : \widehat{\mathrm{FDP}}(t) \le q\} \ \Rightarrow \ \text{FDR} \le q", font_size=30),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"swap it: \ nothing changes"), why(r"negatives mirror the null positives"),
                why(r"knockoff+ \ (the $+1$)"), why(r"exactly, \ in finite samples")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is a coin flip. For a null variable, swapping it with its knockoff "
            "changes nothing about the data's distribution but flips the sign of W. Conditional on all magnitudes and"
            " nonnull statistics, the nonzero null signs are independent fair coins. <bookmark mark='b'/> Hence the "
            "number of nulls with W above t is mirrored by the number of W's below minus t. <bookmark mark='c'/> That"
            " count, plus one, over the number selected, estimates the false discovery proportion. <bookmark "
            "mark='d'/> Choose the smallest nonzero observed absolute W where the estimate is below q, or select none"
            " if there is no such threshold, and the false discovery rate is at most q, exactly, in finite samples, "
            "with no p-values, for any n and p."
        ) as vo:
            intro=label('Nonzero null signs yield the knockoff+ error-control argument',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bars(self):
        d = load("knock")
        W, tr = np.asarray(d["demo"]["W"]), np.asarray(d["demo"]["true"], bool)
        thr = d["demo"]["thr"]
        o = np.argsort(-np.abs(W))[:60]
        Wm = float(np.max(np.abs(W[o])))
        A = axes([0, 61], [-Wm * 1.1, Wm * 1.1], x_length=8.0, y_length=4.4, xlabel=r"variables, \ by $|W_j|$",
                 ylabel=r"$W_j$", xticks=[], yticks=[0], center=[-1.9, 0.3, 0])
        ax = A.ax
        bw = ax.c2p(0.8, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for i, j in enumerate(o):
            h = ax.c2p(0, W[j])[1] - ax.c2p(0, 0)[1]
            r = Rectangle(width=bw, height=max(abs(h), 0.01), stroke_width=0, fill_opacity=0.85,
                          fill_color=TRUEC if tr[j] else (FALSEC if W[j] > 0 else NULLC))
            r.move_to(ax.c2p(i + 1, 0), aligned_edge=DOWN if W[j] >= 0 else UP)
            bars.add(r)
        t1 = DashedLine(ax.c2p(0, thr), ax.c2p(61, thr), color=SIGC, stroke_width=2.5)
        t2 = DashedLine(ax.c2p(0, -thr), ax.c2p(61, -thr), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ $p = {d['p']}$", font_size=22),
            label(rf"{d['k']} real effects", font_size=22),
            label(r"green: \ real", font_size=22, color=TRUEC),
            label(r"red / grey: \ null, \ $W > 0$ / $W < 0$", font_size=22, color=FALSEC),
            label(rf"knockoff+, \ $q = 0.1$:", font_size=22, color=BHC),
            label(rf"{d['demo']['n_sel']} selected, \ {d['demo']['false_sel']} false", font_size=22, color=BHC),
        ), 3.4, 0.4, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulated regression: four hundred observations, a hundred and fifty correlated "
            "variables, twenty real effects. The sixty largest W statistics, in order of size. <bookmark mark='b'/> Real "
            "variables in green stand tall above zero. Null variables come in both signs, as the coin-flip argument says. "
            "<bookmark mark='c'/> The knockoff+ threshold at ten percent selects twenty-three variables, three of them "
            "false."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if W[j] >= 0 else UP) for b, j in zip(bars, o)], lag_ratio=0.02),
                      FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(Create(t1), Create(t2), FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def results(self):
        d = load("knock")
        hdr = [r"\textbf{20 simulated regressions}", r"\textbf{FDR}", r"\textbf{power}"]
        body = [[r"lasso, \ $\lambda$ by CV", f"{100 * d['fdr_lasso']:.0f}\\%", f"{100 * d['pow_lasso']:.0f}\\%"],
                [r"knockoff+, \ $q = 0.1$", f"{100 * d['fdr_knock']:.1f}\\%", f"{100 * d['pow_knock']:.0f}\\%"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.35, colors=[GREY_A, FALSEC, BHC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"the lasso finds every real variable, \ and buries them among false ones", font_size=22, color=FALSEC),
            label(r"20-study mean: 8.2\% $\pm$ 1.7 percentage points (MC SE)", font_size=22, color=BHC),
        ), 12.0, 0.22, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over twenty simulated regressions: the cross-validated lasso finds every real "
            "variable, but sixty-two percent of what it selects is false, Part 32's lesson again. <bookmark "
            "mark='b'/> The estimated knockoff FDR is eight point two percent, with a one point seven "
            "percentage-point Monte Carlo standard error across only twenty studies <bookmark mark='c'/> and still "
            "find ninety-seven percent of the real variables."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def reach(self):
        rows = fit_rows(VGroup(
            label(r"model-X needs the law of $X$, \ not of $y \mid X$: \ any model for the outcome", font_size=26, color=BHC),
            label(r"genetics: \ genotypes modeled by fitted hidden Markov models \ (Sesia, Sabatti \& Cand\`es 2019)", font_size=26),
            label(r"the price: \ $X$'s distribution must be right", font_size=26, color=FALSEC),
            label(r"conformal prediction uses exchangeable observations: \ Part 34", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The striking feature of model-X knockoffs is where the assumption sits: on the "
            "distribution of the variables, not on how the outcome depends on them. Any outcome model, any "
            "machine-learning method, can produce the W's. <bookmark mark='b'/> In genetics, where genotypes along a "
            "chromosome are modeled by fitted hidden Markov models, this has been used at genome scale. <bookmark "
            "mark='c'/> The price is that the distribution of X must be right. <bookmark mark='d'/> A different "
            "exchangeability assumption, across observations, powers conformal prediction, in Part 34."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fixedx(self):
        rows = [
            cmath(r"\text{fixed-X}", r":", r"\tilde X^\top \tilde X = X^\top X, \ \ X^\top \tilde X = X^\top X - D", font_size=30),
            cmath(r"\text{needs}", r":", r"n \ge 2p; \ y \text{ linear-Gaussian in } X", font_size=30),
            cmath(r"\text{model-X}", r":", r"\text{random } X \text{ with known law, \ any } y \mid X", font_size=30),
            cmath(r"\text{second-order}", r":", r"\text{match only means and covariances in practice}", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"Barber \& Cand\`es (2015)"), why(r"the original setting"), why(r"Cand\`es et al. (2018)"), why(r"an approximation")]
        with self.voiceover(
            "<bookmark mark='a'/> The original knockoffs of 2015 were fixed-X: constructed from the observed design so "
            "that the knockoffs have the same correlations among themselves as the originals, and with the originals "
            "except on the diagonal. <bookmark mark='b'/> That version needs at least twice as many observations as "
            "variables and a linear model with Gaussian errors. <bookmark mark='c'/> Model-X knockoffs instead treat "
            "the rows of X as random with a known distribution, and allow any relationship between y and X. <bookmark "
            "mark='d'/> In practice the distribution of X is estimated, and often only its means and covariances are "
            "matched, an approximation whose robustness is an active research question."
        ) as vo:
            intro=label('Fixed-X and model-X knockoffs make different assumptions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
