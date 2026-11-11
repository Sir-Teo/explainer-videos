from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import firm as F
from videos.quant.quant34.common import (BAD, GOOD, HURDLE, PART, PEAK_C, PLAT_C, PM_C, PNL_C, STOP_C, fit_right,
                                         illustration, load)

SCOL = {0.0: GREY_B, 0.5: QC.SPOT, 1.0: QC.DELTA, 2.0: QC.GAIN}


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.reflect()
        self.solve()
        self.peak()
        self.theorem()
        self.grid(t)
        self.regimes()
        self.hist(t)
        self.sims(t)
        self.power(load("power"))
        self.design(load("power"))
        self.payoff(t)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How long a seat lasts", r"When does a manager of known skill first hit a drawdown stop?",
                          part=PART)
        self.add(c)
        with self.voiceover("For the researcher. We derive the continuous drawdown-stop formula for arithmetic Brownian profit with known constant parameters. Its peak at the stop is exponential; the stopping time generally is not. Grid simulations and deadline probabilities have different monitoring and uncertainty conventions. These conditional results do not forecast an actual manager's tenure."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"X_t", r"=", r"\mu t + \sigma W_t", font_size=38, colors={r"X_t": PNL_C}),
                cmath(r"M_t", r"=", r"\max_{s \le t} X_s,\qquad D_t = M_t - X_t", font_size=36, colors={r"M_t": PEAK_C}),
                cmath(r"\tau_d", r"=", r"\inf\{t : D_t \ge d\}", font_size=38, colors={r"\tau_d": STOP_C}),
                cmath(r"S = \mu/\sigma,\ \ \delta = d/\sigma", r":", r"\text{the Sharpe ratio and the stop, in volatilities}",
                      font_size=30)]
        whys = [why('arithmetic cumulative profit, with known constant $\\mu\\in\\mathbb R$, $\\sigma>0$ and $d>0$; not compounded wealth'),
                why(r"the running peak and the drawdown from it"),
                why(r"the stop: the first time the drawdown reaches $d$"),
                why('$S$ has units time$^{-1/2}$, $\\delta$ time$^{1/2}$; using annual numerical values fixes the time unit')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Specify the model and units. <bookmark mark='a'/> X starts at zero and is arithmetic cumulative profit, mu t plus sigma W t, with known constant real mu and positive sigma. This is not compounded wealth. <bookmark mark='b'/> The maximum includes time zero, and drawdown is peak minus profit. <bookmark mark='c'/> For positive fixed d, stop at the first continuous drawdown of d. <bookmark mark='d'/> S equals mu over sigma, with units inverse root time; delta equals d over sigma, with units root time. Their product is dimensionless. Numerical annual conventions make the resulting time a number of years."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def reflect(self):
        rows = [cmath(r"dD_t", r"=", r"-\mu\, dt - \sigma\, dW_t + dM_t", font_size=36),
                cmath(r"f(y)", r"=", r"\mathbb E_y[\tau_d]", font_size=36, colors={r"f(y)": STOP_C}),
                cmath(r"\tfrac{\sigma^2}{2} f'' - \mu f'", r"=", r"-1,\qquad f(d) = 0,\quad f'(0) = 0", font_size=34)]
        whys = [why(r"Lemma 1: the drawdown is a Brownian motion with drift $-\mu$, reflected at zero; it is pushed back "
                    r"up only when the P\&L makes a new peak, when $dM > 0$"),
                why(r"the expected time to the stop from a drawdown of $y$"),
                why(r"Dynkin's formula, as in Part 33: the generator applied to $f$ is minus one; zero at the stop; and "
                    r"reflection makes the slope zero at the peak")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Use a bounded candidate before assuming the expected time exists. <bookmark mark='a'/> Drawdown is reflected Brownian motion with drift minus mu on the interval from zero to d, killed at d. <bookmark mark='b'/> Solve for a nonnegative twice-differentiable function f on this compact interval. <bookmark mark='c'/> Its generator equals minus one, f at d is zero, and f prime at zero is zero. Ito's formula stopped at the smaller of t and tau cancels the reflection term, and gives expected truncated time at most f of y. Hence the expected stopping time is finite. Taking the limit then identifies f as that expectation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def solve(self):
        rows = [cmath(r"f'(y)", r"=", r"\frac{1 - e^{2\mu y/\sigma^2}}{\mu}", font_size=36),
                cmath(r"f(0)", r"=", r"-\int_0^d f'(y)\,dy = \frac{\sigma^2}{2\mu^2}\big(e^{a} - 1 - a\big)", font_size=34,
                      colors={r"f(0)": STOP_C}),
                cmath(r"a", r"=", r"\frac{2\mu d}{\sigma^2} = 2S\delta", font_size=36)]
        whys = [why(r"a first-order linear equation for $f'$: the constant solution $1/\mu$ plus a multiple of "
                    r"$e^{2\mu y/\sigma^2}$, fixed by $f'(0) = 0$"),
                why(r"integrate from the stop back to the peak"),
                why('dimensionless $a$ controls shape; the prefactor also sets absolute time, so $a$ alone does not determine lifetime')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "For nonzero mu, solve the first-order equation for f prime. <bookmark mark='a'/> The reflecting boundary gives one minus the exponential of two mu y over sigma squared, divided by mu. This derivative is nonpositive for either sign of mu. <bookmark mark='b'/> Integrate backwards from f at d equal zero. The bounded nonnegative solution at zero is sigma squared over two mu squared times e to the a minus one minus a. <bookmark mark='c'/> Here a is two mu d over sigma squared, or two S delta. It determines dimensionless shape; the prefactor carries time. Expanding the exponential gives d squared over sigma squared when mu tends to zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def peak(self):
        rows = [cmath(r"q(\epsilon)", r"=", r"\lambda\epsilon+o(\epsilon),\quad \lambda=\frac{2\mu/\sigma^2}{e^{2\mu d/\sigma^2}-1}", font_size=30),
                cmath(r"\Pr(M_\tau\ge x)", r"=", r"e^{-\lambda x}\quad(x\ge0),\qquad \mu=0:\ \lambda=1/d", font_size=30),
                cmath(r"X_\tau", r"=", r"M_\tau-d,\qquad \mathbb E[M_\tau]=1/\lambda", font_size=32),
                cmath(r"\mathbb E[X_\tau]", r"=", r"\mu\,\mathbb E[\tau],\qquad \mathbb E[\tau]<\infty", font_size=32)]
        whys = [why(r"bound the moving lower barrier between $-d$ and $\epsilon-d$ until the next peak; scale-function hitting probabilities have the same first-order rate"),
                why(r"strong Markov and translation invariance at each new peak give multiplicative survival; this is a clock in peak height, not in time"),
                why(r"continuity fixes the drawdown exactly at $d$; the maximum includes zero"),
                why(r"finite mean stopping time makes the stopped Brownian family $L^2$ bounded, allowing mean zero and Wald's identity")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover("The exponential law concerns the peak. <bookmark mark='a'/> Until the peak rises by epsilon, the moving drawdown boundary lies between minus d and epsilon minus d. Fixed-boundary scale-function hitting probabilities sandwich the stop probability and yield the same first-order rate lambda times epsilon. Do not identify a moving boundary with a fixed one for finite epsilon. <bookmark mark='b'/> Strong Markov and translation invariance at successive peak levels make peak survival multiplicative and continuous, hence exponential with rate lambda; at zero drift the rate is one over d. <bookmark mark='c'/> Continuity gives terminal profit equal to peak minus d. <bookmark mark='d'/> The finite mean time already proved makes stopped Brownian motion bounded in second moment. Its terminal mean is zero, so expected profit equals drift times expected time. The stopping time itself is generally not exponential.") as vo:
            step(0)
            for k,mk in enumerate(("a","b","c","d")):
                vo.wait_until(mk)
                if k:step(k)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\mathbb E[\tau_d] = \frac{e^{2S\delta} - 1 - 2S\delta}{2S^2},\qquad "
                            r"\mathbb E[M_\tau] = \sigma\,\frac{e^{2S\delta} - 1}{2S}", font_size=32),
                    MathTex(r"S = 0:\ \ \mathbb E[\tau] = \delta^2,\quad \mathbb E[M_\tau] = d;\qquad "
                            r"S\delta \gg 1:\ \ \mathbb E[\tau] \approx \frac{e^{2S\delta}}{2S^2}", font_size=30),
                    wrapped_label(r"in years, for annual $S$; the life of a seat grows exponentially in the product of the "
                                  r"Sharpe ratio and the stop's depth in volatilities, and quadratically in the depth when "
                                  r"there is no skill", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Drawdown stops (Taylor 1975; Lehoczky 1977)", st, r"this part's proof", width=11.8,
                            font_size=22)
        self.add(card)
        with self.voiceover(
            "The classical drawdown theorem applies to the specified continuous arithmetic Brownian model. <bookmark mark='a'/> For nonzero S, mean time is e to two S delta minus one minus two S delta, divided by two S squared. The peak has the exponential law and the mean displayed here. <bookmark mark='b'/> At zero drift, the limits are delta squared for time and d for peak. The leading exponential time expression requires large positive S delta, not just positive drift. Annual numerical inputs produce years. These known-parameter results omit estimation, changing exposure, jumps, fees and execution."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def grid(self, t):
        Ss, ds, G = t["S"], t["d"], np.asarray(t["grid"], float)
        cells = VGroup()
        for i, S in enumerate(Ss):
            for j, d in enumerate(ds):
                v = G[i, j]
                z = float(np.clip((math.log10(v) + 1) / 4, 0, 1))
                sq = Rectangle(width=1.6, height=0.62, fill_color=interpolate_color(ManimColor(RED_D), ManimColor(GREEN_D), z),
                               fill_opacity=0.85, stroke_color=GREY_D, stroke_width=1)
                sq.move_to([-2.6 + 1.65 * j, 1.7 - 0.68 * i, 0])
                txt = f"{v:.2f}" if v < 10 else (f"{v:.0f}" if v < 1000 else r"> 1000")
                cells.add(VGroup(sq, MathTex(txt, font_size=22).move_to(sq)))
        rl = VGroup(*[MathTex(rf"S = {S:g}", font_size=22).move_to([-4.6, 1.7 - 0.68 * i, 0]) for i, S in enumerate(Ss)])
        cl = VGroup(*[MathTex(rf"\delta = {d:g}", font_size=22).move_to([-2.6 + 1.65 * j, 2.4, 0]) for j, d in enumerate(ds)])
        head = label(r"Expected years to the stop", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"rows: the annual Sharpe ratio; columns: the stop, in annual volatilities (a 5\% stop at 10\% "
                             r"volatility is $\delta = 0.5$)", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        g1 = G[Ss.index(1.0)]
        g2 = G[Ss.index(2.0)]
        self.add(head, rl, cl, cells[0], foot)
        with self.voiceover(
            f"""Evaluate the exact formula under annual numerical conventions. <bookmark mark='a'/> At S one and delta point five, mean time is {g1[0]:.2f} years; at S two it is {g2[0]:.2f}. <bookmark mark='b'/> At delta one the corresponding means are {g1[2]:.2f} and {g2[2]:.2f}; at delta two, {g1[4]:.0f} and {g2[4]:.0f}. Both drift and depth matter, and very large values make finite-horizon simulation difficult. This grid does not prove that depth universally matters more than skill."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[:len(ds) * 3]], lag_ratio=0.04))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[len(ds) * 3:]], lag_ratio=0.04))
        self.wait(0.4)
        self.clear_scene()

    def regimes(self):
        rows = [cmath(r"S\delta \ll -1", r":", r"\mathbb E[\tau] \approx \delta/|S|", font_size=36, colors={r"S\delta \ll -1": BAD}),
                cmath(r"S = 0", r":", r"\mathbb E[\tau] = \delta^2", font_size=36),
                cmath(r"S\delta \gg 1", r":", r"\mathbb E[\tau] \approx e^{2S\delta}/(2S^2)", font_size=36, colors={r"S\delta \gg 1": GOOD})]
        whys = [why(r"a losing manager drifts to the stop: the time is the distance over the speed"),
                why(r"no skill: the diffusion alone; a stop one volatility deep takes a year on average"),
                why(r"a skilled manager must be unlucky to reach the stop, and the drift makes that exponentially rare: "
                    r"a large-deviation rate $2S\delta$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "These are limiting regimes, not a partition by sign alone. <bookmark mark='a'/> When S delta is strongly negative, the leading time is delta divided by absolute S. A small negative drift still needs the full formula. <bookmark mark='b'/> At exactly zero drift the time is delta squared. <bookmark mark='c'/> For large positive S delta, the leading term is the exponential divided by two S squared. The smooth exact expression connects all three cases. No sharp classification of an unknown manager follows from a finite path."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def hist(self, t):
        taus = np.asarray(t["hist"], float)
        th = F.stop_time_sharpe(1.0, 1.0)
        edges = np.linspace(0, 20, 41)
        h, _ = np.histogram(taus, bins=edges, density=True)
        top = float(np.ceil(h.max() * 10) / 10)
        g = axes([0, 20], [0, top], x_length=7.4, y_length=4.2, xlabel=r"years to the stop ($S = 1$, $\delta = 1$)",
                 ylabel=r"density", xticks=[0, 5, 10, 15, 20], yticks=[0, top], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(edges[k + 1], 0)[0] - ax.c2p(edges[k], 0)[0],
                                  height=max(1e-3, ax.c2p(0, h[k])[1] - ax.c2p(0, 0)[1]), fill_color=STOP_C,
                                  fill_opacity=0.6, stroke_width=0).move_to(ax.c2p((edges[k] + edges[k + 1]) / 2, h[k] / 2))
                        for k in range(len(h))])
        mline = DashedLine(ax.c2p(th, 0), ax.c2p(th, top), color=HURDLE, stroke_width=2)
        med = float(np.median(taus))
        long_share = 100 * float(np.mean(taus > 2 * th))
        sim_mean = float(np.mean(taus))
        st = VGroup(label(rf"theorem's mean {th:.2f} years", font_size=17, color=HURDLE),
                    label(rf"simulated mean {sim_mean:.2f}", font_size=17, color=GREY_A),
                    label(rf"median {med:.2f}", font_size=17, color=GREY_A),
                    label(rf"{long_share:.0f}\% last twice the mean", font_size=17, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        self.add(g, bars[0])
        with self.voiceover(
            f"""The cached six thousand grid-monitored paths have stop times from about point zero eight to nineteen point nine five years; all are shown over zero to twenty without clipping the tail. <bookmark mark='a'/> The continuous known-parameter mean is {th:.2f} years. <bookmark mark='b'/> The cached mean is {sim_mean:.2f}, median {med:.2f}, and about {long_share:.0f} percent exceed twice the continuous mean. Grid monitoring delays detection; sampling variation also matters. This is a stopping-time histogram, not the exponential peak law, and we do not claim an exact exponential time distribution. The general simulation helper excludes nonstoppers from reported stop-time means, so other parameter choices require censoring review."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(Create(mline), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def sims(self, t):
        rows = t["sims"]
        hx = [-4.8, -3.2, -1.4, 0.6, 2.6, 4.8]
        head = VGroup(label(r"$S$", font_size=17, color=GREY_B), label(r"$\delta$", font_size=17, color=GREY_B),
                      label(r"theorem", font_size=17, color=GOOD), label(r"daily steps", font_size=17, color=GREY_B),
                      label(r"extrapolated", font_size=17, color=HURDLE), label(r"peak: theorem, sim", font_size=17,
                                                                               color=PEAK_C))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['S']:g}", font_size=22), MathTex(f"{r['d']:g}", font_size=22),
                           MathTex(f"{r['theory']:.3f}", font_size=22), MathTex(f"{r['sim_daily']:.3f}", font_size=22),
                           MathTex(f"{r['extrap']:.3f}", font_size=22),
                           MathTex(rf"{r['peak_theory']:.2f},\ {r['peak_extrap']:.2f}", font_size=22)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.3 - 0.62 * j, 0])
        foot = wrapped_label('4{,}000 paths per grid, independent seeds; heuristic $\\sqrt{\\Delta t}$ extrapolation, no error bars; all six displayed fine-grid stopped fractions are one', 11.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        r = rows[3]
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"""The unchanged simulation uses four thousand paths per grid. <bookmark mark='a'/> At S one and delta one, daily monitoring gives {r['sim_daily']:.2f} years versus continuous mean {r['theory']:.2f}. <bookmark mark='b'/> Combining daily and eighth-day grids using a chosen square-root-step extrapolation gives {r['extrap']:.2f}. The grids have independent seeds and there are no Monte Carlo error bars here. Extrapolation is heuristic, not a proven error bound; deviations are not uniformly tiny. Every selected fine-grid row stopped by its horizon, but the general helper omits survivors from its means. High drift or deep barriers can produce severe censoring."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:4])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[4:])) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def power(self, pw):
        rows = pw["rows"]
        Ss = [r["S"] for r in rows]
        g = axes([-1.0, 2.0], [0, 100], x_length=7.4, y_length=4.2, xlabel=r"the manager's true Sharpe ratio",
                 ylabel=r"stopped within 3 years, \%", xticks=[-1, 0, 1, 2], yticks=[0, 50, 100],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, Ss, [100 * r["d1.0_3y"] for r in rows], STOP_C, stroke_width=3)
        c2 = curve(ax, Ss, [100 * r["d1.5_3y"] for r in rows], PLAT_C, stroke_width=3)
        d1 = VGroup(*[Dot(ax.c2p(r["S"], 100 * r["d1.0_3y"]), radius=0.06, color=STOP_C) for r in rows])
        d2 = VGroup(*[Dot(ax.c2p(r["S"], 100 * r["d1.5_3y"]), radius=0.06, color=PLAT_C) for r in rows])
        leg = legend([(STOP_C, r"stop 1 volatility deep"), (PLAT_C, r"stop 1.5 volatilities deep")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        pr = {r["S"]: r for r in rows}
        self.add(g, leg, c1)
        with self.voiceover(
            f"""These are simulated three-year stop frequencies, with all original six thousand paths retained in each probability denominator. <bookmark mark='a'/> At depth one, the S zero frequency is {100*pr[0.0]['d1.0_3y']:.0f} percent and S one is {100*pr[1.0]['d1.0_3y']:.0f} percent. <bookmark mark='b'/> At depth one point five they become {100*pr[0.0]['d1.5_3y']:.0f} and {100*pr[1.0]['d1.5_3y']:.0f} percent. To call these errors and power, specify for example a simple null S one, alternative S zero, and reject the null when stopped by three years. A deeper barrier lowers both rejection probabilities. It is not automatically a sharper test at equal significance."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(d1))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(d2))
        self.wait(0.4)
        self.clear_scene()

    def design(self, pw):
        pr = {r["S"]: r for r in pw["rows"]}
        rows = [cmath(r"\text{type I}", r":", r"\text{firing a skilled manager}", font_size=34, colors={r"\text{type I}": BAD}),
                cmath(r"\text{type II}", r":", r"\text{keeping one without skill}", font_size=34, colors={r"\text{type II}": BAD}),
                cmath(r"\delta = d/\sigma", r":", r"\text{set the budget, not just the stop}", font_size=34,
                      colors={r"\delta = d/\sigma": GOOD})]
        whys = [why(rf"a Sharpe-1 manager fired within three years: {100 * pr[1.0]['d1.0_3y']:.0f}\% at $\delta = 1$, "
                    rf"{100 * pr[1.0]['d1.5_3y']:.0f}\% at 1.5"),
                why(rf"a Sharpe-0 manager kept for three years: {100 * (1 - pr[0.0]['d1.0_3y']):.0f}\% at $\delta = 1$, "
                    rf"{100 * (1 - pr[0.0]['d1.5_3y']):.0f}\% at 1.5"),
                why(r"the same 7.5\% stop is a different test at 10\% and at 5\% volatility; a platform designs the test "
                    r"through the volatility budget it gives each manager")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Fix a simple null of S one, alternative S zero, and rejection on stopping within three years. <bookmark mark='a'/> Under that convention, firing under the null is type one error; retaining the alternative is type two error. <bookmark mark='b'/> A deeper barrier trades lower false rejection for lower power at the same deadline. An equal-significance comparison requires calibration, and unknown composite skill needs more work. <bookmark mark='c'/> Stop depth, volatility, horizon, costs and the decision objective all matter. A changed risk budget also changes the experiment; these frequencies alone do not establish an optimal live policy."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def payoff(self, t):
        rows = [cmath(r"\mathbb E[X_\tau]", r"=", r"\mu\,\mathbb E[\tau]", font_size=38, colors={r"\mathbb E[X_\tau]": PNL_C}),
                cmath(r"S = 1,\ \delta = 0.5", r":", rf"\mathbb E[X_\tau] = {F.peak_at_stop(1.0, 1.0, 0.5) - 0.5:.2f}\,\sigma",
                      font_size=34),
                cmath(r"S = 1,\ \delta = 1.5", r":", rf"\mathbb E[X_\tau] = {F.peak_at_stop(1.0, 1.0, 1.5) - 1.5:.2f}\,\sigma",
                      font_size=34)]
        whys = [why(r"the expected P\&L of a seat until its stop: positive for a skilled manager, by Wald's identity"),
                why(r"with a shallow stop, a good manager earns a third of a volatility before being stopped"),
                why(r"with a deep one, eight volatilities: the platform keeps the edge far longer; what it pays is more "
                    r"time with the bad managers")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        a1 = F.peak_at_stop(1.0, 1.0, 0.5) - 0.5
        a3 = F.peak_at_stop(1.0, 1.0, 1.5) - 1.5
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Under the known Brownian arithmetic-profit model, finite mean stopping time permits Wald's identity. <bookmark mark='a'/> Expected terminal profit equals mu times expected time. <bookmark mark='b'/> At S one and delta point five it is {a1:.2f} annual-volatility units; <bookmark mark='c'/> at delta one point five, {a3:.2f}. These are stopped arithmetic profits before costs, not annual investor returns or a complete value objective. Deeper stops retain both favorable and unfavorable drifts longer; replacement, capital, risk and learning determine a platform's decision."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Taylor (1975); Lehoczky (1977)", r"the stopped-at-a-drawdown problem for diffusions, and the "
                          r"exponential law of the maximum at the stop", width=12.4, font_size=26),
            desk_question(r"Grossman and Zhou (1993)", r"the investor who must never lose more than a fraction of the peak "
                          r"(Part 8): the optimal policy scales risk with the cushion above the floor", width=12.4,
                          font_size=26),
            desk_question(r"Magdon-Ismail et al. (2004)", r"the expected maximum drawdown of Brownian motion with drift "
                          r"over a fixed horizon, the other half of the question a manager asks", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Howard Taylor and John Lehoczky solved the stopped-at-a-drawdown "
            "problem in the 1970s. <bookmark mark='b'/> Sanford Grossman and Zhongquan Zhou found how an investor who "
            "must never fall below a fraction of the peak should invest: Part eight's floor. <bookmark mark='c'/> And "
            "Malik Magdon-Ismail and co-authors computed the expected maximum drawdown over a fixed horizon, the other "
            "question a manager asks."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the optimal stop under learning", 'with a prior over skill, the stop is a sequential test with a cost of waiting; the Bayes-optimal boundary, a function of time and record, needs a fully specified payoff and observation model; it is not solved here', width=12.4, font_size=26),
            desk_question(r"open: managers who see the stop", 'near the stop a manager may cut risk, or gamble; the equilibrium of a stop rule with a strategic manager and a convex payout is not analyzed here',
                          width=12.4, font_size=26),
            desk_question(r"open: dependent returns", 'Chapter 10 raised research questions about timing and dependence; the stop time for returns with slow regimes, and the best stop for them, need more than Brownian motion',
                          width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Three extensions lie beyond this derivation. <bookmark mark='a'/> Unknown skill requires a specified prior, observation model, objective and cost of waiting before optimizing a boundary. <bookmark mark='b'/> A manager who changes exposure in response to a stop changes the stochastic model and incentives. <bookmark mark='c'/> Dependent returns, regimes, jumps and implementation costs need their own analysis. This lesson solves none of these extensions and does not claim that every version is globally unsolved."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('S=1.5,\\quad \\sigma=0.04,\\quad d=0.06,\\quad \\delta=d/\\sigma,\\quad \\mathbb E[X_\\tau]=\\mu\\mathbb E[\\tau]', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Known constant annual Brownian arithmetic-profit parameters, continuous monitoring, peak includes zero. Compute mean time in years and expected profit as a fraction of initial capital, before costs.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. Under the known continuous Brownian arithmetic-profit model, annual Sharpe is one point five, volatility four percent and stop six percent of initial capital. Compute delta, expected time and expected terminal profit before costs.'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
