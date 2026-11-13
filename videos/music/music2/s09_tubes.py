from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Tubes(SoundScene):
    def construct(self):
        chapter(self, 8, r"Air in a pipe", r"What are the notes of a tube?", lit=(1636, 1753),
                extra=((1948, r"Levine and Schwinger: \ the open end"),))
        self.modes()
        self.listen_pair()
        self.worked()
        self.end()
        self.quiz()

    def column(self, kind: str, y0: float, d: dict, x: float = 0.0) -> VGroup:
        shapes = d["shape_open" if kind == "open" else "shape_stopped"]
        row = d["rows"][kind]
        out = VGroup()
        for i in range(3):
            tv = TubeView(width=4.2, bore=0.5, left="open" if kind == "open" else "closed", right="open")
            tv.curve.set_stroke(opacity=0)
            tv.move_to([x, y0 - 0.95 * i, 0])          # placed before its blur is made: a Lens keeps its end points
            lens = tv.lens(shapes[i], amp=0.2, color=harmonic_color(i + 1 if kind == "open" else 2 * i + 1))
            f = label(rf"{row['sim'][i]:.1f} Hz \ {flat_name(row['notes'][i])}", font_size=24, color=FREQ).next_to(tv, RIGHT, buff=0.25)
            out.add(VGroup(tv, lens, f))
        return out

    # ------------------------------------------------------------------
    def modes(self):
        d = load("tubes")
        left = self.column("open", 1.2, d, x=-4.6)
        right = self.column("stopped", 1.2, d, x=1.9)
        # a pulse meeting each kind of end (drawn from the two rules, to show them)
        demo = VGroup()
        trk = ValueTracker(0.0)
        for j, (name, sign) in enumerate(((r"a closed end: \ the pulse comes back the same way up", 1.0),
                                          (r"an open end: \ it comes back upside down", -1.0))):
            tv = TubeView(width=4.6, bore=0.9, left="open", right="closed" if sign > 0 else "open")
            tv.curve.set_stroke(opacity=0)
            tv.move_to([3.4, 1.2 - 2.2 * j, 0])
            tr_ = Trace(tv.p(0.0), tv.p(1.0), scale=0.33, color=FORCE)
            xs_ = np.linspace(0, 1, 160)

            def upd(m, sign=sign):
                u = trk.get_value() % 2.0
                going = np.exp(-((xs_ - u) / 0.07) ** 2) if u <= 1.0 else np.zeros_like(xs_)
                back = sign * np.exp(-((xs_ - (2.0 - u)) / 0.07) ** 2)
                m.set_shape(going + back)

            tr_.add_updater(upd)
            demo.add(VGroup(tv, tr_, label(name, font_size=24, color=GREY_A).next_to(tv, DOWN, buff=0.15)))
        heads = VGroup(label(r"open at both ends", font_size=30, color=AIR).next_to(left, UP, buff=0.3),
                       label(r"stopped at one end", font_size=30, color=AIR).next_to(right, UP, buff=0.3))
        laws = VGroup(MathTex(r"f_n = n\,\frac{c}{2L}", r"\qquad n = 1, 2, 3, \ldots", font_size=36).next_to(left, DOWN, buff=0.4),
                      MathTex(r"f_n = (2n - 1)\,\frac{c}{4L}", r"\qquad 1, 3, 5, \ldots", font_size=36).next_to(right, DOWN, buff=0.4))
        cap = label(rf"the same pipe, \ {100 * d['L']:.1f} cm long: \ the blur is the pressure inside", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.35)
        chk = label(rf"simulated pipe against the formulas: \ within {max(d['rows']['open']['worst_cents'], d['rows']['stopped']['worst_cents'], 0.01):.2f} cents",
                    font_size=24, color=GOOD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Send a pulse of pressure down a pipe and it comes back from the end, whether the end is closed or open. "
            "At a closed end the air has nowhere to go, and the pressure piles up. At an open end the pressure is "
            "pinned to that of the room outside, so the pulse returns upside down. <bookmark mark='a'/> In a pipe "
            "open at both ends the pressure can only swing in between, and the patterns that fit are the ones we met "
            "on the string: one half-wave, two, three. Their frequencies are whole multiples of the first. "
            "<bookmark mark='b'/> Now stop one end. The pressure swings most at the stopped end and not at all at the "
            "open one, so only a quarter of a wave fits. <bookmark mark='c'/> The lowest note is an octave lower than "
            "before, from the same length of pipe. And the next patterns are three quarter-waves and five: only the "
            "odd multiples. The even ones are missing."
        ) as vo:
            self.play(FadeIn(heads[0]), *[FadeIn(g[0]) for g in left], FadeIn(cap), FadeIn(demo))
            self.play(trk.animate.set_value(vo.until("a") * 0.45), run_time=vo.until("a"), rate_func=linear)
            for g in demo:
                g[1].clear_updaters()
            self.play(FadeOut(demo), run_time=0.3)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[1]), FadeIn(g[2])) for g in left], lag_ratio=0.5), FadeIn(laws[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(heads[1]), *[FadeIn(g[0]) for g in right])
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[1]), FadeIn(g[2])) for g in right], lag_ratio=0.5), FadeIn(laws[1]), run_time=4.0)
            self.play(FadeOut(cap), FadeIn(chk))
        self.left, self.right = left, right
        self.wait(0.3)

    # ------------------------------------------------------------------
    def listen_pair(self):
        d = load("tubes")
        c, b = clip("tubes.pair"), clip("tubes.blown")
        with self.voiceover(
            "Here is that pipe, given one sharp push of air: first open at both ends, then with one end stopped."
        ):
            self.play(Indicate(self.left[0][0], color=TUNE, scale_factor=1.02), Indicate(self.right[0][0], color=TUNE, scale_factor=1.02))
        with self.listen(c) as snd:
            window(snd, r"open, \ open, \ stopped, \ stopped")
            for ev, col in (("o1", self.left), ("o2", self.left), ("s1", self.right), ("s2", self.right)):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                for i, g in enumerate(col):
                    snd.drive(g[1], lambda m, t, t0=t0, i=i: m.set_amp(float(np.exp(-(5.0 + 4.0 * i) * (t - t0))) if t0 <= t < t0 + 0.85 else 0.25))
                snd.wait_until(t0 + 0.85)
        for g in [*self.left, *self.right]:
            g[1].set_amp(1.0)
        with self.voiceover(
            "And the same two pipes with a breath blown across the end. The breath is noise: a hiss with every "
            "frequency in it. The pipe keeps its own."
        ):
            pass
        with self.listen(b) as snd:
            window(snd, r"blown across: \ open, \ then stopped")
            for ev, col, end in (("open", self.left, snd.time_of("stopped")), ("stopped", self.right, b.duration)):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                for i, g in enumerate(col):
                    snd.drive(g[1], lambda m, t, t0=t0, end=end, i=i: m.set_amp(
                        0.25 + 0.75 * (0.6 + 0.4 * np.sin(23 * t + i)) if t0 <= t < min(end - 0.2, t0 + 1.7) else 0.25))
                snd.wait_until(end - 0.25)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        w = load("tubes")["worked"]
        title = label(r"A worked example: \ a flute and a clarinet", font_size=36).to_edge(UP, buff=0.45)
        fl = TubeView(width=5.6, bore=0.5, left="open", right="open")
        fl.curve.set_stroke(opacity=0)
        fl.move_to(LEFT * 3.3 + UP * 1.6)
        cl = TubeView(width=5.6 * w["clar_len"] / w["flute_len"], bore=0.5, left="closed", right="open")
        cl.curve.set_stroke(opacity=0)
        cl.move_to(LEFT * 3.3 + DOWN * 0.3).align_to(fl, LEFT)
        ft = VGroup(label(rf"a flute: \ open at both ends, \ {100 * w['flute_len']:.0f} cm", font_size=26, color=GREY_A),
                    MathTex(r"\frac{c}{2L} = 262\ \text{Hz: middle C}", font_size=34, color=TUNE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        ft.next_to(fl, RIGHT, buff=0.5)
        ct = label(rf"a clarinet: \ about {100 * w['clar_len']:.0f} cm, \ closed by its reed", font_size=26, color=GREY_A).next_to(cl, RIGHT, buff=0.5).align_to(ft, LEFT)
        ask = pause_card(r"The two tubes are nearly the same length. \\ What is the clarinet's lowest note?", width=8.6).move_to(DOWN * 2.2)
        ans = VGroup(MathTex(rf"\frac{{c}}{{4L}} = {w['clar_hz']:.0f}\ \text{{Hz}}", font_size=40, color=TUNE),
                     label(rf"nearly an octave below the flute: \ a real clarinet's bottom note is D, \ {w['clar_real']:.0f} Hz", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.1)
        with self.voiceover(
            "A worked example, with two real instruments. A flute is a pipe open at both ends, about sixty-six "
            "centimetres long. <bookmark mark='a'/> The formula gives 262 hertz: middle C, which is indeed a flute's "
            "lowest note. <bookmark mark='b'/> A clarinet is nearly the same length, but the reed closes one end. "
            "Predict its lowest note."
        ) as vo:
            self.play(FadeIn(title), FadeIn(fl), FadeIn(ft[0]))
            vo.wait_until("a")
            self.play(FadeIn(ft[1]))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(ct), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"A stopped pipe sounds c over four L: {say(w['clar_hz'])} hertz, nearly an octave below the flute. A "
            f"real clarinet's bottom note is the D at {say(w['clar_real'])}. <bookmark mark='a'/> Two instruments "
            "of the same size, an octave apart at the bottom, and all because of what happens at one end."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def end(self):
        d = load("tubes")
        fv = FieldView(d["frames"], d["extent"], width=8.4, solid=d["solid"], loop=True).move_to(LEFT * 2.2 + UP * 0.5)
        cap = label(rf"a stopped pipe {100 * d['plane_len']:.0f} cm long in open air, \ seen in section, \ sounding its lowest note",
                    font_size=24, color=GREY_B).next_to(fv, DOWN, buff=0.2)
        rows = VGroup(
            label(rf"ideal, \ $c/4L$: \ {d['plane_ideal']:.0f} Hz", font_size=28, color=GREY_A),
            label(rf"simulated: \ {d['plane_f1']:.0f} Hz", font_size=28, color=TUNE),
            label(rf"it sounds like a pipe \\ {100 * d['plane_eff']:.0f} cm long", font_size=28, color=RATIO),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.6 + UP * 0.9)
        real = label(r"a round pipe of radius $r$ sounds $0.61\,r$ longer at each open end \ (Levine and Schwinger, 1948)",
                     font_size=26, color=GOOD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One correction, which every flute and organ builder has to make. The pressure is not pinned exactly at "
            "the open end. <bookmark mark='a'/> Here is a stopped pipe in open air, in section. The air just outside "
            "the mouth moves with the air inside, so the pipe behaves as if it were a little longer than it is. "
            f"<bookmark mark='b'/> Our sixty-centimetre pipe should sound {say(d['plane_ideal'])} hertz. It sounds "
            f"{say(d['plane_f1'])}: the note of a pipe {say(100 * d['plane_eff'])} centimetres long. "
            "<bookmark mark='c'/> For a real, round pipe the extra length is about six tenths of the radius at each "
            "open end. That is also where the sound gets out: the little that leaks from the mouth is all you hear."
        ) as vo:
            self.play(FadeIn(fv), FadeIn(cap))
            fv.start(14.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(real))
            self.wait(vo.remaining() + 0.1)
        fv.stop()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("tubes")
        c = clip("tubes.quiz")
        q = listen_card(r"Two pipes, \ A and B, \ sounding the same note. \\ One is open at both ends. \ The other is "
                        r"half as long, \ and stopped. \ Which is the stopped one?", width=10.4).to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                                label(t, font_size=60, color=GREY_A)) for t in ("A", "B")]).arrange(RIGHT, buff=2.6).shift(UP * 0.1)
        with self.voiceover("A question for your ears. Two pipes sounding the same note. One is open at both ends. The "
                            "other is half as long, and stopped at one end. Which is the stopped one?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"pipe A twice, \ then pipe B twice", tag_corner=DR)
            for key, box, end in (("A", boxes[0], snd.time_of("B") - 0.3), ("B", boxes[1], c.duration)):
                for sub in ("c0", "c1"):
                    t0 = snd.time_of(f"{key}.{sub}")
                    snd.wait_until(t0)
                    box[1].set_color(EAR)
                    glow = box[0].copy().set_stroke(EAR, width=5)
                    snd.show(glow)
                    snd.drive(glow, lambda m, t, t0=t0: m.set_stroke(opacity=float(np.exp(-5.0 * max(t - t0, 0))) if t < t0 + 0.85 else 0.0))
                    snd.wait_until(t0 + 0.85)
                box[1].set_color(GREY_A)
        bars = VGroup(*[partial_bars(np.array(d["quiz_partials"][k]), width=3.4, height=1.5, db=False) for k in ("A", "B")])
        for b, box in zip(bars, boxes):
            b.next_to(box, DOWN, buff=0.4)
        tags = VGroup(label(r"stopped: \ odd partials only", font_size=24, color=GOOD).next_to(bars[0], DOWN, buff=0.15),
                      label(r"open: \ all of them", font_size=24, color=GREY_A).next_to(bars[1], DOWN, buff=0.15))
        with self.voiceover(
            f"{d['quiz_answer']}. Same note, but with the second, fourth and sixth partials missing, which gives a "
            "stopped pipe its hollow, woody sound. <bookmark mark='a'/> A clarinet behaves like a stopped pipe, a "
            "flute like an open one, and that difference is a large part of why you can tell them apart. We will "
            "build both in Part 8."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(tags), boxes[0][0].animate.set_stroke(GOOD, width=4))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
