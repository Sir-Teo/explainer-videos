from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.devices()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        card = objectives_card([
            r"an argument is valid when true premises cannot give a false conclusion; \ validity is form",
            r"Zeno: infinitely many stages can take a finite time; \ supertasks remain open",
            r"the \textit{Euthyphro} and the unicorns as Price Lists: \ every exit, computed",
            r"Meno's paradox, recollection, and Plato's line",
            r"Aristotle's 256 moods: \ 15 valid, \ 24 if every term names something",
            r"Mohist substitution failure; \ Nyāya's example as the ground of the universal",
            r"Llull's wheels; \ Leibniz's numbers model the syllogism exactly; \ binary and the Yijing",
            r"relations and nested quantifiers are beyond the syllogism",
        ], title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what this first part built. <bookmark mark='a'/>An argument is valid when true premises "
            "cannot lead to a false conclusion, and validity is a matter of form. Zeno's infinitely many stages can "
            "take a finite time, though supertasks remain a puzzle. <bookmark mark='b'/>The Euthyphro and the "
            "unicorns became Price Lists, with every exit found by calculation. Meno's paradox led to recollection. "
            "<bookmark mark='c'/>Aristotle's two hundred and fifty-six moods, checked by machine: fifteen valid, "
            "twenty-four if every term names something. The Mohists found contexts where substitution fails; the "
            "Nyāya asked how universal premises are known. <bookmark mark='d'/>Llull mechanized combination, Leibniz "
            "turned the syllogism into arithmetic, exactly, and read binary in the Yijing. And Aristotle's logic "
            "cannot handle relations or nested quantifiers."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mk, idx in (("a", [1]), ("b", [2, 3]), ("c", [4, 5]), ("d", [6, 7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()

    def devices(self):
        head = label(r"The Reasoner, so far", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        mods = VGroup(*[VGroup(label(a, font_size=22, color=P.WORLD), label(b, font_size=22, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in (
            (r"\texttt{syllogism.valid, countermodel}", r"the 256 moods, by Venn regions"),
            (r"\texttt{syllogism.leibniz\_countermodel}", r"Leibniz's characteristic numbers"),
            (r"\texttt{prop.mus\_mcs}", r"the Price List engine (built in Part 2)"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4)
        w = wall(upto=1, current=1).scale(0.72).move_to([0, -1.6, 0])
        with self.voiceover(
            "The Reasoner now checks syllogisms two ways, by Venn regions and by Leibniz's numbers, and the Price "
            "List engine, built fully in Part 2, has already found the exits from two old disputes. "
            "<bookmark mark='a'/>And the Wall has its first brick: Zeno, the reminder that some puzzles survive "
            "the mathematics that answers their arithmetic."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in mods], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(w))
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that if a line is cut in the ratio $k : 1$ and each part is cut again in the same ratio, the two "
            r"middle segments are equal.",
            r"Each of the nine moods that need existential import needs some term to be inhabited. For Darapti and "
            r"for Bramantip, which term?",
            r"In Leibniz's two-number scheme, prove that Barbara is valid for every assignment of numbers.",
            r"Llull's first figure joins 9 points in pairs. How many chords would 16 principles need, and how many "
            r"settings has a machine of four wheels of 9 letters?",
            r"Thomson's lamp: why does the sequence of states before $t = 1$ not fix the state at $t = 1$?",
            r"(Essay) Is the \textit{Euthyphro} dilemma a false dilemma? Defend one of the five exits.",
        ], font_size=23)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Plato's line, existential "
            "import, Leibniz's numbers, Llull's combinatorics, Thomson's lamp, and the Euthyphro. Pause, and try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the Price List", [2, 23, 30, 32]),
            (r"existential import and truth-value gaps", [3, 5, 27]),
            (r"substitution failure: `because', `loves'", [20, 22, 27]),
            (r"the universal premise: how is it known?", [15]),
            (r"supertasks and the infinite", [6]),
            (r"Plato's cave", [10, 11]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 2, \textit{The Laws of Thought}: \ Boole, truth tables, and SAT", font_size=26,
                    color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The Price List returns in almost every part. Existential "
            "import and truth-value gaps return in Parts 3, 5 and 27; substitution failure in Parts 20, 22 and 27; "
            "the universal premise in Part 15, on induction; the infinite in Part 6; and the cave in Parts 10 and 11. "
            "<bookmark mark='b'/>Next, Part 2: the laws of thought. Boole's algebra, truth tables, proofs a machine "
            "can check, and the solvers that settle arguments with millions of premises."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kenny, \textit{A New History of Western Philosophy}, vol.\ 1",
             r"Kneale \& Kneale, \textit{The Development of Logic}",
             r"Łukasiewicz, \textit{Aristotle's Syllogistic} (2nd ed., 1957)",
             r"Graham, \textit{Later Mohist Logic, Ethics and Science} (1978); \textit{Disputers of the Tao} (1989)",
             r"Ganeri (ed.), \textit{Indian Logic: A Reader} (2001)",
             r"Eco, \textit{The Search for the Perfect Language} (1995)"],
            [r"Plato, \textit{Euthyphro}, \textit{Meno}, \textit{Republic} VI--VII; Aristotle, \textit{Prior Analytics}",
             r"Thomson, `Tasks and Super-Tasks' (1954); Benacerraf, `Tasks, Super-Tasks, and the Modern Eleatics' "
             r"(1962)",
             r"Strawson, \textit{Introduction to Logical Theory} (1952); Venn, `On the Diagrammatic and Mechanical "
             r"Representation of Propositions' (1880)",
             r"Leibniz, \textit{De arte combinatoria} (1666); `Elementa calculi' (1679); \textit{Explication de "
             r"l'arithmétique binaire} (1703)",
             r"Sotirov, `Arithmetizations of Syllogistic à la Leibniz' (1999)"])
        with self.voiceover("The books and papers this part follows are on screen, and in the notes. Thanks for "
                            "watching."):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
