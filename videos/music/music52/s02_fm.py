from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403

JC = [WHITE, TUNE, BLUE, EAR, GREEN_A]


class Fm(SoundScene):
    def construct(self):
        chapter(self, 1, r"Frequency modulation", r"What happens when a vibrato gets faster than the note?")
        self.vibrato()
        self.formula()
        self.table()
        self.bessel()
        self.sweep()
        self.carson()

    # ------------------------------------------------------------------
    def vibrato(self):
        d = load("vib2fm")
        c = clip("vib2fm.one")
        pic = sgram(d["spec"], width=8.0, height=3.4).move_to(DOWN * 0.3 + LEFT * 1.2)
        pl = label(r"spectrogram, \ 100 Hz to 2 kHz, \ log scale", font_size=15, color=GREY_A).next_to(pic, UP, buff=0.12)
        rate = np.array(d["rate"])
        tt = np.linspace(0, d["seconds"], len(rate))
        rv = label(r"vibrato rate", font_size=18, color=GREY_A).to_edge(RIGHT, buff=0.9).shift(UP * 0.6)
        num = DecimalNumber(4.0, num_decimal_places=0, font_size=40, color=TUNE).next_to(rv, DOWN, buff=0.3)
        unit = label(r"times a second", font_size=16, color=GREY_A).next_to(num, DOWN, buff=0.15)
        info = label(r"a 440 Hz sine, \ swung 60 Hz up and down", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a vibrato, \ faster and faster", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Start where Chowning did, with a vibrato. A sine at four hundred and forty hertz, its pitch swung sixty hertz up and "
            "down. Now make the swing faster: four times a second, then ten, then fifty, then two hundred and twenty. Listen "
            "for the moment it stops being a wobble."
        ):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(pl), FadeIn(rv), FadeIn(num), FadeIn(unit), FadeIn(info))
        with self.listen(c) as snd:
            window(snd, r"a vibrato speeding up", kind="synthesized", detail=r"one sine", corner=DL, tag_corner=DR)
            sweep_head(snd, pic, 0.0, d["seconds"])
            snd.drive(num, lambda m, t: m.set_value(float(np.interp(t, tt, rate))))
        with self.voiceover(
            "Somewhere past twenty swings a second the ear gives up following the pitch, and hears a new colour instead: a "
            "steady, rough, then bright tone. The spectrogram shows why. The single wavy line splits into separate lines, "
            "sidebands, spaced by the vibrato's rate. A vibrato faster than hearing can follow is a spectrum."
        ):
            self.play(Indicate(pic, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        lines = VGroup(
            MathTex(r"y(t) = \sin\!\big(2\pi f_c t + I \sin(2\pi f_m t)\big)", font_size=38),
            MathTex(r"= \sum_{k=-\infty}^{\infty} J_k(I)\,\sin\!\big(2\pi (f_c + k f_m) t\big)", font_size=38),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.7)
        notes = VGroup(label(r"$f_c$: \ the carrier; \ $f_m$: \ the modulator; \ $I$: \ the index, \ the swing in radians \ (peak deviation over $f_m$)", font_size=18, color=WHITE),
                       label(r"$J_k$: \ Bessel's functions of the first kind \ (1824, \ for planets, \ not music)", font_size=18, color=GREY_A),
                       label(r"lines at the carrier plus and minus every multiple of the modulator; \ the index sets how far they spread", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"one line of mathematics", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The mathematics is one line. <bookmark mark='a'/> A carrier at f c whose phase is pushed by I times a sine at f m. "
            "The index I is the swing in radians: the peak frequency deviation divided by the modulator's frequency. "
            "<bookmark mark='b'/> Expand it, and it is a sum of sines at f c plus k f m, for every whole number k, positive and "
            "negative, each with amplitude J k of I: Bessel's functions, which Friedrich Bessel tabulated in 1824 to describe "
            "the orbits of planets. <bookmark mark='c'/> So the lines sit at the carrier plus and minus every multiple of the "
            "modulator, and the index decides how far out they spread."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("bessel")
        rows = VGroup(VGroup(label(r"line, \ Hz", font_size=18, color=GREY_A), label(r"$k$", font_size=18, color=GREY_A),
                             label(r"$|J_k(2)|$", font_size=18, color=GREY_A), label(r"measured", font_size=18, color=GREY_A)))
        for (f, a), m in zip(d["pred"][:8], d["meas"][:8]):
            k = int(round((f - d["fc"]) / d["fm"]))
            rows.add(VGroup(label(f"{f:.0f}", font_size=19, color=WHITE), label(f"{k:+d}", font_size=19, color=WHITE),
                            label(f"{abs(a):.4f}", font_size=19, color=TUNE), label(f"{m:.4f}", font_size=19, color=BLUE)))
        rows.arrange(DOWN, buff=0.22)
        for r in rows:
            for i, mm in enumerate(r):
                mm.set_x(-3.6 + 2.4 * i)
        rows.move_to(DOWN * 0.2)
        note = label(rf"largest difference: \ {d['max_err']:.6f}", font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"$f_c = 1000$, \ $f_m = 250$, \ $I = 2$: \ predicted and measured", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Check it. A carrier at a thousand hertz, a modulator at two hundred and fifty, index two. <bookmark mark='a'/> Bessel's functions predict each line's size; <bookmark mark='b'/> the measured spectrum of the computed sound agrees, line by line, to within {say(d['max_err'] * 1000000.0, 1)} millionths. The line at the carrier itself is only J zero of two, a fifth of full size: most of the energy has moved into the sidebands. The squared Bessel coefficients sum to one for the complex phase modulation. A real sine can have coincident folded sidebands, so its measured power need not be independent of index."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2])) for r in rows[1:]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows[1:]], lag_ratio=0.1), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bessel(self):
        d = load("bessel")
        Is = np.array(d["Is"])
        ax = frame_axes(width=9.0, height=3.6, xlo=0, xhi=10, ylo=-0.5, yhi=1.05, center=LEFT * 0.8 + DOWN * 0.3)
        cs = VGroup(*[curve(Is, d["curves"][str(k)], ax.to, color=JC[k], width=3) for k in range(5)])
        key = VGroup(*[label(rf"$J_{k}$", font_size=20, color=JC[k]) for k in range(5)]).arrange(DOWN, buff=0.25).next_to(ax, RIGHT, buff=0.5)
        xt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, -0.5), DOWN, buff=0.1) for v in (0, 2, 4, 6, 8, 10)])
        xl = label(r"index $I$", font_size=16, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        z = Dot(ax.to(2.405, 0), radius=0.07, color=WHITE)
        zl = label(r"$I \approx 2.405$: \ $J_0$ crosses zero", font_size=17, color=WHITE).to_edge(UP, buff=1.1)
        head = label(r"Bessel's functions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the first five Bessel functions against the index. <bookmark mark='a'/> J zero, the carrier, starts at one and falls; <bookmark mark='b'/> J one, the first pair of sidebands, rises first, then J two, J three, J four, each later than the last: turning up the index brings in sidebands one pair at a time, and the sound brightens. <bookmark mark='c'/> They wobble as they go, and near an index of two point four zero five, J zero crosses zero: its own carrier term disappears, though other sidebands can coincide with that frequency. That wobble is why FM sounds can be glassy and unstable as the index moves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cs[1:]], lag_ratio=0.3), FadeIn(key[1:]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(z), FadeIn(zl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("bessel")
        c = clip("bessel.sweep")
        ax = frame_axes(width=10.0, height=3.0, xlo=0, xhi=3700, ylo=0, yhi=1.05, center=DOWN * 0.5)
        sets = {}
        for Iv in ("0.0", "1.0", "2.0", "4.0", "8.0"):
            lines = d["levels"][Iv]
            sets[Iv] = stems([f for f, _ in lines], [a for _, a in lines], ax.to, color=TUNE, r=0.05)
        xt = VGroup(*[label(f"{k} k", font_size=14, color=GREY_A).next_to(ax.to(k * 1000, 0), DOWN, buff=0.1) for k in (0, 1, 2, 3)])
        il = label(r"index", font_size=18, color=GREY_A).to_corner(UR, buff=0.7).shift(DOWN * 0.6)
        num = DecimalNumber(0.0, num_decimal_places=1, font_size=36, color=TUNE).next_to(il, DOWN, buff=0.2)
        cap = label(r"carrier and modulator both 220 Hz \ (1 : 1): \ every harmonic of 220 is reachable", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"turning up the index, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear the index turned up from zero to eight over six seconds, with carrier and modulator both at two hundred and "
            "twenty hertz."
        ):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(il), FadeIn(num), FadeIn(cap), FadeIn(sets["0.0"]))
        keys = ["0.0", "1.0", "2.0", "4.0", "8.0"]
        with self.listen(c) as snd:
            window(snd, r"the index rising", kind="synthesized", detail=r"two sines", corner=DL, tag_corner=DR)
            shown = [sets["0.0"]]
            snd.drive(num, lambda m, t: m.set_value(min(max(8.0 * t / d["sweep_s"], 0.0), 8.0)))
            for kk in keys[1:]:
                g = sets[kk]
                snd.show(g)
                g.set_opacity(0)
                lvl = float(kk)
                snd.drive(g, lambda m, t, lvl=lvl: m.set_opacity(1.0 if lvl <= 8.0 * t / d["sweep_s"] < lvl * 2 or (lvl == 8.0 and 8.0 * t / d["sweep_s"] >= 8.0) else 0.0))
            snd.drive(sets["0.0"], lambda m, t: m.set_opacity(1.0 if 8.0 * t / d["sweep_s"] < 1.0 else 0.0))
        for kk in keys:
            sets[kk].set_opacity(0.0)
        sets["8.0"].set_opacity(1.0)
        self.add(sets["8.0"])  # listen-owned overlays leave when the sound window closes
        with self.voiceover(
            "From a pure sine, the tone grows brighter and brassier as more sidebands arrive, the lines spreading out across "
            "the harmonics of two hundred and twenty: one knob, the index, does what a filter's cutoff did in Part 51, and with "
            "an envelope on it, does it differently on every note."
        ):
            self.play(Indicate(ax, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def carson(self):
        d = load("bessel")
        bw = d["carson"]
        items = [
            (r"how wide is an FM spectrum? \ Carson's rule \ (1922, \ for radio): \ about $2(I + 1) f_m$", WHITE),
            (rf"at $f_m = 220$: \ index 1, \ {bw['1.0']:.0f} Hz; \ index 4, \ {bw['4.0']:.0f} Hz; \ index 8, \ {bw['8.0']:.0f} Hz", WHITE),
            (r"the same mathematics carried FM radio: \ a voice swinging a carrier at 100 MHz", WHITE),
            (r"a big index on a high note runs past half the sample rate and aliases \ (Part 48): \ index must fall as pitch rises", WHITE),
            (r"simple FM: \ ratio and index set the relative line pattern", TUNE),
        ]
        rows_scene(self, r"how wide, \ and what it costs", items,
                   "How wide does the spectrum get? <bookmark mark='b'/> John Carson, working on radio in 1922, gave the rule: "
                   "about two times the index plus one, times the modulator's frequency. <bookmark mark='c'/> At two hundred and "
                   f"twenty hertz, index one spans about {say(bw['1.0'])} hertz, index four about {say(bw['4.0'])}, index eight "
                   f"about {say(bw['8.0'])}. <bookmark mark='d'/> The same mathematics carries FM radio, a voice swinging a "
                   "carrier at a hundred megahertz. <bookmark mark='e'/> And a big index on a high note runs past half the sample "
                   "rate and aliases, as Part 48 warned, so reducing index on high notes is one way to limit aliasing; oversampling and bandlimited methods also help. "
                   "<bookmark mark='f'/> For this simple sinusoidal modulation, ratio and index describe the relative line pattern; carrier frequency sets its scale, and envelopes can move it.",
                   marks="bcdef")
