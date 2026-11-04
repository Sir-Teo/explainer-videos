from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403

SHAPES = [("line", r"line"), ("parabola", r"parabola"), ("circle", r"circle"), ("cross", r"cross"), ("step", r"step"),
          ("noise", r"noise")]


class Measures(VoiceoverScene):
    def construct(self):
        self.card()
        self.gallery()
        self.ranks()
        self.monotone()
        self.dcor_mi()

    def card(self):
        card = chapter_card(13, r"Measuring dependence", r"One number for a relationship: \ which one?", lit=(), part=PART)
        with self.voiceover("Chapter thirteen. Measuring dependence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def gallery(self):
        d = load("measures")
        panels = VGroup()
        for k, (key, nm) in enumerate(SHAPES):
            c = d[key]
            x, y = np.asarray(c["x"]), np.asarray(c["y"])
            col, row = k % 3, k // 3
            xr = [x.min() - 0.1, x.max() + 0.1]
            yr = [y.min() - 0.1, y.max() + 0.1]
            A = axes(xr, yr, x_length=2.6, y_length=1.7, center=[-4.6 + 3.0 * col, 1.6 - 3.0 * row, 0])
            A.ax.x_axis.set_opacity(0.3)
            A.ax.y_axis.set_opacity(0.3)
            pts = scatter(A.ax, x[:300], y[:300], color=SIM, radius=0.014, opacity=0.6, xr=xr, yr=yr)
            t = label(nm, font_size=20, color=GREY_A).next_to(A, UP, buff=0.05)
            vals = VGroup(*[MathTex(rf"{lab} {c[k2]:.2f}", font_size=16, color=cl) for lab, k2, cl in
                            ((r"r", "pearson", S.EST), (r"\rho_S", "spearman", S.LIK), (r"\tau", "kendall", S.ACCENT),
                             (r"\mathrm{dCor}", "dcor", S.POST), (r"\mathrm{MI}", "mi", S.PRIOR))])
            vals = VGroup(VGroup(*vals[:3]).arrange(RIGHT, buff=0.18), VGroup(*vals[3:]).arrange(RIGHT, buff=0.18))
            vals.arrange(DOWN, buff=0.06)
            vals.width = min(vals.width, 2.7)
            vals.next_to(A, DOWN, buff=0.08)
            panels.add(VGroup(A, pts, t, vals))
        side = VGroup(*[label(t, font_size=18, color=c) for t, c in ((r"$r$: Pearson", S.EST), (r"$\rho_S$: Spearman", S.LIK),
                                                                      (r"$\tau$: Kendall", S.ACCENT), (r"dCor: distance", S.POST),
                                                                      (r"MI: mutual information", S.PRIOR))])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.6, 0.0, 0])
        tag = note(r"simulated: 500 points each").to_corner(DR, buff=0.25)
        with self.voiceover(
            "If correlation misses so much, what should we use instead? <bookmark mark='a'/> Six shapes, five "
            "measures of dependence each. <bookmark mark='b'/> On the noisy line, they all agree there's strong "
            "dependence. <bookmark mark='c'/> On the parabola, the circle and the cross, Pearson's r and the two rank "
            "correlations are all near zero: they measure monotone trends, and these shapes have none. But distance "
            "correlation and mutual information are well above zero. <bookmark mark='d'/> On pure noise, everything is "
            "near zero, apart from a small positive bias in the estimated mutual information. No single number "
            "captures a relationship, but some are blind to more than others."
        ) as vo:
            self.play(FadeIn(side), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(p[0], p[1], p[2])) for p in panels], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(panels[0][3]), FadeIn(panels[4][3]))
            vo.wait_until("c")
            self.play(*[FadeIn(panels[k][3]) for k in (1, 2, 3)])
            vo.wait_until("d")
            self.play(FadeIn(panels[5][3]))
        self.clear_scene()

    def ranks(self):
        rows = [
            cmath(r"\rho_S", r"=", r"\operatorname{corr}\big(\operatorname{rank}(X),\ \operatorname{rank}(Y)\big)", font_size=34),
            cmath(r"\tau", r"=", r"P(\text{concordant}) - P(\text{discordant})", font_size=34),
        ]
        whys = [why(r"Spearman (1904): \ Pearson on the ranks"), why(r"Kendall (1938): \ pairs that agree in order, \ minus pairs that don't")]
        props = label(r"both depend only on the copula: \ unchanged by any increasing transformation, \ robust to outliers",
                      font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The rank correlations deserve a closer look. <bookmark mark='a'/> Charles Spearman's, from 1904, is "
            "Pearson's correlation computed on the ranks instead of the values. <bookmark mark='b'/> Maurice "
            "Kendall's, from 1938, counts pairs of points: the fraction that are in the same order on both variables, "
            "minus the fraction in opposite orders. <bookmark mark='c'/> Both depend only on ranks, so they're "
            "properties of the copula: unchanged by taking logarithms or any other increasing transformation, and "
            "hardly moved by an outlier. Part 16 uses them to build tests that need no distributional assumptions."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.0, x=-0.8, buff=0.8, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(props))
        self.clear_scene()

    def dcor_mi(self):
        rows = [
            cmath(r"\mathrm{dCov}^2(X, Y)", r"=", r"\| \varphi_{X,Y}(s, t) - \varphi_X(s)\,\varphi_Y(t) \|^2_w", font_size=32),
            cmath(r"\mathrm{dCor}(X, Y) = 0", r"\iff", r"X \text{ and } Y \text{ independent}", font_size=34),
            cmath(r"I(X; Y)", r"=", r"\iint f(x, y) \log\frac{f(x, y)}{f_X(x) f_Y(y)}\, dx\, dy", r"\ge", r"0", font_size=32),
        ]
        rows[1][2].set_color(S.POST)
        rows[2][0].set_color(S.PRIOR)
        whys = [why(r"distance between the joint characteristic function and the product of the marginal ones"),
                why(r"Sz\'ekely, Rizzo \& Bakirov (2007): \ unlike $r$"),
                why(r"mutual information: \ Shannon; \ zero iff independent")]
        cost = label(r"the price: \ less interpretable, \ noisier in small samples, \ and MI must be estimated (Part 29)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The other two measures see any kind of dependence. <bookmark mark='a'/> Distance correlation, introduced "
            "by Gábor Székely, Maria Rizzo and Nail Bakirov in 2007, measures how far the joint characteristic "
            "function is from the product of the marginal ones, Part 3's characteristic functions put to work. "
            "<bookmark mark='b'/> Its great property: it's zero only when the variables are independent, which "
            "correlation can't claim. <bookmark mark='c'/> Mutual information, from Claude Shannon's information "
            "theory, measures how far the joint density is from the product of its marginals, and it too is zero "
            "only under independence. <bookmark mark='d'/> The price is interpretability, noise in small samples, "
            "and, for mutual information, the need to estimate densities first, which Part 29 teaches."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.8, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.clear_scene()

    def monotone(self):
        e = load("extras")["mono"]
        rows = VGroup(
            label(r"800 of the World's fathers and sons; \ then replace the son's height by $e^{(\text{height} - 170)/6}$", font_size=24,
                  color=GREY_A),
            MathTex(rf"\text{{Pearson: }} {e['p_raw']:.3f} \to {e['p_exp']:.3f}", font_size=32, color=S.EST),
            MathTex(rf"\text{{Spearman: }} {e['s_raw']:.3f} \to {e['s_exp']:.3f}", font_size=32, color=S.LIK),
            MathTex(rf"\text{{Kendall: }} {e['k_raw']:.3f} \to {e['k_exp']:.3f}", font_size=32, color=S.ACCENT),
            label(r"an increasing transformation keeps the order, \ so the ranks, \ so the copula", font_size=26, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.3, 0])
        tag = simulated_tag()
        with self.voiceover(
            "Here's that invariance, measured. <bookmark mark='a'/> Take eight hundred of the World's fathers and "
            "sons, and then distort the son's height through an exponential: same order, different scale. "
            f"<bookmark mark='b'/> Pearson's correlation drops from {e['p_raw']:.2f} to {e['p_exp']:.2f}. "
            "<bookmark mark='c'/> Spearman's and Kendall's don't move at all, to the last digit. "
            "<bookmark mark='d'/> An increasing transformation preserves order, so it preserves ranks and the copula, "
            "and rank correlations measure only that."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
