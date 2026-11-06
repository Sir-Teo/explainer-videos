from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Outcomes(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Potential outcomes", r"What would have happened to this very patient?",
                            lit=(1923, 1974), part=PART)
        with self.voiceover("Chapter thirteen. Potential outcomes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rubin()
        self.randomize()
        self.bridge()
        self.instrument()
        self.did()

    def rubin(self):
        d = load("outcomes")["doctor"]
        head = label(r"Rubin's perfect doctor", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{patient}", r"Y(0)", r"Y(1)", r"\text{doctor gives}", r"\text{observed}"]

        def cell(v, shown, c):
            return MathTex(str(v) if shown else "?", font_size=24, color=c if shown else GREY_C)
        rows_full, rows_obs = [], []
        for i in range(len(d["y0"])):
            t = d["doctor"][i]
            rows_full.append([MathTex(str(i + 1), font_size=24), cell(d["y0"][i], True, CAUSE),
                              cell(d["y1"][i], True, EFFECT),
                              MathTex(r"\text{drug}" if t else r"\text{none}", font_size=22, color=DOC),
                              MathTex(str(d["observed"][i]), font_size=24)])
            rows_obs.append([MathTex(str(i + 1), font_size=24), cell(d["y0"][i], not t, CAUSE),
                             cell(d["y1"][i], bool(t), EFFECT)])
        grid = ValueGrid(hd, rows_full, col_w=[1.4, 1.2, 1.2, 2.2, 1.6], cell_h=0.44, font_size=20).move_to(
            [-2.6, -0.2, 0])
        obs_cells = [VGroup(grid.cell[i][1], grid.cell[i][2]) for i in range(len(rows_full))]
        q = [VGroup(rows_obs[i][1], rows_obs[i][2]) for i in range(len(rows_full))]
        for i in range(len(rows_full)):
            q[i][0].move_to(grid.cell[i][1])
            q[i][1].move_to(grid.cell[i][2])
        side = stack([(r"years lived without and with the drug", GREY_A),
                      (r"true average effect: \ $E[Y(1) - Y(0)] = " + f"{d['ate']:.1f}" + r"$", BAD),
                      (r"the doctor gives each patient the better option", DOC),
                      (r"observed: \ treated live " + f"{d['naive']:.1f}" + r" years longer", OK),
                      (r"Holland \ (1986): \ we never see both $Y(0)$ and $Y(1)$ for one unit", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=5.4).move_to([4.2, 0.0, 0])
        with self.voiceover(
            "The second great framework for causation comes from statistics. Jerzy Neyman introduced it in 1923 "
            "for agricultural trials, and Donald Rubin made it general in 1974. <bookmark mark='a'/>Each patient has "
            "two potential outcomes: years lived without the drug, and years lived with it. "
            "<bookmark mark='b'/>Here the drug is harmful: on average it costs two years. "
            "<bookmark mark='c'/>Now a perfect doctor, who knows every patient's outcomes, gives each patient "
            "whichever option is better for them. <bookmark mark='d'/>Compare the treated with the untreated, and "
            "the drug appears to add five point six years. <bookmark mark='e'/>Paul Holland called this the "
            "fundamental problem of causal inference: for each patient we see only one potential outcome, never "
            "both. Causal inference is a missing-data problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule),
                      *[FadeIn(VGroup(*grid.cell[i][:3])) for i in range(len(rows_full))])
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[FadeIn(grid.cell[i][3]) for i in range(len(rows_full))])
            vo.wait_until("d")
            self.play(FadeIn(side[3]), *[FadeIn(grid.cell[i][4]) for i in range(len(rows_full))])
            vo.wait_until("e")
            self.play(*[ReplacementTransform(obs_cells[i], q[i]) for i in range(len(rows_full))], FadeIn(side[4]))
        self.clear_scene()

    def randomize(self):
        d = load("outcomes")["doctor"]
        head = label(r"Randomization: \ every assignment, \ enumerated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        diffs = d["rand_diffs"]
        lo, hi = -8, 4
        bins = [0] * 12
        for x in diffs:
            bins[min(11, int((x - lo) // 1))] += 1
        ax = Axes(x_range=[lo, hi, 2], y_range=[0, max(bins) * 1.2, 5], x_length=7.4, y_length=3.4,
                  axis_config={"color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": list(range(lo, hi + 1, 2))}).move_to([-2.3, 0.0, 0])
        ax.y_axis.set_opacity(0)
        bars = VGroup(*[Rectangle(width=ax.x_axis.unit_size * 0.9, height=max(1e-3, ax.y_axis.unit_size * b),
                                  stroke_width=1, stroke_color=CAUSE, fill_color=CAUSE, fill_opacity=0.5).move_to(
            ax.c2p(lo + i + 0.5, b / 2)) for i, b in enumerate(bins)])
        ate = DashedLine(ax.c2p(d["ate"], 0), ax.c2p(d["ate"], max(bins) * 1.15), color=BAD)
        al = label(r"true effect " + f"{d['ate']:.1f}", font_size=18, color=BAD).next_to(ate, UP, buff=0.08)
        side = stack([(f"{d['n_assign']}" + r" ways to treat 4 of 8", WHITE),
                      (r"mean of the differences: \ " + f"{d['rand_mean']:.2f}" + r": \ unbiased", OK),
                      (r"but " + f"{100 * d['frac_wrong_sign']:.0f}" + r"\% of them get the sign wrong", BAD),
                      (r"randomization: \ treatment independent of $(Y(0), Y(1))$", GOAL),
                      (r"sample size makes the estimate precise", GOAL),
                      (r"SUTVA: \ no interference between units, \ one version of treatment", GREY_A)],
                     font_size=20, aligned_edge=LEFT, width=4.6).move_to([4.5, 0.0, 0])
        with self.voiceover(
            "Fisher's answer is randomization. <bookmark mark='a'/>There are seventy ways to give the drug to four "
            "of the eight patients. The Reasoner enumerates every one and computes the observed difference in "
            "means. <bookmark mark='b'/>Their average is exactly minus two: the true effect. A randomized "
            "comparison is unbiased. <bookmark mark='c'/>But with eight patients, thirty percent of the "
            "assignments get even the sign wrong. <bookmark mark='d'/>Randomization makes who is treated "
            "independent of the potential outcomes; only sample size makes the estimate precise. "
            "<bookmark mark='e'/>And the framework needs an assumption Rubin named SUTVA: one patient's treatment "
            "does not affect another's outcome, and there is only one version of the treatment. Vaccines, which "
            "protect the unvaccinated too, break it."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ate), FadeIn(al), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[b.animate.set_fill(BAD, opacity=0.6) for i, b in enumerate(bars) if lo + i >= 0],
                      FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def bridge(self):
        head = label(r"Two languages, \ one theory", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"Y_x(u) \;:=\; \text{the value of } Y \text{ in the model } M_{do(X = x)} \text{ with background } u",
                     font_size=30, color=GOAL).next_to(head, DOWN, buff=0.4)
        rows = [
            (r"potential outcome", r"$Y(1)$, \ $Y(0)$ \ $\Longleftrightarrow$ \ $Y_{x}$ in a structural model", EFFECT),
            (r"ignorability", r"$(Y(0), Y(1)) \perp X \mid Z$ \ $\Longleftrightarrow$ \ $Z$ satisfies the back-door "
                              r"criterion \ (roughly)", EFFECT),
            (r"Galles and Pearl \ (1998)", r"composition, \ effectiveness, \ reversibility: \ the same counterfactual "
                                           r"logic", OK),
            (r"the quarrel", r"graphs make assumptions visible \ (Pearl); \ ignorability states only what estimation "
                             r"needs \ (Imbens, \ 2020)", CAUSE),
            (r"Dawid \ (2000)", r"causal inference without counterfactuals: \ decisions, \ not unobservable worlds", BAD),
        ]
        g = rows_table(rows, top=1.4, gap=0.42, width=8.6, x_text=-2.4)
        with self.voiceover(
            "How does this relate to structural models? <bookmark mark='a'/>Pearl's answer: a potential outcome is "
            "the value Y takes in the model where X has been set by surgery, for a given background. "
            "<bookmark mark='b'/>So Rubin's notation and Pearl's say the same thing. <bookmark mark='c'/>Rubin's "
            "key assumption, that treatment is ignorable given some covariates, corresponds to those covariates "
            "satisfying the back-door criterion. <bookmark mark='d'/>David Galles and Pearl proved the two "
            "frameworks obey the same logic of counterfactuals. <bookmark mark='e'/>The quarrel is practical. "
            "Pearl says graphs make assumptions visible and checkable; Guido Imbens replies that economists find "
            "ignorability, stated directly, closer to what estimation needs. <bookmark mark='f'/>And Philip Dawid "
            "argues that unobservable counterfactuals are unnecessary: causal inference is about decisions, and "
            "can be done with ordinary probability."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            for mk, r in zip("bcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def instrument(self):
        d = load("outcomes")["iv"]
        head = label(r"Instrumental variables \ (Philip Wright, \ 1928)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        g = CausalGraph({"Z": [-5.6, -0.2, 0], "X": [-3.6, -0.2, 0], "Y": [-1.4, -0.2, 0], "U": [-2.5, 1.4, 0]},
                        [("Z", "X"), ("X", "Y"), ("U", "X"), ("U", "Y")], hidden=("U",), radius=0.4, font_size=20,
                        colors={"Z": DOC, "X": CAUSE, "Y": EFFECT}, dashed=(("U", "X"), ("U", "Y")))
        eq = MathTex(r"\hat\beta_{IV} = \frac{\mathrm{cov}(Z, Y)}{\mathrm{cov}(Z, X)}", font_size=36,
                     color=GOAL).move_to([3.2, 1.4, 0])
        side = stack([(r"$Z$ moves $X$, \ and reaches $Y$ only through $X$", DOC),
                      (r"truth $\beta = " + f"{d['beta']:.1f}" + r"$", WHITE),
                      (r"least squares: \ " + f"{d['ols']:.2f}" + r" \ \ (biased by $U$)", BAD),
                      (r"instrument: \ " + f"{d['iv']:.2f}" + r" \ \ ($n = " + f"{d['n']:,}".replace(",", "{,}") + r"$)",
                       OK),
                      (r"quarter of birth and schooling \ (Angrist and Krueger, \ 1991); \ LATE \ (Imbens and Angrist, "
                       r"\ 1994); \ Nobel 2021", GREY_A)], font_size=20, aligned_edge=LEFT, width=6.2).next_to(
            eq, DOWN, buff=0.4)
        with self.voiceover(
            "When confounders are hidden and no front door exists, economists reach for an instrument. "
            "<bookmark mark='a'/>The idea goes back to Philip Wright in 1928, estimating the supply and demand for "
            "flaxseed and butter. An instrument Z shifts the treatment X, and affects the outcome only through X. "
            "<bookmark mark='b'/>Then the ratio of two covariances estimates the effect. "
            "<bookmark mark='c'/>In the Reasoner's simulation the true effect is point five. "
            "<bookmark mark='d'/>Least squares gives one point zero seven, inflated by the hidden confounder. "
            "<bookmark mark='e'/>The instrument gives point four nine. <bookmark mark='f'/>Joshua Angrist and Alan "
            "Krueger used the quarter of a person's birth, which affects how long they must stay in school, to "
            "estimate the return to education; Imbens and Angrist showed what an instrument identifies when effects "
            "vary across people: the effect among those the instrument moves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(eq))
            for mk, r in zip("cdef", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def did(self):
        d = load("outcomes")["did"]
        head = label(r"Difference in differences \ (Card and Krueger, \ 1994)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax = Axes(x_range=[0, 1.2, 1], y_range=[18, 25, 1], x_length=6.0, y_length=4.0,
                  axis_config={"color": GREY_B, "include_ticks": False}).move_to([-3.0, -0.3, 0])
        ax_lab = VGroup(label(r"Feb 1992", font_size=18, color=GREY_A).next_to(ax.c2p(0.1, 18), DOWN, buff=0.15),
                        label(r"Nov 1992", font_size=18, color=GREY_A).next_to(ax.c2p(1.1, 18), DOWN, buff=0.15),
                        label(r"jobs per restaurant", font_size=18, color=GREY_A).next_to(ax.c2p(0, 25), UP,
                                                                                         buff=0.1))
        nj = VGroup(Line(ax.c2p(0.1, d["NJ"][0]), ax.c2p(1.1, d["NJ"][1]), color=CAUSE, stroke_width=4),
                    Dot(ax.c2p(0.1, d["NJ"][0]), color=CAUSE), Dot(ax.c2p(1.1, d["NJ"][1]), color=CAUSE))
        pa = VGroup(Line(ax.c2p(0.1, d["PA"][0]), ax.c2p(1.1, d["PA"][1]), color=EFFECT, stroke_width=4),
                    Dot(ax.c2p(0.1, d["PA"][0]), color=EFFECT), Dot(ax.c2p(1.1, d["PA"][1]), color=EFFECT))
        cf_end = d["NJ"][0] + (d["PA"][1] - d["PA"][0])
        cf = DashedLine(ax.c2p(0.1, d["NJ"][0]), ax.c2p(1.1, cf_end), color=CAUSE, stroke_opacity=0.6)
        gap = DoubleArrow(ax.c2p(1.15, cf_end), ax.c2p(1.15, d["NJ"][1]), buff=0, color=GOAL, stroke_width=3,
                          tip_length=0.15)
        lj = label(r"New Jersey \ (wage rises)", font_size=18, color=CAUSE).next_to(ax.c2p(0.1, d["NJ"][0]), UP,
                                                                                    buff=0.15).shift(RIGHT * 0.9)
        lp = label(r"Pennsylvania", font_size=18, color=EFFECT).next_to(ax.c2p(0.1, d["PA"][0]), UP, buff=0.12).shift(
            RIGHT * 0.6)
        side = stack([(r"after only, \ NJ $-$ PA: \ " + f"{d['naive_after']:.1f}", BAD),
                      (r"before and after, \ NJ alone: \ $+" + f"{d['before_after_NJ']:.1f}" + r"$", BAD),
                      (r"difference in differences: \ $+" + f"{d['did']:.1f}" + r"$", OK),
                      (r"the assumption: \ parallel trends \ (the dashed line)", GOAL),
                      (r"John Snow \ (1855): \ two water companies, \ one parish: \ cholera's cause", GREY_A),
                      (r"also: \ regression discontinuity \ (Thistlethwaite and Campbell, \ 1960)", GREY_A)],
                     font_size=20, aligned_edge=LEFT, width=5.6).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "Another design uses time. <bookmark mark='a'/>In 1992 New Jersey raised its minimum wage; neighbouring "
            "Pennsylvania did not. David Card and Alan Krueger counted jobs at fast-food restaurants in both states, "
            "before and after. <bookmark mark='b'/>Compare the states only afterwards, and New Jersey has fewer "
            "jobs; but it had fewer before. <bookmark mark='c'/>Compare New Jersey with itself, and jobs rose; but "
            "the whole region's economy was changing. <bookmark mark='d'/>The difference in differences subtracts "
            "Pennsylvania's change from New Jersey's: jobs rose by about two point seven per restaurant relative to "
            "the trend, against the textbook prediction. <bookmark mark='e'/>The assumption is parallel trends: "
            "without the law, New Jersey would have followed Pennsylvania's path, the dashed line. "
            "<bookmark mark='f'/>The design is old. John Snow, in 1855, compared London households in one area "
            "served by two water companies, one drawing sewage-laden water from the Thames, and found cholera's "
            "cause. <bookmark mark='g'/>Regression discontinuity, comparing people just either side of a cutoff, "
            "completes the economist's toolkit of natural experiments."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ax_lab))
            vo.wait_until("a")
            self.play(FadeIn(nj), FadeIn(pa), FadeIn(lj), FadeIn(lp))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(cf), GrowFromCenter(gap), FadeIn(side[2]))
            for mk, r in zip("efg", side[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
