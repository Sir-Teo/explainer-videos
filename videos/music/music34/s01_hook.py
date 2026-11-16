from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.tihai()
        self.respect()
        self.plan()
        self.habits()

    # ------------------------------------------------------------------
    def tihai(self):
        d = load("hook")
        c = clip("hook.tihai")
        t = load("tala")["talas"]["Teentaal"]
        g1 = tala_grid(d["theka"], t["vibhags"], t["marks"], cell=0.6).move_to(UP * 1.4)
        second = d["theka"][:d["start"] - 1] + [""] * (16 - d["start"] + 1)
        for k, s0 in enumerate(d["starts"]):
            for i, b in enumerate(d["phrase"]):
                if s0 + i < 16:
                    second[s0 + i] = b
        g2 = tala_grid(second, t["vibhags"], t["marks"], cell=0.6).move_to(DOWN * 0.6)
        for k, s0 in enumerate(d["starts"]):
            for i in range(3):
                if s0 + i < 16:
                    g2.cells[s0 + i][0].set_fill(EAR, opacity=0.25)
        sam = VGroup(Rectangle(width=0.6, height=0.45, stroke_color=TUNE, stroke_width=3, fill_color=TUNE, fill_opacity=0.3), label(r"dha", font_size=17, color=WHITE))
        sam.next_to(g2, RIGHT, buff=0.25)
        saml = label(r"sam", font_size=16, color=TUNE).next_to(sam, UP, buff=0.1)
        cap = label(r"three times dha-ti-dha, \ two beats apart: \ the last stroke falls on beat 1 of the next cycle", font_size=20, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"Teentaal, \ then a tihai \ (our own)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Listen to a sixteen-beat cycle on the tabla, over the drone of a tanpura. Then, in the second cycle, the "
            "drummer breaks off and plays a short phrase three times, with gaps, so that its very last stroke falls on the "
            "first beat of the next cycle, the sam. In a concert, this is the moment musicians and audience arrive "
            "together, often with a nod or a shout. It is called a tihai, and it is arithmetic done in real time."
        ):
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), FadeIn(sam), FadeIn(saml), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Teentaal and a tihai", detail=r"modelled tabla and tanpura", corner=DL, tag_corner=DR)
            b = d["beat"]
            for i in range(16):
                pulse(snd, g1.cells[i][0], i * b, (i + 1) * b - 0.02, buff=0.03)
            for i in range(16):
                pulse(snd, g2.cells[i][0], (16 + i) * b, (17 + i) * b - 0.02, buff=0.03)
            pulse(snd, sam, d["sam"], d["sam"] + 1.2, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def respect(self):
        items = [
            (r"Hindustani \ (north Indian) \ and Carnatic \ (south Indian) \ classical music", WHITE),
            (r"two of the world's great systems of melody and rhythm, \ centuries old and alive", WHITE),
            (r"this part explains their structure; \ it is no substitute for listening to their masters", TUNE),
            (r"every sound here is our own model: \ a tanpura string, \ a tabla, \ a bowed tone", WHITE),
            (r"terms are given in their own languages, \ with their usual meanings", GREY_A),
        ]
        rows_scene(self, r"before we begin", items,
                   "A word before we begin. <bookmark mark='b'/> This part is about the classical music of north and south "
                   "India, Hindustani and Carnatic. <bookmark mark='c'/> They are two of the world's great systems of melody and "
                   "rhythm, centuries old and very much alive. <bookmark mark='d'/> The film explains their structure; it is no "
                   "substitute for listening to their masters, which every viewer should do. <bookmark mark='e'/> Every sound "
                   "here is our own model, a tanpura string, a tabla and a bowed tone, playing phrases written in the manner of "
                   "the ragas named. <bookmark mark='f'/> Terms are given in their own languages, with their usual meanings.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the drone: \ a tanpura and its buzzing bridge, \ modelled",
            r"swara and shruti: \ the notes, \ and the question of their tuning",
            r"raga: \ more than a scale: \ ascent, \ descent, \ phrases, \ ornaments",
            r"thaats and the seventy-two melakartas, \ generated",
            r"tala: \ cycles of beats, \ claps and waves",
            r"the tihai equation, \ solved; \ and how a performance unfolds",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The drone, and the tanpura's buzzing bridge, built as a model. <bookmark mark='b'/> The "
            "notes, swara, and the old question of their tuning, shruti. <bookmark mark='c'/> Raga, which is far more than a "
            "scale. <bookmark mark='d'/> The thaats and the seventy-two melakartas, generated. <bookmark mark='e'/> Tala, "
            "the cycles of beats. <bookmark mark='f'/> The tihai equation, solved, and how a performance unfolds."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def habits(self):
        items = [
            (r"find Sa in the drone first, \ and hear every note against it", WHITE),
            (r"in the alap, \ notice which notes are dwelt on, \ and how each is approached", WHITE),
            (r"once the drum enters, \ count the cycle: \ clap on sam, \ wave on khali", WHITE),
            (r"listen for the tihai coming: \ a phrase that starts to repeat", TUNE),
            (r"and listen to real performances: \ this film's models only point the way", GREY_A),
        ]
        rows_scene(self, r"how to listen", items,
                   "A few habits help when listening to this music. <bookmark mark='b'/> Find Sa in the drone first, and hear every note against it. <bookmark mark='c'/> In the slow opening, notice which notes the performer dwells on, and how each one is approached. <bookmark mark='d'/> Once the drum enters, count the cycle with your hands, the tala’s prescribed gesture on sam and a wave on khali; Rupak notably begins with a wave. <bookmark mark='e'/> Listen for a tihai coming: a phrase that begins to repeat. <bookmark mark='f'/> And listen to real performances: this film's models can only point the way.", marks="cdef")
