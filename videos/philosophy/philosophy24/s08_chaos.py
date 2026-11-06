from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


def to_screen(p, cx=-3.2, cy=-0.5, sx=0.13, sz=0.095):
    """Project a Lorenz point (x, y, z) onto the screen: x across, z up."""
    return np.array([cx + sx * p[0], cy + sz * (p[2] - 25.0), 0])


class Chaos(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Chaos", r"Is unpredictable the same as undetermined?", lit=(1963,), part=PART)
        with self.voiceover("Chapter seven. Chaos."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.attractor()
        self.separation()
        self.horizons()
        self.roulette()

    def attractor(self):
        d = load("lorenz")
        hc = history_card(1963, r"Edward Lorenz", r"`Deterministic Nonperiodic Flow'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        eq = MathTex(r"\dot x &= \sigma (y - x)\\ \dot y &= x(\rho - z) - y\\ \dot z &= xy - \beta z", font_size=32,
                     color=LAW).move_to([4.3, 1.0, 0])
        par = MathTex(r"\sigma = 10,\;\; \rho = 28,\;\; \beta = \tfrac83", font_size=26, color=GREY_A).next_to(
            eq, DOWN, buff=0.3)
        A = [to_screen(p) for p in d["path_a"]]
        B = [to_screen(p) for p in d["path_b"]]
        k = ValueTracker(2)

        def path(P, c, w):
            n = max(2, int(k.get_value()))
            return VMobject(stroke_color=c, stroke_width=w).set_points_as_corners(P[:n])

        pa = always_redraw(lambda: path(A, LAW, 2.0))
        pb = always_redraw(lambda: path(B, CHANCE, 2.0))
        da = always_redraw(lambda: Dot(A[max(1, int(k.get_value())) - 1], radius=0.08, color=LAW))
        db = always_redraw(lambda: Dot(B[max(1, int(k.get_value())) - 1], radius=0.08, color=CHANCE))
        clock = always_redraw(lambda: label(rf"$t = {d['times'][max(1, int(k.get_value())) - 1]:.1f}$",
                                            font_size=22, color=TIME).move_to([4.3, -1.2, 0]))
        start = label(r"two starts $10^{-9}$ apart", font_size=20, color=WHITE).move_to([4.3, -1.9, 0])
        i_split = next(i for i, s in enumerate(d["separation"]) if s > 1.0)
        with self.voiceover(
            "In 1963 the meteorologist Edward Lorenz studied three equations, a drastic simplification of "
            "convection in the atmosphere. <bookmark mark='a'/>Three variables, three equations, with constants ten, "
            "twenty-eight and eight thirds. Nothing is random: this is a deterministic system, and its solutions are "
            "unique. <bookmark mark='b'/>Start two copies one billionth apart. <bookmark mark='c'/>For a long time "
            "they trace the same path, looping around one wing of the attractor, then the other. "
            "<bookmark mark='d'/>Then, around time twenty, the difference has grown large enough to see, and "
            "soon the two are on different wings, as different as two randomly chosen states."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(par))
            vo.wait_until("b")
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(da), FadeIn(db), FadeIn(clock), FadeIn(start))
            vo.wait_until("c")
            self.play(k.animate.set_value(i_split - 30), run_time=8, rate_func=linear)
            vo.wait_until("d")
            self.play(k.animate.set_value(i_split + 120), run_time=4, rate_func=linear)
        for m in (pa, pb, da, db, clock):
            m.clear_updaters()
        self.clear_scene()

    def separation(self):
        d = load("lorenz")
        head = label(r"Exponential growth of error", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 40, 10], y_range=[0, 12, 2], x_length=7.6, y_length=4.0,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True}
                  ).move_to([-2.2, -0.6, 0])
        ylabs = VGroup(*[MathTex(str(k - 10), font_size=18, color=GREY_A).next_to(ax.c2p(0, k), LEFT, buff=0.12)
                         for k in range(0, 13, 2)])
        xl = label(r"time", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$\log_{10}$ of the separation", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        ys = [10 + float(np.log10(max(s, 1e-12))) for s in d["separation"]]
        curve = series_plot(ax, ys, ENT, xs=d["times"], width=2.5)
        lam = d["lyapunov"]
        fit = ax.plot(lambda t: 1 + lam * t / np.log(10), x_range=[0, 22], color=GOAL, stroke_width=3)
        f = MathTex(r"|\delta(t)| \approx |\delta(0)|\, e^{\lambda t}", font_size=34, color=GOAL).move_to(
            [4.6, 1.3, 0])
        side = stack([(rf"the Reasoner's estimate: \ $\lambda \approx {lam:.2f}$", GOAL),
                      (r"Benettin's method: \ follow the gap, \ shrink it back, \ average the stretching", ABS),
                      (r"the error grows tenfold about every 2.5 time units, \ until it fills the attractor", ENT)],
                     font_size=20, aligned_edge=LEFT, width=4.4).move_to([4.6, -0.8, 0])
        assert 0.85 < lam < 0.95
        with self.voiceover(
            "Plot the gap between the two runs, on a logarithmic scale. <bookmark mark='a'/>It climbs along a "
            "straight line: the error grows exponentially, multiplied by e to the lambda t. "
            "<bookmark mark='b'/>Lambda is the largest Lyapunov exponent. The Reasoner estimates it the standard "
            "way, following a tiny gap, shrinking it back after every step, and averaging the stretching: about "
            "zero point nine. <bookmark mark='c'/>So the error grows tenfold roughly every two and a half time "
            "units, until it is as large as the attractor itself, and then it can grow no more. That is what chaos "
            "means: deterministic dynamics with exponential sensitivity to the starting point."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ylabs), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), run_time=3)
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def horizons(self):
        d = load("lorenz")
        head = label(r"The price of a longer forecast", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{initial error}", r"\text{error reaches 1 at}", r"\ln(1/\delta)/\lambda"]
        rows = [[MathTex(rf"10^{{{int(round(np.log10(h['delta'])))}}}", font_size=24),
                 MathTex(f"{h['time']:.1f}", font_size=24, color=ENT),
                 MathTex(f"{h['theory']:.1f}", font_size=24, color=GOAL)] for h in d["horizons"]]
        grid = ValueGrid(hd, rows, col_w=[2.8, 3.4, 2.6], cell_h=0.55, font_size=22).move_to([-2.0, 0.4, 0])
        gaps = [b["time"] - a["time"] for a, b in zip(d["horizons"], d["horizons"][1:])]
        side = stack([(r"each thousandfold gain in precision buys only about 7 time units", BAD),
                      (r"Lorenz \ (1972): \ `Does the flap of a butterfly's wings in Brazil set off a tornado in "
                       r"Texas?'", HIST),
                      (r"weather: \ a horizon of about two weeks", CHANCE)], font_size=20, aligned_edge=LEFT,
                     width=4.4).move_to([4.6, 0.4, 0])
        foot = label(r"unpredictable \ $\neq$ \ undetermined: \ Laplace's demon needs infinite precision, \ not "
                     r"new laws", font_size=22, color=GOAL).to_edge(DOWN, buff=0.5)
        assert all(5.0 < g < 9.5 for g in gaps)
        with self.voiceover(
            "What does a better measurement buy? <bookmark mark='a'/>Start with an error of one in a thousand and "
            "the forecast fails at about time seven. One in a million: about thirteen. One in a billion: about "
            "twenty-two. One in a trillion: about twenty-nine. The last column is the simple estimate, the "
            "logarithm of one over the error, divided by lambda. <bookmark mark='b'/>Each thousandfold gain in "
            "precision buys only about seven more units of time. <bookmark mark='c'/>Lorenz put it as a question "
            "in a talk in 1972: does the flap of a butterfly's wings in Brazil set off a tornado in Texas? "
            "<bookmark mark='d'/>For the real atmosphere, the horizon of detailed forecasting is about two weeks. "
            "<bookmark mark='e'/>But notice what chaos does not show. The Lorenz system is perfectly deterministic. "
            "Unpredictable is not the same as undetermined: Laplace's demon would need infinite precision, not "
            "new laws."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            for mk, r in zip("bcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def roulette(self):
        d = load("roulette")
        head = label(r"Poincaré's roulette wheel", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        vs = d["v"]
        strip = VGroup()
        w = 9.0 / len(vs)
        runs, start = [], 0
        reds = d["red_at_v"]
        for i in range(1, len(reds) + 1):
            if i == len(reds) or reds[i] != reds[start]:
                runs.append((start, i, reds[start]))
                start = i
        flips = len(runs) - 1
        assert flips == 28
        for a, b, red in runs:
            strip.add(Rectangle(width=(b - a) * w, height=0.6, stroke_width=0, fill_color=BAD if red else GREY_D,
                                fill_opacity=0.95).move_to([-4.5 + (a + b) / 2 * w, 1.2, 0]))
        sl = label(rf"the outcome as a function of the initial speed, \ from {vs[0]:.1f} to {vs[-1]:.1f}",
                   font_size=19, color=GREY_A).next_to(strip, UP, buff=0.15)
        dens = ParametricFunction(lambda u: np.array([-4.5 + 9.0 * u, -0.2 + 0.7 * np.exp(-((u - 0.4) / 0.22) ** 2),
                                                       0]), t_range=[0, 1], color=CHANCE, stroke_width=3)
        dl = label(r"any smooth spread of speeds", font_size=19, color=CHANCE).move_to([2.9, 0.4, 0])
        hd = [r"\text{speeds drawn from}", r"P(\text{red})"]
        rows = [[label(r["speeds"], font_size=20),
                 MathTex(f"{r['red']:.3f}", font_size=24, color=BAD)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[4.8, 2.0], cell_h=0.48, font_size=20).move_to([-2.6, -1.8, 0])
        side = stack([(r"the method of arbitrary functions: \ Poincaré \ (1896), \ Strevens \ (2003)", ABS),
                      (r"deterministic, \ yet the chance of red is $\tfrac12$ \ whatever the spread", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=4.6).move_to([4.5, -1.8, 0])
        with self.voiceover(
            "Chaos also explains where deterministic chances come from. Henri Poincaré's example was a roulette "
            "wheel. <bookmark mark='a'/>Spin it with some initial speed and it slows to a stop; where it stops is a "
            "fixed function of the speed. Here is that function, red or black, as the speed runs over a narrow "
            "range: it changes colour twenty-eight times. <bookmark mark='b'/>Now let the croupier's speed vary "
            "according to any smooth spread of values, however lopsided. <bookmark mark='c'/>The Reasoner tries four "
            "very different spreads. The chance of red comes out at one half every time, to within a "
            "hundredth. <bookmark mark='d'/>This is the method of arbitrary functions, developed by Poincaré and, "
            "in our time, by Michael Strevens: when the outcome flips back and forth faster than the spread of "
            "initial conditions can follow, the probability of each outcome is fixed by the dynamics alone. "
            "Deterministic laws, and real chances."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in strip], lag_ratio=0.05), FadeIn(sl), run_time=2)
            vo.wait_until("b")
            self.play(Create(dens), FadeIn(dl))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
        self.clear_scene()
