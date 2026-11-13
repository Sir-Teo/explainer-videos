from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Phase(SoundScene):
    def construct(self):
        chapter(self, 4, r"The other half of the recipe", r"Does it matter where each sine starts?", lit=(1863,),
                extra=((1843, r"Ohm's law of hearing"),))
        self.two_numbers()
        self.high()
        self.low()
        self.why()

    def waves(self, d, name, width=5.6, height=1.9):
        out = VGroup()
        for key, col in (("a", TUNE), ("b", AIR)):
            sc = Scope(width=width, height=height, color=col)
            w = d[f"wave_{name}_{key}"]
            sc.set_wave(w, gain=0.9 / float(np.abs(d[f"wave_{name}_a"]).max()))
            out.add(sc)
        return out

    # ------------------------------------------------------------------
    def two_numbers(self):
        d = load("phase")
        term = MathTex(r"b_n", r"\sin(", r"n x", r"+", r"\varphi_n", r")", font_size=56).to_edge(UP, buff=0.6)
        term[0].set_color(TUNE), term[4].set_color(AIR)
        tags = VGroup(label(r"how much", font_size=26, color=TUNE).next_to(term[0], DOWN, buff=0.25),
                      label(r"where in its swing it starts: \ the phase", font_size=26, color=AIR).next_to(term[4], DOWN, buff=0.25).shift(RIGHT * 1.6))
        ws = self.waves(d, "low").arrange(RIGHT, buff=0.7).move_to(DOWN * 1.0)
        caps = VGroup(label(r"every partial starts at its crest", font_size=24, color=TUNE).next_to(ws[0], UP, buff=0.15),
                      label(r"the same partials, \ each starting at random", font_size=24, color=AIR).next_to(ws[1], UP, buff=0.15))
        same = label(rf"the same amounts of the same {d['low']['harmonics']} partials, \ within {d['low']['spectrum_gap_db']:.1f} dB: \ one spectrum, two waves",
                     font_size=26, color=GOOD).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Every sine in Fourier's sum needs two numbers, and so far we have drawn only one. The first is how much "
            "of it there is. <bookmark mark='a'/> The second is where in its swing it starts: its phase. A spectrum "
            "shows the amounts and throws the phases away. <bookmark mark='b'/> Does that matter? Here are two waves "
            "built from exactly the same partials in exactly the same amounts. In the first, every partial starts "
            "at its crest, and they pile up into one sharp spike in each cycle. <bookmark mark='c'/> In the second, "
            "each partial starts at a random point, and the wave looks like noise. Their spectra are identical. "
            "<bookmark mark='d'/> Ohm's law says your ear will not care: same amounts, same sound."
        ) as vo:
            self.play(FadeIn(term), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(FadeIn(ws[0]), FadeIn(caps[0]))
            vo.wait_until("c")
            self.play(FadeIn(ws[1]), FadeIn(caps[1]))
            vo.wait_until("d")
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    def play_pair(self, c, ws, text):
        with self.listen(c) as snd:
            window(snd, text, kind="synthesized", detail=r"the same partials, \ different phases", corner=DL, tag_corner=UR)
            for key, sc, end in (("A", ws[0], snd.time_of("B") - 0.3), ("B", ws[1], c.duration)):
                t0 = snd.time_of(key)
                snd.wait_until(t0)
                frame = SurroundingRectangle(sc, color=EAR, buff=0.08, stroke_width=3)
                snd.show(frame)
                snd.drive(frame, lambda m, t, t0=t0, end=end: m.set_stroke(opacity=(0.55 + 0.45 * np.sin(20 * t)) if t0 <= t < end else 0.0))
                snd.wait_until(end)

    # ------------------------------------------------------------------
    def high(self):
        d = load("phase")
        c = clip("phase.high")
        ws = self.waves(d, "high").arrange(RIGHT, buff=0.7).move_to(UP * 0.4)
        caps = VGroup(label(r"A: \ crests together", font_size=26, color=TUNE).next_to(ws[0], UP, buff=0.15),
                      label(r"B: \ random phases", font_size=26, color=AIR).next_to(ws[1], UP, buff=0.15))
        head = label(rf"a high note ({flat_name(d['high']['note'])}), \ {d['high']['harmonics']} partials", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Test it. First on a high note, the C above middle C, with seven partials. Wave A, then wave B."
        ):
            self.play(FadeIn(head), FadeIn(ws), FadeIn(caps))
        self.play_pair(c, ws, r"A, \ then B: \ the high note")
        with self.voiceover(
            "They sound the same, or very nearly. Ohm was right. Two waves that look nothing alike, and the ear "
            "reports one sound. This is why a spectrum is such a useful picture: it keeps what you hear and drops "
            "what you mostly do not."
        ):
            self.play(Indicate(caps, color=GOOD, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def low(self):
        d = load("phase")
        c = clip("phase.low")
        q = listen_card(r"The same test, \ three octaves lower. \\ A and B have the same partials in the same amounts. \ "
                        r"Do they sound the same?", width=9.8).to_edge(UP, buff=0.5)
        ws = self.waves(d, "low").arrange(RIGHT, buff=0.7).move_to(DOWN * 0.6)
        caps = VGroup(label(r"A", font_size=40, color=TUNE).next_to(ws[0], UP, buff=0.15), label(r"B", font_size=40, color=AIR).next_to(ws[1], UP, buff=0.15))
        with self.voiceover(
            "Now a question for your ears. The same test, three octaves lower, with sixty partials. Same amounts, "
            "different phases. Do A and B sound the same?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(ws), FadeIn(caps))
        self.play_pair(c, ws, r"A, \ then B: \ the low note")
        ans = VGroup(label(r"A buzzes: \ one sharp spike in every cycle", font_size=26, color=TUNE).next_to(ws[0], DOWN, buff=0.2),
                     label(r"B is smoother, \ and breathier", font_size=26, color=AIR).next_to(ws[1], DOWN, buff=0.2))
        with self.voiceover(
            "No. A has a hard buzz to it; B is smoother and breathier. Same spectrum, different sound. So Ohm's law "
            "has a limit, and it is our first piece of evidence that the list of amounts is not everything."
        ):
            self.play(FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d = load("phase")
        line = Line(LEFT * 5.6, RIGHT * 5.6, color=GREY_C, stroke_width=2).move_to(UP * 1.6)
        hi = VGroup(*[Line(ORIGIN, UP * 0.9, color=TUNE, stroke_width=5).move_to(line.get_left() + RIGHT * (0.6 + 1.5 * k) + UP * 0.45) for k in range(7)])
        lo = VGroup(*[Line(ORIGIN, UP * 0.9 / (1 + 0.04 * k), color=AIR, stroke_width=2.5).move_to(line.get_left() + RIGHT * (0.3 + 0.18 * k) + UP * 0.4 + DOWN * 2.6)
                      for k in range(60)])
        line2 = line.copy().shift(DOWN * 2.6)
        band = Rectangle(width=1.3, height=1.3, stroke_color=EAR, stroke_width=2.5, fill_color=EAR, fill_opacity=0.12)
        b1, b2 = band.copy().move_to(hi[3].get_center() + DOWN * 0.0), band.copy().move_to(lo[30].get_center())
        t1 = label(r"the high note: \ partials far apart: \ each of the ear's resonators holds one", font_size=26, color=TUNE).next_to(line, DOWN, buff=0.3)
        t2 = label(r"the low note: \ partials crowded: \ one resonator holds many, \ and hears how they add up", font_size=26, color=AIR).next_to(line2, DOWN, buff=0.3)
        ax = label(r"frequency $\rightarrow$", font_size=22, color=GREY_B).next_to(line, RIGHT, buff=0.1).shift(UP * 0.3 + LEFT * 1.3)
        with self.voiceover(
            "Why the difference? Think of Helmholtz's resonators. <bookmark mark='a'/> On the high note the partials "
            "are far apart. Each of the ear's resonators catches one of them, alone, and one sine wave sounds the "
            "same wherever it starts. <bookmark mark='b'/> On the low note the partials are sixty-five hertz apart, "
            "and the ear's resonators are not that fine. Several partials land in the same one, and it hears how "
            "they add up inside each cycle: a spike, or a smear. <bookmark mark='c'/> So phase is heard exactly "
            "where the ear cannot separate the partials. How fine the ear's resonators are is a measurement, and "
            "it is the heart of Part 4."
        ) as vo:
            self.play(FadeIn(line), FadeIn(hi), FadeIn(line2), FadeIn(lo), FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(t2))
            vo.wait_until("c")
            self.play(Indicate(b2, color=EAR, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()
