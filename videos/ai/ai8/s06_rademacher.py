from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, NEG, POS, card_body, chapter, curve, load


class Rademacher(VoiceoverScene):
    def construct(self):
        chapter(self, 5, r"Rademacher complexity", r"How well can a family fit pure noise?",
                "Chapter five. Rademacher complexity.")
        self.coins()
        self.theorem()
        self.linear()

    # ------------------------------------------------------------------
    def coins(self):
        r = load("rademacher")
        ds, acc = np.asarray(r["ds"]), np.asarray(r["acc"])
        ax = Axes(x_range=[0, 70, 10], y_range=[0.5, 0.8, 0.1], x_length=6.4, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.0, -1.0, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 0.6, 0.7, 0.8)])
        xl = label(r"how many of the $70$ word rates the line may use", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yn = label(r"coin flips fitted", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c = curve(ax, ds, np.clip(acc, 0.5, 0.8), C.MODEL_Q)
        dots = VGroup(*[Dot(ax.c2p(d, min(a, 0.8)), radius=0.06, color=C.MODEL_Q) for d, a in zip(ds, acc)])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(70, 0.5), color=GREY_B)
        hl = label(r"guessing", font_size=22, color=GREY_B).next_to(half, DOWN, buff=0.08).align_to(half, RIGHT)
        from videos.ai.ai8.compute import rng

        n = int(r["n"])
        flips = rng(1960).choice([-1.0, 1.0], size=n)
        cells = VGroup(*[Square(0.11, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9) for _ in range(n)])
        cells.arrange_in_grid(cols=56, buff=0.02).move_to([-2.4, 2.75, 0])
        if cells.width > 7.4:
            cells.scale_to_fit_width(7.4)
        cl = label(rf"the ${n}$ training pages, \\ each given a coin flip $\sigma_i = \pm 1$", font_size=22, color=GREY_A)
        cl.next_to(cells, RIGHT, buff=0.35)
        keep_in_frame(cl)
        dfn = definition_card(r"empirical Rademacher complexity",
                              MathTex(r"\hat{\mathfrak R}_S(\mathcal H) = \mathbb{E}_\sigma \sup_{h \in \mathcal H}"
                                      r"\frac1n \sum_{i=1}^n \sigma_i\, h(x_i)", font_size=32),
                              width=5.4).move_to([3.9, -0.6, 0])
        dsub = label(r"how well the family's best member \\ correlates with random signs", font_size=21,
                     color=GREY_A).next_to(dfn, DOWN, buff=0.2)
        with self.voiceover(
            "Counting labellings needs a family's worst case. There's a more direct test of capacity, done on the "
            "data you actually have. Give each training page a random label, a coin flip, plus or minus one, and "
            "ask the family to fit them. <bookmark mark='a'/> A linear rule on one word rate gets barely more than "
            f"half. On all seventy, it fits {100 * acc[-1]:.0f} percent of the coin flips: pure noise. "
            "<bookmark mark='b'/> Averaged over the coin flips, the best correlation the family can reach with "
            "random signs is its empirical Rademacher complexity, named for the random plus-or-minus-one variables "
            "of Hans Rademacher. A family that can fit noise well can make any training score look good."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.002), FadeIn(cl), run_time=1.2)
            self.play(LaggedStart(*[c_.animate.set_fill(POS if f > 0 else NEG) for c_, f in zip(cells, flips)],
                                  lag_ratio=0.003), run_time=2.0)
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(Create(c), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(dfn, shift=LEFT * 0.2), FadeIn(dsub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = theorem_card(r"the Rademacher bound",
                           card_body(r"for losses in $[0, 1]$, \ with probability at least $1 - \delta$, \ for "
                                     r"every $h \in \mathcal H$ at once:",
                                     r"R(h) \le \hat R(h) + 2\,\hat{\mathfrak R}_S(\ell \circ \mathcal H) + "
                                     r"3\sqrt{\dfrac{\ln(2/\delta)}{2n}}", width=9.6, font_size=28),
                           who=r"V.~Koltchinskii (2001); \ P.~Bartlett \& S.~Mendelson (2002)", width=10.6, font_size=28)
        thm.move_to(UP * 1.5)
        why_ = VGroup(
            label(r"$\bullet$ \ symmetrize with a ghost sample, \ as for VC", font_size=28, color=GREY_A),
            label(r"$\bullet$ \ the ghost's signs become random $\sigma_i$: \ no counting needed", font_size=28,
                  color=GREY_A),
            label(r"$\bullet$ \ McDiarmid's inequality: \ one example moves the supremum by at most $1/n$", font_size=28,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(thm, DOWN, buff=0.45).align_to(thm, LEFT)
        hist = history_card(2002, r"P.~Bartlett \& S.~Mendelson", r"\textit{Rademacher and Gaussian Complexities: "
                            r"Risk Bounds and Structural Results}", width=5.4, font_size=18, color=HIST)
        hist.to_corner(DR, buff=0.25)
        with self.voiceover(
            "And it bounds the gap. With probability one minus delta, every rule's true risk is at most its "
            "training risk, plus twice the Rademacher complexity of the losses, plus a term that shrinks like one "
            "over root n. <bookmark mark='a'/> The proof starts like VC's, with a ghost sample. <bookmark mark='b'/> "
            "Swapping a real example with its ghost twin is a random sign, so the gap becomes a correlation with "
            "random signs, with no counting at all. <bookmark mark='c'/> And because one example can move the "
            "supremum by at most one over n, McDiarmid's inequality, a cousin of Hoeffding's, makes the measured "
            "complexity concentrate. Koltchinskii, and Bartlett and Mendelson, gave it this form around 2002."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(why_[k], shift=UP * 0.1))
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        r = load("radlin")
        rows = [
            cmath(r"\sup_{|w| \le B} \frac1n \sum_i \sigma_i\, w \cdot x_i", r"=",
                  r"\frac{B}{n} \Big|\sum_i \sigma_i x_i\Big|", font_size=32),
            cmath(r"\hat{\mathfrak R}_S", r"\le", r"\frac{B}{n} \sqrt{\mathbb{E}_\sigma \Big|\sum_i \sigma_i x_i\Big|^2}",
                  font_size=32),
            cmath(r"\hat{\mathfrak R}_S", r"\le", r"\frac{B}{n} \sqrt{\textstyle\sum_i |x_i|^2}", r"\le",
                  r"\frac{B\,R}{\sqrt n}", font_size=32, colors={r"\frac{B\,R}{\sqrt n}": BOUND}),
        ]
        whys = [why(r"Cauchy--Schwarz; \ equality at $w \propto \sum_i \sigma_i x_i$"),
                why(r"Jensen: \ $\mathbb{E}\sqrt{Z} \le \sqrt{\mathbb{E}Z}$"),
                why(r"$\mathbb{E}\,\sigma_i\sigma_j = 0$ \ for $i \ne j$; \ $|x_i| \le R$")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-2.2, buff=0.38, edge=6.9)
        ns = np.asarray(r["ns"], float)
        meas, bound, rb = np.asarray(r["meas"]), np.asarray(r["bound"]), np.asarray(r["rbound"])
        G = log_axes_(ns, meas, bound, rb)
        ax = G.ax
        cm = VGroup(curve(ax, np.log10(ns), np.log10(meas), MEAS, 4),
                    *[Dot(ax.c2p(math.log10(a), math.log10(b)), radius=0.05, color=MEAS) for a, b in zip(ns, meas)])
        cb = curve(ax, np.log10(ns), np.log10(bound), BOUND, 10).set_stroke(opacity=0.45)
        cr = curve(ax, np.log10(ns), np.log10(rb), GREY_B, 2.5)
        key = legend([(MEAS, r"measured: \ $4{,}000$ sign draws"), (BOUND, r"$\frac{B}{n}\sqrt{\sum |x_i|^2}$"),
                      (GREY_B, r"$BR/\sqrt n$")], font_size=19).next_to(G, RIGHT, buff=0.3).align_to(G, UP)
        ratio = float((meas / bound).min())
        info = label(rf"$d = {int(r['d'])}$ word rates, \ $B = 1$; \ $20{{,}}000$ random directions reach "
                     rf"${r['tried']:.2f}$, \ the formula's direction ${r['best']:.2f}$", font_size=21, color=GREY_A)
        info.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "For linear rules with weights of length at most B, the complexity can be computed exactly. "
            "<bookmark mark='a'/> The best weight vector for given signs points along the signed sum of the inputs, "
            "by Cauchy–Schwarz, so the supremum is B over n times the length of that sum. <bookmark mark='b'/> "
            "Jensen moves the expectation inside the square root, <bookmark mark='c'/> and since independent signs "
            "are uncorrelated, the cross terms vanish: B over n times the root of the sum of squared lengths, at most "
            "B times the largest length R, over root n. <bookmark mark='d'/> On the pages: the measured complexity "
            f"sits within {100 * (1 - ratio):.0f} percent of the bound at every size, falling like one over root n. "
            f"Twenty thousand random directions reach only {r['tried']:.2f}; the formula's direction reaches "
            f"{r['best']:.2f}. And notice what's missing: the dimension. Only the length of the weights counts, "
            "which is what the next chapter exploits."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(rows[0]), FadeOut(rows[1]), FadeOut(whys[0]), FadeOut(whys[1]),
                      VGroup(rows[2], whys[2]).animate.to_edge(UP, buff=0.4))
            self.play(FadeIn(G), Create(cb), Create(cr), FadeIn(key[1:]))
            self.play(Create(cm), FadeIn(key[0]), FadeIn(info), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()


def log_axes_(ns, meas, bound, rb):
    from videos.ai.ai8.common import log_axes

    lo = math.floor(math.log10(meas.min()) * 2) / 2
    hi = math.ceil(math.log10(max(bound.max(), rb.max())) * 2) / 2
    return log_axes((0.8, 2.8), (lo, hi), x_length=6.6, y_length=4.0, xticks=[1, 2], yticks=[0, lo, hi] if lo < 0 < hi
                    else [lo, hi], xlabel=r"$n$ pages", ylabel=r"$\hat{\mathfrak R}_S$ \ (log scale)", center=(-1.8, -0.6, 0),
                    font_size=20)
