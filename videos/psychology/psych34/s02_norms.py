from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


def line_card(std: float = 2.0, comps=(1.6, 2.0, 2.6), right=1) -> VGroup:
    """Asch's two cards: a standard line on the left, three comparison lines on the right, letters underneath."""
    k_ = 0.85
    base = -1.0
    left = VGroup(RoundedRectangle(corner_radius=0.06, width=1.6, height=3.2, stroke_color=GREY_B, fill_color=WHITE,
                                   fill_opacity=0.95),
                  Line([0, base, 0], [0, base + k_ * std, 0], color=BLACK, stroke_width=7))
    right_ = VGroup(RoundedRectangle(corner_radius=0.06, width=3.0, height=3.2, stroke_color=GREY_B,
                                     fill_color=WHITE, fill_opacity=0.95))
    for k, c in enumerate(comps):
        x = -0.9 + 0.9 * k
        right_.add(Line([x, base, 0], [x, base + k_ * c, 0], color=BLACK, stroke_width=7),
                   label("ABC"[k], font_size=20, color=BLACK).move_to([x, base - 0.32, 0]))
    g = VGroup(left, right_).arrange(RIGHT, buff=0.5)
    return g


class Norms(VoiceoverScene):
    def construct(self):
        self.card()
        self.sherif()
        self.asch()
        self.numbers()
        self.later()

    def card(self):
        card = chapter_card(1, r"Norms and lines", r"What do people do when the group disagrees with their eyes?",
                            lit={1935: r"Sherif", 1956: r"Asch", 1996: r"Bond \& Smith", 2023: r"Franzen \& Mader"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter one. Norms and lines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sherif(self):
        d = load("sherif")
        est, ph = np.asarray(d["est"]), np.asarray(d["phase"])
        head = heading(r"A light that seems to move")
        A = axes([0.5, 12.5], [0, 9], x_length=6.2, y_length=3.6, xticks=[2.5, 6.5, 10.5], yticks=[0, 3, 6, 9],
                 xfmt=lambda v: {2: "alone", 6: "together", 10: "alone again"}[int(v)], yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"session", ylabel=r"how far it moved \ (inches)", center=[-2.9, -0.4, 0], font_size=15)
        bands = VGroup(*[Rectangle(width=abs(A.ax.c2p(4.5, 0)[0] - A.ax.c2p(0.5, 0)[0]),
                                   height=abs(A.ax.c2p(0, 9)[1] - A.ax.c2p(0, 0)[1]), stroke_width=0,
                                   fill_color=c, fill_opacity=0.08).move_to(A.ax.c2p(2.5 + 4 * k, 4.5))
                         for k, c in enumerate((GREY_B, CROWD, GREY_B))])
        cols = (PERSON, GOOD, AUTH)
        xs = np.arange(1, 13)
        lines = VGroup(*[VGroup(curve(A.ax, xs, est[:, i], cols[i], stroke_width=3),
                                scatter(A.ax, xs, est[:, i], cols[i], radius=0.06)) for i in range(3)])
        rows = rows_of([
            (r"Sherif, \ 1935: \ in a dark room a still point of light seems to drift, \ the autokinetic effect, \ "
             r"and people were asked how far it moved", WHITE),
            (r"alone, \ each settled on a range of their own; \ together, \ their estimates converged on a group "
             r"norm", CROWD),
            (r"tested alone afterwards, \ people kept the group's norm", PERSON),
            (r"Jacobs and Campbell, \ 1961: \ an arbitrary norm planted by confederates was passed on to newcomers, "
             r"\ but decayed toward the natural one over generations", MODEL),
        ], 5.6, 19, 0.3).move_to([3.6, -0.3, 0])
        tag = simulated_tag(r"an illustration of the design, \ not Sherif's data")
        tag2 = historical_tag(r"Sherif (1935); \ Jacobs \& Campbell (1961)")
        with self.voiceover(
            "The first experiments on norms used an illusion. <bookmark mark='a'/> In 1935 Muzafer Sherif sat people "
            "in a dark room with a single, still point of light. In the dark it seems to drift, and he asked them "
            "how far it moved. <bookmark mark='b'/> Alone, each person settled on a range of their own. Put "
            "together, their estimates converged on a group norm. <bookmark mark='c'/> And tested alone afterwards, "
            "they kept the group's norm, as if it were what they'd seen. <bookmark mark='d'/> In 1961 Jacobs and "
            "Campbell planted an extreme norm with confederates and replaced members one by one. Newcomers took it "
            "up, but over the generations it decayed back toward the natural one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(bands))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[Create(l_[0]) for l_ in lines], *[FadeIn(l_[1]) for l_ in lines], FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def asch(self):
        head = heading(r"Asch's lines")
        cards = line_card().scale(0.85).move_to([-3.4, 1.0, 0])
        seats = VGroup()
        for k in range(8):
            real = k == 6
            seats.add(VGroup(Circle(radius=0.26, stroke_width=2, stroke_color=PERSON if real else CROWD,
                                    fill_color=PERSON if real else CROWD, fill_opacity=0.35),
                             label("C" if not real else r"you", font_size=14, color=WHITE)))
            seats[-1][1].move_to(seats[-1][0])
        seats.arrange(RIGHT, buff=0.18).next_to(cards, DOWN, buff=0.55)
        said = VGroup(*[label("A", font_size=20, color=AUTH).next_to(s_, DOWN, buff=0.1) for k, s_ in
                        enumerate(seats) if k != 6])
        rows = rows_of([
            (r"Asch, \ 1951 to 1956: \ a group of students around a table, \ all but one of them confederates; \ "
             r"which line matches the standard?", WHITE),
            (r"18 trials; \ on 12 critical ones the confederates, \ answering aloud before the real participant, "
             r"\ all gave the same wrong answer", CROWD),
            (r"the lines were easy: \ alone, \ almost nobody made a mistake", GOOD),
            (r"two reasons to go along: \ the others may know something, \ as in Sherif's dark room, \ or standing "
             r"out has a cost, \ as at Asch's table, \ where the answer was plain", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.2, 0])
        tag = historical_tag(r"Asch (1951, \ 1955, \ 1956)")
        with self.voiceover(
            "Sherif's light was ambiguous. Solomon Asch wanted a task with an obvious answer. <bookmark mark='a'/> "
            "Between 1951 and 1956 he seated groups of students around a table. All but one were confederates. "
            "Each trial, they were shown a standard line, and asked aloud which of three lines matched it. "
            "<bookmark mark='b'/> There were eighteen trials. On twelve critical ones the confederates, answering "
            "before the real participant, all gave the same wrong answer. <bookmark mark='c'/> The lines were easy. "
            "Alone, almost nobody made a mistake. <bookmark mark='d'/> There are two reasons to go along with a "
            "group. The others may know something you don't, as in Sherif's dark room. Or standing out may cost "
            "you something, as at Asch's table, where the answer was plain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards), FadeIn(seats))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.1) for s_ in said], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def numbers(self):
        head = heading(r"What happened")
        A = axes([-0.6, 2.6], [0, 45], x_length=5.6, y_length=3.8, xticks=None, yticks=[0, 10, 20, 30, 40],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"critical answers that went with the majority",
                 center=[-3.3, -0.3, 0], font_size=15)
        vals = [0.7, 36.8, 36.8 / 4]
        b = bars(A.ax, [0, 1, 2], vals, [GOOD, AUTH, PERSON], width=0.6)
        names = VGroup(*[label(t, font_size=15, color=c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.2) for k, (t, c) in
                         enumerate(((r"alone", GOOD), (r"unanimous majority", AUTH), (r"one ally", PERSON)))])
        tops = VGroup(label(r"almost none", font_size=15, color=GOOD).next_to(A.ax.c2p(0, vals[0]), UP, buff=0.1),
                      label(r"36.8\%", font_size=18, color=AUTH).next_to(A.ax.c2p(1, vals[1]), UP, buff=0.1),
                      label(r"about a quarter as many", font_size=15, color=PERSON)
                      .next_to(A.ax.c2p(2, vals[2]), UP, buff=0.1))
        rows = rows_of([
            (r"123 men, \ three universities: \ 36.8\% of the critical answers went with the wrong majority", AUTH),
            (r"about a quarter of the men never went along; \ about 5\% always did; \ three in four went along at "
             r"least once", CROWD),
            (r"one other person giving the right answer cut errors to about a quarter: \ unanimity, \ not size, \ "
             r"did the work", PERSON),
            (r"a single opponent hardly moved anyone; \ the effect rose to about three, \ and more added little", MODEL),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = historical_tag(r"Asch (1955, \ 1956)")
        with self.voiceover(
            "What happened? <bookmark mark='a'/> Across a hundred and twenty-three men from three universities, "
            "thirty-seven percent of the critical answers went with the wrong majority. <bookmark mark='b'/> But "
            "people differed enormously. About a quarter never went along at all; about five percent always did; "
            "and three in four went along at least once. <bookmark mark='c'/> One other person giving the right "
            "answer cut errors to about a quarter. What did the work was unanimity, not size. "
            "<bookmark mark='d'/> A single opponent hardly moved anyone. The effect rose up to about three, and "
            "more people added little. Asch himself stressed the independence: most answers, even on critical "
            "trials, were right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(b[0]), FadeIn(tops[0]), GrowFromEdge(b[1], DOWN), FadeIn(tops[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(tops[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def later(self):
        head = heading(r"Seventy years later")
        A = axes([-0.6, 2.6], [0, 45], x_length=5.6, y_length=3.8, xticks=None, yticks=[0, 10, 20, 30, 40],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"critical answers with the majority", center=[-3.3, -0.3, 0],
                 font_size=15)
        vals = [36.8, 33.0, 25.0]
        b = bars(A.ax, [0, 1, 2], vals, [AUTH, CROWD, GOOD], width=0.6)
        names = VGroup(*[label(t, font_size=15, color=c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.2) for k, (t, c) in
                         enumerate(((r"Asch, \ 1950s", AUTH), (r"2023", CROWD), (r"2023, \ paid to be right", GOOD)))])
        tops = VGroup(*[label(rf"{v:g}\%", font_size=18, color=c).next_to(A.ax.c2p(k, v), UP, buff=0.1)
                        for k, (v, c) in enumerate(zip(vals, (AUTH, CROWD, GOOD)))])
        rows = rows_of([
            (r"Bond and Smith, \ 1996: \ 133 Asch-type studies from 17 countries: \ conformity was higher in "
             r"collectivist cultures, \ and had declined in the United States since the 1950s", WHITE),
            (r"Franzen and Mader, \ 2023: \ 210 students, \ five confederates: \ 33\% of critical "
             r"answers wrong", CROWD),
            (r"paying for correct answers cut it to 25\%; \ on political statements, \ 38\% went along", GOOD),
            (r"the effect is real and durable; \ its size depends on the sample, \ the culture and the stakes", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Bond \& Smith (1996); \ Franzen \& Mader (2023)")
        with self.voiceover(
            "Has it lasted? <bookmark mark='a'/> In 1996 Bond and Smith gathered a hundred and thirty-three "
            "Asch-type studies from seventeen countries. Conformity was higher in collectivist cultures, and in the "
            "United States it had declined since the 1950s. <bookmark mark='b'/> In 2023 Franzen and Mader "
            "ran Asch's procedure again with two hundred and ten students and five confederates. Thirty-three "
            "percent of the critical answers were wrong. <bookmark mark='c'/> Paying people for correct answers cut "
            "that to twenty-five percent, and on political statements thirty-eight percent went along. "
            "<bookmark mark='d'/> So the effect is real and durable, and its size depends on the sample, the culture "
            "and the stakes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(b[0]), FadeIn(tops[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(tops[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(tops[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
