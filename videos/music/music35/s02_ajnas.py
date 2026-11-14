from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Ajnas(SoundScene):
    def construct(self):
        chapter(self, 1, r"Ajnas: \ the building blocks", r"What is a maqam made of?")
        self.idea()
        self.hear()
        self.grid()
        self.tonics()
        self.names()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"a \textit{jins} \ (plural \textit{ajn\=as}): \ three or four notes, \ usually spanning a fourth", WHITE),
            (r"the Greek tetrachord, \ inherited and transformed: \ al-Kind\=\i, \ al-F\=ar\=ab\=\i, \ Ibn S\=\i n\=a", WHITE),
            (r"each jins has a flavour: \ Rast, \ Bayati, \ Hijaz, \ Saba ...", WHITE),
            (r"a maqam is ajnas joined: \ one on the tonic, \ another higher up", TUNE),
            (r"the steps are written here on the 24-step grid: \ a `quarter tone' is 50 cents", GREY_A),
        ]
        rows_scene(self, r"the jins", items,
                   "Arabic theory builds its modes from small pieces. <bookmark mark='b'/> A jins, plural ajnas, is a group of "
                   "three or four notes, usually spanning a fourth. <bookmark mark='c'/> It descends from the Greek tetrachord, "
                   "inherited and transformed by al-Kindi, al-Farabi and Ibn Sina. <bookmark mark='d'/> Each jins has its own "
                   "flavour and name: Rast, Bayati, Hijaz, Saba. <bookmark mark='e'/> A maqam joins them, one jins on the tonic "
                   "and another higher up. <bookmark mark='f'/> Here the steps are written on the twenty-four-step grid of modern "
                   "Arabic theory, a quarter tone being fifty cents; chapter four asks how real that grid is.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("ajnas")
        c = clip("ajnas.eight")
        names = d["names"]
        ruler = cents_ruler([d["ajnas"][n] for n in names], width=7.0, top=500, labels=names, row_gap=0.62, tick_h=0.3).move_to(RIGHT * 0.6 + DOWN * 0.2)
        steps = VGroup()
        for i, n in enumerate(names):
            a = d["ajnas"][n]
            st = r" \ ".join(str(int(b - x)) for x, b in zip(a, a[1:]))
            steps.add(label(st, font_size=16, color=GREY_A).next_to(ruler.rows[i][0], RIGHT, buff=0.3))
        head = label(r"eight ajnas from C: \ steps in cents", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are eight ajnas, each from C, each played up and down on the oud. Rast: whole tone, then two three-quarter "
            "tones. Bayati: three-quarter, three-quarter, whole. Sikah, three notes, starting on a half-flat. Hijaz: a "
            "semitone, a wide step of three semitones, a semitone. Saba, which stops short of the fourth. And three with only "
            "piano steps: Nahawand, Kurd and Ajam. Listen for the three-quarter tones, the steps the piano cannot make."
        ):
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(steps))
        with self.listen(c) as snd:
            window(snd, r"eight ajnas", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                end = d["starts"][names[i + 1]] - 0.4 if i < len(names) - 1 else c.duration
                pulse(snd, ruler.rows[i][3], d["starts"][n], end, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid(self):
        items = [
            (r"three sizes of step: \ semitone \ (about 100), \ three-quarter tone \ (about 150), \ whole tone \ (200)", WHITE),
            (r"and the augmented second of Hijaz \ (about 300)", WHITE),
            (r"the three-quarter tone is the signature: \ a `neutral' second, \ neither minor nor major", TUNE),
            (r"two of them make a neutral third: \ Rast's E half-flat", WHITE),
            (r"Part 12's scales had two step sizes; \ these have three or four", GREY_A),
        ]
        rows_scene(self, r"the steps", items,
                   "Look at the steps. <bookmark mark='b'/> There are three main sizes: a semitone, about one hundred cents; a "
                   "three-quarter tone, about one hundred and fifty; and a whole tone, two hundred. <bookmark mark='c'/> Hijaz "
                   "adds a wide augmented second, about three hundred. <bookmark mark='d'/> The three-quarter tone is the "
                   "signature of the system, a neutral second, neither minor nor major. <bookmark mark='e'/> Two of them make a "
                   "neutral third, Rast's E half-flat. <bookmark mark='f'/> Part 12's familiar scales had two step sizes; these "
                   "have three or four.", marks="cdef")

    # ------------------------------------------------------------------
    def tonics(self):
        d = load("tonics")
        c = clip("tonics.three")
        cells = VGroup(*[VGroup(label(rf"Bayati on {k}", font_size=26, color=TUNE), label(r"150, \ 150, \ 200", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2) for k in d["tonics"]]).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"one jins, \ three places", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"a jins is a shape, \ not a set of pitches: \ it can sit on many notes of a maqam", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "A jins is a shape, not a fixed set of pitches. Here is jins Bayati on D, then on G, then on A: the same steps, "
            "three-quarter, three-quarter, whole, at three heights. Maqamat place ajnas on different notes, and a modulation "
            "often means moving a jins to a new note, or swapping one jins for another on the same note."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Bayati on D, \ G, \ A", detail=r"an oud model", corner=DL, tag_corner=DR)
            ks = list(d["tonics"])
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def names(self):
        items = [
            (r"R\=ast: \ Persian for `straight', \ `right': \ the basic mode", WHITE),
            (r"\d{H}ij\=az: \ the region of western Arabia; \ Nah\=awand: \ a city in Iran", WHITE),
            (r"Kurd and `Ajam: \ the Kurds and the Persians; \ \d{S}ab\=a: \ the east wind", WHITE),
            (r"names record a history of travel between peoples and cities", TUNE),
            (r"Persian numbers survive in note names: \ \textit{chahargah}, \ the `fourth place'", GREY_A),
        ]
        rows_scene(self, r"what the names mean", items,
                   "The names tell a history. <bookmark mark='b'/> Rast is Persian for straight or right: the basic mode. <bookmark mark='c'/> Hijaz is the region of western Arabia, and Nahawand a city in Iran. <bookmark mark='d'/> Kurd and Ajam refer to the Kurds and the Persians, and Saba is the east wind. <bookmark mark='e'/> The names record centuries of travel between peoples and cities, <bookmark mark='f'/> and Persian numbers survive in note names such as chahargah, the fourth place.", marks="cdef")
