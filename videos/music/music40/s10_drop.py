from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Drop(SoundScene):
    def construct(self):
        chapter(self, 9, r"The build, \ the drop and the sidechain", r"How does dance music make tension without chords?")
        self.edm()
        self.hear()
        self.sidechain()
        self.quiz()
        self.studio()

    # ------------------------------------------------------------------
    def edm(self):
        items = [
            (r"electronic dance music, \ from house and techno to the festival `drop' of the 2010s", WHITE),
            (r"form by texture: \ a build-up adds layers, \ density and brightness; \ the drop removes the tension at once", WHITE),
            (r"the build's devices: \ a snare roll doubling its speed, \ a rising noise sweep, \ a filter opening", WHITE),
            (r"tension without a dominant chord: \ rhythm, \ register and timbre do the work", TUNE),
            (r"a build and drop of ours", GREY_A),
        ]
        rows_scene(self, r"the drop", items,
                   "Electronic dance music, from house and techno to the festival anthems of the 2010s, built its form from "
                   "texture. <bookmark mark='b'/> A build-up adds layers, density and brightness; the drop releases the tension "
                   "at once. <bookmark mark='c'/> The build's devices are a snare roll that doubles its speed, a rising sweep of "
                   "noise, and a filter opening. <bookmark mark='d'/> It is tension without a dominant chord: rhythm, register and "
                   "timbre do the work. <bookmark mark='e'/> Here is a build and drop of ours.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("drop")
        c = clip("drop.build")
        beat = 60.0 / d["bpm"]
        W = 11.0
        total = c.duration
        lanes = VGroup()
        names = [(r"snare: \ 4, \ 8, \ 16, \ 32 a bar", EAR, 0.0, d["t_drop"]), (r"noise riser", GREY_A, 0.0, d["t_drop"]),
                 (r"pad, \ filter opening", BLUE, 0.0, d["t_drop"]), (r"kick, \ four on the floor", TUNE, d["t_drop"], total - 1.0),
                 (r"sub-bass", "#A3E635", d["t_drop"], total - 1.0), (r"pad, \ sidechained", BLUE, d["t_drop"], total - 1.0)]
        for k, (name, col, a, b) in enumerate(names):
            x0 = -4.0 + W * 0.0
            r = Rectangle(width=8.8 * (b - a) / total, height=0.35, stroke_width=0, fill_color=col, fill_opacity=0.6)
            r.move_to([-4.0 + 8.8 * a / total + r.width / 2, 1.8 - 0.6 * k, 0])
            lanes.add(VGroup(label(name, font_size=16, color=col).next_to([-4.2, 1.8 - 0.6 * k, 0], LEFT, buff=0.1), r))
        dropx = -4.0 + 8.8 * d["t_drop"] / total
        dline = DashedLine([dropx, 2.2, 0], [dropx, -1.6, 0], color=WHITE)
        dl = label(r"the drop", font_size=20, color=WHITE).next_to(dline, UP, buff=0.1)
        with self.voiceover(
            "Four bars of build: a snare in quarters, then eighths, sixteenths and thirty-seconds; a noise sweep rising; a "
            "pad whose filter opens bar by bar. Then the drop: a drum-machine kick on every beat, a sine sub-bass between "
            "the kicks, and the pad pumping against the kick."
        ):
            self.play(FadeIn(lanes), Create(dline), FadeIn(dl))
        with self.listen(c) as snd:
            window(snd, r"a build and a drop", kind="synthesized", detail=r"noise, \ additive pad, \ drum-machine voices, \ sine sub", corner=DL, tag_corner=DR)
            playhead = Line([-4.0, 2.1, 0], [-4.0, -1.5, 0], color=WHITE, stroke_width=3)
            snd.show(playhead)
            snd.drive(playhead, lambda m, t: m.move_to([-4.0 + 8.8 * min(t, total) / total, 0.3, 0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sidechain(self):
        d = load("drop")
        g = d["gain_shape"]
        x0, W = -5.5, 11.0
        n = len(g)
        curve = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([[x0 + W * k / (n - 1), -1.5 + 2.6 * v, 0] for k, v in enumerate(g)])
        ax = Line([x0, -1.5, 0], [x0 + W, -1.5, 0], color=GREY_D)
        top = DashedLine([x0, 1.1, 0], [x0 + W, 1.1, 0], color=GREY_D)
        kicks = VGroup(*[Triangle(color=EAR, fill_opacity=1).scale(0.12).rotate(PI).move_to([x0 + W * k / 2, 1.5, 0]) for k in (0, 1)])
        labs = VGroup(label(r"kick", font_size=17, color=EAR).next_to(kicks[0], UP, buff=0.1),
                      label(r"the pad's gain: \ down 14 dB at each kick, \ back within a fifth of a second", font_size=19, color=TUNE).to_edge(DOWN, buff=0.7),
                      label(r"full level", font_size=15, color=GREY_A).next_to(top, RIGHT, buff=0.1).shift(LEFT * 1.2 + UP * 0.2))
        side = label(r"a compressor whose key input is the kick: \ the louder the kick, \ the more the pad gives way", font_size=19, color=WHITE).to_edge(UP, buff=1.0)
        head = label(r"the sidechain", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "That pumping is the sidechain. <bookmark mark='a'/> A compressor turns a sound down when something is loud; keyed "
            "from a sidechain input, it listens to a different sound. <bookmark mark='b'/> Key the pad's compressor from the "
            "kick, and the pad ducks fourteen decibels at every kick and swells back within a fifth of a second. It began "
            "as a way to make room for the kick in a mix, and became an effect in its own right, the breathing sound of "
            "house and its descendants. Part 50 builds the compressor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(top), FadeIn(kicks))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(labs))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("drop")
        c = clip("drop.two")
        card = listen_card(r"A pad under a steady kick, \ twice. \ Once the pad is left alone; \ once it is sidechained to the kick. \ "
                           r"Which version pumps: \ the first or the second?", width=10.4)
        with self.voiceover(
            "A question for your ears. A pad under a steady kick, twice: once left alone, once sidechained to the kick. "
            "Which version pumps, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.9)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        self.play(FadeOut(card), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"first, \ then second", kind="synthesized", detail=r"additive pad, \ drum-machine kick", corner=DL, tag_corner=DR)
            st = d["starts2"]
            pulse(snd, boxes[0], st["plain"], st["ducked"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["ducked"], c.duration, buff=0.08)
        ans = label(r"the second: \ the pad dips at every kick and swells back", font_size=22, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover("The second. The pad dips at every kick and swells back between them: four breaths a bar."):
            self.play(FadeIn(ans), boxes[1][0].animate.set_stroke(TUNE, 4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def studio(self):
        items = [
            (r"the producer became the author: \ a track made in software by one person", WHITE),
            (r"loudness rose through the 1990s and 2000s \ (`the loudness war'), \ until streaming services normalised it", WHITE),
            (r"Part 57 measures loudness; \ Part 50 builds compressors; \ Part 53 the digital workstation", WHITE),
            (r"the song is now shaped in the mix as much as in the writing", TUNE),
            (r"chapter 10: \ what sixty years of charts show", GREY_A),
        ]
        rows_scene(self, r"the producer's song", items,
                   "The producer became the author: a track can be made in software by one person. <bookmark mark='b'/> Loudness "
                   "rose through the 1990s and 2000s, the so-called loudness war, until streaming services began to normalise it. "
                   "<bookmark mark='c'/> Part 57 measures loudness, Part 50 builds compressors, and Part 53 the digital "
                   "workstation. <bookmark mark='d'/> The song is now shaped in the mix as much as in the writing. "
                   "<bookmark mark='e'/> Chapter ten asks what sixty years of charts show.", marks="bcde")
