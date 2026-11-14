from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Why(SoundScene):
    def construct(self):
        chapter(self, 4, r"Why this scale", r"What is special about the white keys?", extra=((1991, r"maximally even sets"),))
        self.even()
        self.two_sizes()
        self.deep()
        self.moved()

    # ------------------------------------------------------------------
    def even(self):
        d = load("why")
        white = twelve(d["formula"], radius=1.6, color=TUNE).move_to(LEFT * 3.6 + DOWN * 0.3)
        black = twelve([n for n in range(12) if n not in d["formula"]], radius=1.6, color=SHORT).move_to(RIGHT * 3.6 + DOWN * 0.3)
        f = MathTex(r"\text{note } k \text{ goes at } \left\lfloor \tfrac{12\,k + 5}{7} \right\rfloor: \quad 0,\ 2,\ 4,\ 5,\ 7,\ 9,\ 11", font_size=38).to_edge(UP, buff=0.5)
        ask = label(r"seven notes out of twelve places, \ as evenly as possible", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        ideal = VGroup(*[Dot(white.at(12 * (k + 5 / 7) / 7), radius=0.07, color=BAD) for k in range(7)])
        spokes = VGroup(*[Line(white.ring.get_center(), d.get_center(), color=BAD, stroke_width=1.5, stroke_opacity=0.5) for d in ideal])
        empty = twelve([], radius=1.6).move_to(white)
        lw = label(r"seven notes, \ as evenly as twelve places allow", font_size=24, color=TUNE).next_to(white, DOWN, buff=0.35)
        lb = label(r"the five left over: \ also as even as can be", font_size=24, color=SHORT).next_to(black, DOWN, buff=0.35)
        with self.voiceover(
            "The stack of fifths is one way to arrive at the white keys. Here is a second, which uses no "
            "fifths at all. Suppose you want seven notes out of twelve, spread as evenly as possible "
            "round the octave. Seven does not divide twelve, so they cannot be equally spaced. The best "
            "you can do is to space them twelve sevenths apart, and move each one back to the nearest "
            "place. <bookmark mark='a'/> That gives places zero, two, four, five, seven, nine and "
            "eleven: C, D, E, F, G, A, B. The white keys. Where you begin the spacing only decides the "
            "key. In 1991 John Clough and Jack Douthett called such a set maximally even. "
            "<bookmark mark='b'/> And the five places left over, the black keys, are the most even way "
            "to choose five. The keyboard is two maximally even sets, fitted together."
        ) as vo:
            self.play(FadeIn(ask), FadeIn(empty))
            self.wait(9.0)
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(d_)) for s_, d_ in zip(spokes, ideal)], lag_ratio=0.25), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeOut(ask), FadeIn(f), FadeOut(empty), FadeIn(white), FadeIn(lw), FadeOut(spokes), FadeOut(ideal))
            vo.wait_until("b")
            self.play(FadeIn(black), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_sizes(self):
        d = load("why")
        rows = VGroup()
        for k in ("2", "3", "4", "5", "6", "7"):
            a, b = d["myhill"][k]
            rows.add(VGroup(label(d["interval_names"][k], font_size=30, color=TUNE), label(rf"{a} or {b} semitones", font_size=30, color=GREY_A)))
        for r in rows:
            r.arrange(RIGHT, buff=0.8)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        x1 = max(r[0].get_right()[0] for r in rows) + 0.7
        for r in rows:
            r[1].align_to(np.array([x1, 0, 0]), LEFT)
        rows.move_to(LEFT * 2.6 + DOWN * 0.2)
        rare = VGroup(label(r"fourths: \ six of 5 semitones, \\ one of 6: \ the tritone, \ F to B", font_size=28, color=EAR)).move_to(RIGHT * 3.4 + UP * 0.4)
        use = label(r"hear the tritone, \\ and you know where you are", font_size=28, color=GREY_A).next_to(rare, DOWN, buff=0.5)
        head = label(r"every kind of interval comes in exactly two sizes", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Evenness has a consequence. In the white-key scale, count intervals in steps of the scale: "
            "a second is one step, a third is two. <bookmark mark='a'/> Every one of them comes in exactly "
            "two sizes. Seconds are one or two semitones. Thirds are three or four: minor and major. And "
            "so on up. <bookmark mark='b'/> But the two sizes are not equally common. Of the seven "
            "fourths, six are perfect, and one is a semitone wider: the tritone, from F to B. An interval "
            "that occurs only once is a landmark. Hear it, and you know exactly which two notes of the "
            "scale you are hearing, and so where home is. A scale of equal steps has no landmarks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=4.5)
            vo.wait_until("b")
            self.play(FadeIn(rare), Indicate(rows[2], color=EAR))
            self.play(FadeIn(use))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def deep(self):
        d = load("why")
        names = ("semitones", "tones", "minor thirds", "major thirds", "fourths or fifths", "tritones")
        short = ("m2", "M2", "m3", "M3", "P4", "tt")
        a = vector_bars(d["vectors"]["major"], width=5.4, height=2.6, color=TUNE, names=short, top=6, font_size=24).move_to(LEFT * 3.5 + DOWN * 0.8)
        b = vector_bars(d["vectors"]["whole-tone"], width=5.4, height=2.6, color=SHORT, names=short, top=6, font_size=24).move_to(RIGHT * 3.5 + DOWN * 0.8)
        la = label(r"the white keys: \ 2, \ 5, \ 4, \ 3, \ 6, \ 1", font_size=28, color=TUNE).next_to(a, UP, buff=0.5)
        lb = label(r"six equal steps: \ 0, \ 6, \ 0, \ 6, \ 0, \ 3", font_size=28, color=SHORT).next_to(b, UP, buff=0.5)
        head = label(r"how many pairs of notes are each interval apart?", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A third property, and the strangest. Take the seven notes and count the pairs. How many "
            "pairs are a semitone apart? Two. A whole tone apart? Five. <bookmark mark='a'/> Minor "
            "thirds, four. Major thirds, three. Fourths or fifths, six. Tritones, one. Six kinds of "
            "interval, and six different counts: every number from one to six, once each. A scale like "
            "that is called deep. <bookmark mark='b'/> Compare a scale of six equal steps. It has no "
            "semitones, no minor thirds and no fifths at all. The white keys contain a little of "
            "everything, in graded amounts, and the interval they have most of is the fifth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(la))
            self.play(LaggedStart(*[FadeIn(x) for x in a], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moved(self):
        d = load("why")
        c = clip("why.fifth")
        kb = keyboard(0, 24, width=11.0, height=1.9).move_to(UP * 1.2)
        sets = {"C": [0, 2, 4, 5, 7, 9, 11], "G": [7, 9, 11, 0, 2, 4, 6], "Db": [1, 3, 5, 6, 8, 10, 0]}
        rows = VGroup(label(r"on C", font_size=30, color=TUNE), label(rf"on G, \ a fifth up: \ {d['common'][6]} of the 7 notes are the same", font_size=30, color=GOOD),
                      label(rf"on D$\flat$, \ a semitone up: \ only {d['common'][0]} are", font_size=30, color=BAD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 1.4)
        with self.voiceover(
            "Those counts are not a curiosity. They say what happens when the scale is moved. Shift all "
            "seven notes up by some interval: the number of notes that stay where they were is the "
            "number of times that interval occurs in the scale. The fifth occurs six times. So a major "
            "scale moved up a fifth keeps six of its seven notes, and changes one. Moved up a semitone, "
            "which occurs twice, it keeps only two. Listen to the scale on C, then on G, then on D flat."
        ):
            self.play(FadeIn(kb), FadeIn(rows[0]))
        with self.listen(c) as snd:
            window(snd, r"a major scale on C, \ on G, \ on D flat", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, (nm, row) in enumerate(zip(("C", "G", "Db"), rows)):
                snd.wait_until(d["starts"][k])
                kb.clear()
                base = set(sets["C"])
                for o in (0, 12):
                    for n in sets[nm]:
                        if n + o in kb.key:
                            kb.light(n + o, TUNE if (n in base or nm == "C") else BAD)
                if k:
                    self.add(row)
                pulse(snd, row, d["starts"][k], d["starts"][k] + 3.2, buff=0.1)
        with self.voiceover(
            "That is the whole idea behind key signatures. Every step along the chain of fifths changes "
            "one note, so nearby keys share nearly everything, and a piece can slip from one to the next "
            "with a single sharp or flat. Part 15 is built on it. For now: the white keys are generated "
            "by fifths, they are as even as possible, their intervals come in two sizes with a single "
            "landmark, and they are deep. No other seven notes out of twelve have all of that."
        ):
            self.play(Indicate(rows[1], color=GOOD, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()
