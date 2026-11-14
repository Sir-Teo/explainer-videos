from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Temper(SoundScene):
    def construct(self):
        chapter(self, 8, r"Temperaments as linear maps", r"Which equal divisions of the octave work, \ and why?")
        self.vals()
        self.finder()
        self.hear()
        self.beyond()
        self.instruments()

    # ------------------------------------------------------------------
    def vals(self):
        d = load("temper")
        v12 = d["vals"]["12"]["val"]
        c = d["commas"]
        rows_ = text_rows([
            (r"a 5-limit interval is a vector of exponents: \ 3/2 \ = \ $2^{-1} 3^{1} 5^{0}$ \ $\to$ \ $[-1, \ 1, \ 0\rangle$", WHITE),
            (rf"12 equal steps maps the primes to steps: \ 2 $\to$ {v12[0]}, \ 3 $\to$ {v12[1]}, \ 5 $\to$ {v12[2]}: \ the `val' $\langle {v12[0]} \ {v12[1]} \ {v12[2]}]$", WHITE),
            (r"the step count of any interval is a dot product: \ 3/2 $\to$ $-12 + 19$ \ = \ 7 steps", TUNE),
            (rf"the syntonic comma 81/80 \ = \ $[{c['81/80'][0]}, \ {c['81/80'][1]}, \ {c['81/80'][2]}\rangle$ $\to$ $-48 + 76 - 28$ \ = \ 0 steps", EAR),
            (r"a temperament is a linear map; \ the commas it ignores are its kernel", GREY_A),
        ], font_size=23)
        head = label(r"a temperament is a linear map", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Part 6 met temperaments as compromises. There is a cleaner way to see them. <bookmark mark='a'/> Any just "
            "interval in the five-limit is a product of powers of two, three and five, so it is a vector of three exponents: "
            "the fifth, three halves, is minus one, one, zero. <bookmark mark='b'/> Twelve-note equal temperament sends the "
            "prime two to twelve steps, three to nineteen, five to twenty-eight. <bookmark mark='c'/> Then the size of any "
            "interval in steps is a dot product: the fifth is minus twelve plus nineteen, seven steps. "
            "<bookmark mark='d'/> And the syntonic comma, eighty-one eightieths, maps to zero steps: twelve-note temperament "
            "ignores it. <bookmark mark='e'/> A temperament is a linear map, and the commas it tempers out are its kernel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finder(self):
        d = load("temper")
        best = d["best"]
        bars = columns([b["worst"] for b in best], [str(b["n"]) for b in best], width=7.6, height=2.8, color=GREY_B,
                       hot=tuple(i for i, b in enumerate(best) if b["n"] in (12, 19, 31, 53)), hot_color=TUNE, fmt="{:.1f}", font_size=15).move_to(LEFT * 2.0 + DOWN * 0.4)
        xl = label(r"steps to the octave \ (each a new record)", font_size=18, color=GREY_A).next_to(bars, DOWN, buff=0.35)
        tbl = VGroup()
        names = {"81/80": r"81/80", "Pythagorean": r"Pyth.", "128/125": r"128/125", "schisma": r"schisma"}
        hdr = VGroup(label(r"", font_size=18), *[label(names[k], font_size=17, color=GREY_A) for k in names]).arrange(RIGHT, buff=0.35)
        tbl.add(hdr)
        for n in ("12", "19", "31", "53"):
            t = d["vals"][n]["tempers"]
            tbl.add(VGroup(label(n, font_size=19, color=TUNE), *[label(r"0" if t[k] else r"$\cdot$", font_size=19, color=EAR if t[k] else GREY_B) for k in names]).arrange(RIGHT, buff=0.6))
        tbl.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 4.3 + DOWN * 0.1)
        tl = label(r"0: \ the comma vanishes", font_size=16, color=EAR).next_to(tbl, DOWN, buff=0.25)
        head = label(r"a temperament finder: \ worst error on 3/2 and 5/4, \ cents", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now a search. For every equal division from five to sixty steps, take the nearest steps to a pure fifth and a pure "
            "major third, and keep the worse error. List the divisions that beat every smaller one. <bookmark mark='a'/> The "
            "records are five, seven, nine, ten, twelve, nineteen, twenty-two, thirty-one, thirty-four and fifty-three. "
            "Twelve, nineteen, thirty-one and fifty-three are the ones history chose: nineteen and thirty-one were proposed in "
            "the sixteenth and seventeenth centuries, fifty-three by Mercator and Holder. <bookmark mark='b'/> The kernel "
            "explains their characters. Twelve tempers out the syntonic comma, the Pythagorean comma and the diesis; nineteen "
            "and thirty-one temper out only the syntonic comma, like meantone; fifty-three tempers out none of these three, "
            "only the tiny schisma, which is why it is so nearly just."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(xl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(tbl), FadeIn(tl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("temper")
        c = clip("temper.four")
        cells = VGroup()
        for k, nm in (("12", r"12 steps"), ("19", r"19 steps"), ("31", r"31 steps"), ("just", r"just")):
            ch = d["chords"][k]
            cells.add(VGroup(label(nm, font_size=26, color=TUNE if k == "just" else WHITE),
                             label(rf"third {ch['third']:.1f}", font_size=18, color=GREY_A), label(rf"fifth {ch['fifth']:.1f}", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=1.2).move_to(UP * 0.2)
        head = label(r"a C major triad in four tunings \ (cents)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the difference in one chord. A C major triad with the thirds and fifths of twelve, nineteen and thirty-one "
            "equal steps, and then just. Twelve's third is fourteen cents wide and shimmers; nineteen's is seven cents narrow; "
            "thirty-one's is within one cent of pure, though its fifth is five cents narrow; the just triad is still."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"12, \ 19, \ 31, \ just", detail=r"Part 7's piano, \ retuned", corner=DL, tag_corner=DR)
            ks = ["12", "19", "31", "just"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.3 if i < 3 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        items = [
            (r"Paul Erlich and the `regular temperament' theorists \ (2000s): \ temperaments named by their kernels", WHITE),
            (r"meantone tempers out 81/80; \ magic, \ 3125/3072; \ porcupine, \ 250/243", WHITE),
            (r"a temperament can be played in many equal divisions: \ meantone in 12, \ 19, \ 31", WHITE),
            (r"the same linear algebra designs keyboards and tunings for new instruments", TUNE),
            (r"Part 6's history, \ rewritten as kernels and images", GREY_A),
        ]
        rows_scene(self, r"regular temperaments", items,
                   "The idea became a field. <bookmark mark='b'/> Paul Erlich and other theorists of the 2000s named temperaments "
                   "by the commas in their kernels: <bookmark mark='c'/> meantone tempers out eighty-one eightieths; others with "
                   "names like magic and porcupine temper out other commas. <bookmark mark='d'/> One temperament can be played in "
                   "several equal divisions: meantone in twelve, nineteen and thirty-one. <bookmark mark='e'/> The same linear "
                   "algebra now designs keyboards and tunings for new instruments. <bookmark mark='f'/> Part 6's history, "
                   "rewritten as kernels and images.", marks="cdef")

    # ------------------------------------------------------------------
    def instruments(self):
        items = [
            (r"Huygens \ (1691) \ argued for 31 equal steps; \ Fokker built a 31-tone organ \ (Haarlem, \ 1950)", WHITE),
            (r"Bosanquet's generalized keyboard \ (1870s): \ 53 steps under the fingers in a regular grid", WHITE),
            (r"19 and 31 keep meantone's spellings: \ C$\sharp$ and D$\flat$ become different keys", WHITE),
            (r"the cost: \ more keys, \ new fingerings, \ and repertory written for twelve", TUNE),
            (r"isomorphic keyboards \ (Part 31) \ make any regular temperament playable", GREY_A),
        ]
        rows_scene(self, r"instruments for more than twelve", items,
                   "Equal divisions beyond twelve have been built. <bookmark mark='b'/> Christiaan Huygens argued for thirty-one equal steps in 1691, and Adriaan Fokker built a thirty-one-tone organ in Haarlem in 1950. <bookmark mark='c'/> R. H. M. Bosanquet's generalized keyboard of the 1870s put fifty-three steps under the fingers in a regular grid. <bookmark mark='d'/> Nineteen and thirty-one keep meantone's spellings: C sharp and D flat become different keys. <bookmark mark='e'/> The cost is more keys, new fingerings, and a repertory written for twelve. <bookmark mark='f'/> The isomorphic keyboards of Part 31 make any regular temperament playable with one set of shapes.", marks="cdef")
