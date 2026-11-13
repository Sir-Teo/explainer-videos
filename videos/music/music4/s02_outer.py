from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Outer(SoundScene):
    def construct(self):
        chapter(self, 1, r"From air to water", r"How does a wave in air get into a fluid?", lit=(1863,),
                extra=((1863, r"Helmholtz on the middle ear"),))
        self.journey()
        self.transformer()
        self.canal()

    # ------------------------------------------------------------------
    def journey(self):
        d = load("outer")
        m = d["middle"]
        ear = ear_diagram().scale(1.25).move_to(UP * 1.45 + LEFT * 0.6)
        names = VGroup(
            label(r"ear canal, \ 2.5 cm", font_size=24, color=AIR).next_to(ear.canal, UP, buff=0.25).shift(RIGHT * 0.7),
            label(r"eardrum", font_size=24, color=FORCE).next_to(ear.drum, DOWN, buff=0.25),
            label(r"three bones", font_size=24, color=BONE).next_to(ear.bones, UP, buff=0.3).shift(RIGHT * 0.1),
            label(r"cochlea: \ a coiled tube of fluid", font_size=24, color=FLUID).next_to(ear.cochlea, DOWN, buff=0.2),
        )
        ratio = m["z_cochlea"] / m["z_air"]
        f = MathTex(r"\text{fraction of the power that gets in} \;=\; \frac{4\,Z_1 Z_2}{(Z_1+Z_2)^2}", font_size=34).move_to(DOWN * 1.35)
        num = label(rf"air: \ $Z_1 = {m['z_air']:.0f}$ \qquad the cochlea's entrance: \ $Z_2 \approx {ratio:.0f}\,Z_1$ \qquad"
                    rf"$\Rightarrow$ \ {100 * m['without']:.1f}\%", font_size=28, color=GREY_A).move_to(DOWN * 2.35)
        pool = label(r"(why you cannot hear the poolside from under water)", font_size=22, color=GREY_B).move_to(DOWN * 3.1)
        with self.voiceover(
            "Follow a sound in. <bookmark mark='a'/> It enters the ear canal, a tube about two and a half "
            "centimetres long, and at the end of it pushes on the eardrum. <bookmark mark='b'/> Behind the eardrum "
            "are three bones, the smallest in your body: the hammer, the anvil and the stirrup. <bookmark mark='c'/> "
            "And the stirrup pushes on a window into the cochlea: a coiled tube, the size of a pea, filled with "
            "fluid. That is where hearing happens, and the fluid is a problem. <bookmark mark='d'/> In Part 2 we "
            "found that when a wave meets a medium that pushes back harder, most of it bounces off, and we had a "
            "formula for the part that gets through. <bookmark mark='e'/> The fluid at the cochlea's entrance "
            f"pushes back about {say(ratio)} times harder than air does. Put that in the formula, and only "
            f"{say(100 * m['without'], 1)} percent of the sound's power gets in. Ninety-nine percent would bounce "
            "off the side of your head. It is the reason you cannot hear people at the poolside when you are "
            "under the water."
        ) as vo:
            self.play(FadeIn(ear.pinna))
            vo.wait_until("a")
            self.play(FadeIn(ear.canal), FadeIn(ear.drum), FadeIn(names[0]), FadeIn(names[1]))
            vo.wait_until("b")
            self.play(FadeIn(ear.bones), FadeIn(names[2]))
            vo.wait_until("c")
            self.play(Create(ear.cochlea), FadeIn(names[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(f))
            vo.wait_until("e")
            self.play(FadeIn(num))
            self.wait(max(vo.remaining() - 5.0, 0.1))
            self.play(FadeIn(pool))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transformer(self):
        d = load("outer")
        m = d["middle"]
        title = label(r"A worked example: \ the middle ear as a transformer", font_size=34).to_edge(UP, buff=0.4)
        big = Circle(radius=1.25, stroke_color=FORCE, stroke_width=4, fill_color=FORCE, fill_opacity=0.15).move_to(LEFT * 4.6 + UP * 0.5)
        small = Circle(radius=1.25 / np.sqrt(m["area_ratio"]), stroke_color=FORCE, stroke_width=4, fill_color=FORCE, fill_opacity=0.5).move_to(LEFT * 1.5 + UP * 0.5)
        rod = Line(big.get_right(), small.get_left(), color=BONE, stroke_width=7)
        t1 = VGroup(label(r"eardrum", font_size=24, color=GREY_A), label(r"55 mm$^2$", font_size=26, color=RATIO)).arrange(DOWN, buff=0.08).next_to(big, DOWN, buff=0.2)
        t2 = VGroup(label(r"the stirrup's footplate", font_size=24, color=GREY_A), label(r"3.2 mm$^2$", font_size=26, color=RATIO)).arrange(DOWN, buff=0.08).next_to(small, DOWN, buff=0.75)
        steps = VGroup(
            MathTex(r"\text{pressure} = \frac{\text{force}}{\text{area}}", font_size=34),
            MathTex(rf"\text{{the same force on }}\tfrac{{55}}{{3.2}} = {m['area_ratio']:.0f}\text{{ times less area}}", font_size=30),
            MathTex(rf"\text{{the bones are a lever: }}\times {m['lever']:.1f}", font_size=30),
            MathTex(rf"\text{{pressure}}\;\times\;{m['pressure_gain']:.0f}", font_size=38, color=GOOD),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(RIGHT * 3.3 + UP * 0.7)
        ask = pause_card(rf"Pressure is multiplied by {m['pressure_gain']:.0f}. \\ How many decibels is that?", width=7.0).move_to(RIGHT * 0.2 + DOWN * 2.6)
        ans = VGroup(MathTex(rf"20\log_{{10}} {m['pressure_gain']:.0f} = {m['gain_db']:.0f}\ \text{{dB}}", font_size=36, color=GOOD),
                     label(rf"power into the cochlea: \ {100 * m['without']:.0f}\% \ $\rightarrow$ \ {100 * m['with']:.0f}\%", font_size=30, color=GOOD)
                     ).arrange(RIGHT, buff=0.9).move_to(DOWN * 2.6)
        with self.voiceover(
            "The three bones are the answer, and here is how they work. Pressure is force divided by area. "
            "<bookmark mark='a'/> The eardrum collects the air's push over about fifty-five square millimetres. "
            "The bones carry that force to the stirrup's footplate, which is only three point two. "
            f"<bookmark mark='b'/> The same force on {say(m['area_ratio'])} times less area is "
            f"{say(m['area_ratio'])} times the pressure. <bookmark mark='c'/> And the bones are also a lever, "
            f"which adds a factor of one point three. <bookmark mark='d'/> Altogether the pressure at the window "
            f"is about {say(m['pressure_gain'])} times the pressure at the eardrum. Pause, and turn that into "
            "decibels."
        ) as vo:
            self.play(FadeIn(title), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(big), FadeIn(t1), FadeIn(rod), FadeIn(small), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Twenty times the logarithm of {say(m['pressure_gain'])} is {say(m['gain_db'])} decibels. The middle "
            "ear does for sound what a low gear does on a bicycle: it trades a large, easy motion for a small, "
            f"forceful one. In our model the share of the power that reaches the fluid rises from "
            f"{say(100 * m['without'])} percent to {say(100 * m['with'])}. And it tells you what happens when the "
            "middle ear is blocked, by fluid behind the eardrum in a child with a cold, or by bones that have "
            "stiffened with age: a loss of twenty or thirty decibels, which is exactly what doctors measure."
        ):
            self.play(FadeOut(ask), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def canal(self):
        d = load("outer")
        hz = round(d["canal_hz"], -2)
        tube = TubeView(width=5.0, bore=0.8, left="open", right="closed").move_to(LEFT * 3.4 + UP * 1.9)
        tl = label(r"the ear canal: \ 2.5 cm, \ closed by the eardrum", font_size=24, color=GREY_A).next_to(tube, UP, buff=0.25)
        ask = pause_card(r"A pipe closed at one end, \ 2.5 cm long. \\ What is its lowest resonance?", width=6.4).move_to(LEFT * 3.4 + DOWN * 0.3)
        ans = MathTex(rf"f = \frac{{c}}{{4L}} \approx {hz:,.0f}\ \text{{Hz}}".replace(",", "{,}"), font_size=40, color=GOOD).move_to(LEFT * 3.4 + DOWN * 0.2)
        g = faxes(100, 12000, [-10, 30], x_length=5.6, y_length=3.4, ylabel=r"quietest sound you can hear (dB)", yticks=[-10, 0, 10, 20, 30], font_size=20)
        g.move_to(RIGHT * 3.4 + DOWN * 0.4)
        thr = fcurve(g, d["f"], d["threshold"], EAR)
        dip = Dot(g.at(d["best_hz"], float(np.min(d["threshold"]))), radius=0.09, color=GOOD)
        dl = label(rf"most sensitive near {round(d['best_hz'], -2):,.0f} Hz".replace(",", "{,}"), font_size=22, color=GOOD).next_to(dip, UP, buff=1.0).shift(LEFT * 1.0)
        lens = tube.lens(np.cos(np.linspace(0, np.pi / 2, 40)), amp=0.3, color=AIR)
        with self.voiceover(
            "One more piece of acoustics before we go inside, and you can do it yourself. The ear canal is a pipe "
            "two and a half centimetres long, open at the outside and closed at the far end by the eardrum. "
            "<bookmark mark='a'/> Part 2 built exactly this pipe. Pause, and work out its lowest resonance."
        ) as vo:
            self.play(FadeIn(tube), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A pipe closed at one end holds a quarter of a wave, so its lowest resonance is the speed of sound "
            f"divided by four times its length: about {say(hz)} hertz. <bookmark mark='a'/> Now look at a "
            "measurement: the quietest sound a young listener can hear, at each frequency. The lower the curve, the "
            f"better the ear. <bookmark mark='b'/> Its best point is near {say(round(d['best_hz'], -2))} hertz, "
            "where the canal resonates. Your ear is most sensitive where its own front door rings, and that "
            "happens to be the region of a baby's cry and of the consonants of speech. We will come back to "
            "this curve in chapter four."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans), FadeIn(lens))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(thr), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(dip), FadeIn(dl))
        self.wait(0.3)
        self.clear_scene()
