from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


def sci_tex(v: float) -> str:
    if v >= 0.01:
        return f"{v:.2f}"
    e = int(np.floor(np.log10(v)))
    return rf"{v / 10 ** e:.1f}\times 10^{{{e}}}"


class Invariance(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Invariance: what stays the same across environments is what will stay the same "
                            "next time.", 8, r"Invariance", r"Causal structure as a guarantee", lit=(2016,))
        self.idea()
        self.icp_method()
        self.icp_table()
        self.anchor()
        self.anchor_chart()
        self.irm()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A causal mechanism does not care which hospital, country or year the data came from. "
            "<bookmark mark='b'/> If y is caused by some of the covariates, the conditional law of y given those causes is "
            "the same in every environment, whatever the environments do to the covariates. <bookmark mark='c'/> Other "
            "predictors, such as effects of y, or proxies for hidden causes, have relations with y that change between "
            "environments. <bookmark mark='d'/> So invariance across the environments one has seen is evidence of "
            "causation, and a model built on causes is robust to every intervention that leaves y's mechanism alone.",
            [(r"\text{causes } S^*", r":", r"P_e(Y \mid X_{S^*}) \ \text{the same for every } e", 40),
             (r"\text{non-causes}", r":", r"P_e(Y \mid X_S) \ \text{changes with } e", 40),
             (r"\text{so}", r":", r"\text{invariance} \Rightarrow \text{evidence of causation}", 40),
             (r"\text{and}", r":", r"\text{causal models are robust to interventions on } X", 38)],
            [r"modularity", r"children, \ proxies", r"turned around", r"the robustness of causes"],
            colors=[(0, FIXC)])

    def icp_method(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Jonas Peters, Peter Bühlmann and Nicolai Meinshausen turned this into a test in 2016: "
            "invariant causal prediction. <bookmark mark='b'/> For every subset S of the predictors, test whether the "
            "residuals of regressing y on X_S have the same distribution in every environment. <bookmark mark='c'/> The "
            "estimate is the intersection of all accepted subsets. <bookmark mark='d'/> Its guarantee is one-sided and "
            "honest: with probability at least one minus alpha, every variable it names is a true cause. It may name too "
            "few, never too many.",
            [(r"\text{for each } S", r":", r"H_{0,S}: \ \text{the residuals of } Y \sim X_S \text{ are invariant}", 38),
             (r"\hat S", r"=", r"\bigcap_{S: \ H_{0,S} \text{ accepted}} S", 40),
             (r"\text{guarantee}", r":", r"P(\hat S \subseteq S^*) \ge 1 - \alpha", 40),
             (r"\text{so}", r":", r"\text{conservative: \ too few, \ never too many}", 40)],
            [r'Peters, \ B\"uhlmann \& Meinshausen (2016)', r"a two-sample problem per $S$", r"what all invariant sets share", r"a confidence statement"],
            colors=[(2, FIXC)])

    def icp_table(self):
        d = load("invariance")["icp"]
        pv = d["pvals"]
        hdr = [r"subset $S$", r"invariance $p$-value", r"verdict"]
        rows = [[r"$\emptyset$", rf"${sci_tex(pv['()'])}$", r"rejected"],
                [r"$\{X_1\}$", rf"${sci_tex(pv['(0,)'])}$", r"accepted"],
                [r"$\{X_2\}$", rf"${sci_tex(pv['(1,)'])}$", r"rejected"],
                [r"$\{X_1, X_2\}$", rf"${sci_tex(pv['(0, 1)'])}$", r"rejected"]]
        cols = [GREY_B, NAIVEC, FIXC, NAIVEC, NAIVEC]
        tab = table_rows([hdr] + rows, font_size=30, col_buff=0.9, row_buff=0.35, colors=cols).move_to([0, 0.6, 0])
        graph = label(r"truth: \ $E \to X_1 \to Y \to X_2 \leftarrow E$ \ \ (three environments, \ 400 points each)", font_size=26, color=GREY_A).next_to(tab, DOWN, buff=0.6)
        est = label(r"$\hat S = \{X_1\}$: \ the true parent, \ and nothing else", font_size=28, color=FIXC).next_to(graph, DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> A small example. Three environments shift the mean of X one; y depends on X one; X two is "
            "a child of y, also pushed by the environment. <bookmark mark='b'/> Using no predictor, y's mean changes between "
            "environments: rejected. <bookmark mark='c'/> Using X one, the residuals look the same everywhere: a p-value of "
            "one, accepted. <bookmark mark='d'/> Using X two, or both, the child's relation to y changes with the "
            "environment: rejected. <bookmark mark='e'/> The intersection of accepted sets is X one, the true parent. The "
            "child, which would be the better predictor within any one environment, is correctly left out."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(graph))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                if k < 2:
                    self.play(FadeIn(tab[1 + k], shift=RIGHT * 0.15))
                else:
                    self.play(FadeIn(tab[3], shift=RIGHT * 0.15), FadeIn(tab[4], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(est, shift=UP * 0.15))
        self.clear_scene()

    def anchor(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Invariance is a strong demand: with hidden confounders, no subset may be invariant. "
            "Dominik Rothenhäusler, Nicolai Meinshausen, Peter Bühlmann and Jonas Peters relaxed it in 2021: anchor "
            "regression. <bookmark mark='b'/> Exogenous anchor variables A, such as the environment, push on the system. "
            "Penalize the part of the residual that the anchors explain, with weight gamma. <bookmark mark='c'/> Gamma equal "
            "to one is least squares; gamma to infinity is instrumental-variables regression; in between, a trade-off. "
            "<bookmark mark='d'/> The guarantee: the anchor solution minimizes the worst-case risk over all shifts in the "
            "anchors' direction up to strength gamma. It is a DRO, with an uncertainty set built from causal structure.",
            [(r"\text{relax}", r":", r"\text{invariance fails with hidden confounders}", 40),
             (r"\hat b_\gamma", r"=", r"\arg\min_b \|(I - P_A)(y - Xb)\|^2 + \gamma\|P_A(y - Xb)\|^2", 38),
             (r"\gamma = 1", r":", r"\text{OLS}; \ \ \gamma \to \infty: \ \text{IV}", 40),
             (r"\text{guarantee}", r":", r"\min_b \sup_{\text{shifts } v: \ vv' \preceq \gamma E[AA']} E_v[(Y - X'b)^2]", 38)],
            [r'Rothenh\"ausler et al. (2021)', r"$P_A$: \ projection on the anchors", r"Part 37's 2SLS", r"chapter 7, \ causally"],
            colors=[(1, FIXC), (3, FIXC)])

    def anchor_chart(self):
        d = load("invariance")
        g = np.asarray(d["gammas"], float)
        xs = np.log10(1 + g)
        tr, te, cf = np.asarray(d["train"]), np.asarray(d["test"]), d["coef"]
        A = axes([0, 1.8], [0, 11.5], x_length=7.4, y_length=4.4, xlabel=r"anchor penalty $\gamma$", ylabel=r"mean squared error",
                 xticks=list(np.log10(1 + np.array([0, 1, 5, 10, 50]))), xfmt=lambda v: f"{10 ** v - 1:.0f}",
                 yticks=[0, 2, 4, 6, 8, 10], center=[-2.5, 0.2, 0])
        ax = A.ax
        l_tr = VGroup(polyline(ax, xs, tr, SRCC, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=SRCC) for a, b in zip(xs, tr)])
        l_te = VGroup(polyline(ax, xs, te, TGTC, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=TGTC) for a, b in zip(xs, te)])
        i_ols, i_best = 1, int(np.argmin(te))
        mk = VGroup(Circle(radius=0.16, color=NAIVEC, stroke_width=3).move_to(ax.c2p(xs[i_ols], te[i_ols])),
                    Circle(radius=0.16, color=FIXC, stroke_width=3).move_to(ax.c2p(xs[i_best], te[i_best])))
        side = side_groups([
            [(r"the anchor $A$: \ mean 0 in training,", WHITE), (r"mean 3 at test", WHITE)],
            [(r"blue: \ training error", SRCC), (r"gold: \ test error", TGTC)],
            [(rf"OLS ($\gamma = 1$): \ test {te[i_ols]:.2f}", NAIVEC), (rf"$b = ({cf[i_ols][0]:.2f}, \ {cf[i_ols][1]:.2f})$", NAIVEC)],
            [(rf"$\gamma = {g[i_best]:.0f}$: \ test {te[i_best]:.2f}", FIXC), (rf"$b = ({cf[i_best][0]:.2f}, \ {cf[i_best][1]:.2f})$", FIXC)],
            [(rf"partialling out ($\gamma = 0$): \ {te[0]:.2f}", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulated system with a hidden confounder. The anchor pushes on X one and on X two; in "
            f"training its mean is zero, in the test environment three. <bookmark mark='b'/> As gamma grows, the training "
            f"error, in blue, rises a little: the fit gives up some in-sample accuracy. <bookmark mark='c'/> Least squares, "
            f"at gamma one, has test error {say(te[i_ols], 2)}. <bookmark mark='d'/> At gamma {g[i_best]:.0f}, the test error falls to "
            f"{say(te[i_best], 2)}, half of least squares': the coefficient on X one turns negative, cancelling the part of "
            f"the child X two that the anchor contaminates. <bookmark mark='e'/> Partialling the anchors out entirely, gamma "
            f"zero, is the worst of all, {say(te[0], 2)}: it fits exactly the directions that will shift."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l_tr), Create(l_te), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(mk[0]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mk[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def irm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In machine learning, Martin Arjovsky, Léon Bottou, Ishaan Gulrajani and David Lopez-Paz "
            "proposed invariant risk minimization in 2019: learn a representation on which the same classifier is optimal "
            "in every environment. <bookmark mark='b'/> Its theory is fragile: Elan Rosenfeld, Pradeep Ravikumar and Andrej "
            "Risteski showed in 2021 that it can fail unless there are more environments than spurious dimensions. "
            "<bookmark mark='c'/> And Gulrajani and Lopez-Paz's DomainBed comparison, the same year, found that careful "
            "ordinary training matched the many invariance methods on standard benchmarks. <bookmark mark='d'/> Invariance "
            "is a powerful idea where the environments are diverse and the causal structure is simple; with deep "
            "representations, it remains a promise more than a method.",
            [(r"\text{IRM}", r":", r"\text{one classifier optimal in every environment}", 40),
             (r"\text{fragile}", r":", r"\text{needs more environments than spurious dimensions}", 38),
             (r"\text{DomainBed}", r":", r"\text{careful ERM matches the invariance methods}", 38),
             (r"\text{so}", r":", r"\text{simple structure: \ yes; \ deep features: \ open}", 40)],
            [r"Arjovsky et al. (2019)", r"Rosenfeld, \ Ravikumar \& Risteski (2021)", r"Gulrajani \& Lopez-Paz (2021)", r"chapter 11"],
            colors=[(1, NAIVEC), (2, NAIVEC)])
