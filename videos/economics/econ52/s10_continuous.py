from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Continuous(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Continuous time: \ two equations, \ one matrix", r"Why is the distribution so cheap to find?",
             "Chapter eight. Continuous time: two equations, one matrix.",
             lit={2022: r"Achdou, Han, Lasry, Lions, Moll"}, scale=("household", "market"), horizon=("a lifetime",))
        self.equations()
        self.matrix()
        self.solved()

    def equations(self):
        hjb = MathTex(r"\rho\, v_j(a) = \max_c\ u(c) + v_j'(a)\,(z_j + r a - c) + \lambda_j\,(v_{-j}(a) - v_j(a))",
                      font_size=36, color=THEORY)
        kfe = MathTex(r"0 = -\frac{d}{da}\big[s_j(a)\, g_j(a)\big] - \lambda_j\, g_j(a) + \lambda_{-j}\, g_{-j}(a)",
                      font_size=36, color=DIST)
        l1 = label(r"Hamilton--Jacobi--Bellman: \ each household's choice, \ looking forward", font_size=20,
                   color=THEORY)
        l2 = label(r"Kolmogorov forward: \ where the households are, \ looking at how they move", font_size=20,
                   color=DIST)
        g = VGroup(l1, hjb, l2, kfe).arrange(DOWN, buff=0.3).move_to(UP * 0.6)
        g[2].shift(DOWN * 0.3)
        g[3].shift(DOWN * 0.3)
        foot = label(r"$s_j(a) = z_j + ra - c_j(a)$: \ the drift of wealth, \ the same in both", font_size=21,
                     color=WHITE).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"Achdou, \ Han, \ Lasry, \ Lions and Moll, \ REStud 89(1) (2022)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "In continuous time, the same economy becomes two equations, as Part fifty-one began to show. "
            "<bookmark mark='a'/> The first is the Hamilton-Jacobi-Bellman equation: the value of holding wealth a "
            "with income state j equals the best flow of utility plus how fast that value changes as wealth "
            "drifts, plus the chance of switching income. <bookmark mark='b'/> The second is the Kolmogorov "
            "forward equation for the density of households: in a steady state, the flow of households out of each "
            "small interval of wealth, as their wealth drifts and their income switches, is balanced by the flow "
            "in. <bookmark mark='c'/> Both are written with the same drift: income plus interest minus consumption. "
            "Yves Achdou, Jiequn Han, Jean-Michel Lasry, Pierre-Louis Lions and Benjamin Moll showed how much that "
            "shared piece buys."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(l1))
            vo.wait_until("a")
            self.play(Write(hjb), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(l2), Write(kfe), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def matrix(self):
        C = load("continuous")
        n = 24
        size = 4.4
        cell = size / (2 * n)
        grid = VGroup()
        for i in range(2 * n):
            for j in range(2 * n):
                same = (i // n) == (j // n)
                on = (same and abs(i - j) <= 1) or (not same and abs(i - j) == n)
                if on:
                    col = THEORY if same else INDIRECT
                    grid.add(Square(side_length=cell * 0.92, stroke_width=0, fill_color=col,
                                    fill_opacity=0.9).move_to([(j - n + 0.5) * cell, (n - i - 0.5) * cell, 0]))
        frame = Square(side_length=size, stroke_color=GREY_B, stroke_width=1.5)
        mat = VGroup(frame, grid).move_to(LEFT * 3.2 + DOWN * 0.3)
        ttl = MathTex(r"\mathbf{A}", font_size=40, color=THEORY).next_to(mat, UP, buff=0.2)
        rhs = VGroup(
            MathTex(r"\rho\,\mathbf{v} = \mathbf{u}(\mathbf{v}) + \mathbf{A}\,\mathbf{v}", font_size=38,
                    color=THEORY),
            MathTex(r"\mathbf{A}^{\!\top} \mathbf{g} = 0", font_size=42, color=DIST),
        ).arrange(DOWN, buff=0.6).move_to(RIGHT * 3.0 + UP * 1.4)
        side = VGroup(
            label(r"green: \ wealth drifts up or down \\ to a neighbouring grid point", font_size=18, color=THEORY),
            label(r"gold: \ income switches", font_size=18, color=INDIRECT),
            label(rf"{C['unknowns']:,} unknowns: \ at most {C['nonzeros']:,} \\ nonzero entries out of "
                  rf"{C['dense']:,}".replace(",", "{,}"), font_size=18, color=WHITE),
            label(r"the forward equation is the \\ transpose of the backward one", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rhs, DOWN, buff=0.5).align_to(rhs, LEFT)
        with self.voiceover(
            "Put wealth on a grid. <bookmark mark='a'/> The Hamilton-Jacobi-Bellman equation becomes a matrix "
            "equation. Each row of the matrix A says where a household at one grid point goes next: to the "
            "neighbouring point up or down, as its wealth drifts, <bookmark mark='b'/> or to the same wealth in the "
            "other income state, when its income switches. Nearly every entry is zero. <bookmark mark='c'/> With "
            f"{C['unknowns']:,} unknowns, at most {C['nonzeros']:,} of the {C['dense']:,} entries are not. <bookmark "
            "mark='d'/> And here is the beautiful part: the Kolmogorov forward equation, discretized the same way, "
            "uses exactly the same matrix, transposed. The rows that say where each household goes are the columns "
            "that say where each household came from. Solve for the value, and the distribution comes almost free."
        ) as vo:
            self.play(Create(frame), FadeIn(ttl), FadeIn(rhs[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid if s.get_fill_color() == ManimColor(THEORY)],
                                  lag_ratio=0.01), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in grid if s.get_fill_color() != ManimColor(THEORY)],
                                  lag_ratio=0.02), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(rhs[1], shift=UP * 0.1), FadeIn(side[3]))
        self.clear_scene()

    def solved(self):
        C = load("continuous")
        Hg = load("huggett")
        a = np.array(C["a"])
        s = np.array(C["s"])
        ax = plane([a[0], 1.5], [-0.12, 0.08], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.6,
                   xticks=[-0.15, 0, 0.5, 1.0, 1.5], yticks=[-0.12, -0.06, 0, 0.06], xlabel=r"wealth",
                   ylabel=r"saving per year", xfmt=lambda v: f"{v:.2f}".replace("-", "{-}") if v < 0 else f"{v:.1f}",
                   yfmt=lambda v: f"{v:.2f}".replace("-", "{-}"), font_size=14)
        lo = path(ax, a, np.clip(s[:, 0], -0.12, 0.08), POOR, 2.8, xr=(a[0], 1.5))
        hi = path(ax, a, np.clip(s[:, 1], -0.12, 0.08), RICH, 2.8, xr=(a[0], 1.5))
        zero = seg(ax, a[0], 0, 1.5, 0, GREY_B, 1.4, dashed=True)
        side = VGroup(
            label(r"orange: \ low income \ dis-saves, \\ down to the limit, \ where it stops", font_size=18,
                  color=POOR),
            label(r"blue: \ high income saves, \\ less as wealth grows", font_size=18, color=RICH),
            label(rf"one household problem: \\ {1000 * C['seconds_one']:.0f} milliseconds", font_size=19,
                  color=WHITE),
            label(rf"the market, \ by bisection: \\ {C['seconds_eq']:.2f} seconds, \ $r = {100 * Hg['r']:.2f}\%$",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"Huggett's economy \ (computed)", corner=DL, font_size=12)
        with self.voiceover(
            "Here is the solution for Huggett's economy of chapter two. <bookmark mark='a'/> A household with low "
            "income runs its bonds down until it reaches the borrowing limit, where its saving stops exactly: in "
            "continuous time, the limit binds only at a single point. <bookmark mark='b'/> A household with high "
            "income saves, and saves less as it grows richer. <bookmark mark='c'/> One household problem, value and "
            f"distribution together, takes about {1000 * C['seconds_one']:.0f} milliseconds here. <bookmark "
            f"mark='d'/> The whole market, found by bisection on the interest rate, {C['seconds_eq']:.2f} seconds. "
            "That speed is what makes the next step possible: economies hit by shocks, solved again and again."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
