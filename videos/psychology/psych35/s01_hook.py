from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


def pegboard(n: int = 4) -> VGroup:
    board = RoundedRectangle(corner_radius=0.08, width=2.6, height=2.6, stroke_color=GREY_B, fill_color="#1B2029",
                             fill_opacity=1)
    pegs = VGroup(*[Circle(radius=0.11, color=GREY_A, fill_opacity=0.9).move_to(
        board.get_center() + [(-0.9 + 0.6 * (k % n)), (0.9 - 0.6 * (k // n)), 0]) for k in range(n * n)])
    return VGroup(board, pegs)


class Hook(VoiceoverScene):
    def construct(self):
        self.pegs()
        self.result()
        self.prophecy()
        self.question()
        self.objectives()

    def pegs(self):
        head = heading(r"An hour of turning pegs")
        board = pegboard().move_to([-4.2, 0.3, 0])
        cap = label(r"turn each peg a quarter turn; \ repeat", font_size=18, color=GREY_A).next_to(board, DOWN,
                                                                                                buff=0.2)
        rows = rows_of([
            (r"Festinger and Carlsmith, \ 1959: \ 71 male students spent an hour on dull tasks, \ turning pegs on a "
             r"board", WHITE),
            (r"then they were asked to tell the next student, \ who was waiting outside, \ that the tasks had been "
             r"interesting", CROWD),
            (r"some were paid one dollar to say it; \ others were paid twenty", PERSON),
            (r"afterwards, \ each rated how much they had actually enjoyed the tasks", MODEL),
        ], 7.2, 22, 0.4).move_to([2.6, -0.1, 0])
        tag = historical_tag(r"Festinger \& Carlsmith (1959)")
        with self.voiceover(
            "In the late 1950s, male students signed up for an experiment and spent an hour on tasks designed "
            "to be dull. <bookmark mark='a'/> They turned pegs on a board a quarter turn at a "
            "time, over and over. <bookmark mark='b'/> Then the experimenter asked a favour. The next "
            "student was waiting outside. Would they tell the newcomer the tasks had been interesting? "
            "<bookmark mark='c'/> Some were paid one dollar to say it. Others were paid twenty, a lot of money in "
            "1959. <bookmark mark='d'/> Afterwards, each one rated how much they had really enjoyed the tasks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(board), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[Rotate(p_, angle=PI / 2) for p_ in board[1]], run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def result(self):
        head = heading(r"One dollar or twenty")
        A = axes([-0.6, 1.6], [0, 1.0], x_length=4.4, y_length=3.6, xticks=None, yticks=None,
                 ylabel=r"how much they said they enjoyed it", center=[-3.9, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [0.8, 0.35], [PERSON, CROWD], width=0.6)
        names = VGroup(label(r"paid \$1", font_size=18, color=PERSON).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                       label(r"paid \$20", font_size=18, color=CROWD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        note = label(r"the direction of the result, \ drawn schematically", font_size=15, color=GREY_B)
        note.next_to(A, UP, buff=0.15)
        rows = rows_of([
            (r"the students paid one dollar rated the tasks as more enjoyable than those paid twenty", PERSON),
            (r"Leon Festinger's reading: \ ``I said it was interesting'' and ``it was boring'' clash; \ with "
             r"\$20 the money explains the lie, \ with \$1 nothing does, \ so the belief moves", WHITE),
            (r"another reading: \ people watch what they did and infer what they must think, \ as an observer would", MODEL),
            (r"this part is about how people read minds, \ other people's and their own", YOU),
        ], 6.4, 21, 0.36).move_to([3.0, -0.2, 0])
        tag = historical_tag(r"Festinger \& Carlsmith (1959)")
        with self.voiceover(
            "Common sense says the twenty-dollar students should have come away liking the task more. "
            "<bookmark mark='a'/> It was the other way round. Those paid one dollar rated the tasks as more "
            "enjoyable than those paid twenty. <bookmark mark='b'/> Leon Festinger's reading was cognitive "
            "dissonance. I said it was interesting, and it was boring, clash. With twenty dollars, the money "
            "explains the lie. With one dollar nothing does, so the belief moves to fit what was said. "
            "<bookmark mark='c'/> There's another reading: people watch what they did, and infer what they must "
            "think, just as an observer would. <bookmark mark='d'/> Either way, this part is about how people read "
            "minds, other people's and their own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(note))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def prophecy(self):
        head = heading(r"When prophecy fails")
        cal = VGroup(RoundedRectangle(corner_radius=0.1, width=2.4, height=2.6, stroke_color=AUTH, fill_color="#1B2029",
                                      fill_opacity=1),
                     label(r"December", font_size=22, color=AUTH), label(r"21", font_size=64, color=WHITE),
                     label(r"1954", font_size=22, color=GREY_A))
        cal[1:].arrange(DOWN, buff=0.15).move_to(cal[0])
        cal.move_to([-4.4, 0.3, 0])
        rows = rows_of([
            (r"Festinger, \ Riecken and Schachter, \ 1956: \ a small group in Chicago believed a flood would end "
             r"the world on 21 December 1954, \ and that its members would be rescued", WHITE),
            (r"the researchers joined the group to watch what happened when the prophecy failed", CROWD),
            (r"the most committed members became more committed, \ and the book reports that they began to seek "
             r"converts", AUTH),
            (r"later studies of failed prophecies did not find the turn to recruiting, \ and the study's methods "
             r"have been criticized", GOOD),
        ], 7.6, 21, 0.36).move_to([2.4, -0.2, 0])
        tag = historical_tag(r"Festinger, \ Riecken \& Schachter (1956)")
        with self.voiceover(
            "Festinger had already watched dissonance in the wild. <bookmark mark='a'/> In 1954 a small group in "
            "Chicago believed a flood would end the world on the twenty-first of December, and that its members "
            "would be rescued. <bookmark mark='b'/> Festinger, Henry Riecken and Stanley Schachter joined the group "
            "to watch what happened when the prophecy failed. <bookmark mark='c'/> When the day passed, the most "
            "committed members became more committed, and the book they wrote reports that they began to seek "
            "converts. <bookmark mark='d'/> Later studies of failed prophecies did not find that turn to "
            "recruiting, and the study's methods have been criticized. It's a story worth holding loosely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cal))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how do you read a mind, \ including your own?")
        rows = rows_of([
            (r"people explain behaviour with theories about hidden causes: \ traits, \ situations, \ beliefs and "
             r"wants", CROWD),
            (r"they use the same theories on themselves, \ and their reports about themselves can be wrong", PERSON),
            (r"in the middle is the area hit hardest by the replication crisis", AUTH),
            (r"and at the end, \ reading a mind is written down as inference, \ by Bayes' rule", MODEL),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how you read a mind, including your own. <bookmark mark='a'/> People explain "
            "behaviour with theories about hidden causes: traits, situations, beliefs and wants. "
            "<bookmark mark='b'/> They use the same theories on themselves, and their reports about themselves can "
            "be wrong. <bookmark mark='c'/> In the middle of the part is the area of psychology hit hardest by the "
            "replication crisis. <bookmark mark='d'/> And at the end, reading a mind is written down as inference, "
            "by Bayes' rule."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 35", font_size=34, color=GREY_B), label(r"Social Cognition", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"attribution: \ Kelley's cube as an analysis of variance, \ and the correspondence bias",
            r"dissonance against self-perception, \ and a 39-lab replication",
            r"attitudes and behaviour, \ and the self's flattering illusions, \ Dunning-Kruger included",
            r"first impressions in a tenth of a second, \ and what thin slices predict",
            r"two collapses: \ behavioural priming and power posing",
            r"mind reading as inverse planning, \ and the limits of introspection",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 35 of Psychology, Built: social cognition, the second part of Act Nine. "
            "<bookmark mark='a'/> We'll treat attribution as Kelley did, as an analysis of variance, and meet the "
            "correspondence bias. We'll set dissonance against self-perception, and read a replication run in "
            "thirty-nine laboratories. We'll weigh attitudes against behaviour, and the self's flattering "
            "illusions, the Dunning-Kruger effect included. We'll see first impressions formed in a tenth of a "
            "second, and what thin slices predict. We'll follow two collapses, behavioural priming and power "
            "posing. And we'll write mind reading as inverse planning, and test the limits of introspection."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
