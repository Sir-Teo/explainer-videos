from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE, expo, load, log_axes, mant

C64, C32 = C.TRUE_P, GRAD


def error_window(values, lo, hi):
    """Disclosed log display limits; invalid errors remain gaps, zero is at the floor."""
    values = np.asarray(values, float)
    valid = np.isfinite(values) & (values >= 0)
    logs = np.full(values.shape, np.nan)
    logs[valid] = np.log10(np.maximum(values[valid], 10.0 ** lo))
    return np.clip(logs, lo, hi), dict(
        floor=int(np.sum(valid & (values < 10.0 ** lo))),
        ceiling=int(np.sum(valid & (values > 10.0 ** hi))), omitted=int(np.sum(~valid)))


def aggregate_minimum(hs, errors):
    """Optimum of the curve actually drawn, not median(direction argmin)."""
    hs, errors = np.asarray(hs, float), np.asarray(errors, float)
    eligible = np.isfinite(hs) & (hs > 0) & np.isfinite(errors) & (errors >= 0)
    if not eligible.any():
        return None
    indices = np.flatnonzero(eligible)
    i = int(indices[np.argmin(errors[eligible])])
    return dict(index=i, h=float(hs[i]), error=float(errors[i]))


def prediction_verdict(ratios):
    if not ratios or not all(math.isfinite(r) and r > 0 for r in ratios):
        return "A finite comparison with the prediction is unavailable."
    factor = max(max(r, 1 / r) for r in ratios)
    if factor < 3:
        return "Both plotted median-curve optima are within a factor of three of the predicted steps."
    return f"The largest discrepancy is a factor of {factor:.1f}; the prediction is an error-model estimate, not a guarantee."


class GradCheck(VoiceoverScene):
    def construct(self):
        self.card()
        self.cancellation()
        self.derive()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Cancellation, and the gradient check", r"How small should a nudge be?", part=PART)
        with self.voiceover("Chapter ten. Cancellation, and the gradient check."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cancellation(self):
        d = load("cancel")
        xs = np.asarray(d["xs"])
        g = log_axes((-6, 0), (-17, 1), x_length=6.8, y_length=4.6, xlabel=r"$x$",
                     ylabel=r"relative error of $(1 - \cos x)/x^2$", center=[-2.6, -0.5, 0], ystep=4)
        ax = g.ax

        def c(key, col, w=3):
            y, _ = error_window(d[key], -17, 1)
            return curve(ax, np.log10(xs), y, col, w)

        c32, c64 = c("naive_fp32", C32), c("naive_fp64", C64)
        ys32, _ = error_window(d["stable_fp32"], -17, 1)
        s32 = VGroup(*[Dot(ax.c2p(math.log10(x_), y_), radius=0.025, color=WHITE)
                       for x_, y_ in zip(xs[::2], ys32[::2]) if np.isfinite(y_)])
        pred = np.asarray(d["pred_fp32"])
        okp = pred < 10
        pr32 = DashedVMobject(curve(ax, np.log10(xs[okp]), np.log10(pred[okp]), C32, 1.5), num_dashes=40)
        leg = VGroup(label(r"float32, \ as written", font_size=22, color=C32),
                     label(r"float64, \ as written", font_size=22, color=C64),
                     label(r"float32, \ rewritten as $2\sin^2(x/2)/x^2$", font_size=22, color=WHITE),
                     label(r"predicted: \ $u / (x^2/2)$", font_size=22, color=C32)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        leg.move_to([4.2, 1.3, 0])
        ex = VGroup(label(rf"float32, \ $x = 10^{{-4}}$:", font_size=22, color=GREY_A),
                    MathTex(rf"\cos x \to {d['cos32_x0']}", font_size=28, color=C32),
                    MathTex(rf"\frac{{1 - \cos x}}{{x^2}} \to {d['naive32_x0']:g} \quad (\text{{true: }} 0.5)", font_size=28,
                            color=C32)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -1.6, 0])
        limits = note(r"display: below $10^{-17}$ (including zero) at the floor; above $10$ at the ceiling",
                      font_size=17).to_edge(DOWN, buff=0.18)
        with self.voiceover(
            "One more way numbers go wrong, and it explains how to check a gradient. Take one minus cos x, over x "
            "squared: for small x it is very nearly one half. <bookmark mark='a'/> Computed as written, in float32, "
            "the error explodes as x shrinks, <bookmark mark='b'/> and at x of ten to the minus four, cos x rounds to "
            "exactly one, and the answer is zero. <bookmark mark='c'/> This is cancellation: subtracting two nearly "
            "equal numbers keeps their rounding errors but loses their size, so the relative error grows like one "
            "over x squared, just as predicted. Float64 only delays it. <bookmark mark='d'/> Rewritten without the "
            "subtraction, the same formula avoids that cancellation over this sampled range. Errors below the "
            "display floor, including zero, are drawn at the floor."
        ) as vo:
            self.play(FadeIn(g), FadeIn(limits))
            vo.wait_until("a")
            self.play(Create(c32), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(Create(pr32), FadeIn(leg[3]), Create(c64), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(s32), FadeIn(leg[2]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"f(x \pm h)", r"=", r"f \pm h f' + \tfrac{h^2}{2} f'' \pm \tfrac{h^3}{6} f''' + \dots", font_size=34),
            cmath(r"\frac{f(x+h) - f(x-h)}{2h}", r"=", r"f' + \tfrac{h^2}{6} f''' + \dots", font_size=34),
            cmath(r"\text{rounding: \ } \frac{u|f| + u|f|}{2h}", r"=", r"\frac{u|f|}{h}", font_size=34),
            cmath(r"E(h)", r"\approx", r"\tfrac{h^2}{6}|f'''| + \frac{u|f|}{h}", font_size=36),
            cmath(r"h^*", r"=", r"\Big(\frac{3u|f|}{|f'''|}\Big)^{1/3}", font_size=36, colors={r"h^*": GRAD}),
        ]
        whys = [why(r"Taylor, \ to third order", font_size=22), why(r"the even terms cancel: \ truncation error", font_size=22),
                why(r"each $f$ is off by about $u|f|$, \\ $u$ the unit roundoff: \ cancellation", font_size=22),
                why(r"both together", font_size=22), why(r"$E'(h)=0$; nonzero $f'''$, local error model", font_size=22)]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-2.2, buff=0.38, edge=6.9)
        head = label(r"central differences: \ two errors", font_size=24, color=GREY_A).to_corner(UL, buff=0.3)
        with self.voiceover(
            "A gradient check is a cancellation on purpose. Expand f a step either side of x, by Taylor's theorem. "
            "<bookmark mark='a'/> Subtract and divide by two h: the even terms cancel, leaving the derivative plus a "
            "truncation error that shrinks like h squared. <bookmark mark='b'/> But each value of f was rounded, by "
            "about u times f, u the unit roundoff, and the subtraction keeps those errors while dividing by a tiny 2 "
            "h: a rounding error that grows like one over h. <bookmark mark='c'/> Add the two, <bookmark mark='d'/> "
            "and set the derivative to zero: this local model predicts a step near the cube root of three u times "
            "the absolute value of f over the absolute third derivative, when that derivative is nonzero. "
            "Too large a step and Taylor's error wins; too small and rounding does."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("vcurve")
        hs = np.asarray(d["hs"])
        pred = d["pred"]
        g = log_axes((-13, 0), (-14, 0), x_length=7.0, y_length=4.6, xlabel=r"the step $h$",
                     ylabel=r"error of the central difference", center=[-2.7, -0.2, 0], xstep=2, ystep=2)
        ax = g.ax
        curves, marks = VGroup(), VGroup()
        optima, limits = {}, []
        for k, col in (("fp64", C64), ("fp32", C32)):
            y = np.asarray(d[f"central_{k}"])
            yy, count = error_window(y, -14, 0)
            optima[k] = aggregate_minimum(hs, y)
            band_lo = np.asarray(d[f"central_{k}_all"]).min(0)
            band_hi = np.asarray(d[f"central_{k}_all"]).max(0)
            low, count_lo = error_window(band_lo, -14, 0)
            high, count_hi = error_window(band_hi, -14, 0)
            limits.append({key: count[key] + count_lo[key] + count_hi[key] for key in count})
            # Missing samples split the ribbon rather than fabricating a connection.
            finite = np.isfinite(low) & np.isfinite(high)
            ribbons = VGroup()
            for run in np.split(np.arange(len(hs)), np.flatnonzero(np.diff(finite.astype(int))) + 1):
                if len(run) >= 2 and finite[run].all():
                    ribbons.add(band(ax, np.log10(hs[run]), low[run], high[run], col, 0.15))
            curves.add(VGroup(ribbons, curve(ax, np.log10(hs), yy, col, 3.5)))
            marker = VGroup()
            predicted = float(pred[k]["central"])
            if math.isfinite(predicted) and 1e-13 <= predicted <= 1:
                ph = math.log10(predicted)
                marker.add(DashedLine(ax.c2p(ph, -14), ax.c2p(ph, 0), color=col, stroke_width=1.8))
            if optima[k] is not None:
                i = optima[k]["index"]
                marker.add(Dot(ax.c2p(math.log10(hs[i]), yy[i]), radius=0.08, color=col))
            marks.add(marker)
        optimum_rows = []
        for k, name, col in (("fp64", "float64", C64), ("fp32", "float32", C32)):
            o = optima[k]
            predicted = float(pred[k]["central"])
            predicted_text = sci(predicted, 1) if math.isfinite(predicted) and predicted > 0 else r"\mathrm{unavailable}"
            text = (rf"{name}: ${sci(o['h'], 1)}$ \ (${predicted_text}$)" if o is not None else
                    rf"{name}: no finite median-curve optimum")
            optimum_rows.append(label(text, font_size=23, color=col))
        e64 = optima["fp64"]["error"] if optima["fp64"] else float("nan")
        e32 = optima["fp32"]["error"] if optima["fp32"] else float("nan")
        table = VGroup(
            label(r"median-curve best step\\(predicted step)", font_size=22, color=GREY_A),
            *optimum_rows,
            label(rf"smallest median errors:\\${sci(e64, 1) if math.isfinite(e64) else '?'}$, "
                  rf"${sci(e32, 1) if math.isfinite(e32) else '?'}$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([4.3, 0.8, 0])
        if table.width > 4.6:
            table.scale_to_fit_width(4.6)
        floors, ceilings, omitted = (sum(c[key] for c in limits) for key in ("floor", "ceiling", "omitted"))
        tag = note(r"computed: chapter 7's network; $8$ paired directions, median and range\\"
                   r"dot: minimum of solid median curve; dashed: predicted step if inside the window\\"
                   rf"median/range samples: $10^{{-14}}$ floor incl. zero ({floors}); $1$ ceiling ({ceilings}); invalid omitted ({omitted})",
                   font_size=16).to_edge(DOWN, buff=0.15)
        ratios = [optima[k]["h"] / pred[k]["central"] if optima[k] is not None and pred[k]["central"] > 0
                  else float("nan") for k in ("fp64", "fp32")]
        verdict = prediction_verdict(ratios)
        slope = float(d["slope_right_fp64"])
        slope_v = (f"Its fitted right-hand slope is {slope:.2f}." if math.isfinite(slope) else
                   "There are too few eligible samples for a fitted right-hand slope.")
        e6 = 10 ** float(d["at_1e-6_fp64"])
        step_v = (f"At chapter seven's step of a millionth, the float64 median error is {e6:.2e}."
                  if math.isfinite(e6) else
                  "At chapter seven's step of a millionth, a finite float64 median error is unavailable.")
        error_v = (f"The smallest median errors are {e64:.2e} in float64 and {e32:.2e} in float32."
                   if math.isfinite(e64) and math.isfinite(e32) else
                   "At least one precision has no finite median-error optimum to report.")
        with self.voiceover(
            "Here it is measured, on chapter seven's network, along the same eight random directions in both "
            "precisions. The solid curves are pointwise median errors, and the shaded bands show the range. "
            "<bookmark mark='a'/> First inspect float64 for the competition between truncation and rounding. "
            f"{slope_v} <bookmark mark='b'/> Now compare float32. <bookmark mark='c'/> Each dot marks the minimum "
            f"of the median curve actually drawn; it is not the median of the eight best steps. {verdict} "
            f"<bookmark mark='d'/> {error_v} For comparison, {step_v} The local error model guides the step choice; "
            "the measured curve checks it. Values outside "
            "the displayed error range are shown at its stated floor or ceiling."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(curves[0][0]), Create(curves[0][1]), FadeIn(table[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(curves[1][0]), Create(curves[1][1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(marks), FadeIn(table[1]), FadeIn(table[2]))
            vo.wait_until("d")
            self.play(FadeIn(table[3]))
        self.wait(0.3)
        self.clear_scene()
