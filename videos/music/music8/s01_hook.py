from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.two_pipes()
        self.two_notes()
        self.plan()

    # ------------------------------------------------------------------
    def two_pipes(self):
        d = load("hook")
        c = clip("hook.pair")
        a = TubeView(width=7.2, bore=0.55, left="open", right="open", color=FLUTE).move_to(UP * 1.5)
        b = TubeView(width=7.2, bore=0.55, left="closed", right="open", color=CLAR).move_to(DOWN * 0.6)
        la = label(r"blown across the end", font_size=28, color=FLUTE).next_to(a, UP, buff=0.2)
        lb = label(r"blown through a reed", font_size=28, color=CLAR).next_to(b, UP, buff=0.2)
        rule = VGroup(DoubleArrow(a.p(0.0) + DOWN * 0.75, a.p(1.0) + DOWN * 0.75, buff=0, color=GREY_B, stroke_width=2, tip_length=0.15),
                      label(rf"{100 * d['length']:.0f} cm, \ both of them", font_size=24, color=GREY_B).move_to(a.p(0.5) + DOWN * 1.02))
        q = listen_card(r"Two pipes of the same length. \ One is blown across its open end, \ the other through a reed. \\ How far apart are their notes?", width=9.6, font_size=26).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two pipes. They are the same length, sixty centimetres, and nearly the same width. One will be "
            "blown across its open end, the way you blow across a bottle. The other has a reed fixed to one "
            "end, and will be blown through that. Listen to both, and judge how far apart their notes are."
        ):
            self.play(FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb), FadeIn(rule), FadeIn(q, shift=UP * 0.2))
        with self.listen(c) as snd:
            window(snd, r"two pipes, \ 60 cm long", detail=r"a model flute, \ then a model clarinet", corner=UL, tag_corner=UR)
            pulse(snd, la, snd.time_of("flute"), snd.time_of("flute") + 2.2, buff=0.12)
            pulse(snd, lb, snd.time_of("clarinet"), snd.time_of("clarinet") + 2.2, buff=0.12)
        ans = VGroup(label(rf"{d['flute_hz']:.0f} Hz", font_size=34, color=FLUTE).next_to(a, RIGHT, buff=0.3),
                     label(rf"{d['clarinet_hz']:.0f} Hz", font_size=34, color=CLAR).next_to(b, RIGHT, buff=0.3))
        note = VGroup(label(r"the same length of air, \ an octave apart", font_size=32, color=TUNE),
                      label(r"and the lower one sounds hollow: \ every other harmonic is nearly missing", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"An octave. The first pipe sounds at {say(d['flute_hz'])} hertz; the second at {say(d['clarinet_hz'])}, "
            "half as fast, from the same length of air. And they differ in colour too. The lower one has "
            "that hollow, woody sound, and if you measure it, every second harmonic is almost missing. The "
            "first pipe is a flute, more or less. The second is a clarinet. Why should a reed lower a pipe by "
            "an octave and hollow out its tone?"
        ):
            self.play(FadeOut(q), FadeIn(ans), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_notes(self):
        d = load("hook")
        c = clip("hook.overtone")
        drone = d["drone"]
        n = 14
        base = DOWN * 2.2 + LEFT * 5.4
        dx = 0.8
        bars = VGroup(*[Rectangle(width=0.42, height=0.5, stroke_width=0, fill_color=GREY_C, fill_opacity=0.7).move_to(base + RIGHT * dx * k, aligned_edge=DOWN) for k in range(n)])
        nums = VGroup(*[label(str(k + 1), font_size=20, color=GREY_B).next_to(bars[k], DOWN, buff=0.1) for k in range(n)])
        cap = label(rf"the harmonics of one sung note, \ {drone:.0f} Hz", font_size=24, color=GREY_B).next_to(nums, DOWN, buff=0.2)
        heights = [max(2.2 * (1 - 0.35 * np.log2(k + 1) / 2), 0.25) for k in range(n)]
        for k, b in enumerate(bars):
            b.stretch_to_fit_height(heights[k]).move_to(base + RIGHT * dx * k, aligned_edge=DOWN)
        head = VGroup(label(r"Tuva, \ southern Siberia", font_size=34, color=HIST), label(r"one singer, \ two notes at once", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A second puzzle, from the other end of the world of wind instruments. In Tuva, in southern "
            "Siberia, herders sing in a way that outsiders at first refuse to believe. One singer holds a "
            "low, steady note, and above it, at the same time, whistles a tune. One throat, two notes. "
            "<bookmark mark='a'/> Here are the harmonics of a single sung note, the way Part 3 would draw "
            "them. Listen to what a throat can do with them. This is not a recording of a Tuvan singer. It "
            "is Monochord, the instrument this series builds, singing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(nums), FadeIn(cap))
        mark = Triangle(color=EAR, fill_opacity=1, stroke_width=0).scale(0.14).rotate(np.pi).set_opacity(0)
        self.add(mark)
        starts = [c.events[f"n{k}"] for k in range(len(d["harmonics"]))]
        hs = d["harmonics"]

        def lit(m, t):
            k = int(np.clip(np.searchsorted(starts, t, side="right") - 1, 0, len(hs) - 1))
            for j, b in enumerate(m):
                on = j == hs[k] - 1 and t < c.duration - 0.05
                b.set_fill(EAR if on else GREY_C, opacity=1.0 if on else 0.7)
            return m

        with self.listen(c) as snd:
            window(snd, r"one voice: \ a drone and its overtones", kind="synthesized", detail=r"a model of a voice", corner=UL, tag_corner=UR)
            snd.drive(bars, lit)
        for b in bars:
            b.set_fill(GREY_C, opacity=0.7)
        with self.voiceover(
            "The low note never moved. The whistle above it was not a second voice. It was one harmonic of "
            "that low note at a time, the eighth, the ninth, the tenth, the twelfth, made so loud that the ear "
            "hears it as a note of its own. How a throat picks out one harmonic is the last thing this part "
            "will explain, and it turns out to be the same idea as the flute and the clarinet."
        ):
            self.play(Indicate(VGroup(*[bars[k] for k in (7, 8, 9, 11)]), color=EAR, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"a column of air that resonates", font_size=32, color=AIR), label(r"$+$", font_size=36),
                      label(r"a valve that lets breath through in time with it", font_size=32, color=REED)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"why the same pipe has two notes, \ and what a reed does",
            r"holes, \ registers, \ and why a clarinet's fingering is the odd one out",
            r"cones: \ the oboe, \ the bassoon, \ the saxophone",
            r"brass: \ lips for a valve, \ and a bell that retunes the tube",
            r"the flute, \ which has no valve at all, \ and the organ",
            r"the voice: \ vowels, \ singers, \ and two notes from one throat",
        ], title=r"Part 8: \ Pipes, Reeds and Voices", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "Here is that idea. Every wind instrument, and every voice, is two things joined in a loop. A "
            "column of air, which has resonances. And a valve, which lets the player's breath through in "
            "puffs, in time with the column. Part 7 ended on the bow, which grips and lets go in time with a "
            "string. This part is that loop again, with air. <bookmark mark='a'/> We will find out why one "
            "pipe has two notes, and what a reed is doing. <bookmark mark='b'/> How holes turn one pipe into "
            "a scale. <bookmark mark='c'/> What changes when the pipe is a cone. <bookmark mark='d'/> How a "
            "brass player gets a tune from a tube with no holes. <bookmark mark='e'/> How a flute works with "
            "no valve at all. <bookmark mark='f'/> And then the oldest instrument, the one you are listening "
            "to me with: the voice."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
