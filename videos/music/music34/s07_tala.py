from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Tala(SoundScene):
    def construct(self):
        chapter(self, 6, r"Tala", r"How do you keep your place in a cycle of sixteen?")
        self.cycles()
        self.hear()
        self.carnatic()
        self.theka()
        self.adi()
        self.laya()

    # ------------------------------------------------------------------
    def cycles(self):
        items = [
            (r"a tala is a cycle of beats \ (\textit{m\=atr\=a}s), \ grouped into sections \ (\textit{vibh\=ag}s)", WHITE),
            (r"each section begins with a clap \ (\textit{t\=al\=\i}) \ or a wave of the hand \ (\textit{kh\=al\=\i})", WHITE),
            (r"beat 1 is \textit{sam}: \ the strongest point, \ where phrases resolve", TUNE),
            (r"the drum's basic pattern for a tala is its \textit{\d{t}hek\=a}, \ spoken as syllables \ (\textit{bols})", WHITE),
            (r"khali sections use open, \ ringing strokes less: \ you can hear where you are", GREY_A),
        ]
        rows_scene(self, r"cycles of beats", items,
                   "Now rhythm. <bookmark mark='b'/> A tala is a cycle of beats, matras, grouped into sections, vibhags. "
                   "<bookmark mark='c'/> Each section begins with a clap of the hands, tali, or a wave, khali. "
                   "<bookmark mark='d'/> Beat one is sam, the strongest point of the cycle, where phrases resolve. "
                   "<bookmark mark='e'/> The tabla's basic pattern for each tala is its theka, spoken and learned as syllables "
                   "called bols. <bookmark mark='f'/> In the khali section the drummer avoids the ringing bass strokes, so a "
                   "listener can hear where in the cycle the music is.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("tala")
        c = clip("tala.three")
        grids = VGroup()
        for name in ("Teentaal", "Jhaptaal", "Rupak"):
            t = d["talas"][name]
            g = tala_grid(t["theka"], t["vibhags"], t["marks"], cell=0.56, size=15)
            grids.add(VGroup(label(rf"{name}: \ {t['beats']} beats \ ({' + '.join(str(v) for v in t['vibhags'])})", font_size=19, color=TUNE), g).arrange(DOWN, buff=0.35))
        grids.arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        grids.scale_to_fit_height(min(grids.height, 6.2))
        with self.voiceover(
            "Three talas, each one cycle and the next sam. Teentaal, sixteen beats in four sections of four, the most common "
            "tala of Hindustani music; its third section is khali, played with dry strokes. Jhaptaal, ten beats, two plus "
            "three plus two plus three. And Rupak, seven beats, three plus two plus two, unusual in starting on a wave: its "
            "sam is khali. X marks the sam's clap, the numbers the other claps, zero the waves."
        ):
            self.play(FadeIn(grids))
        with self.listen(c) as snd:
            window(snd, r"Teentaal, \ Jhaptaal, \ Rupak", detail=r"modelled tabla", corner=DL, tag_corner=DR)
            b = d["beat"]
            for gi, name in enumerate(("Teentaal", "Jhaptaal", "Rupak")):
                n = d["talas"][name]["beats"]
                for i in range(n + 1):
                    cell = grids[gi][1].cells[i % n]
                    t0 = d["starts"][name] + i * b
                    pulse(snd, cell[0], t0, t0 + b - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def carnatic(self):
        items = [
            (r"Carnatic tala: \ the Sul\=adi system, \ built from three kinds of part", WHITE),
            (r"\textit{laghu}: \ a clap and finger counts \ (3, \ 4, \ 5, \ 7 or 9 beats); \ \textit{drutam}: \ a clap and a wave \ (2)", WHITE),
            (r"\textit{\=Adi t\=a\d{l}a}: \ a laghu of 4 and two drutams \ = \ 8 beats, \ the most common", TUNE),
            (r"7 tala shapes $\times$ 5 laghu sizes \ = \ 35 talas, \ multiplied again by subdivisions \ (\textit{nadai})", WHITE),
            (r"the hand gestures are part of the music: \ audiences keep tala along with the performers", GREY_A),
        ]
        rows_scene(self, r"tala in the south", items,
                   "Carnatic music organises tala differently. <bookmark mark='b'/> The Suladi system builds every tala from "
                   "parts: <bookmark mark='c'/> a laghu, a clap followed by finger counts, of three, four, five, seven or nine "
                   "beats; and a drutam, a clap and a wave, two beats. <bookmark mark='d'/> Adi tala, a laghu of four and two "
                   "drutams, eight beats in all, is the most common. <bookmark mark='e'/> Seven shapes times five laghu sizes "
                   "give thirty-five talas, multiplied again by how each beat is subdivided. <bookmark mark='f'/> And the "
                   "gestures are part of the music: audiences keep tala with their hands along with the performers.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def laya(self):
        items = [
            (r"\textit{laya}: \ tempo, \ from very slow \ (\textit{vilambit}) \ to very fast \ (\textit{drut})", WHITE),
            (r"in slow Ektaal a cycle of 12 beats can last a minute: \ each beat subdivided many times", WHITE),
            (r"performances often accelerate across a whole piece, \ slow to fast", WHITE),
            (r"Part 11's metre, \ but with cycles much longer than a Western bar", TUNE),
            (r"Part 37 compares timelines and cycles across the world", GREY_A),
        ]
        rows_scene(self, r"tempo", items,
                   "Tempo has its own vocabulary. <bookmark mark='b'/> Laya runs from vilambit, very slow, to drut, very fast. "
                   "<bookmark mark='c'/> In slow Ektaal a cycle of twelve beats can last close to a minute, each beat divided "
                   "many times. <bookmark mark='d'/> Performances often speed up across a whole piece. <bookmark mark='e'/> It is "
                   "Part 11's metre, with cycles far longer than a Western bar. <bookmark mark='f'/> Part 37 compares timelines "
                   "and cycles across the world.", marks="cdef")

    # ------------------------------------------------------------------
    def adi(self):
        d = load("adi")
        c = clip("adi.hands")
        sym = {"clap": r"clap", "finger": r"finger", "wave": r"wave"}
        cells = VGroup()
        for i, a in enumerate(d["acts"]):
            col = TUNE if a == "clap" else (GREY_A if a == "finger" else BLUE)
            cells.add(VGroup(Square(0.9, stroke_color=GREY_B, stroke_width=1.5), label(sym[a], font_size=17, color=col), label(str(i + 1), font_size=13, color=GREY_A)))
        for cc in cells:
            cc[1].move_to(cc[0])
            cc[2].next_to(cc[0], DOWN, buff=0.1)
        cells.arrange(RIGHT, buff=0.12).move_to(UP * 0.3)
        brace = VGroup(label(r"laghu \ (4)", font_size=19, color=TUNE).next_to(cells[:4], UP, buff=0.3),
                       label(r"drutam", font_size=19, color=BLUE).next_to(cells[4:6], UP, buff=0.3),
                       label(r"drutam", font_size=19, color=BLUE).next_to(cells[6:8], UP, buff=0.3))
        head = label(r"Adi tala, \ kept by hand", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is Adi tala as a Carnatic audience keeps it: a clap, then three counts on the fingers, little finger first, "
            "for the laghu of four; then a clap and a wave, twice, for the two drutams. Eight beats, twice round, and the "
            "clap of the next cycle. Try it with your own hands."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(brace))
        with self.listen(c) as snd:
            window(snd, r"Adi tala", kind="synthesized", detail=r"claps, \ counts and waves", corner=DL, tag_corner=DR)
            b = d["beat"]
            for i in range(17):
                pulse(snd, cells[i % 8][0], i * b, (i + 1) * b - 0.04, buff=0.04)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theka(self):
        items = [
            (r"the theka marks the tala; \ the tala exists without it", WHITE),
            (r"in a solo, \ the tabla player leaves the theka and improvises against the cycle", WHITE),
            (r"a melodic instrument often plays a repeating \textit{lahr\=a} \ to keep the cycle for the drummer", WHITE),
            (r"tala is a shared count in everyone's head; \ the sounds only point to it", TUNE),
            (r"Part 11: \ metre is something listeners infer, \ not something they hear directly", GREY_A),
        ]
        rows_scene(self, r"the tala is not the drum pattern", items,
                   "The tala is not the drum pattern. <bookmark mark='b'/> The theka marks the tala, but the tala exists without it. <bookmark mark='c'/> In a tabla solo the drummer leaves the theka entirely and improvises against the cycle, <bookmark mark='d'/> while a melodic instrument keeps a repeating melody, the lehra, so everyone knows where sam is. <bookmark mark='e'/> The tala is a count shared in everyone's head; the sounds only point to it, <bookmark mark='f'/> as Part 11 found for metre in general.", marks="cdef")
