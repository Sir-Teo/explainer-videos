from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

RHO_COL = {"0.3": FAIL, "0.6": PUB, "0.9": TRUE}


class Remedies(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Remedies: \ plans, \ registered reports, \ many tests", r"What stops a researcher from "
             r"finding what they hoped to find?", "Chapter six. Remedies: plans, registered reports, many tests.",
             lit={2015: "Olken", 2018: "the JDE"}, scale=("world",), horizon=("a decade",))
        self.forking()
        self.plans()
        self.many_tests()

    def forking(self):
        F = load("forking")
        tries = np.array(F["tries"], float)
        lx = np.log10(tries)
        ax = plane([0, 2], [0, 1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[0, np.log10(2), np.log10(5), 1, np.log10(20), np.log10(50), 2],
                   yticks=[0, 0.05, 0.25, 0.5, 0.75, 1.0], xlabel=r"specifications tried \ (no effect is real)",
                   ylabel=r"chance of a significant result", xfmt=lambda v: f"{10 ** v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        five = seg(ax, 0, 0.05, 2, 0.05, GREY_B, 1.6, dashed=True)
        curves = VGroup(*[path(ax, lx, F["curves"][k], RHO_COL[k], 3.2, smooth=False) for k in ("0.3", "0.6",
                                                                                                  "0.9")])
        key = legend_rows([(RHO_COL["0.3"], "specifications that differ a lot"),
                           (RHO_COL["0.6"], "moderately alike"), (RHO_COL["0.9"], "nearly the same")],
                          font_size=15).next_to(ax.ax, RIGHT, buff=0.4).shift(UP * 1.2)
        c6 = F["curves"]["0.6"]
        k5, k20 = F["tries"].index(5), F["tries"].index(20)
        side = VGroup(
            label(rf"five tries: \ {100 * c6[k5]:.0f}\%", font_size=18, color=PUB),
            label(rf"twenty tries: \ {100 * c6[k20]:.0f}\%", font_size=18, color=PUB),
            label(r"the garden of forking paths: \\ no one needs to cheat", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = island_tag(r"computed: \ agora.field.false\_positive \ (equicorrelated $z$-statistics)", corner=DL,
                         font_size=12)
        with self.voiceover(
            "First, the size of the problem. <bookmark mark='a'/> Suppose nothing is real. A researcher who runs one "
            "pre-specified test finds a significant result five times in a hundred: that is what five percent "
            "means. <bookmark mark='b'/> But suppose they try several reasonable specifications and report the "
            f"first that works. If the specifications are moderately alike, five tries give a false positive "
            f"{100 * c6[k5]:.0f} percent of the time, and twenty give {100 * c6[k20]:.0f} percent. <bookmark "
            "mark='c'/> Specifications that differ more raise the rate faster; nearly identical ones barely raise "
            "it. <bookmark mark='d'/> Andrew Gelman and Eric Loken called this the garden of forking paths. No one "
            "needs to cheat: each choice can be made in good faith, after seeing the data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(five), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(Dot(ax.ax.c2p(0, 0.05), radius=0.08, color=WHITE)))
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(key[1]), run_time=1.8)
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curves[0]), Create(curves[2]), FadeIn(key[0]), FadeIn(key[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def plans(self):
        D = tables.REMEDIES_67.data
        cards = point_cards([
            (r"pre-analysis plans", r"outcomes, \ samples and specifications written down and registered before the "
             r"data are seen \ (the AEA's registry for trials since 2013)", TRUE),
            (r"their limits", r"Olken (2015): \ plans cannot anticipate everything, \ suit trials better than "
             r"observational work, \ and can crowd out discovery", PUB),
            (r"registered reports", rf"the design is reviewed and accepted before results exist: \ the JDE piloted it "
             rf"in {D['jde_start']} and kept it in {D['jde_permanent']}", FIRST),
            (r"what they buy", r"the result can no longer decide publication: \ null results enter the record", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"tying the hands in advance", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Olken, \ \emph{JEP} 29(3) (2015); \ the JDE and BITSS, \ pre-results review "
                            r"(2018--2019)", corner=DL, font_size=12)
        with self.voiceover(
            "The remedy for forking paths is to choose the path before seeing the garden. <bookmark mark='a'/> A "
            "pre-analysis plan writes down the outcomes, the sample and the specifications, and registers them, "
            "before the data are seen. The American Economic Association has kept a registry for randomized trials "
            "since 2013. <bookmark mark='b'/> Benjamin Olken weighed the promises and the perils: plans cannot "
            "anticipate everything, they suit trials better than observational work, and they can crowd out the "
            "discoveries nobody planned. <bookmark mark='c'/> Registered reports go further. The design is reviewed "
            "and accepted before the results exist. The Journal of Development Economics piloted this in 2018, "
            "and kept it. <bookmark mark='d'/> What that buys is simple: the result can no longer decide whether "
            "the paper is published, so null results enter the record."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def many_tests(self):
        F = load("forking")
        T = F["rules"]
        cols_ = (r"rule", r"any false positive", r"false positives", r"real effects found \ (of 3)")
        rows_ = [(r"each at 5\%", "none", FAIL), (r"Bonferroni", "Bonferroni", TRUE),
                 (r"Benjamini--Hochberg", "Benjamini-Hochberg", FIRST)]
        widths = (3.4, 2.9, 2.6, 3.2)

        def cell(txt, w, col=WHITE, size=19, fill=None):
            box = Rectangle(width=w, height=0.72, stroke_color=GREY_B, stroke_width=1.2,
                            fill_color=fill or BACKGROUND, fill_opacity=0.18 if fill else 0)
            return VGroup(box, label(txt, font_size=size, color=col).move_to(box))
        tab = VGroup(VGroup(*[cell(t, w, GREY_A, 17) for t, w in zip(cols_, widths)]).arrange(RIGHT, buff=0))
        for name, key, col in rows_:
            r = T[key]
            tab.add(VGroup(cell(name, widths[0], col, 19, col),
                           cell(rf"{100 * r['any_false']:.0f}\%", widths[1]),
                           cell(rf"{r['false']:.2f}", widths[2]),
                           cell(rf"{r['true']:.2f}", widths[3])).arrange(RIGHT, buff=0))
        tab.arrange(DOWN, buff=0).move_to(UP * 0.6)
        head = label(rf"a plan with {F['m']} outcomes, \ {F['real']} of them real \ (80\% power each)", font_size=24,
                     color=GREY_A).next_to(tab, UP, buff=0.4)
        lesson = VGroup(
            label(r"Bonferroni guards against any false positive, \ at the price of missing real effects",
                  font_size=20, color=TRUE),
            label(r"Benjamini and Hochberg control the share of discoveries that are false", font_size=20,
                  color=FIRST),
            label(r"which to use depends on the cost of each mistake \ (Part 4; \ \emph{Statistics, Built} 33)",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5)
        tag = island_tag(r"computed: \ 20,000 simulated studies", corner=DL, font_size=12)
        no_, bf, bh = T["none"], T["Bonferroni"], T["Benjamini-Hochberg"]
        p0, p1, p2 = (100 * x["any_false"] for x in (no_, bf, bh))
        with self.voiceover(
            f"A plan also counts the tests. <bookmark mark='a'/> A trial with {F['m']} pre-registered outcomes, three "
            "of them truly affected, each with eighty percent power. <bookmark mark='b'/> Test each at five percent "
            f"and the trial finds {no_['true']:.1f} of the three real effects on average, but {p0:.0f} "
            "percent of the time it also reports at least one false one. <bookmark mark='c'/> Bonferroni's rule, "
            f"which divides the five percent by the number of tests, cuts that to {p1:.0f} percent, "
            f"and finds only {bf['true']:.1f} real effects. <bookmark mark='d'/> Benjamini and Hochberg's rule "
            f"controls a different thing, the share of discoveries that are false, and sits between: {bh['true']:.1f} "
            f"real effects, a false one {p2:.0f} percent of the time. <bookmark mark='e'/> No rule "
            "is free; the choice depends on what each kind of mistake costs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(head))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(lesson[0]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(lesson[1]))
            vo.wait_until("e")
            self.play(FadeIn(lesson[2]))
        self.clear_scene()
