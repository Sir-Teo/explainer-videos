from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403

KCOL = {"0.0": GREY_A, "1.0": BLUE, "2.0": "#A3E635", "3.0": GOLD, "3.8": EAR}


class Ladder(SoundScene):
    def construct(self):
        chapter(self, 4, r"The ladder filter", r"What made the Moog sound like a Moog?")
        self.rungs()
        self.algebra()
        self.curves()
        self.edge()
        self.bass()
        self.heard()

    # ------------------------------------------------------------------
    def rungs(self):
        stages = VGroup()
        for j in range(4):
            r = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.12, stroke_color=BLUE)
            stages.add(VGroup(r, MathTex(r"\frac{1}{1 + s/\omega_c}", font_size=26)).arrange(ORIGIN))
        stages.arrange(RIGHT, buff=0.7).move_to(UP * 0.6)
        arr = VGroup(*[Arrow(stages[j].get_right(), stages[j + 1].get_left(), buff=0.08, color=GREY_B, stroke_width=3) for j in range(3)])
        inp = VGroup(label(r"in", font_size=20, color=WHITE), Circle(radius=0.22, stroke_color=WHITE).next_to(stages[0], LEFT, buff=0.7))
        inp[0].next_to(inp[1], LEFT, buff=0.4)
        sumtxt = MathTex(r"-", font_size=26).move_to(inp[1])
        a0 = Arrow(inp[1].get_right(), stages[0].get_left(), buff=0.05, color=GREY_B, stroke_width=3)
        out = Arrow(stages[3].get_right(), stages[3].get_right() + RIGHT * 0.9, buff=0.05, color=GREY_B, stroke_width=3)
        ol = label(r"out", font_size=20, color=WHITE).next_to(out, RIGHT, buff=0.1)
        fb_y = stages.get_bottom()[1] - 0.8
        fb = VMobject(stroke_color=EAR, stroke_width=3).set_points_as_corners([stages[3].get_right() + RIGHT * 0.45, [stages[3].get_right()[0] + 0.45, fb_y, 0],
                                                                                [inp[1].get_center()[0], fb_y, 0], inp[1].get_bottom()])
        kl = label(r"$\times k$: \ the resonance knob", font_size=18, color=EAR).next_to(fb, DOWN, buff=0.15)
        info = VGroup(label(r"Robert Moog's patent, \ filed 1966: \ transistor pairs stacked like the rungs of a ladder", font_size=18, color=WHITE),
                      label(r"each rung a one-pole low-pass, \ 6 dB an octave; \ four in a row, \ 24", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        head = label(r"four poles and a loop", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The filter that made the Moog sound like a Moog is a ladder. <bookmark mark='a'/> Robert Moog's patent, filed in "
            "1966, stacks pairs of transistors like the rungs of a ladder, and each rung, with a capacitor, is a one-pole "
            "low-pass: it falls six decibels an octave above its cutoff. <bookmark mark='b'/> Four in a row fall twenty-four. "
            "<bookmark mark='c'/> And the output is fed back to the input, inverted and multiplied by k: the resonance knob."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(stages, arr), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(stages[0]), FadeIn(info[0]))
            vo.wait_until("b")
            self.play(FadeIn(stages[1:]), FadeIn(arr), FadeIn(info[1]), FadeIn(inp), FadeIn(sumtxt), FadeIn(a0), FadeIn(out), FadeIn(ol))
            vo.wait_until("c")
            self.play(Create(fb), FadeIn(kl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        lines = VGroup(
            MathTex(r"G(s) = \frac{1}{1 + s/\omega_c}", font_size=36),
            MathTex(r"Y = G^4\,(X - kY)", font_size=36),
            MathTex(r"H(s) = \frac{Y}{X} = \frac{G^4}{1 + kG^4} = \frac{1}{(1 + s/\omega_c)^4 + k}", font_size=36),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        notes = VGroup(label(r"one rung", font_size=18, color=GREY_A).next_to(lines[0], RIGHT, buff=0.6),
                       label(r"four rungs, \ with the output subtracted", font_size=18, color=GREY_A).next_to(lines[1], RIGHT, buff=0.6),
                       label(r"the whole filter", font_size=18, color=TUNE).next_to(lines[2], DOWN, buff=0.3))
        head = label(r"the linear ladder in three lines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "At low levels the circuit is linear, and the algebra takes three lines. <bookmark mark='a'/> One rung is one over "
            "one plus s over omega c. <bookmark mark='b'/> Four in a row, with k times the output subtracted at the input: Y "
            "equals G to the fourth times X minus k Y. <bookmark mark='c'/> Solve for Y over X: one over one plus s over "
            "omega c, to the fourth, plus k. Everything about the filter's shape is in that denominator."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("ladder")
        f = np.array(d["f"])
        ax = logf_axes(width=8.4, height=4.2, flo=20, fhi=20000, ylo=-60, yhi=20, center=LEFT * 1.2 + DOWN * 0.3)
        cs = VGroup(*[curve(f, np.maximum(np.array(d["resp"][k]), -60), ax.to, color=KCOL[k], width=3) for k in ("0.0", "1.0", "2.0", "3.0", "3.8")])
        key = VGroup(*[label(rf"$k = {float(k):g}$", font_size=18, color=KCOL[k]) for k in ("0.0", "1.0", "2.0", "3.0", "3.8")]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5)
        yt = VGroup(*[label(f"{v:+d}" if v else "0", font_size=14, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.1) for v in (20, 0, -20, -40, -60)])
        cut = DashedLine(ax.to(1000, -60), ax.to(1000, 20), color=WHITE, stroke_width=1, stroke_opacity=0.5)
        cl = label(r"cutoff, \ 1 kHz", font_size=15, color=GREY_A).next_to(ax.to(1000, 20), UP, buff=0.08)
        pk = d["peak"]["3.8"]
        pl = label(rf"$+{pk['db']:.1f}$ dB", font_size=17, color=EAR).next_to(ax.to(pk["f"], pk["db"]), UR, buff=0.08)
        head = label(r"the ladder's response, \ five settings of $k$", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Draw it for a cutoff of one kilohertz. <bookmark mark='a'/> With no feedback, the response is flat below the cutoff, "
            "twelve decibels down at it, and falling twenty-four decibels an octave above. <bookmark mark='b'/> Turn k up to one, "
            "two, three: a hump grows at the cutoff. <bookmark mark='c'/> At three point eight it is a peak "
            f"{say(pk['db'], 1)} decibels high, a narrow band that rings. And look at the left end of the curves: as the "
            "peak rises, the bass falls."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(cut), FadeIn(cl), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cs[1:4]], lag_ratio=0.4), FadeIn(key[1:4]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cs[4]), FadeIn(key[4]), FadeIn(pl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        lines = VGroup(
            MathTex(r"\text{at } s = j\omega_c: \quad 1 + j = \sqrt{2}\,e^{j\pi/4}", font_size=34),
            MathTex(r"(1 + j)^4 = 4\,e^{j\pi} = -4", font_size=34),
            MathTex(r"(1 + j)^4 + k = k - 4", font_size=34),
            MathTex(r"k = 4: \ \text{the denominator vanishes; the filter rings by itself}", font_size=34),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        side = label(r"each rung delays the cutoff frequency by 45 degrees; \ four make 180: \ the feedback stops subtracting and adds", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"why four is the edge", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why does it ring? <bookmark mark='a'/> At the cutoff frequency, each rung's factor is one plus j: a gain of one over "
            "root two and a phase lag of forty-five degrees. <bookmark mark='b'/> Four rungs lag a hundred and eighty degrees, "
            "and one plus j to the fourth is exactly minus four. <bookmark mark='c'/> So the denominator at the cutoff is k "
            "minus four. <bookmark mark='d'/> At k equals four it vanishes: the subtracted feedback has turned round and adds, "
            "and the filter oscillates with no input at all, at its cutoff. Moog's players found this edge and used it, as we "
            "will in the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass(self):
        d = load("ladder")
        ks = ["0", "1", "2", "3", "3.8"]
        vals = [d["dc"][k] for k in ks]
        ax = frame_axes(width=6.0, height=3.0, xlo=-0.5, xhi=4.5, ylo=-16, yhi=0, center=LEFT * 2.0 + DOWN * 0.3)
        bars = VGroup()
        for i, v in enumerate(vals):
            h = 3.0 * (-v) / 16
            bars.add(Rectangle(width=0.6, height=max(h, 0.03), stroke_width=0, fill_color=EAR, fill_opacity=0.8).move_to(ax.to(i, 0) + DOWN * max(h, 0.03) / 2))
        bl = VGroup(*[label(rf"$k={k}$", font_size=16, color=GREY_A).next_to(ax.to(i, 0), UP, buff=0.12) for i, k in enumerate(ks)])
        vl = VGroup(*[label(f"{v:.1f}", font_size=15, color=WHITE).next_to(b, DOWN, buff=0.08) for b, v in zip(bars, vals)])
        eq = MathTex(r"H(0) = \frac{1}{1 + k}", font_size=40).move_to(RIGHT * 3.6 + UP * 0.8)
        txt = VGroup(label(r"the bass level, \ dB", font_size=18, color=GREY_A),
                     label(r"at $k = 3$, \ the bass is a quarter of its amplitude", font_size=17, color=WHITE),
                     label(r"players heard it as the resonance thinning the sound", font_size=17, color=GREY_A),
                     label(r"later designs add some input back to keep the bass", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.5)
        head = label(r"resonance costs bass", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The bass loss is in the denominator too. <bookmark mark='a'/> At zero frequency every rung passes everything, and "
            "H of zero is one over one plus k. <bookmark mark='b'/> At k equals three the bass is a quarter of its amplitude, "
            f"{say(-d['dc']['3'], 1)} decibels down. Players heard it as the resonance thinning the sound, and later designs "
            "add a little of the input back to keep the bass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bl), FadeIn(ghost(bars, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in bars], lag_ratio=0.2), FadeIn(vl), FadeIn(txt[1:]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ladder3")
        c = clip("ladder.three")
        cells = choice_boxes([r"$k = 0$", r"$k = 2$", r"$k = 3.7$"], width=3.0, buff=0.7, colors=[GREY_A, "#A3E635", EAR]).move_to(UP * 0.4)
        cap = label(r"a sawtooth bass, \ two octaves below middle C, \ through the ladder at 500 Hz, \ opened by a pluck envelope", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three resonances, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it on a bass line: the Tune's first phrase two octaves below middle C, through the ladder at five hundred "
            "hertz, opened by a pluck envelope on every note. Feedback zero, two, and three point seven."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        names = ["k0", "k2", "k37"]
        with self.listen(c) as snd:
            window(snd, r"three resonances", kind="synthesized", detail=r"sawtooth and ladder", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "At zero it is round and plain. At two each note gains a vowel, a wah as the envelope sweeps the hump through the "
            "harmonics. At three point seven every note chirps, the filter ringing at the cutoff as it falls, and the bass "
            "underneath has thinned: the classic acid squelch, and the price of it."
        ):
            self.play(Indicate(cells[2], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()
