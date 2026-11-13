from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Beats(SoundScene):
    def construct(self):
        chapter(self, 3, r"Beats", r"What do two tones do when they are almost the same?", lit=(1701,), extra=((1700, r"Sauveur counts beats"),))
        self.sum()
        self.three()
        self.tuning()
        self.fast()

    # ------------------------------------------------------------------
    def sum(self):
        t = np.linspace(0, 1, 1600)
        f1, f2 = 20.0, 22.0
        ga = axes([0, 1], [-1.2, 1.2], x_length=9.6, y_length=1.0, xlabel="", ylabel="", xticks=None, yticks=[], font_size=18)
        gb = axes([0, 1], [-1.2, 1.2], x_length=9.6, y_length=1.0, xlabel="", ylabel="", xticks=None, yticks=[], font_size=18)
        gs = axes([0, 1], [-2.3, 2.3], x_length=9.6, y_length=1.9, xlabel="", ylabel="", xticks=None, yticks=[], font_size=18)
        VGroup(ga, gb, gs).arrange(DOWN, buff=0.3).move_to(LEFT * 0.9 + UP * 0.9)
        a = curve(ga.ax, t, np.sin(2 * np.pi * f1 * t), AIR, stroke_width=2.5)
        b = curve(gb.ax, t, np.sin(2 * np.pi * f2 * t), TUNE, stroke_width=2.5)
        s = curve(gs.ax, t, np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t), WHITE, stroke_width=2.5)
        env = VGroup(curve(gs.ax, t, 2 * np.abs(np.cos(np.pi * (f2 - f1) * t)), LEVEL, stroke_width=2.5),
                     curve(gs.ax, t, -2 * np.abs(np.cos(np.pi * (f2 - f1) * t)), LEVEL, stroke_width=2.5))
        tags = VGroup(label(r"20 cycles", font_size=22, color=AIR).next_to(ga, RIGHT, buff=0.2), label(r"22 cycles", font_size=22, color=TUNE).next_to(gb, RIGHT, buff=0.2),
                      label(r"their sum", font_size=22).next_to(gs, RIGHT, buff=0.2))
        marks = VGroup(*[label(t_, font_size=20, color=c_).move_to(gs.ax.c2p(x, 2.75)) for t_, x, c_ in
                         ((r"in step", 0.0, GOOD), (r"opposed", 0.25, BAD), (r"in step", 0.5, GOOD), (r"opposed", 0.75, BAD), (r"in step", 1.0, GOOD))])
        eq = MathTex(r"\sin 2\pi f_1 t + \sin 2\pi f_2 t \;=\; 2\,", r"\cos\!\bigl(\pi (f_1 - f_2)\, t\bigr)", r"\;\sin\!\bigl(2\pi\,\tfrac{f_1+f_2}{2}\,t\bigr)", font_size=32).move_to(DOWN * 2.2)
        eq[1].set_color(LEVEL)
        rule = label(r"one tone at the average frequency, \ swelling and fading $|f_1 - f_2|$ times a second", font_size=28, color=LEVEL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Take two pure tones that are almost the same, and add them. <bookmark mark='a'/> Here one makes "
            "twenty cycles while the other makes twenty-two. At the start they move together, and the sum is "
            "twice as big. <bookmark mark='b'/> A quarter of the way along, the faster one has gained half a "
            "cycle. Now one pushes while the other pulls, and they cancel. Then they are back in step, then "
            "opposed again. <bookmark mark='c'/> The sum is a single tone whose strength rises and falls. Those "
            "are beats, and one line of trigonometry gives the whole story. <bookmark mark='d'/> The sum of two "
            "sines is a sine at the average frequency, multiplied by a slow cosine at half the difference. The "
            "loudness peaks twice in each turn of that cosine, so the beats come at exactly the difference of "
            "the two frequencies. Two more cycles in one tone than the other: two beats."
        ) as vo:
            self.play(FadeIn(ga), FadeIn(gb), Create(a), Create(b), FadeIn(tags[0]), FadeIn(tags[1]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(gs), Create(s), FadeIn(tags[2]), run_time=2.0)
            self.play(FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[1:]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("c")
            self.play(Create(env[0]), Create(env[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(eq))
            self.wait(max(vo.remaining() - 5.0, 0.1))
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("beats")
        c = clip("beats.three")
        gaps = d["gaps"]
        bx = boxes([rf"{d['f']:.0f} and {d['f'] + g:.0f} Hz" for g in gaps], buff=0.6, width=3.7, height=2.2, font_size=26).move_to(UP * 0.4)
        for b in bx:
            b[1].next_to(b[0], DOWN, buff=0.15)
        rates = VGroup(*[label(rf"{g:.0f} beat" + ("s" if g > 1 else "") + " a second", font_size=26, color=LEVEL).next_to(b[1], DOWN, buff=0.12) for g, b in zip(gaps, bx)])
        shapes = VGroup()
        for g, b in zip(gaps, bx):
            m = VMobject(stroke_color=LEVEL, stroke_width=2, fill_color=LEVEL, fill_opacity=0.18)
            m.set_points_as_corners(envelope_shape(b[0], lambda u, g=g: abs(np.cos(np.pi * g * u)), 0.0, 1.2 if g < 8 else 0.6))
            shapes.add(m)
        with self.voiceover(
            "Listen to it. Three pairs of pure tones near the A above middle C. The first pair is one hertz "
            "apart, the second four, the third twelve."
        ):
            self.play(FadeIn(bx), FadeIn(rates), FadeIn(shapes))
        with self.listen(c) as snd:
            window(snd, r"1, \ 4 and 12 beats a second", kind="synthesized", detail=r"pairs of pure tones", corner=DL, tag_corner=DR)
            for g, b, shape in zip(gaps, bx, shapes):
                t0 = snd.time_of(f"b{int(g)}")
                box = b[0]
                snd.drive(shape, lambda m, t, g=g, box=box, t0=t0: m.set_points_as_corners(
                    envelope_shape(box, lambda u, g=g, t0=t0: abs(np.cos(np.pi * g * (u - t0))), min(max(t, t0), t0 + 3.0), 1.2 if g < 8 else 0.6))
                    .set_fill(opacity=0.5 if t0 <= t < t0 + 3.0 else 0.18))
                snd.wait_until(t0 + 3.05)
        with self.voiceover(
            "At one a second you can follow each swell. At four you can still count. At twelve the beats have "
            "become a flutter, too fast to count but easy to hear."
        ):
            self.play(Indicate(rates, color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuning(self):
        d = load("beats")
        w = d["worked"]
        c = clip("beats.tuning")
        title = label(r"A worked example: \ tuning one string to another", font_size=36).to_edge(UP, buff=0.45)
        ask = pause_card(rf"One string gives {w['a']:.0f} Hz. \ Its neighbour, \ meant to match it, \ gives {w['b']:.0f} Hz. \\ What does the tuner hear?", width=8.6).move_to(UP * 1.3)
        ans = label(rf"{w['beats']:.0f} beats a second. \quad Slacken the string until they slow, \ and stop.", font_size=30, color=GOOD).move_to(UP * 1.3)
        g = axes([0, 8], [0, 7], x_length=8.6, y_length=2.4, xlabel=r"seconds", ylabel=r"beats a second", xticks=[0, 2, 4, 6, 8], yticks=[0, 2, 4, 6], font_size=20)
        g.move_to(DOWN * 1.35)
        line = VGroup(Line(g.ax.c2p(0, 6), g.ax.c2p(6, 0), color=LEVEL, stroke_width=3), Line(g.ax.c2p(6, 0), g.ax.c2p(8, 0), color=GOOD, stroke_width=4))
        dot = Dot(g.ax.c2p(0, 6), radius=0.11, color=TUNE)
        with self.voiceover(
            "A worked example, and it is the oldest precision measurement in music. A string sounds at two "
            "hundred and twenty hertz. Its neighbour, which is supposed to match it, is at two hundred and "
            "twenty-two. What does the tuner hear? Pause, and say."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Two beats a second. And that tells the tuner exactly what to do: change the tension, and listen. If "
            "the beats speed up, turn the other way. If they slow down, keep going, until they stop. "
            "<bookmark mark='a'/> Here is a tone being lowered onto another, from six hertz sharp. Listen to the "
            "beats slow down and vanish."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(line), FadeIn(dot))
        with self.listen(c) as snd:
            window(snd, r"one tone lowered onto another", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            secs = d["tune_seconds"]
            snd.drive(dot, lambda m, t: m.move_to(g.ax.c2p(min(t, 8.0), max(6.0 * (1 - t / secs), 0.0))).set_color(GOOD if t >= secs else TUNE)
                      .scale_to_fit_width(0.22 * (1.0 + 0.5 * abs(np.cos(np.pi * 0.5 * (12 * min(t, secs) - t * min(t, secs))))) if t < secs else 0.3))
        with self.voiceover(
            "No instrument is needed to do that, only patience. A tuner can match two strings to a fraction of a "
            "hertz by ear, which is finer than any pitch you could name. Joseph Sauveur was using beats to "
            "measure frequencies in 1700, before anyone could count vibrations any other way. And beats are how "
            "we will tune an entire keyboard, in Part 6."
        ):
            self.play(Indicate(line[1], color=GOOD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fast(self):
        g = axes([0, 80], [0, 1.15], x_length=9.6, y_length=2.6, xlabel=r"beats a second", ylabel="", xticks=[0, 10, 20, 30, 40, 60, 80], yticks=[], font_size=20)
        g.move_to(DOWN * 0.6)
        zones = VGroup(
            Rectangle(width=g.ax.c2p(8, 0)[0] - g.ax.c2p(0, 0)[0], height=2.6, stroke_width=0, fill_color=GOOD, fill_opacity=0.18).move_to((g.ax.c2p(0, 0) + g.ax.c2p(8, 1.15)) / 2),
            Rectangle(width=g.ax.c2p(20, 0)[0] - g.ax.c2p(8, 0)[0], height=2.6, stroke_width=0, fill_color=TUNE, fill_opacity=0.18).move_to((g.ax.c2p(8, 0) + g.ax.c2p(20, 1.15)) / 2),
            Rectangle(width=g.ax.c2p(80, 0)[0] - g.ax.c2p(20, 0)[0], height=2.6, stroke_width=0, fill_color=BAD, fill_opacity=0.18).move_to((g.ax.c2p(20, 0) + g.ax.c2p(80, 1.15)) / 2))
        names = VGroup(label(r"a slow swell: \ pleasant", font_size=24, color=GOOD).next_to(zones[0], UP, buff=0.5).shift(LEFT * 0.2),
                       label(r"a flutter", font_size=24, color=TUNE).next_to(zones[1], UP, buff=0.12),
                       label(r"a harsh buzz: \ roughness", font_size=26, color=BAD).move_to(g.ax.c2p(48, 0.6)))
        card = history_card(1863, r"Hermann von Helmholtz", r"this roughness \emph{is} dissonance. Consonance is its absence.", width=5.6).to_corner(UL, buff=0.4)
        with self.voiceover(
            "What happens when the beats go faster still? You heard it in Part 4. <bookmark mark='a'/> A few beats "
            "a second are a gentle swell, even a pleasant one: it is the shimmer of a choir or of an accordion. "
            "<bookmark mark='b'/> Past ten or so they become a flutter. <bookmark mark='c'/> And somewhere beyond "
            "twenty a second you can no longer hear them as separate events at all. What is left is a harsh "
            "buzzing quality in the sound: roughness. <bookmark mark='d'/> In 1863 Helmholtz made that buzz into "
            "a theory. Dissonance, he said, is nothing but roughness: beats too fast to follow, grating on the "
            "ear. And consonance is nothing but its absence. It is a physical cause, and it is smooth: a sound "
            "can be a little rough. It is exactly the kind of thing chapter one told us to look for. The "
            "question is whether it is true."
        ) as vo:
            self.play(FadeIn(g))
            for mark, z, n in zip("abc", zones, names):
                vo.wait_until(mark)
                self.play(FadeIn(z), FadeIn(n), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()
