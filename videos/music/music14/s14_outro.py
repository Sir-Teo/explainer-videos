from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403
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
        c = clip("tune.variation14")
        head = VGroup(label(r"Variation 14", font_size=48, color=TUNE), label(r"one phrase, \ eight ways", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        short = [r"as it is", r"neighbours", r"filled in", r"turns", r"upside down", r"backwards", r"expected", r"least expected"]
        chips = VGroup(*[label(nm, font_size=20, color=GREY_B) for nm in short]).arrange(RIGHT, buff=0.34).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "ways to change a melody, and a model that expects. And changing this particular melody "
            "has a history: around 1781 Mozart wrote twelve variations for piano on Ah, vous dirai-je, "
            "maman, and his first one does what our third version does: it fills the tune with running "
            "notes. <bookmark mark='a'/> So here is the "
            "Tune's first phrase, and then that phrase decorated three ways: with neighbour notes, with "
            "its leap filled in by a run, and with turns. Then upside down, and backwards. And then the "
            "model takes over: the seven notes it most expects to follow the first phrase, and the "
            "seven it expects least. Above each version is its surprise, in bits per note."
        ) as vo:
            first = d["phrases"][0]
            pre = roll(first["pitches"], first["beats"], width=10.0, height=2.6, lo=-3, hi=20, lines=(0, 12), color=TUNE).move_to(UP * 0.1)
            moz = VGroup(label(r"W. A. Mozart, \ \textit{Twelve Variations on ``Ah, vous dirai-je, maman''}, \ K. 265", font_size=26, color=WHITE),
                         label(r"Vienna, \ about 1781", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.12).move_to(DOWN * 1.9)
            self.play(FadeIn(head), FadeIn(pre))
            self.wait(5.0)
            self.play(FadeIn(moz))
            vo.wait_until("a")
            self.play(FadeOut(moz), LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.6), run_time=14.0)
            self.play(FadeOut(pre), run_time=0.4)
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 14", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, ph in enumerate(d["phrases"]):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(*shown)
                name = label(ph["name"], font_size=40, color=TUNE).move_to(UP * 2.1)
                r = roll(ph["pitches"], ph["beats"], width=10.0, height=2.6, lo=-3, hi=20, lines=(0, 12), color=CHANCE_C if k >= 6 else TUNE).move_to(UP * 0.1)
                bits = label(rf"{ph['bits']:.1f} bits a note", font_size=30, color=EAR).move_to(DOWN * 1.75)
                shown = [name, r, bits]
                self.add(name, r, bits)
                pulse(snd, chips[k], ph["t0"], ph["t0"] + ph["seconds"], buff=0.06)
                sing(snd, r, [t - 0.0 for t in ph["times"]], hot=WHITE, base=CHANCE_C if k >= 6 else TUNE)
        self.remove(*shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row fourteen of the ledger. {say(v['seconds'])} seconds. The measurement: the continuation "
            f"the model expected costs {say(d['bits_most'], 1)} bits a note, and is a little dull. The one "
            f"it expected least costs {say(d['bits_least'], 1)}, and is nonsense. The Tune itself, at "
            f"{say(d['bits_plain'], 1)}, sits between them, where tunes live."
        ):
            self.play(FadeOut(chips), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a melody is first a contour; \ the intervals come second",
            r"half of all moves are steps; \ a tune fits in an octave, \ and lives near its middle",
            r"phrases are arches, \ a breath long, \ ending lower than they began",
            r"leaps turn back by regression to the mean: \ shuffled notes do it more",
            r"left over for the composer: \ tendency tones, \ repetition, \ question and answer",
            r"a note carries about two and a half bits; \ a counting model is surprised by the Tune's one leap",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A melody is first a contour, and listeners keep the contour before the "
            "intervals. <bookmark mark='a'/> Half of all moves are steps; a tune fits in an octave and "
            "lives near its middle. <bookmark mark='b'/> Phrases are arches, a breath long, and they end "
            "lower than they began. <bookmark mark='c'/> Leaps turn back because of regression to the "
            "mean: shuffled notes do it more than real tunes. <bookmark mark='d'/> What is left over for "
            "the composer is tendency tones, repetition, and phrases that ask and answer. "
            "<bookmark mark='e'/> And a note carries about two and a half bits of news; a model that "
            "only counts is surprised by the Tune exactly once, at its leap."
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
            r"Write the first two phrases of \textit{Happy Birthday} as scale degrees. \ Give every move in semitones, \ the share that are steps, \ the range, \ "
            r"and the shape of each phrase (first note, \ middle, \ last).",
            r"Notes are drawn independently and uniformly from $1, 2, \dots, n$. \ Given that a leap has just gone \textit{up} and landed on $k$, \ "
            r"what is the chance that the next note is lower? \ Average over where upward leaps land, \ and explain the leap rule.",
            r"\textbf{Ear.} \ The lab plays eight melodies: \ some are from the corpus, \ some have the same notes shuffled, \ some were made by the model. \ Say which is which.",
            r"\textbf{Build.} \ With \texttt{melody.NGram}, \ train on every tune but one and plot that tune's surprise. \ Which note of \textit{Frère Jacques} surprises the model most? \ "
            r"Then let the model also see rhythm, \ and see whether phrase endings get cheaper.",
            r"$\bigstar$ \ Among melodies of equal average surprise, \ which are remembered after one hearing? \ Propose a measurement that needs no listeners' opinions of quality.",
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
            (r"tendency tones become a key, \ with a home", [15]),
            (r"two melodies at once: \ counterpoint", [16, 20]),
            (r"motive and sequence become form", [21]),
            (r"raga and maqam: \ melody as the whole of the art", [34, 35]),
            (r"expectation and emotion", [46]),
            (r"machines that predict, \ and compose", [65]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once: the next part turns tendency tones into a key, with a "
            "home. Then two melodies at once, which is counterpoint. Motive and sequence grow into form. "
            "In raga and maqam, melody is the whole of the art. Expectation returns as a theory of "
            "musical emotion. And the counting model of this part is the ancestor of the machines that "
            "compose."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"songwriters", r"keep a tune within an octave, \ save the top note for the chorus, \ and say the hook twice"),
            (r"teachers", r"start children on three notes and steps, \ and add leaps later"),
            (r"lyricists", r"set strong syllables on strong beats, \ and in a tone language follow the tones"),
            (r"analysts", r"before calling something a composer's habit, \ shuffle the notes and count again"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A songwriter keeps a tune within an octave, saves the top note for the "
            "chorus, and says the hook twice. A teacher starts children on three notes and steps. A "
            "lyricist puts strong syllables on strong beats, and in a tone language follows the tones. "
            "And an analyst, before calling anything a composer's habit, shuffles the notes and counts "
            "again."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. Huron, \ \textit{Sweet Anticipation: Music and the Psychology of Expectation} \ (2006)",
             r"D. Temperley, \ \textit{Music and Probability} \ (2007)",
             r"L. B. Meyer, \ \textit{Emotion and Meaning in Music} \ (1956)",
             r"A. S. Bregman, \ \textit{Auditory Scene Analysis} \ (1990)"],
            [r"P. von Hippel and D. Huron, \ ``Why do skips precede reversals? The effect of tessitura on melodic structure'', \ \textit{Music Perception} 18 (2000)",
             r"D. Huron, \ ``The melodic arch in Western folksongs'', \ \textit{Computing in Musicology} 10 (1996)",
             r"W. J. Dowling, \ ``Scale and contour: two components of a theory of memory for melodies'', \ \textit{Psychological Review} 85 (1978)",
             r"D. Deutsch, \ ``Octave generalization and tune recognition'', \ \textit{Perception \& Psychophysics} 11 (1972)",
             r"M. T. Pearce, \ ``Statistical learning and probabilistic prediction in music cognition'', \ \textit{Annals of the New York Academy of Sciences} 1423 (2018)",
             r"P. C. M. Wong and R. L. Diehl, \ ``How can the lyrics of a song in a tone language be understood?'', \ \textit{Psychology of Music} 30 (2002)",
             r"B. P. Gold et al., \ ``Predictability and uncertainty in the pleasure of music'', \ \textit{Journal of Neuroscience} 39 (2019)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        t = load("hook")["tune"]
        r = roll(t["pitches"][7:14], t["beats"][7:14], width=6.0, height=1.8, lo=-2, hi=7, lines=(0,), color=TUNE).move_to(UP * 1.3)
        home = label(r"home", font_size=26, color=EAR).next_to(r.notes[-1], DOWN, buff=0.25)
        q = label(r"every tune has a home note. \ What makes it home, \ and can a tune move house?", font_size=30, color=EAR).move_to(DOWN * 0.6)
        nxt = VGroup(label(r"Part 15", font_size=32, color=GREY_B), label(r"Key", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One thing has been in every chapter without being explained. Ninety-six tunes in a hundred "
            "end on the same degree of the scale. <bookmark mark='a'/> Notes lean toward it. Phrases ask "
            "questions that only it can answer. Every tune has a home note. What makes one note out of "
            "seven the home, how does a listener find it within a few seconds, and can a piece of music "
            "leave home and come back? <bookmark mark='b'/> Next time. Part 15: Key."
        ) as vo:
            self.play(FadeIn(r))
            vo.wait_until("a")
            self.play(FadeIn(home), r.notes[-1].animate.set_fill(EAR), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
