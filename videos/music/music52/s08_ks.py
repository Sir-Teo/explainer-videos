from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Ks(SoundScene):
    def construct(self):
        chapter(self, 7, r"Karplus--Strong, \ tuned", r"Why does the simplest string go out of tune at the top?")
        self.loop()
        self.error()
        self.allpass()
        self.heard()
        self.extensions()

    # ------------------------------------------------------------------
    def loop(self):
        cells = VGroup()
        n = 12
        rng = np.random.default_rng(3)
        vals = rng.uniform(-1, 1, n)
        for i, v in enumerate(vals):
            cells.add(Rectangle(width=0.55, height=0.55, stroke_color=GREY_B, stroke_width=1.5, fill_color=TUNE if v > 0 else BLUE, fill_opacity=0.25 + 0.6 * abs(v)))
        cells.arrange(RIGHT, buff=0.05).move_to(UP * 0.6)
        avg = VGroup(RoundedRectangle(width=1.8, height=0.7, corner_radius=0.12, stroke_color=EAR), label(r"average two", font_size=17, color=EAR)).arrange(ORIGIN).next_to(cells, DOWN, buff=0.9)
        a1 = Arrow(cells.get_right() + DOWN * 0.1, avg.get_right() + RIGHT * 0.1, buff=0.1, color=GREY_B, path_arc=-1.2)
        a2 = Arrow(avg.get_left() + LEFT * 0.1, cells.get_left() + DOWN * 0.1, buff=0.1, color=GREY_B, path_arc=-1.2)
        notes = VGroup(label(r"a delay line one period long, \ filled with noise", font_size=18, color=WHITE),
                       label(r"round and round, \ each pass averaging neighbours: \ the highs die first, \ as on a plucked string", font_size=18, color=GREY_A),
                       label(r"Kevin Karplus and Alex Strong \ (1983): \ a plucked string in a few lines \ (Part 7)", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        head = label(r"a string in a loop", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Physical models start with the simplest one, met in Part 7. <bookmark mark='a'/> Fill a delay line one period long "
            "with noise. <bookmark mark='b'/> Send it round and round, and on each pass average neighbouring samples, so the high "
            "frequencies die faster than the low, as on a plucked string. <bookmark mark='c'/> Kevin Karplus and Alex Strong "
            "published it in 1983: a plucked string in a few lines of code, a remarkably economical plucked-string algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(cells, avg), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(avg), Create(a1), Create(a2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def error(self):
        d = load("ks")
        notes = d["notes"]
        ax = frame_axes(width=9.0, height=3.4, xlo=58, xhi=98, ylo=-20, yhi=36, center=DOWN * 0.3 + LEFT * 0.6)
        a = stems(notes, d["untuned"], ax.to, color=EAR, r=0.06)
        b = stems(np.array(notes) + 0.6, d["tuned"], ax.to, color=TUNE, r=0.06)
        xt = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(ax.to(m, -20), DOWN, buff=0.1) for m, n in ((60, "C4"), (72, "C5"), (84, "C6"), (96, "C7"))])
        yt = VGroup(*[label(f"{v:+d}" if v else "0", font_size=14, color=GREY_A).next_to(ax.to(58, v), LEFT, buff=0.1) for v in (-20, 0, 20)])
        yl = label(r"error, \ cents", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        key = VGroup(label(r"delay rounded to whole samples", font_size=17, color=EAR), label(r"with an all-pass for the fraction", font_size=17, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        eq = MathTex(r"f = \frac{f_s}{N + \tfrac12}", font_size=34).next_to(key, DOWN, buff=0.5)
        worst = max(d["untuned"], key=abs)
        head = label(r"tuning, \ note by note \ (48 kHz)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "But the basic loop cannot play in tune. <bookmark mark='a'/> Its period is a whole number of samples, plus half a "
            "sample for the averaging, so the pitch is the sample rate over N plus a half, and N must be a whole number. At "
            "middle C, N is about a hundred and eighty, and rounding costs a few cents; but at C seven, N is under twenty-three, "
            f"and the error reaches {say(abs(worst))} cents, a third of a semitone. <bookmark mark='b'/> Add an all-pass filter "
            f"that supplies the missing fraction of a sample, and every note lands within {say(max(abs(x) for x in d['tuned']), 1)} "
            "of a cent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(key[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def allpass(self):
        lines = VGroup(
            MathTex(r"H(z) = \frac{c + z^{-1}}{1 + c\,z^{-1}} \qquad |H| = 1", font_size=36),
            MathTex(r"\text{delay at low frequencies} \approx \frac{1 - c}{1 + c} \;\Rightarrow\; c = \frac{1 - \Delta}{1 + \Delta}", font_size=36),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        notes = VGroup(label(r"Part 49's first-order all-pass: \ every frequency through at full strength, \ only delayed", font_size=18, color=WHITE),
                       label(r"choose $c$ so the delay is the missing fraction $\Delta$ of a sample", font_size=18, color=TUNE),
                       label(r"David Jaffe and Julius Smith \ (1983) \ added it, \ with controls for decay and brightness", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"a fraction of a sample", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The fix is Part 49's first-order all-pass. <bookmark mark='a'/> It passes every frequency at full strength and only delays it, and at low frequencies the delay is one minus c over one plus c samples. <bookmark mark='b'/> Choose c to supply the missing delay at low frequencies; a first-order all-pass has frequency-dependent delay. <bookmark mark='c'/> David Jaffe and Julius Smith added this in the same year, 1983, with controls for decay time and brightness, and turned a trick into an instrument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ks")
        c = clip("ks.two")
        cells = choice_boxes([r"rounded", r"tuned by the all-pass"], width=3.8, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(r"the Tune's first phrase, \ C6 to A6, \ on Karplus--Strong strings", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"in and out of tune, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the Tune's first phrase two octaves above middle C, first with the delay rounded, then tuned."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"rounded, \ then tuned", kind="physical model", detail=r"Karplus--Strong", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["untuned"], st["tuned"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["tuned"], c.duration, buff=0.08)
        with self.voiceover(
            "With the delay rounded, the melody's intervals are subtly wrong, each note off by a different amount; tuned, it "
            "sits in place. The same rounding generally produces smaller pitch errors on bass notes. At the top of the keyboard it is the difference between an "
            "instrument and a toy."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extensions(self):
        items = [
            (r"a loss factor in the loop sets the decay time; \ a gentler average keeps more highs", WHITE),
            (r"a pluck position comb \ (Part 1's missing harmonics) \ and a pick's brightness shape the noise before it starts", WHITE),
            (r"a soft clipper in the loop gives distortion that rings with the string: \ an electric guitar", WHITE),
            (r"but what exactly is the loop? \ the string's travelling waves, \ which d'Alembert found in 1747", TUNE),
            (r"the next chapter makes that exact", GREY_A),
        ]
        rows_scene(self, r"more from one loop", items,
                   "One loop goes a long way. <bookmark mark='b'/> A loss factor sets the decay time, and a gentler average keeps "
                   "more highs. <bookmark mark='c'/> A comb for the pluck position, Part 1's missing harmonics, and a pick's "
                   "brightness shape the noise before it starts. <bookmark mark='d'/> A soft clipper inside the loop gives "
                   "distortion that rings with the string: an electric guitar. <bookmark mark='e'/> But what exactly is the loop? "
                   "The string's travelling waves, which d'Alembert found in 1747. <bookmark mark='f'/> The next chapter makes that "
                   "exact.", marks="bcdef")
