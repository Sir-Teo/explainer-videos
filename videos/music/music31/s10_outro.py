from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403
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
        c = clip("tune.variation31")
        head = VGroup(label(r"Variation 31", font_size=48, color=TUNE), label(r"the Tune, \ walked on the Tonnetz", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        names = VGroup(*[label(tex_triad(n), font_size=30, color=TUNE if not n.endswith("m") else BLUE) for n in d["walk"]]).arrange(RIGHT, buff=0.6).move_to(UP * 1.2)
        moves = VGroup(*[label(m, font_size=19, color=GREY_A).move_to((names[i].get_center() + names[i + 1].get_center()) / 2 + DOWN * 0.55) for i, m in enumerate(d["moves"])])
        g = mroll(d["melody"], width=10.0, height=1.4, lo=70, hi=84, color=TUNE, bar_h=0.12).move_to(DOWN * 1.6)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time a program "
            "harmonizes it by walking on the Tonnetz: every two beats it may stay, or take one or two P, L or R steps, to a "
            "triad containing the melody note, preferring the smallest moves and ending at home. The walk it finds is C, C, A "
            "minor, C, F, C, G, C: given only the moves and the melody, it rediscovers the tonic, subdominant and dominant."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(moves), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"Variation 31", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(len(names)):
                pulse(snd, names[i], 2 * i * d["unit"], (2 * i + 2) * d["unit"] - 0.05, buff=0.08)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["melody"]], hot=WHITE, base=TUNE)
        self.play(FadeOut(names), FadeOut(moves), FadeOut(g))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-one of the ledger: {say(v['seconds'])} seconds; the measurement is the walk itself, eight chords and "
            "the moves between them."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        g = load("groups")
        card = objectives_card([
            r"P, \ L and R: \ one voice moves, \ by a semitone or a whole tone",
            rf"the PLR and T/I groups: \ {g['plr']} elements each, \ commuting, \ dual",
            r"the Tonnetz: \ triads as triangles on a torus; \ C to b$\flat$ is five steps",
            r"hexatonic and octatonic cycles walk Part 28's scales",
            r"R, \ L, \ R, \ L ... \ visits all 24 triads: \ Beethoven's chain",
            r"film's mediants and poles, \ Coltrane's thirds: \ the moves in use",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? P, L and R each move one voice, by a semitone or a whole tone. <bookmark mark='a'/> With "
            "transposition and inversion they form two groups of twenty-four that commute, each the dual of the other. "
            "<bookmark mark='b'/> The Tonnetz draws every triad as a triangle on a torus, where B flat minor is five steps "
            "from C. <bookmark mark='c'/> Repeating two moves walks Part 28's symmetric scales. <bookmark mark='d'/> R and L "
            "alternating visit all twenty-four triads, as Beethoven's chain begins to. <bookmark mark='e'/> And film and "
            "jazz use the moves every day."
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
            r"Find the shortest PLR word from C major to F$\sharp$ major, \ and count the semitones the voices move.",
            r"Prove that P, \ L and R each commute with every transposition $T_n$.",
            r"\textbf{Ear.} \ The lab plays eight pairs of triads; \ each pair is P, \ L or R. \ Name them.",
            r"\textbf{Build.} \ Write a program that harmonizes any melody by a walk on the Tonnetz, \ and compare it with Part 17's harmonizer.",
            r"$\bigstar$ \ Which geometry of triads matches what listeners hear?",
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
            (r"the geometry of chords and voice leading", [32]),
            (r"rhythm and scale as mathematics", [33]),
            (r"jazz harmony and its changes", [39]),
            (r"music for picture and play", [44]),
            (r"chords recognized by machine", [62]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in the geometry of chords and voice leading. In the mathematics of rhythm and "
            "scale. In jazz harmony. In music for picture and play. And in machines that recognize chords."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"film composers", r"reach for mediants and poles, \ knowing what they suggest"),
            (r"songwriters", r"move between chords by keeping two notes"),
            (r"jazz players", r"practise cycles of major thirds"),
            (r"analysts", r"name the moves when no key fits"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Film composers reach for mediants and poles, knowing what they suggest. Songwriters move between "
            "chords by keeping two notes. Jazz players practise cycles of major thirds. And analysts name the moves when no "
            "key fits."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. Lewin, \ \textit{Generalized Musical Intervals and Transformations} \ (1987)",
             r"R. Cohn, \ \textit{Audacious Euphony} \ (2012)",
             r"F. Lehman, \ \textit{Hollywood Harmony} \ (2018)",
             r"D. Tymoczko, \ \textit{A Geometry of Music} \ (2011)"],
            [r"A. S. Crans, \ T. M. Fiore, \ R. Satyendra, \ `Musical actions of dihedral groups', \ \textit{Amer. Math. Monthly} \ (2009)",
             r"R. Cohn, \ `Maximally smooth cycles, \ hexatonic systems', \ \textit{Music Analysis} \ (1996)",
             r"C. L. Krumhansl, \ `Perceived triad distance', \ \textit{Journal of Music Theory} \ (1998)",
             r"L. Euler, \ \textit{Tentamen novae theoriae musicae} \ (1739)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if every chord were a point, \ and every progression a path?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act V: \ after tonality", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 32", font_size=32, color=GREY_B), label(r"The Geometry of Chords", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The Tonnetz is a map for triads. <bookmark mark='a'/> What if every chord, of any size, were a point, and every "
            "progression a path through a space? <bookmark mark='b'/> Next time. Part 32: The Geometry of Chords."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
