from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403
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
        c = clip("tune.variation17")
        head = VGroup(label(r"Variation 17", font_size=48, color=TUNE), label(r"the Tune as a chorale", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        gp = choir_roll(d["voices_plain"], width=10.6, height=2.3, lo=40, hi=84, thick=0.08).move_to(UP * 1.05 + RIGHT * 0.6)
        gf = choir_roll(d["voices_full"], width=10.6, height=2.3, lo=40, hi=84, thick=0.08).move_to(DOWN * 2.0 + RIGHT * 0.6)
        lp = label(r"chosen \\ chord by chord", font_size=20, color=GREY_A).next_to(gp, LEFT, buff=0.25)
        lf = label(r"corrected \\ by the rules", font_size=20, color=GREY_A).next_to(gf, LEFT, buff=0.25)
        T = TICKS
        reds = VGroup()
        for k in d["parallels_plain"]:
            t = d["voices_plain"][0][k][1] if k < len(d["voices_plain"][0]) else 0
            reds.add(Line([gp.x(t) + 0.03, gp.frame.get_bottom()[1], 0], [gp.x(t) + 0.03, gp.frame.get_top()[1], 0], color=RED, stroke_width=3))
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a "
            "harmonizer. <bookmark mark='a'/> So the Tune becomes a chorale tune, with a pause at the end of "
            "each phrase, and is harmonized twice: first by the chord-chooser alone, which knows Bach's "
            "chords but not his rules, and then by the full search, which corrects it. Listen for the "
            "places where the first goes wrong; they are marked in red."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(gp), FadeIn(lp), FadeIn(gf), FadeIn(lf))
        with self.listen(c) as snd:
            window(snd, r"Variation 17", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, gp, d["times"]["plain"], start=d["starts"]["plain"])
            sing_roll(snd, gf, d["times"]["full"], start=d["starts"]["full"])
            pulse(snd, lp, d["starts"]["plain"], d["starts"]["full"] - 0.6, buff=0.08)
            pulse(snd, lf, d["starts"]["full"], c.duration, buff=0.08)
            snd.wait_until("full")
            self.add(reds)
        self.remove(reds)
        self.remove(gp, gf, lp, lf)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row seventeen of the ledger. {say(v['seconds'])} seconds. The measurement: the chord-chooser's "
            f"version has {say(len(d['parallels_plain']))} parallel fifths or octaves; the corrected one, none. "
            "The chords are nearly the same in both. What changed is where the voices sing them."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        b = load("census")
        e = load("evaluation")
        card = objectives_card([
            r"364 chorales: \ ranges, \ spacing, \ doubling and motion, \ measured",
            r"each voice a line: \ steps, \ and nearly the shortest way",
            rf"the rules, \ counted: \ Bach writes parallels once in {b['rate']:.0f} chord changes",
            r"chords, \ cadences, \ and the notes between the beats",
            rf"a search over chords and voicings: \ {100 * e['full']['same_chord']:.0f}\% of Bach's chords, \ no parallels",
            r"and the gap: \ lines planned over many beats",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Bach's chorales, as data, show where four voices sing, how far apart, which "
            "note is doubled. <bookmark mark='a'/> Each voice is a line of small steps, and the inner voices "
            "take nearly the shortest way. <bookmark mark='b'/> The rules hold almost always: Bach writes "
            f"parallel fifths or octaves once in about {say(round(b['rate'], -1))} changes of chord. "
            "<bookmark mark='c'/> His chords, cadences and passing notes can be counted too. "
            "<bookmark mark='d'/> A search over chords and voicings, learned from the chorales and "
            "constrained by the rules, finds Bach's chord about four times in ten on tunes it never saw, "
            "and breaks no rule. <bookmark mark='e'/> And what it lacks is the plan of a line over many "
            "beats, which is what the newer machines learn."
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
            r"Harmonize the first phrase of the Tune, \ C C G G A A G, \ by hand: \ one chord to a note, \ I, \ IV or V only, \ "
            r"four voices in range, \ no parallels. \ How many choices of chords are there, \ before voicing?",
            r"Show that if every voice moves to the nearest note of the next chord, \ two voices can still make parallel fifths. \ "
            r"Give the smallest example, \ and the rule that prevents it.",
            r"\textbf{Ear.} \ The lab plays eight short cadences from the chorales. \ Name each: \ authentic, \ half, \ "
            r"or ending on a major chord in a minor key.",
            r"\textbf{Build.} \ Change the harmonizer's chord model to look two chords back instead of one. \ "
            r"Does it find Bach's chord more often on the test chorales? \ Why might it not?",
            r"$\bigstar$ \ Design a listening test that could show a machine's chorales are as good as Bach's. \ "
            r"What would a fair test control for?",
        ], font_size=23)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research "
            "problem, marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"progressions: \ where chapter 6's table comes from", [18]),
            (r"chromatic chords, \ and travelling far quickly", [19]),
            (r"canon and fugue: \ four voices from one melody", [20]),
            (r"the Renaissance before Bach's harmony", [23, 24]),
            (r"machines that compose, \ and how to judge them", [42, 65]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once: the next part asks where the table of progressions comes "
            "from, and the part after it travels to distant keys with chromatic chords. Canon and fugue "
            "make four voices from one melody. The Renaissance shows harmony before Bach's. And the machines "
            "of the frontier return when this series builds composers of its own, and asks how to judge "
            "them."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"choir directors", r"balance the inner voices, \ which carry the passing notes that make the lines"),
            (r"arrangers", r"keep three upper parts close and let the bass move; \ double the root"),
            (r"church musicians", r"harmonize a hymn at sight: \ cadence chords first, \ then the shortest way between"),
            (r"music software", r"auto-harmonizers and accompaniment apps are this part's search, \ larger"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A choir director balances the inner voices, which carry the lines. An arranger "
            "keeps the upper parts close and lets the bass move. A church musician harmonizing a hymn at "
            "sight finds the cadence chords first and takes the shortest way between them. And the "
            "auto-harmonizers in music software are, at heart, this part's search, larger."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. S. Bach, \ \textit{371 vierstimmige Choralges\"ange}, \ ed. C. P. E. Bach \ (Breitkopf, \ 1784--87)",
             r"E. Aldwell and C. Schachter, \ \textit{Harmony and Voice Leading} \ (1978; \ 4th ed. 2011)",
             r"S. Kostka and D. Payne, \ \textit{Tonal Harmony} \ (1984; \ 8th ed. 2018)",
             r"D. Huron, \ \textit{Voice Leading: The Science behind a Musical Art} \ (2016)"],
            [r"K. Ebcio\u{g}lu, \ ``An expert system for harmonizing four-part chorales'', \ \textit{Computer Music Journal} 12 (1988)",
             r"M. Allan and C. K. I. Williams, \ ``Harmonising chorales by probabilistic inference'', \ \textit{NIPS} 17 (2005)",
             r"G. Hadjeres, \ F. Pachet and F. Nielsen, \ ``DeepBach'', \ \textit{ICML} (2017)",
             r"C.-Z. A. Huang and others, \ ``Counterpoint by convolution'', \ \textit{ISMIR} (2017)",
             r"M. S. Cuthbert and C. Ariza, \ ``music21'', \ \textit{ISMIR} (2010): \ the encodings used here"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        ex = [(72, 64, 55, 48), (72, 65, 57, 53), (71, 62, 55, 43), (72, 64, 55, 48)]
        st = block_staff(ex, width=5.0, beats=2).move_to(UP * 1.3)
        q = label(r"why does IV go to V, \ and V to I?", font_size=30, color=EAR).move_to(DOWN * 0.8)
        nxt = VGroup(label(r"Part 18", font_size=32, color=GREY_B), label(r"Progressions", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This part counted which chord follows which, and used the table without asking why. "
            "<bookmark mark='a'/> Why does four go to five, and five to one? Is there a grammar of chords, "
            "like the grammar of a sentence, and did musicians learn it as children learn to speak? In the "
            "conservatories of eighteenth-century Naples, orphans learned it as patterns, by heart. "
            "<bookmark mark='b'/> Next time. Part 18: Progressions."
        ) as vo:
            self.play(FadeIn(st))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
