from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403
from explainer.music.monochord import orchestra as O

SHOW = ["flute", "clarinet", "saxophone", "trumpet p", "trumpet f", "violin"]


def profile_bars(name, w=3.6, h=1.3, col=TUNE, n=12):
    db = O.PROFILES[name][:n]
    g = VGroup()
    base = Line([0, 0, 0], [w, 0, 0], color=GREY_D)
    g.add(base)
    for k, v in enumerate(db):
        hh = h * max(0.0, 1 + v / 60.0)
        g.add(Rectangle(width=w / n * 0.7, height=max(hh, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([w * (k + 0.5) / n, hh / 2, 0]))
    return VGroup(label(name, font_size=17, color=col), g).arrange(DOWN, buff=0.12)


class Orchestra(SoundScene):
    def construct(self):
        chapter(self, 1, r"An orchestra from physical models", r"What is an instrument's sound made of?")
        self.history()
        self.spectra()
        self.same()
        self.which()
        self.tour()
        self.players()
        self.honest()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Haydn's orchestra \ (1760s): \ about thirty players, \ strings with oboes, \ horns, \ sometimes flutes and bassoons", WHITE),
            (r"Beethoven added trombones and piccolo; \ Berlioz, \ from 1830, \ wrote for ninety and more", WHITE),
            (r"Mahler and Strauss, \ around 1900: \ the largest regular orchestras, \ four or more of each wind", WHITE),
            (r"four families: \ woodwinds, \ brass, \ percussion, \ strings, \ each with its own physics \ (Parts 7--9)", TUNE),
            (r"Berlioz's \textit{Treatise on Instrumentation} \ (1844) \ made orchestration a subject", GREY_A),
        ]
        rows_scene(self, r"the orchestra", items,
                   "The orchestra grew. <bookmark mark='b'/> Haydn's, in the 1760s, had about thirty players: strings with "
                   "oboes and horns, sometimes flutes and bassoons. <bookmark mark='c'/> Beethoven added trombones and piccolo, "
                   "and Berlioz, from 1830, wrote for ninety players and more. <bookmark mark='d'/> Mahler and Strauss, around 1900, wrote for "
                   "the largest regular orchestras, four or more of each wind. <bookmark mark='e'/> It has four families, "
                   "woodwinds, brass, percussion and strings, each with its own physics, from Parts 7 to 9. "
                   "<bookmark mark='f'/> And Berlioz's Treatise on Instrumentation of 1844 made orchestration a subject.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def spectra(self):
        cols = [TUNE, BLUE, EAR, GREY_A, "#F59E0B", "#A3E635"]
        g = VGroup(*[profile_bars(n, col=c) for n, c in zip(SHOW, cols)]).arrange_in_grid(rows=2, cols=3, buff=(0.8, 0.6)).move_to(DOWN * 0.2)
        cap = label(r"bar heights: \ the first twelve harmonics, \ in decibels below the strongest \ (60 dB = nothing)", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"spectra measured on the series' physical models", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Our orchestra is built from the series' own instruments. <bookmark mark='a'/> Part 8's flute, clarinet, "
            "saxophone and trumpet models and Part 7's bowed string were each run once, and the strengths of their first "
            "twelve harmonics read off. <bookmark mark='b'/> The flute is nearly a pure tone with a little third harmonic. "
            "The clarinet's odd harmonics are strong and its even ones weak, as Part 8 explained for a cylinder closed at "
            "one end. The saxophone's cone gives all harmonics, falling steadily. The trumpet blown softly is dark, and blown "
            "hard is bright, a difference chapter three returns to. And the bowed string's harmonics fall slowly, with a "
            "gap at the tenth, because the bow sits a tenth of the way along the string, Part 7's Helmholtz motion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.copy().set_opacity(0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tour(self):
        d = load("tour")
        c = clip("tour.eight")
        names = [n for n, _ in d["tour"]]
        cells = VGroup(*[label(n.replace(" p", ""), font_size=20, color=WHITE) for n in names]).arrange_in_grid(rows=2, cols=4, buff=(0.8, 0.5)).move_to(UP * 0.3)
        cap = label(r"each plays the same phrase in a comfortable part of its range: \ additive, \ from the measured spectra", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "With those spectra, any instrument can play any note, by adding up its harmonics with an attack and, for the "
            "strings and flutes, a vibrato. Here is a tour: the same phrase on piccolo, flute, clarinet, saxophone, trumpet, "
            "horn, violin and cello, each in a comfortable part of its range."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"eight instruments", kind="synthesized", detail=r"additive, \ from measured spectra", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(d["starts"]):
                pulse(snd, cells[k], t0, t0 + 8 * beat, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def honest(self):
        items = [
            (r"what the additive orchestra keeps: \ each instrument's average spectrum, \ its attack, \ its vibrato", WHITE),
            (r"what it loses: \ how the spectrum changes with pitch and loudness, \ breath and bow noise, \ the room", WHITE),
            (r"real orchestration manuals rely on those losses: \ registers, \ dynamics, \ articulation", WHITE),
            (r"a model good enough to reason with, \ not to replace players", TUNE),
            (r"chapter 2: \ where each instrument can play", GREY_A),
        ]
        rows_scene(self, r"what the model keeps", items,
                   "Be clear about what this orchestra is. <bookmark mark='b'/> It keeps each instrument's average spectrum, its "
                   "attack and its vibrato. <bookmark mark='c'/> It loses how the spectrum changes with pitch and loudness, the "
                   "noise of breath and bow, and the room. <bookmark mark='d'/> Real orchestration manuals rely on exactly those "
                   "things: registers, dynamics, articulation. <bookmark mark='e'/> So this is a model good enough to reason "
                   "with, not to replace players. <bookmark mark='f'/> Chapter two asks where each instrument can play.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def players(self):
        items = [
            (r"winds must breathe: \ a phrase longer than a breath needs a rest or a second player", WHITE),
            (r"brass tire: \ high, \ loud passages need rests, \ and the embouchure has limits", WHITE),
            (r"strings change bow: \ a long note at forte needs several bows, \ felt as tiny pulses", WHITE),
            (r"idiomatic writing: \ what lies under the fingers sounds easy, \ and sounds better", TUNE),
            (r"our additive players never tire; \ real ones always do", GREY_A),
        ]
        rows_scene(self, r"writing for players", items,
                   "Orchestration is also writing for people. <bookmark mark='b'/> Wind players must breathe, so a phrase longer than a breath needs a rest or a second player. <bookmark mark='c'/> Brass players tire, so high, loud passages need rests. <bookmark mark='d'/> String players change bow, so a long loud note needs several bows, felt as tiny pulses. <bookmark mark='e'/> Writing that lies under the fingers sounds easy, and sounds better. <bookmark mark='f'/> Our additive players never tire; real ones always do.", marks="cdef")

    # ------------------------------------------------------------------
    def same(self):
        d = load("same")
        c = clip("same.eight")
        names = d["names"]
        cells = VGroup(*[label(n.replace(" p", ""), font_size=20, color=WHITE) for n in names]).arrange_in_grid(rows=2, cols=4, buff=(0.9, 0.5)).move_to(UP * 0.3)
        cap = label(r"same pitch, \ same level, \ same length: \ only the spectrum and the attack differ", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear the definition of timbre at work: one note, middle C, at the same level and length, on eight of our "
            "instruments in turn. Only the spectrum and the attack differ, and each is unmistakable."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"one note, \ eight instruments", kind="synthesized", detail=r"additive, \ from measured spectra", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(d["starts"]):
                pulse(snd, cells[k], t0, t0 + 1.2, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def which(self):
        d = load("which")
        c = clip("which.three")
        card = listen_card(r"Three notes, \ all middle C, \ all at the same level: \ a violin, \ a clarinet and a flute, \ in some order. \ "
                           r"Which is the clarinet: \ the first, \ second or third?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three notes, all middle C, all at the same level: a violin, a clarinet and a flute, in "
            "some order. Which is the clarinet, the first, the second or the third?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.8, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.85)
                         for t in (r"first", r"second", r"third")]).arrange(RIGHT, buff=1.0).move_to(UP * 1.2)
        self.play(FadeOut(card), FadeIn(boxes))
        names = d["names"]
        with self.listen(c) as snd:
            window(snd, r"three middle Cs", kind="synthesized", detail=r"additive, \ from measured spectra", corner=DL, tag_corner=DR)
            for k, n in enumerate(names):
                end = d["starts"][names[k + 1]] - 0.3 if k < 2 else c.duration
                pulse(snd, boxes[k], d["starts"][n], end, buff=0.08)
        def bars(lv, col):
            g = VGroup(Line([0, 0, 0], [2.4, 0, 0], color=GREY_D))
            for k, v in enumerate(lv):
                h = 1.3 * max(0.0, 1 + v / 50.0)
                g.add(Rectangle(width=0.26, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([0.4 * (k + 0.5), h / 2, 0]))
            return g
        specs = VGroup(*[VGroup(bars(d["levels"][n], EAR if n == "clarinet" else GREY_A), label(n, font_size=18, color=EAR if n == "clarinet" else GREY_A)).arrange(DOWN, buff=0.12)
                         .next_to(boxes[k], DOWN, buff=0.35) for k, n in enumerate(names)])
        cap = label(r"the first six harmonics of each: \ the clarinet's 2nd and 4th are nearly missing", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second. The violin came first, and the flute last. The clarinet gives itself away by its hollow sound: its "
            "bore, closed at the reed, favours the odd harmonics, so the third and fifth are strong while the second and "
            "fourth are weak, as its spectrum showed a moment ago. The flute is nearly a pure tone, and the violin's harmonics fall away "
            "smoothly. Timbre is identity, even on one note."
        ):
            self.play(boxes[1][0].animate.set_stroke(EAR, 4), FadeIn(specs), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
