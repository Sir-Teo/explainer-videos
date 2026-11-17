from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403
from videos.music.variations import rows_before

CELL = {"sung": (r"sung", r"a little out of tune", GREY_A), "tuned": (r"hard-tuned", r"snapped to the scale", TUNE),
        "vocoded": (r"vocoded", r"onto a sawtooth chord", BLUE), "stretched": (r"stretched", r"one second made eight", EAR)}


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune50")
        c = clip("tune.variation50")
        head = VGroup(label(r"Variation 50", font_size=48, color=TUNE), label(r"the Tune, \ sung and reshaped", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for k in d["names"]:
            a, b, col = CELL[k]
            cells.add(VGroup(RoundedRectangle(width=2.9, height=1.6, corner_radius=0.15, stroke_color=GREY_B), VGroup(label(a, font_size=24, color=col), label(b, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its first phrase sung "
            "a little out of tune; hard-tuned; vocoded onto a chord; and its first second stretched eightfold by the phase "
            "vocoder."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        st = d["starts"]
        names = d["names"]
        with self.listen(c) as snd:
            window(snd, r"Variation 50", kind="synthesized", detail=r"Part 8's voice, \ reshaped", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune50")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty of the ledger. As sung, the median pitch error is {say(d['before'])} cents; after correction, "
            f"{say(d['after'], 1)}. And one second became {say(d['stretched_s'], 1)}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a nonlinear shaper makes harmonics; \ its symmetry decides which",
            r"Chebyshev sums select harmonics for a unit cosine, \ within bandwidth limits",
            r"intermodulation clarity depends on tuning, register and shaper",
            r"digital distortion aliases; \ oversampling cures it best",
            r"compressors, \ limiters, \ gates and sidechains are gains that follow levels",
            r"PSOLA and the phase vocoder untie pitch from time; \ correction snaps pitch to a scale",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A nonlinear shaper makes harmonics, and its symmetry decides which. <bookmark mark='a'/> Chebyshev sums produce selected harmonics for a unit-amplitude cosine, subject to digital bandwidth limits. <bookmark mark='b'/> Two tones make intermodulation whose perceived clarity depends on tuning, register and the shaper. <bookmark mark='c'/> Digital distortion aliases, and oversampling cures it best. <bookmark mark='d'/> Compressors, limiters, gates and sidechains are gains that follow levels. <bookmark mark='e'/> And PSOLA and the phase vocoder untie pitch from time, while correction snaps pitch to a scale."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A compressor has threshold $-20$ dB, \ ratio 4 and no knee. \ What comes out for $-8$ dB in?",
            r"Prove that an odd shaper, \ $f(-x) = -f(x)$, \ fed a pure tone, \ makes only odd harmonics.",
            r"\textbf{Ear.} \ The lab plays the Tune hard-tuned or natural, \ in random order; \ say which is which.",
            r"\textbf{Build.} \ Add a look-ahead to the compressor, \ so that no sample exceeds the threshold.",
            r"$\bigstar$ \ How small can a neural amplifier model be, \ indistinguishable at every setting and alias-free?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"synthesis: \ waveshaping and alias-free oscillators", [51]),
            (r"physical models: \ nonlinear strings and reeds", [52]),
            (r"recording and mixing: \ compressors at work", [56]),
            (r"mastering and loudness: \ limiters and the loudness war", [57]),
            (r"pitch and transcription: \ finding pitch in recordings", [61]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In synthesis, with waveshaping and oscillators that do not alias. In physical models of "
            "nonlinear strings and reeds. In recording and mixing, where compressors go to work. In mastering, with limiters "
            "and the loudness war. And in pitch and transcription, finding pitch in recordings."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"guitarists", r"choose fifths under heavy distortion, \ full chords when clean"),
            (r"mix engineers", r"compress for density, \ and set the attack for punch"),
            (r"producers", r"key a compressor from the kick, \ so the bass makes room"),
            (r"vocal editors", r"correct pitch gently, \ unless the snap is the point"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Guitarists choose fifths under heavy distortion and full chords when clean. Mix engineers compress "
            "for density and set the attack for punch. Producers key a compressor from the kick, so the bass makes room. And "
            "vocal editors correct pitch gently, unless the snap is the point."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"U. Z\"olzer \ (ed.), \ \textit{DAFX: \ Digital Audio Effects} \ (2nd ed., \ 2011)",
             r"J. O. Smith, \ \textit{Spectral Audio Signal Processing} \ (2011)",
             r"V. V\"alim\"aki and others, \ `Virtual analog effects' \ (in \textit{DAFX})",
             r"D. Arfib, \ `Digital synthesis of complex spectra by means of multiplication of nonlinear distorted sine waves' \ (1979)"],
            [r"D. Giannoulis, \ M. Massberg and J. D. Reiss, \ `Digital dynamic range compressor design' \ (2012)",
             r"J. Laroche and M. Dolson, \ `Improved phase vocoder time-scale modification of audio' \ (1999)",
             r"E. Moulines and F. Charpentier, \ `Pitch-synchronous waveform processing ...' \ (1990)",
             r"A. de Cheveign\'e and H. Kawahara, \ `YIN, \ a fundamental frequency estimator ...' \ (2002)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 50, "New York, 1906: two hundred tons",
            "What if the machine makes the sound in the first place?",
            "Every effect so far has changed a sound that already existed. <bookmark mark='a'/> In 1906 an instrument "
            "of dynamos, nearly two hundred tons of them, sent tones down telephone lines to subscribers. Sixty years "
            "later a module the size of a book did the same job. What if the machine makes the sound in the first "
            "place? <bookmark mark='b'/> Next time. Part 51: Synthesis One, Oscillators and Filters.",
            signoff=clip("bridge.signoff"))
