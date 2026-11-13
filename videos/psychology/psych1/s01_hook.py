from __future__ import annotations

from videos.psychology.psych1.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.kant()
        self.wager()
        self.three_questions()
        self.objectives()

    # ------------------------------------------------------------------
    # the three objections, drawn
    @staticmethod
    def cloud(width=2.0, color=KANT, opacity=0.85) -> VGroup:
        """A thought: a few overlapping discs."""
        spec = [(-0.32, -0.02, 0.26), (-0.08, 0.13, 0.33), (0.2, 0.06, 0.3), (0.38, -0.08, 0.2), (0.05, -0.12, 0.3),
                (-0.2, -0.13, 0.22)]
        g = VGroup(*[Circle(radius=r * width, stroke_width=0, fill_color=color, fill_opacity=opacity)
                     .move_to([x * width, y * width, 0]) for x, y, r in spec])
        return g

    def tile(self, picture: Mobject, i: int, quote: str, width=4.3) -> VGroup:
        title, _ = OBJECTIONS[i]
        num = label(rf"{i + 1}", font_size=40, color=KANT)
        t = label(title, font_size=34, color=WHITE)
        head = VGroup(num, t).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        q = wrapped_label(rf"``{quote}''", width - 0.2, 25, GREY_A)
        frame = panel(width, 2.5, color=GREY_D)
        if picture.width > width - 0.5:
            picture.scale_to_fit_width(width - 0.5)
        picture.move_to(frame)
        g = VGroup(frame, picture, head, q)
        head.next_to(frame, DOWN, buff=0.28)
        q.next_to(head, DOWN, buff=0.2)
        g.frame, g.picture, g.head, g.quote = frame, picture, head, q
        return g

    def no_mathematics(self) -> VGroup:
        c = self.cloud(1.9)
        ruler = Rectangle(width=2.6, height=0.32, stroke_color=GREY_A, stroke_width=2, fill_color="#2A2F3A",
                          fill_opacity=1)
        ticks = VGroup(*[Line(UP * (0.14 if k % 5 == 0 else 0.08), ORIGIN, color=GREY_A, stroke_width=1.5)
                         .move_to(ruler.get_top() + RIGHT * (-1.2 + 0.12 * k), aligned_edge=UP) for k in range(21)])
        r = VGroup(ruler, ticks).next_to(c, DOWN, buff=0.22)
        q = MathTex(r"?\ \text{cm}", font_size=34, color=P.ACCENT).next_to(r, RIGHT, buff=0.15)
        return VGroup(c, r, q)

    def no_experiment(self) -> VGroup:
        def atom(color):
            return Circle(radius=0.2, stroke_width=0, fill_color=color, fill_opacity=1)

        joined = VGroup(atom("#7EC8F5"), atom("#F2C14E")).arrange(RIGHT, buff=-0.06)
        apart = VGroup(atom("#7EC8F5"), atom("#F2C14E")).arrange(RIGHT, buff=0.3)
        again = joined.copy()
        arrows = [MathTex(r"\rightarrow", font_size=30, color=GREY_B) for _ in range(2)]
        chem = VGroup(joined, arrows[0], apart, arrows[1], again).arrange(RIGHT, buff=0.16)
        c = self.cloud(1.3)
        cut = DashedLine(c.get_top() + UP * 0.1, c.get_bottom() + DOWN * 0.1, color=WHITE, stroke_width=2.5)
        no = Cross(VGroup(cut), stroke_color=P.ERR, stroke_width=5, scale_factor=0.45).move_to(cut)
        mind = VGroup(c, cut, no)
        return VGroup(chem, mind).arrange(DOWN, buff=0.3)

    def observer(self) -> VGroup:
        lid = VGroup(ArcBetweenPoints(LEFT * 0.6, RIGHT * 0.6, angle=-PI / 2.2, color=WHITE, stroke_width=3),
                     ArcBetweenPoints(LEFT * 0.6, RIGHT * 0.6, angle=PI / 2.2, color=WHITE, stroke_width=3))
        iris = Circle(radius=0.2, stroke_width=0, fill_color="#7EC8F5", fill_opacity=1)
        pupil = Dot(radius=0.08, color=BLACK)
        eye = VGroup(lid, iris, pupil)
        c = self.cloud(1.5)
        gaze = DashedLine(ORIGIN, RIGHT * 0.9, color=GREY_B, stroke_width=2)
        g = VGroup(eye, gaze, c).arrange(RIGHT, buff=0.18)
        g.thought = c
        return g

    def kant(self):
        k = archive.KANT_1786.data
        head = VGroup(label(r"1786", font_size=64, color=KANT),
                      label(r"Immanuel Kant, \ K\"onigsberg", font_size=38),
                      label(r"\emph{Metaphysical Foundations of Natural Science}, \ Preface", font_size=28,
                            color=GREY_A)).arrange(DOWN, buff=0.22)
        # the ranking of the sciences, as steps going down
        steps = VGroup()
        for i, (name, mark, color) in enumerate(((r"physics", r"a science proper", WHITE),
                                                  (r"chemistry", r"``a systematic art''", GREY_A),
                                                  (r"psychology", r"further from a science still", KANT))):
            block = Rectangle(width=3.9, height=1.0, stroke_color=color, stroke_width=2, fill_color=color,
                              fill_opacity=0.1)
            nm = label(name, font_size=36, color=color).move_to(block)
            mk = label(mark, font_size=26, color=color).next_to(block, RIGHT, buff=0.3)
            st = VGroup(block, nm, mk).shift(DOWN * 1.0 * i + RIGHT * 1.3 * i)
            steps.add(st)
        steps.move_to([0, -1.6, 0])
        pic3 = self.observer()
        tiles = VGroup(self.tile(self.no_mathematics(), 0, k["mathematics"]),
                       self.tile(self.no_experiment(), 1, k["experiment"]),
                       self.tile(pic3, 2, k["observation"])).arrange(RIGHT, buff=0.42, aligned_edge=UP)
        tiles.move_to([0, 0.75, 0])
        banner = label(r"Kant, 1786: \ why there can be no science of the mind", font_size=34, color=KANT)
        banner.to_edge(UP, buff=0.3)
        tiles.next_to(banner, DOWN, buff=0.3)
        verdict = label(rf"``{k['verdict']}''", font_size=34, color=KANT)
        verdict.next_to(tiles, DOWN, buff=0.4)
        src = historical_tag(archive.KANT_1786.cite)
        with self.voiceover(
            "In 1786 Immanuel Kant, the most influential philosopher in Europe, explained why there could never be a "
            "science of the mind. <bookmark mark='a'/> He had just set out what makes physics a science, and he "
            "measured the other fields against it. Chemistry fell short. Psychology, he said, fell further. And he "
            "gave three reasons. <bookmark mark='b'/> First: mathematics can't be applied to what goes on in the "
            "mind. A thought has no length and no weight. There's nothing to put a number on. "
            "<bookmark mark='c'/> Second: you can't experiment on it. A chemist can separate a substance into its "
            "parts and put them together again. The contents of a mind can be told apart in thought, but they "
            "can't be held apart, or recombined at will. <bookmark mark='d'/> Third: even watching your own mind "
            "changes it. The observation alters and distorts the state of the thing observed. "
            "<bookmark mark='e'/> So psychology could describe the soul, the way a naturalist describes a "
            "landscape. But it could never be a science of the soul."
        ) as vo:
            head.move_to(ORIGIN)
            self.play(FadeIn(head, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(head.animate.scale(0.7).to_edge(UP, buff=0.45))
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.15 + RIGHT * 0.15) for s in steps], lag_ratio=0.6),
                      run_time=5.0)
            vo.wait_until("b")
            self.play(FadeOut(head), FadeOut(steps), FadeIn(banner))
            self.play(FadeIn(tiles[0], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(tiles[1], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(tiles[2], shift=UP * 0.2))
            self.play(pic3.thought.animate.stretch(1.25, 0).stretch(0.8, 1), rate_func=there_and_back,
                      run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(verdict, shift=UP * 0.15))
        self.clear_scene()

    def wager(self):
        board = wager_board().scale(1.15).move_to(UP * 0.3)
        strip = timeline(lit=(1786, 1850)).to_edge(DOWN, buff=0.8)
        bed = history_card(r"22 October 1850", r"Gustav Fechner, Leipzig",
                           r"measure the smallest change a person can notice, and count sensation in those steps",
                           color=P.ACCENT, width=6.3, font_size=26)
        frog = history_card(r"January 1850", r"Hermann Helmholtz, K\"onigsberg",
                            r"times a signal travelling down a frog's nerve", color=NERVE, width=6.3, font_size=26)
        cards = VGroup(bed, frog).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to([0, -0.95, 0])
        with self.voiceover(
            "These weren't foolish objections. Kant was describing the psychology of his day accurately, and each "
            "objection names a real difficulty. <bookmark mark='a'/> So think of it as a wager. If Kant is right, "
            "nobody will ever write an equation about the mind that predicts a measurement. Nobody will run an "
            "experiment on a thought. And every attempt to observe a mind will be defeated by the observing. "
            "<bookmark mark='b'/> This series is the story of how that wager was taken up: a hundred and "
            "seventy-five years of it so far. <bookmark mark='c'/> It starts on a particular morning. The "
            "twenty-second of October, 1850, in Leipzig. A physicist named Gustav Fechner is lying in bed, and "
            "it occurs to him that you might not need to measure a sensation directly. You could measure the "
            "smallest change in the world that a person can notice, and count sensation in those steps. "
            "<bookmark mark='d'/> In the same year, in Königsberg, the city where Kant had lived and died, "
            "Hermann Helmholtz was timing a signal on its way down a frog's nerve. Two measurements of the mind's "
            "machinery in a single year, sixty-four years after Kant said there could be none."
        ) as vo:
            self.play(FadeIn(board.head), LaggedStart(*[FadeIn(r.objection, shift=RIGHT * 0.15) for r in board.rows],
                                                     lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r.reply) for r in board.rows], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(strip))
            vo.wait_until("c")
            self.play(board.animate.scale(1 / 1.15).to_edge(UP, buff=0.4))
            self.play(FadeIn(bed, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(frog, shift=UP * 0.2))
        self.clear_scene()

    def three_questions(self):
        rows = VGroup()
        for n, q, a, c in (
            (r"1", r"What happens?", r"the phenomenon, measured, and measured first on you", P.HUMAN),
            (r"2", r"What would produce it?", r"a mechanism, written as mathematics and built as running code",
             P.PSYCHE),
            (r"3", r"How do we know?", r"what was claimed, how big it was, and what happened when it was run again",
             P.ACCENT),
        ):
            num = label(n, font_size=66, color=c)
            body = VGroup(label(q, font_size=48, color=c), label(a, font_size=30, color=GREY_A))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        head = heading(r"Three questions, for every topic")
        rows.next_to(head, DOWN, buff=0.75)
        with self.voiceover(
            "The series puts three questions to every topic. <bookmark mark='a'/> One: what happens? The "
            "phenomenon, measured, and measured first on you. <bookmark mark='b'/> Two: what would produce it? A "
            "mechanism, written as mathematics and built as a program that runs. <bookmark mark='c'/> And three: "
            "how do we know? Kant's third objection never went away, because the investigator is a mind too, and "
            "the easiest person to fool. So every finding in this series goes into a ledger, with what happened "
            "when somebody ran it again."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 1", font_size=34, color=GREY_B), label(r"Kant's Wager", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"your own reaction time, \ and the question of where the time goes",
            r"Helmholtz measures the speed of a nerve; \ Donders subtracts one task from another to time a thought",
            r"what subtraction assumes, \ and how distributions can test it; \ additive factors",
            r"the first laboratories, \ the ban on the mind, \ the revolution that brought it back",
            r"Marr's three levels of explanation, \ and the homunculus this series is built to remove",
            r"the four devices of the series: \ Psyche, \ the Pool, \ the Battery, \ the Ledger",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part one: Kant's wager. <bookmark mark='a'/> In this part we time your reactions, and ask where the "
            "time goes. <bookmark mark='b'/> We follow Helmholtz as he measures the speed of a nerve, and Donders "
            "as he subtracts one task from another to time a thought. <bookmark mark='c'/> We find out what his "
            "subtraction assumed, and how to test it. <bookmark mark='d'/> Then the history in three steps: the "
            "first laboratories, the behaviourists who banned the mind, and the revolution that brought it back. "
            "<bookmark mark='e'/> We meet David Marr's three levels of explanation, and the homunculus, the bad "
            "explanation this series is built to get rid of. <bookmark mark='f'/> And we set up the four devices "
            "that run through all sixty-two parts."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
