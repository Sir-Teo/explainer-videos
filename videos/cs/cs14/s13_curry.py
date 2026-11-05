from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class CurryHoward(VoiceoverScene):
    def construct(self):
        self.card()
        self.dictionary()
        self.programs()
        self.missing()
        self.kripke()
        self.callcc()

    def card(self):
        card = chapter_card(12, r"Propositions as types", r"Is a type a theorem?", lit=(1969,),
                            extra=((1969, r"Unix; \ ARPANET; \ Howard's correspondence"),), part=PART)
        with self.voiceover("Chapter twelve. Propositions as types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dictionary(self):
        head = label(r"The Curry--Howard correspondence", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"$A \to B$: \ $A$ implies $B$", r"a function from $A$ to $B$"],
                [r"$A \land B$: \ $A$ and $B$", r"a pair: \ an $A$ and a $B$"],
                [r"$A \lor B$: \ $A$ or $B$", r"a tagged union: \ an $A$ or a $B$, \ and which"],
                [r"$\bot$: \ false", r"the empty type: \ no values at all"],
                [r"$\lnot A = A \to \bot$", r"a function that could never be called"],
                [r"a proof of $A$", r"a program of type $A$"],
                [r"simplifying a proof", r"running the program \ ($\beta$-reduction)"]]
        tab = grid_table([r"logic", r"programs"], rows, widths=[5.4, 6.4], row_h=0.55, font_size=22,
                         mono_cols=()).next_to(head, DOWN, buff=0.5)
        cap = label(r"Curry \ (1934, \ 1958) \ and Howard \ (1969, \ published 1980)", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.2)
        with self.voiceover(
            "Here is the deepest idea in this part. <bookmark mark='a'/> Read a type as a proposition. A function "
            "type, A to B, is the proposition A implies B, and a function of that type is a proof of it: give it "
            "evidence for A and it produces evidence for B. <bookmark mark='b'/> A pair is a proof of A and B. A "
            "tagged union, an A or a B together with which one, is a proof of A or B. The empty type, with no "
            "values at all, is falsehood, and not A is a function from A to the empty type, which could never "
            "actually be called. <bookmark mark='c'/> A proof is a program. And simplifying a proof, removing a "
            "detour through a lemma, is exactly running the program by beta reduction. Haskell Curry noticed the "
            "first signs of this in 1934; William Howard wrote it down in full in 1969."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[2:6]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[6])), FadeIn(VGroup(*tab.cells[7])), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def programs(self):
        c = load("curry")
        head = label(r"Proof search is program search", font_size=34).to_edge(UP, buff=0.3)
        names = ["K", "composition", "swap", "cases", "contraposition", "not not excluded middle"]
        rows, cols = [], []
        for r in c["rows"]:
            if r["name"] in names:
                rows.append([r["formula"], r["program"]])
                cols.append([WHITE, YES])
        tab = grid_table([r"theorem", r"the program our prover found"], rows, widths=[5.0, 7.0], row_h=0.55,
                         font_size=20, colors=cols, mono_cols=(0, 1)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"to prove $A \to B$, \ write a function: \ assume an $A$, \ build a $B$", font_size=21, color=GREY_A),
            label(r"$\lnot\lnot(A \lor \lnot A)$: \ a clever program for a theorem that looks classical", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "If proofs are programs, a theorem prover is a program synthesizer. <bookmark mark='a'/> Our prover "
            "searches for a lambda term of a given type. A implies B implies A is the function that takes x and "
            "y and returns x: the constant combinator. Composition proves the syllogism: from A implies B and B "
            "implies C, A implies C. Swapping a pair proves that and is commutative. Case analysis on a tagged "
            "union proves that or can be eliminated. <bookmark mark='b'/> And the last row is a small gem: not not "
            "of A or not A. It sounds like excluded middle, but it is provable without it. The program is a trick: "
            "it is handed a refutation x, and uses it against itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:-1]], lag_ratio=0.5), FadeIn(pts[0]),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[-1])), FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def missing(self):
        c = load("curry")
        head = label(r"True, \ but with no program", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in c["rows"]:
            if r["program"] is None:
                rows.append([r["name"], r["formula"], "true" if r["classical"] else "false", "none"])
                cols.append([WHITE, WHITE, YES, NO])
        tab = grid_table([r"law", r"formula", r"truth table", r"program"], rows, widths=[3.6, 4.4, 1.8, 1.6],
                         row_h=0.55, font_size=21, colors=cols, mono_cols=(1,)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"classically true: \ every row of the truth table", font_size=22, color=GREY_A),
            label(r"but no program has these types: \ \textbf{intuitionistic} logic, \ where a proof must construct",
                  font_size=22, color=HEAD),
            label(r"a program for $A \lor \lnot A$ would have to \textit{decide} $A$: \ for every $A$", font_size=22,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Some theorems of ordinary logic have no program at all. <bookmark mark='a'/> Excluded middle, A or "
            "not A. Double negation elimination. Peirce's law. And one half of de Morgan's laws. Every row of their "
            "truth tables comes out true. <bookmark mark='b'/> But our prover finds no program for any of them, "
            "and in a moment we will prove that none exists. The logic of programs is intuitionistic logic, in "
            "which a proof must construct what it claims. <bookmark mark='c'/> Think about what a program of type "
            "A or not A would have to do: return either evidence for A, or a refutation of A, and say which. For "
            "every proposition A. It would decide everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def kripke(self):
        c = load("curry")
        lem = next(r for r in c["rows"] if r["name"] == "excluded middle")
        head = label(r"Why none exists: \ a Kripke model", font_size=34).to_edge(UP, buff=0.3)
        w0 = VGroup(Circle(radius=0.55, color=DATA, fill_opacity=0.15), MathTex(r"w_0", font_size=30)).move_to(
            LEFT * 3.4 + DOWN * 1.2)
        w1 = VGroup(Circle(radius=0.55, color=YES, fill_opacity=0.15), MathTex(r"w_1", font_size=30)).move_to(
            LEFT * 3.4 + UP * 1.3)
        w0[1].move_to(w0[0])
        w1[1].move_to(w1[0])
        up = Arrow(w0[0].get_top(), w1[0].get_bottom(), buff=0.05, color=GREY_B)
        a1 = label(r"$A$ known", font_size=20, color=YES).next_to(w1, RIGHT, buff=0.3)
        a0 = label(r"$A$ not yet known", font_size=20, color=GREY_B).next_to(w0, RIGHT, buff=0.3)
        side = VGroup(
            label(r"worlds are states of knowledge; \ knowledge only grows, \ upward", font_size=21, color=GREY_A),
            label(r"at $w_0$: \ $A$ is not known", font_size=21, color=GREY_A),
            label(r"at $w_0$: \ $\lnot A$ is not known either, \ since $A$ becomes known at $w_1$", font_size=21,
                  color=GREY_A),
            label(r"so $A \lor \lnot A$ fails at $w_0$", font_size=22, color=NO),
            label(r"and anything with a program holds in every such model: \ no program for $A \lor \lnot A$",
                  font_size=21, color=HEAD),
            label(rf"found by our search: \ {lem['countermodel']['worlds']} worlds; \ de Morgan's half needs 3",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "To show that no program exists, we need a world where the formula fails and programs still make "
            "sense. Saul Kripke supplied one in 1965. <bookmark mark='a'/> Picture states of knowledge, which "
            "only grow, upward. In the lower world, w zero, we do not yet know A. In the world above it, we do. "
            "<bookmark mark='b'/> At w zero, A is not known. Not A is not known either, because not A would mean A "
            "can never become known, and above us it does. So A or not A fails at w zero. <bookmark mark='c'/> And "
            "every formula that has a program holds in every such model. So excluded middle has no program. Our "
            "search finds a two-world model like this for each of the first three laws, and a three-world model "
            "for de Morgan's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(w0), FadeIn(w1), GrowArrow(up), FadeIn(a0), FadeIn(a1))
            vo.wait_until("b")
            self.play(FadeIn(side[1:4]))
            vo.wait_until("c")
            self.play(FadeIn(side[4:]))
        self.wait(0.3)
        self.clear_scene()

    def callcc(self):
        head = label(r"Classical logic is control flow", font_size=34).to_edge(UP, buff=0.3)
        t = MathTex(r"\mathsf{call/cc} \;:\; ((A \to B) \to A) \to A", font_size=42, color=HEAD).next_to(head, DOWN,
                                                                                                    buff=0.6)
        pts = VGroup(
            label(r"Peirce's law \textit{is} the type of call-with-current-continuation \ (Griffin, \ 1990)",
                  font_size=23, color=GREY_A),
            label(r"a program that can jump back in time \ proves what a pure function cannot", font_size=23,
                  color=GREY_A),
            label(r"the continuation: \ ``the rest of the program'', \ made into a value \ (Part 15)", font_size=22,
                  color=YES),
            label(r"and propositions as types are the foundation of proof assistants: \ Lean, \ Rocq \ (Part 54)",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "There is a twist. <bookmark mark='a'/> In 1990 Timothy Griffin noticed that Peirce's law, which no "
            "pure function can prove, is exactly the type of an operator called call with current continuation. "
            "<bookmark mark='b'/> It captures the rest of the computation as a function, so a program can jump "
            "back and try again: it can promise an A, and if it is ever called on to deliver, change its answer. "
            "Classical logic corresponds to programs with control. <bookmark mark='c'/> Part 15 builds "
            "continuations. <bookmark mark='d'/> And propositions as types are the foundation of the proof "
            "assistants of Part 54, where checking a proof is type checking a program."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(t), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
