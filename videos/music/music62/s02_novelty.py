from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Novelty(SoundScene):
    def construct(self):
        chapter(self, 1, r"Where the beats might be", r"What does a machine listen to when it looks for the beat?")
        self.what()
        self.curve()
        self.drums()
        self.others()
        self.accents()
        self.periodic()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"a beat is a percept: \ the pulse listeners tap, \ not a sound; \ it can fall in silence", WHITE),
            (r"but beats usually coincide with note starts, \ accents, \ chord changes", WHITE),
            (r"so start from Part 61's spectral flux: \ a curve that rises wherever something begins", WHITE),
            (r"subtract its local mean, \ keep what sticks up: \ the novelty curve", TUNE),
        ]
        rows_scene(self, r"what to listen for", items,
                   "A beat is not a sound. <bookmark mark='b'/> It is the pulse a listener taps, and it can fall in silence, "
                   "inside a held note or a rest. <bookmark mark='c'/> But beats usually coincide with note starts, accents and "
                   "chord changes. <bookmark mark='d'/> So machines start from Part 61's spectral flux, a curve that rises "
                   "wherever something begins. <bookmark mark='e'/> Subtract its local mean, keep what sticks up, and you have the "
                   "novelty curve.", marks="bcde")

    # ------------------------------------------------------------------
    def curve(self):
        d = load("tempo")
        t, nov = np.array(d["t"]), np.array(d["nov"])
        ax = frame_axes(width=11.0, height=2.4, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=DOWN * 0.2)
        cv = curve(t, nov, ax.to, color=TUNE, width=2)
        beats = VGroup(*[Line(ax.to(b, 0), ax.to(b, -0.2), color=GREY_B, stroke_width=3) for b in np.arange(0, t[-1], 0.6)])
        bars = VGroup(*[Line(ax.to(b, 0), ax.to(b, -0.35), color=WHITE, stroke_width=3) for b in np.arange(0, t[-1], 2.4)])
        xt = VGroup(*[label(f"{v:g} s", font_size=13, color=GREY_A).next_to(ax.to(v, -0.35), DOWN, buff=0.08) for v in range(0, int(t[-1]) + 1, 2)])
        note = label(r"grey ticks: \ the beats, \ every 0.6 s \ (100 a minute); \ white: \ every fourth", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the session's novelty curve", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the novelty curve of Part 56's session playing the Tune's first two phrases. <bookmark mark='a'/> Kick, "
            "snare, hi-hat, bass, guitar, piano and voice all start things, and the curve is a forest of peaks. "
            "<bookmark mark='b'/> But the forest has a rhythm: the tallest peaks fall on the beats, every six tenths of a "
            "second, a hundred a minute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(beats), FadeIn(bars), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"energy: \\ the simplest, \\ good for drums, \\ deaf to a change of chord at the same loudness", WHITE),
            (r"spectral flux: \\ Part 61's, \\ hears a new note even under a sustained one", WHITE),
            (r"phase deviation: \\ a steady note's phase advances predictably; \\ a new note breaks the pattern", WHITE),
            (r"band by band: \\ the low band for kick and bass, \\ the high for hi-hats; \\ each says something about the meter", WHITE),
            (r"networks now learn their own novelty from annotated beats", TUNE),
        ]
        rows_scene(self, r"other novelty curves", items,
                   "Spectral flux is one choice among several. <bookmark mark='b'/> Energy is the simplest: good for drums, deaf to a "
                   "change of chord at the same loudness. <bookmark mark='c'/> Spectral flux, Part 61's, hears a new note even under "
                   "a sustained one. <bookmark mark='d'/> Phase deviation listens to the phase: a steady note's phase advances "
                   "predictably, and a new note breaks the pattern. <bookmark mark='e'/> Band by band, the low band hears kick and "
                   "bass, the high band the hi-hats, and each says something different about the meter. <bookmark mark='f'/> And "
                   "networks now learn their own novelty from annotated beats.", marks="bcdef")

    # ------------------------------------------------------------------
    def drums(self):
        d = load("drums")
        c = clip("drums.two")
        nd, nf = np.array(d["nov_drums"]), np.array(d["nov_full"])
        t = np.arange(len(nd)) * d["hop_s"]
        a1 = frame_axes(width=11.0, height=1.3, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=UP * 0.9)
        a2 = frame_axes(width=11.0, height=1.3, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=DOWN * 1.1)
        c1 = curve(t, nd, a1.to, color=EAR, width=2)
        c2 = curve(np.arange(len(nf)) * d["hop_s"], nf, a2.to, color=TUNE, width=2)
        l1 = label(r"the drums alone", font_size=16, color=EAR).next_to(a1, UP, buff=0.08).align_to(a1, LEFT)
        l2 = label(r"the whole band", font_size=16, color=TUNE).next_to(a2, UP, buff=0.08).align_to(a2, LEFT)
        head = label(r"drums, \ and everything else", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover("Hear the drums alone, then the whole band, and compare their novelty curves."):
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(l1), FadeIn(l2))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"drums, \ then band", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            snd.show(c1, c2)
            for axis, start, stop in ((a1, st["drums"], st["full"]), (a2, st["full"], c.duration)):
                playhead = VGroup(Line(DOWN * 0.65, UP * 0.65, color=WHITE, stroke_width=3), Dot(radius=0.08, color=WHITE))
                def sweep(m, tt, ax=axis, begin=start, end=stop):
                    elapsed = np.clip(tt - begin, 0, t[-1])
                    m.move_to(ax.to(elapsed, 0.525))
                    m.set_opacity(1.0 if begin <= tt < end else 0.0)
                snd.show(playhead)
                snd.drive(playhead, sweep)
            snd.drive(c1, lambda m, tt: m.set_opacity(1.0 if tt >= st["drums"] else 0.0))
            snd.drive(c2, lambda m, tt: m.set_opacity(1.0 if tt >= st["full"] else 0.0))
        self.add(c1, c2)
        with self.voiceover(
            "The drums give a clean, regular comb; the band adds peaks for every sung note and chord, between the beats as well "
            f"as on them. Here both give the same tempo, {say(d['bpm_full'])} a minute, but in music without drums, a string "
            "quartet or a solo voice, the clean comb is gone, and that is where trackers struggle."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def accents(self):
        items = [
            (r"a dynamic accent: \ louder", WHITE),
            (r"an agogic accent: \ longer; \ a long note after short ones feels like a beat", WHITE),
            (r"a harmonic accent: \ where the chord changes", WHITE),
            (r"a melodic accent: \ the top or bottom of a contour, \ a leap", WHITE),
            (r"novelty curves see the first well, \ the others barely: \ part of why music without drums is hard", TUNE),
        ]
        rows_scene(self, r"what makes a beat strong", items,
                   "What makes a beat feel strong? Music theorists name several kinds of accent. <bookmark mark='b'/> A dynamic "
                   "accent: louder. <bookmark mark='c'/> An agogic accent: longer; a long note after short ones feels like a beat. "
                   "<bookmark mark='d'/> A harmonic accent, where the chord changes. <bookmark mark='e'/> A melodic accent, at the "
                   "top or bottom of a contour, or after a leap. <bookmark mark='f'/> Novelty curves see the first kind well and the "
                   "others barely, which is part of why music without drums is hard to track.", marks="bcdef")

    # ------------------------------------------------------------------
    def periodic(self):
        d = load("tempo")
        A = np.array(d["A"])
        bpm = np.array(d["bpm_axis"])
        pic = picture(A[::-1], 0, 1, 8.0, 3.2).move_to(DOWN * 0.3 + LEFT * 0.6)
        lo, hi = bpm.min(), bpm.max()
        y0, y1 = pic.get_bottom()[1], pic.get_top()[1]

        def ypos(b):                                 # rows run from the slowest lag (top of the array) to the fastest
            k = np.argmin(np.abs(bpm - b))
            return y1 - (y1 - y0) * (k + 0.5) / len(bpm)
        ticks = VGroup(*[label(f"{b}", font_size=13, color=GREY_A).move_to([pic.get_left()[0] - 0.35, ypos(b), 0]) for b in (50, 100, 200)])
        yl = label(r"beats a minute", font_size=14, color=GREY_A).rotate(PI / 2).next_to(ticks, LEFT, buff=0.15)
        xl = label(r"time through the passage", font_size=14, color=GREY_A).next_to(pic, DOWN, buff=0.15)
        side = VGroup(label(r"bright rows: \ periods at which the novelty repeats", font_size=17, color=WHITE),
                      label(r"100: \ the beat", font_size=17, color=TUNE), label(r"200: \ the eighth notes", font_size=17, color=WHITE),
                      label(r"50: \ every second beat", font_size=17, color=WHITE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(pic, RIGHT, buff=0.4)
        head = label(r"a tempogram", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How fast? <bookmark mark='a'/> Slide a six-second window along the novelty curve and correlate it with itself at "
            "every lag, as YIN did for pitch, but a thousand times slower. Each column is one window, each row a tempo. "
            "<bookmark mark='b'/> The brightest row is a hundred beats a minute. But the rows at two hundred, the eighth notes, "
            "and fifty, every second beat, are bright too: rhythm repeats at every level of its own hierarchy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(ticks), FadeIn(yl), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side[1:]], lag_ratio=0.4), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()
