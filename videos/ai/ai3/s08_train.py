from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import GRAD, MONO, load

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
        self.descent()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Training by going downhill", r"Can descent find what counting found?", part=3)
        with self.voiceover("Chapter seven. Training."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
