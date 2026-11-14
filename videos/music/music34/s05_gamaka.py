from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Gamaka(SoundScene):
    def construct(self):
        chapter(self, 4, r"Gamaka", r"Where, \ exactly, \ is a note?")
        self.kinds()
        self.hear()
        self.between()
        self.histogram()
        self.carnatic()
        self.kampita()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"\textit{m\=\i\d{n}\d{d}} \ (meend): \ a slow glide from one note to another", WHITE),
            (r"\textit{\=andolan}: \ a slow swing around a note, \ in some ragas only on some notes", WHITE),
            (r"\textit{ka\d{n}}: \ a grace note touched on the way in", WHITE),
            (r"\textit{gamak}: \ a fast, \ heavy oscillation between notes", TUNE),
            (r"the ornament belongs to the raga: \ the same note ornamented differently is a different raga", GREY_A),
        ]
        rows_scene(self, r"ornaments that are not optional", items,
                   "In this music ornaments are not decoration. <bookmark mark='b'/> Meend is a slow glide from one note to "
                   "another. <bookmark mark='c'/> Andolan is a slow swing around a note, in some ragas only on particular notes. "
                   "<bookmark mark='d'/> Kan is a grace note touched on the way in. <bookmark mark='e'/> Gamak is a fast, heavy "
                   "oscillation. <bookmark mark='f'/> And the ornaments belong to the raga: the same note, ornamented the wrong "
                   "way, makes a different raga, or no raga at all.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("gamaka")
        c = clip("gamaka.two")
        p1 = contour_plot(d["plain"], d["rate"], width=9.6, height=1.8, lo=-1, hi=6, color=BLUE).move_to(UP * 1.4)
        p2 = contour_plot(d["gamaka"], d["rate"], width=9.6, height=1.8, lo=-1, hi=6, color=TUNE).move_to(DOWN * 1.2)
        l1 = label(r"plain notes", font_size=19, color=BLUE).next_to(p1, LEFT, buff=0.3).shift(RIGHT * 0.2)
        l2 = label(r"with meend and andolan", font_size=19, color=TUNE).next_to(p2, LEFT, buff=0.3).shift(RIGHT * 0.2)
        l1.scale_to_fit_width(min(l1.width, 1.6))
        l2.scale_to_fit_width(min(l2.width, 1.6))
        with self.voiceover(
            "Here is one phrase of ours, S R G m G R G R S, drawn as pitch against time. First as plain notes, each held "
            "steady. Then with glides between them and slow swings on three of the notes. Listen to both over the drone, and "
            "watch the line: in the second, very little of the time is spent sitting exactly on a note."
        ):
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"plain, \ then ornamented", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            for key, p in (("plain", p1), ("gamaka", p2)):
                T = len(d[key]) / d["rate"]
                dot = Dot(p.ax.c2p(0, d[key][0]), radius=0.08, color=WHITE)
                snd.show(dot)
                start = d["starts"][key]

                def mover(m, t, key=key, p=p, start=start, T=T):
                    x = min(max(t - start - 0.3, 0.0), T - 0.02)
                    i = int(x * d["rate"])
                    m.move_to(p.ax.c2p(x, d[key][min(i, len(d[key]) - 1)]))

                snd.drive(dot, mover)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        d = load("gamaka")
        bars = columns(d["hist"], None, width=10.6, height=2.6, color=TUNE, bar=0.9).move_to(DOWN * 0.3)
        names = VGroup(*[label(n, font_size=18, color=GREY_A).move_to(bars.bars[int(c / 10)].get_bottom() + DOWN * 0.3)
                         for n, c in (("S", 0), ("R", 200), ("G", 400), ("m", 500), ("P", 700), ("D", 900), ("N", 1100))])
        head = label(r"how long our ornamented alap spends at each pitch \ (cents above Sa, \ folded into one octave)", font_size=23, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"peaks at the notes, \ with wide skirts: \ the glides and swings fill the space between", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Computational studies of raga draw a picture like this from real recordings. Track the pitch of a performance "
            "moment by moment and count how long it spends at each pitch, folded into one octave. This one is from a short alap "
            "of our own, with ornaments. There are peaks at the notes, Sa, Re, Ga, Pa, and wide skirts between them, where the "
            "glides and swings pass through. Real performances give much broader, raga-specific shapes, and the shape is a "
            "fingerprint: it can tell ragas with the same scale apart."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(names), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def carnatic(self):
        items = [
            (r"Carnatic music names ten classical gamakas; \ in practice, \ \textit{kampita}, \ the oscillation, \ dominates", WHITE),
            (r"in some Carnatic ragas almost every note oscillates", WHITE),
            (r"notation gives the notes; \ the gamakas are learned from a teacher's voice", WHITE),
            (r"Part 10's question again: \ what can a score hold?", TUNE),
            (r"Part 61 tracks pitch automatically, \ the tool these studies rely on", GREY_A),
        ]
        rows_scene(self, r"gamaka in the south", items,
                   "In Carnatic music ornament goes further. <bookmark mark='b'/> Its theory names ten classical gamakas, and in "
                   "practice the oscillation called kampita dominates: <bookmark mark='c'/> in some ragas almost every note "
                   "moves. <bookmark mark='d'/> Notation gives the notes; the gamakas are learned from a teacher's voice. "
                   "<bookmark mark='e'/> It is Part 10's question again: what can a score hold? <bookmark mark='f'/> Part 61 "
                   "builds automatic pitch tracking, the tool all these studies rely on.", marks="cdef")

    # ------------------------------------------------------------------
    def kampita(self):
        d = load("kampita")
        c = clip("kampita.phrase")
        p = contour_plot(d["contour"], d["rate"], width=10.4, height=2.6, lo=-1, hi=9, color=EAR).move_to(DOWN * 0.2)
        head = label(r"kampita: \ notes that move \ (a phrase of ours in the Carnatic manner)", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"S R g m P m g R S: \ only Sa and Pa held still", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Here is the idea pushed further, in the manner of Carnatic singing: a phrase in which only Sa and Pa are held "
            "still, and every other note oscillates, some widely. Watch the line: the komal Ga and Ma swing through more than "
            "a semitone. In many Carnatic ragas, this movement is what the note is."
        ):
            self.play(FadeIn(head), FadeIn(p), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"kampita", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            T = len(d["contour"]) / d["rate"]
            dot = Dot(p.ax.c2p(0, d["contour"][0]), radius=0.08, color=WHITE)
            snd.show(dot)

            def mover(m, t):
                x = min(max(t - 0.3, 0.0), T - 0.02)
                m.move_to(p.ax.c2p(x, d["contour"][min(int(x * d["rate"]), len(d["contour"]) - 1)]))

            snd.drive(dot, mover)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def between(self):
        items = [
            (r"in this music much of the time is spent between named pitches", WHITE),
            (r"a glide's speed and curve are part of the raga", WHITE),
            (r"Western notation, \ built on fixed pitches, \ has no symbol for most of them", WHITE),
            (r"computer studies measure them from pitch tracks: \ duration, \ depth, \ rate of oscillation", TUNE),
            (r"the next section draws one", GREY_A),
        ]
        rows_scene(self, r"the space between the notes", items,
                   "Think about what this means. <bookmark mark='b'/> In this music much of the time is spent between the named pitches. <bookmark mark='c'/> How fast a glide moves, and the curve it follows, are part of the raga. <bookmark mark='d'/> Western notation, built on fixed pitches, has no symbol for most of this. <bookmark mark='e'/> Computer studies measure it directly from pitch tracks: how long, how deep, how fast each oscillation is. <bookmark mark='f'/> Here is one drawn.", marks="cdef")
