from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403
from videos.music.variations import rows_before

VC = [TUNE, BLUE, EAR, GREY_A]


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
        d = load("tune53")
        c = clip("tune.variation53")
        st = d["starts"]
        head = VGroup(label(r"Variation 53", font_size=48, color=TUNE), label(r"the Tune, \ tracked and in a tempo canon", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        canon = d["canon"]
        tc = d["t_conv"]
        span = tc + 2.0
        W_ = 11.0
        x0 = -W_ / 2
        bars = VGroup()
        times = []
        for v, k, a, du in canon:
            b = Rectangle(width=max(W_ * du / span - 0.01, 0.02), height=0.08, stroke_width=0, fill_color=VC[v], fill_opacity=1.0)
            b.move_to([x0 + W_ * a / span + b.width / 2, -2.2 + 0.9 * v + 0.05 * (k - 60), 0])
            bars.add(b)
            times.append(st["canon"] + a)
        conv = DashedLine([x0 + W_ * tc / span, -2.4, 0], [x0 + W_ * tc / span, 1.4, 0], color=WHITE, stroke_width=2)
        cl = label(rf"all four meet: \ {tc:.1f} s", font_size=16, color=WHITE).next_to(conv, UP, buff=0.1)
        rl = VGroup(*[label(rf"speed {r:g}", font_size=14, color=VC[i]).move_to([x0 - 0.6, -2.0 + 0.9 * i, 0]) for i, r in enumerate(d["ratios"])])
        trk = label(r"first: \ the tracker module \ (lead, \ bass, \ arpeggio, \ drums)", font_size=18, color=GREY_A).move_to(UP * 2.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here it is first as a "
            "four-channel tracker module, lead, bass, arpeggio and drums, played by the engine. <bookmark mark='b'/> Then the "
            "whole Tune as a tempo canon, Nancarrow's form: four voices at speeds three, four, five and six, the slowest "
            "starting first, each started so that all four arrive together on the last note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(trk))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(rl), FadeIn(conv), FadeIn(cl))
        with self.listen(c) as snd:
            window(snd, r"Variation 53", kind="synthesized", detail=r"tracker, \ then canon", corner=DL, tag_corner=DR)
            pulse(snd, trk, st["tracker"], st["canon"] - 0.3, buff=0.12)
            for vv in range(4):
                idx = [i for i, row in enumerate(canon) if row[0] == vv]
                flash(snd, [bars[i] for i in idx], [times[i] for i in idx], hot=WHITE, base=VC[vv])
            ln = Line([x0, -2.4, 0], [x0, 1.4, 0], color=WHITE, stroke_width=2, stroke_opacity=0.6)
            snd.show(ln)
            snd.drive(ln, lambda m, t: m.move_to([x0 + W_ * min(max(t - st["canon"], 0), span) / span, -0.5, 0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune53")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-three of the ledger: {say(len(d['rows']))} tracker rows; four voices meeting on the last note after "
            f"{say(d['t_conv'], 1)} seconds; and the canon rendered in blocks identical, to the last bit, to the canon rendered "
            "at once."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"music as instructions is old: \ pinned cylinders, \ paper rolls, \ Nancarrow's canons",
            r"MUSIC N split instruments from notes; \ MIDI is the notes",
            r"MIDI 1.0: \ 320 microseconds a byte, \ seven-bit data, \ running status; \ MPE and 2.0 go further",
            r"a MIDI file stores a performance thousands of times smaller than its sound",
            r"an engine must give the same music in any block size, \ meet every deadline, \ and time notes to the sample",
            r"parallel paths must be delayed to the slowest, \ or they comb",
        ], title=r"What we found", font_size=21).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Music as instructions is old: pinned cylinders, paper rolls, Nancarrow's canons. "
            "<bookmark mark='a'/> MUSIC N split instruments from notes, and MIDI is the notes. <bookmark mark='b'/> MIDI 1.0 "
            "sends a byte every three hundred and twenty microseconds, with seven-bit data and running status; MPE and MIDI 2.0 "
            "go further. <bookmark mark='c'/> A MIDI file stores a performance thousands of times smaller than its sound. "
            "<bookmark mark='d'/> An engine must give the same music in any block size, meet every deadline, and time notes to "
            "the sample. <bookmark mark='e'/> And parallel paths must be delayed to the slowest, or they comb."
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
            r"With running status, \ how long does a 10-note chord take to arrive, \ and how long without?",
            r"Prove that a variable-length quantity of $n$ bytes holds every number below $2^{7n}$, \ and that no code is the start of another.",
            r"\textbf{Ear.} \ The lab plays a groove with notes snapped to blocks or placed exactly, \ at random; \ say which.",
            r"\textbf{Build.} \ Add a tempo change to the MIDI writer \ (a second tempo event) \ and make the reader honour it.",
            r"$\bigstar$ \ What is the best-sounding neural effect guaranteed never to miss a deadline?",
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
            (r"microphones and loudspeakers: \ the ends of the chain", [54]),
            (r"recording and mixing: \ the session in the workstation", [56]),
            (r"live sound: \ latency on stage", [59]),
            (r"transcription: \ from audio back to MIDI", [61]),
            (r"machines that compose: \ MIDI corpora as training data", [65]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In microphones and loudspeakers, the two ends of the chain. In recording and mixing, "
            "the session inside the workstation. In live sound, where latency meets a stage. In transcription, from audio back "
            "to MIDI. And in machines that compose, trained on MIDI corpora."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"producers", r"record with small blocks, \ mix with large ones"),
            (r"engineers", r"trust delay compensation, \ and check parallel paths by ear"),
            (r"plug-in developers", r"never allocate or lock in the audio thread"),
            (r"performers", r"use MPE for slides and swells MIDI 1.0 cannot say"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Producers record with small blocks and mix with large ones. Engineers trust delay compensation "
            "and still check parallel paths by ear. Plug-in developers never allocate or lock in the audio thread. And "
            "performers use MPE for the slides and swells MIDI 1.0 cannot say."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"MIDI Manufacturers Association, \ \textit{The Complete MIDI 1.0 Detailed Specification} \ (1983--96)",
             r"M. V. Mathews, \ \textit{The Technology of Computer Music} \ (1969)",
             r"M. Puckette, \ \textit{The Theory and Technique of Electronic Music} \ (2007)",
             r"K. Gann, \ \textit{The Music of Conlon Nancarrow} \ (1995)"],
            [r"J. McCartney, \ `Rethinking the computer music language: \ SuperCollider' \ (2002)",
             r"A. McLean, \ `Making programming languages to dance to' \ (2014)",
             r"R. Bencina, \ `Real-time audio programming 101: \ time waits for nothing' \ (2011)",
             r"C. Chafe and others, \ `Effect of time delay on ensemble accuracy' \ (2004)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act X: \ the studio and the stage", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Everything so far has been numbers inside a computer.", font_size=24, color=WHITE).move_to(UP * 1.7)
        q = label(r"how does air become numbers, \ and numbers become air?", font_size=30, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 54", font_size=32, color=GREY_B), label(r"Microphones and Loudspeakers", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That ends the act on electric sound. Everything so far has been numbers inside a computer. <bookmark mark='a'/> How "
            "does air become numbers, and numbers become air? <bookmark mark='b'/> Next time, the studio and the stage begin. "
            "Part 54: Microphones and Loudspeakers."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
