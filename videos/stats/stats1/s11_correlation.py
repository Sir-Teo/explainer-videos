from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403
from videos.stats.stats1.compute import correlation_cloud

POS, NEG = S.EST, S.RESID


class Correlation(VoiceoverScene):
    def construct(self):
        self.card()
        self.scatter()
        self.cosine()
        self.cauchy()
        self.range_()

    def card(self):
        card = chapter_card(10, r"Two variables: correlation as a cosine", r"When one is big, is the other?",
                            lit=(1886,), part=PART)
        with self.voiceover("Chapter ten. Two variables: correlation as a cosine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes_(self, center=(-2.4, -0.3, 0), w=7.4, h=5.6):
        return axes([150, 192], [154, 200], x_length=w, y_length=h, xlabel=r"mid-parent height (cm)",
                    ylabel=r"adult child (cm)", xticks=[165, 170, 175, 180, 185, 190],
                    yticks=[160, 170, 180, 190], center=list(center))

    def scatter(self):
        d = load("correlation")
        mid, ch = np.asarray(d["mid"]), np.asarray(d["child"])
        A = self.axes_()
        ax = A.ax
        mx, my = mid.mean(), ch.mean()
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=S.DATA) for a, b in zip(mid, ch)])
        vx = DashedLine(ax.c2p(mx, 154), ax.c2p(mx, 200), color=GREY_B, stroke_width=2)
        hy = DashedLine(ax.c2p(150, my), ax.c2p(192, my), color=GREY_B, stroke_width=2)
        prod = (mid - mx) * (ch - my)
        q = d["quad"]
        signs = VGroup(MathTex("+", font_size=60, color=POS).move_to(ax.c2p(187, 193)),
                       MathTex("+", font_size=60, color=POS).move_to(ax.c2p(165, 159)),
                       MathTex("-", font_size=60, color=NEG).move_to(ax.c2p(165, 193)),
                       MathTex("-", font_size=60, color=NEG).move_to(ax.c2p(187, 159)))
        # a few products drawn as signed rectangles from the centre
        inside = (mid > 163) & (mid < 189) & (ch > 157) & (ch < 195)
        pp = np.where(inside, prod, np.nan)
        order = np.argsort(np.where(np.isnan(pp), 0, pp))
        pick = [int(np.nanargmax(pp)), int(np.nanargmin(pp)), int(order[int(0.85 * len(order))])]
        rects = VGroup()
        for i in pick:
            a, b = ax.c2p(mx, my), ax.c2p(mid[i], ch[i])
            col = POS if prod[i] > 0 else NEG
            rects.add(Polygon(a, [b[0], a[1], 0], b, [a[0], b[1], 0], stroke_color=col, stroke_width=2,
                              fill_color=col, fill_opacity=0.3))
        eqs = VGroup(
            cmath(r"\mathrm{cov}", r"=", r"\frac1n\sum_i (x_i - \bar x)(y_i - \bar y)", font_size=32),
            MathTex(rf"= {d['cov']:.1f}\ \text{{cm}}^2", font_size=32),
            cmath(r"r", r"=", r"\frac{\mathrm{cov}}{s_x s_y}", font_size=36),
            MathTex(rf"= {d['r']:.2f}", font_size=36, color=S.ACCENT),
        )
        eqs[1].next_to(eqs[0], DOWN, buff=0.15).align_to(eqs[0][1], LEFT)
        eqs[2].next_to(eqs[1], DOWN, buff=0.5).align_to(eqs[0], LEFT)
        eqs[3].next_to(eqs[2], DOWN, buff=0.15).align_to(eqs[2][1], LEFT)
        eqs.move_to([4.6, 0.5, 0])
        counts = label(rf"agree: \ {q['pp'] + q['mm']} \qquad disagree: \ {q['pm'] + q['mp']}", font_size=26)
        counts.move_to([4.6, -2.4, 0])
        tag = simulated_tag(r"simulated: 400 World families")
        hc = history_card(1886, r"Francis Galton", r"``co-relation'', \ from the heights of parents and children",
                          color=S.MUSEUM, width=4.6, font_size=20).move_to([4.6, 2.6, 0])
        with self.voiceover(
            "Now two variables at once. <bookmark mark='a'/> Four hundred families from the World: the mid-parent "
            "height, the average of the two parents, with mothers' heights scaled up by eight percent as Galton "
            "did, against the height of their grown child. Galton, studying exactly this in 1886, invented the idea "
            "we're about to build. <bookmark mark='b'/> Draw a cross through the two means. It cuts the plane into "
            "four quadrants. In the top right and bottom left, both are above average or both below: they agree. In "
            f"the other two they disagree. <bookmark mark='c'/> Here {q['pp'] + q['mm']} families agree and "
            f"{q['pm'] + q['mp']} disagree. <bookmark mark='d'/> To turn that into a number, multiply each family's "
            "two deviations. A family that agrees gives a positive product, a rectangle of positive area; one that "
            "disagrees, a negative one. <bookmark mark='e'/> Average the products: that's the covariance, "
            f"{d['cov']:.1f} square centimetres. <bookmark mark='f'/> Its units are awkward, so divide by both "
            f"standard deviations. The result, the correlation r, has no units at all. Here it's {d['r']:.2f}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(vx), Create(hy), FadeOut(hc))
            self.play(*[p.animate.set_color(POS if v > 0 else NEG) for p, v in zip(dots, prod)], FadeIn(signs))
            vo.wait_until("c")
            self.play(FadeIn(counts))
            vo.wait_until("d")
            self.play(LaggedStart(*[DrawBorderThenFill(r) for r in rects], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(Write(eqs[0]), FadeIn(eqs[1]))
            vo.wait_until("f")
            self.play(Write(eqs[2]), FadeIn(eqs[3]))
        self.clear_scene()

    def cosine(self):
        d = load("correlation")
        xc, yc = np.asarray(d["xc"]), np.asarray(d["yc"])
        ns = NSpace(scale=0.62, center=[-3.4, -1.6, 0], angle=-0.6, tilt=0.35, axis_len=4.0,
                    axis_labels=[r"obs.\ 1", r"obs.\ 2", r"obs.\ 3"])
        vx = ns.vector(xc, color=S.EST)
        vy = ns.vector(yc, color=MEDIAN)
        lx = ns.point_label(MathTex(r"\mathbf x - \bar x\mathbf 1", font_size=28, color=S.EST), xc, offset=(0.5, -0.15))
        ly = ns.point_label(MathTex(r"\mathbf y - \bar y\mathbf 1", font_size=28, color=MEDIAN), yc, offset=(-0.3, 0.45))

        def arc():
            u, w = xc / np.linalg.norm(xc), yc / np.linalg.norm(yc)
            ang = np.arccos(np.clip(u @ w, -1, 1))
            perp = w - (u @ w) * u
            perp = perp / np.linalg.norm(perp)
            pts = [ns.project(1.0 * (np.cos(t) * u + np.sin(t) * perp)) for t in np.linspace(0, ang, 30)]
            m = VMobject(color=S.ACCENT, stroke_width=3)
            m.set_points_smoothly(pts)
            return m

        theta = always_redraw(arc)
        data = VGroup(MathTex(r"x = (2,\ 5,\ 8)", font_size=32, color=S.EST),
                      MathTex(r"y = (3,\ 3.5,\ 7.5)", font_size=32, color=MEDIAN)).arrange(DOWN, buff=0.15)
        data.to_corner(UL, buff=0.4)
        rows = [
            cmath(r"r", r"=", r"\frac{\sum_i (x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_i (x_i - \bar x)^2}\sqrt{\sum_i (y_i - \bar y)^2}}",
                  font_size=30),
            cmath(r"r", r"=", r"\frac{\mathbf u \cdot \mathbf v}{\|\mathbf u\|\,\|\mathbf v\|}", font_size=34),
            cmath(r"r", r"=", r"\cos\theta", font_size=40, colors={r"\cos\theta": S.ACCENT}),
        ]
        whys = [why(r"the $1/n$'s cancel"), why(r"$\mathbf u, \mathbf v$: the centred data"), why(r"the angle between them")]
        nums = MathTex(rf"\theta = {d['angle']:.1f}^\circ, \quad \cos\theta = {d['cos']:.3f} = r", font_size=32,
                       color=S.ACCENT)
        with self.voiceover(
            "Correlation has a geometric meaning that makes everything about it obvious. <bookmark mark='a'/> Take "
            "just three pairs of numbers. As in chapter five, the three x's are one point in three-dimensional "
            "space, and so are the three y's. Centre each, by subtracting its mean, and we have two arrows. "
            "<bookmark mark='b'/> Write out r: the covariance over the two standard deviations. The one over n's "
            "cancel, and what's left is the dot product of the two centred vectors, divided by both their lengths. "
            "<bookmark mark='c'/> That's the cosine of the angle between them. <bookmark mark='d'/> Here the angle "
            f"is {d['angle']:.1f} degrees, and its cosine is {d['cos']:.3f}, exactly the correlation of these six "
            "numbers. With four hundred families, the vectors live in four hundred dimensions, but there are still "
            "just two of them, and the angle between them is still the correlation."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(data))
            vo.wait_until("a")
            self.add(vx, vy)
            self.play(NSpace.reveal(vx, vy), FadeIn(lx), FadeIn(ly))
            self.play(ns.turn(0.6, run_time=3.0))
            vo.wait_until("b")
            step = ladder(self, rows, whys, keep=3, top=2.9, x=2.4, buff=0.5)
            step(0)
            step(1)
            vo.wait_until("c")
            self.add(theta)
            step(2)
            vo.wait_until("d")
            nums.next_to(rows[2], DOWN, buff=0.4)
            self.play(FadeIn(nums))
            self.play(ns.turn(-1.0, run_time=4.0))
        for m in (vx, vy, theta):
            m.clear_updaters()
        self.clear_scene()

    def cauchy(self):
        rows = [
            cmath(r"0", r"\le", r"\|\mathbf u - t\mathbf v\|^2", font_size=38),
            cmath(r"0", r"\le", r"\|\mathbf u\|^2 - 2t\,\mathbf u\cdot\mathbf v + t^2\|\mathbf v\|^2", font_size=38),
            cmath(r"(\mathbf u \cdot \mathbf v)^2", r"\le", r"\|\mathbf u\|^2\,\|\mathbf v\|^2", font_size=38),
            cmath(r"-1", r"\le", r"r \le 1", font_size=42, colors={r"r \le 1": S.ACCENT}),
        ]
        whys = [why(r"a length is never negative, \ for every $t$"), why(r"expand"),
                why(r"a quadratic in $t$ that never dips below $0$: \ discriminant $\le 0$"),
                why(r"divide; \ equality iff $\mathbf u \parallel \mathbf v$")]
        pics = VGroup()
        g = np.random.Generator(np.random.PCG64(11))
        for k, rr in enumerate((-1.0, -0.5, 0.0, 0.5, 0.9, 1.0)):
            n = 60
            a, b = correlation_cloud(rr, n, g)
            scale = 0.68 / max(abs(a).max(), abs(b).max())
            box = Square(1.5, stroke_color=GREY_D, stroke_width=1)
            pts = VGroup(*[Dot([scale * u, scale * v, 0], radius=0.02, color=S.DATA) for u, v in zip(a, b)])
            cap = MathTex(rf"r = {rr:g}", font_size=24, color=S.ACCENT).next_to(box, DOWN, buff=0.1)
            pics.add(VGroup(box, pts.move_to(box), cap))
        pics.arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.5)
        ptag = note(r"illustrative: draws rescaled to the displayed sample $r$").next_to(pics, UP, buff=0.1).align_to(pics, RIGHT)
        with self.voiceover(
            "The geometry also proves the most important fact about r: it always lies between minus one and one. "
            "<bookmark mark='a'/> The length of u minus t times v can't be negative, whatever t is. "
            "<bookmark mark='b'/> Expand it, and it's a quadratic in t. <bookmark mark='c'/> A quadratic that never "
            "dips below zero has at most one real root, so its discriminant can't be positive. That's the "
            "Cauchy–Schwarz inequality. <bookmark mark='d'/> Divide through, and r is trapped between minus one and "
            "one, with equality only when the two arrows point the same way or opposite ways, which means every "
            "point lies exactly on a line. <bookmark mark='e'/> A cosine of one is a perfect straight line rising; "
            "zero is no linear relation at all; minus one a perfect line falling."
        ) as vo:
            title = label(r"Why $-1 \le r \le 1$", font_size=40, color=S.ACCENT).to_corner(UL, buff=0.5)
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.4)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pics], lag_ratio=0.2), FadeIn(ptag))
        self.clear_scene()

    def range_(self):
        d = load("correlation")
        mid, ch, tall = np.asarray(d["mid"]), np.asarray(d["child"]), np.asarray(d["tall"])
        A = self.axes_(center=(-2.6, -0.3, 0))
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=S.DATA) for a, b in zip(mid, ch)])
        cut = DashedLine(ax.c2p(mid[tall].min(), 154), ax.c2p(mid[tall].min(), 200), color=S.ACCENT, stroke_width=2)
        b, a0 = np.polyfit(mid, ch, 1)
        fit = Line(ax.c2p(163, a0 + b * 163), ax.c2p(189, a0 + b * 189), color=S.EST, stroke_width=4)
        bt, at = np.polyfit(mid[tall], ch[tall], 1)
        fit_t = Line(ax.c2p(mid[tall].min(), at + bt * mid[tall].min()), ax.c2p(189, at + bt * 189), color=S.ACCENT,
                     stroke_width=4)
        txt = VGroup(
            MathTex(rf"r = {d['r']:.2f}", r",\ \ \text{slope} = " + f"{d['slope']:.2f}", font_size=32, color=S.EST),
            MathTex(rf"\text{{tallest quarter: }} r = {d['r_tall']:.2f}", r",\ \ \text{slope} = " + f"{bt:.2f}",
                    font_size=30, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, 1.2, 0])
        notes = VGroup(label(r"$r$ measures how tightly the points hug a line, \ not how steep it is", font_size=24,
                             color=GREY_A),
                       label(r"and neither says anything about cause \ (chapter 12; \ Part 36)", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for n_ in notes:
            if n_.width > 5.4:
                n_.width = 5.4
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.6, 0])
        with self.voiceover(
            "Two warnings about what r is not. <bookmark mark='a'/> It's not the slope. The line that best predicts "
            f"a child's height from the mid-parent has slope {d['slope']:.2f}: an inch taller in parents, two thirds "
            "of an inch taller in children on average, very close to Galton's own estimate of two thirds. The "
            f"correlation is {d['r']:.2f}. Change the units of one variable and the slope changes; r doesn't. "
            "<bookmark mark='b'/> And r depends on the range you look at. Keep only the families whose parents are "
            f"in the tallest quarter. The slope barely changes, {bt:.2f}, but the correlation falls to "
            f"{d['r_tall']:.2f}. <bookmark mark='c'/> Nothing about how height is inherited has changed. We've only "
            "thrown away most of the spread in x, and r measures how much of the spread in y lines up with the "
            "spread in x. Studies of selected groups, like university entrance tests among those admitted, fall "
            "into this trap constantly. <bookmark mark='d'/> And neither r nor the slope says anything about cause. "
            "That's two chapters and thirty-five parts away."
        ) as vo:
            self.play(FadeIn(A), LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=0.003), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(Create(cut), *[p.animate.set_opacity(0.15) for p, t in zip(dots, tall) if not t])
            self.play(*[p.animate.set_color(S.ACCENT) for p, t in zip(dots, tall) if t], Create(fit_t),
                      FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.clear_scene()
