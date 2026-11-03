from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, illustration, load, pause,
                                         real_data, running_min)

SIG = QC.DELTA


class Signature(VoiceoverScene):
    def construct(self):
        s = load("sigvol")
        self.card()
        self.unroll(s)
        self.derive()
        self.lab(s)
        self.replay(s)

    def card(self):
        c = chapter_card(16, r"Signature volatility models", r"Can calibration become a regression?", lit=(2023,),
                         part=PART)
        with self.voiceover("Chapter sixteen. Signature volatility models."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def unroll(self, s):
        p = s["path"]
        t, W = np.asarray(p["t"]), np.asarray(p["W"])
        sig = np.asarray(p["sig"])
        vol = np.asarray(p["vol"])
        words = s["words"]
        n = len(t) - 1
        g = axes([0, 0.5], [W.min() - 0.05, W.max() + 0.05], x_length=5.6, y_length=2.3, xlabel=r"time $t$",
                 ylabel=r"driver $W_t$", xticks=[0, 0.25, 0.5], yticks=[], font_size=14).to_corner(UL, buff=0.4)
        g2 = axes([0, 0.5], [min(vol.min(), 0) - 0.05, vol.max() + 0.05], x_length=5.6, y_length=2.0, xlabel=r"time $t$",
                  ylabel=r"volatility $\sigma_t = \langle \ell, \widehat{\mathbb{X}}_t\rangle$", xticks=[0, 0.25, 0.5],
                  yticks=[], font_size=14).next_to(g, DOWN, buff=0.55).align_to(g, LEFT)
        tr = ValueTracker(0)
        lw = tracing(g.ax, t, W, tr, WHITE, stroke_width=2)
        lv = tracing(g2.ax, t, vol, tr, SIG, stroke_width=2.4)
        d = len(words)
        sc = np.maximum(np.abs(sig).max(0), 1e-9)
        base = RIGHT * 1.0 + UP * 0.2  # bars reach 1.8 either way; their word labels sit below, inside the frame
        cols = [GREY_B] + [IV] * 2 + [OPT] * 4 + [ROUGH] * 8

        def bars():
            i = int(tr.get_value())
            grp = VGroup()
            for j in range(d):
                h = 1.8 * sig[i, j] / sc[j]
                grp.add(Rectangle(width=0.26, height=max(abs(h), 0.01), stroke_width=0, fill_color=cols[j],
                                  fill_opacity=0.9).move_to(base + RIGHT * 0.36 * j + UP * h / 2))
            return grp

        bb = always_redraw(bars)
        axis = Line(base + LEFT * 0.2, base + RIGHT * 0.36 * d, stroke_color=GREY_C)
        wl = VGroup(*[Text(w_ if w_ else "1", font="DejaVu Sans Mono", font_size=12, color=cols[j]).rotate(PI / 2).move_to(
            base + RIGHT * 0.36 * j + DOWN * 2.15) for j, w_ in enumerate(words)])
        cap = wrapped_label(r"the signature of $(t, W_t)$ to depth 3: 15 iterated integrals, each scaled to its own range",
                            5.8, 17, GREY_A).next_to(axis, UP, buff=2.0).align_to(axis, LEFT)
        q = pause(r"Depth 1 only: what kind of model is $\sigma_t = \ell_0 + \ell_1 t + \ell_2 W_t$?", width=6.4,
                  font_size=19).to_corner(DR, buff=0.2).shift(UP * 0.25)  # below the word labels, above the source
        src = illustration(r"one simulated path; the weights $\ell$ are the calibrated ones of this chapter", corner=DL)
        with self.voiceover(
            "Christa Cuchiero, Guido Gazzani and Sara Svaluto-Ferro asked: what if volatility were a linear function "
            "of the path's signature? Part five built the signature, the iterated integrals of a path. Here is the "
            "driving path, time and a Brownian motion together. As it unrolls, its signature to depth three, "
            "fifteen numbers, grows on the right: the increments, the areas, the higher iterated integrals. "
            "<bookmark mark='a'/> Volatility is a weighted sum of those fifteen bars, drawn below: a path-dependent "
            "volatility, built from the path's own geometry. <bookmark mark='b'/> Pause and predict: keep only "
            "depth one, a constant, time and W. What kind of model is that? <bookmark mark='c'/> Volatility linear "
            "in a Gaussian driver: a Stein-Stein-type model. Higher depths add path dependence."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2), FadeIn(lw), FadeIn(lv), FadeIn(axis), FadeIn(bb), FadeIn(wl), FadeIn(cap),
                      FadeIn(src))
            self.play(tr.animate.set_value(n), run_time=8, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
        for m in (lw, lv, bb):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\sigma_t", r"=", r"\langle \ell, \widehat{\mathbb{X}}_{0, t}\rangle,\qquad \widehat{\mathbb{X}} = "
                      r"\text{signature of } (t, W_t)", font_size=36, colors={r"\sigma_t": SIG}),
                cmath(r"\log S_T", r"=", r"\int_0^T \sigma_t\,dZ_t - \tfrac12\int_0^T \sigma_t^2\,dt = \ell^\top A - "
                      r"\tfrac12\,\ell^\top B\,\ell", font_size=36, colors={r"\log S_T": OPT}),
                cmath(r"A", r"=", r"\rho A^W + \sqrt{1 - \rho^2}\,A^\perp,\quad A^W = \int \widehat{\mathbb{X}}\,dW,\quad "
                      r"B = \int \widehat{\mathbb{X}}\widehat{\mathbb{X}}^\top dt", font_size=32, colors={r"A": OPT}),
                cmath(r"\text{linear functionals of } \widehat{\mathbb{X}}", r"\approx", r"\text{any continuous path "
                      r"functional (on compacts)}", font_size=32, colors={r"\text{linear functionals of } \widehat{\mathbb{X}}": GREY_A})]
        whys = [why(r"the model: volatility linear in the parameters $\ell$ (Cuchiero, Gazzani and Svaluto-Ferro, SIAM J. "
                    r"Financial Math. 2023)"),
                why(r"$\sigma$ is linear in $\ell$: the stochastic integral is linear, the quadratic variation quadratic"),
                why(r"$Z = \rho W + \sqrt{1 - \rho^2}W^\perp$: store both integrals per path, and $\rho$ is free too"),
                why(r"universality (Stone--Weierstrass, Part 5): as depth grows, any reasonable path-dependent "
                    r"volatility is reachable")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.8, buff=0.75, edge=6.9)
        with self.voiceover(
            "Here is why this is clever. Volatility is the inner product of a parameter vector ell with the "
            "signature. <bookmark mark='a'/> The log price is the stochastic integral of sigma minus half its "
            "quadratic variation. Because sigma is linear in ell, the first term is linear in ell and the second "
            "quadratic: ell transpose A minus a half ell transpose B ell. <bookmark mark='b'/> A and B depend only "
            "on the simulated paths. Store them once, for both the Brownian motion and its independent partner, "
            "and the correlation rho is free too. <bookmark mark='c'/> And linear functionals of signatures can "
            "approximate any continuous function of the path, so the family is as rich as we like."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, s):
        card = lab_card(r"pricing a signature model", [
            "def sigvol_logS(ell, rho, A_W, A_perp, B):",
            "    A = rho * (A_W @ ell) + np.sqrt(1 - rho*rho) * (A_perp @ ell)",
            "    q = np.einsum('pi,i->p', np.einsum('pij,j->pi', B, ell), ell)",
            "    return A - 0.5 * q              # log S_T on every path",
            "",
            "ST = np.exp(sigvol_logS(ell, rho, f['AW'], f['AP'], f['B']))",
            "price = np.mean(np.maximum(cp * (ST / ST.mean() - K), 0))",
        ], source="explainer/quant/house/rough.py: sigvol_logS", width=8.0).to_edge(UP, buff=0.4)
        outs = [f"{s['paths']:,} paths, features built once; one parameter vector prices all {load('rbergomi')['n']} quotes",
                f"fit on seed 1: {s['rmse_in']:.2f} vol points;  re-priced on fresh paths: {s['rmse_out']:.2f}"]
        with self.voiceover(
            "In the House, pricing a new parameter vector is three lines of linear algebra on stored arrays: no "
            "new simulation. Each call prices every path at every expiry at once. <bookmark mark='a'/> Fitted to "
            f"the Surface on one set of ten thousand paths, the error is {s['rmse_in']:.2f} volatility points; on a "
            f"fresh set, {s['rmse_out']:.2f}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=2.5, font_size=17)
        self.wait(0.5)
        self.clear_scene()

    def replay(self, s):
        cv = running_min(s["curve"])
        steps = np.arange(len(cv))
        best = s["best"]
        idx = sorted(set([0, 1, len(best) // 3, 2 * len(best) // 3, len(best) - 1]))
        ck = [best[i]["eval"] for i in idx]
        Q = load("rb_replay")
        T, k, iv = np.asarray(Q["T"]), np.asarray(Q["k"]), np.asarray(Q["iv"])
        Td = np.round(T * 365).astype(int)
        cols = [ROUGH, IV, OPT]

        def frame(j):
            biv = np.asarray(best[idx[j]]["iv"], float)
            g = axes([-0.45, 0.45], [0.3, 1.0], x_length=5.0, y_length=3.4, xlabel=r"log-moneyness $k$",
                     ylabel=r"implied volatility", xticks=[-0.4, 0, 0.4], yticks=[0.4, 0.6, 0.8, 1.0],
                     yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=13)
            grp = VGroup(g)
            for dd, c in zip((4, 16, 79), cols):
                m = Td == dd
                o = np.argsort(k[m])
                grp.add(VGroup(*[Dot(g.ax.c2p(a, min(max(y, 0.3), 1.0)), radius=0.04, color=c) for a, y in zip(k[m], iv[m])]))
                ok = np.isfinite(biv[m][o])
                if ok.sum() > 1:
                    grp.add(curve(g.ax, k[m][o][ok], np.clip(biv[m][o][ok], 0.3, 1.0), c, stroke_width=2.5))
            return grp

        rp = TrainingReplay(steps, cv, frame, ck, ylabel=r"fit error (vol points)", xlabel=r"model evaluation", color=SIG)
        b2 = load("bergomi2f")
        rb = s["rbergomi_rmse"]
        board = VGroup(*[VGroup(label(n_, font_size=18, color=c), MathTex(f"{v:.2f}", font_size=24, color=c)).arrange(RIGHT, buff=0.25)
                         for n_, v, c in sorted([(r"rough Bergomi", rb, MODEL_COL["rBergomi"]),
                                                  (r"two-factor Bergomi", b2["rmse"], VAR),
                                                  (r"signature model", s["rmse_out"], SIG)], key=lambda r: r[1])]
                       ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
        best_name = min([("rough Bergomi", rb), ("the two-factor Bergomi model", b2["rmse"]),
                         ("the signature model", s["rmse_out"])], key=lambda r: r[1])[0]
        cards = wrapped_label(r"Cuchiero, Gazzani, M\"oller and Svaluto-Ferro (Mathematical Finance 35(1), 2025): signature "
                              r"models fit SPX and VIX options jointly, without jumps or roughness", 11.0, 18, GREY_A).next_to(
            board, UP, buff=0.2)
        with self.voiceover(
            "Watch the sixteen numbers calibrate: the error on the right, the smiles at three expiries on the left. "
            "Because each evaluation is only linear algebra, the search is cheap. <bookmark mark='a'/> Re-priced on "
            "fresh paths, the scores on our Surface: rough Bergomi, the two-factor Bergomi model, and the signature "
            f"model. Lowest: {best_name}. <bookmark mark='b'/> With Janka Möller, the same group showed in "
            "2025 that signature models fit S&P and VIX options jointly, with neither jumps nor roughness: "
            "path dependence, again, doing the work."
            " Next: what desks actually use, and the House's rough lab."
        ) as vo:
            self.play(FadeIn(rp))
            rp.play(self, run_time=7)
            vo.wait_until("a")
            self.play(FadeIn(board))
            vo.wait_until("b")
            self.play(FadeIn(cards))
        self.wait(0.4)
        self.clear_scene()
