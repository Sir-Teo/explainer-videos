from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Multicalibration(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Multicalibration: calibrated for every group one can name.", 10,
                            r"Multicalibration", r"Sufficiency for many groups at once", lit=(2018,))
        self.idea()
        self.algorithm()
        self.history()
        self.groups()
        self.honest()
        self.conformal()
        self.family()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A model can calibrate overall while missing opposing subgroup errors. <bookmark mark='b'/> Multicalibration asks for small conditional residuals across a specified class of groups and sufficiently large score cells, including chosen intersections. <bookmark mark='c'/> For each protected group-bin cell, average outcome minus prediction should be small. A guarantee must specify the group class, bin resolution, tolerance and minimum cell mass. <bookmark mark='d'/> Rich computable group classes can be handled with an appropriate auditing oracle and sample complexity. No finite sample automatically protects every computable subgroup, including arbitrarily tiny or adaptively chosen cells.",
            [(r"\text{calibration}", r":", r"E[Y \mid R = v] = v", 40),
             (r"\text{multicalibration}", r":", r"|E[Y - R \mid G, R \approx v]| \le \alpha \ \ \forall G \in \mathcal{C}", 40),
             (r"\mathcal{C}", r":", r"\text{many groups, \ intersections}", 40),
             (r"\text{protects}", r":", r"\text{specified auditable class; minimum cell mass}", 40)],
            [r"too weak", r"H\'ebert-Johnson et al. (2018)", r"a rich class", r"class and complexity matter"],
            colors=[(1, OKC)])

    def algorithm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The algorithm is a patching loop, a cousin of boosting from Part thirty-four. <bookmark "
            "mark='b'/> Find a group and score bin where the average residual, outcome minus score, is largest. <bookmark "
            "mark='c'/> If it exceeds alpha, shift that cell's scores by the residual. <bookmark mark='d'/> Repeat. Each "
            "patch reduces the squared error by at least alpha squared times the cell's share, so the loop stops after at "
            "most order one over alpha squared, times one over the smallest share, patches, however many groups there are.",
            [(r"\text{find}", r":", r"(G, b) = \arg\max |\overline{Y - R}_{\,G, b}|", 40),
             (r"\text{patch}", r":", r"R \ \leftarrow \ R + \overline{Y - R}_{\,G, b} \ \text{on the cell}", 40),
             (r"\text{repeat}", r":", r"\text{until every cell is within } \alpha", 40),
             (r"\text{stops}", r":", r"\text{each patch cuts the squared error}", 40)],
            [r"like boosting", r"the worst cell", r"a shift", r"a potential argument"],
            colors=[(1, OKC)])

    def history(self):
        d = load("multical")
        h = np.asarray(d["train_hist"])
        it = np.arange(len(h))
        A = axes([0, len(h) - 1], [0, 0.11], x_length=7.2, y_length=4.2, xlabel=r"patch number",
                 ylabel=r"largest cell violation, \ training half", xticks=list(range(0, len(h), 3)), yticks=[0, 0.05, 0.1],
                 center=[-2.4, 0.2, 0])
        ax = A.ax
        thr = DashedLine(ax.c2p(0, 0.02), ax.c2p(len(h) - 1, 0.02), color=OKC, stroke_width=2)
        line = VGroup(polyline(ax, it, h, S.ACCENT, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=S.ACCENT) for a, b in zip(it, h)])
        side = side_groups([
            [(r"base model: \ logistic on age", WHITE), (r"and log prior offences; \ no race", WHITE)],
            [(r"groups: \ Black, \ white, \ women, \ under 25", GREY_A), (r"five score bins; \ cells of 100 or more", GREY_A)],
            [(rf"gold: \ worst violation, \ {h[0]:.3f} at the start", S.ACCENT)],
            [(rf"{len(h) - 1} patches: \ below $\alpha = 0.02$", OKC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> On the COMPAS data: a logistic regression on age and the log of prior offences, with "
            f"no race in it, fitted to a random half of the {6172:,} defendants. <bookmark mark='b'/> The groups: Black, "
            f"white, women, and people under twenty-five, crossed with five score bins, and only cells of at least a hundred "
            f"people. <bookmark mark='c'/> The worst cell starts {100 * h[0]:.0f} percentage points off. <bookmark "
            f"mark='d'/> {len(h) - 1} patches bring every cell within two points, alpha, on the training half."
        ) as vo:
            self.play(FadeIn(A), Create(thr), FadeIn(museum_tag(r"ProPublica's COMPAS data (the Museum)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(line[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(line[0]), FadeIn(VGroup(*line[2:])), FadeIn(side[3]), run_time=3)
        self.wait(1.0)
        self.clear_scene()

    def groups(self):
        d = load("multical")
        names = d["names"]
        per = d["per"]
        A = axes([-0.6, 3.6], [0, 0.085], x_length=7.4, y_length=4.2, xlabel=r"", ylabel=r"calibration gap on the held-out half",
                 xticks=None, yticks=[0, 0.02, 0.04, 0.06, 0.08], center=[-2.4, 0.3, 0])
        ax = A.ax
        bef, aft = VGroup(), VGroup()
        for k, nm in enumerate(names):
            for grp, key, dx, col in ((bef, "before", -0.2, BADC), (aft, "after", 0.2, OKC)):
                v = per[nm][key]
                b = Rectangle(width=0.36, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to(ax.c2p(k + dx, 0), aligned_edge=DOWN)
                grp.add(VGroup(b, label(rf"{v:.3f}", font_size=18, color=col).next_to(b, UP, buff=0.08)))
        ticks = VGroup(*[label(nm, font_size=22, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.2) for k, nm in enumerate(names)])
        side = side_groups([
            [(rf"{d['splits']} random halves; \ the patches", WHITE), (r"replayed on the other half", WHITE)],
            [(r"red: \ the base model", BADC), (r"green: \ after patching", OKC)],
            [(rf"women: \ {per['women']['before']:.3f} to {per['women']['after']:.3f}", OKC),
             (rf"under 25: \ {per['under 25']['before']:.3f} to {per['under 25']['after']:.3f}", OKC)],
            [(r"white-group gap increases; overall improvement", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The real test is on the other half, which the patches never saw, repeated over {d['splits']} random splits. The gap is the size-weighted average miscalibration across each group's score bins. <bookmark mark='b'/> In red the base model, in green after the patches. <bookmark mark='c'/> For women the gap falls from {say(per['women']['before'], 3)} to {say(per['women']['after'], 3)}, and for people under twenty-five from {say(per['under 25']['before'], 3)} to {say(per['under 25']['after'], 3)}: these absolute gaps describe errors without identifying their sign. Directional bias would need signed residuals, which this chart does not show. <bookmark mark='d'/> For the two race groups, the gaps were already small, about two to three points, consistent with the last chapter's calibration curves, and the white-group average gap increases. The displayed gaps alone do not establish population significance or fairness for every group."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ticks), FadeIn(museum_tag(r"ProPublica's COMPAS data (the Museum)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bef), FadeIn(side[1]))
            self.play(FadeIn(aft))
            vo.wait_until("c")
            self.play(Indicate(aft[2]), Indicate(aft[3]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def honest(self):
        d = load("multical")
        self.lad_voiceover(
            "<bookmark mark='a'/> Held-out calibration is better evidence than training calibration. Our reported gap is a size-weighted mean absolute cell residual across four overlapping groups, not the maximum multicalibration violation. <bookmark mark='b'/> The training average falls more than the test average, because patch selection fits residual noise as well as signal. <bookmark mark='c'/> Twenty random halves reuse the same defendants, so their split-to-split variability describes this resampling exercise; it is not uncertainty for independent new populations. The white-group average gap actually increases, even while the overall gap decreases. <bookmark mark='d'/> Population transfer requires complexity control for the audited class, confidence and cell-mass factors, not just one over alpha squared observations per cell. Our alpha .02 stopping criterion is an empirical eligible-cell condition, not a held-out population certificate.",
            [(r"\text{held out}", r":", rf"{d['before']:.3f} \ \to \ {d['after']:.3f}", 40),
             (r"\text{training}", r":", rf"{d['in_before']:.3f} \ \to \ {d['in_after']:.3f}", 40),
             (r"\text{the gap}", r":", r"\text{patches fit noise}", 40),
             (r"\text{theory}", r":", r"\text{class complexity, confidence and cell mass}", 40)],
            [r"real, \ smaller", r"optimistic", r"Part 56's winner's curse", r"generalization"],
            colors=[(0, OKC), (1, BADC)])

    def conformal(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part fifty-seven made the same move for prediction sets. <bookmark mark='b'/> Split "
            "conformal prediction covers ninety-five percent on average, and can cover far less in a subgroup. Mondrian "
            "conformal fixes coverage within a few named groups, by calibrating separately in each. <bookmark mark='c'/> "
            "Isaac Gibbs, John Cherian and Emmanuel Candes asked for coverage over a whole class of groups, or of weighting "
            "functions, at once, and achieved it with a quantile regression over that class, the conformal analogue of "
            "multicalibration. <bookmark mark='d'/> Both answer the same question: guaranteed on average is not guaranteed "
            "for you, so ask for every subpopulation one can describe, and pay with data.",
            [(r"\text{split conformal}", r":", r"\text{marginal coverage}", 40),
             (r"\text{Mondrian}", r":", r"\text{coverage in named groups}", 40),
             (r"\text{conditional conformal}", r":", r"\text{coverage over a class}", 40),
             (r"\text{shared idea}", r":", r"\text{guarantees for a specified function class}", 40)],
            [r"Part 57", r"group by group", r"Gibbs, \ Cherian \& Cand\`es", r"multicalibration's twin"],
            colors=[(2, OKC)])

    def family(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Several related notions extend this idea. <bookmark mark='b'/> Multiaccuracy controls average residuals over a specified function or group class without requiring score-bin calibration. <bookmark mark='c'/> Outcome indistinguishability restricts which tests can distinguish real outcomes from simulated model outcomes. Its strength depends on what the tests observe and their computational class. <bookmark mark='d'/> Omniprediction results post-process suitably multicalibrated scores into decisions competitive with a specified comparator class for a specified class of losses. This does not mean optimal for every loss or every possible decision. Exact sufficiency retains its conflict with separation under the usual nondegeneracy assumptions; approximate finite-class calibration needs quantitative analysis.",
            [(r"\text{multiaccuracy}", r":", r"E[Y - R \mid G] \approx 0", 40),
             (r"\text{outcome indistinguishability}", r":", r"\text{no test in a class can tell}", 40),
             (r"\text{omniprediction}", r":", r"\text{good for every loss at once}", 40),
             (r"\text{still}", r":", r"\text{sufficiency, \ not separation}", 40)],
            [r"Kim, \ Ghorbani \& Zou (2019)", r"Dwork et al. (2021)", r"Gopalan et al. (2022)", r"chapter 9"],
            colors=[(3, BADC)])
