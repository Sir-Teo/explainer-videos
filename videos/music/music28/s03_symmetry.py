from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403
from videos.music.music28.s02_wholetone import clock


class Symmetry(SoundScene):
    def construct(self):
        chapter(self, 2, r"Every symmetric scale", r"How many scales map onto themselves?")
        self.shapes()
        self.symmetric()
        self.heard()
        self.why()
        self.hexatonic()
        self.modes()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("census")
        bs = d["by_size"]
        ks = list(range(0, 13))
        bars = columns([bs[str(k)] for k in ks], [str(k) for k in ks], width=9.0, height=2.8, color=GREY_B, fmt="{:.0f}", font_size=17)
        bars.move_to(DOWN * 0.4)
        t = label(rf"every set of pitch classes, \ up to transposition: \ {d['classes']} shapes, \ by number of notes", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.4)
        cap = label(r"$2^{12} = 4096$ sets; \ Burnside's lemma \ (Part 12) \ counts the shapes without listing them", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How many scales could a composer choose from? Any set of the twelve pitch classes is a candidate: two to the "
            "twelfth, four thousand and ninety-six of them. Count sets that differ only by transposition as one shape, and "
            f"there are {say(d['classes'])}, which Part 12 counted with Burnside's lemma. Most have five, six or seven notes. "
            "Now ask of each shape: does some transposition, other than by an octave, map it onto itself?"
        ):
            self.play(FadeIn(t), FadeIn(bars), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symmetric(self):
        d = load("census")
        sym = d["symmetric"]
        cells = VGroup()
        for s in sym:
            mode = s["mode"]
            col = TUNE if mode else GREY_A
            g = clock(s["pcs"], radius=0.48, color=col, labels=False)
            tag = label(rf"mode {mode}" if mode else rf"{len(s['pcs'])} notes", font_size=16, color=col)
            sub = label(rf"{s['period']} transp.", font_size=14, color=GREY_B)
            cells.add(VGroup(g, tag, sub).arrange(DOWN, buff=0.12))
        cells.arrange_in_grid(rows=3, cols=5, buff=(0.45, 0.25)).move_to(DOWN * 0.25)
        head = label(rf"the {d['n_symmetric']} shapes with limited transposition \ (empty and full sets left out)", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        small = [i for i, s in enumerate(sym) if not s["mode"]]
        big = [i for i, s in enumerate(sym) if s["mode"]]
        with self.voiceover(
            f"Only {say(d['n_symmetric'])} of the {say(d['classes'])} shapes do, leaving out the empty set and all twelve notes. <bookmark mark='a'/> The small ones are familiar chords: the tritone, the augmented triad, the diminished seventh, and a few six-note sets. <bookmark mark='b'/> The highlighted ones are Messiaen’s selected seven scales, rather than all sets above a unique size threshold; these are the scales that Olivier Messiaen listed in 1944 as his modes of limited transposition: the whole-tone scale is his first mode, the octatonic his second. Each label gives how many different transpositions the shape has: two, three, four or six, never twelve."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cells[i]) for i in small], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(cells[i]) for i in big], lag_ratio=0.12), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = text_rows([
            (r"a set maps onto itself under a transposition by $t$ \ $\Rightarrow$ \ also by $2t$, \ $3t$, \ ...", WHITE),
            (r"so it repeats every $d$ semitones, \ $d$ = the greatest common divisor of $t$ and 12: \ 1, \ 2, \ 3, \ 4 or 6", WHITE),
            (r"the scale is built from one pattern of $d$ semitones, \ copied $12/d$ times round the octave", WHITE),
            (r"whole-tone: \ the pattern \{0\} every 2; \ octatonic: \ \{0, 1\} every 3; \ mode 3: \ \{0, 2, 3\} every 4", TUNE),
            (r"counted this way, \ every symmetric shape is checked: \ none is missed", GREY_A),
        ], font_size=24)
        head = label(r"why so few: \ a short proof", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why so few? A short proof. <bookmark mark='a'/> If transposing by t semitones maps a set onto itself, so does "
            "transposing by two t, three t, and so on. <bookmark mark='b'/> So the set also maps onto itself under the "
            "smallest of those steps, d, the greatest common divisor of t and twelve, which must be one, two, three, four "
            "or six. <bookmark mark='c'/> The scale is then one pattern of d semitones copied twelve over d times round the "
            "octave. <bookmark mark='d'/> The whole-tone scale is a single note every two semitones; the octatonic is a "
            "half step, the pair zero and one, every three; Messiaen's third mode the pattern zero, two, three every four. "
            "<bookmark mark='e'/> The program checks that every one of the fifteen shapes is built this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        items = [
            (r"Olivier Messiaen, \ \textit{Technique of my Musical Language} \ (1944)", WHITE),
            (r"the modes cannot be transposed more than a few times without repeating: \ their `charm of impossibilities'", WHITE),
            (r"he heard them as colours: \ he had a form of synaesthesia, \ by his own account", WHITE),
            (r"modes 2 and 3 everywhere in his music, \ from the 1930s to the end of his life", TUNE),
            (r"a compositional use of transpositional symmetry", GREY_A),
        ]
        rows_scene(self, r"Messiaen's modes", items,
                   "Messiaen arrived at them by ear. <bookmark mark='b'/> He set them out in his Technique of my Musical "
                   "Language, of 1944, <bookmark mark='c'/> and called their symmetry a charm of impossibilities: they "
                   "cannot be transposed more than a few times without coming back to themselves. <bookmark mark='d'/> He "
                   "heard them as colours; by his own account he had a form of synaesthesia. <bookmark mark='e'/> The "
                   "second and third modes run through his music from the 1930s to the end of his life. "
                   "<bookmark mark='f'/> It is a small theorem, used by a composer; this film does not establish priority for a mathematical discovery.", marks="cdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("modes")
        c = clip("modes.three")
        keys = ["m1", "m2", "m3"]
        cols = VGroup()
        rolls = []
        for i, k in enumerate(("1", "2", "3")):
            ln = d["lines"][k]
            cl = clock([int(n[0]) - 60 for n in ln[:-1]], radius=0.9, color=TUNE, labels=False)
            r = mroll(ln, width=3.2, height=1.4, lo=58, hi=74, color=TUNE, bar_h=0.1)
            rolls.append(r)
            name = label([r"mode 1: \ whole-tone", r"mode 2: \ octatonic", r"mode 3: \ nine notes"][i], font_size=20, color=GREY_A)
            cols.add(VGroup(name, cl, r).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.8).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here are Messiaen's first three modes, each rising from C: the whole-tone scale, with steps of two; the "
            "octatonic, alternating one and two; and the third mode, nine notes in the pattern two, one, one, repeated three "
            "times. Each has a colour that does not change when it is transposed by its own period."
        ):
            self.play(FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"modes 1, \ 2 and 3", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                st = d["starts"][k]
                flash(snd, rolls[i].notes, [st + n[1] * d["unit"] for n in d["lines"][str(i + 1)]], hot=WHITE, base=TUNE)
                end = d["starts"][keys[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cols[i][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hexatonic(self):
        items = [
            (r"the hexatonic scale \{0, 3, 4, 7, 8, 11\}: \ half step, \ minor third, \ repeated", WHITE),
            (r"it holds three major and three minor triads, \ a major third apart", WHITE),
            (r"Richard Cohn: \ `hexatonic poles', \ C major to A$\flat$ minor, \ the uncanny in Wagner and in film", WHITE),
            (r"symmetric sets give chords that are close in notes and far in keys", TUNE),
            (r"Part 32 maps this closeness as geometry", GREY_A),
        ]
        rows_scene(self, r"the six-note symmetric sets", items,
                   "One of the smaller symmetric sets has its own story. <bookmark mark='b'/> The hexatonic scale alternates a half step and a minor third: zero, three, four, seven, eight, eleven, a transposition of the canonical shape. <bookmark mark='c'/> It holds three major and three minor triads, a major third apart. <bookmark mark='d'/> The theorist Richard Cohn calls the move from C major to A flat minor, the two triads in it that share no notes, a hexatonic pole, and hears it as the sound of the uncanny, in Wagner and in film scores. <bookmark mark='e'/> Symmetric sets give chords that are close in notes and far apart in keys. <bookmark mark='f'/> Part 32 maps that closeness as a geometry.", marks="cdef")
