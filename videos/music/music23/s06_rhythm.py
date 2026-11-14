from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403

GLYPH = {1: r"short", 2: r"long", 3: r"long+"}


class Rhythm(SoundScene):
    def construct(self):
        chapter(self, 5, r"The rhythmic modes", r"How do you write down long and short?", extra=((1250, r"Johannes de Garlandia"),))
        self.feet()
        self.six()
        self.ligatures()

    # ------------------------------------------------------------------
    def feet(self):
        items = [
            (r"the answer of Notre Dame: \ a few fixed patterns of long and short, \ repeated", WHITE),
            (r"a long is worth two or three breves; \ a breve one or two: \ the unit is a group of three, \ a `perfection'", WHITE),
            (r"six patterns, \ named after the feet of Latin poetry: \ trochee, \ iamb, \ dactyl, \ anapaest, \ spondee, \ tribrach", WHITE),
            (r"described by Johannes de Garlandia, \ about 1250, \ after the music already used them", GREY_A),
            (r"rhythm as a choice from a menu, \ not a sequence of independent lengths", TUNE),
        ]
        rows_scene(self, r"a menu of rhythms", items,
                   "The answer of the Notre Dame singers was not to write every length, but to choose from a menu. "
                   "<bookmark mark='b'/> A piece, or a passage, moves in one fixed pattern of long and short notes, "
                   "repeated, and everyone knows which. The short note is the breve; a long is worth two breves or three; "
                   "and the unit of the pattern is a group of three breves, which they called a perfection. "
                   "<bookmark mark='c'/> There were six patterns, and theorists named them after the feet of Latin "
                   "poetry: trochee, iamb, dactyl, anapaest, spondee and tribrach. <bookmark mark='d'/> They are "
                   "described by Johannes de Garlandia around 1250, decades after the music that used them. "
                   "<bookmark mark='e'/> Rhythm, for these singers, was a choice from a short menu, not a string of "
                   "independent lengths.")

    # ------------------------------------------------------------------
    def six(self):
        d = load("rhythm")
        c = clip("rhythm.modes")
        rows_ = VGroup()
        rolls = []
        for m in range(1, 7):
            info = d["modes"][str(m)]
            notes = info["notes"]
            g = mroll(notes, width=7.2, height=0.5, lo=60, hi=71, total=27.0, bar_h=0.12)
            pat = " ".join({1: "B", 2: "L", 3: r"L."}[x] for x in info["pattern"])
            t = label(rf"{m}. \ {info['name']}: \ {pat}", font_size=20, color=TUNE if m % 2 else BLUE)
            t.next_to(g, LEFT, buff=0.4)
            rows_.add(VGroup(t, g))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.22, aligned_edge=RIGHT).move_to(DOWN * 0.15 + RIGHT * 0.9)
        key = label(r"L: \ long \ (two breves); \ L.: \ perfect long \ (three); \ B: \ breve", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.3)
        head = label(r"one line in each of the six modes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the six, each applied to the same rising and falling line. The first mode is long, short; the "
            "second short, long; the third a perfect long and two breves, the second of them doubled; the fourth the "
            "third reversed; the fifth all perfect longs, the slow pattern the chant itself was given; and the sixth all "
            "breves. Listen to each one, and notice that the first mode is the one you hear most: it was by far the most "
            "common."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"the six rhythmic modes", detail=r"one synthetic voice", kind="synthesized", corner=UL, tag_corner=UR)
            for m in range(1, 7):
                st = d["starts"][str(m)]
                flash(snd, rolls[m - 1].notes, [st + n[1] * d["unit"] for n in d["modes"][str(m)]["notes"]], hot=WHITE, base=TUNE)
                end = d["starts"][str(m + 1)] - 0.4 if m < 6 else c.duration
                pulse(snd, rows_[m - 1][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ligatures(self):
        d = load("rhythm")
        rows_ = VGroup()
        GROUPS = {1: [3, 2, 2, 2], 2: [2, 2, 2, 3], 3: [1, 3, 3, 3], 5: [3, 3, 3], 6: [4, 3, 3]}
        for m, groups in GROUPS.items():
            boxes = VGroup()
            for gsz in groups:
                box = VGroup(*[Square(side_length=0.22, stroke_width=0, fill_color=TUNE if m % 2 else BLUE, fill_opacity=0.9) for _ in range(gsz)]).arrange(RIGHT, buff=0.0)
                frame = SurroundingRectangle(box, buff=0.05, color=GREY_B, stroke_width=1.2)
                boxes.add(VGroup(box, frame))
            boxes.arrange(RIGHT, buff=0.35)
            t = label(rf"{' '.join(str(x) for x in groups)} \ $\to$ \ mode {m}", font_size=21, color=WHITE).next_to(boxes, RIGHT, buff=0.5)
            rows_.add(VGroup(boxes, t))
        rows_.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 1.0 + UP * 0.3)
        cap = VGroup(label(r"the notes were bound into groups, \ ligatures; \ the pattern of group sizes says the mode", font_size=21, color=GREY_A),
                     label(r"a reader parses the page: \ the same shapes mean different lengths in different patterns", font_size=21, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        head = label(r"reading the mode from the page", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How did a singer know which mode to sing? Not from the shape of any one note. <bookmark mark='a'/> Notes "
            "were written bound together in groups called ligatures, and the pattern of group sizes signalled the mode: "
            "a group of three followed by twos meant the first mode; twos ending in a three, the second; a single note "
            "then threes, the third; threes throughout, the fifth; a four then threes, the sixth. <bookmark mark='b'/> "
            "So reading this music is parsing: the same sign means a long in one context and a short in another, and "
            "only the pattern decides. The film's program does exactly that, reading a row of ligature sizes and naming "
            "the mode, or refusing when no pattern fits. It is the first rhythm written in the music of the Western "
            "church, and it was written as a grammar."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.2), FadeIn(cap[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
