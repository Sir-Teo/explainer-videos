from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403
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
        c = clip("tune.variation19")
        head = VGroup(label(r"Variation 19", font_size=48, color=TUNE), label(r"one tune, \ three chromatic harmonizations", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        titles = {"mixture": r"with borrowed chords and applied dominants", "neapolitan": r"in minor, \ with the Neapolitan",
                  "trapdoor": r"through a diminished-seventh trapdoor into A$\flat$"}
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built chromatic "
            "harmony. <bookmark mark='a'/> So the Tune's two phrases are harmonized three times. First in C major, "
            "with borrowed chords from the minor and applied dominants. Then in C minor, with an applied dominant "
            "and the Neapolitan before the cadence. And last, a phrase in C that slips through a diminished seventh "
            "and comes out in A flat major, four keys away, carrying the Tune with it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            plan = VGroup(*[label(rf"{k + 1}. \ " + titles[n], font_size=30, color=WHITE) for k, n in enumerate(d["order"])]).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in plan], lag_ratio=0.5), run_time=3.0)
        self.play(FadeOut(plan))
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 19", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for name in d["order"]:
                snd.wait_until(name)
                if shown is not None:
                    self.remove(*shown)
                ver = d["versions"][name]
                g = chord_roll(ver["chords"], width=10.4, height=3.0, lo=34, hi=84, thick=0.12).move_to(DOWN * 0.3)
                names = VGroup(*[label(tex(n), font_size=21, color=TUNE) for n in ver["names"]])
                for k, n in enumerate(names):
                    n.move_to([g.xk(k), g.frame.get_bottom()[1] - 0.35, 0])
                t = label(titles[name], font_size=30, color=GREY_A).next_to(g, UP, buff=0.35)
                shown = [g, names, t]
                self.add(*shown)
                sing_chords(snd, g, ver["times_c"])
                hot_ = [k for k, n in enumerate(ver["names"]) if ("/" in n or "of" in n or "♭" in n or n == "N6")]
                cold = [k for k in range(len(names)) if k not in hot_]
                for ks, base in ((hot_, EAR), (cold, TUNE)):
                    if ks:
                        flash(snd, [names[k] for k in ks], [ver["times_c"][k] for k in ks], hot=WHITE, base=base)
        if shown is not None:
            self.remove(*shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row nineteen of the ledger. {say(v['seconds'])} seconds. The measurement: twenty-four chords, "
            f"{say(load('tune')['outside_c'])} of them outside C major, one phrase carried four keys away, and still not "
            "one pair of parallel fifths or octaves. The voice leading of Part 17 holds even here."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        a = load("applied")
        p = load("paths")
        one = sum(1 for x in p["chromatic"].values() if x == 1)
        card = objectives_card([
            rf"applied dominants: \ a borrowed leading note; \ {100 * a['bach_share']:.0f} beats in 100 of Bach's major chorales",
            r"mixture: \ the minor's chords in a major key",
            r"the Neapolitan and the augmented sixths: \ the strongest ways into the dominant",
            r"the diminished seventh: \ one chord, \ eight keys; \ the German sixth, \ a door a semitone up",
            r"four pure minor thirds overshoot the octave: \ the doors need equal temperament",
            rf"chromatic mediants and the hexatonic cycle; \ from C, \ {one} of 23 keys one chord away; \ tension as distance",
        ], title=r"What we found", font_size=25).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A single borrowed leading note makes any chord a temporary home, and Bach did it on "
            f"about {say(round(100 * a['bach_share']))} beats in a hundred. <bookmark mark='a'/> A major key can borrow the "
            "minor's chords. <bookmark mark='b'/> The Neapolitan and the augmented sixths approach the dominant from "
            "outside the key. <bookmark mark='c'/> The diminished seventh can lead to eight keys, and the German sixth "
            "is a dominant seventh in disguise. <bookmark mark='d'/> These doors are exact only in equal temperament: "
            "pure thirds never close the octave. <bookmark mark='e'/> And smooth motion opens another road, the "
            f"chromatic mediants; with all the doors, {say(one)} of the twenty-three other keys are one chord from C, "
            "and Lerdahl's distance turns each step into a number."
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
            r"Spell the diminished seventh on G$\sharp$ four ways, \ and resolve each to its tonic in four voices.",
            r"Prove that a chord which divides the octave into equal parts has as many distinct transpositions \ "
            r"as its step, \ and count them for the augmented triad and the diminished seventh.",
            r"\textbf{Ear.} \ The lab plays ten cadences in C minor. \ For each, \ name the chord before V: \ "
            r"iv6, \ N6, \ or an augmented sixth \ (which?)",
            r"\textbf{Build.} \ Give the pathfinder a cost for each kind of step, \ and find the cheapest route from C to every key. \ "
            r"Which keys change their route?",
            r"$\bigstar$ \ Design a corpus measure of chromaticism that a listener would agree with, \ "
            r"and say how you would test it.",
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
            (r"form: \ the journey between keys, \ and where it turns", [21]),
            (r"analysis: \ is chromatic harmony a grammar?", [22]),
            (r"the Romantic century: \ a chromaticism index", [27]),
            (r"new scales: \ the octatonic and whole-tone collections", [28]),
            (r"jazz: \ tritone substitution and reharmonization", [39]),
            (r"film music", [44]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? In form, where a journey between keys is the drama. In analysis, which asks "
            "whether this is a grammar. In the Romantic century, where we measure chromaticism across two hundred "
            "years. In the new scales of the twentieth century, built from the symmetry of the diminished seventh and "
            "the augmented triad. In jazz, whose tritone substitution is the German sixth's trick again. And in film "
            "music."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"pianists", r"learn the three diminished sevenths, \ and resolve each eight ways"),
            (r"songwriters", r"borrow iv and $\flat$VI from the minor, \ for a shadow over a major chorus"),
            (r"arrangers", r"approach a cadence through the Neapolitan or a German sixth"),
            (r"film composers", r"move by chromatic mediants: \ one held note, \ two semitones, \ a new world"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. Pianists learn the three diminished sevenths and their resolutions. Songwriters borrow "
            "the minor four and flat six for a shadow over a major chorus. Arrangers approach a cadence through the "
            "Neapolitan or a German sixth. And film composers move by chromatic mediants when they want a new world."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"S. G. Laitz, \ \textit{The Complete Musician} \ (4th ed., \ 2015)",
             r"E. Aldwell and C. Schachter, \ \textit{Harmony and Voice Leading} \ (4th ed., \ 2011)",
             r"F. Lerdahl, \ \textit{Tonal Pitch Space} \ (2001)",
             r"R. Cohn, \ \textit{Audacious Euphony} \ (2012)",
             r"D. Tymoczko, \ \textit{A Geometry of Music} \ (2011)"],
            [r"R. Cohn, \ ``Maximally smooth cycles, \ hexatonic systems, \ and the analysis of late-Romantic triadic progressions'', \ \textit{Music Analysis} 15 (1996)",
             r"D. Tymoczko, \ ``The geometry of musical chords'', \ \textit{Science} 313 (2006)",
             r"F. Lerdahl and C. L. Krumhansl, \ ``Modeling tonal tension'', \ \textit{Music Perception} 24 (2007)",
             r"E. Kurth, \ \textit{Romantische Harmonik und ihre Krise in Wagners Tristan} \ (1920)",
             r"F. Lehman, \ \textit{Hollywood Harmony} \ (2018)"],
            font_size=20)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"can a melody be its own accompaniment?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"chords, \ and the lines inside them", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 20", font_size=32, color=GREY_B), label(r"Canon and Fugue", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part treated harmony as chords, and found at the end that chords are lines moving together. "
            "<bookmark mark='a'/> The next part starts from lines. Can a melody be its own accompaniment, entering "
            "against itself, a few beats later, and still make harmony? <bookmark mark='b'/> Next time. Part 20: Canon "
            "and Fugue."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
