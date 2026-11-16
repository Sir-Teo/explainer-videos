from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403


class Free(SoundScene):
    def construct(self):
        chapter(self, 9, r"Free jazz, \ and what improvisers do", r"What is left when the changes go?")
        self.ornette()
        self.after()
        self.duo()
        self.models()
        self.memory()
        self.feedback()

    # ------------------------------------------------------------------
    def ornette(self):
        items = [
            (r"1959 again: \ Ornette Coleman's \textit{The Shape of Jazz to Come}", WHITE),
            (r"no piano, \ no fixed changes: \ the soloist sets the harmony as he goes, \ the bass follows", WHITE),
            (r"\textit{Free Jazz} \ (1961): \ two quartets improvising at once, \ for over half an hour", WHITE),
            (r"Coleman called his principle `harmolodics': \ melody, \ harmony and rhythm of equal weight", TUNE),
            (r"the third answer to bebop in one year: \ more changes, \ fewer, \ or none", GREY_A),
        ]
        rows_scene(self, r"Ornette Coleman", items,
                   "1959 again. Ornette Coleman's The Shape of Jazz to Come. <bookmark mark='b'/> No piano and no fixed changes: "
                   "players negotiate melodic and harmonic direction together rather than following a fixed chord chart. <bookmark mark='c'/> His Free Jazz, from "
                   "1961, set two quartets improvising at once for over half an hour. <bookmark mark='d'/> Coleman called his "
                   "principle harmolodics, giving melody, harmony and rhythm equal weight. <bookmark mark='e'/> It was the third "
                   "answer to bebop in a single year: more changes, fewer, or none.", marks="bcde")

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (r"Cecil Taylor: \ clusters and energy at the piano, \ from the late 1950s", WHITE),
            (r"Coltrane's \textit{A Love Supreme} \ (1964), \ and his later collective improvisations", WHITE),
            (r"Chicago's AACM \ (1965): \ musicians organising their own concerts, \ schools and compositions", WHITE),
            (r"free does not mean random: \ players listen, \ answer and build, \ without a shared chart", TUNE),
            (r"the question becomes: \ what structure do improvisers carry inside?", GREY_A),
        ]
        rows_scene(self, r"after 1959", items,
                   "Others went further. <bookmark mark='b'/> Cecil Taylor brought clusters and energy to the piano from the late "
                   "1950s. <bookmark mark='c'/> Coltrane moved from A Love Supreme, in 1964, to collective improvisations. "
                   "<bookmark mark='d'/> In Chicago, the Association for the Advancement of Creative Musicians, founded in 1965, "
                   "organised its own concerts, schools and compositions. <bookmark mark='e'/> Free does not mean random: players "
                   "listen, answer and build, without a shared chart. <bookmark mark='f'/> So the question becomes: what "
                   "structure do improvisers carry inside them?", marks="cdef")

    # ------------------------------------------------------------------
    def duo(self):
        d = load("echo")
        c = clip("echo.duo")
        calls = [tuple(x) for f in d["calls"] for x in f]
        answers = [tuple(x) for a in d["answers"] for x in a]
        total = d["eighths"]
        roll = voices_roll([[[m, e, 1.0] for m, e in calls], [[m, e, 1.0] for m, e in answers]], width=12.0, height=2.8,
                           colors=[TUNE, BLUE], total=total, lo=56, hi=88, bar_h=0.13).move_to(DOWN * 0.3)
        leg = VGroup(label(r"saxophone: \ a figure", font_size=19, color=TUNE), label(r"piano: \ the answer, \ a fourth up and backwards", font_size=19, color=BLUE)).arrange(RIGHT, buff=0.9).next_to(roll, UP, buff=0.35)
        head = label(r"a toy free duo \ (ours): \ no changes, \ only answers", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a toy of our own that shows the difference. No chord changes at all: the saxophone plays a short figure, and the piano answers with the same figure a fourth higher and backwards; the saxophone's next figure starts from where the answer ended. Crude as it is, it does the one thing chapter eight's improviser cannot: it responds to the other part’s symbolic note data; this toy does not analyze live audio."
        ):
            self.play(FadeIn(head), FadeIn(leg), FadeIn(roll))
        from explainer.music.monochord import blues as BL
        with self.listen(c) as snd:
            window(snd, r"a free duo", kind="synthesized", detail=r"an additive saxophone, \ Part 7's piano, \ a cymbal", corner=DL, tag_corner=DR)
            flash(snd, roll.parts[0].notes, list(BL.swing_times([e for _, e in calls], d["bpm"])), hot=WHITE, base=TUNE)
            flash(snd, roll.parts[1].notes, list(BL.swing_times([e for _, e in answers], d["bpm"])), hot=WHITE, base=BLUE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        boxes = VGroup()
        for title, body, col in ((r"referent", ("a tune or changes,", "a mode or a mood"), TUNE),
                                 (r"knowledge base", ("vocabulary: formulas,", "scales, licks, habits"), BLUE),
                                 (r"in the moment", ("choose the next event;", "hear it, continue or change"), EAR)):
            r = RoundedRectangle(width=3.6, height=1.9, corner_radius=0.15, stroke_color=col, stroke_width=2)
            detail = VGroup(*[label(line, font_size=17, color=WHITE) for line in body]).arrange(DOWN, buff=0.1)
            if detail.width > r.width - 0.4:
                detail.scale_to_fit_width(r.width - 0.4)
            t = VGroup(label(title, font_size=22, color=col), detail).arrange(DOWN, buff=0.22).move_to(r)
            boxes.add(VGroup(r, t))
        boxes.arrange(RIGHT, buff=0.7).move_to(UP * 0.4)
        arrows = VGroup(CurvedArrow(boxes[0].get_top(), boxes[2].get_top(), color=GREY_B, angle=-0.6),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=GREY_B))
        loop = CurvedArrow(boxes[2].get_bottom() + RIGHT * 0.8, boxes[2].get_bottom() + LEFT * 0.8, color=EAR, angle=-2.5)
        cap = label(r"after Jeff Pressing \ (1988): \ improvisation as choice, \ guided by a referent and a stored vocabulary", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        head = label(r"a model of improvising", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The psychologist and musician Jeff Pressing proposed a model in 1988. <bookmark mark='a'/> An improviser works "
            "from a referent, the tune, its changes, a mode or a mood; <bookmark mark='b'/> draws on a knowledge base, the "
            "vocabulary of formulas, scales and habits built over years; <bookmark mark='c'/> and in the moment chooses the "
            "next event, hears it, and decides whether to continue or change. Our program has a referent and a tiny "
            "vocabulary, and chooses by dice; it does not hear itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            for mark, b in zip("abc", boxes):
                vo.wait_until(mark)
                self.play(FadeIn(b))
            self.play(FadeIn(arrows), Create(loop), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        items = [
            (r"Philip Johnson-Laird \ (2002): \ how much can be computed in real time?", WHITE),
            (r"he argued that chord sequences need memory and planning, \ but each new note can be chosen by simple rules", WHITE),
            (r"so improvisers learn the changes slowly, \ and play the notes fast", WHITE),
            (r"a split our program shares: \ the changes are given, \ the notes are chosen locally", TUNE),
            (r"fast thinking needs well-practised material", GREY_A),
        ]
        rows_scene(self, r"what can be done in real time?", items,
                   "The psychologist Philip Johnson-Laird asked in 2002 how much of improvising can be computed in real time. "
                   "<bookmark mark='b'/> He argued that chord sequences need memory and planning, but that each new note can be "
                   "chosen by simple rules. <bookmark mark='c'/> So improvisers learn the changes slowly, and play the notes fast. "
                   "<bookmark mark='d'/> Our program shares that split: the changes are given, and the notes are chosen locally. "
                   "<bookmark mark='e'/> Fast thinking needs well-practised material.", marks="bcde")

    # ------------------------------------------------------------------
    def feedback(self):
        items = [
            (r"improvising is social: \ the drummer answers the soloist, \ the pianist anticipates", WHITE),
            (r"Ingrid Monson's \textit{Saying Something} \ (1996): \ jazz as conversation, \ studied from the rhythm section", WHITE),
            (r"a band's interplay is where our program is weakest", WHITE),
            (r"Part 43 turns to performing together", TUNE),
            (r"chapter 10: \ what the scanner and the database add", GREY_A),
        ]
        rows_scene(self, r"a conversation", items,
                   "And improvising is social. <bookmark mark='b'/> The drummer answers the soloist, the pianist anticipates. "
                   "<bookmark mark='c'/> Ingrid Monson's Saying Something, of 1996, studied jazz as conversation, from the "
                   "rhythm section's side. <bookmark mark='d'/> That interplay is where our program is weakest. "
                   "<bookmark mark='e'/> Part 43 turns to performing together. <bookmark mark='f'/> Chapter ten asks what the "
                   "brain scanner and the database add.", marks="cdef")
