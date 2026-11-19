from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

SHORT = {"Angrist and Krueger (1991)": r"Angrist, Krueger (1991)", "Staiger and Stock (1997)": r"Staiger, Stock (1997)",
         "Kane and Rouse (1993)": r"Kane, Rouse (1993)", "Card (1995)": r"Card (1995)",
         "Conneely and Uusitalo (1997)": r"Conneely, Uusitalo (1997)", "Harmon and Walker (1995)":
         r"Harmon, Walker (1995)", "Lemieux and Card (1998)": r"Lemieux, Card (1998)", "Maluccio (1997)":
         r"Maluccio (1997)", "Duflo (1999)": r"Duflo (1999)"}


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The Dials: \ what is a year of school worth?", r"What do eleven natural experiments say, "
             r"and why do they disagree with the regressions?", "Chapter eleven. The Dials: what is a year of school "
             "worth?", lit=("households",), scale=("person",), horizon=("a decade",))
        self.forest()
        self.weak()
        self.why()

    def forest(self):
        dl = load("dial")
        dial = dials.DIALS["return_schooling"]
        color = DIAL_STATUS.get(dial.status, GREY_C)
        head = VGroup(label(dial.name, font_size=28),
                      VGroup(RoundedRectangle(width=3.6, height=0.4, corner_radius=0.08, stroke_width=0,
                                              fill_color=color, fill_opacity=1),
                             label(dial.status, font_size=19, color=BACKGROUND))).arrange(RIGHT, buff=0.4)
        head[1][1].move_to(head[1][0])
        head.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
        x0, x1, lo, hi = -0.2, 6.3, 0.0, 0.28

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        top, step = 2.5, 0.41
        n = len(dl["rows"])
        axis_y = top - step * (n - 1) - 0.3
        axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), axis_y - 0.06, 0], [X(v), axis_y + 0.06, 0], color=GREY_C),
                                MathTex(f"{v:.2f}", font_size=20, color=GREY_B).move_to([X(v), axis_y - 0.28, 0]))
                         for v in (0, 0.05, 0.10, 0.15, 0.20, 0.25)])
        grid = VGroup(*[DashedLine([X(v), axis_y, 0], [X(v), top + 0.25, 0], color=GREY_D, stroke_width=1)
                        for v in (0.05, 0.10, 0.15, 0.20, 0.25)])
        unit = label(r"rise in earnings per year of school \ (0.10 = 10\%)", font_size=18, color=GREY_B).next_to(
            ticks, DOWN, buff=0.12)
        rows = VGroup()
        for k, (who, sample, b_ols, b_iv, se) in enumerate(dl["rows"]):
            y = top - step * k
            nm = label(SHORT.get(who, who), font_size=18, color=WHITE)
            smp = label(sample.split(",")[0] if who.startswith("Angrist") else sample, font_size=14, color=GREY_B)
            t = VGroup(nm, smp).arrange(RIGHT, buff=0.15).move_to([x0 - 0.35, y, 0], aligned_edge=RIGHT)
            bar = Line([X(max(b_iv - 1.96 * se, lo)), y, 0], [X(min(b_iv + 1.96 * se, hi)), y, 0], color=IVC,
                       stroke_width=4)
            ivd = Dot([X(b_iv), y, 0], radius=0.075, color=IVC)
            olsd = Square(0.13, stroke_width=0, fill_color=OLSC, fill_opacity=1).move_to([X(b_ols), y, 0])
            rows.add(VGroup(t, bar, ivd, olsd))
        key = VGroup(Square(0.15, stroke_width=0, fill_color=OLSC, fill_opacity=1),
                     label(r"least squares", font_size=19, color=OLSC),
                     Dot(radius=0.075, color=IVC), label(r"natural experiment, \ 95\% interval", font_size=19,
                                                          color=IVC)).arrange(RIGHT, buff=0.12)
        key[2].shift(RIGHT * 0.25)
        key[3].shift(RIGHT * 0.25)
        key.to_edge(UP, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Card, Econometrica 69(5) (2001), table 2", corner=DR, font_size=13)
        above, total = dl["iv_above"], dl["n"]
        with self.voiceover(
            "This part enters a second dial: the return to a year of school, the proportional rise in earnings it "
            "brings. Its estimates come from natural experiments, each set beside the plain regression on the same "
            "data, as David Card collected them in 2001. <bookmark mark='a'/> Angrist and Krueger's three cohorts, "
            "with quarter of birth, and Staiger and Stock's sharper version. <bookmark mark='b'/> Tuition and "
            "distance to college for American women; a four-year college nearby for American men; growing up in "
            "a Finnish university town. <bookmark mark='c'/> Britain's changes in the school-leaving age; a "
            "programme for Canadian veterans; distance to school in the rural Philippines; and Indonesia's great "
            "school-building programme of the 1970s, studied by Esther Duflo. <bookmark mark='d'/> Look at the "
            "squares and the dots. The regressions cluster between five and nine percent. The natural experiments "
            f"spread wider, and in {above} studies of {total} they sit above the regression on the same data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), Create(axis), FadeIn(ticks), FadeIn(grid), FadeIn(unit), FadeIn(tag))
            groups = ((0, 4), (4, 7), (7, 11))
            for mk, (i, j) in zip("abc", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), Create(r[1]), FadeIn(r[2], scale=0.6),
                                                       FadeIn(r[3], scale=0.6)) for r in rows[i:j]], lag_ratio=0.3),
                          run_time=1.8)
            vo.wait_until("d")
            self.play(*[Indicate(r[3], color=OLSC, scale_factor=1.6) for r in rows], run_time=1.2)
            self.play(*[Indicate(r[2], color=IVC, scale_factor=1.6) for r in rows], run_time=1.2)
        self.clear_scene()

    def weak(self):
        w = load("weak")
        edges, h = w["edges"], w["hist"]
        ax = axes([-0.05, 0.25], [0, max(h) * 1.15], x_length=6.4, y_length=3.8, xticks=[0, 0.05, 0.10, 0.15, 0.20],
                  yticks=None, xlabel=r"two-stage least squares estimate", font_size=19,
                  center=LEFT * 2.6 + DOWN * 0.5)
        a = ax.ax
        bars = VGroup()
        for e0, e1, v in zip(edges[:-1], edges[1:], h):
            if v == 0:
                continue
            r = Rectangle(width=a.c2p(e1, 0)[0] - a.c2p(e0, 0)[0], height=a.c2p(0, v)[1] - a.c2p(0, 0)[1],
                          stroke_width=0.8, stroke_color=BACKGROUND, fill_color=GREY_B, fill_opacity=0.85)
            r.move_to(a.c2p((e0 + e1) / 2, 0), aligned_edge=DOWN)
            bars.add(r)
        top = max(h) * 1.1

        def vline(v, col, txt, side):
            ln = DashedLine(a.c2p(v, 0), a.c2p(v, top), color=col, stroke_width=3)
            t = label(txt, font_size=19, color=col).next_to(a.c2p(v, top), UP, buff=0.08)
            t.shift(side * (t.width / 2 + 0.08))
            return VGroup(ln, t)

        truth = vline(w["truth"], E.TRUTH, rf"planted {w['truth']:.2f}", LEFT)
        ols = vline(w["ols"], OLSC, rf"least squares {w['ols']:.3f}", RIGHT)
        rows = VGroup(
            label(rf"{w['K']} instruments of pure noise, \\ drawn {w['reps']} times", font_size=24, color=GREY_A),
            label(rf"median first-stage $F$: \ {w['F_median']:.1f}", font_size=24, color=GREY_A),
            label(rf"median estimate: \ {w['median']:.3f}, \\ just where least squares was", font_size=24,
                  color=OLSC),
            label(rf"the real instrument, \ the new school: \\ {w['real']['estimate']:.3f}, \ first-stage $F$ = "
                  rf"{w['real']['F']:.0f}", font_size=24, color=IVC),
            label(r"Staiger and Stock (1997): \\ worry when $F$ is below about 10", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        head = VGroup(label(r"Bound, Jaeger and Baker (1995): \ instruments that know nothing", font_size=27,
                            color=E.MISS),
                      label(r"real quarters of birth replaced by random ones: \ estimates much like the published "
                            r"ones", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        tag = island_tag(rf"simulated: the Island's school records ({w['n']:,} islanders)".replace(",", "{,}"),
                         corner=DR, font_size=14)
        with self.voiceover(
            "Some instruments in that table are weak: they move schooling only a little. In 1995 John Bound, David "
            "Jaeger and Regina Baker showed why that matters with a startling experiment. They replaced the real "
            "quarters of birth with random ones, and got estimates much like the published ones. "
            f"<bookmark mark='a'/> Try it on the Island. Take {w['K']} instruments of pure noise, coin flips with "
            "nothing to do with schooling or pay, and run two-stage least squares. <bookmark mark='b'/> Do it "
            f"{w['reps']} times. <bookmark mark='c'/> The estimates don't scatter around zero. They pile up "
            "around the least-squares answer, bias and all. With many weak instruments, the first stage fits "
            "noise, and the noise brings the endogeneity back in. <bookmark mark='d'/> The real instrument, the "
            f"new school, gives {w['real']['estimate']:.3f}, and its first stage is strong. <bookmark mark='e'/> "
            "Douglas Staiger and James Stock's rule of thumb followed: report the first-stage F statistic, and worry "
            "when it is below about ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(truth))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ols), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def why(self):
        dial = dials.DIALS["return_schooling"]
        reasons = point_cards([
            (r"ability bias is small", r"the fear that sank the regressions \\ was overstated", OLSC),
            (r"schooling is mismeasured", r"errors in reported years \\ pull least squares down", GREY_B),
            (r"the people moved gain more", r"instruments move those who \\ would have left early: a LATE",
             E.ACCENT),
            (r"publication", r"large, significant IV estimates \\ are likelier to be printed", E.MISS),
        ], width=12.6, cols=2, font_size=21).move_to(UP * 0.7)
        meaning = wrapped_label(dial.meaning, 12.2, 21, GREY_A).to_edge(DOWN, buff=0.95)
        sc = load("schooling")
        own = label(rf"the Island's school records: \ least squares {sc['ols']:.3f}, \ the new school "
                    rf"{sc['iv']:.3f}, \ planted {sc['truth']:.2f}", font_size=21, color=E.TRUTH).next_to(
            meaning, DOWN, buff=0.2)
        tag = published_tag(r"Card (2001); Ashenfelter, Harmon and Oosterbeek, Labour Econ.\ 6 (1999)", corner=DR,
                            font_size=13).shift(UP * 0.0)
        with self.voiceover(
            "Why would the natural experiments find more than the regressions, when we feared the regressions were "
            "too high? Card weighed several explanations. Here are four. <bookmark mark='a'/> The ability bias may simply be small. "
            "<bookmark mark='b'/> Reported schooling contains errors, and errors pull least squares down, "
            "offsetting the ability bias. <bookmark mark='c'/> The people an instrument moves, those who'd have left "
            "school early without a college nearby or a stricter law, may gain more from a year than the average "
            "person: Imbens and Angrist's local effect, at work. <bookmark mark='d'/> And journals may favour large, "
            "significant estimates: Orley Ashenfelter and his coauthors found signs of exactly that. "
            "<bookmark mark='e'/> The dial's status is settled within a range. A year of school raises earnings by "
            "something like six to fifteen percent, a return few investments match. Part 38 comes back to it."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c_ in zip("abcd", reasons.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(meaning), FadeIn(own))
        self.clear_scene()
