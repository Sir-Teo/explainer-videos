from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Projection(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Projection: \ the rule as a polynomial", r"Can a whole policy be a dozen numbers?",
             "Chapter six. Projection: the rule as a polynomial.", lit={1992: r"Judd"}, scale=("nation",),
             horizon=("a century",))
        self.idea()
        self.residual()
        self.degrees()

    def idea(self):
        eqs = VGroup(
            MathTex(r"c(k) \;\approx\; \hat c(k;\theta) = \sum_{j=0}^{n-1} \theta_j\, T_j\!\big(x(k)\big)",
                    font_size=40, color=PROJ),
            MathTex(r"R(k;\theta) = u'\big(\hat c(k)\big) - \beta\, u'\big(\hat c(k')\big)\, f'(k')", font_size=38,
                    color=THEORY),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.5)
        rows = VGroup(
            label(r"$T_j$: \ Chebyshev polynomials; \ $\theta$: \ the unknowns", font_size=21, color=GREY_A),
            label(r"collocation: \ $R = 0$ at the $n$ Chebyshev nodes", font_size=22, color=PROJ),
            label(r"Galerkin: \ $R$ orthogonal to each $T_j$ \ (zero on average, \ weighted)", font_size=22,
                  color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eqs, DOWN, buff=0.6)
        tag = published_tag(r"Judd, \ JET (1992)", corner=DR, font_size=12)
        with self.voiceover(
            "A different idea, from Kenneth Judd in 1992: stop storing the rule at grid points, and write it as a "
            "formula. <bookmark mark='a'/> Approximate consumption by a sum of Chebyshev polynomials with unknown "
            "coefficients theta. <bookmark mark='b'/> For any theta, the Euler equation leaves a residual: how far "
            "marginal utility today is from its discounted value tomorrow. <bookmark mark='c'/> Choose the n "
            "coefficients so that the residual is exactly zero at n points, Chebyshev's nodes: that is "
            "collocation, n equations in n unknowns, solved by Newton's method. <bookmark mark='d'/> Or make the "
            "residual zero on average against each polynomial: that is Galerkin's method. Either way, the whole "
            "policy becomes a handful of numbers."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Write(eqs[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def residual(self):
        P = load("projection")
        r = np.array(P["resid"])
        scale = np.max(np.abs(r))
        ax = plane([0.5, 1.5], [-1.2, 1.2], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.4,
                   xticks=[0.5, 0.75, 1.0, 1.25, 1.5], yticks=[-1, 0, 1], xlabel=r"capital, \ share of steady state",
                   ylabel=r"Euler residual \ (scaled to its largest)", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        zero = DashedLine(ax.ax.c2p(0.5, 0), ax.ax.c2p(1.5, 0), color=GREY_B, stroke_width=1.6)
        curve = path(ax, P["resid_k"], r / scale, PROJ, 3.0)
        nodes = VGroup(*[dot(ax, x, 0, WHITE, 0.09) for x in P["nodes"]])
        side = VGroup(
            label(r"degree 3: \ four \\ coefficients", font_size=19, color=PROJ),
            label(r"white: \ the four \\ Chebyshev nodes, \\ where the residual \\ is set to zero", font_size=18,
                  color=WHITE),
            label(rf"largest residual: \\ ${scale / 10 ** np.floor(np.log10(scale)):.1f} \times "
                  rf"10^{{{int(np.floor(np.log10(scale)))}}}$", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is the residual of a polynomial of degree three, four coefficients, across the range of capital. "
            "<bookmark mark='a'/> It wiggles, as it must, because a cubic cannot be exactly the true rule. "
            "<bookmark mark='b'/> But it passes through zero at the four nodes where collocation forced it to, and "
            "between them it stays small. <bookmark mark='c'/> Chebyshev's nodes are spread so that those "
            "wiggles are about as even, and as small, as any placement can make them."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_, scale=1.5) for n_ in nodes], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(nodes, color=PROJ, scale_factor=1.4))
        self.clear_scene()

    def degrees(self):
        P = load("projection")
        rows = P["rows"]
        ax = plane([0, 11], [-9, 0], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.6,
                   xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], yticks=[-8, -6, -4, -2, 0],
                   xlabel=r"degree of the polynomial", ylabel=r"worst Euler error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for r in rows:
            p0, p1 = ax.ax.c2p(r["degree"] - 0.35, r["ee"]), ax.ax.c2p(r["degree"] + 0.35, 0)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=PROJ,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        gal = dot(ax, 4, P["galerkin5"], VALUE, 0.1)
        slope = (rows[-1]["ee"] - rows[0]["ee"]) / (rows[-1]["degree"] - rows[0]["degree"])
        side = VGroup(
            label(rf"each extra degree: \\ about {10 ** (-slope):.0f} times \\ more accurate", font_size=19,
                  color=PROJ),
            label(r"purple: \ Galerkin, \\ degree 4", font_size=18, color=VALUE),
            label(rf"degree 8: \ one dollar \\ in {10 ** (-rows[7]['ee']) / 1e6:.0f} million, \\ in "
                  rf"{1000 * rows[7]['seconds']:.0f} milliseconds", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "And as the degree rises? <bookmark mark='a'/> The worst Euler error falls steadily, from about one "
            "dollar in two hundred and fifty with a straight line, <bookmark mark='b'/> to one in "
            f"{10 ** (-rows[7]['ee']) / 1e6:.0f} million at degree eight, each extra degree making the rule about "
            f"{10 ** (-slope):.0f} times more accurate. This is what mathematicians call spectral convergence, and "
            "it is the reward for a smooth problem. <bookmark mark='c'/> Galerkin's method, at degree four, lands "
            "in the same place as collocation. <bookmark mark='d'/> And the whole computation takes a few "
            "thousandths of a second. Projection's weakness is the other side of the same coin: a kink, such as a "
            "borrowing limit, ruins a single smooth polynomial, which is why the household used a grid."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in bars[:4]], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in bars[4:]], lag_ratio=0.3), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(gal, scale=1.5), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()
