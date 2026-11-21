from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Schools(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Schools: \ class size and teachers", r"What does a school produce, and with what?",
             "Chapter eight. Schools: class size and teachers.", lit={1999: r"Krueger; Angrist and Lavy",
                                                                     2014: r"Chetty et al."},
             scale=("person", "city"), horizon=("a year", "a lifetime"))
        self.california()
        self.star()
        self.maimonides()
        self.teachers()

    def california(self):
        C = load("caschools")
        x, y = np.array(C["str"]), np.array(C["score"])
        ax = plane([13.5, 26.5], [600, 710], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[14, 16, 18, 20, 22, 24, 26], yticks=[600, 630, 660, 690], xlabel=r"pupils per teacher",
                   ylabel=r"average test score", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.035, color=SCHOOL, fill_opacity=0.6) for a, b in zip(x, y)])
        fit = seg(ax, 14, C["naive_a"] + 14 * C["naive"], 26, C["naive_a"] + 26 * C["naive"], CHILD, 3.2)
        side = VGroup(
            label(rf"{C['n']} California \\ districts, \ 1998--99", font_size=18, color=WHITE),
            label(rf"one pupil more per \\ teacher: \ {C['naive']:.2f} points".replace("-", "{-}"), font_size=18,
                  color=CHILD),
            label(r"but small classes are \\ in richer districts, \\ with fewer pupils \\ learning English",
                  font_size=17, color=HOLD),
            label(rf"allow for those two: \\ {C['controls']:.2f} \ (s.e. {C['controls_se']:.2f})".replace("-", "{-}"),
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"California Department of Education, \ via Stock and Watson and AER", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Schools are where the economic approach has been most argued over, because so much public money is "
            f"at stake. <bookmark mark='a'/> Here are California's {C['n']} elementary districts at the end of the "
            "1990s, the textbook data of Stock and Watson: average test scores against the number of pupils per "
            f"teacher. <bookmark mark='b'/> One more pupil per teacher goes with a score {abs(C['naive']):.2f} "
            "points lower. <bookmark mark='c'/> But smaller classes are found in richer districts, with fewer "
            "children still learning English, and those children would score higher anyway. <bookmark mark='d'/> "
            "Allow for those two differences and the slope falls by more than half, to "
            f"{say_num(C['controls'], 2)}. Which differences have been missed? A comparison like this can never be "
            "sure. An experiment can."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), fit.animate.set_opacity(0.4))
        self.clear_scene()

    def star(self):
        S = load("star")
        qs = np.array(S["qs"])
        gap = np.array(S["q_small"]) - np.array(S["q_regular"])
        axL = plane([0, 3], [40, 60], center=LEFT * 4.0 + DOWN * 0.35, x_length=3.8, y_length=4.2, xticks=[],
                    yticks=[40, 45, 50, 55, 60], ylabel=r"average percentile", yfmt=lambda v: f"{v:.0f}",
                    font_size=13)
        bars = VGroup()
        for i, (t, col) in enumerate((("small", SMALL), ("regular", REGULAR), ("regular+aide", GREY_A))):
            v = S["means"][t]
            p0, p1 = axL.ax.c2p(i + 0.2, 40), axL.ax.c2p(i + 0.8, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(f"{v:.1f}", font_size=14, color=WHITE).next_to(r, UP, buff=0.05),
                            label(t.replace("regular+aide", r"with \\ an aide"), font_size=14,
                                  color=col).next_to(axL.ax.c2p(i + 0.5, 40), DOWN, buff=0.15)))
        axR = plane([0, 1], [-2, 12], center=RIGHT * 0.9 + DOWN * 0.35, x_length=4.6, y_length=4.2,
                    xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 5, 10], xlabel=r"pupils ranked, \ lowest to highest",
                    ylabel=r"small minus regular, \ percentile points", xfmt=lambda v: f"{100 * v:.0f}\\%",
                    yfmt=lambda v: f"{v:.0f}", font_size=13)
        zero = DashedLine(axR.ax.c2p(0, 0), axR.ax.c2p(1, 0), color=GREY_B, stroke_width=1.4)
        gl = path(axR, qs, gap, SMALL, 3.2)
        sub = S["sub"]
        side = VGroup(
            label(rf"Tennessee, \ 1985: \ {S['n']:,} \\ kindergarteners in \\ {S['schools']} schools, \ assigned "
                  r"\\ at random".replace(",", "{,}"), font_size=16, color=WHITE),
            label(r"small classes: \ 13--17; \\ regular: \ 22--25", font_size=16, color=SMALL),
            label(rf"small, \ within schools: \\ {S['small']:+.1f} percentile points \\ (s.e. {S['small_se']:.1f})",
                  font_size=16, color=SMALL),
            label(rf"an aide: \ {S['aide']:+.1f} \ (s.e. {S['aide_se']:.1f})", font_size=16, color=GREY_A),
            label(rf"free lunch: \ {sub['free lunch']['small']:+.1f}; \\ black pupils: \ "
                  rf"{sub['black pupils']['small']:+.1f}; \\ white: \ {sub['white pupils']['small']:+.1f}",
                  font_size=16, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.25)
        tag = data_tag(r"Project STAR, \ via Stock and Watson and AER; \ estimated here", corner=DL, font_size=12)
        with self.voiceover(
            "In 1985 Tennessee ran one. <bookmark mark='a'/> Project STAR assigned "
            f"{S['n']:,} kindergarten pupils in {S['schools']} schools, and their teachers, at random to small "
            "classes of thirteen to seventeen, regular classes of twenty-two to twenty-five, or regular classes "
            "with a teacher's aide. <bookmark mark='b'/> Here are the scores at the end of kindergarten, reading "
            "and maths together, as percentiles of the regular classes: the small classes averaged "
            f"{S['means']['small']:.1f}, the others about {S['means']['regular']:.0f}. On the right, the gap at "
            "every rank, from the weakest pupils to the strongest: it is positive all the way along. <bookmark "
            f"mark='c'/> Comparing pupils within the same school, small classes scored {S['small']:.1f} percentile "
            f"points higher, with a standard error of {S['small_se']:.1f}. <bookmark mark='d'/> The aides did "
            "nothing measurable. <bookmark mark='e'/> The gains were larger for poor children and for black "
            "children. Alan Krueger, analysing the same experiment, put the first year's gain at about four points, "
            "growing about a point a year after."
        ) as vo:
            self.play(FadeIn(axL), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=WHITE, scale_factor=1.04))
            self.play(FadeIn(axR), Create(zero), run_time=0.8)
            self.play(Create(gl), run_time=2.5)
            for mk, r_ in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def maimonides(self):
        M = load("maimonides")
        e = np.array(M["rule_e"])
        ax = plane([0, 162], [0, 45], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 40, 80, 120, 160], yticks=[0, 10, 20, 30, 40], xlabel=r"pupils enrolled in the grade",
                   ylabel=r"average class size", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        saw = path(ax, e, M["rule"], CHILD, 3.2, smooth=False)
        en, cs = np.array(M["enrolment"]), np.array(M["class_size"])
        k = np.arange(0, len(en), 4)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.025, color=SCHOOL, fill_opacity=0.5) for a, b in zip(en[k],
                                                                                                        cs[k])])
        cuts = VGroup(*[vline(ax, c + 0.5, 0, 45, GREY_B, 1.4) for c in (40, 80, 120)])
        side = VGroup(
            label(r"Maimonides: \ no more \\ than 40 to a class", font_size=17, color=CHILD),
            label(r"41 pupils: \ two classes \\ of 20 or 21", font_size=17, color=WHITE),
            label(rf"the Island: \ naive \\ {M['naive']:+.3f} per pupil".replace("-", "{-}"), font_size=17,
                  color=HOLD),
            label(rf"at the cutoffs: \\ {M['iv']:+.3f} \ (truth \ {M['effect']:+.3f})".replace("-", "{-}"),
                  font_size=17, color=GAIN),
            label(r"Israel, \ 1991: \ gains; \\ 2002--11: \ none, \ and \\ schools bunch just \\ above the cutoffs",
                  font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Angrist and Lavy, \ QJE (1999); \ Angrist et al., \ AER: Insights (2019)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "Israel has an older rule, from the twelfth-century scholar Maimonides: no more than forty pupils to a "
            "class. <bookmark mark='a'/> So a grade of forty is one class of forty, <bookmark mark='b'/> but a grade "
            "of forty-one is split into two classes of twenty or twenty-one. Class size falls off a cliff at each "
            "multiple of forty, for reasons that have nothing to do with the pupils. <bookmark mark='c'/> On the "
            "Island, where bigger schools are in richer towns, the naive slope of scores on class size is about "
            f"zero. <bookmark mark='d'/> Comparing schools just either side of the cutoffs recovers the planted "
            f"effect: {say_num(M['iv'], 3)} standard deviations per pupil. <bookmark mark='e'/> Joshua Angrist and "
            "Victor Lavy found gains from smaller classes in Israel's 1991 data. Returning with data from 2002 to "
            "2011, Angrist, Lavy and colleagues found none, and found something else: too many schools enrolled "
            "just enough pupils to get the extra class. Where a rule pays, people learn to meet it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(Create(saw), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(saw, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(cuts), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.004), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def teachers(self):
        T = load("teachers")
        Cl, So = T["clean"], T["sorted"]
        tr, raw, sh = np.array(Cl["true"]), np.array(Cl["raw"]), np.array(Cl["shrunk"])
        axL = plane([-0.45, 0.45], [-0.45, 0.45], center=LEFT * 3.6 + DOWN * 0.35, x_length=4.6, y_length=4.4,
                    xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[-0.4, -0.2, 0, 0.2, 0.4],
                    xlabel=r"a teacher's true effect", ylabel=r"estimated",
                    xfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"),
                    font_size=13)
        diag = seg(axL, -0.4, -0.4, 0.4, 0.4, GREY_B, 1.6, dashed=True)
        p_raw = VGroup(*[Dot(axL.ax.c2p(a, b), radius=0.03, color=HOLD) for a, b in zip(tr, raw)])
        p_sh = VGroup(*[Dot(axL.ax.c2p(a, b), radius=0.03, color=SCHOOL) for a, b in zip(tr, sh)])
        dv, ds = np.array(Cl["d_va"]), np.array(Cl["d_score"])
        dvs, dss = np.array(So["d_va"]), np.array(So["d_score"])
        axR = plane([-0.25, 0.25], [-0.25, 0.25], center=RIGHT * 1.6 + DOWN * 0.35, x_length=4.4, y_length=4.4,
                    xticks=[-0.2, 0, 0.2], yticks=[-0.2, 0, 0.2], xlabel=r"change in the teachers' predicted effect",
                    ylabel=r"change in scores", xfmt=lambda v: f"{v:.1f}".replace("-", "{-}"),
                    yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=13)
        one = seg(axR, -0.22, -0.22, 0.22, 0.22, GREY_B, 1.6, dashed=True)
        p_mv = VGroup(*[Dot(axR.ax.c2p(a, b), radius=0.03, color=SCHOOL) for a, b in zip(dv, ds)
                        if abs(a) < 0.25 and abs(b) < 0.25])
        p_mvs = VGroup(*[Dot(axR.ax.c2p(a, b), radius=0.03, color=LOSS) for a, b in zip(dvs, dss)
                         if abs(a) < 0.25 and abs(b) < 0.25])
        side = VGroup(
            label(rf"raw: \ spread {Cl['sd_raw']:.2f} \\ against a true {Cl['sd_true']:.2f}", font_size=16,
                  color=HOLD),
            label(rf"shrunk by reliability \\ {Cl['reliability']:.2f}: \ {Cl['sd_shrunk']:.2f}", font_size=16,
                  color=SCHOOL),
            label(rf"teachers move: \ slope \\ {Cl['forecast_coef']:.2f} \ (s.e. {Cl['forecast_se']:.2f})",
                  font_size=16, color=SCHOOL),
            label(rf"if schools' pupils differ \\ and the estimate ignores \\ it: \ {So['forecast_coef']:.2f}",
                  font_size=16, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.2)
        Tt = tables.SCHOOLS_49.data
        foot = label(rf"Chetty, \ Friedman and Rockoff: \ a teacher one s.d. better adds {Tt['cfr_math']:.2f} s.d. "
                     rf"in maths, \ {Tt['cfr_eng']:.2f} in English, \ {Tt['cfr_earn']:.1f}\% to earnings at 28",
                     font_size=17, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Class size is one input; the teacher is another. <bookmark mark='a'/> On the Island, teachers differ in "
            "how much their pupils gain in a year. Estimate each teacher's effect from two years of classes and "
            f"the estimates are too spread out, {Cl['sd_raw']:.2f} against a true {Cl['sd_true']:.2f}, because a "
            "class of twenty-five is a noisy measure. <bookmark mark='b'/> Shrink each estimate toward the average "
            f"in proportion to its reliability, {Cl['reliability']:.2f} here, and the spread is right. <bookmark "
            "mark='c'/> But are the estimates biased by which pupils a teacher gets? Raj Chetty, John Friedman and "
            "Jonah Rockoff tested this when teachers moved between schools: if the estimates are unbiased, a "
            "school's scores should change one for one with the predicted effect of the teachers who arrive and "
            f"leave. On the Island the slope is {Cl['forecast_coef']:.2f}. <bookmark mark='d'/> If schools' pupils "
            "differ and the estimates ignore it, the test catches it: the slope falls to "
            f"{So['forecast_coef']:.2f}. <bookmark mark='e'/> In real data the test passed, and they found that a "
            f"teacher one standard deviation better raises scores by {Tt['cfr_math']:.2f} standard deviations in "
            f"maths and {Tt['cfr_eng']:.2f} in English, and earnings at twenty-eight by {Tt['cfr_earn']:.1f} "
            "percent."
        ) as vo:
            self.play(FadeIn(axL), Create(diag), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in p_raw], lag_ratio=0.004), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Transform(p_raw, p_sh), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(axR), Create(one), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in p_mv], lag_ratio=0.01), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(p_mvs), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
