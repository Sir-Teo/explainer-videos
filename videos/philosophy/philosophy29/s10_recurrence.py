from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Recurrence(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"The individual and the eternal return", r"Could you will your life again?",
                            lit=(1843, 1882), part=PART)
        with self.voiceover("Chapter nine. The individual and the eternal return."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kierkegaard()
        self.nietzsche()
        self.demon()
        self.ca()
        self.simmel()

    def kierkegaard(self):
        hc = history_card(1843, r"S{\o}ren Kierkegaard", r"\textit{Either/Or}; \ \textit{Fear and Trembling}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.3)
        stages = VGroup()
        for i, (n, d, c) in enumerate([(r"aesthetic", r"living for the interesting moment", OBJ),
                                       (r"ethical", r"choosing oneself, \ under universal duties", ACT),
                                       (r"religious", r"the individual before God, \ beyond the universal", BODY)]):
            b = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=c, fill_opacity=0.12)
            t = VGroup(label(n, font_size=22, color=c), wrapped_label(d, 3.0, 16, GREY_A)).arrange(DOWN, buff=0.1)
            stages.add(VGroup(b, t.move_to(b)).move_to([-4.0 + 4.0 * i, 0.6, 0]))
        leaps = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.08, color=GREY_B)
                         for i in range(2)])
        lt = VGroup(*[label(r"a leap", font_size=16, color=GREY_A).next_to(a, UP, buff=0.05) for a in leaps])
        rows = stack([(r"Abraham: \ a teleological suspension of the ethical", BODY),
                      (r"`anxiety is the dizziness of freedom' \ (1844)", BAD),
                      (r"`subjectivity is truth': \ what matters is how one exists, \ not what one can prove", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The existentialists had two nineteenth-century ancestors. The first is Søren Kierkegaard, writing in "
            "Copenhagen under a series of pseudonyms. <bookmark mark='a'/>In Either/Or, of 1843, and later books, "
            "he describes stages of existence: the aesthetic, living for the interesting moment; "
            "<bookmark mark='b'/>the ethical, choosing oneself under universal duties; <bookmark mark='c'/>and the "
            "religious, the single individual before God. No argument carries you from one to the next; each "
            "transition is a leap. <bookmark mark='d'/>In Fear and Trembling, Abraham, ready to sacrifice Isaac at "
            "God's command, stands outside the ethical altogether: a teleological suspension of the ethical. "
            "<bookmark mark='e'/>Anxiety, he wrote in 1844, is the dizziness of freedom. <bookmark mark='f'/>And "
            "truth is subjectivity: what matters most is not what one can prove, but how one exists."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, s in zip("abc", stages):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(GrowArrow(leaps[0]), GrowArrow(leaps[1]), FadeIn(lt))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def nietzsche(self):
        hc = history_card(1882, r"Friedrich Nietzsche", r"\textit{The Gay Science}", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [
            (r"\S 125", r"`God is dead, \ and we have killed him': \ the collapse of the ground of European values",
             BAD),
            (r"genealogy \ (1887)", r"master morality, \ `good' and `bad'; \ slave morality, \ born of resentment, \ "
                                    r"`good' and `evil'", SIGN),
            (r"perspectivism", r"there are no facts free of every perspective, \ only interpretations", ACT),
            (r"the task", r"to create values, \ not to find them: \ the \textit{\"Ubermensch} of "
                          r"\textit{Zarathustra} \ (1883--85)", GOAL),
        ]
        g = rows_table(rows, top=1.0, gap=0.48)
        with self.voiceover(
            "The second ancestor is Friedrich Nietzsche. <bookmark mark='a'/>In The Gay Science, of 1882, a madman "
            "runs into the market place with a lantern in daylight, crying that God is dead, and we have killed him. "
            "It is not an argument against God's existence, but a diagnosis: the belief that grounded European "
            "values has collapsed, and most people have not noticed. <bookmark mark='b'/>In the Genealogy of "
            "Morality, of 1887, he traced our values to their origins: a master morality of good and bad, and a "
            "slave morality, born of resentment, of good and evil. <bookmark mark='c'/>He held that there are no "
            "facts free of every perspective, only interpretations. <bookmark mark='d'/>And so values must be "
            "created, not found: the task he gave to the figure of the Übermensch in Thus Spoke Zarathustra."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def demon(self):
        q = quote_card(r"What, \ if some day or night a demon were to steal after you into your loneliest loneliness "
                       r"and say to you: \ `This life as you now live it and have lived it, \ you will have to live "
                       r"once more and innumerable times more' \dots", r"Friedrich Nietzsche",
                       r"\textit{The Gay Science}, \ \S 341: \ `The greatest weight'", width=10.8,
                       font_size=24).move_to([0, 1.0, 0])
        rows = stack([(r"a test: \ would you throw yourself down and curse the demon, \ or answer \ `never have I heard "
                       r"anything more divine'?", BODY),
                      (r"a hypothesis? \ in unpublished notes \ (1881) \ Nietzsche tried to prove it: \ finite force, \ "
                       r"infinite time", TIME)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "The Gay Science also contains Nietzsche's most famous thought experiment. "
            "<bookmark mark='a'/>What, if some day or night a demon were to steal after you into your loneliest "
            "loneliness and say to you: this life as you now live it and have lived it, you will have to live once "
            "more and innumerable times more, every pain and every joy, in the same succession and sequence. "
            "<bookmark mark='b'/>Would you curse the demon? Or would you answer: never have I heard anything more "
            "divine? Whether you could will your life again, exactly as it is, is the test of how you are living it. "
            "<bookmark mark='c'/>But Nietzsche also wondered whether it was true. In unpublished notes he sketched a "
            "proof: if the world has a finite amount of force and infinite time, its states must recur. The Reasoner "
            "can test both halves of that."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def ca(self):
        d = load("recurrence")
        head = label(r"A finite, \ reversible world returns", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        per = {int(k): v for k, v in d["periods"].items()}
        assert d["show_n"] == 11 and d["show_period"] == 93 and per[11] == 93 and per[15] == 510 and per[19] == 513
        assert all(v is not None for v in per.values()) and d["rule"] == 150
        rows = d["rows"]
        T = d["show_period"]
        cs = 0.118
        x0, y0 = -5.6, 1.9
        cells = VGroup()
        for t, row in enumerate(rows[:T + 1]):
            for i, v in enumerate(row):
                if v:
                    cells.add(Square(side_length=cs, stroke_width=0, fill_color=TIME, fill_opacity=0.9).move_to(
                        [x0 + t * cs, y0 - i * cs, 0]))
        border = Rectangle(width=(T + 1) * cs, height=11 * cs, color=GREY_D, stroke_width=1).move_to(
            [x0 + T * cs / 2, y0 - 5 * cs, 0])
        start = Rectangle(width=cs * 1.6, height=11 * cs + 0.12, color=OK, stroke_width=2).move_to(
            [x0, y0 - 5 * cs, 0])
        end = start.copy().move_to([x0 + T * cs, y0 - 5 * cs, 0])
        tl = label(r"time $\rightarrow$ \ \ (11 cells, \ one column per step)", font_size=17, color=GREY_A).next_to(
            border, DOWN, buff=0.12).align_to(border, LEFT)
        sl = label(r"start", font_size=16, color=OK).next_to(start, UP, buff=0.08)
        el = label(r"step 93: \ the start again", font_size=16, color=OK).next_to(end, UP, buff=0.08)
        eq = MathTex(r"x_{t+1} \;=\; f(x_t) \,\oplus\, x_{t-1}", font_size=30, color=TIME).move_to([-3.6, -0.6, 0])
        eql = label(r"run it backwards: \ $x_{t-1} = f(x_t) \oplus x_{t+1}$", font_size=18, color=GREY_A).next_to(
            eq, DOWN, buff=0.15)
        hd = [r"n", r"5", r"7", r"9", r"11", r"13", r"15", r"17", r"19"]
        cells_t = [[label(r"return time", font_size=17, color=GREY_A)] +
                   [MathTex(str(per[n]), font_size=19, color=TIME) for n in (5, 7, 9, 11, 13, 15, 17, 19)]]
        grid = ValueGrid(hd, cells_t, col_w=[1.8] + [0.75] * 8, cell_h=0.45, font_size=18).move_to([2.6, -0.7, 0])
        foot = label(r"a reversible law on finitely many states: \ every state returns \ (Poincar\'e, \ 1890)",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "First, a world that is finite and deterministic, and whose law can be run backwards. "
            "<bookmark mark='a'/>Take a ring of eleven cells, each on or off, and a rule due to Edward Fredkin: a "
            "cell's next state is a fixed function of its neighbourhood now, combined, by exclusive or, with its "
            "state one step ago. Any such rule can be run backwards. <bookmark mark='b'/>Start from a single live "
            "cell and let it run. The pattern grows, breaks up, recombines, and at step ninety-three it is exactly "
            "where it began, and so it will be again every ninety-three steps, forever. "
            "<bookmark mark='c'/>On other rings the return takes from nine steps to more than five hundred, but it "
            "always comes. <bookmark mark='d'/>The reason is simple. There are finitely many states, and a "
            "reversible law never sends two states to the same successor, so the history can never fall into a cycle "
            "that excludes its start. Henri Poincaré proved the continuous version in 1890 for bounded mechanical "
            "systems, which return arbitrarily close to where they began."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(eql), Create(border))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), FadeIn(tl), run_time=4)
            self.play(Create(start), Create(end), FadeIn(sl), FadeIn(el))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def simmel(self):
        d = load("recurrence")
        head = label(r"Simmel's wheels", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sim = {r["T"]: r for r in d["simmel"]}
        assert sim[10]["closest"] == 0.0450703 and sim[100]["closest"] == 0.0028175
        assert sim[1000]["closest"] == 9.6e-06 and sim[1000]["at"] == 355 and sim[100000]["at"] == 355
        wheels = VGroup()
        for i, (rate, tex) in enumerate([(1, r"1"), (2, r"2"), (1 / math.pi, r"1/\pi")]):
            c = Circle(radius=0.62, color=[ACT, WORLD, BODY][i], stroke_width=3).move_to([-5.4 + 1.6 * i, 1.2, 0])
            m = Line(c.get_center(), c.get_center() + UP * 0.62, color=[ACT, WORLD, BODY][i], stroke_width=4)
            t = MathTex(rf"\text{{rate}}\ {tex}", font_size=22, color=[ACT, WORLD, BODY][i]).next_to(c, DOWN,
                                                                                                 buff=0.15)
            wheels.add(VGroup(c, m, t))
        hd = [r"\text{up to time}", r"\text{closest return of the third wheel}", r"\text{at }t"]
        cells = [[MathTex(f"{T:,}".replace(",", r"\,"), font_size=21),
                  MathTex(f"{sim[T]['closest']:.7f}".rstrip("0"), font_size=21, color=BODY),
                  MathTex(str(sim[T]["at"]), font_size=21)] for T in (10, 100, 1000, 10000, 100000)]
        grid = ValueGrid(hd, cells, col_w=[2.0, 4.2, 1.2], cell_h=0.44, font_size=19).move_to([3.0, 0.2, 0])
        note = label(r"355/113 is the famous approximation of $\pi$; \ the next better one waits until 103\,993", font_size=18,
                     color=GREY_A).next_to(grid, DOWN, buff=0.2)
        foot = stack([(r"never exactly: \ $1/\pi$ is irrational", BAD),
                      (r"so the proof needs a finite, \ discrete world; \ as a test of a life, \ it needs no physics",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=5.2, buff=0.2).move_to([-3.6, -1.6, 0])
        with self.voiceover(
            "Now the objection. <bookmark mark='a'/>In 1907 the sociologist Georg Simmel imagined three wheels on one "
            "axle, marked at the top, turning at rates one, two, and one over pi. <bookmark mark='b'/>The first two "
            "are back at the top together at every whole number of turns. The third never is, because one over pi "
            "is irrational. <bookmark mark='c'/>It comes close. By time ten its closest return is four and a half "
            "hundredths of a turn; by a hundred, under three thousandths; at time three hundred and fifty-five, "
            "less than one hundred thousandth, because three hundred and fifty-five over a hundred and thirteen is "
            "the famous approximation of pi. And then nothing better until a hundred and three thousand nine "
            "hundred and ninety-three. Close, but never exact. <bookmark mark='d'/>So the cosmological proof needs a "
            "world with finitely many discrete states. As a test of how you live, the demon needs no physics at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w) for w in wheels], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[Rotate(w[1], angle=-2 * math.pi * r * 2, about_point=w[0].get_center())
                        for w, r in zip(wheels, (1, 2, 1 / math.pi))], run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(note))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
