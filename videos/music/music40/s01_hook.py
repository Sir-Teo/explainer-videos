from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.thirty()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        card = listen_card(r"The same song of ours, \ twice, \ with two different openings. \ "
                           r"In each, \ how long before the singer comes in: \ about five seconds, \ ten, \ or twenty?", width=10.4)
        with self.voiceover(
            "A question for your ears. The same song of ours, twice, with two different openings. In each, how long before "
            "the singer comes in: about five seconds, ten, or twenty?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        W = 11.0
        rows_ = VGroup()
        for name, col in (("long", BLUE), ("short", TUNE)):
            bar = Rectangle(width=W, height=0.45, stroke_color=GREY_B, stroke_width=1.2)
            rows_.add(VGroup(label({"long": r"first", "short": r"second"}[name], font_size=20, color=col), bar).arrange(RIGHT, buff=0.4))
        rows_.arrange(DOWN, buff=0.9, aligned_edge=RIGHT).move_to(UP * 0.3)
        scale = 32.0
        ticks = VGroup()
        for s in range(0, 33, 5):
            x = rows_[1][1].get_left()[0] + W * s / scale
            ticks.add(VGroup(Line([x, -1.3, 0], [x, -1.15, 0], color=GREY_B), label(f"{s} s", font_size=15, color=GREY_A).move_to([x, -1.5, 0])))
        self.play(FadeOut(card), FadeIn(rows_), FadeIn(ticks))
        for name, k, col in (("long", 0, BLUE), ("short", 1, TUNE)):
            c = clip("hook.long") if name == "long" else clip("hook.short")
            bar = rows_[k][1]
            fill = Rectangle(width=0.01, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.6).align_to(bar, LEFT).align_to(bar, DOWN)
            with self.listen(c) as snd:
                window(snd, {"long": r"the first opening", "short": r"the second"}[name], kind="synthesized",
                       detail=r"guitar, \ bass, \ drums, \ a model voice", corner=DL, tag_corner=DR)
                snd.show(fill)
                x0 = bar.get_left()[0]
                snd.drive(fill, lambda m, t, x0=x0: m.stretch_to_fit_width(max(W * min(t, scale) / scale, 0.01)).move_to([x0 + max(W * min(t, scale) / scale, 0.01) / 2, m.get_center()[1], 0]))
            self.add(fill.copy().stretch_to_fit_width(W * min(c.duration, scale) / scale).align_to(bar, LEFT))
        marks = VGroup()
        for name, k in (("long", 0), ("short", 1)):
            x = rows_[k][1].get_left()[0] + W * d["enters"][name] / scale
            marks.add(VGroup(Line([x, rows_[k][1].get_bottom()[1] - 0.1, 0], [x, rows_[k][1].get_top()[1] + 0.1, 0], color=EAR, stroke_width=5),
                             label(rf"voice: \ {d['enters'][name]:.0f} s", font_size=18, color=EAR).next_to(rows_[k][1], UP, buff=0.08).set_x(x)))
        ans = label(r"about twenty, \ then about five: \ the hit single's intro, \ 1980s against 2010s", font_size=22, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "About twenty seconds in the first, and about five in the second. That is roughly what happened to the hit single. "
            "A study of top-ten singles in America found that the average introduction shrank from over twenty seconds in "
            "the mid-1980s to about five by the mid-2010s."
        ):
            self.play(FadeIn(marks), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thirty(self):
        items = [
            (r"Hubert L\'eveill\'e Gauvin \ (2018): \ 303 US top-ten singles, \ 1986--2015", WHITE),
            (r"intros shrank by about four fifths; \ the voice and the title arrived sooner; \ tempos rose", WHITE),
            (r"some services count streams after thirty seconds; \ payment terms vary", WHITE),
            (r"a listener who skips before then costs the song its income: \ form follows the medium", TUNE),
            (r"this part follows the popular song from the sheet-music standard to the drop", GREY_A),
        ]
        rows_scene(self, r"the thirty-second rule", items,
                   "The study was Hubert Léveillé Gauvin's, in 2018: three hundred and three American top-ten singles from 1986 to 2015. <bookmark mark='b'/> The intros shrank by about four fifths, the voice and the title arrived sooner, and tempos rose. <bookmark mark='c'/> Why? One possible incentive: some major streaming services count a stream after thirty seconds, although payment arrangements vary. <bookmark mark='d'/> That threshold may encourage an early hook, but this historical trend does not by itself establish streaming as its cause. <bookmark mark='e'/> This part follows the popular song from the sheet-music standard to the drop, and finds each form shaped by the technology that sold it.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"AABA to verse--chorus; \ loops and rock harmony; \ riffs",
            r"the backbeat and groove: \ rock, \ funk, \ disco, \ house, \ trap",
            r"hooks and prosody",
            r"the drum machine: \ an 808 from first principles",
            r"sampling, \ the break, \ and flow, \ measured",
            r"the build, \ the drop and the sidechain; \ sixty years of charts",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. From AABA to verse and chorus, loops and rock harmony, and riffs. <bookmark mark='b'/> The "
            "backbeat and groove, from rock to trap. <bookmark mark='c'/> Hooks, and how words sit on beats. "
            "<bookmark mark='d'/> The drum machine, with an 808 built from first principles. <bookmark mark='e'/> Sampling, "
            "the break, and rap's flow, measured. <bookmark mark='f'/> And the build, the drop and the sidechain; then what "
            "sixty years of charts show. Every song, riff, beat and verse is ours; the voice is Part 17's model, which sings "
            "vowels rather than words."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
