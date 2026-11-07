from __future__ import annotations

import numpy as np
from videos.quant.quant10.common import FullRangeReplay as TrainingReplay

from explainer.quant import *  # noqa: F403
from explainer.quant.house import smile as SM
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


class SVI(VoiceoverScene):
    def construct(self):
        r = load("svi_replay")
        s = load("surface")
        self.card()
        self.sliders()
        self.derive()
        self.lab(r, s)
        self.replay(r)
        self.table(r)

    def card(self):
        c = chapter_card(4, r"SVI: a smile in five numbers", r"How do you fit a smile without breaking it?", lit=(2004,),
                         part=PART)
        with self.voiceover("Chapter four. SVI: a smile in five numbers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sliders(self):
        g = axes([-1, 1], [0, 0.4], x_length=7.0, y_length=4.4, xlabel=r"log-moneyness $k$", ylabel=r"total variance $w(k)$",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.2, 0.4], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        P = {x: ValueTracker(v) for x, v in (("a", 0.04), ("b", 0.12), ("rho", -0.3), ("m", 0.05), ("s", 0.2))}
        k = np.linspace(-1, 1, 201)

        def w():
            return SM.svi_total_variance(k, *(P[x].get_value() for x in ("a", "b", "rho", "m", "s")))

        def asym(sign):
            a, b, rho, m = (P[x].get_value() for x in ("a", "b", "rho", "m"))
            end = float(sign)
            return DashedLine(ax.c2p(m, float(np.clip(a, 0, 0.4))),
                              ax.c2p(end, float(np.clip(a + b * (rho + sign) * (end - m), 0, 0.4))),
                              color=GREY_B, stroke_width=2)
        line = always_redraw(lambda: curve(ax, k, np.clip(w(), 0, 0.4), IV, stroke_width=4))
        asl = always_redraw(lambda: asym(-1))
        asr = always_redraw(lambda: asym(1))
        ro = VGroup(*[readout(rf"{t} =", lambda x=x: P[x].get_value(), digits=3, font_size=28, color=c)
                      for x, t, c in (("a", "a", GREY_A), ("b", "b", IV), ("rho", r"\rho", BAD), ("m", "m", LV),
                                      ("s", r"\sigma", OPT))]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ro.to_edge(RIGHT, buff=1.2).shift(UP * 0.8)
        what = VGroup(*[label(t, font_size=19, color=GREY_B) for t in (
            r"a: lifts the whole smile", r"b: opens the wings", r"$\rho$: tilts it (the skew)", r"m: slides it sideways",
            r"$\sigma$: rounds the vertex")]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ro, DOWN, buff=0.45)
        src = illustration(r"raw SVI, illustrative parameters; dashes: the two asymptotes")
        with self.voiceover(
            """In 2004 Jim Gatheral published SVI, stochastic volatility inspired, used at Merrill Lynch since 1999. Its total variance is a hyperbola with five parameters. <bookmark mark='a'/> a lifts it; b controls the wing slopes. <bookmark mark='b'/> rho tilts, m shifts, and sigma rounds the vertex. The straight asymptotic wings are a useful parametrization consistent with Lee's slope bounds when constrained. Lee's theorem does not require every admissible smile to have exactly straight wings."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.add(line, asl, asr)
            self.play(FadeIn(ro), FadeIn(what))
            vo.wait_until("a")
            self.play(P["a"].animate.set_value(0.1), run_time=1.2)
            self.play(P["a"].animate.set_value(0.04), run_time=0.8)
            self.play(P["b"].animate.set_value(0.25), run_time=1.2)
            self.play(P["b"].animate.set_value(0.12), run_time=0.8)
            vo.wait_until("b")
            self.play(P["rho"].animate.set_value(0.5), run_time=1.2)
            self.play(P["rho"].animate.set_value(-0.3), run_time=0.8)
            self.play(P["m"].animate.set_value(0.4), run_time=1)
            self.play(P["m"].animate.set_value(0.05), run_time=0.8)
            self.play(P["s"].animate.set_value(0.02), run_time=1)
            self.play(P["s"].animate.set_value(0.2), run_time=0.8)
        for m_ in (line, asl, asr, *ro):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"w(k)", r"=", r"a + b\Big(\rho(k - m) + \sqrt{(k - m)^2 + \sigma^2}\Big)", font_size=38,
                      colors={r"w(k)": IV}),
                cmath(r"w'(\pm\infty)", r"=", r"b(\rho \pm 1),\qquad \min_k w = a + b\sigma\sqrt{1 - \rho^2}", font_size=36),
                cmath(r"b(1 + |\rho|)", r"\le", r"2", font_size=38, colors={r"b(1 + |\rho|)": BAD}),
                cmath(r"\psi", r"=", r"\frac{b}{2\sqrt{w_0}}\Big(\rho - \frac{m}{\sqrt{m^2 + \sigma^2}}\Big),\quad "
                      r"p = \frac{b(1 - \rho)}{\sqrt{w_0}},\quad c = \frac{b(1 + \rho)}{\sqrt{w_0}}", font_size=32,
                      colors={r"\psi": LV}),
                cmath(r"\min_{a,\,b\rho,\,b}\ \sum_i \nu_i\big(w(k_i) - w_i\big)^2", r"\to",
                      r"\text{linear for fixed } (m, \sigma)", font_size=34, colors={r"\min_{a,\,b\rho,\,b}\ \sum_i \nu_i\big(w(k_i) - w_i\big)^2": OPT})]
        whys = [why(r"Gatheral (2004): raw SVI, total implied variance at one expiry"),
                why(r"far out, the square root is $|k - m|$: two straight wings; set $w' = 0$ for the bottom"),
                why(r"Chapter 3's Lee bound applied to the steeper wing"),
                why(r"the jump-wings form: ATM variance $v$, ATM skew $\psi$, put and call wing slopes $p, c$, minimum "
                    r"variance $\tilde v$: the numbers a desk quotes and moves"),
                why(r"weighted least squares; Zeliade (2009): for fixed $(m, \sigma)$ the rest is linear, so the search is "
                    r"two-dimensional")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.72, edge=6.9)
        with self.voiceover(
            "The formula. <bookmark mark='a'/> Far out, the square root becomes an absolute value: straight wings of "
            "slope b times rho plus or minus one; set the derivative to zero for the bottom. <bookmark mark='b'/> Lee's "
            "bound becomes a box: b times one plus the absolute value of rho, at most two. <bookmark mark='c'/> Desks "
            "quote the jump-wings form: at-the-money variance and skew, the two wing slopes, the minimum. And Gatheral "
            "and Jacquier proved in 2011 that Heston's implied variance becomes exactly SVI at long maturity. "
            "<bookmark mark='d'/> For fixed m and sigma the fit is linear in the rest, Zeliade's 2009 reduction to a "
            "two-dimensional search."
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

    def lab(self, r, s):
        per = [p for p in s["per"] if p["expiry"] == r["expiry"]][0]
        q = per["svi"]
        rm = [t for t in r["table"] if t["expiry"] == r["expiry"]][0]["rmse"]
        card = lab_card(r"fitting SVI to one expiry", [
            "def fit_svi(k, w, weights=None):",
            "    def resid(p):",
            "        a, b, rho, m, s = p",
            "        return np.sqrt(wt) * (svi_total_variance(k, a, b, rho, m, s) - w)",
            "    for m0 in (-0.1, 0.0, 0.1):",
            "        for s0 in (0.05, 0.2):",
            "            p0 = [max(w.min() * 0.5, 1e-4), 0.1, -0.2, m0, s0]",
            "            lo = [-w.max(), 1e-6, -0.999, -1.0, 1e-3]",
            "            hi = [w.max() * 2, 2.0 / (1 + 0.999), 0.999, 1.0, 2.0]",
            "            r = optimize.least_squares(resid, p0, bounds=(lo, hi))",
            "            if best is None or r.cost < best.cost:",
            "                best = r",
        ], source="explainer/quant/house/smile.py", width=8.6).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        n = per["n"]
        days = per["T"] * 365
        with self.voiceover(
            f"Here is the House's fitter. The residual is the weighted gap in total variance. Six starting points, a bounded least-squares search from each, and the bounds include Lee's: b times one plus absolute rho can never exceed two. <bookmark mark='a'/> Run it on the Surface's {days:.0f}-day expiry, {n} quotes, weighted by vega: five numbers, and a fit within {rm:.2f} volatility points."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"fit_svi(k, iv**2 * T, weights=vega)   # {r['expiry']}, {n} quotes",
                                 f"a={q['a']:.4f}  b={q['b']:.4f}  rho={q['rho']:.3f}  m={q['m']:.3f}  s={q['s']:.3f}",
                                 f"rmse {rm:.2f} vol points;  b(1+|rho|) = {q['b'] * (1 + abs(q['rho'])):.3f} <= 2"])
        self.wait(0.6)
        self.clear_scene()

    def replay(self, r):
        runs = r["runs"]
        k, iv, T = np.asarray(r["k"]), np.asarray(r["iv"]), r["T"]
        L = max(len(x["rmse"]) for x in runs)
        loss = np.array([np.pad(x["rmse"], (0, L - len(x["rmse"])), mode="edge") for x in runs])
        steps = np.arange(L)
        ck = [0, 2, 4, 7, 10, 15, 22, L - 1]
        cols = [IV, LV, BAD, OPT, SPOT, RV]
        kk = np.linspace(-0.6, 0.6, 81)

        def params_at(run, step_):
            idx = np.asarray(run["path_i"])
            j = int(np.searchsorted(idx, min(step_, idx[-1]), side="right") - 1)
            return np.asarray(run["path"])[max(j, 0)]

        def frame(i):
            g = axes([-0.6, 0.6], [0.3, 0.9], x_length=5.2, y_length=3.4, xlabel=r"log-moneyness",
                     ylabel=r"IV: 30--90\% viewport (clipped)", xticks=[-0.5, 0, 0.5], yticks=[0.4, 0.6, 0.8],
                     yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
            m = (iv >= 0.3) & (iv <= 0.9) & (np.abs(k) <= 0.6)
            dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.035, color=WHITE) for a, b in zip(k[m], iv[m])])
            curves = VGroup()
            for run, c in zip(runs, cols):
                p = params_at(run, ck[i])
                w = SM.svi_total_variance(kk, *p)
                curves.add(curve(g.ax, kk, np.clip(np.sqrt(np.maximum(w, 1e-8) / T), 0.3, 0.9), c, stroke_width=2.5))
            return VGroup(g, dots, curves)
        rp = TrainingReplay(steps, loss, frame, ck, ylabel=r"RMSE (vol points, log scale)", xlabel=r"residual call (includes finite differences)",
                            log_y=True)
        nf = r["nfev"]
        fi, fl = r["first"], r["final"]
        side = wrapped_label(rf"six random starts, {min(fi):.0f} to {max(fi):.0f} vol points off; all end at "
                     rf"{min(fl):.3f}; solver nfev {min(nf)}--{max(nf)}; replay includes finite-difference calls", width=12.6, font_size=18, color=GREY_A).to_edge(DOWN, buff=0.4)
        src = real_data(rf"the Surface, expiry {r['expiry']}, unweighted fits", corner=UR)
        lo, hi, n0, n1, best = min(fi), max(fi), min(nf), max(nf), min(fl)
        with self.voiceover(
            f"""Watch six fixed random starts. Their starting errors range from {lo:.0f} to {hi:.0f} volatility points. The right plot retains every residual call, including numerical Jacobian evaluations. <bookmark mark='a'/> The solver reports function-evaluation counts from {n0} to {n1}, excluding some finite-difference calls; these counts therefore differ from the replay's call counter. The final errors are near {best:.3f} volatility points. This is evidence about these six starts, not proof that every SVI calibration is benign. Separately fitted maturities can still cross, as Chapter three showed."""
        ) as vo:
            self.play(FadeIn(rp), FadeIn(src))
            rp.play(self, run_time=9)
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def table(self, r):
        rows = r["table"]
        hdr = [r"days", r"$v$ (ATM var.)", r"$\psi$ (skew)", r"$p$ (put wing)", r"$c$ (call wing)", r"$\tilde v$ (min var.)",
               r"$g_{\min}$"]
        data_rows = [[f"{x['days']:.0f}", f"{x['v']:.3f}", f"{x['psi']:+.3f}", f"{x['pw']:.2f}", f"{x['cw']:.2f}",
                      f"{x['vt']:.3f}", f"{x['g_min']:.2f}"] for x in rows]
        tab = VGroup()
        for i, rr in enumerate([hdr] + data_rows):
            tab.add(VGroup(*[label(c, font_size=18 if i else 18, color=GREY_A if i == 0 else WHITE) for c in rr]))
        widths = [max(row[j].width for row in tab) for j in range(len(hdr))]
        for row in tab:
            for j, c in enumerate(row):
                c.move_to([sum(widths[:j]) + 0.45 * j + widths[j] / 2, 0, 0])
        tab.arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(ORIGIN).shift(DOWN * 0.2)
        if tab.width > 12.6:
            tab.scale_to_fit_width(12.6)
        head = label(r"the Surface's eleven expiries in jump-wings form", font_size=26).to_edge(UP, buff=0.35)
        mm = wrapped_label(r"Martini and Mingone (2022) characterize exactly which raw SVI parameters are free of "
                           r"butterfly arbitrage; every fit here has $g_{\min} > 0$", 12, 19, GREY_B).to_edge(DOWN, buff=0.3)
        gmin = min(x["g_min"] for x in rows)
        last = rows[-1]
        pw, cw = last["pw"], last["cw"]
        with self.voiceover(
            f"And here is the whole Surface in the trader's coordinates, one row per expiry. The at-the-money variance climbs with maturity, the skew psi is small, and the wings steepen: at the longest expiry the put wing is {pw:.2f} and the call wing {cw:.2f}. <bookmark mark='a'/> The smallest g across all eleven fits is {gmin:.2f}: no negative g was found on the sampled log-moneyness grid from minus one to one. That finite scan is not a proof for all strikes. Claude Martini and Arianna Mingone mapped, in 2022, exactly which SVI parameters guarantee that; and Chapter three showed that slices which are clean one by one can still cross. The cure is to fit the surface as one object. Next: SSVI."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(x) for x in tab[1:]], lag_ratio=0.15, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(mm))
        self.wait(0.4)
        self.clear_scene()
