from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403
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
        c = clip("tune.variation12")
        head = VGroup(label(r"Variation 12", font_size=48, color=TUNE), label(r"one tune, \ ten scales", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        chips = VGroup(*[label(nm, font_size=20, color=GREY_B) for nm in d["names"]]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.0)
        kb = keyboard(-5, 19, width=10.0, height=1.7).move_to(DOWN * 0.9)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "scales. <bookmark mark='a'/> So here is the Tune with each phrase in a different mode, from "
            "the brightest to the darkest but one; and then its first phrase four more times: in the "
            "darkest mode, and in scales of five, six and eight notes. A second voice below the melody "
            "fills in the notes the Tune leaves out, and a held C says where home is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kb))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.15), run_time=3.0)
        ev = c.events
        shown = None
        i = 0
        with self.listen(c) as snd:
            window(snd, r"Variation 12", detail=r"Part 7's piano, \ two voices over a held C", corner=DL, tag_corner=DR)
            for k, ph in enumerate(d["phrases"]):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(*shown)
                name = label(ph["name"], font_size=44, color=TUNE).move_to(LEFT * 3.2 + UP * 1.6)
                clock = twelve(ph["notes"], radius=1.0, color=TUNE, font_size=15, dot=0.08).move_to(RIGHT * 3.0 + UP * 1.5)
                shown = [name, clock]
                self.add(name, clock)
                pulse(snd, chips[k], ph["t0"], ph["t0"] + ph["seconds"], buff=0.06)
                n = len(ph["melody"])
                ts = [ev[f"n{i + j}"] for j in range(n)]
                play_keys(snd, kb, ph["melody"] + ph["under"], ts + ts, hold=0.45)
                flash(snd, [clock.dots[m % 12] for m in ph["melody"]], ts, base=TUNE, hot=WHITE, fade=0.2)
                i += n
        kb.clear()
        self.remove(*shown, kb)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twelve of the ledger. {say(v['seconds'])} seconds. The measurement: from the brightest "
            f"mode to the darkest, {say(d['lowered'])} notes fall by a semitone, one at a time, and the "
            "Tune goes from a nursery to somewhere much less safe."
        ):
            self.play(FadeOut(chips), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        g, e, f = load("gaps"), load("every"), load("frontier")
        card = objectives_card([
            r"stacked fifths leave steps of two sizes at 5, \ 7 and 12 notes: \ the three-gap theorem",
            r"seven modes, \ bright to dark, \ each the last with one note lowered",
            r"the white keys are maximally even; \ their intervals come in two sizes; \ they are deep: \ 2, 5, 4, 3, 6, 1",
            r"minor borrows a leading note; \ whole-tone and octatonic scales have 2 and 3 versions",
            r"six fillings of a fourth; \ $2 \times 6 \times 6 = 72$ parent scales",
            rf"{e['total']} shapes of scale on twelve notes; \ of the 66 with seven, \ ours is the most even and the smoothest",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Stack fifths, and the steps come in two sizes at five, seven and twelve "
            "notes; a theorem says why. <bookmark mark='a'/> Seven notes give seven modes, in order of "
            "brightness, each the one before with a single note lowered. <bookmark mark='b'/> The white "
            "keys are as even as seven notes among twelve can be; every interval in them comes in two "
            "sizes; and they are deep. <bookmark mark='c'/> The minor scale borrows a leading note, and "
            "scales that map onto themselves have no home. <bookmark mark='d'/> A fourth can be filled "
            "six ways, and south Indian theory builds seventy-two parent scales from that. "
            "<bookmark mark='e'/> And of the three hundred and fifty-two shapes a scale can have on "
            "twelve notes, the one on every keyboard is the most even and the smoothest of its size."
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
            r"A pure fifth is 702 cents. \ Stack five of them from C and fold them into one octave. \ Name the five notes, \ give the steps between them in cents, \ "
            r"and say which interval of the major scale is missing from this scale altogether.",
            r"Use Burnside's lemma to count the shapes of scale on six notes to the octave \ (necklaces of six beads in two colours), \ and list them. \ "
            r"Which of them maps onto itself when turned?",
            r"\textbf{Ear.} \ The lab plays eight scales on C in a random order, \ each one of the seven modes. \ Name each, \ or at least say whether it is brighter or darker than the one before.",
            r"\textbf{Build.} \ With \texttt{scales.stack}, \ use a generator other than the pure fifth: \ a fifth of 697 cents (meantone) and one of 709. \ "
            r"At which numbers of notes do the steps come in two sizes now?",
            r"$\bigstar$ \ On nineteen equal notes to the octave, \ which seven are maximally even? \ Is that scale deep, \ and does it have a landmark interval? \ "
            r"What would its ``black keys'' be?",
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
            (r"intervals and chords, \ built from the scale", [13]),
            (r"how melodies move through a scale", [14]),
            (r"keys, \ and moving between them by one note", [15]),
            (r"the mathematics of evenness and necklaces", [33]),
            (r"raga, \ maqam, \ slendro and pelog, \ on their own terms", [34, 35, 36]),
            (r"blue notes, \ and scales that are bent", [38]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once: the next part builds intervals and chords out of the "
            "scale, and the one after asks how melodies move through it. The deep-scale property becomes "
            "the system of keys. Evenness and necklaces return as mathematics. The scales of India, the "
            "Arab world and Java each get a part of their own. And the blues scale comes back with the "
            "notes that no scale on a keyboard can hold."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"improvisers", r"learn each mode as a colour over a chord: \ Dorian over minor, \ Mixolydian over a dominant, \ Lydian for brightness"),
            (r"film composers", r"reach for Lydian for wonder, \ Phrygian for menace, \ whole-tone for a dream: \ one changed note each"),
            (r"songwriters", r"write whole songs on the five black keys, \ where no two notes can clash"),
            (r"instrument makers", r"choose which notes to leave out: \ a harmonica, \ a kalimba and a steel tongue drum are scales made solid"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. An improviser learns each mode as a colour to play over a chord. A film "
            "composer reaches for Lydian when the scene needs wonder and Phrygian when it needs menace, "
            "and the difference is one note. A songwriter can write a whole song on the five black keys, "
            "where nothing clashes. And an instrument maker decides which notes to leave out: a "
            "harmonica or a kalimba is a scale made solid."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. Tymoczko, \ \textit{A Geometry of Music} \ (2011), \ ch. 4",
             r"W. A. Sethares, \ \textit{Tuning, Timbre, Spectrum, Scale} \ (2nd ed., 2005)",
             r"H. Powers et al., \ ``Mode'', \ \textit{The New Grove Dictionary of Music and Musicians} \ (2001)",
             r"O. Messiaen, \ \textit{Technique de mon langage musical} \ (1944)"],
            [r"N. Carey and D. Clampitt, \ ``Aspects of well-formed scales'', \ \textit{Music Theory Spectrum} 11 (1989)",
             r"J. Clough and J. Douthett, \ ``Maximally even sets'', \ \textit{Journal of Music Theory} 35 (1991)",
             r"J. Clough and G. Myerson, \ ``Variety and multiplicity in diatonic systems'', \ \textit{J. Music Theory} 29 (1985)",
             r"C. Gamer, \ ``Some combinational resources of equal-tempered systems'', \ \textit{J. Music Theory} 11 (1967)",
             r"V. T. S\'os, \ ``On the distribution mod 1 of the sequence $n\alpha$'', \ \textit{Ann. Univ. Sci. Budapest} 1 (1958)",
             r"S. E. Trehub, E. G. Schellenberg and S. B. Kamenetsky, \ ``Infants' and adults' perception of scale structure'', \ \textit{JEP: HPP} 25 (1999)",
             r"K. Z. Gill and D. Purves, \ ``A biological rationale for musical scales'', \ \textit{PLoS ONE} 4 (2009)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        kb = keyboard(0, 12, width=7.0, height=1.8, lit=(0, 4, 7)).move_to(UP * 1.2)
        q = label(r"three notes of a scale, \ sounded together. \ Why these three?", font_size=32, color=EAR).move_to(DOWN * 0.6)
        nxt = VGroup(label(r"Part 13", font_size=32, color=GREY_B), label(r"Intervals and Chords", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We have chosen our notes. So far we have played them one at a time. The next question is "
            "what happens when notes of a scale sound together. <bookmark mark='a'/> Take every other "
            "note of the scale, three of them, and you have a chord that half the world's songs are "
            "built on. Why that spacing, and how many chords does a scale contain? "
            "<bookmark mark='b'/> Next time. Part 13: Intervals and Chords."
        ) as vo:
            self.play(FadeIn(kb))
            vo.wait_until("a")
            self.play(FadeIn(q), *[Indicate(kb.key[n], color=GOLD) for n in (0, 4, 7)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
