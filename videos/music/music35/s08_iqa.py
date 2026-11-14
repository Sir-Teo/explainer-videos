from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


def iqa_row(strokes, cell=0.55):
    g = VGroup()
    g.cells = []
    for i, s in enumerate(strokes):
        box = Square(cell, stroke_color=GREY_B, stroke_width=1.2)
        txt = label({"dum": "D", "tek": "T", "ka": "k"}.get(s, ""), font_size=18, color=TUNE if s == "dum" else (BLUE if s else GREY_B))
        cg = VGroup(box, txt)
        txt.move_to(box)
        g.add(cg)
        g.cells.append(cg)
    g.arrange(RIGHT, buff=0.05)
    return g


class Iqa(SoundScene):
    def construct(self):
        chapter(self, 7, r"Rhythmic cycles", r"How many beats in a Turkish song?")
        self.idea()
        self.quiz()
        self.baladi()
        self.usul()
        self.syllables()
        self.dance()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"\textit{\=iq\=a`} \ (Arabic), \ \textit{usul} \ (Turkish): \ a rhythmic cycle of strong and weak strokes", WHITE),
            (r"\textit{dum}: \ the low stroke at the centre of the drum; \ \textit{tek}: \ the high stroke at the rim", WHITE),
            (r"maqsum \ (8): \ D T -- T D -- T --, \ the commonest Arabic cycle", WHITE),
            (r"cycles of 9 \ (aksak), \ 10 \ (sam\=a`\=\i\ thaq\=\i l) \ and far longer", TUNE),
            (r"the drum keeps the cycle; \ the melody moves freely over it", GREY_A),
        ]
        rows_scene(self, r"dum and tek", items,
                   "Rhythm in this music is organised in cycles too. <bookmark mark='b'/> The Arabic iqa, the Turkish usul, is a "
                   "cycle of strong and weak strokes. <bookmark mark='c'/> Dum is the low stroke at the centre of the drum, tek "
                   "the high stroke at the rim. <bookmark mark='d'/> Maqsum, eight beats, dum tek, tek dum, tek, is the commonest "
                   "Arabic cycle. <bookmark mark='e'/> There are cycles of nine, aksak, of ten, samai thaqil, and far longer. "
                   "<bookmark mark='f'/> The drum keeps the cycle; the melody moves freely over it.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("iqa")
        c = clip("iqa.quiz")
        card = listen_card(r"Three cycles on the darbuka, \ each three times round. \ One has 8 beats, \ one 9, \ one 10. \ "
                           r"Which has ten, \ A, \ B or C? \ Count the beats between the deep strokes that start each cycle.", width=10.4)
        with self.voiceover(
            "A question for your ears. Three cycles on the darbuka, each three times round. One has eight beats, one nine, "
            "one ten. Which has ten? Count from each deep stroke that begins a cycle."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        rows_ = VGroup()
        for k, name in zip("ABC", d["order"]):
            rows_.add(VGroup(label(k, font_size=34, color=GREY_A), iqa_row(d["iqaat"][name]["strokes"])).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.3)
        for r in rows_:
            r[1].set_opacity(0.15)
        self.play(FadeOut(card), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 9's membrane", corner=DL, tag_corner=DR)
            b = d["beat"]
            for gi, (k, name) in enumerate(zip("ABC", d["order"])):
                n = len(d["iqaat"][name]["strokes"])
                for i in range(3 * n):
                    t0 = d["starts"][k] + i * b
                    pulse(snd, rows_[gi][1].cells[i % n][0], t0, t0 + b - 0.02, buff=0.02)
        ans = label(r"A: \ maqsum, \ 8; \ \ B: \ sam\=a`\=\i\ thaq\=\i l, \ 10; \ \ C: \ aksak, \ 9", font_size=22, color=TUNE).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "B has ten: samai thaqil, a slow, stately cycle used for an instrumental form of the same name. A was maqsum, "
            "eight; C was aksak, nine, the limping cycle of Turkish music, two, two, two, three."
        ):
            self.play(*[r[1].animate.set_opacity(1.0) for r in rows_], FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def usul(self):
        items = [
            (r"Ottoman usul reach very long cycles: \ 28, \ 32, \ even 120 beats", WHITE),
            (r"the long cycles carry slow vocal forms; \ the short ones, \ dances and songs", WHITE),
            (r"the cycle shapes the melody: \ phrases begin and end with the strong strokes", WHITE),
            (r"Part 34's tala, \ Part 33's timelines, \ and these: \ cycles everywhere", TUNE),
            (r"Part 37 compares them across the world", GREY_A),
        ]
        rows_scene(self, r"long cycles", items,
                   "The cycles can be very long. <bookmark mark='b'/> Ottoman usul reach twenty-eight, thirty-two, even one hundred "
                   "and twenty beats. <bookmark mark='c'/> The long cycles carry slow vocal forms, the short ones dances and songs. "
                   "<bookmark mark='d'/> And the cycle shapes the melody: phrases begin and end with its strong strokes. "
                   "<bookmark mark='e'/> Part 34's tala, Part 33's timelines, and these: cycles everywhere. <bookmark mark='f'/> "
                   "Part 37 compares them across the world.", marks="cdef")

    # ------------------------------------------------------------------
    def baladi(self):
        d = load("baladi")
        c = clip("baladi.two")
        rows_ = VGroup(*[VGroup(label(k, font_size=24, color=TUNE), iqa_row(d["strokes"][k])).arrange(RIGHT, buff=0.5) for k in ("maqsum", "baladi")]).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.3)
        cap = label(r"one stroke apart: \ the second beat is tek in maqsum, \ dum in baladi", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"maqsum and baladi", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Two cycles of eight can differ by a single stroke. Maqsum's second beat is tek, a light stroke; baladi's is dum, "
            "a heavy one, which gives it a weightier, earthier feel, the rhythm of much popular and folk music. Listen to "
            "both, three cycles each."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"maqsum, \ baladi", detail=r"Part 9's membrane", corner=DL, tag_corner=DR)
            b = d["beat"]
            for gi, k in enumerate(("maqsum", "baladi")):
                for i in range(24):
                    t0 = d["starts"][k] + i * b
                    pulse(snd, rows_[gi][1].cells[i % 8][0], t0, t0 + b - 0.02, buff=0.02)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dance(self):
        items = [
            (r"many cycles belong to dances: \ the \textit{dabke} line dance of the Levant, \ \textit{raqs sharq\=\i}", WHITE),
            (r"the darbuka player follows and leads the dancer", WHITE),
            (r"the riq keeps the cycle with jingles; \ the daf marks the strong strokes", WHITE),
            (r"the same cycle can be played plainly or filled with rolls and ornaments", TUNE),
            (r"Part 37: \ timelines as the backbone of dance music worldwide", GREY_A),
        ]
        rows_scene(self, r"rhythm and dance", items,
                   "Many of these cycles belong to dances. <bookmark mark='b'/> The dabke, a line dance of the Levant, and raqs sharqi each have their rhythms, <bookmark mark='c'/> and the darbuka player both follows and leads the dancer. <bookmark mark='d'/> The riq keeps the cycle with its jingles, the daf marks the strong strokes, <bookmark mark='e'/> and the same cycle can be played plainly or filled with rolls and ornaments. <bookmark mark='f'/> Part 37 hears timelines as the backbone of dance music worldwide.", marks="cdef")

    # ------------------------------------------------------------------
    def syllables(self):
        items = [
            (r"students learn cycles by speaking them: \ dum, \ tek, \ ka", WHITE),
            (r"teachers clap the strong strokes and tap the weak ones", WHITE),
            (r"Turkish usul are counted with `d\"um' and `tek' on the knees", WHITE),
            (r"Part 34's bols, \ in another language", TUNE),
            (r"rhythm you can say is rhythm you can remember", GREY_A),
        ]
        rows_scene(self, r"speaking the cycles", items,
                   "These cycles are spoken before they are played. <bookmark mark='b'/> Students learn them as syllables, dum, tek, ka; <bookmark mark='c'/> teachers clap the strong strokes and tap the weak ones; <bookmark mark='d'/> Turkish students beat usul on their knees, saying düm and tek. <bookmark mark='e'/> They are Part 34's bols in another language. <bookmark mark='f'/> Rhythm you can say is rhythm you can remember.", marks="cdef")
