from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Orient(VoiceoverScene):
    def construct(self):
        self.card()
        self.area()
        self.rounding()
        self.underflow()
        self.adaptive()

    def card(self):
        card = chapter_card(1, r"The one primitive", r"Left, right, or on the line?", lit=(1997, 2008),
                            extra=((1997, r"Shewchuk's predicates"), (2008, r"Kettner et al.")), part=PART)
        with self.voiceover("Chapter one. The one primitive."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def area(self):
        head = label(r"Orientation is the sign of an area", font_size=34).to_edge(UP, buff=0.35)
        P, Q, R = np.array([-5.6, -1.6, 0]), np.array([-1.6, -2.2, 0]), np.array([-2.6, 1.6, 0])
        tri = Polygon(P, Q, R, color=DATA, stroke_width=2.5).set_fill(DATA, 0.25)
        lab = VGroup(MathTex("p", font_size=32).next_to(P, LEFT, buff=0.1),
                     MathTex("q", font_size=32).next_to(Q, RIGHT, buff=0.1),
                     MathTex("r", font_size=32).next_to(R, UP, buff=0.1))
        arc = CurvedArrow(P + (Q - P) * 0.35 + UP * 0.35, P + (R - P) * 0.35 + RIGHT * 0.35, angle=1.2, color=HEAD,
                          stroke_width=2, tip_length=0.14)
        R2 = np.array([-3.2, -3.4, 0])
        side = VGroup(
            MathTex(r"\mathrm{orient}(p, q, r) = \det\begin{pmatrix} q_x - p_x & q_y - p_y \\ r_x - p_x & r_y - p_y"
                    r"\end{pmatrix}", font_size=32, color=LAM),
            label(r"twice the signed area of the triangle $pqr$", font_size=22, color=WHITE),
            label(r"$> 0$: \ $r$ is left of $p \to q$ \ (counter-clockwise)", font_size=22, color=DATA),
            label(r"$< 0$: \ right \ (clockwise); \ \ $= 0$: \ collinear", font_size=22, color=YES),
            label(r"hulls, \ sweeps, \ triangulations and polygon tests \\ are all built from this one sign", font_size=22,
                  color=HEAD),
            label(r"its cousin, \ \textbf{in-circle}, \ is a $3 \times 3$ determinant \ (chapter 6)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        if side.width > 7.4:
            side.width = 7.4
            side.to_edge(RIGHT, buff=0.45)
        tri2 = Polygon(P, Q, R2, color=YES, stroke_width=2.5).set_fill(YES, 0.2)
        with self.voiceover(
            "Almost every algorithm in this part asks one question, over and over. <bookmark mark='a'/> Walk from p "
            "to q; is r on your left? The answer is the sign of a two by two determinant built from the differences "
            "of the coordinates. <bookmark mark='b'/> The determinant is twice the signed area of the triangle p q "
            "r: <bookmark mark='c'/> positive when the three points turn counter-clockwise, <bookmark mark='d'/> "
            "negative when they turn clockwise, and zero when they lie on one line. <bookmark mark='e'/> Convex "
            "hulls, sweeps, triangulations and point-in-polygon tests are all built from this sign. <bookmark "
            "mark='f'/> Its cousin, the in-circle test, asks whether a point lies inside the circle through three "
            "others; it is a three by three determinant, and we will meet it with Delaunay."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tri), FadeIn(lab), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), tri.animate.set_fill(DATA, 0.45))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(arc))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Transform(tri, tri2), lab[2].animate.next_to(R2, DOWN, buff=0.1),
                      FadeOut(arc))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def rounding(self):
        head = label(r"Why floating point gets it wrong", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"\underbrace{(q_x - p_x)(r_y - p_y)}_{a} \;-\; \underbrace{(q_y - p_y)(r_x - p_x)}_{b}",
                    font_size=34, color=LAM),
            label('finite normal operations, round to nearest: \\ relative error $\\varepsilon = 2^{-53}$',
                  font_size=22, color=WHITE),
            label(r"near a line, \ $a$ and $b$ almost cancel: \ the rounding errors can be larger than $a - b$ itself",
                  font_size=22, color=NO),
            MathTex(r"|\,\text{error}\,| \;\le\; (3 + 16\varepsilon)\,\varepsilon\,(|a| + |b|)", font_size=34,
                    color=YES),
            label('Shewchuk (1997): \\ proved error bounds for the arithmetic domain assumed', font_size=22, color=YES),
            label(r"Kettner et al. (2008): \ with wrong signs, \ incremental hulls lose points, \ loop, \ or come out "
                  r"non-convex", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Why does it fail? <bookmark mark='a'/> The determinant is a difference of two products, a minus b. <bookmark mark='b'/> For finite normal operations, rounding to the nearest double gives a small relative-error bound; underflow and overflow need separate handling. <bookmark mark='c'/> Near a line, a and b are almost equal, and their difference is tiny: smaller than the rounding errors made computing them. The sign of the result is then noise. <bookmark mark='d'/> But the error can be bounded. Jonathan Shewchuk proved that it is at most about three epsilon times the sizes of a and b. <bookmark mark='e'/> Within those arithmetic assumptions, a computed magnitude strictly exceeding the bound certifies the sign. <bookmark mark='f'/> When it isn't, ignoring the problem is dangerous: Kettner's paper shows the textbook incremental hull losing points, looping, and returning a polygon that is not convex."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def adaptive(self):
        o = load("orient")
        head = label(r"Adaptive exact predicates", font_size=34).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"1. \ compute $a - b$ in floating point", font_size=23, color=WHITE),
            label('2. \\ normal finite arithmetic and $|a-b|>$ bound: \\ accept the sign', font_size=23, color=YES),
            label(r"3. \ otherwise: \ redo it exactly \ (Shewchuk: \ expansions of doubles; \ here, \ rationals)",
                  font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = []
        for r in o["rows"]:
            rows.append([r["inputs"], f"{r['float_ns']:.0f} ns", words(r["float_wrong"]), (f"{r['adaptive_ns']:.0f} ns" if r['adaptive_ns'] < 1000 else
                                                                         f"{r['adaptive_ns'] / 1000:.1f} $\\mu$s"),
                         f"{100 * r['exact_share']:.0f}\\%", f"{r['exact_ns'] / 1000:.1f} µs".replace("µ", r"$\mu$")])
        tab = grid_table([r"20,000 tests", r"float", r"float wrong", r"adaptive", r"needed exact", r"always exact"],
                         rows, widths=[2.8, 1.5, 2.0, 1.8, 2.2, 2.2], row_h=0.5, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, NO, YES, HEAD, GREY_A]] * len(rows))
        tab.next_to(steps, DOWN, buff=0.5).set_x(0)
        foot = VGroup(
            label('finite normal inputs often pass the filter; \\ measured fallback rates and times are instance-specific',
                  font_size=21, color=YES),
            label('integer hulls and incremental triangulations use Python integers; \\\\ floating constructions remain numerical', font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A filtered predicate can combine speed with an exact sign. <bookmark mark='a'/> First compute the determinant in floating point. <bookmark mark='b'/> Trust it only when the operations remain finite and normal and its magnitude strictly exceeds the certified error bound. Underflow, overflow and ambiguous signs take the exact route. <bookmark mark='c'/> Shewchuk uses expansions of doubles; our teaching fallback uses rational arithmetic on the original represented inputs. <bookmark mark='d'/> The table records twenty thousand seeded tests of each kind, including raw timing repetitions and exact reference signs. Fallback share and speed depend on these inputs and this implementation. <bookmark mark='e'/> Filtering saves exact work when the floating result is certified; exactness is not universally free. <bookmark mark='f'/> Integer hulls and incremental triangulations use Python's unbounded integers. Fortune's sweep, linear programming and robot planning still use floating constructions, so an exact predicate alone does not make every later coordinate exact."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.wait(0.3)
        self.clear_scene()


    def underflow(self):
        x = 1e-200
        points = ((0., 0.), (x, 0.), (0., x))
        floating = G.orient_float(*points)
        sign, exact = G.orient_adaptive(*points)
        assert floating == 0 and sign == 1 and exact
        head = label('A nonzero determinant can round to zero', font_size=33).to_edge(UP, buff=.35)
        P, Q, R = np.array([-4.8,-1.4,0]), np.array([-2.,-1.4,0]), np.array([-4.8,1.4,0])
        triangle = Polygon(P,Q,R,color=DATA,stroke_width=3).set_fill(DATA,.2)
        tags = VGroup(MathTex('p=(0,0)',font_size=29).next_to(P,DOWN),
                      MathTex('q=(x,0)',font_size=29).next_to(Q,DOWN),
                      MathTex('r=(0,x)',font_size=29).next_to(R,UP))
        scale_note = label('schematic coordinates; shape enlarged',font_size=19,color=GREY_A).move_to(LEFT*3.4+DOWN*2.5)
        rows = VGroup(
            MathTex(r'x=\operatorname{fl}(10^{-200})>0',font_size=36,color=DATA),
            MathTex(r'\det=x^2>0\quad\quad',font_size=36,color=YES),
            MathTex(r'\operatorname{fl}(x^2)=0',font_size=36,color=NO),
            label('a rounded zero estimate is not a sign certificate',font_size=23,color=NO),
            label('unsafe arithmetic: use the exact fallback',font_size=24,color=YES),
        ).arrange(DOWN,buff=.4).move_to(RIGHT*2.7)
        if rows.width>6.9:rows.width=6.9;rows.set_x(2.7)
        with self.voiceover("Here is why the arithmetic domain matters. The stored binary64 number x approximates ten to the minus two hundred. <bookmark mark='a'/> These represented coordinates form a genuine counter-clockwise triangle: the exact determinant is x squared, which is positive. <bookmark mark='b'/> Its floating product underflows to zero. A rounded zero and a zero error estimate do not prove that the exact sign is zero. <bookmark mark='c'/> Our filter routes this case to rational arithmetic and returns positive. Overflow also takes that route. The diagram enlarges the coordinates so we can see the geometry.") as vo:
            self.play(FadeIn(head),Create(triangle),FadeIn(tags),FadeIn(scale_note),FadeIn(rows[0]))
            vo.wait_until('a');self.play(FadeIn(rows[1]))
            vo.wait_until('b');self.play(FadeIn(rows[2]),FadeIn(rows[3]))
            vo.wait_until('c');self.play(FadeIn(rows[4]),Indicate(triangle,color=YES))
        self.wait(.3);self.clear_scene()

