from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Dependence(VoiceoverScene):
    def construct(self):
        self.card()
        self.gallery()
        self.covariance()
        self.diversify()
        self.pairwise()

    def card(self):
        card = chapter_card(2, r"Dependence", r"Uncorrelated is not independent", lit=(), part=PART)
        with self.voiceover("Chapter two. Dependence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def gallery(self):
        d = load("dependence")
        specs = [("x", "y", r"$Y = X^2 + \text{noise}$", d["r_par"], [-3, 3], [-0.5, 9]),
                 ("cx", "cy", r"a ring", d["r_ring"], [-1.4, 1.4], [-1.4, 1.4]),
                 ("x", "z", r"$Y = S X$, \ $S = \pm 1$", d["r_sign"], [-3.2, 3.2], [-3.2, 3.2])]
        panels = VGroup()
        for k, (a, b, ttl, r, xr, yr) in enumerate(specs):
            A = axes(xr, yr, x_length=3.6, y_length=3.0, center=[-4.4 + 4.4 * k, 0.2, 0])
            A.ax.x_axis.set_opacity(0.4)
            A.ax.y_axis.set_opacity(0.4)
            pts = scatter(A.ax, d[a], d[b], color=SIM, radius=0.02, opacity=0.6)
            t = label(ttl, font_size=24).next_to(A, UP, buff=0.2)
            rr = MathTex(rf"r = {r:.3f}", font_size=30, color=S.ACCENT).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, pts, t, rr))
        sign = label(rf"knowing $|X| > 1.5$ makes $|Y| > 1.5$ certain: \ {100 * d['p_big']:.0f}\% $\to$ "
                     rf"{100 * d['p_big_given']:.0f}\%", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        intro = label('Dependence beyond a straight line', font_size=36)
        with self.voiceover(
            "Correlation measures one kind of dependence: how well a straight line fits. <bookmark mark='a'/> Here y "
            "is x squared, plus independent noise: its mean is determined by x. The population correlation is zero, because "
            "the parabola's two arms cancel. <bookmark mark='b'/> A noisy ring: knowing x restricts y to two narrow bands, yet the population "
            "correlation is zero. <bookmark mark='c'/> And here y is x times a random sign. With an independent fair sign, each variable is "
            "standard normal, the correlation is zero, but the size of y is exactly the size of x: if x is beyond "
            "one and a half, so is y, every time. <bookmark mark='d'/> For finite, positive variances, independence implies zero correlation. Zero "
            "correlation implies nothing of the kind."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(panels[k][0]), FadeIn(panels[k][2]), FadeIn(panels[k][1], lag_ratio=0.002),
                          FadeIn(panels[k][3]))
            self.play(FadeIn(sign), FadeIn(note(r"simulated: 1,200 of 2,000 draws; summaries use all 2,000").to_edge(UP, buff=0.3)))
            vo.wait_until("d")
            self.play(*[Indicate(p[3], color=S.RESID) for p in panels])
        self.clear_scene()

    def covariance(self):
        rows = [
            cmath(r"\mathrm{Cov}(X, Y)", r"=", r"E[(X - EX)(Y - EY)]", r"=", r"E[XY] - EX\, EY", font_size=34),
            cmath(r"\Sigma", r"=", r"\mathrm{Cov}(\mathbf X)", r"=", r"E[(\mathbf X - \boldsymbol\mu)(\mathbf X - \boldsymbol\mu)^\top]",
                  font_size=34),
            cmath(r"\mathbf u^\top \Sigma\, \mathbf u", r"=", r"\mathrm{Var}(\mathbf u^\top \mathbf X)", r"\ge", r"0", font_size=36),
            cmath(r"|\mathrm{Cov}(X, Y)|", r"\le", r"\sigma_X\,\sigma_Y", font_size=36),
        ]
        rows[2][0].set_color(S.ACCENT)
        whys = [why(r"the expected product of deviations"), why(r"all the pairs, \ as a matrix"),
                why(r"PSD: \ Part 4, chapter 5"), why(r"Cauchy--Schwarz in $L^2$: \ $|\rho| \le 1$")]
        lp = label(r"random variables with finite variance form an inner-product space, \ $L^2$: \ $\langle X, Y\rangle = E[XY]$",
                   font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        intro = label('Covariance and finite second moments', font_size=36)
        with self.voiceover(
            "Covariance is what correlation is built from. <bookmark mark='a'/> The expected product of the two "
            "deviations from the means, or the mean of the product minus the product of the means. "
            "<bookmark mark='b'/> For a vector of variables, all the covariances form a matrix, <bookmark mark='c'/> "
            "and it's positive semidefinite, by Part 4's argument: every linear combination has a variance, and "
            "variances aren't negative. <bookmark mark='d'/> And covariance is bounded by the product of the "
            "standard deviations: Cauchy–Schwarz again. <bookmark mark='e'/> That's not a coincidence. Random "
            "variables with finite variance form an inner-product space, with the expected product as the inner "
            "product. Covariance is an inner product, correlation a cosine, and in the next chapter conditional "
            "expectation will be a projection."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.6, buff=0.5, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(lp))
        self.clear_scene()

    def diversify(self):
        e = load("extras")
        ns = np.asarray(e["div_ns"])
        A = axes([0, 50], [0, 1.05], x_length=7.2, y_length=4.2, xlabel=r"number of variables averaged, $n$",
                 ylabel=r"$\mathrm{Var}(\bar X) / \sigma^2$", xticks=[1, 10, 20, 30, 40, 50], yticks=[0, 0.2, 0.5, 1],
                 center=[-2.4, -0.5, 0])
        ax = A.ax
        cols = {"0.0": S.LIK, "0.2": S.ACCENT, "0.5": S.RESID}
        cvs = VGroup(*[curve(ax, ns, np.asarray(e[f"div_{k}"]), c, 3) for k, c in cols.items()])
        floors = VGroup(*[DashedLine(ax.c2p(0, float(k)), ax.c2p(50, float(k)), color=c, stroke_width=1.5) for k, c in cols.items()
                          if float(k) > 0])
        leg = legend([(c, rf"$\rho = {k}$") for k, c in cols.items()], font_size=22).move_to([4.6, 2.0, 0])
        f = MathTex(r"\mathrm{Var}(\bar X)", r"=", r"\frac{\sigma^2}{n}\big(1 + (n - 1)\rho\big)", r"\ \to\ ", r"\rho\,\sigma^2",
                    font_size=32)
        f.width = min(f.width, 5.2)
        f.move_to([4.15, 0.6, 0])
        f[4].set_color(S.RESID)
        why_ = label(r"$\mathrm{Var}(\sum X_i) = \sum_i \mathrm{Var} X_i + \sum_{i \ne j}\mathrm{Cov}(X_i, X_j)$", font_size=22,
                     color=GREY_B).next_to(f, DOWN, buff=0.25)
        why_.width = min(why_.width, 5.2)
        take = label(r"averaging kills independent noise, \ but not shared noise", font_size=26, color=S.ACCENT)
        take.width = min(take.width, 5.0)
        take.move_to([4.1, -1.6, 0])
        with self.voiceover(
            "Correlation matters most when we average. <bookmark mark='a'/> The variance of a sum is the sum of the "
            "variances plus all the covariances. For n variables with equal variance and equal correlation rho, the "
            "variance of their average is sigma squared over n, times one plus n minus one times rho. "
            "<bookmark mark='b'/> With no correlation it falls like one over n, the sigma over root n of Part 1. "
            "<bookmark mark='c'/> With correlation it doesn't fall to zero; it levels off at rho sigma squared. "
            "<bookmark mark='d'/> Averaging kills independent noise but not shared noise. That's why diversifying "
            "across correlated stocks has limits, and why a hundred measurements made with the same biased "
            "instrument are worth little more than one."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(why_))
            vo.wait_until("b")
            self.play(Create(cvs[0]), FadeIn(leg))
            vo.wait_until("c")
            self.play(Create(cvs[1]), Create(cvs[2]), Create(floors))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def pairwise(self):
        hdr = [r"X", r"Y", r"Z = X \oplus Y"]
        data = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
        tab = VGroup()
        for j, h in enumerate(hdr):
            tab.add(MathTex(h, font_size=30, color=S.ACCENT).move_to([(-6.0, -4.9, -3.5)[j], 2.0, 0]))
        for i, r in enumerate(data):
            for j, v in enumerate(r):
                tab.add(MathTex(str(v), font_size=32).move_to([(-6.0, -4.9, -3.5)[j], 1.2 - 0.7 * i, 0]))
        pr = VGroup(*[MathTex(r"\tfrac14", font_size=28, color=GREY_B).move_to([-2.1, 1.2 - 0.7 * i, 0]) for i in range(4)])
        pr.add(MathTex(r"P", font_size=30, color=GREY_B).move_to([-2.1, 2.0, 0]))
        rule = Line([-6.5, 1.65, 0], [-1.7, 1.65, 0], color=GREY_D)
        rows = VGroup(
            MathTex(r"P(X = x, Z = z) = \tfrac14 = P(X = x)\,P(Z = z)", font_size=28),
            label(r"so each pair is independent \ ($X, Y$; \ $X, Z$; \ $Y, Z$)", font_size=24, color=COND),
            MathTex(r"\text{but } P(X = 1, Y = 1, Z = 1) = 0 \ne \tfrac18", font_size=28, color=S.RESID),
            label(r"any two determine the third: \ pairwise independent, \ not mutually", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for r in rows:
            if r.width > 6.2:
                r.width = 6.2
        rows.move_to([3.4, 0.6, 0])
        hc = note(r"S. N. Bernstein's example, \ 1920s").to_corner(UR, buff=0.3)
        use = label(r"why mutual independence is assumed of samples, \ and why checking pairs is not enough", font_size=22,
                    color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Independence has one more subtlety once there are three variables. <bookmark mark='a'/> Flip two fair "
            "coins, X and Y, and let Z be one when they differ and zero when they agree: the exclusive or. Four "
            "equally likely rows. <bookmark mark='b'/> Look at any two of the three. X and Z: each of the four "
            "combinations has probability a quarter, the product of the marginals. So every pair is independent. "
            "<bookmark mark='c'/> But all three together are not: X and Y both one forces Z to be zero, so the "
            "triple of ones has probability zero, not an eighth. <bookmark mark='d'/> Any two determine the third. "
            "This is Sergei Bernstein's example: pairwise independence does not imply mutual independence, which is "
            "why mutual independence is what we assume of a sample, and why checking pairs is never enough."
        ) as vo:
            self.play(FadeIn(tab[:3]), Create(rule), FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in tab[3:]], lag_ratio=0.06), FadeIn(pr))
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(use))
        self.clear_scene()
