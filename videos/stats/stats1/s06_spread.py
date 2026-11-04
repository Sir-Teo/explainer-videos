from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Spread(VoiceoverScene):
    def construct(self):
        self.card()
        self.squares()
        self.pythagoras()
        self.robust()
        self.chebyshev()

    def card(self):
        card = chapter_card(5, r"Spread, and why squares", r"How far from the centre is typical?", lit=(), part=PART)
        with self.voiceover("Chapter five. Spread, and why squares."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def squares(self):
        d = load("heights")
        x = np.round(np.asarray(d["x"][:7]), 1)
        m = float(x.mean())
        dev = x - m
        L = axes([155, 190], [0, 1], x_length=11.0, y_length=0.4, xlabel=r"height (cm)",
                 xticks=[155, 160, 165, 170, 175, 180, 185, 190], center=[0, 0.9, 0])
        L.ax.y_axis.set_opacity(0)
        ax = L.ax
        ys = [1.35 + 0.29 * i for i in range(len(x))]
        dots = VGroup(*[Dot([ax.c2p(v, 0)[0], y, 0], radius=0.08, color=S.DATA) for v, y in zip(x, ys)])
        mline = Line([ax.c2p(m, 0)[0], 1.1, 0], [ax.c2p(m, 0)[0], ys[-1] + 0.3, 0], color=MEAN, stroke_width=4)
        mlab = MathTex(rf"\bar x = {m:.1f}", font_size=30, color=MEAN).next_to(mline, UP, buff=0.08)
        sticks = VGroup(*[Line([ax.c2p(m, 0)[0], y, 0], [ax.c2p(v, 0)[0], y, 0], color=DEV, stroke_width=4)
                          for v, y in zip(x, ys)])
        devs = VGroup(*[MathTex(f"{v:+.1f}", font_size=20, color=DEV).next_to(st, UP, buff=0.02)
                        for v, st in zip(dev, sticks)])
        u = 0.12  # screen units per cm, for the squares
        sq = VGroup(*[Square(side_length=abs(v) * u, stroke_color=DEV, stroke_width=2, fill_color=DEV,
                             fill_opacity=0.35) for v in dev])
        sq.arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([-2.2, -2.0, 0])
        sq_lab = VGroup(*[MathTex(f"{v * v:.0f}", font_size=20, color=GREY_A).next_to(s_, DOWN, buff=0.08)
                          for v, s_ in zip(dev, sq)])
        var = float(np.mean(dev ** 2))
        avg = Square(side_length=np.sqrt(var) * u, stroke_color=S.ACCENT, stroke_width=3, fill_color=S.ACCENT,
                     fill_opacity=0.35).move_to([4.9, -2.0, 0]).align_to(sq, DOWN)
        side = BraceBetweenPoints(avg.get_corner(DL), avg.get_corner(DR), direction=DOWN, color=S.ACCENT)
        side_l = MathTex(rf"s = {np.sqrt(var):.2f}", font_size=30, color=S.ACCENT).next_to(side, DOWN, buff=0.08)
        alab = MathTex(rf"\text{{average area}} = {var:.1f}", font_size=28, color=S.ACCENT).next_to(avg, UP, buff=0.15)
        formula = cmath(r"s^2", r"=", r"\frac1n \sum_i (x_i - \bar x)^2", font_size=36).move_to([3.7, 0.0, 0])
        n1 = note(r"for a sample, \ dividing by $n - 1$ instead: \ Part 8").next_to(formula, DOWN, buff=0.15)
        n1.align_to(formula, LEFT)
        tag = simulated_tag(r"simulated: seven World adults")
        with self.voiceover(
            "A centre isn't enough. Two towns can have the same average height, one where everyone is close to "
            "it and one where nobody is. We need a number for spread. <bookmark mark='a'/> Here are seven heights "
            f"and their mean, {m:.1f}. Each person's deviation is their distance from the mean, with a sign: "
            "positive above, negative below. <bookmark mark='b'/> The deviations always add up to zero; that's what "
            "made the mean the balance point. So their average tells us nothing. <bookmark mark='c'/> Instead, "
            "square each one. Literally: turn each deviation into a square whose side is the deviation. "
            "<bookmark mark='d'/> The variance is the average area of these squares, "
            f"{var:.1f} square centimetres. <bookmark mark='e'/> Its square root, the side of the average square, "
            f"is the standard deviation: {np.sqrt(var):.2f} centimetres. It's in the data's own units, and it's the "
            "most used measure of spread there is."
        ) as vo:
            self.play(FadeIn(L), LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(mline), FadeIn(mlab))
            self.play(LaggedStart(*[Create(s_) for s_ in sticks], lag_ratio=0.1), FadeIn(devs))
            vo.wait_until("b")
            self.play(Indicate(devs, color=DEV, scale_factor=1.2))
            vo.wait_until("c")
            self.play(*[TransformFromCopy(st, s_) for st, s_ in zip(sticks, sq)], run_time=2.0)
            self.play(FadeIn(sq_lab))
            vo.wait_until("d")
            self.play(Write(formula), FadeIn(n1))
            self.play(TransformFromCopy(sq, avg), FadeIn(alab), run_time=1.6)
            vo.wait_until("e")
            self.play(GrowFromCenter(side), FadeIn(side_l))
        self.clear_scene()

    def pythagoras(self):
        s = load("spread")
        x = np.asarray(s["three"])
        c = 160.0
        v = x - c
        m = float(x.mean())
        proj = np.full(3, m - c)
        res = v - proj
        ns = NSpace(scale=0.72, center=[-3.4, -1.5, 0], angle=-0.7, tilt=0.4, axis_len=6.0,
                    axis_labels=[r"person 1", r"person 2", r"person 3"])
        diag = ns.line([1, 1, 1], extent=7.0, color=GREY_B)
        dlab = ns.point_label(label(r"all equal: \ $c\,\mathbf 1$", font_size=22, color=GREY_B), [4.2, 4.2, 4.2], offset=(-0.9, 0.35))
        vx = ns.vector(v, color=S.DATA)
        vlab = ns.point_label(MathTex(r"\mathbf x - c\mathbf 1", font_size=30, color=S.DATA), v, offset=(0.5, 0.25))
        vp = ns.vector(proj, color=MEAN, stroke_width=6)
        plab = ns.point_label(MathTex(r"(\bar x - c)\mathbf 1", font_size=28, color=MEAN), proj / 2, offset=(0.55, -0.45))
        vr = ns.vector(res, color=DEV, origin=proj)
        rlab = ns.point_label(MathTex(r"\mathbf x - \bar x\mathbf 1", font_size=28, color=DEV), proj + res / 2,
                              offset=(0.2, 0.5))
        ra = ns.right_angle(proj, -proj, res, size=0.5)
        coords = label(rf"heights $({x[0]:.1f},\ {x[1]:.1f},\ {x[2]:.1f})$, \ $c = {c:.0f}$", font_size=24,
                       color=GREY_A).to_corner(UL, buff=0.35)
        rows = [
            cmath(r"\|\mathbf x - c\mathbf 1\|^2", r"=", r"\|\mathbf x - \bar x\mathbf 1\|^2", r"+",
                  r"\|(\bar x - c)\mathbf 1\|^2", font_size=32,
                  colors={r"\|\mathbf x - \bar x\mathbf 1\|^2": DEV, r"\|(\bar x - c)\mathbf 1\|^2": MEAN}),
            cmath(r"\sum_i (x_i - c)^2", r"=", r"\sum_i (x_i - \bar x)^2", r"+", r"n(\bar x - c)^2", font_size=32,
                  colors={r"\sum_i (x_i - \bar x)^2": DEV, r"n(\bar x - c)^2": MEAN}),
        ]
        whys = [why(r"Pythagoras: \ the residual is $\perp \mathbf 1$"), why(r"written out")]
        for r in rows:
            r.scale(0.95)
        nums = MathTex(rf"{np.sum(v ** 2):.2f}", r"=", rf"{np.sum(res ** 2):.2f}", r"+", rf"{3 * (m - c) ** 2:.2f}",
                       font_size=32)
        nums[2].set_color(DEV)
        nums[4].set_color(MEAN)
        with self.voiceover(
            "Why squares, rather than absolute values? Because squares are geometry. <bookmark mark='a'/> Take a "
            "sample of three heights. Three numbers are one point in three-dimensional space: person one along "
            "this axis, person two along that one, person three up. <bookmark mark='b'/> Subtract any candidate "
            "centre c from all three, and you get this white vector. The diagonal line is every point whose three "
            "coordinates are equal: every way of replacing the sample by one number. <bookmark mark='c'/> Now drop "
            "a perpendicular from the white point onto the diagonal. The foot is exactly the mean, repeated three "
            "times: the mean is the projection of the data onto the diagonal. <bookmark mark='d'/> What's left, the "
            "deviations from the mean, is the red vector, at right angles to the diagonal. <bookmark mark='e'/> So "
            "Pythagoras applies. The squared distance from the data to any centre equals the squared deviations "
            "from the mean, plus n times the squared distance from the mean to that centre. "
            "<bookmark mark='f'/> That one identity says three things at once: that the mean minimizes the sum of "
            "squares, which we found in the last chapter; that spread around any point splits into spread around "
            "the mean plus an offset; and, when we come to regression and the analysis of variance, that sums of "
            "squares can be cut into pieces. Absolute values have no Pythagoras. That's why squares won."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(coords))
            vo.wait_until("a")
            self.play(ns.turn(0.5, run_time=3.0))
            vo.wait_until("b")
            self.add(diag, vx)
            self.play(NSpace.reveal(diag, vx), FadeIn(vlab), FadeIn(dlab))
            vo.wait_until("c")
            self.add(vp)
            self.play(NSpace.reveal(vp), FadeIn(plab))
            vo.wait_until("d")
            self.add(vr, ra)
            self.play(NSpace.reveal(vr, ra), FadeIn(rlab))
            self.play(ns.turn(-0.9, run_time=4.0))
            vo.wait_until("e")
            step = ladder(self, rows, whys, keep=2, top=3.2, x=2.6, buff=0.55)
            step(0)
            step(1)
            nums.next_to(rows[1], DOWN, buff=0.4).align_to(rows[1], LEFT)
            self.play(FadeIn(nums))
            vo.wait_until("f")
            self.play(ns.turn(0.6, run_time=4.0))
        for m_ in (vx, vp, vr, diag, ra):
            m_.clear_updaters()
        self.clear_scene()

    def robust(self):
        s = load("spread")
        h, y = s["height"], s["income"]
        hd = VGroup(label(r"", font_size=24), label(r"SD", font_size=26, color=S.ACCENT),
                    label(r"MAD $\times 1.4826$", font_size=26, color=MEDIAN),
                    label(r"IQR $/ 1.349$", font_size=26, color=MODE))
        r1 = VGroup(label(r"heights (cm)", font_size=26), MathTex(f"{h['sd']:.2f}", font_size=34),
                    MathTex(f"{1.4826 * h['mad']:.2f}", font_size=34), MathTex(f"{h['iqr'] / 1.349:.2f}", font_size=34))
        r2 = VGroup(label(r"incomes", font_size=26), MathTex(fmt_int(round(y['sd'])), font_size=34),
                    MathTex(fmt_int(round(1.4826 * y['mad'])), font_size=34),
                    MathTex(fmt_int(round(y['iqr'] / 1.349)), font_size=34))
        tab = VGroup(hd, r1, r2)
        for j in range(4):
            xs = [-4.6, -1.4, 1.8, 5.0][j]
            for row in tab:
                row[j].move_to([xs, 0, 0])
        for i, row in enumerate(tab):
            row.set_y(1.2 - 1.1 * i)
        defs = VGroup(
            label(r"MAD: \ the median of $|x_i - \mathrm{median}|$", font_size=26, color=MEDIAN),
            label(r"IQR: \ $Q_3 - Q_1$, \ the width of the middle half", font_size=26, color=MODE),
            label(r"the factors make all three agree for a normal distribution", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.3, 0])
        tag = simulated_tag(r"simulated: all 741{,}311 adults of the World")
        with self.voiceover(
            "Squares have a cost, though: they magnify big deviations. <bookmark mark='a'/> Two other measures of "
            "spread don't. The MAD is the median of the absolute deviations from the median. The interquartile "
            "range is the width of the middle half of the data. Each is scaled by a constant so that, for a normal "
            "distribution, all three agree. <bookmark mark='b'/> For the World's heights they nearly do: "
            f"{h['sd']:.2f}, {1.4826 * h['mad']:.2f} and {h['iqr'] / 1.349:.2f} centimetres. The heights are close to "
            "a bell, a slightly flattened one, because men and women are mixed. <bookmark mark='c'/> For incomes, "
            f"they don't. The standard deviation is {money(round(y['sd']))}; the robust measures say about "
            f"{money(round(1.4826 * y['mad']))} and {money(round(y['iqr'] / 1.349))}. The standard deviation is "
            "more than twice as big, because a few enormous incomes, squared, dominate it. "
            "<bookmark mark='d'/> Neither answer is wrong. They're answers to different questions, and Part 30 is "
            "about choosing between them when some of the data are bad."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(defs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(r1, shift=UP * 0.2), FadeIn(defs[2]))
            vo.wait_until("c")
            self.play(FadeIn(r2, shift=UP * 0.2))
            self.play(Indicate(r2[1], color=S.RESID, scale_factor=1.3))
            vo.wait_until("d")
            self.play(Indicate(VGroup(r2[2], r2[3]), color=MEDIAN, scale_factor=1.15))
        self.clear_scene()

    def chebyshev(self):
        s = load("spread")
        ks, cheb = s["ks"], s["cheb"]
        fh, fy = s["frac_height"], s["frac_income"]
        A = axes([0, 5], [0, 1], x_length=7.2, y_length=4.2, ylabel=r"share within $k$ SDs of the mean",
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.5, -0.6, 0])
        ax = A.ax
        bars = VGroup()
        for i, k in enumerate(ks):
            for j, (val, col) in enumerate(((cheb[i], GREY_B), (fh[i], S.TRUTH), (fy[i], MEAN))):
                xl = 0.6 + i * 1.15 + j * 0.3
                r = Rectangle(width=ax.c2p(0.28, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, val)[1] - ax.c2p(0, 0)[1],
                              stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([ax.c2p(xl, 0)[0], (ax.c2p(0, val)[1] + ax.c2p(0, 0)[1]) / 2, 0])
                bars.add(r)
            bars.add(MathTex(f"k = {k:g}", font_size=26, color=GREY_A).next_to(ax.c2p(0.9 + i * 1.15, 0), DOWN,
                                                                             buff=0.15))
        leg = legend([(GREY_B, r"Chebyshev's guarantee, $1 - 1/k^2$"), (S.TRUTH, r"the World's heights"),
                      (MEAN, r"the World's incomes")], font_size=22).move_to([4.2, 1.7, 0])
        thm = theorem_card(r"Chebyshev (1867)", r"For any distribution with a variance, \ at least $1 - 1/k^2$ of "
                           r"it lies within $k$ standard deviations of the mean.", color=S.ACCENT, width=5.0,
                           font_size=22).move_to([4.2, -1.1, 0])
        with self.voiceover(
            "How much of the data does a standard deviation describe? <bookmark mark='a'/> Chebyshev proved a "
            "guarantee in 1867 that holds for every distribution with a variance at all: at least one minus one over "
            "k squared of it lies within k standard deviations of the mean. Three quarters within two standard "
            "deviations; eight ninths within three. <bookmark mark='b'/> For the World's heights, the truth is far "
            f"better: {pct(fh[1])} percent within two standard deviations, and {pct(fh[2])} percent within three. "
            f"<bookmark mark='c'/> Even the incomes beat the guarantee: {pct(fy[1])} percent within two, though for "
            "a strange reason: their standard deviation is so inflated by the tail that two of them reach most of "
            "the way to the rich. <bookmark mark='d'/> Chebyshev's bound is a guarantee, not a description. Its "
            "virtue is that it never fails. We'll prove it in two lines in Part 6, and it's the ancestor of the "
            "concentration inequalities that run all the way into the PhD stages."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=LEFT * 0.2))
            self.play(LaggedStart(*[GrowFromEdge(bars[i * 4], DOWN) for i in range(len(ks))], lag_ratio=0.2),
                      *[FadeIn(bars[i * 4 + 3]) for i in range(len(ks))], FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(bars[i * 4 + 1], DOWN) for i in range(len(ks))], lag_ratio=0.2),
                      FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(bars[i * 4 + 2], DOWN) for i in range(len(ks))], lag_ratio=0.2),
                      FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(Circumscribe(thm, color=S.ACCENT))
        self.clear_scene()
