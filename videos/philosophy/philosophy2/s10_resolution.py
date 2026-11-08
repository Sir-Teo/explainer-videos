from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403
from explainer.philosophy.reasoner import prop

KN = ["a", "b", "c"]


def cm(c, font_size=30, color=WHITE):
    return MathTex(clause_tex(frozenset(c), KN), font_size=font_size, color=color)


class Resolution(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"One rule: resolution", r"Can a machine prove things with a single rule?",
                            lit=(1965,), part=PART)
        with self.voiceover("Chapter nine. One rule: resolution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rule()
        self.refutation()
        self.island()
        self.complete()

    def rule(self):
        r = MathTex(r"\dfrac{A \lor x \qquad B \lor \lnot x}{A \lor B}", font_size=64).move_to([0, 1.6, 0])
        r_x = VGroup()
        cases = VGroup(
            label(r"if $x$ is true, \ $B$ must hold", font_size=28, color=OK),
            label(r"if $x$ is false, \ $A$ must hold", font_size=28, color=OK),
            label(r"either way: \ $A \lor B$", font_size=30, color=GOAL)).arrange(DOWN, buff=0.25).move_to(
            [0, -0.8, 0])
        empty = VGroup(MathTex(r"\dfrac{x \qquad \lnot x}{\square}", font_size=56),
                       label(r"the empty clause: \ no valuation satisfies it", font_size=26, color=BAD)).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Natural deduction has ten rules, and needs a person to choose which to use next. Resolution has one "
            "rule, and a machine can apply it blindly. <bookmark mark='a'/>From a clause containing x, and a clause "
            "containing not x, infer the clause made of everything else. A or x; B or not x; therefore A or B. "
            "<bookmark mark='b'/>It is sound by cases. If x is true, the second clause needs B. <bookmark mark='c'/>If x "
            "is false, the first needs A. <bookmark mark='d'/>Either way, A or B. <bookmark mark='e'/>And when the two "
            "clauses are just x and not x, nothing is left: the empty clause, drawn as a box, which no valuation "
            "can satisfy. A contradiction, in its purest form."
        ) as vo:
            self.play(Write(r))
            vo.wait_until("a")
            self.play(Indicate(r, color=CONN, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(cases[0]))
            vo.wait_until("c")
            self.play(FadeIn(cases[1]))
            vo.wait_until("d")
            self.play(FadeIn(cases[2]))
            vo.wait_until("e")
            self.play(FadeIn(empty, shift=UP * 0.2))
        self.clear_scene()

    def refutation(self):
        steps = VGroup(
            label(r"1.\ \ premises $\Gamma$, and the \emph{negation} of the conclusion", font_size=30),
            label(r"2.\ \ everything into clauses (Chapter 5)", font_size=30),
            label(r"3.\ \ resolve, and resolve again", font_size=30),
            label(r"4.\ \ the empty clause appears: \ $\Gamma \models \varphi$", font_size=30, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-2.0, 0.3, 0])
        hcs = VGroup(history_card(1960, r"Martin Davis \& Hilary Putnam", r"resolution on propositional clauses",
                                  width=4.4, color=HIST, font_size=20),
                     history_card(1965, r"John Alan Robinson", r"one rule for all of first-order logic "
                                  r"(Part 3): the engine of automated reasoning", width=4.4, color=HIST,
                                  font_size=20)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Resolution proves things by refutation. <bookmark mark='a'/>To show that premises entail a conclusion, "
            "add the conclusion's negation, <bookmark mark='b'/>turn everything into clauses, <bookmark mark='c'/>and "
            "resolve until the empty clause appears. <bookmark mark='d'/>If it does, the premises and the negated "
            "conclusion cannot all be true: the conclusion follows. <bookmark mark='e'/>Martin Davis and Hilary Putnam "
            "used resolution on propositional clauses in 1960. In 1965 John Alan Robinson made it the single rule of "
            "a prover for the full logic of Part 3, and it has been the engine of automated reasoning ever since."
        ) as vo:
            self.play(FadeIn(steps[0], shift=RIGHT * 0.2))
            for k, mk in enumerate("bcd", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(steps[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(h, shift=LEFT * 0.2) for h in hcs], lag_ratio=0.4))
        self.clear_scene()

    def island(self):
        d = load("knights")
        base = [frozenset(c) for c in d["clauses"]]
        r = prop.resolution_refute(base + [frozenset([-2])])
        assert r["refuted"]
        proof = r["proof"]
        assert proof[-1][0] == frozenset() and {proof[-1][1], proof[-1][2]} == {frozenset([-3]), frozenset([3])}
        head = label(r"the island, as clauses", font_size=28, color=GREY_A)
        cls = VGroup(*[cm(c, font_size=30) for c in base]).arrange_in_grid(rows=5, cols=2, buff=(0.6, 0.22),
                                                                          cell_alignment=LEFT)
        neg = cm([-2], font_size=34, color=GOAL)
        negl = label(r"add: \ B is a knave (to refute)", font_size=24, color=GOAL)
        negg = VGroup(neg, negl).arrange(RIGHT, buff=0.3)
        left = VGroup(head, cls, negg).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.5)
        pos = {c: m for c, m in zip(base, cls)}
        pos[frozenset([-2])] = neg
        lines = VGroup()
        anims = []
        for i, (c, a, b) in enumerate(proof):
            row = VGroup(MathTex(rf"{i + 1}.", font_size=28, color=GREY_B),
                         cm(c, font_size=34, color=BAD if not c else OK),
                         MathTex(r"\Leftarrow", font_size=28, color=GREY_C),
                         cm(a, font_size=26, color=GREY_A), cm(b, font_size=26, color=GREY_A)).arrange(RIGHT,
                                                                                                    buff=0.25)
            lines.add(row)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.4, -0.2, 0])
        sol = label(r"so B is a knight", font_size=30, color=OK).next_to(lines, DOWN, buff=0.45)
        with self.voiceover(
            f"Back to the island. Our two equations become {len(base)} clauses. <bookmark mark='a'/>To prove that B is "
            "a knight, add the opposite, not b, and look for the empty clause. <bookmark mark='b'/>"
            f"The Reasoner finds a refutation in {len(proof)} steps. Each step resolves two clauses already on the "
            "board, which flash as they are used."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cls], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(FadeIn(negg, shift=UP * 0.2))
            vo.wait_until("b")
            for i, (c, a, b) in enumerate(proof):
                pa, pb = pos.get(a), pos.get(b)
                fl = [Indicate(m, color=GOAL, scale_factor=1.15) for m in (pa, pb) if m is not None]
                self.play(*fl, FadeIn(lines[i], shift=LEFT * 0.2), run_time=1.2)
                pos[c] = lines[i][1]
            self.play(FadeIn(sol))
        with self.voiceover(
            "Read it as an argument. A is a knave: the puzzle's clauses contain that directly, since a knight could "
            "never say 'we are all knaves'. Then, with B a knave, C would have to be both a knave and a knight. The "
            "box closes. B is a knight, as the table said, and now we know why."
        ):
            self.play(Indicate(lines[-1], color=BAD))
        self.clear_scene()

    def complete(self):
        thm = theorem_card(r"Refutation completeness", r"if a set of clauses is unsatisfiable, resolution derives "
                           r"the empty clause", who=r"Robinson 1965", width=7.4, font_size=26).move_to([0, 1.6, 0])
        d = load("solvers")["php"]
        rows = [r for r in d if "resolution_derived" in r]
        bars = bar_row([r["resolution_derived"] for r in rows],
                       [rf"{r['n'] + 1} pigeons, {r['n']} hole{'s' if r['n'] > 1 else ''}" for r in rows],
                       [BAD] * len(rows), width=5.2,
                       log=True, fmt=lambda v: f"{v:,}")
        bars.move_to([0, -1.6, 0])
        bl = label(r"resolvents generated, log scale (Chapter 12)", font_size=22, color=GREY_B).next_to(bars, UP,
                                                                                                    buff=0.2)
        with self.voiceover(
            "Resolution is refutation complete: if a set of clauses is unsatisfiable, resolution eventually derives "
            "the empty clause. So it, too, decides validity. <bookmark mark='a'/>But blind resolution can generate "
            "enormous numbers of clauses, and choosing which pair to resolve next is the whole art. Our resolver "
            "takes the shortest clauses first, and throws away any clause that says more than one it already has. "
            "Even so, on a family of formulas we will meet in Chapter twelve, the count explodes. The next two "
            "chapters search for models instead, and learn as they go."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(bars))
        self.clear_scene()
