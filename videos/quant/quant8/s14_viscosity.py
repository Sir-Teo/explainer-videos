from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import BAD, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


def zigzag(x, kinks):
    """1 - |x| with extra notches: a function with |u'| = 1 almost everywhere and u(+-1) = 0."""
    u = 1 - np.abs(x)
    for c, d in kinks:  # a V-shaped notch of depth d centred at c
        u = np.minimum(u, np.abs(x - c) + (1 - abs(c)) - d)
    return u


class Viscosity(VoiceoverScene):
    def construct(self):
        v = load("viscosity")
        self.card()
        self.candidates()
        self.touch()
        self.theory()
        self.schemes(v)

    def card(self):
        c = chapter_card(4, r"When the value function has kinks: viscosity solutions",
                         r"What does an equation mean where its solution has no derivative?", lit=(1983,), part=PART)
        with self.voiceover("Chapter four. When the value function has kinks: viscosity solutions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def candidates(self):
        g = axes([-1, 1], [-0.2, 1.1], x_length=7.0, y_length=3.8, xlabel=r"$x$", xticks=[-1, 0, 1], yticks=[0, 1],
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        x = np.linspace(-1, 1, 401)
        cands = [zigzag(x, []), zigzag(x, [(0.0, 0.6)]), zigzag(x, [(-0.4, 0.3), (0.4, 0.3)]),
                 zigzag(x, [(-0.6, 0.15), (0.0, 0.5), (0.5, 0.2)]), np.abs(np.abs(x) - 0.5) * 0 + 0.5 - np.abs(np.abs(
                     x) - 0.5)]
        cols = [GOOD, UNDER, VALUE, KELLY, OVER]
        lines = VGroup(*[curve(ax, x, c_, col, stroke_width=3.5) for c_, col in zip(cands, cols)])
        eq = MathTex(r"|u'(x)| = 1 \ \text{ on } (-1, 1),\qquad u(-1) = u(1) = 0", font_size=34).to_edge(UP, buff=0.6)
        side = VGroup(
            wrapped_label(r"where do kinks come from? constraints (a floor), stopping (exercise or wait: a maximum of "
                          r"two functions), and any $\max$ or $\min$ in the problem", 4.6, 20, GREY_A),
            wrapped_label(r"no smooth function solves this; infinitely many zig-zags solve it everywhere except at "
                          r"their kinks", 4.6, 20, VALUE),
            wrapped_label(r"which one is ``the'' solution? (it is the distance to the boundary, $1 - |x|$, the value "
                          r"of the fastest exit)", 4.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        q = pause_card(r"Which zig-zag will a computer find?", width=4.6, font_size=22).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The verification theorem needed a smooth value function. Real problems break that. A floor, a choice between "
            "stopping and waiting, any maximum of two functions: each puts a kink in the value, a point where the second "
            "derivative in the HJB equation does not exist. <bookmark mark='a'/> The simplest example shows how bad it gets. "
            "Ask for a function whose slope is plus or minus one everywhere on the interval, and zero at both ends. No smooth "
            "function does it. A tent does it, everywhere except its peak; so does a tent with a notch; so do infinitely many "
            "zig-zags. <bookmark mark='b'/> If almost everywhere is good enough, the equation has no unique answer, and a "
            "numerical scheme could converge to any of them, or to none. Pause and predict: which one will a computer find? "
            "<bookmark mark='c'/> The one we want is the tent: the distance to the boundary, the value of the fastest way "
            "out. We need a definition that picks it."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.35, run_time=4), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), lines[1:].animate.set_stroke(opacity=0.25), lines[0].animate.set_stroke(width=6))
        self.wait(0.4)
        self.clear_scene()

    def touch(self):
        g = axes([-1, 1], [-0.1, 1.2], x_length=7.6, y_length=4.4, xticks=[-1, 0, 1], yticks=[], font_size=18)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        ax = g.ax
        x = np.linspace(-1, 1, 401)
        u = 0.5 - np.abs(np.abs(x) - 0.5)  # peaks at -0.5 and 0.5 (kinks pointing up), a valley at 0 (pointing down)
        line = curve(ax, x, u, VALUE, stroke_width=4)
        slope = ValueTracker(-0.9)
        # above the peak at x = -0.5: phi(x) = 0.5 + s (x + 0.5) + 2 (x + 0.5)^2, touching from above
        xs = np.linspace(-0.95, -0.05, 120)
        phi_up = always_redraw(lambda: curve(ax, xs, 0.5 + slope.get_value() * (xs + 0.5) + 2.5 * (xs + 0.5) ** 2,
                                             GOOD, stroke_width=3))
        read_up = DecimalNumber(-0.9, num_decimal_places=2, include_sign=True, font_size=30, color=GOOD)
        read_up.add_updater(lambda m: m.set_value(slope.get_value()))
        ru = VGroup(MathTex(r"\varphi'(x_0) =", font_size=30, color=GOOD), read_up).arrange(RIGHT, buff=0.12)
        xs2 = np.linspace(-0.45, 0.45, 120)
        phi_dn = curve(ax, xs2, 0.0 - 2.5 * xs2 ** 2, OVER, stroke_width=3)
        dot_up = Dot(ax.c2p(-0.5, 0.5), color=GOOD)
        dot_dn = Dot(ax.c2p(0.0, 0.0), color=OVER)
        card = definition_card(r"viscosity solution of $F(x, u, u', u'') = 0$", VGroup(
            wrapped_label(r"subsolution: wherever a smooth $\varphi$ touches $u$ from above at $x_0$ ($u - \varphi$ has "
                          r"a local max), $F(x_0, u, \varphi', \varphi'') \le 0$", 4.6, 19, GREY_A),
            wrapped_label(r"supersolution: wherever $\varphi$ touches from below (a local min), $F \ge 0$", 4.6, 19,
                          GREY_A),
            wrapped_label(r"here $F = |u'| - 1$; a solution is both", 4.6, 19, VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15), kind=r"Definition (Crandall and Lions 1983)", width=5.6,
            color=VALUE).to_edge(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        ok = label(r"peak: from above, every touching slope has $|\varphi'| \le 1$: passes", font_size=20, color=GOOD)
        bad = label(r"valley: from below, $\varphi' = 0$ fits, and $|0| - 1 < 0$: fails", font_size=20, color=OVER)
        VGroup(ok, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(card, DOWN, buff=0.35).align_to(card, LEFT)
        ru.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        with self.voiceover(
            "Crandall and Lions found it in 1983: never differentiate u. Touch it with smooth test functions instead, and "
            "put their derivatives into the equation. <bookmark mark='a'/> At a peak, a smooth function touches from above "
            "with any slope between minus one and one, and every one passes the subsolution test; from below nothing "
            "touches. The peak passes. <bookmark mark='b'/> At the valley, a flat parabola touches from below, and the "
            "supersolution test needs its slope's size minus one to be at least zero. It is minus one: the valley fails. "
            "<bookmark mark='c'/> Every downward kink fails, so only the tent survives."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(card))
            vo.wait_until("a")
            self.add(phi_up)
            self.play(FadeIn(dot_up), FadeIn(ru))
            self.play(slope.animate.set_value(0.9), run_time=3, rate_func=there_and_back_with_pause)
            self.play(FadeIn(ok))
            vo.wait_until("b")
            self.play(Create(phi_dn), FadeIn(dot_dn), run_time=1.5)
            self.play(FadeIn(bad), Flash(dot_dn, color=OVER))
            vo.wait_until("c")
        phi_up.clear_updaters()
        read_up.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def theory(self):
        cards = VGroup(
            theorem_card(r"Comparison", r"a subsolution below the boundary data stays below a supersolution above it; "
                         r"so there is at most one viscosity solution", who=r"Crandall, Ishii and Lions (1992); "
                         r"Fleming and Soner, ch.\ 2", width=6.2, color=VALUE),
            theorem_card(r"Barles--Souganidis (1991)", r"a numerical scheme that is monotone, stable and consistent "
                         r"converges to the viscosity solution", who=r"\textit{Asymptotic Analysis} 4", width=6.2,
                         color=KELLY),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"the value function of a control problem is always a viscosity solution of its HJB "
                             r"equation (Lions 1983; Pham ch.\ 4; Touzi ch.\ 5--6): the dynamic programming principle "
                             r"is exactly the touching test", 12.0, 21, GREY_A).next_to(cards, DOWN, buff=0.6)
        with self.voiceover(
            "Two theorems make this the right notion. The comparison principle: a subsolution that starts below a "
            "supersolution stays below it, so there can be only one viscosity solution. And the value function of a control "
            "problem is always a viscosity solution of its HJB equation, smooth or not: the dynamic programming principle is "
            "the touching test. <bookmark mark='a'/> The third is the one engineers use. Guy Barles and Panagiotis "
            "Souganidis proved in 1991 that a numerical scheme that is monotone, stable and consistent converges to the "
            "viscosity solution. Monotone means that raising the value at a neighbour can only raise the update. The next "
            "experiment shows what happens without it."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def schemes(self, v):
        x = np.asarray(v["x"])
        times = list(v["times"])
        up, ce = np.asarray(v["upwind_snaps"]), np.asarray(v["central_snaps"])
        gs = [axes([-1, 1], [-0.4, 1.4], x_length=5.4, y_length=3.0, xticks=[-1, 0, 1], yticks=[0, 1], font_size=16)
              for _ in range(2)]
        VGroup(*gs).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        heads = VGroup(label(r"upwind (Godunov): monotone", font_size=22, color=GOOD).next_to(gs[0], UP, buff=0.1),
                       label(r"central differences: not monotone", font_size=22, color=OVER).next_to(gs[1], UP, buff=0.1))
        tent = VGroup(*[curve(g.ax, x, 1 - np.abs(x), GREY_C, stroke_width=1.5) for g in gs])
        k = ValueTracker(0)

        def prof(g, arr, col):
            return always_redraw(lambda: curve(g.ax, x, np.where(np.abs(arr[int(k.get_value())]) < 1.38,
                                                                 arr[int(k.get_value())], np.nan), col, stroke_width=3.5))

        pu, pc = prof(gs[0], up, GOOD), prof(gs[1], ce, OVER)
        tn = DecimalNumber(times[0], num_decimal_places=2, font_size=30, color=GREY_A)
        tn.add_updater(lambda m: m.set_value(times[int(k.get_value())]))
        tlab = VGroup(MathTex(r"t =", font_size=30, color=GREY_A), tn).arrange(RIGHT, buff=0.1).next_to(
            VGroup(*gs), DOWN, buff=0.25)
        grid = v["grids"]
        head = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"nodes", r"upwind: max error",
                                                                       r"central: max error")])
        def sci(z):
            e = int(np.floor(np.log10(z)))
            return rf"{z / 10 ** e:.0f} \times 10^{{{e}}}"

        cells = [head] + [VGroup(MathTex(n, font_size=26), MathTex(sci(grid[n]["upwind"]), font_size=26, color=GOOD),
                                 MathTex(sci(grid[n]["central"]), font_size=26, color=OVER)) for n in ("21", "81", "321")]
        tab = VGroup(*[m for r_ in cells for m in r_]).arrange_in_grid(rows=4, cols=3, buff=(0.8, 0.15))
        tab.to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        side = wrapped_label(r"the floor solver of chapter 2 takes a maximum of averages of the next values with "
                             r"positive weights: monotone, which is why it converged", 5.2, 19, GREY_A).next_to(
            tab, RIGHT, buff=0.6)
        src = illustration(r"$u_t + |u_x| = 1$ from $u = 0$, marched to $t = 6$")
        with self.voiceover(
            "Test it. March the equation, u t plus the size of u x equals one, forward in time from zero until it settles. "
            "On the left, an upwind scheme that looks at each neighbour from the side the information comes from: monotone. "
            "On the right, the textbook central difference: consistent, but not monotone. <bookmark mark='a'/> The upwind "
            "profile rises like water filling a tent and stops exactly at the distance function. The central profile develops "
            "teeth between neighbouring nodes, and the teeth grow. <bookmark mark='b'/> On every grid the upwind error is at "
            f"the level of rounding. The central error reaches ten to the {int(np.log10(grid['321']['central']))} on the "
            "finest grid: refining makes it worse. <bookmark mark='c'/> Consistency is not enough. Monotonicity is what makes a "
            "grid converge to the right kink, and it is why chapter two's solver, a maximum of positively weighted averages, "
            "found portfolio insurance."
        ) as vo:
            self.play(*[FadeIn(g) for g in gs], FadeIn(heads), FadeIn(tent), FadeIn(src))
            self.add(pu, pc, tlab)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(times) - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.3, run_time=2))
            vo.wait_until("c")
            self.play(FadeIn(side))
        for m in (pu, pc, tn):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
