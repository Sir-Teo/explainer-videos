from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Touch(SoundScene):
    def construct(self):
        chapter(self, 4, r"Loudness and articulation", r"How does a pianist connect two notes?")
        self.dynamics()
        self.hear()
        self.overlap()
        self.touch()

    # ------------------------------------------------------------------
    def dynamics(self):
        d = load("tune")
        vel = d["vel"]
        ph = d["phrases"]
        bars = value_bars(vel, width=11.4, height=1.6, base=0.2, scale=1.6, color=EAR)
        bars.move_to(DOWN * 0.3)
        seps = VGroup()
        n = len(vel)
        for i in range(1, n):
            if ph[i] != ph[i - 1]:
                x = bars[0].get_left()[0] + 11.4 * i / n
                seps.add(DashedLine([x, bars[0].get_y() - 0.2, 0], [x, bars[0].get_y() + 1.9, 0], color=GREY_D, stroke_width=1))
        cap = label(r"each note's velocity in the performed Tune; \ dashed lines: \ phrase boundaries", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"loudness across the whole Tune", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Loudness first. Here is every note's velocity in the performed Tune, all six phrases. <bookmark mark='a'/> Each "
            "phrase swells towards its middle and falls away at its ends, the phrase arch; within that, the higher notes "
            "stand out. Measured performances show the same coupling: where pianists slow down they usually also play "
            "softer, so loudness and tempo rise and fall together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[1:]], lag_ratio=0.03), FadeIn(seps))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("artic")
        c = clip("artic.three")
        vs = d["versions"]
        tot = max(p["t"] + p["dur"] for v in vs.values() for p in v)
        cols = {"legato": TUNE, "as written": GREY_B, "staccato": BLUE}
        rolls = VGroup(*[VGroup(label(k, font_size=19, color=cols[k]),
                                perf_roll(v, width=9.2, height=0.9, lo=58, hi=72, total=tot, color=cols[k])).arrange(RIGHT, buff=0.4)
                         for k, v in vs.items()]).arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(UP * 0.2)
        r = d["ratios"]
        cap = label(rf"held: \ legato {r['legato']:.2f}, \ as written {r['as written']:.2f}, \ staccato {r['staccato']:.2f} \ of each note's slot", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three articulations, \ same notes, \ same timing", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Articulation is how long each note is held against the time before the next one. Hear the first phrase three "
            "ways: legato, each note held a little past the start of the next; as written, with a small gap; and "
            "staccato, each note released early. The onsets are identical; only the releases move."
        ):
            self.play(FadeIn(head), FadeIn(rolls), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"legato, \ written, \ staccato", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, k in enumerate(vs):
                flash(snd, rolls[i][1].notes, [st[k] + p["t"] for p in vs[k]], hot=WHITE, base=cols[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overlap(self):
        items = [
            (r"on a piano, \ legato is an overlap: \ the next key goes down before the last comes up", WHITE),
            (r"Repp \ (1997) \ measured it: \ pianists overlap legato notes by tens of milliseconds", WHITE),
            (r"the overlap shrinks when notes are fast, \ and grows when they are slow", WHITE),
            (r"staccato, \ portato, \ tenuto: \ points on the same scale of held time", TUNE),
            (r"the pedal adds another layer: \ strings keep sounding after the key is released \ (Part 7)", GREY_A),
        ]
        rows_scene(self, r"legato, \ measured", items,
                   "On a piano, legato is literally an overlap: the next key goes down before the last one comes up. "
                   "<bookmark mark='b'/> Bruno Repp measured it in 1997: pianists overlap legato notes by tens of milliseconds, "
                   "<bookmark mark='c'/> and the overlap grows with the time between notes. <bookmark mark='d'/> Staccato, "
                   "portato and tenuto are points on the same scale of held time. <bookmark mark='e'/> And the sustain pedal adds "
                   "another layer, keeping the strings sounding after the keys are released, as Part 7 showed.", marks="bcde")

    # ------------------------------------------------------------------
    def touch(self):
        items = [
            (r"`touch': \ the old debate over whether pianists can change tone colour, \ not only loudness", WHITE),
            (r"for a single note, \ hammer velocity fixes the sound \ (Part 7): \ a robot matching the velocity matches the tone", WHITE),
            (r"but touch also means timing between voices, \ balance within a chord, \ pedal, \ and key noise", WHITE),
            (r"so `colour' on a piano is mostly how many notes are balanced and timed, \ not one note's tone", TUNE),
            (r"chapter 5: \ instruments whose players shape every note's pitch", GREY_A),
        ]
        rows_scene(self, r"touch", items,
                   "What about touch? <bookmark mark='b'/> Pianists have long argued about whether they can change a note's tone "
                   "colour, and not only its loudness. <bookmark mark='c'/> For a single note, hammer velocity fixes the sound, "
                   "as Part 7 showed: a robot that matches the velocity matches the tone, apart from key noise. "
                   "<bookmark mark='d'/> But touch also means the timing between voices, the balance within a chord, the pedal. "
                   "<bookmark mark='e'/> So colour on a piano is mostly how many notes are balanced and timed, not one note's "
                   "tone. <bookmark mark='f'/> Chapter five turns to instruments whose players shape every note's pitch.",
                   marks="bcdef")
