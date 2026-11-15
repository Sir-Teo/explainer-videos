from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Tempo(SoundScene):
    def construct(self):
        chapter(self, 2, r"Tempo, \ and its octave", r"Why do machines tap at double speed?")
        self.prior()
        self.slow()
        self.wild()
        self.listeners()

    # ------------------------------------------------------------------
    def prior(self):
        d = load("tempo")
        bpm = np.array(d["ac_bpm"])
        ac, wt = np.array(d["ac"]), np.array(d["weighted"])
        sel = (bpm >= 30) & (bpm <= 300)
        ax = frame_axes(width=9.0, height=3.0, xlo=np.log2(30), xhi=np.log2(300), ylo=0, yhi=1.05, center=DOWN * 0.4 + LEFT * 0.6)
        c1 = curve(np.log2(bpm[sel]), ac[sel], ax.to, color=GREY_B, width=2)
        c2 = curve(np.log2(bpm[sel]), wt[sel], ax.to, color=TUNE, width=3)
        prior = curve(np.log2(bpm[sel]), np.exp(-0.5 * np.log2(bpm[sel] / 120) ** 2), ax.to, color=BLUE, width=2)
        xt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(np.log2(v), 0), DOWN, buff=0.1) for v in (30, 60, 120, 240)])
        xl = label(r"beats a minute \ (log scale)", font_size=14, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        key = VGroup(label(r"autocorrelation of the novelty", font_size=15, color=GREY_B), label(r"a prior: \ listeners lean toward 120", font_size=15, color=BLUE),
                     label(r"their product", font_size=15, color=TUNE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        found = label(rf"found: \ {d['bpm']:.0f} beats a minute", font_size=20, color=TUNE).to_edge(DOWN, buff=0.35)
        head = label(r"choosing one tempo", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "To choose one tempo, add up the autocorrelation over the whole passage. <bookmark mark='a'/> It has peaks at the "
            "beat and at its multiples and fractions: rhythm is a hierarchy. <bookmark mark='b'/> Something must choose a level. "
            "Listeners asked to tap along prefer tempos near a hundred and twenty a minute, so trackers multiply by a prior "
            "centred there. <bookmark mark='c'/> On the session, the product peaks at a hundred, the tempo it was played at."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(prior), FadeIn(key[1]), run_time=1.0)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(key[2]), FadeIn(found), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slow(self):
        d = load("tempo")
        hd = load("halfdouble")
        c = clip("halfdouble.two")
        boxes = choice_boxes([rf"clicks at {hd['written_bpm']:.0f}: \ as written", rf"clicks at {hd['found_bpm']:.0f}: \ as found"], width=4.2, height=0.9, buff=0.8, size=19).move_to(UP * 0.5)
        note = VGroup(label(rf"with the prior: \ {d['slow_found']:.0f}; \ with no prior: \ {d['slow_flat']:.0f}", font_size=19, color=WHITE),
                      label(r"both are defensible: \ a slow chord every beat, \ or a lively eighth-note pulse", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25).next_to(boxes, DOWN, buff=0.5)
        head = label(r"a slow piece", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Now a slow piece, written at fifty beats a minute, a chord every beat with eighth notes above. Hear it with clicks at the written tempo, then at the tempo the tracker found."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = hd["starts"]
        with self.listen(c) as snd:
            window(snd, r"50, \ then as found", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["written"], st["found"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["found"], c.duration, buff=0.08)
        with self.voiceover(
            f"The tracker, leaning toward a hundred and twenty, chose {say(d['slow_found'])}: double time. With no prior it finds "
            f"{say(d['slow_flat'])}. Neither is simply wrong: many listeners would tap the eighth notes too. This is the "
            "tempo octave problem, and it is why trackers are scored at more than one metrical level."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wild(self):
        items = [
            (r"a live band drifts: \\ a few beats a minute faster by the end of a song is common", WHITE),
            (r"classical performers shape tempo deliberately: \\ Part 43's phrase arches, \\ held cadences", WHITE),
            (r"a click track removes drift; \\ much recorded pop since the 1980s is built on one", WHITE),
            (r"so a single tempo describes a recording only roughly; \\ a tempo curve describes a performance", TUNE),
        ]
        rows_scene(self, r"tempo in real performances", items,
                   "And real tempos move. <bookmark mark='b'/> A live band drifts; a few beats a minute faster by the end of a song is "
                   "common. <bookmark mark='c'/> Classical performers shape tempo on purpose, with the phrase arches and held "
                   "cadences of Part 43. <bookmark mark='d'/> A click track removes drift, and much recorded pop since the 1980s is "
                   "built on one. <bookmark mark='e'/> So a single tempo describes a recording only roughly; a tempo curve describes "
                   "a performance.", marks="bcde")

    # ------------------------------------------------------------------
    def listeners(self):
        items = [
            (r"people disagree too: \ asked to tap, \ listeners split between levels, \ above all at slow and fast tempos", WHITE),
            (r"a tempo is not one number for long: \ performers speed up, \ slow down, \ and hold", WHITE),
            (r"so evaluations ask: \ did the system find a beat at some sensible level? \ and the right one?", WHITE),
            (r"the prior is a fact about listeners, \ not about the music", TUNE),
        ]
        rows_scene(self, r"which level?", items,
                   "This is not only a machine's problem. <bookmark mark='b'/> Asked to tap along, listeners split between levels, "
                   "above all at slow and fast tempos. <bookmark mark='c'/> And a tempo is not one number for long: performers "
                   "speed up, slow down and hold. <bookmark mark='d'/> So evaluations ask two questions: did the system find a beat "
                   "at some sensible level, and did it find the one most listeners tap? <bookmark mark='e'/> The prior near a "
                   "hundred and twenty is a fact about listeners, not about the music.", marks="bcde")
