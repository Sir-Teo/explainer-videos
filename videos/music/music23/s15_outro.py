from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403
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
        c = clip("tune.variation23")
        head = VGroup(label(r"Variation 23", font_size=48, color=TUNE), label(r"the Tune, \ three centuries early", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = mroll(d["chant"], width=3.9, height=2.6, lo=58, hi=79, color=TUNE)
        g2 = voices_roll([d["chant"], d["organum"]], width=3.9, height=2.6, colors=[TUNE, BLUE], lo=58, hi=79)
        m = d["motet"]
        g3 = voices_roll([m["upper"], m["tenor"]], width=3.9, height=2.6, colors=[TUNE, GREY_A], lo=50, hi=79)
        cols = VGroup(*[VGroup(label(t, font_size=20, color=GREY_A), g).arrange(DOWN, buff=0.25) for t, g in (
            (r"as chant", g1), (r"as organum at the fifth", g2), (r"as an isorhythmic motet", g3))]).arrange(RIGHT, buff=0.55).move_to(UP * 0.4)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a thousand years of "
            "machinery, so the Tune goes back in time. <bookmark mark='a'/> First as chant, one voice in free rhythm, in F "
            "with a B flat, as singers of the tritus modes often sang. Then as organum at the fifth below, by the "
            "Enchiriadis rule. And last as an isorhythmic motet: its first seven notes as the color of a tenor, laid "
            "through a talea of four notes and a rest, with a free voice above."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"Variation 23", detail=r"synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            st = d["starts"]
            flash(snd, g1.notes, [st["chant"] + n[1] * d["unit"] for n in d["chant"]], hot=WHITE, base=TUNE)
            flash_voices(snd, g2, [d["chant"], d["organum"]], st["organum"], d["unit"], colors=[TUNE, BLUE])
            flash_voices(snd, g3, [m["upper"], m["tenor"]], st["motet"], m["unit"], colors=[TUNE, GREY_A])
            pulse(snd, cols[0][0], st["chant"], st["organum"] - 0.5, buff=0.08)
            pulse(snd, cols[1][0], st["organum"], st["motet"] - 0.5, buff=0.08)
            pulse(snd, cols[2][0], st["motet"], c.duration, buff=0.08)
        self.play(FadeOut(cols))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-three of the ledger. {say(v['seconds'])} seconds. The measurement: a color of "
            f"{say(len(d['color']))} pitches through a talea of {say(sum(1 for x in d['talea'] if x > 0))} notes, which meet "
            f"again after {say(d['meet'])} notes. The Tune, which has always been a melody over chords, sounds here like "
            "music written before chords existed."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        cz = load("census")
        iso = load("isorhythm")
        card = objectives_card([
            r"chant: \ eight modes by final, \ range and reciting tone; \ the theorists' rule is an algorithm",
            r"Guido: \ hexachords and solmization, \ a shortest path; \ the staff",
            r"organum: \ parallel, \ then free, \ then florid; \ the tritone forced the first independence",
            r"rhythm written: \ six modes read from ligatures, \ then Franco's shapes, \ then mensuration",
            rf"isorhythm: \ color against talea; \ the taleae of de Vitry's motets found by a scan",
            rf"the century counted: \ perfect intervals on the beat, \ {100 * cz['parallels']['trecento']['parallels'] / cz['parallels']['trecento']['moves']:.0f} parallels in 100 moves, \ open final chords",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Chant was organized by mode, and the medieval rule for finding a mode is already an "
            "algorithm. <bookmark mark='a'/> Guido gave singers syllables, hexachords and the staff, and choosing "
            "syllables is a shortest-path problem. <bookmark mark='b'/> Organum went from parallel to free to florid, and "
            "the tritone forced the voices apart. <bookmark mark='c'/> Rhythm was written first as a grammar of "
            "patterns, then note by note, then on two levels of measure. <bookmark mark='d'/> Isorhythm builds a tenor "
            "from two cycles, and a scan finds them in de Vitry's motets. <bookmark mark='e'/> And a century of music, "
            "counted, keeps perfect intervals on the beat, tolerates parallels, and ends without a third."
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
            r"A tenor's color has 28 pitches and its talea 8 notes. \ After how many notes do they begin together again, \ and how many statements of each is that?",
            r"Prove that Franco's rules \ (imperfection and alteration) \ read any row of breves and semibreves in perfect time as whole perfections.",
            r"\textbf{Ear.} \ The lab sings psalm verses in the eight modes in random order. \ Name each one's mode.",
            r"\textbf{Build.} \ Improve the talea scan so that it also requires the pitches to change while the rhythm repeats, \ and run it on the corpus.",
            r"$\bigstar$ \ Learn the rules of \textit{musica ficta} from edited pieces, \ and measure where two editions of the same piece disagree.",
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
            (r"the Renaissance: \ smooth lines, \ full triads, \ the end of isorhythm", [24]),
            (r"the Baroque: \ modes become keys", [25]),
            (r"modal jazz and modal rock: \ the modes return", [39]),
            (r"minimalism: \ cycles of different lengths, \ again", [30]),
            (r"musical traditions with modes of their own", [35]),
            (r"finding music in archives by machine", [63]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the Renaissance, which smoothed the lines, filled in the triads and let "
            "isorhythm go. In the Baroque, where the modes turn into keys. In modal jazz and rock, where the old modes "
            "return. In minimalism, where cycles of different lengths drift against each other as color and talea did. "
            "In other traditions with modes of their own. And in machines that search the archives."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"choirs", r"read a modern edition knowing which accidentals are the editor's"),
            (r"composers", r"use color and talea: \ two cycles that rarely align make long, \ unrepeating music"),
            (r"teachers", r"solmization is still taught: \ movable do is Guido's hexachord, \ widened"),
            (r"scholars", r"treat editions as data, \ with the uncertain parts marked"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Choirs singing this music can tell the editor's accidentals from the scribe's. Composers "
            "still use two cycles of different lengths to make long music that never quite repeats. Teachers of "
            "movable do are teaching Guido's hexachord, widened to seven notes. And scholars can treat editions as data, "
            "with the uncertain parts marked as uncertain."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"R. H. Hoppin, \ \textit{Medieval Music} \ (1978)",
             r"R. Taruskin, \ \textit{The Oxford History of Western Music}, \ vol. 1 \ (2005)",
             r"T. F. Kelly, \ \textit{Capturing Music: \ The Story of Notation} \ (2014)",
             r"D. Hiley, \ \textit{Western Plainchant: \ A Handbook} \ (1993)"],
            [r"\textit{Polyphonic Music of the Fourteenth Century}, \ ed. L. Schrade and others \ (1956--1991)",
             r"M. S. Cuthbert and C. Ariza, \ ``music21'', \ \textit{ISMIR} \ (2010): \ the corpus",
             r"U. Günther, \ ``Das Ende der ars nova'', \ \textit{Die Musikforschung} 16 \ (1963)",
             r"M. Bent, \ \textit{Counterpoint, \ Composition, \ and Musica Ficta} \ (2002)",
             r"E. Cardine, \ \textit{Sémiologie grégorienne} \ (1970)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what happens when every voice becomes equal?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act IV: \ a thousand years", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 24", font_size=32, color=GREY_B), label(r"The Renaissance", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Act Four has begun its thousand years. <bookmark mark='a'/> By 1430 the tenor was losing its privilege; "
            "the next century made every voice equal, imitating one another, in full triads. <bookmark mark='b'/> Next "
            "time. Part 24: The Renaissance."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
