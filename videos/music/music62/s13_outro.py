from __future__ import annotations

from videos.music.music62.common import *  # noqa: F403
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
        d = load("follow")
        c = clip("tune.variation62")
        st = d["starts"]
        keys = d["names"]
        names = {"stiff": (r"chords on the written beats", GREY_B), "follow": (r"chords placed by the follower", TUNE)}
        head = VGroup(label(r"Variation 62", font_size=48, color=TUNE), label(r"accompanied by a listener", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=4.6, height=1.2, corner_radius=0.12, stroke_color=names[k][1]),
                                label(names[k][0], font_size=18, color=names[k][1])).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        note = label(r"Part 8's voice sings the Tune freely; \ the piano either ignores it or listens", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here Part 8's voice "
            "sings it freely, with rubato, and a piano accompanies twice: first playing its chords on the written beats, deaf "
            "to the singer; then placing each chord where the follower hears the singer has got to."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 62", kind="physical model", detail=r"Part 8's voice, \ Part 38's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("follow")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Row sixty-two of the ledger. The deaf piano drifts away from the singer as the rubato grows. The follower stays "
            f"with them, a median {say(d['median_ms'])} milliseconds behind: close enough to sound like accompaniment, late "
            "enough to sound like a careful one."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"novelty curves show where things begin; \ autocorrelation shows how often",
            r"a prior near 120 picks the tempo's level, \ and sometimes the wrong one",
            r"dynamic programming tracks beats; \ rubato defeats a fixed period",
            r"chroma folds octaves; \ an HMM with Bach's transitions hears chords in context",
            r"time warping aligns performances, \ offline and live",
            r"repetition finds form where novelty cannot; \ annotators set the ceiling",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Novelty curves show where things begin, and autocorrelation how often. <bookmark mark='a'/> A "
            "prior near a hundred and twenty picks the tempo's level, and sometimes the wrong one. <bookmark mark='b'/> Dynamic "
            "programming tracks beats, and rubato defeats a fixed period. <bookmark mark='c'/> Chroma folds the octaves, and an "
            "HMM with Bach's transitions hears chords in context. <bookmark mark='d'/> Time warping aligns performances, offline "
            "and live. <bookmark mark='e'/> And repetition finds a song's form where novelty cannot, while annotators set the "
            "ceiling for all of it."
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
            r"A tracker's beats are each 50 ms late. \ Within a 70 ms tolerance, \ what is its F-measure? \ And if they are 80 ms late?",
            r"Show that the Viterbi recursion finds the most likely state sequence of an HMM, \ by induction on the frame.",
            r"\textbf{Ear.} \ The lab plays the session with clicks shifted by random amounts; \ which are late? \ Find your threshold.",
            r"\textbf{Build.} \ Add a tempo that drifts to the beat tracker: \ let the period itself be a hidden state.",
            r"$\bigstar$ \ How close to a human accompanist can a predictive follower play, \ and where does it fail?",
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
            (r"finding music: \ beat-matched playlists and fingerprints", [63]),
            (r"source separation: \ beats and chords as guides", [64]),
            (r"machines that compose: \ bars, \ chords and form as structure", [65]),
            (r"research: \ annotators and their disagreements", [67]),
            (r"the concert: \ an accompanist that listens", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In finding music, with beat-matched playlists and fingerprints. In source separation, "
            "where beats and chords guide the separator. In machines that compose, which need bars, chords and form. In "
            "research, with annotators and their disagreements. And in the concert at the end of the series."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"tempo", r"report it with its octave in doubt; \ check by tapping"),
            (r"beats", r"F within 70 ms, \ and at any sensible level"),
            (r"chords", r"a prior suited to the music, \ not to Bach by default"),
            (r"structure", r"repetition and novelty together; \ two annotators if you can"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Report a tempo with its octave in doubt, and check by tapping. Score beats within seventy "
            "milliseconds, at the right level and at any sensible one. Give a chord recognizer a prior suited to the music, not "
            "Bach by default. And find structure with repetition and novelty together, against two annotators if you can."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"M. Müller, \ \textit{Fundamentals of Music Processing} \ (2nd ed., \ 2021)",
             r"A. Lerch, \ \textit{An Introduction to Audio Content Analysis} \ (2nd ed., \ 2022)",
             r"R. B. Dannenberg and C. Raphael, \ `Music score alignment and computer accompaniment' \ (CACM, \ 2006)",
             r"J. B. L. Smith et al., \ `Design and creation of a large-scale database of structural annotations' \ (ISMIR, \ 2011)"],
            [r"D. P. W. Ellis, \ `Beat tracking by dynamic programming' \ (J. New Music Research, \ 2007)",
             r"J. Foote, \ `Automatic audio segmentation using a measure of audio novelty' \ (ICME, \ 2000)",
             r"S. Dixon, \ `Live tracking of musical performances using on-line time warping' \ (DAFx, \ 2005)",
             r"B. McFee and D. P. W. Ellis, \ `Analyzing song structure with spectral clustering' \ (ISMIR, \ 2014)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act XI: \ listening machines", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"2002: \ in London you could dial four digits, \ hold your phone up in a noisy bar, \ and get the song's name by text.", font_size=23, color=WHITE).move_to(UP * 1.7)
        q = label(r"how do ten bad seconds find one song among millions, \ and what decides what we hear next?", font_size=27, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 63", font_size=32, color=GREY_B), label(r"Finding Music", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "2002: in London you could dial four digits, hold your phone up in a noisy bar, and get the song's name back by "
            "text message. <bookmark mark='a'/> How do ten bad seconds find one song among millions, and what decides what we "
            "hear next? <bookmark mark='b'/> Next time. Part 63: Finding Music."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
