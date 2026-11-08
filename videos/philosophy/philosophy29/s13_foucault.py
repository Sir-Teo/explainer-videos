from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Foucault(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Power and the gaze", r"How does being watched make us who we are?", lit=(1791, 1975),
                            part=PART)
        with self.voiceover("Chapter twelve. Power and the gaze."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.discipline()
        self.panopticon()
        self.power()
        self.gaming()
        self.datafied()

    def discipline(self):
        hc = history_card(1975, r"Michel Foucault", r"\textit{Discipline and Punish}", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [
            (r"1757", r"the public execution of Damiens: \ power displayed on a body, \ as spectacle", BAD),
            (r"1838", r"eighty years later, \ a timetable for young prisoners: \ rise at six, \ prayer, \ work, \ "
                      r"school, \ by the minute", ACT),
            (r"the shift", r"from punishing the body to training the soul: \ discipline", SIGN),
            (r"its tools", r"hierarchical observation, \ normalizing judgement, \ the examination", WORLD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5)
        with self.voiceover(
            "Michel Foucault's Discipline and Punish, of 1975, opens with two documents. <bookmark mark='a'/>The "
            "first describes the public execution of Damiens, who had tried to kill the king, in 1757: power "
            "displayed on a body, as spectacle. <bookmark mark='b'/>The second, from eighty years later, is a "
            "timetable for young prisoners in Paris: rise at six, prayer, work, school, meals, each to the minute. "
            "<bookmark mark='c'/>Between them punishment moved from the body to the soul. Its aim was no longer to "
            "destroy but to train: discipline. <bookmark mark='d'/>Its tools spread from prisons to schools, "
            "barracks, hospitals and factories: hierarchical observation, normalizing judgement, and their "
            "combination, the examination, which ranks each individual against a norm."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def panopticon(self):
        head = label(r"The Panopticon \ (Bentham, \ 1791)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cen = np.array([-3.0, -0.3, 0])
        ring_o = Circle(radius=2.6, color=GREY_B).move_to(cen)
        ring_i = Circle(radius=1.9, color=GREY_B).move_to(cen)
        cells = VGroup()
        for k in range(16):
            t = 2 * math.pi * k / 16
            cells.add(Line(cen + 1.9 * np.array([math.cos(t), math.sin(t), 0]),
                           cen + 2.6 * np.array([math.cos(t), math.sin(t), 0]), color=GREY_B, stroke_width=1.5))
        people = VGroup(*[Dot(cen + 2.25 * np.array([math.cos(2 * math.pi * (k + 0.5) / 16),
                                                     math.sin(2 * math.pi * (k + 0.5) / 16), 0]), radius=0.07,
                              color=BODY) for k in range(16)])
        tower = Circle(radius=0.45, color=SIGN, fill_opacity=0.5).move_to(cen)
        rays = VGroup(*[DashedLine(cen, p.get_center(), color=SIGN, stroke_width=1.2, dash_length=0.08)
                        for p in people])
        q = quote_card(r"He who is subjected to a field of visibility, \ and who knows it, \ assumes responsibility "
                       r"for the constraints of power \dots\ he becomes the principle of his own subjection.",
                       r"Foucault", r"\textit{Discipline and Punish}", width=6.0, font_size=21).move_to([3.4, 0.6, 0])
        foot = label(r"the tower may be empty: \ visibility, \ not violence, \ does the work", font_size=20,
                     color=GOAL).move_to([3.4, -2.0, 0])
        with self.voiceover(
            "Its emblem is a prison designed by Jeremy Bentham in 1791. <bookmark mark='a'/>Cells in a ring, each "
            "lit from behind, so that every prisoner is visible. <bookmark mark='b'/>In the centre, a tower with "
            "blinds, from which a guard can see every cell, while no prisoner can see whether he is being watched. "
            "<bookmark mark='c'/>So each must behave, at every moment, as if he were. Foucault: he who is subjected "
            "to a field of visibility, and who knows it, assumes responsibility for the constraints of power; he "
            "becomes the principle of his own subjection. <bookmark mark='d'/>The tower may as well be empty. "
            "Visibility, not violence, does the work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ring_o), Create(ring_i), Create(cells), FadeIn(people))
            vo.wait_until("b")
            self.play(FadeIn(tower), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(tower.animate.set_fill(opacity=0.0), rays.animate.set_opacity(0.25), FadeIn(foot))
        self.clear_scene()

    def power(self):
        head = label(r"Power and knowledge", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"power/knowledge", r"power is not only repression; \ it produces knowledge, \ categories and the people "
                                 r"they describe", SIGN),
            (r"normalization", r"the norm sorts the normal from the abnormal, \ and people come to measure "
                               r"themselves by it", ACT),
            (r"biopower \ (1976)", r"the government of populations: \ birth rates, \ health, \ statistics", WORLD),
            (r"`man' \ (1966)", r"a recent invention, \ who may be erased `like a face drawn in sand at the edge of "
                                r"the sea'", OBJ),
        ]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "From this Foucault drew a general view of power. <bookmark mark='a'/>Power is not only a force that "
            "says no. It is productive: it produces knowledge, categories, and the very kinds of people the "
            "categories describe, the delinquent, the patient, the pupil. He wrote of power slash knowledge. "
            "<bookmark mark='b'/>Its characteristic operation is normalization: the norm sorts the normal from the "
            "abnormal, and people come to measure themselves by it. <bookmark mark='c'/>In 1976 he named biopower: "
            "the government not of individuals but of populations, through birth rates, public health and "
            "statistics. <bookmark mark='d'/>And in The Order of Things, a decade earlier, he had argued that man, as "
            "the object of the human sciences, is a recent invention, and may be erased, like a face drawn in sand "
            "at the edge of the sea."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gaming(self):
        d = load("gaming")
        head = label(r"A norm that people optimize against, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["n"] == 20000 and d["movers"] == 3049 and d["accepted_before"] == 6179
        assert d["accepted_after"] == 9228 and d["precision_after"] == 0.6696 and d["tau"] == 0.5
        bins, h0, h1 = d["bins"], d["hist_before"], d["hist_after"]
        top = max(max(h0), max(h1))
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, top * 1.05, 1000], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16},
                  x_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 0}},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 0,
                                                                                    "group_with_commas": False}}
                  ).move_to([-2.2, -0.5, 0])

        def bars(h, col, op):
            g = VGroup()
            for k, v in enumerate(h):
                if v == 0:
                    continue
                x0, x1 = bins[k], bins[k + 1]
                hgt = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
                g.add(Rectangle(width=ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0], height=hgt, stroke_width=0,
                                fill_color=col, fill_opacity=op).move_to(ax.c2p((x0 + x1) / 2, 0) + UP * hgt / 2))
            return g

        b0, b1 = bars(h0, GREY_B, 0.5), bars(h1, SIGN, 0.8)
        thr = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, top), color=BAD, stroke_width=3)
        tl = label(r"threshold", font_size=16, color=BAD).next_to(thr, UP, buff=0.08)
        xl = label(r"score", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        side = stack([(r"20\,000 people; \ honestly, \ score = quality", GREY_A),
                      (r"once the threshold is known, \ 3\,049 within reach move exactly to it", SIGN),
                      (r"accepted: \ 6\,179 $\to$ 9\,228", ACT),
                      (r"of those accepted, \ only 67\% now truly qualify", BAD),
                      (r"Goodhart \ (1975): \ a regularity collapses once it is used for control", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.6, buff=0.26).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Normalization can be computed. <bookmark mark='a'/>Twenty thousand people are sorted by a score, and "
            "those at or above a threshold are accepted: for a loan, a school, a job. At first, the score honestly "
            "measures their underlying quality. <bookmark mark='b'/>Now the threshold becomes known, and everyone "
            "within reach of it does what it takes to reach it exactly. Three thousand and forty-nine people move. "
            "The population piles up at the norm, and the region just below it empties. "
            "<bookmark mark='c'/>The number accepted rises from six thousand one hundred and seventy-nine to nine "
            "thousand two hundred and twenty-eight. <bookmark mark='d'/>And the score stops measuring what it "
            "measured: of those accepted, only sixty-seven percent now truly qualify. <bookmark mark='e'/>The "
            "economist Charles Goodhart observed in 1975 that any observed statistical regularity tends to "
            "collapse once pressure is placed upon it for control purposes; more briefly, when a measure becomes a "
            "target, it ceases to be a good measure. Machine learning now studies this as strategic classification "
            "and performative prediction."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b0], lag_ratio=0.03), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(thr), FadeIn(tl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.03), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def datafied(self):
        head = label(r"The datafied subject", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Deleuze \ (1990)", r"`societies of control': \ not enclosures but codes and passwords; \ not "
                                  r"individuals but `dividuals', \ split into data", SIGN),
            (r"Zuboff \ (2019)", r"surveillance capitalism: \ behaviour harvested to predict and shape behaviour", BAD),
            (r"ahead", r"fairness, \ privacy and gaming in algorithmic decisions: \ Part 41", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Foucault's analysis was extended to the age of data. <bookmark mark='a'/>Gilles Deleuze, in 1990, "
            "described societies of control, run not by enclosures like the prison but by codes and passwords, "
            "dealing not with individuals but with what he called dividuals, people split into data. "
            "<bookmark mark='b'/>Shoshana Zuboff, in 2019, described surveillance capitalism, in which behaviour is "
            "harvested to predict and shape behaviour. <bookmark mark='c'/>Fairness, privacy and gaming in algorithmic decisions return in Part 41."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
