from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def num(v):
    from fractions import Fraction
    f = Fraction(v).limit_denominator(100)
    return str(f.numerator) if f.denominator == 1 else rf"\tfrac{{{f.numerator}}}{{{f.denominator}}}"


class Duality(VoiceoverScene):
    def construct(self):
        self.card()
        self.bounds()
        self.strong()
        self.prices()

    def card(self):
        card = chapter_card(3, r"Duality", r"How do you prove that nothing is better?", lit=(1947, 1902),
                            extra=((1947, r"von Neumann's duality"), (1902, r"Farkas' lemma")), part=PART)
        with self.voiceover("Chapter three. Duality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bounds(self):
        d = load("duality")
        head = label(r"Bound the profit by adding up constraints", font_size=32).to_edge(UP, buff=0.3)
        cons = MathTex(r"2x_1 + 3x_2 + x_3 &\le 5 \quad \cdot\, y_1 \\ 4x_1 + x_2 + 2x_3 &\le 11 \quad \cdot\, y_2 \\ "
                       r"3x_1 + 4x_2 + 2x_3 &\le 8 \quad \cdot\, y_3", font_size=32, color=WHITE)
        cons.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        rule = MathTex(r"\text{if } y \ge 0 \text{ and } y^{\mathsf T}A \ge c^{\mathsf T}: \quad "
                       r"5x_1 + 4x_2 + 3x_3 \;\le\; y^{\mathsf T}A\,x \;\le\; y^{\mathsf T} b", font_size=32,
                       color=LAM).next_to(cons, DOWN, buff=0.4).set_x(0)
        rows = []
        for f in d["family"]:
            y = f["y"]
            rows.append([rf"$({num(y[0])}, {num(y[1])}, {num(y[2])})$", r"yes" if f["feasible"] else r"no",
                         rf"$\le {num(f['bound'])}$" if f["feasible"] else r"---"])
        tab = grid_table([r"multipliers $y$", r"covers $c$?", r"proves profit"], rows, widths=[3.4, 2.2, 2.6],
                         row_h=0.46, font_size=22, mono_cols=(),
                         colors=[[WHITE, YES if f["feasible"] else NO, YES if f["feasible"] else NO]
                                 for f in d["family"]])
        tab.next_to(rule, DOWN, buff=0.4).set_x(0)
        foot = label(r"the best bound is itself a linear program: \ the \textbf{dual}", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How could anyone prove that thirteen is the best possible profit? <bookmark mark='a'/> Multiply each "
            "constraint by a non-negative number and add them up. <bookmark mark='b'/> If the combined left side has "
            "at least the objective's coefficients, five, four and three, then for any feasible plan the profit is "
            "at most the combined right side. <bookmark mark='c'/> Three times the first constraint gives "
            "six, nine and three, which covers five, four and three, so the profit is at most fifteen. Five thirds "
            "of the third constraint proves thirteen and a third. Five quarters of the second fails: it doesn't "
            "cover the coefficients of the second and third products. And one of the first plus one of the third "
            "proves exactly thirteen. <bookmark mark='d'/> Finding the best bound is itself a linear program, the "
            "dual: minimize five y one plus eleven y two plus eight y three, subject to the covering conditions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cons))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for r in tab.cells[1:]:
                self.play(FadeIn(VGroup(*r), shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def strong(self):
        head = label(r"Weak and strong duality", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"\text{primal: } \max\ c^{\mathsf T}x \ \ \text{s.t. } Ax \le b,\ x \ge 0 \qquad \qquad "
                    r"\text{dual: } \min\ b^{\mathsf T}y \ \ \text{s.t. } A^{\mathsf T}y \ge c,\ y \ge 0",
                    font_size=30, color=WHITE),
            label(r"\textbf{weak}: \ every feasible $x$ and $y$ have $c^{\mathsf T}x \le b^{\mathsf T}y$ \ (the "
                  r"argument we just made)", font_size=22, color=LAM),
            label(r"\textbf{strong}: \ the optima are \textbf{equal} \ (von Neumann, 1947; \ Gale, Kuhn and Tucker, "
                  r"1951)", font_size=22, color=YES),
            label(r"the proof: \ \textbf{Farkas' lemma} \ (1902): \ either $Ax = b,\ x \ge 0$ has a solution, \ or some "
                  r"$y$ has $y^{\mathsf T}A \ge 0$ and $y^{\mathsf T}b < 0$, \ never both", font_size=22, color=HEAD),
            label(r"geometry: \ a point outside a convex cone can be \textbf{separated} from it by a hyperplane", font_size=22,
                  color=DATA),
            label(r"so every optimum comes with a certificate a sceptic can check in one matrix multiplication",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        # a little picture: a cone and a point outside it, with a separating line
        o = np.array([4.6, -2.6, 0])
        cone = Polygon(o, o + np.array([1.6, 0.5, 0]), o + np.array([0.6, 1.3, 0]), stroke_width=0).set_fill(DATA, 0.3)
        r1 = Line(o, o + np.array([1.9, 0.6, 0]), color=DATA)
        r2 = Line(o, o + np.array([0.75, 1.62, 0]), color=DATA)
        pt = Dot(o + np.array([-0.4, 1.2, 0]), color=NO)
        sep = DashedLine(o + np.array([-0.6, -0.25, 0]), o + np.array([0.9, 1.9, 0]), color=HEAD)
        pic = VGroup(cone, r1, r2, pt, sep)
        with self.voiceover(
            (
            "Every linear program has a dual. <bookmark mark='a'/> Our primal maximizes over nonnegative x with "
            'A x at most b; its dual minimizes b transpose y with nonnegative y and A transpose y at least c. '
            "<bookmark mark='b'/> Weak duality holds for every feasible pair. <bookmark mark='c'/> If the primal "
            'is feasible with a finite optimum, strong duality gives an attained equal dual optimum. This does '
            "not say that every infeasible or unbounded program has an optimal pair. <bookmark mark='d'/> One "
            "form of Farkas' lemma says exactly one alternative holds: A x equals b for some nonnegative x, or a "
            "vector y satisfies A transpose y nonnegative and b transpose y negative. <bookmark mark='e'/> This "
            "is separation from the finitely generated cone of A's columns. <bookmark mark='f'/> To certify an "
            'optimum, check both feasibilities and equal objective values; matrix-vector checks suffice once the '
            'candidate pair is supplied.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
                if mk == "e":
                    self.play(FadeIn(pic))
        self.wait(0.3)
        self.clear_scene()

    def prices(self):
        d = load("duality")
        head = label(r"What the dual means: \ prices", font_size=34).to_edge(UP, buff=0.35)
        rows = []
        for i, nm in enumerate((r"resource 1", r"resource 2", r"resource 3")):
            rows.append([nm, rf"${num(d['y'][i])}$", rf"${num(d['shadow'][i])}$", rf"${num(d['slack'][i])}$"])
        tab = grid_table([r"", r"dual price $y_i$", r"profit from one more unit", r"unused at the optimum"], rows,
                         widths=[2.2, 2.4, 3.8, 3.4], row_h=0.5, font_size=22, mono_cols=(),
                         colors=[[WHITE, YES, HEAD, LAM]] * 3)
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label('$y_i$: \\ local marginal resource value while the basis remains valid',
                  font_size=22, color=YES),
            label(r"measured: \ adding one unit of resource 1 earns $\tfrac13$ here, \ less than $y_1 = 1$, \ because the "
                  r"basis changes", font_size=21, color=GREY_A),
            label(r"\textbf{complementary slackness}: \ a resource with slack has price 0; \ a product priced above its "
                  r"profit is not made", font_size=22, color=LAM),
            label(r"resource 2 has 1 unit to spare, \ so its price is 0; \ product 2's reduced cost is 3, \ so $x_2 = 0$",
                  font_size=21, color=GREY_A),
            label(r"in practice: \ every LP solver reports these prices; \ economists read them as market prices",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.26).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Dual variables are local sensitivity bounds. <bookmark mark='a'/> While the same optimal basis "
            'remains valid, y i gives the change in optimal value per infinitesimal unit of resource i. '
            "<bookmark mark='b'/> A whole extra unit can leave that range. We add one unit and resolve: resource "
            "one's gain is one third, although its original dual price is one. <bookmark mark='c'/> "
            'Complementary slackness says a resource with positive slack has zero price, and a product with '
            "strictly positive reduced cost is unused. <bookmark mark='d'/> Resource two has slack one and price "
            "zero; product two has reduced cost three and quantity zero. <bookmark mark='e'/> These prices "
            'describe this mathematical model and its local range; they need not equal the finite change from '
            'any proposed large intervention.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
