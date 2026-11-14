from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403

ZONES = [(0.4, 1 / 1.8, r"separate events", GREY_D), (1 / 1.8, 4.0, r"a beat", GOOD), (4.0, 10.0, r"too fast to tap: \\ divisions of a beat", TUNE),
         (10.0, 20.0, r"a flutter", GREY_B), (20.0, 50.0, r"a tone", AIR)]


class Pulse(SoundScene):
    def construct(self):
        chapter(self, 1, r"A pulse", r"How fast can a beat be, \ and how slow?", extra=((1815, r"Maelzel's metronome"),))
        self.metronome()
        self.sweep()
        self.window()
        self.tapping()
        self.pair()

    # ------------------------------------------------------------------
    def metronome(self):
        rows = VGroup()
        for bpm in (60, 120):
            n = 4 if bpm == 60 else 8
            tk = ticks([k * 60.0 / bpm for k in range(n + 1)], 0.0, 4.0, width=8.0, height=0.5, color=TUNE)
            rows.add(VGroup(tk, label(rf"{bpm} to the minute: \ one every {60 / bpm:g} s", font_size=28, color=GREY_A).next_to(tk, UP, buff=0.3)))
        rows.arrange(DOWN, buff=1.0).move_to(UP * 0.6)
        eq = MathTex(r"\text{seconds between beats} = \frac{60}{\text{beats per minute}}", font_size=40).to_edge(DOWN, buff=0.9)
        body = Polygon([-0.9, -1.6, 0], [0.9, -1.6, 0], [0.3, 1.6, 0], [-0.3, 1.6, 0], color=GREY_B, stroke_width=3, fill_color=GREY_E, fill_opacity=0.5)
        arm = VGroup(Line(ORIGIN, UP, color=WHITE, stroke_width=4), Rectangle(width=0.34, height=0.22, stroke_width=0, fill_color=TUNE, fill_opacity=1.0))
        clock = ValueTracker(0.0)

        def swing_arm(m, dt):                                        # a pendulum that follows the body wherever it is put
            clock.increment_value(dt)
            h = body.height
            pivot = body.get_bottom() + UP * 0.16 * h
            a = 0.42 * np.sin(2 * np.pi * clock.get_value())
            tip = pivot + 0.78 * h * np.array([np.sin(a), np.cos(a), 0.0])
            m[0].put_start_and_end_on(pivot, tip)
            m[1].set_width(0.105 * h).move_to(pivot + 0.68 * (tip - pivot))

        swing_arm(arm, 0.0)
        arm.add_updater(swing_arm)
        with self.voiceover(
            "The simplest rhythm is a pulse: one sound after another, evenly spaced. Musicians measure "
            "its speed, the tempo, in beats per minute, and since 1815, when Maelzel put his metronome "
            "on sale, they have been able to write that number at the top of a score. "
            "<bookmark mark='a'/> Sixty to the minute is one beat every second. <bookmark mark='b'/> A "
            "hundred and twenty is one every half second. <bookmark mark='c'/> Sixty divided by the tempo "
            "gives the time between beats, and that time is what the ear and the body actually deal with."
        ) as vo:
            self.play(FadeIn(body), FadeIn(arm))
            vo.wait_until("a")
            self.play(body.animate.scale(0.55).to_corner(UL, buff=0.6), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        arm.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def axis(self):
        d = load("tempo")
        lo, hi = np.log10(d["rate0"]), np.log10(d["rate1"])
        width = 12.0
        X = lambda rate: -width / 2 + width * (np.log10(rate) - lo) / (hi - lo)          # noqa: E731
        base = Line([X(d["rate0"]), 0, 0], [X(d["rate1"]), 0, 0], color=GREY_C, stroke_width=2)
        g = VGroup(base)
        g.zones = VGroup()
        for k, (a, b, name, col) in enumerate(ZONES):
            r = Rectangle(width=X(b) - X(a), height=0.9, stroke_width=0, fill_color=col, fill_opacity=0.28).move_to([(X(a) + X(b)) / 2, 0.45, 0])
            g.zones.add(VGroup(r, label(name, font_size=22, color=GREY_B if k == 0 else col).move_to(r.get_center() + UP * 0.95)))
        g.add(g.zones)
        for rate, text in ((0.5, r"one every 2 s"), (1, r"1 a second"), (2, r"2"), (5, r"5"), (10, r"10"), (20, r"20"), (50, r"50")):
            g.add(Line([X(rate), -0.1, 0], [X(rate), 0.1, 0], color=GREY_B, stroke_width=2), label(text, font_size=20, color=GREY_B).move_to([X(rate), -0.38, 0]))
        g.X = X
        return g

    def sweep(self):
        d = load("tempo")
        c = clip("tempo.sweep")
        ax = self.axis().move_to(UP * 0.3)
        self.ax = ax
        note = listen_note(r"clicks that speed up steadily. \ Notice when you can first tap along, \\ when you no longer can, \ and when the clicks turn into a note.", width=9.6, font_size=26).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How slow can a pulse be, and still be felt as a pulse? And how fast? Here is a train of "
            "clicks that speeds up steadily, from one every two and a half seconds to fifty a second. "
            "Notice three moments: when you can first tap along, when you no longer can, and when the "
            "clicks turn into a note."
        ):
            self.play(FadeIn(ax[0]), *[FadeIn(m) for m in ax[2:]], FadeIn(note))
        self.play(FadeOut(note))
        g = np.log(d["rate1"] / d["rate0"]) / d["seconds"]
        marker = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1.0).scale(0.14).rotate(PI).move_to([ax.X(d["rate0"]) + ax.get_center()[0] * 0 , ax[0].get_y() + 1.25, 0])
        y_m = marker.get_y()
        x0, x1 = ax[0].get_left()[0], ax[0].get_right()[0]
        lamp = Dot(radius=0.2, color=TUNE).move_to(DOWN * 1.9)
        self.add(marker, lamp)
        times = np.asarray(d["times"])
        with self.listen(c) as snd:
            window(snd, r"clicks, \ faster and faster", kind="synthesized", detail=r"clicks", corner=DL, tag_corner=DR)
            snd.drive(marker, lambda m, t: m.move_to([x0 + (x1 - x0) * min(max(t, 0.0) / d["seconds"], 1.0), y_m, 0]))
            snd.drive(lamp, lambda m, t: m.set_opacity(float(np.exp(-18.0 * max(t - times[max(np.searchsorted(times, t, side="right") - 1, 0)], 0.0)))))
        self.remove(lamp)
        self.marker = marker

    # ------------------------------------------------------------------
    def window(self):
        d = load("tempo")
        ax, marker = self.ax, self.marker
        lim = d["limits"]
        best = VGroup(Line([ax.X(1 / lim["preferred_s"]) + ax.get_center()[0] * 0, ax[0].get_y(), 0], [ax.X(1 / lim["preferred_s"]), ax[0].get_y() + 0.9, 0], color=WHITE, stroke_width=4))
        best.add(label(r"about two a second: \ where tapping is steadiest", font_size=24, color=WHITE).next_to(best[0], DOWN, buff=0.75))
        with self.voiceover(
            "Slower than about one click every two seconds, there is no beat: each click is an event by "
            "itself, and you cannot predict the next. <bookmark mark='a'/> Then a window opens. From "
            "about two seconds between beats down to a quarter of a second, you can tap along, walk, or "
            "dance. <bookmark mark='b'/> Faster than that, your hand cannot keep up, but you still hear "
            "a rhythm; these are the divisions of a beat, and they run out at about ten to the second. "
            "<bookmark mark='c'/> Then comes a flutter. And at about twenty a second the clicks fuse into "
            "a tone with a pitch, as Part 4 found. <bookmark mark='d'/> So the beat lives in a window "
            "only three octaves wide. In the middle of it, near two beats a second, people tap most "
            "steadily, and that is the tempo of a brisk walk, and of a great deal of dance music."
        ) as vo:
            self.play(FadeOut(marker), FadeIn(ax.zones[0]))
            vo.wait_until("a")
            self.play(FadeIn(ax.zones[1]))
            vo.wait_until("b")
            self.play(FadeIn(ax.zones[2]))
            vo.wait_until("c")
            self.play(FadeIn(ax.zones[3]), FadeIn(ax.zones[4]))
            vo.wait_until("d")
            self.play(FadeIn(best))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tapping(self):
        beat = [k * 1.0 for k in range(7)]
        cl = ticks(beat, -0.5, 6.5, width=11.0, height=0.7, color=TUNE, stroke_width=5).move_to(UP * 1.2)
        tp = ticks([b - 0.1 for b in beat], -0.5, 6.5, width=11.0, height=0.7, color=LOW, stroke_width=5).move_to(DOWN * 0.4)
        lc = label(r"the clicks", font_size=26, color=TUNE).next_to(cl, UP, buff=0.25).align_to(cl, LEFT)
        lt = label(r"a listener's taps", font_size=26, color=LOW).next_to(tp, DOWN, buff=0.25).align_to(tp, LEFT)
        guides = VGroup(*[DashedLine([cl.x_of(b), cl.base.get_y(), 0], [cl.x_of(b), tp.base.get_y() + 0.7, 0], color=GREY_D, stroke_width=1.5, dash_length=0.06) for b in beat])
        early = label(r"early, \ by a few hundredths of a second, \ and the tapper does not know it", font_size=28, color=LOW).to_edge(DOWN, buff=1.1)
        react = label(r"a reaction to each click would be late, \ by about a fifth of a second", font_size=26, color=GREY_B).next_to(early, DOWN, buff=0.25)
        with self.voiceover(
            "One more fact about the beat, before we build on it. Ask people to tap along with a "
            "metronome, and measure when the finger lands. <bookmark mark='a'/> It lands early: a few "
            "hundredths of a second before the click, time after time, and the tapper does not know it. "
            "<bookmark mark='b'/> If we were reacting to each click, we would be late, by a fifth of a "
            "second or so. We are not reacting. We are predicting when the next beat will come, and "
            "aiming at it. A beat is not a sound. It is a prediction that sounds keep confirming."
        ) as vo:
            self.play(FadeIn(cl), FadeIn(lc))
            vo.wait_until("a")
            self.play(FadeIn(guides), LaggedStart(*[GrowFromEdge(m, DOWN) for m in tp.marks], lag_ratio=0.25), FadeIn(tp.base), FadeIn(lt), FadeIn(early), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(react))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pair(self):
        d = load("tempo")
        c = clip("tempo.pair")
        card = listen_card(r"Nine strokes, \ twice. \ Which is faster: \ A or B?", width=8.0)
        with self.voiceover("How finely can we judge a tempo? Nine strokes, twice. Which is faster: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"a wood block, \ modelled", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 1.0)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
        ans = VGroup(label(rf"A: \ {d['bpm_a']:.0f} to the minute", font_size=30, color=GREY_A), label(rf"B: \ {d['bpm_b']:.0f}", font_size=30, color=GOOD)).arrange(RIGHT, buff=1.0).move_to(DOWN * 1.6)
        with self.voiceover(
            f"B. It was {say(d['bpm_b'])} to the minute against {say(d['bpm_a'])}: five per cent faster. "
            "That is close to the limit for most of us. A listener can usually tell two tempos apart "
            "when they differ by a few per cent of the time between beats, whatever the tempo is; "
            "practised musicians do a little better. Tempo, like pitch and loudness, is judged by ratios."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
