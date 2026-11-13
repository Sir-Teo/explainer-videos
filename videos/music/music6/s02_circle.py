from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Comma(SoundScene):
    def construct(self):
        chapter(self, 1, r"The circle that will not close", r"Do twelve fifths make seven octaves?", lit=(-530,))
        self.walk()
        self.proof()
        self.wolf()

    # ------------------------------------------------------------------
    def walk(self):
        d = load("circle")
        c = clip("circle.walk")
        steps = d["steps"]
        circ = FifthsCircle(radius=2.0, names=tuple(s["name"] for s in steps[:12])).move_to(LEFT * 3.6 + DOWN * 0.2)
        g = axes([0, 1260], [0, 1], x_length=6.2, y_length=0.6, xlabel=r"cents above C", ylabel="", xticks=[0, 200, 400, 600, 800, 1000, 1200], yticks=[], font_size=18)
        g.move_to(RIGHT * 3.3 + DOWN * 1.6)
        table = VGroup(label(r"each step: \ $\times\,\tfrac32$, \ then halve until it fits in the octave", font_size=26, color=GREY_A),
                       MathTex(r"\left(\tfrac32\right)^{12} = \frac{531441}{4096} = 129.746\ldots", font_size=32),
                       MathTex(r"2^{7} = 128", font_size=32)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.3 + UP * 1.6)
        with self.voiceover(
            "Start with the purest interval after the octave: the fifth, three to two. Tune a note a pure fifth "
            "above C, and you have G. A pure fifth above that, D. Keep going, and whenever a note lands outside "
            "the octave, halve its frequency to bring it back. <bookmark mark='a'/> A fifth is seven of the "
            "twelve steps on a keyboard, so after twelve fifths you have been round every one of the twelve "
            "notes, and you should be back on C. Listen to the twelve notes, and then to the thirteenth."
        ) as vo:
            self.play(FadeIn(circ.ring), FadeIn(circ.dots[0]), FadeIn(circ.names[0]), FadeIn(table[0]))
            vo.wait_until("a")
            self.play(FadeIn(g))
        marks = VGroup()
        with self.listen(c) as snd:
            window(snd, r"twelve pure fifths, \ folded into one octave", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for k, s in enumerate(steps):
                snd.wait_until(f"s{k}")
                if k < 12:
                    circ.dots[k].set_color(TUNE)
                    self.add(circ.dots[k], circ.names[k])
                    if k:
                        self.add(circ.edge(k - 1))
                    m = Line(g.ax.c2p(s["cents"], 0), g.ax.c2p(s["cents"], 0.8), color=TUNE, stroke_width=4)
                else:
                    m = Line(g.ax.c2p(s["cents"], 0), g.ax.c2p(s["cents"], 0.8), color=BAD, stroke_width=4)
                marks.add(m)
                self.add(m)
                self.play(m.animate(rate_func=there_and_back).set_stroke(width=9), run_time=0.4)
        both = clip("circle.both")
        gap = label(rf"the thirteenth note is {d['comma_cents']:.1f} cents above the octave", font_size=28, color=BAD).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "The thirteenth note is not C. It is a little higher. <bookmark mark='a'/> Twelve fifths multiply the "
            "frequency by a hundred and twenty-nine point seven. Seven octaves multiply it by a hundred and "
            f"twenty-eight. The difference is {say(d['comma_cents'], 1)} cents, almost a quarter of a semitone, "
            "and it has had a name for two thousand years: the Pythagorean comma. In cents the sum is easier still. "
            "A pure fifth is seven hundred and two cents. Twelve of them make eight thousand four hundred and "
            "twenty-four, and seven octaves are eight thousand four hundred. Two cents too many in each fifth, "
            "twelve times over. Here is the true C and the overshot one, together."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(table[1]), FadeIn(table[2]), FadeIn(gap))
        with self.listen(both) as snd:
            window(snd, r"C, \ and the note twelve fifths later", kind="synthesized", corner=DL, tag_corner=DR, tag=False)
            snd.drive(marks[-1], lambda m, t: m.set_stroke(width=4 + 5 * abs(np.cos(np.pi * d["beat"] * t))))
            snd.drive(marks[0], lambda m, t: m.set_stroke(width=4 + 5 * abs(np.cos(np.pi * d["beat"] * t))))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        d = load("circle")
        title = label(r"A worked example: \ could any number of fifths close the circle?", font_size=34).to_edge(UP, buff=0.45)
        ask = pause_card(r"For the circle to close, \ some number of fifths must equal some number of octaves: \\ $\left(\tfrac32\right)^m = 2^n$. \quad Can that ever happen?", width=10.0).move_to(UP * 1.2)
        steps = VGroup(MathTex(r"\left(\tfrac32\right)^m = 2^n \quad\Longleftrightarrow\quad 3^m = 2^{\,m+n}", font_size=38),
                       label(r"every power of 3 is odd; \quad every power of 2 is even", font_size=32, color=GREY_A),
                       label(r"never.", font_size=44, color=BAD)).arrange(DOWN, buff=0.35).move_to(UP * 0.9)
        moral = VGroup(label(r"no stack of pure fifths ever returns to its starting note", font_size=30, color=EAR),
                       label(r"every tuning is a decision about where to put the error", font_size=32, color=TUNE)).arrange(DOWN, buff=0.25).move_to(DOWN * 2.0)
        with self.voiceover(
            "Perhaps twelve is just the wrong number. Could some other number of fifths come out exactly on an "
            "octave? Pause, and decide. It takes one line."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "For m fifths to equal n octaves, three halves to the power m must equal two to the power n. Multiply "
            "out the halves, and that says a power of three equals a power of two. <bookmark mark='a'/> But every "
            "power of three is odd, and every power of two is even. <bookmark mark='b'/> It can never happen. Not "
            "with twelve fifths, not with fifty-three, not with a million. <bookmark mark='c'/> So the trouble is "
            "not in our instruments or our ears. It is in the integers. No stack of pure fifths ever returns to "
            "its starting note, and the same goes for pure thirds, which need a five. Every tuning system ever "
            "devised is a decision about where to put an error that cannot be removed."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(moral[0]))
            self.wait(max(vo.remaining() - 6.0, 0.1))
            self.play(FadeIn(moral[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wolf(self):
        d = load("circle")
        c = clip("circle.wolf")
        circ = FifthsCircle(radius=2.0).move_to(LEFT * 3.6 + DOWN * 0.3)
        edges = VGroup(*[circ.edge(k, color=PURE if name != "G#" else BAD, stroke_width=6 if name != "G#" else 9) for k, (name, _) in enumerate(d["fifths"])])
        head = label(r"Pythagorean tuning: \ eleven pure fifths, \ and the one left over", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        wl = VGroup(label(r"the last fifth, \ G$\sharp$ to E$\flat$:", font_size=26, color=BAD),
                    label(rf"{d['wolf_cents']:.1f} cents, \ a whole comma narrow", font_size=26, color=BAD),
                    label(rf"it beats {d['wolf_beat']:.0f} times a second: \ the \textbf{{wolf}}", font_size=28, color=BAD)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 1.3)
        bx = boxes((r"C to G", r"G$\sharp$ to E$\flat$"), buff=0.5, width=2.7, height=1.1, font_size=28).move_to(RIGHT * 3.2 + DOWN * 0.7)
        with self.voiceover(
            "The oldest answer is the bluntest. Tune eleven fifths pure, in a chain from E flat up to G sharp, and "
            "let the twelfth be whatever is left. <bookmark mark='a'/> That is Pythagorean tuning, the tuning of "
            "medieval Europe and of classical China. Eleven of its fifths are perfect. <bookmark mark='b'/> The "
            f"twelfth, from G sharp to E flat, has to absorb the whole comma. It is {say(d['wolf_cents'], 1)} "
            "cents instead of seven hundred and two, and it howls. Musicians called it the wolf. Here is a pure "
            "fifth, and then the wolf."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e, (n, _) in zip(edges, d["fifths"]) if n != "G#"], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(edges[circ.index("G#")]), FadeIn(wl), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"a pure fifth, \ then the wolf", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("pure", "wolf"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        cost = VGroup(label(r"the price is paid elsewhere too:", font_size=24, color=GREY_A), label(r"every major third is $\tfrac{81}{64}$,", font_size=24, color=GREY_A),
                      label(r"the restless third of Part 5", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(RIGHT * 3.2 + DOWN * 2.4)
        with self.voiceover(
            "As long as music stayed away from that one fifth, the wolf did no harm. But Pythagorean tuning has "
            "a second cost, and it is in every key. Its major thirds are all made of four pure fifths. That is "
            "the restless third of eighty-one to sixty-four that we met in Part 5, and it is the reason this "
            "tuning was abandoned."
        ):
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()
