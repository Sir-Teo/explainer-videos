from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Reharm(SoundScene):
    def construct(self):
        chapter(self, 7, r"Reharmonisation", r"How many ways can one melody be harmonised?")
        self.rule()
        self.table()
        self.hear()
        self.arrangers()

    # ------------------------------------------------------------------
    def rule(self):
        items = [
            (r"to reharmonise: \ keep the melody, \ change the chords under it", WHITE),
            (r"the one constraint: \ each melody note must be a chord tone or a tension of its new chord", WHITE),
            (r"secondary dominants: \ make each chord's predecessor its own V7 \ (Part 19)", WHITE),
            (r"tritone substitutes: \ replace those dominants a tritone away \ (Part 38)", TUNE),
            (r"Monochord does each, \ mechanically, \ to a phrase of ours", GREY_A),
        ]
        rows_scene(self, r"reharmonisation", items,
                   "To reharmonise is to keep a melody and change the chords under it. <bookmark mark='b'/> This toy retains melody pitches that it labels chord tones or permitted tensions. Reharmonization in practice can also use deliberate non-chord tones and other contextual constraints. <bookmark mark='c'/> One move is the secondary dominant of Part 19: make each chord's predecessor its own dominant seventh. <bookmark mark='d'/> Another is Part 38's tritone substitute: replace those dominants with the dominant a tritone away. <bookmark mark='e'/> Monochord does each, mechanically, to a phrase of ours.", marks="bcde")

    # ------------------------------------------------------------------
    def table(self):
        d = load("reharm")
        ph = d["phrase"]
        cols = VGroup()
        for i, (m, a, du) in enumerate(ph):
            col = VGroup(label(NN[m % 12], font_size=24, color=TUNE))
            for k, key in enumerate(("diatonic", "secondary", "tritone")):
                s = d["schemes"][key][i]
                changed = key != "diatonic" and s != d["schemes"]["diatonic"][i]
                col.add(label(sym(s), font_size=19, color=(EAR if changed else WHITE)))
            col.arrange(DOWN, buff=0.4)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.55).move_to(RIGHT * 0.8 + DOWN * 0.1)
        names = VGroup(label(r"melody", font_size=19, color=TUNE), label(r"diatonic", font_size=19, color=GREY_A),
                       label(r"secondary dominants", font_size=19, color=GREY_A), label(r"tritone substitutes", font_size=19, color=GREY_A))
        for n_, row_el in zip(names, cols[0]):
            n_.next_to(row_el, LEFT, buff=0.6).set_x(cols.get_left()[0] - 1.6)
        head = label(r"a phrase of ours, \ harmonised three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"pink: \ chords the second and third schemes changed", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here is a seven-note phrase of ours in C, harmonised three ways. <bookmark mark='a'/> Diatonically, each note "
            "gets the strongest chord of the key that contains it. <bookmark mark='b'/> With secondary dominants, chords "
            "before a change become the dominant of what follows, where the melody note fits. <bookmark mark='c'/> And with "
            "tritone substitutes, those dominants move a tritone away, and the bass begins to slide by semitones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names[0]), *[FadeIn(c[0]) for c in cols], FadeIn(cap))
            for mark, k in zip("abc", (1, 2, 3)):
                vo.wait_until(mark)
                self.play(FadeIn(names[k]), *[FadeIn(c[k]) for c in cols])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("reharm")
        c = clip("reharm.three")
        ph = d["phrase"]
        beat = 60.0 / d["bpm"]
        rows_ = VGroup()
        for key, col in (("diatonic", GREY_A), ("secondary", BLUE), ("tritone", EAR)):
            row = VGroup(*[VGroup(Rectangle(width=0.4 * du, height=0.6, stroke_color=col, stroke_width=1.5), label(sym(s), font_size=14, color=WHITE))
                           for (m, a, du), s in zip(ph, d["schemes"][key])])
            for cell in row:
                cell[1].move_to(cell[0])
            row.arrange(RIGHT, buff=0.04)
            rows_.add(VGroup(label(key, font_size=19, color=col), row).arrange(RIGHT, buff=0.4))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(UP * 0.2)
        with self.voiceover(
            "Hear the three, on an additive saxophone over piano and bass: the plain harmony, then the secondary dominants, "
            "then the tritone substitutes. The melody never changes; listen to how differently it reads. In the third, "
            "several melody notes become altered tensions of their chords, flat ninths and sharp fifths: the sharper sound "
            "of later jazz."
        ):
            self.play(FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"three harmonisations", kind="synthesized", detail=r"an additive saxophone over Part 7's piano and bass", corner=DL, tag_corner=DR)
            for r, key in zip(rows_, ("diatonic", "secondary", "tritone")):
                t0 = d["starts"][key]
                for (m, a, du), cell in zip(ph, r[1]):
                    pulse(snd, cell, t0 + a * beat, t0 + (a + du) * beat - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arrangers(self):
        items = [
            (r"reharmonisation is the arranger's and the pianist's art: \ a familiar tune made new", WHITE),
            (r"Bill Evans and later pianists reharmonised standards chorus by chorus", WHITE),
            (r"a reharmonisation can change a tune's mood, \ its sense of key, \ even its form", WHITE),
            (r"Part 41 orchestrates; \ Part 42 composes with these tools", TUNE),
            (r"chapter 8 builds a player that improvises through any changes", GREY_A),
        ]
        rows_scene(self, r"the art of it", items,
                   "Reharmonisation is the arranger's and the pianist's art: a familiar tune made new. <bookmark mark='b'/> "
                   "Bill Evans and the pianists after him reharmonised standards chorus by chorus. <bookmark mark='c'/> A "
                   "reharmonisation can change a tune's mood, its sense of key, even its form. <bookmark mark='d'/> Part 41 "
                   "orchestrates, and Part 42 composes, with these tools. <bookmark mark='e'/> Chapter eight builds a player "
                   "that improvises through any changes.", marks="bcde")
