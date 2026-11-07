from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono


def tx(s: str) -> str:
    """One of the instrument's assertions (unicode) as LaTeX: multi-letter names upright-italic, primes kept."""
    s = re.sub(r"\b([A-Za-z]+)'(\d+)", r"\1'_{\2}", s)
    s = re.sub(r"\b([A-Za-z]{2,})\b", r"\\mathit{\1}", s)
    for a, b in ((">>>", r" \mathbin{>\!\!>\!\!>} "), (">>", r" \mathbin{>\!\!>} "), ("≥", r" \ge "),
                 ("≤", r" \le "), ("∧", r" \,\wedge\, "), ("∨", r" \,\vee\, "), ("¬", r" \neg "),
                 ("⇒", r" \Rightarrow "), ("≠", r" \ne "), ("*", r" \cdot ")):
        s = s.replace(a, b)
    return s


def listing_lines(rows) -> list[str]:
    return ["    " * r["depth"] + r["code"] for r in rows]


class Hoare(VoiceoverScene):
    def construct(self):
        self.card()
        self.triple()
        self.assign()
        self.sequence()
        self.consequence()
        self.conditional()
        self.loop()
        self.soundness()

    def card(self):
        card = chapter_card(2, r"Floyd--Hoare logic", r"Can we calculate with programs as we do with numbers?",
                            lit=(1967, 1969, 1978),
                            extra=((1967, r"Floyd: \ Assigning Meanings to Programs"),
                                   (1969, r"Hoare: \ An Axiomatic Basis"),
                                   (1978, r"Cook: \ relative completeness")), part=PART)
        with self.voiceover("Chapter two. Floyd–Hoare logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def triple(self):
        head = label(r"The Hoare triple", font_size=36).to_edge(UP, buff=0.3)
        t = MathTex(r"\{P\}", r"\ c\ ", r"\{Q\}", font_size=64)
        t[0].set_color(DATA)
        t[1].set_color(HEAD)
        t[2].set_color(YES)
        t.move_to([-3.3, 2.2, 0])
        before = Rectangle(width=2.8, height=3.3, stroke_color=GREY_C, stroke_width=1.5).move_to([-5.1, -0.75, 0])
        after = Rectangle(width=2.8, height=3.3, stroke_color=GREY_C, stroke_width=1.5).move_to([-1.5, -0.75, 0])
        lb = label(r"states before", font_size=17, color=GREY_B).next_to(before, DOWN, buff=0.1)
        la = label(r"states after", font_size=17, color=GREY_B).next_to(after, DOWN, buff=0.1)
        P = Ellipse(width=2.0, height=1.8, color=DATA, fill_opacity=0.15).move_to([-5.1, -0.35, 0])
        Q = Ellipse(width=2.0, height=1.8, color=YES, fill_opacity=0.15).move_to([-1.5, -0.35, 0])
        tP = MathTex(r"P", font_size=30, color=DATA).move_to(P.get_left() + RIGHT * 0.3)
        tQ = MathTex(r"Q", font_size=30, color=YES).move_to(Q.get_top() + DOWN * 0.3)
        starts = [[-5.5, -0.3, 0], [-5.0, -0.8, 0], [-4.6, -0.1, 0]]
        ends = [[-1.9, -0.6, 0], [-1.2, -0.9, 0], [-1.4, -0.15, 0]]
        good = VGroup(*[VGroup(Dot(a, radius=0.06, color=WHITE), Dot(b, radius=0.06, color=WHITE),
                               Arrow(a, b, buff=0.08, stroke_width=2, color=HEAD,
                                     max_tip_length_to_length_ratio=0.06)) for a, b in zip(starts, ends)])
        spin_at = [-4.8, 0.25, 0]
        spin = VGroup(Dot(spin_at, radius=0.06, color=WHITE),
                      Arc(radius=0.22, start_angle=-PI / 2, angle=1.8 * PI, color=NO, stroke_width=2).move_to(
                          [-4.55, 0.25, 0]).add_tip(tip_length=0.1))
        spin_l = label(r"never ends", font_size=16, color=NO).move_to([-4.4, 1.15, 0])
        out_a, out_b = [-5.6, -2.0, 0], [-2.2, -1.95, 0]
        outside = VGroup(Dot(out_a, radius=0.06, color=GREY_B), Dot(out_b, radius=0.06, color=GREY_B),
                         DashedLine(out_a, out_b, buff=0.08, color=GREY_C, stroke_width=1.5))
        out_l = label(r"dashed: \ starts outside $P$, \ no promise", font_size=16, color=GREY_B).move_to(
            [-3.3, -2.95, 0])
        notes = VGroup(
            wrapped_label(r"if $P$ holds before $c$ runs, \ and $c$ terminates, \ then $Q$ holds afterwards", 5.8,
                          font_size=21, color=WHITE),
            wrapped_label(r"an assertion is a set of states: \ every run that starts in $P$ and ends, \ ends in $Q$",
                          5.8, font_size=21, color=HEAD),
            wrapped_label(r"\textbf{partial correctness}: \ a run that never ends satisfies every triple; \ "
                          r"termination is a separate proof", 5.8, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 0.6, 0])
        ex = MathTex(r"\{x = 5\}", r"\ x := x + 1\ ", r"\{x = 6\}", font_size=38).next_to(notes, DOWN, buff=0.5)
        ex[0].set_color(DATA)
        ex[2].set_color(YES)
        with self.voiceover(
            "Hoare's logic has one kind of sentence. <bookmark mark='a'/> P, c, Q says: if P holds before c runs,"
            " and c finishes, then Q holds afterwards. <bookmark mark='b'/> Think of each assertion as a set of "
            "states: every run that starts in P and ends, ends in Q. <bookmark mark='c'/> A run that never ends "
            "satisfies the triple trivially. This is partial correctness, and termination needs its own proof. "
            "<bookmark mark='d'/> If x is five, then after x gets x plus one, x is six."
        ) as vo:
            self.play(FadeIn(head), Write(t))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(before), Create(after), FadeIn(lb), FadeIn(la), FadeIn(P), FadeIn(Q), FadeIn(tP),
                      FadeIn(tQ), FadeIn(notes[1]))
            self.play(LaggedStart(*[GrowFromPoint(g, g[0].get_center()) for g in good], lag_ratio=0.3),
                      FadeIn(outside), FadeIn(out_l))
            vo.wait_until("c")
            self.play(FadeIn(spin), FadeIn(spin_l), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(ex, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def assign(self):
        fl = load("hoare")["flow"]["swap"][0]
        head = label(r"Assignment: \ substitute, \ backwards", font_size=36).to_edge(UP, buff=0.3)
        ax = MathTex(r"\{\, Q[e/x] \,\}", r"\quad x := e \quad", r"\{\, Q \,\}", font_size=46)
        ax[0].set_color(DATA)
        ax[2].set_color(YES)
        ax.next_to(head, DOWN, buff=0.4)
        axl = label(r"the assignment axiom: \ $Q$ with $e$ written for $x$", font_size=19, color=GREY_A).next_to(
            ax, DOWN, buff=0.15)
        goal = MathTex(r"\{\ ?\ \}", r"\quad x := x + 1 \quad", r"\{\, x > 5 \,\}", font_size=36)
        goal[2].set_color(YES)
        rows = VGroup(MathTex(r"x", r">", r"5", font_size=40, color=YES),
                      MathTex(r"(x + 1)", r">", r"5", font_size=40, color=WHITE),
                      MathTex(r"x", r">", r"4", font_size=40, color=DATA))
        whys = VGroup(label(r"what we want after", font_size=19, color=YES),
                      label(r"write $x + 1$ for $x$", font_size=19, color=WHITE),
                      label(r"simplify: \ the precondition", font_size=19, color=DATA))
        VGroup(goal, *rows).arrange(DOWN, buff=0.4).move_to([-3.6, -0.6, 0])
        for r in rows:
            r.set_x(-4.6)
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5)
        whys.align_to(whys[0], LEFT).set_x(-1.3, direction=LEFT)
        # the instrument's own step: the last line of the swap, the postcondition pushed through it
        post = MathTex(tx(fl["after"]), font_size=30, color=YES)
        code = mono(fl["code"], size=24)
        pre = MathTex(tx(fl["before"]), font_size=30, color=DATA)
        ours = VGroup(pre, code, post).arrange(DOWN, buff=0.45).move_to([4.2, -0.2, 0])
        up = Arrow(post.get_left() + LEFT * 0.25, pre.get_left() + LEFT * 0.25, buff=0.05, color=HEAD,
                   stroke_width=3, max_tip_length_to_length_ratio=0.12)
        ol = label(r"our tool, \ on the swap's last line", font_size=18, color=GREY_A).next_to(ours, UP, buff=0.3)
        fwd = MathTex(r"\{P\}\ x := e\ \{\, \exists x_0.\ P[x_0/x] \,\wedge\, x = e[x_0/x] \,\}", font_size=30,
                      color=GREY_A)
        fwdl = label(r"forwards needs the lost old value: \ an existential", font_size=18, color=GREY_B)
        fwdg = VGroup(fwd, fwdl).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Assignment comes first, and it runs backwards. <bookmark mark='a'/> To know what must hold before x "
            "gets e, take what we want afterwards and write e wherever it says x. <bookmark mark='b'/> We want x "
            "greater than five after x gets x plus one. Substitute: x plus one greater than five. <bookmark "
            "mark='c'/> Simplify: x greater than four. <bookmark mark='d'/> Our tool does the same to real code, "
            "here the swap's last line. <bookmark mark='e'/> Going forwards is harder: the assignment destroys "
            "the old x, and the rule needs an existential to remember it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(ax), FadeIn(axl))
            vo.wait_until("b")
            self.play(FadeIn(goal), FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(ol), FadeIn(post), FadeIn(code))
            self.play(GrowArrow(up), ReplacementTransform(post.copy(), pre))
            vo.wait_until("e")
            self.play(FadeIn(fwdg))
        self.wait(0.4)
        self.clear_scene()

    def sequence(self):
        sw = load("hoare")["programs"]["swap"]
        fl = load("hoare")["flow"]["swap"]
        head = label(r"Sequence: \ assertions flow backwards", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\dfrac{\{P\}\ c_1\ \{R\} \qquad \{R\}\ c_2\ \{Q\}}{\{P\}\ c_1 ;\, c_2\ \{Q\}}", font_size=36)
        rule.move_to([3.7, 2.0, 0])
        xc = -3.3
        lines = listing_lines(sw["listing"])
        code = VGroup(*[mono(s, size=24) for s in lines])
        ys_code = [1.0, -0.1, -1.2]
        for c, y in zip(code, ys_code):
            c.move_to([xc, y, 0])
        ys_assert = [-1.75, -0.65, 0.45, 1.55]           # after line 3, between 2-3, between 1-2, before line 1
        post = MathTex(tx(fl[0]["after"]), font_size=28, color=YES).move_to([xc, ys_assert[0], 0])
        befores = [MathTex(tx(st["before"]), font_size=28, color=YES).move_to([xc, y, 0])
                   for st, y in zip(fl[:3], ys_assert[1:])]
        pre = MathTex(r"\{\," + tx(fl[3]["before"]) + r"\,\}", font_size=28, color=DATA).move_to([xc, 2.25, 0])
        pre_l = label(r"the precondition", font_size=17, color=DATA).next_to(pre, LEFT, buff=0.25)
        post_l = label(r"the postcondition", font_size=17, color=YES).next_to(post, DOWN, buff=0.15)
        line_of = {1: 0, 2: 1, 3: 2}
        notes = VGroup(
            wrapped_label(r"start from the postcondition at the bottom; \ push it up through each line with the "
                          r"assignment axiom", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"each assertion between two lines is the $R$ of the rule: \ no cleverness needed", 5.6,
                          font_size=20, color=YES),
            wrapped_label(r"what reaches the top must now be compared with the precondition", 5.6, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, -0.7, 0])
        marker = SurroundingRectangle(code[2], color=HEAD, buff=0.08, stroke_width=2)
        with self.voiceover(
            "Sequencing glues triples together: if c one takes P to R, and c two takes R to Q, the pair takes P "
            "to Q. <bookmark mark='a'/> That gives a mechanical method. Start from the swap's postcondition at "
            "the bottom. <bookmark mark='b'/> Push it up through each line by substitution. <bookmark mark='c'/> "
            "Each assertion between two lines is the R of the rule, and no cleverness was needed. <bookmark "
            "mark='d'/> What arrives at the top must now be compared with the precondition."
        ) as vo:
            self.play(FadeIn(head), Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(post), FadeIn(post_l), FadeIn(notes[0]))
            vo.wait_until("b")
            src = post
            for k, st in enumerate(fl[:3]):
                tgt = code[line_of[st["line"]]]
                if k == 0:
                    self.play(Create(marker.move_to(tgt)), run_time=0.5)
                else:
                    self.play(marker.animate.move_to(tgt), run_time=0.5)
                self.play(ReplacementTransform(src.copy(), befores[k]), run_time=1.2)
                src = befores[k]
            self.play(FadeOut(marker))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), *[Indicate(b, color=HEAD, scale_factor=1.04) for b in befores[:2]])
            vo.wait_until("d")
            self.play(FadeIn(pre), FadeIn(pre_l), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def consequence(self):
        fl = load("hoare")["flow"]["swap"]
        head = label(r"Consequence: \ the logic meets arithmetic", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\dfrac{P \Rightarrow P' \qquad \{P'\}\ c\ \{Q'\} \qquad Q' \Rightarrow Q}"
                       r"{\{P\}\ c\ \{Q\}}", font_size=36).next_to(head, DOWN, buff=0.35)
        top = fl[2]["before"]                               # what reached the top of the swap
        assert top.replace(" ", "") == "x+y-(x+y-y)=Y∧x+y-y=X"
        rows = VGroup(
            MathTex(r"x + y - (x + y - y)", r"=", r"Y", r"\wedge", r"x + y - y", r"=", r"X", font_size=40),
            MathTex(r"x + y - x", r"=", r"Y", r"\wedge", r"x", r"=", r"X", font_size=40),
            MathTex(r"y", r"=", r"Y", r"\wedge", r"x", r"=", r"X", font_size=40),
            MathTex(r"x", r"=", r"X", r"\wedge", r"y", r"=", r"Y", font_size=40, color=DATA),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([-2.2, -0.35, 0])
        rows[0].set_color(YES)
        whys = VGroup(label(r"what reached the top", font_size=19, color=YES),
                      label(r"$x + y - y = x$", font_size=19, color=WHITE),
                      label(r"$x + y - x = y$", font_size=19, color=WHITE),
                      label(r"reordered: \ the precondition itself", font_size=19, color=DATA))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5)
        whys.set_x(3.0, direction=LEFT)
        for w in whys:
            w.align_to(whys[0], LEFT)
        whys.shift(RIGHT * (2.6 - whys.get_left()[0]))
        foot = VGroup(
            wrapped_label(r"these identities hold in wrap-around arithmetic too: \ $w$-bit integers form a ring "
                          r"\ (Part 4), \ so the swap is right even when $x + y$ overflows", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"what remains is a statement about integers, \ not programs: \ a \textbf{verification "
                          r"condition}, \ for a machine to check \ (Chapter 4)", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The rule of consequence lets us strengthen a precondition or weaken a postcondition. <bookmark "
            "mark='a'/> This is what arrived at the top of the swap. <bookmark mark='b'/> x plus y minus y is x. "
            "<bookmark mark='c'/> And x plus y minus x is y. <bookmark mark='d'/> Reordered, it is the "
            "precondition, and the swap is proved. <bookmark mark='e'/> These identities hold in sixteen-bit "
            "wrap-around arithmetic too, so the swap is right even when the sum overflows. What remains is a "
            "statement about integers, a verification condition, for a machine to check."
        ) as vo:
            self.play(FadeIn(head), Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k].copy(), rows[k + 1]), FadeIn(whys[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    def conditional(self):
        mx = load("hoare")["programs"]["max"]
        fl = load("hoare")["flow"]["max"]
        head = label(r"Conditionals: \ prove both branches", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\dfrac{\{P \wedge b\}\ c_1\ \{Q\} \qquad \{P \wedge \neg b\}\ c_2\ \{Q\}}"
                       r"{\{P\}\ \mathbf{if}\ b\ \mathbf{then}\ c_1\ \mathbf{else}\ c_2\ \{Q\}}", font_size=34)
        rule.next_to(head, DOWN, buff=0.3)
        code = code_block(listing_lines(mx["listing"]), size=24).move_to([-5.0, 0.15, 0])
        post = MathTex(r"\{\," + tx(fl[0]["after"]) + r"\,\}", font_size=30, color=YES).next_to(
            code, DOWN, buff=0.35).align_to(code, LEFT)
        b1 = MathTex(tx(fl[0]["before"]), font_size=30, color=YES)
        b2 = MathTex(tx(fl[1]["before"]), font_size=30, color=YES)
        b1.next_to(code[1], RIGHT, buff=0.9)
        b2.next_to(code[3], RIGHT, buff=0.9).align_to(b1, LEFT)
        k1 = label(r"all true when $a \ge b$", font_size=18, color=HEAD).next_to(b1, RIGHT, buff=0.3)
        k2 = label(r"all true when $b > a$", font_size=18, color=HEAD).next_to(b2, RIGHT, buff=0.3)
        both = MathTex(tx(fl[2]["before"]), font_size=28, color=DATA)
        if both.width > 12.4:
            both.width = 12.4
        both.next_to(post, DOWN, buff=0.45).set_x(0)
        both_l = label(r"the precondition of the whole \textbf{if}: \ always true, \ so $\{\mathit{true}\}$ "
                       r"suffices", font_size=20, color=DATA).next_to(both, DOWN, buff=0.25)
        with self.voiceover(
            "For a conditional, prove both branches, each knowing which way the test went. <bookmark mark='a'/> "
            "Push the maximum's postcondition up each branch. <bookmark mark='b'/> In one, m becomes a; in the "
            "other, b. <bookmark mark='c'/> When a is at least b, every part of the first is true; otherwise b "
            "exceeds a, and every part of the second is true. <bookmark mark='d'/> The precondition of the whole "
            "if combines the two, and it always holds, so true suffices."
        ) as vo:
            self.play(FadeIn(head), Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(post))
            vo.wait_until("b")
            self.play(ReplacementTransform(post.copy(), b1))
            self.play(ReplacementTransform(post.copy(), b2))
            vo.wait_until("c")
            self.play(FadeIn(k1))
            self.play(FadeIn(k2))
            vo.wait_until("d")
            self.play(ReplacementTransform(VGroup(b1.copy(), b2.copy()), both))
            self.play(FadeIn(both_l))
        self.wait(0.4)
        self.clear_scene()

    def loop(self):
        g = load("hoare")["programs"]["gauss"]
        fl = load("hoare")["flow"]["gauss"]
        head = label(r"Loops: \ the invariant", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\dfrac{\{I \wedge b\}\ c\ \{I\}}{\{I\}\ \mathbf{while}\ b\ \mathbf{do}\ c\ "
                       r"\{I \wedge \neg b\}}", font_size=36).move_to([-3.6, 2.15, 0])
        code = code_block(listing_lines(g["listing"]), size=22).move_to([-4.6, 0.1, 0])
        back = CurvedArrow(code[4].get_right() + RIGHT * 0.15, code[2].get_right() + RIGHT * 0.15, angle=PI / 2,
                           color=GREY_B, stroke_width=2, tip_length=0.15)
        inv = [st for st in fl if st["code"].startswith("while")][0]["before"]
        inv_m = MathTex(r"I:\ " + tx(inv), font_size=28, color=YES).next_to(code, DOWN, buff=0.4).align_to(
            code, LEFT)
        rows = VGroup(
            MathTex(r"2s'", r"=", r"2s", r"+", r"2(i + 1)", font_size=36),
            MathTex(r"2s'", r"=", r"i(i + 1)", r"+", r"2(i + 1)", font_size=36),
            MathTex(r"2s'", r"=", r"(i + 1)(i + 2)", font_size=36),
            MathTex(r"2s'", r"=", r"i'(i' + 1)", font_size=36, color=YES),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([1.6, 1.0, 0])
        whys = VGroup(label(r"$i' = i + 1$, \ $s' = s + i'$", font_size=18, color=GREY_A),
                      label(r"the invariant", font_size=18, color=YES),
                      label(r"factor out $i + 1$", font_size=18, color=GREY_A),
                      label(r"the invariant, \ one step on", font_size=18, color=YES))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        for w in whys:
            w.align_to(whys[0], LEFT)
        whys.shift(RIGHT * (4.3 - whys.get_left()[0]))
        ex = MathTex(r"I \wedge \neg(i < n)", r"\;\Rightarrow\;", r"i = n", r"\;\Rightarrow\;", r"2s = n(n + 1)",
                     font_size=36, color=DATA).move_to([0, -2.3, 0])
        ex_l = label(r"at the exit, \ with $i \le n$ from the invariant: \ Gauss's formula", font_size=19,
                     color=DATA).next_to(ex, DOWN, buff=0.2)
        foot = label(r"finding the invariant takes insight; \ checking it takes algebra", font_size=21,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Loops need the one ingredient a machine cannot supply: an invariant. <bookmark mark='a'/> If the "
            "body, entered with the invariant and the test true, restores the invariant, then the loop leaves "
            "with the invariant and the test false. <bookmark mark='b'/> Gauss's loop adds one, two, three, up to"
            " n, and its invariant says twice s is i times i plus one. <bookmark mark='c'/> After the body, twice"
            " the new s is twice s plus twice i plus one. <bookmark mark='d'/> The invariant replaces twice s; "
            "factor out i plus one, and it is the invariant again, one step on. <bookmark mark='e'/> At the exit,"
            " i equals n: Gauss's formula."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule))
            vo.wait_until("b")
            self.play(FadeIn(code), Create(back), FadeIn(inv_m))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            for k in range(3):
                self.play(TransformMatchingTex(rows[k].copy(), rows[k + 1]), FadeIn(whys[k + 1]), run_time=1.0)
            vo.wait_until("e")
            self.play(FadeIn(ex), FadeIn(ex_l))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def soundness(self):
        head = label(r"Sound, \ and complete relative to arithmetic", font_size=36).to_edge(UP, buff=0.3)
        true_e = Ellipse(width=5.4, height=3.8, color=YES, fill_opacity=0.08).move_to([-3.6, 0.0, 0])
        der = Ellipse(width=3.0, height=2.0, color=DATA, fill_opacity=0.2).move_to([-3.9, -0.3, 0])
        lt = label(r"true triples", font_size=20, color=YES).next_to(true_e.get_top(), DOWN, buff=0.3)
        ld = label(r"derivable triples", font_size=19, color=DATA).move_to(der)
        oracle = RoundedRectangle(width=3.4, height=0.6, corner_radius=0.1, stroke_color=KERN, fill_color=KERN,
                                  fill_opacity=0.15).move_to([-3.6, -2.75, 0])
        ol = label(r"oracle: \ every true assertion", font_size=18, color=KERN).move_to(oracle)
        der_big = Ellipse(width=5.2, height=3.6, color=DATA, fill_opacity=0.2).move_to(true_e)
        oarr = Arrow(oracle.get_top(), true_e.get_bottom() + UP * 0.25, buff=0.05, color=KERN, stroke_width=2.5,
                     max_tip_length_to_length_ratio=0.3)
        notes = VGroup(
            wrapped_label(r"\textbf{sound}: \ every derivable triple is true \ (induction on the derivation, \ rule "
                          r"by rule)", 5.8, font_size=20, color=YES),
            wrapped_label(r"not absolutely complete: \ $\{\mathit{true}\}\ c\ \{\mathit{false}\}$ holds exactly "
                          r"when $c$ never halts \ (Part 25), \ and assertions about integers contain all of "
                          r"arithmetic \ (G\"odel)", 5.8, font_size=20, color=NO),
            wrapped_label(r"Stephen Cook \ (1978): \ \textbf{relatively complete}: \ every true triple is derivable "
                          r"if the consequence rule may use every true assertion, \ and the assertion language can "
                          r"express the assertions a proof needs", 5.8, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.5, -0.1, 0])
        with self.voiceover(
            "Two questions about any logic. <bookmark mark='a'/> Is it sound: is every derived triple true? Yes, "
            "by induction on the derivation. <bookmark mark='b'/> Is it complete: can every true triple be "
            "derived? Not absolutely. The triple true, c, false holds exactly when c never halts, which is "
            "undecidable, and assertions about integers contain all of arithmetic, which Gödel showed no proof "
            "system captures. <bookmark mark='c'/> Stephen Cook proved in 1978 the best possible result: if the "
            "consequence rule may consult every true assertion, and assertions can express what proofs need, "
            "every true triple is derivable. Hoare logic is complete relative to arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(true_e), FadeIn(lt))
            vo.wait_until("a")
            self.play(FadeIn(der), FadeIn(ld), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(oracle), FadeIn(ol), GrowArrow(oarr), FadeIn(notes[2]))
            self.play(Transform(der, der_big), ld.animate.move_to(true_e.get_center() + DOWN * 0.3), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO)
