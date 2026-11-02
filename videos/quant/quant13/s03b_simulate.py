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
            wrapped_label(r"one weekly step of the fitted variance, " + f"{qd['N']:,}".replace(",", "{,}") +
                          r" draws each; white: the exact law (a scaled non-central $\chi^2$), probability per bin; bars "
                          r"clipped at the top", 12.4, 19, GREY_A),
            MathTex(rf"\text{{Euler: }} {100 * a['neg']:.0f}\%\ \text{{of draws below zero}};\quad "
                    rf"\text{{mean}}\ {a['mean_euler']:.3f}\ \text{{vs exact}}\ {a['mean_exact']:.3f};\quad "
                    rf"\text{{QE}}\ {a['mean_qe']:.3f}", font_size=28),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Desks price exotics by simulation. So take one week-long step of the fitted variance from a low level, "
            "zero point zero five, a hundred thousand times. White: the exact law, piled against zero. "
            f"<bookmark mark='a'/> Euler adds a Gaussian shock: {100 * a['neg']:.0f} percent of draws go negative. Floor "
            f"them at zero and the mean is {a['mean_euler']:.3f} instead of {a['mean_exact']:.3f}, a bias that "
            "compounds. <bookmark mark='b'/> Andersen's quadratic-exponential scheme puts a point mass at zero, here "
            f"{a['zero_qe']:.2f}, with an exponential tail, sized to match the mean and variance exactly: "
            f"{a['mean_qe']:.3f}. <bookmark mark='c'/> Started high, QE switches to a scaled Gaussian squared, which "
            "matches almost perfectly."
        )
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
            (
            f"Why is this hard? Feller's ratio is {fel:.2f} on our fit, below one, so by Part five's boundary test the "
            "variance reaches zero and its law spikes there. <bookmark mark='a'/> Score each scheme by the transport "
            "distance to the exact law, over three start values and three step sizes. <bookmark mark='b'/> QE wins "
            f"all nine, by a median factor of {ratio:.0f}. Its advantage is largest exactly when Feller fails."
        )
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
            (
            (
            "QE, derived. Over one step, the variance's conditional mean and variance are known exactly: Part five's "
            "CIR moments. <bookmark mark='a'/> Their ratio psi measures relative width. <bookmark mark='b'/> Small "
            "psi: a constant times a shifted Gaussian squared. Its mean is a times one plus b squared, its variance "
            "two a squared times one plus two b squared; set them equal to m and s squared and solve: these b and a. "
            "<bookmark mark='c'/> Large psi: zero with probability p, else an exponential with rate beta. The mean "
            "is one minus p over beta and the second moment twice that over beta; matching gives p and beta. "
            "Andersen switches at one and a half, where both are valid. <bookmark mark='d'/> For the price, solve the "
            "variance equation for its stochastic integral and substitute; only the orthogonal part needs a fresh "
            "Gaussian, and one constant makes the price an exact martingale."
        )
        )
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
            (
            "In the House: the exact moments, the switch on psi, both branches, and the price step. "
            "<bookmark mark='a'/> Run it on a three-month at-the-money call against the exact Fourier price, with "
            "two, eight and thirty-two steps. QE is close from the start; Euler needs dozens of steps."
        )
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.8)
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
            (
            "Three pointers. Broadie and Kaya simulated Heston exactly in 2006: unbiased, but slow. "
            "<bookmark mark='a'/> Choi and Kwok, in 2024, made exact-type sampling fast with Poisson conditioning. "
            "<bookmark mark='b'/> And Andersen and Piterbarg showed that moments of the price can explode in finite "
            "time, which bounds the smile's wings: the link to Lee's formula in Part twelve."
            " Next: the model rates and currency desks prefer, SABR."
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
