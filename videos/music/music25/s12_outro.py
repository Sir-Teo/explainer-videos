from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403
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
        c = clip("tune.variation25")
        head = VGroup(label(r"Variation 25", font_size=48, color=TUNE), label(r"the Tune, \ as an overture and a chaconne", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = voices_roll([d["overture"], d["overture_bass"]], width=5.4, height=2.8, colors=[TUNE, GREY_A], lo=34, hi=84, bar_h=0.11)
        g2 = voices_roll([d["chaconne"], d["ground"]], width=5.4, height=2.8, colors=[EAR, GREY_A], lo=34, hi=84, bar_h=0.11)
        cols = VGroup(VGroup(label(r"French overture: \ dotted, \ with a rushing upbeat", font_size=20, color=TUNE), g1).arrange(DOWN, buff=0.25),
                      VGroup(label(r"chaconne: \ a ground, \ the reprise ornamented", font_size=20, color=EAR), g2).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built the gestures of the "
            "Baroque. <bookmark mark='a'/> So the Tune becomes, first, the slow opening of a French overture, its long "
            "notes dotted and over-dotted, with a rushing scale before a strong note; and then a chaconne, a set of "
            "variations over a repeating bass, its melody heard plain and then again ornamented with trills and "
            "mordents."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"Variation 25", detail=r"Part 1's string on Part 7's soundboard", corner=DL, tag_corner=DR)
            flash_voices(snd, g1, [d["overture"], d["overture_bass"]], d["starts"]["overture"], d["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, g2, [d["chaconne"], d["ground"]], d["starts"]["chaconne"], d["unit"], colors=[EAR, GREY_A])
            pulse(snd, cols[0][0], d["starts"]["overture"], d["starts"]["chaconne"] - 0.5, buff=0.08)
            pulse(snd, cols[1][0], d["starts"]["chaconne"], c.duration, buff=0.08)
        self.play(FadeOut(cols))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-five of the ledger. {say(v['seconds'])} seconds. The measurement: a ground of eight bass notes "
            f"heard twice, and a reprise that adds {say(d['ornaments'])} ornament notes to the Tune's fourteen. A Baroque "
            "player would have added them without being asked."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        h = load("hook")
        co = load("corelli")
        k = load("keys")
        m = load("modes")
        pal = m["palestrina"]
        tagged = sum(pal[x] for x in ("dor", "mix", "ion", "aeo", "phr"))
        card = objectives_card([
            r"Galilei: \ the octave needs four times the weight; \ the numbers belong to the strings",
            r"monody, \ recitative and aria, \ opera: \ a top and a bottom",
            rf"the figured bass: \ a realizer recovers {100 * co['agreement']['pitch_classes']:.0f} in 100 of Corelli's notes, \ none of his melody",
            r"ritornello form found by a program, \ which misses a return in the minor",
            rf"Werckmeister III: \ C's third {k['werck_C']['third_error']:.0f} cents wide, \ F$\sharp$'s {k['werck_Fs']['third_error']:.0f}",
            rf"modes to keys: \ Ionian and Aeolian {100 * (pal['ion'] + pal['aeo']) / tagged:.0f} in 100 in Palestrina; \ all of Bach's chorales",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Galilei's weights broke an ancient legend, and with it an unreliable numerical legend, without removing mathematics from musical acoustics. <bookmark mark='a'/> Monody put one voice on top of a bass, and opera grew from it. <bookmark mark='b'/> The figured bass holds most of the harmony and leaves the melodic realization underdetermined. <bookmark mark='c'/> Ritornello form is returns, which a program can find, if it allows for mode. <bookmark mark='d'/> Well temperament gave keys real colours. <bookmark mark='e'/> And eight modes became two keys, between Palestrina and Bach."
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
            r"A string sounds 196 Hz under 4 kg. \ What weight makes it sound 294 Hz, \ a fifth higher? \ And what did the legend predict?",
            r"Show that a quarter-comma meantone fifth is $1200\log_2(5)/4 \approx 696.6$ cents, \ and that four of them, \ less two octaves, \ make a pure third.",
            r"\textbf{Ear.} \ The lab plays a cadence in each of the twelve keys in Werckmeister III, \ shuffled. \ Rank them from smoothest to roughest.",
            r"\textbf{Build.} \ Extend the ritornello finder so that it allows for mode, \ and test it on the film's concerto.",
            r"$\bigstar$ \ Estimate the tempo range of the sarabande from treatises and documented timings, \ with its uncertainty.",
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
            (r"the Classical style: \ contrast within a movement", [26]),
            (r"the sonata, \ heir of the binary dance", [21, 26]),
            (r"equal temperament wins", [6, 27]),
            (r"opera and song", [40]),
            (r"orchestration from Monteverdi's named instruments", [41]),
            (r"performance practice as evidence", [43]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the Classical style, which puts contrast inside a movement. In the sonata, "
            "the binary dance grown large. In equal temperament's victory. In opera and song. In orchestration, which "
            "began with instruments named in a score. And in performance, where evidence and taste still argue."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"keyboard players", r"realize a figured bass: \ the chords from the numbers, \ a line on top"),
            (r"singers", r"ornament the da capo: \ the return is the singer's"),
            (r"ensembles", r"choose a pitch and a temperament, \ and say why"),
            (r"programmers", r"find returns at any transposition: \ match intervals, \ not pitches"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Keyboard players still realize figured basses, and the good ones add a line on top. Singers "
            "ornament the return of a da capo aria. Ensembles choose a pitch and a temperament, and should say why. And "
            "programmers looking for repeats at any transposition match intervals, not pitches."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"M. Bukofzer, \ \textit{Music in the Baroque Era} \ (1947)",
             r"R. Taruskin, \ \textit{The Oxford History of Western Music}, \ vol. 2 \ (2005)",
             r"R. Donington, \ \textit{The Interpretation of Early Music} \ (1963)",
             r"B. Haynes, \ \textit{A History of Performing Pitch} \ (2002)"],
            [r"V. Galilei, \ \textit{Dialogo della musica antica et della moderna} \ (1581)",
             r"J. Mattheson, \ \textit{Der vollkommene Capellmeister} \ (1739)",
             r"J.-P. Rameau, \ \textit{Traité de l'harmonie} \ (1722)",
             r"J. J. Quantz, \ \textit{Versuch einer Anweisung die Flöte traversiere zu spielen} \ (1752)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 25, "Vienna, the early 1780s",
            "What did listeners expect, so that a composer could surprise them?",
            "A Baroque movement often keeps one governing affect, and builds its form from returns. "
            "<bookmark mark='a'/> The next generation, in Vienna, put contrast inside the movement. In the early "
            "1780s Mozart wrote twelve variations on a French song, and the song is our Tune. His style ran on "
            "expectations so widely shared that Haydn could end a quartet with a joke about where the ending is. What "
            "were they, and can they be measured? <bookmark mark='b'/> Next time. Part 26: The Classical Style.")
