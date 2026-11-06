from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono)


class Reductions(VoiceoverScene):
    def construct(self):
        self.card()
        self.poly()
        self.complete()
        self.search()

    def card(self):
        card = chapter_card(4, r"Reductions and completeness", r"How can one problem be as hard as all of them?",
                            lit=(1971, 1972), extra=((1971, r"Cook"), (1972, r"Karp")), part=PART)
        with self.voiceover("Chapter four. Reductions and completeness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def poly(self):
        head = label(r"$A \le_p B$: \ a \textbf{polynomial-time} $f$ with $\ x \in A \iff f(x) \in B$", font_size=30).to_edge(
            UP, buff=0.35)
        a = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=DATA).set_fill(DATA, 0.12)
        f = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=LAM).set_fill(LAM, 0.12)
        b = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=HEAD).set_fill(HEAD, 0.12)
        row = VGroup(a, f, b).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.8)
        tl = VGroup(label(r"instance $x$ of $A$", font_size=20, color=DATA).move_to(a),
                    label(r"compute $f(x)$", font_size=20, color=LAM).move_to(f),
                    label(r"solver for $B$", font_size=20, color=HEAD).move_to(b))
        ar = VGroup(Arrow(a.get_right(), f.get_left(), buff=0.1, color=GREY_B),
                    Arrow(f.get_right(), b.get_left(), buff=0.1, color=GREY_B))
        frame = DashedVMobject(SurroundingRectangle(VGroup(f, b), buff=0.25, color=YES), num_dashes=50)
        fl = label(r"a solver for $A$", font_size=20, color=YES).next_to(frame, UP, buff=0.1)
        lines = VGroup(
            label(r"same idea as Part 25, \ with a budget: \ $f$ must run in polynomial time", font_size=22,
                  color=WHITE),
            label(r"if $B \in$ P then $A \in$ P: \ polynomial of a polynomial", font_size=22, color=YES),
            label(r"read backwards: \ if $A$ is hard, \ $B$ is at least as hard", font_size=22, color=NO),
            label(r"reductions compose: \ $A \le_p B$ and $B \le_p C$ give $A \le_p C$", font_size=22, color=DATA),
        ).arrange(DOWN, buff=0.28).next_to(row, DOWN, buff=0.8)
        with self.voiceover(
            "Part 25 carried impossibility from problem to problem with reductions. Here they get a budget. "
            "<bookmark mark='a'/> A reduces to B in polynomial time if a polynomial-time function f turns every "
            "instance of A into an instance of B with the same answer. <bookmark mark='b'/> Then a fast solver for "
            "B gives a fast solver for A: compute f, and ask. A polynomial applied to a polynomial is still a "
            "polynomial. <bookmark mark='c'/> Read the other way, if A is hard, then B is at least as hard. "
            "<bookmark mark='d'/> And reductions chain: if A reduces to B and B to C, then A reduces to C."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(x) for x in ar], lag_ratio=0.4), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(fl), FadeIn(lines[1]))
            for mk, ln in zip("cd", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def complete(self):
        head = label(r"Hardness and completeness", font_size=34).to_edge(UP, buff=0.35)
        np_ = Ellipse(width=5.2, height=4.0, color=HEAD).set_fill(HEAD, 0.06).shift(LEFT * 4.0 + DOWN * 0.5)
        p_ = Ellipse(width=2.0, height=1.4, color=DATA).set_fill(DATA, 0.15).move_to(np_.get_center() + LEFT * 1.2
                                                                                   + DOWN * 0.6)
        npc = Ellipse(width=2.0, height=1.3, color=NO).set_fill(NO, 0.2).move_to(np_.get_center() + RIGHT * 1.2
                                                                               + UP * 0.6)
        lab = VGroup(label(r"NP", font_size=24, color=HEAD).next_to(np_.get_top(), DOWN, buff=0.15),
                     label(r"P", font_size=24, color=DATA).move_to(p_),
                     label(r"NP-complete", font_size=20, color=NO).move_to(npc))
        dots_ = VGroup(*[Dot(np_.get_center() + np.array([x, y, 0]), radius=0.05, color=GREY_B)
                         for x, y in ((-1.9, 0.4), (-0.3, 1.1), (0.2, -1.2), (-0.9, 0.6), (0.9, -0.6), (1.8, -0.4))])
        arrows = VGroup(*[Arrow(d.get_center(), npc.get_center(), buff=0.12, stroke_width=1.5, color=GREY_C,
                                max_tip_length_to_length_ratio=0.12) for d in dots_])
        lines = VGroup(
            label(r"$B$ is \textbf{NP-hard} if every problem in NP reduces to it", font_size=22, color=WHITE),
            label(r"\textbf{NP-complete}: \ NP-hard and in NP", font_size=22, color=NO),
            label(r"one NP-complete problem in P \ $\Rightarrow$ \\ every NP problem in P: \ P = NP", font_size=22,
                  color=YES),
            label(r"one NP-complete problem \textbf{not} in P \ $\Rightarrow$ \ none of them is", font_size=22,
                  color=NO),
            label(r"but does any NP-complete problem exist? \\ That needs a reduction \textbf{from every} NP "
                  r"problem at once", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(np_, RIGHT, buff=0.4).shift(UP * 0.2)
        if lines.get_right()[0] > 6.9:
            left = lines.get_left()[0]
            lines.width = 6.9 - left
            lines.shift(RIGHT * (left - lines.get_left()[0]))
        with self.voiceover(
            "Now the key definitions. <bookmark mark='a'/> A problem is NP-hard if every problem in NP reduces to "
            "it. <bookmark mark='b'/> It is NP-complete if, in addition, it is in NP itself: the hardest problems in "
            "the class. <bookmark mark='c'/> If any single NP-complete problem had a polynomial algorithm, then by "
            "composing reductions every problem in NP would, and P would equal NP. <bookmark mark='d'/> If any one "
            "of them provably has no polynomial algorithm, then none of them does. <bookmark mark='e'/> But it is "
            "not obvious that NP-complete problems exist at all. To prove one, you need a reduction from every "
            "problem in NP simultaneously, including ones nobody has thought of yet. That is what Stephen Cook and "
            "Leonid Levin did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(np_), FadeIn(p_), FadeIn(lab[0]), FadeIn(lab[1]), FadeIn(dots_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.1), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(npc), FadeIn(lab[2]), FadeIn(lines[1]))
            for mk, ln in zip("cde", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def search(self):
        d = load("selfreduce")
        head = label(r"Deciding is enough: \ search reduces to decision", font_size=32).to_edge(UP, buff=0.35)
        rows = VGroup()
        for st in d["steps"]:
            t = rf"set $x_{st['var']}$ = {'1' if st['value'] else '0'}: \ still satisfiable? \ " + (
                r"\textbf{yes}, keep it" if st["kept"] else r"no, \ so $x_" + str(st["var"]) + r"$ = "
                + ("0" if st["value"] else "1"))
            rows.add(label(t, font_size=21, color=YES if st["kept"] else NO))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        res = label(r"result: \ " + ", \\ ".join(rf"$x_{i + 1}$ = {int(b)}" for i, b in enumerate(d["model"]))
                    + rf"; \ {d['calls']} calls to the decision procedure", font_size=21,
                    color=HEAD).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        notes = VGroup(
            label(r"fix one variable at a time; \\ ask the yes/no oracle \\ whether the rest is still satisfiable",
                  font_size=21, color=WHITE),
            label(r"$n$ questions find a solution: \\ \textbf{self-reducibility}", font_size=21, color=YES),
            label(r"so P = NP would give fast \\ \textbf{finding}, \ not just fast \\ \textbf{deciding}",
                  font_size=21, color=DATA),
            label(r"true of every NP-complete problem; \\ factoring is the odd one out: \\ deciding "
                  r"``is $N$ composite?'' \\ is easy, \ finding a factor is not", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        with self.voiceover(
            "One more consequence of completeness. NP is defined by yes-or-no questions, but we usually want the "
            "solution itself. <bookmark mark='a'/> Suppose we only had a decision procedure for SAT. Set the first "
            "variable to one and ask whether the formula is still satisfiable. If yes, keep it; if not, it must be "
            "zero. Then the next variable. <bookmark mark='b'/> On the small formula that chapter six will use, five questions, one to "
            "check and one per variable, produce a satisfying assignment. This is called self-reducibility. <bookmark mark='c'/> So a fast decision "
            "procedure would give fast search too: P equal to NP would mean finding, not just deciding. <bookmark "
            "mark='d'/> Every NP-complete problem behaves this way. Factoring is the interesting exception: deciding "
            "whether a number is composite is easy, as chapter three said, but finding a factor seems hard."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(res), FadeIn(notes[1]))
            for mk, n_ in zip("cd", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
