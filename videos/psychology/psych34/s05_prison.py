from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


def timeline(days: int, stop: int, width: float, color, label_text: str) -> VGroup:
    """A study's planned days as boxes, the days it ran filled."""
    w = width / days
    g = VGroup()
    for k in range(days):
        ran = k < stop
        g.add(Rectangle(width=w * 0.9, height=0.4, stroke_color=color, stroke_width=1.5,
                        fill_color=color if ran else BLACK, fill_opacity=0.7 if ran else 0.2))
    g.arrange(RIGHT, buff=w * 0.1)
    cap = label(label_text, font_size=18, color=color).next_to(g, UP, buff=0.12, aligned_edge=LEFT)
    return VGroup(g, cap)


class Prison(VoiceoverScene):
    def construct(self):
        self.card()
        self.textbook()
        self.record()
        self.bbc()

    def card(self):
        card = chapter_card(4, r"The prison that wasn't", r"What did the Stanford prison experiment show?",
                            lit={1971: r"Zimbardo", 2006: r"Reicher \& Haslam", 2019: r"Le Texier"}, part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover("Chapter four. The prison that wasn't."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def textbook(self):
        head = heading(r"The textbook version")
        tl = timeline(14, 6, 9.0, AUTH, r"planned: \ two weeks; \ stopped after six days").move_to([0, 2.0, 0])
        rows = rows_of([
            (r"August 1971: \ Philip Zimbardo turned a basement corridor at Stanford into a mock prison", WHITE),
            (r"24 male students, \ screened as healthy, \ assigned by chance to be guards or prisoners", CROWD),
            (r"guards turned cruel within days; \ some prisoners left early; \ the study was stopped after six of a "
             r"planned fourteen days", AUTH),
            (r"the lesson taught for decades: \ put good people in a bad role, \ and the role takes over", YOU),
        ], 12.4, 23, 0.4).move_to([0, -0.9, 0])
        tag = historical_tag(r"the Stanford prison experiment (1971)")
        with self.voiceover(
            "If Milgram showed what an authority could make people do, the Stanford prison experiment seemed to "
            "show what a role could. <bookmark mark='a'/> In August 1971 Philip Zimbardo turned a basement corridor "
            "at Stanford into a mock prison. <bookmark mark='b'/> Twenty-four male students, screened as healthy, "
            "were assigned by chance to be guards or prisoners. <bookmark mark='c'/> The guards turned cruel within "
            "days, some prisoners left early, and the study was stopped after six of a planned fourteen days. "
            "<bookmark mark='d'/> The lesson taught for decades was simple. Put good people in a bad role, and the "
            "role takes over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tl[1]), FadeIn(tl[0]))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def record(self):
        head = heading(r"The record")
        rows = rows_of([
            (r"Thibault Le Texier, \ 2019, \ \emph{American Psychologist}: \ the study's archives and interviews with "
             r"15 of the participants", WHITE),
            (r"the guards were given precise instructions about how to treat the prisoners, \ and were not told that "
             r"they were subjects too", AUTH),
            (r"recordings he and others describe show the ``warden'', \ a member of the research team, \ pressing a "
             r"reluctant guard to be tougher", AUTH),
            (r"so it was not an experiment on what a role does by itself: \ it was a demonstration, \ staged by "
             r"people who knew the result they wanted", CROWD),
            (r"Zimbardo replied that the critics ignored the data; \ textbooks have slowly begun to change", GREY_A),
        ], 12.4, 22, 0.36).move_to([0, -0.3, 0])
        tag = published_tag(r"Le Texier (2019)")
        with self.voiceover(
            "That isn't what the record shows. <bookmark mark='a'/> In 2019 Thibault Le Texier "
            "published, in American Psychologist, a study of the experiment's archives and interviews with fifteen "
            "of the participants. <bookmark mark='b'/> The guards had been given precise instructions about how to "
            "treat the prisoners, and weren't told that they were being studied too. <bookmark mark='c'/> Recordings "
            "he and others describe show the warden, a member of the research team, pressing a reluctant guard to be tougher. "
            "<bookmark mark='d'/> So it wasn't an experiment on what a role does by itself. It was a demonstration, "
            "staged by people who knew the result they wanted. <bookmark mark='e'/> Zimbardo replied that his "
            "critics ignored the data, and textbooks have only slowly begun to change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bbc(self):
        head = heading(r"A prison study without the coaching")
        tl = timeline(8, 8, 6.0, CROWD, r"the BBC prison study: \ eight days").move_to([-3.4, 1.9, 0])
        guards = VGroup(*[Circle(radius=0.22, stroke_color=AUTH, stroke_width=2, fill_color=AUTH, fill_opacity=0.25)
                          for _ in range(5)]).arrange(RIGHT, buff=0.5).move_to([-3.4, 0.4, 0])
        prisoners = VGroup(*[Circle(radius=0.22, stroke_color=GOOD, stroke_width=2, fill_color=GOOD,
                                    fill_opacity=0.5) for _ in range(5)]).arrange(RIGHT, buff=0.08)
        prisoners.move_to([-3.4, -1.1, 0])
        gl = label(r"guards: \ no shared identity", font_size=18, color=AUTH).next_to(guards, DOWN, buff=0.15)
        pl = label(r"prisoners: \ a group", font_size=18, color=GOOD).next_to(prisoners, DOWN, buff=0.15)
        rows = rows_of([
            (r"Stephen Reicher and Alex Haslam, \ 2006: \ men randomly divided into guards and prisoners, \ filmed "
             r"for television", WHITE),
            (r"the guards did not take to their role: \ they were hesitant to use their authority, \ and never "
             r"became a group", AUTH),
            (r"the prisoners did become a group, \ and in the end overcame the guards", GOOD),
            (r"what people do in a role depends on whether they identify with it, \ the same reading as chapter "
             r"three's engaged followers", YOU),
        ], 5.8, 20, 0.34).move_to([3.5, -0.3, 0])
        tag = published_tag(r"Reicher \& Haslam (2006)")
        with self.voiceover(
            "What happens when you run a prison study without the coaching? <bookmark mark='a'/> For a BBC "
            "television series, Stephen Reicher and Alex Haslam randomly divided men into guards and prisoners, and "
            "filmed what happened. They published the study in 2006. <bookmark mark='b'/> The "
            "guards didn't take to their role. They were hesitant to use their authority, and never became a group. "
            "<bookmark mark='c'/> The prisoners did become a group, and in the end they overcame the guards. "
            "<bookmark mark='d'/> What people do in a role depends on whether they identify with it, which is the "
            "same reading as chapter three's engaged followers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(guards), FadeIn(prisoners))
            vo.wait_until("b")
            self.play(guards.animate.arrange(RIGHT, buff=0.9).move_to([-3.4, 0.4, 0]), FadeIn(gl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(prisoners.animate.arrange(RIGHT, buff=0.02).move_to([-3.4, -1.1, 0]), FadeIn(pl),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
