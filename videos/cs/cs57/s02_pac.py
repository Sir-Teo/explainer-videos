from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def unit_square(side: float, center):
    """A frame for the unit square and a map from its coordinates to the scene's."""
    frame = Square(side_length=side, stroke_color=GREY_C, stroke_width=1.5).move_to(center)
    o = frame.get_corner(DL)

    def at(x, y):
        return o + np.array([x * side, y * side, 0])
    return frame, at


def box_poly(at, x0, x1, y0, y1, **kw):
    return Polygon(at(x0, y0), at(x1, y0), at(x1, y1), at(x0, y1), **kw)


def log_axes(xr, yr, x_length, y_length, xticks, yticks, fx, fy, font=16):
    """Axes whose coordinates are log10 of the data; tick labels written as the data values."""
    ax = CornerAxes(x_range=[*xr, 1], y_range=[*yr, 1], x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    xt = VGroup(*[label(fx(v), font_size=font, color=GREY_B).next_to(ax.c2p(math.log10(v), yr[0]), DOWN, buff=0.1)
                  for v in xticks])
    yt = VGroup(*[label(fy(v), font_size=font, color=GREY_B).next_to(ax.c2p(xr[0], math.log10(v)), LEFT, buff=0.1)
                  for v in yticks])
    return VGroup(ax, xt, yt), ax


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Pac(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.finite()
        self.agnostic()
        self.rectangles()
        self.curves()
        self.bridge()

    def card(self):
        card = chapter_card(1, r"Probably approximately correct", r"How many examples are enough?",
                            lit=(1984, 2010), extra=((1984, r"Valiant: \ \textit{A Theory of the Learnable}"),
                                                     (2010, r"Valiant's Turing Award")), part=PART)
        with self.voiceover("Chapter one. Probably approximately correct."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def game(self):
        c = load("compress")
        m = 12
        P, L = c["points"][:m], c["labels"][:m]
        tx0, tx1, ty0, ty1 = c["target"]
        head = label(r"The learning game", font_size=36).to_edge(UP, buff=0.3)
        frame, at = unit_square(4.6, [-4.0, -0.35, 0])
        dl = label(r"inputs $x \sim D$", font_size=18, color=GREY_A).next_to(frame, UP, buff=0.12)
        pos = [p for p, y in zip(P, L) if y]
        bx = (min(p[0] for p in pos), max(p[0] for p in pos), min(p[1] for p in pos), max(p[1] for p in pos))
        err = box_poly(at, tx0, tx1, ty0, ty1, stroke_width=0, fill_color=NO, fill_opacity=0.45)
        tgt = DashedVMobject(box_poly(at, tx0, tx1, ty0, ty1, color=YES, stroke_width=2.5), num_dashes=40)
        hyp = box_poly(at, *bx, color=HEAD, stroke_width=3, fill_color=BG, fill_opacity=1)
        dots = VGroup(*[Dot(at(*p), radius=0.06, color=YES if y else GREY_B) for p, y in zip(P, L)])
        legend = VGroup(
            label(r"target $c$ \ (hidden)", font_size=17, color=YES),
            label(r"hypothesis $h$", font_size=17, color=HEAD),
            label(r"error region", font_size=17, color=NO),
        ).arrange(RIGHT, buff=0.35).next_to(frame, DOWN, buff=0.18)
        src = note(rf"{m} uniform points from our instrument's sample; \ target "
                   rf"$[{tx0:g}, {tx1:g}] \times [{ty0:g}, {ty1:g}]$", font_size=16).next_to(legend, DOWN, buff=0.12)
        W = 6.2
        side = VGroup(
            wrapped_label(r"nature fixes an unknown distribution $D$ on inputs, \ and an unknown target $c$ from a "
                          r"class $\mathcal H$ the learner knows", W, font_size=19, color=WHITE),
            wrapped_label(r"the learner sees $m$ examples $\big(x, c(x)\big)$, \ $x \sim D$, \ and returns a "
                          r"hypothesis $h_S$", W, font_size=19, color=WHITE),
            MathTex(r"L_D(h) = \Pr_{x \sim D}\big[h(x) \ne c(x)\big]", font_size=32, color=NO),
            MathTex(r"\Pr_{S \sim D^m}\big[\,L_D(h_S) \le \epsilon\,\big] \ \ge\ 1 - \delta", font_size=34,
                    color=HEAD),
            wrapped_label(r"for \textit{every} $D$ and every $c \in \mathcal H$, \ with $m$ and running time "
                          r"polynomial in $1/\epsilon$ and $1/\delta$: \ \textbf{probably} \ ($1-\delta$) \ "
                          r"\textbf{approximately} \ ($\epsilon$) \ \textbf{correct}", W, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([3.45, -0.2, 0])
        with self.voiceover(
            "In 1984 Leslie Valiant asked what it should mean for a machine to learn from examples. "
            "<bookmark mark='a'/> Nature fixes a distribution over inputs, which the learner never sees, "
            "and a target from a class the learner knows: here, a hidden rectangle. <bookmark mark='b'/> "
            "The learner receives m examples, each drawn from the distribution with its label, and returns "
            "a hypothesis: here, the tightest box around the positive points. <bookmark mark='c'/> Its "
            "error is the probability of the region where hypothesis and target disagree, shaded red. "
            "<bookmark mark='d'/> Valiant asked that, with probability at least one minus delta over the "
            "sample, the error be at most epsilon, <bookmark mark='e'/> for every distribution and every "
            "target, using examples and computation polynomial in one over epsilon and one over delta. "
            "Probably, approximately, correct."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(dl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.12), FadeIn(side[1]),
                      run_time=2.5)
            self.play(Create(hyp))
            self.bring_to_front(dots)
            vo.wait_until("c")
            self.add(err)
            self.bring_to_front(hyp, dots)
            self.play(FadeIn(err), Create(tgt), FadeIn(legend), FadeIn(src), Write(side[2]))
            vo.wait_until("d")
            self.play(Write(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def finite(self):
        f = load("finite")
        H, eps, delta, m = f["H"], f["eps"], f["delta"], f["m"]
        head = label(r"A finite class: \ the union bound", font_size=36).to_edge(UP, buff=0.3)
        fs = 27
        P1 = r"\Pr\big[\text{a bad } h \text{ fits all } m\big]"
        P2 = r"\Pr\big[\text{some bad } h \text{ fits all } m\big]"
        rows = [
            MathTex(P1, r"\le", r"(1-\epsilon)^m", r"\le", r"e^{-\epsilon m}", font_size=fs),
            MathTex(P2, r"\le", r"|\mathcal H|", r"e^{-\epsilon m}", font_size=fs),
            MathTex(r"|\mathcal H|", r"e^{-\epsilon m}", r"\le", r"\delta", font_size=fs),
            MathTex(r"m", r"\ge", r"\frac{1}{\epsilon}\Big(\ln|\mathcal H| + \ln\frac{1}{\delta}\Big)", font_size=fs),
            MathTex(r"m", r"\ge", rf"\frac{{1}}{{{eps:g}}}\Big(\ln {H} + \ln {round(1 / delta)}\Big)", r"=",
                    rf"{m}", font_size=fs),
        ]
        rows[3][2].set_color(YES)
        rows[4][4].set_color(YES)
        whys = [
            label(r"each example exposes a bad $h$ \ (error $> \epsilon$) \ with probability $> \epsilon$; \ "
                  r"$1 - x \le e^{-x}$", font_size=17, color=GREY_B),
            label(r"the union bound \ (Part 2): \ at most $|\mathcal H|$ bad hypotheses", font_size=17, color=GREY_B),
            label(r"ask for failure probability at most $\delta$", font_size=17, color=GREY_B),
            label(r"take logarithms and solve for $m$", font_size=17, color=GREY_B),
            label(rf"$|\mathcal H| = {H}$, \ $\epsilon = \delta = {eps:g}$", font_size=17, color=YES),
        ]
        col = stacked(rows, whys, buff=0.24).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.45)
        # the failure probability |H| e^{-eps m} against m, on a log scale
        g, ax = log_axes((0, 300), (-2, 3), 5.2, 4.2, [], [0.01, 1, 100], lambda v: "", lambda v: f"{v:g}")
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -2), DOWN, buff=0.1)
                      for v in (0, 100, 200, 300)])
        g.add(xt)
        g.move_to([3.85, -0.15, 0])
        xl = label(r"examples $m$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yl = label(rf"$|\mathcal H|\,e^{{-\epsilon m}}$ \ for $|\mathcal H| = {H}$, \ $\epsilon = {eps:g}$",
                   font_size=17, color=NO).next_to(ax, UP, buff=0.15)
        m_end = (math.log10(H) + 2) * math.log(10) / eps
        curve = Line(ax.c2p(0, math.log10(H)), ax.c2p(m_end, -2), color=NO, stroke_width=3)
        dl = DashedLine(ax.c2p(0, math.log10(delta)), ax.c2p(300, math.log10(delta)), color=HEAD, stroke_width=2)
        dlab = label(rf"$\delta = {delta:g}$", font_size=17, color=HEAD).next_to(ax.c2p(20, math.log10(delta)), UP,
                                                                               buff=0.08, aligned_edge=LEFT)
        vm = DashedLine(ax.c2p(m, -2), ax.c2p(m, math.log10(delta)), color=YES, stroke_width=2)
        mlab = label(rf"$m = {m}$", font_size=18, color=YES).next_to(ax.c2p(m, -1.75), LEFT, buff=0.12)
        with self.voiceover(
            "Start with a finite class that contains a perfect hypothesis, the realizable case, and call a "
            "hypothesis bad if its error exceeds epsilon. <bookmark mark='a'/> A fixed bad hypothesis "
            "survives each random example with probability less than one minus epsilon, so it survives all "
            "m of them with probability at most e to the minus epsilon m. <bookmark mark='b'/> By the union"
            " bound of Part 2, the chance that any bad hypothesis survives is at most the class size times "
            "that. <bookmark mark='c'/> Ask for this to be at most delta, <bookmark mark='d'/> and solve: m"
            " at least one over epsilon, times the log of the class size plus the log of one over delta. "
            "<bookmark mark='e'/> For a thousand hypotheses, with epsilon and delta both five hundredths, a"
            " hundred and ninety-nine examples suffice, whichever consistent hypothesis is returned. The "
            "class size enters only through its logarithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(xl))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            self.play(Create(curve), FadeIn(yl))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]), Create(dl), FadeIn(dlab))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(col[3][1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(col[4][1]), Create(vm), FadeIn(mlab))
        self.wait(0.4)
        self.clear_scene()

    def agnostic(self):
        f = load("finite")
        H, eps, delta, m_real = f["H"], f["eps"], f["delta"], f["m"]
        m_agn = math.ceil(math.log(2 * H / delta) / (2 * eps ** 2))
        head = label(r"Agnostic learning: \ no hypothesis is perfect", font_size=36).to_edge(UP, buff=0.3)
        # illustrative: sixteen hypotheses' true errors, and sample errors that tighten as m grows
        rng = np.random.default_rng(57)
        N = 16
        true = 0.22 + 0.22 * rng.random(N)
        true[11] = 0.17
        z = rng.standard_normal(N)
        ax = Axes(x_range=[0, N + 1, 1], y_range=[0, 0.6, 0.1], x_length=5.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
        ax.move_to([-3.75, 0.05, 0])
        yt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.2, 0.4, 0.6)])
        xl = label(r"sixteen hypotheses", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        tdots = VGroup(*[Dot(ax.c2p(i + 1, t), radius=0.07, color=WHITE) for i, t in enumerate(true)])

        def sample(m):
            s = true + z * np.sqrt(true * (1 - true) / m)
            return VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.06, color=DATA) for i, v in enumerate(s)]), s

        def ties(dots):
            return VGroup(*[Line(tdots[i].get_center(), dots[i].get_center(), color=DATA, stroke_width=1.5,
                                 stroke_opacity=0.6) for i in range(N)])
        s50, v50 = sample(40)
        s800, v800 = sample(800)
        mlab = label(r"$m = 40$", font_size=19, color=DATA).next_to(ax, UP, buff=0.12)
        mlab2 = label(r"$m = 800$", font_size=19, color=DATA).move_to(mlab)
        legend = VGroup(VGroup(Dot(radius=0.07, color=WHITE), label(r"true error $L_D(h)$", font_size=17)).arrange(
            RIGHT, buff=0.1), VGroup(Dot(radius=0.06, color=DATA), label(r"sample error $L_S(h)$", font_size=17,
                                                                        color=DATA)).arrange(RIGHT, buff=0.1)
        ).arrange(RIGHT, buff=0.4).next_to(xl, DOWN, buff=0.15)
        ill = note(r"illustrative", font_size=16).next_to(legend, DOWN, buff=0.1)
        best = int(np.argmin(true))
        erm = int(np.argmin(v800))
        ring = Circle(radius=0.17, color=YES, stroke_width=3).move_to(tdots[best])
        ringl = label(r"$h^*$", font_size=18, color=YES).next_to(ring, DOWN, buff=0.05)
        fs = 25
        rows = [
            MathTex(r"\Pr\big[\,|L_S(h) - L_D(h)| > \epsilon\,\big]", r"\le", r"2e^{-2m\epsilon^2}", font_size=fs),
            MathTex(r"\Pr\big[\,\exists h:\ |L_S(h) - L_D(h)| > \epsilon\,\big]", r"\le", r"2|\mathcal H|",
                    r"e^{-2m\epsilon^2}", font_size=fs),
            MathTex(r"m", r"\ge", r"\frac{\ln(2|\mathcal H|/\delta)}{2\epsilon^2}", font_size=fs + 2),
            MathTex(r"L_D(\hat h) \le L_S(\hat h) + \epsilon \le L_S(h^*) + \epsilon \le L_D(h^*) + 2\epsilon",
                    font_size=fs),
        ]
        rows[2][2].set_color(YES)
        whys = [
            label(r"Hoeffding \ (Part 20): \ $L_S(h)$ averages $m$ independent coin flips", font_size=17,
                  color=GREY_B),
            label(r"union bound over the class", font_size=17, color=GREY_B),
            label(r"ask for at most $\delta$, \ solve for $m$", font_size=17, color=GREY_B),
            label(r"so the sample's best, \ $\hat h$, \ is within $2\epsilon$ of the class's best, \ $h^*$",
                  font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.26).move_to([3.35, 0.35, 0])
        if col.get_right()[0] > 6.85:
            col.shift(LEFT * (col.get_right()[0] - 6.85))
        cmp_ = wrapped_label(rf"$|\mathcal H| = {H}$, \ $\epsilon = \delta = {eps:g}$: \ realizable, \ {m_real} "
                             rf"examples; \ every sample error within $\epsilon$, \ {m_agn:,} \ --- \ "
                             r"$1/\epsilon$ has become $1/\epsilon^2$", 6.4, font_size=19, color=HEAD)
        cmp_.next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Usually no hypothesis is perfect. The agnostic model asks only that the learner come within "
            "epsilon of the best one in the class, and the natural learner minimizes its error on the "
            "sample. <bookmark mark='a'/> For a fixed hypothesis, the sample error averages m independent "
            "coin flips, and Hoeffding's inequality from Part 20 says it strays more than epsilon from the "
            "truth with probability at most two e to the minus two m epsilon squared. <bookmark mark='b'/> "
            "A union bound covers the whole class, <bookmark mark='c'/> and solving gives m of order the "
            "log of the class size over epsilon squared. <bookmark mark='d'/> Then the best hypothesis on "
            "the sample is within two epsilon of the best of all. <bookmark mark='e'/> Noise costs a "
            "square: for the same thousand hypotheses, two thousand one hundred and twenty examples, more "
            "than ten times as many."
        ) as vo:
            t50 = ties(s50)
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xl), FadeIn(legend), FadeIn(ill),
                      FadeIn(tdots))
            vo.wait_until("a")
            self.play(FadeIn(s50), Create(t50), FadeIn(mlab), Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            vo.wait_until("c")
            t800 = ties(s800)
            self.play(Transform(s50, s800), Transform(t50, t800), Transform(mlab, mlab2),
                      TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]), run_time=2)
            vo.wait_until("d")
            self.play(Write(rows[3]), FadeIn(col[3][1]), Create(ring), FadeIn(ringl),
                      Indicate(s50[erm], color=YES, scale_factor=1.8))
            vo.wait_until("e")
            self.play(FadeIn(cmp_))
        self.wait(0.4)
        self.clear_scene()

    def rectangles(self):
        c = load("compress")
        tx0, tx1, ty0, ty1 = c["target"]
        head = label(r"Rectangles: \ infinitely many, \ still learnable", font_size=36).to_edge(UP, buff=0.3)
        frame, at = unit_square(4.6, [-4.0, -0.25, 0])
        tgt = box_poly(at, tx0, tx1, ty0, ty1, color=YES, stroke_width=2.5)
        s = 0.06                                      # strip thickness, for the picture
        strips = VGroup(
            box_poly(at, tx0, tx1, ty1 - s, ty1, stroke_width=0, fill_color=KERN, fill_opacity=0.3),
            box_poly(at, tx0, tx1, ty0, ty0 + s, stroke_width=0, fill_color=KERN, fill_opacity=0.3),
            box_poly(at, tx0, tx0 + s, ty0, ty1, stroke_width=0, fill_color=KERN, fill_opacity=0.3),
            box_poly(at, tx1 - s, tx1, ty0, ty1, stroke_width=0, fill_color=KERN, fill_opacity=0.3),
        )
        slabs = VGroup(
            label(r"$\epsilon/4$", font_size=17, color=KERN).next_to(strips[0], UP, buff=0.06),
            label(r"$\epsilon/4$", font_size=17, color=KERN).next_to(strips[1], DOWN, buff=0.06),
            label(r"$\epsilon/4$", font_size=17, color=KERN).next_to(strips[2], LEFT, buff=0.06),
            label(r"$\epsilon/4$", font_size=17, color=KERN).next_to(strips[3], RIGHT, buff=0.06),
        )
        # a box that reaches into every strip
        pts = [(0.45, ty1 - 0.03), (0.33, ty0 + 0.025), (tx0 + 0.03, 0.5), (tx1 - 0.035, 0.6), (0.5, 0.5),
               (0.4, 0.62)]
        dots = VGroup(*[Dot(at(*p), radius=0.06, color=YES) for p in pts])
        hx0, hx1 = min(p[0] for p in pts), max(p[0] for p in pts)
        hy0, hy1 = min(p[1] for p in pts), max(p[1] for p in pts)
        hyp = box_poly(at, hx0, hx1, hy0, hy1, color=HEAD, stroke_width=4)
        ill = note(r"strip widths illustrative", font_size=16).next_to(frame, DOWN, buff=0.15)
        fs = 27
        rows = [
            MathTex(r"\Pr\big[\text{a strip is empty}\big]", r"=", r"\big(1 - \tfrac{\epsilon}{4}\big)^m",
                    font_size=fs),
            MathTex(r"\Pr\big[\text{some strip is empty}\big]", r"\le", r"4", r"\big(1 - \tfrac{\epsilon}{4}"
                    r"\big)^m", r"\le", r"4", r"e^{-\epsilon m/4}", font_size=fs),
            MathTex(r"4", r"e^{-\epsilon m/4}", r"\le", r"\delta", font_size=fs),
            MathTex(r"m", r"\ge", r"\frac{4}{\epsilon}\ln\frac{4}{\delta}", font_size=fs + 4),
        ]
        rows[3][2].set_color(YES)
        whys = [
            label(r"each strip has probability $\epsilon/4$ under $D$", font_size=17, color=GREY_B),
            label(r"union bound over four strips; \ $1 - x \le e^{-x}$", font_size=17, color=GREY_B),
            label(r"ask for at most $\delta$", font_size=17, color=GREY_B),
            label(r"the tightest box is then $\epsilon$-good with probability $\ge 1 - \delta$", font_size=17,
                  color=YES),
        ]
        key = wrapped_label(r"the learner returns the tightest box around the positive examples; \ it sits inside "
                            r"the target, \ and if an example lands in each strip, \ the error region lies inside "
                            r"the strips: \ error $\le \epsilon$", 6.3, font_size=19, color=WHITE)
        col = stacked(rows, whys, buff=0.24)
        if col.width > 6.2:
            col.scale_to_fit_width(6.2)
        right = VGroup(key, col).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.3, -0.2, 0])
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        with self.voiceover(
            "Most interesting classes are infinite, rectangles for instance, and yet rectangles can be "
            "learned, by the argument that opens Kearns and Vazirani's textbook. <bookmark mark='a'/> The "
            "learner returns the tightest box around the positive examples, which sits inside the target. "
            "Draw four strips along the target's sides, each of probability epsilon over four. If an "
            "example lands in every strip, the box misses only parts of the strips, so its error is at most"
            " epsilon. <bookmark mark='b'/> One strip is missed by all m examples with probability one "
            "minus epsilon over four, to the m. <bookmark mark='c'/> A union bound over the four strips, "
            "<bookmark mark='d'/> set below delta, <bookmark mark='e'/> gives four over epsilon times the "
            "log of four over delta examples, with no class size anywhere."
        ) as vo:
            self.play(FadeIn(head), Create(frame), Create(tgt))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.2), FadeIn(key))
            self.play(Create(hyp))
            self.play(FadeIn(strips), FadeIn(slabs), FadeIn(ill))
            self.bring_to_front(hyp, dots)
            vo.wait_until("b")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(col[3][1]))
        self.wait(0.4)
        self.clear_scene()

    def curves(self):
        r = load("rect")
        rows = r["rows"]
        head = label(r"The bound against measurement", font_size=36).to_edge(UP, buff=0.3)
        g, ax = log_axes((1, 3.4), (-3, 0.5), 8.0, 4.6, [10, 100, 1000], [0.001, 0.01, 0.1, 1],
                         lambda v: f"{v:,}", lambda v: f"{v:g}")
        g.next_to(head, DOWN, buff=0.4).shift(LEFT * 1.6)
        xl = label(r"examples $m$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yl = label(r"error of the tightest box", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(
            ax, LEFT)

        def line(key, color, dashed=False):
            pts = [ax.c2p(math.log10(q["m"]), max(-3, min(0.5, math.log10(q[key])))) for q in rows]
            v = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
            return DashedVMobject(v, num_dashes=40) if dashed else v

        def dots(key, color):
            return VGroup(*[Dot(ax.c2p(math.log10(q["m"]), math.log10(q[key])), radius=0.05, color=color)
                            for q in rows if math.log10(q[key]) <= 0.5])
        mean, p95, bnd = line("mean", DATA), line("p95", HEAD), line("rect_bound", NO, dashed=True)
        md, pd = dots("mean", DATA), dots("p95", HEAD)
        names = VGroup(
            label(r"mean error", font_size=18, color=DATA),
            label(r"95th percentile \ ($\delta = 0.05$)", font_size=18, color=HEAD),
            label(r"bound $\frac{4}{m}\ln\frac{4}{\delta}$", font_size=18, color=NO),
        )
        last = rows[-1]
        for n, k in zip(names, ("mean", "p95", "rect_bound")):
            n.next_to(ax.c2p(math.log10(last["m"]), math.log10(last[k])), RIGHT, buff=0.15)
        names[0].shift(DOWN * 0.1)
        ratios = [q["rect_bound"] / q["p95"] for q in rows if q["m"] >= 100]
        side = wrapped_label(rf"from $m = 100$ on, \ the bound is {min(ratios):.1f} to {max(ratios):.1f} times the "
                             r"95th percentile: \ loose by a constant, \ and it holds for \textit{every} $D$, \ not "
                             r"just this uniform one", 3.6, font_size=19, color=WHITE).move_to([5.0, -1.9, 0])
        src = note(rf"{len(rows)} sample sizes, \ 200 trials each, \ uniform points, \ target "
                   rf"$[0.2, 0.7] \times [0.3, 0.75]$", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "How loose is that? Our instrument learned this rectangle two hundred times at each of eight "
            "sample sizes. <bookmark mark='a'/> The mean error falls like one over m. <bookmark mark='b'/> "
            "The ninety-fifth percentile is the error beaten with probability one minus delta, which is "
            "what the theorem bounds. <bookmark mark='c'/> The bound lies above it everywhere; from a "
            "hundred examples on, by a factor of two to three. That constant is the price of a guarantee "
            "for every distribution, not just the uniform one we sampled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(md), FadeIn(names[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(p95), FadeIn(pd), FadeIn(names[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(bnd), FadeIn(names[2]), FadeIn(side), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def bridge(self):
        gr = load("growth")["rows"]
        r10 = next(q for q in gr if q["m"] == 10)       # counted labelling by labelling (larger m: formula)
        head = label(r"What replaces $\ln|\mathcal H|$?", font_size=36).to_edge(UP, buff=0.3)
        f0 = MathTex(r"m \ge \frac{1}{\epsilon}\Big(", r"\ln|\mathcal H|", r"+ \ln\frac{1}{\delta}\Big)",
                     font_size=40)
        f1 = MathTex(r"m \ge \frac{1}{\epsilon}\Big(", r"\ln \Pi_{\mathcal H}(\,\cdot\,)", r"+ \ln\frac{1}{\delta}"
                     r"\Big)", font_size=40)
        f0[1].set_color(NO)
        f1[1].set_color(YES)
        f0.next_to(head, DOWN, buff=0.45)
        f1.move_to(f0)
        inf = label(r"half-planes, \ rectangles: \ $|\mathcal H| = \infty$", font_size=20, color=NO).next_to(
            f0, DOWN, buff=0.2)
        W = 11.0
        full = Rectangle(width=W, height=0.55, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
        real = Rectangle(width=W * r10["realized"] / r10["all"], height=0.55, stroke_width=0, fill_color=YES,
                         fill_opacity=0.9)
        VGroup(full, real).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0.3, -1.0, 0])
        fl = label(rf"all labellings of {r10['m']} points: \ $2^{{{r10['m']}}} = {format(r10['all'], ',').replace(',', '{,}')}$", font_size=20,
                   color=GREY_A).next_to(full, UP, buff=0.12).align_to(full, LEFT)
        rl = label(rf"those half-planes can produce: \ {r10['realized']}", font_size=20, color=YES).next_to(
            real, RIGHT, buff=0.2)
        foot = wrapped_label(r"what matters is the number of \textit{behaviours} on the sample, \ the growth function "
                             r"$\Pi_{\mathcal H}(m)$; \ Chapter 2 shows one number, \ the VC dimension, \ controls it",
                             12.4, font_size=21, color=HEAD).to_edge(DOWN, buff=0.4)
        src = note(r"counted by our instrument, \ each labelling checked by a linear program", font_size=16).next_to(
            real, DOWN, buff=0.2).align_to(full, LEFT)
        with self.voiceover(
            "So what replaces the size of the class? <bookmark mark='a'/> For half-planes, as for "
            "rectangles, it is infinite. But a learner only meets what the class does on its sample. "
            "<bookmark mark='b'/> Ten points can be labelled in a thousand and twenty-four ways. "
            "<bookmark mark='c'/> Half-planes produce only ninety-two of them; our instrument checked every"
            " labelling with a linear program. <bookmark mark='d'/> That count of behaviours, the growth "
            "function, can take the place of the class size, and Chapter two shows that one number, the VC "
            "dimension, controls it."
        ) as vo:
            self.play(FadeIn(head), Write(f0))
            vo.wait_until("a")
            self.play(FadeIn(inf))
            vo.wait_until("b")
            self.play(GrowFromEdge(full, LEFT), FadeIn(fl))
            vo.wait_until("c")
            self.play(GrowFromEdge(real, LEFT), FadeIn(rl), FadeIn(src))
            vo.wait_until("d")
            self.play(TransformMatchingTex(f0, f1), FadeOut(inf), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, BG)
