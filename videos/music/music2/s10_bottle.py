from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Bottle(SoundScene):
    def construct(self):
        chapter(self, 9, r"A bottle", r"Why does a bottle hum one note, \ and such a low one?", lit=(1863,))
        self.puzzle()
        self.numbers()
        self.fill()

    # ------------------------------------------------------------------
    def puzzle(self):
        d = load("bottle")
        b = d["bottle"]
        bot = bottle_shape(height=4.6, body_w=1.9, neck_w=0.6, neck_h=1.5).move_to(LEFT * 4.6 + DOWN * 0.3)
        top = bot.outline.get_top()
        plug = Rectangle(width=0.5, height=1.1, stroke_width=0, fill_color=MASS, fill_opacity=0.75).move_to(top + DOWN * 0.7)
        home = plug.get_center().copy()
        clock = {"t": 0.0}

        def bob(m, dt):
            clock["t"] += dt
            m.move_to(home + UP * 0.16 * np.sin(2 * PI * 0.9 * clock["t"]))

        spring = label(r"the air in the body: \ a spring", font_size=24, color=FORCE).next_to(bot, RIGHT, buff=0.2).shift(DOWN * 1.0)
        mass = label(r"the air in the neck: \ a mass", font_size=24, color=MASS).next_to(bot, RIGHT, buff=0.2).shift(UP * 1.45)
        rows = [
            MathTex(r"m", r"=", r"\rho\, A\, L", font_size=40),
            MathTex(r"k", r"=", r"\rho\, c^2\, \frac{A^2}{V}", font_size=40),
            MathTex(r"f", r"=", r"\frac{1}{2\pi}\sqrt{\frac{k}{m}}", r"=", r"\frac{c}{2\pi}\sqrt{\frac{A}{V L}}", font_size=40),
        ]
        whys = [why(r"the plug of air in the neck"), why(r"push it in by $x$: the body's pressure rises by $\rho c^2 A x / V$"),
                why(r"a mass on a spring")]
        rows[0][0].set_color(MASS), rows[1][0].set_color(FORCE), rows[2][4].set_color(TUNE)
        step = ladder(self, rows, whys, keep=3, top=1.7, buff=0.6, x=1.6)
        c_quarter = C / (4 * (b["neck_len"] + b["body_len"]))
        puzzle = VGroup(label(rf"{100 * (b['neck_len'] + b['body_len']):.0f} cm from top to bottom", font_size=28, color=RATIO),
                        label(rf"as a stopped pipe: \ about {c_quarter:.0f} Hz", font_size=28, color=GREY_A),
                        label(rf"what it hums: \ {d['sim']:.0f} Hz", font_size=32, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        puzzle.move_to(RIGHT * 1.6 + UP * 0.6)
        with self.voiceover(
            "Blow across a bottle and it hums one low note. That is strange. Our bottle is eighteen centimetres from "
            f"top to bottom. As a stopped pipe it should sound near {say(c_quarter, )} hertz. It hums at "
            f"{say(d['sim'])}: more than an octave lower. <bookmark mark='a'/> Hermann von Helmholtz explained it. "
            "The bottle is not acting as a pipe at all. The air in the neck moves in and out as one lump: a mass. "
            "<bookmark mark='b'/> The air in the body is squeezed and released by it: a spring. "
            "<bookmark mark='c'/> The mass is the density times the volume of the neck. <bookmark mark='d'/> The "
            "spring is the stiffness of the air in the body: push the plug in, and the pressure inside rises. "
            "<bookmark mark='e'/> A mass on a spring has one frequency, and here it is. A wider neck raises the note. "
            "A longer neck or a bigger body lowers it."
        ) as vo:
            self.play(FadeIn(bot), FadeIn(puzzle[0]))
            self.play(FadeIn(puzzle[1]))
            self.wait(2.5)
            self.play(FadeIn(puzzle[2]))
            vo.wait_until("a")
            self.play(FadeOut(puzzle), run_time=0.3)
            plug.add_updater(bob)
            self.play(FadeIn(plug), FadeIn(mass))
            vo.wait_until("b")
            self.play(FadeIn(spring))
            vo.wait_until("c")
            step(0)
            vo.wait_until("d")
            step(1)
            vo.wait_until("e")
            step(2)
        plug.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("bottle")
        b = d["bottle"]
        c = clip("bottle.empty")
        bot = bottle_shape(height=4.2, body_w=1.75, neck_w=0.55, neck_h=1.4).move_to(LEFT * 5.0 + DOWN * 0.2)
        spec = VGroup(label(rf"{b['volume'] * 1e6:.0f} ml", font_size=26, color=GREY_A),
                      label(rf"neck: \ {2000 * b['neck_r']:.0f} mm wide, \ {100 * b['neck_len']:.0f} cm long", font_size=26, color=GREY_A),
                      label(rf"plus {1000 * (b['neck_eff'] - b['neck_len']):.0f} mm for the air at its two ends", font_size=24, color=GREY_B)
                      ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(bot, RIGHT, buff=0.5).shift(UP * 1.6)
        res = VGroup(
            VGroup(label(r"Helmholtz's formula", font_size=28), label(rf"{d['lumped']:.1f} Hz", font_size=30, color=GREY_A)),
            VGroup(label(r"neck and body as two tubes, \ solved exactly", font_size=28), label(rf"{d['exact']:.1f} Hz", font_size=30, color=GOOD)),
            VGroup(label(r"simulated, \ and measured from the sound", font_size=28), label(rf"{d['sim']:.1f} Hz", font_size=30, color=TUNE)),
        )
        for r in res:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        res.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(spec, DOWN, buff=0.6).align_to(spec, LEFT)
        for r in res:
            r[1].set_x(res.get_right()[0] - 0.4)
        note_ = label(rf"the note {flat_name(d['note'])}, \ and it rings for about {d['q']:.0f} swings", font_size=26, color=TUNE)
        note_.next_to(res, DOWN, buff=0.4).align_to(res, LEFT)
        with self.voiceover(
            f"Our bottle holds a third of a litre. <bookmark mark='a'/> Helmholtz's formula says "
            f"{say(d['lumped'], 1)} hertz. <bookmark mark='b'/> Treat the neck and the body properly, as two tubes "
            f"joined together, and the exact answer is {say(d['exact'], 1)}. <bookmark mark='c'/> The simulation, "
            f"which knows neither formula, gives {say(d['sim'], 1)}. So the famous formula is half a semitone sharp "
            "for a bottle this shape: the body is not small enough to count as a simple spring. Here is the bottle, "
            "slapped on the mouth twice, and then blown."
        ) as vo:
            self.play(FadeIn(bot), FadeIn(spec))
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]), FadeIn(note_))
        top = bot.outline.get_top()
        with self.listen(c) as snd:
            window(snd, r"slapped, \ slapped, \ blown")
            for ev in ("slap1", "slap2"):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                lens = Lens(top + LEFT * 0.45 + UP * 0.25, top + RIGHT * 0.45 + UP * 0.25, amp=0.26, color=TUNE, opacity=0.45)
                snd.show(lens)
                snd.drive(lens, ring(at=t0, rate=5.0, stop_at=t0 + 0.95))
            t0 = snd.time_of("blown")
            snd.wait_until(t0)
            lens = Lens(top + LEFT * 0.45 + UP * 0.25, top + RIGHT * 0.45 + UP * 0.25, amp=0.26, color=TUNE, opacity=0.45)
            snd.show(lens)
            snd.drive(lens, lambda m, t: m.set_amp(0.55 + 0.45 * np.sin(31 * t) * np.sin(7.3 * t) if t0 <= t < t0 + 2.2 else 0.0))
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fill(self):
        d = load("bottle")
        c = clip("bottle.fills")
        sw = d["sweep"]
        g = axes([0, 0.85], [150, 420], x_length=5.6, y_length=3.6, xlabel=r"how full the body is", ylabel=r"its note (Hz)",
                 xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[200, 300, 400], font_size=20, xfmt=lambda v: f"{100 * v:.0f}\\%")
        g.move_to(RIGHT * 3.4 + UP * 0.2)
        ex = curve(g.ax, [r["fill"] for r in sw], [r["exact"] for r in sw], GOOD, stroke_width=3, smooth=True)
        lu = DashedVMobject(curve(g.ax, [r["fill"] for r in sw], [r["lumped"] for r in sw], GREY_B, stroke_width=2, smooth=True), num_dashes=40)
        dots = VGroup(*[Dot(g.ax.c2p(r["fill"], r["sim"]), radius=0.07, color=TUNE) for r in sw])
        leg = VGroup(label(r"dots: \ simulated", font_size=22, color=TUNE), label(r"line: \ two tubes, \ exact", font_size=22, color=GOOD),
                     label(r"dashes: \ Helmholtz's formula", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        leg.move_to(g.ax.c2p(0.04, 385), aligned_edge=UL)
        fills = (0.0, 0.3, 0.6)
        bots = VGroup(*[bottle_shape(height=3.0, body_w=1.25, neck_w=0.4, neck_h=1.0, fill=f) for f in fills]).arrange(RIGHT, buff=0.5)
        bots.move_to(LEFT * 3.9 + DOWN * 0.2)
        hz = VGroup(*[label(rf"{v:.0f} Hz", font_size=26, color=FREQ).next_to(b, DOWN, buff=0.2) for v, b in zip(d["three_hz"], bots)])
        with self.voiceover(
            "Now pour water in. Water takes up room, the spring of air gets smaller and therefore stiffer, and the "
            "note goes up. <bookmark mark='a'/> The curve is the note against how full the body is: the exact "
            "two-tube answer as a line, the simulation as dots, Helmholtz's formula dashed. Empty, a third full, "
            "and nearly two thirds full."
        ) as vo:
            self.play(FadeIn(bots), FadeIn(hz))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(ex), Create(lu), LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.15), FadeIn(leg), run_time=2.5)
        with self.listen(c) as snd:
            window(snd, r"empty, \ a third full, \ nearly two thirds")
            for k, b in enumerate(bots):
                t0 = snd.time_of(f"f{k}")
                snd.wait_until(t0)
                top = b.outline.get_top()
                lens = Lens(top + LEFT * 0.35 + UP * 0.22, top + RIGHT * 0.35 + UP * 0.22, amp=0.22, color=TUNE, opacity=0.45)
                snd.show(lens)
                snd.drive(lens, ring(at=t0, rate=5.0, stop_at=t0 + 0.95))
                hz[k].set_color(TUNE)
                snd.wait_until(t0 + 0.9)
        pay = payoff_card([(r"the air inside a guitar and a violin", [7]), (r"ocarinas and blown jugs", [8]),
                           (r"the port of a bass loudspeaker", [54])], font_size=24).scale(0.85).to_edge(DOWN, buff=0.3).shift(LEFT * 3.2)
        with self.voiceover(
            "So that is how the bottles at the start of this part were tuned: by solving this curve for six notes. "
            "<bookmark mark='a'/> And the same mass on a spring is hiding in a great many instruments. The air "
            "inside a guitar or a violin is a Helmholtz resonator, with the sound hole as its neck. So is an "
            "ocarina. So is the port on the front of a bass loudspeaker."
        ) as vo:
            vo.wait_until("a")
            self.play(bots.animate.shift(UP * 0.9), hz.animate.shift(UP * 0.9), FadeIn(pay))
        self.wait(0.3)
        self.clear_scene()
