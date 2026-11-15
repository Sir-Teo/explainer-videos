from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403
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
        d = load("tune")
        c = clip("tune.variation44")
        head = VGroup(label(r"Variation 44", font_size=48, color=TUNE), label(r"the Tune, \ on cue", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        w, e = d["click"]
        cells = VGroup(
            VGroup(label(r"1. \ a cue", font_size=22, color=TUNE), label(rf"14 beats at {d['bpm']:.1f} \ (a {w}-{e} click): \ the last note lands on a hit at {d['hit']:.1f} s", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"2. \ a leitmotif, \ three moods", font_size=22, color=TUNE), label(r"heroic \ (horn), \ tender \ (flute), \ menacing \ (low strings, \ minor)", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"3. \ an adaptive loop", font_size=22, color=TUNE), label(r"four passes, \ a layer added each time: \ bass, \ drums, \ brass", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        hitbar = VGroup(Line([-4.5, -2.0, 0], [4.5, -2.0, 0], color=GREY_D), Line([4.0, -2.2, 0], [4.0, -1.8, 0], color=EAR, stroke_width=4),
                        label(rf"hit: \ {d['hit']:.1f} s", font_size=14, color=EAR).move_to([4.0, -1.55, 0]))
        head_ph = Dot([-4.5, -2.0, 0], radius=0.08, color=WHITE)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, three things. A "
            f"cue: the tempo chosen so that fourteen beats carry the first two phrases to a hit point at {say(d['hit'], 1)} "
            "seconds, where the brass lands. Then the first phrase as a leitmotif in three moods. And then an adaptive loop, "
            "gaining a layer on every pass."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(hitbar), FadeIn(head_ph))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Variation 44", kind="synthesized", detail=r"orchestra, \ piano, \ bass, \ drums", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["cue"], st["moods"] - 0.4, buff=0.1)
            pulse(snd, cells[1], st["moods"], st["loop"] - 0.4, buff=0.1)
            pulse(snd, cells[2], st["loop"], c.duration, buff=0.1)
            snd.drive(head_ph, lambda m, now: m.move_to([-4.5 + 8.5 * min(max(now - st["cue"], 0), d["hit"]) / d["hit"], -2.0, 0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-four of the ledger: {say(v['seconds'], 1)} seconds; the measurement is the cue's arithmetic, the "
            "tempo and click that land its last note on the hit."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"music tells a viewer how to read a picture",
            r"a leitmotif keeps its contour and rhythm while its mood changes",
            r"hits are arithmetic: \ beats = seconds $\times$ tempo / 60, \ to within a frame",
            r"sound may lag a picture more than it may lead it",
            r"adaptive scores are state machines; \ waiting for a boundary costs half its length",
            r"hardware limits made a style: \ duty cycles, \ arpeggio chords, \ noise drums",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Music tells a viewer how to read a picture. <bookmark mark='a'/> A leitmotif keeps its "
            "contour and rhythm while its mood changes. <bookmark mark='b'/> Hits are arithmetic: beats equal seconds times "
            "tempo over sixty, to within a frame. <bookmark mark='c'/> Sound may lag a picture more than it may lead it. "
            "<bookmark mark='d'/> Adaptive scores are state machines, and waiting for a musical boundary costs half its "
            "length on average. <bookmark mark='e'/> And hardware limits made a style: duty cycles, arpeggio chords and noise "
            "drums."
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
            r"A hit falls 9.5 s after a cue's downbeat. \ Which tempos between 100 and 130 put it on a beat?",
            r"Prove that waiting for the next boundary of length u delays a randomly timed event by u/2 on average.",
            r"\textbf{Ear.} \ The lab plays door slams with random offsets; \ say early, \ in sync or late.",
            r"\textbf{Build.} \ Add a state \ (`stealth') \ to the adaptive score, \ with its own segment and layers.",
            r"$\bigstar$ \ Which transition rule best balances responsiveness and coherence for players?",
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
            (r"the auditory scene: \ how the ear binds sound and source", [45]),
            (r"expectation and emotion", [46]),
            (r"oscillators and filters, \ from scratch", [51]),
            (r"the workstation and the sequencer", [53]),
            (r"machines that compose, \ and generative audio", [65, 66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the auditory scene, how the ear binds a sound to its source. In expectation and "
            "emotion. In oscillators and filters built from scratch. In the workstation and the sequencer. And in machines "
            "that compose, and generative audio."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"film composers", r"spot with the director, \ then set tempos to the frame"),
            (r"music editors", r"cut, \ stretch and move cues when the picture changes"),
            (r"game audio teams", r"write segments, \ layers and stingers, \ then the rules in middleware"),
            (r"mixers", r"duck music under dialogue, \ and carve the speech band"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Film composers spot with the director, then set their tempos to the frame. Music editors cut, "
            "stretch and move cues whenever the picture changes. Game audio teams write segments, layers and stingers, and "
            "then the rules that join them. And mixers duck the music under dialogue and carve out the speech band."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"F. Karlin and R. Wright, \ \textit{On the Track} \ (2nd ed., \ 2004)",
             r"F. Lehman, \ \textit{Hollywood Harmony} \ (2018)",
             r"K. Collins, \ \textit{Game Sound} \ (2008)",
             r"A. J. Cohen, \ `Congruence-association model of music and multimedia' \ (2013)"],
            [r"M. G. Boltz, \ `Musical soundtracks as a schematic influence on the cognitive processing of filmed events' \ (2001)",
             r"ITU-R BT.1359, \ `Relative timing of sound and vision for broadcasting' \ (1998)",
             r"M. Z. Land and P. N. McConnell, \ the iMUSE patent \ (1994)",
             r"K. Collins \ (ed.), \ \textit{From Pac-Man to Pop Music} \ (2008)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"how does the ear decide which sounds belong together?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VIII: \ the mind", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"The craft is done: \ composing, \ performing, \ scoring.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 45", font_size=32, color=GREY_B), label(r"The Scene", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The craft is done: orchestrating, composing, performing and scoring. Act eight turns to the mind. "
            "<bookmark mark='a'/> When many sounds arrive at once, how does the ear decide which belong together? "
            "<bookmark mark='b'/> Next time. Part 45: The Scene."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
