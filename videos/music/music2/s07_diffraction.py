from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Diffraction(SoundScene):
    def construct(self):
        chapter(self, 6, r"Round the corner", r"Why can you hear the bass through a wall of people?", lit=(1687,),
                extra=((1678, r"Huygens's wavelets"),))
        self.wavelength()
        self.wall()
        self.measured()
        self.listen_wall()

    # ------------------------------------------------------------------
    def wavelength(self):
        law = MathTex(r"\lambda", r"=", r"\frac{c}{f}", font_size=64).to_edge(UP, buff=0.5)
        law[0].set_color(RATIO)
        sub = label(r"wavelength: \ how far the sound travels during one vibration", font_size=28, color=GREY_A).next_to(law, DOWN, buff=0.25)
        items = [(r"the lowest note we hear", 20), (r"a double bass, \ low E", 41.2), (r"the A an orchestra tunes to", 440),
                 (r"the top of a piccolo", 4186), (r"the highest note we hear", 20000)]
        rows = VGroup()
        scale = 11.0 / 17.2
        for i, (name, hz) in enumerate(items):
            lam = C / hz
            bar = Line(ORIGIN, RIGHT * max(lam * scale, 0.02), color=RATIO, stroke_width=7)
            txt = rf"{lam:.1f} m" if lam >= 1 else (rf"{lam * 100:.0f} cm" if lam >= 0.1 else rf"{lam * 1000:.0f} mm")
            rows.add(VGroup(label(name, font_size=26), label(rf"{hz:,.0f} Hz".replace(",", "{,}"), font_size=26, color=FREQ), bar,
                            label(txt, font_size=26, color=RATIO)))
        for i, r in enumerate(rows):
            y = 0.9 - 0.75 * i
            r[0].move_to([-6.6, y + 0.22, 0], aligned_edge=LEFT)
            r[1].move_to([-1.6, y + 0.22, 0], aligned_edge=LEFT)
            r[2].move_to([-6.6, y - 0.12, 0], aligned_edge=LEFT)
            r[3].next_to(r[2], RIGHT, buff=0.2)
        person = VGroup(Line([-6.6, -3.2, 0], [-6.6 + 1.7 * scale, -3.2, 0], color=GREY_B, stroke_width=7),
                        label(r"a person, \ 1.7 m", font_size=22, color=GREY_B))
        person[1].next_to(person[0], RIGHT, buff=0.2)
        with self.voiceover(
            "The number is the wavelength: how far the sound travels during one vibration. It is the speed divided "
            "by the frequency. <bookmark mark='a'/> And for sound, wavelengths are the size of the things around us. "
            "The lowest note we hear is seventeen metres long: the length of a house. A double bass's low E is eight "
            "metres. The A an orchestra tunes to is seventy-eight centimetres. <bookmark mark='b'/> The top of a "
            "piccolo is eight centimetres, and the highest sound we hear, seventeen millimetres. "
            "<bookmark mark='c'/> A thousand to one, and you are somewhere in the middle of that range. So a person, "
            "a pillar or a wall is a small thing to a bass note and a large thing to a high one."
        ) as vo:
            self.play(FadeIn(law), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.5), run_time=max(vo.until("b") - 0.2, 3.0))
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(person))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        d = load("diffraction")
        low = FieldView(d["low"], d["extent"], width=6.2, solid=d["solid"]).move_to(LEFT * 3.4 + DOWN * 0.3)
        high = FieldView(d["high"], d["extent"], width=6.2, solid=d["solid"]).move_to(RIGHT * 3.4 + DOWN * 0.3)
        caps = VGroup(label(rf"{d['low_hz']:.0f} Hz: \ a wavelength of {C / d['low_hz']:.1f} m", font_size=26, color=RATIO).next_to(low, UP, buff=0.15),
                      label(rf"{d['high_hz']:,.0f} Hz: \ a wavelength of {100 * C / d['high_hz']:.0f} cm".replace(",", "{,}"),
                            font_size=26, color=RATIO).next_to(high, UP, buff=0.15))
        marks = VGroup()
        for fv in (low, high):
            marks.add(Dot(fv.point(*d["source"]), radius=0.07, color=TUNE), Dot(fv.point(*d["listener"]), radius=0.08, color=EAR))
        key = VGroup(VGroup(Dot(radius=0.07, color=TUNE), label(r"source", font_size=22, color=TUNE)).arrange(RIGHT, buff=0.12),
                     VGroup(Dot(radius=0.08, color=EAR), label(r"listener", font_size=22, color=EAR)).arrange(RIGHT, buff=0.12),
                     label(rf"a wall {d['wall_top']:.0f} m high, \ seen from the side", font_size=22, color=GREY_B)
                     ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is a wall, four metres high, seen from the side, with a source on one side and a listener on the "
            "other. <bookmark mark='a'/> On the left, a low tone, with a wavelength of two metres. On the right, a "
            "tone three octaves higher, with a wavelength of twenty-five centimetres. <bookmark mark='b'/> The low "
            "tone pours over the top of the wall and fills the space behind it. The high tone goes on in nearly "
            "straight lines, and leaves a shadow. Christiaan Huygens had the picture in 1678: every point a wave "
            "reaches becomes a small source of its own. A long wave spreads from the wall's edge in all directions. "
            "A short one mostly cancels itself, except straight ahead."
        ) as vo:
            self.play(FadeIn(low), FadeIn(high), FadeIn(marks), FadeIn(key))
            fps = (len(d["low"]) - 1) / max(vo.remaining() - 1.0, 8.0)       # the whole run, slowed to fit the telling
            low.start(fps), high.start(fps)
            vo.wait_until("a")
            self.play(FadeIn(caps))
            self.wait(vo.remaining() + 0.1)
        low.stop(), high.stop()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("diffraction")
        g = axes([np.log10(80), np.log10(1700)], [-32, 0], x_length=7.0, y_length=3.8, xlabel=r"frequency (Hz)",
                 ylabel=r"level behind the wall, \ against no wall (dB)", xticks=[np.log10(v) for v in (125, 250, 500, 1000)],
                 yticks=[-30, -20, -10, 0], font_size=20, xfmt=lambda v: f"{10 ** v:.0f}")
        g.move_to(LEFT * 2.6 + DOWN * 0.3)
        line = curve(g.ax, np.log10(d["hz"]), d["loss"], TUNE, stroke_width=3)
        mk = VGroup(*[Dot(g.ax.c2p(np.log10(t["hz"]), t["maekawa"]), radius=0.08, color=GOOD) for t in d["table"]])
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=TUNE, stroke_width=3), label(r"our simulation", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.08, color=GOOD), label(r"Maekawa's chart for noise barriers (1968)", font_size=24, color=GOOD)).arrange(RIGHT, buff=0.15),
                     ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(g, UP, buff=0.25).align_to(g, LEFT)
        rows = VGroup(label(r"behind the wall", font_size=26, color=GREY_B))
        for t in d["table"][:4]:
            rows.add(VGroup(label(rf"{t['hz']} Hz", font_size=28, color=FREQ), label(rf"${t['db']:.0f}$ dB", font_size=28, color=LEVEL)).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 4.6 + DOWN * 0.2)
        lo, hi = d["table"][0], d["table"][3]
        with self.voiceover(
            "How much gets round? We ran the simulation with the wall and without it, and compared what the listener "
            f"receives at every frequency. <bookmark mark='a'/> At {lo['hz']} hertz the wall costs "
            f"{say(-lo['db'])} decibels. At a thousand it costs {say(-hi['db'])}. Each octave up, the wall works a "
            "few decibels better. <bookmark mark='b'/> The green points are the chart that engineers have used since "
            "1968 to design noise barriers along motorways. Our simulation knows nothing about that chart, and lands "
            f"within {say(d['worst_vs_maekawa'])} decibels of it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(leg[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mk], lag_ratio=0.2), FadeIn(leg[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_wall(self):
        d = load("diffraction")
        c = clip("diffraction.wall")
        sp = Spectrogram(c, width=10.4, height=3.6, fmax=2600.0, marks=[(500, "500 Hz"), (1000, "1 kHz"), (2000, "2 kHz")])
        sp.move_to(UP * 0.4)
        t_b = c.events["behind"]
        div = DashedLine([sp.x_of(t_b - 0.25), sp.frame.get_bottom()[1], 0], [sp.x_of(t_b - 0.25), sp.frame.get_top()[1], 0],
                         color=GREY_B, stroke_width=1.5)
        tags = VGroup(label(r"in the open", font_size=28, color=GOOD).move_to([sp.x_of(t_b / 2 - 0.3), sp.frame.get_top()[1] + 0.3, 0]),
                      label(r"behind the wall", font_size=28, color=BAD).move_to([sp.x_of(t_b + (c.duration - t_b) / 2), sp.frame.get_top()[1] + 0.3, 0]))
        sp.playhead.set_opacity(0)
        with self.voiceover(
            "Now apply that measured curve to a sound. The Tune's first phrase, on the string from Part 1: first in "
            "the open, then from behind the wall."
        ):
            self.play(FadeIn(sp), FadeIn(div), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"the Tune in the open, \ then behind the wall", detail=r"the wall's measured effect, applied")
            sp.playhead.set_opacity(1)
            snd.drive(sp.playhead, sp.follow())
        sp.playhead.set_opacity(0)
        with self.voiceover(
            f"It is quieter, by {say(-d['drop_db'])} decibels overall. But listen to how it is quieter. The low part "
            "of each note survives and the brightness goes, so the string sounds dull and far away. "
            "<bookmark mark='a'/> That is the sound of every party heard from the next room, and of a band heard "
            "from outside the hall. You have known what diffraction sounds like all your life."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(tags[1], color=BAD, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()
