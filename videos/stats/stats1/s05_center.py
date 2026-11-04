from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Center(VoiceoverScene):
    def construct(self):
        self.card()
        self.squares()
        self.absolute()
        self.lp()
        self.clock()

    def card(self):
        card = chapter_card(4, r"The centre as an optimization", r"Which single number best stands for all of them?",
                            lit=(1805,), part=PART)
        with self.voiceover("Chapter four. The centre as an optimization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lanes(self, x, x_range=(0, 200)):
        """Each income in its own lane, so deviations to a centre don't overlap."""
        L = axes(list(x_range), [0, 1], x_length=11.0, y_length=0.4, xlabel=r"income (thousands)",
                 xticks=[0, 50, 100, 150, 200], center=[0, 0.75, 0])
        L.ax.y_axis.set_opacity(0)
        ax = L.ax
        ys = [1.15 + 0.24 * i for i in range(len(x))]
        dots = VGroup(*[Dot([ax.c2p(v, 0)[0], y, 0], radius=0.08, color=S.DATA) for v, y in zip(x, ys)])
        guides = VGroup(*[DashedLine(ax.c2p(v, 0), [ax.c2p(v, 0)[0], y, 0], color=GREY_D, stroke_width=1,
                                     dash_length=0.05) for v, y in zip(x, ys)])
        return L, dots, guides, ys

    def squares(self):
        d = load("centers")
        x = np.asarray(d["nine"])
        L, dots, guides, ys = self.lanes(x)
        ax = L.ax
        c = ValueTracker(10.0)
        cline = always_redraw(lambda: Line([ax.c2p(c.get_value(), 0)[0], 0.85, 0],
                                           [ax.c2p(c.get_value(), 0)[0], ys[-1] + 0.3, 0], color=S.ACCENT,
                                           stroke_width=3))
        clab = always_redraw(lambda: MathTex("c", font_size=36, color=S.ACCENT)
                             .next_to([ax.c2p(c.get_value(), 0)[0], ys[-1] + 0.3, 0], UP, buff=0.08))
        sticks = always_redraw(lambda: VGroup(*[Line([ax.c2p(c.get_value(), 0)[0], y, 0], [ax.c2p(v, 0)[0], y, 0],
                                                     color=DEV, stroke_width=3) for v, y in zip(x, ys)]))
        grid = np.asarray(d["grid"])
        sq = np.asarray(d["sq"])
        F = axes([0, 200], [0, sq.max() * 1.05], x_length=11.0, y_length=2.4, center=[0, -2.25, 0])
        fax = F.ax
        fl = label(r"$\sum_i (x_i - c)^2$", font_size=28, color=DEV).next_to(F, LEFT, buff=0.15).shift(UP * 0.6)
        sel = (grid >= 0) & (grid <= 200)
        loss = curve(fax, grid[sel], sq[sel], DEV, 3)
        rider = always_redraw(lambda: Dot(fax.c2p(c.get_value(), float(np.interp(c.get_value(), grid, sq))),
                                          radius=0.08, color=S.ACCENT))
        tag = simulated_tag(r"simulated: nine World incomes")
        steps = [
            cmath(r"\frac{d}{dc}\sum_i (x_i - c)^2", r"=", r"-2\sum_i (x_i - c)", font_size=34),
            cmath(r"-2\sum_i (x_i - c)", r"=", r"0", font_size=34),
            cmath(r"c", r"=", r"\frac1n \sum_i x_i", r"=", r"\bar x", font_size=34, colors={r"\bar x": MEAN}),
        ]
        whys = [why(r"chain rule"), why(r"at the bottom"), why(r"the mean")]
        for r in steps:
            r.scale(0.9)
        mean_l = Line([ax.c2p(d["mean9"], 0)[0], 0.85, 0], [ax.c2p(d["mean9"], 0)[0], ys[-1] + 0.3, 0],
                      color=MEAN, stroke_width=4)
        mean_t = MathTex(rf"\bar x = {d['mean9']:.1f}", font_size=30, color=MEAN).next_to(mean_l.get_top(), RIGHT, buff=0.15)
        with self.voiceover(
            "If you had to replace nine numbers by one, which would you choose? <bookmark mark='a'/> Here are nine "
            "incomes from the World, in thousands, each in its own lane. Pick a candidate centre, c, and measure "
            "how far it is from each income. <bookmark mark='b'/> Legendre's answer, in 1805, and Gauss's, was to square those "
            "distances and add them up, and choose the c that makes the total as small as possible. "
            "<bookmark mark='c'/> Slide c, and watch the total. It falls, reaches a bottom, and rises again. "
            "<bookmark mark='d'/> Where is the bottom? Differentiate: the derivative is minus twice the sum of the "
            "deviations. Set it to zero, and c must be the ordinary average. <bookmark mark='e'/> The mean is the "
            f"answer to an optimization problem. Here it's {d['mean9']:.1f} thousand. And notice where it sits: to "
            "the right of seven of the nine people, pulled there by one large income."
        ) as vo:
            self.play(FadeIn(L), FadeIn(guides), LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=0.1),
                      FadeIn(tag))
            vo.wait_until("a")
            self.add(sticks, cline, clab)
            self.play(c.animate.set_value(150.0), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(F), FadeIn(fl), Create(loss), run_time=2.0)
            self.add(rider)
            vo.wait_until("c")
            self.play(c.animate.set_value(5.0), run_time=2.5)
            self.play(c.animate.set_value(d["mean9"]), run_time=2.0)
            vo.wait_until("d")
            board = VGroup(*steps)
            for r in steps:
                r.move_to([3.2, -1.0, 0])
            self.play(FadeOut(F), FadeOut(fl), FadeOut(loss), FadeOut(rider))
            step = ladder(self, steps, whys, keep=3, top=-0.35, x=1.4, buff=0.35)
            for i in range(3):
                step(i, run_time=1.0)
            vo.wait_until("e")
            self.play(FadeIn(mean_l), FadeIn(mean_t), FadeOut(cline), FadeOut(clab))
        self.play(FadeOut(VGroup(*steps, *whys, board)), FadeOut(sticks))
        self.keep = dict(L=L, dots=dots, guides=guides, ys=ys, mean_l=mean_l, mean_t=mean_t, tag=tag)

    def absolute(self):
        d = load("centers")
        k = self.keep
        x = np.asarray(d["nine"])
        ax, ys = k["L"].ax, k["ys"]
        c = ValueTracker(d["mean9"])
        cline = always_redraw(lambda: Line([ax.c2p(c.get_value(), 0)[0], 0.85, 0],
                                           [ax.c2p(c.get_value(), 0)[0], ys[-1] + 0.3, 0], color=S.ACCENT,
                                           stroke_width=3))

        def pulls():
            g = VGroup()
            cx = ax.c2p(c.get_value(), 0)[0]
            for v, y in zip(x, ys):
                px = ax.c2p(v, 0)[0]
                if abs(px - cx) < 0.05:
                    continue
                direction = LEFT if px < cx else RIGHT
                g.add(Arrow([cx, y, 0], [cx, y, 0] + direction * 0.7, buff=0, color=MEDIAN if px < cx else S.EST,
                            stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.4))
            return g

        arrows = always_redraw(pulls)

        def count():
            left = int(np.sum(x < c.get_value() - 1e-9))
            right = int(np.sum(x > c.get_value() + 1e-9))
            return MathTex(rf"\text{{left}}: {left} \qquad \text{{right}}: {right} \qquad \text{{slope}} = {left - right}",
                           font_size=32).move_to([0, -0.4, 0])

        cnt = always_redraw(count)
        grid, ab = np.asarray(d["grid"]), np.asarray(d["ab"])
        F = axes([0, 200], [0, ab.max() * 1.05], x_length=11.0, y_length=2.0, center=[0, -2.4, 0])
        fax = F.ax
        sel = (grid >= 0) & (grid <= 200)
        loss = curve(fax, grid[sel], ab[sel], MEDIAN, 3)
        fl = label(r"$\sum_i |x_i - c|$", font_size=28, color=MEDIAN).next_to(F, LEFT, buff=0.15).shift(UP * 0.5)
        rider = always_redraw(lambda: Dot(fax.c2p(c.get_value(), float(np.interp(c.get_value(), grid, ab))),
                                          radius=0.08, color=S.ACCENT))
        med_l = Line([ax.c2p(d["median9"], 0)[0], 0.85, 0], [ax.c2p(d["median9"], 0)[0], ys[-1] + 0.3, 0],
                     color=MEDIAN, stroke_width=4)
        med_t = MathTex(rf"\text{{median}} = {d['median9']:.1f}", font_size=30, color=MEDIAN)
        med_t.next_to(med_l.get_top(), LEFT, buff=0.15)
        # the richest income moves far right: the mean follows, the median does not
        top = ValueTracker(float(x[-1]))
        with self.voiceover(
            "Now change the loss. <bookmark mark='a'/> Instead of squared distances, add up the plain distances, "
            "the absolute values. Laplace preferred this one. <bookmark mark='b'/> Its derivative is easy to read "
            "off the picture: every income to the left of c pulls the total up as c moves right, one unit per unit, "
            "and every income to the right pulls it down. So the slope is the number on the left minus the number "
            "on the right. <bookmark mark='c'/> It's a tug of war. The total keeps falling while more people are on "
            "the right, and stops falling when the two sides are equal: <bookmark mark='d'/> at the middle "
            f"observation, the median, {d['median9']:.1f} thousand. <bookmark mark='e'/> The median doesn't care how "
            "far away people are, only which side they're on. Make the richest person three times richer, and the "
            "median doesn't move. The mean does."
        ) as vo:
            self.play(FadeOut(k["mean_t"]), k["mean_l"].animate.set_opacity(0.4))
            vo.wait_until("a")
            self.add(cline)
            self.play(FadeIn(F), FadeIn(fl), Create(loss))
            self.add(rider)
            vo.wait_until("b")
            self.add(arrows, cnt)
            self.play(c.animate.set_value(10.0), run_time=2.0)
            vo.wait_until("c")
            self.play(c.animate.set_value(70.0), run_time=3.0)
            self.play(c.animate.set_value(d["median9"]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(med_l), FadeIn(med_t))
            vo.wait_until("e")
            arrows.clear_updaters()
            self.play(FadeOut(arrows), FadeOut(cline), FadeOut(rider), FadeOut(cnt))
            rich = k["dots"][-1]
            mean_track = always_redraw(lambda: Line(
                [ax.c2p(np.mean(np.r_[x[:-1], top.get_value()]), 0)[0], 0.85, 0],
                [ax.c2p(np.mean(np.r_[x[:-1], top.get_value()]), 0)[0], ys[-1] + 0.3, 0],
                color=MEAN, stroke_width=4))
            self.remove(k["mean_l"])
            self.add(mean_track)
            rich.add_updater(lambda m: m.move_to([ax.c2p(min(top.get_value(), 200), 0)[0], ys[-1], 0]))
            self.play(top.animate.set_value(float(x[-1]) * 3), run_time=3.0)
            rich.clear_updaters()
            mean_track.clear_updaters()
        self.clear_scene()

    def lp(self):
        d = load("centers")
        x = np.asarray(d["big"])
        ps, cs = d["ps"], d["lp"]
        L = axes([0, 400], [0, 1], x_length=11.6, y_length=0.4, xlabel=r"income (thousands), 200 adults",
                 xticks=[0, 100, 200, 300, 400], center=[0, -1.2, 0])
        L.ax.y_axis.set_opacity(0)
        ax = L.ax
        g = np.random.Generator(np.random.PCG64(6))
        pts = VGroup(*[Dot(ax.c2p(v, 0) + UP * (0.15 + 0.5 * g.random()), radius=0.035, color=S.DATA)
                       for v in x])
        formula = cmath(r"c_p", r"=", r"\arg\min_c \sum_i |x_i - c|^p", font_size=40).to_edge(UP, buff=0.5)
        marks = {r"median": (1.0, d["median200"], MEDIAN), r"mean": (2.0, d["mean200"], MEAN),
                 r"midrange": (np.inf, d["midrange"], MIDRANGE)}
        ticks = VGroup()
        for name, (p, v, col) in marks.items():
            t = VGroup(Line(ax.c2p(v, 0) + UP * 0.9, ax.c2p(v, 0) + UP * 1.3, color=col, stroke_width=3),
                       label(rf"{name}\ \ $p = {'\\infty' if np.isinf(p) else int(p)}$", font_size=22, color=col))
            t[1].next_to(t[0], UP, buff=0.08)
            if name == r"median":
                t[1].next_to(t[0].get_top(), LEFT, buff=0.1)
            elif name == r"mean":
                t[1].next_to(t[0].get_top(), RIGHT, buff=0.1)
            ticks.add(t)
        pv = ValueTracker(0)  # index into ps

        def marker():
            i = pv.get_value()
            j = int(np.floor(i))
            j2 = min(j + 1, len(ps) - 1)
            f = i - j
            v = (1 - f) * cs[j] + f * cs[j2]
            pp = (1 - f) * ps[j] + f * ps[j2]
            m = VGroup(Triangle(fill_opacity=1, fill_color=S.ACCENT, stroke_width=0).scale(0.14).rotate(PI)
                       .move_to(ax.c2p(v, 0) + UP * 2.0),
                       MathTex(rf"p = {pp:.1f}:\ \ c_p = {v:.1f}", font_size=30, color=S.ACCENT))
            m[1].next_to(m[0], UP, buff=0.1)
            return m

        mk = always_redraw(marker)
        mode = load("centers")["modes"]
        with self.voiceover(
            "Squares and absolute values are two members of one family. <bookmark mark='a'/> Raise the distances to "
            "any power p, add them up, and minimize. p equals one gives the median; p equals two gives the mean. "
            "<bookmark mark='b'/> Here's the whole family on two hundred incomes. Start at p equals one, at the "
            f"median, {d['median200']:.1f} thousand. <bookmark mark='c'/> As p grows, far-away incomes count for more "
            f"and more, and the centre is dragged toward them: {d['mean200']:.1f} at p equals two, and then far past "
            "anything typical. <bookmark mark='d'/> As p goes to infinity only the two most extreme incomes matter, "
            f"and the centre becomes the midrange, halfway between the smallest and the largest: {d['midrange']:.1f} "
            "thousand, an income almost nobody has. <bookmark mark='e'/> And at the other end, as p shrinks toward "
            "zero, the loss just counts how many points you miss, and the centre becomes the mode: the most crowded "
            f"place. For the World's heights, the most crowded five-centimetre window is centred at {mode[2][1]:.1f}. "
            "So the choice of a centre is a choice of a loss: how much do you mind being far from the people who are "
            "far away?"
        ) as vo:
            self.play(FadeIn(L), FadeIn(pts, lag_ratio=0.005), Write(formula))
            vo.wait_until("a")
            self.play(FadeIn(ticks[0]), FadeIn(ticks[1]))
            vo.wait_until("b")
            self.add(mk)
            vo.wait_until("c")
            self.play(pv.animate.set_value(3), run_time=3.0)
            self.play(pv.animate.set_value(len(ps) - 1), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(ticks[2]))
            vo.wait_until("e")
            self.play(pv.animate.set_value(0), run_time=2.0)
        mk.clear_updaters()
        self.clear_scene()

    def clock(self):
        d = load("centers")
        t = np.asarray(d["times"])
        cen, R = np.array([-3.6, -0.3, 0]), 2.3

        def at(h, r=R):
            a = PI / 2 - 2 * PI * h / 24
            return cen + r * np.array([np.cos(a), np.sin(a), 0])

        face = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(cen)
        hours = VGroup(*[label(lbl, font_size=22, color=GREY_B).move_to(at(h, R + 0.4))
                         for h, lbl in ((0, r"midnight"), (6, r"6 am"), (12, r"noon"), (18, r"6 pm"))])
        dots = VGroup(*[Dot(at(h), radius=0.1, color=S.DATA) for h in t])
        L = axes([0, 24], [0, 1], x_length=5.6, y_length=0.4, xlabel=r"hours after midnight",
                 xticks=[0, 6, 12, 18, 24], center=[3.4, -1.2, 0])
        L.ax.y_axis.set_opacity(0)
        lin = VGroup(*[Dot(L.ax.c2p(h, 0) + UP * 0.15, radius=0.08, color=S.DATA) for h in t])
        arith = VGroup(Line(L.ax.c2p(d["arith"], 0), L.ax.c2p(d["arith"], 0) + UP * 1.0, color=S.RESID,
                            stroke_width=4),
                       label(rf"average: \ {int(d['arith'])}:{int(round(60 * (d['arith'] % 1))):02d} am", font_size=26,
                             color=S.RESID))
        arith[1].next_to(arith[0], UP, buff=0.1)
        on_clock = Dot(at(d["arith"]), radius=0.12, color=S.RESID)
        fh = d["frechet"]
        fr_dot = Dot(at(fh), radius=0.12, color=MEAN)
        hh, mm = int(fh) % 24, int(round(60 * (fh % 1)))
        fr_lab = label(rf"Fr\'echet mean: \ {hh - 12 if hh > 12 else hh}:{mm:02d} pm", font_size=26, color=MEAN)
        fr_lab.next_to(fr_dot, DOWN, buff=0.25)
        eq = cmath(r"\bar x", r"=", r"\arg\min_c \sum_i d(x_i, c)^2", font_size=36, colors={r"\bar x": MEAN})
        eq.move_to([3.4, 1.6, 0])
        tag = note(r"illustrative: six bedtimes").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Seeing the mean as a minimum pays off immediately. <bookmark mark='a'/> Here are six bedtimes, from "
            "twenty to eleven at night to half past one in the morning. What's the average bedtime? "
            "<bookmark mark='b'/> Write them as hours after midnight and average the numbers, and you get "
            f"{int(d['arith'])}:{int(round(60 * (d['arith'] % 1))):02d}: about noon. That's absurd: nobody here goes "
            "to bed at noon. The numbers wrapped around midnight, and the formula didn't know. "
            "<bookmark mark='c'/> But the mean was never really the formula; it was the point that minimizes the "
            "total squared distance. On a clock, distance is the distance around the circle. Minimize that, and "
            f"the centre is {hh - 12 if hh > 12 else hh}:{mm:02d} pm, two minutes before midnight. "
            "<bookmark mark='d'/> This is the Fréchet mean, after Maurice Fréchet, and it works for anything you can "
            "measure distances between: directions, shapes, networks, whole probability distributions. We'll meet "
            "it again in Part 61."
        ) as vo:
            self.play(Create(face), FadeIn(hours), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(L), *[TransformFromCopy(a, b) for a, b in zip(dots, lin)])
            self.play(FadeIn(arith), FadeIn(on_clock))
            vo.wait_until("c")
            self.play(Write(eq))
            self.play(GrowFromCenter(fr_dot), FadeIn(fr_lab))
            vo.wait_until("d")
            self.play(Indicate(fr_dot, color=MEAN, scale_factor=1.5))
        self.clear_scene()
