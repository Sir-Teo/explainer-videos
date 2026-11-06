from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


def node(t: str, color=WHITE, font_size=30) -> VGroup:
    m = MathTex(t, font_size=font_size, color=color)
    c = Circle(radius=max(m.width, m.height) / 2 + 0.16, stroke_color=color, stroke_width=2, fill_color="#151A24",
               fill_opacity=1)
    return VGroup(c, m.move_to(c))


class Recursion(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Recursive functions", r"Which functions can arithmetic talk about?",
                            lit=(1931,), part=PART)
        with self.voiceover("Chapter three. Recursive functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.combinators()
        self.library()
        self.ackermann()
        self.represent()

    def combinators(self):
        head = label(r"Five ways to make a function", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"zero", r"Z(x) = 0"), (r"successor", r"S(x) = x + 1"), (r"projection", r"P^n_i(x_1, \dots, x_n) = x_i"),
                (r"composition", r"C(f; g_1, \dots, g_k)(\vec x) = f(g_1(\vec x), \dots, g_k(\vec x))"),
                (r"primitive recursion", r"R(g, h):\ \ f(\vec x, 0) = g(\vec x), \quad f(\vec x, y{+}1) = "
                                         r"h(\vec x, y, f(\vec x, y))")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.8 - 0.62 * i
            la = label(a, font_size=24, color=NUM)
            lb = MathTex(b, font_size=30)
            la.move_to([-6.0 + la.width / 2, y, 0])
            lb.move_to([-2.9 + lb.width / 2, y, 0])
            tab.add(VGroup(la, lb))
        R = node(r"R", GOAL).move_to([-2.4, -1.4, 0])
        P1 = node(r"P^1_1", TAPE, 24).move_to([-3.8, -2.7, 0])
        C = node(r"C", PROV).move_to([-1.0, -2.7, 0])
        S_ = node(r"S", TAPE, 26).move_to([-1.9, -3.6, 0])
        P3 = node(r"P^3_3", TAPE, 24).move_to([-0.1, -3.6, 0])
        es = VGroup(*[Line(a.get_center(), b.get_center(), buff=0.38, color=GREY_B, stroke_width=2)
                      for a, b in ((R, P1), (R, C), (C, S_), (C, P3))])
        tree = VGroup(es, R, P1, C, S_, P3)
        expl = VGroup(MathTex(r"x + 0 = x", font_size=32), MathTex(r"x + (y{+}1) = (x + y) + 1", font_size=32),
                      label(r"addition, \ as a tree of five combinators", font_size=24, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -2.4, 0])
        with self.voiceover(
            "Which functions can arithmetic express? Gödel's answer in 1931 used what we now call the primitive "
            "recursive functions. <bookmark mark='a'/>Start from three simple kinds: the zero function, successor, "
            "and the projections that pick out one argument. <bookmark mark='b'/>Then close under two ways of "
            "building: composition, plugging functions into functions; and primitive recursion, defining the value "
            "at y plus one from the value at y. <bookmark mark='c'/>Addition, for instance, is a primitive "
            "recursion: x plus zero is x, and x plus y plus one is the successor of x plus y. As a tree, it is five "
            "combinators."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[3:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(tree, shift=UP * 0.1), FadeIn(expl))
        self.clear_scene()

    def library(self):
        d = load("recursion")
        head = label(r"The Reasoner builds and runs them", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"function", font_size=24, color=P.CLAIM), label(r"defined by", font_size=24, color=P.CLAIM),
              label(r"size", font_size=24, color=P.CLAIM), label(r"a value", font_size=24, color=P.CLAIM)]
        defs = {"add": (r"x + y", r"x + 0 = x,\ \ x + (y{+}1) = \mathsf{S}(x + y)", r"3 + 4 = 7"),
                "mul": (r"x \cdot y", r"x \cdot 0 = 0,\ \ x \cdot (y{+}1) = x \cdot y + x", r"3 \cdot 4 = 12"),
                "exp": (r"x^y", r"x^0 = 1,\ \ x^{y+1} = x^y \cdot x", r"2^5 = 32"),
                "pred": (r"x \dot- 1", r"0 \dot- 1 = 0,\ \ (y{+}1) \dot- 1 = y", r"7 \dot- 1 = 6"),
                "fact": (r"x!", r"0! = 1,\ \ (y{+}1)! = y! \cdot (y{+}1)", r"5! = 120")}
        rows = [[MathTex(defs[k][0], font_size=30), MathTex(defs[k][1], font_size=26),
                 MathTex(str(d["sizes"][k]), font_size=28, color=NUM), MathTex(defs[k][2], font_size=28, color=OK)]
                for k in ("add", "mul", "exp", "pred", "fact")]
        grid = ValueGrid(hd, rows, col_w=[1.6, 6.6, 1.2, 2.6], cell_h=0.72, font_size=26).move_to([0, 0.0, 0])
        note = label(r"size: \ the number of combinators in the tree; \ each one built from the last",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The Reasoner has these combinators as a small programming language. <bookmark mark='a'/>Multiplication "
            "is a recursion over addition; exponentiation a recursion over multiplication; then predecessor and "
            "factorial. Each is a tree built from the trees before it, and the Reasoner runs each one on its "
            "arguments, by nothing but zero, successor and recursion. <bookmark mark='b'/>Almost every function "
            "met in number theory, primes, remainders, the n-th prime, is primitive recursive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(5)], lag_ratio=0.35), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def ackermann(self):
        d = load("recursion")
        hc = history_card(1928, r"Wilhelm Ackermann", r"a computable function that is not primitive recursive",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        eqs = VGroup(MathTex(r"A(0, n) = n + 1", font_size=30), MathTex(r"A(m{+}1, 0) = A(m, 1)", font_size=30),
                     MathTex(r"A(m{+}1, n{+}1) = A(m, A(m{+}1, n))", font_size=30)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.45)
        hd = [MathTex(r"m \backslash n", font_size=26, color=P.CLAIM)] + [MathTex(str(n), font_size=26, color=P.CLAIM)
                                                                          for n in range(5)]
        rows = [[MathTex(str(m), font_size=26, color=P.CLAIM)] + [MathTex(str(v), font_size=28) for v in d["ack"][m]]
                for m in range(4)]
        rows.append([MathTex("4", font_size=26, color=P.CLAIM), MathTex(str(d["a40"]), font_size=28, color=BAD),
                     MathTex(f"{d['a41']:,}".replace(",", "{,}"), font_size=28, color=BAD),
                     label(rf"{d['a42_digits']:,} digits".replace(",", "{,}"), font_size=22, color=BAD),
                     MathTex(r"\cdots", font_size=28, color=BAD), MathTex(r"\cdots", font_size=28, color=BAD)])
        grid = ValueGrid(hd, rows, col_w=[1.1, 1.0, 1.5, 2.2, 1.2, 1.2], cell_h=0.6, font_size=26).move_to(
            [-0.4, -0.9, 0])
        cap = label(r"$A(4, 2) = 2^{65536} - 3$: \ the size of $V_6$ in Part 6, \ minus three", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        diag = label(r"the diagonal again: \ list the primitive recursive $f_0, f_1, \dots$; \ then $f_n(n) + 1$ "
                     r"is computable, \ and on no list", font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But not every computable function is primitive recursive. <bookmark mark='a'/>Wilhelm Ackermann found "
            "one in 1928; this simpler version is Rózsa Péter's. Each row recurses on the row before it. "
            "<bookmark mark='b'/>Row one adds, row two doubles, row three is exponential. Row four is a tower: A of "
            "four and one is sixty-five thousand, five hundred and thirty-three, and A of four and two has nineteen "
            "thousand, seven hundred and twenty-nine digits. <bookmark mark='c'/>That is two to the sixty-five "
            "thousand five hundred and thirty-six, minus three: the size of stage six of the hierarchy in Part 6. "
            "Ackermann's function eventually outgrows every primitive recursive function. <bookmark mark='d'/>And "
            "there is a quicker proof that something is missing: the diagonal. List the primitive recursive "
            "functions; one plus the n-th function at n is computable, and differs from every function on the "
            "list. Capturing all computation will need Turing."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(eqs))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(5)])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r][1:])) for r in range(5)], lag_ratio=0.4),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeOut(cap), FadeIn(diag))
        self.clear_scene()

    def represent(self):
        head = label(r"Arithmetic can check any computation", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        dc = definition_card(r"representable", r"$f$ is represented by a formula $\varphi(x, y)$ if, whenever "
                             r"$f(n) = m$, \ $Q \vdash \varphi(\bar n, \bar m)$ \ and \ $Q \vdash \forall y\,"
                             r"(\varphi(\bar n, y) \to y = \bar m)$", width=10.6, font_size=25,
                             color=P.CLAIM).move_to([0, 1.3, 0])
        thm = theorem_card(r"Gödel (1931)", r"every primitive recursive function \ (indeed every computable one) \ "
                           r"is representable in $Q$", width=10.6, font_size=25).next_to(dc, DOWN, buff=0.35)
        s1 = VGroup(label(r"$\Sigma_1$ sentences: \ $\exists y\,\psi(y)$, \ with $\psi$ checkable step by step",
                          font_size=25, color=PROV),
                    label(r"$\Sigma_1$-completeness: \ $Q$ proves every \textit{true} $\Sigma_1$ sentence: \ "
                          r"`this computation halts with this output'", font_size=25, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is what all this buys. <bookmark mark='a'/>A function is represented in Q by a formula when Q "
            "proves, for each input, the right output, and that no other output is right. "
            "<bookmark mark='b'/>Gödel showed that every primitive recursive function is representable; we now "
            "know the same for every computable function. <bookmark mark='c'/>The sentences that say a computation "
            "succeeds have a simple shape, there exists a y such that a checkable condition holds. They are called "
            "sigma one. And Q proves every true sigma one sentence. Whenever a computation halts, arithmetic can "
            "prove that it does. Hold on to that; it is half of Gödel's proof."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in s1], lag_ratio=0.4))
        self.clear_scene()
