from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Speed(SoundScene):
    def construct(self):
        chapter(self, 3, r"The speed of sound", r"Why 340 metres a second, \ and not some other number?", lit=(1687, 1816))
        self.newton()
        self.laplace()
        self.temperature()

    # ------------------------------------------------------------------
    def newton(self):
        d = load("speed")
        card = history_card(1687, r"Isaac Newton, \ \textit{Principia}",
                            r"the first calculation of the speed of sound: 979 feet a second. Guns timed across "
                            r"a field gave about 1,142.", width=5.4).to_corner(UL, buff=0.45)
        string = MathTex(r"c_{\text{string}}", r"=", r"\sqrt{\frac{T}{\mu}}", font_size=46)
        airf = MathTex(r"c_{\text{air}}", r"=", r"\sqrt{\frac{P}{\rho}}", font_size=46)
        string[2].set_color(STR), airf[2].set_color(AIR)
        whys = VGroup(label(r"what pulls it back, \ over what has to be moved", font_size=24, color=GREY_A),
                      label(r"pressure, \ over density", font_size=24, color=GREY_A))
        forms = VGroup(VGroup(string, whys[0]).arrange(RIGHT, buff=0.4), VGroup(airf, whys[1]).arrange(RIGHT, buff=0.4))
        forms.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(card, RIGHT, buff=0.5).align_to(card, UP)
        if forms.get_right()[0] > 6.8:
            forms.scale_to_fit_width(6.8 - forms.get_left()[0]).next_to(card, RIGHT, buff=0.5).align_to(card, UP)
        nums = VGroup(
            MathTex(r"\sqrt{\frac{101{,}325\ \text{Pa}}{1.293\ \text{kg/m}^3}}", r"=", rf"{d['newton']:.0f}\ \text{{m/s}}", font_size=40),
            label(r"measured, \ at freezing: \ 331 m/s", font_size=30, color=GOOD),
            label(rf"Newton's value is {100 * d['short']:.0f}\% too low", font_size=30, color=BAD),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.7)
        nums[0][2].set_color(BAD)
        with self.voiceover(
            "On a string, the speed of a wave was the square root of the tension over the mass per unit length: "
            "what pulls the string back, over what has to be moved. <bookmark mark='a'/> Newton made the same "
            "argument for air in 1687. What pushes a squeezed parcel back is the pressure. What has to be moved is "
            "the density. <bookmark mark='b'/> Put in the numbers for air at freezing, and you get "
            f"{say(d['newton'])} metres a second. <bookmark mark='c'/> The measured speed is 331. Newton was "
            f"{say(100 * d['short'])} percent short, he knew it, and nobody could say why for more than a century."
        ) as vo:
            self.play(FadeIn(card), FadeIn(string), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(FadeIn(airf), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(FadeIn(nums[0]))
            vo.wait_until("c")
            self.play(FadeIn(nums[1]), FadeIn(nums[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laplace(self):
        d = load("speed")
        card = history_card(1816, r"Pierre-Simon Laplace",
                            r"squeezed air warms, and in a sound wave there is no time for the heat to leak away: "
                            r"the air is stiffer than Boyle's law says, by the factor $\gamma = 1.4$",
                            width=5.6).to_corner(UL, buff=0.45)
        law = MathTex(r"c", r"=", r"\sqrt{\frac{\gamma P}{\rho}}", r"=", rf"{d['laplace']:.0f}\ \text{{m/s}}", font_size=50)
        law[2].set_color(AIR), law[4].set_color(GOOD)
        law.move_to(RIGHT * 3.0 + UP * 2.1)
        # the race: the same row of parcels under two gas laws
        y1, y2 = -0.4, -1.7
        x0, x1 = -5.6, 5.6
        tracks = VGroup(Line([x0, y1, 0], [x1, y1, 0], color=GREY_D, stroke_width=2), Line([x0, y2, 0], [x1, y2, 0], color=GREY_D, stroke_width=2))
        names = VGroup(label(r"parcels that obey Boyle's law \ (Newton)", font_size=24, color=BAD).next_to(tracks[0], UP, buff=0.12).align_to(tracks, LEFT),
                       label(r"parcels that warm when squeezed \ (Laplace)", font_size=24, color=GOOD).next_to(tracks[1], UP, buff=0.12).align_to(tracks, LEFT))
        ticks = VGroup()
        for m in range(0, 7):
            x = x0 + (x1 - x0) * m / 6
            ticks.add(Line([x, y2 - 0.08, 0], [x, y2 + 0.08, 0], color=GREY_D), label(f"{m} m", font_size=18, color=GREY_C).move_to([x, y2 - 0.3, 0]))
        tr = ValueTracker(0.0)      # milliseconds
        p1 = Dot(color=BAD, radius=0.11).move_to([x0, y1, 0])
        p2 = Dot(color=GOOD, radius=0.11).move_to([x0, y2, 0])
        p1.add_updater(lambda m: m.set_x(x0 + (x1 - x0) * min(d["newton_sim"] * tr.get_value() / 1000 / 6, 1)))
        p2.add_updater(lambda m: m.set_x(x0 + (x1 - x0) * min(d["laplace_sim"] * tr.get_value() / 1000 / 6, 1)))
        res = VGroup(label(rf"measured in the simulation: \ {d['newton_sim']:.1f} m/s", font_size=26, color=BAD),
                     label(rf"measured in the simulation: \ {d['laplace_sim']:.1f} m/s", font_size=26, color=GOOD))
        res[0].next_to(tracks[0], UP, buff=0.12).align_to(tracks, RIGHT)
        res[1].next_to(tracks[1], UP, buff=0.12).align_to(tracks, RIGHT)
        told = label(r"neither run was told a speed: \ only a gas law, \ and Newton's second law for each parcel",
                     font_size=24, color=TUNE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The answer came from Laplace in 1816. Squeeze air and it warms. In a sound wave the squeezing and "
            "releasing happen hundreds of times a second: far too fast for the heat to leak away. Warm air pushes "
            "back harder, so the air is stiffer than Newton assumed, by a factor of one point four. "
            f"<bookmark mark='a'/> That gives {say(d['laplace'])} metres a second. <bookmark mark='b'/> We can "
            "check both with the row of parcels from the last chapter. One row obeys Newton's gas law, the other "
            "Laplace's. Same push, six metres of tube. <bookmark mark='c'/> "
            f"The first pulse travels at {say(d['newton_sim'])} metres a second. The second at "
            f"{say(d['laplace_sim'])}."
        ) as vo:
            stiff = VGroup(
                MathTex(r"PV = \text{const}", r"\;\Longrightarrow\;", r"\text{stiffness} = P", font_size=34, color=BAD),
                MathTex(r"PV^{\gamma} = \text{const}", r"\;\Longrightarrow\;", r"\text{stiffness} = \gamma P", font_size=34, color=GOOD),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.2)
            tags = VGroup(label(r"slow squeezing: \ the heat leaks away (Boyle)", font_size=22, color=GREY_B).next_to(stiff[0], UP, buff=0.1).align_to(stiff, LEFT),
                          label(r"fast squeezing: \ the heat stays", font_size=22, color=GREY_B).next_to(stiff[1], DOWN, buff=0.1).align_to(stiff, LEFT))
            self.play(FadeIn(card), FadeIn(stiff[0]), FadeIn(tags[0]))
            self.wait(4.0)
            self.play(FadeIn(stiff[1]), FadeIn(tags[1]))
            vo.wait_until("a")
            self.play(Write(law))
            self.play(FadeOut(stiff), FadeOut(tags), run_time=0.4)
            vo.wait_until("b")
            self.play(FadeIn(tracks), FadeIn(names), FadeIn(ticks), FadeIn(p1), FadeIn(p2))
            self.play(tr.animate.set_value(22.0), run_time=max(vo.until("c") + 2.5, 5.0), rate_func=linear)
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(told))
        p1.clear_updaters()
        p2.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def temperature(self):
        d = load("speed")
        c = clip("speed.pipe")
        g = axes([-12, 40], [320, 356], x_length=5.4, y_length=3.4, xlabel=r"temperature ($^\circ$C)", ylabel=r"speed of sound (m/s)",
                 xticks=[-10, 0, 10, 20, 30], yticks=[325, 335, 345, 355], font_size=20)
        g.move_to(LEFT * 3.7 + UP * 0.5)
        ts = np.linspace(-12, 40, 60)
        line = curve(g.ax, ts, [331.3 * np.sqrt(1 + t / 273.15) for t in ts], AIR)
        dots = VGroup(*[Dot(g.ax.c2p(r["c"], r["speed"]), radius=0.06, color=TUNE) for r in d["temps"]])
        law = MathTex(r"c = \sqrt{\gamma R\, T}", font_size=40, color=AIR).next_to(g, UP, buff=0.25)
        pipe = TubeView(width=5.4, bore=0.7).move_to(RIGHT * 3.4 + UP * 1.6)
        pipe.curve.set_stroke(opacity=0)
        ptag = label(rf"an open pipe, \ {100 * d['pipe_len']:.1f} cm", font_size=24, color=GREY_A).next_to(pipe, UP, buff=0.3)
        read = VGroup(label(rf"at {d['cold']:.0f}$^\circ$C: \ {d['pipe_hz']['cold']:.1f} Hz", font_size=30, color=AIR),
                      label(rf"at {d['warm']:.0f}$^\circ$C: \ {d['pipe_hz']['warm']:.1f} Hz", font_size=30, color=RATIO),
                      label(rf"{d['cents']:.0f} cents sharper: \ three quarters of a semitone", font_size=28, color=TUNE)
                      ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(pipe, DOWN, buff=0.7)
        with self.voiceover(
            "Notice what is not in Laplace's formula once you use the gas law: the pressure. Only the temperature "
            "is left. <bookmark mark='a'/> Sound goes about six tenths of a metre a second faster for every degree. "
            "<bookmark mark='b'/> That matters to anyone who plays a wind instrument, because, as we will see in "
            "chapter eight, the note of a pipe is set by the time sound takes to run along it. Here is one pipe, "
            f"cold and then warm."
        ) as vo:
            self.play(FadeIn(g), FadeIn(law))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pipe), FadeIn(ptag))
        shape = np.sin(np.pi * np.linspace(0, 1, 60))
        with self.listen(c) as snd:
            window(snd, r"the pipe cold, \ then warm")
            for ev, row in (("c1", 0), ("c2", 0), ("w1", 1), ("w2", 1)):
                snd.wait_until(ev)
                if ev in ("c1", "w1"):
                    self.add(read[row])
                lens = pipe.lens(shape, amp=0.3, color=AIR if row == 0 else RATIO)
                snd.show(lens)
                t0 = snd.time_of(ev)
                snd.drive(lens, ring(at=t0, rate=6.0, stop_at=t0 + 0.85))
        with self.voiceover(
            f"{say(d['cents'])} cents: three quarters of a semitone, from a change of twenty-five degrees. "
            f"<bookmark mark='a'/> About {say(d['per_degree'])} cents for every degree. This is why an orchestra "
            "tunes after the players have warmed their instruments, and why an organ and a piano that agree in "
            "winter can disagree in summer. <bookmark mark='b'/> It also settles a detail of Krakatoa. The pulse went "
            "round the world at about 313 metres a second: the speed of sound in air at thirty below zero. It filled "
            "the whole depth of the atmosphere, and most of the atmosphere is cold."
        ) as vo:
            self.play(FadeIn(read[2]))
            vo.wait_until("b")
            cold = Dot(g.ax.c2p(-12, 323), radius=0.09, color=BAD)
            self.play(FadeIn(cold), Flash(cold, color=BAD))
        self.wait(0.3)
        self.clear_scene()
