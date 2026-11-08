from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.horses()
        self.maths()
        self.objectives()

    def title(self):
        t = part_title(PART)
        recap = VGroup(label(r"Part 1: \ Aristotle cannot see relations", font_size=28, color=GREY_A),
                       label(r"Part 2: \ propositional logic cannot see inside sentences", font_size=28,
                             color=GREY_A)).arrange(DOWN, buff=0.25).next_to(t, DOWN, buff=0.8)
        with self.voiceover(
            "In Part 1, Aristotle's logic stumbled on an argument a child can see is valid. In Part 2 we built a "
            "complete logic of whole sentences, and it could not see inside a sentence at all. "
            "<bookmark mark='a'/>This part opens sentences up. Its logic, first-order logic, is the logic of 'all', "
            "'some', and relations between things, and it is still the standard language of mathematics and of "
            "analytic philosophy."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(recap))
        self.clear_scene()

    def horses(self):
        d = load("tableaux")["horses"]
        arg = VGroup(label(r"Every horse is an animal.", font_size=32),
                     label(r"So every head of a horse is the head of an animal.", font_size=32, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.5)
        p = fm(d["premises"][0], font_size=36)
        c = fm(d["conclusion"], font_size=34, color=GOAL)
        form = VGroup(p, c).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.3, 0])
        key = label(r"$H$: horse \quad $A$: animal \quad $\mathrm{Hd}(x, y)$: $x$ is a head of $y$", font_size=24,
                    color=GREY_A).next_to(form, DOWN, buff=0.35)
        res = label(rf"the Reasoner's tableau: \ closed, \ {len(d['steps'])} steps, \ {d['branches']} branches "
                    r"\ $\checkmark$", font_size=28, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is De Morgan's argument again. <bookmark mark='a'/>In the new notation: for every x, if x is a "
            "horse, x is an animal. <bookmark mark='b'/>Therefore, for every x, if there is a y such that x is a head "
            "of y and y is a horse, then there is a y such that x is a head of y and y is an animal. The relation "
            "'head of' is now visible, and so is the order of the quantifiers. <bookmark mark='c'/>The Reasoner's "
            f"new prover, built in Chapter six, checks it in {len(d['steps'])} steps: valid."
        ) as vo:
            self.play(FadeIn(arg))
            vo.wait_until("a")
            self.play(Write(p))
            vo.wait_until("b")
            self.play(Write(c), FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(res, shift=UP * 0.2))
        self.clear_scene()

    def maths(self):
        cont = MathTex(r"\forall \varepsilon > 0\ \exists \delta > 0\ \forall x\ "
                       r"(|x - a| < \delta \to |f(x) - f(a)| < \varepsilon)", font_size=40).move_to([0, 1.6, 0])
        cl = label(r"$f$ is continuous at $a$: \ three nested quantifiers", font_size=26, color=GREY_A).next_to(
            cont, DOWN, buff=0.25)
        rus = MathTex(r"\exists x\, (\mathrm{King}(x) \land \forall y\, (\mathrm{King}(y) \to y = x) \land "
                      r"\mathrm{Bald}(x))", font_size=36).move_to([0, -0.6, 0])
        rl = label(r"Russell (1905): \ `the king of France is bald'", font_size=26, color=GREY_A).next_to(rus, DOWN,
                                                                                                    buff=0.25)
        wall_ = label(r"this part's brick: \ validity is undecidable (Church, Turing 1936)", font_size=28,
                      color=P.WALL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The same notation writes mathematics. <bookmark mark='a'/>A function is continuous at a when for every "
            "epsilon there is a delta such that for every x, if x is within delta of a, then f of x is within "
            "epsilon of f of a. Three quantifiers, nested, in an order that matters. <bookmark mark='b'/>And it "
            "writes philosophy: Bertrand Russell's analysis of 'the present king of France is bald' is one sentence "
            "of first-order logic. <bookmark mark='c'/>This power has a price. Its brick in the Wall: in full "
            "first-order logic no machine can decide validity. Every valid argument can be confirmed by calculation, "
            "but on an invalid argument, proof search may run forever without returning a negative answer."
        ) as vo:
            self.play(Write(cont), FadeIn(cl))
            vo.wait_until("a")
            self.play(Indicate(cont, color=CONN))
            vo.wait_until("b")
            self.play(Write(rus), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(wall_))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Frege's notation; variables, quantifiers, and the scope of `all' and `some'",
            r"Tarski's definition of truth in a structure",
            r"counting, `the', and Aristotle's logic, all inside first-order logic",
            r"proofs with quantifiers, and tableaux that find countermodels",
            r"Gödel's completeness theorem; compactness; nonstandard numbers",
            r"Löwenheim--Skolem and Skolem's paradox; undecidability",
            r"second-order logic, Lindström's theorem, and Quine's criterion of existence",
        ], font_size=26)
        with self.voiceover(
            "So: <bookmark mark='a'/>Frege's notation, and what variables and quantifiers do. Tarski's definition of "
            "truth in a structure. <bookmark mark='b'/>How to say exactly 'at least two', 'the', and all of "
            "Aristotle's logic. <bookmark mark='c'/>Proofs with quantifiers, and trees that hunt for countermodels. "
            "Gödel's completeness theorem, and its strange consequences: numbers larger than all the natural "
            "numbers, and a countable model of the theory of uncountable sets. <bookmark mark='d'/>Then the limits: "
            "undecidability, second-order logic, Lindström's theorem on why this logic is special, and Quine's "
            "criterion of what exists."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, idx in (("a", [0, 1]), ("b", [2]), ("c", [3, 4]), ("d", [5, 6])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()
