from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Galileo's paradox and Hilbert's hotel; \ Dedekind's definition of the infinite",
            r"the rationals counted by a tree; \ the reals not: \ the diagonal; \ Cantor's theorem",
            r"Cantor's absolute and his critics; \ Russell's letter \ (the Wall); \ separation; \ ZFC",
            r"sets from nothing; \ Ackermann's coding; \ the cumulative hierarchy",
            r"ordinals to $\varepsilon_0$; \ Goodstein's sequences and the hydra; \ the alephs; \ line = square",
            r"choice, \ Vitali, \ Banach--Tarski; \ the continuum: \ Gödel's $L$ and Cohen's forcing \ (the Wall)",
            r"large cardinals and determinacy; \ realism and the multiverse; \ rival foundations",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The hotel, Galileo's paradox, and Dedekind's definition "
            "that turns the paradox into a property. <bookmark mark='b'/>A tree that counts the fractions, and the "
            "diagonal that shows the reals cannot be counted, nor any set's subsets by the set itself. "
            "<bookmark mark='c'/>Cantor's critics; Russell's letter, which brought down naive set theory, and the axioms that replaced "
            "it. <bookmark mark='d'/>Sets built from nothing, numbered by Ackermann, stacked in a cone. "
            "<bookmark mark='e'/>Ordinals past infinity, Goodstein's sequences that must come home, the hydra that always dies, and the alephs. "
            "<bookmark mark='f'/>Choice and its monsters, and the continuum problem, which the axioms provably "
            "cannot settle. <bookmark mark='g'/>And the search for new axioms, with the philosophical question it "
            "raises: what are sets?"
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{sets.ackermann\_decode, code}", r"the hereditarily finite sets, \ numbered"),
                (r"\texttt{sets.V, rank, von\_neumann}", r"the cumulative hierarchy, \ finite stages"),
                (r"\texttt{sets.cantor\_check, diagonal}", r"Cantor's theorem, \ by brute force"),
                (r"\texttt{sets.Ord}", r"ordinal arithmetic below $\varepsilon_0$"),
                (r"\texttt{sets.goodstein, hydra\_battle}", r"Goodstein's sequences; \ Hercules and the hydra"),
                (r"\texttt{sets.paradoxical\_check, tictactoe}", r"the free group; \ Zermelo's games"),
                (r"\texttt{matrix.*}, \ \texttt{modal.*}, \ \texttt{fol.*}, \ \dots", r"Parts 1--5")]
        lefts = [label(a, font_size=22, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=22, color=GREY_A) for _, b in mods]
        lw = max(m.width for m in lefts)
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([x0 + lw + 0.5 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked against known values: \ \texttt{tests/philosophy/test\_sets.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=6, current=6).scale(0.4).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has a module for sets. <bookmark mark='a'/>It numbers the hereditarily finite sets, "
            "builds the finite stages of the hierarchy, checks Cantor's theorem by brute force, computes with "
            "ordinals below epsilon zero, runs Goodstein's sequences, and checks the paradoxical split of the free "
            "group. Its tests compare it with known values: Goodstein's sequence from four, the sizes of the stages, "
            "and the five thousand, four hundred and seventy-eight positions of noughts and crosses. "
            "<bookmark mark='b'/>And the Wall has its sixth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[6], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that the set of all \textit{finite} subsets of $\mathbb{N}$ is countable. \ (Hint: Ackermann.)",
            r"Show by a diagonal argument that the functions from $\mathbb{N}$ to $\mathbb{N}$ cannot be listed.",
            r"Compute $(\omega+1)\cdot 2$, \ $2\cdot(\omega+1)$, \ $\omega\cdot(\omega+1)$, \ and compare $\omega + "
            r"\omega^2$ with $\omega^2 + \omega$.",
            r"Write the first five terms of Goodstein's sequence from 5, \ with their ordinals.",
            r"Use separation to show that no set contains every set. \ Why does the iterative conception agree?",
            r"(Essay) Is the continuum hypothesis true, false, or neither? \ Defend a view against one rival.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Two counting arguments, a "
            "little ordinal arithmetic, a Goodstein sequence, the universal set, and an essay on the continuum. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the diagonal, \ the halting problem, \ incompleteness", [7]),
            (r"the liar: \ another self-reference", [8]),
            (r"what numbers are: \ Benacerraf, \ structuralism", [9]),
            (r"Goodstein and $\varepsilon_0$: \ the strength of arithmetic", [7]),
            (r"infinite games and strategies", [34]),
            (r"the infinite in physics and in time", [25]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 7, \textit{The Limits of Proof}: \ Gödel, Turing, Tarski, Löb", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The diagonal returns in Part 7, as the halting problem and "
            "Gödel's incompleteness theorems, and in Part 8 as the liar. What numbers are, after Benacerraf, in Part "
            "9. Goodstein's theorem and epsilon zero measure the strength of arithmetic in Part 7. Infinite games "
            "return in Part 34, and the infinite in space and time in Part 25. <bookmark mark='b'/>Next, Part 7: "
            "the limits of proof."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Enderton, \textit{Elements of Set Theory} (1977); \ Kunen, \textit{Set Theory} (2011)",
             r"Potter, \textit{Set Theory and Its Philosophy} (2004)",
             r"Jech, \textit{Set Theory} (3rd ed., 2003); \ Kanamori, \textit{The Higher Infinite} (2003)",
             r"van Heijenoort (ed.), \textit{From Frege to Gödel} (1967)"],
            [r"Galileo 1638; Bolzano 1851; Cantor 1874, 1883, 1891; Dedekind 1888; Hilbert 1900, 1926; König 1905",
             r"Russell 1902, 1908; Frege 1893, 1903; Zermelo 1904, 1908, 1913, 1930; Fraenkel 1922; Skolem 1922",
             r"von Neumann 1923, 1925; Kuratowski 1921; Ackermann 1937; Goodstein 1944; Kirby \& Paris 1982",
             r"Vitali 1905; Banach \& Tarski 1924; Gödel 1938, 1947; Cohen 1963; Easton 1970; Solovay 1970",
             r"Boolos 1971; Maddy 1988; Martin \& Steel 1989; Woodin 2001; Feferman 2011; Hamkins 2012"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
