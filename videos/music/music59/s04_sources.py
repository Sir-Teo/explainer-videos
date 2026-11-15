from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Sources(SoundScene):
    def construct(self):
        chapter(self, 3, r"Point and line sources", r"Why does a line of loudspeakers carry further than one?")
        self.inverse()
        self.curves()
        self.transition()
        self.limits()

    # ------------------------------------------------------------------
    def inverse(self):
        items = [
            (r"a point source spreads its power over a sphere: \ area $4\pi r^2$", WHITE),
            (r"intensity falls as $1/r^2$: \ 6 dB less for every doubling of distance", WHITE),
            (r"from 10 m to 80 m, \ three doublings: \ 18 dB: \ the front row deafened or the back row starved", WHITE),
            (r"a long line source spreads over a cylinder: \ area $2\pi r L$; \ intensity as $1/r$: \ 3 dB per doubling", TUNE),
        ]
        rows_scene(self, r"spheres and cylinders", items,
                   "The trouble in a stadium is distance. <bookmark mark='b'/> A point source spreads its power over a sphere whose "
                   "area grows as r squared, <bookmark mark='c'/> so its intensity falls six decibels for every doubling of "
                   "distance. <bookmark mark='d'/> From ten metres to eighty is three doublings, eighteen decibels: the front row "
                   "deafened, or the back row starved. <bookmark mark='e'/> But a long line of sources spreads over a cylinder, "
                   "whose area grows only as r: three decibels per doubling.", marks="bcde")

    # ------------------------------------------------------------------
    def curves(self):
        d = load("arrays")
        dist = np.array(d["dists"])
        ax = frame_axes(width=9.0, height=3.2, xlo=np.log10(2), xhi=np.log10(200), ylo=-40, yhi=5, center=DOWN * 0.3 + LEFT * 0.6)

        def cv(c, col, w=3):
            c = np.array(c)
            ref = float(np.interp(4.0, dist, c))
            return curve(np.log10(dist), np.clip(c - ref, -40, 5), ax.to, color=col, width=w)
        pt = cv(d["curves"]["1000"]["point"], GREY_A)
        l250 = cv(d["curves"]["250"]["line"], BLUE)
        l1k = cv(d["curves"]["1000"]["line"], TUNE)
        xt = VGroup(*[label(f"{v} m", font_size=14, color=GREY_A).next_to(ax.to(np.log10(v), -40), DOWN, buff=0.1) for v in (2, 4, 8, 16, 32, 64, 128)])
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(np.log10(2), v), LEFT, buff=0.1) for v in (0, -20, -40)])
        key = VGroup(label(r"one point source", font_size=16, color=GREY_A), label(rf"a {d['length']:.1f} m line, \ 250 Hz", font_size=16, color=BLUE),
                     label(rf"the same line, \ 1 kHz", font_size=16, color=TUNE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        pdb = d["per_doubling"]
        note = label(rf"per doubling: \ point {pdb['1000']['point']:.1f} dB; \ line at 1 kHz {pdb['1000']['line_near']:.1f} dB close in; \ at 250 Hz {pdb['250']['line_near']:.1f} dB, \ then {pdb['250']['line_far']:.1f} past 26 m",
                     font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"level against distance", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here it is computed: {say(d['n'])} sources in a vertical line {say(d['length'], 1)} metres long, against one, "
            "on a logarithmic scale of distance, each a third-octave average. <bookmark mark='a'/> The point source falls six "
            "decibels at every doubling. <bookmark mark='b'/> The line at one kilohertz falls under three, all the way out "
            "past a hundred metres. <bookmark mark='c'/> At two hundred and fifty hertz the line falls at three decibels at "
            "first, then bends to six beyond about twenty-six metres: far enough away, every line looks like a point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(note), FadeIn(ghost(VGroup(pt, l250, l1k), 0.25)))
            vo.wait_until("a")
            self.play(Create(pt), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(l1k), FadeIn(key[2]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(l250), FadeIn(key[1]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transition(self):
        d = load("arrays")
        eq = MathTex(r"d_t \approx \frac{L^2 f}{2c}", font_size=44, color=TUNE).move_to(UP * 1.6)
        rows = VGroup(VGroup(label(r"frequency", font_size=17, color=GREY_A), label(r"the line behaves as a line out to", font_size=17, color=GREY_A)))
        for f in ("250", "1000", "4000"):
            rows.add(VGroup(label(f"{int(f)} Hz", font_size=19, color=WHITE), label(f"about {d['transition'][f]:.0f} m", font_size=19, color=TUNE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].set_x(-2.4)
            r[1].set_x(1.8)
        rows.move_to(DOWN * 0.4)
        note = label(rf"for a {d['length']:.1f} m line: \ the higher the frequency, \ the further the cylinder reaches", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"the transition distance", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How far does a line act as a line? <bookmark mark='a'/> Roughly to the transition distance, its length squared "
            "times the frequency over twice the speed of sound. <bookmark mark='b'/> For our eight-metre line: about "
            f"{say(d['transition']['250'])} metres at two hundred and fifty hertz, about {say(d['transition']['1000'])} at a "
            "kilohertz, and four hundred at four kilohertz. So a line array throws its treble much further than its bass, which "
            "is one reason arenas need subwoofers of their own and why the mix changes along the room."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        d = load("arrays")
        pdb = d["per_doubling"]["4000"]
        items = [
            (rf"the elements must be close: \ less than half a wavelength apart to act as one line \ (here {d['spacing'] * 100:.0f} cm: \ up to about {d['half_wave_hz']:.0f} Hz, \ with care to 1 kHz or so)", WHITE),
            (rf"at 4 kHz our line of separate sources falls {pdb['line_near']:.1f} dB per doubling: \ no better than a point", WHITE),
            (r"the cure: \ a waveguide in each box that turns its tweeter into a flat, \ continuous strip of sound, \ edge to edge with the next", WHITE),
            (r"Christian Heil and Marcel Urban's `wavefront sculpture' \ (1992): \ the rules that made the modern line array", TUNE),
        ]
        rows_scene(self, r"a line, \ or a row of points", items,
                   "There is a condition. <bookmark mark='b'/> The elements must be close: less than half a wavelength apart to act "
                   f"as one line. Our boxes are {say(d['spacing'] * 100)} centimetres apart, which strictly holds only to about five "
                   "hundred hertz, and with care to a kilohertz or so. <bookmark mark='c'/> At four kilohertz our line of separate "
                   f"sources falls {say(pdb['line_near'], 1)} decibels per doubling: no better than a point. <bookmark mark='d'/> The "
                   "cure is a waveguide in each box that turns its tweeter into a flat, continuous strip of sound, edge to edge with "
                   "the next box's. <bookmark mark='e'/> Christian Heil and Marcel Urban set out these rules as wavefront sculpture "
                   "in 1992, and they made the modern line array.", marks="bcde")
