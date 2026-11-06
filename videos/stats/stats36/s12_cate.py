from __future__ import annotations

import numpy as np

from videos.stats.stats36.common import *  # noqa: F403

LC = {"T-learner": GREY_B, "X-learner": Y0C, "DR-learner": PSC, "causal forest": BANDC, "linear, interacted": TAUC}


class CATE(VoiceoverScene):
    def construct(self):
        self.card()
        self.goal()
        self.learners()
        self.forest()
        self.grade()
        self.calib()
        self.cautions()

    def card(self):
        card = chapter_card(11, r"Heterogeneous effects", r"For whom does it work?", lit=(2018,), part=PART)
        with self.voiceover("Chapter eleven. Heterogeneous effects."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def goal(self):
        rows = [
            cmath(r"\tau(x)", r"=", r"E[Y(1) - Y(0) \mid X = x]", font_size=34),
            cmath(r"\text{identified}", r":", r"E[Y \mid T = 1, x] - E[Y \mid T = 0, x]", font_size=32),
            cmath(r"\text{not}", r":", r"\tau_i \text{ itself, \ nor who is harmed}", font_size=32),
            cmath(r"\text{the World}", r":", r"\tau(x) = -\big(9 + 0.3(\text{sbp} - 150) + 0.08(\text{age} - 60)\big)", font_size=26),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"the conditional average effect"), why(r"under unconfoundedness, \ in each $x$"),
                why(r"Part 35's limit"), why(r"the truth to grade against")]
        with self.voiceover(
            "<bookmark mark='a'/> An average effect may hide large differences between people. The conditional average "
            "effect asks for the average effect among patients with covariates x. <bookmark mark='b'/> In a randomized trial, "
            "or under unconfoundedness, it is the difference of two regression functions. <bookmark mark='c'/> It is still an "
            "average: individual effects, and the share of people harmed, remain out of reach, as Part 35 showed. <bookmark "
            "mark='d'/> In the World's trial we know the systematic part of each patient's effect: it grows with their true "
            "pressure and their age. So we can grade the methods."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def learners(self):
        rows = [
            cmath(r"\text{T-learner}", r":", r"\hat\mu_1(x) - \hat\mu_0(x), \ \text{one model per arm}", font_size=28),
            cmath(r"\text{S-learner}", r":", r"\text{one model with } T \text{ as a feature}", font_size=28),
            cmath(r"\text{X-learner}", r":", r"\text{impute each unit's effect from the other arm, \ then regress}", font_size=28),
            cmath(r"\text{DR-learner}", r":", r"\text{regress AIPW pseudo-outcomes } \psi_i \text{ on } x", font_size=28),
        ]
        rows[2][-1].set_color(Y0C)
        whys = [why(r"two separate fits"), why(r"may shrink the effect to zero"),
                why(r"K\"unzel, \ Sekhon, \ Bickel \& Yu (2019)"), why(r"Kennedy (2023)")]
        with self.voiceover(
            "<bookmark mark='a'/> The meta-learners build effect estimates from any regression method. The T-learner fits "
            "one model per arm and subtracts. <bookmark mark='b'/> The S-learner fits a single model with treatment as a "
            "feature, which a regularized learner may simply ignore. <bookmark mark='c'/> The X-learner of Sören Künzel and "
            "colleagues imputes each patient's effect using the other arm's model, then regresses those imputed effects on x. "
            "<bookmark mark='d'/> Edward Kennedy's DR-learner regresses the doubly robust scores of chapter nine on x."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def forest(self):
        rows = [
            cmath(r"\text{centre}", r":", r"\tilde Y = Y - \hat m(X), \ \ \tilde T = T - \hat e(X)", font_size=30),
            cmath(r"\text{split}", r":", r"\max \ \tfrac{n_L n_R}{n^2}(\hat\tau_L - \hat\tau_R)^2, \ \ \hat\tau = \tfrac{\sum \tilde T \tilde Y}{\sum \tilde T^2}", font_size=28),
            cmath(r"\text{honest}", r":", r"\text{split on one half; \ estimate the leaves on the other}", font_size=28),
            cmath(r"\text{average}", r":", r"\text{many such trees on subsamples}", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"out-of-bag forests: \ local centring"), why(r"look for effect differences, \ not outcome differences"),
                why(r"Athey \& Imbens (2016)"), why(r"Wager \& Athey (2018); \ Athey, \ Tibshirani \& Wager (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> The causal forest of Stefan Wager and Susan Athey is built for the purpose. First centre "
            "the outcome and the treatment by their predicted values from ordinary forests. <bookmark mark='b'/> Then grow "
            "trees that split, not where the outcome changes, but where the effect changes: each split maximizes the "
            "difference between the children's effect estimates, each a residual-on-residual slope. <bookmark mark='c'/> "
            "The trees are honest: one half of each subsample chooses the splits and the other half estimates the leaves, "
            "so a leaf's estimate is not biased by the search that created it. <bookmark mark='d'/> Average many such trees, "
            "and, as Wager and Athey proved, the estimates are asymptotically normal, with valid confidence intervals."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def grade(self):
        d = load("cate")
        L = d["learners"]
        order = ["T-learner", "DR-learner", "X-learner", "causal forest", "linear, interacted"]
        A = axes([0, 6], [0, 5], x_length=7.6, y_length=4.2, xlabel=r"", ylabel=r"RMSE vs the truth (mm Hg)",
                 xticks=[], yticks=[0, 1, 2, 3, 4, 5], center=[-1.8, 0.4, 0])
        ax = A.ax
        vals = [d["rmse_const"]] + [L[k]["rmse"] for k in order]
        cols = [MISSC] + [LC[k] for k in order]
        bars = VGroup(*[bars_at(ax, [i + 0.5], [v], 0.6, c) for i, (v, c) in enumerate(zip(vals, cols))])
        names = [r"everyone: \ the ATE"] + order
        labs = VGroup(*[label(n, font_size=16, color=c).rotate(PI / 8).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.3) for i, (n, c) in enumerate(zip(names, cols))])
        nums = VGroup(*[label(rf"{v:.2f}", font_size=18, color=c).next_to(b, UP, buff=0.06) for v, c, b in zip(vals, cols, bars)])
        side = fit_rows(VGroup(
            label(r"the trial's 2,000 patients train; \ 2,000 other islanders grade", font_size=20),
            label(r"forests on baseline, \ age, \ BMI, \ sex", font_size=20, color=GREY_A),
            label(r"causal forest and X-learner: \ best of the black boxes", font_size=20, color=BANDC),
            label(r"a linear model in the right variables: \ best of all", font_size=20, color=TAUC),
        ), 3.8, 0.4, [5.1, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Train each method on the trial's two thousand patients, and grade its predictions on two "
            "thousand other eligible islanders, against the World's true effect function. <bookmark mark='b'/> Giving "
            "everyone the trial's average effect has an error of " + say(d["rmse_const"]) + " millimetres, partly because "
            "the islanders are older than the trial. <bookmark mark='c'/> The T-learner does a little better, and the "
            "DR-learner, whose pseudo-outcomes are very noisy at this sample size, does worse. <bookmark mark='d'/> The "
            "X-learner and the causal forest cut the error of the constant by about two fifths. <bookmark mark='e'/> And a linear model "
            "with treatment interactions does best of all, because here the true effect really is linear in pressure and "
            "age. Flexible methods pay for their flexibility in variance."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), FadeIn(labs), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1], DOWN), GrowFromEdge(bars[2], DOWN), FadeIn(nums[1:3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[3], DOWN), GrowFromEdge(bars[4], DOWN), FadeIn(nums[3:5]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(GrowFromEdge(bars[5], DOWN), FadeIn(nums[5]), FadeIn(side[3]))
        self.clear_scene()

    def calib(self):
        d = load("cate")
        L = d["learners"]
        A = axes([-18, 0], [-18, 0], x_length=4.6, y_length=4.6, xlabel=r"predicted $\hat\tau(x)$, \ by decile", ylabel=r"true $\tau(x)$",
                 xticks=[-15, -10, -5, 0], yticks=[-15, -10, -5, 0], center=[-3.2, 0.2, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-18, -18), ax.c2p(0, 0), color=GREY_B, stroke_width=2)
        curves = {}
        for k in ("causal forest", "T-learner", "linear, interacted"):
            xs = np.clip(L[k]["dec_pred"], -18, 0)
            ys = np.clip(L[k]["dec_true"], -18, 0)
            curves[k] = VGroup(polyline(ax, xs, ys, LC[k], 3), *[Dot(ax.c2p(a, b), radius=0.06, color=LC[k]) for a, b in zip(xs, ys)])
        side = fit_rows(VGroup(
            label(r"sort the islanders by predicted effect; \ ten groups", font_size=22),
            label(r"green: \ causal forest", font_size=22, color=BANDC),
            label(r"grey: \ T-learner", font_size=22, color=GREY_B),
            label(r"gold: \ linear, \ interacted", font_size=22, color=TAUC),
            label(r"forest: \ too timid; \ T-learner: \ too bold", font_size=22, color=MISSC),
        ), 5.0, 0.4, [3.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A more useful check for decisions: sort the islanders into ten groups by predicted effect, "
            "and compare each group's average prediction with its true average effect. <bookmark mark='b'/> The causal "
            "forest, <bookmark mark='c'/> the T-learner, <bookmark mark='d'/> and the linear model. <bookmark mark='e'/> All "
            "of them rank people correctly: those predicted to benefit most really do. But the causal forest is too timid, "
            "predicting too little benefit for those who gain most, the averaging bias of Part 34; the T-learner is too "
            "bold, mistaking the noise of two separate fits for heterogeneity; the linear model sits on the diagonal."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), Create(diag), FadeIn(side[0]))
            for m_, k, r in (("b", "causal forest", 1), ("c", "T-learner", 2), ("d", "linear, interacted", 3)):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(side[r]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"heterogeneity found by search is Part 33's multiplicity again", font_size=26, color=MISSC),
            label(r"test for it: \ calibration tests, \ the best linear predictor (Chernozhukov et al. 2018)", font_size=26, color=GREY_A),
            label(r"use it for policy: \ treat when $\hat\tau(x)$ beats the cost \ (Athey \& Wager 2021)", font_size=26, color=BANDC),
            label(r"and remember chapter 11 of Part 35: \ most subgroup findings are noise", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Some cautions. Heterogeneity discovered by searching is Part 33's multiplicity problem in "
            "new clothes. <bookmark mark='b'/> It should be tested, for instance by checking whether the predicted effects "
            "predict differences in actual outcomes, as Chernozhukov and colleagues' best-linear-predictor tests do. "
            "<bookmark mark='c'/> When used for decisions, the target is a treatment rule: treat when the predicted benefit "
            "exceeds the cost, as in Athey and Wager's policy learning. <bookmark mark='d'/> And recall the subgroup chapter "
            "of Part 35: most claimed differences between subgroups are noise. Part 62 returns to all this."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
