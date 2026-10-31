from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, bits_axes, lr_tex, load, panel, takeaway_card

AW, L2, AD = OPT_COLORS["adamw"], OPT_COLORS["adam_l2"], OPT_COLORS["adam"]


def heat(A, center, cell=0.68, lo=None, hi=None):
    """A grid of held-out losses: brighter is better (lower)."""
    A = np.asarray(A, float)
    lo = np.nanmin(A) if lo is None else lo
    hi = np.nanmax(A) if hi is None else hi
    g = VGroup()
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            v = A[i, j]
            t = 0.0 if not np.isfinite(v) else float(np.clip((hi - v) / max(hi - lo, 1e-9), 0, 1))
            col = interpolate_color(ManimColor("#1B2A6B"), ManimColor(C.BITS), t ** 1.5)
            sq = Square(cell, stroke_width=1, stroke_color=BACKGROUND, fill_color=col, fill_opacity=1)
            sq.move_to(np.array(center) + np.array([(j - (A.shape[1] - 1) / 2) * cell, ((A.shape[0] - 1) / 2 - i) * cell, 0]))
            txt = MathTex(f"{v:.2f}" if np.isfinite(v) else r"\times", font_size=20,
                          color=BLACK if t > 0.6 else WHITE).move_to(sq)
            g.add(VGroup(sq, txt))
    return g


class Decay(VoiceoverScene):
    def construct(self):
        self.card()
        self.sgd()
        self.adam()
        self.grids()
        self.curves()
        self.takeaway()

    def card(self):
        c = chapter_card(7, r"Weight decay is not L2", r"What does shrinking the weights do inside Adam?", part=PART)
        with self.voiceover("Chapter seven. Weight decay is not L2."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def sgd(self):
        head = label(r"two ways to keep weights small", font_size=30).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\tilde L(\theta)", "=", r"L(\theta) + \tfrac{\lambda}{2}\,\|\theta\|^2", font_size=36),
            cmath(r"\theta", r"\leftarrow", r"\theta - \eta\,\big(\nabla L + \lambda\theta\big)", font_size=36),
            cmath(r"\theta", r"\leftarrow", r"(1 - \eta\lambda)\,\theta - \eta\,\nabla L", font_size=36,
                  colors={r"(1 - \eta\lambda)\,\theta - \eta\,\nabla L": AW}),
        ]
        whys = [why(r"an L2 penalty on the loss"), why(r"gradient descent on it"), why(r"the same thing: \ \textit{decay} the weights by $\eta\lambda$")]
        step = ladder(self, rows, whys, keep=3, top=2.0, x=-1.4, buff=0.6, edge=6.9)
        same = label(r"for plain gradient descent, \ an L2 penalty and weight decay are one and the same", font_size=26,
                     color=AW).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "There are two ways to keep a network's weights small. <bookmark mark='a'/> Add a penalty to the loss, "
            "lambda over two times the squared size of the weights: L2 regularization. <bookmark mark='b'/> Take a "
            "gradient step on it, and the penalty contributes lambda times theta. <bookmark mark='c'/> Rearranged, "
            "that is: shrink every weight by a factor one minus eta lambda, then take the ordinary step. Weight "
            "decay. <bookmark mark='d'/> For plain gradient descent the two are identical, so for decades the words "
            "were used interchangeably."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("d")
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    def adam(self):
        hist = history_card(2017, r"Ilya Loshchilov \& Frank Hutter", r"\textit{Decoupled Weight Decay Regularization}: "
                            r"\ in Adam, \ L2 and weight decay are different, \ and decay works better", width=6.0)
        hist.to_corner(UR, buff=0.3)
        rows = VGroup(
            cmath(r"\text{Adam} + \text{L2:}\quad", r"\theta", r"\leftarrow", r"\theta - \eta\, \frac{\hat m(\nabla L + \lambda\theta)}{\sqrt{\hat v} + \epsilon}",
                  font_size=32, colors={r"\theta - \eta\, \frac{\hat m(\nabla L + \lambda\theta)}{\sqrt{\hat v} + \epsilon}": L2}),
            cmath(r"\text{AdamW:}\quad", r"\theta", r"\leftarrow", r"(1 - \eta\lambda)\,\theta - \eta\, \frac{\hat m}{\sqrt{\hat v} + \epsilon}",
                  font_size=32, colors={r"(1 - \eta\lambda)\,\theta - \eta\, \frac{\hat m}{\sqrt{\hat v} + \epsilon}": AW}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-1.6, 0.2, 0])
        notes = VGroup(label(r"the penalty's pull is divided by $\sqrt{\hat v}$: \ weights with large gradients are "
                             r"barely decayed", font_size=22, color=L2),
                       label(r"every weight shrinks by the same factor, \ whatever its gradients", font_size=22, color=AW))
        notes[0].next_to(rows[0], DOWN, buff=0.15).align_to(rows[0], LEFT)
        notes[1].next_to(rows[1], DOWN, buff=0.15).align_to(rows[1], LEFT)
        with self.voiceover(
            "Adam breaks that equivalence. <bookmark mark='a'/> Put an L2 penalty into Adam, and the penalty's pull "
            "goes through Adam's division by the root mean square gradient. A weight whose gradients are large is "
            "barely decayed at all, and one whose gradients are tiny is decayed hard: the opposite of what one would "
            "want. <bookmark mark='b'/> Ilya Loshchilov and Frank Hutter pointed this out in 2017, and proposed "
            "applying the decay directly to the weights, outside Adam: AdamW. It became the default optimizer of "
            "the transformer era."
        ) as vo:
            self.play(FadeIn(hist, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grids(self):
        d = load("decay")
        lrs = list(d["lrs"])
        GA, GL = np.asarray(d["grid_adamw"], float), np.asarray(d["grid_adam_l2"], float)
        both = np.concatenate([GA.ravel(), GL.ravel()])
        lo, hi = float(np.nanmin(both)), float(np.nanpercentile(both, 90))
        ha = heat(GA, [-3.4, -0.3, 0], lo=lo, hi=hi)
        hl = heat(GL, [3.4, -0.3, 0], lo=lo, hi=hi)

        def frame(h, grid, strengths, title, col):
            g = VGroup()
            for i, lr in enumerate(lrs):
                g.add(MathTex(lr_tex(lr), font_size=20, color=GREY_B).next_to(h[i * len(strengths)], LEFT, buff=0.12))
            for j, w in enumerate(strengths):
                g.add(MathTex(f"{w:g}", font_size=20, color=GREY_B).next_to(h[(len(lrs) - 1) * len(strengths) + j], DOWN, buff=0.1))
            g.add(label(title, font_size=24, color=col).next_to(h, UP, buff=0.2))
            i, j = np.unravel_index(np.nanargmin(grid), grid.shape)
            g.add(SurroundingRectangle(h[i * len(strengths) + j], color=WHITE, buff=0.0, stroke_width=3))
            return g

        fa = frame(ha, GA, list(d["wd"]), r"AdamW: \ decay $\lambda$ \ (across)", AW)
        fl = frame(hl, GL, list(d["l2"]), r"Adam $+$ L2: \ penalty $\lambda$ \ (across)", L2)
        tag = note(r"held-out bits after $2{,}000$ steps; \ rows: \ learning rate; \ brighter is better; \ $128$ units, "
                   r"\ trained on only $50{,}000$ characters").to_edge(DOWN, buff=0.2)
        sa, sl = np.asarray(d["seeds_adamw"], float), np.asarray(d["seeds_adam_l2"], float)
        none = float(d["none"])
        ba, bl = d["best_adamw"], d["best_adam_l2"]
        sep = sa.max() < sl.min()
        gap = float(sl.mean() - sa.mean())
        # Separate the results into readable cards instead of shrinking one long
        # line across the full frame. Only the first two methods have seed ranges.
        res = VGroup()
        for x, name, mean, spread, col in (
                (-4.45, r"AdamW", sa.mean(), (sa.min(), sa.max()), AW),
                (0, r"Adam $+$ L2", sl.mean(), (sl.min(), sl.max()), L2),
                (4.45, r"no decay", none, None, AD)):
            box = panel(4.1, 1.25, center=[x, 2.85, 0], color=col)
            title = label(name, font_size=24, color=col).move_to([x, 3.24, 0])
            value = label(rf"${mean:.3f}$ bits", font_size=34).move_to([x, 2.85, 0])
            detail = (label(rf"$3$ seeds: \ ${spread[0]:.3f}$--${spread[1]:.3f}$", font_size=20, color=GREY_A)
                      if spread else label(r"baseline", font_size=20, color=GREY_A))
            detail.move_to([x, 2.45, 0])
            res.add(VGroup(box, title, value, detail))
        if sep and gap > 0:
            verdict = (f"AdamW's best is {gap:.3f} bits better than the best L2 penalty, and all three of its seeds beat "
                       "all three of L2's.")
        elif gap > 0:
            verdict = (f"AdamW's best is ahead by {gap:.3f} bits on average, but the seeds overlap: on this model the "
                       "difference is within the luck of the draw.")
        else:
            verdict = (f"here the best L2 penalty does as well as AdamW, or better, by {-gap:.3f} bits: on this small "
                       "model the decoupling doesn't pay.")
        helps = min(sa.mean(), sl.mean()) < none - 0.01
        cols_a = list(d["bestcol_adamw"])
        steady = len(set(cols_a)) <= 2
        ea, el = ba[0] >= max(lrs), bl[0] >= max(lrs)
        etxt = (" Both bests are at our largest learning rate, so a still larger one might help both." if ea and el else
                (" AdamW's best is at our largest learning rate, so it might gain a little more." if ea else
                 (" The L2 penalty's best is at our largest learning rate, so it might gain a little more." if el
                  else "")))
        said1 = (" Both beat no decay at all, so here it really is regularizing." if helps else
            " Neither beats no decay by much: even here, it barely regularizes.")
        said2 = (" And in AdamW's grid the best decay strength barely moves as the learning rate "
            "changes, which is what decoupling promised: two knobs that can be set separately."
            if steady else
            " In AdamW's grid the best decay strength still moves with the learning rate: "
            "the product of the two is what matters.")
        with self.voiceover(
            "Does it matter? A test where regularization should matter: a smaller character model that sees only "
            "fifty thousand characters of training text, over and over. <bookmark mark='a'/> On the left, AdamW at five learning "
            "rates and six decay strengths; on the right, Adam with an L2 penalty, on the same grid of rates. "
            "Brighter is better. <bookmark mark='b'/> The best of each, rerun from three seeds: " + verdict + " <bookmark mark='v'/>"
            + said1 + " <bookmark mark='e'/>" + etxt + " <bookmark mark='c'/>"
            + said2
        ) as vo:
            self.play(FadeIn(ha), FadeIn(fa[:-1]), FadeIn(tag))
            self.play(FadeIn(hl), FadeIn(fl[:-1]))
            vo.wait_until("a")
            self.play(Indicate(fa[-2]), Indicate(fl[-2]))
            vo.wait_until("b")
            self.play(Create(fa[-1]), Create(fl[-1]),
                      LaggedStart(*[FadeIn(card, shift=UP * 0.1) for card in res], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[ha[i * len(d['wd']) + c_] for i, c_ in enumerate(cols_a)]), color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    def curves(self):
        d = load("decay")
        ca, cl, c0 = (np.asarray(d[k], float) for k in ("curve_adamw", "curve_adam_l2", "curve0_adamw"))
        allv = np.concatenate([ca[1:, 1], cl[1:, 1], c0[1:, 1]])
        lo, hi = float(allv.min()) - 0.05, float(min(allv.max(), allv.min() + 1.5)) + 0.05
        g = bits_axes([0, float(ca[-1, 0])], [lo, hi], x_length=7.2, y_length=4.4, center=[-2.4, -0.4, 0], x_step=500,
                      y_step=round((hi - lo) / 4, 2), yfmt=lambda v: f"{v:.2f}")
        ax = g.ax
        lines = [curve(ax, c0[1:, 0], np.clip(c0[1:, 1], lo, hi), AD, 3), curve(ax, cl[1:, 0], np.clip(cl[1:, 1], lo, hi), L2, 3),
                 curve(ax, ca[1:, 0], np.clip(ca[1:, 1], lo, hi), AW, 3.5)]
        ba, bl = d["best_adamw"], d["best_adam_l2"]
        lg = VGroup(label(rf"no decay, \ $\eta = {lr_tex(ba[0])}$", font_size=22, color=AD),
                    label(rf"Adam $+$ L2, \ $\eta = {lr_tex(bl[0])}$, \ $\lambda = {bl[1]:g}$", font_size=22, color=L2),
                    label(rf"AdamW, \ $\eta = {lr_tex(ba[0])}$, \ $\lambda = {ba[1]:g}$", font_size=22, color=AW))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.2, 0])
        keep_in_frame(lg)
        rise0 = float(c0[-1, 1] - c0[1:, 1].min())
        ctag = note(r"seed $0$; \ scored during training on the first $20{,}000$ held-out characters").to_corner(DL, buff=0.2)
        lnk = label(r"what decay does to normalized weights: \ Chapter 15", font_size=22, color=GREY_A).next_to(lg, DOWN, buff=0.6)
        lnk.align_to(lg, LEFT)
        keep_in_frame(lnk)
        said3 = (f"<bookmark mark='a'/> Without decay, the model starts to memorize its fifty thousand characters, and "
            f"the held-out loss climbs back up by {rise0:.2f} bits from its best. "
            if rise0 > 0.02 else
            "<bookmark mark='a'/> Even without decay, the held-out loss keeps falling to the end. ")
        said4 = ("With decay, it ends lower. " if ca[-1, 1] < c0[-1, 1] else
            "With decay, it ends no lower on this stretch of text. ")
        with self.voiceover(
            "Watch the held-out loss during training, seed zero. "
            + said3
            + "<bookmark mark='b'/> "
            + said4
            + "In large language models trained on fresh data, it does something else, which Chapter fifteen "
            "measures."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(ctag))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(lnk), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Decouple the decay",
                          r"In Adam, an L2 penalty is divided by $\sqrt{\hat v}$; \ AdamW shrinks every weight by "
                          r"$(1 - \eta\lambda)$ directly. \ Weight decay and L2 are the same only for plain SGD.",
                          r"Next: \ a ruler for steps, \ from the model's own predictions")
        with self.voiceover(
            "So in Adam, an L2 penalty and weight decay are different things, and the decoupled version is the one "
            "the field adopted. Next, a deeper question: what is the right way to measure the size of a step at "
            "all?"
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
