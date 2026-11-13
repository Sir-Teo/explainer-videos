from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord import ClipStore
from explainer.music.monochord.physics import String, pluck_shape, simulate
from videos.music.soundcheck.compute import CACHE, CLIPS

clip = clip_loader(CACHE, CLIPS)


class SoundCheck(SoundScene):
    """Every piece of the sound pipeline once: narration, a listening window with a playhead, events timed like
    bookmarks, a picture driven by the clip's clock, stereo, levels, and the sync reference (a flash on each click)."""

    def construct(self):
        self.sync()
        self.string()
        self.pan_and_levels()

    def sync(self):
        c = clip("clicks.five")
        title = label(r"Sound check", font_size=48).to_edge(UP, buff=0.5)
        lamps = VGroup(*[Square(0.9, stroke_color=GREY_C, stroke_width=2, fill_color=WHITE, fill_opacity=0.0)
                         for _ in range(5)]).arrange(RIGHT, buff=0.4)
        with self.voiceover("This is the sound check. Five clicks, and a square that lights on each one.") as vo:
            self.play(FadeIn(title), FadeIn(lamps))
        with self.listen(c) as snd:
            snd.show(listen_bar(snd, r"five clicks").to_edge(DOWN, buff=0.6), sound_tag("synthesized"))
            for i in range(5):
                snd.wait_until(f"click{i}")
                lamps[i].set_fill(WHITE, opacity=1.0)   # the frame at the click is white: the sync test reads it
                self.wait(1 / 15)
                lamps[i].set_fill(MC.TUNE, opacity=0.5)
        self.clear_scene()

    def string(self):
        c = clip("tone.open")
        s = String.tuned(130.81, L=1.0)
        run = simulate(s, lambda x: pluck_shape(x, s.L, 0.18, 1.0), 2 / s.f1, N=240, snapshot_every=4)
        view = StringView(width=10.0, scale=0.9).shift(UP * 1.6)
        view.set_shape(run.snaps[0])
        spec = Spectrogram(c, width=9.0, height=2.6, fmax=3000,
                           marks=[(130.81 * n, str(n)) for n in (1, 4, 8, 12, 16, 20)]).shift(DOWN * 1.7)
        cap = note(r"the string, slowed 400 times \quad $\cdot$ \quad its sound, at full speed", font_size=22)
        cap.next_to(view, DOWN, buff=0.9)
        with self.voiceover("One pluck of the monochord's open string. <bookmark mark='a'/> Above, the simulated "
                            "string in slow motion. Below, the spectrogram of what you are about to hear.") as vo:
            self.play(FadeIn(view))
            vo.wait_until("a")
            self.play(FadeIn(spec), FadeIn(cap))
        with self.listen(c) as snd:
            snd.show(listen_bar(snd).to_corner(DL, buff=0.4), sound_tag("physical model"))
            snd.drive(view, view.film(run.snaps, run.t_snap[1], slow=400, loop=True))
            snd.drive(spec.playhead, spec.follow())
        self.clear_scene()

    def pan_and_levels(self):
        c, lv = clip("pan.sweep"), clip("levels.steps")
        dots = VGroup(*[Dot(radius=0.16, color=GREY_C) for _ in range(5)]).arrange(RIGHT, buff=1.6).shift(UP * 1.2)
        lr = VGroup(label(r"left", font_size=26, color=GREY_B).next_to(dots, LEFT, buff=0.5),
                    label(r"right", font_size=26, color=GREY_B).next_to(dots, RIGHT, buff=0.5))
        with self.voiceover("Stereo: the same note from left to right.") as vo:
            self.play(FadeIn(dots), FadeIn(lr))
        with self.listen(c) as snd:
            snd.show(listen_bar(snd, r"headphones").to_corner(DL, buff=0.4))
            for i in range(5):
                snd.wait_until(f"p{i}")
                self.play(dots[i].animate.set_color(MC.TUNE).scale(1.4), run_time=0.15)
        bars = VGroup(*[Rectangle(width=1.2, height=h, stroke_width=0, fill_color=MC.LEVEL, fill_opacity=0.9)
                        for h in (2.0, 1.0, 0.5)]).arrange(RIGHT, buff=0.6, aligned_edge=DOWN).shift(DOWN * 2.2)
        tags = VGroup(*[label(t, font_size=24, color=GREY_A).next_to(b, UP, buff=0.1)
                        for t, b in zip((r"0 dB", r"$-6$ dB", r"$-12$ dB"), bars)])
        with self.voiceover("And levels: each tone six decibels below the last.") as vo:
            self.play(FadeIn(bars.set_opacity(0.25)), FadeIn(tags))
        with self.listen(lv) as snd:
            snd.show(listen_bar(snd).to_corner(DR, buff=0.4))
            for i in range(3):
                snd.wait_until(f"s{i}")
                self.play(bars[i].animate.set_opacity(1.0), run_time=0.15)
        self.wait(0.3)
        self.clear_scene()
