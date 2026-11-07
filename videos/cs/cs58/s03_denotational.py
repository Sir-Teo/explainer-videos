from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono


def sem(e: str) -> str:
    """The semantic brackets around a term (TeX)."""
    return r"[\![\," + e + r"\,]\!]"


def node(sym: str, color=GREY_B):
    """A node of a syntax tree: a small circle with its symbol."""
    c = Circle(radius=0.3, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    t = MathTex(sym, font_size=30, color=WHITE).move_to(c)
    return VGroup(c, t)


class Denotational(VoiceoverScene):
    def construct(self):
        self.card()
        self.denote()
        self.equations()
        self.compute()
        self.contexts()
        self.recursion()

    def card(self):
        card = chapter_card(2, r"Meaning as mathematics", r"What object does a program stand for?",
                            lit=(1971,), extra=((1971, r"Scott and Strachey: \ toward a mathematical semantics"),),
                            part=PART)
        with self.voiceover("Chapter two. Meaning as mathematics. What object does a program stand for?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def denote(self):
        head = label(r"A program denotes an object", font_size=36).to_edge(UP, buff=0.3)
        p1 = mono("fun x -> x * x", size=24, color=WHITE)
        p2 = mono("fun x -> x * x + 0", size=24, color=WHITE)
        VGroup(p1, p2).arrange(DOWN, buff=1.4, aligned_edge=LEFT).move_to([-4.3, 0.1, 0])
        ins = VGroup(*[MathTex(str(n), font_size=30, color=DATA) for n in (-2, -1, 0, 1, 2, 3)]).arrange(
            DOWN, buff=0.3)
        outs = VGroup(*[MathTex(str(n * n), font_size=30, color=YES) for n in (-2, -1, 0, 1, 2, 3)]).arrange(
            DOWN, buff=0.3)
        VGroup(ins, outs).arrange(RIGHT, buff=1.6).move_to([3.4, 0.1, 0])
        for a, b in zip(ins, outs):
            b.set_y(a.get_y())
        maps = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.15, stroke_width=2, color=GREY_B,
                              max_tip_length_to_length_ratio=0.12) for a, b in zip(ins, outs)])
        oval = SurroundingRectangle(VGroup(ins, outs), buff=0.3, corner_radius=0.3, color=YES, stroke_width=2)
        dots = MathTex(r"\vdots", font_size=30, color=GREY_B).next_to(oval, DOWN, buff=0.1)
        cap = label(r"the squaring function on the integers: \ a set of pairs", font_size=21,
                    color=YES).next_to(oval, UP, buff=0.2)
        a1 = Arrow(p1.get_right(), oval.get_left() + UP * 0.5, buff=0.2, color=HEAD, stroke_width=3)
        a2 = Arrow(p2.get_right(), oval.get_left() + DOWN * 0.5, buff=0.2, color=HEAD, stroke_width=3)
        b1 = MathTex(sem(r"\cdot"), font_size=32, color=HEAD).next_to(a1.get_center(), UP, buff=0.15)
        b2 = MathTex(sem(r"\cdot"), font_size=32, color=HEAD).next_to(a2.get_center(), DOWN, buff=0.15)
        foot = wrapped_label(r"different steps, \ the same meaning: \ a denotation keeps \textit{what} is computed "
                             r"and forgets \textit{how}", 12.4, font_size=22, color=WHITE).to_edge(DOWN, buff=0.45)
        ill = note(r"illustrative", font_size=16).next_to(dots, DOWN, buff=0.1)
        with self.voiceover(
            "Operational semantics says what a machine does with a program. Denotational semantics, begun by Dana "
            "Scott and Christopher Strachey at Oxford in their paper of nineteen seventy-one, asks instead what a "
            "program is. <bookmark mark='a'/> Each term is mapped, by the semantic brackets, to a mathematical "
            "object called its denotation. The term fun x arrow x times x denotes the squaring function on the "
            "integers: a set of pairs, and nothing more. <bookmark mark='b'/> A different program, x times x plus "
            "zero, takes more steps, and denotes exactly the same function. <bookmark mark='c'/> So the denotation "
            "keeps what is computed and forgets how. That is precisely what we need before we can say that two "
            "programs are interchangeable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(p1))
            self.play(GrowArrow(a1), FadeIn(b1), Create(oval), FadeIn(ins), FadeIn(cap))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(m), FadeIn(o)) for m, o in zip(maps, outs)],
                                  lag_ratio=0.3), FadeIn(dots), FadeIn(ill), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(p2))
            self.play(GrowArrow(a2), FadeIn(b2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def equations(self):
        head = label(r"One equation per construct", font_size=36).to_edge(UP, buff=0.3)
        fs = 33
        eqs = VGroup(
            MathTex(sem("n") + r"\rho", "=", "n", font_size=fs),
            MathTex(sem("x") + r"\rho", "=", r"\rho(x)", font_size=fs),
            MathTex(sem(r"e_1 \oplus e_2") + r"\rho", "=", sem("e_1") + r"\rho \oplus " + sem("e_2") + r"\rho",
                    font_size=fs),
            MathTex(sem(r"\mathsf{if}\ e_0\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2") + r"\rho", "=",
                    sem("e_1") + r"\rho \ \text{or}\ " + sem("e_2") + r"\rho, \ \text{by}\ " + sem("e_0") +
                    r"\rho", font_size=fs),
            MathTex(sem(r"\mathsf{fun}\ x \to e") + r"\rho", "=", r"\lambda v.\ " + sem("e") + r"\rho[x \mapsto v]",
                    font_size=fs),
            MathTex(sem(r"e_1\ e_2") + r"\rho", "=", sem("e_1") + r"\rho\,\big(" + sem("e_2") + r"\rho\big)",
                    font_size=fs),
            MathTex(sem(r"\mathsf{fix}\ f\ x \to e") + r"\rho", "=", r"\ ?", font_size=fs, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        for e in eqs:
            e.shift(RIGHT * (eqs[0][1].get_x() - e[1].get_x()))
        eqs.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        bot = wrapped_label(r"$\rho$: \ the environment, \ values of free variables; \ \ $\bot$ \ (``bottom''): \ "
                            r"the meaning of a term that never finishes, \ and any operation on $\bot$ gives $\bot$",
                            12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        eqs.set_y((head.get_bottom()[1] + bot.get_top()[1]) / 2)
        # the syntax tree of (1 + 2) * x, meanings flowing up
        cx, cy = 4.7, eqs.get_y() + 0.3
        times = node(r"\times").move_to([cx, cy + 1.2, 0])
        plus = node("+").move_to([cx - 1.0, cy, 0])
        xv = node("x").move_to([cx + 1.0, cy, 0])
        one = node("1").move_to([cx - 1.6, cy - 1.2, 0])
        two = node("2").move_to([cx - 0.4, cy - 1.2, 0])
        edges = VGroup(*[Line(a[0].get_center(), b[0].get_center(), color=GREY_C, stroke_width=1.8).set_z_index(-1)
                         for a, b in ((times, plus), (times, xv), (plus, one), (plus, two))])
        tree = VGroup(edges, times, plus, xv, one, two)
        env = MathTex(r"\rho = \{x \mapsto 4\}", font_size=26, color=DATA).next_to(tree, DOWN, buff=0.35)
        vals = [MathTex(v, font_size=26, color=DATA).next_to(n, d, buff=0.12) for v, n, d in
                (("1", one, DOWN), ("2", two, DOWN), ("4", xv, RIGHT), ("3", plus, LEFT), ("12", times, RIGHT))]
        vals[0].next_to(one, LEFT, buff=0.12)
        vals[1].next_to(two, RIGHT, buff=0.12)
        ill = note(r"illustrative", font_size=16).next_to(env, DOWN, buff=0.12)
        with self.voiceover(
            "There is one equation for each construct, and the environment, rho, supplies the values of the free "
            "variables. <bookmark mark='a'/> A numeral means its number. A variable means what the environment says. "
            "<bookmark mark='b'/> An arithmetic term means the operation applied to the meanings of its sides; a "
            "conditional means one branch or the other, by the meaning of its condition. <bookmark mark='c'/> A "
            "function means a mathematical function: given v, the meaning of its body with x bound to v. An "
            "application means the function's meaning applied to the argument's. A term that never finishes means "
            "bottom, the undefined element, and bottom spreads through every operation. <bookmark mark='d'/> Notice "
            "that each right-hand side mentions only the meanings of the parts. This is compositionality: meaning is "
            "assembled from the leaves up, with no machine and no order of steps. <bookmark mark='e'/> One construct "
            "is missing, and it is the interesting one: fix."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[2]))
            self.play(FadeIn(eqs[3]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[4]))
            self.play(FadeIn(eqs[5]), FadeIn(bot))
            vo.wait_until("d")
            self.play(Create(edges), *[FadeIn(n) for n in (times, plus, xv, one, two)], FadeIn(env), FadeIn(ill))
            for group in ((vals[0], vals[1], vals[2]), (vals[3],), (vals[4],)):
                self.play(*[FadeIn(v, scale=1.3) for v in group], run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(eqs[6]))
        self.wait(0.4)
        self.clear_scene()

    def compute(self):
        head = label(r"Computing a meaning by algebra", font_size=36).to_edge(UP, buff=0.3)
        fs = 34
        sq = r"\mathsf{fun}\ x \to x \times x"
        rows = VGroup(
            MathTex(sem(r"(" + sq + r")\ (1 + 2)") + r"\rho", font_size=fs),
            MathTex(r"=", sem(sq) + r"\rho", r"\big(", sem("1 + 2") + r"\rho", r"\big)", font_size=fs),
            MathTex(r"=", r"\big(\lambda v.\ " + sem(r"x \times x") + r"\rho[x \mapsto v]\big)", r"\big(", r"3",
                    r"\big)", font_size=fs),
            MathTex(r"=", sem(r"x \times x") + r"\rho[x \mapsto 3]", font_size=fs),
            MathTex(r"=", r"3 \times 3", r"=", r"9", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        rows.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        for r in rows[1:]:
            r.shift(RIGHT * 0.5)
        rows[4][3].set_color(YES)
        whys = VGroup(
            label(r"squaring, \ applied to one plus two", font_size=22, color=GREY_B),
            label(r"the application equation", font_size=22, color=GREY_B),
            label(r"the function equation; \ arithmetic", font_size=22, color=GREY_B),
            label(r"apply the map", font_size=22, color=GREY_B),
            label(r"variable, \ arithmetic: \ the big-step tree's 9", font_size=22, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5)
        wx = max(r.get_right()[0] for r in rows) + 0.5
        for w in whys:
            w.set_x(wx + w.width / 2)
        if whys.get_right()[0] > 6.85:
            whys.shift(LEFT * (whys.get_right()[0] - 6.85))
        foot = wrapped_label(r"no evaluation order, \ no machine: \ each line replaces equals by equals", 12.4,
                             font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Let us compute one meaning by nothing but equations. <bookmark mark='a'/> Squaring, applied to one "
            "plus two. <bookmark mark='b'/> By the application equation, its meaning is the meaning of the "
            "function applied to the meaning of the argument. <bookmark mark='c'/> The function means the map "
            "taking v to the meaning of x times x with x bound to v; and one plus two means three. "
            "<bookmark mark='d'/> Apply the map: the meaning of x times x, with x bound to three. "
            "<bookmark mark='e'/> And that is three times three, nine. The big-step tree of chapter one reached the "
            "same nine by evaluating. Here there was no evaluation at all, only algebra, and each line followed "
            "from the one before by replacing equals by equals, the way we simplify any expression in school."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("bcde", start=1):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=1.4)
            self.play(Circumscribe(rows[4][3], color=YES), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def contexts(self):
        head = label(r"Compositionality pays", font_size=36).to_edge(UP, buff=0.3)
        left = mono("fun x -> (fun y -> y + y) (", size=26, color=WHITE)
        hole = DashedVMobject(Rectangle(width=2.9, height=0.62, color=HEAD, stroke_width=2), num_dashes=30)
        right = mono(")", size=26, color=WHITE)
        ctx = VGroup(left, hole, right).arrange(RIGHT, buff=0.12).move_to([0, 1.7, 0])
        ctx_l = label(r"a context $C[\ \cdot\ ]$: \ a program with a hole", font_size=21, color=HEAD).next_to(
            ctx, UP, buff=0.3)
        e1 = mono("x * x", size=24, color=DATA)
        e2 = mono("x * x + 0", size=24, color=LAM)
        plugs = VGroup(e1, e2).arrange(RIGHT, buff=2.5).move_to([0, -0.2, 0])
        pl = VGroup(MathTex(sem("e_1") + "=" + sem("e_2"), font_size=30, color=WHITE)).next_to(plugs, DOWN,
                                                                                               buff=0.35)
        thm = MathTex(sem("e_1"), "=", sem("e_2"), r"\quad\implies\quad", sem("C[e_1]"), "=", sem("C[e_2]"),
                      font_size=36, color=YES).move_to([0, -1.7, 0])
        pf = wrapped_label(r"proof: \ induction on $C$, \ since every equation uses only the meanings of the parts; \ "
                           r"so an optimizer \ (Part 13) \ may rewrite $x \times x + 0$ to $x \times x$ anywhere",
                           12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Compositionality pays for itself at once. <bookmark mark='a'/> Take any program with a hole in it. "
            "This is called a context. <bookmark mark='b'/> Plug in two terms with the same meaning, <bookmark "
            "mark='c'/> and the whole programs have the same meaning, whatever the context is. The proof is an "
            "induction on the context, and it goes through because every equation looks only at the meanings of "
            "the parts. <bookmark mark='d'/> This is what licenses an optimizer, like Part 13's, to replace x times "
            "x plus zero by x times x anywhere in a program: one local fact about meanings, used everywhere. "
            "Whether the converse holds, whether programs that no context can tell apart always have equal "
            "meanings, is the question of chapter four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), Create(hole), FadeIn(ctx_l))
            vo.wait_until("b")
            self.play(FadeIn(e1), FadeIn(e2), FadeIn(pl))
            c1 = e1.copy()
            self.play(c1.animate.move_to(hole), run_time=1.0)
            self.play(Transform(c1, e2.copy().move_to(hole)), run_time=1.0)
            vo.wait_until("c")
            self.play(Write(thm))
            vo.wait_until("d")
            self.play(FadeIn(pf))
        self.wait(0.4)
        self.clear_scene()

    def recursion(self):
        head = label(r"Recursion is an equation", font_size=36).to_edge(UP, buff=0.3)
        fs = 32
        r0 = MathTex(sem(r"\mathsf{fix}\ f\ x \to e") + r"\rho", r"=", r"g", font_size=fs)
        r1 = MathTex(r"g", r"=", r"\lambda v.\ " + sem("e") + r"\rho[f \mapsto", r"g", r",\ x \mapsto v]",
                     font_size=fs)
        r2 = MathTex(r"g", r"=", r"F(", r"g", r")", r"\qquad F(h) =", r"\lambda v.\ " + sem("e") +
                     r"\rho[f \mapsto", r"h", r",\ x \mapsto v]", font_size=fs)
        for r in (r1, r2):
            r[0].set_color(HEAD)
            r[3].set_color(HEAD)
        r0[2].set_color(HEAD)
        der = VGroup(r0, r1).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.4)
        r2.move_to(r1, aligned_edge=LEFT)
        ff = MathTex(r"\text{factorial:}\quad F(h)(n) = \begin{cases} 1 & n = 0 \\ n \cdot h(n-1) & "
                     r"\text{otherwise} \end{cases}", font_size=32, color=WHITE).next_to(der, DOWN, buff=0.5)
        ns = list(range(-3, 4))
        A = [r"\bot"] * 3 + ["1", "1", "2", "6"]
        B = ["0"] * 3 + ["1", "1", "2", "6"]
        cw = 1.0
        hdr = VGroup(MathTex("n", font_size=31, color=GREY_B),
                     *[MathTex(str(n), font_size=31, color=GREY_B) for n in ns])
        rowA = VGroup(MathTex(r"g_1", font_size=31, color=YES), *[MathTex(a, font_size=31, color=YES) for a in A])
        rowB = VGroup(MathTex(r"g_2", font_size=31, color=NO), *[MathTex(b, font_size=31, color=NO) for b in B])
        for r in (hdr, rowA, rowB):
            for k, m in enumerate(r):
                m.move_to([k * cw, 0, 0])
        rowA.shift(DOWN * 0.62)
        rowB.shift(DOWN * 1.24)
        tab = VGroup(hdr, rowA, rowB)
        rule_ = Line(hdr.get_left() + DOWN * 0.28 + LEFT * 0.2, hdr.get_right() + DOWN * 0.28 + RIGHT * 0.2,
                     color=GREY_D, stroke_width=1.5)
        tab.add(rule_)
        tab.next_to(ff, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        notes = VGroup(
            wrapped_label(r"both satisfy $g = F(g)$: \ substitute and check", 5.2, font_size=21, color=WHITE),
            wrapped_label(r"\texttt{fact (-1)} calls \texttt{fact (-2)}, \ \texttt{fact (-3)}, \ \ldots \ and never "
                          r"stops", 5.2, font_size=21, color=GREY_A),
            wrapped_label(r"the meaning is $g_1$: \ the \textbf{least defined} solution, \ the least fixed point",
                          5.2, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.7)
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        body = VGroup(der, ff, tab, notes, r2)
        body.shift(UP * ((head.get_bottom()[1] - 0.3 + -3.6) / 2 - body.get_y()))
        with self.voiceover(
            "Recursion is where the mathematics has to work. <bookmark mark='a'/> The meaning of fix f x arrow e "
            "should be a function g that satisfies its own definition: the map from v to the meaning of the body, "
            "with f bound to g itself. <bookmark mark='b'/> Write the right-hand side as a functional F, which takes "
            "a candidate h to an improved one. Then g equals F of g: a recursive function means a fixed point of F. "
            "<bookmark mark='c'/> For factorial, F of h, at n, is one if n is zero, and n times h of n minus one "
            "otherwise. <bookmark mark='d'/> But an equation can have several solutions. Both of these are fixed "
            "points of factorial's F: they agree on the naturals, and on negative numbers one is undefined while the "
            "other is zero. <bookmark mark='e'/> Which is the meaning? Run fact on minus one, and it calls itself on "
            "minus two, minus three, forever. So the answer there is undefined: the least defined fixed point. Making"
            " least precise, and proving that it always exists, is domain theory, the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r0))
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r1, r2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(ff))
            vo.wait_until("d")
            self.play(FadeIn(hdr), Create(rule_))
            self.play(FadeIn(rowA), FadeIn(rowB), FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]), Indicate(rowA, color=YES))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
