from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Jitter(SoundScene):
    def construct(self):
        chapter(self, 9, r"Jitter and clocks", r"What if the samples are taken at slightly the wrong times?")
        self.slope()
        self.table()
        self.sidebands()
        self.practice()

    # ------------------------------------------------------------------
    def slope(self):
        ax = frame_axes(width=10.0, height=3.2, xlo=0, xhi=1.0, ylo=-1.2, yhi=1.2, center=DOWN * 0.3)
        tt = np.linspace(0, 1, 400)
        w = curve(tt, np.sin(2 * np.pi * 2 * tt), ax.to, color=WHITE, width=3)
        t0 = 0.5 / 2 / 2 * 0 + 0.0
        tz = 0.5
        e = 0.03
        p1, p2 = ax.to(tz, np.sin(2 * np.pi * 2 * tz)), ax.to(tz + e, np.sin(2 * np.pi * 2 * (tz + e)))
        mark = VGroup(Dot(p1, radius=0.08, color=TUNE), Dot(p2, radius=0.08, color=EAR),
                      Line(ax.to(tz, -1.2), ax.to(tz, 1.2), color=TUNE, stroke_width=1.5, stroke_opacity=0.6),
                      Line(ax.to(tz + e, -1.2), ax.to(tz + e, 1.2), color=EAR, stroke_width=1.5, stroke_opacity=0.6),
                      Brace(Line(p2, [p2[0], p1[1], 0]), RIGHT, color=EAR))
        eq = MathTex(r"\text{error} \approx \text{slope} \times \text{timing error}, \qquad \mathrm{SNR} = -20\log_{10}(2\pi f \sigma_t)", font_size=34).to_edge(DOWN, buff=0.5)
        head = label(r"a sample taken late", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The theorem assumes samples taken at exactly equal times. A real clock wobbles: that is jitter. "
            "<bookmark mark='a'/> A sample taken a little late reads the wave a little further along. Where the wave is "
            "steep, the error is large; where it is flat, small. <bookmark mark='b'/> So the error is the slope times the timing "
            "error, and for a sine of frequency f, with random timing errors of size sigma, the signal-to-noise ratio is minus "
            "twenty log ten of two pi f sigma: high frequencies, being steepest, suffer most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), Create(w))
            vo.wait_until("a")
            self.play(FadeIn(mark))
            vo.wait_until("b")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("jitter")
        rows = d["rows"]
        names = {1e-10: r"100 picoseconds", 1e-9: r"1 nanosecond", 1e-8: r"10 nanoseconds", 1e-7: r"100 nanoseconds"}
        g = VGroup(VGroup(label(r"timing error \ (rms)", font_size=19, color=GREY_A), label(r"predicted", font_size=19, color=GREY_A), label(r"measured", font_size=19, color=GREY_A)))
        for r in rows:
            g.add(VGroup(label(names[r["sigma"]], font_size=21, color=WHITE), label(rf"{r['theory']:.1f} dB", font_size=21, color=GREY_A), label(rf"{r['measured']:.1f} dB", font_size=21, color=TUNE)))
        for i, row in enumerate(g):
            y = 1.6 - 0.75 * i
            row[0].move_to([-3.0, y, 0])
            row[1].move_to([0.8, y, 0])
            row[2].move_to([3.6, y, 0])
        head = label(r"a 10 kHz sine, \ sampled at 48 kHz with jitter", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"each row: \ one second of samples, \ each taken at a random time error of the stated size", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Check the formula on a ten-kilohertz sine. <bookmark mark='a'/> With a hundred picoseconds of jitter, the formula "
            f"predicts {say(rows[0]['theory'], 1)} decibels and we measure {say(rows[0]['measured'], 1)}. <bookmark mark='b'/> "
            f"One nanosecond: {say(rows[1]['measured'], 1)}. <bookmark mark='c'/> Ten: {say(rows[2]['measured'], 1)}. "
            f"<bookmark mark='d'/> A hundred: {say(rows[3]['measured'], 1)}. To keep a ten-kilohertz tone as clean as sixteen "
            "bits allow, the clock must hold its timing to about two hundred picoseconds, a hundred-thousandth of a sample."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(cap), FadeIn(ghost(g[1:], 0.15)))
            for mark, row in zip("abcd", g[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(row))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sidebands(self):
        d = load("sidebands")
        fr = np.array(d["fr"])
        ax = frame_axes(width=10.0, height=3.2, xlo=fr[0], xhi=fr[-1], ylo=-160, yhi=0, center=DOWN * 0.4)
        P = np.array(d["P"]) - max(d["P"])
        P0 = np.array(d["P0"]) - max(d["P0"])
        c0 = curve(fr, np.clip(P0, -160, 0), ax.to, color=GREY_A, width=2)
        c1 = curve(fr, np.clip(P, -160, 0), ax.to, color=EAR, width=2.5)
        ticks = VGroup(*[label(f"{v / 1000:g} k", font_size=15, color=GREY_A).next_to(ax.to(v, -160), DOWN, buff=0.12) for v in (8000, 9000, 10000, 11000, 12000)])
        tags = VGroup(label(r"sidebands at 9 and 11 kHz", font_size=17, color=EAR).next_to(ax.to(11000, d["measured"]), UR, buff=0.15))
        key = VGroup(label(r"grey: \ a perfect clock", font_size=16, color=GREY_A), label(r"pink: \ the clock wobbling 10 ns, \ 1,000 times a second", font_size=16, color=EAR)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)
        head = label(r"jitter with a rhythm of its own", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Random jitter adds noise. Jitter with a rhythm of its own does something else. <bookmark mark='a'/> Here is a "
            "ten-kilohertz sine sampled by a perfect clock: one line. <bookmark mark='b'/> Now let the clock wobble by ten "
            "nanoseconds, a thousand times a second. Two new tones appear, at nine and eleven kilohertz: sidebands. Theory "
            f"puts them at twenty log ten of pi f a, {say(d['predicted'], 1)} decibels below the tone; we measure "
            f"{say(d['measured'], 1)}. Faint, but they are tones, not noise, and they move with the music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(c0))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(key[1]), FadeIn(tags))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"jitter matters only at the moments of conversion: \ in the A-to-D and the D-to-A", WHITE),
            (r"data copied between devices is not changed by jitter on the way, \ provided every bit arrives", WHITE),
            (r"real jitter is not always random: \ periodic wobble makes sidebands, \ tones either side of each tone", WHITE),
            (r"good converters recover a clean clock, \ often with a phase-locked loop, \ before converting", TUNE),
            (r"an engineering problem, \ largely solved: \ but the formula says where to look when it is not", GREY_A),
        ]
        rows_scene(self, r"jitter in practice", items,
                   "Where does jitter matter? <bookmark mark='b'/> Only at the moments of conversion: in the analogue-to-digital "
                   "and the digital-to-analogue converter. <bookmark mark='c'/> Data copied between devices is not changed by "
                   "jitter on the way, provided every bit arrives. <bookmark mark='d'/> Real jitter is not always random: a "
                   "periodic wobble makes sidebands, faint tones either side of every tone. <bookmark mark='e'/> Good converters "
                   "recover a clean clock, often with a phase-locked loop, before converting. <bookmark mark='f'/> It is an "
                   "engineering problem, largely solved; the formula says where to look when it is not.", marks="bcdef")
