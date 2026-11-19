from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

ABILITY_LO, ABILITY_HI = "#5DADEC", "#F2B84B"


def ability_color(a: float):
    t = float(np.clip((a + 2) / 4, 0, 1))
    return interpolate_color(ManimColor(ABILITY_LO), ManimColor(ABILITY_HI), t)


class Selection(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Omitted variables and selection", r"Does school raise pay, or do able people do both?",
             "Chapter five. Omitted variables and selection.", lit=("households",), scale=("person",),
             horizon=("a decade",))
        self.records()
        self.formula()
        self.school()
        self.choosers()

    def _axes(self):
        from explainer.ai.viz import axes

        return axes([4, 18], [1.4, 3.4], x_length=6.4, y_length=4.6, xticks=[6, 9, 12, 15, 18],
                    yticks=[1.5, 2.0, 2.5, 3.0], xlabel=r"years of schooling", ylabel=r"log of yearly earnings",
                    font_size=20, center=LEFT * 2.4 + DOWN * 0.2)

    def records(self):
        sc = load("schooling")
        ax = self._axes()
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(x, y), radius=0.04, color=GREY_A, fill_opacity=0.7)
                        for x, y in zip(sc["school"], sc["logw"]) if 4 < x < 18 and 1.4 < y < 3.4])
        xs = np.array([5.0, 17.0])
        ym = float(np.mean(sc["logw"]))
        xm = float(np.mean(sc["school"]))
        ols = Line(a.c2p(xs[0], ym + sc["ols"] * (xs[0] - xm)), a.c2p(xs[1], ym + sc["ols"] * (xs[1] - xm)),
                   color=OLSC, stroke_width=4)
        rows = VGroup(
            label(rf"the Island's school records: \ {sc['n']:,} islanders".replace(",", "{,}"), font_size=25),
            label(rf"least squares: \ each year of school, \\ ${100 * sc['ols']:.1f}\%$ higher earnings", font_size=25,
                  color=OLSC),
            label(r"but who stays in school longer?", font_size=26, color=E.ACCENT),
            label(r"the able: \ ability raises schooling \\ \emph{and} pay", font_size=25, color=ABILITY_HI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        key = VGroup(Dot(radius=0.07, color=ABILITY_LO), label(r"less able", font_size=20, color=ABILITY_LO),
                     Dot(radius=0.07, color=ABILITY_HI), label(r"more able", font_size=20, color=ABILITY_HI)).arrange(
            RIGHT, buff=0.15).next_to(ax, UP, buff=0.1).shift(RIGHT * 1.5)
        tag = island_tag(r"simulated: the Island's school records (300 of 1,200 shown); ability is planted",
                         corner=DR, font_size=15)
        with self.voiceover(
            "The same problem has a second form, and it's everywhere. <bookmark mark='a'/> Here are the Island's "
            "school records: every islander's years of schooling and earnings. <bookmark mark='b'/> The best line "
            f"says each extra year of school goes with about {100 * sc['ols']:.0f} percent higher earnings. Is that "
            "what a year of school does? <bookmark mark='c'/> Ask who stays in school longer. <bookmark mark='d'/> "
            "On the Island, as everywhere, it's partly the able: the ones who find school easier, and who would "
            "earn more whatever their schooling. Colour each islander by ability, which we planted and the "
            "statistician can't see, and the able sit high and to the right. Part of the line is ability, not "
            "school."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.005), FadeIn(rows[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ols), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            colored = [d.animate.set_color(ability_color(a_)) for d, a_ in
                       zip(dots, [a_ for x, y, a_ in zip(sc["school"], sc["logw"], sc["ability"]) if 4 < x < 18
                                  and 1.4 < y < 3.4])]
            self.play(*colored, FadeIn(key), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def formula(self):
        sc = load("schooling")
        eqs = VGroup(
            MathTex(r"\log w = \alpha + \rho\,S + \gamma\,A + e", font_size=44),
            MathTex(r"\operatorname{plim}\ \hat\rho_{\text{least squares}} = \rho + \gamma\,"
                    r"\frac{\operatorname{cov}(S, A)}{\operatorname{var}(S)}", font_size=44),
            MathTex(rf"= {sc['truth']:.3f} + {sc['gamma']:.2f}\times\frac{{{sc['cov_sa']:.2f}}}{{{sc['var_s']:.2f}}}"
                    rf" = {sc['truth'] + sc['bias_formula']:.3f}", font_size=40, color=OLSC),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        rows = VGroup(
            label(rf"this sample's least squares: \ {sc['ols']:.3f}", font_size=25, color=OLSC),
            label(rf"with ability held fixed (if only we could): \ {sc['with_ability']:.3f}", font_size=25,
                  color=GREY_A),
            label(rf"the planted return: \ {sc['truth']:.3f}", font_size=25, color=E.TRUTH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "The size of the mistake has a formula, the omitted-variable bias. <bookmark mark='a'/> Suppose earnings "
            "depend on schooling and on ability. <bookmark mark='b'/> Leave ability out, and the schooling "
            "coefficient picks up ability's effect, times how strongly ability and schooling move together. "
            "<bookmark mark='c'/> With the Island's numbers, the line should overstate the return by almost three "
            f"points. <bookmark mark='d'/> This sample's line says {sc['ols']:.3f}; the planted return is "
            f"{sc['truth']:.2f}. If we could measure ability and hold it fixed, the bias would go. But ability "
            "is exactly what we can't measure."
        ) as vo:
            self.play(Write(eqs[0]))
            vo.wait_until("a")
            self.play(Indicate(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        self.clear_scene()

    def school(self):
        sc = load("schooling")
        w = sc["wald"]
        m = w["means"]
        k = 2.4
        rows = VGroup()
        for i, (nm, xs, ys, col) in enumerate(((r"grew up near the new school", m["x1"], m["y1"], IVC),
                                               (r"grew up across the Island", m["x0"], m["y0"], GREY_B))):
            t = label(nm, font_size=25, color=col)
            sch = label(rf"{xs:.2f} years of school", font_size=25)
            lw = label(rf"log earnings {ys:.3f}", font_size=25)
            rows.add(VGroup(t, sch, lw).arrange(RIGHT, buff=0.7))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 1.4)
        eq = MathTex(r"\hat\rho_{\text{IV}} = \frac{\Delta \log w}{\Delta S} = "
                     rf"\frac{{{w['dy']:.3f}}}{{{w['dx']:.2f}}} = {w['estimate']:.3f}", font_size=44, color=IVC)
        eq.move_to(DOWN * 0.6)
        res = label(rf"two-stage least squares: \ {sc['iv']:.3f} \ (s.e.\ {sc['iv_se']:.3f}); \ planted "
                    rf"{sc['truth']:.2f}", font_size=25, color=E.TRUTH).next_to(eq, DOWN, buff=0.5)
        why = label(r"the school changed where you could study, \ not how able you were", font_size=25,
                    color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = island_tag(r"simulated: the Island; the school was built on the east side in year 20", corner=DR,
                         font_size=15)
        with self.voiceover(
            "An instrument can rescue us here too. <bookmark mark='a'/> Twenty years ago the Island built a second "
            "school, on its east side. Islanders who grew up near it stayed in school about two years longer than "
            f"those across the Island, {w['dx']:.1f} years on average. <bookmark mark='b'/> And their earnings are "
            f"higher, by {w['dy']:.3f} in logs. <bookmark mark='c'/> Divide one by the other: "
            f"{w['estimate']:.3f}, almost exactly the planted eight percent. <bookmark mark='d'/> It works because "
            "where the school was built changed how much schooling islanders could get, and nothing about how "
            "able they were. That, again, is an argument, not a fact in the data. Real studies have used distance "
            "to a college, changes in the school-leaving age and new school buildings in exactly this way."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0][0]), FadeIn(rows[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1]), FadeIn(rows[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0][2]), FadeIn(rows[1][2]))
            vo.wait_until("c")
            self.play(Write(eq))
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def choosers(self):
        from explainer.ai.viz import axes

        rows = VGroup(
            label(r"who signs up for a training programme?", font_size=30, color=E.ACCENT),
            label(r"people whose earnings have just fallen \\ (Ashenfelter's dip, 1978)", font_size=25),
            label(r"people who expect to gain the most", font_size=25),
            label(r"people with less going for them \\ in the first place", font_size=25),
            label(r"compare trainees with everyone else, \\ and you compare different people", font_size=26,
                  color=NONEXP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.6).shift(UP * 0.2)
        # a schematic of the dip: the shape Ashenfelter found, not his numbers
        ax = axes([-5, 3], [0, 10], x_length=5.0, y_length=3.4, xticks=[-4, -2, 0, 2], yticks=[],
                  xlabel=r"years from enrolling", ylabel=r"earnings", font_size=18, center=RIGHT * 3.7 + DOWN * 0.1)
        a = ax.ax
        yrs = np.linspace(-5, 3, 81)
        others = 6.2 + 0.25 * (yrs + 5)
        dip = np.where(yrs < -1.5, 0.0, np.where(yrs < 0, -2.2 * (yrs + 1.5) / 1.5, -2.2 + 1.9 * np.minimum(yrs, 1.2) / 1.2))
        trainees = 3.6 + 0.2 * (yrs + 5) + dip
        oth = VMobject(stroke_color=GREY_B, stroke_width=4).set_points_smoothly([a.c2p(x, y) for x, y in zip(yrs, others)])
        tra = VMobject(stroke_color=NONEXP, stroke_width=4).set_points_smoothly(
            [a.c2p(x, y) for x, y in zip(yrs, trainees)])
        enrol = DashedLine(a.c2p(0, 0), a.c2p(0, 10), color=GREY_C, stroke_width=2)
        keys = VGroup(label(r"everyone else", font_size=19, color=GREY_B).next_to(a.c2p(3, others[-1]), UP, buff=0.1)
                      .shift(LEFT * 0.6),
                      label(r"trainees", font_size=19, color=NONEXP).next_to(a.c2p(3, trainees[-1]), DOWN, buff=0.12)
                      .shift(LEFT * 0.4),
                      label(r"enrol", font_size=18, color=GREY_C).next_to(a.c2p(0, 10), UP, buff=0.05),
                      label(r"the dip", font_size=19, color=NONEXP).next_to(a.c2p(0, 2.4), DOWN + LEFT, buff=0.15))
        sch = note(r"schematic, after Ashenfelter (1978)", font_size=15, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        with self.voiceover(
            "The deepest form of the problem is choice. <bookmark mark='a'/> Think of a training programme for the "
            "unemployed. Who signs up? <bookmark mark='b'/> People whose earnings have just dropped: Orley "
            "Ashenfelter noticed in 1978 that trainees' earnings dip in the year before they enrol, and recover "
            "afterwards whether or not the training helped. <bookmark mark='c'/> People who expect to gain the "
            "most. <bookmark mark='d'/> And people with less going for them to begin with. <bookmark mark='e'/> "
            "Compare trainees with everyone else, and you're comparing different people. Economists in the 1970s "
            "had a toolkit of regressions and corrections for exactly this. The next chapter is the test of that "
            "toolkit."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(sch), Create(oth), FadeIn(keys[0]), FadeIn(enrol), FadeIn(keys[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), Create(tra, run_time=2.5), FadeIn(keys[1]))
            self.play(FadeIn(keys[3]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
