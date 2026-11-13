from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation3")
        head = VGroup(label(r"Variation 3", font_size=48, color=TUNE),
                      label(r"the Tune assembled from pure tones", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        head.to_edge(UP, buff=0.4)
        n = np.arange(1, 17)
        amps = np.abs(np.sin(n * np.pi * 0.11)) / n
        bars = partial_bars(amps / amps.max(), width=8.6, height=2.6, db=False).move_to(UP * 0.5)
        for b in bars.bars:
            b.set_opacity(0.12)
        how = label(r"each note: \ the string's own partials, \ but only the first few", font_size=26, color=GREY_A).next_to(bars, UP, buff=0.2)
        count = label(r"1 partial", font_size=36, color=TUNE).next_to(bars, RIGHT, buff=0.4)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a way of "
            "taking sounds apart, so the Variation puts one together. <bookmark mark='a'/> Each note is a sum of "
            "pure tones, with the amounts and the decays of the plucked string. But the first phrase is allowed "
            "only one partial: plain sine waves. The second phrase gets two. Then three, five, eight and sixteen. "
            "Listen to a string come into being."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(how), FadeIn(count))
        words = None
        with self.listen(c) as snd:
            window(snd, r"Variation 3", kind="synthesized", detail=r"sums of sines", tag_corner=DR)
            phrase, k_in = -1, 0
            for k, nt in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if nt["phrase"] != phrase:
                    phrase, k_in = nt["phrase"], 0
                    names = [m["name"] for m in c.notes if m["phrase"] == phrase]
                    new = VGroup(*[label(t, font_size=40, color=GREY_D) for t in names]).arrange(RIGHT, buff=0.7).move_to(DOWN * 2.2)
                    if words is not None:
                        self.remove(words)
                    words = new
                    self.remove(count)
                    kk = nt["partials"]
                    count = label(rf"{kk} partial" + ("s" if kk > 1 else ""), font_size=36, color=TUNE).next_to(bars, RIGHT, buff=0.4)
                    self.add(words, count)
                kk = nt["partials"]
                t0 = nt["t"]
                for j, b in enumerate(bars.bars):
                    on = j < kk
                    snd.drive(b, lambda m, t, on=on, t0=t0, j=j: m.set_opacity((0.3 + 0.65 * float(np.exp(-(1.0 + 0.25 * j) * max(t - t0, 0)))) if on else 0.12))
                words[k_in].set_color(TUNE)
                k_in += 1
        rows = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rows, highlight=(len(rows) - 1,)).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Row three of the ledger. {say(v['seconds'])} seconds, and by the last phrase the sound is "
            f"{say(d['brighter'], 1)} times as bright, for its pitch, as it was in the first. Sixty-five rows to go."
        ):
            self.play(FadeOut(words), FadeOut(how), FadeOut(count), bars.animate.scale(0.6).shift(UP * 1.0), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"any wave is a sum of sines; \ the amount of each is an average of the wave times that sine",
            r"the DFT does it for samples; \ the fast algorithm does it in $N \log N$ steps",
            r"a row of resonators is a Fourier analyser; \ the ear ignores phase only where it can separate the partials",
            r"a spectrogram needs a window, \ and the window decides what you see",
            r"$\Delta t \cdot \Delta f \ge 1/4\pi$: \ you cannot know exactly when and exactly what pitch",
            r"timbre is a recipe that changes in time: \ attack, \ brightness, \ and their motion",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Fourier was right: any wave is a sum of sines, and the amount of each is an average. "
            "<bookmark mark='a'/> A computer does it for samples, and since 1965 does it fast. <bookmark mark='b'/> "
            "A row of resonators does the same job, and the ear behaves like one, ignoring phase wherever it can "
            "pull the partials apart. <bookmark mark='c'/> To watch a recipe change you need a window, and the "
            "window shapes what you see. <bookmark mark='d'/> There is a hard limit on knowing when and what pitch "
            "together. <bookmark mark='e'/> And the recipe is not the whole sound: timbre lives in how the recipe "
            "changes, most of all at the start."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, r in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Find the Fourier coefficients of a sawtooth wave by Fourier's recipe. \ Which is the first harmonic "
            r"more than 40 dB below the fundamental? \ Compare with a square wave.",
            r"Show that playing a signal backwards replaces its transform $X[k]$ by its complex conjugate, \ so that "
            r"no magnitude changes. \ What happens to the phases?",
            r"\textbf{Ear.} \ The lab plays three tones on one note. \ Put them in order of brightness, \ and say "
            r"which one has only odd harmonics.",
            r"\textbf{Build.} \ Write the inverse of \texttt{fourier.stft} by overlap and add, \ and show that a Hann "
            r"window with a hop of a quarter gives back the sound exactly.",
            r"$\bigstar$ \ Build a reassigned constant-Q transform, \ and measure how accurately it finds the onsets "
            r"and pitches of Monochord's notes against an ordinary one.",
        ], font_size=24)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"the spectrogram", [4, 7, 8, 9]),
            (r"resonators as an analyser; \ phase", [4]),
            (r"brightness, attack and flux", [5, 41, 51]),
            (r"the fast transform, \ windows, \ leakage", [48, 49, 58]),
            (r"constant Q", [61, 62]),
            (r"noise and its colours", [46, 51, 55]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? The spectrogram is in almost every part from here on. Resonators and phase "
            "are the starting point of Part 4, on the ear. Brightness and attack return when we orchestrate, and "
            "when we build synthesizers. The fast transform and its windows are the foundation of digital audio "
            "and of every audio codec. And constant Q is how our listening machines will see."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"mixing and mastering engineers", r"read a spectrum analyser all day: \ know its window and its bin width before trusting it"),
            (r"audio programmers", r"the FFT, \ overlap-add, \ and the trade between latency and resolution"),
            (r"sound designers", r"attack decides identity: \ swap attacks and tails to make new instruments"),
            (r"researchers in music information retrieval", r"constant-Q and mel pictures are the input to most models"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A mixing engineer reads a spectrum analyser all day, and should know its window and "
            "its bin width before believing it. Audio programmers live with the trade between resolution and "
            "delay. Sound designers know that the attack decides what an instrument is, and build new ones by "
            "swapping attacks and tails. And most machines that listen take one of this part's pictures as input."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"W. M. Hartmann, \ \textit{Signals, Sound, and Sensation} \ (1997)",
             r"M. M\"uller, \ \textit{Fundamentals of Music Processing} \ (2nd ed., 2021), ch.\ 2",
             r"J. O. Smith, \ \textit{Mathematics of the Discrete Fourier Transform} \ (2nd ed., 2007)",
             r"H. von Helmholtz, \ \textit{On the Sensations of Tone} \ (1863; tr.\ Ellis)"],
            [r"J. Fourier, \ \textit{Th\'eorie analytique de la chaleur} \ (1822)",
             r"J. W. Cooley and J. W. Tukey, \ ``An algorithm for the machine calculation of complex Fourier series'', \ \textit{Math. Comp.} 19 (1965)",
             r"D. Gabor, \ ``Theory of communication'', \ \textit{J. IEE} 93 (1946)",
             r"F. J. Harris, \ ``On the use of windows for harmonic analysis with the discrete Fourier transform'', \ \textit{Proc. IEEE} 66 (1978)",
             r"J. C. Brown, \ ``Calculation of a constant Q spectral transform'', \ \textit{JASA} 89 (1991)",
             r"J. M. Grey, \ ``Multidimensional perceptual scaling of musical timbres'', \ \textit{JASA} 61 (1977)",
             r"J. N. Oppenheim and M. O. Magnasco, \ ``Human time-frequency acuity beats the Fourier uncertainty principle'', \ \textit{PRL} 110 (2013)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        d = load("missing")
        c = clip("missing.tease")
        n = np.arange(1, 9)
        sets = [np.ones(8), np.array([0, 0, 0, 1, 1, 1, 1, 1.0]), np.array([1, 0, 0, 0, 0, 0, 0, 0.0])]
        bars = VGroup(*[partial_bars(np.maximum(s, 0.001), width=3.4, height=1.6, db=False) for s in sets]).arrange(RIGHT, buff=0.8).move_to(UP * 0.9)
        tags = VGroup(*[label(t, font_size=24, color=GREY_A).next_to(b, UP, buff=0.15) for t, b in
                        zip((r"partials 1 to 8", r"partials 4 to 8 only", r"partial 1 alone"), bars)])
        with self.voiceover(
            "One last sound, because this part's picture has a hole in it. Here is a tone with eight partials. "
            "Then the same tone with its lowest three partials taken out, so that there is no energy at all at the "
            "frequency of the note. Then that lowest partial by itself."
        ):
            self.play(FadeIn(bars), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"all eight, \ the top five, \ the lowest alone", kind="synthesized", corner=DL, tag_corner=DR)
            for ev, b in zip(("full", "upper", "pure"), bars):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                frame = SurroundingRectangle(b, color=EAR, buff=0.12, stroke_width=3)
                snd.show(frame)
                snd.drive(frame, lambda m, t, t0=t0: m.set_stroke(opacity=(0.55 + 0.45 * np.sin(20 * t)) if t0 <= t < t0 + 1.6 else 0.0))
                snd.wait_until(t0 + 1.6)
        nxt = VGroup(label(r"Part 4", font_size=34, color=GREY_B), label(r"The Ear", font_size=54, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second tone has nothing at the bottom, and yet its pitch did not move. It is the same note as the "
            "first and the third. This is what Seebeck's siren did, and Ohm's law cannot explain it. "
            "<bookmark mark='a'/> A spectrum says what is in the air. It does not say what you hear. For that we "
            "have to open the instrument that does the listening. That is Part 4: The Ear."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
