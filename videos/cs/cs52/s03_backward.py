from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 1.6 x 10^{16}."""
    e = math.floor(math.log10(abs(v)))
    m = v / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


class Backward(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.picture()
        self.residual()
        self.hilbert()
        self.digits()

    def card(self):
        card = chapter_card(2, r"Backward error analysis",
                            r"Is the computed answer the exact answer to a nearby question?", lit=(1963, 1970),
                            extra=((1963, r"Wilkinson: \ \textit{Rounding Errors in Algebraic Processes}"),
                                   (1970, r"Wilkinson's Turing Award")), part=PART)
        with self.voiceover("Chapter two. Backward error analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"Wilkinson's model of rounding", font_size=36).to_edge(UP, buff=0.3)
        axiom = MathTex(r"\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)",
                        r",\qquad |\delta| \le u = 2^{-53} \approx 1.1 \times 10^{-16}", font_size=36)
        axiom[0].set_color(HEAD)
        axiom.next_to(head, DOWN, buff=0.4)
        src = note(r"$\circ$ is $+, -, \times, \div$; \ $u$ is the unit roundoff of IEEE double precision \ "
                   r"(Part 4)", font_size=17).next_to(axiom, DOWN, buff=0.15)
        cols = {r"s": YES, r"\hat a": DATA, r"\hat b": DATA, r"\hat c": DATA}
        rows = VGroup(
            cmath(r"s", r"=", r"\mathrm{fl}\big(\mathrm{fl}(a + b) + c\big)", colors=cols, font_size=34),
            cmath(r"s", r"=", r"\big((a + b)(1 + \delta_1) + c\big)(1 + \delta_2)", colors=cols, font_size=34),
            cmath(r"s", r"=", r"a\,(1 + \delta_1)(1 + \delta_2)", r"+", r"b\,(1 + \delta_1)(1 + \delta_2)", r"+",
                  r"c\,(1 + \delta_2)", colors=cols, font_size=34),
            cmath(r"s", r"=", r"\hat a", r"+", r"\hat b", r"+", r"\hat c", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.next_to(src, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        whys = VGroup(
            label(r"two additions, \ each rounded once", font_size=18, color=GREY_B),
            label(r"apply the model twice", font_size=18, color=GREY_B),
            label(r"multiply out", font_size=18, color=GREY_B),
            label(r"the \textit{exact} sum of changed data", font_size=18, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        whys.set_x(4.6)
        for w in whys:
            w.align_to(whys[2], LEFT)
        whys.shift(RIGHT * (6.7 - whys.get_right()[0]))
        bound = label(r"with $\dfrac{|\hat a - a|}{|a|} \le 2u + u^2$: \ a \textbf{backward error} of about two "
                      r"roundings", font_size=21, color=DATA).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "James Wilkinson learned his trade beside Turing at the National Physical Laboratory, and he analysed "
            "rounding with one simple model. <bookmark mark='a'/> Every floating-point operation returns the exact "
            "result times one plus delta, where delta is at most the unit roundoff, about ten to the minus sixteen "
            "in double precision. <bookmark mark='b'/> Add three numbers. Each addition rounds once. "
            "<bookmark mark='c'/> Multiply it out, and each input picks up its own small factor. "
            "<bookmark mark='d'/> So the computed sum is the exact sum of slightly different numbers, each changed "
            "by about two roundings. That is a backward error: not how wrong the answer is, but how far the data "
            "must move to make it exactly right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(axiom), FadeIn(src))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(*[ReplacementTransform(x, y) for x, y in zip(rows[2].copy(), rows[3])], FadeIn(whys[3]))
            self.play(FadeIn(bound))
        self.wait(0.4)
        self.clear_scene()

    def picture(self):
        head = label(r"Forward error $\le$ condition $\times$ backward error", font_size=36).to_edge(UP, buff=0.3)
        cx = -3.8
        l_in = Line([cx - 2.7, 1.3, 0], [cx + 2.7, 1.3, 0], color=GREY_C)
        l_out = Line([cx - 2.7, -1.5, 0], [cx + 2.7, -1.5, 0], color=GREY_C)
        n_in = label(r"data", font_size=20, color=DATA).next_to(l_in, UP, buff=0.12).align_to(l_in, RIGHT)
        n_out = label(r"answers", font_size=20, color=YES).next_to(l_out, UP, buff=0.12).align_to(l_out, RIGHT)
        px, pxh = Dot([cx - 1.7, 1.3, 0], color=WHITE), Dot([cx - 0.7, 1.3, 0], color=HEAD)
        py, pyh = Dot([cx - 1.9, -1.5, 0], color=WHITE), Dot([cx + 1.4, -1.5, 0], color=KERN)
        tx = MathTex(r"x", font_size=28).next_to(px, DL, buff=0.08)
        txh = MathTex(r"\hat x", font_size=28, color=HEAD).next_to(pxh, UR, buff=0.08)
        ty = MathTex(r"y", font_size=28).next_to(py, LEFT, buff=0.12)
        tyh = MathTex(r"\hat y", font_size=28, color=KERN).next_to(pyh, UR, buff=0.08)
        a1 = Arrow(px.get_center(), py.get_center(), buff=0.12, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(pxh.get_center(), pyh.get_center(), buff=0.12, color=HEAD, stroke_width=2.5)
        a3 = DashedVMobject(Arrow(px.get_center(), pyh.get_center(), buff=0.12, color=KERN, stroke_width=2),
                            num_dashes=24)
        fa = MathTex(r"f", font_size=26, color=GREY_B).next_to(a1, LEFT, buff=0.08)
        fb = MathTex(r"f", font_size=26, color=HEAD).next_to(a2.get_center(), UR, buff=0.08)
        alg = label(r"dashed: \ what the algorithm computes", font_size=17, color=KERN).to_edge(
            DOWN, buff=0.45).align_to(l_out, LEFT)
        bb = BraceBetweenPoints(px.get_center() + UP * 0.12, pxh.get_center() + UP * 0.12, UP, color=HEAD)
        bt = label(r"backward error", font_size=17, color=HEAD).next_to(bb, UP, buff=0.05)
        fb2 = BraceBetweenPoints(py.get_center() + DOWN * 0.12, pyh.get_center() + DOWN * 0.12, DOWN, color=NO)
        ft = label(r"forward error", font_size=17, color=NO).next_to(fb2, DOWN, buff=0.05)
        cols = {r"\kappa": KERN, r"\text{forward}": NO, r"\text{backward}": HEAD,
                r"\left|\frac{x\,f'(x)}{f(x)}\right|": KERN, r"\frac{|\hat y - y|}{|y|}": NO,
                r"\frac{|\Delta x|}{|x|}": HEAD}
        rows = VGroup(
            cmath(r"\hat y", r"=", r"f(\hat x)", r"=", r"f(x + \Delta x)", colors=cols, font_size=34),
            cmath(r"\hat y - y", r"\approx", r"f'(x)\,\Delta x", colors=cols, font_size=34),
            cmath(r"\frac{|\hat y - y|}{|y|}", r"\approx", r"\left|\frac{x\,f'(x)}{f(x)}\right|", r"\cdot",
                  r"\frac{|\Delta x|}{|x|}", colors=cols, font_size=34),
            cmath(r"\text{forward}", r"\lesssim", r"\kappa", r"\times", r"\text{backward}", colors=cols,
                  font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.4, 0.1, 0])
        whys = VGroup(label(r"the computed answer is exact for nearby data", font_size=18, color=GREY_B),
                      label(r"to first order in $\Delta x$", font_size=18, color=GREY_B),
                      label(r"divide by $y = f(x)$; \ multiply and divide by $x$", font_size=18, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        box = SurroundingRectangle(rows[3], color=HEAD, buff=0.15, stroke_width=2)
        with self.voiceover(
            "Why ask the question backwards? Because the two errors are tied together by the condition number. "
            "<bookmark mark='a'/> Suppose the computed answer, y hat, is the exact answer for data x plus delta "
            "x. <bookmark mark='b'/> To first order, the answer moves by f prime of x times delta x. "
            "<bookmark mark='c'/> Divide by y, and multiply and divide by x: the relative forward error is kappa "
            "times the relative backward error. <bookmark mark='d'/> Forward error is at most the condition number "
            "times the backward error. The algorithm controls one factor and the problem the other, and each can "
            "be studied on its own."
        ) as vo:
            self.play(FadeIn(head), Create(l_in), Create(l_out), FadeIn(n_in), FadeIn(n_out))
            self.play(FadeIn(px), FadeIn(tx), FadeIn(py), FadeIn(ty), GrowArrow(a1), FadeIn(fa))
            vo.wait_until("a")
            self.play(Create(a3), FadeIn(alg), FadeIn(pyh), FadeIn(tyh))
            self.play(FadeIn(pxh), FadeIn(txh), GrowArrow(a2), FadeIn(fb), GrowFromCenter(bb), FadeIn(bt))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]), GrowFromCenter(fb2),
                      FadeIn(ft))
            vo.wait_until("d")
            self.play(*[ReplacementTransform(x, y) for x, y in zip(rows[2].copy(), rows[3])])
            self.play(Create(box))
        self.wait(0.4)
        self.clear_scene()

    def residual(self):
        head = label(r"For $Ax = b$, \ the residual is the backward error", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"r": DATA, r"\Delta A": HEAD, r"\eta": HEAD, r"\kappa(A)\,\eta": KERN}
        rows = VGroup(
            cmath(r"r", r"=", r"b - A\hat x", colors=cols, font_size=34),
            cmath(r"(A + \Delta A)\,\hat x = b", r",\qquad", r"\Delta A", r"=", r"\frac{r\,\hat x^{\mathsf T}}"
                  r"{\|\hat x\|^2}", colors=cols, font_size=34),
            cmath(r"\frac{\|\Delta A\|}{\|A\|}", r"=", r"\frac{\|r\|}{\|A\|\,\|\hat x\|}", r"=", r"\eta",
                  colors=cols, font_size=34),
            cmath(r"x - \hat x", r"=", r"A^{-1} r", colors=cols, font_size=34),
            cmath(r"\frac{\|x - \hat x\|}{\|\hat x\|}", r"\le", r"\|A^{-1}\|\,\frac{\|r\|}{\|\hat x\|}", r"=",
                  r"\kappa(A)\,\eta", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        whys = VGroup(
            label(r"what $\hat x$ leaves over; \ anyone can compute it", font_size=18, color=GREY_B),
            label(r"a rank-one change makes $\hat x$ exact: \ $\Delta A\,\hat x = r$", font_size=18, color=GREY_B),
            label(r"the backward error $\eta$, \ relative to $A$", font_size=18, color=HEAD),
            label(r"since $A x - A \hat x = b - A\hat x$", font_size=18, color=GREY_B),
            label(r"take norms; \ $\|r\| = \eta\,\|A\|\,\|\hat x\|$", font_size=18, color=KERN),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        x0 = max(w.get_left()[0] for w in whys)
        for w in whys:
            w.align_to([x0, 0, 0], LEFT)
        box = SurroundingRectangle(rows[4][4], color=KERN, buff=0.12, stroke_width=2)
        with self.voiceover(
            "For linear systems the rule is exact, and the backward error can be measured. "
            "<bookmark mark='a'/> Given a computed solution x hat, form the residual: b minus A x hat. "
            "<bookmark mark='b'/> Add to A the rank-one matrix r times x hat transposed, over the size of x hat "
            "squared, and x hat solves the changed system exactly. <bookmark mark='c'/> That change, relative to A, "
            "has size the norm of r over the norm of A times the norm of x hat. Call it eta: it is computed after "
            "the fact, from things we have. <bookmark mark='d'/> Meanwhile the true error, x minus x hat, is A "
            "inverse times r. <bookmark mark='e'/> Take norms, and the relative error is at most kappa times eta, "
            "with no approximation at all."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                if i in (0, 3):
                    self.play(Write(rows[i]), FadeIn(whys[i]))
                else:
                    self.play(TransformMatchingTex(rows[i - 1].copy(), rows[i]), FadeIn(whys[i]))
            self.play(Create(box))
        self.wait(0.4)
        self.clear_scene()

    def hilbert(self):
        rows = load("backward")["rows"]
        head = label(r"Testing the rule on Hilbert systems", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[3, 13, 1], y_range=[-18, 0, 2], x_length=7.2, y_length=4.7, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.3, -0.4, 0])
        xt = VGroup(*[label(rf"{n}", font_size=17, color=GREY_B).next_to(ax.c2p(n, -18), DOWN, buff=0.12)
                      for n in (4, 6, 8, 10, 12)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to(ax.c2p(3, p), LEFT, buff=0.1)
                      for p in (-16, -12, -8, -4, 0)])
        xl = label(r"size $n$ of the Hilbert matrix", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yl = label(r"relative error", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        yl.shift(RIGHT * 0.45)

        def series(key, color, dashed=False):
            pts = [ax.c2p(r["n"], math.log10(r[key])) for r in rows]
            line = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
            if dashed:
                line = DashedVMobject(line, num_dashes=40)
            dots = VGroup(*[Dot(p, radius=0.06, color=color) for p in pts])
            return VGroup(line, dots)
        back = series("backward", YES)
        fwd = series("forward", NO)
        bnd = series("bound", HEAD, dashed=True)
        keys = VGroup(
            label(r"backward error $\eta$", font_size=20, color=YES),
            label(r"forward error", font_size=20, color=NO),
            label(r"bound $\kappa\,\eta$", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        keys.move_to([0, 1.6, 0]).align_to([2.0, 0, 0], LEFT)
        r4, r12 = rows[0], rows[-1]
        notes = VGroup(
            wrapped_label(rf"$\eta$ stays between ${sci(min(r['backward'] for r in rows))}$ and "
                          rf"${sci(max(r['backward'] for r in rows))}$: \ as stable as rounding allows", 4.6,
                          font_size=18, color=YES),
            wrapped_label(rf"forward error: \ ${sci(r4['forward'])}$ at $n = 4$, \ ${r12['forward']:.3f}$ at "
                          rf"$n = 12$", 4.6, font_size=18, color=NO),
            wrapped_label(r"$x$ known, \ $b = Hx$, \ solved by LAPACK's pivoted elimination \ (computed)", 4.6,
                          font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(keys, DOWN, buff=0.45).align_to(keys, LEFT)
        with self.voiceover(
            "Our instrument tests the rule on Hilbert systems. It picks x, sets b to H times x, and solves with "
            "LAPACK's pivoted elimination, through NumPy. <bookmark mark='a'/> The backward error stays near ten "
            "to the minus seventeen at every size: the algorithm is as stable as rounding allows. "
            "<bookmark mark='b'/> The forward error climbs from two times ten to the minus thirteen at size four "
            "to about five percent at size twelve. <bookmark mark='c'/> And at every size it stays below kappa "
            "times eta, the bound we derived. Nothing went wrong inside the algorithm; the problem amplified the "
            "rounding of its own data."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[2]))
            vo.wait_until("a")
            self.play(Create(back), FadeIn(keys[0]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(fwd), FadeIn(keys[1]), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(bnd), FadeIn(keys[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def digits(self):
        rows = {r["n"]: r for r in load("backward")["rows"]}
        head = label(r"Which digits can we trust?", font_size=36).to_edge(UP, buff=0.3)
        strips = VGroup()
        for n, y in ((4, 1.7), (8, 0.55), (12, -0.6)):
            r = rows[n]
            good = max(0, math.floor(-math.log10(r["forward"])))
            boxes = VGroup(*[Square(side_length=0.4, stroke_width=1, stroke_color=GREY_D,
                                    fill_color=YES if i < good else NO, fill_opacity=0.75) for i in range(16)])
            boxes.arrange(RIGHT, buff=0.06).move_to([0.9, y, 0])
            name = label(rf"$n = {n}$: \ $\kappa \approx {sci(r['kappa'])}$", font_size=20, color=WHITE)
            name.next_to(boxes, LEFT, buff=0.35)
            tail = label(rf"{good} right", font_size=20, color=YES).next_to(boxes, RIGHT, buff=0.3)
            strips.add(VGroup(name, boxes, tail))
        cap = note(r"each box a significant decimal digit of $x$; \ computed from the forward error", font_size=17)
        cap.next_to(strips, DOWN, buff=0.3)
        lines = VGroup(
            wrapped_label(r"digits lost $\approx \log_{10}\kappa$: \ a backward stable algorithm loses only what the "
                          r"problem itself destroys", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"Wilkinson, \ \textit{Rounding Errors in Algebraic Processes} \ (1963); \ the Turing Award, "
                          r"\ 1970", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In digits, the picture is simple. <bookmark mark='a'/> At size four, twelve of the sixteen digits are "
            "right. <bookmark mark='b'/> At size eight, seven. <bookmark mark='c'/> At size twelve, one. "
            "<bookmark mark='d'/> Each time, the digits lost are about the logarithm of kappa: a backward stable "
            "algorithm loses only what the problem itself destroys. <bookmark mark='e'/> This was Wilkinson's "
            "great clarification, set out in his 1963 book, Rounding Errors in Algebraic Processes, and it earned "
            "him the Turing Award in 1970. The next chapter applies it to the most used algorithm of all, Gaussian "
            "elimination."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", strips):
                vo.wait_until(mk)
                self.play(FadeIn(s[0]), LaggedStart(*[FadeIn(b) for b in s[1]], lag_ratio=0.05), FadeIn(s[2]))
            self.play(FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, LAM)
