from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Tuning(SoundScene):
    def construct(self):
        chapter(self, 9, r"Pitch correction", r"How does a machine know what note you meant?")
        self.detect()
        self.yin_()
        self.speeds()
        self.hear_speeds()
        self.story()
        self.editing()

    # ------------------------------------------------------------------
    def detect(self):
        items = [
            (r"first, \ find the pitch: \ a voice's waveform repeats once a period", WHITE),
            (r"autocorrelation compares the signal with itself shifted: \ it matches best at a shift of one period", WHITE),
            (r"Hildebrand had used the same tool to find echoes from oil-bearing rock", WHITE),
            (r"the trap: \ it also matches at two periods, \ three, \ ... \ so octave errors lurk", TUNE),
            (r"YIN \ (de Cheveign\'e and Kawahara, \ 2002) \ is built to avoid them", GREY_A),
        ]
        rows_scene(self, r"finding the pitch", items,
                   "A pitch corrector must first find the pitch. <bookmark mark='b'/> A voice's waveform repeats once a period. "
                   "<bookmark mark='c'/> Autocorrelation compares the signal with a shifted copy of itself, and it matches best "
                   "when the shift is one period. <bookmark mark='d'/> Hildebrand had used the same tool to find echoes from "
                   "oil-bearing rock. <bookmark mark='e'/> The trap is that it also matches at two periods, and three, so octave "
                   "errors lurk. <bookmark mark='f'/> YIN, by Alain de Cheveigné and Hideki Kawahara in 2002, is built to avoid "
                   "them.", marks="bcdef")

    # ------------------------------------------------------------------
    def yin_(self):
        rows_ = text_rows([
            (r"the difference function: \ $d(\tau) = \sum_j (x_j - x_{j+\tau})^2$, \ zero at a perfect period", WHITE),
            (r"normalise it by its running mean, \ so small shifts do not win by default", WHITE),
            (r"take the first dip below a threshold, \ not the deepest: \ a period estimate, \ reducing octave errors", TUNE),
            (r"refine between samples by fitting a parabola", WHITE),
            (r"frame by frame, \ every 5 ms, \ it tracks the voice's pitch as it moves", GREY_A),
        ], font_size=23)
        head = label(r"YIN, \ step by step", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "YIN goes in four steps. <bookmark mark='a'/> Compute the difference between the signal and its shifted self, "
            "squared and summed: zero at a perfect period. <bookmark mark='b'/> Normalise it by its running mean, so that tiny "
            "shifts do not win by default. <bookmark mark='c'/> Take the first dip below a threshold, not the deepest: this reduces octave errors but does not guarantee the correct period. <bookmark mark='d'/> Refine the answer between samples by fitting a parabola. "
            "<bookmark mark='e'/> Done frame by frame, every few milliseconds, it tracks the voice's pitch as it moves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speeds(self):
        d = load("correct")
        t = np.array(d["t"])
        ax = frame_axes(width=11.0, height=3.6, xlo=0, xhi=t[-1], ylo=-1, yhi=11, center=DOWN * 0.4)
        def semis(f):
            return 12 * np.log2(np.maximum(np.asarray(f, float), 1) / 261.6256)
        f0 = np.array(d["f0"])
        sung = VGroup(*[Dot(ax.to(a, semis(b)), radius=0.03, color=GREY_A) for a, b in zip(t, f0) if b > 0])
        def track(key, col):
            v = np.array(d[key])
            segs = VGroup()
            run = []
            for a, b in zip(t, v):
                if b > 0:
                    run.append((a, semis(b)))
                elif run:
                    if len(run) > 1:
                        segs.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners([ax.to(x, y) for x, y in run]))
                    run = []
            if len(run) > 1:
                segs.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners([ax.to(x, y) for x, y in run]))
            return segs
        tracks = VGroup(track("250", BLUE), track("60", EAR), track("0", TUNE))
        key = VGroup(label(r"grey: \ the pitch as sung", font_size=16, color=GREY_A), label(r"blue: \ corrected slowly \ (250 ms)", font_size=16, color=BLUE),
                     label(r"pink: \ faster \ (60 ms)", font_size=16, color=EAR), label(r"gold: \ instantly", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        names = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(ax.to(0, s), LEFT, buff=0.12) for n, s in (("C", 0), ("E", 4), ("G", 7), ("A", 9))])
        head = label(r"the target, \ at three speeds", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Then choose the nearest scale note as this program's target; that heuristic cannot determine a singer's intended note in every context. <bookmark mark='a'/> Here is the out-of-tune voice's "
            "pitch, as YIN measured it. <bookmark mark='b'/> A slow corrector glides towards the target over a quarter of a "
            "second: the singer's own scoops and vibrato survive, and the result sounds natural. <bookmark mark='c'/> A faster "
            "one arrives in sixty milliseconds. <bookmark mark='d'/> At speed zero, the target jumps straight to the scale note "
            "and every glide between notes vanishes: the pitch moves in steps. That is the setting Believe used. PSOLA then "
            "moves the voice to whichever target was chosen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(sung), FadeIn(key[0]))
            for mark, tr, k in zip("bcd", tracks, key[1:]):
                vo.wait_until(mark)
                self.play(Create(tr), FadeIn(k))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"Auto-Tune was sold to fix flat notes invisibly, \ and became routine in pop production", WHITE),
            (r"Cher's `Believe' \ (1998) \ made the artefact the point", WHITE),
            (r"T-Pain built a style on it; \ in hip-hop and Afrobeats it became an instrument", WHITE),
            (r"the same software, \ set gently, \ is inaudible; \ set hard, \ it is unmistakable", TUNE),
            (r"a tool's mistakes become an art's materials, \ as fuzz did", GREY_A),
        ]
        rows_scene(self, r"from repair to style", items,
                   "The story of pitch correction is the story of fuzz again. <bookmark mark='b'/> Auto-Tune was sold to fix flat "
                   "notes invisibly, and it became routine in pop production. <bookmark mark='c'/> Cher's Believe, in 1998, made "
                   "the artefact the point. <bookmark mark='d'/> T-Pain built a style on it, and in hip-hop and Afrobeats it became "
                   "an instrument. <bookmark mark='e'/> Gentle settings can be transparent on suitable material, while fast correction often produces an audible effect. "
                   "<bookmark mark='f'/> A tool's mistakes became an art's materials, as fuzz did.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear_speeds(self):
        d = load("speeds")
        c = clip("speeds.three")
        cells = VGroup()
        for t, col in ((r"a 250 ms glide", BLUE), (r"a 60 ms glide", EAR), (r"instant", TUNE)):
            cells.add(VGroup(RoundedRectangle(width=3.2, height=1.2, corner_radius=0.15, stroke_color=col), label(t, font_size=22, color=WHITE)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.5).move_to(UP * 0.3)
        head = label(r"three speeds, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the three speeds on the out-of-tune voice: a slow glide, a faster one, and instant."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = ["slow", "fast", "instant"]
        with self.listen(c) as snd:
            window(snd, r"three speeds", kind="synthesized", detail=r"Part 8's voice, \ PSOLA", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "The slow glide still sounds like a singer, a little more in tune. The fast one tightens it. The instant one "
            "snaps from note to note: no singer moves like that, which is exactly why it became a sound of its own."
        ):
            self.play(Indicate(cells[2], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def editing(self):
        items = [
            (r"Celemony's Melodyne \ (2001): \ every note of a recording drawn as a blob on a piano roll", WHITE),
            (r"drag a blob and the note moves, \ by the same detection and shifting, \ done offline and with care", WHITE),
            (r"its Direct Note Access \ (2009) \ separated the notes of a chord, \ so a guitar's single string could be retuned", WHITE),
            (r"the singer's vibrato and scoops can be kept, \ flattened or redrawn", TUNE),
            (r"Part 61 builds the transcription underneath: \ pitches and onsets from audio", GREY_A),
        ]
        rows_scene(self, r"editing pitch by hand", items,
                   "Correction need not be automatic. <bookmark mark='b'/> Celemony's Melodyne, from 2001, draws every note of a "
                   "recording as a blob on a piano roll. <bookmark mark='c'/> Drag a blob and the note moves, by the same detection "
                   "and shifting, done offline and with care. <bookmark mark='d'/> Its Direct Note Access, in 2009, separated the "
                   "notes of a chord, so that a single string of a guitar could be retuned. <bookmark mark='e'/> The singer's "
                   "vibrato and scoops can be kept, flattened or redrawn. <bookmark mark='f'/> Part 61 builds the transcription "
                   "underneath: pitches and onsets from audio.", marks="bcdef")
