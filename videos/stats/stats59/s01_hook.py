from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.claims()
        self.scatter()
        self.pvals()
        self.board()
        self.why_now()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(2019,)).to_edge(UP, buff=0.35)
        hc = history_card(2019, r"P. Sur \& E. Cand\`es, \ \emph{A modern maximum-likelihood theory for high-dimensional logistic regression}",
                          r"in \emph{PNAS}: \ with one variable for every five observations, \ the logistic MLE overestimates every "
                          r"effect by half, \ its standard errors are too small, \ and the likelihood-ratio test's $\chi^2$ "
                          r"approximation rejects true nulls far too often", color=CLASSC, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"the textbook: \ unbiased MLE, \ inverse Fisher information, \ Wilks's $\chi^2$", font_size=26, color=GREY_A),
            label(r"all three are fixed-$p$ results: \ $p$ stays put while $n \to \infty$", font_size=26, color=CLASSC),
            label(r"but genomics, \ advertising and surveys now have $p$ a fifth of $n$, \ or more", font_size=26, color=PROPC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2019 Pragya Sur and Emmanuel Candès published a short alarm in the Proceedings of the "
            "National Academy of Sciences. Fit a logistic regression with one variable for every five observations, and the "
            "maximum-likelihood estimates overestimate every effect by about a half; their standard errors are too small; and "
            "the likelihood-ratio test's chi-squared approximation rejects true null hypotheses far too often. <bookmark "
            "mark='b'/> The textbook says the MLE is unbiased, its variance is the inverse Fisher information, and twice the "
            "log likelihood ratio is chi-squared. <bookmark mark='c'/> All three are statements in which p stays fixed while n "
            "goes to infinity. <bookmark mark='d'/> But genomics, advertising and surveys routinely have p a fifth of n, or "
            "more."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def claims(self):
        d = load("hook")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Their setting: n observations, p equal to a fifth of n, Gaussian covariates, and coefficients "
            f"scaled so that the linear predictor has variance gamma squared equal to five. <bookmark mark='b'/> In the limit, "
            f"the MLE of each coefficient is alpha star times the truth plus noise: alpha star is {say(d['alpha'], 3)}. <bookmark "
            f"mark='c'/> The noise has standard deviation sigma star, {say(d['sigma'], 2)} in their units, against the "
            f"classical prediction of about {say(d['se_classical_null'], 1)}. <bookmark mark='d'/> And twice the log likelihood "
            f"ratio for a null coefficient is not chi-squared with one degree of freedom, but {say(d['factor'], 3)} times one.",
            [(r"p/n = \kappa = 0.2", r",", r"\ \gamma^2 = \mathrm{Var}(x'\beta) = 5", 38),
             (r"\hat\beta_j", r"\approx", rf"\alpha_\star\beta_j + \sigma_\star Z, \ \ \alpha_\star = {d['alpha']:.3f}", 38),
             (r"\sigma_\star", r"=", rf"{d['sigma']:.2f} \ \ (\text{{classical: }} {d['se_classical_null']:.1f})", 38),
             (r"2\log\mathrm{LR}", r"\Rightarrow", rf"{d['factor']:.3f}\,\chi^2_1, \ \text{{not }} \chi^2_1", 38)],
            [r"the proportional regime", r"inflated by half", r"standard errors too small", r"Wilks fails"],
            colors=[(1, CLASSC), (2, CLASSC), (3, CLASSC)])

    def scatter(self):
        d = load("hook")
        beta, bh = np.asarray(d["beta"]), np.asarray(d["beta_hat"])
        bv = d["b_val"]
        lim = 3.0 * bv
        A = axes([-lim, lim], [-lim, lim], x_length=5.0, y_length=5.0, xlabel=r"true $\beta_j$", ylabel=r"MLE $\hat\beta_j$",
                 xticks=[-bv, 0, bv], yticks=[-2 * bv, 0, 2 * bv], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", center=[-2.6, 0.0, 0])
        ax = A.ax
        r = np.random.default_rng(0)
        jit = r.uniform(-0.12, 0.12, len(beta)) * bv
        dots = VGroup(*[Dot(ax.c2p(a + j, float(np.clip(b, -lim, lim))), radius=0.035, color=SIMC, fill_opacity=0.6) for a, b, j in zip(beta, bh, jit)])
        ident = Line(ax.c2p(-lim, -lim), ax.c2p(lim, lim), color=GREY_B, stroke_width=2)
        theo = Line(ax.c2p(-lim / d["alpha"], -lim), ax.c2p(lim / d["alpha"], lim), color=PROPC, stroke_width=3)
        side = fit_rows(VGroup(
            label(rf"one fit: \ $n = {d['n']:,}$, \ $p = {d['p']}$; \ $\beta_j \in \{{-{bv:.0f}, 0, {bv:.0f}\}}$", font_size=22),
            label(r"grey: \ the textbook's line, \ slope 1", font_size=22, color=GREY_B),
            label(rf"green: \ Sur--Cand\`es, \ slope $\alpha_\star = {d['alpha']:.3f}$", font_size=22, color=PROPC),
            label(rf"fitted slope: \ {d['slope']:.3f}", font_size=22, color=SIMC),
            label(rf"spread of the nulls: \ {d['sd_null']:.2f} \ (theory {d['sigma']:.2f}; \ textbook {d['se_classical_null']:.2f})", font_size=22, color=GREY_A),
        ), 5.4, 0.38, [3.6, 0.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> One fit is enough to see it. Two thousand observations, four hundred variables; an eighth of "
            f"the coefficients are plus {bv:.0f}, an eighth minus {bv:.0f}, the rest zero. <bookmark mark='b'/> Each dot is a "
            f"coefficient, true value across, estimate up; the grey line is what the textbook expects. <bookmark mark='c'/> "
            f"The estimates follow the green line instead, slope {say(d['alpha'], 2)}, as Sur and Candès predict. <bookmark "
            f"mark='d'/> The fitted slope is {say(d['slope'], 3)}. <bookmark mark='e'/> And the null coefficients scatter with "
            f"standard deviation {say(d['sd_null'], 2)}: the theory says {say(d['sigma'], 2)}, the textbook "
            f"{say(d['se_classical_null'], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.002), Create(ident), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(theo), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def pvals(self):
        d = load("lrt")
        edges = np.linspace(0, 1, 21)
        pc, pr = np.asarray(d["p_classic"]), np.asarray(d["p_rescaled"])
        A = axes([0, 1], [0, 0.16], x_length=5.2, y_length=3.6, xlabel=r"$p$-value, \ $\chi^2_1$", ylabel=r"fraction of null tests",
                 xticks=[0, 0.5, 1], yticks=[0, 0.05, 0.1, 0.15], center=[-3.4, 0.5, 0])
        B = axes([0, 1], [0, 0.16], x_length=5.2, y_length=3.6, xlabel=rf"$p$-value, \ rescaled by {d['factor']:.3f}", ylabel=r"fraction of null tests",
                 xticks=[0, 0.5, 1], yticks=[0, 0.05, 0.1, 0.15], center=[3.4, 0.5, 0])
        h1 = hist_bars(A.ax, edges, np.histogram(pc, edges)[0] / len(pc), color=CLASSC, opacity=0.7)
        h2 = hist_bars(B.ax, edges, np.histogram(pr, edges)[0] / len(pr), color=PROPC, opacity=0.7)
        f1 = DashedLine(A.ax.c2p(0, 0.05), A.ax.c2p(1, 0.05), color=GREY_B, stroke_width=2)
        f2 = DashedLine(B.ax.c2p(0, 0.05), B.ax.c2p(1, 0.05), color=GREY_B, stroke_width=2)
        foot = fit_rows(VGroup(
            label(rf"{d['reps']} fits at $n = {d['n']:,}$, \ $p = {d['p']}$; \ the LRT for a coefficient that is truly zero", font_size=24, color=GREY_A),
            label(rf"left: \ {100 * d['size_classic']:.1f}\% below 0.05, \ {100 * d['size_classic_01']:.1f}\% below 0.01; \ right: \ {100 * d['size_rescaled']:.1f}\% and {100 * d['size_rescaled_01']:.1f}\%", font_size=24, color=GREY_A),
        ), 12.4, 0.2, [0, -2.8, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The likelihood-ratio test, run {d['reps']} times on a coefficient that is truly zero. "
            f"<bookmark mark='b'/> With the textbook chi-squared, the p-values pile up near zero: {100 * d['size_classic']:.1f} "
            f"percent fall below five percent, and {100 * d['size_classic_01']:.1f} below one. <bookmark mark='c'/> Divide the "
            f"statistic by Sur and Candès's factor, {say(d['factor'], 3)}, and the histogram is flat: "
            f"{100 * d['size_rescaled']:.1f} percent below five percent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), Create(f1), Create(f2), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(h1, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(h2, lag_ratio=0.05), FadeIn(foot[1]), run_time=2.0)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("approximation", "rescaled"),
                   f"<bookmark mark='a'/> On the Board: the likelihood-ratio test with the chi-squared approximation, at a "
                   f"fifth as many variables as observations, rejects a true null {100 * br[0]['achieved']:.1f} percent of the "
                   f"time at the five percent level: broken. <bookmark mark='b'/> Rescaled by the Sur–Candès factor, "
                   f"{100 * br[1]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def why_now(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Why classical asymptotics fail. <bookmark mark='b'/> Fixed-p theory expands around the truth, "
            "and the error of each estimated coordinate is of order one over root n. <bookmark mark='c'/> With p coordinates "
            "all estimated at once, those errors add up: the remainder terms grow like p over root n, which does not vanish "
            "when p is proportional to n. <bookmark mark='d'/> So the limits change: not just bigger standard errors, but "
            "different laws, with bias, inflated variance and rescaled statistics. <bookmark mark='e'/> This part finds them "
            "exactly, with four tools: random matrix theory, approximate message passing, Gordon's comparison inequality, "
            "and the physicists' replica method.",
            [(r"why fixed-$p$ theory fails:", GREY_A),
             (r"each coordinate's error is $O(1/\sqrt n)$", GREY_A),
             (r"$p$ of them at once: \ remainders of order $p/\sqrt n$, \ which do not vanish", CLASSC),
             (r"new limits: \ bias, \ inflated variance, \ rescaled statistics", PROPC),
             (r"the tools: \ random matrices, \ AMP, \ Gordon's comparison, \ the replica method", AMPC)])

    def upgrade(self):
        cards = [
            upgrade_card(22, r"the MLE is efficient, \ and $2\log\mathrm{LR} \Rightarrow \chi^2$", r"$p$ fixed as $n \to \infty$",
                         r"chapters 1 and 9: \ the proportional limits, \ and their corrections"),
            upgrade_card(52, r"high-dimensional rates, \ up to constants", r"sparsity; \ rates, \ not exact errors",
                         r"chapters 3--8: \ exact errors, \ constants included"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part twenty-two said the MLE is efficient and Wilks's statistic is "
            "chi-squared, assuming p fixed as n grows; chapters one and nine give the proportional limits and the corrections. "
            "<bookmark mark='b'/> Part fifty-two gave high-dimensional rates, up to constants, under sparsity; chapters three "
            "to eight give exact errors, constants included."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 59", font_size=34, color=GREY_B), label(r"High-Dimensional Asymptotics", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the proportional regime; \ Sur--Cand\`es's logistic MLE and LRT, \ solved exactly",
            r"random matrices: \ Stieltjes transforms, \ free convolution; \ exact ridge and ridgeless risk",
            r"robust regression in high dimensions; \ AMP and state evolution; \ Gordon's comparison",
            r"the replica method; \ random features; \ corrected inference; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 32, \ 51, \ 52").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.amp}, \ the state-evolution cobweb").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-nine: high-dimensional asymptotics. <bookmark mark='b'/> The proportional regime, "
            "and the logistic MLE and likelihood-ratio test solved exactly; random matrix tools, Stieltjes transforms and free "
            "convolution; exact risks for ridge and ridgeless regression; robust regression in high dimensions; approximate "
            "message passing and its state evolution; Gordon's comparison inequality; the replica method; random features; "
            "corrected inference; and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
