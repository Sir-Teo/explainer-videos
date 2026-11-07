from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class ListDecoding(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. List-decodable learning: when most of the data are not what you want.", 3,
                            r"List-decodable learning", r"When the inliers are a minority", lit=(2017,))
        self.problem()
        self.chart()
        self.theory()
        self.lower()
        self.uses()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What if the contamination is more than half? With an alpha fraction of inliers, alpha below "
            "a half, no single estimate can be right: the outliers could be a second, equally plausible population. "
            "<bookmark mark='b'/> Moses Charikar, Jacob Steinhardt and Gregory Valiant asked in 2017 for a list instead: a short "
            "list of candidates, one of which is close to the inliers' mean. <bookmark mark='c'/> The list must have about one "
            "over alpha entries, since the adversary can plant that many fake populations. <bookmark mark='d'/> Its best entry "
            "can achieve dimension-free error of order one over root alpha for bounded-covariance inliers, apart from sampling terms.",
            [(r"\alpha < \tfrac12", r":", r"\text{no single answer is identifiable}", 40),
             (r"\text{output}", r":", r"\text{a list } L, \ \ \min_{\ell \in L}\|\ell - \mu\| \text{ small}", 40),
             (r"|L|", r"\approx", r"1/\alpha", 40),
             (r"\text{accuracy}", r":", r"O(1/\sqrt\alpha), \ \text{bounded covariance + sampling terms}", 40)],
            [r"a majority of outliers", r"Charikar, \ Steinhardt \& Valiant (2017)", r"one per fake population", r"dimension-free"],
            colors=[(1, FIXC)])

    def chart(self):
        d = load("listdec")
        X = np.asarray(d["X"])
        A = axes([-5.5, 5.5], [-5.0, 4.5], x_length=6.0, y_length=5.0, xlabel=r"$x_1$", ylabel=r"$x_2$",
                 xticks=[-4, 0, 4], yticks=[-4, 0, 4], center=[-2.7, 0.0, 0])
        ax = A.ax
        inl = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=FIXC) for a, b in X[:d["n_in"]]])
        out = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=BADC) for a, b in X[d["n_in"]:]])
        lst = VGroup(*[VGroup(Dot(ax.c2p(a, b), radius=0.11, color=TGTC), Circle(radius=0.2, color=TGTC, stroke_width=2).move_to(ax.c2p(a, b))) for a, b in d["list"]])
        mean = Dot(ax.c2p(*d["mean"]), radius=0.11, color=NAIVEC)
        side = side_groups([
            [(r"300 points: \ 90 inliers (30\%)", WHITE), (r"three planted clusters of 70", BADC)],
            [(rf"red: \ the mean, \ {d['mean_err']:.2f} away", NAIVEC), (r"from the inliers' centre $(1, 1)$", NAIVEC)],
            [(r"gold: \ a list of $\lceil 1/\alpha \rceil = 4$", TGTC), (r"candidates, \ by clustering", TGTC)],
            [(rf"best entry: \ {d['best']:.2f} from $(1, 1)$", FIXC), (r"as close as the inliers' own mean", FIXC)],
            [(r"which is right needs", GREY_A), (r"outside information", GREY_A)],
        ], width=4.4, pos=(4.3, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A two-dimensional picture. Ninety inliers, thirty percent, and three planted clusters of "
            f"seventy points each. <bookmark mark='b'/> The overall mean, in red, is {say(d['mean_err'], 2)} from the inliers' "
            f"centre, near none of the groups. <bookmark mark='c'/> A list of four candidates, one over alpha rounded up, found "
            f"by clustering, <bookmark mark='d'/> has an entry {say(d['best'], 2)} from the inliers' centre: as close as the "
            f"mean of the ninety inliers themselves. <bookmark mark='e'/> Which entry is right "
            f"cannot be told from the data alone: a small labelled set, or a known property of the inliers, picks it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(inl), FadeIn(out), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(mean, scale=0.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l, scale=0.5) for l in lst], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def theory(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Clustering is adequate for these four well-separated groups. K-means has no adversarial list-decoding guarantee here. <bookmark mark='b'/> Theoretical algorithms use convex relaxation, filtering or moment certificates and need explicit inlier covariance and sample assumptions. <bookmark mark='c'/> For bounded covariance, dimension-free error of order one over root alpha is the reference scale. Runtime depends on the chosen accuracy, list size and model; we make no universal near-linear runtime claim. <bookmark mark='d'/> Crowdsourcing provides one motivation: a reliable minority may need a small amount of trusted information to select from the list.",
            [(r"\text{clustering}", r":", r"\text{fine when separated}", 40),
             (r"\text{no separation}", r":", r"\text{a convex program, \ then rounding}", 40),
             (r"\text{optimal}", r":", r"O(1/\sqrt\alpha) \ \text{for bounded-covariance inliers}", 40),
             (r"\text{use}", r":", r"\text{crowdsourcing with a reliable minority}", 40)],
            [r"the easy case", r"Charikar et al.", r"later work", r"Steinhardt's motivation"],
            colors=[(2, FIXC)])

    def uses(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Where list decoding is used. <bookmark mark='b'/> Clustering mixtures: each component is a "
            "minority, and list decoding finds every component's mean. <bookmark mark='c'/> Learning from untrusted sources: a "
            "trusted few verify the list. <bookmark mark='d'/> And robust regression with a majority of corrupted responses, "
            "where a short list of candidate regressions replaces a single fit.",
            [(r"where it is used:", GREY_A),
             (r"mixtures: \ each component is a minority", FIXC),
             (r"untrusted data: \ a trusted few verify the list", TGTC),
             (r"regression with mostly corrupted responses", DEPTHC)])

    def lower(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> List size and accuracy are separate questions, and both depend on the inlier model. <bookmark mark='b'/> Around one over alpha equally plausible clusters force a list of comparable order in worst-case constructions. The exact integer count involves rounding. <bookmark mark='c'/> For inliers with covariance bounded by the identity, the natural worst-case accuracy scale is one over root alpha, apart from sampling terms and the specified list-size regime. <bookmark mark='d'/> Gaussian inliers have additional structure and allow stronger accuracy guarantees with list-size and computational trade-offs. The bounded-covariance lower bound is not a Gaussian minimax theorem.",
            [(r"\text{list size}", r"\ge", r"\lfloor 1/\alpha\rfloor: \ \text{equally plausible clusters}", 38),
             (r"\text{symmetric}", r":", r"\text{no data can tell them apart}", 40),
             (r"\text{error}", r"\gtrsim", r"1/\sqrt\alpha: \ \text{a blended shift}", 40),
             (r"\text{both}", r":", r"\text{model, list size and sample assumptions matter}", 40)],
            [r"a counting argument", r"exchangeable groups", r"a moment-matching construction", r"Diakonikolas \& Kane (2023)"],
            colors=[(3, FIXC)])
