from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403

GC = {"5": EAR, "20": TUNE, "80": BLUE}


class Grains(SoundScene):
    def construct(self):
        chapter(self, 4, r"Granular synthesis", r"What if a sound were made of tiny pieces?")
        self.gabor()
        self.uncertainty()
        self.engine()
        self.heard()
        self.cloud()
        self.history()

    # ------------------------------------------------------------------
    def gabor(self):
        items = [
            (r"1946--47: \ Dennis Gabor describes sound as a grid of `acoustical quanta': \ short tone bursts, \ each a sine in a bell-shaped window", WHITE),
            (r"Fourier's sines last forever; \ Gabor's last milliseconds: \ a sound is a mosaic of them", WHITE),
            (r"Iannis Xenakis composed with clouds of grains on tape \ (1959; \ Part 30)", WHITE),
            (r"Curtis Roads ran the first computer granular synthesis \ (1975); \ Barry Truax made it run live \ (1986)", WHITE),
            (r"granular synthesis: \ make sounds by scattering thousands of grains", TUNE),
        ]
        rows_scene(self, r"acoustical quanta", items,
                   "A different idea of sound began in physics. <bookmark mark='b'/> In 1946 and 1947 Dennis Gabor, who later "
                   "invented holography, described sound as a grid of acoustical quanta: short tone bursts, each a sine inside a "
                   "bell-shaped window. <bookmark mark='c'/> The Fourier-series basis is indefinitely sustained; Gabor used windowed tones, and a sound is "
                   "a mosaic of them. <bookmark mark='d'/> Iannis Xenakis composed with clouds of grains cut from tape in 1959, as "
                   "Part 30 told. <bookmark mark='e'/> Curtis Roads ran the first computer granular synthesis in 1975, and Barry "
                   "Truax made it run live in 1986. <bookmark mark='f'/> Granular synthesis makes sounds by scattering thousands of "
                   "grains.", marks="bcdef")

    # ------------------------------------------------------------------
    def uncertainty(self):
        d = load("gabor")
        cells = VGroup()
        for r in d["rows"]:
            k = str(int(r["ms"]))
            sh = d["shapes"][k]
            w = wave_path(np.array(sh["y"]), width=3.0, height=1.0, color=GC[k], stroke=1.6)
            sf, sp = np.array(sh["spec_f"]), np.array(sh["spec"])
            ax = frame_axes(width=3.0, height=1.2, xlo=0, xhi=2000, ylo=0, yhi=1.05)
            cells.add(VGroup(label(rf"{r['ms']:.0f} ms", font_size=22, color=GC[k]), w, VGroup(ax, curve(sf, sp, ax.to, color=GC[k], width=2.5)),
                             label(rf"{r['bw']:.0f} Hz wide", font_size=17, color=WHITE)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.8).move_to(UP * 0.1)
        cap = label(r"three grains at 1 kHz \ (length: \ width at half height); \ below each, \ its spectrum from 0 to 2 kHz", font_size=15, color=GREY_A).next_to(cells, UP, buff=0.3)
        rule = label(rf"length $\times$ width $\approx {np.mean([r['product'] for r in d['rows']]):.2f}$, \ for these Gaussian grains and width definitions", font_size=19, color=TUNE).to_edge(DOWN, buff=0.5)
        head = label(r"short in time, \ wide in frequency", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        rows = d["rows"]
        with self.voiceover(
            "Every grain trades time for frequency. <bookmark mark='a'/> A grain five milliseconds long, a click with a hint of "
            f"pitch, spreads over {say(rows[0]['bw'])} hertz. <bookmark mark='b'/> Twenty milliseconds: {say(rows[1]['bw'])} "
            f"hertz. Eighty milliseconds: {say(rows[2]['bw'])}, a clear tone. <bookmark mark='c'/> Length times width stays near "
            f"{say(np.mean([r['product'] for r in rows]), 2)}: a width-duration product under these chosen width definitions; the uncertainty principle gives a lower bound when widths are defined as standard deviations. A "
            "grain's length decides whether you hear its pitch, or only its click."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(cells[2]))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def engine(self):
        knobs = VGroup(*[VGroup(RoundedRectangle(width=2.5, height=1.0, corner_radius=0.12, stroke_color=c), VGroup(label(t, font_size=19, color=c), label(s, font_size=13, color=GREY_A)).arrange(DOWN, buff=0.08)).arrange(ORIGIN)
                         for t, s, c in ((r"position", r"where in the source", TUNE), (r"density", r"grains a second", BLUE), (r"length", r"of each grain", EAR),
                                         (r"pitch", r"read speed", GOLD), (r"scatter", r"randomness", GREY_A))]).arrange(RIGHT, buff=0.25).move_to(UP * 0.8)
        notes = VGroup(label(r"each grain: \ a short window read from the source at its position and speed, \ shaped by a Hann window, \ added in", font_size=18, color=WHITE),
                       label(r"read position and playback time are independent: \ time and pitch come apart \ (as with PSOLA in Part 50)", font_size=18, color=TUNE),
                       label(r"regular starts give a steady tone; \ random starts \ (a Poisson cloud) \ give a texture", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        head = label(r"a granular engine", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Our granular engine reads grains out of a recorded sound. <bookmark mark='a'/> Five knobs: where in the source to "
            "read, how many grains a second, how long each is, how fast it is read, and how much randomness to add. "
            "<bookmark mark='b'/> Each grain is a short window read at its position and speed, shaped by a Hann window and "
            "added in. <bookmark mark='c'/> Because the read position and the playback time are independent, time and pitch "
            "come apart, as PSOLA's did in Part 50. <bookmark mark='d'/> Regular starts give a steady tone; random starts, a "
            "Poisson cloud, give a texture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(knobs, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(knobs))
            for mark, n in zip("bcd", notes):
                vo.wait_until(mark)
                self.play(FadeIn(n), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("grains")
        c = clip("grains.five")
        names = d["names"]
        labels_ = {"source": r"the source", "freeze": r"frozen", "stretch": r"four times longer", "shift": r"a fifth higher", "cloud": r"a cloud"}
        cells = choice_boxes([labels_[k] for k in names], width=2.3, height=1.0, buff=0.25, size=18, colors=[GREY_A, TUNE, BLUE, GOLD, EAR]).move_to(UP * 0.4)
        cnt = d["counts"]
        sub = VGroup(*[label(t, font_size=13, color=GREY_A).next_to(cells[i], DOWN, buff=0.15) for i, t in enumerate(
            [r"Part 8's voice", rf"{cnt['freeze']} grains", rf"{cnt['stretch']} grains", rf"{cnt['shift']} grains", rf"{cnt['cloud']} grains"])])
        head = label(r"one voice, \ four ways, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it on Part 8's voice singing the Tune's first phrase. Then the voice frozen on one vowel, every grain read from "
            "the same place. Then stretched to four times its length. Then a fifth higher at the same speed. Then scattered into "
            "a cloud, positions and pitches at random."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(sub))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"grains", kind="synthesized", detail=r"Part 8's voice, \ in pieces", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "The frozen vowel hangs in the air like a held organ note. The stretch keeps the pitch while time slows, with a "
            "faint shimmer where grains overlap. The shift raises the pitch without speeding up. The cloud dissolves the "
            "melody into a swarm: the same grains, no longer in order."
        ):
            self.play(Indicate(cells[4], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        d = load("grains")
        g = np.array(d["cloud"])
        ax = frame_axes(width=9.0, height=3.6, xlo=0, xhi=4.0, ylo=-0.7, yhi=d["source_s"] + 0.2, center=DOWN * 0.3)
        dots = VGroup(*[Dot(ax.to(t, p), radius=0.03, color=interpolate_color(ManimColor(BLUE), ManimColor(EAR), (np.log2(r) * 12 + 7) / 14)) for t, p, r in g])
        diag = DashedLine(ax.to(0, 0), ax.to(4.0, 3.5), color=WHITE, stroke_width=1.5, stroke_opacity=0.6)
        xl = label(r"when the grain plays, \ s", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"where it was read, \ s", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.2).rotate(PI / 2)
        key = label(r"colour: \ the grain's pitch, \ a fifth down \ (blue) \ to a fifth up \ (pink)", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"the cloud, \ grain by grain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is the cloud, half of its {say(d['counts']['cloud'])} grains drawn. <bookmark mark='a'/> Each dot is one grain: "
            "when it played, across, and where in the voice it was read, up. Played in order, the dots would lie on the dashed "
            "line. <bookmark mark='b'/> Scattered by more than half a second, and coloured by pitch, they make a band instead of "
            "a line: the melody is still there, smeared, which is why the cloud still sounds faintly like the Tune."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(diag), FadeIn(ghost(dots, 0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(key))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"granular time-stretching is in every DAW: \ a loop played at a new tempo, \ the pitch kept", WHITE),
            (r"Paulstretch's eight-hundred-per-cent slowdowns \ (Part 50) \ are grains with random phases", WHITE),
            (r"granular instruments freeze, \ scrub and scatter any recording in real time", WHITE),
            (r"the cost is smearing: \ a drum hit read by overlapping grains blurs, \ as the phase vocoder's did", WHITE),
            (r"grains cut a sound in time; \ the next idea cuts it by frequency, \ into sines and the rest", TUNE),
        ]
        rows_scene(self, r"grains at work", items,
                   "Grains are everywhere now. <bookmark mark='b'/> Granular time-stretching is in many audio tools: a loop played at a new tempo, its pitch kept. <bookmark mark='c'/> Paulstretch, mentioned in Part 50, uses overlapping spectral windows with randomized phases. <bookmark mark='d'/> Granular instruments freeze, scrub and scatter any recording in real time. <bookmark mark='e'/> The cost is smearing: a drum hit read by overlapping grains blurs, as the phase vocoder's did. <bookmark mark='f'/> Grains cut a sound in time; the next idea cuts it by frequency, into sines and the rest.", marks="bcdef")
