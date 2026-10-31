from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, MONO, PART, load, matrix_heat

LETTERS = " abcdefghijklmnopqrstuvwxyz"


def row_log_probabilities(scores):
    """Normalize each row stably; adding a row constant cannot change the picture."""
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 2 or not np.isfinite(scores).all():
        raise ValueError("score snapshots must be a finite matrix")
    shifted = scores - scores.max(axis=1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))


def recorded_curve_prefix(values, count):
    """A one-point trace repeats its own point instead of revealing a future sample."""
    values = np.asarray(values, dtype=float)
    shown = values[:max(0, int(count))]
    return np.repeat(shown, 2, axis=0) if len(shown) == 1 else shown


def training_readout(d):
    """Keep finite-run performance and the explicitly masked correlation observable."""
    train, valid, target = (float(d[k]) for k in ("bits_train", "bits_valid", "H_cond"))
    if not np.isfinite([train, valid, target]).all():
        raise ValueError("training loss summaries must be finite")
    gap = train - target
    correlation = d["metrics"]["correlation"]
    corr = float(d["corr"]) if d["corr"] is not None else math.nan
    if abs(gap) < 0.02:
        loss_verdict = (f"After {d['steps']} Adam updates, the full-training loss is {train:.3f} bits per letter, "
                        f"within 0.02 bits of the counting reference {target:.3f}. This is a finite-run result.")
    else:
        loss_verdict = (f"After {d['steps']} Adam updates, the full-training loss is {train:.3f} bits per letter; "
                        f"its difference from the counting reference is {gap:+.3f} bits. This finite run has not "
                        "matched the reference within 0.02 bits.")
    if math.isfinite(corr):
        correlation_verdict = (f"On {correlation['count']} letter pairs whose counted conditional probability "
                               f"exceeds {correlation['threshold']:g}, the normalized log probabilities have "
                               f"Pearson correlation {corr:.3f} with the counted log probabilities.")
        corr_tex = f"{corr:.3f}"
    else:
        correlation_verdict = (f"For the recorded mask of {correlation['count']} letter pairs, Pearson correlation "
                               "is undefined; no correlation value is inferred.")
        corr_tex = r"\text{undefined}"
    return dict(gap=gap, corr_tex=corr_tex, loss_verdict=loss_verdict,
                correlation_verdict=correlation_verdict, correlation=correlation)


def score_grid(Z, size=3.9, lo=-8.0, hi=0.0, center=ORIGIN, color=C.MODEL_Q) -> VGroup:
    """Normalized log probabilities; the explicit display scale saturates below lo."""
    c = size / 27
    dark, lit = ManimColor("#121826"), ManimColor(color)
    g = VGroup()
    for i in range(27):
        for j in range(27):
            v = float(np.clip((Z[i, j] - lo) / (hi - lo), 0, 1)) ** 1.2
            g.add(Square(side_length=c, stroke_width=0, fill_color=interpolate_color(dark, lit, v), fill_opacity=1)
                  .move_to(np.asarray(center) + np.array([-size / 2 + (j + 0.5) * c, size / 2 - (i + 0.5) * c, 0])))
    return g


class Train(VoiceoverScene):
    def construct(self):
        self.card()
        self.first()
        self.descent()
        self.steps()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Training with our library", r"Can descent find what counting found?", part=PART)
        with self.voiceover("Chapter eight. Training with our library."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def first(self):
        d = load("grad0")
        G = np.asarray(d["grad"])
        assert d["diff"] < 1e-12
        col = {r"q_{j\mid i}": C.MODEL_Q, r"\hat p_{j \mid i}": C.TRUE_P}
        rows = [
            cmath(r"\frac{\partial \mathcal L}{\partial z_{ij}}", r"=",
                  r"\frac1N \sum_{t:\, c_t = i} \big(q_{j \mid i} - [c_{t+1} = j]\big)", font_size=34),
            cmath(r"\frac{\partial \mathcal L}{\partial z_{ij}}", r"=", r"\frac{n_i}{N}\,\big(", r"q_{j\mid i}", r"-",
                  r"\hat p_{j \mid i}", r"\big)", font_size=34, colors=col),
            cmath(r"\frac{\partial \mathcal L}{\partial z_{ij}}\Big|_{z = 0}", r"=",
                  r"\frac{n_i}{N}\,\big(\tfrac{1}{27} - \hat p_{j \mid i}\big)", font_size=34),
        ]
        whys = [why(r"natural-log cross-entropy (nats): \\ each pair's guess minus its truth", font_size=21),
                why(r"$n_i$ pairs start with $i$; \\ $\hat p$: Part 1's counts", font_size=21),
                why(r"all scores equal: \ $q = 1/27$", font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.4, x=-3.9, buff=0.35, edge=6.9)
        heat = matrix_heat(G, cell=0.1, pos=C.TRUE_P, neg=C.SURPRISE).move_to([-4.9, -2.35, 0])
        LET = " abcdefghijklmnopqrstuvwxyz"
        pairs = VGroup(label(r"pushed up hardest:", font_size=22, color=C.SURPRISE),
                       *[data_text(f"'{LET[i]}' then '{LET[j]}'".replace("' '", "space"), font=MONO, font_size=18,
                                   color=WHITE) for i, j in d["top"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        pairs.next_to(heat, RIGHT, buff=0.4).align_to(heat, UP)
        hcap = label(r"the first gradient, \ $27 \times 27$: \ red pushes a score up", font_size=20, color=GREY_B)
        hcap.next_to(heat, UP, buff=0.1).align_to(heat, LEFT)
        chk = label(rf"computed on ${d['pairs']:,}$ pairs: \ library against formula, \ ${sci(d['diff'], 0)}$".replace(",", "{,}"),
                    font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3).shift(RIGHT * 2.2)
        with self.voiceover(
            "Before we train, look at the first gradient. Differentiate the average natural-log surprise, in nats, with respect to one "
            "score, z i j: every pair of letters that starts with i adds its guess minus its truth. "
            "<bookmark mark='a'/> Collected, that's the share of pairs starting with i, times Part 1's q minus p hat: "
            "the model's probabilities minus the counted ones. <bookmark mark='b'/> At the start every guess is one "
            "twenty-seventh. <bookmark mark='c'/> Computed on the books, the library's gradient matches the formula, "
            "and the biggest pushes, in red, go to the commonest pairs. Gradient descent is counting, done a little "
            "at a time. The plots report bits by dividing the natural-log loss by log two."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(heat), FadeIn(hcap), FadeIn(pairs), FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descent(self):
        d = load("train")
        measured = training_readout(d)
        curve = np.asarray(d["curve"], dtype=float)
        snaps = np.asarray(d["snaps"], dtype=float)
        snap_steps = [int(v) for v in d["snap_steps"]]
        if len(snaps) != len(snap_steps) or not np.isfinite(curve).all():
            raise ValueError("training snapshots/curve do not match their recorded contract")
        # The initial state is explicit; saved snapshots are after each labeled update.
        scores = [np.zeros((27, 27)), *snaps]
        shown_steps = [0, *snap_steps]
        cg = [-4.2, 0.2, 0]
        grids = [score_grid(row_log_probabilities(s), center=cg) for s in scores]
        gl = label(r"model: \ $\log q(j\mid i)$", font_size=25, color=C.MODEL_Q)
        gl.next_to(grids[0], UP, buff=0.42)
        raw = label(r"$729$ learned raw scores $z$; \ then log-softmax", font_size=18, color=GREY_A)
        raw.next_to(gl, UP, buff=0.1)
        row_letters = VGroup(*[data_text(LETTERS[i] if i else "␣", font=MONO, font_size=11, color=GREY_B)
                              .next_to(grids[0][27 * i], LEFT, buff=0.05) for i in range(27)])
        col_letters = VGroup(*[data_text(LETTERS[j] if j else "␣", font=MONO, font_size=11, color=GREY_B)
                              .next_to(grids[0][j], UP, buff=0.05) for j in range(27)])
        orientation = label(r"rows: previous $i$; \ columns: next $j$", font_size=17, color=GREY_B)
        orientation.next_to(raw, UP, buff=0.1)
        scale = VGroup(*[Square(side_length=0.18, stroke_width=0,
                               fill_color=interpolate_color(ManimColor("#121826"), ManimColor(C.MODEL_Q), (k / 8) ** 1.2),
                               fill_opacity=1) for k in range(9)]).arrange(RIGHT, buff=0)
        scale.next_to(grids[0], DOWN, buff=0.12)
        model_scale = scale.copy()
        count_scale = scale.copy()
        for k, square in enumerate(count_scale):
            square.set_fill(interpolate_color(ManimColor("#121826"), ManimColor(C.COUNTING), (k / 8) ** 1.2))
        model_raw = raw.copy()
        scale_text = label(r"natural log: \ $\le -8$ (dark) \ to $0$ (bright)", font_size=17, color=GREY_A)
        scale_text.next_to(scale, DOWN, buff=0.06)
        yrange = np.r_[curve[:, 1], d["H_cond"], d["bits_train"], d["bits_valid"]]
        ylo = math.floor(2 * (float(yrange.min()) - 0.15)) / 2
        yhi = math.ceil(2 * (float(yrange.max()) + 0.15)) / 2
        yticks = sorted({ylo, 0.5 * round(ylo + yhi), yhi})
        ax = Axes(x_range=[0, int(d["steps"]), 500], y_range=[ylo, yhi, 0.5], x_length=5.6, y_length=3.6,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
        ax.move_to([2.6, 0.4, 0])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in yticks])
        xl = label(r"Adam update number", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        bl = VGroup(label(r"bits per letter", font_size=22, color=GREY_A),
                    label(r"sampled minibatch loss, before update", font_size=17, color=GREY_B))
        bl.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        floor = DashedLine(ax.c2p(0, d["H_cond"]), ax.c2p(d["steps"], d["H_cond"]), color=C.COUNTING, stroke_width=2)
        fl = label(rf"counting reference: \ ${d['H_cond']:.3f}$", font_size=21, color=C.COUNTING)
        fl.next_to(floor, UP, buff=0.08).align_to(floor, RIGHT)
        t = ValueTracker(0)

        def trace():
            recorded = recorded_curve_prefix(curve, t.get_value())
            if not len(recorded):
                return VMobject()
            return ax.plot_line_graph(recorded[:, 0], recorded[:, 1], add_vertex_dots=False,
                                      line_color=GRAD, stroke_width=3)

        line = always_redraw(trace)
        start = label(r"initial $z = 0$: \ $\log_2 27 = 4.75$", font_size=23, color=GREY_A)
        start.move_to([2.6, 3.3, 0])
        end = label(rf"full train: ${d['bits_train']:.3f}$; \ new text: ${d['bits_valid']:.3f}$ bits", font_size=24,
                    color=GRAD).move_to([2.6, -2.15, 0])
        count_grid = score_grid(d["logcond"], center=cg, color=C.COUNTING)
        count_title = label(r"counted: \ $\log \hat p(j\mid i)$", font_size=25, color=C.COUNTING).move_to(gl)
        count_raw = label(r"counted conditionals; \ zero entries floored at $10^{-9}$", font_size=18, color=GREY_A)
        count_raw.move_to(raw)
        corr_info = measured["correlation"]
        corr = label(rf"normalized logs: \ Pearson $r = {measured['corr_tex']}$ \\ "
                     rf"${corr_info['count']}$ pairs with $\hat p(j\mid i) > {sci(corr_info['threshold'], 0)}$",
                     font_size=22, color=WHITE).to_edge(DOWN, buff=0.15)
        dice = np.random.default_rng(1500).random(52)

        def writes(z):
            probabilities = np.exp(row_log_probabilities(z))
            cdf = np.cumsum(probabilities, axis=1)
            i, output = 0, ""
            for u in dice:
                i = int(min(np.searchsorted(cdf[i], u), 26))
                output += LETTERS[i]
            return output

        def write_row(k):
            heading = label(rf"after update ${shown_steps[k]:,}$:".replace(",", "{,}"), font_size=22, color=GRAD)
            text = data_text(writes(scores[k]), font=MONO, font_size=21, color=WHITE)
            return VGroup(heading, text).arrange(RIGHT, buff=0.3).move_to([0, -2.85, 0])

        rows_w = [write_row(k) for k in range(len(scores))]
        for row in rows_w:
            if row.width > 13.2:
                row.scale_to_fit_width(13.2)
        loss_verdict = measured["loss_verdict"]
        correlation_verdict = measured["correlation_verdict"]
        with self.voiceover(
            f"Now let's train. Counting gives a reference of {d['H_cond']:.3f} bits per letter. "
            "<bookmark mark='a'/> The training loop instead samples letter pairs from the books. It learns 729 raw "
            "scores, initially zero, with Adam. The picture shows their row-normalized natural log probabilities, "
            "not the raw scores. Its scale is shared with the counted comparison: values below minus eight are "
            "equally dark. <bookmark mark='w'/> Underneath, samples use the same random dice at every checkpoint. "
            "Heatmaps are after the labeled update; the curve records minibatch loss just before that update. "
            "The final train and new-text numbers use the full respective corpora."
        ) as vo:
            self.play(FadeIn(grids[0]), FadeIn(gl), FadeIn(raw), FadeIn(row_letters), FadeIn(col_letters),
                      FadeIn(orientation), FadeIn(scale), FadeIn(scale_text))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(bl), Create(floor), FadeIn(fl), FadeIn(start))
            vo.wait_until("w")
            self.play(FadeIn(rows_w[0]))
        marks = [int(np.searchsorted(curve[:, 0], step, side="right")) for step in snap_steps]
        with self.voiceover(
            f"{loss_verdict} <bookmark mark='a'/> {correlation_verdict} Raw scores can shift by a different "
            "constant in each row without changing probabilities, so the comparison uses normalized logs. "
            "Maximum likelihood connects the counting solution to the optimization objective; a finite run "
            "need not reach it. <bookmark mark='b'/> The same optimization loop, with richer models, trains the "
            "later systems in this series."
        ) as vo:
            self.add(line)
            shown = rows_w[0]
            for k, mark in enumerate(marks):
                run_time = 1.2 if k < len(marks) - 1 else 2.0
                self.play(t.animate(rate_func=linear).set_value(mark),
                          Transform(grids[0], grids[k + 1], rate_func=linear),
                          FadeOut(shown, rate_func=squish_rate_func(smooth, 0.0, 0.35)),
                          FadeIn(rows_w[k + 1], rate_func=squish_rate_func(smooth, 0.4, 0.75)), run_time=run_time)
                shown = rows_w[k + 1]
            self.play(FadeIn(end))
            vo.wait_until("a")
            self.play(FadeIn(corr))
            self.play(Transform(grids[0], count_grid), Transform(gl, count_title), Transform(scale, count_scale),
                      Transform(raw, count_raw), run_time=1.0)
            self.play(Transform(grids[0], score_grid(d["logp"], center=cg)),
                      Transform(gl, label(r"model: \ $\log q(j\mid i)$", font_size=25, color=C.MODEL_Q).move_to(gl)),
                      Transform(scale, model_scale), Transform(raw, model_raw),
                      run_time=1.0)
            vo.wait_until("b")
        line.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        d = load("gdlr")
        etas = [float(e) for e in d["etas"]]
        K = len(etas)
        cols = [GREY_B, C.TRUE_P, C.REWARD, GRAD, C.SURPRISE]
        S = int(d["steps"])
        g1 = axes([0, math.log10(S + 1), 1], [3.2, 5.0, 0.5], x_length=5.6, y_length=3.6,
                  xlabel=r"$1 +$ updates \ (log scale)",
                  ylabel=r"bits per letter", xticks=[0, 1, 2, 3], xfmt=lambda v: {0: "1", 1: "10", 2: "100", 3: "1000"}[int(v)],
                  yticks=[3.5, 4.0, 4.5], center=[-3.3, -0.6, 0])
        g2 = axes([0, S, 1000], [0, 0.08, 0.02], x_length=5.0, y_length=3.6, xlabel=r"step",
                  ylabel=r"largest curvature $\lambda_{\max}$ \ (nats objective)",
                  xticks=[0, 1000, 2000, 3000], yticks=[0, 0.04, 0.08],
                  center=[3.6, -0.6, 0])
        c1, c2, lines = VGroup(), VGroup(), VGroup()
        loss_clipped, curvature_clipped, thresholds_omitted = 0, 0, 0
        for k in range(K):
            b = np.asarray(d[f"bitcurve{k}"])
            t = np.arange(len(b)) * 10 + 1
            loss_clipped += int(((b < 3.2) | (b > 5.0)).sum())
            c1.add(curve(g1.ax, np.log10(t), np.clip(b, 3.2, 5.0), cols[k], 2.5))
            lm = np.asarray(d[f"lamcurve{k}"])
            curvature_clipped += int(((lm < 0) | (lm > 0.08)).sum())
            c2.add(curve(g2.ax, np.arange(len(lm)) * 25, np.clip(lm, 0, 0.08), cols[k], 1.6).set_stroke(opacity=0.55 if k == K - 1 else 1.0))
            if 2 / etas[k] < 0.08:
                lines.add(DashedLine(g2.ax.c2p(0, 2 / etas[k]), g2.ax.c2p(S, 2 / etas[k]), color=cols[k], stroke_width=1.5))
            else:
                thresholds_omitted += 1
        leg = VGroup(*[label(rf"$\eta = {e:.0f}$" if e >= 10 else rf"$\eta = {e:.1f}$", font_size=20, color=c)
                       for e, c in zip(etas, cols)]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        floor = DashedLine(g1.ax.c2p(0, d["H_cond"]), g1.ax.c2p(math.log10(S + 1), d["H_cond"]), color=C.COUNTING,
                           stroke_width=1.5)
        dl = label(r"dashed: \ $2/\eta$ for each step size", font_size=20, color=GREY_B).next_to(g2, DOWN, buff=0.05)
        tag = note(rf"full-batch count objective; \ clipped display samples: loss ${loss_clipped}$, curvature "
                   rf"${curvature_clipped}$; \ ${thresholds_omitted}$ out-of-window threshold lines omitted",
                   font_size=17).to_edge(DOWN, buff=0.15)
        m, sp, mono = d["last_mean"], d["last_spread"], d["monotone"]
        settled = [sp[k] < 1e-3 for k in range(K)]
        e2, e3 = etas[2], etas[3]
        if settled[2] and not settled[3]:
            verdict = (f"Over the final {d['metrics']['final_tail_states']} recorded states, step {e2:.0f} has mean loss "
                       f"{m[2]:.3f} bits and range {sp[2]:.4f}; step {e3:.0f} has mean {m[3]:.3f} and range "
                       f"{sp[3]:.4f}. Only the first is within our 0.001-bit late-window variation criterion. "
                       "That describes this finite window, not convergence for all future updates.")
        else:
            verdict = (f"Over the final {d['metrics']['final_tail_states']} recorded states, steps {e2:.0f} and "
                       f"{e3:.0f} have mean losses {m[2]:.3f} and {m[3]:.3f} bits, with ranges {sp[2]:.4f} and "
                       f"{sp[3]:.4f}. The displayed local stability scale is not a universal convergence test.")
        with self.voiceover(
            "How large a step can plain full-batch gradient descent take here? Chapter fourteen will derive the "
            "local quadratic stability scale, two over the largest curvature. It is not a global guarantee as "
            "curvature changes. <bookmark mark='a'/> At the start, every score zero, the Hessian's largest "
            f"eigenvalue is {d['lam0']:.4f}, which would allow steps up to {d['eta0']:.0f}. <bookmark mark='b'/> But "
            f"the counting solution has curvature {d['lam_star']:.3f}, giving a local scale of "
            f"{d['eta_star']:.0f}. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(floor), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c2[0]), Create(c1[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines), FadeIn(dl), Create(c2[1]), Create(c1[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Create(c1[k]) for k in range(2, K)], *[Create(c2[k]) for k in range(2, K)], run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
