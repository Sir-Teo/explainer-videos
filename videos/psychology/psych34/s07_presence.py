from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Presence(VoiceoverScene):
    def construct(self):
        self.card()
        self.triplett()
        self.drive()
        self.roaches()
        self.loafing()

    def card(self):
        card = chapter_card(6, r"The presence of others", r"Does an audience help or hurt?",
                            lit={1898: r"Triplett", 1965: r"Zajonc", 1979: r"Latan\'e et al.", 2020: r"Halfmann et al."},
                            part=PART, scale=("person", "group"), marr=("what", "how"))
        with self.voiceover("Chapter six. The presence of others."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def triplett(self):
        head = heading(r"The first experiment in social psychology?")
        reels = VGroup()
        for k in range(2):
            wheel = VGroup(Circle(radius=0.55, stroke_color=CROWD if k else PERSON, stroke_width=3),
                           Line(ORIGIN, RIGHT * 0.55, color=CROWD if k else PERSON, stroke_width=3))
            reels.add(VGroup(wheel, label(r"alone" if k == 0 else r"side by side", font_size=18,
                                          color=PERSON if k == 0 else CROWD).next_to(wheel, DOWN, buff=0.2)))
        reels.arrange(RIGHT, buff=1.6).move_to([-3.6, 0.8, 0])
        rows = rows_of([
            (r"Triplett, \ 1898: \ children turned fishing reels as fast as they could, \ alone and in "
             r"competition with another child", WHITE),
            (r"he reported that many children were faster with a competitor beside them", PERSON),
            (r"Stroebe, \ 2012: \ reanalyses of Triplett's own figures show little effect: \ about half the children "
             r"were no faster", AUTH),
            (r"the field's founding experiment was weaker than its legend, \ a pattern this part keeps finding", YOU),
        ], 6.2, 20, 0.36).move_to([3.3, -0.3, 0])
        tag = historical_tag(r"Triplett (1898); \ Stroebe (2012)")
        with self.voiceover(
            "Social psychology likes to date its first experiment to 1898. <bookmark mark='a'/> Norman Triplett had "
            "children turn fishing reels as fast as they could, alone and in competition with another child. <bookmark mark='b'/> He reported that many were "
            "faster with a competitor beside them. <bookmark mark='c'/> But in 2012 Wolfgang Stroebe pointed out "
            "that reanalyses of Triplett's own figures show little effect, with about half the children no faster "
            "at all. <bookmark mark='d'/> The field's founding experiment was weaker than its legend, a pattern this "
            "part keeps finding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(reels))
            self.play(*[Rotate(r_[0][1], angle=4 * PI * (1 + 0.15 * k), about_point=r_[0][0].get_center())
                        for k, r_ in enumerate(reels)], run_time=3)
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def drive(self):
        d = load("impact")
        head = heading(r"Zajonc's drive")
        A = axes([0.5, 3.0], [0, 1.0], x_length=6.0, y_length=3.8, xticks=[1, 2, 3], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: {1: "alone", 2: "watched", 3: "crowd"}[int(v)], yfmt=lambda v: f"{v:g}",
                 xlabel=r"drive", ylabel=r"chance of the right response", center=[-2.9, -0.4, 0], font_size=15)
        D = np.asarray(d["D"])
        cs = VGroup(curve(A.ax, D, d["easy"], GOOD, stroke_width=4), curve(A.ax, D, d["hard"], AUTH, stroke_width=4))
        key = legend([(GOOD, r"well learned: \ the right response dominates"),
                      (AUTH, r"new: \ a wrong response dominates")], font_size=15).move_to(A.ax.c2p(1.9, 0.12))
        rows = rows_of([
            (r"Zajonc, \ 1965: \ the presence of others raises arousal, \ or drive", WHITE),
            (r"drive multiplies the strength of whatever response is already dominant", MODEL),
            (r"on a well-learned task the dominant response is right, \ and an audience helps; \ on a new one it is "
             r"wrong, \ and an audience hurts", PERSON),
            (r"Psyche: \ the right response's chance as drive rises, \ softmax over drive times habit strength", MODEL),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.drive}")
        with self.voiceover(
            "Sometimes audiences helped and sometimes they hurt. <bookmark mark='a'/> In 1965 Zajonc proposed "
            "one rule for both. The presence of others raises arousal, or drive. <bookmark mark='b'/> And drive "
            "multiplies the strength of whatever response is already dominant. <bookmark mark='c'/> On a "
            "well-learned task the dominant response is the right one, so an audience helps. On a new task it's "
            "often wrong, so an audience hurts. <bookmark mark='d'/> Here it is in Psyche: the chance of the right "
            "response as drive rises, for an easy task and a hard one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs[0]), Create(cs[1]), FadeIn(key), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def roaches(self):
        head = heading(r"Cockroaches, \ twice")
        cols = VGroup()
        for k, (title, txt, c) in enumerate((
                (r"1969", r"runway: \ faster with an audience of roaches; \ maze: \ slower", GOOD),
                (r"2020, \ preregistered", r"slower with an audience in both: \ inhibition, \ but no facilitation", AUTH))):
            box = RoundedRectangle(corner_radius=0.1, width=5.6, height=2.0, stroke_color=c, fill_color=BLACK,
                                   fill_opacity=0.4)
            cols.add(VGroup(box, label(title, font_size=24, color=c).next_to(box.get_top(), DOWN, buff=0.2),
                            wrapped_label(txt, 5.0, 21, WHITE).move_to(box).shift(DOWN * 0.25)))
        cols.arrange(RIGHT, buff=0.6).move_to([0, 1.2, 0])
        rows = rows_of([
            (r"Zajonc, \ Heingartner and Herman, \ 1969: \ cockroaches fleeing a light down a straight runway or "
             r"through a maze, \ alone or watched by other roaches", WHITE),
            (r"Halfmann, \ Bredeh\"oft and H\"ausser, \ 2020: \ a preregistered direct replication found an audience "
             r"slowed the roaches on both tasks", AUTH),
            (r"the classic interaction did not reappear; \ in people, \ the effects of an audience are small and "
             r"vary with the task", YOU),
        ], 12.4, 21, 0.3).move_to([0, -1.8, 0])
        tag = published_tag(r"Zajonc et al.\ (1969); \ Halfmann et al.\ (2020)")
        with self.voiceover(
            "Zajonc tested his rule on cockroaches, whose dominant response is to run from light. "
            "<bookmark mark='a'/> In 1969, with two colleagues, he had them flee down a straight runway or through a "
            "maze, alone or watched by other roaches. With an audience they were faster on the runway and slower in "
            "the maze, just as drive predicts. <bookmark mark='b'/> In 2020 Halfmann and colleagues ran a "
            "preregistered direct replication. An audience slowed the roaches on both tasks. <bookmark mark='c'/> "
            "The famous interaction didn't reappear. In people, the effects of an audience are small, and vary with "
            "the task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def loafing(self):
        head = heading(r"Many hands make light the work")
        A = axes([0.5, 6.5], [0, 100], x_length=5.6, y_length=3.6, xticks=[1, 2, 6], yticks=[0, 25, 50, 75, 100],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%", xlabel=r"people they believed were shouting",
                 ylabel=r"effort, \ against alone", center=[-3.0, -0.4, 0], font_size=15)
        pts = [(1, 100), (2, 82), (6, 74)]
        c = VGroup(curve(A.ax, [p[0] for p in pts], [p[1] for p in pts], CROWD, stroke_width=4),
                   scatter(A.ax, [p[0] for p in pts], [p[1] for p in pts], CROWD, radius=0.08))
        rows = rows_of([
            (r"Latan\'e, \ Williams and Harkins, \ 1979: \ students shouted as loudly as they could, \ sometimes "
             r"believing others shouted with them", WHITE),
            (r"believing one other shouted, \ they gave 82\% of their solo effort; \ believing five others, \ 74\%",
             CROWD),
            (r"Karau and Williams, \ 1993: \ 78 studies: \ social loafing is moderate and general, \ and shrinks when "
             r"each person's work is identifiable or the task matters to them", GOOD),
            (r"the same crowd can energize and dilute: \ an audience watches you, \ a group hides you", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Latan\'e, \ Williams \& Harkins (1979); \ Karau \& Williams (1993)")
        with self.voiceover(
            "Groups can also make people work less. <bookmark mark='a'/> In 1979 Latané, Williams and Harkins had "
            "students shout as loudly as they could, sometimes believing others "
            "were shouting with them. <bookmark mark='b'/> Believing one other person shouted, they gave eighty-two "
            "percent of their solo effort. Believing five others did, seventy-four. <bookmark mark='c'/> In 1993 "
            "Karau and Williams pooled seventy-eight studies. Social loafing is moderate and general, and it shrinks "
            "when each person's work can be identified, or when the task matters to them. <bookmark mark='d'/> So "
            "the same crowd can energize and dilute. An audience watches you; a group hides you."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c[0]), FadeIn(c[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
