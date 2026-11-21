from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

KINDS = (("linear", r"linear, \ 40 points", VFI), ("cubic", r"cubic spline, \ 40 points", POLICY),
         ("chebyshev", r"Chebyshev, \ 12 points", PROJ))


def _one_in(e):
    return f"{10 ** (-e):,.0f}".replace(",", "{,}")


class Interpolation(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Between the grid points", r"Where should the points go, \ and what goes between them?",
             "Chapter four. Between the grid points.", lit={1901: r"Runge"}, scale=("nation",),
             horizon=("a century",))
        self.idea()
        self.compare()
        self.runge()
        self.placement()

    def idea(self):
        ax = plane([0, 10], [0, 6], center=LEFT * 1.5 + DOWN * 0.3, x_length=7.6, y_length=4.4, xticks=[],
                   yticks=[], xlabel=r"next year's capital", ylabel=r"value", font_size=14)
        xs = np.linspace(0.5, 9.5, 7)
        f = lambda x: 5 - 0.08 * (x - 6.2) ** 2  # noqa: E731
        pts = VGroup(*[dot(ax, x, f(x), GRID, 0.08) for x in xs])
        fine = np.linspace(0.5, 9.5, 200)
        smooth = path(ax, fine, f(fine), POLICY, 2.4)
        best_grid = dot(ax, xs[np.argmax(f(xs))], f(xs).max(), VFI, 0.11)
        best = dot(ax, 6.2, 5.0, POLICY, 0.11)
        side = VGroup(
            label(r"on the grid: \\ the best of seven", font_size=19, color=VFI),
            label(r"between the points: \\ an interpolated value, \\ searched for its peak", font_size=19,
                  color=POLICY),
            label(r"golden-section search: \\ each step keeps the \\ better 62\% of the interval", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The staircase of the last chapter came from a restriction: next year's capital had to be one of the "
            "grid points. <bookmark mark='a'/> The best of seven points may be some way from the true best. "
            "<bookmark mark='b'/> Instead, keep the value function only at the grid points, fill in between them "
            "by interpolation, and search the filled-in curve for its peak, wherever it lies. <bookmark mark='c'/> "
            "A golden-section search does that without derivatives: each step keeps the better sixty-two percent "
            "of the interval, so sixty steps pin the peak down to far less than a billionth of the range."
        ) as vo:
            self.play(FadeIn(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(best_grid, scale=1.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(smooth), FadeIn(best, scale=1.5), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(best, color=WHITE, scale_factor=1.8))
        self.clear_scene()

    def compare(self):
        It = load("interp")
        R = load("grids")
        ax = plane([0.6, 1.4], [-8, 0], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.2, y_length=4.6,
                   xticks=[0.6, 0.8, 1.0, 1.2, 1.4], yticks=[-8, -6, -4, -2, 0],
                   xlabel=r"capital, \ share of steady state", ylabel=r"Euler-equation error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        grid1000 = R["rows"][-1]["ee"]
        ref = path(ax, grid1000["k"], grid1000["log10"], EGM, 1.2, smooth=False).set_opacity(0.45)
        curves = VGroup(*[path(ax, It[k]["ee"]["k"], It[k]["ee"]["log10"], c, 1.6, smooth=False)
                          for k, _, c in KINDS])
        side = VGroup(
            label(r"faint: \ the 1,000-point grid".replace(",", "{,}"), font_size=17, color=EGM),
            *[label(rf"{n}: \\ one dollar in {_one_in(It[k]['ee']['max'])}", font_size=18, color=c)
              for k, n, c in KINDS],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "How much does it buy? <bookmark mark='a'/> For reference, the thousand-point grid, faint. <bookmark "
            "mark='b'/> Forty points with straight lines between them nearly match it, at about one dollar in "
            f"{_one_in(It['linear']['ee']['max'])}. <bookmark mark='c'/> The same forty points joined by a cubic "
            f"spline: one in {_one_in(It['cubic']['ee']['max'])}, thousands of times better, because the value "
            "function is smooth and a spline uses its curvature. <bookmark mark='d'/> And twelve points, placed "
            "where Chebyshev says and joined by one polynomial: one dollar in "
            f"{_one_in(It['chebyshev']['ee']['max'])}. Smooth problems reward smooth approximations."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(ref), FadeIn(side[0]))
            for mk, c_, s_ in zip("bcd", curves, side[1:]):
                vo.wait_until(mk)
                self.play(Create(c_), FadeIn(s_), run_time=1.4)
        self.clear_scene()

    def runge(self):
        R = load("interp")["runge"]
        ax = plane([-1, 1], [-0.5, 2.0], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.2, y_length=4.6,
                   xticks=[-1, -0.5, 0, 0.5, 1], yticks=[-0.5, 0, 0.5, 1, 1.5, 2],
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        f = path(ax, R["x"], R["f"], WHITE, 2.6)
        even = path(ax, R["x"], R["even"], ERR, 2.2, yr=(-0.5, 2.0))
        cheb = path(ax, R["x"], R["cheb"], PROJ, 2.2)
        pe = VGroup(*[dot(ax, x, 1 / (1 + 25 * x * x), ERR, 0.06) for x in R["xe"]])
        pc = VGroup(*[dot(ax, x, 1 / (1 + 25 * x * x), PROJ, 0.06) for x in R["xc"]])
        side = VGroup(
            label(r"white: \ $1/(1 + 25x^2)$", font_size=19, color=WHITE),
            label(rf"red: \ {R['n']} evenly spaced \\ points, \ one polynomial: \\ error {R['err_even']:.2f}",
                  font_size=18, color=ERR),
            label(rf"pink: \ {R['n']} Chebyshev \\ points: \ error {R['err_cheb']:.2f}", font_size=18, color=PROJ),
            label(r"more even points \\ make it worse", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Runge (1901)", corner=DL, font_size=12)
        with self.voiceover(
            "Why Chebyshev's points? Carl Runge found the warning in 1901. <bookmark mark='a'/> Take this smooth, "
            "harmless-looking bump. <bookmark mark='b'/> Pass one polynomial through eleven evenly spaced points on "
            "it, and the polynomial swings wildly near the ends, missing by "
            f"{R['err_even']:.1f}; adding more evenly spaced points makes the swings larger, not smaller. "
            "<bookmark mark='c'/> Put the eleven points where Chebyshev's nodes are, crowded towards the ends, and "
            f"the error falls to {R['err_cheb']:.2f}, and keeps falling as points are added. Where you put the "
            "points matters as much as how many you use."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(f), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(pe), Create(even), FadeIn(side[1]), run_time=1.6)
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(pc), Create(cheb), FadeIn(side[2]), run_time=1.6)
        self.clear_scene()

    def placement(self):
        n = 24
        even = np.linspace(0, 1, n)
        cheb = (np.sort(solve.chebyshev_nodes(n, 0, 1)))
        sq = np.linspace(0, 1, n) ** 2

        def row(xs, col, y, name):
            base = Line(LEFT * 4.5, RIGHT * 4.5, color=GREY_D, stroke_width=1.5).shift(UP * y)
            ticks = VGroup(*[Line(UP * 0.18, DOWN * 0.18, color=col, stroke_width=2.4).move_to(
                [-4.5 + 9 * x, y, 0]) for x in xs])
            nm = label(name, font_size=19, color=col).next_to(base, UP, buff=0.25).align_to(base, LEFT)
            return VGroup(base, ticks, nm)

        rows = VGroup(row(even, GRID, 1.6, r"evenly spaced"),
                      row(cheb, PROJ, 0.0, r"Chebyshev: \ crowded at both ends, \ for polynomials"),
                      row(sq, EGM, -1.6, r"squared: \ crowded near the borrowing limit, \ where the household's "
                                         r"rule bends"))
        foot = label(r"put the points where the function bends", font_size=24, color=E.ACCENT).to_edge(DOWN,
                                                                                                    buff=0.6)
        with self.voiceover(
            "Three ways to place twenty-four points. <bookmark mark='a'/> Evenly, the natural first choice. "
            "<bookmark mark='b'/> Chebyshev's nodes, crowded at both ends, the right choice for a single polynomial "
            "across the whole range. <bookmark mark='c'/> And a grid that crowds its points near the borrowing "
            "limit, the one the household of chapter five uses, because that is where its consumption rule bends "
            "sharply. <bookmark mark='d'/> The rule is simple to state and easy to forget: put the points where the "
            "function bends."
        ) as vo:
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0]), FadeIn(r_[2]), LaggedStart(*[GrowFromCenter(t) for t in r_[1]],
                                                                   lag_ratio=0.05), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
