from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

SHAPE_TEXT = {
    "cobb-douglas": (r"Cobb--Douglas", r"$u = x^{a} y^{1-a}$: \ a fixed share of spending on each"),
    "substitutes": (r"perfect substitutes", r"$u = x + y$: \ any fish for any coconut, one for one"),
    "complements": (r"perfect complements", r"$u = \min(x, y)$: \ left shoe, right shoe"),
    "quasilinear": (r"quasilinear", r"$u = 2 \log x + y$: \ coconuts are money"),
}


class Shapes(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The shapes of wanting", r"How easily will someone trade one good for another?",
             "Chapter four. The shapes of wanting.")
        self.convexity()
        self.four()
        self.ces()

    def convexity(self):
        ax = goods_axes(center=LEFT * 2.9 + DOWN * 0.2, top=10, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        cd = cs.Preference("cobb-douglas", a=0.5)
        xs = np.linspace(0.6, 10, 300)
        ic = curve(ax, xs, cd.indifference(4.0, xs), color=IC, top=10)
        p1, p2 = (1.8, 16 / 1.8), (8.0, 2.0)
        d1, d2 = Dot(a.c2p(*p1), radius=0.09), Dot(a.c2p(*p2), radius=0.09)
        mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        chord = DashedLine(a.c2p(*p1), a.c2p(*p2), color=GREY_B, stroke_width=2.5)
        dm = Dot(a.c2p(*mid), radius=0.1, color=PASS)
        slopes = VGroup()
        for x in (1.5, 4.0, 8.0):
            y = 16 / x
            k = y / x                 # MRS = y / x
            dx = 1.1 / np.sqrt(1 + k * k)      # the same length on screen, however steep
            slopes.add(Line(a.c2p(x - dx, y + k * dx), a.c2p(x + dx, y - k * dx), color=E.ACCENT, stroke_width=3))
        rows = VGroup(
            label(r"two bundles equally good: \ 1.8 fish and 8.9 coconuts, \\ or 8 fish and 2 coconuts",
                  font_size=23),
            label(r"their average, \ 4.9 and 5.4, \ is better: \\ averages beat extremes", font_size=23, color=PASS),
            label(r"convex tastes: \ the curve bows toward the origin", font_size=23, color=IC),
            label(r"so the MRS falls along it: \\ the more fish you have, \ the fewer coconuts \\ you'd give for "
                  r"another", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Most people's curves have a particular shape. <bookmark mark='a'/> Here are two bundles this person "
            "likes equally: lots of coconuts and little fish, or the other way round. <bookmark mark='b'/> Their "
            "average, a bit of each, lies above the curve: it's better than either extreme. "
            "<bookmark mark='c'/> Tastes like that are called convex, and their indifference curves bow toward the "
            "origin. <bookmark mark='d'/> Convexity has a meaning you can feel: the more fish you already have, the "
            "fewer coconuts you'd give up for another one. The slope of the curve, the marginal rate of "
            "substitution, falls as you move along it."
        ) as vo:
            self.play(FadeIn(ax), Create(ic))
            vo.wait_until("a")
            self.play(FadeIn(d1, scale=1.5), FadeIn(d2, scale=1.5), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(dm, scale=1.5), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(ic, color=IC), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(s_) for s_ in slopes], lag_ratio=0.3), FadeIn(rows[3]))
        self.clear_scene()

    def four(self):
        sh = load("shapes")
        xs = np.array(sh["xs"])
        panels = VGroup()
        for key in ("cobb-douglas", "substitutes", "complements", "quasilinear"):
            ax = goods_axes(top=12, x_length=2.6, y_length=2.6, font_size=15, xlabel=r"", ylabel=r"",
                            ticks=(0, 6, 12))
            cv = VGroup(*[poly(ax, np.array(c_), color=IC, width=2.5, top=12) for c_ in sh["maps"][key]["curves"]])
            t = VGroup(label(SHAPE_TEXT[key][0], font_size=22, color=E.ACCENT),
                       label(SHAPE_TEXT[key][1], font_size=17, color=GREY_A)).arrange(DOWN, buff=0.08)
            panels.add(VGroup(VGroup(ax, cv), t).arrange(DOWN, buff=0.15))
        panels.arrange_in_grid(rows=1, cols=4, buff=0.35).move_to(DOWN * 0.1)
        if panels.width > 13.4:
            panels.width = 13.4
        with self.voiceover(
            "Four shapes do most of the work in economics. <bookmark mark='a'/> Cobb–Douglas tastes, where a person "
            "always spends the same share of their money on each good, whatever the prices. "
            "<bookmark mark='b'/> Perfect substitutes: straight lines, for goods that are interchangeable at a "
            "fixed rate, like two brands of the same salt. <bookmark mark='c'/> Perfect complements: right angles, "
            "for goods used in fixed proportions, like left and right shoes; an extra left shoe is worth nothing. "
            "<bookmark mark='d'/> And quasilinear tastes, where one good acts like money: every curve is the same "
            "curve shifted up, so a richer person buys no more of the other good. It's the shape behind consumer "
            "surplus, in Part 2."
        ) as vo:
            for mk, p_ in zip("abcd", panels):
                vo.wait_until(mk)
                self.play(FadeIn(p_, shift=UP * 0.15))
        self.clear_scene()

    def ces(self):
        sh = load("shapes")
        sig = list(sh["sigmas"])
        ax = goods_axes(center=LEFT * 2.8 + DOWN * 0.2, top=12, ticks=(0, 4, 8, 12))
        curves = [poly(ax, np.array(sh["ces"][f"{s:g}"]), color=IC, width=4, top=12) for s in sig]
        k1 = sig.index(1.0)
        shown = curves[k1].copy()
        sv = DecimalNumber(1.0, num_decimal_places=2, font_size=40, color=E.ACCENT)
        slab = VGroup(MathTex(r"\sigma =", font_size=40, color=E.ACCENT), sv).arrange(RIGHT, buff=0.15)
        eq = MathTex(r"u = \left(\tfrac12 x^{\rho} + \tfrac12 y^{\rho}\right)^{1/\rho},\quad "
                     r"\sigma = \frac{1}{1-\rho}", font_size=34)
        rows = VGroup(
            eq, slab,
            label(r"$\sigma$, the elasticity of substitution: \\ the percent change in $y/x$ \\ for a one percent "
                  r"change in the MRS", font_size=22, color=GREY_A),
            label(r"$\sigma \to 0$: \ complements; \ $\sigma = 1$: \ Cobb--Douglas; \\ $\sigma \to \infty$: \ "
                  r"substitutes", font_size=23, color=IC),
            label(r"Arrow, Chenery, Minhas and Solow (1961), \\ for production; \ the same curves for tastes",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The first three are members of one family. <bookmark mark='a'/> Its utility has a single parameter, "
            "sigma, the elasticity of substitution: how much the ratio of fish to coconuts a person buys responds "
            "to the rate at which they trade. <bookmark mark='b'/> With sigma near zero, the curves are right "
            "angles: complements. <bookmark mark='c'/> As sigma rises, the corners soften. At exactly one, the "
            "family becomes Cobb–Douglas. <bookmark mark='d'/> And as sigma grows large, the curves flatten into "
            "straight lines: substitutes. <bookmark mark='e'/> Economists call it CES, constant elasticity of "
            "substitution. Kenneth Arrow, Hollis Chenery, Bagicha Minhas and Robert Solow introduced it in 1961 for "
            "machines and workers. One number to say how replaceable one thing is by another: it will return for "
            "trade, for capital and labour, and for robots."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rows[0]), Create(shown))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(Transform(shown, curves[0]), sv.animate.set_value(sig[0]), run_time=1.5)
            vo.wait_until("c")
            for k in range(1, k1 + 1):
                self.play(Transform(shown, curves[k]), sv.animate.set_value(sig[k]), run_time=1.2)
            vo.wait_until("d")
            for k in range(k1 + 1, len(sig)):
                self.play(Transform(shown, curves[k]), sv.animate.set_value(sig[k]), run_time=1.2)
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
