from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Sets(SoundScene):
    def construct(self):
        chapter(self, 2, r"Pitch-class sets", r"When are two chords the same chord?")
        self.operations()
        self.quiz()
        self.prime()
        self.vector()
        self.lewin()

    # ------------------------------------------------------------------
    def operations(self):
        s = [0, 1, 4, 6]
        a = pc_clock(s, radius=1.15, color=TUNE).move_to(LEFT * 4.2 + DOWN * 0.3)
        b = pc_clock([(x + 3) % 12 for x in s], radius=1.15, color=BLUE).move_to(DOWN * 0.3)
        c = pc_clock([(-x) % 12 for x in s], radius=1.15, color=EAR).move_to(RIGHT * 4.2 + DOWN * 0.3)
        la = label(r"a set: \ C, \ C$\sharp$, \ E, \ F$\sharp$", font_size=21, color=TUNE).next_to(a, DOWN, buff=0.45)
        lb = label(r"$T_3$: \ add 3, \ a rotation", font_size=21, color=BLUE).next_to(b, DOWN, buff=0.45)
        lc = label(r"$I_0$: \ $x \to -x$, \ a reflection", font_size=21, color=EAR).next_to(c, DOWN, buff=0.45)
        head = label(r"two operations on the clock", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Theorists after Schoenberg needed names for the cells he used. They treat a chord as a set of pitch classes on "
            "the twelve-hour clock, ignoring octave and order. <bookmark mark='a'/> Transposing a set adds the same number "
            "to every member: on the clock, a rotation. <bookmark mark='b'/> Inverting it turns every interval upside down: "
            "x goes to minus x, a reflection across the line through C and F sharp. Two sets related by these operations "
            "are said to belong to the same set class; their interval content is the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(c), FadeIn(lc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sets")
        c = clip("sets.quiz")
        card = listen_card(r"Two four-note chords, \ each struck and then broken. \ "
                           r"Is B a transposition of A, \ or its inversion? \ Listen to the order of the small and large steps.", width=10.4)
        with self.voiceover(
            "A question for your ears. Two four-note chords, each struck and then broken upwards. B is either A transposed, "
            "or A turned upside down. Which? Listen to the order of the small and large steps as each chord is broken."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = pc_clock([x % 12 for x in d["A"]], radius=1.2, color=GREY_A).move_to(LEFT * 3.3 + DOWN * 0.2)
        gb = pc_clock([x % 12 for x in d["B"]], radius=1.2, color=GREY_A).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"A: \ steps of 1, \ 3, \ 2 semitones, \ upwards", font_size=21, color=TUNE).next_to(ga, DOWN, buff=0.45),
                     label(r"B: \ 2, \ 3, \ 1: \ the same steps reversed, \ the inversion", font_size=21, color=EAR).next_to(gb, DOWN, buff=0.45))
        with self.voiceover(
            "B is the inversion. A, broken upwards, climbs by one, three and two semitones; B climbs by two, three and one, "
            "the same steps in the reverse order, which is what turning a chord upside down does. Both have the same prime "
            "form, zero one four six, and so the same set class."
        ):
            self.play(FadeIn(ans), ga.dots.animate.set_color(TUNE), gb.dots.animate.set_color(EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prime(self):
        ex = load("sets")["examples"]
        rows_ = VGroup()
        hdr = VGroup(*[label(t, font_size=19, color=GREY_B) for t in (r"chord", r"pitch classes", r"prime form", r"interval vector")])
        rows_.add(hdr)
        for name in ("major triad", "minor triad", "dominant seventh", "half-diminished", "Tristan chord", "all-interval tetrachord"):
            e = ex[name]
            rows_.add(VGroup(label(name, font_size=20, color=WHITE), label(", ".join(str(x) for x in e["set"]), font_size=20, color=GREY_A),
                             label("(" + " ".join(str(x) for x in e["prime"]) + ")", font_size=20, color=TUNE),
                             label("[" + "".join(str(x) for x in e["iv"]) + "]", font_size=20, color=BLUE)))
        xs = [-4.4, -1.2, 1.6, 4.4]
        for i, r in enumerate(rows_):
            for k, cell in enumerate(r):
                cell.move_to([xs[k], 2.0 - 0.6 * i, 0])
        head = label(r"prime forms: \ one name for each set class", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Each set class gets one name, its prime form: rotate the set to its most compact arrangement, do the same for "
            "its inversion, take the more compact of the two and start it on zero. <bookmark mark='a'/> The major and minor "
            "triads have the same prime form, zero three seven: one is the other upside down. <bookmark mark='b'/> So do the "
            "dominant seventh and the half-diminished seventh. <bookmark mark='c'/> And Wagner's Tristan chord, from Part 27, "
            "has the half-diminished seventh's prime form, zero two five eight: set theory hears no difference, though Wagner's "
            "context does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[3]), FadeIn(rows_[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[5]), FadeIn(rows_[6]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vector(self):
        rows_ = text_rows([
            (r"interval classes: \ 1 to 6 \ (an interval and its inversion count as one: \ 5 semitones = 7)", WHITE),
            (r"the interval vector counts each class among all pairs of the set's notes", WHITE),
            (r"major triad, \ [001110]: \ one minor third, \ one major third, \ one fourth or fifth", WHITE),
            (r"\{0, 1, 4, 6\}: \ [111111]: \ every interval class exactly once, \ an `all-interval' tetrachord", TUNE),
            (r"the vector is a set's harmonic colour, \ the same for every transposition and inversion", GREY_A),
        ], font_size=24)
        head = label(r"the interval vector", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The second tool is the interval vector. <bookmark mark='a'/> Fold intervals into six classes, counting an "
            "interval and its inversion as one, so that five semitones and seven are both class five. <bookmark mark='b'/> "
            "Then count each class among all the pairs of notes in the set. <bookmark mark='c'/> A major triad has three "
            "pairs: one minor third, one major third, one fourth or fifth. <bookmark mark='d'/> The set zero one four six "
            "has six pairs, one of every class, which is why it is called the all-interval tetrachord. "
            "<bookmark mark='e'/> The vector is a set's harmonic colour, unchanged by transposition and inversion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lewin(self):
        items = [
            (r"David Lewin \ (1987): \ attend to the operations, \ not only the sets", WHITE),
            (r"$T_n$ and $I_n$ form a group of 24 operations \ (the dihedral group)", WHITE),
            (r"a piece moves from one set to another by an operation: \ the operation is the musical idea", WHITE),
            (r"the same group acts on triads: \ the neo-Riemannian transformations", TUNE),
            (r"Part 31 builds this theory of transformations", GREY_A),
        ]
        rows_scene(self, r"operations as objects", items,
                   "One more idea, which later parts build on. <bookmark mark='b'/> The theorist David Lewin argued, in 1987, that what matters is often the operation, not the sets. <bookmark mark='c'/> The twelve transpositions and twelve inversions form a group of twenty-four operations, the symmetries of a twelve-sided polygon. <bookmark mark='d'/> A passage that moves from one set to another by an inversion is about that inversion. <bookmark mark='e'/> The same group acts on major and minor triads, which leads to the neo-Riemannian transformations. <bookmark mark='f'/> Part 31 builds this theory.", marks="cdef")
