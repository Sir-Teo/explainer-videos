from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Size(SoundScene):
    def construct(self):
        chapter(self, 4, r"The size of a voice leading", r"How far does a progression travel?")
        self.quiz()
        self.norms()
        self.algorithm()
        self.sizes()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("vlsize")
        c = clip("vlsize.quiz")
        card = listen_card(r"C major to F major, \ twice, \ in two different voicings of the move. \ "
                           r"Which sounds smoother, \ A or B? \ Then: \ how would you measure it?", width=10.4)
        with self.voiceover(
            "An easy question for the ears, and a harder one for the mind. C major goes to F major and back, twice each, in "
            "two different ways. Which sounds smoother, A or B? And then: how would you put a number on it?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cols = VGroup()
        for k in "AB":
            w = d["ways"][k]
            mv = r", \ ".join(f"{x:+d}" for x in w["moves"])
            cols.add(VGroup(label(k, font_size=40, color=GREY_A), label(r"C E G \ to \ " + (r"C F A" if k == "A" else r"F A C"), font_size=24, color=WHITE),
                            label(rf"moves: \ {mv}", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=2.4).move_to(UP * 0.3)
        self.play(FadeOut(card), FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, cols[0][0], d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.1)
            pulse(snd, cols[1][0], d["starts"]["B"], c.duration, buff=0.1)
        a, b = d["ways"]["A"], d["ways"]["B"]
        ans = VGroup(label(rf"A: \ {a['taxicab']:.0f} semitones in all", font_size=22, color=TUNE).next_to(cols[0], DOWN, buff=0.4),
                     label(rf"B: \ {b['taxicab']:.0f} semitones in all", font_size=22, color=EAR).next_to(cols[1], DOWN, buff=0.4))
        with self.voiceover(
            "A is smoother: C holds, E rises a semitone to F, G rises a tone to A, three semitones in all. In B every voice "
            "leaps up a fourth, fifteen semitones in all, and the progression sounds like a block being lifted. Same two "
            f"chords; one voice leading is five times the size of the other. And A is the smallest possible: no way of "
            f"moving C major's three voices onto F major's notes adds up to less than {say(d['best'])} semitones."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def norms(self):
        d = load("vlsize")
        hdr = VGroup(*[label(s, font_size=21, color=GREY_A) for s in (r"voice leading", r"moves", r"sum", r"Euclidean", r"largest")])
        rows_ = [hdr]
        names = {"A": r"C E G \ to \ C F A", "B": r"C E G \ to \ F A C", "C": r"C E G \ to \ A F C"}
        for k in "ABC":
            w = d["ways"][k]
            rows_.append(VGroup(label(names[k], font_size=21, color=WHITE), label(r", \ ".join(f"{x:+d}" for x in w["moves"]), font_size=21, color=WHITE),
                                label(f"{w['taxicab']:.0f}", font_size=21, color=TUNE), label(f"{w['euclid']:.2f}", font_size=21, color=BLUE),
                                label(f"{w['max']:.0f}", font_size=21, color=EAR)))
        xs = [-4.4, -1.0, 1.4, 3.2, 5.0]
        tbl = VGroup()
        for i, r in enumerate(rows_):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 1.5 - 0.85 * i, 0])
            tbl.add(r)
        head = label(r"three ways to measure the same move", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (r"the sum \ (taxicab): \ total semitones moved", TUNE),
            (r"Euclidean: \ the straight-line length in chord space", BLUE),
            (r"largest: \ the biggest single leap", EAR),
            (r"all three agree that A is smallest; \ by the largest leap, \ B and C tie", GREY_A))]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is more than one way to measure. <bookmark mark='a'/> Add up the semitones each voice moves, the taxicab "
            "size. <bookmark mark='b'/> Or take the straight-line length of the path in chord space, the Euclidean size. "
            "<bookmark mark='c'/> Or look only at the biggest single leap. <bookmark mark='d'/> For these three ways from C "
            "major, all three measures agree that A is the smallest, and the first two that B, every voice up a fourth, is "
            "the largest; C, which sends C down to A, lies between, nine semitones by the sum but a leap of five at most, the "
            "same largest leap as B. In many musical cases the measures agree; where they do not, choosing one is "
            "part of the theory. This part uses the sum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tbl[0]), FadeIn(tbl[1]))
            self.play(FadeIn(tbl[2]), FadeIn(tbl[3]), FadeIn(cap[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
            vo.wait_until("d")
            self.play(FadeIn(cap[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algorithm(self):
        items = [
            (r"try every way of giving one chord's notes to the other's voices: \ 3! \ = \ 6 for triads", WHITE),
            (r"each voice moves the short way round the octave", WHITE),
            (r"keep the smallest sum: \ the minimal voice leading", WHITE),
            (r"a theorem: \ some minimal voice leading never crosses voices, \ so only the n rotations need trying", TUNE),
            (r"Monochord's \texttt{geometry.vl} does it for any chords of equal size, \ in any tuning", GREY_A),
        ]
        rows_scene(self, r"finding the smallest voice leading", items,
                   "How does a program find the smallest voice leading? <bookmark mark='b'/> Try every way of handing one chord's "
                   "notes to the other chord's voices: six ways for triads, twenty-four for four-note chords. "
                   "<bookmark mark='c'/> Let each voice move the short way round the octave. <bookmark mark='d'/> Keep the "
                   "smallest total. <bookmark mark='e'/> A theorem from Tymoczko's work saves effort: there is always a smallest "
                   "voice leading in which no voices cross, so it is enough to try the n rotations of one sorted chord against the "
                   "other. <bookmark mark='f'/> Monochord's version tries them all, for chords of any equal size, in any tuning.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def sizes(self):
        items = [
            (r"a triad to a seventh chord: \ one voice must double, \ or split in two", WHITE),
            (r"G$^7$ to C: \ B to C, \ F to E, \ D to C, \ G holds: \ D and B both land on C", WHITE),
            (r"cardinality equivalence \ (the C of OPTIC, \ chapter 7) \ allows exactly this", TUNE),
            (r"the minimum is then taken over every way to double", WHITE),
            (r"four-part harmony doubles a triad's note: \ Part 17's doubling rules choose which", GREY_A),
        ]
        rows_scene(self, r"chords of different sizes", items,
                   "What about chords of different sizes? <bookmark mark='b'/> To go from a triad to a seventh chord, or back, some voice must double or split. <bookmark mark='c'/> G seven to C: B rises to C, F falls to E, D falls to C, and G holds; two voices meet on C. <bookmark mark='d'/> Cardinality equivalence, the C of the next chapter's five letters, allows exactly this. <bookmark mark='e'/> The smallest voice leading is then taken over every way of doubling. <bookmark mark='f'/> Four-part harmony doubles one note of every triad, and Part 17's doubling rules choose which.", marks="cdef")
