from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403
from videos.music.variations import rows_before


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
        d = load("tune52")
        c = clip("tune.variation52")
        st = d["starts"]
        head = VGroup(label(r"Variation 52", font_size=48, color=TUNE), label(r"the Tune, \ in FM and in grains", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        total = c.duration
        W = 12.0
        x0 = -W / 2

        def X(t):
            return x0 + W * t / total
        keys = [(m, a, dd) for m, a, dd in d["keys"]]
        bells = [(m, a + st["bells"], dd) for m, a, dd in d["bells"]]
        bars = VGroup()
        for m, a, dd in keys + bells:
            col = TUNE if a < st["bells"] else EAR
            b = Rectangle(width=max(W * dd / total - 0.03, 0.03), height=0.09, stroke_width=0, fill_color=col, fill_opacity=1.0)
            b.move_to([X(a) + b.width / 2, -1.6 + 0.12 * (m - 58), 0])
            bars.add(b)
        rng = np.random.default_rng(2)
        g0, g1 = st["grains"], st["back"] - 0.3
        specks = VGroup(*[Dot([X(g0 + (g1 - g0) * u), -1.6 + 0.12 * (2 + 22 * v), 0], radius=0.025, color=interpolate_color(ManimColor(BLUE), ManimColor(EAR), v)) for u, v in zip(rng.random(260), rng.random(260))])
        back = Rectangle(width=W * 1.6 / total, height=0.09, stroke_width=0, fill_color=TUNE, fill_opacity=1.0).move_to([X(st["back"]) + W * 0.8 / total, -1.6 + 0.12 * 2, 0])
        labs = VGroup(label(r"FM keys", font_size=17, color=TUNE).move_to([X(st["keys"] + 1.5), 1.6, 0]), label(r"FM bells", font_size=17, color=EAR).move_to([X(st["bells"] + 1.5), 1.6, 0]),
                      label(r"grains", font_size=17, color=BLUE).move_to([X((g0 + g1) / 2), 1.6, 0]), label(r"back", font_size=17, color=TUNE).move_to([X(st["back"]) + 0.3, 1.6, 0]))
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its first two "
            "phrases on the FM electric piano and the next two on FM bells; then the whole dissolved into grains, scattering in "
            "time and pitch and gathering again; then one clean note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(specks), FadeIn(back), FadeIn(labs))
        with self.listen(c) as snd:
            window(snd, r"Variation 52", kind="synthesized", detail=r"FM and grains", corner=DL, tag_corner=DR)
            flash(snd, list(bars), [a for _, a, _ in keys + bells], hot=WHITE, base=TUNE)
            ln = Line([x0, -1.8, 0], [x0, 1.4, 0], color=WHITE, stroke_width=2, stroke_opacity=0.7)
            snd.show(ln)
            snd.drive(ln, lambda m, t: m.move_to([X(min(max(t, 0), total)), -0.2, 0]))
            snd.drive(specks, lambda m, t: m.set_opacity(0.4 + 0.6 * (g0 <= t <= g1) * (0.5 + 0.5 * np.sin(9 * t))))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune52")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Row fifty-two of the ledger. FM's lines match Bessel's functions to within "
            f"{say(d['bessel_err'] * 1e6, 1)} millionths, and the dissolve used {say(d['grains'])} grains in ten seconds."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"FM puts lines at $f_c \pm k f_m$ with sizes $J_k(I)$: \ the ratio picks the lines, \ the index the brightness",
            r"operators and algorithms made FM an instrument, \ and feedback can make sawtooth-like spectra",
            r"grains trade time for frequency, \ and free time from pitch",
            r"spectral models turn a recording into knobs; \ samplers keep the recording",
            r"tuned Karplus--Strong, \ waveguides and modes compute physics, \ each with its own exactness and cost",
            r"methods differ most in what they let a player control",
        ], title=r"What we found", font_size=21).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? FM puts lines at the carrier plus and minus multiples of the modulator, with sizes given by "
            "Bessel's functions: the ratio picks the lines, the index the brightness. <bookmark mark='a'/> Operators and "
            "algorithms made FM an instrument, and feedback can make sawtooth-like spectra. <bookmark mark='b'/> Grains trade time for "
            "frequency, and free time from pitch. <bookmark mark='c'/> Spectral models turn a recording into knobs, while "
            "samplers keep the recording. <bookmark mark='d'/> Tuned Karplus-Strong, waveguides and modes compute physics, each "
            "with its own exactness and cost. <bookmark mark='e'/> And the methods differ most in what they let a player control."
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
            r"A carrier at 400 Hz is modulated at 100 Hz with index 1. \ Using Carson's rule, \ how wide is the spectrum, \ and which lines does it hold?",
            r"Prove the complex phase-modulation coefficient identity: \ $\sum_k J_k(I)^2 = 1$.",
            r"\textbf{Ear.} \ The lab plays FM tones at random ratios; \ say which are harmonic and which are bells.",
            r"\textbf{Build.} \ Add a bow to the waveguide string \ (a friction curve at the contact point) \ and find its threshold.",
            r"$\bigstar$ \ How few parameters can match an instrument across its range, \ including playing it never heard?",
        ], font_size=21)
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
            (r"MIDI and the sequencer: \ playing these engines", [53]),
            (r"recording and mixing: \ sampled and modelled instruments in the session", [56]),
            (r"compression for the ear: \ sines and noise in codecs", [58]),
            (r"source separation: \ taking a mix apart, \ as the spectral model took a note apart", [64]),
            (r"generative audio: \ differentiable and neural synthesizers", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next time, in MIDI and the sequencer, which play these engines. In recording and "
            "mixing, with sampled and modelled instruments in the session. In codecs, which split sound into sines and noise. "
            "In source separation, taking a mix apart as the spectral model took a note apart. And in generative audio, with "
            "differentiable and neural synthesizers."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"sound designers", r"move the FM index with an envelope; \ keep ratios simple for pitch"),
            (r"composers", r"freeze, \ stretch and scatter recordings with grains"),
            (r"instrument makers", r"sample the attack, \ model the resonance"),
            (r"game audio", r"strike objects through their modes, \ thousands at once"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Sound designers move the FM index with an envelope and keep ratios simple for clear pitch. "
            "Composers freeze, stretch and scatter recordings with grains. Instrument makers sample the attack and model the "
            "resonance. And game audio strikes objects through their modes, thousands at once."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. M. Chowning, \ `The synthesis of complex audio spectra by means of frequency modulation' \ (1973)",
             r"C. Roads, \ \textit{Microsound} \ (2001)",
             r"J. O. Smith, \ \textit{Physical Audio Signal Processing} \ (2010)",
             r"S. Bilbao, \ \textit{Numerical Sound Synthesis} \ (2009)"],
            [r"K. Karplus and A. Strong; \ D. Jaffe and J. O. Smith \ (both 1983)",
             r"M. E. McIntyre, \ R. T. Schumacher and J. Woodhouse, \ `On the oscillations of musical instruments' \ (1983)",
             r"X. Serra and J. O. Smith, \ `Spectral modeling synthesis' \ (1990)",
             r"D. Gabor, \ `Acoustical quanta and the theory of hearing' \ (1947)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act IX: \ electric sound", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"January 1983: \ two synthesizers from rival firms, \ joined by a five-pin cable.", font_size=24, color=WHITE).move_to(UP * 1.7)
        q = label(r"how did a few pages of specification run an industry for forty years?", font_size=28, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 53", font_size=32, color=GREY_B), label(r"MIDI, \ Sequencers and the DAW", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In January 1983, on a trade-show floor, two synthesizers from rival firms were joined by a five-pin cable, and a key "
            "pressed on one sounded the other. <bookmark mark='a'/> How did a few pages of specification run an industry for "
            "forty years? <bookmark mark='b'/> Next time. Part 53: MIDI, Sequencers and the DAW."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
