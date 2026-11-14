from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Form(SoundScene):
    def construct(self):
        chapter(self, 8, r"How a performance unfolds", r"Why does a concert start without a beat?")
        self.arc()
        self.alap()
        self.jhala()
        self.gat()
        self.vocal()
        self.length()

    # ------------------------------------------------------------------
    def arc(self):
        stages = [(r"\=al\=ap", r"no pulse, \ no drum: \ the raga revealed note by note", 0.30, BLUE),
                  (r"jo\d{r}", r"a pulse, \ still no drum", 0.17, "#A3E635"),
                  (r"jh\=al\=a", r"fast, \ with the drone strings struck between notes", 0.11, EAR),
                  (r"gat", r"a composition in a tala, \ with tabla, \ and improvisation", 0.42, TUNE)]
        bars = VGroup()
        x = -6.0
        for name, desc, w, col in stages:
            W = 12.0 * w
            r = Rectangle(width=W, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to([x + W / 2, 0.8, 0])
            bars.add(VGroup(r, label(rf"\textit{{{name}}}", font_size=22, color=BLACK).move_to(r), label(desc, font_size=16, color=GREY_A).next_to(r, DOWN, buff=0.3)))
            x += W
        for i, b in enumerate(bars):
            if i % 2:
                b[2].shift(DOWN * 0.55)
            b[2].scale_to_fit_width(min(b[2].width, 3.6))
        head = label(r"an instrumental performance in the Hindustani manner \ (typical proportions)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the order runs from no pulse to fast pulse: \ the raga first, \ then time", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A Hindustani instrumental performance has an arc. <bookmark mark='a'/> It opens with alap: no pulse and no "
            "drum, the raga revealed note by note, often for a long time. <bookmark mark='b'/> Then jor: a pulse appears, "
            "still without the drum. <bookmark mark='c'/> Then jhala: fast, with the drone strings struck between the "
            "melody notes. <bookmark mark='d'/> And finally the gat: a composition in a tala, with tabla, and improvisation "
            "around it, ending in tihais. The order is the point: first the raga, then time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            for mark, b in zip("abcd", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b))
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alap(self):
        items = [
            (r"the \=al\=ap begins around Sa, \ then works upward, \ a few notes at a time", WHITE),
            (r"each new note is introduced, \ dwelt on, \ connected to the raga's phrases", WHITE),
            (r"the vadi is reached with weight; \ upper Sa is a climax", WHITE),
            (r"it is improvised, \ yet strictly within the raga's grammar", TUNE),
            (r"Part 22's question: \ a grammar that generates, \ heard live", GREY_A),
        ]
        rows_scene(self, r"the alap", items,
                   "The alap has its own shape. <bookmark mark='b'/> It begins around Sa and works upward a few notes at a time. "
                   "<bookmark mark='c'/> Each new note is introduced, dwelt on, and joined to the raga's characteristic "
                   "phrases. <bookmark mark='d'/> The vadi is reached with weight, and the upper Sa is a climax. "
                   "<bookmark mark='e'/> It is improvised, yet strictly within the raga's grammar: <bookmark mark='f'/> Part "
                   "22's idea of a grammar that generates, heard live.", marks="cdef")

    # ------------------------------------------------------------------
    def gat(self):
        items = [
            (r"the gat: \ a fixed composition of a cycle or two, \ returned to again and again", WHITE),
            (r"between returns: \ improvised variations, \ faster runs \ (\textit{t\=ans}), \ tihais", WHITE),
            (r"the tabla accompanies, \ and also answers with its own solos", WHITE),
            (r"players trade phrases: \ \textit{sawal--jawab}, \ question and answer", TUNE),
            (r"the composition is the frame; \ the performance is mostly made in the moment", GREY_A),
        ]
        rows_scene(self, r"the gat", items,
                   "The gat holds the second half together. <bookmark mark='b'/> It is a fixed composition of a cycle or two, "
                   "returned to again and again, <bookmark mark='c'/> and between returns come improvised variations, fast runs "
                   "called tans, and tihais. <bookmark mark='d'/> The tabla accompanies, and answers with solos of its own; "
                   "<bookmark mark='e'/> the players trade phrases, sawal-jawab, question and answer. <bookmark mark='f'/> The "
                   "composition is the frame; most of the performance is made in the moment.", marks="cdef")

    # ------------------------------------------------------------------
    def vocal(self):
        items = [
            (r"vocal forms: \ \textit{dhrupad}, \ austere and old; \ \textit{khay\=al}, \ the main classical form today", WHITE),
            (r"lighter forms: \ \textit{\d{t}hum\.r\=\i}, \ \textit{ghazal}, \ \textit{bhajan}", WHITE),
            (r"Carnatic concerts centre on composed songs, \ \textit{k\d{r}tis}, \ with improvised sections around them", WHITE),
            (r"Tyagaraja, \ Dikshitar and Syama Sastri \ (around 1800): \ the composers of the Carnatic `trinity'", TUNE),
            (r"Part 40 turns to the song across traditions", GREY_A),
        ]
        rows_scene(self, r"songs and singers", items,
                   "The voice is at the centre of both traditions. <bookmark mark='b'/> Dhrupad is the old, austere vocal form; "
                   "khayal the main classical form today; <bookmark mark='c'/> and lighter forms, thumri, ghazal and bhajan, "
                   "border on popular music. <bookmark mark='d'/> Carnatic concerts centre on composed songs, kritis, with "
                   "improvised sections around them, <bookmark mark='e'/> many by the composers of around 1800 known as the "
                   "trinity: Tyagaraja, Muthuswami Dikshitar and Syama Sastri. <bookmark mark='f'/> Part 40 turns to the song "
                   "across traditions.", marks="cdef")

    # ------------------------------------------------------------------
    def jhala(self):
        d = load("jhala")
        c = clip("jhala.fast")
        notes = sargam(d["notes"], size=22, color=TUNE, buff=0.22).move_to(UP * 0.8)
        dots = VGroup(*[VGroup(*[Dot(radius=0.04, color=GREY_B) for _ in range(3)]).arrange(DOWN, buff=0.06).next_to(n, DOWN, buff=0.25) for n in notes])
        head = label(r"jh\=al\=a: \ a melody note, \ then the drone strings, \ faster and faster \ (ours)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"gold: \ the melody; \ grey: \ strokes on the high drone string between", font_size=20, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Jhala is the climax of the opening. After each melody note the player strikes the high drone strings, the "
            "chikari, several times, so the melody rides on a rapid rhythmic pulse, and the whole thing accelerates. Here is "
            "a short jhala of our own: one melody note, three drone strokes, speeding up."
        ):
            self.play(FadeIn(head), FadeIn(notes), FadeIn(dots), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"jh\=al\=a", kind="synthesized", detail=r"bowed tone, \ modelled string", corner=DL, tag_corner=DR)
            t = 0.0
            n = len(d["notes"])
            for i in range(n):
                u = d["unit0"] + (d["unit1"] - d["unit0"]) * i / (n - 1)
                pulse(snd, notes[i], t, t + u * 0.25, buff=0.04)
                for k in range(3):
                    pulse(snd, dots[i][k], t + u * (k + 1) / 4, t + u * (k + 1) / 4 + 0.06, buff=0.02)
                t += u
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def length(self):
        items = [
            (r"a single raga can be explored for an hour or more", WHITE),
            (r"concerts traditionally ran through the night, \ ragas following the hours", WHITE),
            (r"audiences respond aloud: \ appreciation at a fine phrase, \ shouts at a tihai's landing", WHITE),
            (r"recordings shortened performances to fit 78s, \ then LPs, \ then streaming", TUNE),
            (r"Part 60 looks at how media shape music's forms", GREY_A),
        ]
        rows_scene(self, r"time and the audience", items,
                   "Time works differently here. <bookmark mark='b'/> A single raga can be explored for an hour or more, <bookmark mark='c'/> and concerts traditionally ran through the night, the ragas following the hours. <bookmark mark='d'/> Audiences respond aloud, praising a fine phrase and shouting when a tihai lands. <bookmark mark='e'/> Recording shortened performances to fit the three-minute disc, then the long-playing record, then streaming. <bookmark mark='f'/> Part 60 looks at how media shape music's forms.", marks="cdef")
