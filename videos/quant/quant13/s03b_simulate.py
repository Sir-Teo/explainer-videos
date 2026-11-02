from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, simulated

LAB_QE = [
    "m = theta + (v - theta) * E                 # exact mean",
    "s2 = v*xi**2*E/kappa*(1-E) + theta*xi**2/(2*kappa)*(1-E)**2",
    "psi = s2 / (m * m)",
    "quad = psi <= psi_c                         # 1.5",
    "b2 = 2/psi - 1 + sqrt(2/psi) * sqrt(2/psi - 1)",
    "vn[quad] = m/(1 + b2) * (sqrt(b2) + Z)**2   # squared Gaussian",
    "p = (psi - 1) / (psi + 1)                   # mass at zero",
    "beta = (1 - p) / m",
    "vn[~quad] = where(U <= p, 0, log((1-p)/(1-U)) / beta)",
    "x += K0 + k1*v + k2*vn + sqrt(k3*v + k4*vn) * Z2",
]


class Simulate(VoiceoverScene):
    def construct(self):
        qd = load("qe_density")
        q = load("qe")
        self.card()
        self.onestep(qd)
        self.feller(qd)
        self.derive()
        self.lab(q, qd)
        self.qe(q)
        self.cards()

    def card(self):
        c = chapter_card(5, r"Heston III: simulating it honestly", r"How do you take one step of a variance that hits zero?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter five. Feller's condition, and simulating Heston honestly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _panel(self, h, key, title, col, top=0.12):
        e = np.asarray(h["edges"])
        x0, x1 = float(e[0]), float(e[-1])
        a = axes([x0, x1], [0, top], x_length=3.9, y_length=3.0, xlabel=r"next week's variance",
                 xticks=[0, round(x1 / 2, 1), round(x1, 1)], yticks=[0, top / 2, top], yfmt=lambda u: f"{u:.2f}",
                 font_size=13)
        vals = np.asarray(h[key])
        bars = VGroup()
        for lo, hi, p in zip(e[:-1], e[1:], vals):
            if p <= 0:
                continue
            hgt = abs(a.ax.c2p(0, min(p, top))[1] - a.ax.c2p(0, 0)[1])
            bars.add(Rectangle(width=abs(a.ax.c2p(hi, 0)[0] - a.ax.c2p(lo, 0)[0]) * 0.92, height=max(hgt, 1e-3),
                               stroke_width=0, fill_color=BAD if hi <= 0 else col, fill_opacity=0.8)
                     .move_to(a.ax.c2p((lo + hi) / 2, min(p, top) / 2)))
        ex = np.asarray(h["exact"])
        pts = []
        for lo, hi, p in zip(e[:-1], e[1:], ex):
            pts += [a.ax.c2p(lo, min(p, top)), a.ax.c2p(hi, min(p, top))]
        exact = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_as_corners(pts)
        t = label(title, font_size=18, color=col).next_to(a, UP, buff=0.12)
        zero = DashedLine(a.ax.c2p(0, 0), a.ax.c2p(0, top), stroke_color=GREY_C, stroke_width=1.5)
        return VGroup(a, zero, bars, exact, t)

    def onestep(self, qd):
        h1, h2 = qd["hist"]["0.05"], qd["hist"]["0.5"]
        p1 = self._panel(h1, "euler_raw", r"Euler, from $v = 0.05$", BAD)
        p2 = self._panel(h1, "qe", r"QE, from $v = 0.05$", RV)
        p3 = self._panel(h2, "qe", r"QE, from $v = 0.5$", RV, top=0.06)
        P = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.7)
        r = {(round(z["v"], 3), z["dt"]): z for z in qd["rows"]}
        a = r[(0.05, "week")]
        b = r[(0.5, "week")]
        spike1 = label(rf"spike: {h1['exact'][int(np.argmax(np.asarray(h1['edges'])[:-1] >= 0))]:.2f}", font_size=16,
                       color=WHITE).next_to(p1[0].ax.c2p(0.05, 0.12), UP, buff=0.02)
        spike2 = label(rf"atom at 0: {a['zero_qe']:.2f}", font_size=16, color=RV).next_to(p2[0].ax.c2p(0.05, 0.12), UP,
                                                                                           buff=0.02)
        foot = VGroup(
            wrapped_label(rf"one weekly step of the fitted variance, {qd['N']:,} draws each; white: the exact law (a scaled "
                          r"non-central $\chi^2$), probability per bin; bars clipped at the top".replace(",", "{,}"),
                          12.4, 19, GREY_A),
            MathTex(rf"\text{{Euler: }} {100 * a['neg']:.0f}\%\ \text{{of draws below zero}};\quad "
                    rf"\text{{mean}}\ {a['mean_euler']:.3f}\ \text{{vs exact}}\ {a['mean_exact']:.3f};\quad "
                    rf"\text{{QE}}\ {a['mean_qe']:.3f}", font_size=28),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To price exotics, desks simulate. So take one step of Heston's variance, a week long, starting from a "
            "low variance, zero point zero five, with our fitted parameters, and draw a hundred thousand times. The "
            "white outline is the exact distribution of next week's variance: a scaled non-central chi-squared, "
            "piled up against zero. <bookmark mark='a'/> The plain Euler step adds a Gaussian shock to the "
            f"variance, and {100 * a['neg']:.0f} percent of the draws land below zero: variance cannot be negative. "
            "Floor them at zero, and the mean comes out at "
            f"{a['mean_euler']:.3f} instead of the exact {a['mean_exact']:.3f}. The bias compounds every step. "
            "<bookmark mark='b'/> Leif Andersen's quadratic-exponential scheme, QE, does something smarter. Near "
            f"zero, it puts a point mass at zero, here {a['zero_qe']:.2f}, and an exponential tail above it, sized "
            f"so that the mean and variance are exactly right: mean {a['mean_qe']:.3f}. <bookmark mark='c'/> "
            "Started high, at zero point five, the variance is far from zero, and QE switches to its other branch: "
            "a scaled, shifted Gaussian squared, which matches the exact law almost perfectly."
        ) as vo:
            self.play(FadeIn(p1[0]), FadeIn(p1[1]), FadeIn(p1[4]), Create(p1[3]), FadeIn(foot[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p1[2]], lag_ratio=0.02), FadeIn(spike1),
                      FadeIn(foot[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(p2[0]), FadeIn(p2[1]), FadeIn(p2[4]), Create(p2[3]),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p2[2]], lag_ratio=0.02), FadeIn(spike2), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(p3[0]), FadeIn(p3[1]), FadeIn(p3[4]), Create(p3[3]),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p3[2]], lag_ratio=0.02), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def feller(self, qd):
        v0, kappa, theta, xi, rho = qd["params"]
        fel = 2 * kappa * theta / xi ** 2
        rows_ = qd["rows"]
        tab = VGroup(*[MathTex(rf"v = {z['v']:.2f},\ \text{{{z['dt']}}}:\ \ W_1^{{\text{{Euler}}}} = {z['w1_euler']:.4f},\ \ "
                               rf"W_1^{{\text{{QE}}}} = {z['w1_qe']:.4f}", font_size=24,
                               color=RV if z['w1_qe'] < z['w1_euler'] else BAD) for z in rows_])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        row = cmath(r"\frac{2\kappa\theta}{\xi^2}", r"=", rf"{fel:.2f} < 1", font_size=40, colors={r"\frac{2\kappa\theta}{\xi^2}": BAD})
        w = why(r"Feller's test (Part 5): below one, the variance reaches zero with positive probability; the exact law "
                r"then piles up a spike at zero, the hardest case for any scheme", 22)
        top = VGroup(row, w).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.5)
        tab.next_to(top, DOWN, buff=0.45)
        ratio = float(np.median([z["w1_euler"] / z["w1_qe"] for z in rows_]))
        foot = wrapped_label(r"$W_1$, the transport distance to the exact law: how far probability must move. (The "
                             r"Kolmogorov distance punishes QE's atom at zero, which the exact law smears into a spike "
                             r"of the same mass; the transport distance does not.)", 12.0, 19, GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Why is this hard at all? Feller's ratio, two kappa theta over xi squared, is {fel:.2f} on our fit, below "
            "one. By Part five's boundary test, the variance then touches zero with positive probability, and its "
            "exact law has that spike at zero. <bookmark mark='a'/> So measure each scheme by how far its draws are "
            "from the exact law: the transport distance, how far probability has to move to turn one into the other. "
            "Three starting variances, three step sizes, a day, a week and a month. <bookmark mark='b'/> QE is closer "
            f"in every one of the nine cases, by a median factor of {ratio:.0f}. Pause and predict: if Feller held, would "
            "Euler be fine? Better, but still biased: QE's advantage is largest exactly when Feller fails."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.1) for t_ in tab], lag_ratio=0.15, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"m", r"=", r"\theta + (v - \theta)\,e^{-\kappa\Delta},\quad s^2 = \frac{v\xi^2 e^{-\kappa\Delta}}{\kappa}"
                      r"\big(1 - e^{-\kappa\Delta}\big) + \frac{\theta\xi^2}{2\kappa}\big(1 - e^{-\kappa\Delta}\big)^2",
                      font_size=30, colors={r"m": VAR}),
                cmath(r"\psi", r"=", r"s^2/m^2", font_size=36, colors={r"\psi": VAR}),
                cmath(r"v'", r"=", r"a\,(b + Z)^2,\quad b^2 = \tfrac2\psi - 1 + \sqrt{\tfrac2\psi}\sqrt{\tfrac2\psi - 1},"
                      r"\quad a = \frac{m}{1 + b^2}\qquad (\psi \le 1.5)", font_size=30, colors={r"v'": RV}),
                cmath(r"v'", r"=", r"\begin{cases} 0 & \text{prob. } p = \frac{\psi - 1}{\psi + 1} \\ "
                      r"\text{Exp}(\beta),\ \beta = \frac{1 - p}{m} & \text{otherwise}\end{cases}\qquad (\psi > 1.5)",
                      font_size=30, colors={r"v'": RV}),
                cmath(r"\ln S'", r"=", r"\ln S + \tfrac{\rho}{\xi}\big(v' - v - \kappa\theta\Delta\big) + "
                      r"\big(\tfrac{\kappa\rho}{\xi} - \tfrac12\big)\!\int\! v + \sqrt{1 - \rho^2}\!\int\!\sqrt v\,dW^\perp",
                      font_size=30, colors={r"\ln S'": SPOT})]
        whys = [why(r"the exact conditional mean and variance of CIR over one step (Part 5)", 20),
                why(r"how wide the next variance is, relative to its mean", 20),
                why(r"small $\psi$: a scaled non-central $\chi^2$ with one degree of freedom, matching $m$ and $s^2$", 20),
                why(r"large $\psi$: a mass at zero plus an exponential, matching $m$ and $s^2$ (two equations, two unknowns)",
                    20),
                why(r"solve the variance equation for $\int\sqrt v\,dW^2$ and substitute; integrals by the trapezoid; "
                    r"a constant $K_0^*$ keeps $S$ a martingale exactly (Andersen 2008)", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            "Here is QE, derived. Over one step of length delta, the variance's conditional mean m and variance s "
            "squared are known exactly: they are Part five's CIR moments. <bookmark mark='a'/> Their ratio, psi, says "
            "how wide the next variance is relative to its mean. <bookmark mark='b'/> When psi is small, draw the "
            "next variance as a constant times a shifted Gaussian squared. The two constants, a and b, are fixed by "
            "two equations: match the mean, match the variance. <bookmark mark='c'/> When psi is large, the variance "
            "is near zero: draw zero with probability p, and otherwise an exponential with rate beta, again two "
            "unknowns fixed by the two moments. Andersen switches at psi equal to one and a half. "
            "<bookmark mark='d'/> Then the price. Solve the variance equation for the stochastic integral that "
            "drives it, and substitute: the correlated part of the log price becomes a function of the start and end "
            "variances, and only the orthogonal part needs a fresh Gaussian. One more constant makes the discrete "
            "price an exact martingale."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, q, qd):
        card = lab_card(r"Andersen's QE step", LAB_QE, source="explainer/quant/house/stochvol.py: heston_qe",
                        width=8.6).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.4)
        rows = q["rows"]

        def row(n, scheme):
            z = next(r for r in rows if r["scheme"] == scheme and r["n"] == n and r["K"] == 1.0)
            return z

        outs = [f"3-month ATM call, {q['n_paths']:,} paths, exact {q['exact']['1.0']:.5f}"]
        for n in (2, 8, 32):
            e, a = row(n, "Euler"), row(n, "QE")
            outs.append(f"{n:>3} steps   Euler {100 * e['rel']:+6.1f}%   QE {100 * a['rel']:+6.1f}%   (s.e. "
                        f"{100 * a['se'] / q['exact']['1.0']:.1f}%)")
        with self.voiceover(
            "And here it is in the House, ten lines out of the loop body of heston underscore q e: the exact moments, "
            "the switch on psi, the squared-Gaussian branch, the point mass and the exponential, and the price step. "
            "<bookmark mark='a'/> Run it on a three-month at-the-money call under our fitted model, against the "
            "exact Fourier price, with two, eight and thirty-two time steps."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.8)
        self.clear_scene()

    def qe(self, q):
        rows = q["rows"]
        ns = sorted({r["n"] for r in rows})
        ex = q["exact"]["1.0"]
        g = axes([np.log10(1.5), np.log10(180)], [-0.05, 0.25], x_length=6.8, y_length=4.0, xlabel=r"time steps (3 months)",
                 ylabel=r"error of the Monte Carlo price, \% of price", xticks=[np.log10(n) for n in ns],
                 xfmt=lambda u: f"{10 ** u:.0f}", yticks=[0, 0.1, 0.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16,
                 log_x=True).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax

        def line(scheme, col):
            pts = [(np.log10(r["n"]), r["bias"] / ex) for r in rows if r["scheme"] == scheme and r["K"] == 1.0]
            dots = VGroup(*[Dot(ax.c2p(*p_), radius=0.06, color=col) for p_ in pts])
            ln = VMobject(stroke_color=col, stroke_width=3).set_points_as_corners([ax.c2p(*p_) for p_ in pts])
            return VGroup(ln, dots)

        eu, qe = line("Euler", BAD), line("QE", RV)
        zero = DashedLine(ax.c2p(np.log10(1.5), 0), ax.c2p(np.log10(180), 0), stroke_color=GREY_C, stroke_width=1.5)
        leg = legend([(BAD, r"Euler, variance floored at zero"), (RV, r"Andersen's QE scheme (2008)")],
                     font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        e2 = next(r for r in rows if r["scheme"] == "Euler" and r["n"] == 2 and r["K"] == 1.0)
        q2 = next(r for r in rows if r["scheme"] == "QE" and r["n"] == 2 and r["K"] == 1.0)
        side = VGroup(
            wrapped_label(r"pricing a 3-month at-the-money call under the fitted Heston, 200{,}000 paths, against the exact "
                          r"Fourier price", 4.4, 19, GREY_A),
            wrapped_label(rf"with 2 steps, Euler is {100 * e2['rel']:.0f}\% too high and QE {100 * abs(q2['rel']):.0f}\% too "
                          r"low; from 16 steps, QE is inside the Monte Carlo noise", 4.4, 20, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is the whole curve. Euler, with two steps, is "
            f"{100 * e2['rel']:.0f} percent too high, and needs dozens of steps to get inside the noise. "
            "<bookmark mark='a'/> QE, with two steps, is off by about "
            f"{100 * abs(q2['rel']):.0f} percent, and from sixteen steps its error disappears into the Monte Carlo "
            "noise. It is the House's Heston simulator, and every Heston path in this part comes from it."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]), FadeIn(leg[0]), Create(eu[0]), FadeIn(eu[1]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), Create(qe[0]), FadeIn(qe[1]), FadeIn(side[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def cards(self):
        c1 = history_card(2006, r"Broadie and Kaya, \textit{Operations Research}",
                          r"Exact simulation of Heston: draw $v_T$ from its non-central $\chi^2$ law, then $\int v$ given both "
                          r"ends by inverting its characteristic function. Unbiased, but slow.", color=QC.IDEA, width=4.1)
        c2 = history_card(2024, r"Choi and Kwok, \textit{EJOR}",
                          r"Simulation schemes for Heston with Poisson conditioning: exact-type sampling of the variance "
                          r"path's integral without the slow Bessel draws.", color=QC.IDEA, width=4.1)
        c3 = history_card(2007, r"Andersen and Piterbarg, \textit{Finance Stoch.}",
                          r"Moment explosions: in stochastic volatility models $\mathbb{E}[S_T^p]$ can become infinite at "
                          r"a finite time for $p > 1$; it decides the wings, and links to Lee's moment formula (Part 12).",
                          color=QC.IDEA, width=4.1)
        G = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            "Three further pointers. Mark Broadie and Özgür Kaya showed in 2006 how to simulate Heston exactly, with "
            "no time-step bias at all, by drawing the end variance from its chi-squared law and then the integrated "
            "variance given both ends: unbiased, but slow. <bookmark mark='a'/> In 2024 Jaehyuk Choi and Yue Kuen "
            "Kwok found a faster exact-type scheme by conditioning on a Poisson variable. <bookmark mark='b'/> And "
            "Leif Andersen and Vladimir Piterbarg showed that in these models moments of the price can explode at a "
            "finite time, which is what decides how fat the smile's wings can be, the link to Lee's formula in Part "
            "twelve."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
