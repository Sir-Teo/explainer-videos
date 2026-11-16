from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Bright(SoundScene):
    def construct(self):
        chapter(self, 3, r"Loudness and brightness", r"Is a loud note just a soft note turned up?")
        self.quiz_like()
        self.why()
        self.swell()
        self.ranges_db()
        self.balance()

    # ------------------------------------------------------------------
    def quiz_like(self):
        d = load("bright")
        c = clip("bright.two")
        def bars(db, col):
            g = VGroup(Line([0, 0, 0], [4.2, 0, 0], color=GREY_D))
            for k, v in enumerate(db[:12]):
                h = 1.6 * max(0.0, 1 + v / 70.0)
                g.add(Rectangle(width=0.25, height=max(h, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([0.35 * (k + 0.5), h / 2, 0]))
            return g
        soft = VGroup(label(rf"blown softly: \ brightness {round(d['centroid']['soft'])} Hz", font_size=19, color=BLUE), bars(d["profiles"]["soft"], BLUE)).arrange(DOWN, buff=0.2)
        loud = VGroup(label(rf"blown hard: \ brightness {round(d['centroid']['loud'])} Hz", font_size=19, color=EAR), bars(d["profiles"]["loud"], EAR)).arrange(DOWN, buff=0.2)
        g = VGroup(soft, loud).arrange(RIGHT, buff=1.2).move_to(UP * 0.2)
        cap = label(r"brightness: \ the spectral centroid, \ the power-weighted average frequency of the harmonics", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"Part 8's trumpet model, \ one note, \ two breaths", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        ghost = VGroup(*[VGroup(RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.9)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        card = listen_card(r"One trumpet note, \ twice, \ played back at exactly the same level. \ "
                           r"One was blown softly and turned up, \ one blown hard and turned down. \ Which was blown hard?", width=10.4)
        with self.voiceover(
            "Is a loud note just a soft note turned up? A question for your ears. Part 8's trumpet model, the physical model "
            "itself, plays one note twice, and both are played back at exactly the same level. One was blown softly and "
            "turned up, the other blown hard and turned down. Which was blown hard, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card), FadeIn(head), FadeIn(ghost))
        with self.listen(c) as snd:
            window(snd, r"same level, \ two breaths", detail=r"Part 8's lip-reed trumpet", corner=DL, tag_corner=DR)
            pulse(snd, ghost[0], d["starts"]["soft"], d["starts"]["loud"] - 0.3, buff=0.12)
            pulse(snd, ghost[1], d["starts"]["loud"], c.duration, buff=0.12)
        with self.voiceover(
            "The second. Blown softly, the note is almost only its fundamental; blown hard, the upper harmonics rise by tens "
            "of decibels, and turning it down does not take them away. The brightness, measured as the spectral centroid, "
            "roughly doubles. Your ear heard the effort, not the level."
        ):
            self.play(FadeOut(ghost), FadeIn(g), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"in brass, \ the sound wave steepens as it travels down the tube at high pressure: \ shock-like fronts, \ the `brassy' blare", WHITE),
            (r"in our model, \ harder blowing makes the lips close more abruptly: \ sharper pulses, \ more harmonics", WHITE),
            (r"the ear judges loudness partly by brightness: \ a bright note sounds loud even when played quietly", WHITE),
            (r"so a fortissimo cannot be faked by turning a piano up: \ the colour gives it away", TUNE),
            (r"Part 4's loudness, \ and Part 3's spectrum, \ working together", GREY_A),
        ]
        rows_scene(self, r"why louder is brighter", items,
                   "Why? <bookmark mark='b'/> In real brass at high pressure, the sound wave steepens as it travels down the tube, almost into shock fronts: the brassy blare. <bookmark mark='c'/> In our model, which has no such steepening, harder blowing makes the lips close more abruptly, and sharper pulses carry more harmonics. <bookmark mark='d'/> And the ear judges loudness partly by brightness: brightness can influence inferred effort and loudness, but the relation depends on the spectrum and level. <bookmark mark='e'/> So a fortissimo cannot be faked by turning up a pianissimo; the colour gives it away. <bookmark mark='f'/> Part 4's loudness and Part 3's spectrum, working together.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def balance(self):
        items = [
            (r"instruments differ in power: \ a trumpet at forte can cover a whole woodwind section", WHITE),
            (r"dynamic markings are relative: \ the same \textit{f} means different levels on flute and trombone", WHITE),
            (r"orchestrators mark the loud instruments down and the soft ones up, \ to balance", WHITE),
            (r"manuals give rules of thumb for how many of one instrument balance another", TUNE),
            (r"chapter 4: \ what happens when many players share one part", GREY_A),
        ]
        rows_scene(self, r"balance", items,
                   "That makes balance an orchestrator's problem. <bookmark mark='b'/> Instruments differ in power: a trumpet at "
                   "forte can cover a whole woodwind section. <bookmark mark='c'/> Dynamic markings are relative, so the same "
                   "forte means different levels on a flute and on a trombone. <bookmark mark='d'/> Orchestrators mark the loud "
                   "instruments down and the soft ones up, <bookmark mark='e'/> and manuals since Rimsky-Korsakov's give rules of "
                   "thumb for how many of one instrument balance another. <bookmark mark='f'/> Chapter four asks what happens when "
                   "many players share one part.", marks="cdef")

    # ------------------------------------------------------------------
    def swell(self):
        d = load("swell")
        c = clip("swell.one")
        cen = d["centroids"]
        x0, W = -5.0, 10.0
        mx = max(cen)
        pts = [[x0 + W * k / (len(cen) - 1), -1.5 + 2.8 * v / mx, 0] for k, v in enumerate(cen)]
        line = VMobject(color=EAR, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.07, color=EAR) for p in pts])
        ax = Line([x0, -1.5, 0], [x0 + W, -1.5, 0], color=GREY_D)
        labs = VGroup(label(rf"{cen[0]:.0f} Hz", font_size=16, color=WHITE).next_to(dots[0], UP, buff=0.1), label(rf"{cen[-1]:.0f} Hz", font_size=16, color=WHITE).next_to(dots[-1], UP, buff=0.1),
                      label(r"brightness through the swell \ (spectral centroid, \ every 0.4 s)", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.9))
        head = label(r"one note, \ the breath rising", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear a swell on one note: the trumpet model's breath rising from soft to hard, made from three simulations at "
            f"rising pressures, crossfaded. The brightness climbs from about {say(round(cen[0], -1))} to "
            f"{say(round(cen[-1], -1))} hertz as the note grows louder: the colour changes with the dynamic."
        ):
            self.play(FadeIn(head), FadeIn(ax), Create(line), FadeIn(dots), FadeIn(labs))
        with self.listen(c) as snd:
            window(snd, r"a swell", detail=r"Part 8's lip-reed trumpet", corner=DL, tag_corner=DR)
            for k, dd in enumerate(dots):
                pulse(snd, dd, k * c.duration / 8, (k + 1) * c.duration / 8, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ranges_db(self):
        items = [
            (r"a single flute or violin spans perhaps 30 to 40 dB from its softest to its loudest", WHITE),
            (r"brass reach much higher levels: \ a trombone section at full power can exceed 110 dB nearby", WHITE),
            (r"orchestral dynamic range depends on score, room and measurement", WHITE),
            (r"so the orchestrator controls loudness by number and choice of instruments, \ not only by markings", TUNE),
            (r"Part 57 measures loudness; \ Part 55 the hall that carries it", GREY_A),
        ]
        rows_scene(self, r"dynamic range across the orchestra", items,
                   "How wide is the orchestra's dynamic range? <bookmark mark='b'/> A single flute or violin spans perhaps thirty or forty decibels from its softest to its loudest. <bookmark mark='c'/> Brass reach much higher levels: a trombone section at full power can exceed a hundred and ten decibels nearby. <bookmark mark='d'/> A full orchestra can span a very wide dynamic range, depending on the work, room and measurement position, <bookmark mark='e'/> so the orchestrator controls loudness by the number and choice of instruments, not only by the markings. <bookmark mark='f'/> Part 57 measures loudness, and Part 55 the hall that carries it.", marks="cdef")
