from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Schools(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Schools", r"Do new schools raise wages, and do children in them learn?",
             "Chapter eight. Schools.", lit={2001: r"Duflo", 2016: r"Banerjee et al.", 2022: r"learning poverty"},
             scale=("nation", "classroom"), horizon=("a generation",))
        self.design()
        self.island()
        self.learning()
        self.tarl()

    def design(self):
        T = tables.SCHOOLS_46.data
        cells = VGroup()
        heads = VGroup(label(r"many new schools", font_size=20, color=SCHOOL), label(r"few new schools", font_size=20,
                                                                                    color=CONTROL))
        rowsl = VGroup(label(r"young enough \\ to attend", font_size=20, color=WHITE),
                       label(r"too old", font_size=20, color=GREY_A))
        txt = [[r"schooling \\ rises most", r"schooling \\ rises a little"], [r"no change \\ from schools",
                                                                              r"no change \\ from schools"]]
        for i in range(2):
            for j in range(2):
                box = Rectangle(width=3.0, height=1.25, stroke_color=GREY_B, stroke_width=1.8,
                                fill_color=SCHOOL if (i == 0 and j == 0) else GREY_D,
                                fill_opacity=0.25 if (i == 0 and j == 0) else 0.12)
                box.move_to(np.array([-0.6 + 3.1 * j, 0.9 - 1.35 * i, 0]))
                cells.add(VGroup(box, label(txt[i][j], font_size=18, color=WHITE).move_to(box)))
        for j, h in enumerate(heads):
            h.next_to(cells[j][0], UP, buff=0.15)
        for i, r_ in enumerate(rowsl):
            r_.next_to(cells[2 * i][0], LEFT, buff=0.25)
        diff = MathTex(r"(\text{young} - \text{old})_{\text{many}} - (\text{young} - \text{old})_{\text{few}}",
                       font_size=32, color=THEORY).to_edge(DOWN, buff=1.6)
        res = label(rf"Duflo, \ 2001: \ each school per 1,000 children: \ +{T['years_lo']}--{T['years_hi']} years of "
                    rf"school, \ +{T['wage_lo']}--{T['wage_hi']}\% wages".replace("1,000", "1{,}000"), font_size=20,
                    color=E.ACCENT).to_edge(DOWN, buff=0.7)
        head = label(rf"Indonesia, \ 1973--79: \ over {T['schools']:,} primary schools".replace(",", "{,}"),
                     font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.SCHOOLS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Between 1973 and 1979, with money from the oil boom, Indonesia's government built more than "
            f"{T['schools']:,} primary schools. Esther Duflo found an experiment in the way they were placed. "
            "<bookmark mark='a'/> More schools went to regions where fewer children had been enrolled, so some "
            "regions got many and others few. <bookmark mark='b'/> And only children young enough to attend could "
            "benefit; those already past primary school age could not. <bookmark mark='c'/> So compare young and "
            "old where many schools were built, and young and old where few were: a difference in differences, as "
            "in Part four. <bookmark mark='d'/> Each new school per thousand children raised schooling by "
            f"{T['years_lo']} to {T['years_hi']} years, and later wages by {T['wage_lo']} to {T['wage_hi']} percent. "
            "Divide one by the other and you have the return to a year of school."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(heads), FadeIn(rowsl), *[FadeIn(c[0]) for c in cells],
                      run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(heads, color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(cells[0][1]), FadeIn(cells[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(cells[2][1]), FadeIn(cells[3][1]), Write(diff))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.clear_scene()

    def island(self):
        R = load("inpres")
        I = np.array(R["intensity"])
        ds, dw = np.array(R["dschool"]), np.array(R["dwage"])
        a1 = plane([0, 5], [0, 2], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.0, y_length=4.2,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1, 1.5, 2], xlabel=r"new schools per 1,000 children",
                   ylabel=r"extra years of school, \ young - old", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=13)
        a2 = plane([0, 5], [0, 0.35], center=RIGHT * 3.0 + DOWN * 0.3, x_length=5.0, y_length=4.2,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"new schools per 1,000 children",
                   ylabel=r"extra log wage, \ young - old", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        p1 = VGroup(*[dot(a1, x, y, SCHOOL, 0.035) for x, y in zip(I, ds) if 0 <= x <= 5 and 0 <= y <= 2])
        p2 = VGroup(*[dot(a2, x, y, GAIN, 0.035) for x, y in zip(I, dw) if 0 <= x <= 5 and 0 <= y <= 0.35])
        b1, b2 = np.polyfit(I, ds, 1), np.polyfit(I, dw, 1)
        f1 = seg(a1, 0, np.polyval(b1, 0), 5, np.polyval(b1, 5), E.ACCENT, 3.0)
        f2 = seg(a2, 0, np.polyval(b2, 0), 5, np.polyval(b2, 5), E.ACCENT, 3.0)
        l1 = label(rf"slope {R['school_per_school']:.3f} years", font_size=17, color=E.ACCENT).next_to(a1, UP,
                                                                                                    buff=0.15)
        l2 = label(rf"slope {R['wage_per_school']:.4f}", font_size=17, color=E.ACCENT).next_to(a2, UP, buff=0.15)
        wald = MathTex(rf"\frac{{{R['wage_per_school']:.4f}}}{{{R['school_per_school']:.3f}}} = "
                       rf"{R['wald']:.3f}", font_size=38, color=THEORY).to_edge(DOWN, buff=0.35)
        wl = label(rf"planted: \ {R['truth']:.2f}", font_size=18, color=GREY_A).next_to(wald, RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island builds schools the same way, in {TRUTH['inpres']['regions']} regions. <bookmark mark='a'/> "
            "Each dot is a region: across, how many schools it got; up the side, how much more schooling its young "
            "cohort has than its old one. The more schools, the bigger the gap, by "
            f"{R['school_per_school']:.3f} years per school. <bookmark mark='b'/> The same for wages, measured "
            f"years later: {R['wage_per_school']:.4f} in log wages per school. <bookmark mark='c'/> The ratio is "
            "the return to a year of school, an instrumental-variables estimate of the kind in Part four, with the "
            f"schools as the instrument: {R['wald']:.3f}, against a planted {R['truth']:.2f}. Duflo's own estimates "
            "ran from about seven to eleven percent, and a recent reanalysis by David Roodman argues their "
            "uncertainty was understated. Chapter fourteen adds both to the dial."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in p1], lag_ratio=0.004), Create(f1), FadeIn(l1), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in p2], lag_ratio=0.004), Create(f2), FadeIn(l2), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(wald), FadeIn(wl))
        self.clear_scene()

    def learning(self):
        T = tables.SCHOOLS_46.data
        ring_out = Circle(radius=1.7, stroke_color=GREY_C, stroke_width=3).move_to(LEFT * 3.0 + DOWN * 0.2)
        frac = T["learning_poverty"] / 100
        arc = Arc(radius=1.7, start_angle=PI / 2, angle=-TAU * frac, stroke_color=LOSS, stroke_width=14).move_to(
            ring_out.get_center(), aligned_edge=ORIGIN)
        arc.shift(ring_out.get_center() - arc.get_arc_center())
        big = label(rf"{T['learning_poverty']}\%", font_size=54, color=LOSS).move_to(ring_out)
        side = VGroup(
            label(r"of 10-year-olds in low- and \\ middle-income countries \\ could not read a simple text, \\ 2022",
                  font_size=22, color=WHITE),
            label(rf"{T['pre_pandemic']}\% before the pandemic", font_size=22, color=GREY_A),
            label(r"schooling is not learning: \\ children sit in classes \\ pitched above their level", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 2.6 + DOWN * 0.2)
        tag = published_tag(tables.SCHOOLS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Building schools raised enrolment across the poor world. Learning is another matter. "
            "<bookmark mark='a'/> The World Bank counts a child in learning poverty if, at ten, they cannot read "
            f"and understand a simple text. In 2022 it estimated that {T['learning_poverty']} percent of "
            "ten-year-olds in low- and middle-income countries were in learning poverty, <bookmark mark='b'/> up "
            f"from {T['pre_pandemic']} percent before the pandemic closed schools. <bookmark mark='c'/> Many of "
            "these children are in school. The curriculum moves on whether or not they keep up, and the teacher "
            "teaches to the top of the class. Children who fell behind in the second year can sit through the "
            "fifth understanding little."
        ) as vo:
            self.play(FadeIn(tag), Create(ring_out), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(arc), FadeIn(big), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def tarl(self):
        T = tables.SCHOOLS_46.data
        chain = flow_chain([(r"test every \\ child quickly", SCHOOL), (r"group by level, \\ not by grade", SCHOOL),
                            (r"teach what the \\ group can learn", GAIN), (r"re-test, \\ regroup", SCHOOL)],
                           notes=[r"can they read \\ a word? \ a story?", r"for an hour or two \\ a day",
                                  r"letters, \ words, \\ paragraphs", r"every few weeks"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        ax = plane([0, 2], [0, 0.8], center=DOWN * 2.0 + RIGHT * 2.6, x_length=4.0, y_length=2.0, xticks=[],
                   yticks=[0, 0.4, 0.8], yfmt=lambda v: f"{v:.1f}", font_size=12)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"Haryana: \ an hour a day", T["tarl_haryana"], SCHOOL),
                                          (r"Uttar Pradesh: \ camps", T["tarl_up"], GAIN))):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=13, color=WHITE).next_to(r, DOWN, buff=0.08),
                            label(rf"{v:.2f}", font_size=15, color=WHITE).next_to(r, UP, buff=0.05)))
        cap = label(r"language gains, \\ standard deviations", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.4)
        tag = published_tag(tables.SCHOOLS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The Indian organization Pratham built a response, called Teaching at the Right Level. <bookmark "
            "mark='a'/> Test every child quickly: can they read a letter, a word, a short story? <bookmark "
            "mark='b'/> For an hour or two a day, group children by what they can do, not by their grade. "
            "<bookmark mark='c'/> Teach what each group is ready to learn. <bookmark mark='d'/> Test again and "
            "regroup every few weeks. <bookmark mark='e'/> Randomized evaluations with Banerjee and Duflo found "
            f"language gains of {T['tarl_haryana']} standard deviations where government teachers ran it for an "
            f"hour a day in Haryana, and {T['tarl_up']} where volunteers ran short intensive camps in Uttar "
            "Pradesh. In two other states, where teachers did not adopt the method, it achieved little: the idea "
            "works only if someone actually changes how the class is taught."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(ax), FadeIn(cap), *[GrowFromEdge(b[0], DOWN) for b in bars],
                      *[FadeIn(b[1:]) for b in bars], run_time=1.8)
        self.clear_scene()
