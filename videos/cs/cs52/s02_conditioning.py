from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 1.6 x 10^{16}."""
    e = math.floor(math.log10(abs(v)))
    m = v / 10 ** e
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


class Conditioning(VoiceoverScene):
    def construct(self):
        self.card()
        self.scalar()
        self.examples()
        self.matrix()
        self.hilbert()
        self.stability()

    def card(self):
        card = chapter_card(1, r"Conditioning and stability", r"How far can the answer move when the data moves?",
                            lit=(1948,), extra=((1948, r"Turing: \ the condition number"),), part=PART)
        with self.voiceover("Chapter one. Conditioning and stability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def scalar(self):
        head = label(r"How sensitive is a problem?", font_size=36).to_edge(UP, buff=0.3)
        cx = -3.9
        l_in = Line([cx - 2.6, 1.2, 0], [cx + 2.6, 1.2, 0], color=GREY_C)
        l_out = Line([cx - 2.6, -1.6, 0], [cx + 2.6, -1.6, 0], color=GREY_C)
        n_in = label(r"data $x$", font_size=20, color=DATA).next_to(l_in, UP, buff=0.35).align_to(l_in, LEFT)
        n_out = label(r"answer $f(x)$", font_size=20, color=HEAD).next_to(l_out, DOWN, buff=0.35).align_to(l_out,
                                                                                                         LEFT)
        r_in = Rectangle(width=0.36, height=0.2, stroke_width=0, fill_color=DATA, fill_opacity=0.9).move_to(
            [cx - 0.7, 1.2, 0])
        r_out = Rectangle(width=2.6, height=0.2, stroke_width=0, fill_color=HEAD, fill_opacity=0.9).move_to(
            [cx + 0.4, -1.6, 0])
        b_in = Brace(r_in, UP, buff=0.05, color=DATA)
        b_out = Brace(r_out, DOWN, buff=0.05, color=HEAD)
        t_in = MathTex(r"\Delta x", font_size=28, color=DATA).next_to(b_in, UP, buff=0.05)
        t_out = MathTex(r"\Delta f", font_size=28, color=HEAD).next_to(b_out, DOWN, buff=0.05)
        maps = VGroup(DashedLine(r_in.get_corner(DL), r_out.get_corner(UL), color=GREY_B, stroke_width=1.5),
                      DashedLine(r_in.get_corner(DR), r_out.get_corner(UR), color=GREY_B, stroke_width=1.5))
        fl = MathTex(r"f", font_size=30, color=GREY_A).next_to(maps, RIGHT, buff=0.15)
        ill = note(r"illustrative", font_size=16).next_to(l_out, DOWN, buff=0.85).align_to(l_out, RIGHT)
        cols = {r"\kappa": HEAD}
        rows = VGroup(
            cmath(r"\kappa", r"=", r"\frac{|\Delta f|\,/\,|f(x)|}{|\Delta x|\,/\,|x|}", colors=cols, font_size=36),
            cmath(r"\kappa", r"=", r"\frac{|f(x+\Delta x) - f(x)|}{|\Delta x|}", r"\cdot", r"\frac{|x|}{|f(x)|}",
                  colors=cols, font_size=36),
            cmath(r"\kappa", r"=", r"\left|\frac{x\,f'(x)}{f(x)}\right|", colors=cols, font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([3.3, 0.0, 0])
        whys = VGroup(
            label(r"relative change out, \ over relative change in", font_size=18, color=GREY_B),
            label(r"write $\Delta f$ out and regroup", font_size=18, color=GREY_B),
            label(r"let $\Delta x \to 0$: \ the quotient becomes $f'(x)$", font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        box = SurroundingRectangle(rows[2], color=HEAD, buff=0.15, stroke_width=2)
        whys[2].next_to(box, DOWN, buff=0.1).align_to(rows[2], LEFT)
        foot = label(r"no algorithm and no rounding appear: \ $\kappa$ belongs to the problem", font_size=21,
                     color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Before asking whether an algorithm is good, ask whether the problem is hard. <bookmark mark='a'/> "
            "Nudge the data x by a small relative amount. The answer moves too, and the ratio of the two relative "
            "changes is the problem's condition number, kappa. <bookmark mark='b'/> Write the change in f as f at "
            "x plus delta x, minus f at x, and regroup: a difference quotient, times x over f of x. "
            "<bookmark mark='c'/> As the nudge shrinks, the quotient becomes the derivative. Kappa is the size of x "
            "times f prime of x, over f of x. <bookmark mark='d'/> Notice what is missing: no algorithm, no "
            "rounding. Kappa belongs to the problem alone, and a problem with a large kappa is called ill "
            "conditioned."
        ) as vo:
            self.play(FadeIn(head), Create(l_in), Create(l_out), FadeIn(n_in), FadeIn(n_out))
            vo.wait_until("a")
            self.play(FadeIn(r_in), GrowFromCenter(b_in), FadeIn(t_in))
            self.play(Create(maps), FadeIn(fl), FadeIn(r_out), GrowFromCenter(b_out), FadeIn(t_out), FadeIn(ill))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Create(box))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def examples(self):
        sc = load("cond")["scalar"]
        head = label(r"Four problems, \ four condition numbers", font_size=36).to_edge(UP, buff=0.3)
        names = [r"$x - 1$ \ at $x = 1.000001$", r"$\sqrt{x}$", r"$e^{x}$ \ at $x = 100$",
                 r"$\tan x$ \ at $x = 1.5707$"]
        forms = [r"\kappa = \left|\frac{x}{x - 1}\right|", r"\kappa = \frac{1}{2}", r"\kappa = |x|",
                 r"\kappa = \left|\frac{x}{\sin x \cos x}\right|"]
        lo, hi = -1, 7
        bx0, bx1 = -0.4, 5.0

        def X(v):
            return bx0 + (bx1 - bx0) * (math.log10(v) - lo) / (hi - lo)
        cols = (NO, YES, HEAD, KERN)
        ys = [1.55, 0.45, -0.65, -1.75]
        hdr = VGroup(label(r"problem", font_size=19, color=GREY_B).move_to([-5.2, 2.45, 0]),
                     label(r"$\kappa$, \ derived", font_size=19, color=GREY_B).move_to([-2.2, 2.45, 0]),
                     label(r"$\kappa$, \ computed \ (log scale)", font_size=19, color=GREY_B).move_to(
                         [(bx0 + bx1) / 2, 2.45, 0]))
        rows, bars, vals = VGroup(), VGroup(), VGroup()
        for nm, fm, r, y, c in zip(names, forms, sc, ys, cols):
            n = label(nm, font_size=20, color=WHITE).move_to([-5.2, y, 0])
            f = MathTex(fm, font_size=28, color=c).move_to([-2.2, y, 0])
            rows.add(VGroup(n, f))
            k = r["kappa"]
            b = Rectangle(width=X(k) - bx0, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.8)
            b.move_to([bx0 + (X(k) - bx0) / 2, y, 0])
            bars.add(b)
            vals.add(label(rf"{k:,.0f}" if k >= 10 else rf"{k:g}", font_size=19, color=c).next_to(b, RIGHT,
                                                                                                   buff=0.12))
        axis = Line([bx0, -2.3, 0], [bx1, -2.3, 0], color=GREY_D)
        ticks = VGroup()
        for p in (0, 2, 4, 6):
            ticks.add(Line([X(10 ** p), -2.36, 0], [X(10 ** p), -2.24, 0], color=GREY_D))
            ticks.add(MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to([X(10 ** p), -2.3, 0], DOWN,
                                                                                 buff=0.12))
        one = DashedLine([X(1), 2.1, 0], [X(1), -2.3, 0], color=GREY_C, stroke_width=1.2)
        foot = wrapped_label(r"you lose about $\log_{10}\kappa$ of your sixteen digits: \ subtracting nearby numbers "
                             r"loses six of them here, \ Part 4's cancellation, \ before any algorithm runs", 12.6,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Four small problems show the range. <bookmark mark='a'/> Subtracting one from a number very close to "
            "one: kappa is x over x minus one, about a million. That is Part 4's cancellation, and now we see it "
            "is the problem's fault, not the computer's. <bookmark mark='b'/> The square root has kappa one half "
            "everywhere: it halves relative errors. <bookmark mark='c'/> The exponential has kappa equal to x, so at "
            "x equal to one hundred, kappa is a hundred. <bookmark mark='d'/> The tangent, close to a right "
            "angle, has kappa about sixteen thousand. <bookmark mark='e'/> The rule of thumb: from data good "
            "to sixteen digits, expect about sixteen, minus the logarithm of kappa to base ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(axis), FadeIn(ticks), Create(one))
            for mk, rw, b, v in zip("abcd", rows, bars, vals):
                vo.wait_until(mk)
                self.play(FadeIn(rw), GrowFromEdge(b, LEFT), FadeIn(v))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def matrix(self):
        head = label(r"The condition number of a matrix", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\Delta b": DATA, r"\Delta x": HEAD, r"\|A\|\,\|A^{-1}\|": KERN, r"\kappa(A)": KERN}
        rows = VGroup(
            cmath(r"A", r"\Delta x", r"=", r"\Delta b", colors=cols, font_size=34),
            cmath(r"\Delta x", r"=", r"A^{-1}", r"\Delta b", colors=cols, font_size=34),
            cmath(r"\|\Delta x\|", r"\le", r"\|A^{-1}\|", r"\,\|\Delta b\|", colors=cols, font_size=34),
            cmath(r"\frac{\|\Delta x\|}{\|x\|}", r"\le", r"\|A\|\,\|A^{-1}\|", r"\frac{\|\Delta b\|}{\|b\|}",
                  colors=cols, font_size=34),
            cmath(r"\kappa(A)", r"=", r"\|A\|\,\|A^{-1}\|", r"=", r"\frac{\sigma_{\max}}{\sigma_{\min}}",
                  colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-4.6, -0.2, 0]).to_edge(LEFT, buff=0.4)
        whys = VGroup(
            label(r"subtract $Ax = b$ from $A(x + \Delta x) = b + \Delta b$", font_size=18, color=GREY_B),
            label(r"solve for the change", font_size=18, color=GREY_B),
            label(r"take norms", font_size=18, color=GREY_B),
            label(r"divide by $\|x\| \ge \|b\| / \|A\|$", font_size=18, color=GREY_B),
            label(r"in the 2-norm \ (Chapter 5)", font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.35)
        x0 = max(w.get_left()[0] for w in whys)
        for w in whys:
            w.align_to([x0, 0, 0], LEFT)
        # the unit circle and its image under an illustrative A
        c0 = np.array([2.7, 0.7, 0])
        c1 = np.array([5.4, 0.7, 0])
        circ = Circle(radius=0.75, color=DATA, stroke_width=3).move_to(c0)
        ell = Ellipse(width=2.6, height=0.5, color=HEAD, stroke_width=3).rotate(0.5).move_to(c1)
        ax1 = Line(c1, c1 + 1.3 * np.array([math.cos(0.5), math.sin(0.5), 0]), color=KERN, stroke_width=3)
        ax2 = Line(c1, c1 + 0.25 * np.array([-math.sin(0.5), math.cos(0.5), 0]), color=KERN, stroke_width=3)
        s1 = MathTex(r"\sigma_{\max}", font_size=24, color=KERN).next_to(ax1.get_end(), UP, buff=0.08)
        s2 = MathTex(r"\sigma_{\min}", font_size=24, color=KERN).next_to(ax2.get_end(), LEFT, buff=0.1)
        arr = Arrow(c0 + RIGHT * 0.85, c1 + LEFT * 1.25, buff=0.05, color=GREY_B, stroke_width=2.5)
        al = MathTex(r"A", font_size=28).next_to(arr, UP, buff=0.05)
        cap = wrapped_label(r"$A$ turns the unit circle into an ellipse; \ $\kappa$ is how flat it is", 4.6,
                            font_size=18, color=GREY_A).next_to(VGroup(circ, ell), DOWN, buff=0.3)
        ill = note(r"illustrative", font_size=16).next_to(cap, DOWN, buff=0.1)
        with self.voiceover(
            "For a linear system A x equals b, perturb the right-hand side. <bookmark mark='a'/> Subtract the two "
            "equations: A times delta x equals delta b. <bookmark mark='b'/> So delta x is A inverse times delta "
            "b, and its size is at most the norm of A inverse times the size of delta b. <bookmark mark='c'/> "
            "Since b is A x, x is at least as large as b over the norm of A. Divide: the relative change in x is at "
            "most the norm of A, times the norm of A inverse, times the relative change in b. <bookmark mark='d'/> "
            "That product is the matrix's condition number, a name Alan Turing gave it in 1948. "
            "<bookmark mark='e'/> Geometrically, A turns the unit circle into an ellipse, and kappa is its longest "
            "axis over its shortest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(whys[4]))
            vo.wait_until("e")
            self.play(Create(circ), GrowArrow(arr), FadeIn(al))
            self.play(TransformFromCopy(circ, ell), FadeIn(cap), FadeIn(ill))
            self.play(Create(ax1), Create(ax2), FadeIn(s1), FadeIn(s2))
        self.wait(0.4)
        self.clear_scene()

    def hilbert(self):
        hil = load("cond")["hilbert"]
        eps = 2.0 ** -52
        head = label(r"Hilbert's matrix: \ hard by nature", font_size=36).to_edge(UP, buff=0.3)
        H = Matrix([[r"1", r"\tfrac12", r"\tfrac13", r"\tfrac14"], [r"\tfrac12", r"\tfrac13", r"\tfrac14",
                                                                     r"\tfrac15"],
                    [r"\tfrac13", r"\tfrac14", r"\tfrac15", r"\tfrac16"], [r"\tfrac14", r"\tfrac15", r"\tfrac16",
                                                                           r"\tfrac17"]],
                   element_to_mobject_config={"font_size": 30}, h_buff=0.85, v_buff=0.7).move_to([-4.3, 0.6, 0])
        Hl = MathTex(r"H_4 =", font_size=32).next_to(H, LEFT, buff=0.15)
        hdef = label(r"$h_{ij} = \dfrac{1}{i + j - 1}$", font_size=24, color=DATA).next_to(H, DOWN, buff=0.35)
        hn = wrapped_label(r"neighbouring columns are almost parallel, \ so $H x = b$ barely pins $x$ down", 4.6,
                           font_size=19, color=GREY_A).next_to(hdef, DOWN, buff=0.3)
        base_y, per = -2.5, 0.26
        xs = [0.9, 2.6, 4.3]
        base = Line([0.0, base_y, 0], [5.4, base_y, 0], color=GREY_C)
        bars, tops, names = VGroup(), VGroup(), VGroup()
        for r, x in zip(hil, xs):
            h = per * math.log10(r["kappa"])
            b = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=NO if r["kappa"] > 1 / eps else KERN,
                          fill_opacity=0.85).move_to([x, base_y + h / 2, 0])
            bars.add(b)
            tops.add(MathTex(sci(r["kappa"]), font_size=22, color=WHITE).next_to(b, UP, buff=0.08))
            names.add(MathTex(rf"n = {r['n']}", font_size=24, color=GREY_A).next_to([x, base_y, 0], DOWN, buff=0.15))
        ly = base_y + per * math.log10(1 / eps)
        lim = DashedLine([0.0, ly, 0], [5.4, ly, 0], color=HEAD, stroke_width=2)
        liml = label(rf"$1/\varepsilon \approx {sci(1 / eps)}$", font_size=18, color=HEAD).next_to(lim, UP,
                                                                                                buff=0.08).align_to(
            lim, LEFT)
        kl = label(r"$\kappa(H_n)$, \ computed", font_size=19, color=GREY_B).move_to([2.2, 2.5, 0])
        left = [max(0, round(16 - math.log10(r["kappa"]))) for r in hil]
        dig = label(rf"digits that survive: \ about {left[0]}, \ {left[1]} \ and {left[2]} of 16", font_size=20,
                    color=WHITE).next_to(base, DOWN, buff=0.65)
        with self.voiceover(
            "Some problems are ill conditioned through and through. <bookmark mark='a'/> David Hilbert's matrix "
            "has entries one over i plus j minus one. It arises when fitting polynomials by least squares, and its "
            "neighbouring columns are so nearly parallel that the system barely determines x. "
            "<bookmark mark='b'/> Our instrument measures its condition number: about sixteen thousand for size "
            "four, fifteen billion for size eight, <bookmark mark='c'/> and for size twelve, one point six times "
            "ten to the sixteen, past one over machine epsilon. <bookmark mark='d'/> By the rule of thumb, twelve "
            "digits survive at size four, six at size eight, and none at size twelve, whatever algorithm we use."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(H), FadeIn(Hl), FadeIn(hdef), FadeIn(hn))
            vo.wait_until("b")
            self.play(Create(base), FadeIn(kl), FadeIn(names))
            for b, t in zip(bars[:2], tops[:2]):
                self.play(GrowFromEdge(b, DOWN), FadeIn(t))
            vo.wait_until("c")
            self.play(Create(lim), FadeIn(liml))
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(tops[2]))
            vo.wait_until("d")
            self.play(FadeIn(dig))
        self.wait(0.4)
        self.clear_scene()

    def stability(self):
        head = label(r"Stability: \ the algorithm's share", font_size=36).to_edge(UP, buff=0.3)
        X = Ellipse(width=3.6, height=2.6, color=DATA, stroke_width=2, fill_color=DATA, fill_opacity=0.08).move_to(
            [-4.0, 0.4, 0])
        Y = Ellipse(width=3.6, height=2.6, color=YES, stroke_width=2, fill_color=YES, fill_opacity=0.08).move_to(
            [4.0, 0.4, 0])
        xl = label(r"data", font_size=20, color=DATA).next_to(X, UP, buff=0.1)
        yl = label(r"answers", font_size=20, color=YES).next_to(Y, UP, buff=0.1)
        px = Dot([-4.4, 0.7, 0], color=WHITE)
        pxt = Dot([-3.9, 0.15, 0], color=HEAD)
        ball = Circle(radius=0.85, color=HEAD, stroke_width=1.5).move_to(px).set_stroke(opacity=0.6)
        py = Dot([3.6, 1.0, 0], color=WHITE)
        pyt = Dot([4.4, -0.1, 0], color=KERN)
        lx = MathTex(r"x", font_size=28).next_to(px, LEFT, buff=0.1)
        lxt = MathTex(r"\tilde x", font_size=28, color=HEAD).next_to(pxt, DOWN, buff=0.1)
        ly = MathTex(r"f(x)", font_size=28).next_to(py, UP, buff=0.1)
        lyt = MathTex(r"\tilde f(x) = f(\tilde x)", font_size=28, color=KERN).next_to(pyt, DOWN, buff=0.12)
        a_f = CurvedArrow(px.get_center() + RIGHT * 0.1, py.get_center() + LEFT * 0.1, angle=-0.35, color=WHITE,
                          stroke_width=2.5)
        af = MathTex(r"f \ \text{(exact)}", font_size=24).next_to(a_f, UP, buff=0.05)
        a_alg = DashedVMobject(CurvedArrow(px.get_center() + RIGHT * 0.1, pyt.get_center() + LEFT * 0.12,
                                           angle=0.12, color=KERN, stroke_width=2.5), num_dashes=30)
        aalg = label(r"the algorithm $\tilde f$, \ rounding as it goes", font_size=19, color=KERN).move_to(
            [0, 0.72, 0])
        a_back = CurvedArrow(pxt.get_center() + RIGHT * 0.1, pyt.get_center() + LEFT * 0.12, angle=0.35,
                             color=HEAD, stroke_width=2)
        aback = MathTex(r"f", font_size=24, color=HEAD).next_to(a_back, DOWN, buff=0.05)
        lines = VGroup(
            label(r"\textbf{backward stable}: \ $\tilde f(x) = f(\tilde x)$ \ for some $\tilde x$ with "
                  r"$|\tilde x - x| / |x|$ a small multiple of $\varepsilon$", font_size=21, color=HEAD),
            label(r"then the answer's error is about $\kappa \times \varepsilon$: \ the problem's conditioning "
                  r"times the algorithm's stability", font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Conditioning is the problem's share of the error. Stability is the algorithm's. "
            "<bookmark mark='a'/> The exact map f takes data x to the answer f of x. The algorithm, f tilde, "
            "rounds at every step and lands somewhere else. <bookmark mark='b'/> James Wilkinson's question was: is "
            "there nearby data, x tilde, for which that wrong answer is exactly right? If there always is, within a "
            "small multiple of machine epsilon, the algorithm is called backward stable. <bookmark mark='c'/> A "
            "backward stable algorithm commits no more error than rounding the data once would, and conditioning "
            "turns that into the answer's error. The hook's two equations were well conditioned; elimination "
            "without row swaps was simply unstable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(X), FadeIn(Y), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(px), FadeIn(lx), FadeIn(py), FadeIn(ly), Create(a_f), FadeIn(af))
            self.play(Create(a_alg), FadeIn(aalg), FadeIn(pyt))
            vo.wait_until("b")
            self.play(Create(ball), FadeIn(pxt), FadeIn(lxt))
            self.play(Create(a_back), FadeIn(aback), FadeIn(lyt))
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES)
