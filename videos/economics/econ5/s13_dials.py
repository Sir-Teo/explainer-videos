from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The Dials: \ how consistent are people?", r"Across studies, how close do people come to "
             r"the economist's consumer?", "Chapter eleven. The Dials: how consistent are people?")
        self.dial()
        self.called()

    def dial(self):
        dial = dials.DIALS["consistency"]
        dl = load("dial")
        color = DIAL_STATUS.get(dial.status, GREY_C)
        head = VGroup(label(r"consistency with utility maximization", font_size=28),
                      VGroup(RoundedRectangle(width=3.6, height=0.4, corner_radius=0.08, stroke_width=0,
                                              fill_color=color, fill_opacity=1),
                             label(dial.status, font_size=19, color=BACKGROUND))).arrange(RIGHT, buff=0.4)
        head[1][1].move_to(head[1][0])
        head.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        x0, x1, lo, hi = -0.6, 6.2, 0.55, 1.0

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        top, step = 2.2, 0.62
        n = len(dial.estimates)
        axis_y = top - step * (n - 1) - 0.4
        axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), axis_y - 0.06, 0], [X(v), axis_y + 0.06, 0], color=GREY_C),
                                MathTex(f"{v:.2f}", font_size=20, color=GREY_B).move_to([X(v), axis_y - 0.28, 0]))
                         for v in (0.6, 0.7, 0.8, 0.9, 1.0)])
        unit = label(r"Afriat's efficiency index \ (1 = perfectly consistent)", font_size=18, color=GREY_B).next_to(
            ticks, DOWN, buff=0.12)
        rows = VGroup()
        for k, e in enumerate(dial.estimates):
            y = top - step * k
            c = DESIGN_COLOR.get(e.design, GREY_B)
            t = VGroup(label(rf"{e.who.split(',')[0].split(' and ')[0]} et al.\ ({e.year})" if " and " in e.who
                             else rf"{e.who} ({e.year})", font_size=19, color=WHITE),
                       label(e.sample, font_size=15, color=GREY_B)).arrange(DOWN, aligned_edge=RIGHT, buff=0.04)
            t.move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            dot = Dot([X(e.value), y, 0], radius=0.1, color=c)
            val = label(f"{e.value:.2f}" if e.year == 2001 else f"{e.value:.3f}", font_size=18,
                        color=c).next_to(dot, UP, buff=0.06)
            rows.add(VGroup(t, dot, val))
        rand = VGroup()
        for j, (name, v) in enumerate(dl["random"]):
            ln = DashedLine([X(v), axis_y, 0], [X(v), top + 0.35, 0], color=RANDOM, stroke_width=2)
            lab = label(name.replace("random choice, ", r"random: \ "), font_size=14, color=RANDOM)
            lab.next_to(ln, UP, buff=0.05).shift(RIGHT * (0.55 if j == 0 else -0.55))
            rand.add(VGroup(ln, lab))
        meaning = wrapped_label(dial.meaning, 12.4, 20, GREY_A).to_edge(DOWN, buff=0.3)
        tag = published_tag(r"Harbaugh et al.\ (2001); Choi et al.\ (2007, 2014); Chen et al.\ (2023)", corner=UR,
                            font_size=12)
        with self.voiceover(
            "This part enters a new dial: how consistent people's choices are, measured by Afriat's efficiency "
            "index. <bookmark mark='a'/> First the yardsticks: random choice scores about 0.65 on Harbaugh's eleven "
            "sets and 0.60 on fifty budgets. <bookmark mark='b'/> Children of seven score 0.93, eleven-year-olds 0.96, "
            "and students 0.94. <bookmark mark='c'/> Berkeley students with fifty budgets averaged 0.954. "
            "<bookmark mark='d'/> Dutch adults online, 0.88; and the human subjects of a 2023 study, choosing food, "
            "0.96. <bookmark mark='e'/> The status: settled within a range. People are far more consistent than "
            "chance, children included, but not perfectly, and how consistent varies from person to person in ways "
            "that go with wealth. The studies differ in their budgets, so compare a score only with random choice "
            "on the same budgets."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(unit), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rand], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
            vo.wait_until("e")
            self.play(FadeIn(meaning))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["mcfadden_bart"]
        t = tables.MCFADDEN_BART.data
        cc = call_card(r"BART's share of Bay Area work trips", c.when,
                       rf"McFadden's logit model of travellers' choices: \ {100 * t['mcfadden']:.1f}\% \ (the official "
                       rf"projection: \ about {100 * t['official']:.0f}\%)", rf"{t['year_actual']}: \ "
                       rf"{100 * t['actual']:.1f}\%", c.verdict, width=11.6, font_size=25).move_to(UP * 0.9)
        rows = VGroup(
            label(r"choices modelled as a random utility: \ each traveller's ranking has a part \\ the analyst sees "
                  r"(time, cost) and a part they don't", font_size=24),
            label(r"Daniel McFadden: \ Nobel prize, 2000, \ with James Heckman", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"McFadden, Access 20 (2002); AER 91(3) (2001)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? Revealed preference has a famous success. <bookmark mark='a'/> In the early 1970s the San "
            "Francisco Bay Area was building BART, a new rapid-transit system. The official projection said it "
            "would carry about fifteen percent of work trips. Daniel McFadden built a model from a survey of "
            "individual commuters' choices between car, bus and train, and predicted 6.3 percent. "
            "<bookmark mark='b'/> In 1975 BART carried 6.2 percent. <bookmark mark='c'/> McFadden's model treated "
            "each choice as revealing a ranking with a part the analyst can see, like travel time and cost, and a "
            "part they can't. <bookmark mark='d'/> That idea, random utility, won him the Nobel prize in 2000, and "
            "it's the frontier of this part."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
