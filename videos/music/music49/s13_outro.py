from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403
from videos.music.variations import rows_before

SPACE = {"dry": (r"dry", GREY_A), "tiled room": (r"a tiled room", BLUE), "plate": (r"a steel plate", TUNE), "spring": (r"a spring", EAR), "cathedral": (r"a cathedral", GOLD)}


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
        d = load("tune49")
        c = clip("tune.variation49")
        head = VGroup(label(r"Variation 49", font_size=48, color=TUNE), label(r"the Tune in five spaces", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for k in d["names"]:
            name, col = SPACE[k]
            rt = d["rt60"].get(k)
            parts = [label(name, font_size=22, color=col)]
            parts.append(label(rf"RT60 {rt:.1f} s" if rt else r"no reverberation", font_size=16, color=WHITE))
            cells.add(VGroup(RoundedRectangle(width=2.3, height=1.5, corner_radius=0.15, stroke_color=GREY_B), VGroup(*parts).arrange(DOWN, buff=0.15)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.1)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its first phrase in "
            "five spaces: dry; in the simulated tiled room; on the finite-difference plate; on the spring; and in a cathedral "
            "made of a feedback delay network with long delays."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        st = d["starts"]
        names = d["names"]
        with self.listen(c) as snd:
            window(snd, r"Variation 49", kind="synthesized", detail=r"Part 7's piano, \ in five spaces", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune49")
        r = d["rt60"]
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-nine of the ledger: the reverberation times. {say(r['tiled room'], 1)} seconds in the room, "
            f"{say(r['plate'], 1)} on the plate, {say(r['spring'], 1)} on the spring, and {say(r['cathedral'], 1)} in the "
            "cathedral."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a linear effect is its impulse response; \ applying it is convolution",
            r"feedback places poles; \ poles and zeros shape the frequency response",
            r"an all-pass changes only timing, \ and timing can be heard in attacks",
            r"one delay makes a comb, \ a pitch, \ a flanger; \ several make a chorus",
            r"a room is a sum of images; \ Sabine and Eyring predict its decay",
            r"Schroeder's combs, \ delay networks, \ plates and springs imitate rooms",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A linear effect is its impulse response, and applying it is convolution. <bookmark mark='a'/> "
            "Feedback places poles, and poles and zeros shape the frequency response. <bookmark mark='b'/> An all-pass changes "
            "only timing, and timing can be heard in attacks. <bookmark mark='c'/> One delay makes a comb, a pitch, a flanger; "
            "several make a chorus. <bookmark mark='d'/> A room is a sum of images, and Sabine and Eyring predict its decay. "
            "<bookmark mark='e'/> And Schroeder's combs, delay networks, plates and springs imitate rooms."
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
            r"A room is 10 by 8 by 4 m, \ its surfaces absorbing 20\%. \ What reverberation time does Sabine predict?",
            r"Prove that a first-order all-pass $H(z) = (c + z^{-1})/(1 + c z^{-1})$ has $|H| = 1$ on the unit circle.",
            r"\textbf{Ear.} \ The lab plays a groove through a random filter; \ say which kind, \ and roughly where.",
            r"\textbf{Build.} \ Fit a feedback delay network's line gains to match the tiled room's RT60.",
            r"$\bigstar$ \ How small can a feedback delay network be and still pass for a given room?",
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
            (r"dynamics and distortion: \ effects that are not linear", [50]),
            (r"synthesis: \ filters that sweep and resonate", [51]),
            (r"physical models: \ delay lines that are strings and tubes", [52]),
            (r"rooms and space: \ real halls, \ measured", [55]),
            (r"recording and mixing: \ equalizers and reverbs at work", [56]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In dynamics and distortion, effects that are not linear. In synthesis, with filters "
            "that sweep and resonate. In physical models, where delay lines become strings and tubes. In rooms and space, "
            "with real halls. And in recording and mixing, where equalizers and reverbs go to work."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"mix engineers", r"send many tracks to one reverb, \ so they share a space"),
            (r"producers", r"pre-delay a vocal's reverb, \ so the words stay clear"),
            (r"acousticians", r"measure halls by sweep, \ and predict them with Sabine first"),
            (r"plug-in makers", r"model plates, \ springs and circuits from their physics"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Mix engineers send many tracks to one reverb, so they share a space. Producers pre-delay a "
            "vocal's reverb, so the words stay clear. Acousticians measure halls by sweep, and predict them with Sabine first. "
            "And plug-in makers model plates, springs and circuits from their physics."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. O. Smith, \ \textit{Introduction to Digital Filters} \ (2007)",
             r"J. O. Smith, \ \textit{Physical Audio Signal Processing} \ (2010)",
             r"U. Z\"olzer \ (ed.), \ \textit{DAFX: \ Digital Audio Effects} \ (2nd ed., \ 2011)",
             r"S. Bilbao, \ \textit{Numerical Sound Synthesis} \ (2009)"],
            [r"M. R. Schroeder, \ `Natural sounding artificial reverberation' \ (1962)",
             r"J. B. Allen and D. A. Berkley, \ `Image method for efficiently simulating small-room acoustics' \ (1979)",
             r"J.-M. Jot and A. Chaigne, \ `Digital delay networks for designing artificial reverberators' \ (1991)",
             r"V. V\"alim\"aki and others, \ `Fifty years of artificial reverberation' \ (2012)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 49, "1951, and 1998",
            "What happens when the effect is not linear?",
            "Every effect in this part obeyed superposition. <bookmark mark='a'/> Two accidents made two sounds. An "
            "amplifier damaged on the way to a session in 1951 gave a record its fuzz, and in 1998 a pitch corrector "
            "set to act instantly made a voice snap between notes, and that became a style. What happens when the "
            "effect is not linear? <bookmark mark='b'/> Next time. Part 50: Dynamics, Distortion and Pitch.")
