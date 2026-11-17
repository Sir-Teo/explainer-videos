from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403
from videos.music.variations import rows_before

CELLS = {"16n": (r"16 bits", r"error, \ no dither", r"+60 dB"), "16t": (r"16 bits", r"error, \ dithered", r"+60 dB"),
         "8n": (r"8 bits", r"error, \ no dither", r"+24 dB"), "8t": (r"8 bits", r"error, \ dithered", r"+24 dB"),
         "4n": (r"4 bits", r"the Tune, \ no dither", ""), "4t": (r"4 bits", r"the Tune, \ dithered", ""),
         "1n": (r"1 bit", r"the Tune's sign alone", ""), "ds": (r"1 bit", r"delta-sigma, \ 64 times", "")}


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
        d = load("tune48")
        c = clip("tune.variation48")
        head = VGroup(label(r"Variation 48", font_size=48, color=TUNE), label(r"the Tune at 16, \ 8, \ 4 and 1 bit", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for k in d["names"]:
            a, b, g = CELLS[k]
            col = BLUE if g else (TUNE if k != "1n" else EAR)
            parts = [label(a, font_size=24, color=WHITE), label(b, font_size=16, color=col)]
            if g:
                parts.append(label(g, font_size=15, color=GREY_A))
            cells.add(VGroup(RoundedRectangle(width=2.8, height=1.5, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5),
                             VGroup(*parts).arrange(DOWN, buff=0.12)).arrange(ORIGIN))
        cells.arrange_in_grid(rows=2, cols=4, buff=(0.35, 0.4)).move_to(DOWN * 0.3)
        cap = label(r"blue: \ only the error is played, \ raised by the gain shown; \ gold: \ the Tune itself", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its first phrase "
            "at sixteen, eight, four and one bit. At sixteen and eight bits you hear only the error, raised by sixty and by "
            "twenty-four decibels, without dither and then with it; at four bits and one, the Tune itself; and last, one bit "
            "again, as a delta-sigma stream at sixty-four times the rate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        each = d["each"]
        with self.listen(c) as snd:
            window(snd, r"Variation 48", kind="synthesized", detail=r"Part 7's piano, \ converted", corner=DL, tag_corner=DR)
            for i, k in enumerate(d["names"]):
                pulse(snd, cells[i], st[k], st[k] + each, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune48")
        s = d["snr"]
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-eight of the ledger. With dither, the signal stands {say(s['16'])} decibels above the error at sixteen "
            f"bits, {say(s['8'])} at eight, and {say(s['4'])} at four. One bit, sixty-four times faster, gets back to "
            f"{say(s['ds'])}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a band-limited signal is fixed exactly by samples at more than twice its top frequency",
            r"anything above half the rate folds back down: \ filter first",
            r"converters output the smooth curve, \ not stairs",
            r"each bit buys about 6 dB; \ triangular dither makes the error plain noise",
            r"noise shaping moves noise out of the ear's way; \ with enough speed, \ one bit suffices",
            r"jitter costs most at high frequencies; \ high rates buy margins, \ little more",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A band-limited signal is fixed exactly by samples taken at more than twice its top frequency. "
            "<bookmark mark='a'/> Anything above half the rate folds back down, so filter first. <bookmark mark='b'/> "
            "Converters output the smooth curve, not stairs. <bookmark mark='c'/> Each bit buys about six decibels, and "
            "triangular dither makes the error plain noise. <bookmark mark='d'/> Noise shaping moves the noise out of the ear's "
            "way, and with enough speed one bit suffices. <bookmark mark='e'/> Jitter costs most at high frequencies, and high "
            "sample rates buy margins, and little more."
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
            r"A 30 kHz tone is sampled at 44.1 kHz with no filter. \ At what frequency is it heard?",
            r"Prove that triangular dither of two steps makes the error's mean and variance independent of the input.",
            r"\textbf{Ear.} \ The lab plays the Tune at 4 bits, \ with and without dither, \ in random order; \ say which is which.",
            r"\textbf{Build.} \ Write a third-order delta-sigma modulator and measure its gain per octave of oversampling.",
            r"$\bigstar$ \ How far below Nyquist can music be sampled before listeners notice?",
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
            (r"filters, \ delay and reverb: \ the numbers, \ processed", [49]),
            (r"dynamics and distortion: \ where aliasing comes back", [50]),
            (r"synthesis: \ oscillators without aliasing", [51]),
            (r"mastering and loudness: \ dither and true peaks", [57]),
            (r"compression for the ear: \ hiding noise, \ again", [58]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In filters, delay and reverb, where the numbers are processed. In dynamics and "
            "distortion, where aliasing returns. In synthesis, which needs oscillators that do not alias. In mastering, with "
            "dither and true peaks. And in compression for the ear, which hides noise again, far more boldly."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"recording engineers", r"record at 24 bits and leave headroom; \ the floor is far below"),
            (r"mastering engineers", r"dither once, \ at the last step to 16 bits"),
            (r"plug-in designers", r"oversample anything that makes new high frequencies"),
            (r"listeners", r"compare formats blind, \ and level-matched"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Recording engineers record at twenty-four bits and leave headroom, since the floor is far below. "
            "Mastering engineers dither once, at the last step to sixteen bits. Plug-in designers oversample anything that "
            "makes new high frequencies. And listeners compare formats blind, and at matched levels."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"K. C. Pohlmann, \ \textit{Principles of Digital Audio} \ (6th ed., \ 2010)",
             r"J. O. Smith, \ \textit{Mathematics of the Discrete Fourier Transform} \ (2007)",
             r"R. Schreier and G. C. Temes, \ \textit{Understanding Delta-Sigma Data Converters} \ (2005)",
             r"C. E. Shannon, \ `Communication in the presence of noise' \ (1949)",
             r"A. V. Oppenheim and R. W. Schafer, \ \textit{Discrete-Time Signal Processing} \ (3rd ed., \ 2010)"],
            [r"S. P. Lipshitz, \ R. A. Wannamaker and J. Vanderkooy, \ `Quantization and dither: \ a theoretical survey' \ (1992)",
             r"M. A. Gerzon and P. G. Craven, \ `Optimal noise shaping and dither of digital signals' \ (1989)",
             r"E. B. Meyer and D. R. Moran, \ `Audibility of a CD-standard A/D/A loop ...' \ (2007)",
             r"J. D. Reiss, \ `A meta-analysis of high resolution audio perceptual evaluation' \ (2016)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 48, "Chicago, 1947",
            "What can be done to a list of numbers? Can arithmetic build a room?",
            "The sound is now a list of numbers. <bookmark mark='a'/> In 1947 an engineer put a loudspeaker and a "
            "microphone in a tiled bathroom and sold the echo. Fifteen years later, at Bell Labs, Manfred Schroeder "
            "built a room out of arithmetic. What can be done to a list of numbers? <bookmark mark='b'/> Next time. "
            "Part 49: Filters, Delay and Reverb.",
            signoff=clip("bridge.signoff"))
