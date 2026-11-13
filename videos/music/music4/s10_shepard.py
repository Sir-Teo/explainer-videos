from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403

NAMES = ("A", r"B$\flat$", "B", "C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$")


class Shepard(SoundScene):
    def construct(self):
        chapter(self, 9, r"Two kinds of high", r"Can a scale rise for ever?", lit=(1863,), extra=((1964, r"Shepard's tones"),))
        self.stairs()
        self.how()
        self.helix()

    def spectrum(self, at=DOWN * 0.6, x_length=10.4, y_length=2.6):
        g = faxes(20, 20000, [0, 1.15], x_length=x_length, y_length=y_length, ylabel="", yticks=[], fticks=(27.5, 110, 440, 1760, 7040), font_size=20)
        g.move_to(at)
        fs = np.geomspace(22, 19000, 200)
        bell = fcurve(g, fs, np.exp(-0.5 * (np.log2(fs / 440.0) / 1.6) ** 2), GREY_B, stroke_width=2)
        return g, bell

    def lines(self, g, step: float) -> VGroup:
        out = VGroup()
        for k in range(10):
            f = 27.5 * 2 ** (k - 1 + (step % 12) / 12.0)
            if 21 < f < 19500:
                a = float(np.exp(-0.5 * (np.log2(f / 440.0) / 1.6) ** 2))
                out.add(Line(g.at(f, 0), g.at(f, a), color=TUNE, stroke_width=5))
        return out

    # ------------------------------------------------------------------
    def stairs(self):
        d = load("shepard")
        c = clip("shepard.stairs")
        q = listen_card(r"A scale that climbs for twenty-four steps. \\ Is the last tone higher than the first?", width=8.6).to_edge(UP, buff=0.4)
        g, bell = self.spectrum()
        ls = self.lines(g, 0)
        count = label(r"step 0", font_size=32, color=TUNE).next_to(g, RIGHT, buff=-1.6).shift(UP * 1.2)
        with self.voiceover(
            "One more experiment on pitch, and it is the strangest. In 1964 Roger Shepard, at Bell Laboratories, "
            "built a set of twelve tones on a computer. Played in order they make a rising scale. Listen to "
            "twenty-four steps of it, and decide: is the last tone higher than the first?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(bell), FadeIn(ls), FadeIn(count))
        with self.listen(c) as snd:
            window(snd, r"twenty-four steps up", kind="synthesized", detail=r"Shepard tones", corner=DL, tag_corner=DR)
            for s in d["steps"]:
                snd.wait_until(f"s{s}")
                self.remove(ls, count)
                ls = self.lines(g, s)
                count = label(rf"step {s}", font_size=32, color=TUNE).move_to(count)
                self.add(ls, count)
                self.play(ls.animate(rate_func=there_and_back).set_stroke(width=8), run_time=0.36)
        res = VGroup(label(r"step 12 and step 24 are not like step 0. \ They \emph{are} step 0:", font_size=28, color=GREY_A),
                     label(rf"largest difference between the waveforms: \ {d['same_as_start']:.1f}", font_size=30, color=GOOD)).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Every step went up. There is no doubt about that; you heard twenty-four rises in a row. And yet the "
            "last tone is not higher than the first. It is the first: the same waveform, sample for sample. So "
            "is the thirteenth. The scale climbed two octaves and arrived exactly where it started, twice."
        ):
            self.play(FadeOut(q), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how(self):
        g, bell = self.spectrum(at=DOWN * 0.2, y_length=3.0)
        s = ValueTracker(0.0)
        ls = always_redraw(lambda: self.lines(g, s.get_value() % 12))
        head = label(r"one Shepard tone: \ partials an octave apart, \ under a fixed curve", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        foot = label(r"twelve steps on, \ every partial stands where its neighbour stood", font_size=28, color=GOOD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the trick. Each of Shepard's tones is made of partials exactly an octave apart, right "
            "across the range of hearing, and their strengths follow a fixed bell-shaped curve: strong in the "
            "middle, fading to nothing at the top and the bottom. <bookmark mark='a'/> To step up, every partial "
            "slides to the right together. The ones near the top fade out as they go. New ones fade in at the "
            "bottom, too quietly to notice. <bookmark mark='b'/> After twelve steps each partial has moved one "
            "octave, and stands exactly where its neighbour stood. The picture is the one we started with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(bell), FadeIn(ls))
            vo.wait_until("a")
            self.play(s.animate.set_value(11.999), run_time=max(vo.until("b") + 1.0, 3.0), rate_func=linear)
            self.play(FadeIn(foot))
        self.wait(0.3)
        ls.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def helix(self):
        circ = Circle(radius=1.5, color=GREY_C, stroke_width=2).move_to(LEFT * 4.0 + DOWN * 0.2)
        names = VGroup(*[label(n, font_size=24, color=GREY_A).move_to(circ.get_center() + 1.9 * np.array([np.sin(TAU * k / 12), np.cos(TAU * k / 12), 0]))
                         for k, n in enumerate(NAMES)])
        ang = ValueTracker(0.0)
        hand = always_redraw(lambda: Line(circ.get_center(), circ.get_center() + 1.5 * np.array([np.sin(ang.get_value()), np.cos(ang.get_value()), 0]),
                                          color=TUNE, stroke_width=5))
        cl = label(r"which note of the twelve: \ \textbf{chroma}", font_size=26, color=TUNE).next_to(circ, DOWN, buff=0.75)
        th = np.linspace(0, 3 * TAU, 300)
        centre = RIGHT * 3.2 + DOWN * 1.9
        hx = VMobject(stroke_color=EAR, stroke_width=4)
        hx.set_points_smoothly([centre + np.array([1.5 * np.sin(t), 0.42 * np.cos(t) + 1.15 * t / TAU, 0]) for t in th])
        cs = VGroup(*[Dot(centre + np.array([0.0, 0.42 + 1.15 * k, 0]), radius=0.09, color=GOOD) for k in range(4)])
        cn = VGroup(*[label(rf"C{k + 2}", font_size=22, color=GOOD).next_to(c_, UR, buff=0.06) for k, c_ in enumerate(cs)])
        up = Arrow(centre + RIGHT * 2.4 + DOWN * 0.2, centre + RIGHT * 2.4 + UP * 3.6, color=AIR, stroke_width=3, buff=0)
        hl = label(r"how high: \ \textbf{height}", font_size=26, color=AIR).rotate(PI / 2).next_to(up, RIGHT, buff=0.12)
        notes = VGroup(label(r"an ordinary scale climbs the spiral: \ round, \ and up", font_size=26, color=EAR),
                       label(r"Shepard's scale goes round, \ and stays level", font_size=26, color=TUNE)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What Shepard had done was to pull apart two things that normally travel together. "
            "<bookmark mark='a'/> One is which note of the twelve a tone is: its position round a circle. "
            "Psychologists call it chroma. <bookmark mark='b'/> The other is simply how high the tone is: its "
            "height. An ordinary scale changes both at once. It goes round the circle, and it climbs, so that "
            "after twelve steps it is back above where it started: a spiral. <bookmark mark='c'/> Shepard's tones "
            "contain every octave at once, so they have a chroma but no particular height. They can only go "
            "round. <bookmark mark='d'/> And this tells us something about the ear. Two tones an octave apart are "
            "judged the same in a way that no other pair is. Why the octave? Because every partial of the upper "
            "note is already a partial of the lower one: the upper note adds nothing new. That is the first fact "
            "of harmony, and it is where Part 5 begins. Composers, meanwhile, use Shepard's staircase whenever "
            "they want tension that climbs and climbs, and never arrives."
        ) as vo:
            self.play(FadeIn(circ), FadeIn(names), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(hand), FadeIn(cl))
            self.play(ang.animate.set_value(TAU), run_time=max(vo.until("b") - 0.2, 1.0), rate_func=linear)
            self.play(Create(hx), GrowArrow(up), FadeIn(hl), FadeIn(notes[0]), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(VGroup(a, b)) for a, b in zip(cs, cn)], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(ang.animate.set_value(3 * TAU), run_time=max(vo.until("d") - 0.2, 1.0), rate_func=linear)
        self.wait(0.3)
        hand.clear_updaters()
        self.clear_scene()
