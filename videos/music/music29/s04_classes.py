from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Classes(SoundScene):
    def construct(self):
        chapter(self, 3, r"Counting the chords", r"How many different chords are there?", extra=((1973, r"Forte's \textit{The Structure of Atonal Music}"),))
        self.brute()
        self.trichords()
        self.burnside()
        self.forte()

    # ------------------------------------------------------------------
    def brute(self):
        d = load("classes")
        ks = list(range(0, 13))
        bars = columns([d["by_size"][str(k)] for k in ks], [str(k) for k in ks], width=9.0, height=2.8, color=TUNE, fmt="{:.0f}", font_size=17)
        bars.move_to(DOWN * 0.4)
        t = label(rf"set classes by number of notes: \ {d['brute']} in all", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.35)
        cap = label(r"found by computing the prime form of every one of the 4,096 sets", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How many set classes are there? The blunt way is to compute the prime form of every one of the four thousand "
            f"and ninety-six sets and count the different answers. There are {say(d['brute'])}. Most have five, six or seven "
            f"notes: {say(d['by_size']['6'])} hexachords, {say(d['by_size']['5'])} pentachords, {say(d['by_size']['4'])} "
            f"tetrachords and {say(d['by_size']['3'])} trichords. Part 28 counted three hundred and fifty-two shapes under "
            "transposition alone; inversion folds most of them in pairs."
        ):
            self.play(FadeIn(t), FadeIn(bars), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def burnside(self):
        d = load("classes")
        rows_ = text_rows([
            (r"Burnside's lemma \ (Part 12): \ classes = the average number of sets each operation leaves unchanged", WHITE),
            (r"12 transpositions: \ $T_k$ fixes $2^{\gcd(k,12)}$ sets \ (4,096 for $T_0$, \ 64 for $T_6$, \ ...)", WHITE),
            (r"12 inversions: \ $x \to k - x$ has 0 or 2 fixed notes, \ and pairs the rest: \ $2^7$ or $2^6$ sets", WHITE),
            (r"$(4096 + 4\cdot 2 + 2\cdot 4 + 2\cdot 8 + 2\cdot 16 + 64 + 6\cdot 128 + 6\cdot 64) \ / \ 24 \ = \ 5376/24 \ = \ 224$", TUNE),
            (rf"the brute-force count agrees: \ {d['brute']} = {d['burnside']}", GREY_A),
        ], font_size=24)
        head = label(r"the same number, \ without listing anything", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The elegant way needs no listing at all. <bookmark mark='a'/> Burnside's lemma, which Part 12 used, says the "
            "number of classes is the average, over all the operations, of how many sets each operation leaves unchanged. "
            "<bookmark mark='b'/> A transposition by k leaves unchanged the sets that repeat every greatest common divisor of "
            "k and twelve: two to the power of that divisor of them. <bookmark mark='c'/> An inversion has either no fixed "
            "pitch classes or two, and swaps the rest in pairs, so it leaves two to the seventh or two to the sixth sets "
            "alone. <bookmark mark='d'/> Add the twenty-four counts and divide by twenty-four: two hundred and twenty-four. "
            "<bookmark mark='e'/> The brute-force count agrees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forte(self):
        items = [
            (r"Allen Forte \ (1973): \ every class of 3 to 9 notes named, \ `4-z15', \ `6-20' ...", WHITE),
            (r"his table: \ 12 trichords, \ 29 tetrachords, \ 38 pentachords, \ 50 hexachords \ (and complements)", WHITE),
            (r"the counts above match his table exactly", TUNE),
            (r"analysis as naming: \ which classes a piece uses, \ and how they are related", WHITE),
            (r"the names are a tool; \ which notes form a `set' in a piece is the analyst's choice", GREY_A),
        ]
        rows_scene(self, r"Forte's names", items,
                   "In 1973 Allen Forte published names for every class of three to nine notes, names like four z fifteen or six "
                   "twenty. <bookmark mark='c'/> His table lists twelve trichords, twenty-nine tetrachords, thirty-eight "
                   "pentachords and fifty hexachords, with the larger sets as their complements, <bookmark mark='d'/> and the "
                   "counts the program found match it exactly. <bookmark mark='e'/> Analysis in this tradition names the classes "
                   "a piece uses and how they are related. <bookmark mark='f'/> The names are a tool; which notes count as a set "
                   "in a real piece is still the analyst's decision, as Part 28's frontier warned.", marks="cdef")

    # ------------------------------------------------------------------
    def trichords(self):
        d = load("trichords")
        c = clip("trichords.twelve")
        cells = VGroup()
        for pf, iv in zip(d["classes"], d["ivs"]):
            cl = pc_clock(pf, radius=0.55, color=TUNE, labels=False)
            cells.add(VGroup(cl, label("(" + " ".join(str(x) for x in pf) + ")", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12))
        cells.arrange_in_grid(rows=2, cols=6, buff=(0.45, 0.4)).move_to(DOWN * 0.2)
        head = label(r"all twelve three-note chords \ (up to transposition and inversion)", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here are all twelve classes of three-note chord, each in prime form, played as a close chord on middle C. From "
            "the cluster of three semitones, through chords built of seconds and fourths, to the familiar ones near the end: "
            "the diminished triad, the major and minor triad, which are one class, and the augmented triad. Every "
            "three-note sonority in any music is one of these twelve."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"twelve trichords", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(12):
                pulse(snd, cells[i], i * d["step"] * d["unit"], (i * d["step"] + 1.2) * d["unit"], buff=0.06)
        self.wait(0.3)
        self.clear_scene()
