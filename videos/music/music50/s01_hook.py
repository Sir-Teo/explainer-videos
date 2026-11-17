from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.accidents()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune's first phrase, \ sung twice by the same voice. \ One version was passed through a pitch corrector "
                           r"set to act instantly. \ Which one?", width=10.0)
        with self.voiceover(
            "In 1951 a guitar amplifier damaged on the way to a Memphis session gave a record its torn tone. That story comes later; listen first. The Tune's first phrase, sung twice by the same computed voice. One version was passed "
            "through a pitch corrector set to act instantly. Which one?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 0.6)
        mic = VGroup(RoundedRectangle(width=0.5, height=0.9, corner_radius=0.25, stroke_color=GREY_A), Line(DOWN * 0.45, DOWN * 0.9, color=GREY_A)).to_edge(DOWN, buff=1.2)
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(mic))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one voice, \ twice", kind="synthesized", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        t, f0, tg = np.array(d["t"]), np.array(d["f0"]), np.array(d["target"])
        t2, f2 = np.array(d["t2"]), np.array(d["f2"])
        ax = frame_axes(width=11.0, height=3.4, xlo=0, xhi=max(t[-1], t2[-1]), ylo=-1, yhi=11, center=DOWN * 0.3)
        def semis(f):
            return 12 * np.log2(np.maximum(f, 1) / 261.6256)
        def dots(tt, ff, col, r=0.035):
            return VGroup(*[Dot(ax.to(a, semis(b)), radius=r, color=col) for a, b in zip(tt, ff) if b > 0])
        tend = max(t[-1], t2[-1])
        grid = VGroup(*[DashedLine(ax.to(0, s), ax.to(tend, s), color=GREY_B, stroke_width=0.8, stroke_opacity=0.5) for s in (0, 2, 4, 5, 7, 9)])
        names = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(ax.to(0, s), LEFT, buff=0.15) for n, s in (("C", 0), ("D", 2), ("E", 4), ("F", 5), ("G", 7), ("A", 9))])
        a = dots(t, f0, EAR)
        b = dots(t2, f2, TUNE)
        key = VGroup(label(rf"first: \ as sung, \ a median {d['before_cents']:.0f} cents off", font_size=17, color=EAR),
                     label(rf"second: \ corrected, \ {d['after_cents']:.1f} cents off", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        head = label(r"the second was corrected", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second. Here are the two pitch tracks, measured frame by frame, against the notes of the scale. "
            f"<bookmark mark='a'/> As sung, every note sits a little off, by a median of {say(d['before_cents'])} cents. "
            f"<bookmark mark='b'/> Corrected, each note snaps onto the line, to within {say(d['after_cents'], 1)} cents, "
            "and jumps between notes without gliding. That instant snap is the sound of a genre."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(grid), FadeIn(names), FadeIn(ghost(VGroup(a, b), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(key[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def accidents(self):
        items = [
            (r"1951: \ `Rocket 88' was recorded at Memphis Recording Service through a guitar amplifier damaged on the way", WHITE),
            (r"its fuzzy, \ torn tone was kept, \ and distortion became the sound of rock", WHITE),
            (r"1997: \ Andy Hildebrand, \ who had found oil by autocorrelation, \ released Auto-Tune", WHITE),
            (r"1998: \ Cher's `Believe' set its speed to instant: \ the voice snapped between notes, \ and a style was born", TUNE),
            (r"both are nonlinear or time-varying: \ effects that the last part's linear rules cannot describe", GREY_A),
        ]
        rows_scene(self, r"two accidents, \ two genres", items,
                   "Two celebrated production stories illustrate how artifacts became musical resources. <bookmark mark='b'/> In 1951 Rocket 88 was recorded at Sam Phillips's Memphis Recording Service, before the Sun label was founded "
                   "through a guitar amplifier damaged on the way to the session. <bookmark mark='c'/> Its fuzzy, torn tone was "
                   "kept, and distortion became the sound of rock. <bookmark mark='d'/> In 1997 Andy Hildebrand, a geophysicist who "
                   "had used autocorrelation to find oil, released Auto-Tune, to fix singers' pitch discreetly. "
                   "<bookmark mark='e'/> In 1998 Cher's Believe set its speed to instant: the voice snapped between notes, and a "
                   "style was born. <bookmark mark='f'/> Both are nonlinear or time-varying: effects the last part's linear rules "
                   "cannot describe.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"nonlinearity, \ harmonics, \ and Chebyshev's exact shaper",
            r"intermodulation, \ the power chord, \ and aliasing",
            r"compressors, \ limiters, \ gates and sidechains",
            r"time and pitch: \ resampling, \ overlap-add, \ the phase vocoder",
            r"pitch detection, \ PSOLA and pitch correction",
            r"vocoders and ring modulation",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Nonlinearity, harmonics, and Chebyshev's exact shaper. <bookmark mark='b'/> Intermodulation, "
            "the power chord, and aliasing. <bookmark mark='c'/> Compressors, limiters, gates and sidechains. "
            "<bookmark mark='d'/> Time and pitch: resampling, overlap-add and the phase vocoder. <bookmark mark='e'/> Pitch "
            "detection, PSOLA and pitch correction. <bookmark mark='f'/> And vocoders and ring modulation."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
