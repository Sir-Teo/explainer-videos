from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


def canvas(kind: str, color) -> VGroup:
    """A schematic stand-in for an abstract painting (not a reproduction): a grid of tinted cells, or circles."""
    frame = Rectangle(width=2.2, height=1.7, stroke_color=color, stroke_width=3, fill_color="#14181F", fill_opacity=1)
    marks = VGroup()
    if kind == "grid":
        for i in range(4):
            for j in range(5):
                marks.add(Square(side_length=0.3, stroke_width=0, fill_color=color,
                                 fill_opacity=0.15 + 0.12 * ((i * 3 + j * 5) % 6)).move_to(
                    frame.get_center() + [(-0.8 + 0.4 * j), (0.6 - 0.4 * i), 0]))
    else:
        for (x, y, r) in ((-0.5, 0.25, 0.42), (0.45, -0.2, 0.3), (0.2, 0.45, 0.16), (-0.35, -0.45, 0.2)):
            marks.add(Circle(radius=r, color=color, stroke_width=3).move_to(frame.get_center() + [x, y, 0]))
        marks.add(Line(frame.get_center() + [-0.9, -0.6, 0], frame.get_center() + [0.9, 0.55, 0], color=color,
                       stroke_width=2))
    return VGroup(frame, marks)


def matrix_table(ing, outg, font_size: int = 20, cell: float = 0.62) -> VGroup:
    """Tajfel's matrix as two rows of numbers: the top row for a member of your own group, the bottom row for a member
    of the other.  ``.cols[j]`` is column j (a VGroup of its two numbers and its box)."""
    cols = VGroup()
    for j, (a, b) in enumerate(zip(ing, outg)):
        box = Rectangle(width=cell, height=1.1, stroke_color=GREY_D, stroke_width=1)
        ta = label(f"{a:.0f}", font_size=font_size, color=IN).move_to(box.get_center() + UP * 0.25)
        tb = label(f"{b:.0f}", font_size=font_size, color=OUTG).move_to(box.get_center() + DOWN * 0.25)
        cols.add(VGroup(box, ta, tb).shift(RIGHT * j * cell))
    names = VGroup(label(r"a member of your group", font_size=16, color=IN),
                   label(r"a member of the other group", font_size=16, color=OUTG)).arrange(DOWN, buff=0.28,
                                                                                         aligned_edge=RIGHT)
    names.next_to(cols, LEFT, buff=0.25)
    out = VGroup(names, cols)
    out.cols = cols
    return out


class Hook(VoiceoverScene):
    def construct(self):
        self.paintings()
        self.matrix()
        self.question()
        self.objectives()

    def paintings(self):
        head = heading(r"Klee or Kandinsky?")
        a = canvas("grid", IN).move_to([-4.6, 1.0, 0])
        b = canvas("circles", OUTG).move_to([-2.0, 1.0, 0])
        la = label(r"``Klee''", font_size=18, color=IN).next_to(a, DOWN, buff=0.15)
        lb = label(r"``Kandinsky''", font_size=18, color=OUTG).next_to(b, DOWN, buff=0.15)
        note = label(r"schematic stand-ins, \ not the paintings", font_size=14, color=GREY_B).next_to(
            VGroup(la, lb), DOWN, buff=0.25)
        rows = rows_of([
            (r"Henri Tajfel: \ born in Poland, \ Jewish, \ captured in 1940 as a soldier in the French army, \ he "
             r"survived the war as a prisoner; \ afterwards he worked with Jewish orphans", WHITE),
            (r"at Bristol, \ from 1967, \ he asked what the least is that it takes for people to discriminate", CROWD),
            (r"Tajfel, \ Billig, \ Bundy and Flament, \ 1971: \ schoolboys aged 14 and 15 were divided by a trivial "
             r"test, \ in one study their preference between pictures said to be by Klee and by Kandinsky", PERSON),
            (r"each boy knew only his own group; \ nobody met, \ nobody competed, \ nobody could gain for himself", YOU),
        ], 6.4, 20, 0.36).move_to([3.1, -0.2, 0])
        tag = historical_tag(r"Tajfel, \ Billig, \ Bundy \& Flament (1971)")
        with self.voiceover(
            "Henri Tajfel was born in Poland, and he was Jewish. Captured in 1940 as a soldier in the French army, "
            "he survived the war as a prisoner, and afterwards worked with Jewish orphans. <bookmark mark='a'/> At "
            "Bristol, from 1967, he asked what the least is that it takes for people to discriminate. "
            "<bookmark mark='b'/> In 1971 Tajfel and his colleagues divided schoolboys of fourteen and fifteen by a "
            "trivial test. In one study it was their preference between pictures said to be by Klee and by "
            "Kandinsky. <bookmark mark='c'/> Each boy knew only which group he was in. Nobody met, nobody "
            "competed, and nobody could gain anything for himself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(a), FadeIn(b), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(la), FadeIn(lb), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def matrix(self):
        d = load("matrix")
        head = heading(r"Points for two strangers")
        T = matrix_table(d["ingroup"], d["outgroup"]).move_to([0.3, 1.4, 0])
        cols = T.cols
        right = SurroundingRectangle(cols[d["pick_joint"]], color=GOOD, buff=0.04)
        fair = SurroundingRectangle(cols[d["pick_fair"]], color=GREY_A, buff=0.04)
        left = SurroundingRectangle(cols[d["pick_difference"]], color=AUTH, buff=0.04)
        lr = label(r"most in total, \ and most for your group", font_size=15, color=GOOD).next_to(right, DOWN, buff=0.15)
        lf = label(r"equal", font_size=15, color=GREY_A).next_to(fair, DOWN, buff=0.15)
        ll = label(r"your group furthest ahead", font_size=15, color=AUTH).next_to(left, DOWN, buff=0.15)
        rows = rows_of([
            (r"each boy chose a column: \ points, \ worth money, \ for one boy in his own group and one in the other",
             WHITE),
            (r"the right end gives both the most, \ and his own group the most", GOOD),
            (r"the boys pulled toward the left: \ they often gave their own group fewer points so that it could "
             r"beat the other", AUTH),
            (r"a meaningless label, \ strangers, \ nothing to gain: \ and still, \ favouritism", YOU),
        ], 12.0, 21, 0.3).move_to([0, -1.9, 0])
        tag = historical_tag(r"Tajfel, \ Billig, \ Bundy \& Flament (1971); \ the matrix drawn in their style")
        with self.voiceover(
            "Then each boy filled in booklets of matrices like this one. <bookmark mark='a'/> Each column is a "
            "choice: points, worth money, for one anonymous boy in his own group, on top, and one in the other "
            "group, below. <bookmark mark='b'/> The right end gives the most points in total, and the most to his "
            "own group. The middle is equal. The left end leaves his own group furthest ahead, with fewer points "
            "for everyone. <bookmark mark='c'/> The boys pulled toward the left. They often gave their own group "
            "fewer points, so that it could beat the other. <bookmark mark='d'/> A meaningless label, strangers, "
            "nothing to gain, and still, favouritism."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(T))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(right), FadeIn(lr), FadeIn(rows[1]))
            self.play(Create(fair), FadeIn(lf))
            self.play(Create(left), FadeIn(ll))
            vo.wait_until("c")
            self.play(Indicate(cols[0], color=AUTH), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how little does it take to make a group?")
        rows = rows_of([
            (r"how groups turn into us and them: \ identity, \ competition and categories", CROWD),
            (r"how prejudice is measured: \ by asking, \ by reaction time, \ and by sending out identical "
             r"applications", PERSON),
            (r"what a bias score means for one person, \ and for a crowd", MODEL),
            (r"and what changes behaviour, \ as opposed to scores", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how little it takes to make a group. <bookmark mark='a'/> It follows how groups "
            "turn into us and them: identity, competition and categories. <bookmark mark='b'/> It asks how "
            "prejudice is measured: by asking people, by timing them, and by sending out identical job "
            "applications with different names. <bookmark mark='c'/> It asks what a bias score means for one "
            "person, and for a crowd. <bookmark mark='d'/> And it asks what changes behaviour, as opposed to "
            "scores."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 36", font_size=34, color=GREY_B), label(r"Us and Them", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"minimal groups, \ social identity, \ and a summer camp as run and as staged",
            r"stereotypes as categories, \ and a correlation that is not there",
            r"measuring prejudice by asking, \ including a question nobody has to answer",
            r"the Implicit Association Test: \ what reliability does to prediction",
            r"audit studies, \ stereotype threat, \ and contact",
            r"what reduces prejudice, \ a faked study and its real successor, \ and small biases that compound",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 36 of Psychology, Built: us and them, the third part of Act Nine. "
            "<bookmark mark='a'/> We'll start with minimal groups and social identity, and a summer camp as it was "
            "run and as it was staged. We'll treat stereotypes as categories, and find a correlation that isn't "
            "there. We'll measure prejudice by asking, including a question nobody has to answer. We'll take apart "
            "the Implicit Association Test, and see what reliability does to prediction. We'll read audit "
            "studies, stereotype threat and contact. And we'll ask what reduces prejudice, follow a faked study "
            "to its real successor, and watch small biases compound."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
