from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403

NAMES = [r"A", r"B", r"C", r"D", r"E", r"F", r"G", r"H"]


class Arena(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Arenas: pairwise votes, and the Bradley-Terry model behind the ranking.", 3,
                            r"Arenas", r"Ranking by pairwise votes")
        self.votes()
        self.model()
        self.board_chart()
        self.intervals()
        self.elo_()
        self.style()
        self.cautions()

    def votes(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Some things have no answer key: which of two essays is better written, which explanation "
            "is clearer. <bookmark mark='b'/> Wei-Lin Chiang and colleagues' Chatbot Arena, described in 2024, shows a "
            "visitor two anonymous models' answers to the visitor's own prompt, and records a vote. <bookmark mark='c'/> "
            "Millions of votes later, the models are ranked. <bookmark mark='d'/> The statistics are a century old: Ernst "
            "Zermelo in 1929, and Ralph Bradley and Milton Terry in 1952, for ranking chess players and taste tests from "
            "pairwise contests.",
            [(r"\text{no answer key}", r":", r"\text{preferences}", 40),
             (r"\text{arena}", r":", r"\text{two answers, \ one vote}", 40),
             (r"\text{many votes}", r":", r"\text{a ranking}", 40),
             (r"\text{model}", r":", r"\text{Zermelo (1929), \ Bradley \& Terry (1952)}", 40)],
            [r"open-ended tasks", r"Chiang et al. (2024)", r"crowdsourced", r"Part 21's MM"],
            colors=[(3, HONC)])

    def model(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Bradley-Terry model gives each model a strength theta. <bookmark mark='b'/> The "
            "probability that i beats j is the logistic function of theta i minus theta j. <bookmark mark='c'/> So each "
            "battle is a row of a logistic regression, with plus one in model i's column, minus one in model j's, and the "
            "vote as the outcome; one model is fixed at zero, because only differences are identified. <bookmark mark='d'/> "
            "Fit by maximum likelihood, Part twenty-four's IRLS, or Hunter's minorize-maximize algorithm from Part "
            "twenty-one. The Elo scale is the same thing, multiplied by four hundred over log ten.",
            [(r"\text{strengths}", r":", r"\theta_1, \dots, \theta_K", 40),
             (r"P(i \succ j)", r"=", r"\frac{1}{1 + e^{-(\theta_i - \theta_j)}}", 40),
             (r"\text{a battle}", r":", r"x = e_i - e_j, \ \ \theta_{\text{ref}} = 0", 40),
             (r"\text{Elo points}", r"=", r"\theta \times 400 / \ln 10", 40)],
            [r"Bradley--Terry", r"logistic", r"a regression row", r"Parts 21 and 24"],
            colors=[(1, HONC)])

    def board_chart(self):
        d = load("arena")
        th, fit, se = np.asarray(d["theta"]), np.asarray(d["fit"]), np.asarray(d["se_sandwich"])
        A = axes([-0.2, 1.3], [0.4, 8.6], x_length=6.8, y_length=4.8, xlabel=r"Bradley--Terry strength (model A $= 0$)",
                 ylabel=r"", xticks=[0, 0.5, 1], center=[-0.6, 0.0, 0])
        ax = A.ax
        cols = [MODA] * 8
        lb = Leaderboard(ax, [rf"model {n}" for n in NAMES], fit, np.where(se > 0, se, 1e-6), colors=cols)
        rows = lb.rows(font_size=22)
        truth = VGroup(*[Line(ax.c2p(th[k], lb.y(i) - 0.3), ax.c2p(th[k], lb.y(i) + 0.3), color=WHITE, stroke_width=3)
                         for i, k in enumerate(lb.order)])
        ties = VGroup(*[SurroundingRectangle(rows[list(lb.order).index(k)], color=S.ACCENT, buff=0.04) for k in d["rank_one"]])
        ties.count = len(d["rank_one"])
        side = side_groups([
            [(rf"{d['n']:,} simulated battles".replace(",", "{,}"), WHITE), (r"8 models", GREY_A)],
            [(r"blue: \ fitted strengths", MODA), (r"with sandwich 95\% intervals", MODA)],
            [(r"white ticks: \ the true strengths", WHITE)],
            [(rf"gold: \ {ties.count} candidates in simultaneous rank-1 set", S.ACCENT)],
        ], pos=(4.9, 0.3, 0), width=3.6)
        with self.voiceover(
            "<bookmark mark='a'/> Eight simulated models compete in six thousand independent battles from a connected Bradley-Terry model. Strengths are relative to model A. <bookmark mark='b'/> The blue intervals are marginal sandwich Wald intervals, not simultaneous bands. The reference model is fixed at zero by parametrization, rather than known with infinite precision in an absolute scale. <bookmark mark='c'/> White ticks show the generating relative strengths. A single realized table need not contain every tick in every interval. <bookmark mark='d'/> Gold highlights a separate asymptotic confidence set for rank one, computed using Bonferroni simultaneous pairwise contrasts and the full covariance matrix. A candidate remains if no competitor has a positive lower bound over it. This corrects the earlier interval-overlap heuristic; it is still a large-sample construction, not an exact finite-sample rank theorem."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(truth), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(ties), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def intervals(self):
        d = load("arena")
        se, sw, bs = np.asarray(d["se"]), np.asarray(d["se_sandwich"]), np.asarray(d["se_boot"])
        self.lad_voiceover(
            f"<bookmark mark='a'/> Three ways to get the intervals. <bookmark mark='b'/> The inverse Fisher information, which trusts the model: for the top model, a standard error of {se[7]:.3f}. <bookmark mark='c'/> An independent-battle sandwich, robust to some variance misspecification but still requiring a well-defined target: {sw[7]:.3f}. And the bootstrap over battles, {bs[7]:.3f}. <bookmark mark='d'/> Here the model is true, and all three agree; over {d['reps']} fresh arenas, the sandwich interval for the gap between the top two models covered {100 * d['cov_sandwich']:.1f} percent of the time. In a real arena voters differ and prompts differ, the model is wrong, and dependence may require clustering by voter or prompt. An ordinary sandwich or bootstrap over individual battles alone does not repair that dependence or self-selection. Chatbot Arena reports both.",
            [(r"\text{model-based}", r":", rf"\mathrm{{SE}}(\hat\theta_H) = {se[7]:.3f}", 40),
             (r"\text{sandwich}", r":", rf"{sw[7]:.3f}, \ \ \text{{bootstrap}}: {bs[7]:.3f}", 40),
             (r"\text{coverage}", r":", rf"{100 * d['cov_sandwich']:.1f}\% \ \text{{over {d['reps']} arenas}}", 40),
             (r"\text{misspecified}", r":", r"\text{prefer sandwich or bootstrap}", 40)],
            [r"Fisher information", r"Part 22", r"the gap H $-$ G", r"Chiang et al. (2024)"],
            colors=[(2, HONC)])

    def elo_(self):
        d = load("arena")
        fit, se = np.asarray(d["fit"]), np.asarray(d["se_sandwich"])
        lo, hi = np.asarray(d["elo_lo"]), np.asarray(d["elo_hi"])
        A = axes([-0.2, 1.5], [0.4, 8.6], x_length=6.8, y_length=4.8, xlabel=r"strength (logistic scale; model A $= 0$)",
                 ylabel=r"", xticks=[0, 0.5, 1, 1.5], center=[-0.6, 0.0, 0])
        ax = A.ax
        lb = Leaderboard(ax, [rf"model {n}" for n in NAMES], fit, np.where(se > 0, se, 1e-6), colors=[MODA] * 8)
        rows = lb.rows(font_size=22)
        el = VGroup(*[Line(ax.c2p(lo[k], lb.y(i) - 0.25), ax.c2p(hi[k], lb.y(i) - 0.25), color=NAIVEC, stroke_width=4)
                      for i, k in enumerate(lb.order)])
        side = side_groups([
            [(r"blue: \ Bradley--Terry, \ 95\% intervals", MODA)],
            [(r"red: \ online Elo, \ the same battles", NAIVEC), (r"in 50 random orders: \ min to max", NAIVEC)],
            [(r"Elo depends on the order", NAIVEC), (r"the likelihood does not", MODA)],
        ], pos=(4.9, 0.3, 0), width=3.6)
        with self.voiceover(
            "<bookmark mark='a'/> Why not Elo's online ratings, which chess uses? <bookmark mark='b'/> Elo updates after each game by a fixed step towards the surprise. Its ratings depend on the order in which the games were played. Feed the same six thousand battles in fifty random orders, and the resulting min-to-max Elo ranges, shown in red, describe ordering sensitivity. They are not confidence intervals and need not exceed every likelihood interval. <bookmark mark='c'/> For a fixed set of comparisons between models that do not change, the order carries no information, and the maximum-likelihood fit uses all of them at once. Chatbot Arena moved from online Elo to Bradley-Terry for this reason."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(el), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def style(self):
        d = load("arena")
        th, raw, ctl = np.asarray(d["theta"]), np.asarray(d["style_raw"]), np.asarray(d["style_ctl"])
        A = axes([-0.6, 7.6], [-0.1, 1.15], x_length=8.0, y_length=4.2, xlabel=r"", ylabel=r"fitted strength",
                 xticks=None, yticks=[0, 0.5, 1], center=[-1.9, 0.3, 0])
        ax = A.ax
        g_raw, g_ctl, g_true = VGroup(), VGroup(), VGroup()
        for k in range(8):
            for grp, v, dx, c in ((g_raw, raw[k], -0.17, NAIVEC), (g_ctl, ctl[k], 0.17, HONC)):
                h = max(abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), 0.02)
                b = Rectangle(width=0.3, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
                b.move_to(ax.c2p(k + dx, 0), aligned_edge=DOWN if v >= 0 else UP)
                grp.add(b)
            g_true.add(Line(ax.c2p(k - 0.4, th[k]), ax.c2p(k + 0.4, th[k]), color=WHITE, stroke_width=3))
        ticks = VGroup(*[label(n, font_size=24, color=S.ACCENT if k == 3 else GREY_A).next_to(ax.c2p(k, -0.1), DOWN, buff=0.15)
                         for k, n in enumerate(NAMES)])
        side = side_groups([
            [(r"model D writes longer answers;", S.ACCENT), (r"voters prefer length", S.ACCENT)],
            [(rf"red: \ plain Bradley--Terry: \ D at {raw[3]:.2f}", NAIVEC), (r"ranked near the top", NAIVEC)],
            [(rf"green: \ with a length term: \ {ctl[3]:.2f}", HONC), (rf"true {th[3]:.2f}; \ $\hat\gamma = {d['gamma']:.2f}$", HONC)],
        ], pos=(4.9, 0.3, 0), width=3.6)
        with self.voiceover(
            f"<bookmark mark='a'/> Votes measure preference, and preference mixes substance with style. In this "
            f"simulation, model D writes longer answers, and voters prefer longer answers, whatever their quality. "
            f"<bookmark mark='b'/> Plain Bradley-Terry puts D at {raw[3]:.2f}, near the top, though its true strength is "
            f"{th[3]:.2f}. <bookmark mark='c'/> Add the difference in length as a covariate, as Chatbot Arena's style "
            f"control did in August 2024, and D's strength drops to {ctl[3]:.2f}, with the length effect estimated at "
            f"{d['gamma']:.2f} against a true {d['gamma_true']}. It estimates a conditional equal-length comparison in this correctly specified simulation. Length is itself an output of the model, so adjusting it is not automatically causal confounder control, "
            f"and it works only if length varies within each model's answers, so that it is not confused with the model "
            f"itself."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ticks), FadeIn(g_true), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(g_raw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(g_ctl), FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def cautions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Cautions an arena inherits from the degree. <bookmark mark='b'/> The voters are a "
            "self-selected sample, and their prompts are not a designed population: Part eighteen. <bookmark mark='c'/> "
            "Models that are tested many times privately before release, with only the best version shown, enjoy the "
            "winner's curse of chapter two. <bookmark mark='d'/> And the ranking answers one question, which answer this "
            "crowd prefers, not which model is more accurate or more helpful for a given use.",
            [(r"\text{voters}", r":", r"\text{a self-selected sample}", 40),
             (r"\text{private variants}", r":", r"\text{the winner's curse}", 40),
             (r"\text{the estimand}", r":", r"\text{this crowd's preference}", 40),
             (r"\text{not}", r":", r"\text{accuracy for your use}", 40)],
            [r"Part 18", r"chapter 2", r"say what is estimated", r"Part 19"],
            colors=[(0, NAIVEC), (1, NAIVEC)])
