from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403
from videos.music.variations import rows_before

ROMAN = {1: "I", 4: "IV", 5: "V"}


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
        c = clip("tune.variation13")
        head = VGroup(label(r"Variation 13", font_size=48, color=TUNE), label(r"one tune, \ one set of chords, \ six voicings", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        chips = VGroup(*[label(nm, font_size=19, color=GREY_B) for nm in d["names"]]).arrange(RIGHT, buff=0.32).to_edge(DOWN, buff=1.0)
        kb = keys(36, 84, width=12.4, height=1.6).move_to(DOWN * 1.1)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "chords. <bookmark mark='a'/> So here is the Tune with a chord under every two beats, only "
            "ever one, four or five, and each phrase voiced a different way. Block triads in root "
            "position. The same kind of chords, re-voiced so that the hand hardly moves. Spread wide, "
            "the way the harmonic series is spaced. Sevenths, as shells. Then close chords over a bass, "
            "and a full close. The melody is gold; the chords are blue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kb))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.5), run_time=14.0)
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 13", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            mel_t = [n["t"] for ph in d["phrases"] for n in ph["melody"]]
            mel_m = [n["midi"] for ph in d["phrases"] for n in ph["melody"]]
            ch_t = [ch["t"] for ph in d["phrases"] for ch in ph["chords"]]
            ch_m = [ch["midis"] for ph in d["phrases"] for ch in ph["chords"]]

            def fn(_, t):
                kb.clear()
                for m, a, b in zip(ch_m, ch_t, ch_t[1:] + [c.duration]):
                    if a <= t < b:
                        for x in m:
                            kb.on(x, BLUE)
                for m, a, b in zip(mel_m, mel_t, mel_t[1:] + [c.duration]):
                    if a <= t < b:
                        kb.on(m, GOLD)

            snd.drive(kb.key[min(kb.key)], fn)
            for k, ph in enumerate(d["phrases"]):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(*shown)
                name = label(ph["name"], font_size=40, color=TUNE).move_to(UP * 2.0)
                cells = VGroup(*[VGroup(label(ROMAN[ch["degree"]], font_size=34, color=WHITE),
                                        label(r", \ ".join(tex(n[:-1].replace("b", "♭").replace("#", "♯")) for n in ch["names"]), font_size=22, color=BLUE)).arrange(DOWN, buff=0.12)
                                 for ch in ph["chords"]]).arrange(RIGHT, buff=0.9).move_to(UP * 0.75)
                shown = [name, cells]
                self.add(name, cells)
                pulse(snd, chips[k], ph["t0"], ph["t0"] + ph["seconds"], buff=0.06)
                flash(snd, [x[0] for x in cells], [ch["t"] for ch in ph["chords"]], hot=GOLD, base=WHITE, fade=0.5, hold=0.6)
        kb.clear()
        self.remove(*shown, kb)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirteen of the ledger. {say(v['seconds'])} seconds. The measurement: over the whole "
            f"Tune, block triads in root position make the three voices travel {say(d['block_motion'])} "
            f"semitones. Re-voiced, the same chords need {say(d['voiced_motion'])}. The notes are the "
            "same. Only the order from bottom to top has changed."
        ):
            self.play(FadeOut(chips), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        vo_ = load("voicing")
        card = objectives_card([
            r"an interval is a number and a quality; \ the quality is a direction on the line of fifths",
            r"three notes with no two adjacent: \ exactly the four triads; \ a scale holds 3 major, \ 3 minor, \ 1 diminished",
            r"Rameau: \ a chord has a root, \ in any inversion; \ the ear finds it as a missing fundamental",
            r"the dominant seventh carries the scale's one tritone, \ and the tritone resolves",
            r"voicing: \ thirds turn to mud in the bass; \ double the root; \ the fifth can go, \ the third cannot",
            r"four notations; \ and Euler's map, \ where neighbours share two notes",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? An interval has a number and a quality, and the quality is a direction "
            "on the line of fifths. <bookmark mark='a'/> Ask for three notes with no two of them "
            "adjacent, and you get exactly the four triads; a major scale holds three major, three "
            "minor and one diminished. <bookmark mark='b'/> Rameau was right that a chord has a root "
            "whichever way up it stands, and the ear finds that root the way it finds a missing "
            "fundamental. <bookmark mark='c'/> The dominant seventh carries the scale's one tritone, "
            "and the tritone resolves. <bookmark mark='d'/> A chord's voicing can matter more than its "
            "name: thirds turn to mud in the bass, the root is the note to double, the fifth can be "
            "left out and the third cannot. <bookmark mark='e'/> And chords can be written four ways, "
            "and laid out on a map where neighbours share two notes."
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
            r"Name each interval and its inversion: \ D up to F$\sharp$; \ E up to C; \ B up to F; \ A$\flat$ up to F$\sharp$. \ "
            r"How many steps apart are the two notes of each on the line of fifths?",
            r"Three notes divide the twelve-note circle into three steps that add up to twelve. \ Prove that if every step is at least three semitones, \ "
            r"the notes form a major, \ minor, \ diminished or augmented triad, \ and nothing else.",
            r"\textbf{Ear.} \ The lab plays ten triads. \ For each, \ say whether it is major, \ minor, \ diminished or augmented, \ and which of its notes is in the bass.",
            r"\textbf{Build.} \ With \texttt{chords.voicings} and \texttt{chords.spacing\_roughness}, \ find the smoothest five-voice spacing of a G seventh chord over the G at the bottom of the bass staff. \ "
            r"Which note does it double? \ And if one note may be left out?",
            r"$\bigstar$ \ The root model ties on the diminished triad and splits A, C, E, G almost evenly. \ Give the lowest note extra weight. \ "
            r"How much weight makes the model agree with the chord symbols in a songbook, \ and what does it then get wrong?",
        ], font_size=23)
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
            (r"melody: \ which notes of a tune are chord notes", [14]),
            (r"keys, \ and the pull of five to one", [15, 18]),
            (r"voice leading, \ in two parts and in four", [16, 17]),
            (r"the map of chords, \ as geometry", [32]),
            (r"jazz changes: \ shells, \ extensions and chord scales", [39]),
            (r"distortion; \ and machines that name chords", [50, 62]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once. The next part asks which notes of a melody belong to "
            "the chord beneath them. Then keys, and the pull of five to one. Then voice leading, first "
            "in two parts and then in four. Euler's map returns as geometry. Shells, extensions and "
            "chord scales are the working vocabulary of jazz. And the distorted power chord and the "
            "chord-naming machine each get a part of their own."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"pianists and guitarists", r"learn every chord in every inversion, \ and choose the one nearest the last"),
            (r"arrangers", r"keep thirds out of the bass, \ and space a chord as the harmonic series is spaced"),
            (r"session players", r"read charts in numbers, \ and play them in whatever key the singer needs"),
            (r"producers", r"thin a chord before distorting it: \ root and fifth survive, \ thirds do not"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A pianist or a guitarist learns every chord in every inversion, and then "
            "chooses whichever lies nearest the last. An arranger keeps thirds out of the bass. A "
            "session player reads a chart in numbers, and plays it in whatever key the singer needs. "
            "And a producer thins a chord before distorting it, because roots and fifths survive and "
            "thirds do not."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J.-P. Rameau, \ \textit{Trait\'e de l'harmonie} \ (1722; \ trans. P. Gossett, 1971)",
             r"R. Parncutt, \ \textit{Harmony: A Psychoacoustical Approach} \ (1989)",
             r"S. Laitz, \ \textit{The Complete Musician} \ (4th ed., 2015), \ chs. 1--6",
             r"D. Tymoczko, \ \textit{A Geometry of Music} \ (2011), \ chs. 2--3"],
            [r"R. Parncutt, \ ``Revision of Terhardt's psychoacoustical model of the root(s) of a musical chord'', \ \textit{Music Perception} 6 (1988)",
             r"L. Euler, \ \textit{Tentamen novae theoriae musicae} \ (1739)",
             r"R. Cohn, \ ``Neo-Riemannian operations, parsimonious trichords, and their Tonnetz representations'', \ \textit{J. Music Theory} 41 (1997)",
             r"P. Harrison and M. Pearce, \ ``Simultaneous consonance in music perception and composition'', \ \textit{Psychological Review} 127 (2020)",
             r"P. Johnson-Laird, O. Kang and Y. C. Leong, \ ``On musical dissonance'', \ \textit{Music Perception} 30 (2012)",
             r"H. V. Koops et al., \ ``Annotator subjectivity in harmony annotations of popular music'', \ \textit{J. New Music Research} 48 (2019)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        kb = keys(60, 84, width=8.0, height=1.6).move_to(UP * 1.3)
        q = label(r"a chord is notes at one moment. \ What makes a line of notes a tune?", font_size=32, color=EAR).move_to(DOWN * 0.5)
        nxt = VGroup(label(r"Part 14", font_size=32, color=GREY_B), label(r"Melody", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We have stacked notes on top of each other. But most of the music people carry in their "
            "heads is not a stack. It is a line: one note after another. <bookmark mark='a'/> Why do "
            "some lines of notes stick, so that you can sing them back after one hearing, while others "
            "fall apart? What makes a row of pitches a tune? <bookmark mark='b'/> Next time. Part 14: "
            "Melody."
        ) as vo:
            self.play(FadeIn(kb))
            for k, m in enumerate((60, 60, 67, 67, 69, 69, 67)):
                self.play(Indicate(kb.key[m - 60], color=GOLD, scale_factor=1.0), run_time=0.35)
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
