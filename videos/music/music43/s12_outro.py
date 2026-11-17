from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403
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
        c = clip("tune.variation43")
        head = VGroup(label(r"Variation 43", font_size=48, color=TUNE), label(r"the Tune, \ performed", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        tot = max(d["performed_s"], d["written_s"])
        a = perf_roll(d["deadpan"], width=11.4, height=1.1, lo=58, hi=71, total=tot, color=GREY_B)
        b = perf_roll(d["performed"], width=11.4, height=1.1, lo=58, hi=71, total=tot, vel=True)
        g = VGroup(VGroup(label(r"as written", font_size=17, color=GREY_B), a).arrange(DOWN, buff=0.08, aligned_edge=LEFT),
                   VGroup(label(r"performed", font_size=17, color=TUNE), b).arrange(DOWN, buff=0.08, aligned_edge=LEFT)).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        diff = value_bars(d["stretch"], width=11.4, height=0.9, base=1.0, scale=2.5).next_to(g, DOWN, buff=0.35)
        dl = label(r"each note's length, \ performed against written", font_size=15, color=GREY_A).next_to(diff, DOWN, buff=0.12)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, the whole Tune, "
            "first exactly as written, then performed by this part's five rules: the same notes, with the differences drawn "
            "below. You will hear the written version first."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(diff), FadeIn(dl))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Variation 43", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            flash(snd, a.notes, [st["written"] + p["t"] for p in d["deadpan"]], hot=WHITE, base=GREY_B)
            flash(snd, b.notes, [st["performed"] + p["t"] for p in d["performed"]], hot=WHITE, base=TUNE)
            cursor(snd, a, st["written"], 1.0, color=WHITE)
            cursor(snd, b, st["performed"], 1.0, color=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-three of the ledger. The measurement is the performance itself: phrase ends up to "
            f"{say(100 * (d['max_stretch_mid'] - 1))} per cent longer than written, the last note "
            f"{say(100 * (d['last_stretch'] - 1))} per cent, and the whole Tune {say(d['written_s'], 1)} seconds as written "
            f"and {say(d['performed_s'], 1)} performed."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a performance is the score plus deviations, \ measurable note by note",
            r"rules capture the common part: \ arches, \ contrast, \ punctuation",
            r"a final ritardando slows like a body braking",
            r"vibrato is heard at its mean pitch",
            r"players stay together by correcting a fraction of each asynchrony, \ between 0 and 2",
            r"normalized timing supports identification; \ corroborating evidence matters",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A performance is the score plus deviations, measurable note by note. <bookmark mark='a'/> Rules capture the common part: arches, contrast, punctuation. <bookmark mark='b'/> A final ritardando slows like a body braking. <bookmark mark='c'/> Vibrato is heard at its average pitch. <bookmark mark='d'/> Players stay together by correcting a fraction of each asynchrony, and this duo model is stable when total correction lies between zero and two; quartet stability depends on its interaction matrix. <bookmark mark='e'/> And normalized timing can support recording identification, but requires corroboration rather than a universal copy threshold."
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
            r"A ritardando falls to half tempo with q = 2. \ At what point of it is the tempo 0.8?",
            r"Prove that a duo's asynchrony has variance $2\sigma_T^2/(1-b^2) + 4\sigma_M^2/(1+b)$, \ b = 1 $-$ $\alpha_1$ $-$ $\alpha_2$.",
            r"\textbf{Ear.} \ The lab plays duos with random corrections; \ say which drift, \ which hold, \ which shake.",
            r"\textbf{Build.} \ Write a rule of your own \ (for example `faster uphill') \ and hear it on the Tune.",
            r"$\bigstar$ \ Is an interpretation a measurable object?",
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
            (r"music for picture: \ playing to a click and to a film", [44]),
            (r"expectation and emotion", [46]),
            (r"MIDI and the workstation: \ performance as data", [53]),
            (r"beat tracking and transcription", [61, 62]),
            (r"generative audio", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In music for picture, where players perform to a click and a film. In expectation "
            "and emotion. In MIDI and the workstation, where performance is data. In beat tracking and transcription. And in "
            "generative audio."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"performers", r"record themselves and look at the timing, \ not only listen"),
            (r"producers", r"`humanise' sequenced parts with timing and velocity variation"),
            (r"chamber groups", r"decide who leads each passage, \ and rehearse the hand-offs"),
            (r"teachers", r"space practice, \ interleave, \ and protect students' hands and ears"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Performers record themselves and look at the timing, not only listen. Producers humanise "
            "sequenced parts with small variations of timing and velocity. Chamber groups decide who leads each passage and "
            "rehearse the hand-offs. And teachers space practice, interleave it, and protect their students' hands and ears."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"C. E. Seashore, \ \textit{Psychology of Music} \ (1938)",
             r"A. Gabrielsson, \ `Music performance research at the millennium' \ (2003)",
             r"A. Williamon \ (ed.), \ \textit{Musical Excellence} \ (2004)",
             r"N. Cook, \ \textit{Beyond the Score} \ (2013)"],
            [r"A. Friberg, \ R. Bresin and J. Sundberg, \ `Overview of the KTH rule system' \ (2006)",
             r"A. Friberg and J. Sundberg, \ `Does music performance allude to locomotion?' \ (1999)",
             r"A. M. Wing and others, \ `Optimal feedback correction in string quartet synchronization' \ (2014)",
             r"B. H. Repp, \ `Diversity and commonality in music performance' \ (1992)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what does music do when it has a picture to serve?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VII: \ the craft", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Our performers played for listeners who only listened.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 44", font_size=32, color=GREY_B), label(r"Music for Picture and Play", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Our performers played for listeners who only listened. <bookmark mark='a'/> What does music do when it has a "
            "picture to serve, or a player to follow? <bookmark mark='b'/> Next time. Part 44: Music for Picture and Play."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        play_signoff(self, 43, clip("bridge.signoff"), clear=(top,))
        self.clear_scene()
