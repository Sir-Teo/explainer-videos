from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, expo, load, log_axes, mant

CLASS_COL = [C.TRUE_P, GRAD, C.BITS]


def region_image(P, side, width):
    """Class probabilities on a grid as a picture: each pixel the classes' colours, mixed by probability."""
    cols = np.array([ManimColor(c).to_rgb() for c in CLASS_COL])
    rgb = (np.asarray(P)[:, :, None] * cols[None]).sum(1).reshape(side, side, 3)
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = 0.45 * rgb + 0.55 * bg
    rgb = rgb[::-1]  # rows from the top
    img = ImageMobject((np.concatenate([rgb, np.ones((side, side, 1))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(width)


def symlog(v, lin=1e-3):
    """Signed log scale for eigenvalues relative to the largest: 0 at 0, +-1 at +-1, log-spaced below."""
    v = np.asarray(v, float)
    return np.sign(v) * np.log10(1 + np.abs(v) / lin) / math.log10(1 + 1 / lin)


def displayed_logs(values, lo, hi):
    values = np.asarray(values, float)
    valid = np.isfinite(values) & (values >= 0)
    out = np.full(values.shape, np.nan)
    out[valid] = np.clip(np.log10(np.maximum(values[valid], 10.0 ** lo)), lo, hi)
    counts = dict(floor=int(np.sum(valid & (values < 10.0 ** lo))),
                  ceiling=int(np.sum(valid & (values > 10.0 ** hi))), omitted=int(np.sum(~valid)))
    return out, counts


def spectrum_state(eigenvalues, thresholds):
    eigenvalues = np.asarray(eigenvalues, float)
    finite = eigenvalues[np.isfinite(eigenvalues)]
    omitted = int(eigenvalues.size - finite.size)
    rho = float(np.max(np.abs(finite))) if finite.size else float("nan")
    if not finite.size:
        return dict(eigenvalues=finite, normalized=np.zeros(finite.shape), rho=rho, omitted=omitted,
                    negative=None, high_positive=None, flat=None)
    if rho == 0:
        return dict(eigenvalues=finite, normalized=np.zeros(finite.shape), rho=rho, omitted=omitted,
                    negative=0, high_positive=0, flat=1.0)
    normalized = finite / rho
    return dict(eigenvalues=finite, normalized=normalized, rho=rho, omitted=omitted,
                negative=int(np.sum(normalized < -thresholds["negative_relative"])),
                high_positive=int(np.sum(normalized > thresholds["outlier_relative"])),
                flat=float(np.mean(np.abs(normalized) <= thresholds["flat_relative"])))


def power_comparison(estimates, eigenvalues):
    estimates, eigenvalues = np.asarray(estimates, float), np.asarray(eigenvalues, float)
    finite = eigenvalues[np.isfinite(eigenvalues)]
    rho = float(np.max(np.abs(finite))) if finite.size else float("nan")
    dominant = np.unique(finite[np.abs(finite) == rho])
    target = float(dominant[0]) if dominant.size == 1 else None
    if target is None or not rho > 0 or not estimates.size or not np.isfinite(estimates[-1]):
        # Equal positive/negative dominant magnitudes need not yield a convergent Rayleigh quotient.
        return dict(target=target, rho=rho, relative=np.full(estimates.shape, np.nan), available=False)
    return dict(target=target, rho=rho, relative=np.abs(estimates - target) / abs(target), available=True)


def curvature_verdict(initial, final):
    if initial["negative"] is None or final["negative"] is None:
        return "Relative negative-curvature counts are unavailable for an empty spectrum."
    a, b = initial["negative"], final["negative"]
    if b < a:
        return f"The count below the stated negative cutoff decreases from {a} to {b} between the first and final checkpoints."
    if b > a:
        return f"The count below the stated negative cutoff increases from {a} to {b} between the first and final checkpoints."
    return f"The count below the stated negative cutoff is {a} at both endpoints; intermediate checkpoints may differ."


def radius_verdict(initial, final):
    a, b = initial["rho"], final["rho"]
    if not (math.isfinite(a) and math.isfinite(b)):
        return "A finite absolute spectral-radius comparison is unavailable."
    if b < a:
        return f"The absolute spectral radius decreases from {a:.3g} to {b:.3g}."
    if b > a:
        return f"The absolute spectral radius increases from {a:.3g} to {b:.3g}."
    return f"The absolute spectral radius is {a:.3g} at both endpoints."


class HVP(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.checks()
        self.replay()

    def card(self):
        card = chapter_card(13, r"Hessian-vector products", r"Can we use curvature without the Hessian?", part=PART)
        with self.voiceover("Chapter thirteen. Curvature without the Hessian."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"H v", r"=", r"\lim_{t \to 0} \frac{\nabla f(\theta + t v) - \nabla f(\theta)}{t}", font_size=38,
                  colors={r"H v": HESS}),
            cmath(r"H v", r"=", r"\nabla_\theta \big(\nabla f(\theta) \cdot v\big)", font_size=40, colors={r"H v": HESS}),
            cmath(r"\text{cost}(H v)", r"\approx", r"c \times \text{cost}(\nabla f)", font_size=40),
        ]
        whys = [why(r"how the gradient changes along $v$"), why(r"$v$ is fixed: \ the gradient of one number"),
                why(r"reverse mode, run through the gradient's own computation")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.6, buff=0.65, edge=6.9)
        hist = history_card(1994, r"Barak Pearlmutter, \ \textit{Fast Exact Multiplication by the Hessian}",
                            r"$Hv$ exactly, \ for a few times the cost of a gradient, \ without forming $H$", width=8.0,
                            font_size=19, color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A Hessian with a billion rows is out of reach, but its product with one vector is not. "
            "<bookmark mark='a'/> H times v is how the gradient changes as you move along v. <bookmark mark='b'/> "
            "Since v is fixed, that's the gradient of a single number, the gradient dotted with v. "
            "<bookmark mark='c'/> And a gradient of one number is what reverse mode does cheaply: run it once more, "
            "through the computation of the gradient itself, and you get H v exactly, for a small multiple of the "
            "cost of a gradient. Barak Pearlmutter published the trick in 1994."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=HESS, scale_factor=1.04))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        d = load("hessian")
        hs, fe = np.asarray(d["hs"]), np.asarray(d["fd_err"])
        g1 = log_axes((-10, -1), (-10, 0), x_length=5.4, y_length=3.6, xlabel=r"step $h$",
                      ylabel=r"finite differences of gradients: error", center=[-3.6, -0.5, 0], ystep=2, xstep=3)
        displayed_fd, fd_limits = displayed_logs(fe, -10, 0)
        c1 = curve(g1.ax, np.log10(hs), displayed_fd, GRAD, 3)
        eligible = np.isfinite(fe) & (fe >= 0) & np.isfinite(hs) & (hs >= 1e-10) & (hs <= 0.1)
        best = VGroup()
        if eligible.any():
            ii = np.flatnonzero(eligible)
            i = int(ii[np.argmin(fe[eligible])])
            best.add(Dot(g1.ax.c2p(math.log10(hs[i]), displayed_fd[i]), radius=0.07, color=GRAD))
        lam = np.asarray(d["lam_est"])
        final_eigenvalues = np.asarray(d[f"eig{len(d['keep']) - 1}"])
        power = power_comparison(lam, final_eigenvalues)
        K_ = min(40, len(lam))
        plotted_power, power_limits = displayed_logs(power["relative"][:K_], -16, 0)
        g2 = log_axes((0, max(K_ - 1, 1)), (-16, 0), x_length=4.6, y_length=3.2,
                      xlabel=r"power product index (starts at $0$)",
                      ylabel=r"relative error vs. signed dominant-magnitude eigenvalue", xticks=[], ystep=4,
                      font_size=17, center=[3.6, -0.7, 0])
        for k_ in sorted({0, (K_ - 1) // 2, max(K_ - 1, 1)}):
            g2.add(MathTex(str(k_), font_size=18, color=GREY_B).next_to(g2.ax.c2p(k_, -16), DOWN, buff=0.1))
        c2 = VGroup(curve(g2.ax, np.arange(K_), plotted_power, HESS, 3),
                    *[Dot(g2.ax.c2p(i, float(v)), radius=0.035, color=HESS)
                      for i, v in enumerate(plotted_power) if math.isfinite(v)])
        ratio = d["t_hvp"] / d["t_grad"]
        info = VGroup(
            label(rf"a ${d['sizes'][0]}$--${d['sizes'][1]}$--${d['sizes'][2]}$--${d['sizes'][3]}$ network; "
                  rf"${d['P']}$ parameters (computed)", font_size=22, color=GREY_A),
            label(rf"max product discrepancy vs. full Hessian: ${sci(d['hv_full_diff'], 1)}$",
                  font_size=22, color=HESS),
            label(rf"this benchmark: ${ratio:.1f}$ gradient evaluations' time", font_size=22, color=HESS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.35)
        fdl = label(rf"best recorded error: ${sci(d['fd_best'], 1)}$", font_size=20, color=GRAD)
        fdl.next_to(g1, DOWN, buff=0.1).align_to(g1, LEFT)
        if power["available"]:
            last = float(power["relative"][-1])
            pwl = label(rf"signed target ${power['target']:.3g}$; final relative error ${sci(last, 1)}$",
                        font_size=19, color=HESS)
            power_v = f"For this stored spectrum the signed dominant-magnitude target is {power['target']:.3g}; the final relative error is {last:.2e}."
        else:
            pwl = label(r"no finite final dominant-target comparison; curve omitted", font_size=19, color=GREY_A)
            power_v = "A finite final comparison with a unique signed nonzero dominant-magnitude target is unavailable, so that convergence comparison is omitted."
        pwl.next_to(g2, DOWN, buff=0.1).align_to(g2, LEFT)
        if pwl.width > 5.2:
            pwl.scale_to_fit_width(5.2)
        limits = note(r"finite-difference display: $10^{-10}$ floor, $1$ ceiling; power: $10^{-16}$ floor, $1$ ceiling\\"
                      rf"floor counts incl. zero: ${fd_limits['floor']}$ / ${power_limits['floor']}$; ceiling: "
                      rf"${fd_limits['ceiling']}$ / ${power_limits['ceiling']}$; invalid omitted: "
                      rf"${fd_limits['omitted']}$ / ${power_limits['omitted']}$", font_size=15).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Check it on the stored final parameters of a small network. <bookmark mark='a'/> Against the full "
            f"Hessian, the maximum product discrepancy is {d['hv_full_diff']:.2e}. In this benchmark a product takes "
            f"{ratio:.1f} times a gradient's time. <bookmark mark='b'/> The best recorded finite-difference relative "
            f"error is {d['fd_best']:.2e}. <bookmark mark='c'/> Repeated products and normalization are power iteration. "
            "With a strictly dominant eigenvalue magnitude and a nonzero initial projection on its eigenspace, "
            "they approach that eigenspace. The eigenvalue may be negative: largest magnitude is not largest "
            f"algebraic value. {power_v} Display floors and ceilings are stated below the plots."
        ) as vo:
            self.play(FadeIn(info[0]), FadeIn(g1), FadeIn(g2), FadeIn(limits))
            vo.wait_until("a")
            self.play(FadeIn(info[1]), FadeIn(info[2]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(best), FadeIn(fdl), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(pwl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("hessian")
        keep = [int(k) for k in d["keep"]]
        K = len(keep)
        X, y = np.asarray(d["X"]), np.asarray(d["y"])
        side = len(np.asarray(d["grid_xs"]))
        W = 3.4
        cen = np.array([-4.7, 0.55, 0])
        imgs = [region_image(d[f"region{k}"], side, W).move_to(cen) for k in range(K)]
        frame = SurroundingRectangle(imgs[0], buff=0, color=GREY_D, stroke_width=1.5)
        lo, hi = float(np.asarray(d["grid_xs"])[0]), float(np.asarray(d["grid_xs"])[-1])

        def to_xy(p):
            return cen + np.array([(p[0] - lo) / (hi - lo) - 0.5, (p[1] - lo) / (hi - lo) - 0.5, 0]) * W

        pts = VGroup(*[Dot(to_xy(p), radius=0.03, color=CLASS_COL[int(c)]) for p, c in zip(X, y)]).set_z_index(3)
        # the loss curve
        cv = np.asarray(d["curve"])
        g1 = log_axes((0, math.log10(d["steps"] + 1)), (-5, 1), x_length=3.4, y_length=1.25, xlabel=r"step $+1$",
                      ylabel=r"loss", center=[-4.5, -2.55, 0], ystep=3, font_size=16)
        a1 = g1.ax
        okc = cv[:, 0] >= 0
        loss_display, loss_limits = displayed_logs(cv[okc, 1], -5, 1)
        lc = curve(a1, np.log10(cv[okc, 0] + 1), loss_display, C.LOSS, 2.5)
        thresholds = d["spectrum_thresholds"]
        assert thresholds["scale"] == "spectral_radius"
        states = [spectrum_state(d[f"eig{k}"], thresholds) for k in range(K)]
        # Per-checkpoint absolute spectral radius keeps every finite normalized eigenvalue in [-1, 1].
        P = int(d["P"])
        g2 = axes([0, P, 100], [-1.05, 1.05, 0.5], x_length=6.2, y_length=3.6, xlabel=r"eigenvalues, \ smallest to largest",
                  ylabel=r"$\lambda/\rho(H)$; $\rho(H)=\max|\lambda|$ (signed log)", xticks=[], yticks=[-1, 0, 1],
                  yfmt=lambda v: {-1: "-1", 0: "0", 1: "1"}[int(v)], font_size=18, center=[2.9, -0.95, 0])
        a2 = g2.ax
        for v in (-0.1, -0.01, 0.01, 0.1):
            yv = float(symlog(v))
            g2.add(MathTex(f"{v:g}", font_size=14, color=GREY_C).next_to(a2.c2p(0, yv), LEFT, buff=0.08))

        def spectrum(k):
            values = np.sort(states[k]["normalized"])
            return VGroup(*[Dot(a2.c2p(i, float(symlog(v))), radius=0.022,
                                color=(HESS if v > thresholds["outlier_relative"] else
                                       (C.SURPRISE if v < -thresholds["negative_relative"] else GREY_B)))
                            for i, v in enumerate(values)])

        def readout(k):
            state = states[k]
            if state["negative"] is None:
                detail = r"no finite eigenvalues: relative cutoff counts unavailable"
            elif state["rho"] == 0:
                detail = r"$\rho(H)=0$: all finite eigenvalues are zero"
            else:
                detail = (rf"$\rho(H)={state['rho']:.3g}$; high-positive ${state['high_positive']}$; "
                          rf"negative ${state['negative']}$; near-zero ${100 * state['flat']:.0f}\%$")
            block = VGroup(
                label(rf"step ${keep[k]:,}$".replace(",", "{,}") + rf": loss ${d[f'loss{k}']:.4f}$; training accuracy "
                      rf"${100 * d[f'acc{k}']:.0f}\%$", font_size=22, color=WHITE),
                label(detail, font_size=20, color=GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([2.9, 2.6, 0])
            if block.width > 6.5:
                block.scale_to_fit_width(6.5)
            return block

        dots = [spectrum(k) for k in range(K)]
        reads = [readout(k) for k in range(K)]
        marker = Dot(radius=0.06, color=WHITE)

        def mpos(k):
            t = keep[k] + 1
            value, _ = displayed_logs([d[f"loss{k}"]], -5, 1)
            return a1.c2p(math.log10(t), float(value[0]) if math.isfinite(value[0]) else -5)

        def marker_opacity(k):
            value = float(d[f"loss{k}"])
            return float(math.isfinite(value) and value >= 0)

        marker.move_to(mpos(0)).set_opacity(marker_opacity(0))
        title = label(rf"three spirals, \ a ${P}$-parameter network, \ trained with Adam: \ its full Hessian at "
                      rf"${K}$ checkpoints", font_size=22, color=GREY_A).to_edge(UP, buff=0.2)
        cutoff_note = label(
            rf"relative cutoffs: negative $\lambda<-{thresholds['negative_relative']:g}\rho$; "
            rf"near-zero $|\lambda|\leq {thresholds['flat_relative']:g}\rho$\\"
            rf"high-positive $\lambda>{thresholds['outlier_relative']:g}\rho$; zero radius: all finite eigenvalues zero",
            font_size=17, color=GREY_A).move_to([2.9, 1.85, 0])
        if cutoff_note.width > 6.5:
            cutoff_note.scale_to_fit_width(6.5)
        tag = note(rf"computed; training cohort ${len(y)}$; omitted eigenvalues: "
                   rf"${sum(state['omitted'] for state in states)}$\\loss display: $10^{{-5}}$ floor incl. zero "
                   rf"({loss_limits['floor']}); $10$ ceiling ({loss_limits['ceiling']}); invalid omitted ({loss_limits['omitted']})",
                   font_size=14).to_corner(DR, buff=0.15)
        initial, final = states[0], states[-1]
        mixed = np.any(initial["eigenvalues"] < 0) and np.any(initial["eigenvalues"] > 0)
        initial_v = ("The initial Hessian has both positive and negative curvature directions. That alone does not "
                     "establish a stationary saddle point." if mixed else
                     "The stored initial spectrum does not have both positive and negative eigenvalues.")
        neg_v = curvature_verdict(initial, final)
        radius_v = radius_verdict(initial, final)
        final_v = (f"At the final checkpoint, {final['high_positive']} eigenvalues exceed the chosen positive cutoff, "
                   f"and {100 * final['flat']:.0f} percent lie inside the stated relative near-zero cutoff."
                   if final["negative"] is not None else
                   "At the final checkpoint the relative cutoff counts are undefined.")
        with self.voiceover(
            "Now watch a landscape change as a network learns three interleaved spirals. This network has "
            f"{P} parameters, with its full Hessian computed at {K} stored checkpoints. Accuracy is on the "
            f"{len(y)} training examples. <bookmark mark='a'/> {initial_v} <bookmark mark='b'/> "
            "The signed-log plot divides each spectrum by its own absolute spectral radius, so its shape and "
            f"absolute size must be read separately. {neg_v} <bookmark mark='c'/> Final counts: {final_v} "
            f"Absolute scale: {radius_v} "
            "The cutoffs are stated relative to each checkpoint's spectral radius. High-positive is a selected "
            "cutoff, not a fitted statistical outlier test. Sagun and colleagues studied concentration of neural "
            "network Hessian spectra in 2016; this small training example reports its own measured outcome."
        ) as vo:
            self.play(FadeIn(title), FadeIn(imgs[0]), FadeIn(frame), FadeIn(pts), FadeIn(g1), Create(lc), FadeIn(marker),
                      FadeIn(g2), FadeIn(dots[0]), FadeIn(reads[0]), FadeIn(cutoff_note), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(dots[0], color=C.SURPRISE, scale_factor=1.0))
            vo.wait_until("b")
            for k in range(1, K):
                rt = 1.0
                self.play(FadeOut(imgs[k - 1]), FadeIn(imgs[k]), Transform(dots[0], dots[k]),
                          FadeOut(reads[k - 1]), FadeIn(reads[k]),
                          marker.animate.move_to(mpos(k)).set_opacity(marker_opacity(k)), run_time=rt)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()
