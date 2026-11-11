from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import (BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog, polyline,
                                         predict, sci, axes, data_range, pause_card, flat_camera)

ORDER = ["Monte Carlo (QE, 50 steps)", "Monte Carlo, control variate", "ADI (Craig-Sneyd)", "Carr-Madan FFT", "COS"]


class COS(VoiceoverScene):
    def construct(self):
        cd = load("cos_density")
        f = load("fourier")
        r = load("race")
        rc = load("race_cv")
        self.card()
        self.rebuild(cd)
        self.derive()
        self.truncate(cd, f)
        self.race(r, rc)

    def card(self):
        c = chapter_card(16, r"Fourier II: the COS method, and the race", r"Which method should price this option?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter sixteen. Fourier methods, part two: the cosine method, and the race."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rebuild(self, cd):
        y = np.asarray(cd["y"])
        tru = np.asarray(cd["true"])
        Ns = ["2", "4", "8", "16", "32", "64", "128"]
        yr = data_range(tru, *[cd["rec"][n] for n in Ns])
        g = axes([y[0], y[-1]], yr, x_length=7.0, y_length=4.2, xlabel=r"log-return $\log(S_T/S_0)$",
                 ylabel=r"density", xticks=[-0.8, -0.4, 0, 0.4], yticks=[0, 1, 2], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        truth = curve(ax, y, tru, GREY_B, stroke_width=5)
        Ns = ["2", "4", "8", "16", "32", "64", "128"]
        recs = [curve(ax, y, np.asarray(cd["rec"][n]), QC.DELTA, stroke_width=3) for n in Ns]
        errs = {n: float(np.max(np.abs(np.asarray(cd["rec"][n]) - tru))) for n in Ns}
        tag = MathTex(r"N = 2", font_size=32, color=QC.DELTA).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        A = np.asarray(cd["A"])
        positive = A > 0
        coeff_yr = data_range(np.log10(A[positive]))
        h = axes([0, len(A)], coeff_yr, x_length=4.2, y_length=3.0, xlabel=r"$k$",
                 ylabel=r"$|A_k|$ ($\log_{10}$)", xticks=[0, 100, 200], yticks=[-10, -5, 0], font_size=14)
        h.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        dots = VGroup(*[Dot(h.ax.c2p(k, np.log10(a_)), radius=0.025, color=QC.DELTA)
                        for k, a_ in enumerate(A) if a_ > 0])
        src = illustration(rf"Heston, one year: $v_0 = \theta = 0.04$, $\kappa = 1.5$, $\xi = 0.5$, $\rho = -0.7$; range "
                           rf"$[{cd['a']:.2f}, {cd['b']:.2f}]$")
        with self.voiceover(
            f"In grey is a high-term numerical Heston density reference, not an exact density. The cosine approximations retain all saved values, including negative oscillations. <bookmark mark='a'/> As terms are added, shape and tails improve. On these sampled density sites the sixty-four-term maximum discrepancy is {errs['64']:.1e}; at one hundred and twenty-eight it is {errs['128']:.1e}, finite rather than gone. <bookmark mark='b'/> The coefficient plot shows all strictly positive saved magnitudes without an artificial floor; exact zeros have no finite logarithm and are omitted. Rapid decay is favourable in this example. Exponential convergence requires appropriate analyticity and coefficient decay and does not hold for every model."
        ) as vo:
            self.play(FadeIn(g), Create(truth), FadeIn(src))
            self.play(Create(recs[0]), FadeIn(tag))
            vo.wait_until("a")
            cur = recs[0]
            for k in range(1, len(Ns)):
                self.play(ReplacementTransform(cur, recs[k]),
                          Transform(tag, MathTex(rf"N = {Ns[k]}", font_size=32, color=QC.DELTA).move_to(tag)), run_time=1.0)
                cur = recs[k]
                self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(h), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=2.5))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"V", r"=", r"e^{-rT}\int_{\mathbb{R}} v(y)f(y)\,dy\ \approx\ e^{-rT}\int_a^b v(y)f(y)\,dy", font_size=32,
                  colors={r"V": OPT}),
            cmath(r"f(y)", r"=", r"{\sum_{k \ge 0}}' A_k\cos\Big(k\pi\frac{y - a}{b - a}\Big),\quad A_k = \frac{2}{b - a}"
                  r"\int_a^b f(y)\cos\Big(k\pi\frac{y - a}{b - a}\Big)dy", font_size=28),
            cmath(r"A_k", r"\approx", r"\frac{2}{b - a}\,\mathrm{Re}\Big[\varphi\Big(\frac{k\pi}{b - a}\Big)e^{ik\pi\frac{x-a}{b - a}}\Big]",
                  font_size=32, colors={r"A_k": QC.DELTA}),
            cmath(r"V", r"\approx", r"e^{-rT}{\sum_{k < N}}'\,\mathrm{Re}\Big[\varphi\Big(\frac{k\pi}{b - a}\Big)"
                  r"e^{ik\pi\frac{x - a}{b - a}}\Big]V_k", font_size=32, colors={r"V": GOOD}),
            cmath(r"\text{error}", r"=", r"\text{tail/coefficient truncation} + \text{series} + \text{roundoff}", font_size=34, colors={r"\text{error}": BAD}),
        ]
        whys = [why(r"$x=\log(S_0/K)$, $y=\log(S_T/K)$; monetary payoff $v(y)$; cumulant-based range is a heuristic, not a tail certificate"),
                why(r"an $L^2$ density has an $L^2$ cosine expansion; pointwise or uniform convergence requires additional regularity"),
                why(r"$\varphi$ is the CF of $y-x$; extending finite-range coefficients to the whole line introduces a tail approximation"),
                why(r"the payoff's cosine coefficients $V_k$ are in closed form (the code's \texttt{chi} and \texttt{psi})"),
                why(r"exponential for densities analytic in a strip; Junike (2024) gives the $N$ for a target error "
                    r"(chapter 19)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Define x as log initial stock over strike, y as log terminal stock over strike, and phi as the characteristic function of y minus x. The payoff v of y is in currency units. Cut its density integral to a finite interval; a cumulant rule proposes the interval but does not certify payoff-tail error. <bookmark mark='a'/> A square-integrable density admits a cosine expansion in the L2 sense, with additional conditions for stronger convergence. The prime halves the constant term. <bookmark mark='b'/> Extending coefficient integrals to the full line introduces a tail approximation and gives the characteristic function with phase x minus a. <bookmark mark='c'/> Monetary payoff coefficients are elementary integrals, yielding the displayed pricing sum. <bookmark mark='d'/> Errors include tail and coefficient truncation, finite series and roundoff. Exponential series decay needs suitable analyticity, boundary behaviour and coefficient bounds. Conditional error-control results require their full assumptions."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def truncate(self, cd, f):
        L = np.asarray(cd["L"], float)
        e = np.asarray(cd["errL"])
        ok = e > 0
        yr = data_range(np.log10(e[ok]))
        g = axes(data_range(L), yr, x_length=5.6, y_length=3.8, xlabel=r"range half-width $L$ (in standard deviations)",
                 ylabel=r"price error, $N = 4{,}096$ ($\log_{10}$)", xticks=[10, 20, 30, 40], yticks=[-15, -10, -5, 0],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ok = e > 0
        line = polyline(g.ax, L[ok], np.log10(e[ok]), BAD, radius=0.05)
        mark = DashedLine(g.ax.c2p(16, yr[0]), g.ax.c2p(16, yr[1]), stroke_color=GREY_B, stroke_width=1.5)
        reference_note = wrapped_label(r"$L=40$: zero discrepancy by construction against the same 4,096-term reference; not a zero tail-error claim", 5.6, 20, GREY_A).next_to(g, DOWN, buff=0.2)
        cos = [x for x in f["rows"] if x["method"] == "COS"]
        card = lab_card(r"the COS sum", [
            "k = np.arange(N)",
            "w = k * np.pi / (b - a)",
            "chi = (np.cos(w * (0 - a)) * 1.0 - np.cos(0.0) * np.exp(a)",
            "       + w * np.sin(w * (0 - a)) * 1.0) / (1 + w * w)",
            "psi = np.where(k == 0, -a, np.sin(w * (0 - a)) / np.where(k == 0, 1, w))",
            "Vk = 2.0 / (b - a) * (psi - chi)",
            "phi = cf(w, T)",
            "terms = (phi[None, :] * np.exp(1j * w[None, :] * (x[:, None] - a))).real * Vk[None, :]",
            "terms[:, 0] *= 0.5",
            "put = K * terms.sum(axis=1)",
        ], source="explainer/quant/house/stochvol.py  cos_price", width=6.6, font_size=16).to_edge(RIGHT, buff=0.3)
        card.shift(UP * 1.2)
        out = [f"N = {x['N']:>3}: error {x['err']:.1e}" for x in cos if x["N"] in (32, 64, 128, 256)]
        e16 = float(e[list(L).index(16.0)])
        with self.voiceover(
            f"Vary the interval half-width while retaining four thousand and ninety-six terms. The discrepancy from the same method at L forty is {e[0]:.2f} at L four, and {e16:.3g} at L sixteen. This comparison combines range and finite-series effects; it is not an exact truncation-error measurement. L forty has zero discrepancy by construction and is labelled separately, rather than plotted at a fake logarithmic zero. <bookmark mark='a'/> The code computes put coefficients, multiplies by characteristic-function phases, sums and uses put–call parity. <bookmark mark='b'/> The displayed {cos[-2]['N']}-term reference discrepancy is {cos[-2]['err']:.3g}. Shared assumptions and correlated numerical errors still limit what agreement establishes."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(mark), FadeIn(reference_note))
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            lab_run(self, card, out, font_size=17)
        self.wait(0.5)
        self.clear_scene()

    def race(self, r, rc):
        pts = r["points"] + rc["points"]
        xr = data_range([np.log10(p["time"]) for p in pts])
        yr = data_range([np.log10(p["err"]) for p in pts])
        g = loglog(*xr, *yr, r"wall-clock time (seconds, one core)", r"MC: one sampling s.e.; others: absolute reference error", x_length=7.4,
                   y_length=4.6, xt=[-4, -2, 0], yt=[-8, -6, -4, -2, 0])
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        clock = ValueTracker(xr[0])
        by = {m: sorted([q for q in pts if q["method"] == m], key=lambda q: q["time"]) for m in ORDER}

        def draw(m):
            def make():
                rr = [q for q in by[m] if np.log10(q["time"]) <= clock.get_value()]
                grp = VGroup()
                pp = [ax.c2p(np.log10(q["time"]), np.log10(q["err"])) for q in rr]
                if len(pp) > 1:
                    grp.add(VMobject(stroke_color=METHOD_COL[m], stroke_width=3).set_points_as_corners(pp))
                grp.add(*[Dot(q_, radius=0.06, color=METHOD_COL[m]) for q_ in pp])
                return grp
            return always_redraw(make)

        lines = [draw(m) for m in ORDER]
        leg = legend([(METHOD_COL[m], m) for m in ORDER], font_size=15).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        cv = rc["points"][-1]
        mc = by[ORDER[0]][-1]
        cos_best = min(by["COS"], key=lambda q: q["err"])
        side = VGroup(
            wrapped_label(rf"the stock as control buys a variance ratio of {cv['ratio']:.1f}: the line shifts down by "
                          rf"$\sqrt{{{cv['ratio']:.1f}}}$ and keeps its slope", 4.0, 17, GREY_A),
            wrapped_label(r"Fourier for vanillas when the model has a characteristic function (Bermudans too: Fang and "
                          r"Oosterlee 2009); grids for low-dimensional early exercise and barriers; simulation for "
                          r"many high-dimensional or path-dependent products", 4.0, 17, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        q = predict(r"Why is a terminal-density vanilla formula insufficient for a barrier?", width=4.0, font_size=19).to_corner(DR, buff=0.25)
        src = illustration(r"synthetic zero-rate/zero-dividend case; MC: one s.e., excluding 50-step QE and fitted-control bias; COS numerical reference",
                           corner=DL)
        with self.voiceover(
            f"The same saved timings now include a stock control variate. The clock spans the recorded data range on a shared CPU. This is a comparison of different diagnostics, not a matched total-accuracy race. <bookmark mark='a'/> For COS, grids and FFT, the vertical metric is absolute difference from the chosen COS reference. The best displayed COS difference is {cos_best['err']:.3g}. Sharing a reference limits independent validation. <bookmark mark='b'/> For Monte Carlo, height is one estimated sampling standard error, excluding fifty-step QE bias and any same-sample control-fitting bias. A fixed population control changes the asymptotic variance constant, with work and estimation effects considered separately. Here the empirical ratio is {cv['ratio']:.1f}. <bookmark mark='c'/> Characteristic-function methods are useful for suitable vanillas; grids for manageable state dimensions; simulation for many high-dimensional and path-dependent problems. A terminal density alone cannot identify a barrier touch. COS backward-recursion extensions can nevertheless handle barriers and Bermudans. Next, industry workloads and hardware."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), *[FadeIn(x) for x in lines])
            vo.wait_until("a")
            self.play(clock.animate.set_value(xr[0] + 0.5 * (xr[1] - xr[0])), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(clock.animate.set_value(xr[1]), run_time=4, rate_func=linear)
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(q))
        for x in lines:
            x.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
