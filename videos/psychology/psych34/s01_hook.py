from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403

PRODS = [r"``Please continue.''", r"``The experiment requires that you continue.''",
         r"``It is absolutely essential that you continue.''", r"``You have no other choice, \ you must go on.''"]


def generator(n: int = 30, width: float = 12.4) -> VGroup:
    """The shock generator as a strip of 30 switches, 15 to 450 volts."""
    sw = VGroup()
    w = width / n
    for k in range(n):
        v = 15 * (k + 1)
        col = interpolate_color(ManimColor(GREY_D), ManimColor(AUTH), k / (n - 1))
        box = RoundedRectangle(corner_radius=0.04, width=w * 0.82, height=0.62, stroke_color=GREY_B, stroke_width=1.2,
                               fill_color=col, fill_opacity=0.35)
        box.move_to([-width / 2 + w * (k + 0.5), 0, 0])
        sw.add(VGroup(box, label(str(v), font_size=11, color=GREY_A).next_to(box, DOWN, buff=0.08)))
    return sw


class Hook(VoiceoverScene):
    def construct(self):
        self.basement()
        self.board()
        self.result()
        self.question()
        self.objectives()

    def basement(self):
        head = heading(r"1961: \ a basement at Yale")
        rows = rows_of([
            (r"newspaper ads in New Haven: \ men aged 20 to 50, \ paid to take part in a study of memory and "
             r"learning", WHITE),
            (r"in the basement of Linsly-Chittenden Hall, \ an experimenter in a grey coat, \ and another "
             r"``volunteer'' who was in on it", CROWD),
            (r"a rigged draw made the real volunteer the teacher; \ the other man, \ the learner, \ was strapped "
             r"into a chair in the next room", AUTH),
            (r"each wrong answer: \ a shock, \ 15 volts stronger than the last", PERSON),
        ], 6.4, 22, 0.4).move_to([3.1, -0.2, 0])
        room1 = RoundedRectangle(corner_radius=0.08, width=3.0, height=2.4, stroke_color=GREY_B, stroke_width=2)
        room2 = RoundedRectangle(corner_radius=0.08, width=2.2, height=2.4, stroke_color=GREY_B, stroke_width=2)
        rooms = VGroup(room1, room2).arrange(RIGHT, buff=0.0).move_to([-3.6, 0.2, 0])
        exp_ = VGroup(Circle(radius=0.26, color=AUTH, fill_opacity=0.4), label(r"experimenter", font_size=14,
                                                                              color=AUTH))
        tea = VGroup(Circle(radius=0.26, color=PERSON, fill_opacity=0.4), label(r"teacher", font_size=14,
                                                                               color=PERSON))
        lea = VGroup(Circle(radius=0.26, color=CROWD, fill_opacity=0.4), label(r"learner", font_size=14,
                                                                              color=CROWD))
        for g_ in (exp_, tea, lea):
            g_[1].next_to(g_[0], DOWN, buff=0.08)
        exp_.move_to(room1.get_center() + LEFT * 0.75 + UP * 0.45)
        tea.move_to(room1.get_center() + RIGHT * 0.55 + DOWN * 0.45)
        lea.move_to(room2.get_center())
        box = Rectangle(width=0.7, height=0.35, stroke_color=AUTH, fill_color=AUTH, fill_opacity=0.25)
        box.next_to(tea, UP, buff=0.12)
        wire = DashedLine(box.get_right(), lea[0].get_left(), color=AUTH, stroke_width=2)
        plan = VGroup(rooms, exp_, tea, lea, box, wire)
        cap = label(r"two rooms, \ one wire", font_size=18, color=GREY_A).next_to(rooms, DOWN, buff=0.2)
        tag = historical_tag(r"Milgram (1963, \ 1974)")
        with self.voiceover(
            "In the summer of 1961, newspaper ads in New Haven offered men between twenty and fifty a small payment "
            "to take part in a study of memory and learning at Yale. <bookmark mark='a'/> Those who came were led "
            "to the basement of Linsly-Chittenden Hall. There they met an experimenter in a grey coat, and another "
            "volunteer, a pleasant middle-aged man, who was in fact working for the experimenter. "
            "<bookmark mark='b'/> A rigged draw made the real volunteer the teacher. The other man, the learner, was "
            "strapped into a chair in the next room. <bookmark mark='c'/> The teacher would read out word pairs, and "
            "for each wrong answer give the learner an electric shock, fifteen volts stronger than the last. "
            "<bookmark mark='d'/>"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rooms), FadeIn(exp_), FadeIn(tea), FadeIn(lea), FadeIn(cap), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Indicate(lea, color=CROWD))
            vo.wait_until("c")
            self.play(FadeIn(box), Create(wire), FadeIn(rows[3]))
            vo.wait_until("d")
        self.clear_scene()

    def board(self):
        head = heading(r"The procedure, \ as a trial strip")
        gen = generator().move_to([0, 0.4, 0])
        marks = VGroup()
        for v, text, c in ((300, r"300: \ he pounds on the wall", CROWD),
                           (315, r"315: \ again; \ then silence", AUTH), (450, r"450: \ the last switch", AUTH)):
            sw = gen[v // 15 - 1][0]
            up = 0.8 if v != 315 else 1.5
            arrow = Arrow(sw.get_top() + UP * up, sw.get_top() + UP * 0.05, buff=0, color=c, stroke_width=3,
                          max_tip_length_to_length_ratio=0.2)
            marks.add(VGroup(arrow, label(text, font_size=18, color=c).next_to(arrow, UP, buff=0.08)))
        keep_in_frame(marks[2][1])
        prods = VGroup(*[label(rf"{k + 1}.\ \ {p}", font_size=22, color=interpolate_color(
            ManimColor(WHITE), ManimColor(AUTH), k / 3)) for k, p in enumerate(PRODS)])
        prods.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-1.6, -2.15, 0])
        ptitle = label(r"if the teacher hesitates, \ the experimenter's prods, \ in order:", font_size=20,
                       color=GREY_A).next_to(prods, UP, buff=0.22, aligned_edge=LEFT)
        tag = historical_tag(r"Milgram (1963, \ 1974)")
        with self.voiceover(
            "Here is the shock generator, as a strip of thirty switches, from fifteen to four hundred and fifty "
            "volts. <bookmark mark='a'/> No shock was real; the learner was an actor. In the first version Milgram "
            "published, he made no sound until three hundred volts, when he pounded on the wall. "
            "<bookmark mark='b'/> At three hundred and fifteen he pounded again, and then fell silent. The teacher "
            "was told to treat silence as a wrong answer, and go on. "
            "<bookmark mark='c'/> Four hundred and fifty is the last switch. <bookmark mark='d'/> Whenever the "
            "teacher hesitated, the experimenter had four prods, in order. Please continue. The experiment requires "
            "that you continue. It is absolutely essential that you continue. And: you have no other choice, you "
            "must go on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(s) for s in gen], lag_ratio=0.05), run_time=2.5)
            for m, mk in zip("abc", marks):
                vo.wait_until(m)
                self.play(FadeIn(mk, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(ptitle), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in prods], lag_ratio=0.9),
                      run_time=6)
        self.clear_scene()

    def result(self):
        head = heading(r"Before and after")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.4, y_length=3.8, xticks=None, yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"share of men", center=[-3.9, -0.3, 0], font_size=15)
        b = VGroup(bars(A.ax, [0], [1], GREY_B, width=0.6), bars(A.ax, [1], [65], AUTH, width=0.6))
        names = VGroup(label(r"predicted \ (psychiatrists)", font_size=16, color=GREY_B)
                       .next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                       label(r"observed", font_size=16, color=AUTH).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        vals = VGroup(label(r"about 1 in 1{,}000", font_size=17, color=GREY_B).next_to(A.ax.c2p(0, 2), UP, buff=0.1),
                      label(r"26 of 40", font_size=20, color=AUTH).next_to(A.ax.c2p(1, 65), UP, buff=0.1))
        rows = rows_of([
            (r"psychiatrists Milgram asked to predict expected almost no one to go to the end", GREY_A),
            (r"in the first published version, \ 26 of the 40 men, \ 65\%, \ went to 450 volts", AUTH),
            (r"many sweated, \ trembled and argued, \ and kept going; \ the other 14 stopped, \ none before 300 volts",
             CROWD),
            (r"it became psychology's most famous finding, \ and the archives would later complicate nearly every "
             r"part of it", YOU),
        ], 6.4, 21, 0.36).move_to([3.0, -0.2, 0])
        tag = historical_tag(r"Milgram (1963, \ 1974)")
        with self.voiceover(
            "Milgram asked psychiatrists to predict what people would do. <bookmark mark='a'/> They "
            "expected almost no one to go to the end, about one in a thousand. <bookmark mark='b'/> In the first "
            "version he published, in 1963, twenty-six of the forty men, sixty-five percent, went all the way to "
            "four hundred and fifty volts. <bookmark mark='c'/> Many sweated, trembled and argued, and kept going. "
            "The other fourteen stopped, none of them before three hundred volts. <bookmark mark='d'/> It became the "
            "most famous finding in psychology. This part tells it as it was run, as it was retold, and as the "
            "archives now show it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(b[0]), FadeIn(vals[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vals[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how much is decided by who is in the room?")
        rows = rows_of([
            (r"the famous studies: \ Asch's lines, \ Milgram's generator, \ Zimbardo's prison, \ the 38 witnesses",
             AUTH),
            (r"each as it was run, \ as it was retold, \ and as the record now shows it", CROWD),
            (r"then the mathematics the famous studies never had: \ thresholds, \ networks and crowds", MODEL),
        ], 12.4, 28, 0.5).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how much of what you do is decided by who is in the room. <bookmark mark='a'/> It "
            "takes the famous studies: Asch's lines, Milgram's generator, Zimbardo's prison and the thirty-eight "
            "witnesses. <bookmark mark='b'/> Each one as it was run, as it was retold, and as the record now shows "
            "it. <bookmark mark='c'/> Then it builds the mathematics those studies never had: thresholds, networks "
            "and crowds."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 34", font_size=34, color=GREY_B), label(r"Social Influence", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"norms and conformity: \ Sherif's light, \ Asch's lines, \ and what later samples found",
            r"obedience: \ Milgram's variations as a dose-response curve, \ and what the archives show",
            r"the prison study and the 38 witnesses: \ two stories and their records",
            r"bystanders, \ audiences, \ loafers and groups that decide",
            r"persuasion: \ two routes, \ and norms in the field",
            r"thresholds, \ opinions on networks, \ contagion and the wisdom of crowds, \ computed",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 34 of Psychology, Built: social influence, the first part of Act Nine, on other people. "
            "<bookmark mark='a'/> We'll start with norms and conformity: Sherif's moving light, Asch's lines, and "
            "what later samples found. We'll redraw obedience as a dose-response curve across Milgram's variations, "
            "and read what his archives show. We'll take two famous stories, the prison study and the thirty-eight "
            "witnesses, and set them against their records. We'll meet bystanders, audiences, loafers and groups "
            "that decide. We'll look at persuasion's two routes and at norms tested in the field. And we'll compute "
            "thresholds, opinions on networks, contagion and the wisdom of crowds."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
