from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def basin_image(which, steps, width):
    """Newton's basins for z^3 - 1 as a picture: the colour of the root reached, darker when it took more steps,
    black where it never converged.  Row 0 of the arrays is the bottom of the window, so the rows are flipped."""
    cols = np.array([ManimColor(c).to_rgb() for c in (DATA, HEAD, LAM)])
    w = np.asarray(which)
    rgb = np.zeros(w.shape + (3,))
    for r in range(3):
        rgb[w == r] = cols[r]
    rgb *= (1 - 0.7 * np.clip(np.asarray(steps, float) / 20, 0, 1))[..., None]
    rgba = np.concatenate([rgb, np.ones(w.shape + (1,))], -1)
    img = ImageMobject((np.flipud(rgba) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.stretch_to_fit_width(width)
    return img.stretch_to_fit_height(width)


def window(img, meta, c, w, color=WHITE):
    """The square of the complex plane centred at c, w wide, drawn on a picture of the window ``meta``."""
    C, W = meta["center"], meta["width"]
    p = img.get_center() + np.array([(c[0] - C[0]) / W * img.width, (c[1] - C[1]) / W * img.height, 0])
    return Square(side_length=w / W * img.width, color=color, stroke_width=2.5).move_to(p)


class Roots(VoiceoverScene):
    def construct(self):
        self.card()
        self.bisection()
        self.newton()
        self.race()
        self.fractal()

    def card(self):
        card = chapter_card(10, r"Roots and Newton's fractal", r"How fast can we find where a function is zero?",
                            lit=(1690, 1879), extra=((1690, r"Raphson: \ Newton's method as we write it"),
                                                     (1879, r"Cayley: \ Newton's method on complex numbers")),
                            part=PART)
        with self.voiceover("Chapter ten. Roots, and Newton's fractal."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graph(self, x0=0.9, x1=2.1, center=(-3.4, 0.2)):
        ax = Axes(x_range=[x0, x1, 0.5], y_range=[-1.5, 2.5, 1], x_length=5.8, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([*center, 0])
        f = ax.plot(lambda x: x * x - 2, x_range=[x0, x1, 0.01], color=DATA, stroke_width=3)
        fl = MathTex(r"f(x) = x^2 - 2", font_size=26, color=DATA).next_to(ax.c2p(x0, 2.3), RIGHT, buff=0.1)
        ticks = VGroup()
        for v in (1.0, 1.5, 2.0):
            ticks.add(Line(ax.c2p(v, -0.06), ax.c2p(v, 0.06), color=GREY_C),
                      label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
        return ax, f, fl, ticks

    def bisection(self):
        r = load("roots")
        bis = r["bisection"]
        head = label(r"Bisection: \ one bit per step", font_size=36).to_edge(UP, buff=0.3)
        ax, f, fl, ticks = self.graph()
        star = Dot(ax.c2p(math.sqrt(2), 0), radius=0.07, color=YES)
        sl = MathTex(r"\sqrt2", font_size=24, color=YES).next_to(star, UP, buff=0.15).shift(LEFT * 0.15)
        a, b = 1.0, 2.0
        brackets = []
        for _ in range(6):
            brackets.append((a, b))
            m = (a + b) / 2
            if (a * a - 2) * (m * m - 2) <= 0:
                b = m
            else:
                a = m

        def bar(lo, hi):
            return VGroup(Line(ax.c2p(lo, -0.9), ax.c2p(hi, -0.9), color=HEAD, stroke_width=7),
                          Dot(ax.c2p(lo, lo * lo - 2), radius=0.07, color=NO),
                          Dot(ax.c2p(hi, hi * hi - 2), radius=0.07, color=YES))
        bars = [bar(lo, hi) for lo, hi in brackets]
        bl = label(r"the bracket", font_size=17, color=HEAD).next_to(ax.c2p(1.0, -0.9), DOWN, buff=0.2)
        bl.align_to(ax.c2p(1.0, 0), LEFT)
        rows = VGroup(
            cmath(r"f(a)\, f(b)", r"<", r"0", font_size=34),
            cmath(r"|x_k - x_*|", r"\le", r"\frac{b - a}{2^{k+1}}", font_size=34),
            cmath(r"\text{digits}", r"\approx", r"(k+1)\log_{10} 2", r"\approx", r"0.3\,(k+1)", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([3.4, 0.6, 0])
        whys = VGroup(
            label(r"a sign change: \ a root lies between", font_size=18, color=GREY_B),
            label(r"keep the half that still changes sign", font_size=18, color=GREY_B),
            label(r"one bit per step", font_size=18, color=GREY_B),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.12).align_to(rr, LEFT)
        res = label(rf"after 40 steps: \ {bis[-1]:.1f} correct digits \ (computed)", font_size=20,
                    color=HEAD).next_to(whys[2], DOWN, buff=0.45).align_to(rows, LEFT)
        with self.voiceover(
            "Every method in this chapter hunts for a zero, and our test case is the square root of two, the "
            "positive root of x squared minus two. <bookmark mark='a'/> Bisection needs only a sign change. f is "
            "negative at one and positive at two, so a root lies between them. <bookmark mark='b'/> Evaluate the "
            "midpoint, keep the half that still changes sign, and repeat. The bracket halves every time, "
            "<bookmark mark='c'/> so each step gains one bit, about three tenths of a decimal digit. Bisection "
            "cannot fail, and it is slow: after forty steps, twelve digits."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(f), FadeIn(fl), FadeIn(star), FadeIn(sl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]), FadeIn(bars[0]), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            cur = bars[0]
            for nb in bars[1:]:
                self.play(Transform(cur, nb), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def newton(self):
        head = label(r"Newton: \ follow the tangent", font_size=36).to_edge(UP, buff=0.3)
        ax, f, fl, ticks = self.graph(x0=0.8, x1=2.2)
        xs = [2.0]
        for _ in range(2):
            x = xs[-1]
            xs.append(x - (x * x - 2) / (2 * x))
        tans, drops, dots, names = VGroup(), VGroup(), VGroup(), VGroup()
        for k in range(2):
            x, xn = xs[k], xs[k + 1]
            tans.add(Line(ax.c2p(x, x * x - 2), ax.c2p(xn - 0.08, -0.08 * 2 * x), color=HEAD, stroke_width=2.5))
            drops.add(DashedLine(ax.c2p(xn, 0), ax.c2p(xn, xn * xn - 2), color=GREY_B, stroke_width=1.5))
        for k, x in enumerate(xs):
            dots.add(Dot(ax.c2p(x, x * x - 2), radius=0.07, color=HEAD))
            names.add(MathTex(rf"x_{k} = {x:.5g}", font_size=22, color=HEAD))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax.c2p(1.5, -0.4), DOWN, buff=0.25)
        names.align_to(ax.c2p(1.2, 0), LEFT)
        cols = {r"e_k^2": HEAD}
        rows = VGroup(
            cmath(r"f(x_k + h)", r"\approx", r"f(x_k)", r"+", r"f'(x_k)\, h", font_size=32),
            cmath(r"h", r"=", r"-\frac{f(x_k)}{f'(x_k)}", font_size=32),
            cmath(r"x_{k+1}", r"=", r"x_k", r"-\frac{f(x_k)}{f'(x_k)}", font_size=32),
            cmath(r"e_{k+1}", r"\approx", r"\frac{f''(x_*)}{2 f'(x_*)}", r"\,", r"e_k^2", colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([3.4, 0.5, 0])
        whys = VGroup(
            label(r"the tangent line at $x_k$", font_size=18, color=GREY_B),
            label(r"set it to zero", font_size=18, color=GREY_B),
            label(r"Newton's step", font_size=18, color=GREY_B),
            wrapped_label(r"one more Taylor term: \ the error is squared, \ so the correct digits double", 5.4,
                          font_size=18, color=HEAD),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        sec = wrapped_label(r"\textbf{secant}: \ the slope through the last two points instead of $f'$; \ order "
                            r"$\tfrac{1 + \sqrt5}{2} \approx 1.618$", 5.6, font_size=18, color=LAM).next_to(
            whys[3], DOWN, buff=0.3).align_to(rows, LEFT)
        with self.voiceover(
            "Newton's method uses the slope as well. <bookmark mark='a'/> Near x, f of x plus h is about f of x "
            "plus f prime of x times h: the tangent line. <bookmark mark='b'/> Set that to zero, solve for h, "
            "<bookmark mark='c'/> and step. From two, the tangent lands at one and a half, and the next at one point "
            "four one six seven. <bookmark mark='d'/> Keep one more term of Taylor's series, and the new error is "
            "a constant times the old error squared. An error of a thousandth becomes about a millionth: the "
            "correct digits double at every step. <bookmark mark='e'/> The secant method replaces the derivative "
            "by the slope through the last two points. Its order is the golden ratio, one point six one eight."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(f), FadeIn(fl), FadeIn(dots[0]),
                      FadeIn(names[0]))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            for k in range(2):
                self.play(Create(tans[k]), run_time=0.8)
                self.play(Create(drops[k]), FadeIn(dots[k + 1]), FadeIn(names[k + 1]), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(sec))
        self.wait(0.4)
        self.clear_scene()

    def race(self):
        r = load("roots")
        head = label(r"The race, \ computed", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 20, 5], y_range=[0, 16, 4], x_length=6.2, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.9, 0.3, 0])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, 5, 10, 15, 20)])
        yt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 4, 8, 12, 16)])
        xl = label(r"iteration", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"correct digits of $\sqrt2$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        lim = DashedLine(ax.c2p(0, 16), ax.c2p(20, 16), color=GREY_D, stroke_width=1.5)
        liml = label(r"double precision", font_size=16, color=GREY_B).next_to(ax.c2p(20, 16), DOWN, buff=0.1)
        liml.align_to(ax.c2p(20, 0), RIGHT)

        def series(ys, color, upto):
            pts = [ax.c2p(i + 1, v) for i, v in enumerate(ys[:upto])]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.05, color=color) for p in pts])
        s_b = series(r["bisection"], NO, 20)
        s_s = series(r["secant"], LAM, 6)
        s_n = series(r["newton"], YES, 5)
        tags = VGroup(label(r"bisection", font_size=18, color=NO).next_to(ax.c2p(20, r["bisection"][19]), UP,
                                                                         buff=0.15),
                      label(r"secant", font_size=18, color=LAM).next_to(ax.c2p(6, r["secant"][5]), RIGHT, buff=0.15)
                      .shift(DOWN * 0.45),
                      label(r"Newton", font_size=18, color=YES).next_to(ax.c2p(4, r["newton"][3]), LEFT,
                                                                        buff=0.15))
        rows = VGroup(
            label(r"Newton: \ " + r", \ ".join(f"{v:.1f}" for v in r["newton"][:5]), font_size=20, color=YES),
            label(r"secant: \ " + r", \ ".join(f"{v:.1f}" for v in r["secant"][:6]), font_size=20, color=LAM),
            label(rf"bisection, \ 20 steps: \ {r['bisection'][19]:.1f}", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows.move_to([4.0, 1.3, 0])
        rt = label(r"digits after each step", font_size=18, color=GREY_A).next_to(rows, UP, buff=0.2).align_to(
            rows, LEFT)
        cols = {r"1.618": LAM, r"1.414": YES}
        eff = VGroup(
            cmath(r"\text{secant: }", r"1.618", r"\text{ per evaluation}", colors=cols, font_size=28),
            cmath(r"\text{Newton: }", r"\sqrt2", r"=", r"1.414", r"\text{ per evaluation}", colors=cols,
                  font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ew = wrapped_label(r"Newton needs $f$ and $f'$ each step: \ two evaluations, \ so per evaluation its order "
                           r"is $2^{1/2}$", 5.0, font_size=18, color=GREY_B)
        right = VGroup(ew, eff).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rows, DOWN, buff=0.6)
        right.align_to(rows, LEFT)
        with self.voiceover(
            "Here is the race, computed. <bookmark mark='a'/> Bisection climbs its straight line, three tenths of "
            "a digit per step. <bookmark mark='b'/> The secant method's correct digits go one, two, three, six, "
            "nine and a half, then nearly sixteen, the limit of double precision. <bookmark mark='c'/> Newton's go one, "
            "two and a half, five and a half, twelve, sixteen: doubling. <bookmark mark='d'/> But each Newton "
            "step evaluates both f and its derivative. Counted per evaluation, Newton's order is the square root "
            "of two, and the secant method, at one point six one eight, is the faster of the two."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(lim),
                      FadeIn(liml), FadeIn(rt))
            vo.wait_until("a")
            self.play(Create(s_b), FadeIn(tags[0]), FadeIn(rows[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(s_s), FadeIn(tags[1]), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(s_n), FadeIn(tags[2]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(right))
        self.wait(0.4)
        self.clear_scene()

    def fractal(self):
        fr = load("fractal")
        m0, m1, m2 = fr["full_meta"], fr["zoom1_meta"], fr["zoom2_meta"]
        head = label(r"Newton's fractal", font_size=36).to_edge(UP, buff=0.3)
        full = basin_image(fr["full_which"], fr["full_steps"], 5.7).move_to([-3.2, -0.3, 0])
        frame = SurroundingRectangle(full, color=GREY_D, buff=0, stroke_width=1.5)
        roots = [(1.0, 0.0), (-0.5, math.sqrt(3) / 2), (-0.5, -math.sqrt(3) / 2)]
        rdots = VGroup(*[Circle(radius=0.1, color=WHITE, stroke_width=3).move_to(
            full.get_center() + np.array([x / m0["width"] * full.width, y / m0["width"] * full.height, 0]))
            for x, y in roots])
        rows = VGroup(
            cmath(r"z", r"\leftarrow", r"z", r"-", r"\frac{z^3 - 1}{3z^2}", font_size=34),
            cmath(r"z", r"\leftarrow", r"\frac{2z^3 + 1}{3z^2}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.0, 2.0, 0])
        rows.align_to([0.35, 0, 0], LEFT)
        key = VGroup()
        for c, t in ((DATA, r"$1$"), (HEAD, r"$e^{2\pi i/3}$"), (LAM, r"$e^{-2\pi i/3}$")):
            key.add(VGroup(Square(0.26, stroke_width=0, fill_color=c, fill_opacity=1),
                           label(t, font_size=20, color=c)).arrange(RIGHT, buff=0.15))
        key.arrange(RIGHT, buff=0.4)
        kt = label(r"colour: \ the root reached \ (darker: \ more steps)", font_size=18, color=GREY_A)
        keyg = VGroup(kt, key).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rows, DOWN, buff=0.45)
        keyg.align_to(rows, LEFT)
        facts = VGroup(
            wrapped_label(r"each basin is calm near its root, \ but the boundary is no line: \ where two colours "
                          r"meet, \ the third appears between them, \ at every scale", 5.4, font_size=19,
                          color=WHITE),
            label(rf"$360 \times 360$ starts, \ 40 steps: \ {100 * m0['unconverged']:.3f}\% never settle",
                  font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(keyg, DOWN, buff=0.45).align_to(rows, LEFT)
        with self.voiceover(
            "Newton's method works for complex numbers too, and in 1879 Arthur Cayley asked which root it finds "
            "from a given start. For z squared minus one the answer is simple: the nearer root. "
            "<bookmark mark='a'/> For z cubed minus one, colour every starting point by the root it reaches, "
            "darker where it takes longer. <bookmark mark='b'/> Each root sits in a calm basin of its own colour. "
            "<bookmark mark='c'/> But the boundary between basins is not a line. Wherever two colours meet, the "
            "third appears between them, in smaller and smaller copies."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(full), FadeIn(frame), FadeIn(keyg), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(d) for d in rdots], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(facts))

        # zoom: shrink the full picture to the left, then open two windows
        W = 3.7
        y = 0.35
        self.play(FadeOut(rows), FadeOut(keyg), FadeOut(facts), FadeOut(rdots), FadeOut(frame))
        self.play(full.animate.scale_to_fit_width(W).move_to([-4.6, y, 0]))
        z1 = basin_image(fr["zoom1_which"], fr["zoom1_steps"], W).move_to([0, y, 0])
        z2 = basin_image(fr["zoom2_which"], fr["zoom2_steps"], W).move_to([4.6, y, 0])
        r1 = window(full, m0, m1["center"], m1["width"])
        r2 = window(z1, m1, m2["center"], m2["width"])
        f1 = SurroundingRectangle(z1, color=WHITE, buff=0, stroke_width=2)
        f2 = SurroundingRectangle(z2, color=WHITE, buff=0, stroke_width=2)
        c1 = VGroup(DashedLine(r1.get_corner(UR), f1.get_corner(UL), color=GREY_B, stroke_width=1.5),
                    DashedLine(r1.get_corner(DR), f1.get_corner(DL), color=GREY_B, stroke_width=1.5))
        c2 = VGroup(DashedLine(r2.get_corner(UR), f2.get_corner(UL), color=GREY_B, stroke_width=1.5),
                    DashedLine(r2.get_corner(DR), f2.get_corner(DL), color=GREY_B, stroke_width=1.5))
        caps = VGroup(
            label(rf"width {m0['width']:g}", font_size=18, color=GREY_A),
            label(rf"width {m1['width']:g}: \ {m0['width'] / m1['width']:.0f}$\times$, \ on the boundary",
                  font_size=18, color=GREY_A),
            label(rf"width {m2['width']:g}: \ {m0['width'] / m2['width']:.0f}$\times$, \ inside a basin",
                  font_size=18, color=GREY_A),
        )
        for cp, im in zip(caps, (full, z1, z2)):
            cp.next_to(im, DOWN, buff=0.2)
        steps2 = int(np.asarray(fr["zoom2_steps"]).max())
        flat = label(rf"every start here: \ the same root, \ in {steps2} steps", font_size=18, color=HEAD).next_to(
            caps[2], DOWN, buff=0.12)
        foot = wrapped_label(r"so library root finders are \textbf{safeguarded}: \ Brent's method \ (1973) \ keeps a "
                             r"bisection bracket and takes secant-like steps only while they stay inside it",
                             12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        z1.save_state()
        z1.replace(r1)
        z2.save_state()
        z2.replace(r2)
        with self.voiceover(
            "Zoom in. <bookmark mark='a'/> A window fifteen times smaller, on the boundary: the same structure, "
            "buds on buds. In the exact picture it never ends, because every point on the boundary of one basin "
            "is on the boundary of all three. <bookmark mark='b'/> Zoom twenty times further, but into the "
            "interior of a basin, and the picture goes flat: every start there reaches the same root in six "
            "steps. <bookmark mark='c'/> Fast near a root, unpredictable far from one: that is why the root "
            "finders in libraries are safeguarded. Brent's method, from 1973, keeps a bisection bracket and takes "
            "fast interpolation steps only while they stay inside it."
        ) as vo:
            self.play(FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(Create(r1))
            self.play(Restore(z1), Create(f1), Create(c1), run_time=1.5)
            self.play(FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(Create(r2))
            self.play(Restore(z2), Create(f2), Create(c2), run_time=1.5)
            self.play(FadeIn(caps[2]), FadeIn(flat))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
