from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

LOW = "#F25F5C"
HIGH = "#7FD1B9"


class Continuous(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Continuous time", r"Why is the same household faster to solve in continuous time?",
             "Chapter ten. Continuous time.", lit={2022: r"Achdou et al."}, scale=("household", "nation"),
             horizon=("a lifetime",))
        self.equation()
        self.upwind()
        self.results()

    def equation(self):
        H = TRUTH["hjb"]
        eq = MathTex(r"\rho\, v_j(a) = \max_c\; u(c) + v_j'(a)\,\big(z_j + r a - c\big) + "
                     r"\lambda_j\big(v_{-j}(a) - v_j(a)\big)", font_size=38, color=HJB).move_to(UP * 1.8)
        rows = VGroup(
            label(rf"two incomes, \ $z = {H['z'][0]}$ or ${H['z'][1]}$, \ switching at rate {H['lam'][0]} a year; \ "
                  rf"$r = {H['r']}$, \ $\rho = {H['rho']}$; \ borrowing down to ${H['a_min']}$".replace("-", "{-}"),
                  font_size=20, color=GREY_A),
            label(r"the Hamilton--Jacobi--Bellman equation: \ Bellman's equation for an instant", font_size=22,
                  color=WHITE),
            label(r"the first-order condition is simply $u'(c) = v_j'(a)$: \ no maximization step at all",
                  font_size=22, color=HJB),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Achdou, Han, Lasry, Lions and Moll, \ REStud (2022)", corner=DR, font_size=12)
        with self.voiceover(
            "Now let time run continuously. <bookmark mark='a'/> A household earns one of two incomes, switching "
            "between them at random, and saves or borrows at a fixed rate, down to a limit. <bookmark mark='b'/> "
            "Its Bellman equation becomes the Hamilton-Jacobi-Bellman equation: the return on being in a state "
            "equals the flow of utility, plus the value of the wealth it is accumulating, plus the expected gain "
            "from a switch of income. <bookmark mark='c'/> Because time is continuous, the best consumption "
            "satisfies a plain first-order condition, marginal utility equals the slope of the value function, "
            "with no search. Yves Achdou, Jiequn Han, Jean-Michel Lasry, Pierre-Louis Lions and Benjamin Moll "
            "showed in 2022 how fast this can be solved."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def upwind(self):
        C = load("hjb")
        line = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_D, stroke_width=1.5).shift(UP * 1.6)
        pts = VGroup(*[Dot([-5 + i, 1.6, 0], radius=0.07, color=GRID) for i in range(11)])
        arrows = VGroup()
        for i in range(11):
            right = i < 6
            a0 = np.array([-5 + i, 2.0, 0])
            arrows.add(Arrow(a0, a0 + (RIGHT if right else LEFT) * 0.55, buff=0, color=HIGH if right else LOW,
                             stroke_width=3, max_tip_length_to_length_ratio=0.35))
        cap = VGroup(
            label(r"saving: \ difference forward", font_size=18, color=HIGH),
            label(r"dissaving: \ difference backward", font_size=18, color=LOW),
        ).arrange(RIGHT, buff=1.4).next_to(line, DOWN, buff=0.4)
        n = 12
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                blk_i, blk_j = i // 6, j // 6
                on = (abs(i - j) <= 1 and blk_i == blk_j) or (abs(i - j) == 6)
                sq = Square(side_length=0.2, stroke_width=0.5, stroke_color=GREY_D,
                            fill_color=HJB if on else BLACK, fill_opacity=0.85 if on else 0.0)
                sq.move_to([j * 0.21, -i * 0.21, 0])
                cells.add(sq)
        cells.move_to(LEFT * 3.2 + DOWN * 1.9)
        side = VGroup(
            label(r"each step: \ one sparse \\ linear system", font_size=19, color=WHITE),
            label(rf"{C['size']:,} unknowns: \\ {C['nnz']:,} non-zeros of \\ "
                  rf"{C['size'] ** 2 / 1e6:.0f} million entries".replace(",", "{,}"), font_size=19, color=HJB),
            label(rf"{C['iters']} steps, \ {1000 * C['seconds']:.0f} ms", font_size=21, color=EGM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.6 + DOWN * 1.9)
        with self.voiceover(
            "How is it solved? On a grid of wealth, the slope of the value function is a difference between "
            "neighbouring points. <bookmark mark='a'/> The trick is to take the difference in the direction the "
            "household is moving: forward where it saves, backward where it runs its wealth down. This upwind "
            "rule is what keeps the method stable. <bookmark mark='b'/> Then each step solves one linear system "
            "for the whole value function at once, an implicit step that can be as large as you like. <bookmark "
            f"mark='c'/> The system has {C['size']:,} unknowns, but each grid point talks only to its two "
            "neighbours and to the same wealth in the other income state, so of a million entries only about "
            f"three thousand are not zero. <bookmark mark='d'/> {C['iters']} steps, a few hundredths of a second."
        ) as vo:
            self.play(Create(line), FadeIn(pts))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.1), FadeIn(cap), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(cells), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def results(self):
        C = load("hjb")
        a = np.array(C["a"])
        s = np.array(C["s"])
        g = np.array(C["g"])
        top = 0.6
        keep = a <= top
        ax1 = plane([a[0], top], [-0.1, 0.08], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.2, y_length=4.2,
                    xticks=[-0.15, 0, 0.2, 0.4, 0.6], yticks=[-0.1, -0.05, 0, 0.05], xlabel=r"wealth",
                    ylabel=r"saving, \ a year", xfmt=lambda v: f"{v:.2f}".replace("-", "{-}"),
                    yfmt=lambda v: f"{v:.2f}".replace("-", "{-}"), font_size=13)
        zero = DashedLine(ax1.ax.c2p(a[0], 0), ax1.ax.c2p(top, 0), color=GREY_B, stroke_width=1.4)
        s_lo = path(ax1, a[keep], s[keep, 0], LOW, 2.6, yr=(-0.1, 0.08))
        s_hi = path(ax1, a[keep], s[keep, 1], HIGH, 2.6, yr=(-0.1, 0.08))
        gmax = float(np.max(g[keep][1:]))
        ax2 = plane([a[0], top], [0, gmax * 1.15], center=RIGHT * 3.1 + DOWN * 0.3, x_length=5.2, y_length=4.2,
                    xticks=[-0.15, 0, 0.2, 0.4, 0.6], yticks=[0], xlabel=r"wealth", ylabel=r"how many have it",
                    xfmt=lambda v: f"{v:.2f}".replace("-", "{-}"), yfmt=lambda v: "", font_size=13)
        g_lo = path(ax2, a[keep][1:], g[keep][1:, 0], LOW, 2.4, yr=(0, gmax * 1.15))
        g_hi = path(ax2, a[keep][1:], g[keep][1:, 1], HIGH, 2.4, yr=(0, gmax * 1.15))
        spike = Line(ax2.ax.c2p(a[0], 0), ax2.ax.c2p(a[0], gmax * 1.1), color=LOW, stroke_width=5)
        sl = label(rf"{100 * C['at_limit']:.1f}\% \\ at the limit", font_size=15, color=LOW).next_to(
            ax2.ax.c2p(a[0], gmax * 1.1), RIGHT, buff=0.12)
        key = VGroup(label(r"red: \ low income", font_size=16, color=LOW),
                     label(r"green: \ high income", font_size=16, color=HIGH)).arrange(RIGHT, buff=0.6).to_edge(
            UP, buff=0.5)
        foot = label(r"the distribution comes from the same matrix, \ transposed: \ $A^{\top} g = 0$", font_size=20,
                     color=HJB).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The results. <bookmark mark='a'/> Saving: with low income the household runs its wealth down, faster "
            "the more it has, until it reaches the borrowing limit and stops there; with high income it saves, "
            "less as it grows richer. <bookmark mark='b'/> And the distribution of wealth across many such "
            "households, which in discrete time needs a separate simulation. Here it comes from the same sparse "
            "matrix, transposed: the Kolmogorov forward equation. <bookmark mark='c'/> "
            f"{100 * C['at_limit']:.1f} percent of households sit exactly at the borrowing limit, low earners who "
            "have run out. That spike is a feature of the economics, and the method captures it exactly."
        ) as vo:
            self.play(FadeIn(key), FadeIn(ax1), Create(zero))
            vo.wait_until("a")
            self.play(Create(s_lo), Create(s_hi), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(ax2), Create(g_lo), Create(g_hi), FadeIn(foot), run_time=1.8)
            vo.wait_until("c")
            self.play(GrowFromEdge(spike, DOWN), FadeIn(sl))
        self.clear_scene()
