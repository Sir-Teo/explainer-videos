from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.three()
        self.story()
        self.plan()
        self.toussaint()

    # ------------------------------------------------------------------
    def three(self):
        d = load("hook")
        c = clip("hook.three")
        cols = [TUNE, BLUE, EAR]
        neck = VGroup()
        for r, col in zip(d["rhythms"], cols):
            g = necklace(r["pattern"], radius=1.25, color=col)
            neck.add(VGroup(g, label(rf"{r['name']}: \ E({r['k']}, {r['n']})", font_size=22, color=col).next_to(g, DOWN, buff=0.35),
                            pattern_text(r["pattern"], size=20, color=GREY_A)).arrange(DOWN, buff=0.3))
        neck.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        head = label(r"three rhythms from three continents", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Three rhythms. The tresillo, three strokes in eight pulses, heard all over Cuban and Latin American music. The "
            "cinquillo, five in eight. And the bell pattern of West Africa, seven strokes in twelve pulses. Each is drawn as a "
            "necklace: the cycle of pulses round a circle, strokes as beads. Listen to all three."
        ):
            self.play(FadeIn(head), FadeIn(neck))
        with self.listen(c) as snd:
            window(snd, r"tresillo, \ cinquillo, \ bell", detail=r"Part 11's clave", corner=DL, tag_corner=DR)
            for r, g in zip(d["rhythms"], neck):
                cyc = 3 if r["n"] == 8 else 2
                t_on = d["starts"][r["name"]]
                pulse(snd, g, t_on, t_on + cyc * r["n"] * d["pulse"] + 0.6, buff=0.12)
                ons = [i for i, ch in enumerate(r["pattern"]) if ch == "x"]
                for cc in range(cyc):
                    for j, o in enumerate(ons):
                        t0 = d["starts"][r["name"]] + (cc * r["n"] + o) * d["pulse"]
                        pulse(snd, g[0].dots[j], t0, t0 + d["pulse"] * 0.9, buff=0.04)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"2003: \ Eric Bjorklund times the pulses of a neutron accelerator \ (the Spallation Neutron Source)", WHITE),
            (r"the problem: \ spread k pulses over n time slots as evenly as possible", WHITE),
            (r"his solution is Euclid's algorithm for the greatest common divisor, \ run on sequences", WHITE),
            (r"2005: \ Godfried Toussaint notices that it generates the world's traditional rhythms", TUNE),
            (r"the same mathematics makes scales: \ this part follows it into tiling, \ bells and temperaments", GREY_A),
        ]
        rows_scene(self, r"a timing problem", items,
                   "These rhythms have a strange connection to physics. <bookmark mark='b'/> In 2003 Eric Bjorklund, an "
                   "engineer, had to time the pulses of a neutron accelerator, the Spallation Neutron Source. "
                   "<bookmark mark='c'/> His problem: spread k pulses over n time slots as evenly as possible. "
                   "<bookmark mark='d'/> His solution turned out to be Euclid's ancient algorithm for the greatest common divisor, "
                   "run on sequences instead of numbers. <bookmark mark='e'/> Two years later the computer scientist Godfried "
                   "Toussaint noticed that the algorithm generates the traditional rhythms of Cuba, Ghana, Bulgaria, Persia and "
                   "Brazil. <bookmark mark='f'/> The same mathematics makes scales, and this part follows it further.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"Euclid's rhythms, \ and why they are the most even",
            r"one shape, \ two uses: \ the bell pattern is the major scale",
            r"stacks of fifths, \ continued fractions, \ and which scale sizes work",
            r"oddity, \ homometry, \ and canons that tile time",
            r"Sanskrit prosody and Fibonacci; \ bells rung in every order",
            r"temperaments as linear maps, \ and a scale without octaves",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Euclid's rhythms, and why they are the most even. <bookmark mark='b'/> The discovery that the "
            "bell pattern and the major scale are one shape. <bookmark mark='c'/> Stacks of fifths, continued fractions, and "
            "which sizes of scale work. <bookmark mark='d'/> Rhythmic oddity, rhythms with the same intervals, and canons that "
            "tile time. <bookmark mark='e'/> Sanskrit prosody's Fibonacci numbers, and bells rung in every possible order. "
            "<bookmark mark='f'/> Temperaments as linear maps, and a scale with no octaves at all."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toussaint(self):
        items = [
            (r"Godfried Toussaint \ (1944--2019), \ computational geometer at McGill", WHITE),
            (r"he compared the clave rhythms of the world as geometry: \ distances between necklaces", WHITE),
            (r"he built family trees of rhythms from those distances, \ as biologists build them for species", WHITE),
            (r"his question: \ why is the son clave so popular? \ his answer drew on evenness and other measures", TUNE),
            (r"\textit{The Geometry of Musical Rhythm} \ (2013): \ this part's main source", GREY_A),
        ]
        rows_scene(self, r"Toussaint and rhythm", items,
                   "A word about Toussaint. <bookmark mark='b'/> Godfried Toussaint, who died in 2019, was a computational geometer at McGill University. <bookmark mark='c'/> He compared the rhythms of the world as geometric objects, measuring distances between necklaces. <bookmark mark='d'/> From those distances he built family trees of rhythms, as biologists build them for species. <bookmark mark='e'/> He asked why the son clave is so popular, and answered with evenness and several other measures. <bookmark mark='f'/> His book The Geometry of Musical Rhythm is this part's main source.", marks="cdef")
