from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Spread(SoundScene):
    def construct(self):
        chapter(self, 5, r"Spreading out", r"Why is it quieter at the back?", lit=(1687,))
        self.rings()
        self.law()
        self.walk()
        self.worked()

    # ------------------------------------------------------------------
    def rings(self):
        d = load("spread")
        fv = FieldView(d["frames"][8:37], d["extent"], width=6.6, loop=True).move_to(LEFT * 3.4 + DOWN * 0.1)
        tag = label(r"simulated: \ one push of air, \ seen from above", font_size=22, color=GREY_B).next_to(fv, DOWN, buff=0.15)
        # the same power through a bigger and bigger surface
        c0 = RIGHT * 3.6 + DOWN * 0.2
        shells = VGroup(*[Circle(radius=r, color=AIR, stroke_width=2.5, stroke_opacity=0.9 - 0.2 * i).move_to(c0)
                          for i, r in enumerate((0.7, 1.4, 2.1))])
        src = Dot(c0, radius=0.07, color=TUNE)
        rl = VGroup(*[label(t, font_size=24, color=RATIO).move_to(c0 + RIGHT * r + UP * 0.22 + LEFT * 0.2)
                      for t, r in ((r"$r$", 0.7), (r"$2r$", 1.4), (r"$3r$", 2.1))])
        area = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (r"area $\times 1$", r"area $\times 4$", r"area $\times 9$")])
        area.arrange(RIGHT, buff=0.5).next_to(shells, DOWN, buff=0.3)
        with self.voiceover(
            "Give the air one push at a point, and the disturbance runs outward in every direction at once. "
            "<bookmark mark='a'/> The energy in that first push never grows. It only has more and more room. "
            "<bookmark mark='b'/> In open space the room is the surface of a sphere, and the surface of a sphere "
            "grows as the square of its radius. Twice as far from the source, the same power is spread over four "
            "times the area. Three times as far, nine times the area."
        ) as vo:
            self.play(FadeIn(fv), FadeIn(tag))
            fv.start(5.0)
            vo.wait_until("b")
            self.play(FadeIn(src), LaggedStart(*[Create(s) for s in shells], lag_ratio=0.5), FadeIn(rl), run_time=2.5)
            self.play(FadeIn(area))
        self.wait(0.3)
        fv.stop()
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        d = load("spread")
        thm = theorem_card(r"The inverse-square law",
                           MathTex(r"I \;=\; \frac{P}{4\pi r^2}", r"\qquad\Longrightarrow\qquad", r"-6\ \text{dB for every doubling of the distance}",
                                   font_size=36),
                           who=r"a point source in open space", width=11.4, color=GOOD).to_edge(UP, buff=0.45)
        g = axes([0, 3.2], [-20, 1], x_length=5.6, y_length=3.0, xlabel=r"distance (doublings)", ylabel=r"level (dB)",
                 xticks=[0, 1, 2, 3], yticks=[-18, -12, -6, 0], font_size=20, xfmt=lambda v: f"{2 ** int(v)} m")
        g.move_to(LEFT * 3.4 + DOWN * 1.3)
        pts = VGroup(*[Dot(g.ax.c2p(i, v), radius=0.08, color=TUNE) for i, v in enumerate(d["space_levels"])])
        line = Line(g.ax.c2p(0, 0), g.ax.c2p(3, -18.06), color=GOOD, stroke_width=2)
        res = VGroup(
            label(r"simulated: \ one ray of a spherical wave", font_size=26, color=GREY_A),
            MathTex(r"p \propto r^{%.3f}" % d["space_exponent"], font_size=40, color=TUNE),
            label(rf"{d['per_doubling_db']:.2f} dB per doubling", font_size=30, color=TUNE),
            label(r"in a plane (our pictures from above): \\ $p \propto r^{%.2f}$, \ about 3 dB per doubling" % d["plane_exponent"],
                  font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 1.3)
        with self.voiceover(
            "So the intensity is the power divided by the area of the sphere, four pi r squared. That is the "
            "inverse-square law. <bookmark mark='a'/> In decibels: every doubling of the distance costs six. "
            "<bookmark mark='b'/> Our simulation agrees. Following one ray of a spherical wave outward, the pressure "
            f"falls as the distance to the power {say(d['space_exponent'], 3)}: "
            f"{say(d['per_doubling_db'], 2)} decibels per doubling. <bookmark mark='c'/> One caution about this "
            "part's pictures. They show sound in a flat sheet of air, seen from above, and in a sheet the energy "
            "spreads round a circle, not over a sphere. There, the loss is only about three decibels per doubling."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(line), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.3), FadeIn(res[0]), run_time=2.0)
            self.play(FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        d = load("spread")
        c = clip("spread.walk")
        x0, x1 = -5.4, 5.4
        ground = Line([x0, -0.4, 0], [x1, -0.4, 0], color=GREY_D, stroke_width=2)

        def X(r):
            return x0 + 0.6 + (x1 - x0 - 1.2) * (r - 1) / 7.0

        mono = StringView(width=1.0, scale=0.3, stroke_width=3).move_to([x0 + 0.1, 0.1, 0])
        posts = VGroup(*[VGroup(Line([X(r), -0.5, 0], [X(r), -0.3, 0], color=GREY_C), label(f"{r} m", font_size=24, color=RATIO).move_to([X(r), -0.8, 0]))
                         for r in d["space_r"]])
        ear = Dot([X(1), 0.1, 0], radius=0.13, color=EAR)
        lev = VGroup(*[label(rf"${v:.0f}$ dB" if i else r"0 dB", font_size=28, color=LEVEL).move_to([X(r), 0.8, 0])
                       for i, (r, v) in enumerate(zip(d["space_r"], d["space_levels"]))])
        lev.set_opacity(0.0)
        meter = Meter(width=0.45, height=2.4).move_to([5.9, 1.8, 0])
        head = label(r"one string, \ a listener walking away", font_size=30, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Here is what that sounds like. Our string, heard from one metre, then two, four and eight. Every step "
            "doubles the distance."
        ):
            self.play(FadeIn(head), FadeIn(ground), FadeIn(mono), FadeIn(posts), FadeIn(ear), FadeIn(meter))
        self.add(lev)
        with self.listen(c) as snd:
            window(snd, r"at 1, \ 2, \ 4 and 8 metres")
            for k, r in enumerate(d["space_r"]):
                t0 = snd.time_of(f"r{k}")
                snd.wait_until(t0)
                ear.move_to([X(r), 0.1, 0])
                lev[k].set_opacity(1.0)
                top = 10 ** (d["space_levels"][k] / 20)
                lens = Lens(mono.p(0), mono.p(1), amp=0.14, color=TUNE)
                snd.show(lens)
                snd.drive(lens, ring(at=t0, rate=1.6, stop_at=t0 + 1.2))
                snd.drive(meter, lambda m, t, top=top, t0=t0: m.set_level(top * float(np.exp(-1.6 * max(t - t0, 0.0)))))
                snd.wait_until(t0 + 1.15)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("spread")
        b = d["busker"]
        title = label(r"A worked example: \ a trumpeter in a square", font_size=36).to_edge(UP, buff=0.5)
        given = VGroup(label(rf"{b['at_1m']:.0f} dB at one metre", font_size=32, color=LEVEL),
                       label(rf"you are {b['metres']:.0f} metres away, \ in the open", font_size=32, color=RATIO)).arrange(DOWN, buff=0.25).move_to(UP * 1.5)
        ask = pause_card(r"How loud is the trumpet where you are standing?", width=8.4).move_to(DOWN * 0.6)
        work = VGroup(MathTex(r"32 = 2^5", r"\quad\Longrightarrow\quad", r"5 \times 6\ \text{dB} = 30\ \text{dB}", font_size=40),
                      MathTex(rf"{b['at_1m']:.0f} - 30 = {b['level']:.0f}\ \text{{dB}}", font_size=48, color=TUNE),
                      label(r"about as loud as someone talking next to you", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        with self.voiceover(
            f"One worked example. A trumpeter in a town square measures {say(b['at_1m'])} decibels at one metre. "
            f"<bookmark mark='a'/> You are {say(b['metres'])} metres away, with no walls nearby. How loud is the "
            "trumpet where you are? Pause, and work it out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(given[0]))
            vo.wait_until("a")
            self.play(FadeIn(given[1]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Thirty-two is two, doubled five times. Five doublings at six decibels each is thirty. "
            f"<bookmark mark='a'/> So {say(b['level'])} decibels: the level of someone talking beside you."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]))
            vo.wait_until("a")
            self.play(FadeIn(work[1]), FadeIn(work[2]))
        with self.voiceover(
            "That is outdoors, with nothing to send the sound back. Indoors, the walls return most of what would "
            "have escaped, which is the whole reason for a concert hall, and the subject of Part 55. "
            "<bookmark mark='a'/> And notice what the law does not say. It says how the level falls. It says nothing "
            "about which sounds get past an obstacle. For that, we need one more number."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(work[1], color=LEVEL, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
