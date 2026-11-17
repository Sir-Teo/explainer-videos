from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403
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
        c = clip("tune.variation24")
        vs = d["voices"]
        head = VGroup(label(r"Variation 24", font_size=48, color=TUNE), label(r"the Tune, \ as a point of imitation", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g = voices_roll(vs, width=11.4, height=3.6, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.12).move_to(DOWN * 0.4)
        tags = VGroup()
        for k, (name, base, t0) in enumerate(d["entries"]):
            j = ["soprano", "alto", "tenor", "bass"].index(name)
            tags.add(label(rf"{k + 1}", font_size=22, color=WHITE).next_to(g.parts[j].notes[0], UP, buff=0.1))
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built the habits of "
            "sixteenth-century polyphony. <bookmark mark='a'/> So the Tune's first phrase becomes a point of imitation: "
            "the soprano begins, the tenor enters four beats later an octave below, the alto at the fifth, then the bass, "
            "and as each voice finishes the phrase it continues in free counterpoint, found by Part 20's search, "
            "consonant on every beat once all four have entered."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"Variation 24", detail=r"four synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash(snd, list(tags), [e[2] * d["unit"] for e in d["entries"]], hot=TUNE, base=WHITE, fade=0.8)
            cursor(snd, g, 0.0, d["unit"])
        self.play(FadeOut(g), FadeOut(tags))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-four of the ledger. {say(v['seconds'])} seconds. The measurement: after the last entry, "
            f"{say(d['beats'] - d['dissonant_beats'])} of {say(d['beats'])} beats consonant above the bass. The Tune, "
            "which was a melody with chords, is now four equal melodies."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        t = load("thirds")["census"]
        dz = load("dissonance")["groups"]
        st = load("style")
        im = load("imitation")
        names = list(dz)
        card = objectives_card([
            rf"thirds: \ in {100 * t['fourteenth century']['third']:.0f} in 100 sonorities of the 14th century, \ {100 * t['Palestrina']['third']:.0f} of Palestrina's",
            rf"imitation: \ {100 * im['share']:.0f} in 100 of Palestrina's movements open with a point",
            rf"dissonance: \ {100 * dz[names[0]]['shares']['free']:.1f} in 100 free in Palestrina; \ the rules are habits followed 97 times in 100",
            r"printing made Josquin a brand, \ and attribution a problem",
            rf"twelve numbers: \ {100 * st['books']['accuracy']:.0f} in 100 on Monteverdi's books, \ {100 * st['composer']['accuracy']:.0f} on an unfair comparison",
            rf"the second practice: \ free dissonance {100 * dz[names[1]]['shares']['free']:.0f}, \ {100 * dz[names[2]]['shares']['free']:.0f}, \ {100 * dz[names[3]]['shares']['free']:.0f} in 100",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The third became the sound of the century, and then a place to end. "
            "<bookmark mark='a'/> Equal voices built pieces from points of imitation. <bookmark mark='b'/> Palestrina's "
            "dissonance rules are real habits, unclassified by this simplified treatment detector about three times in a hundred. <bookmark mark='c'/> Printing made "
            "Josquin's name a brand, and his works a puzzle. <bookmark mark='d'/> A statistical test can tell styles "
            "apart, and is easily fooled by the wrong comparison. <bookmark mark='e'/> And Monteverdi's second practice "
            "is visible in the numbers, book by book, consistent with broader stylistic changes, without treating detector labels as a complete adjudication of Artusi’s critique."
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
            r"Zarlino's triad is 4:5:6. \ Compute its third and fifth in cents, \ and the error of each in 12 and in 31 equal steps.",
            r"Prove that two voices entering at the octave or the fifth keep the half steps of a mode in corresponding places, \ and that at the second they do not.",
            r"\textbf{Ear.} \ The lab plays ten cadences, \ some with prepared and some with struck dissonances. \ Sort them.",
            r"\textbf{Build.} \ Add three features to the stylometric test, \ and measure whether the accuracy on Monteverdi's books improves under leave-one-out.",
            r"$\bigstar$ \ Design an attribution test held out by source, \ and say what result would show it is recognizing scribes, \ not composers.",
        ], font_size=22)
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
            (r"the Baroque: \ figured bass, \ the second practice as the norm", [25]),
            (r"tuning: \ meantone and well temperament", [6, 25]),
            (r"the fugue's ancestry: \ imitation", [20]),
            (r"chromaticism, \ again", [27]),
            (r"style by statistics: \ computational musicology", [62, 67]),
            (r"text and music: \ the song", [40]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the Baroque, which makes the second practice its norm and the bass its "
            "foundation. In tuning, from meantone to well temperament. In the fugue, imitation's heir. In nineteenth-"
            "century chromaticism. In the statistics of style, in the parts on music research. And in the song, where the "
            "words come first again."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"choirs", r"tune thirds pure by ear: \ the 5:4 of Zarlino, \ not the piano's"),
            (r"composers", r"write points of imitation: \ a motive, \ entries at the octave and fifth, \ a cadence"),
            (r"editors", r"mark which accidentals are theirs"),
            (r"scholars", r"test attributions with fair comparisons and held-out sources"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Choirs can tune their thirds pure, as Zarlino's numbers say, rather than as a piano does. "
            "Composers still write points of imitation. Editors mark which accidentals are theirs. And scholars can "
            "test attributions fairly, with held-out sources."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. W. Atlas, \ \textit{Renaissance Music} \ (1998)",
             r"K. Jeppesen, \ \textit{The Style of Palestrina and the Dissonance} \ (1927); \ \textit{Counterpoint} \ (1931)",
             r"G. Zarlino, \ \textit{Le istitutioni harmoniche} \ (1558); \ N. Vicentino, \ \textit{L'antica musica} \ (1555)",
             r"C. V. Palisca, \ `The Artusi--Monteverdi controversy' \ (1968)"],
            [r"The Josquin Research Project \ (J. Rodin, \ C. S. Sapp and others), \ Stanford",
             r"M. S. Cuthbert and C. Ariza, \ `music21' \ (2010): \ the Palestrina and Monteverdi encodings",
             r"G. M. Artusi, \ \textit{L'Artusi, \ overo delle imperfettioni della moderna musica} \ (1600)",
             r"C. Monteverdi, \ preface to the fifth book \ (1605); \ G. C. Monteverdi, \ \textit{Dichiaratione} \ (1607)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 24, "Florence, 1589",
            "What happens to music when the words, and the bass, take charge?",
            "Monteverdi's second practice put the words in charge, and the old rules gave way. <bookmark mark='a'/> "
            "In Florence the lutenist Vincenzo Galilei, the astronomer's father, was hanging weights on strings to "
            "test an ancient story, and arguing for a new kind of song. Out of that argument came opera, the figured "
            "bass, and a new idea of key. <bookmark mark='b'/> Next time. Part 25: The Baroque.")
