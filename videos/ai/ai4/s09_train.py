from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, MONO, PART, load, matrix_heat

LETTERS = " abcdefghijklmnopqrstuvwxyz"


def score_grid(Z, size=3.9, lo=-8.0, hi=0.0, center=ORIGIN) -> VGroup:
    """27 x 27 scores as cells: bright where the score (a log probability) is high."""
    c = size / 27
    dark, lit = ManimColor("#121826"), ManimColor(GRAD)
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
        whys = [why(r"each pair that starts with $i$: \\ its guess minus its truth (Part 1)", font_size=21),
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
            "Before we train, look at the first gradient. Differentiate the average surprise with respect to one "
            "score, z i j: every pair of letters that starts with i adds its guess minus its truth. "
            "<bookmark mark='a'/> Collected, that's the share of pairs starting with i, times Part 1's q minus p hat: "
            "the model's probabilities minus the counted ones. <bookmark mark='b'/> At the start every guess is one "
            "twenty-seventh. <bookmark mark='c'/> Computed on the books, the library's gradient matches the formula, "
            "and the biggest pushes, in red, go to the commonest pairs. Gradient descent is counting, done a little "
            "at a time."
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
        assert abs(d["bits_train"] - d["H_cond"]) < 0.02 and d["corr"] > 0.99
        curve = np.asarray(d["curve"])
        snaps = np.asarray(d["snaps"])
        logp_final = np.asarray(d["logp"])
        logc = np.asarray(d["logcond"])

        def logsoft(z):
            return z - np.log(np.exp(z).sum(1, keepdims=True))

        cg = [-4.2, 0.2, 0]
        grids = [score_grid(logsoft(s), center=cg) for s in snaps]
        gl = label(r"$729$ scores $z_{ij}$: \ next letter $j$ after letter $i$", font_size=24, color=GREY_A)
        gl.next_to(grids[0], UP, buff=0.2)
        rows = VGroup(*[Text(LETTERS[i] if i else "␣", font=MONO, font_size=11, color=GREY_B)
                        .next_to(grids[0][27 * i], LEFT, buff=0.05) for i in range(27)])
        ax = Axes(x_range=[0, int(d["steps"]), 500], y_range=[3.0, 5.0, 0.5], x_length=5.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([2.6, 0.4, 0])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (3.0, 4.0, 5.0)])
        xl = label(r"steps of gradient descent", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        bl = label(r"bits per letter", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        floor = DashedLine(ax.c2p(0, d["H_cond"]), ax.c2p(d["steps"], d["H_cond"]), color=C.COUNTING, stroke_width=2)
        fl = label(rf"Part 1, by counting: \ ${d['H_cond']:.2f}$", font_size=24, color=C.COUNTING).next_to(floor, UP, buff=0.08)
        fl.align_to(floor, RIGHT)
        t = ValueTracker(0)
        line = always_redraw(lambda: ax.plot_line_graph(curve[:max(2, int(t.get_value())), 0],
                                                        np.clip(curve[:max(2, int(t.get_value())), 1], 3.0, 5.0),
                                                        add_vertex_dots=False, line_color=GRAD, stroke_width=3))
        start = label(r"all $27$ letters equal: \ $\log_2 27 = 4.75$", font_size=24, color=GREY_A).move_to([3.3, 2.65, 0])
        end = label(rf"descent: \ ${d['bits_train']:.2f}$ \ \ (new text: ${d['bits_valid']:.2f}$)", font_size=26,
                    color=GRAD).move_to([2.6, -2.15, 0])
        cnt = score_grid(logc, center=[-4.2, 0.2, 0])
        corr = label(rf"the scores become the log of the counts: \ correlation ${d['corr']:.3f}$", font_size=26,
                     color=WHITE).to_edge(DOWN, buff=0.2)
        assert abs(curve[0, 1] - np.log2(27)) < 0.01
        # what the scores write: letters sampled from them, with the same dice at every checkpoint
        dice = np.random.default_rng(1500).random(52)

        def writes(z):
            p_ = np.exp(z - z.max(1, keepdims=True))
            c_ = np.cumsum(p_ / p_.sum(1, keepdims=True), 1)
            i, out = 0, ""
            for u in dice:
                i = int(min(np.searchsorted(c_[i], u), 26))
                out += LETTERS[i]
            return out

        snap_steps = (1, 50, 200, int(d["steps"]))

        def write_row(k):
            head_ = label(rf"step ${snap_steps[k]:,}$, \ it writes:".replace(",", "{,}"), font_size=24, color=GRAD)
            body_ = data_text(writes(snaps[k]), font=MONO, font_size=22, color=WHITE)
            return VGroup(head_, body_).arrange(RIGHT, buff=0.3).move_to([0, -2.8, 0])

        rows_w = [write_row(k) for k in range(len(snaps))]
        for r_ in rows_w:
            if r_.width > 13.2:
                r_.scale_to_fit_width(13.2)
        with self.voiceover(
            "Now let's use it. In part one, counting letter pairs got us to 3.33 bits per letter. <bookmark mark='a'/> "
            "This time, nothing is counted. The model has 729 adjustable scores, one for every pair of letters, all "
            "starting at zero, and our library trains them by gradient descent on the books. <bookmark mark='w'/> "
            "Underneath, the text the scores write, drawn with the same dice at every step: for now, noise."
        ) as vo:
            self.play(FadeIn(grids[0]), FadeIn(gl), FadeIn(rows))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(bl), Create(floor), FadeIn(fl), FadeIn(start))
            vo.wait_until("w")
            self.play(FadeIn(rows_w[0]))
        n = len(curve)
        marks = [int(np.searchsorted(curve[:, 0], s)) + 1 for s in (50, 200, 1500)]
        with self.voiceover(
            "The loss falls fast, then settles: at 3.33 bits, the counting answer. <bookmark mark='a'/> And the "
            "scores themselves have become the logarithms of the counts. That's maximum likelihood again, reached by "
            "walking downhill instead of by counting. <bookmark mark='b'/> The same loop, with more numbers and "
            "better models, trains everything else in this series."
        ) as vo:
            self.add(line)
            shown = rows_w[0]
            for k, m in enumerate(marks):
                rt = 1.5 if k < 2 else 2.0
                # the scores change smoothly; the text it writes cross-fades, so it is never a letter-by-letter blur
                self.play(t.animate(rate_func=linear).set_value(min(m, n)), Transform(grids[0], grids[k + 1], rate_func=linear),
                          FadeOut(shown, rate_func=squish_rate_func(smooth, 0.0, 0.35)),
                          FadeIn(rows_w[k + 1], rate_func=squish_rate_func(smooth, 0.4, 0.75)), run_time=rt)
                shown = rows_w[k + 1]
            self.play(FadeIn(end))
            vo.wait_until("a")
            self.play(FadeIn(corr))
            self.play(Transform(grids[0], cnt), run_time=1.0)
            self.play(Transform(grids[0], score_grid(logp_final, center=[-4.2, 0.2, 0])), run_time=1.0)
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
        g1 = axes([0, math.log10(S), 1], [3.2, 5.0, 0.5], x_length=5.6, y_length=3.6, xlabel=r"step",
                  ylabel=r"bits per letter", xticks=[0, 1, 2, 3], xfmt=lambda v: {0: "1", 1: "10", 2: "100", 3: "1000"}[int(v)],
                  yticks=[3.5, 4.0, 4.5], center=[-3.3, -0.6, 0])
        g2 = axes([0, S, 1000], [0, 0.08, 0.02], x_length=5.0, y_length=3.6, xlabel=r"step",
                  ylabel=r"largest curvature $\lambda_{\max}$", xticks=[0, 1000, 2000, 3000], yticks=[0, 0.04, 0.08],
                  center=[3.6, -0.6, 0])
        c1, c2, lines = VGroup(), VGroup(), VGroup()
        for k in range(K):
            b = np.asarray(d[f"bitcurve{k}"])
            t = np.arange(len(b)) * 10 + 1
            c1.add(curve(g1.ax, np.log10(t), np.clip(b, 3.2, 5.0), cols[k], 2.5))
            lm = np.asarray(d[f"lamcurve{k}"])
            c2.add(curve(g2.ax, np.arange(len(lm)) * 25, np.clip(lm, 0, 0.08), cols[k], 1.6).set_stroke(opacity=0.55 if k == K - 1 else 1.0))
            if 2 / etas[k] < 0.08:
                lines.add(DashedLine(g2.ax.c2p(0, 2 / etas[k]), g2.ax.c2p(S, 2 / etas[k]), color=cols[k], stroke_width=1.5))
        leg = VGroup(*[label(rf"$\eta = {e:.0f}$" if e >= 10 else rf"$\eta = {e:.1f}$", font_size=20, color=c)
                       for e, c in zip(etas, cols)]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        floor = DashedLine(g1.ax.c2p(0, d["H_cond"]), g1.ax.c2p(math.log10(S), d["H_cond"]), color=C.COUNTING,
                           stroke_width=1.5)
        dl = label(r"dashed: \ $2/\eta$ for each step size", font_size=20, color=GREY_B).next_to(g2, DOWN, buff=0.05)
        tag = note(r"computed: \ full-batch gradient descent from the pair counts").to_corner(DR, buff=0.2)
        m, sp, mono = d["last_mean"], d["last_spread"], d["monotone"]
        settled = [sp[k] < 1e-3 for k in range(K)]
        e2, e3 = etas[2], etas[3]
        if settled[2] and not settled[3]:
            verdict = (f"With a step of {e2:.0f}, under that limit, the loss settles at {m[2]:.3f} bits. With {e3:.0f}, "
                       "over it, it never settles: the curvature climbs to two over the step and hovers there, the edge "
                       "of stability that Part 11 takes up.")
        else:
            verdict = (f"Here the limit is not sharp: steps of {e2:.0f} and {e3:.0f} end at {m[2]:.3f} and {m[3]:.3f} "
                       "bits.")
        with self.voiceover(
            "How large a step can plain gradient descent take here? Chapter fourteen will give the rule: less than two "
            "over the largest curvature. <bookmark mark='a'/> At the start, every score zero, the Hessian's largest "
            f"eigenvalue is {d['lam0']:.4f}, which would allow steps up to {d['eta0']:.0f}. <bookmark mark='b'/> But "
            f"the curvature grows as the model learns, to {d['lam_star']:.3f} at the counting answer, and that allows "
            f"only {d['eta_star']:.0f}. <bookmark mark='c'/> " + verdict
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
