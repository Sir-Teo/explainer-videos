from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats1.common import *  # noqa: F403
from videos.stats.stats1.compute import qq_demo


class QQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.build()
        self.why_straight()
        self.quetelet()
        self.curvature()

    def card(self):
        card = chapter_card(8, r"The QQ plot", r"Is this a bell curve? Ask the quantiles", lit=(1835,), part=PART)
        with self.voiceover("Chapter eight. The QQ plot."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def build(self):
        d = load("qq")
        z, x = qq_demo(d["men_x"])
        n = len(x)
        # left: the standard normal with its n quantiles; right: the QQ plot
        N = axes([-3, 3], [0, 0.45], x_length=5.0, y_length=2.4, xlabel=r"standard normal $z$", xticks=[-2, 0, 2],
                 center=[-3.2, 1.6, 0])
        nx = N.ax
        zz = np.linspace(-3, 3, 200)
        dens = curve(nx, zz, stats.norm.pdf(zz), S.TRUTH, 3, smooth=True)
        cuts = VGroup(*[Line(nx.c2p(v, 0), nx.c2p(v, stats.norm.pdf(v)), color=S.TRUTH, stroke_width=2)
                        for v in z])
        Q = axes([-2.4, 2.4], [150, 192], x_length=6.0, y_length=5.2, xlabel=r"normal quantile $z_i$",
                 ylabel=r"sorted heights $x_{(i)}$ (cm)", xticks=[-2, -1, 0, 1, 2], yticks=[150, 160, 170, 180, 190],
                 center=[3.4, -0.2, 0])
        qx = Q.ax
        dots = VGroup(*[Dot(qx.c2p(a, b), radius=0.08, color=S.EST) for a, b in zip(z, x)])
        sorted_col = VGroup(*[MathTex(f"{v:.1f}", font_size=26, color=S.DATA) for v in x])
        sorted_col.arrange(DOWN, buff=0.07)
        sorted_col.scale_to_fit_height(6.6).move_to([-6.35, -0.25, 0])
        recipe = VGroup(label(r"1.\ \ sort the data", font_size=24), label(r"2.\ \ the $i$-th of $n$ gets the "
                        r"normal quantile $z_i = \Phi^{-1}\!\big(\tfrac{i - 1/2}{n}\big)$", font_size=24),
                        label(r"3.\ \ plot $(z_i,\ x_{(i)})$", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        recipe.move_to([-3.2, -1.9, 0])
        tag = simulated_tag(rf"simulated: {n} of the World's men", corner=UR)
        with self.voiceover(
            "A histogram tells you a distribution's shape. To ask whether that shape is a particular one, a bell "
            "curve for instance, there's a sharper tool. <bookmark mark='a'/> Take fifteen men from the World and "
            "sort their heights. <bookmark mark='b'/> Now slice a standard bell curve into fifteen pieces of equal "
            "probability, and take the middle of each slice: fifteen normal quantiles, crowded in the centre and "
            "spread out in the tails. <bookmark mark='c'/> Pair them up: the smallest height with the smallest "
            "normal quantile, the second with the second, and so on, and plot each pair. "
            "<bookmark mark='d'/> That's a quantile–quantile plot, introduced in this form by Wilk and "
            "Gnanadesikan in 1968. If the data came from a bell curve, the points should lie on a straight line. "
            "Here they nearly do."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(N), Create(dens))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in sorted_col], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(FadeIn(Q))
            self.play(LaggedStart(*[AnimationGroup(Indicate(cuts[i], color=S.EST), Indicate(sorted_col[i], color=S.EST),
                                                   GrowFromCenter(dots[i])) for i in range(n)], lag_ratio=0.25),
                      run_time=5.0)
            vo.wait_until("d")
            self.play(FadeOut(sorted_col), FadeIn(recipe))
        self.clear_scene()

    def why_straight(self):
        head = label(r"Normal quantiles form a line", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"X", r"=", r"\mu + \sigma Z", font_size=40, colors={r"\mu + \sigma Z": S.TRUTH}),
            cmath(r"P(X \le \mu + \sigma z)", r"=", r"P(Z \le z)", font_size=40),
            cmath(r"Q_X(p)", r"=", r"\mu + \sigma\, \Phi^{-1}(p)", font_size=40, colors={r"\mu + \sigma\, \Phi^{-1}(p)": S.TRUTH}),
        ]
        whys = [why(r"any normal is a shifted, stretched standard one"), why(r"$\sigma > 0$: \ the event is the same"),
                why(r"so its quantiles are a straight line in $\Phi^{-1}(p)$")]
        tail = VGroup(label(r"slope $= \sigma$, \ intercept $= \mu$", font_size=32, color=S.TRUTH),
                      label(r"the same for any location--scale family: \ replace $\Phi$ by its CDF", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.25).move_to([0, -2.4, 0])
        with self.voiceover(
            "Why a straight line? <bookmark mark='a'/> Every normal distribution is a standard one, shifted by its "
            "mean and stretched by its standard deviation: X equals mu plus sigma Z. <bookmark mark='b'/> So the "
            "chance that X is below mu plus sigma z is exactly the chance that Z is below z. "
            "<bookmark mark='c'/> Which means the quantiles of X are the quantiles of Z, stretched and shifted: a "
            "straight line, whose slope is sigma and whose intercept is mu. <bookmark mark='d'/> So a QQ plot does "
            "three things at once. It tests the shape without needing to know the centre or the spread; and if the "
            "shape is right, the line's intercept and slope estimate them. And the same argument works for any "
            "family that's just one shape shifted and stretched."
        ) as vo:
            self.play(FadeIn(head))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.6)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(tail, shift=UP * 0.2))
        self.clear_scene()

    def quetelet(self):
        d = load("qq")
        zc, xc = np.asarray(d["chest_z"]), np.asarray(d["chest_x"])
        Q = axes([-3.4, 3.4], [32, 49], x_length=7.0, y_length=5.0, xlabel=r"normal quantile",
                 ylabel=r"chest (inches)", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[33, 36, 39, 42, 45, 48],
                 center=[-2.6, 0.1, 0])
        qx = Q.ax
        counts = museum.CHEST_COUNT
        pts = VGroup(*[Dot(qx.c2p(a, b), radius=0.04 + 0.05 * np.sqrt(c / max(counts)), color=S.MUSEUM)
                       for a, b, c in zip(zc, xc, counts)])
        line = Line(qx.c2p(-3.2, d["chest_icept"] - 3.2 * d["chest_slope"]),
                    qx.c2p(3.2, d["chest_icept"] + 3.2 * d["chest_slope"]), color=S.EST, stroke_width=3)
        fit = VGroup(MathTex(rf"\text{{intercept}} = {d['chest_icept']:.2f}", font_size=30, color=S.EST),
                     MathTex(rf"\text{{mean}} = {d['chest_mean']:.2f}", font_size=30, color=GREY_A),
                     MathTex(rf"\text{{slope}} = {d['chest_slope']:.2f}", font_size=30, color=S.EST),
                     MathTex(rf"\text{{SD}} = {d['chest_sd']:.2f}", font_size=30, color=GREY_A))
        fit.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 0.9, 0])
        hc = history_card(1846, r"Adolphe Quetelet, \emph{Lettres \dots\ sur la th\'eorie des probabilit\'es}",
                          rf"the chests of {fmt_int(d['chest_n'])} Scottish militiamen, \ and \emph{{l'homme moyen}}",
                          color=S.MUSEUM, width=5.0, font_size=20).move_to([4.2, -1.8, 0])
        src = historical_tag(r"Edinburgh Medical and Surgical Journal (1817), corrected by Stigler (1986)")
        with self.voiceover(
            "In 1846 Adolphe Quetelet, the Belgian astronomer who became a statistician, published the chest "
            "measurements of Scottish militiamen and argued that they followed the same curve as errors of "
            "astronomical observation. <bookmark mark='a'/> Here is his table, as Stigler corrected it against the "
            f"original 1817 source: {money(d['chest_n'])} men, in sixteen one-inch classes, as a QQ plot. Each class "
            "is one point, sized by how many men it holds. <bookmark mark='b'/> It's very nearly a straight line. "
            f"<bookmark mark='c'/> Its intercept, {d['chest_icept']:.2f} inches, is the mean chest, and its slope, "
            f"{d['chest_slope']:.2f}, is close to the standard deviation, {d['chest_sd']:.2f}. "
            "<bookmark mark='d'/> Quetelet drew a large conclusion: that nature aims at an average man, and that "
            "individuals are errors around him. That idea, l'homme moyen, shaped the next century of statistics, "
            "and some of its worst misuses too. The curve is a fact about these measurements. The meaning he gave "
            "it was a choice."
        ) as vo:
            self.play(FadeIn(Q), FadeIn(src), FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(line))
            vo.wait_until("c")
            self.play(FadeIn(fit[0]), FadeIn(fit[1]))
            self.play(FadeIn(fit[2]), FadeIn(fit[3]))
            vo.wait_until("d")
            self.play(Indicate(hc, color=S.MUSEUM, scale_factor=1.03))
        self.clear_scene()

    def panel(self, name, title, center, ylab, color):
        d = load("qq")
        z, x = np.asarray(d[name + "_z"]), np.asarray(d[name + "_x"])
        med, sc = d[name + "_fit"]
        lo, hi = np.quantile(x, [0.005, 0.995])
        pad = 0.1 * (hi - lo)
        P = axes([-3.2, 3.2], [lo - pad, hi + pad], x_length=3.8, y_length=3.6, xlabel=r"normal quantile",
                 xticks=[-2, 0, 2], center=center)
        ax = P.ax
        keep = (x >= lo - pad) & (x <= hi + pad)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=color) for a, b in zip(z[keep], x[keep])])
        zlo = max(-3.0, (lo - pad - med) / sc)
        zhi = min(3.0, (hi + pad - med) / sc)
        ref = Line(ax.c2p(zlo, med + zlo * sc), ax.c2p(zhi, med + zhi * sc),
                   color=GREY_B, stroke_width=2)
        t = label(title, font_size=26, color=color).next_to(P, UP, buff=0.2)
        y = label(ylab, font_size=20, color=GREY_B).next_to(P, DOWN, buff=0.55)
        omitted = label(rf"{len(x) - int(keep.sum())} extreme points off scale", font_size=17,
                        color=GREY_B).next_to(t, UP, buff=0.08)
        return VGroup(P, ref, dots, t, y, omitted)

    def curvature(self):
        pa = self.panel("men", r"men's heights", [-4.6, -0.2, 0], r"straight: \ a bell", S.EST)
        pb = self.panel("income", r"incomes", [0, -0.2, 0], r"bends up: \ a long right tail", MEDIAN)
        pc = self.panel("t3", r"$t_3$ draws", [4.6, -0.2, 0], r"S-shaped: \ heavy tails on both sides", MODE)
        head = label(r"reading the bends", font_size=34).to_edge(UP, buff=0.4)
        tag = note(r"300 points each: \ the World's men and incomes (simulated); \ $t_3$ computed").to_corner(DR,
                                                                                                         buff=0.3)
        with self.voiceover(
            "When the line bends, the bend tells you how the shape differs. <bookmark mark='a'/> Three hundred of "
            "the World's men: straight. Their heights are close to a bell. <bookmark mark='b'/> Three hundred "
            "incomes: the points bend upward, more and more steeply on the right. The top incomes are far higher "
            "than a bell curve with this centre and spread would ever produce: a long right tail, the skew of the "
            "last chapter, seen without computing a single moment. <bookmark mark='c'/> And three hundred draws from "
            "a distribution with heavy tails on both sides, Student's t with three degrees of freedom: the points "
            "are flat in the middle and bend away at both ends, an S. Extreme values in both directions come more "
            "often than a bell allows. <bookmark mark='d'/> The QQ plot is the statistician's most used diagnostic: "
            "for residuals of a regression in Part 12, for the assumptions of a test in Part 10, for whether a "
            "model's errors behave. It's worth learning to read at a glance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pa[0]), Create(pa[1]), FadeIn(pa[2], lag_ratio=0.005), FadeIn(pa[3:]))
            vo.wait_until("b")
            self.play(FadeIn(pb[0]), Create(pb[1]), FadeIn(pb[2], lag_ratio=0.005), FadeIn(pb[3:]))
            vo.wait_until("c")
            self.play(FadeIn(pc[0]), Create(pc[1]), FadeIn(pc[2], lag_ratio=0.005), FadeIn(pc[3:]))
            vo.wait_until("d")
            self.play(*[Indicate(p[2], color=WHITE, scale_factor=1.03) for p in (pa, pb, pc)])
        self.clear_scene()
