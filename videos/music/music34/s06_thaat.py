from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


def scale_cell(sc, w=1.1, h=0.22, col=GREY_B, on=TUNE):
    g = VGroup()
    for k in range(12):
        g.add(Rectangle(width=w / 12, height=h, stroke_width=0.5, stroke_color=DIM, fill_color=on if k in sc else BLACK, fill_opacity=0.95 if k in sc else 0.2).move_to([k * w / 12, 0, 0]))
    return g


class Thaat(SoundScene):
    def construct(self):
        chapter(self, 5, r"Thaats and melakartas", r"How many parent scales are there?", extra=((1660, r"Venkatamakhin"),))
        self.thaats()
        self.hear3()
        self.melas()
        self.names()
        self.misfits()

    # ------------------------------------------------------------------
    def thaats(self):
        d = load("thaat")
        cells = VGroup()
        named = {tuple(v): k for k, v in d["thaats"].items()}
        for sc in d["space"]:
            t = tuple(sc)
            nm = named.get(t)
            cell = VGroup(scale_cell(sc, on=TUNE if nm else GREY_B), label(nm or "", font_size=13, color=TUNE)).arrange(DOWN, buff=0.06)
            cells.add(cell)
        cells.arrange_in_grid(rows=4, cols=8, buff=(0.32, 0.28)).move_to(DOWN * 0.3)
        head = label(r"Bhatkhande's thaats: \ 10 of the 32 possible seven-note scales", font_size=25, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"Sa and Pa fixed; \ Re, \ Ga, \ Ma, \ Dha, \ Ni each in one of two forms: \ $2^5$ \ = \ 32", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In the early twentieth century the Hindustani scholar Vishnu Narayan Bhatkhande sorted the ragas of the north "
            "into ten families by their scales, the thaats. <bookmark mark='a'/> With Sa and Pa fixed, and each of the "
            "other five notes in one of two forms, there are two to the fifth, thirty-two possible scales; the program lists "
            "them all, each as twelve cells. <bookmark mark='b'/> Bhatkhande's ten are lit: Bilawal, the major scale; "
            "Kalyan, with raised Ma; Bhairavi, with every flattable note flat; and the more exotic Marwa, Purvi, Todi and "
            "Bhairav, with their lowered Re. Many ragas fit no thaat exactly, and the scheme is a teaching tool rather than a "
            "law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
            vo.wait_until("a")
            vo.wait_until("b")
            lit = VGroup(*[cells[i] for i, sc in enumerate(d["space"]) if tuple(sc) in named])
            self.play(Indicate(lit, color=WHITE, scale_factor=1.08))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def melas(self):
        d = load("thaat")
        cells = VGroup()
        inv = {v: k for k, v in d["thaat_melas"].items()}
        for n in range(1, 73):
            hot = n in inv
            cells.add(VGroup(Square(0.42, stroke_width=1, stroke_color=GREY_B, fill_color=TUNE if hot else BLACK, fill_opacity=0.8 if hot else 0.0),
                             label(str(n), font_size=13, color=BLACK if hot else GREY_A)))
        for c_ in cells:
            c_[1].move_to(c_[0])
        cells.arrange_in_grid(rows=6, cols=12, buff=0.08).move_to(LEFT * 1.6 + DOWN * 0.3)
        side = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (r"Venkatamakhin \ (17th century): \ every scale with Sa, \ Pa, \ one Ma, \ two of four Ri/Ga places, \ two of four Dha/Ni", WHITE),
            (r"2 Ma $\times$ 6 $\times$ 6 \ = \ 72 \ \textit{m\=e\d{l}akartas}", TUNE),
            (r"numbered in a fixed order: \ 29 is the major scale, \ 65 the Lydian", WHITE),
            (r"Bhatkhande's ten thaats are ten of them \ (gold)", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.4)).move_to(RIGHT * 4.6)
        head = label(r"the 72 melakartas, \ generated", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The south had done this more thoroughly two centuries earlier. <bookmark mark='a'/> The scholar Venkatamakhin, "
            "in the seventeenth century, counted every scale with Sa and Pa, one of two Mas, and Ri and Ga in two of the four "
            "places between Sa and Ma, Dha and Ni in two of the four above Pa. <bookmark mark='b'/> Two Mas, six ways for "
            "the lower pair, six for the upper: seventy-two melakartas, the parent scales of Carnatic music. "
            "<bookmark mark='c'/> They are numbered in a fixed order; the program generates them in it: number twenty-nine "
            "is the major scale, Dheerashankarabharanam, and sixty-five the Lydian, Mechakalyani. <bookmark mark='d'/> "
            "Bhatkhande's ten thaats are ten of the seventy-two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(side[0]))
            for mark, r in zip("bcd", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def names(self):
        items = [
            (r"each melakarta's name encodes its number: \ the \textit{ka\d{t}apay\=adi} system", WHITE),
            (r"consonants stand for digits; \ the first two syllables' digits, \ reversed, \ give the number", WHITE),
            (r"\textit{Dh\=\i ra\'sa\.nkar\=abhara\d{n}am}: \ dha \ = \ 9, \ ra \ = \ 2: \ 92 reversed, \ 29", TUNE),
            (r"a memory system, \ like Part 33's \textit{yam\=at\=ar\=aja}", WHITE),
            (r"from the 72 come thousands of ragas, \ each with its own rules", GREY_A),
        ]
        rows_scene(self, r"names that are numbers", items,
                   "The names hide a code. <bookmark mark='b'/> In the katapayadi system, consonants stand for digits, "
                   "<bookmark mark='c'/> and the digits of a melakarta's first two syllables, reversed, give its number: "
                   "<bookmark mark='d'/> in Dheerashankarabharanam, dha is nine and ra is two, so ninety-two reversed, "
                   "twenty-nine. <bookmark mark='e'/> It is a memory system, like Part 33's yamataraja. <bookmark mark='f'/> From "
                   "the seventy-two parent scales come thousands of ragas, each with its own rules.", marks="cdef")

    # ------------------------------------------------------------------
    def hear3(self):
        d = load("thaats3")
        c = clip("thaats3.three")
        cells = VGroup()
        for name, col in (("Bilawal", TUNE), ("Kalyan", BLUE), ("Bhairav", EAR)):
            cells.add(VGroup(label(name, font_size=26, color=col), sargam(d["phrases"][name], size=17, color=WHITE, buff=0.16)).arrange(DOWN, buff=0.25))
        cells.arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        head = label(r"one phrase, \ three thaats", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear what a thaat changes. One phrase of ours, the same shape each time, in three thaats: Bilawal, the major "
            "scale; Kalyan, with its raised Ma; and Bhairav, with lowered Re and Dha, a morning sound with an augmented second "
            "between Re and Ga."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Bilawal, \ Kalyan, \ Bhairav", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            ks = ["Bilawal", "Kalyan", "Bhairav"]
            for i, k in enumerate(ks):
                n = len(d["phrases"][k])
                for j in range(n):
                    t0 = d["starts"][k] + 0.2 + j * d["unit"]
                    pulse(snd, cells[i][1][j], t0, t0 + d["unit"] - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def misfits(self):
        items = [
            (r"some ragas use both forms of a note: \ Khamaj climbs with Ni and descends with komal ni", WHITE),
            (r"some fit no thaat at all, \ or two at once", WHITE),
            (r"many ragas share a thaat and differ in everything else", WHITE),
            (r"the thaat is a filing system for scales; \ the raga lives in the movement", TUNE),
            (r"Part 35's maqam has its own families, \ built from smaller pieces", GREY_A),
        ]
        rows_scene(self, r"what thaats leave out", items,
                   "The thaat system has gaps. <bookmark mark='b'/> Some ragas use both forms of a note: Khamaj climbs with Ni and descends with komal Ni. <bookmark mark='c'/> Some fit no thaat at all, or two at once. <bookmark mark='d'/> And many ragas share a thaat but differ in everything else. <bookmark mark='e'/> The thaat is a filing system for scales; the raga lives in the movement. <bookmark mark='f'/> Part 35's maqam builds its families differently, from smaller pieces.", marks="cdef")
