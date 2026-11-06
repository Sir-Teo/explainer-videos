from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class LocalPoly(VoiceoverScene):
    def construct(self):
        self.card()
        self.nw()
        self.local_linear()
        self.kernels()
        self.boundary()
        self.design()
        self.motorcycle()
        self.loess_robust()

    def card(self):
        card = chapter_card(5, r"Local polynomials", r"Regression, \ one neighbourhood at a time", lit=(1964,), part=PART)
        with self.voiceover("Chapter five. Local polynomial regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def nw(self):
        rows = [
            cmath(r"m(x)", r"=", r"E(Y \mid X = x)", font_size=32),
            cmath(r"\hat m_{\mathrm{NW}}(x)", r"=", r"\dfrac{\sum_i K((x - x_i)/h)\, y_i}{\sum_i K((x - x_i)/h)}", font_size=30),
            cmath(r"", r"=", r"\arg\min_a \textstyle\sum_i K\bigl(\tfrac{x - x_i}{h}\bigr)(y_i - a)^2", font_size=30),
            cmath(r"\text{local linear}", r":", r"\arg\min_{a, b} \textstyle\sum_i K(\cdot)(y_i - a - b(x_i - x))^2, \ \hat m = \hat a", font_size=26),
        ]
        rows[3][2].set_color(KDEC)
        whys = [why(r"the regression function, \ any shape"), why(r"Nadaraya (1964); \ Watson (1964)"),
                why(r"a locally constant fit"), why(r"a locally weighted line")]
        with self.voiceover(
            "<bookmark mark='a'/> Now regression: estimate the conditional mean m of x, of any shape. "
            "<bookmark mark='b'/> Elizbar Nadaraya and Geoffrey Watson's estimator, both in 1964, is a kernel-weighted "
            "average of the responses near x. <bookmark mark='c'/> It is the weighted least-squares fit of a constant. "
            "<bookmark mark='d'/> Fitting a weighted line instead and keeping its intercept gives local linear regression, "
            "and in general a local polynomial, the approach Jianqing Fan and Irène Gijbels systematized."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def local_linear(self):
        rows = [
            cmath(r"\hat m(x)", r"=", r"\textstyle\sum_i \ell_i(x)\, y_i", font_size=32),
            cmath(r"\text{bias, NW}", r"\approx", r"h^2 \mu_2 \bigl(\tfrac12 m'' + m' f'/f\bigr)", font_size=30),
            cmath(r"\text{bias, local linear}", r"\approx", r"\tfrac12 h^2 \mu_2\, m''", font_size=30),
            cmath(r"\text{variance, both}", r"\approx", r"\dfrac{\sigma^2(x) R(K)}{n h f(x)}", font_size=30),
        ]
        rows[2][2].set_color(KDEC)
        whys = [why(r"a linear smoother: \ the equivalent kernel $\ell(x)$"), why(r"a design-bias term: \ slope times $f'/f$"),
                why(r"gone, \ and the same at the boundary"), why(r"Fan (1992): \ same variance, \ less bias")]
        with self.voiceover(
            "<bookmark mark='a'/> Both are linear smoothers: the fit is a weighted sum of the responses, with weights l of x "
            "called the equivalent kernel. <bookmark mark='b'/> Nadaraya–Watson's bias has a curvature term and a second "
            "term, slope times f prime over f, which appears wherever the design density changes. "
            "<bookmark mark='c'/> Local linear's bias is the curvature term alone, the same at the boundary as in the "
            "interior. <bookmark mark='d'/> And their variances are the same to first order, so Jianqing Fan showed in 1992 "
            "that local linear is the better choice, with minimax efficiency among linear smoothers."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kernels(self):
        d = load("locpoly")
        x = np.asarray(d["x"])
        A = axes([-0.05, 1.05], [-0.03, 0.21], x_length=7.4, y_length=4.4, xlabel=r"$x_i$", ylabel=r"weight $\ell_i(x)$",
                 xticks=[0, 0.5, 1], yticks=[0, 0.1, 0.2], center=[-2.0, 0.3, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(-0.05, 0), ax.c2p(1.05, 0), color=GREY_D, stroke_width=1)
        ek = {k: polyline(ax, x, np.asarray(v), NWC if k.startswith("0") else KDEC, 3) for k, v in d["ek"].items()}
        rows = fit_rows(VGroup(
            label(r"101 equally spaced $x_i$; \ $h = 0.1$", font_size=22),
            label(r"at $x = 0.5$: \ both the same bump", font_size=22, color=KDEC),
            label(r"orange: \ NW at $x = 0$: \ half a bump, \ all inside", font_size=22, color=NWC),
            label(r"blue: \ local linear at $x = 0$: \ negative far weights", font_size=22, color=KDEC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The equivalent kernels for a hundred and one equally spaced points and h of point one. "
            "<bookmark mark='b'/> At the centre, both methods give the same symmetric bump. <bookmark mark='c'/> At the left "
            "boundary, Nadaraya–Watson can only average points to the right, so its weights are half a bump, centred away "
            "from zero. <bookmark mark='d'/> Local linear's weights reach further and turn negative: it extrapolates the "
            "local trend back to the edge, which removes the bias."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ek["0_0.5"]), Create(ek["1_0.5"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ek["0_0"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ek["1_0"]), FadeIn(rows[3]))
        self.clear_scene()

    def boundary(self):
        d = load("locpoly")
        x = np.asarray(d["x"])
        A = axes([0, 1], [0, 2.1], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"fit", xticks=[0, 0.5, 1], yticks=[0, 1, 2],
                 center=[-2.0, 0.3, 0])
        ax = A.ax
        truth = curve(ax, x, 2 * x, TRUE, 10).set_stroke(opacity=0.35)
        nw = polyline(ax, x, d["lin"]["0"], NWC, 3)
        ll = polyline(ax, x, d["lin"]["1"], KDEC, 3)
        rows = fit_rows(VGroup(
            label(r"noise-free data on the line $y = 2x$", font_size=22, color=TRUE),
            label(rf"NW: \ at 0 it says {d['lin']['0'][0]:.2f}, \ at 1, \ {d['lin']['0'][-1]:.2f}", font_size=22, color=NWC),
            label(r"local linear: \ exact everywhere", font_size=22, color=KDEC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The consequence, with no noise at all: data exactly on the line y equals two x. "
            "<bookmark mark='b'/> Nadaraya–Watson bends at both ends, to point one five at zero and one point eight five at "
            "one, because it can only average neighbours on one side. <bookmark mark='c'/> Local linear reproduces the line "
            "exactly: any local polynomial of degree p reproduces polynomials of degree p."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(nw), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ll), FadeIn(rows[2]))
        self.clear_scene()

    def design(self):
        d = load("locpoly")
        e, w, ee = np.asarray(d["e"]), np.asarray(d["w"]), np.asarray(d["ee"])
        A = axes([1.4, 5.3], [40, 100], x_length=7.4, y_length=4.4, xlabel=r"eruption length (minutes)",
                 ylabel=r"wait until the next (minutes)", xticks=[2, 3, 4, 5], yticks=[50, 70, 90], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=WHITE, fill_opacity=0.6) for a, b in zip(e, w)])
        fit = curve(ax, ee, np.asarray(d["fw"]), KDEC, 4)
        b = np.polyfit(e, w, 1)
        rows = fit_rows(VGroup(
            label(r"each eruption against the wait that followed", font_size=22),
            label(r"blue: \ local linear, \ $h = 0.3$", font_size=22, color=KDEC),
            label(rf"least squares line: \ {b[1]:.1f} $+$ {b[0]:.1f} $\times$ length", font_size=22, color=GREY_A),
            label(r"two clusters, \ a gap between: \ the line is nearly right", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real regression: each Old Faithful eruption's length against the wait that followed it, "
            "the basis of the rangers' predictions. <bookmark mark='b'/> The local linear fit with h of point three. "
            "<bookmark mark='c'/> It is close to the least-squares line, thirty-three plus eleven minutes per minute of "
            "eruption, <bookmark mark='d'/> with a flattening among the long eruptions. Through the gap between the two "
            "clusters, where there are almost no data, the local fit simply interpolates."
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def motorcycle(self):
        d = load("locpoly")
        t, a, tt = np.asarray(d["t"]), np.asarray(d["a"]), np.asarray(d["tt"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"milliseconds after impact",
                 ylabel=r"head acceleration ($g$)", xticks=[0, 20, 40, 60], yticks=[-100, 0, 50], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE, fill_opacity=0.7) for x, y in zip(t, a)])
        nw = curve(ax, tt, np.asarray(d["nw"]), NWC, 3)
        ll = curve(ax, tt, np.asarray(d["ll"]), KDEC, 3)
        rows = fit_rows(VGroup(
            label(r"133 readings from a simulated crash", font_size=22),
            label(r"orange: \ Nadaraya--Watson, \ $h = 2$ ms", font_size=22, color=NWC),
            label(r"blue: \ local linear, \ $h = 2$ ms", font_size=22, color=KDEC),
            label(r"they part at the ends, \ and where the slope is steep", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic test bed: a helmeted cadaver in a simulated motorcycle crash, and the "
            "acceleration of its head over the first sixty milliseconds, a hundred and thirty-three readings at irregular "
            "times. Flat, then a sharp dip to minus a hundred and thirty g, a rebound, and a ringing decay. "
            "<bookmark mark='b'/> Nadaraya–Watson with a two-millisecond bandwidth. <bookmark mark='c'/> Local linear with "
            "the same bandwidth. <bookmark mark='d'/> They agree where the curve is flat and part where the slope is steep and "
            "the times are unevenly spaced: there the design bias of Nadaraya–Watson shows."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(nw), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ll), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def loess_robust(self):
        rows = [
            cmath(r"\text{LOESS}", r":", r"\text{local linear (or quadratic), \ the nearest } \alpha n \text{ points}", font_size=28),
            cmath(r"K", r"=", r"\tfrac{70}{81}(1 - |u|^3)^3: \ \text{tricube}", font_size=30),
            cmath(r"\text{robustness}", r":", r"\text{reweight by } (1 - (r_i/6\,\mathrm{MAD})^2)^2_+, \ \text{refit}", font_size=28),
            cmath(r"\text{span}", r":", r"\text{a bandwidth that adapts to the design}", font_size=30),
        ]
        rows[2][2].set_color(KDEC)
        whys = [why(r"Cleveland (1979)"), why(r"smooth, \ compact"), why(r"bisquare weights: \ outliers fade out"),
                why(r"wide where data are sparse")]
        with self.voiceover(
            "<bookmark mark='a'/> William Cleveland's LOESS, the most used smoother in practice, is local linear or quadratic "
            "regression on the nearest fraction alpha of the points. <bookmark mark='b'/> With the tricube kernel. "
            "<bookmark mark='c'/> And with robustness iterations: residuals far from zero, measured against six median "
            "absolute residuals, get small bisquare weights, and the fit is redone, so a few wild points can't drag it. "
            "<bookmark mark='d'/> Using a fixed number of neighbours rather than a fixed width makes the bandwidth wide where "
            "data are sparse and narrow where they are dense, a natural defence against the curse."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
