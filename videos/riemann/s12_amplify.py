from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import MU_COLORS, label, load, mobius_small, note, schematic_tag


def spikes(ax: Axes, us, vals, color, stroke_width=1.2) -> VMobject:
    """Many vertical bars as a single VMobject (fast to draw)."""
    pts = []
    for u, v in zip(us, vals):
        a, b = ax.c2p(u, 0), ax.c2p(u, v)
        pts += [a, b, a]
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


class Amplification(VoiceoverScene):
    def construct(self):
        self.goal()
        self.family()
        self.average()
        self.copies()
        self.budget()
        self.algebra()

    # ------------------------------------------------------------------
    def goal(self):
        a1 = MathTex(r"A_1(D)", r"=", r"\sum_{N(n) \approx D} \mu(n)", font_size=54).move_to(UP * 1.8)
        a1[0].set_color(C.MOBIUS)
        a1[2].set_color(C.MOBIUS)
        twist = note(r"(sum over Eisenstein integers $n$ of norm about $D$; the paper also inserts a twist $\nu(n)$, "
                     r"to handle every $L$-function at once)", font_size=24).next_to(a1, DOWN, buff=0.3)
        cells = VGroup()
        for n in range(1001, 1041):
            m = mobius_small(n)
            cells.add(Square(0.26, stroke_width=1, stroke_color=GREY_C, fill_color=MU_COLORS[m], fill_opacity=0.85))
        cells.arrange(RIGHT, buff=0.04).next_to(twist, DOWN, buff=0.5)
        cl = note(r"about $D$ terms, each $+1$, $-1$ or $0$", font_size=26).next_to(cells, DOWN, buff=0.2)
        bounds = VGroup(
            MathTex(r"\text{trivially:}\quad |A_1(D)| \le D", font_size=40),
            MathTex(r"\text{needed:}\quad |A_1(D)| \le D^{\,\theta}\ \text{ for a fixed } \theta < 1", font_size=40, color=C.ZERO_FREE),
        ).arrange(DOWN, buff=0.35).next_to(cl, DOWN, buff=0.6)
        conseq = note(r"$\Rightarrow$ no zeros with $\Real(s) > \theta$ \ (the M\"obius argument)", font_size=28).next_to(bounds, DOWN, buff=0.3)

        with self.voiceover(
            "Here's the plan. By the Möbius argument, it's enough to show that one sum cancels: <bookmark mark='a'/> the sum of mu "
            "of n, over Eisenstein integers n whose norm is about D. Call it A one of D. <bookmark mark='t'/> There are about D "
            "terms, each plus one, minus one, or zero, <bookmark mark='b'/> so trivially, it's at most D in size. "
            "<bookmark mark='n'/> We need it to be at most D to some fixed power less than one."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(a1), FadeIn(twist))
            vo.wait_until("t")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(bounds[0]))
            vo.wait_until("n")
            self.play(FadeIn(bounds[1]), FadeIn(conseq))
        self.wait(0.5)
        self.clear_scene(a1)
        self.a1 = a1

    # ------------------------------------------------------------------
    def family(self):
        fam = MathTex(r"A_u(D)", r"=", r"\sum_{N(n) \approx D} \mu(n)", r"\Big(\frac{u}{n}\Big)_{\!6}", font_size=52).move_to(UP * 2.2)
        fam[0].set_color(C.MOBIUS)
        fam[2].set_color(C.MOBIUS)
        fam[3].set_color(C.CHARACTER)
        tw = label(r"twist by the sixth-power symbol of $u$", font_size=28, color=C.CHARACTER).next_to(fam, DOWN, buff=0.35)
        tw.align_to(fam[3], RIGHT)
        cards = VGroup()
        for tex in [r"A_1", r"A_2", r"A_\omega", r"A_{1+\omega}", r"A_{3}", r"A_{2\omega}", r"A_{4+\omega}", r"\cdots"]:
            box = RoundedRectangle(width=1.25, height=0.85, corner_radius=0.1, color=GREY_B, stroke_width=1.5)
            cards.add(VGroup(box, MathTex(tex, font_size=34).move_to(box)))
        cards.arrange(RIGHT, buff=0.2).move_to(DOWN * 0.6)
        cards[0][0].set_color(C.MOBIUS).set_stroke(width=3)
        cards[0][1].set_color(C.MOBIUS)
        brace = Brace(cards, DOWN, buff=0.2)
        bl = label(r"a family: one sum for every $u$ with $N(u) \le H$", font_size=30).next_to(brace, DOWN, buff=0.15)
        ours = label(r"ours: $u = 1$", font_size=28, color=C.MOBIUS).next_to(cards[0], UP, buff=0.25)

        with self.voiceover(
            "Proving that a single sum cancels is hard. So instead of studying it alone, <bookmark mark='e'/> embed it in a whole "
            "family. <bookmark mark='t'/> For each Eisenstein integer u, twist the sum by the sixth-power symbol, u over n. "
            "<bookmark mark='f'/> That gives a family of sums, A u of D, one for each u up to some size H. <bookmark mark='o'/> "
            "Our sum is the member with u equal to one, since the symbol of one is always one."
        ) as vo:
            vo.wait_until("e")
            self.play(ReplacementTransform(self.a1, fam[:3]))
            vo.wait_until("t")
            self.play(Write(fam[3]), FadeIn(tw))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.1), GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("o")
            self.play(FadeIn(ours), Indicate(cards[0], color=C.MOBIUS))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def average(self):
        t = load("toy_family")
        us, A = t["u"], t["A"]
        H = int(t["H"][0])
        rms = float(np.sqrt(np.mean(A**2)))
        ax = Axes(x_range=[0, H, 500], y_range=[-90, 90, 30], x_length=11.6, y_length=3.5, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"include_numbers": False}, y_axis_config={"include_numbers": True}).move_to(DOWN * 1.05)
        bars = spikes(ax, us, np.clip(A, -90, 90), GREY_C, stroke_width=0.8)
        xnums = VGroup(*[MathTex(f"{v:,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, -90), DOWN, buff=0.1)
                         for v in range(500, H + 1, 500)])
        band = VGroup(*[DashedLine(ax.c2p(0, s * rms), ax.c2p(H, s * rms), color=YELLOW, stroke_width=2) for s in (1, -1)])
        band_l = label(r"typical size $\approx \sqrt{D}$", font_size=26, color=YELLOW).next_to(ax.c2p(H, rms), UR, buff=0.05).shift(LEFT * 1.6 + UP * 0.25)
        band_l.add_background_rectangle(opacity=0.8, buff=0.04)
        ul = MathTex("u", font_size=28).next_to(ax.c2p(H, -90), RIGHT, buff=0.15)
        toy = note(r"toy version, computed: $D = 4000$, quadratic symbols $(\tfrac{u}{n})$ over ordinary integers, $u \le 3000$",
                   font_size=22).next_to(ax, DOWN, buff=0.4)
        ms = MathTex(r"\sum_{N(u) \le H} \big|A_u(D)\big|^2", r"\;\lesssim\;", r"D \cdot H", font_size=50).to_edge(UP, buff=0.55)
        ms[0].set_color(C.MOBIUS)
        ms_l = label(r"the crucial estimate (Proposition in the 11/12 paper, with $H$ a bit larger than $D$)", font_size=26,
                     color=GREY_A).next_to(ms, DOWN, buff=0.2)
        meaning = label(r"$H$ members, total $\approx D H$ $\Rightarrow$ a typical member has size $\sqrt{D}$:\ "
                        r"\textbf{square-root cancellation, on average}", font_size=28).next_to(ms_l, DOWN, buff=0.25)

        with self.voiceover(
            "The crucial estimate in the paper says that this family is small on average. <bookmark mark='s'/> Add up the "
            "squares of all the members, and you get at most about D times H. <bookmark mark='m'/> With about H members, that "
            "means a typical member has size only about the square root of D: <bookmark mark='c'/> perfect cancellation, on "
            "average, just like coin flips."
        ) as vo:
            self.play(Write(ms), FadeIn(ms_l))
            vo.wait_until("s")
            self.play(Create(ax), FadeIn(ul), FadeIn(toy), FadeIn(xnums))
            self.play(Create(bars), run_time=2.5, rate_func=linear)
            vo.wait_until("m")
            self.play(FadeIn(meaning))
            vo.wait_until("c")
            self.play(Create(band), FadeIn(band_l))
        self.ax, self.bars, self.band, self.band_l, self.toy, self.ul = ax, bars, band, band_l, toy, ul
        self.ms = VGroup(ms, ms_l, meaning)
        self.A = A

    # ------------------------------------------------------------------
    def copies(self):
        ax, A = self.ax, self.A
        t = load("toy_family")
        copies = [int(c) for c in t["copies"]]
        a1_bar = Line(ax.c2p(1, 0), ax.c2p(1, A[0]), color=C.MOBIUS, stroke_width=6)
        cbars = VGroup(*[Line(ax.c2p(c, 0), ax.c2p(c, A[c - 1]), color=C.MOBIUS, stroke_width=5) for c in copies])
        cdots = VGroup(*[Dot(ax.c2p(c, A[c - 1]), radius=0.07, color=C.MOBIUS) for c in copies])
        a1_dot = Dot(ax.c2p(1, A[0]), radius=0.09, color=YELLOW)
        level = DashedLine(ax.c2p(0, A[0]), ax.c2p(t["H"][0], A[0]), color=C.MOBIUS, stroke_width=2.5)
        a1_l = MathTex(r"A_1", font_size=30, color=YELLOW).next_to(a1_dot, UL, buff=0.05)
        spread = max(abs(A[c - 1] - A[0]) for c in copies)
        stat = label(rf"every copy is within {spread:.1f} of $A_1 = {A[0]:.1f}$; \ a typical member is $\pm{np.sqrt(np.mean(A**2)):.0f}$",
                     font_size=26, color=C.MOBIUS).next_to(ax, UP, buff=0.12)
        key = VGroup(
            MathTex(r"\Big(\frac{p^6}{n}\Big)_{\!6} = \Big(\frac{p}{n}\Big)_{\!6}^{6} = 1", r"\quad\text{unless } p \mid n",
                    font_size=40),
            MathTex(r"\Rightarrow\quad A_{p^6}(D) \;\approx\; A_1(D)", font_size=44, color=C.MOBIUS),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        key[0][0].set_color(C.CHARACTER)
        toy2 = note(r"in the toy version the copies sit at $u = p^2$ (squares of primes), and all hover near $A_1$",
                    font_size=24, color=C.MOBIUS).next_to(key, DOWN, buff=0.25)
        vals = [A[c - 1] for c in copies]
        assert all(abs(v - A[0]) < 5 for v in vals) and float(np.sqrt(np.mean(A**2))) > 4 * max(abs(v - A[0]) for v in vals)

        with self.voiceover(
            "But averages can hide outliers. One member could still be large, and it might be ours. <bookmark mark='k'/> Now use "
            "the fact from before: the symbol of a sixth power is one. <bookmark mark='p'/> So when u is p to the sixth, for an "
            "Eisenstein prime p, the twist does nothing at all, except on the few n that are divisible by p. "
            "<bookmark mark='a'/> Our sum doesn't appear in the family just once. It appears over and over again."
        ) as vo:
            self.play(FadeOut(self.ms))
            vo.wait_until("k")
            self.play(FadeIn(key[0]))
            vo.wait_until("p")
            self.play(FadeIn(key[1]))
            vo.wait_until("a")
            self.play(self.bars.animate.set_stroke(opacity=0.3), FadeOut(self.band), FadeOut(self.band_l), Create(a1_bar),
                      FadeIn(a1_dot, scale=2), FadeIn(a1_l))
            self.play(LaggedStart(*[Create(b) for b in cbars], lag_ratio=0.12), FadeIn(cdots), FadeIn(toy2), run_time=2)
        with self.voiceover(
            "You can see it in the toy version: <bookmark mark='l'/> every highlighted bar lands at the same height as the "
            "first one. In effect, each is a copy of it."
        ) as vo:
            vo.wait_until("l")
            self.play(Create(level), FadeIn(stat), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budget(self):
        count = VGroup(
            MathTex(r"\#\{\,p : N(p^6) \le H\,\}", r"\;\approx\;", r"H^{1/6}", font_size=44),
            MathTex(r"H^{1/6} \cdot |A_1(D)|^2", r"\;\lesssim\;", r"\sum_{N(u)\le H} |A_u(D)|^2", r"\;\lesssim\;", r"D\, H",
                    font_size=44),
        ).arrange(DOWN, buff=0.5).to_edge(UP, buff=0.6)
        count[0][2].set_color(YELLOW)
        count[1][0].set_color(C.MOBIUS)
        brace = Brace(count[1][0], DOWN, buff=0.15, color=C.MOBIUS)
        bl = label(r"the copies alone", font_size=26, color=C.MOBIUS).next_to(brace, DOWN, buff=0.08)
        brace2 = Brace(count[1][4], DOWN, buff=0.15)
        bl2 = label(r"the whole budget", font_size=26).next_to(brace2, DOWN, buff=0.08)

        with self.voiceover(
            "Now count. <bookmark mark='c'/> Sixth powers of primes up to size H: there are roughly H to the one sixth of them. "
            "<bookmark mark='e'/> Each copy contributes about A one squared to the total, <bookmark mark='b'/> and the total is "
            "at most D times H."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(count[0]))
            vo.wait_until("e")
            self.play(Write(count[1][:3]), GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("b")
            self.play(Write(count[1][3:]), GrowFromCenter(brace2), FadeIn(bl2))

        # Schematic "energy budget": the copies' share grows like |A_1|^2.
        a = ValueTracker(0.35)
        x0, y0, W = -5.0, -2.3, 9.0
        frame = Rectangle(width=W, height=0.7, color=WHITE, stroke_width=2.5).move_to([x0 + W / 2, y0, 0])
        fl = label(r"total budget $D H$", font_size=26).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        fill = always_redraw(lambda: Rectangle(width=max(0.01, W * a.get_value() ** 2), height=0.6, stroke_width=0,
                                               fill_color=C.MOBIUS if a.get_value() <= 1.0 else C.DANGER, fill_opacity=0.8)
                             .move_to([x0 + W * a.get_value() ** 2 / 2, y0, 0]))
        readout = VGroup(MathTex(r"|A_1| =", font_size=32), DecimalNumber(0.35, num_decimal_places=2, font_size=32),
                         MathTex(r"\cdot D^{11/12}", font_size=32)).arrange(RIGHT, buff=0.12)
        readout.next_to(frame, DOWN, buff=0.3).align_to(frame, LEFT)
        readout.set_color(C.MOBIUS)

        def upd(m):
            m[1].set_value(a.get_value())
            m.set_color(C.MOBIUS if a.get_value() <= 1.0 else C.DANGER)

        readout.add_updater(upd)
        over = label(r"impossible: the copies would exceed the budget", font_size=28, color=C.DANGER).next_to(frame, DOWN, buff=0.3)
        over.align_to(frame, RIGHT)
        tag = schematic_tag(DR)
        with self.voiceover(
            "So here's the squeeze. If our sum were large, <bookmark mark='g'/> its copies alone would eat up more and more of the "
            "budget, <bookmark mark='o'/> and past a certain size, they wouldn't fit. That size is D to the eleven twelfths."
        ) as vo:
            self.play(Create(frame), FadeIn(fl), FadeIn(fill), FadeIn(readout), FadeIn(tag))
            vo.wait_until("g")
            self.play(a.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("o")
            self.play(a.animate.set_value(1.12), run_time=1.0)
            self.play(FadeIn(over))
            self.play(a.animate.set_value(1.0), FadeOut(over), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        lines = VGroup(
            MathTex(r"H^{1/6}\,|A_1(D)|^2", r"\;\lesssim\;", r"D\,H", font_size=46),
            MathTex(r"|A_1(D)|^2", r"\;\lesssim\;", r"D\,H^{5/6}", font_size=46),
            MathTex(r"|A_1(D)|^2", r"\;\lesssim\;", r"D^{1 + 5/6} = D^{11/6}", r"\qquad (H \approx D)", font_size=46),
            MathTex(r"|A_1(D)|", r"\;\lesssim\;", r"D^{11/12}", font_size=56),
        ).arrange(DOWN, buff=0.45).move_to(LEFT * 1.6 + UP * 0.6)
        for l in lines:
            l[0].set_color(C.MOBIUS)
        lines[3][2].set_color(C.ZERO_FREE)
        lines[2][3].set_color(GREY_B)
        why = VGroup(
            label(r"divide by $H^{1/6}$", font_size=26, color=GREY_A),
            label(r"take $H$ about $D$", font_size=26, color=GREY_A),
            label(r"square root", font_size=26, color=GREY_A),
        )
        for i, w in enumerate(why):
            w.next_to(VGroup(lines[i], lines[i + 1]), RIGHT, buff=0.5).set_y((lines[i].get_y() + lines[i + 1].get_y()) / 2)
            w.set_x(4.6)
        box = SurroundingRectangle(lines[3], color=C.ZERO_FREE, buff=0.2, corner_radius=0.1)
        concl = VGroup(
            label(r"a power saving $\Rightarrow$ no zeros with $\Real(s) > \tfrac{11}{12}$", font_size=34, color=C.ZERO_FREE),
            MathTex(r"\tfrac{11}{12} = 1 - \tfrac12\cdot\tfrac16 \qquad\text{(the 6 is from the sixth powers)}", font_size=34),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        fine = note(r"(the paper takes $H = D^{1+\vartheta}$ with $\vartheta$ small, and tracks factors $D^{\varepsilon}$)",
                    font_size=22).to_corner(UR, buff=0.3)

        with self.voiceover(
            "Now just divide. <bookmark mark='a'/> A one squared is at most D times H to the five sixths. "
            "<bookmark mark='b'/> Take H about the same size as D, and A one squared is at most D to the eleven sixths. "
            "<bookmark mark='c'/> So A one is at most D to the eleven twelfths."
        ) as vo:
            self.play(FadeIn(lines[0]), FadeIn(fine))
            vo.wait_until("a")
            self.play(FadeIn(why[0]), TransformFromCopy(lines[0], lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(why[1]), TransformFromCopy(lines[1], lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(why[2]), TransformFromCopy(lines[2], lines[3]), Create(box))
        with self.voiceover(
            "That's a power saving! <bookmark mark='z'/> And by the Möbius argument, it means there are no zeros to the right of "
            "eleven twelfths. <bookmark mark='s'/> The exponent comes straight from the sixth powers: one, minus half of one "
            "sixth. <bookmark mark='r'/> Everything now rests on the crucial estimate. Why should the whole family be small on "
            "average?"
        ) as vo:
            vo.wait_until("z")
            self.play(FadeIn(concl[0]))
            vo.wait_until("s")
            self.play(FadeIn(concl[1]))
            vo.wait_until("r")
            self.play(Indicate(lines[0][2], color=YELLOW))
        self.wait(0.8)
        self.clear_scene()
