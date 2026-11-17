from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


def face(color=GREY_A, mouth=0.0) -> VGroup:
    """A schematic face: a head, two eyes and a mouth whose curve is set by ``mouth`` (-1 to 1)."""
    head = Ellipse(width=1.3, height=1.6, color=color, stroke_width=3)
    eyes = VGroup(Dot([-0.25, 0.2, 0], radius=0.06, color=color), Dot([0.25, 0.2, 0], radius=0.06, color=color))
    m = ArcBetweenPoints([-0.3, -0.35, 0], [0.3, -0.35, 0], angle=0.9 * mouth if mouth else 0.0001, color=color,
                         stroke_width=3)
    return VGroup(head, eyes, m)


class Impressions(VoiceoverScene):
    def construct(self):
        self.card()
        self.tenth()
        self.elections()
        self.slices()

    def card(self):
        card = chapter_card(6, r"First impressions", r"What do people read from a face in a tenth of a second?",
                            lit={1993: r"Ambady \& Rosenthal", 2005: r"Todorov et al.", 2006: r"Willis \& Todorov"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter six. First impressions."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def tenth(self):
        head = heading(r"A tenth of a second")
        faces = VGroup(*[face(c, m) for c, m in ((CROWD, 0.6), (GREY_A, 0.0), (AUTH, -0.4))]).arrange(RIGHT, buff=0.7)
        faces.move_to([-3.4, 1.0, 0])
        bar = VGroup(*[Rectangle(width=w, height=0.3, stroke_width=0, fill_color=c, fill_opacity=0.8)
                       for w, c in ((0.3, PERSON), (1.5, CROWD), (3.0, MODEL))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.18)
        bar.move_to([-4.0, -1.2, 0])
        bl = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(b_, RIGHT, buff=0.15) for t, b_ in
                      zip((r"100 ms", r"500 ms", r"1{,}000 ms"), bar)])
        rows = rows_of([
            (r"Willis and Todorov, \ 2006: \ people judged faces they saw for 100, \ 500 or 1{,}000 milliseconds", WHITE),
            (r"judgments of trustworthiness, \ competence, \ likeability, \ aggressiveness and attractiveness after "
             r"100 ms agreed closely with judgments made with no time limit", CROWD),
            (r"more time made people more confident and their impressions more differentiated, \ not different", MODEL),
            (r"agreement between judges is not accuracy: \ whether a face reveals character is another question", YOU),
        ], 6.4, 20, 0.34).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Willis \& Todorov (2006)")
        with self.voiceover(
            "People read minds from faces, and fast. <bookmark mark='a'/> In 2006 Willis and "
            "Todorov showed people faces for a tenth of a second, half a second or a whole second. "
            "<bookmark mark='b'/> Judgments of trustworthiness, competence, likeability, aggressiveness and "
            "attractiveness made after a tenth of a second agreed closely with judgments made with no time limit. "
            "<bookmark mark='c'/> More time made people more confident, and their impressions more "
            "differentiated, but not different. <bookmark mark='d'/> Notice what was measured, though: people "
            "agreeing with each other. Whether a face reveals character is another question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(faces))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[GrowFromEdge(b_, LEFT) for b_ in bar], lag_ratio=0.3),
                      FadeIn(bl))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def elections(self):
        head = heading(r"Faces and votes")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.4, y_length=3.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"2004 Senate races called correctly", center=[-3.9, -0.3, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [50, 68.8], [GREY_B, PERSON], width=0.6)
        names = VGroup(label(r"chance", font_size=16, color=GREY_B).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"the more competent face", font_size=16, color=PERSON).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                            buff=0.15))
        top = label(r"68.8\%", font_size=18, color=PERSON).next_to(A.ax.c2p(1, 68.8), UP, buff=0.1)
        rows = rows_of([
            (r"Todorov and colleagues, \ 2005, \ \emph{Science}: \ people judged which of two unfamiliar candidates "
             r"looked more competent, \ after as little as a second", WHITE),
            (r"the candidate judged more competent won 68.8\% of the 2004 US Senate races", PERSON),
            (r"the judges had never seen the candidates before: \ the faces alone carried the prediction", CROWD),
            (r"so a snap impression of a face may move votes, \ whatever the face does or does not say about the "
             r"candidate", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Todorov et al.\ (2005)")
        with self.voiceover(
            "Snap impressions also have consequences. <bookmark mark='a'/> In 2005 Todorov and colleagues showed "
            "people pairs of unfamiliar political candidates, for as little as a second, and asked which looked "
            "more competent. <bookmark mark='b'/> The candidate judged more competent had won sixty-eight point "
            "eight percent of the 2004 United States Senate races. <bookmark mark='c'/> The judges had never "
            "seen the candidates before. The faces alone carried the prediction. <bookmark mark='d'/> So a snap impression "
            "of a face may move votes, whatever the face does or doesn't say about the candidate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), GrowFromEdge(b[0], DOWN))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(top), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def slices(self):
        head = heading(r"Thin slices of behaviour")
        clip = VGroup(*[Rectangle(width=1.2, height=0.8, stroke_color=CROWD, fill_color="#1B2029", fill_opacity=1)
                        for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to([-3.6, 1.0, 0])
        cl = VGroup(*[label(r"10 s", font_size=16, color=CROWD).move_to(c_) for c_ in clip])
        mute = label(r"silent", font_size=18, color=GREY_A).next_to(clip, DOWN, buff=0.2)
        rows = rows_of([
            (r"Ambady and Rosenthal, \ 1993: \ strangers watched three silent 10-second clips of a college teacher, "
             r"\ under half a minute in all", WHITE),
            (r"their ratings predicted the teacher's end-of-semester evaluations by students who had sat through "
             r"the whole course", CROWD),
            (r"in a second study, \ similar ratings of high-school teachers predicted their principal's ratings", MODEL),
            (r"thin slices carry real information about how people come across; \ Part 53 asks what that is worth "
             r"in interviews", YOU),
        ], 7.0, 21, 0.38).move_to([2.7, -0.4, 0])
        tag = published_tag(r"Ambady \& Rosenthal (1993)")
        with self.voiceover(
            "Brief impressions of behaviour do better than faces. <bookmark mark='a'/> In 1993 Ambady and "
            "Rosenthal had strangers watch three silent ten-second clips of a college teacher, under half "
            "a minute in all. <bookmark mark='b'/> Their ratings predicted the teacher's end-of-semester "
            "evaluations by students who had sat through the whole course. <bookmark mark='c'/> In a second study, "
            "similar ratings of high-school teachers predicted their principal's ratings. <bookmark mark='d'/> Thin "
            "slices carry real information about how people come across. Part 53 asks what that's worth in a job "
            "interview."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(clip), FadeIn(cl), FadeIn(mute))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
