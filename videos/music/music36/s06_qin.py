from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Qin(SoundScene):
    def construct(self):
        chapter(self, 5, r"The guqin", r"What is a scholar's instrument for?")
        self.instrument()
        self.hui()
        self.hear()
        self.opentuning()
        self.threesounds()
        self.tablature()
        self.repertory()

    # ------------------------------------------------------------------
    def instrument(self):
        items = [
            (r"the \textit{guqin}: \ a seven-string zither, \ played on the lap or a table, \ some 3,000 years of history", WHITE),
            (r"the instrument of the scholar: \ Confucius is said to have played it", WHITE),
            (r"quiet by design: \ for self-cultivation, \ not for an audience", WHITE),
            (r"three kinds of sound: \ open strings, \ stopped notes, \ and harmonics", TUNE),
            (r"Part 1's string, \ played with every one of its harmonics", GREY_A),
        ]
        rows_scene(self, r"the qin", items,
                   "From bronze to silk. <bookmark mark='b'/> The guqin is a seven-string zither, played on a table, with some three "
                   "thousand years of history, <bookmark mark='c'/> the instrument of the scholar; Confucius is said to have "
                   "played it. <bookmark mark='d'/> It is quiet by design, made for self-cultivation rather than for an audience. "
                   "<bookmark mark='e'/> It has three kinds of sound: open strings, stopped notes, and harmonics. "
                   "<bookmark mark='f'/> It is Part 1's string, played with all its harmonics.", marks="cdef")

    # ------------------------------------------------------------------
    def hui(self):
        d = load("qin")
        L = 11.0
        string = Line(LEFT * L / 2, RIGHT * L / 2, color=TUNE, stroke_width=3).move_to(UP * 0.6)
        studs = VGroup()
        for h, n in zip(d["hui"], d["hui_partials"]):
            num, den = (int(x) for x in h.split("/"))
            x = -L / 2 + L * num / den
            studs.add(VGroup(Dot([x, 0.6, 0], radius=0.08, color=WHITE), label(h, font_size=14, color=GREY_A).move_to([x, 1.0, 0]),
                             label(str(n), font_size=15, color=EAR).move_to([x, 0.2, 0])))
        legend = VGroup(label(r"position on the string", font_size=16, color=GREY_A), label(r"partial sounded when touched there", font_size=16, color=EAR)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(string, DOWN, buff=0.9).to_edge(LEFT, buff=0.8)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"13 \textit{hui}, \ inlaid studs, \ mark 1/8, \ 1/6, \ 1/5, \ 1/4, \ 1/3, \ 2/5, \ 1/2 ... \ of the string", WHITE),
            (r"touch lightly at a hui and the string sounds the harmonic with a node there", TUNE))]).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"the thirteen hui", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Along the qin's face run thirteen inlaid studs, the hui. <bookmark mark='a'/> They mark an eighth, a sixth, a "
            "fifth, a quarter, a third, two fifths and a half of the string's length, and the same from the other end. "
            "<bookmark mark='b'/> Touch the string lightly at a hui and pluck, and it sounds the harmonic that has a node "
            "there: the second partial at the half, the third at a third or two thirds, the fifth at any of the fifths. The "
            "studs are Part 1's harmonic nodes, inlaid in mother-of-pearl."
        ) as vo:
            self.play(FadeIn(head), Create(string), FadeIn(studs), FadeIn(legend))
            for mark, r in zip("ab", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("qin")
        c = clip("qin.harmonics")
        cells = VGroup(*[VGroup(label(r["hui"] if r["hui"] != "1" else r"open", font_size=24, color=TUNE if r["partial"] > 1 else WHITE),
                                label(rf"partial {r['partial']}", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15) for r in d["rows"]]).arrange(RIGHT, buff=0.7).move_to(UP * 0.4)
        head = label(r"one string: \ open, \ then harmonics at six hui", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is one string, open, then touched at a half, a third, a quarter, a fifth, a sixth and an eighth: the "
            "octave, the twelfth, two octaves, the major third above that, the fifth above that, and three octaves. Qin "
            "music uses these pure, bell-like harmonics as a whole register of its own."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"harmonics", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            for i in range(len(cells)):
                pulse(snd, cells[i], i * d["step"], (i + 1) * d["step"] - 0.05, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tablature(self):
        items = [
            (r"qin notation, \ \textit{jianzipu}: \ compound characters built from pieces of others", WHITE),
            (r"each says which string, \ which hui, \ which finger, \ and how to pluck or slide", WHITE),
            (r"it records actions, \ not pitches; \ rhythm is mostly left to the teacher", WHITE),
            (r"a tablature, \ like Part 10's lute tablature, \ but far richer in technique", TUNE),
            (r"modern players reconstruct old pieces from it: \ \textit{dapu}", GREY_A),
        ]
        rows_scene(self, r"a notation of gestures", items,
                   "The qin has its own notation. <bookmark mark='b'/> Jianzipu writes each sound as a compound character built "
                   "from pieces of others, <bookmark mark='c'/> saying which string, which hui, which finger, and how to pluck or "
                   "slide. <bookmark mark='d'/> It records actions, not pitches, and leaves most of the rhythm to the teacher. "
                   "<bookmark mark='e'/> It is a tablature, like the lute tablatures of Part 10, far richer in technique. "
                   "<bookmark mark='f'/> Modern players reconstruct old pieces from it, a practice called dapu.", marks="cdef")

    # ------------------------------------------------------------------
    def opentuning(self):
        d = load("openqin")
        c = clip("openqin.open")
        cells = VGroup(label(r"C", font_size=24, color=TUNE), label(r"D", font_size=24, color=TUNE), label(r"F", font_size=24, color=TUNE), label(r"G", font_size=24, color=TUNE), label(r"A", font_size=24, color=TUNE), label(r"c", font_size=24, color=BLUE), label(r"d", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"the qin's seven open strings", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'A common tuning for the seven strings is C, D, F, G, A, C, D: a pentatonic collection, here on F, spread over more than an octave. Players tune it by harmonics, matching a harmonic on one string to a harmonic on another, so the fifths and fourths come out pure. Listen to the open strings in order.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"open strings", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            ts = [i * d["unit"] for i in range(7)]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def threesounds(self):
        d = load("stopped")
        c = clip("stopped.three")
        cells = VGroup(label(r"open string", font_size=24, color=WHITE), label(r"stopped note", font_size=24, color=TUNE), label(r"harmonic", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"one pitch, \ three sounds", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The qin's three kinds of sound can give the same pitch. Here is one note as an open string, as a stopped note pressed on another string, and as a harmonic, standing in here as a pure, bell-like tone. Qin players call the harmonics the sound of heaven, the open strings the sound of earth, and the stopped notes the sound of humanity."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"open, \ stopped, \ harmonic", detail=r"plucked string and a pure tone", corner=DL, tag_corner=DR)
            ts = d["times"]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def repertory(self):
        items = [
            (r"thousands of qin pieces survive in tablature, \ from the 15th century on", WHITE),
            (r"\textit{Liu Shui}, \ `Flowing Water', \ travelled on the Voyager spacecraft in 1977", WHITE),
            (r"pieces often have titles and stories: \ a landscape, \ a poem, \ a friendship", WHITE),
            (r"the qin was inscribed on UNESCO's list of intangible heritage in 2003", TUNE),
            (r"a scholar's art: \ playing, \ calligraphy, \ painting and chess went together", GREY_A),
        ]
        rows_scene(self, r"the repertory", items,
                   "The qin has a great repertory. <bookmark mark='b'/> Thousands of pieces survive in tablature, from the fifteenth century on. <bookmark mark='c'/> One, Liu Shui, Flowing Water, was chosen for the golden record carried by the Voyager spacecraft in 1977. <bookmark mark='d'/> Pieces have titles and stories: a landscape, a poem, the friendship of a player and the one listener who understood him. <bookmark mark='e'/> The qin was recognised as intangible heritage by UNESCO in 2003. <bookmark mark='f'/> It was a scholar's art, practised alongside calligraphy, painting and the game of go.", marks="cdef")
