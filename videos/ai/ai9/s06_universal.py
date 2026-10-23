from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import HINGE, NEURON, PART, WEIGHT, load, log_axes


class Universal(VoiceoverScene):
    def construct(self):
        self.card()
        self.neuron()
        self.hinges()
        self.rate()
        self.bumps()
        self.theorem()

    def card(self):
        card = chapter_card(5, r"One layer can do anything", r"What can a sum of bent lines draw?", part=PART)
        with self.voiceover("Chapter five. What one layer can do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def neuron(self):
        ins = VGroup(*[Circle(radius=0.34, color=GREY_B, stroke_width=3).move_to([-5.6, 2.1 - 1.4 * k, 0]) for k in range(4)])
        il = VGroup(*[MathTex(rf"x_{k + 1}", font_size=34).move_to(ins[k]) for k in range(4)])
        body = Circle(radius=0.72, color=NEURON, stroke_width=4).move_to([-2.4, 0.0, 0])

        def toward(c_):  # an arrow from an input to the edge of the body, aimed at its centre
            d_ = body.get_center() - c_.get_center()
            d_ = d_ / np.linalg.norm(d_)
            return Arrow(c_.get_center() + 0.36 * d_, body.get_center() - 0.76 * d_, buff=0, color=GREY_C, stroke_width=3,
                         max_tip_length_to_length_ratio=0.12)

        arrows = VGroup(*[toward(c_) for c_ in ins])
        wl = VGroup(*[MathTex(rf"w_{k + 1}", font_size=30, color=WEIGHT).move_to(arrows[k].point_from_proportion(0.42) + UP * 0.28)
                      for k in range(4)])
        sig = MathTex(r"\Sigma", font_size=50).move_to(body)
        out = Arrow(body.get_right(), body.get_right() + RIGHT * 1.6, buff=0.05, color=NEURON, stroke_width=5)
        colors = {r"\mathbf{w}\cdot\mathbf{x} + b": WEIGHT}
        f = cmath(r"\text{out}", "=", r"\max\big(0,\;", r"\mathbf{w}\cdot\mathbf{x} + b", r"\big)", colors=colors,
                  font_size=44).move_to([3.7, 2.4, 0])
        fl = label(r"a weighted sum, \ then a bend: \ ReLU", font_size=28, color=GREY_A).next_to(f, DOWN, buff=0.2)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-0.5, 2, 1], x_length=4.6, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.7, -0.9, 0])
        relu = VMobject(color=NEURON, stroke_width=5).set_points_as_corners([ax.c2p(-2, 0), ax.c2p(0, 0), ax.c2p(2, 2)])
        hl = label(r"one unit, \ along one input: \ a hinge", font_size=28, color=NEURON).next_to(ax, DOWN, buff=0.2)
        cite_ = cite(r"ReLU: \ V.~Nair \& G.~Hinton (2010); \ X.~Glorot, A.~Bordes \& Y.~Bengio (2011)", corner=DL)
        with self.voiceover(
            "Backpropagation can train any layer. So what can layers represent? Start with one unit, as modern "
            "networks build it. It takes some numbers, <bookmark mark='a'/> multiplies each by a weight and adds them "
            "up, plus a constant, exactly like Part 6's logistic regression, <bookmark mark='b'/> and then bends the "
            "result: anything below zero becomes zero. That bend, the rectified linear unit or ReLU, replaced the "
            "smooth S-shaped curves around 2010. <bookmark mark='c'/> Along any one input, a unit is a hinge: flat, "
            "then rising."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(il), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(wl), Create(body), FadeIn(sig))
            vo.wait_until("b")
            self.play(GrowArrow(out), Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(ax), Create(relu), FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hinges(self):
        h = load("hinges")
        xs, y = np.asarray(h["xs"]), np.asarray(h["y"])
        ns = [2, 4, 8, 16, 64]
        ax = Axes(x_range=[-3, 3, 1], y_range=[-2.2, 2.2, 1], x_length=8.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.4, -0.6, 0])
        tgt = DashedVMobject(curve(ax, xs, y, WHITE, 3), num_dashes=70)
        tl = label(r"the target \ (illustrative)", font_size=24, color=GREY_A).next_to(ax.c2p(-3, 2.2), DR, buff=0.1)

        def fit(n):
            return curve(ax, xs, np.clip(np.asarray(h[f"fit{n}"]), -2.2, 2.2), HINGE, 5)

        def parts(n):
            P = np.asarray(h[f"parts{n}"])
            return VGroup(*[curve(ax, xs, np.clip(p, -2.2, 2.2), NEURON, 1.6).set_stroke(opacity=0.55) for p in P])

        def knots(n):
            return VGroup(*[Line(ax.c2p(k, -2.2), ax.c2p(k, -2.0), color=HINGE, stroke_width=3)
                            for k in np.asarray(h[f"knots{n}"])])

        nv = Integer(ns[0], font_size=40, color=HINGE)
        nl = VGroup(label(r"hinges:", font_size=32), nv).arrange(RIGHT, buff=0.2).move_to([0, 2.2, 0]).align_to([3.4, 0, 0], LEFT)
        ev = DecimalNumber(h[f"err{ns[0]}"], num_decimal_places=4, font_size=32, color=C.SURPRISE)
        el = VGroup(label(r"typical miss:", font_size=26, color=GREY_A), ev).arrange(RIGHT, buff=0.15).next_to(nl, DOWN, buff=0.3)
        el.align_to(nl, LEFT)
        colors = {r"\max(0,\, x - k_i)": NEURON}
        f = cmath(r"f(x) \approx a + b x +", r"\sum_i", r"c_i", r"\max(0,\, x - k_i)", colors=colors, font_size=34)
        f.to_edge(UP, buff=0.35).shift(LEFT * 1.4)
        how = label(r"positions $k_i$ evenly spaced; \\ slopes $c_i$ by least squares", font_size=24, color=GREY_A)
        how.next_to(el, DOWN, buff=0.5).align_to(nl, LEFT)
        tag = note(r"computed").to_corner(DR, buff=0.2)
        cur_fit, cur_parts, cur_knots = fit(ns[0]), parts(ns[0]), knots(ns[0])
        e64 = float(h["err64"])
        with self.voiceover(
            "Add hinges together, each with its own position and slope, and you can draw a curve. "
            "<bookmark mark='a'/> Two hinges make a crude zigzag. <bookmark mark='b'/> Four. Eight. Sixteen. "
            f"Sixty-four, and the typical miss is down to {e64:.4f}."
        ) as vo:
            self.play(Create(ax), Create(tgt), FadeIn(tl), Write(f), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cur_parts), Create(cur_fit), FadeIn(cur_knots), FadeIn(nl), FadeIn(el), FadeIn(how))
            vo.wait_until("b")
            for n in ns[1:]:
                nf, np_, nk = fit(n), parts(n), knots(n)
                self.play(Transform(cur_fit, nf), FadeOut(cur_parts), FadeIn(np_), Transform(cur_knots, nk),
                          ChangeDecimalToValue(nv, n), ChangeDecimalToValue(ev, h[f"err{n}"]), run_time=1.2)
                cur_parts = np_
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        h = load("hinges")
        ns, errs = np.asarray(h["ns"], float), np.asarray(h["errs"])
        g = log_axes([0, 3], [-5, 0], 6.0, 2.5, center=[-1.6, -2.0, 0], xlabel=r"hinges $n$",
                     ylabel=r"typical miss \ (log scale)", xticks=range(0, 4), yticks=range(-5, 1, 2))
        ax = g.ax
        pts = VGroup(*[Dot(ax.c2p(np.log10(n), np.log10(e)), radius=0.07, color=HINGE) for n, e in zip(ns, errs)])
        a0 = np.log10(errs[3]) + 2 * np.log10(ns[3])
        guide = DashedLine(ax.c2p(0.5, a0 - 1.0), ax.c2p(2.6, a0 - 5.2), color=C.BITS, stroke_width=2.5, dash_length=0.1)
        gl = label(r"slope $-2$", font_size=22, color=C.BITS).next_to(guide.get_end(), UP, buff=0.12).shift(LEFT * 0.3)
        slope = float(h["slope"])
        rows = [cmath(r"|f(x) - \ell(x)|", r"\le", r"\tfrac{h^2}{8}\, \max |f''|", font_size=38),
                cmath(r"h", r"=", r"\tfrac{6}{n+1}", font_size=38),
                cmath(r"\text{miss}", r"\le", r"\tfrac{36}{8}\,\max|f''|\,(n+1)^{-2}", font_size=38)]
        # the chords: the target joined dot to dot at n = 8 evenly spaced hinges (the picture behind the bound)
        xs_, ys_ = np.asarray(h["xs"]), np.asarray(h["y"])
        ax3 = Axes(x_range=[-3, 3, 1], y_range=[-2.2, 2.2, 1], x_length=6.4, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.2, -1.95, 0])
        kn8 = np.linspace(-3, 3, 10)
        fk = np.interp(kn8, xs_, ys_)
        tgt3 = DashedVMobject(curve(ax3, xs_, ys_, WHITE, 2.5), num_dashes=60)
        chord = curve(ax3, xs_, np.interp(xs_, kn8, fk), HINGE, 4)
        kdots = VGroup(*[Dot(ax3.c2p(a_, b_), radius=0.06, color=HINGE) for a_, b_ in zip(kn8, fk)])
        hb = BraceBetweenPoints(ax3.c2p(kn8[4], -2.2), ax3.c2p(kn8[5], -2.2), DOWN, color=GREY_B)
        hlab = MathTex(r"h", font_size=30, color=GREY_A).next_to(hb, DOWN, buff=0.06)
        pic3 = VGroup(ax3, tgt3, chord, kdots, hb, hlab)
        pic3_l = label(r"$n = 8$ hinges: \ the curve joined dot to dot", font_size=24, color=HINGE)
        pic3_l.next_to(ax3, UP, buff=0.05).align_to(ax3, LEFT)
        whys = [why(r"a straight chord over a piece of width $h$"), why(r"$n$ hinges cut $[-3, 3]$ into $n + 1$ pieces"),
                why(r"double the hinges, \ quarter the miss")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.6, buff=0.42, edge=6.9)
        ls = label(r"least squares does at least as well \\ as joining the dots at the hinges", font_size=22,
                   color=GREY_A).move_to([4.6, -1.0, 0])
        measured = label(rf"measured slope: \ ${slope:.2f}$", font_size=28, color=HINGE).move_to([4.6, -2.2, 0])
        with self.voiceover(
            "How fast does the miss shrink? <bookmark mark='p'/> Joining the dots at the hinges gives straight chords, and over a piece of "
            "width h a chord misses a smooth curve by at most h squared over eight, times the curve's bending. "
            "<bookmark mark='a'/> With n hinges spread over the interval, h is six over n plus one. "
            "<bookmark mark='b'/> So the miss falls like one over n squared: double the hinges, and it quarters. "
            "Least squares can only do better than joining the dots. <bookmark mark='c'/> On log-log axes that's a "
            f"line of slope minus two, and the measured slope is {slope:.2f}."
        ) as vo:
            self.play(Create(ax3), Create(tgt3))
            vo.wait_until("p")
            self.play(Create(chord), FadeIn(kdots), FadeIn(pic3_l))
            step(0)
            self.play(GrowFromCenter(hb), FadeIn(hlab))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(ls))
            vo.wait_until("c")
            self.play(FadeOut(pic3), FadeOut(pic3_l))
            self.play(FadeIn(g), LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.15), run_time=1.6)
            self.play(Create(guide), FadeIn(gl), FadeIn(measured))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bumps(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.6, 2.0, 1], x_length=6.0, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, 1.2, 0])
        a_, b_, c_ = -0.6, 0.0, 0.6
        hw = b_ - a_
        x = np.linspace(-3, 3, 241)
        r = lambda t: np.maximum(t, 0)  # noqa: E731
        h1, h2, h3 = r(x - a_) / hw, -2 * r(x - b_) / hw, r(x - c_) / hw
        cols = (NEURON, C.MODEL_Q, NEURON)
        hs = [curve(ax, x, np.clip(hh, -1.6, 2.0), cc, 3) for hh, cc in zip((h1, h2, h3), cols)]
        bump = curve(ax, x, h1 + h2 + h3, C.BITS, 5)
        tex = cmath(r"\max(0, x - a) - 2\max(0, x - b) + \max(0, x - c)", font_size=28).next_to(ax, UP, buff=0.15)
        bl = label(r"three hinges: \ a bump", font_size=24, color=C.BITS).next_to(ax, DOWN, buff=0.15)
        # bumps at evenly spaced points, each as tall as the curve there, add up to the curve joined dot to dot
        hd = load("hinges")
        xs, yy = np.asarray(hd["xs"]), np.asarray(hd["y"])
        ax2 = Axes(x_range=[-3, 3, 1], y_range=[-2.2, 2.2, 1], x_length=6.0, y_length=3.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, -1.2, 0])
        t = np.linspace(-3, 3, 9)
        step_ = t[1] - t[0]
        fv = np.interp(t, xs, yy)
        hats = [np.maximum(0, 1 - np.abs(xs - ti) / step_) * fi for ti, fi in zip(t, fv)]
        hat_m = VGroup(*[curve(ax2, xs, hh, NEURON, 2.2).set_stroke(opacity=0.8) for hh in hats])
        tot = curve(ax2, xs, np.sum(hats, 0), HINGE, 5)
        tgt = DashedVMobject(curve(ax2, xs, yy, WHITE, 2.5), num_dashes=60)
        sl = label(r"one bump per point, \ as tall as the curve there: \\ together, \ the curve joined dot to dot",
                   font_size=22, color=GREY_A).next_to(ax2, UP, buff=0.15)
        two = label(r"in more dimensions: \ bumps built \\ from more units each", font_size=22, color=GREY_A)
        two.move_to([-3.4, -2.2, 0])
        with self.voiceover(
            "Here's another way to see it. <bookmark mark='a'/> Take three hinges: one up, one down twice as steeply, "
            "and one up again. <bookmark mark='b'/> Their sum is a bump: zero, up, down, and zero again. "
            "<bookmark mark='c'/> Put a bump at each of a row of points, each as tall as the curve is there, and add "
            "them up: you get the curve, joined dot to dot. <bookmark mark='d'/> Any continuous curve can be drawn "
            "this way, as finely as you like. In more dimensions the bumps take more units each, but the idea "
            "survives."
        ) as vo:
            self.play(Create(ax), Write(tex))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in hs], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(ReplacementTransform(VGroup(*hs), bump), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(tgt), FadeIn(sl))
            self.play(LaggedStart(*[Create(m) for m in hat_m], lag_ratio=0.15), run_time=2.0)
            self.play(ReplacementTransform(hat_m.copy(), tot), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(two))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        th = theorem_card(r"Universal approximation",
                          r"for any continuous $f$ on a closed, bounded set and any $\epsilon > 0$, \ some network with "
                          r"one hidden layer of finitely many units is within $\epsilon$ of $f$ everywhere: \ for any "
                          r"continuous activation that is not a polynomial",
                          who=r"G.~Cybenko (1989); \ K.~Hornik, M.~Stinchcombe \& H.~White (1989); \ M.~Leshno, V.~Lin, "
                              r"A.~Pinkus \& S.~Schocken (1993)", width=10.6, font_size=27, color=HINGE).move_to(UP * 1.3)
        nots = VGroup(label(r"how many units? \ \ (it doesn't say)", font_size=28, color=C.SURPRISE),
                      label(r"will training find them? \ \ (it doesn't say)", font_size=28, color=C.SURPRISE),
                      label(r"will it generalize? \ \ (Part 8)", font_size=28, color=C.SURPRISE))
        nots.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.9)
        with self.voiceover(
            "That's the universal approximation theorem, proved in 1989 by George Cybenko for S-shaped units, and by "
            "Kurt Hornik, Maxwell Stinchcombe and Halbert White in general. In 1993 Moshe Leshno and colleagues "
            "pinned it down: any continuous activation works, as long as it is not a polynomial. <bookmark mark='a'/> It says a "
            "network can represent the answer. <bookmark mark='b'/> It doesn't say how many units that takes, "
            "<bookmark mark='c'/> or whether training will find them, <bookmark mark='d'/> or whether what's learned "
            "from examples holds up on new ones, the subject of Part 8. The first question has a surprising answer."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(th.body, color=HINGE, scale_factor=1.02))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(nots[k], shift=RIGHT * 0.15))
        self.wait(0.3)
        self.clear_scene()
