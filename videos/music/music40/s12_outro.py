from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403
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
        c = clip("tune.variation40")
        head = VGroup(label(r"Variation 40", font_size=48, color=TUNE), label(r"the Tune, \ produced", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        beat = 60.0 / d["bpm"]
        segs = [(r"intro", 0.0, d["verse_at"], GREY_A), (r"verse: \ the Tune's second phrase, \ low", d["verse_at"], d["chorus_at"], BLUE),
                (r"chorus: \ its first phrase as the hook", d["chorus_at"], d["starts"]["beat"] - 1.0, TUNE)]
        total = d["starts"]["beat"] - 1.0
        W = 12.0
        timeline = VGroup()
        for name, a, b, col in segs:
            r = Rectangle(width=W * (b - a) / total, height=0.6, stroke_width=1, stroke_color=col, fill_color=col, fill_opacity=0.3)
            r.move_to([-W / 2 + W * (a + b) / 2 / total, 1.2, 0])
            timeline.add(VGroup(r, label(name, font_size=15, color=WHITE).move_to(r)))
        slices = VGroup()
        for k in d["order"]:
            cell = Rectangle(width=0.62, height=0.55, stroke_color=GREY_B if k is not None else GREY_D, stroke_width=1.2,
                             fill_color=VOICE_C[(k or 0) % 4], fill_opacity=0.35 if k is not None else 0.0)
            slices.add(VGroup(cell, label(str(k + 1) if k is not None else r"--", font_size=14, color=WHITE).move_to(cell)))
        slices.arrange(RIGHT, buff=0.04).move_to(DOWN * 1.2)
        sl = label(r"then a beat: \ sixteen slices of Variation 7's recording, \ re-sequenced over drum-machine voices", font_size=18, color=GREY_A).next_to(slices, UP, buff=0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First as a pop single "
            f"of ours: a short intro, the voice entering after {say(round(d['voice_enters']))} seconds; a verse made from the "
            "Tune's second phrase, sung low; and a chorus that makes its first phrase the hook, over one, five, six, four, "
            "with a second voice and a sidechained pad. <bookmark mark='b'/> Then as a beat that samples Variation 7, the "
            "Tune played by Part 7's strings: its recording cut into sixteen slices and re-sequenced over drum-machine voices."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(timeline))
            vo.wait_until("b")
            self.play(FadeIn(slices), FadeIn(sl))
        st = d["starts"]
        step = 60.0 / d["bpm2"] / 4
        with self.listen(c) as snd:
            window(snd, r"Variation 40", kind="synthesized", detail=r"a model voice, \ band, \ pad, \ drum-machine voices, \ Variation 7's strings", corner=DL, tag_corner=DR)
            playhead = Line([-W / 2, 1.6, 0], [-W / 2, 0.8, 0], color=WHITE, stroke_width=3)
            snd.show(playhead)
            snd.drive(playhead, lambda m, t: m.move_to([-W / 2 + W * min(t, total) / total, 1.2, 0]))
            for rep in range(8):
                for k in range(16):
                    t0 = st["beat"] + (rep * 16 + k) * step
                    pulse(snd, slices[k], t0, t0 + step - 0.02, buff=0.02)
        self.play(FadeOut(timeline), FadeOut(slices), FadeOut(sl))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row forty of the ledger: {say(v['seconds'])} seconds; the measurements are when the voice enters, and how the "
            "beat was cut."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"AABA gave way to verse--chorus; \ loops became prominent alongside directional progressions",
            r"riffs and the backbeat; \ funk's one; \ four on the floor",
            r"prosody: \ stress on strong positions; \ hooks repeat",
            r"an 808 is a struck resonator and six square waves",
            r"sampling chops and re-sequences; \ flow is syllables on a grid",
            r"the drop and the sidechain; \ intros shrank from twenty seconds to five",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The thirty-two bar song gave way to verse and chorus, and loops became prominent alongside directional progressions. "
            "<bookmark mark='a'/> Riffs and the backbeat carry the music, from funk's one to four on the floor. "
            "<bookmark mark='b'/> Good prosody puts stresses on strong positions, and hooks repeat. <bookmark mark='c'/> An "
            "808 is a struck resonator and six square waves. <bookmark mark='d'/> Sampling chops and re-sequences, and flow "
            "is syllables on a grid. <bookmark mark='e'/> The drop and the sidechain make tension without chords; and the "
            "hit single's intro shrank from twenty seconds to five."
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
            r"For the kick model, \ how long until it falls 60 dB at a decay setting of 0.45 s?",
            r"Prove that a sidechain ducking D dB with release time $\tau$ is back within 1 dB after $\tau\ln{D}$ seconds.",
            r"\textbf{Ear.} \ The lab plays pads under a kick, \ some sidechained; \ say which, \ and how deep.",
            r"\textbf{Build.} \ Write a verse of your own on the sixteenth grid and measure its flow.",
            r"$\bigstar$ \ Do new platforms change how songs are written, \ or only which songs win?",
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
            (r"composing as search", [42]),
            (r"filters, \ dynamics and the compressor", [50]),
            (r"synthesis, \ and the workstation", [51]),
            (r"mastering and loudness", [57]),
            (r"the business of music", [60]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In composing as search. In filters, dynamics and the compressor. In synthesis and "
            "the workstation. In mastering and loudness. And in the business of music."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"songwriters", r"put the hook early, \ and test the words by speaking them over the beat"),
            (r"producers", r"program drums on a sixteen-step grid, \ and sidechain the pads"),
            (r"rappers", r"write to the beat, \ syllable by syllable"),
            (r"labels", r"clear every sample, \ or replay it"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Songwriters put the hook early, and test the words by speaking them over the beat. Producers "
            "program drums on a sixteen-step grid and sidechain the pads. Rappers write to the beat, syllable by syllable. "
            "Rights checks distinguish recordings from compositions; replaying avoids using the original recording but does not automatically remove composition rights."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. Temperley, \ \textit{The Musical Language of Rock} \ (2018)",
             r"M. Ohriner, \ \textit{Flow: \ The Rhythmic Voice in Rap Music} \ (2019)",
             r"A. Krims, \ \textit{Rap Music and the Poetics of Identity} \ (2000)",
             r"J. Covach and A. Flory, \ \textit{What's That Sound?} \ (5th ed. 2018)"],
            [r"M. Mauch and others, \ `The evolution of popular music: \ USA 1960--2010' \ (2015)",
             r"J. Serr\`a and others, \ `Measuring the evolution of contemporary western popular music' \ (2012)",
             r"H. L\'eveill\'e Gauvin, \ `Drawing listener attention in popular music' \ (2018)",
             r"K. Jakubowski and others, \ `Dissecting an earworm' \ (2017)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"how do you choose which instrument plays which note?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VII: \ the craft", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Act VI has heard many musics; \ Act VII turns to making music.", font_size=24, color=WHITE).move_to(UP * 1.7)
        lead.scale_to_fit_width(min(lead.width, 12.5))
        nxt = VGroup(label(r"Part 41", font_size=32, color=GREY_B), label(r"Orchestration", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Act VI has heard many musics; Act VII turns to making music. <bookmark mark='a'/> How do you choose which "
            "instrument plays which note? <bookmark mark='b'/> Next time. Part 41: Orchestration."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
