from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def sem(e: str) -> str:
    """The semantic brackets (TeX)."""
    return r"[\![\," + e + r"\,]\!]"


def M(s, fs=28, color=WHITE):
    return MathTex(s, font_size=fs, color=color)


def rule(prems, concl, name=None, color=GREY_B, name_color=GREY_B, buff=0.5, fs=20):
    """An inference rule: premises above a line, the conclusion below, the rule's name to the right."""
    p = VGroup(*prems).arrange(RIGHT, buff=buff, aligned_edge=DOWN) if prems else VGroup()
    w = max(p.width if prems else 0.0, concl.width) + 0.25
    line = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=2, color=color)
    concl.next_to(line, DOWN, buff=0.12)
    if prems:
        p.next_to(line, UP, buff=0.12)
    nm = label(name, font_size=fs, color=name_color).next_to(line, RIGHT, buff=0.12) if name else VectorizedPoint(
        line.get_right())
    g = VGroup(p, line, concl, nm)
    g.prem, g.line, g.concl, g.name = p, line, concl, nm
    return g


def cell(v, w=0.5, h=0.4, fs=20):
    r = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.2, fill_color=BG, fill_opacity=1)
    t = MathTex(r"\bot" if v is None else str(v), font_size=fs, color=GREY_C if v is None else YES)
    if t.width > w - 0.06:
        t.scale_to_fit_width(w - 0.06)
    return VGroup(r, t.move_to(r))


def fact_loop(n: int):
    """The states of  while x > 0 do (y := y * x; x := x - 1)  from x = n, y = 1."""
    x, y, out = n, 1, [(n, 1)]
    while x > 0:
        y, x = y * x, x - 1
        out.append((x, y))
    return out


def stepwise(self, rows, whys, marks, vo, run_time=1.3):
    """Write the first row, then grow each next row from a copy of the previous one at its bookmark."""
    self.play(Write(rows[0]), FadeIn(whys[0]))
    for k, mk in enumerate(marks, start=1):
        vo.wait_until(mk)
        self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=run_time)


class Axiomatic(VoiceoverScene):
    def construct(self):
        self.card()
        self.triples()
        self.machine()
        self.assign()
        self.loop()
        self.scott()
        self.completeness()

    def card(self):
        card = chapter_card(7, r"Hoare logic, \ proved sound", r"Why should we believe the rules?",
                            lit=(1969, 1978), extra=((1969, r"Hoare: \ an axiomatic basis for computer programming"),
                                                     (1978, r"Cook: \ soundness and relative completeness")),
                            part=PART)
        with self.voiceover("Chapter seven. Hoare logic, proved sound. Why should we believe the rules?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ derivable against true
    def triples(self):
        head = label(r"Derivable, \ and true", font_size=36).to_edge(UP, buff=0.3)
        fs = 24
        tree = rule([M(r"\{x > 4\}\ x := x + 1\ \{x > 5\}", fs), M(r"\{x > 5\}\ y := x\ \{y > 5\}", fs)],
                    M(r"\{x > 4\}\ x := x + 1;\ y := x\ \{y > 5\}", fs, HEAD), r"\textsc{Seq}", buff=0.35)
        lt = label(r"$\vdash$: \ a derivation, \ built from the rules", font_size=21, color=HEAD)
        left = VGroup(lt, tree).arrange(DOWN, buff=0.35).move_to([-3.5, 1.5, 0])
        if left.get_left()[0] < -6.8:
            left.shift(RIGHT * (-6.8 - left.get_left()[0]))
        eP = Ellipse(width=1.7, height=2.2, color=DATA, stroke_width=2).move_to([2.6, 1.2, 0])
        eQ = Ellipse(width=1.7, height=2.2, color=YES, stroke_width=2).move_to([5.6, 1.2, 0])
        lP = MathTex("P", font_size=28, color=DATA).next_to(eP, UP, buff=0.1)
        lQ = MathTex("Q", font_size=28, color=YES).next_to(eQ, UP, buff=0.1)
        ds = VGroup(*[Dot(eP.get_center() + UP * dy + RIGHT * dx, radius=0.06, color=DATA)
                      for dx, dy in ((-0.25, 0.55), (0.2, 0.0), (-0.15, -0.55))])
        de = VGroup(*[Dot(eQ.get_center() + UP * dy + RIGHT * dx, radius=0.06, color=YES)
                      for dx, dy in ((0.2, 0.5), (-0.2, 0.05), (0.15, -0.6))])
        runs = VGroup(*[Arrow(a.get_center(), b.get_center(), buff=0.1, color=GREY_B, stroke_width=2,
                              max_tip_length_to_length_ratio=0.08) for a, b in zip(ds, de)])
        rl = MathTex(r"\langle c, \sigma \rangle \Downarrow \sigma'", font_size=22, color=GREY_B).next_to(
            runs, UP, buff=0.05).shift(UP * 0.55)
        rt = label(r"$\models$: \ every run from $P$ that ends, \ ends in $Q$", font_size=21, color=YES)
        rt.next_to(VGroup(eP, eQ), UP, buff=0.5)
        dfn = MathTex(r"\models \{P\}\,c\,\{Q\}", r"\iff", r"\sigma \models P \ \text{ and } \ \langle c, \sigma "
                      r"\rangle \Downarrow \sigma' \implies \sigma' \models Q", font_size=30, color=WHITE)
        dfn.move_to([0, -1.0, 0])
        thms = VGroup(
            VGroup(MathTex(r"\vdash \{P\}\,c\,\{Q\}", r"\implies", r"\models \{P\}\,c\,\{Q\}", font_size=32,
                           color=YES), label(r"soundness: \ the rules never lie", font_size=21, color=YES)).arrange(
                RIGHT, buff=0.5),
            VGroup(MathTex(r"\models \{P\}\,c\,\{Q\}", r"\implies", r"\vdash \{P\}\,c\,\{Q\}", font_size=32,
                           color=KERN), label(r"relative completeness \ (Cook, \ 1978)", font_size=21,
                                              color=KERN)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(dfn, DOWN, buff=0.5)
        ill = note(r"illustrative triples", font_size=16).next_to(tree, DOWN, buff=0.15).align_to(tree, RIGHT)
        with self.voiceover(
            "Part fifty-four used Hoare's rules to prove programs correct. But the rules are symbols on paper. Why "
            "believe them? <bookmark mark='a'/> A triple can be derivable: built from the rules, like this sequence "
            "of two assignments. <bookmark mark='b'/> Or it can be true: every run of the program that starts in a "
            "state satisfying P, and ends, ends in a state satisfying Q. <bookmark mark='c'/> Truth is defined by "
            "the operational semantics, the steps of chapter one, now for commands. <bookmark mark='d'/> Soundness "
            "says every derivable triple is true. And Stephen Cook showed in nineteen seventy-eight the converse, "
            "with a precise proviso we will come to: every true triple is derivable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(tree.prem))
            self.play(Create(tree.line), FadeIn(tree.name), FadeIn(tree.concl), FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(rt), Create(eP), Create(eQ), FadeIn(lP), FadeIn(lQ), FadeIn(ds))
            self.play(LaggedStart(*[GrowArrow(a) for a in runs], lag_ratio=0.3), FadeIn(rl), FadeIn(de))
            vo.wait_until("c")
            self.play(Write(dfn))
            vo.wait_until("d")
            self.play(FadeIn(thms[0]))
            self.play(FadeIn(thms[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the big-step machine for commands
    def machine(self):
        head = label(r"Big steps for commands", font_size=36).to_edge(UP, buff=0.3)
        fs = 26
        r1 = rule([], M(r"\langle x := e,\ \sigma \rangle \Downarrow \sigma[x \mapsto " + sem("e") + r"\sigma]", fs),
                  r"\textsc{Assign}")
        r2 = rule([M(r"\langle c_1, \sigma \rangle \Downarrow \sigma_1", fs),
                   M(r"\langle c_2, \sigma_1 \rangle \Downarrow \sigma'", fs)],
                  M(r"\langle c_1; c_2,\ \sigma \rangle \Downarrow \sigma'", fs), r"\textsc{Seq}", buff=0.4)
        r3 = rule([M(sem("b") + r"\sigma = \mathsf{false}", fs)],
                  M(r"\langle \mathsf{while}\ b\ \mathsf{do}\ c,\ \sigma \rangle \Downarrow \sigma", fs),
                  r"\textsc{While-F}")
        loopprem = M(r"\langle \mathsf{while}\ b\ \mathsf{do}\ c,\ \sigma_1 \rangle \Downarrow \sigma'", fs)
        r4 = rule([M(sem("b") + r"\sigma = \mathsf{true}", fs), M(r"\langle c, \sigma \rangle \Downarrow \sigma_1", fs),
                   loopprem],
                  M(r"\langle \mathsf{while}\ b\ \mathsf{do}\ c,\ \sigma \rangle \Downarrow \sigma'", fs),
                  r"\textsc{While-T}", buff=0.4)
        top = VGroup(r1, r2).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        mid = VGroup(r3).set_x(0)
        rs = VGroup(top, mid, r4).arrange(DOWN, buff=0.55).next_to(head, DOWN, buff=0.4)
        for g in (top, r4):
            if g.width > 13.2:
                g.scale_to_fit_width(13.2)
        rs.set_x(0)
        box = SurroundingRectangle(loopprem, buff=0.08, color=KERN, stroke_width=2)
        bl = wrapped_label(r"the loop reappears in its own premise: \ proofs about loops go by induction on the "
                           r"\textit{derivation}, \ which shrinks, \ not on the program, \ which does not", 11.5,
                           font_size=21, color=KERN).next_to(rs, DOWN, buff=0.45)
        other = label(r"plus \textsc{Skip} and two rules for \textsf{if}; \ $\sigma$ a state, \ "
                      r"$[\![\,e\,]\!]\sigma$ the value of $e$ in it", font_size=19, color=GREY_B).next_to(
            bl, DOWN, buff=0.25)
        with self.voiceover(
            "First, the meaning of commands, in big steps. A state, sigma, gives every variable a value. <bookmark "
            "mark='a'/> Assignment updates one variable. A sequence runs the first command, then the second from "
            "where the first left off. <bookmark mark='b'/> A loop whose test is false stops at once. <bookmark "
            "mark='c'/> A loop whose test is true runs its body once, then runs the whole loop again. <bookmark "
            "mark='d'/> Notice that the loop reappears in its own premise. A proof about loops cannot go by "
            "induction on the program, which does not shrink; it goes by induction on the derivation of the run, "
            "which does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1, shift=DOWN * 0.15))
            self.play(FadeIn(r2, shift=DOWN * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(r3, shift=DOWN * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(r4, shift=DOWN * 0.15))
            vo.wait_until("d")
            self.play(Create(box), FadeIn(bl))
            self.play(FadeIn(other))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ soundness: assignment
    def assign(self):
        head = label(r"Soundness, \ by induction on the derivation", font_size=36).to_edge(UP, buff=0.3)
        goal = MathTex(r"\text{case } \textsc{Assign}:\quad \models \{Q[e/x]\}\ x := e\ \{Q\}", font_size=30,
                       color=HEAD).next_to(head, DOWN, buff=0.35)
        fs = 30
        rows = VGroup(
            M(r"\sigma \models Q[e/x]", fs),
            M(sem("Q[e/x]") + r"\,\sigma = \mathsf{true}", fs),
            M(sem("Q") + r"\,\big(\sigma[x \mapsto " + sem("e") + r"\sigma]\big) = \mathsf{true}", fs),
            M(r"\sigma[x \mapsto " + sem("e") + r"\sigma] \models Q", fs),
            M(r"\sigma' \models Q", fs + 2, YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(goal, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        whys = VGroup(
            label(r"assume the precondition", font_size=22, color=GREY_B),
            label(r"what $\models$ means", font_size=20, color=GREY_B),
            label(r"substitution lemma \ (induction on $Q$)", font_size=20, color=YES),
            label(r"what $\models$ means", font_size=20, color=GREY_B),
            label(r"\textsc{Assign} allows exactly one final state", font_size=20, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.6
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        if whys.get_right()[0] > 6.85:
            whys.shift(LEFT * (whys.get_right()[0] - 6.85))
        others = VGroup(
            label(r"\textsc{Seq}: \ $\sigma \models P$ gives $\sigma_1 \models R$ \ (hypothesis for $c_1$), \ then "
                  r"$\sigma' \models Q$ \ (hypothesis for $c_2$)", font_size=20, color=WHITE),
            label(r"\textsc{Consequence}: \ $P \Rightarrow P'$ \ and \ $Q' \Rightarrow Q$ \ are true assertions: \ "
                  r"logic alone", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        if others.width > 13.2:
            others.scale_to_fit_width(13.2)
        with self.voiceover(
            "Soundness is proved by induction on the derivation of the triple, one case per rule. <bookmark "
            "mark='a'/> Assignment first, the rule that runs backwards. Suppose the state satisfies Q with e put "
            "in place of x. <bookmark mark='b'/> That is, the assertion evaluates to true in sigma. <bookmark "
            "mark='c'/> A substitution lemma, proved by induction on the assertion, moves the substitution into the "
            "state: Q is true once x is updated to the value of e. <bookmark mark='d'/> So the updated state "
            "satisfies Q. <bookmark mark='e'/> And by the assignment rule that updated state is the only possible "
            "final state. <bookmark mark='f'/> Sequencing chains the two hypotheses through the middle state, and "
            "consequence is pure logic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(goal))
            vo.wait_until("a")
            stepwise(self, rows, whys, "bcde", vo)
            self.play(Circumscribe(rows[-1], color=YES))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(t) for t in others], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ soundness: the while case
    def loop(self):
        n = load("fact")["n"]
        st = fact_loop(n)
        assert st[-1][1] == load("fact")["value"]
        head = label(r"The while case: \ an induction inside the induction", font_size=36).to_edge(UP, buff=0.3)
        goal = MathTex(r"\models \{I \wedge b\}\ c\ \{I\}", r"\implies", r"\models \{I\}\ \mathsf{while}\ b\ "
                       r"\mathsf{do}\ c\ \{I \wedge \neg b\}", font_size=30, color=WHITE).next_to(head, DOWN, buff=0.3)
        goal[0].set_color(GREY_A)
        prog = VGroup(mono("while x > 0 do (y := y * x; x := x - 1)", size=19, color=WHITE),
                      MathTex(rf"I \equiv x \ge 0 \ \wedge\ y \cdot x! = {n}!", font_size=28, color=YES)).arrange(
            RIGHT, buff=0.7).next_to(goal, DOWN, buff=0.35)
        boxes = VGroup()
        for x, y in st:
            t = MathTex(rf"x = {x},\ y = {y}", font_size=24, color=WHITE)
            b = RoundedRectangle(width=t.width + 0.4, height=0.6, corner_radius=0.1, stroke_color=GREY_B,
                                 stroke_width=1.8, fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.85).move_to([0, 0.05, 0])
        if boxes.width > 13.4:
            boxes.scale_to_fit_width(13.4)
        arrs = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.06, color=GREY_B,
                              stroke_width=2.4) for k in range(len(st) - 1)])
        cl = VGroup(*[MathTex("c", font_size=24, color=GREY_B).next_to(a, UP, buff=0.05) for a in arrs])
        tests = VGroup(*[MathTex(r"b" if x > 0 else r"\neg b", font_size=26, color=YES if x > 0 else NO).next_to(
            bx, UP, buff=0.15) for (x, _), bx in zip(st, boxes)])
        invs = VGroup(*[MathTex(rf"I:\ {y} \cdot {x}! = {n}!\ \checkmark", font_size=22, color=YES).next_to(
            bx, DOWN, buff=0.15) for (x, y), bx in zip(st, boxes)])
        ex = label(rf"leaves with $I \wedge \neg b$: \ $x = 0$, \ so $y = {n}! = {st[-1][1]}$", font_size=22,
                   color=YES).next_to(invs, DOWN, buff=0.3)
        cases = VGroup(
            label(r"induction on the derivation of $\langle \mathsf{while}\ b\ \mathsf{do}\ c, \sigma\rangle "
                  r"\Downarrow \sigma'$:", font_size=21, color=WHITE),
            label(r"\textsc{While-F}: \ $\sigma' = \sigma$, \ $I$ holds and $b$ is false", font_size=20, color=NO),
            label(r"\textsc{While-T}: \ the body keeps $I$ \ (outer hypothesis), \ then the shorter derivation "
                  r"from $\sigma_1$ \ (inner hypothesis)", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ex, DOWN, buff=0.3)
        if cases.width > 13.2:
            cases.scale_to_fit_width(13.2)
        if cases.get_bottom()[1] < -3.75:
            cases.shift(UP * (-3.75 - cases.get_bottom()[1]))
        ill = note(r"illustrative loop: \ factorial, \ as in chapter one", font_size=16).to_corner(DR, buff=0.15)
        with self.voiceover(
            "The loop rule is the heart of the proof. Our outer hypothesis: the body, started with the invariant "
            "and the test true, keeps the invariant. We must show the loop keeps it, and leaves with the test false."
            " <bookmark mark='a'/> Take factorial as a loop, with invariant: x is not negative, and y times x "
            "factorial is three factorial. <bookmark mark='b'/> Run it from x equals three. <bookmark mark='c'/> "
            "Each pass of the body starts with the test true and the invariant holding, so the outer hypothesis "
            "gives the invariant again. <bookmark mark='d'/> When the test fails, the loop stops, with the invariant "
            "and not the test: y is six. <bookmark mark='e'/> The proof does the same by an inner induction, on the"
            " derivation of the loop's run. If the loop stopped at once, the invariant still holds. Otherwise the "
            "body keeps it, and the rest of the run has a shorter derivation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(goal))
            vo.wait_until("a")
            self.play(FadeIn(prog), FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(boxes[0]), FadeIn(tests[0]), FadeIn(invs[0]))
            vo.wait_until("c")
            for k in range(len(arrs)):
                self.play(GrowArrow(arrs[k]), FadeIn(cl[k]), FadeIn(boxes[k + 1]), run_time=0.7)
                self.play(FadeIn(tests[k + 1]), FadeIn(invs[k + 1]), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(ex), boxes[-1][0].animate.set_stroke(color=YES))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(t) for t in cases], lag_ratio=0.5), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the same proof, by fixed-point induction
    def scott(self):
        rows_k = load("kleene")["rows"]
        head = label(r"The same proof, \ against the denotation", font_size=36).to_edge(UP, buff=0.3)
        fs = 27
        eqs = VGroup(
            M(sem(r"\mathsf{while}\ b\ \mathsf{do}\ c") + r"= \mathrm{fix}\,\Phi", fs, DATA),
            M(r"\Phi(w)\,\sigma = \begin{cases} w(" + sem("c") + r"\sigma) & \text{if } " + sem("b") + r"\sigma \\ "
              r"\sigma & \text{otherwise} \end{cases}", fs, DATA),
            M(r"S(w):\ \ \sigma \models I \ \text{ and } \ w(\sigma) \neq \bot \implies w(\sigma) \models I \wedge "
              r"\neg b", fs, HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        fs2 = 28
        rows = VGroup(
            M(r"S(\bot)", fs2),
            M(r"S(w) \implies S(\Phi\,w)", fs2),
            M(r"S(\Phi^k(\bot)) \ \text{ for every } k", fs2),
            M(r"S\big(\textstyle\bigsqcup_k \Phi^k(\bot)\big)", fs2),
            M(r"S(" + sem(r"\mathsf{while}\ b\ \mathsf{do}\ c") + r")", fs2 + 2, YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(eqs, DOWN, buff=0.35).align_to(eqs, LEFT)
        whys = VGroup(
            label(r"vacuous: \ $\bot$ never answers", font_size=19, color=GREY_B),
            label(r"the hypothesis for the body $c$", font_size=19, color=GREY_B),
            label(r"induction on $k$", font_size=19, color=GREY_B),
            label(r"$S$ is closed under limits of chains", font_size=19, color=YES),
            label(r"Scott's fixed-point induction", font_size=19, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.4
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        ks = range(5)
        x0 = 3.0
        ys = [-2.4 + 1.0 * k for k in ks]
        strips = VGroup(*[VGroup(*[cell(v) for v in rows_k[k]["table"][:5]]).arrange(RIGHT, buff=0.04).move_to(
            [x0 + 1.4, y, 0]) for k, y in zip(ks, ys)])
        names = VGroup(*[MathTex(r"\bot" if k == 0 else (r"\Phi(\bot)" if k == 1 else rf"\Phi^{{{k}}}(\bot)"),
                                 font_size=22, color=DATA).next_to(strips[k], LEFT, buff=0.2) for k in ks])
        ticks = VGroup(*[VGroup(*[MathTex(r"\checkmark", font_size=16, color=YES).next_to(c, DOWN, buff=0.03)
                                  for c, v in zip(strips[k], rows_k[k]["table"][:5]) if v is not None])
                         for k in ks])
        idx = VGroup(*[MathTex(str(i), font_size=18, color=GREY_B).next_to(c, UP, buff=0.06)
                       for i, c in enumerate(strips[-1])])
        xl = MathTex(r"x =", font_size=18, color=GREY_B).next_to(idx, LEFT, buff=0.15)
        cap = wrapped_label(r"the loop's iterates from $x = n,\ y = 1$: \ final $y$ \ (the numbers of chapter "
                            r"three's chain)", 3.6, font_size=18, color=GREY_B).next_to(idx, UP, buff=0.15)
        right = VGroup(strips, names, ticks, idx, xl, cap)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        if whys.get_right()[0] > right.get_left()[0] - 0.2:
            VGroup(eqs, rows, whys).scale((right.get_left()[0] - 0.2 + 6.7) / (whys.get_right()[0] + 6.7),
                                          about_point=np.array([-6.7, 0, 0]))
        with self.voiceover(
            "The same theorem can be proved against chapter two's denotation instead. <bookmark mark='a'/> There, "
            "a loop means the least fixed point of a functional, phi: test, and either run the body and continue, "
            "or stop. <bookmark mark='b'/> Call a meaning w safe if, from any state satisfying the invariant, "
            "whenever it answers at all, it answers with the invariant and not the test. <bookmark mark='c'/> "
            "Bottom is safe: it never answers. <bookmark mark='d'/> Phi preserves safety, by the hypothesis for the"
            " body. <bookmark mark='e'/> So every approximation in the Kleene chain is safe. <bookmark mark='f'/> "
            "Safety is a property closed under limits of chains, so the limit is safe, <bookmark mark='g'/> and the"
            " limit is the loop. This is Scott's fixed-point induction; it is exactly chapter four's admissibility "
            "again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(FadeIn(cap), FadeIn(idx), FadeIn(xl), FadeIn(names[0]), FadeIn(strips[0]))
            stepwise(self, rows, whys, "de", vo)
            for k in range(1, 5):
                self.play(FadeIn(names[k]), FadeIn(strips[k]), FadeIn(ticks[k]), run_time=0.6)
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]), run_time=1.3)
            vo.wait_until("g")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(whys[4]), run_time=1.3)
            self.play(Circumscribe(rows[4], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Cook: relative completeness
    def completeness(self):
        head = label(r"Cook: \ complete, \ relative to arithmetic", font_size=36).to_edge(UP, buff=0.3)
        fs = 32
        rows = VGroup(
            M(r"\vdash \{\mathrm{wlp}(c, Q)\}\ c\ \{Q\}", fs),
            M(r"I = \mathrm{wlp}(\mathsf{while}\ b\ \mathsf{do}\ c,\ Q)", fs),
            M(r"I \wedge b \Rightarrow \mathrm{wlp}(c, I), \quad I \wedge \neg b \Rightarrow Q", fs),
            M(r"\models \{P\}\,c\,\{Q\} \iff \big(P \Rightarrow \mathrm{wlp}(c, Q)\big)", fs),
            M(r"\vdash \{P\}\,c\,\{Q\}", fs + 4, YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        whys = VGroup(
            label(r"by induction on $c$", font_size=21, color=GREY_B),
            label(r"the while case: \ the invariant is the wlp itself", font_size=21, color=HEAD),
            label(r"both true, \ so \textsc{While} applies", font_size=21, color=GREY_B),
            label(r"the definition of wlp", font_size=21, color=GREY_B),
            label(r"\textsc{Consequence}, \ with $P \Rightarrow \mathrm{wlp}$ as an axiom", font_size=21,
                  color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.4
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        wl = label(r"$\mathrm{wlp}(c, Q)$: \ the states from which $c$ ends in $Q$ or runs forever", font_size=19,
                   color=GREY_A).next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT)
        right = VGroup(
            label(r"why only \textit{relative}:", font_size=22, color=NO),
            MathTex(r"\models \{\mathsf{true}\}\ \mathsf{skip}\ \{P\} \iff P \text{ is true}", font_size=26,
                    color=WHITE),
            wrapped_label(r"so a complete proof system would list every true statement of arithmetic, \ which "
                          r"G\"odel's theorem \ (1931) \ rules out", 4.4, font_size=19, color=GREY_A),
            wrapped_label(r"Cook's proviso: \ true assertions are given, \ and assertions can express wlp \ "
                          r"(arithmetic can, \ by G\"odel's coding of sequences)", 4.4, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        right.to_edge(RIGHT, buff=0.3).set_y(-0.6)
        frame = SurroundingRectangle(right, buff=0.2, corner_radius=0.1, color=GREY_D, stroke_width=1.5)
        if whys.get_right()[0] > frame.get_left()[0] - 0.2:
            VGroup(rows, whys, wl).scale((frame.get_left()[0] - 0.2 + 6.7) / (whys.get_right()[0] + 6.7),
                                         about_point=np.array([-6.7, rows.get_y(), 0]))
        foot = label(r"Part 54's tools generate the verification conditions; \ this chapter is why their rules are "
                     r"right", font_size=20, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the converse. Cook's idea is to use the weakest liberal precondition: the states from which the "
            "command either ends in Q, or runs forever. <bookmark mark='a'/> By induction on the command, the triple"
            " with wlp in front is derivable. <bookmark mark='b'/> In the while case, the invariant nobody had to "
            "invent is the loop's wlp itself, <bookmark mark='c'/> and both premises of the loop rule are true. "
            "<bookmark mark='d'/> A true triple means P implies the wlp, <bookmark mark='e'/> so consequence "
            "finishes the proof. <bookmark mark='f'/> Why only relative? A true triple with skip is just a true "
            "statement of arithmetic, and by Gödel no proof system lists them all. So Cook assumes the true "
            "assertions are given, and that assertions can express wlp. <bookmark mark='g'/> Part fifty-four's "
            "tools discharge exactly those assertions; this chapter is why their rules are right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(wl))
            vo.wait_until("a")
            stepwise(self, rows, whys, "bcde", vo)
            vo.wait_until("f")
            self.play(Create(frame), LaggedStart(*[FadeIn(t) for t in right], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.wait(0.6)
        self.clear_scene()


_ = (LAM, DATA)
