from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403


class Sabine(SoundScene):
    def construct(self):
        chapter(self, 1, r"Sabine's law", r"How long does a room go on sounding, \ and why?")
        self.decay()
        self.derive()
        self.cushions()
        self.eyring()
        self.bands()
        self.targets()

    # ------------------------------------------------------------------
    def decay(self):
        items = [
            (r"a sound in a room reaches you directly, \ then by one wall, \ two, \ three, \ ever more and ever fainter", WHITE),
            (r"after a few dozen reflections the energy is spread evenly and moves in every direction: \ a diffuse field", WHITE),
            (r"each bounce loses a fraction of the energy, \ so the level falls a fixed number of decibels a second", WHITE),
            (r"the reverberation time $T_{60}$: \ how long the level takes to fall 60 dB, \ to a millionth of the energy", TUNE),
            (r"Sabine's stopwatch measured the time to inaudibility, \ close to the same thing", GREY_A),
        ]
        rows_scene(self, r"a sound that dies away", items,
                   "What did Sabine measure? <bookmark mark='b'/> A sound in a room reaches you directly, then by one wall, by two, "
                   "by three, by ever more paths and ever fainter. <bookmark mark='c'/> After a few dozen reflections the energy is "
                   "spread evenly through the room and moves in every direction at once: a diffuse field. <bookmark mark='d'/> Each "
                   "bounce loses a fraction of the energy, so the level falls by a fixed number of decibels every second. "
                   "<bookmark mark='e'/> The reverberation time, T sixty, is how long the level takes to fall by sixty decibels, to "
                   "a millionth of its energy. <bookmark mark='f'/> Sabine's stopwatch measured the time until the organ pipe "
                   "became inaudible, which in a quiet room at night is close to the same thing.", marks="bcdef")

    # ------------------------------------------------------------------
    def derive(self):
        lines = VGroup(
            MathTex(r"\text{energy } E \text{ in volume } V:\quad \text{each square metre of wall is hit by } \tfrac{c}{4}\,\tfrac{E}{V} \text{ a second}", font_size=30),
            MathTex(r"\frac{dE}{dt} = -\frac{c\,A}{4V}\,E, \qquad A = \textstyle\sum_i \alpha_i S_i \ \ (\text{square metres of open window})", font_size=30),
            MathTex(r"E(t) = E_0\, e^{-cAt/4V}", font_size=32),
            MathTex(r"10\log_{10} e^{-cAT/4V} = -60 \ \Rightarrow\ T_{60} = \frac{24\ln 10}{c}\,\frac{V}{A} = 0.161\,\frac{V}{A}", font_size=32, color=TUNE),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"the law, \ derived", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"V in cubic metres, \ A in square metres, \ c = 343 m/s", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The law follows from the diffuse field in four lines. <bookmark mark='a'/> If the room holds energy E in volume V, "
            "spread evenly and moving every way, then each square metre of wall is struck by c over four times E over V every "
            "second; the quarter comes from averaging over the angles of arrival. <bookmark mark='b'/> A surface of area S with "
            "absorption coefficient alpha takes alpha S of that. Add them up into A, the room's absorption, measured in square "
            "metres of open window, which absorbs everything. The energy falls at a rate proportional to itself, "
            "<bookmark mark='c'/> so it decays exponentially. <bookmark mark='d'/> Set the decay to sixty decibels and solve: T "
            "sixty is nought point one six one times the volume over the absorption. Big rooms ring longer; soft rooms ring "
            "less. Sabine found the constant by experiment, before anyone had derived it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cushions(self):
        d = load("cushions")
        c = clip("cushions.three")
        n = np.array(d["n"])
        T = np.array(d["T"])
        ax = frame_axes(width=8.4, height=3.2, xlo=0, xhi=2000, ylo=0, yhi=6.0, center=DOWN * 0.2 + LEFT * 0.6)
        cv = curve(n, T, ax.to, color=TUNE, width=3)
        xt = VGroup(*[label(f"{v:,}", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (0, 500, 1000, 1500, 2000)])
        yt = VGroup(*[label(f"{v} s", font_size=15, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.12) for v in (0, 2, 4, 6)])
        xl = label(r"seat cushions in the room", font_size=16, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        dots = VGroup(*[Dot(ax.to(k, t), radius=0.1, color=EAR) for k, t in zip(d["stages"], d["Ts"])])
        tags = VGroup(*[label(rf"{t:.1f} s", font_size=17, color=EAR).next_to(dt, UR, buff=0.08) for dt, t in zip(dots, d["Ts"])])
        side = label(rf"a room of the Fogg's size: \ {d['V']:,.0f} m$^3$, \ {d['A0']:.1f} m$^2$ of absorption bare, \ {d['cushion']:.2f} m$^2$ a cushion",
                     font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"Sabine's cushions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is Sabine's experiment, simulated. <bookmark mark='a'/> A room of the Fogg's size, two thousand eight hundred "
            "cubic metres, with about eighty square metres of absorption in its bare plaster, glass and wooden seats. Each "
            "cushion adds about a fifth of a square metre. <bookmark mark='b'/> The reverberation time falls as one over the "
            "absorption, steeply at first, then more and more slowly: every cushion helps less than the last. Hear the room with "
            "none, with three hundred and with fifteen hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(side), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(dots[1:]), FadeIn(tags[1:]), run_time=1.5)
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"none, \ 300, \ 1,500 cushions", kind="physical model", detail=r"Part 8's voice, \ a simulated room", corner=DL, tag_corner=DR)
            pulse(snd, dots[0], st["c0"], st["c300"] - 0.3, buff=0.06)
            pulse(snd, dots[1], st["c300"], st["c1500"] - 0.3, buff=0.06)
            pulse(snd, dots[2], st["c1500"], c.duration, buff=0.06)
            pulse(snd, cv, 0, c.duration, rate=5.0, color=GREY_B, buff=0.04)
        with self.voiceover(
            f"From {say(d['Ts'][0], 1)} seconds, to {say(d['Ts'][1], 1)}, to {say(d['Ts'][2], 1)}: a muddle, then a "
            "church, then a lecture room. Sabine's own cure for the Fogg was felt on the walls; it helped, though the room was "
            "never good, and it was demolished in 1973."
        ):
            self.play(Indicate(dots[2], color=TUNE, scale_factor=1.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def eyring(self):
        items = [
            (r"Sabine's law assumes the absorption nibbles at a sound continuously", WHITE),
            (r"in fact a sound is absorbed in jumps, \ one wall at a time, \ about $c\,S/4V$ times a second", WHITE),
            (r"Eyring \ (1930): \ $T_{60} = 0.161\,V \,/\, \bigl(-S\ln(1 - \bar\alpha)\bigr)$", TUNE),
            (r"for a live room the two agree; \ for a dead one Sabine overestimates: \ with every surface open window, \ $\bar\alpha = 1$, \ Sabine still gives a decay", WHITE),
            (r"and air absorbs too, \ in the treble: \ add $4mV$ to $A$, \ which matters in big halls above 2 kHz", GREY_A),
        ]
        rows_scene(self, r"Eyring's correction", items,
                   "Sabine's law has a flaw that shows in dead rooms. <bookmark mark='b'/> It assumes the absorption nibbles at a "
                   "sound continuously. <bookmark mark='c'/> In fact a sound is absorbed in jumps, one wall at a time, about c S "
                   "over four V times a second. <bookmark mark='d'/> Carl Eyring, at Bell Labs in 1930, counted the jumps: T "
                   "sixty is nought point one six one V over minus S times the log of one minus the average absorption. "
                   "<bookmark mark='e'/> For a live room the two agree. For a dead one Sabine overestimates: make every surface an "
                   "open window, alpha one, and Sabine's law still gives a decay, while Eyring's correctly gives none. "
                   "<bookmark mark='f'/> And the air absorbs too, in the treble: add four m V to the absorption, which matters in "
                   "big halls above two kilohertz.", marks="bcdef")

    # ------------------------------------------------------------------
    def bands(self):
        rows = VGroup(VGroup(label(r"surface", font_size=17, color=GREY_A), label(r"125 Hz", font_size=17, color=GREY_A),
                             label(r"500 Hz", font_size=17, color=GREY_A), label(r"2 kHz", font_size=17, color=GREY_A)))
        data = [(r"painted brick or plaster", (0.01, 0.02, 0.03), WHITE), (r"wooden panel on a frame", (0.30, 0.10, 0.07), BLUE),
                (r"carpet on concrete", (0.02, 0.15, 0.50), WHITE), (r"heavy curtain, \ folded", (0.10, 0.50, 0.70), WHITE),
                (r"an audience, \ seated", (0.40, 0.80, 0.90), TUNE), (r"open window", (1.0, 1.0, 1.0), GREY_A)]
        for nm, vals, col in data:
            rows.add(VGroup(label(nm, font_size=19, color=col), *[label(f"{v:.2f}", font_size=19, color=col) for v in vals]))
        rows.arrange(DOWN, buff=0.25)
        for r in rows:
            r[0].set_x(-3.4)
            for i, m in enumerate(r[1:]):
                m.set_x(0.6 + 2.0 * i)
        rows.move_to(DOWN * 0.1)
        note = label(r"absorption coefficients, \ typical values: \ so a room has a reverberation time for each band", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"absorption depends on frequency", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Absorption depends on frequency, so a room has a reverberation time for every band. <bookmark mark='a'/> Hard "
            "plaster absorbs almost nothing anywhere. A wooden panel on a frame absorbs the bass, because it moves. Carpet and "
            "curtains absorb the treble, because the air must squeeze through their fibres, and fibres only catch fast air. "
            "<bookmark mark='b'/> The best absorber in a concert hall is the audience, which is why halls are tuned with "
            "seats that absorb as much as a person does, so that a rehearsal sounds like a concert."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(note), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:5]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(rows[5]), FadeIn(rows[6]))
            self.play(Indicate(rows[5], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def targets(self):
        uses = [(r"a recording studio's control room", 0.3, GREY_A), (r"a lecture room", 0.7, WHITE), (r"opera", 1.4, BLUE),
                (r"chamber music", 1.6, BLUE), (r"a symphony hall", 2.0, TUNE), (r"an organ in a large church", 3.5, EAR), (r"a cathedral", 6.0, EAR)]
        ax = frame_axes(width=8.0, height=0.1, xlo=0, xhi=7.0, ylo=0, yhi=1, center=DOWN * 2.2 + RIGHT * 1.2)
        ticks = VGroup(*[label(f"{v} s", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in range(0, 8)])
        bars = VGroup()
        for i, (nm, t, col) in enumerate(uses):
            y = 2.3 - 0.62 * i
            bar = Rectangle(width=8.0 * t / 7.0, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.75)
            bar.move_to([ax.to(0, 0)[0] + bar.width / 2, y, 0])
            bars.add(VGroup(bar, label(nm, font_size=18, color=col).next_to([ax.to(0, 0)[0], y, 0], LEFT, buff=0.2)))
        head = label(r"how long should a room ring?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How long should a room ring? <bookmark mark='a'/> For speech, short: a control room, a third of a second; a "
            "lecture room, under a second, so that each syllable is gone before the next. <bookmark mark='b'/> For music, "
            "longer: opera and chamber music about a second and a half, a symphony hall about two seconds, enough to join the "
            "notes of a phrase and to make an orchestra sound bigger than it is. <bookmark mark='c'/> Organ music was written "
            "for churches of three or four seconds and more, and plainchant for cathedrals that ring for six. Music and rooms "
            "grew up together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(ghost(bars, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(bars[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[2:5]], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(bars[5]), FadeIn(bars[6]))
        self.wait(0.4)
        self.clear_scene()
