from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog, predict, sci, axes, data_range, pause_card, flat_camera

ORDER = ["Monte Carlo (QE, 50 steps)", "ADI (Craig-Sneyd)", "Carr-Madan FFT", "COS"]

# the history of this part, in its own strip (the series' timeline has one entry a year)
HISTORY = [
    (1947, r"Crank--Nicolson", QC.IDEA), (1949, r"Metropolis--Ulam name ``Monte Carlo''", QC.IDEA),
    (1967, r"Sobol's sequence", QC.IDEA), (1977, r"Boyle (simulation), Schwartz (grids)", QC.IDEA),
    (1979, r"binomial trees", QC.IDEA), (1996, r"Broadie--Glasserman: Greeks", QC.IDEA),
    (1999, r"Carr--Madan: the FFT", QC.IDEA), (2001, r"Longstaff--Schwartz", QC.IDEA),
    (2006, r"smoking adjoints", QC.IDEA), (2008, r"multilevel MC; COS", QC.IDEA),
    (2011, r"JPMorgan's FPGAs", QC.FIRM), (2021, r"a quantum threshold", QC.IDEA),
    (2024, r"quantum signal processing", QC.IDEA),
]


class Hook(VoiceoverScene):
    def construct(self):
        r = load("race")
        self.title_card()
        self.race(r)
        self.spread(r)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"One price, many machines")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part sixteen. Computing prices. The models of the last six parts are equations; this part is about "
            "turning them into numbers, fast enough and accurately enough for a trading desk."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def race(self, r):
        """The four engines start together; each point appears when the wall clock reaches it."""
        pts = r["points"]
        xr = data_range([np.log10(q["time"]) for q in pts])
        yr = data_range([np.log10(q["err"]) for q in pts])
        g = loglog(*xr, *yr, r"wall-clock time (seconds, one core)", r"absolute error; MC: one standard error", x_length=8.4,
                   y_length=4.6, xt=[-4, -3, -2, -1, 0, 1], yt=[-8, -6, -4, -2, 0])
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        clock = ValueTracker(xr[0])
        by = {m: sorted([q for q in pts if q["method"] == m], key=lambda q: q["time"]) for m in ORDER}

        def draw(m):
            def make():
                t = clock.get_value()
                rr = [q for q in by[m] if np.log10(q["time"]) <= t]
                grp = VGroup()
                if len(rr) > 1:
                    grp.add(VMobject(stroke_color=METHOD_COL[m], stroke_width=3).set_points_as_corners(
                        [ax.c2p(np.log10(q["time"]), np.log10(q["err"])) for q in rr]))
                for q in rr:
                    grp.add(Dot(ax.c2p(np.log10(q["time"]), np.log10(q["err"])), radius=0.07,
                                color=METHOD_COL[m]))
                return grp
            return always_redraw(make)

        lines = [draw(m) for m in ORDER]
        hand = always_redraw(lambda: DashedLine(ax.c2p(clock.get_value(), yr[0]), ax.c2p(clock.get_value(), yr[1]),
                                                stroke_color=GREY_B, stroke_width=1.5))
        tick = readout(r"\log_{10}(t / \text{s}) =", lambda: clock.get_value(), digits=1, font_size=26, color=GREY_A)
        tick.next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        leg = legend([(METHOD_COL[m], m) for m in ORDER], font_size=17).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        cos_hit = min(q["time"] for q in by["COS"] if q["err"] < 1e-5)
        mc_first = min(q["time"] for q in by[ORDER[0]])
        note_ = wrapped_label(rf"COS is below $10^{{-5}}$ after {cos_hit * 1e3:.2f} ms; Monte Carlo's first point "
                              rf"arrives after {mc_first * 1e3:.0f} ms", 3.6, 18, GREY_A).next_to(leg, DOWN, buff=0.4)
        note_.align_to(leg, LEFT)
        src = illustration(r"one Heston call, zero rates; separate shared-CPU timings; MC: sampling error only")
        with self.voiceover(
            "A one-year Heston call, with zero rates and dividends, priced four ways. These are separately timed runs on a shared CPU, revealed as an illustrative clock reaches each recorded time. <bookmark mark='a'/> The vertical axis needs care. Grid and Fourier points show absolute error against a high-resolution COS reference. Monte Carlo points show one estimated sampling standard error, which excludes the bias of its fifty-step QE discretization. This is not a common total-error guarantee. <bookmark mark='b'/> In this fixed low-dimensional benchmark, Fourier methods reach small reference errors quickly. A path-dependent or many-asset payoff can change the choice of method. Timing and accuracy depend on this implementation, grid and machine."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), *[FadeIn(x) for x in lines], FadeIn(hand), FadeIn(tick))
            vo.wait_until("a")
            self.play(clock.animate.set_value(xr[0] + 0.4 * (xr[1] - xr[0])), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(clock.animate.set_value(xr[1]), run_time=max(vo.remaining(0.5), 2.0), rate_func=linear)
        self.play(FadeIn(note_))
        self.wait(0.6)
        self.clear_scene()

    def spread(self, r):
        pts = r["points"]
        best = {}
        for p_ in pts:
            b = best.get(p_["method"])
            if b is None or p_["err"] < b["err"]:
                best[p_["method"]] = p_
        rows = VGroup()
        for m in ORDER:
            b = best[m]
            rows.add(VGroup(label(m, font_size=24, color=METHOD_COL[m]),
                            MathTex(rf"\text{{{'one SE' if m == ORDER[0] else 'abs. error'}}}\ {sci(b['err'])}", font_size=28),
                            MathTex(rf"{b['time']:.4f}\,\text{{s}}", font_size=28)))
        rows.arrange(DOWN, buff=0.45)
        for row in rows:
            row[0].set_x(-3.6)
            row[1].set_x(1.2)
            row[2].set_x(4.2)
        head = label(rf"one Heston call, four engines (price {r['ref']:.4f})", font_size=28).to_edge(UP, buff=0.9)
        rows.next_to(head, DOWN, buff=0.6)
        q = predict(r"Ten times smaller sampling SE: how much work for iid paths at fixed cost?", width=7.4,
                    font_size=22).to_edge(DOWN, buff=0.4)
        src = illustration(r"smallest displayed metric per method; CPU timings are implementation-specific", corner=UR)
        with self.voiceover(
            "These rows select the smallest displayed error metric for each method, with the time of that same run. The Monte Carlo row is a standard error; the others are errors against the reference, so they do not certify equally accurate prices. A numerical reference itself also has truncation and floating-point error. <bookmark mark='a'/> Pause and predict. For an unbiased independent-path estimator with fixed variance and constant cost per path, how much work buys ten times smaller sampling standard error? A hundred times. That scaling does not remove time-discretization bias or price-model error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows],
                                                             lag_ratio=0.4, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        x0, x1 = -6.2, 6.2

        def X(y):
            return x0 + (x1 - x0) * (y - 1940) / (2030 - 1940)

        axis = Line([x0, -3.0, 0], [x1, -3.0, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), -3.06, 0], [X(y), -2.94, 0], color=GREY_D),
                                Text(str(y), font_size=17, color=GREY_C).next_to([X(y), -3.0, 0], DOWN, buff=0.12))
                         for y in range(1940, 2031, 10)])
        dots = VGroup(*[Dot([X(yr), -3.0, 0], radius=0.065, color=col) for yr, _, col in HISTORY])
        labs = VGroup(*[wrapped_label(rf"{yr}: {name}", 5.9, 25, col) for yr, name, col in HISTORY])
        labs.arrange_in_grid(rows=7, cols=2, cell_alignment=LEFT, buff=(0.5, 0.22)).move_to(UP * 0.5)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.35)
        strip = VGroup(axis, ticks)
        with self.voiceover(
            "How we got here. In 1947 John Crank and Phyllis Nicolson published a time-stepping scheme for the heat "
            "equation, the grid method this part still uses. <bookmark mark='a'/> Two years later Nicholas "
            "Metropolis and Stanislaw Ulam named the method of solving equations with random numbers after a casino: "
            "Monte Carlo. In 1967 Ilya Sobol built points more even than random ones. <bookmark mark='b'/> Finance "
            "arrived in 1977, when the same journal carried Phelim Boyle's simulation of an option and Eduardo "
            "Schwartz's grid for warrants. Trees followed in 1979. <bookmark mark='c'/> Then the modern toolkit: Greeks "
            "by simulation in 1996, the fast Fourier transform in 1999, American options by regression in 2001, "
            "adjoint Greeks in 2006, and in 2008 both multilevel simulation and the cosine method. <bookmark mark='d'/> "
            "Then the hardware: programmable chips in 2011, and in 2021 an estimate of what a quantum computer "
            "would need."
        ) as vo:
            self.play(FadeIn(head), Create(strip), FadeIn(dots), run_time=1.2)
            groups = [(0, 2, "a"), (2, 3, "b"), (3, 5, "c"), (5, 10, "d")]
            for a, b, mk in groups:
                self.play(LaggedStart(*[FadeIn(labs[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          *[Indicate(dots[i], scale_factor=1.6) for i in range(a, b)])
                vo.wait_until(mk)
            self.play(LaggedStart(*[FadeIn(labs[i], shift=UP * 0.1) for i in range(10, len(HISTORY))], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Monte Carlo's error bar; random numbers, paths and parallel streams",
            r"Variance reduction: control variates, antithetics, strata; importance sampling learned by cross-entropy",
            r"Quasi-Monte Carlo: discrepancy, Sobol nets, the Brownian bridge, effective dimension",
            r"Multilevel Monte Carlo: the complexity theorem, Euler against Milstein",
            r"American options: Longstaff--Schwartz run backward, the duality bound, five assets",
            r"Greeks three ways; adjoint differentiation and its cost",
            r"Finite differences: stability, Crank--Nicolson's ringing, the American put as a complementarity problem",
            r"ADI for Heston on non-uniform grids",
            r"Fourier: Carr--Madan, Lewis, COS, and the race",
            r"The industry's machines; quantum amplitude estimation; the frontier",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan, in nineteen chapters. Monte Carlo, its error bar and its random numbers. The tricks that "
            "shrink the error. Quasi-random points and the Brownian bridge. Multilevel simulation. American options, "
            "bracketed from both sides. Greeks and adjoints. Grids in one and two dimensions. Fourier methods and the "
            "race. Then how banks run all this, what a quantum computer would buy, and the frontier."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data", "vol"))
        with self.voiceover(
            "This part supplies numerical pricing methods for the House. Each method has a defined scope and a different error diagnostic. <bookmark mark='a'/> The practical rule is to distinguish sampling uncertainty, discretization and truncation bias, reference error and model assumptions. A standard error alone does not certify a price's total accuracy."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
