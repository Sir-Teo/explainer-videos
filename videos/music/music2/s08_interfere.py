from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Interfere(SoundScene):
    def construct(self):
        chapter(self, 7, r"Two sources", r"What happens where two sounds meet?", lit=(1807,),
                extra=((1801, r"Young: \ waves add"),))
        self.pattern()
        self.rule()
        self.walk()
        self.worked()

    def field(self, d, width=6.0):
        fv = FieldView(d["frames"], d["extent"], width=width, loop=True)
        return fv

    # ------------------------------------------------------------------
    def pattern(self):
        d = load("interfere")
        fv = self.field(d).move_to(LEFT * 3.5 + DOWN * 0.2)
        srcs = VGroup(*[Dot(fv.point(*s), radius=0.08, color=TUNE) for s in d["sources"]])
        cap = label(rf"two sources, \ {d['gap']:.1f} m apart, \ both sounding {d['hz']:.0f} Hz", font_size=24, color=GREY_A).next_to(fv, UP, buff=0.15)
        loud = heat_image(d["rms"][::-1], 0.0, float(np.percentile(d["rms"], 99.5)), width=6.0)
        loud.stretch_to_fit_height(6.0 * d["extent"][1] / d["extent"][0]).move_to(RIGHT * 3.5 + DOWN * 0.2)
        cap2 = label(r"how loud it is at each place", font_size=24, color=GREY_A).next_to(loud, UP, buff=0.15)
        with self.voiceover(
            "Sound waves are small, so two of them in the same air simply add. Where both push, the air is pushed "
            "twice as hard. Where one pushes and the other pulls, nothing happens. <bookmark mark='a'/> Here are two "
            "sources sounding the same tone, a little over a metre apart. <bookmark mark='b'/> And here, on the "
            "right, is how loud the tone is at each place. The space is striped. Along the bright bands the two "
            "waves arrive in step. Along the dark ones they arrive exactly out of step, and a listener standing "
            "there hears almost nothing, with two sources playing at full strength."
        ) as vo:
            self.play(FadeIn(fv), FadeIn(srcs), FadeIn(cap))
            self.play(fv.tracker.animate(run_time=vo.until("b"), rate_func=linear).set_value(vo.until("b") * 6))
            self.add(loud, cap2)
            start = fv.tracker.get_value()
            left = vo.remaining() + 0.1
            self.play(fv.tracker.animate(run_time=left, rate_func=linear).set_value(start + left * 6))
        self.fv, self.loud = fv, loud
        self.keep = Group(fv, srcs, cap, loud, cap2)

    # ------------------------------------------------------------------
    def rule(self):
        d = load("interfere")
        self.play(FadeOut(self.fv), FadeOut(self.keep[1]), FadeOut(self.keep[2]), run_time=0.4)
        loud = self.loud
        w, h = loud.width, loud.height
        c0 = loud.get_center()

        def P(x, y):
            return c0 + np.array([(x / d["extent"][0] - 0.5) * w, (y / d["extent"][1] - 0.5) * h, 0])

        xs, ex = d["x"], d["exact"]
        i_q = int(np.argmin(np.where((xs > 4.2) & (xs < 5.6), ex, 9)))
        i_l = int(np.argmax(np.where((xs > 4.6) & (xs < 6.2), ex, -1)))
        s1, s2 = d["sources"]
        pts = {"quiet": (xs[i_q], d["line_y"]), "loud": (4.0, d["line_y"])}
        lam = d["wavelength"]
        rows = VGroup()
        for name, col in (("loud", GOOD), ("quiet", BAD)):
            x, y = pts[name]
            r1, r2 = np.hypot(x - s1[0], y - s1[1]), np.hypot(x - s2[0], y - s2[1])
            diff = abs(r1 - r2) / lam
            rows.add(VGroup(label(rf"a {name} place", font_size=30, color=col),
                            MathTex(rf"|r_1 - r_2| = {abs(r1 - r2):.2f}\ \text{{m}} = {diff:.2f}\,\lambda", font_size=34)).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(LEFT * 3.4 + UP * 1.0)
        thm = VGroup(label(r"in step where the paths differ by $0, \lambda, 2\lambda, \ldots$", font_size=28, color=GOOD),
                     label(r"out of step where they differ by $\tfrac{1}{2}\lambda, \tfrac{3}{2}\lambda, \ldots$", font_size=28, color=BAD)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(LEFT * 3.4 + DOWN * 1.6)
        rays = VGroup()
        for name, col in (("loud", GOOD), ("quiet", BAD)):
            x, y = pts[name]
            rays.add(VGroup(Line(P(*s1), P(x, y), color=col, stroke_width=2.5), Line(P(*s2), P(x, y), color=col, stroke_width=2.5),
                            Dot(P(x, y), radius=0.08, color=col)))
        ask = label(r"Which places are loud, \ and which are quiet?", font_size=32, color=TUNE).move_to(LEFT * 3.4 + UP * 2.6)
        self.play(FadeIn(ask), run_time=0.4)
        with self.voiceover(
            "The rule is simple geometry. Pick a place and measure its distance from each source. "
            "<bookmark mark='a'/> If the two distances are equal, or differ by a whole number of wavelengths, the "
            "waves arrive in step. <bookmark mark='b'/> If they differ by half a wavelength, crest meets trough. "
            "Thomas Young worked this out for light in 1801, and used it to argue that light was a wave. For sound "
            "you can check it by walking about."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(rays[0]), FadeIn(rows[0]), FadeIn(thm[0]))
            vo.wait_until("b")
            self.play(Create(rays[1]), FadeIn(rows[1]), FadeIn(thm[1]))
        self.wait(0.3)
        self.play(FadeOut(rows), FadeOut(thm), FadeOut(rays), FadeOut(ask), run_time=0.4)

    # ------------------------------------------------------------------
    def walk(self):
        d = load("interfere")
        c = clip("interfere.walk")
        loud = self.loud
        w, h = loud.width, loud.height
        c0 = loud.get_center()

        def P(x, y):
            return c0 + np.array([(x / d["extent"][0] - 0.5) * w, (y / d["extent"][1] - 0.5) * h, 0])

        path = DashedLine(P(1.0, d["line_y"]), P(7.0, d["line_y"]), color=WHITE, stroke_width=1.5)
        mic = Dot(P(1.0, d["line_y"]), radius=0.1, color=EAR)
        g = axes([1, 7], [0, 1.1], x_length=6.0, y_length=2.6, xlabel=r"position along the walk (m)", ylabel=r"pressure, \ relative",
                 xticks=[1, 3, 5, 7], yticks=[0, 0.5, 1], font_size=20)
        g.move_to(LEFT * 3.5 + UP * 0.9)
        ex = curve(g.ax, d["x"], d["exact"], GOOD, stroke_width=2)
        sim = curve(g.ax, d["x"], d["sim"], TUNE, stroke_width=3)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=TUNE, stroke_width=3), label(r"simulated", font_size=22, color=TUNE)).arrange(RIGHT, buff=0.12),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=GOOD, stroke_width=2), label(r"the exact field of two sources", font_size=22, color=GOOD)).arrange(RIGHT, buff=0.12)
                     ).arrange(RIGHT, buff=0.5).next_to(g, DOWN, buff=0.2)
        head = Line(g.ax.c2p(1, 0), g.ax.c2p(1, 1.1), color=WHITE, stroke_width=2)
        meter = Meter(width=0.45, height=1.5).move_to(LEFT * 5.6 + DOWN * 2.7)
        mtag = label(r"what the microphone hears", font_size=22, color=GREY_B).next_to(meter, RIGHT, buff=0.25)
        with self.voiceover(
            "Take a microphone along the dashed line, at a metre a second. <bookmark mark='a'/> The curve is the "
            "pressure it should find. The simulation and the exact formula for two sources agree to within "
            f"{say(100 * d['worst'])} percent of the peak. The quietest spot is {say(-d['quiet_db'])} decibels below "
            "the loudest. Listen to the walk."
        ) as vo:
            self.play(Create(path), FadeIn(mic), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(sim), Create(ex), FadeIn(leg), FadeIn(meter), FadeIn(mtag))
        env = d["walk_env"]
        with self.listen(c) as snd:
            window(snd, r"a walk through the pattern", kind="synthesized", detail=r"its level from the computed field",
                   corner=DR, tag_corner=UR)
            snd.show(head)
            snd.drive(mic, lambda m, t: m.move_to(P(1.0 + min(t, 6.0), d["line_y"])))
            snd.drive(head, lambda m, t: m.set_x(g.ax.c2p(1.0 + min(t, 6.0), 0)[0]))
            snd.drive(meter, meter.follow(env))
        with self.voiceover(
            "One tone, two sources, and a listener who hears it come and go eight times in six metres."
        ):
            pass
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        cb = load("interfere")["comb"]
        title = label(r"A worked example: \ two loudspeakers, one seat", font_size=36).to_edge(UP, buff=0.45)
        spk = VGroup(*[Square(0.5, color=TUNE, fill_opacity=0.3) for _ in range(2)]).arrange(RIGHT, buff=4.0).move_to(UP * 1.9)
        seat = Dot(DOWN * 0.6 + RIGHT * 0.9, radius=0.12, color=EAR)
        rays = VGroup(Line(spk[0].get_bottom(), seat.get_center(), color=GREY_B, stroke_width=2), Line(spk[1].get_bottom(), seat.get_center(), color=GREY_B, stroke_width=2))
        tag = label(rf"this seat is {100 * cb['extra']:.0f} cm nearer the right-hand speaker", font_size=26, color=RATIO).next_to(seat, DOWN, buff=0.3)
        ask = pause_card(r"Both speakers play the same music. \\ Which frequency is cancelled at this seat?", width=8.6).move_to(DOWN * 2.4)
        ans = VGroup(MathTex(rf"\tfrac{{1}}{{2}}\lambda = {100 * cb['extra']:.0f}\ \text{{cm}}", r"\;\Longrightarrow\;", rf"f = {cb['nulls'][0]:.0f}\ \text{{Hz}}", font_size=40),
                     label(rf"and again at {cb['nulls'][1]:,.0f} and {cb['nulls'][2]:,.0f} Hz: \ a comb of missing notes".replace(",", "{,}"), font_size=28, color=GREY_A)
                     ).arrange(DOWN, buff=0.25).move_to(DOWN * 2.3)
        ans[0][2].set_color(TUNE)
        with self.voiceover(
            "A worked example. Two loudspeakers play the same music, and your seat is thirty-four centimetres "
            "nearer to one of them than to the other. <bookmark mark='a'/> Which frequency is cancelled where you "
            "sit? Pause, and work it out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(spk), FadeIn(seat), Create(rays), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"The one whose half wavelength is thirty-four centimetres: {say(cb['nulls'][0])} hertz, about the C "
            "above middle C. <bookmark mark='a'/> And every odd multiple of it as well. The music reaches you with a "
            "row of notches cut out of it, like the teeth of a comb, and the notches fall somewhere else in the next "
            "seat. That is why the same recording sounds different from every seat when it comes from two "
            "loudspeakers, a problem Part 58 has to deal with. It is also how noise-cancelling headphones work: they "
            "are a second source, placed so that your ear is always in a dark band."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans[0]))
            vo.wait_until("a")
            self.play(FadeIn(ans[1]))
        self.wait(0.3)
        self.clear_scene()
