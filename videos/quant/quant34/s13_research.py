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
        with self.voiceover("For the researcher. Every platform runs drawdown stops, and every manager wants to know the "
                            "odds. This chapter derives the expected time to a stop exactly, and the profit earned before "
                            "it, and reads the stop as a statistical test."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"X_t", r"=", r"\mu t + \sigma W_t", font_size=38, colors={r"X_t": PNL_C}),
                cmath(r"M_t", r"=", r"\max_{s \le t} X_s,\qquad D_t = M_t - X_t", font_size=36, colors={r"M_t": PEAK_C}),
                cmath(r"\tau_d", r"=", r"\inf\{t : D_t \ge d\}", font_size=38, colors={r"\tau_d": STOP_C}),
                cmath(r"S = \mu/\sigma,\ \ \delta = d/\sigma", r":", r"\text{the Sharpe ratio and the stop, in volatilities}",
                      font_size=30)]
        whys = [why(r"the manager's cumulative P\&L: drift $\mu$ is skill, $\sigma$ the volatility budget, both annual"),
                why(r"the running peak and the drawdown from it"),
                why(r"the stop: the first time the drawdown reaches $d$"),
                why(r"the problem has two numbers only: how good the manager is, and how deep the stop is in units of "
                    r"their own volatility")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The setup. <bookmark mark='a'/> A manager's cumulative profit is Brownian motion with drift: the drift is "
            "skill, the volatility is the budget. <bookmark mark='b'/> Its running peak, and the drawdown from the peak. "
            "<bookmark mark='c'/> The stop is the first time the drawdown reaches d. <bookmark mark='d'/> Scaling time "
            "and money, only two numbers matter: the Sharpe ratio, and the stop's depth in units of the manager's own "
            "volatility."
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
        with self.voiceover(
            "Lemma one. <bookmark mark='a'/> The drawdown moves like the profit, reversed, except that at zero it is "
            "pushed back up: whenever the profit makes a new peak. It is a reflected Brownian motion with drift minus "
            "mu. <bookmark mark='b'/> Let f of y be the expected time to the stop from a drawdown of y. "
            "<bookmark mark='c'/> Dynkin's formula, exactly as in Part thirty-three: the generator applied to f is minus "
            "one; f is zero at the stop; and the reflection at the peak makes its slope zero there."
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
                why(r"the whole answer depends on one number, twice the Sharpe ratio times the stop in volatilities")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The solution is two lines. <bookmark mark='a'/> The equation is first order in the slope: a constant, one "
            "over mu, plus an exponential, fixed by the zero slope at the peak. <bookmark mark='b'/> Integrate from the "
            "stop back to the peak, and the expected time to the stop is sigma squared over two mu squared, times e to "
            "the a, minus one, minus a. <bookmark mark='c'/> And a is twice the Sharpe ratio times the stop's depth in "
            "volatilities. One number decides everything."
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
        rows = [cmath(r"\Pr(\text{fall } d \text{ before rising } \epsilon)", r"=", r"\frac{s(\epsilon) - s(0)}{s(\epsilon) - s(-d)} "
                      r"\approx \lambda\,\epsilon", font_size=30),
                cmath(r"\lambda", r"=", r"\frac{2\mu/\sigma^2}{e^{a} - 1}", font_size=36),
                cmath(r"M_{\tau}", r"\sim", r"\text{Exp}(\lambda),\quad \mathbb E[M_\tau] = \frac{\sigma^2}{2\mu}\big(e^a - "
                      r"1\big)", font_size=32, colors={r"M_{\tau}": PEAK_C}),
                cmath(r"\mathbb E[X_\tau]", r"=", r"\mathbb E[M_\tau] - d = \mu\,\mathbb E[\tau]", font_size=34)]
        whys = [why(r"Lemma 2: at each new peak the process starts afresh; with the scale function "
                    r"$s(x) = e^{-2\mu x/\sigma^2}$, the chance of a stop before the peak rises by $\epsilon$"),
                why(r"so stops arrive at a constant rate per unit of new peak: a memoryless clock in the peak, not in time"),
                why(r"the peak at the stop is exponential (Lehoczky 1977)"),
                why(r"the P\&L when stopped is the peak less the stop, and Wald's identity checks it against the "
                    r"expected time")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Lemma two: how much the manager makes before the stop. <bookmark mark='a'/> At every new peak the process "
            "starts afresh. The scale function gives the chance of falling d before the peak rises a little further: "
            "proportional to that little bit. <bookmark mark='b'/> So stops arrive at a constant rate per unit of new "
            "peak. <bookmark mark='c'/> The peak reached before the stop is therefore exponential, with this mean. "
            "<bookmark mark='d'/> The profit at the stop is the peak less d, and Wald's identity, the drift times the "
            "expected time, gives the same number: a check on both lemmas."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
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
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> In years, with an annual Sharpe ratio S and a stop delta volatilities "
            "deep, the expected time to the stop is e to the two S delta, minus one, minus two S delta, over two S "
            "squared; the expected peak before it has the same exponential. <bookmark mark='b'/> With no skill, the "
            "time is delta squared, the diffusion's own scale. With a lot of skill, it grows exponentially in S times "
            "delta. These formulas are classical, Taylor's in 1975 and Lehoczky's in 1977; the proof here is the "
            "series' own."
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
        with self.voiceover(
            "The formula as a table. <bookmark mark='a'/> Rows are Sharpe ratios, columns the stop in volatilities. A "
            f"five percent stop on a ten percent volatility budget is half a volatility: a Sharpe-one manager lasts "
            f"{g1[0]:.2f} years on average, a Sharpe-two manager {g2[0]:.2f}. <bookmark mark='b'/> One volatility deep, "
            f"{g1[2]:.1f} and {g2[2]:.1f} years. Two volatilities deep, {g1[4]:.0f} and {g2[4]:.0f}. The depth of the "
            "stop, relative to the volatility, matters far more than the manager's skill."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[:len(ds) * 3]], lag_ratio=0.04))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[len(ds) * 3:]], lag_ratio=0.04))
        self.wait(0.4)
        self.clear_scene()

    def regimes(self):
        rows = [cmath(r"S < 0", r":", r"\mathbb E[\tau] \approx \delta/|S|", font_size=36, colors={r"S < 0": BAD}),
                cmath(r"S = 0", r":", r"\mathbb E[\tau] = \delta^2", font_size=36),
                cmath(r"S > 0", r":", r"\mathbb E[\tau] \approx e^{2S\delta}/(2S^2)", font_size=36, colors={r"S > 0": GOOD})]
        whys = [why(r"a losing manager drifts to the stop: the time is the distance over the speed"),
                why(r"no skill: the diffusion alone; a stop one volatility deep takes a year on average"),
                why(r"a skilled manager must be unlucky to reach the stop, and the drift makes that exponentially rare: "
                    r"a large-deviation rate $2S\delta$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Three regimes. <bookmark mark='a'/> A losing manager drifts to the stop: the time is the distance over the "
            "speed. <bookmark mark='b'/> A manager without skill reaches it by diffusion alone: a stop one volatility "
            "deep takes a year on average. <bookmark mark='c'/> A skilled manager reaches it only by bad luck, and the "
            "drift makes that exponentially rare: a large-deviation rate of twice S delta. That asymmetry is what lets a "
            "stop tell the three apart."
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
        edges = np.linspace(0, 10, 41)
        h, _ = np.histogram(np.clip(taus, 0, 9.999), bins=edges, density=True)
        top = float(np.ceil(h.max() * 10) / 10)
        g = axes([0, 10], [0, top], x_length=7.4, y_length=4.2, xlabel=r"years to the stop ($S = 1$, $\delta = 1$)",
                 ylabel=r"density", xticks=[0, 2, 4, 6, 8, 10], yticks=[0, top], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
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
        with self.voiceover(
            "The distribution behind the mean. <bookmark mark='a'/> Six thousand simulated Sharpe-one managers with a "
            "stop one volatility deep. <bookmark mark='b'/> The mean matches the theorem, but the median is only "
            f"{med:.1f} years, and {long_share:.0f} percent of managers last more than twice the mean. "
            "The stop time is roughly exponential: most good managers are stopped early, by luck, and a few last for "
            "a decade."
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
        foot = wrapped_label(r"4{,}000 paths at daily and eighth-of-a-day steps, extrapolated linearly in $\sqrt{\Delta t}$ "
                             r"to continuous monitoring; time in years, peak in volatilities", 11.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        r = rows[3]
        with self.voiceover(
            "Checked by simulation. <bookmark mark='a'/> With daily steps, the simulated time is too long: a daily "
            "check notices the drawdown late, the same bias as Part thirty-three's bands. For a Sharpe ratio of one and "
            f"a stop one volatility deep, {r['sim_daily']:.2f} years against the theorem's {r['theory']:.2f}. "
            "<bookmark mark='b'/> Extrapolating two step sizes to continuous monitoring gives "
            f"{r['extrap']:.2f}, and every row comes within a few percent, peaks included."
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
        with self.voiceover(
            "The stop as a test. <bookmark mark='a'/> The chance a manager is stopped within three years, by true "
            f"Sharpe ratio. With a stop one volatility deep, a manager without skill is stopped {100 * pr[0.0]['d1.0_3y']:.0f} "
            f"percent of the time, but so is a Sharpe-one manager, {100 * pr[1.0]['d1.0_3y']:.0f} percent: a test with "
            "little power. <bookmark mark='b'/> One and a half volatilities deep, "
            f"{100 * pr[0.0]['d1.5_3y']:.0f} percent against {100 * pr[1.0]['d1.5_3y']:.0f}: a much sharper test, at the "
            "price of letting losing managers run longer."
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
        with self.voiceover(
            "Designing the test. <bookmark mark='a'/> Two errors: firing a skilled manager, and keeping one without "
            "skill. <bookmark mark='b'/> A deeper stop makes the first rarer and the second more common. "
            "<bookmark mark='c'/> And depth is measured in volatilities, so the same seven and a half percent stop is a "
            "different test at ten percent volatility and at five. A platform designs its test mostly through the "
            "volatility budget it gives each manager."
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
        with self.voiceover(
            "What a seat earns before its stop. <bookmark mark='a'/> By Wald's identity, the drift times the expected "
            f"time. <bookmark mark='b'/> With a stop half a volatility deep, a Sharpe-one manager earns {a1:.2f} "
            f"volatilities before being stopped. <bookmark mark='c'/> One and a half volatilities deep, {a3:.1f}. A "
            "shallow stop throws away most of a good manager's value; its benefit is that it also throws away the bad "
            "ones quickly. Chapter three's simulation is this trade-off, with skill drawn from a pool."
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
                          r"exponential law of the maximum at the stop", width=12.4, font_size=18),
            desk_question(r"Grossman and Zhou (1993)", r"the investor who must never lose more than a fraction of the peak "
                          r"(Part 8): the optimal policy scales risk with the cushion above the floor", width=12.4,
                          font_size=18),
            desk_question(r"Magdon-Ismail et al. (2004)", r"the expected maximum drawdown of Brownian motion with drift "
                          r"over a fixed horizon, the other half of the question a manager asks", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
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
            desk_question(r"open: the optimal stop under learning", r"with a prior over skill, the stop is a sequential "
                          r"test with a cost of waiting; the Bayes-optimal boundary, a function of time and record, has no "
                          r"closed form for platform payoffs", width=12.4, font_size=18),
            desk_question(r"open: managers who see the stop", r"near the stop a manager may cut risk, or gamble; the "
                          r"equilibrium of a stop rule with a strategic manager and a convex payout is unsolved",
                          width=12.4, font_size=18),
            desk_question(r"open: dependent returns", r"Chapter 10 found premia whose losses persist; the stop time for "
                          r"returns with slow regimes, and the best stop for them, need more than Brownian motion",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With a prior over skill, the stop is a sequential test with a "
            "cost of waiting; the optimal boundary, a function of time and record, has no closed form for a platform's "
            "payoffs. <bookmark mark='b'/> A manager who can see the stop may cut risk near it, or gamble; the "
            "equilibrium with a strategic manager and a convex payout is unsolved. <bookmark mark='c'/> And Chapter ten "
            "found premia whose losses persist, for which Brownian motion is the wrong model."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a manager with Sharpe 1.5 runs 4\% volatility under a 6\% stop. What is the expected time to the "
                       r"stop, and the expected P\&L before it?")
        with self.voiceover(
            "Pause and predict. A manager with a Sharpe ratio of one and a half runs four percent volatility under a six "
            "percent stop. What is the expected time to the stop, and the expected profit before it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
