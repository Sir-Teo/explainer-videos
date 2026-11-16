from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Alias(SoundScene):
    def construct(self):
        chapter(self, 4, r"Aliasing in nonlinear effects", r"What happens to harmonics above the Nyquist frequency?")
        self.why()
        self.quiz()
        self.cures()
        self.elsewhere()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a digital shaper makes its harmonics inside the computer, \ after the anti-aliasing filter", WHITE),
            (r"a 4 kHz tone's fifth harmonic is 20 kHz; \ its seventh, \ 28 kHz, \ is above the Nyquist frequency", WHITE),
            (r"it folds back down, \ as Part 48 showed: \ 28 kHz at 48 kHz sampling is heard at 20 kHz", WHITE),
            (r"folded harmonics are not harmonics: \ they fall between the notes, \ and move the wrong way", TUNE),
            (r"the harder the drive and the higher the note, \ the worse it gets", GREY_A),
        ]
        rows_scene(self, r"harmonics that fold", items,
                   "Nonlinearity has a digital trap. <bookmark mark='b'/> A digital shaper makes its harmonics inside the computer, "
                   "after the anti-aliasing filter has done its work. <bookmark mark='c'/> A four-kilohertz tone's fifth harmonic is "
                   "twenty kilohertz, but its seventh, twenty-eight, is above the Nyquist frequency, <bookmark mark='d'/> and it "
                   "folds back down, as Part 48 showed: at forty-eight kilohertz sampling, twenty-eight is heard at twenty. "
                   "<bookmark mark='e'/> Folded harmonics are not harmonics: they fall between the notes, and they move the wrong "
                   "way. <bookmark mark='f'/> The harder the drive and the higher the note, the worse it gets.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("alias")
        c = clip("alias.two")
        card = listen_card(r"A sine sweeping up from 500 Hz to 6 kHz through a hard clip, \ twice. \ One was computed at 48 kHz, \ "
                           r"one 8 times faster and filtered down. \ Which has tones that move the wrong way?", width=10.4)
        with self.voiceover(
            "Listen. A sine sweeping up from five hundred hertz to six kilohertz through a hard clip, twice. One was computed "
            "at forty-eight kilohertz, the other eight times faster and filtered back down. In which do you hear tones moving "
            "the wrong way?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        sec = d["seconds"]
        def panel(title, color, raw):
            ax = frame_axes(width=5.2, height=2.6, xlo=0, xhi=sec, ylo=0, yhi=24000, center=ORIGIN)
            ts = np.linspace(0, sec, 300)
            f = d["f0"] + (d["f1"] - d["f0"]) * ts / sec
            g = VGroup(ax, label(title, font_size=19, color=color).next_to(ax, UP, buff=0.15))
            for k in (1, 3, 5, 7, 9, 11):
                fk = k * f
                if raw:
                    fa = np.array([min(v % 48000, 48000 - v % 48000) for v in fk])
                    g.add(curve(ts, fa, ax.to, color=WHITE if k == 1 else (color if np.all(fk < 24000) else EAR), width=2 if k == 1 else 1.2))
                else:
                    keep = fk < 24000
                    if keep.any():
                        g.add(curve(ts[keep], fk[keep], ax.to, color=WHITE if k == 1 else color, width=2 if k == 1 else 1.2))
            return g
        a = panel(r"first", EAR, True)
        b = panel(r"second", TUNE, False)
        grp = VGroup(a, b).arrange(RIGHT, buff=1.0).move_to(UP * 0.1)
        cap = label(r"lines: \ the sweep and its odd harmonics, \ 0 to 24 kHz; \ pink lines have folded", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(card), FadeIn(VGroup(a[0], a[1], b[0], b[1])))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a clipped sweep, \ twice", kind="synthesized", detail=r"a sine, \ hard clip", corner=DL, tag_corner=DR)
            pulse(snd, a[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, b[0], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            "The first. The sweep's high harmonics hit the Nyquist frequency, fold, and come back down as the sweep goes up: "
            "faint tones moving the wrong way, and a grainy whine. Computed eight times faster, the harmonics have room above "
            "hearing, and filtering before decimation removes many high components; finite oversampling does not eliminate every alias from an unlimited-bandwidth shaper."
        ):
            self.play(FadeIn(VGroup(*a[2:])), FadeIn(VGroup(*b[2:])), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cures(self):
        d = load("alias")["measure"]
        rows = [(r"computed at 48 kHz", d["plain"], EAR), (r"antiderivative antialiasing", d["adaa"], BLUE), (r"8 times oversampled", d["x8"], TUNE)]
        bars = VGroup()
        for i, (n, v, col) in enumerate(rows):
            y = 1.0 - 0.9 * i
            w = 7.0 * (-v) / 50.0
            bars.add(VGroup(label(n, font_size=19, color=col).move_to([-1.8, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-1.5 + w / 2, y, 0]),
                            label(rf"{v:.1f} dB", font_size=18, color=WHITE).move_to([-1.5 + w + 0.6, y, 0])))
        cap = label(r"a 3,733 Hz sine through tanh, \ driven 4 times: \ the energy that is not at a harmonic, \ dB below the total \ (longer is better)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"three ways to compute a shaper", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How bad is it, and what cures it? Measure the energy of a driven tone that does not fall on a harmonic. "
            f"<bookmark mark='a'/> Computed plainly at forty-eight kilohertz: {say(-d['plain'], 1)} decibels below the total. "
            "<bookmark mark='b'/> With antiderivative antialiasing, which applies the shaper to the straight line between "
            f"samples and averages it, {say(-d['adaa'], 1)}: a little better, almost for free. <bookmark mark='c'/> Computed eight "
            f"times faster and filtered down: {say(-d['x8'], 1)}. Oversampling costs eight times the work, and buys the most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(VGroup(*[b[0] for b in bars]), 0.3)))
            for mark, b in zip("abc", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def elsewhere(self):
        items = [
            (r"every nonlinear digital process can alias: \ shapers, \ compressors with fast attacks, \ ring modulators", WHITE),
            (r"a compressor whose gain jumps within a cycle is multiplying by a fast signal, \ which makes new frequencies", WHITE),
            (r"a naive square-wave oscillator aliases too: \ its corners are infinitely sharp", WHITE),
            (r"the general cure is the same: \ work at a higher rate, \ or make the new frequencies band-limited from the start", TUNE),
            (r"Part 51 builds oscillators that never alias", GREY_A),
        ]
        rows_scene(self, r"aliasing hides everywhere", items,
                   "Aliasing hides everywhere. <bookmark mark='b'/> Every nonlinear digital process can alias: shapers, compressors "
                   "with fast attacks, ring modulators. <bookmark mark='c'/> A compressor whose gain jumps within a cycle is "
                   "multiplying by a fast signal, and that makes new frequencies. <bookmark mark='d'/> A naive square-wave "
                   "oscillator aliases too, since its corners are infinitely sharp. <bookmark mark='e'/> The general cure is the "
                   "same: work at a higher rate, or make the new frequencies band-limited from the start. <bookmark mark='f'/> Part "
                   "51 builds oscillators that never alias.", marks="bcdef")
