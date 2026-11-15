from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


def op_box(n, color=TUNE, r=0.32):
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=3), label(str(n), font_size=20, color=WHITE))


def algo(kind):
    g = VGroup()
    if kind == "stack":
        ops = VGroup(*[op_box(i) for i in (3, 2, 1)]).arrange(DOWN, buff=0.45)
        g.add(ops, *[Arrow(ops[i].get_bottom(), ops[i + 1].get_top(), buff=0.05, color=GREY_B, stroke_width=3) for i in range(2)])
        name = r"a stack: \ 3 modulates 2 modulates 1"
    elif kind == "pairs":
        a = VGroup(op_box(2), op_box(1)).arrange(DOWN, buff=0.45)
        b = VGroup(op_box(4), op_box(3)).arrange(DOWN, buff=0.45)
        pr = VGroup(a, b).arrange(RIGHT, buff=0.7)
        g.add(pr, Arrow(a[0].get_bottom(), a[1].get_top(), buff=0.05, color=GREY_B, stroke_width=3), Arrow(b[0].get_bottom(), b[1].get_top(), buff=0.05, color=GREY_B, stroke_width=3))
        name = r"two pairs, \ summed"
    elif kind == "y":
        top = VGroup(op_box(2), op_box(3)).arrange(RIGHT, buff=0.5)
        one = op_box(1).next_to(top, DOWN, buff=0.6)
        g.add(top, one, *[Arrow(t.get_bottom(), one.get_top(), buff=0.05, color=GREY_B, stroke_width=3) for t in top])
        name = r"two modulators on one carrier"
    else:
        ops = VGroup(*[op_box(i) for i in (1, 2, 3, 4)]).arrange(RIGHT, buff=0.3)
        g.add(ops)
        name = r"all carriers: \ additive"
    return VGroup(g, label(name, font_size=15, color=GREY_A).next_to(g, DOWN, buff=0.3))


class Ops(SoundScene):
    def construct(self):
        chapter(self, 3, r"Operators and algorithms", r"How did a keyboard of 1983 make a piano from sines?")
        self.operators()
        self.algorithms()
        self.feedback()
        self.heard()
        self.era()

    # ------------------------------------------------------------------
    def operators(self):
        items = [
            (r"Yamaha's name for one oscillator with its own envelope and level: \ an operator", WHITE),
            (r"a modulator's level is an index; \ a carrier's level is a loudness", WHITE),
            (r"the DX7: \ six operators per voice, \ wired in one of 32 algorithms", WHITE),
            (r"every operator has its own ratio to the key and its own envelope: \ each sideband family can rise and die on its own", WHITE),
            (r"our engine: \ up to six operators, \ any of several wirings, \ feedback on one", TUNE),
        ]
        rows_scene(self, r"operators", items,
                   "Yamaha made Chowning's two oscillators into a system. <bookmark mark='b'/> An operator is one sine oscillator "
                   "with its own envelope and its own output level. <bookmark mark='c'/> When it modulates another, its level is an "
                   "index; when it is heard, its level is a loudness. <bookmark mark='d'/> The DX7 had six operators per voice, "
                   "wired in one of thirty-two algorithms. Every operator has its own ratio to the key and its own envelope, so each "
                   "family of sidebands can rise and die on its own schedule, as a real instrument's partials do. "
                   "<bookmark mark='f'/> Our engine follows the same plan: up to six operators, a choice of wirings, and feedback "
                   "on one.", marks="bcdf")

    # ------------------------------------------------------------------
    def algorithms(self):
        al = VGroup(*[algo(k) for k in ("stack", "pairs", "y", "parallel")]).arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to(DOWN * 0.2)
        note = label(r"arrows: \ modulates; \ the bottom row is heard", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"four algorithms", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "An algorithm is a wiring diagram. <bookmark mark='a'/> A stack: three modulates two modulates one, so the "
            "sidebands of sidebands pile up into dense spectra. <bookmark mark='b'/> Two pairs, summed: two simple FM sounds "
            "layered, as in the electric piano we are about to hear. <bookmark mark='c'/> Two modulators on one carrier: their "
            "sidebands multiply into combinations. <bookmark mark='d'/> And all carriers, no modulation at all: the DX7 could be "
            "a small additive organ too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(ghost(al, 0.3)))
            for mark, a in zip("abcd", al):
                vo.wait_until(mark)
                self.play(FadeIn(a), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def feedback(self):
        d = load("dx")
        fb = d["feedback"]
        saw = (20 * np.log10(1 / np.arange(1, 9))).tolist()
        hs = VGroup(*[harm_bars(fb[k], width=0.16, gap=0.24, floor=-40.0, height=2.0, color=c, labels=False) for k, c in (("0.0", GREY_A), ("0.8", BLUE), ("1.5", TUNE))])
        cells = VGroup(*[VGroup(label(t, font_size=18, color=c), h).arrange(DOWN, buff=0.3) for t, c, h in
                         ((r"feedback 0: \ a sine", GREY_A, hs[0]), (r"feedback 0.8", BLUE, hs[1]), (r"feedback 1.5", TUNE, hs[2]))]).arrange(RIGHT, buff=1.0)
        sb = harm_bars(saw, width=0.16, gap=0.24, floor=-40.0, height=2.0, color=EAR, labels=False)
        cells.add(VGroup(label(r"a sawtooth: \ $1/k$", font_size=18, color=EAR), sb).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.8).move_to(DOWN * 0.1)
        f15 = fb["1.5"]
        note = label(rf"at 1.5 the 2nd, \ 3rd and 4th harmonics sit at ${f15[1]:.1f}$, \ ${f15[2]:.1f}$, \ ${f15[3]:.1f}$ dB; \ a sawtooth's at $-6.0$, \ $-9.5$, \ $-12.0$", font_size=17, color=WHITE).to_edge(DOWN, buff=0.6)
        cap = label(r"the first 8 harmonics, \ dB re the first, \ from $-40$", font_size=15, color=GREY_A).next_to(cells, UP, buff=0.4)
        head = label(r"an operator modulating itself", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "One wiring is strange: an operator modulating itself, its own output fed back into its phase. "
            "<bookmark mark='a'/> With no feedback it is a sine. <bookmark mark='b'/> Turn the feedback up and harmonics "
            "appear, falling smoothly: <bookmark mark='c'/> at one and a half, the second, third and fourth harmonics sit at "
            f"{say(f15[1], 1)}, {say(f15[2], 1)} and {say(f15[3], 1)} decibels, close to a sawtooth's. One sine and one "
            "feedback path make the subtractive synthesizer's favourite wave."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(cells[2]))
            vo.wait_until("c")
            self.play(FadeIn(cells[3]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("dx")
        c = clip("dx.three")
        cells = VGroup(
            VGroup(algo("pairs")[0].copy().scale(0.7), label(r"electric piano: \ a body pair 1 : 1, \ a tine pair 1 : 14 with a fast-dying index", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2),
            VGroup(VGroup(op_box(2).scale(0.7), op_box(1).scale(0.7)).arrange(DOWN, buff=0.35), label(r"bass: \ 1 : 1 with feedback, \ two octaves down", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2),
            VGroup(VGroup(op_box(2).scale(0.7), op_box(1).scale(0.7)).arrange(DOWN, buff=0.35), label(r"bell: \ 1 : 3.5, \ an octave up", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(UP * 0.2)
        head = label(r"three patches, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three patches on the Tune's first phrase. An electric piano of four operators: a pair at one to one for the body, "
            "and a pair at one to fourteen whose index dies in thirty milliseconds, for the metallic tine at the start of every "
            "note. A bass of two operators with feedback, two octaves down. And a bell at one to three point five, an octave up."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        names = ["epiano", "bass", "bell"]
        with self.listen(c) as snd:
            window(snd, r"three FM patches", kind="synthesized", detail=r"a four-operator engine", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.12)
        with self.voiceover(
            "The electric piano is the sound of a thousand nineteen-eighties ballads: a soft body, a bright ping on top. The "
            "bass is round and punchy, the bell glassy. Each is a handful of numbers: ratios, levels and envelope times."
        ):
            self.play(Indicate(cells[0], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        items = [
            (r"a DX7 voice was 155 parameters, \ set through one slider and a small display", WHITE),
            (r"few players programmed it; \ most used the factory sounds, \ which is why so many records share them", WHITE),
            (r"the electric piano, \ the bass, \ the tubular bells: \ heard on countless records of the 1980s", WHITE),
            (r"FM moved into sound cards and game consoles: \ Part 44's chip music is its cousin", WHITE),
            (r"the hard part was never the arithmetic; \ it was finding the knobs, \ as Part 51's search found", TUNE),
        ]
        rows_scene(self, r"the sound of a decade", items,
                   "FM's success had a side effect. <bookmark mark='b'/> A DX7 voice was a hundred and fifty-five parameters, set "
                   "through one slider and a small display. <bookmark mark='c'/> Few players programmed it; most used the factory "
                   "sounds, which is why so many records share them: <bookmark mark='d'/> the electric piano, the bass, the tubular "
                   "bells. <bookmark mark='e'/> FM then moved into computer sound cards and game consoles, the cousins of Part 44's "
                   "chip music. <bookmark mark='f'/> The hard part was never the arithmetic; it was finding the knobs, as Part 51's "
                   "search found.", marks="bcdef")
