from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class CausalFairness(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eleven. Causal fairness: which paths from the group to the decision are allowed?", 11,
                            r"Causal fairness", r"Fair along which paths?", lit=(2017,))
        self.limits()
        self.definition()
        self.graph()
        self.chart()
        self.paths()
        self.critique()
        self.rules()

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The criteria of chapter eight are all observational: statements about the joint "
            "distribution of score, outcome and group. <bookmark mark='b'/> Moritz Hardt and coauthors noted that two "
            "worlds with different causal structures can produce identical joint distributions, one in which the score "
            "uses the group through a legitimate path and one in which it uses it through an illegitimate one. <bookmark "
            "mark='c'/> No observational criterion can tell them apart. <bookmark mark='d'/> To say which dependence is "
            "unfair, one needs to say how it arose, and that is a causal question, Part thirty-six's territory.",
            [(r"\text{chapter 8}", r":", r"\text{statements about } P(R, Y, A)", 40),
             (r"\text{two worlds}", r":", r"\text{same distribution, \ different causes}", 40),
             (r"\text{so}", r":", r"\text{observational criteria cannot decide}", 40),
             (r"\text{needed}", r":", r"\text{a causal model}", 40)],
            [r"observational", r"Hardt, \ Price \& Srebro (2016)", r"indistinguishable", r"Part 36"],
            colors=[(2, BADC), (3, OKC)])

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Kusner and colleagues define counterfactual fairness within a structural causal model. <bookmark mark='b'/> Condition on an individual's observed information, infer a distribution of background factors, and compare predictions when the protected attribute is intervened on while those background factors are shared. <bookmark mark='c'/> Equality of these counterfactual predictive distributions is the criterion; a small group-average prediction gap does not establish it. <bookmark mark='d'/> Using genuine nondescendants can suffice. In a correctly specified additive model, subtracting the known structural effect of A recovers an invariant component. Ordinary regression residuals need not do that, especially with confounding, nonlinearities, clipping or an incorrectly estimated effect.",
            [(r"\text{SCM}", r":", r"U, \ A \ \to \ X \ \to \ \hat Y", 40),
             (r"\text{counterfactual fairness}", r":", r"\hat Y_{A \leftarrow a}(U) \overset{d}{=} \hat Y_{A \leftarrow a'}(U) \mid X, A", 40),
             (r"\text{sufficient}", r":", r"\text{use only non-descendants of } A", 40),
             (r"\text{linear case}", r":", r"\text{remove the correct structural effect, not any regression}", 40)],
            [r"Kusner et al. (2017)", r"Part 36's models", r"the individual counterfactual", r"a recipe"],
            colors=[(1, OKC)])

    def graph(self):
        G = CausalGraph({"A": (-2.2, 1.0), "U": (-2.2, -1.2), "P": (0.4, 0.0), "Y": (2.8, -1.2)},
                        [("A", "P"), ("U", "P"), ("U", "Y")], center=[-2.2, 0.0, 0], scale=1.0, radius=0.42,
                        colors={"A": GRPA, "U": GREY_A, "P": BADC, "Y": OKC},
                        labels={"A": r"$A$", "U": r"$U$", "P": r"index", "Y": r"$Y$"})
        side = side_groups([
            [(r"$A$: \ group, \ half the population", GRPA)],
            [(r"$U$: \ propensity, \ same in both groups", GREY_A)],
            [(r"index $= 1.5 + U + 1.2A +$ noise", BADC), (r"heavier policing of group A", BADC)],
            [(r"$Y$: \ rearrest, \ depends on $U$ only", OKC)],
        ], pos=(4.0, 0.2, 0))
        with self.voiceover(
            "<bookmark mark='a'/> Our revised toy uses a continuous prior-arrest measurement index, not an integer count. Train on ten thousand simulated people and evaluate on twenty thousand independent people. <bookmark mark='b'/> Background propensity U and measurement noise have the same law in both groups. <bookmark mark='c'/> The measurement is one point five plus U plus one point two times A plus noise. The coefficient one point two is known by construction. Subtracting it times A leaves one point five plus U plus noise, unchanged by a paired intervention on A. <bookmark mark='d'/> The outcome depends only on U in this toy. This deliberately specified model permits an oracle fair feature; real arrest data do not identify that decomposition automatically."
        ) as vo:
            self.play(FadeIn(G), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(G.node("A")))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(G.node("U")))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(G.path(["A", "P"], BADC)))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(G.path(["U", "Y"], OKC)))
        self.wait(1.0)
        self.clear_scene()

    def chart(self):
        d = load("cfair")
        vals = [d["true_gap"], d["priors"]["gap"], d["residual"]["gap"]]
        names = [r"true risk", r"score on priors", r"score on residual"]
        cols = [GREY_A, BADC, OKC]
        A = axes([-0.6, 2.6], [-0.03, 0.1], x_length=6.6, y_length=4.2, xlabel=r"", ylabel=r"group A minus the others",
                 xticks=None, yticks=[0, 0.025, 0.05, 0.075, 0.1], center=[-2.6, 0.3, 0])
        ax = A.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(2.6, 0), color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for k, (v, nm, c) in enumerate(zip(vals, names, cols)):
            h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            b = Rectangle(width=0.8, height=max(h, 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN if v >= 0 else UP)
            t = label(rf"{v:+.3f}", font_size=20, color=c).next_to(b, UP if v >= 0 else DOWN, buff=0.08)
            n = label(nm, font_size=20, color=GREY_A).next_to(ax.c2p(k, -0.03), DOWN, buff=0.15)
            bars.add(VGroup(b, t, n))
        side = side_groups([
            [(rf"grey: \ true rearrest gap, \ {d['true_gap']:+.3f}", GREY_A), (r"zero, \ up to sampling", GREY_A)],
            [(rf"red: \ logistic on priors: \ {d['priors']['gap']:+.3f}", BADC), (rf"AUC {d['priors']['auc']:.3f}", BADC)],
            [(rf"green: \ on the residual: \ {d['residual']['gap']:+.3f}", OKC), (rf"AUC {d['residual']['auc']:.3f}", OKC)],
            [(r"fairer and more accurate,", OKC), (r"because the bias was noise", OKC)],
        ], pos=(3.9, 0.3, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> The average score of group A minus that of the others. The true rearrest rates differ by {say(d['true_gap'], 3)}, zero up to sampling. <bookmark mark='b'/> A logistic regression on prior arrests scores group A {say(d['priors']['gap'], 3)} higher, about nine points, with an area under the ROC curve of {say(d['priors']['auc'], 2)}. <bookmark mark='c'/> A regression on the oracle structural residual after subtracting the known coefficient one point two times A, a function of U and noise only, scores the groups within {say(abs(d['residual']['gap']), 3)} of each other, and its area under the curve is higher, {say(d['residual']['auc'], 2)}. <bookmark mark='d'/> Here fairness and accuracy agree, because the extra priors were measurement error with respect to risk. That is a property of this specified causal model. Directly paired counterfactual predictions agree to numerical precision for the oracle residual and change for the raw index. Group-average gaps and AUC alone would not prove counterfactual fairness."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def paths(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Not every path from the group is unfair. <bookmark mark='b'/> Niki Kilbertus and "
            "colleagues, also in 2017, separated proxy variables from resolving variables: a path through a variable "
            "chosen freely, such as the department applied to, may be acceptable, while a path through a proxy for the "
            "group is not. <bookmark mark='c'/> Razieh Nabi and Ilya Shpitser made it a path-specific effect, Part "
            "thirty-six's mediation analysis: constrain the effect of A along the forbidden paths only, and estimate the "
            "best predictor subject to that. <bookmark mark='d'/> Which paths are forbidden is a moral and legal choice; "
            "once made, the statistics are identification and estimation, as in Part sixty-two.",
            [(r"\text{resolving variables}", r":", r"\text{acceptable paths}", 40),
             (r"\text{proxies}", r":", r"\text{forbidden paths}", 40),
             (r"\text{path-specific}", r":", r"\text{constrain effects on forbidden paths}", 40),
             (r"\text{then}", r":", r"\text{identify and estimate}", 40)],
            [r"Kilbertus et al. (2017)", r"proxies", r"Nabi \& Shpitser (2018)", r"Part 62"],
            colors=[(2, OKC)])

    def critique(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The approach has critics. <bookmark mark='b'/> It needs a counterfactual: what would "
            "this person's record have been, had their race been different? The legal scholar Issa Kohler-Hausmann argued "
            "that race is not a variable one can intervene on while holding the rest of a life fixed, because so much of a "
            "life is constituted by it. <bookmark mark='c'/> And the answer depends entirely on an unverifiable model, here "
            "of how policing adds priors. A different model gives a different fair predictor. <bookmark mark='d'/> The "
            "honest position, as in Part sixty-two's sensitivity analysis: state the causal assumptions, show how the "
            "conclusion moves when they change, and let the reader judge.",
            [(r"\text{the counterfactual}", r":", r"\text{race as an intervention?}", 40),
             (r"\text{the model}", r":", r"\text{unverifiable from the data}", 40),
             (r"\text{different model}", r":", r"\text{different fair predictor}", 40),
             (r"\text{honest}", r":", r"\text{assumptions, \ then sensitivity}", 40)],
            [r"Kohler-Hausmann (2019)", r"the policing model", r"no free lunch", r"Part 62"],
            colors=[(0, BADC), (3, OKC)])

    def rules(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Fairness also enters decisions, not just predictions. <bookmark mark='b'/> Part "
            "sixty-two learned treatment rules by maximizing estimated welfare over a class. Fairness constraints change the "
            "class: rules whose benefit, or whose error rates, are balanced across groups. <bookmark mark='c'/> And "
            "decisions change the future data. Lydia Liu and colleagues showed in 2018 that a fairness constraint imposed "
            "once can, through its effect on the next period's outcomes, help a group or harm it, depending on the dynamics. "
            "<bookmark mark='d'/> Fairness in one period is a static criterion; the people affected live in many.",
            [(r"\text{fair rules}", r":", r"\max_{\pi \in \Pi_{\text{fair}}} \hat V(\pi)", 40),
             (r"\Pi_{\text{fair}}", r":", r"\text{balanced benefits or errors}", 40),
             (r"\text{dynamics}", r":", r"\text{decisions change the next data}", 40),
             (r"\text{delayed impact}", r":", r"\text{can help, \ or harm}", 40)],
            [r"Part 62's policy learning", r"a constrained class", r"Liu et al. (2018)", r"open problem 4"],
            colors=[(3, BADC)])
