from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403
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
        c = clip("tune.variation22")
        head = VGroup(label(r"Variation 22", font_size=48, color=TUNE), label(r"the Tune, \ reduced and regrown", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = mroll(d["skeleton"], width=11.0, height=1.3, lo=66, hi=88, total=48.0, color=BLUE).move_to(UP * 0.8)
        g2 = mroll(d["regrown"], width=11.0, height=1.3, lo=66, hi=88, total=48.0, color=TUNE).move_to(DOWN * 1.2)
        t1 = label(r"the skeleton: \ a note every four beats", font_size=22, color=BLUE).next_to(g1, UP, buff=0.15)
        t2 = label(r"regrown along a different derivation", font_size=22, color=TUNE).next_to(g2, UP, buff=0.15)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built reductions and "
            "grammars. <bookmark mark='a'/> So the Tune is reduced to its skeleton, a note every four beats over its "
            "harmony, and then regrown by the elaboration grammar along a different derivation: the same skeleton, the "
            "same chords, a different surface."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(t1), FadeIn(g2), FadeIn(t2))
        with self.listen(c) as snd:
            window(snd, r"Variation 22", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g1.notes, [d["starts"]["skeleton"] + n[1] * d["beat"] for n in d["skeleton"]], hot=WHITE, base=BLUE)
            flash(snd, g2.notes, [d["starts"]["regrown"] + n[1] * d["beat"] for n in d["regrown"]], hot=WHITE, base=TUNE)
            pulse(snd, t1, d["starts"]["skeleton"], d["starts"]["regrown"] - 0.5, buff=0.08)
            pulse(snd, t2, d["starts"]["regrown"], c.duration, buff=0.08)
        self.play(FadeOut(g1), FadeOut(g2), FadeOut(t1), FadeOut(t2))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-two of the ledger. {say(v['seconds'])} seconds. The measurement: {say(len(d['skeleton']))} skeleton "
            f"notes grown into {say(len(d['regrown']))}, and on {say(d['chord_tones_on_strong_beats'])} of "
            f"{say(d['strong_beats'])} strong beats a note of the chord. The grammar keeps the harmony most of the time; it "
            "never keeps the Tune's repetitions."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        u = load("urlinie")
        l_ = load("learned")
        b = l_["bits"]
        tot = u["real"].get("5-4-3-2-1", 0) + u["real"].get("3-2-1", 0)
        card = objectives_card([
            r"reduction: \ passing, \ neighbour, \ arpeggiation; \ a prolonged note lasts in the mind",
            rf"the \textit{{Ursatz}}: \ {tot} of {u['n']} major tunes end on a descent to the tonic \ (shuffled: \ about 3)",
            r"preference rules recover the Tune's phrase ends and its I--V--I",
            r"harmony as a grammar: \ trees, \ recursion, \ ambiguity growing like the Catalan numbers",
            rf"trained on Bach: \ the grammar {b['functional']:.1f} bits a chord, \ chord pairs {b['bigram']:.1f}",
            r"a theory and its author: \ the argument; \ recursion heard over seconds, \ not minutes",
        ], title=r"What we found", font_size=23).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Reduction rests on a few ways one note serves another. <bookmark mark='a'/> Schenker's "
            "descent to the tonic is really there at the ends of tunes, far beyond chance. <bookmark mark='b'/> A handful "
            "of explicit preference rules recover the Tune's phrases and its tonic, dominant, tonic. "
            "<bookmark mark='c'/> Harmony can be written as a recursive grammar, whose ambiguity grows like the Catalan "
            "numbers. <bookmark mark='d'/> Trained on Bach, such a grammar describes but does not out-predict chord "
            "pairs. <bookmark mark='e'/> And the theory's author, and whether nesting is heard at all, remain open "
            "arguments."
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
            r"Reduce \textit{Ode to Joy}'s first eight bars \ (Part 14's version) \ to a note every four beats, \ by hand, \ using this part's score.",
            r"Prove that the number of binary trees over $n$ leaves is the Catalan number $C_{n-1}$, \ and say why the parse counts of chapter 6 are Catalan numbers.",
            r"\textbf{Ear.} \ The lab plays eight short passages and two skeletons for each. \ Choose the skeleton that fits.",
            r"\textbf{Build.} \ Add the rule TR $\to$ SR TR to the grammar, \ retrain it, \ and report its bits per chord and coverage.",
            r"$\bigstar$ \ Design an experiment that measures a listener's reduction of a melody directly.",
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
            (r"the Renaissance: \ counterpoint before tonality", [24]),
            (r"the classical style: \ topics and schemata at work", [26]),
            (r"twelve tones: \ music after the \textit{Ursatz}", [29]),
            (r"jazz: \ the deepest trees", [39]),
            (r"expectation and emotion", [46]),
            (r"machines that compose", [65]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? In the Renaissance, whose counterpoint predates the tonal tree. In the classical "
            "style, where topics and schemata meet. In twelve-tone music, written against everything the Ursatz stands "
            "for. In jazz, where the trees are deepest. In expectation and emotion, the listener's side. And in machines "
            "that compose."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"performers", r"know which notes are structural: \ they shape the phrase"),
            (r"improvisers", r"elaborate a skeleton: \ the changes are the tree, \ the solo the surface"),
            (r"arrangers", r"keep the skeleton, \ change the surface: \ a variation"),
            (r"analysts", r"say which level an analysis describes, \ and test it"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. Performers who know which notes are structural shape a phrase around them. Improvisers "
            "elaborate a skeleton, the changes underneath. Arrangers keep the skeleton and change the surface. And "
            "analysts can say which level they describe, and test it."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. Cadwallader and D. Gagné, \ \textit{Analysis of Tonal Music: \ A Schenkerian Approach} \ (3rd ed., \ 2011)",
             r"F. Lerdahl and R. Jackendoff, \ \textit{A Generative Theory of Tonal Music} \ (1983)",
             r"H. Schenker, \ \textit{Der freie Satz} \ (1935)",
             r"L. B. Meyer, \ \textit{Emotion and Meaning in Music} \ (1956); \ L. G. Ratner, \ \textit{Classic Music} \ (1980)"],
            [r"M. Rohrmeier, \ ``Towards a generative syntax of tonal harmony'', \ \textit{Journal of Mathematics and Music} 5 \ (2011)",
             r"S. Koelsch and others, \ ``Processing of hierarchical syntactic structure in music'', \ \textit{PNAS} 110 \ (2013)",
             r"P. Ewell, \ ``Music theory and the white racial frame'', \ \textit{Music Theory Online} 26 \ (2020)",
             r"M. D. Hauser, \ N. Chomsky and W. T. Fitch, \ ``The faculty of language'', \ \textit{Science} 298 \ (2002)",
             r"M. Rohrmeier, \ ``The syntax of jazz harmony'', \ \textit{Music Theory and Analysis} 7 \ (2020)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"how did music come to have harmony at all?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act III: \ the grammar of one tradition", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 23", font_size=32, color=GREY_B), label(r"Chant to Polyphony", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part ends Act Three, the grammar of one tradition, written and tested. <bookmark mark='a'/> Act Four "
            "goes back a thousand years, to ask how that tradition came to have harmony at all: from a single line of "
            "chant to many voices. <bookmark mark='b'/> Next time. Part 23: Chant to Polyphony."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
