from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import BUDGET_COLORS, DCOL, FIT, NCOL, PART, SP, load, predict_card, takeaway_card

ACOLS = [C.CONTEXT, C.TRUE_P, C.BITS]  # approaches 1, 2, 3


def lnd(ch, N, D):
    return float(ch["E"]) + float(ch["A"]) * np.asarray(N, float) ** -float(ch["alpha"]) + \
        float(ch["B"]) * np.asarray(D, float) ** -float(ch["beta"])


def optimum(ch, C):
    al, be, A, B = float(ch["alpha"]), float(ch["beta"]), float(ch["A"]), float(ch["B"])
    G = (al * A / (be * B)) ** (1 / (al + be))
    n = G * (np.asarray(C, float) / 6) ** (be / (al + be))
    return n, np.asarray(C, float) / 6 / n


class Valley(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.predict()
        self.lagrange()
        self.surface()
        self.methods()
        self.takeaway()

    def card(self):
        card = chapter_card(8, r"Chinchilla's valley", r"How should a fixed budget be split between size and data?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter eight. Chinchilla's valley."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lagrange(self):
        ch = load("chinchilla")
        E, A, al, B, be = (float(ch[k]) for k in ("E", "A", "alpha", "B", "beta"))
        a3 = float(ch["a3"])
        colors = {r"N": NCOL, r"D": DCOL, r"\alpha": NCOL, r"\beta": DCOL, r"\lambda": C.BITS}
        law = cmath(r"L(N, D)", r"=", r"E", r"+", r"\frac{A}{N^{\alpha}}", r"+", r"\frac{B}{D^{\beta}}", font_size=40)
        law.to_edge(UP, buff=0.35)
        vals = label(rf"fitted to our ${int(ch['n_points'])}$ runs: \ $E = {E:.2f}$, \ $\alpha = {al:.2f}$, \ "
                     rf"$\beta = {be:.2f}$ \ (off by ${float(ch['rms']):.3f}$ bits on average)", font_size=22,
                     color=GREY_A).next_to(law, DOWN, buff=0.15)
        rows = [
            cmath(r"\mathcal{L}", r"=", r"L(N, D) + \lambda\,(6ND - C)", font_size=34, colors=colors),
            cmath(r"\partial_N:\ \ \frac{\alpha A}{N^{\alpha + 1}} = 6\lambda D", r",\qquad",
                  r"\partial_D:\ \ \frac{\beta B}{D^{\beta + 1}} = 6\lambda N", font_size=32),
            cmath(r"\frac{\alpha A}{N^{\alpha}}", r"=", r"\frac{\beta B}{D^{\beta}}", font_size=34),
            cmath(r"N_{\text{opt}}", r"=", r"G\,\Big(\frac{C}{6}\Big)^{\beta/(\alpha+\beta)}", r",\quad",
                  r"D_{\text{opt}} = G^{-1}\Big(\frac{C}{6}\Big)^{\alpha/(\alpha+\beta)}", font_size=32),
        ]
        whys = [why(r"a Lagrange multiplier \ (Part 4)"), why(r"both derivatives zero"),
                why(r"multiply by $N$ and by $D$: \ both equal $6\lambda ND$"),
                why(r"solve, \ with $G = (\alpha A / \beta B)^{1/(\alpha+\beta)}$")]
        step = ladder(self, rows, whys, keep=4, top=1.15, x=-1.4, buff=0.42, edge=6.9)
        res = label(rf"ours: \ $\beta/(\alpha+\beta) = {a3:.2f}$", font_size=30, color=C.BITS).move_to([-1.0, -3.3, 0])
        cite_ = cite(r"Hoffmann et al.\ (2022), \ approach 3", corner=DR)
        # the fit's quality: every run's measured loss against the formula's
        s_ = load("sweep")
        N_, D_, L_ = np.asarray(s_["N"], float), np.asarray(s_["D"], float), np.asarray(s_["bits"], float)
        ii, jj = np.where(np.isfinite(L_) & (D_[None] >= 2 ** 17))
        meas, pred = L_[ii, jj], lnd(ch, N_[ii], D_[jj])
        lo_, hi_ = float(min(meas.min(), pred.min())) - 0.05, float(max(meas.max(), pred.max())) + 0.05
        fx = Axes(x_range=[lo_, hi_, (hi_ - lo_) / 4], y_range=[lo_, hi_, (hi_ - lo_) / 4], x_length=3.4, y_length=3.4,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -1.3, 0])
        diag = DashedLine(fx.c2p(lo_, lo_), fx.c2p(hi_, hi_), color=GREY_B, stroke_width=1.5)
        fdots = VGroup(*[Dot(fx.c2p(a, b), radius=0.035, color=C.BITS) for a, b in zip(pred, meas)])
        fl = VGroup(label(r"measured", font_size=20, color=GREY_A).next_to(fx, LEFT, buff=0.1).rotate(PI / 2),
                    label(r"the formula", font_size=20, color=GREY_A).next_to(fx, DOWN, buff=0.1))
        fitpic = VGroup(fx, diag, fdots, fl)
        with self.voiceover(
            "In 2022, Jordan Hoffmann and colleagues at DeepMind fitted one formula to all their runs at once: a "
            "floor, plus a term that shrinks with the parameters, plus one that shrinks with the data. Fitted to "
            f"our {int(ch['n_points'])} runs, it misses by {float(ch['rms']):.3f} bits on average. "
            "<bookmark mark='a'/> Now spend a budget. Training costs six operations per parameter per character, "
            "so six N D equals C. Which split gives the lowest loss? Add a Lagrange multiplier, as in part four. "
            "<bookmark mark='b'/> Set both derivatives to zero. <bookmark mark='c'/> Multiply the first by N and "
            "the second by D, and both sides equal six lambda N D. So at the optimum, the last parameter and the "
            "last character pay off equally. <bookmark mark='d'/> Solve, and the best size grows as the budget to "
            f"the power beta over alpha plus beta: {a3:.2f} for our models."
        ) as vo:
            self.play(Write(law), FadeIn(vals), FadeIn(cite_), Create(fx), Create(diag), FadeIn(fl))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in fdots], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(fitpic))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface(self):
        ch, s = load("chinchilla"), load("sweep")
        N, D, Lb = np.asarray(s["N"], float), np.asarray(s["D"], float), np.asarray(s["bits"], float)
        xr = (math.floor(np.log10(N.min()) * 4) / 4, math.ceil(np.log10(N.max()) * 4) / 4)
        yr = (math.log10(D.min()) + 0.3, math.log10(D.max()))
        zlo = float(np.nanmin(Lb)) - 0.05
        ztop = zlo + 1.6
        axes = ThreeDAxes(x_range=[*xr, 1], y_range=[*yr, 1], z_range=[zlo, ztop, 0.5], x_length=6.4, y_length=6.4,
                          z_length=3.2, axis_config={"stroke_color": GREY_C, "include_ticks": False}).shift(DOWN * 0.4)

        def f(u, v):
            return float(min(lnd(ch, 10 ** u, 10 ** v), ztop))

        surf = loss_surface(axes, f, xr, yr, resolution=(36, 36), z_lo=zlo, z_hi=ztop, opacity=0.8)
        pts = VGroup()
        for i in range(len(N)):
            for j in range(len(D)):
                if np.isfinite(Lb[i, j]) and yr[0] <= math.log10(D[j]) <= yr[1] and Lb[i, j] <= ztop:
                    pts.add(Dot3D(axes.c2p(math.log10(N[i]), math.log10(D[j]), Lb[i, j]), radius=0.045, color=WHITE,
                                  resolution=(6, 6)))
        isos = VGroup()
        for C_, col in zip(np.asarray(ch["budgets"], float), BUDGET_COLORS):
            us = np.linspace(xr[0], xr[1], 120)
            vs = math.log10(C_ / 6) - us
            ok = (vs >= yr[0]) & (vs <= yr[1])
            if ok.sum() < 3:
                continue
            isos.add(VMobject(stroke_color=col, stroke_width=4).set_points_smoothly(
                [axes.c2p(u, v, f(u, v)) + np.array([0, 0, 0.03]) for u, v in zip(us[ok], vs[ok])]))
        Cs = np.geomspace(1e9, 1e15, 80)
        no, do = optimum(ch, Cs)
        ok = (np.log10(no) >= xr[0]) & (np.log10(no) <= xr[1]) & (np.log10(do) >= yr[0]) & (np.log10(do) <= yr[1])
        path = VMobject(stroke_color=WHITE, stroke_width=6).set_points_smoothly(
            [axes.c2p(math.log10(n_), math.log10(d_), f(math.log10(n_), math.log10(d_))) + np.array([0, 0, 0.05])
             for n_, d_ in zip(no[ok], do[ok])])
        xl = MathTex(r"\log N", font_size=36, color=NCOL).move_to(axes.c2p(xr[1] + 0.35, yr[0], zlo))
        yl = MathTex(r"\log D", font_size=36, color=DCOL).move_to(axes.c2p(xr[0], yr[1] + 0.35, zlo))
        head = label(r"the loss over size and data \ (the fitted law; \ dots: \ our runs)", font_size=28).to_edge(UP, buff=0.3)
        k0 = label(r"the floor: \ $\log N$ and $\log D$; \ the height: \ the loss", font_size=22, color=GREY_A)
        k1 = label(r"coloured: \ budgets $6ND = C$, \ $10^{11}$ to $10^{13}$", font_size=22, color=GREY_A)
        k2 = label(r"white: \ the floor of the valley, \ the best $N$ and $D$ for each budget", font_size=22, color=WHITE)
        keys = VGroup(k0, k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.3)
        for m in (head, keys):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        with self.voiceover(
            "Here is the whole picture: the fitted loss as a surface above the plane of size and data, both on log "
            "scales, with our runs as points on it. <bookmark mark='a'/> A budget is a straight line across the "
            "plane: where N times D is fixed, more of one means less of the other. <bookmark mark='b'/> Along each "
            "line the surface dips into a valley. Too small a model can't hold what it reads: it underfits. Too "
            "big a model reads too little to finish learning. <bookmark mark='c'/> Join the lowest points of every "
            "valley, and you have the path to follow as the budget grows: the floor of Chinchilla's valley."
        ) as vo:
            self.play(FadeIn(head), FadeIn(k0))
            self.move_camera(phi=62 * DEGREES, theta=-128 * DEGREES, run_time=2.0,
                             added_anims=[Create(axes), FadeIn(surf)])
            self.play(FadeIn(pts), run_time=1.0)
            self.begin_ambient_camera_rotation(rate=0.12)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in isos], lag_ratio=0.25), FadeIn(k1), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(path), FadeIn(k2), run_time=2.0)
            self.wait(1.5)
            self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1.2,
                         added_anims=[FadeOut(VGroup(axes, surf, pts, isos, path))])
        self.clear_scene()

    # ------------------------------------------------------------------
    def methods(self):
        ch = load("chinchilla")
        budgets = np.asarray(ch["budgets"], float)
        a1, a2, a3 = float(ch["a1"]), float(ch["a2"]), float(ch["a3"])
        lo3, hi3 = float(ch["a3_lo"]), float(ch["a3_hi"])
        # left: the iso-FLOP valleys (approach 2)
        allp = np.concatenate([np.asarray(ch[f"iso{C_:.0e}"]).reshape(-1, 3) for C_ in budgets])
        x0, x1 = math.floor(np.log10(allp[:, 0].min()) * 2) / 2, math.ceil(np.log10(allp[:, 0].max()) * 2) / 2
        y0 = math.floor((allp[:, 2].min() - 0.05) * 10) / 10
        y1 = min(math.ceil((allp[:, 2].max() + 0.05) * 10) / 10, y0 + 1.6)
        ax = CornerAxes(x_range=[x0, x1, 0.5], y_range=[y0, y1, 0.2], x_length=5.6, y_length=3.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.5, -0.5, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                      for v in np.arange(math.ceil(y0 * 5) / 5, y1 + 1e-9, 0.2)])
        xn = label(r"parameters $N$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"held-out bits, \ at each budget", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        vall, stars = VGroup(), VGroup()
        nopt2, lopt2 = np.asarray(ch["nopt2"], float), np.asarray(ch["lopt2"], float)
        for C_, col, n2, l2 in zip(budgets, BUDGET_COLORS, nopt2, lopt2):
            p = np.asarray(ch[f"iso{C_:.0e}"]).reshape(-1, 3)
            keep = p[:, 2] <= y1
            vall.add(VGroup(curve(ax, np.log10(p[keep, 0]), p[keep, 2], col, 3),
                            *[Dot(ax.c2p(math.log10(a), b), radius=0.05, color=col) for a, b in zip(p[keep, 0], p[keep, 2])]))
            if np.isfinite(n2) and y0 <= l2 <= y1:
                stars.add(Star(n=5, outer_radius=0.12, color=WHITE, fill_opacity=1).move_to(ax.c2p(math.log10(n2), l2)))
        bkey = VGroup(*[label(rf"$C = {C_ / 10 ** math.floor(math.log10(C_)):g}\times "
                                rf"10^{{{int(math.floor(math.log10(C_)))}}}$",
                              font_size=18, color=col) for C_, col in zip(budgets, BUDGET_COLORS)])
        bkey.arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(ax.c2p(x1, y1), DL, buff=0.1)
        # right: the three estimates of the exponent, against Chinchilla's and Kaplan's
        rows = VGroup(
            VGroup(label(r"", font_size=22), label(r"ours", font_size=24, color=GREY_A),
                   label(r"Chinchilla", font_size=24, color=GREY_A)),
            VGroup(label(r"1. \ the envelope", font_size=22, color=ACOLS[0]), MathTex(f"{a1:.2f}", font_size=30, color=ACOLS[0]),
                   MathTex(r"0.50", font_size=30, color=GREY_B)),
            VGroup(label(r"2. \ the valleys", font_size=22, color=ACOLS[1]), MathTex(f"{a2:.2f}", font_size=30, color=ACOLS[1]),
                   MathTex(r"0.49", font_size=30, color=GREY_B)),
            VGroup(label(r"3. \ the fitted law", font_size=22, color=ACOLS[2]),
                   MathTex(rf"{a3:.2f}\ \scriptstyle({lo3:.2f}\text{{--}}{hi3:.2f})", font_size=30, color=ACOLS[2]),
                   MathTex(r"0.46", font_size=30, color=GREY_B)),
        )
        for i, r_ in enumerate(rows):
            y = 1.75 - 0.55 * i
            r_[0].move_to([0.4, y, 0], aligned_edge=LEFT)
            r_[1].move_to([4.1, y, 0])
            r_[2].move_to([6.2, y, 0])
        hd = label(r"$N_{\text{opt}} \propto C^{\,a}$: \ the exponent $a$", font_size=28, color=WHITE).next_to(rows, UP, buff=0.35)
        kap = label(r"Kaplan (2020): \ $a = 0.73$", font_size=24, color=SP).next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT)
        tpp = float(ch["tpp3"])
        tp = label(rf"the fitted optimum: \ about ${tpp:.0f}$ characters \\ per parameter \ (Chinchilla: \ about $20$ "
                   r"tokens)", font_size=22, color=C.BITS).next_to(kap, DOWN, buff=0.3).align_to(rows, LEFT)
        boot = note(r"in brackets: \ $80\%$ of $100$ bootstrap refits").to_corner(DR, buff=0.2)
        near = all(0.4 <= v <= 0.62 for v in (a1, a2, a3))
        spread = max(a1, a2, a3) - min(a1, a2, a3)
        said1 = (
            "Like theirs, ours say that size and data should grow together, in roughly equal proportion. "
            if near else
            f"Ours spread by {spread:.2f}, and they lean {'toward the model' if a3 > 0.55 else 'toward the data'}. "
        )
        said2 = (
            "Kaplan's 0.73 is well above all three. " if max(a1, a2, a3) < 0.65 else "Kaplan's was 0.73. "
        )
        with self.voiceover(
            "Chinchilla read that path three ways, and so can we. One: the lower envelope of all the training "
            "curves, the best model at each compute. Two: a parabola through the bottom of each budget's valley. "
            "<bookmark mark='a'/> Three: the formula we just solved. <bookmark mark='b'/> "
            f"Our three estimates of the exponent: {a1:.2f}, {a2:.2f} and {a3:.2f}. Chinchilla's were 0.50, 0.49 and "
            "0.46. "
            + said1
            + "<bookmark mark='c'/> "
            + said2
            + f"In characters per parameter, our optimum is about {tpp:.0f}; Chinchilla's was about twenty tokens."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(bkey))
            self.play(LaggedStart(*[Create(v) for v in vall], lag_ratio=0.25), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(st, scale=0.4) for st in stars], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(hd), FadeIn(rows[0]), FadeIn(boot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[:2]) for r_ in rows[1:]], lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(kap), FadeIn(tp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Your budget grows tenfold. \ Make the model $10\times$ bigger, \ train it on $10\times$ "
                          r"the data, \ or grow both by about $3\times$?")
        with self.voiceover(
            "Pause and predict. Your budget grows tenfold. Should you make the model ten times bigger, train it on "
            "ten times the data, or grow both by about three?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Grow size and data together",
                           r"At the optimum the last parameter and the last token pay off equally: \ for language "
                           r"models, \ about $20$ tokens per parameter \ (Hoffmann et al., 2022).",
                           r"next: \ why the first scaling laws said otherwise")
        with self.voiceover(
            "The takeaway: at the compute optimum, the last parameter and the last token pay off equally, and for "
            "language models that means growing size and data together, at about twenty tokens per parameter. Next: "
            "why the first scaling laws said otherwise."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
