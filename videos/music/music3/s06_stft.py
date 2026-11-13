from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Spectrogram_(SoundScene):
    pass


class Spectrogram(Spectrogram_):
    def construct(self):
        chapter(self, 5, r"Time and frequency together", r"How do you watch a recipe change?", lit=(1807,),
                extra=((1946, r"Gabor; \ the sound spectrograph"),))
        self.idea()
        self.read()
        self.glide()

    # ------------------------------------------------------------------
    def idea(self):
        from explainer.music.viz import Spectrogram as Sp

        d = load("stft")
        c = clip("stft.phrase")
        y = c.mono
        n = 900
        env = np.abs(y[: len(y) // n * n]).reshape(n, -1).max(axis=1)
        env = env / env.max()
        sp = Sp(c, width=10.4, height=3.2, fmax=2200.0, marks=[(500, "500 Hz"), (1000, "1 kHz"), (2000, "2 kHz")])
        sp.move_to([0, -1.3, 0])
        sp.playhead.set_opacity(0)
        x0, x1, yw = sp.frame.get_left()[0], sp.frame.get_right()[0], 2.6       # the wave sits exactly above its picture
        wave = VGroup(*[Line([x0 + (x1 - x0) * i / n, yw - 0.6 * v, 0], [x0 + (x1 - x0) * i / n, yw + 0.6 * v, 0], color=AIR, stroke_width=1.2)
                        for i, v in enumerate(env)])
        wt = label(r"the Tune's opening: \ pressure against time", font_size=24, color=GREY_A).next_to(wave, UP, buff=0.1)
        cover = Rectangle(width=x1 - x0 + 0.06, height=3.26, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to(sp.frame)
        win = Rectangle(width=0.5, height=1.45, stroke_color=TUNE, stroke_width=2.5, fill_color=TUNE, fill_opacity=0.15).move_to([x0 + 0.25, yw, 0])
        tr = ValueTracker(0.0)
        win.add_updater(lambda m: m.set_x(x0 + 0.25 + (x1 - x0 - 0.5) * tr.get_value()))

        def uncover(m):
            w = max((x1 - x0 + 0.06) * (1 - tr.get_value()), 0.001)
            m.stretch_to_fit_width(w)
            m.set_x(x1 + 0.03 - w / 2)

        cover.add_updater(uncover)
        facts = label(rf"each stretch: \ {d['window_ms']:.0f} ms, \ faded in and out; \ a new one every {d['hop_ms']:.0f} ms", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A spectrum of the whole Tune would tell you which notes are in it, and nothing about their order. "
            "Music is change, and we want to see the recipe changing. <bookmark mark='a'/> So take a short stretch "
            "of the sound, a few hundredths of a second, and find its spectrum. Stand that spectrum up as a column: "
            "frequency upward, brightness for strength. <bookmark mark='b'/> Slide the stretch along a little and "
            "do it again, and again. <bookmark mark='c'/> The columns side by side make a picture of sound: time "
            "across, frequency up. It is called a spectrogram, and since the nineteen forties, when Bell "
            "Laboratories built a machine to draw one, it has been the standard way to look at sound."
        ) as vo:
            self.play(FadeIn(wave), FadeIn(wt))
            vo.wait_until("a")
            self.add(sp, cover)
            self.play(FadeIn(win), FadeIn(sp.frame), FadeIn(facts))
            vo.wait_until("b")
            self.play(tr.animate.set_value(1.0), run_time=max(vo.remaining() - 0.5, 6.0), rate_func=linear)
        win.clear_updaters(), cover.clear_updaters()
        self.remove(cover)
        self.play(FadeOut(win), FadeOut(facts), run_time=0.3)
        self.sp, self.c = sp, c

    # ------------------------------------------------------------------
    def read(self):
        d = load("stft")
        sp, c = self.sp, self.c
        with self.voiceover("Here it is, with the sound."):
            pass
        with self.listen(c) as snd:
            window(snd, r"the Tune's opening, \ and its spectrogram", corner=DL, tag_corner=UR)
            sp.playhead.set_opacity(1)
            snd.drive(sp.playhead, sp.follow())
        sp.playhead.set_opacity(0)
        notes = VGroup(label(r"a level stripe: \ one partial of one note", font_size=26, color=TUNE),
                       label(r"a sharp left edge: \ a pluck", font_size=26, color=AIR),
                       label(r"stripes that fade from the top first: \ the high partials dying soonest", font_size=26, color=RATIO),
                       label(rf"our transform against the standard library's: \ the same to 15 decimal places", font_size=24, color=GOOD)
                       ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Learn to read it, because we will use it in every part from here on. <bookmark mark='a'/> A level "
            "stripe is one partial of one note. Each note is a stack of stripes, evenly spaced: its harmonics. "
            "<bookmark mark='b'/> A sharp left edge is a pluck: the instant the note begins. <bookmark mark='c'/> "
            "And the stripes fade from the top downward, because, as we found in Part 1, a string's high partials "
            "die first. <bookmark mark='d'/> One check before we rely on it: our own transform and the standard "
            "library's agree to the last decimal place."
        ) as vo:
            self.play(sp.animate.shift(UP * 1.1), run_time=0.6)
            for mark, nrow in zip("abcd", notes):
                vo.wait_until(mark)
                self.play(FadeIn(nrow, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glide(self):
        from explainer.music.viz import Spectrogram as Sp

        d = load("stft")
        c = clip("stft.glide")
        sp = Sp(c, width=10.0, height=3.8, fmax=2000.0, marks=[(392, "392 Hz"), (784, "784"), (1176, "1176"), (1568, "1568")])
        sp.move_to(DOWN * 0.2)
        sp.playhead.set_opacity(0)
        head = label(rf"Part 2's horn, \ passing at {d['pass_kmh']:.0f} km/h", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A spectrogram earns its keep when the pitch moves. Here is the horn from Part 2, driving past. "
            "<bookmark mark='a'/> Four stripes, its four partials, level while it approaches, sliding down as it "
            "passes, level again as it leaves. And notice that the stripes stay evenly spaced the whole way: each "
            "partial falls by the same ratio, so the horn keeps its character while its pitch drops. Watch it and "
            "listen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sp))
        with self.listen(c) as snd:
            window(snd, r"a horn passing: \ its partials slide down together", kind="synthesized", detail=r"Part 2's passing horn", corner=DL, tag_corner=UR)
            sp.playhead.set_opacity(1)
            snd.drive(sp.playhead, sp.follow())
        sp.playhead.set_opacity(0)
        self.wait(0.3)
        self.clear_scene()

