from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403
from videos.music.variations import rows_before

TRACKS = [("lead", r"lead: \ saw and pulse, \ brass envelope, \ vibrato", TUNE), ("bass", r"bass: \ square, \ pluck", EAR),
          ("arp", r"arpeggio: \ narrow pulse", BLUE), ("pad", r"pad: \ five-voice unison", GREY_A)]


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
        d = load("tune51")
        c = clip("tune.variation51")
        head = VGroup(label(r"Variation 51", font_size=48, color=TUNE), label(r"the Tune, \ switched on", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        pad_notes = [[m, a, dd] for keys, a, dd in d["pad"] for m in keys]
        voices = [d["lead"], d["bass"], d["arp"], pad_notes]
        lanes = VGroup()
        rolls = []
        for (k, t, col), v in zip(TRACKS, voices):
            lo = min(n[0] for n in v) - 1
            hi = max(n[0] for n in v) + 1
            r = mroll(v, width=9.6, height=0.9, lo=lo, hi=hi, color=col, total=48 * d["beat"], bar_h=0.07)
            rolls.append(r)
            lanes.add(VGroup(label(t, font_size=14, color=col), r).arrange(RIGHT, buff=0.3))
        for ln in lanes:
            ln[0].set_x(-6.9 + ln[0].width / 2)
            ln[1].set_x(1.6)
        lanes.arrange(DOWN, buff=0.3).move_to(DOWN * 0.4)
        for ln in lanes:
            ln[0].set_x(-6.9 + ln[0].width / 2)
            ln[1].set_x(1.6)
        solo = label(r"first the lead alone, \ then all four", font_size=17, color=GREY_A).next_to(lanes, DOWN, buff=0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here it is switched on, "
            "as Wendy Carlos made Bach: four lines, each played on its own patch, one at a time, and layered. A brass lead with "
            "a filter envelope and vibrato; a plucked square bass; a narrow pulse arpeggio; and a soft unison pad. First the "
            "lead alone, then all four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lanes), FadeIn(solo))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Variation 51", kind="synthesized", detail=r"four tracks, \ one patch each", corner=DL, tag_corner=DR)
            lead8 = [n for n in d["lead"] if n[1] < 8 * d["beat"] - 1e-6]
            flash(snd, rolls[0].notes[:len(lead8)], [st["solo"] + n[1] for n in lead8], hot=WHITE, base=TUNE)
            for r, v, (k, _, col) in zip(rolls, voices, TRACKS):
                flash(snd, r.notes, [st["full"] + n[1] for n in v], hot=WHITE, base=col)
            cursor(snd, rolls[0], st["full"], 1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune51")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cn = d["counts"]
        with self.voiceover(
            f"Row fifty-one of the ledger. {say(d['notes'])} notes on four tracks, counting each pad chord once: "
            f"{say(cn['lead'])} in the lead, {say(cn['bass'])} in the bass, {say(cn['arp'])} in the arpeggio. The lead's "
            f"oscillator keeps its aliasing {say(-d['alias_pb'])} decibels below its harmonics on average; a naive one would "
            f"manage only {say(-d['alias_naive'])}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"additive synthesis sums sines; \ the Hammond borrows tempered ones",
            r"subtractive synthesis filters a rich wave: \ a few knobs, \ every harmonic",
            r"a naive digital sawtooth aliases; \ band-limited steps cut it by 14 to 16 dB",
            r"the ladder is four poles and a loop: \ it rings at $k = 4$, \ and saturates",
            r"trapezoid and Newton step its circuit to second order",
            r"envelopes, \ LFOs, \ pulse width, \ sync and unison move a sound; \ fitting finds its knobs",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Additive synthesis sums sines, and the Hammond borrows tempered ones. <bookmark mark='a'/> "
            "Subtractive synthesis filters a rich wave: a few knobs move every harmonic. <bookmark mark='b'/> A naive digital "
            "sawtooth aliases, and band-limited steps cut it by fourteen to sixteen decibels. <bookmark mark='c'/> The ladder "
            "is four poles and a loop: its ideal linear stability boundary is k equals four, and its transistors saturate. <bookmark mark='d'/> The "
            "trapezoid with Newton's method steps its circuit to second order. <bookmark mark='e'/> And envelopes, LFOs, pulse "
            "width, sync and unison move a sound, while fitting finds its knobs."
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
            r"A ladder has its cutoff at 500 Hz and $k = 2$. \ What are its gains, \ in dB, \ at 0 Hz and at 500 Hz?",
            r"Prove that a pulse of width $w$ has harmonics of size proportional to $|\sin(\pi k w)|/k$.",
            r"\textbf{Ear.} \ The lab plays high notes on a naive or a PolyBLEP sawtooth, \ at random; \ say which is which.",
            r"\textbf{Build.} \ Add a peaking filter to the patch and refit the hook's target: \ how far does the distance fall?",
            r"$\bigstar$ \ Can gradient descent fit an analogue patch to a recorded note as reliably as a search?",
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
            (r"FM, \ grains and physical models: \ the other ways out of the oscillator", [52]),
            (r"MIDI and sequencers: \ how a keyboard talks to a synthesizer", [53]),
            (r"recording and mixing: \ synthesizers in the session", [56]),
            (r"pitch and transcription: \ the hook's inverse problem, \ for whole recordings", [61]),
            (r"generative audio: \ differentiable synthesizers inside networks", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next time, in FM, grains and physical models, the other ways out of the oscillator. In "
            "MIDI and sequencers, where a keyboard learns to talk to a synthesizer. In recording and mixing. In transcription, "
            "which is the hook's inverse problem for whole recordings. And in generative audio, with differentiable "
            "synthesizers inside networks."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"sound designers", r"start from a sawtooth and a filter envelope, \ then subtract"),
            (r"players", r"turn the resonance up gently: \ it costs the bass"),
            (r"plug-in developers", r"band-limit every jump, \ and step the ladder implicitly"),
            (r"producers", r"detune a little: \ the drift that analogue had for free"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Sound designers start from a sawtooth and a filter envelope, and subtract. Players turn the "
            "resonance up gently, because it costs the bass. Plug-in developers band-limit every jump and step the ladder "
            "implicitly. And producers detune a little, for the drift that analogue had for free."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"C. Roads, \ \textit{The Computer Music Tutorial} \ (2nd ed., \ 2023)",
             r"W. Pirkle, \ \textit{Designing Software Synthesizer Plug-Ins in C++} \ (2nd ed., \ 2021)",
             r"T. Pinch and F. Trocco, \ \textit{Analog Days} \ (2002)",
             r"V. Zavalishin, \ \textit{The Art of VA Filter Design} \ (2012, \ rev. 2018)",
             r"C. Dodge and T. A. Jerse, \ \textit{Computer Music} \ (2nd ed., \ 1997)"],
            [r"V. V\"alim\"aki and A. Huovilainen, \ `Oscillator and filter algorithms for virtual analog synthesis' \ (2006)",
             r"A. Huovilainen, \ `Non-linear digital implementation of the Moog ladder filter' \ (2004)",
             r"T. Stilson and J. Smith, \ `Alias-free digital synthesis of classic analog waveforms' \ (1996)",
             r"J. Engel and others, \ `DDSP: \ differentiable digital signal processing' \ (2020)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 51, "Stanford, 1967",
            "Why did a vibrato faster than the note sound like a bell?",
            "In 1967 a composer at Stanford turned a vibrato up until it was faster than the note itself. "
            "<bookmark mark='a'/> Why did he hear bells? <bookmark mark='b'/> Next time. Part 52: Synthesis Two, FM, "
            "Grains and Physical Models.")
