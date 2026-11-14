from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Instruments(SoundScene):
    def construct(self):
        chapter(self, 9, r"The instruments", r"How do you play between the keys?")
        self.oud()
        self.qanun()
        self.tuning()
        self.levers()
        self.ney()
        self.neyhear()

    # ------------------------------------------------------------------
    def oud(self):
        items = [
            (r"the oud: \ a short-necked lute with no frets", WHITE),
            (r"the player's finger places every note: \ any pitch is available", WHITE),
            (r"its fretted ancestors are what al-F\=ar\=ab\=\i\ described, \ Zalzal's fret among them", WHITE),
            (r"the European lute descends from it: \ \textit{al-`\=ud}, \ `the wood'", TUNE),
            (r"this film's oud is a plucked-string model through Part 7's guitar body", GREY_A),
        ]
        rows_scene(self, r"the oud", items,
                   "The central instrument is the oud. <bookmark mark='b'/> It is a short-necked lute with no frets, "
                   "<bookmark mark='c'/> so the player's finger places every note, and any pitch is available. "
                   "<bookmark mark='d'/> Its fretted ancestors are what al-Farabi described, Zalzal's fret among them. "
                   "<bookmark mark='e'/> The European lute descends from it: the name comes from al-ud, the wood. "
                   "<bookmark mark='f'/> The oud in this film is a plucked-string model through Part 7's guitar body.", marks="cdef")

    # ------------------------------------------------------------------
    def qanun(self):
        items = [
            (r"the q\=an\=un: \ a plucked zither of about 26 triple courses", WHITE),
            (r"under each course, \ small levers, \ \textit{mand\=al}s, \ shorten the string by small steps", WHITE),
            (r"Arabic qanuns: \ often quarter-tone steps; \ Turkish: \ finer steps, \ near commas", WHITE),
            (r"the player flips levers mid-phrase to change maqam: \ modulation by hand", TUNE),
            (r"a fixed-pitch instrument made flexible, \ lever by lever", GREY_A),
        ]
        rows_scene(self, r"the qanun", items,
                   "The qanun solves the problem mechanically. <bookmark mark='b'/> It is a plucked zither of about twenty-six "
                   "triple courses of strings, <bookmark mark='c'/> and under each course small levers, mandals, shorten the "
                   "string by small steps. <bookmark mark='d'/> Arabic qanuns often have quarter-tone steps; Turkish ones finer "
                   "steps, close to commas. <bookmark mark='e'/> The player flips levers in the middle of a phrase to change "
                   "maqam: modulation by hand. <bookmark mark='f'/> A fixed-pitch instrument made flexible, lever by lever.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def ney(self):
        items = [
            (r"the ney: \ an end-blown reed flute, \ breathy and vocal; \ the Sufi instrument", WHITE),
            (r"pitch bent by the angle of the lips and partly covered holes", WHITE),
            (r"strings: \ kemen\c{c}e, \ violin; \ Persian: \ t\=ar, \ set\=ar, \ sant\=ur, \ kam\=anche", WHITE),
            (r"percussion: \ darbuka, \ riq \ (tambourine), \ daf \ (frame drum)", TUNE),
            (r"and above all the voice, \ which every instrument imitates", GREY_A),
        ]
        rows_scene(self, r"the rest of the ensemble", items,
                   "The rest of the ensemble. <bookmark mark='b'/> The ney is an end-blown reed flute, breathy and close to the "
                   "voice, the instrument of Sufi music, <bookmark mark='c'/> its pitch bent by the lips and partly covered holes. "
                   "<bookmark mark='d'/> Bowed strings include the kemençe and the violin; Persian music has the tar, setar, "
                   "santur and kamancheh. <bookmark mark='e'/> Percussion: the darbuka, the riq tambourine and the daf frame "
                   "drum. <bookmark mark='f'/> And above all the voice, which every instrument imitates.", marks="cdef")

    # ------------------------------------------------------------------
    def levers(self):
        d = load("mandal")
        c = clip("mandal.levers")
        cells = VGroup(*[VGroup(label(f"{s}", font_size=26, color=TUNE if s == 350 else WHITE), label(r"cents", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.1) for s in d["steps"]]).arrange(RIGHT, buff=1.0).move_to(UP * 0.4)
        head = label(r"a course lowered lever by lever \ (the oud model standing in)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"E, \ then a quarter-tone grid of steps down to E$\flat$: \ 350 is Rast's third", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Here is what the levers do, with our oud model standing in for one qanun course. C, then the third above it, "
            "lowered one step at a time: four hundred, three hundred and seventy-five, three hundred and fifty, three "
            "hundred and twenty-five, three hundred cents. A qanun player does this with a flick of the thumb, in the middle "
            "of a phrase."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"lever by lever", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i in range(len(d["steps"])):
                pulse(snd, cells[i], i * d["step_time"], (i + 1) * d["step_time"] - 0.1, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuning(self):
        items = [
            (r"five or six courses of paired strings", WHITE),
            (r"tuned mostly in fourths: \ for example C, \ F, \ A, \ D, \ G, \ C \ (one common Arabic tuning)", WHITE),
            (r"fourths put a whole jins under one hand position", WHITE),
            (r"the player can bend a note by sliding or by pressure", TUNE),
            (r"Part 7's strings, \ with the frets taken away", GREY_A),
        ]
        rows_scene(self, r"tuning the oud", items,
                   "The oud's tuning suits the ajnas. <bookmark mark='b'/> It has five or six courses of paired strings, <bookmark mark='c'/> tuned mostly in fourths, for example C, F, A, D, G, C in one common Arabic tuning. <bookmark mark='d'/> Fourths put a whole jins under one position of the hand, <bookmark mark='e'/> and with no frets the player can bend a note by sliding or pressing. <bookmark mark='f'/> Part 7's strings, with the frets taken away.", marks="cdef")

    # ------------------------------------------------------------------
    def neyhear(self):
        d = load("ney")
        c = clip("ney.bayati")
        cells = VGroup(*[label(f"{int(cc)}", font_size=24, color=TUNE) for cc in d["seq"]]).arrange(RIGHT, buff=0.5).move_to(UP * 0.4)
        head = label(r"a breathy, \ ney-like tone \ (synthesized): \ jins Bayati", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"four harmonics and filtered breath noise: \ a sketch of the ney's colour, \ not a model of the instrument", font_size=20, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "For the ney's colour, a sketch rather than a model: four harmonics with filtered breath noise, playing jins "
            "Bayati up and down. A real ney's tone comes from an air jet across the rim, the physics of Part 8, and its "
            "player bends every note."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"ney-like Bayati", kind="synthesized", detail=r"additive tone and noise", corner=DL, tag_corner=DR)
            for i in range(len(d["seq"])):
                pulse(snd, cells[i], i * 0.5, i * 0.5 + 0.45, buff=0.05)
        self.wait(0.3)
        self.clear_scene()
