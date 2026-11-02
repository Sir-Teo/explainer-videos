from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card, tbar

HAC_CODE = [
    "def _hac_meat(X, u, lags, kernel=\"bartlett\"):",
    "    Xu = X * u[:, None]                 # the scores x_t u_t",
    "    S = Xu.T @ Xu                       # lag 0: White",
    "    for l_ in range(1, lags + 1):",
    "        w = 1 - l_ / (lags + 1) if kernel == \"bartlett\" else 1.0",
    "        G = Xu[l_:].T @ Xu[:-l_]        # lag-l autocovariance",
    "        S += w * (G + G.T)",
    "    return S",
    "# in ols(..., se=\"nw\"):",
    "S = _hac_meat(Xd, u, lags)",
    "V = XtX_inv @ S @ XtX_inv              # bread, meat, bread",
]


class HAC(VoiceoverScene):
    def construct(self):
        o = load("overlap")
        h = load("hac")
        s = load("har_size")
        self.card()
        self.window(o, h)
        self.derive()
        self.lab(h, o)
        self.size(s, h)

    def card(self):
        c = chapter_card(2, r"Newey--West: counting dependent data", r"How many independent observations do you have?",
                         part=PART)
        with self.voiceover("Chapter two. Newey-West: counting dependent data."):
            show_card(self, c)
        self.play(FadeOut(c))

    def window(self, o, h):
        acf = np.asarray(h["acf"])
        K = 100
        g = axes([-K - 2, K + 2], [-0.4, 1.05], x_length=8.2, y_length=3.6, xlabel=r"lag $k$, months",
                 ylabel=r"autocorrelation of the scores $x_t \hat u_t$", xticks=[-100, -59, 0, 59, 100],
                 yticks=[0, 0.5, 1], font_size=17).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
        ax = g.ax
        ks = np.arange(-K, K + 1)
        vals = np.array([acf[abs(k)] for k in ks])
        L = ValueTracker(0.0)

        def bars():
            Lv = L.get_value()
            out = VGroup()
            for k, v in zip(ks, vals):
                w = max(0.0, 1 - abs(k) / (Lv + 1)) if Lv > 0 else (1.0 if k == 0 else 0.0)
                out.add(Line(ax.c2p(k, 0), ax.c2p(k, v), stroke_width=2.4,
                             color=interpolate_color(ManimColor(GREY_D), ManimColor(DATA_C), w)))
            return out
        bar_m = always_redraw(bars)
        tri = always_redraw(lambda: Polygon(ax.c2p(-L.get_value() - 1, 0), ax.c2p(0, 1.0), ax.c2p(L.get_value() + 1, 0),
                                            stroke_color=EST, stroke_width=2, fill_color=EST, fill_opacity=0.12)
                            if L.get_value() > 0.5 else VectorizedPoint(ax.c2p(0, 0)))
        Ls, tL = np.asarray(h["L"], float), np.asarray(h["t_L"])
        tval = lambda: float(np.interp(L.get_value(), Ls, tL))  # noqa: E731
        t_ro = readout(r"t =", tval, digits=1, font_size=36, color=EST)
        L_ro = readout(r"L =", lambda: L.get_value(), digits=0, font_size=30, color=GREY_A)
        lrv = lambda: tL[0] ** 2 / max(tval(), 0.5) ** 2  # noqa: E731
        thermo_ax = axes([0, 1], [0, 40], x_length=0.6, y_length=3.0, yticks=[1, 10, 20, 30], font_size=15,
                         ylabel=r"$\hat S / \hat\Gamma_0$")
        fill = always_redraw(lambda: Rectangle(width=0.5, height=max(thermo_ax.ax.c2p(0, min(lrv(), 40))[1]
                                                                      - thermo_ax.ax.c2p(0, 0)[1], 0.01),
                                               stroke_width=0, fill_color=EST, fill_opacity=0.7).move_to(
            thermo_ax.ax.c2p(0.5, 0), aligned_edge=DOWN))
        right = VGroup(VGroup(t_ro, L_ro).arrange(DOWN, aligned_edge=LEFT, buff=0.2), VGroup(thermo_ax, fill)).arrange(
            RIGHT, buff=0.7).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        top = wrapped_label(rf"Shiller, 1871--2020: five-year real returns on the log dividend yield, "
                            rf"{h['T']:,} overlapping windows. Neighbours share 59 of 60 months.".replace(",", "{,}"),
                            12.0, 22, GREY_A).to_edge(UP, buff=0.35)
        src = real_data(r"autocorrelations of the regression's own scores; the window is Bartlett's triangle")
        with self.voiceover(
            "Chapter one's sandwich, with the band lit. Regress the next five years' real return on today's dividend "
            f"yield, over Shiller's century and a half. Least squares reports a t-statistic of {o['est']['naive']['t']:.0f}. "
            "<bookmark mark='a'/> Here are the autocorrelations of the regression's scores, lag by lag. Neighbouring "
            "windows share fifty-nine of sixty months, so they stay high out to lag fifty-nine and beyond. The naive "
            "formula keeps only lag zero. <bookmark mark='b'/> Newey and West lay a triangle over the bars and add them "
            "up, weighted by its height. As the window opens, the long-run variance climbs and the t-statistic falls. "
            f"<bookmark mark='c'/> At a hundred and twenty months it is {h['t_nw']:.1f}. The window is the estimator: too "
            "narrow misses dependence, too wide adds noise."
        ) as vo:
            self.play(FadeIn(top), FadeIn(g), FadeIn(src), FadeIn(right))
            self.add(bar_m, tri)
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(L.animate.set_value(60), run_time=vo.until("c") * 0.6, rate_func=linear)
            self.play(L.animate.set_value(120), run_time=max(vo.until("c") - 0.2, 0.5), rate_func=linear)
            vo.wait_until("c")
            self.play(Indicate(t_ro, color=EST))
        bar_m.clear_updaters()
        tri.clear_updaters()
        fill.clear_updaters()
        t_ro.num.clear_updaters()
        L_ro.num.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"S": EST, r"\hat S_{NW}": EST, r"h": ALT}
        rows = [cmath(r"\sqrt T(\hat\beta - \beta)", r"=", r"\Big(\tfrac1T \textstyle\sum x_t x_t^\top\Big)^{-1}"
                      r"\tfrac{1}{\sqrt T}\textstyle\sum_t z_t", font_size=36, colors=C_),
                cmath(r"\mathrm{Var}\Big(\tfrac{1}{\sqrt T}\textstyle\sum_t z_t\Big)", r"=",
                      r"\textstyle\sum_{|k|<T}\big(1 - \tfrac{|k|}{T}\big)\Gamma_k \;\to\; S = "
                      r"\textstyle\sum_{k=-\infty}^{\infty}\Gamma_k", font_size=36, colors=C_),
                cmath(r"S", r"=", r"2\pi f_z(0)", font_size=36, colors=C_),
                cmath(r"\hat S_{NW}", r"=", r"\hat\Gamma_0 + \textstyle\sum_{k=1}^{L}\big(1 - \tfrac{k}{L+1}\big)"
                      r"(\hat\Gamma_k + \hat\Gamma_k^\top)", font_size=36, colors=C_),
                cmath(r"y_t = \textstyle\sum_{j=1}^{h}\varepsilon_{t+j}", r"\Rightarrow",
                      r"\rho_k = \tfrac{h - k}{h},\ \ \textstyle\sum_{|k|<h}\rho_k = h", font_size=36, colors=C_)]
        whys = [why(r"chapter one, scaled: $z_t = x_t u_t$ are the scores"),
                why(r"expand the square of a sum: every pair of dates contributes its covariance; stationarity"),
                why(r"the long-run variance is the spectrum of the scores at frequency zero"),
                why(r"Bartlett weights keep $\hat S$ positive; truncating the plain sum can go negative"),
                why(r"overlap alone: the naive variance is too small by a factor $h$, its standard error by $\sqrt h$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.75, edge=6.8)
        with self.voiceover(
            "Why a sum of autocovariances? Chapter one's error, scaled by root T, is a fixed matrix times the scaled sum "
            "of the scores. <bookmark mark='a'/> The variance of a sum adds every pair's covariance: T terms on the "
            "diagonal, and T minus k pairs k apart, each sharing gamma k. Divide by T and let T grow: the limit is S, the "
            "sum of all the autocovariances, the long-run variance, <bookmark mark='b'/> which is also the spectrum of "
            "the scores at frequency zero, the power in their slowest movements. <bookmark mark='c'/> Summing all sample "
            "autocovariances is noisy and can even go negative; Bartlett's declining weights keep it positive; Hansen and "
            "Hodrick used flat weights out to the horizon. <bookmark mark='d'/> With h-month overlap, neighbours k apart "
            "have correlation h minus k over h, and these sum to h: the naive variance is h times too small, sixty times "
            "for five-year returns."
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
        self.wait(0.5)
        self.clear_scene()

    def lab(self, h, o):
        card = lab_card(r"Newey--West in the House", HAC_CODE, source="explainer/quant/house/econ.py", width=7.4,
                        font_size=18).to_corner(UL, buff=0.35)
        outs = [f"ols(fwd, dy)                    t = {o['est']['naive']['t']:.1f}",
                f"ols(..., se='nw', lags=120)     t = {h['t_nw']:.1f}",
                f"ols(..., se='hh', lags=59)      t = {h['t_hh']:.1f}",
                f"hodrick_se(r1, dy, 60)          t = {h['t_hodrick']:.1f}"]
        notes = VGroup(
            label(r"Hodrick (1992), ``1B'':", font_size=22, color=ALT),
            wrapped_label(r"under the null, regress one-month returns on the predictor summed back over five years: "
                          r"no overlapping residuals enter at all", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4).shift(DOWN * 0.4)
        with self.voiceover(
            "The House's code. The scores are regressors times residuals; lag zero is White; each lag's autocovariance "
            "is added on both sides of the diagonal with Bartlett's weight; the meat goes between the bread. "
            f"<bookmark mark='a'/> On Shiller's data: naive, {o['est']['naive']['t']:.1f}. Newey-West with a hundred and twenty lags, "
            f"{h['t_nw']:.1f}. Hansen-Hodrick, {h['t_hh']:.1f}. <bookmark mark='b'/> And Robert Hodrick's 1992 "
            "alternative avoids overlap altogether: regress one-month returns on the yield summed over the past five "
            f"years. It gives {h['t_hodrick']:.1f}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs[:3], run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(notes))
            r = Text(outs[3], font="DejaVu Sans Mono", font_size=19, color=WHITE).scale(card.text_scale)
            r.next_to(card.out, DOWN, buff=0.12).align_to(card.out, LEFT)
            self.play(AddTextLetterByLetter(r), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    def size(self, s, h):
        rates = s["rate"]
        names = [r"naive", rf"NW, $L = {s['L_rot']}$", r"NW, $L = h - 1$", r"NW, wide, fixed-$b$", r"EWC"]
        cols = [BAD, ALT, ALT, GOOD, GOOD]
        rhos = ["0.0", "0.9", "0.95", "0.99"]
        g = axes([0, 4], [0, 0.6], x_length=7.4, y_length=3.6, ylabel=r"rejections of a true null at 5\%, $h = 12$",
                 xticks=[], yticks=[0, 0.05, 0.2, 0.4, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        groups = VGroup()
        for i, rho in enumerate(rhos):
            v = rates[f"{rho}|12"]
            grp = VGroup(*[tbar(ax, i + 0.14 + 0.18 * j, min(v[j], 0.6), cols[j], width=0.15) for j in range(5)])
            groups.add(grp)
        labs = VGroup(*[MathTex(rf"\rho = {r}", font_size=20, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                        for i, r in enumerate(["0", "0.9", "0.95", "0.99"])])
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(4, 0.05), color=GOOD, stroke_width=2)
        leg = legend(list(zip(cols, names)), font_size=18).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        r95 = rates["0.95|12"]
        txt = VGroup(
            label(rf"{s['reps']:,} null worlds per bar, $T = {s['T']}$ months".replace(",", "{,}"), font_size=19,
                  color=GREY_B),
            MathTex(r"t \Rightarrow \frac{W(1)}{\sqrt{Q_b(\tilde W)}}\ \ (b = L/T \text{ fixed})", font_size=28),
            MathTex(rf"\hat S_{{EWC}} = \tfrac1\nu \textstyle\sum_{{j=1}}^{{\nu}} \Lambda_j^2,\ \ t \sim t_\nu,\ "
                    rf"\nu = {s['nu']}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        bs, cvs, poly = h["b_grid"], h["cv_grid"], h["cv_poly"]
        cvtab = MathTex(r"b:\ " + r",\ ".join(f"{b:g}" for b in bs) + r"\\ \text{cv}:\ "
                        + r",\ ".join(f"{c:.2f}" for c in cvs), font_size=22, color=GOOD)
        cvtab.next_to(txt, DOWN, buff=0.25).align_to(txt, LEFT)
        if cvtab.width > 5.4:
            cvtab.scale_to_fit_width(5.4)
        q = predict(r"Monthly returns, no overlap ($h = 1$), a predictor with $\rho = 0$. Does Newey--West still "
                    r"over-reject?", width=11.0).to_edge(DOWN, buff=0.15)
        r0 = rates["0.0|1"]
        with self.voiceover(
            "Do the corrections work? Simulate worlds where nothing predicts anything, with twelve-month overlapping "
            "returns, and count how often each test rejects at five percent. <bookmark mark='a'/> With a persistent "
            f"predictor, the naive test rejects {100 * r95[0]:.0f} percent of the time, Newey-West with the usual short "
            f"window {100 * r95[1]:.0f}, with the window at the overlap {100 * r95[2]:.0f}. <bookmark mark='b'/> Nicholas "
            "Kiefer and Timothy Vogelsang explained why in 2005: hold the window's share of the sample, b, fixed, and "
            "the estimated long-run variance stays random, so t has fatter tails. Their fixed-b critical values grow "
            f"with b; simulated, about {cvs[2]:.2f} at a tenth of the sample, {cvs[4]:.2f} at three tenths. "
            "<bookmark mark='c'/> Lazarus, Lewis, Stock and Watson recommended in 2018 a much wider window with fixed-b "
            f"values, or the equal-weighted cosine estimator, {s['nu']} squared cosine projections with Student's t. They "
            f"reject {100 * r95[3]:.0f} and {100 * r95[4]:.0f} percent here. <bookmark mark='d'/> Pause and predict: no "
            f"overlap, no persistence. Every test is near five percent; naive {100 * r0[0]:.1f}. The problem is overlap "
            "times persistence."
            " Overlap is one shape of dependence. Next: shocks shared across firms."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), Create(five), FadeIn(leg), FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for grp in groups for b in grp[:3]], lag_ratio=0.08,
                                  run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]), FadeIn(cvtab))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for grp in groups for b in grp[3:]], lag_ratio=0.1,
                                  run_time=2), FadeIn(txt[2]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
