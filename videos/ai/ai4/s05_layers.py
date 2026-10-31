from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE, load, matrix_heat


def gap(x: float) -> str:
    """A measured difference, for the narration: 'exactly zero', or its size."""
    return "exactly zero" if x == 0 else f"{x:.0e}".replace("e-", " times ten to the minus ").replace("e+", "e")


def gap_tex(x: float) -> str:
    return "0" if x == 0 else sci(x, 1)


class Layers(VoiceoverScene):
    def construct(self):
        self.card()
        self.matmul()
        self.softmax()
        self.layernorm()

    def card(self):
        card = chapter_card(4, r"The Jacobians of real layers", r"What does a layer's derivative look like?", part=PART)
        with self.voiceover("Chapter four. The Jacobians of real layers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def matmul(self):
        d = load("jacobians")
        col = {r"G": GRAD, r"G^\top": GRAD, r"X^\top": VALUE, r"W^\top": VALUE}
        rows = [
            cmath(r"Y_{ik}", r"=", r"\textstyle\sum_j X_{ij}\, W_{jk}", font_size=36),
            cmath(r"\frac{\partial \mathcal L}{\partial W_{jk}}", r"=", r"\textstyle\sum_i G_{ik}\, X_{ij}", font_size=36),
            cmath(r"\frac{\partial \mathcal L}{\partial W}", r"=", r"X^\top", r"G", font_size=36, colors=col),
            cmath(r"\frac{\partial \mathcal L}{\partial X}", r"=", r"G", r"W^\top", font_size=36, colors=col),
        ]
        whys = [why(r"a layer: \ inputs $X$ (one row per token) times weights $W$"),
                why(r"$W_{jk}$ touches only column $k$ of $Y$; \ $G = \partial\mathcal L / \partial Y$ arrives from above"),
                why(r"the sum over $i$ is a matrix product"), why(r"the same argument, for $X$")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-3.4, buff=0.4, edge=6.9)
        T, dd = int(d["T"]), int(d["d"])
        cost = VGroup(
            label(rf"GPT-2's first MLP matrix, \ ${dd} \times {4 * dd}$, \ over ${fmt_int(T)}$ tokens:", font_size=24,
                  color=GREY_A),
            label(rf"the full Jacobian $\partial Y / \partial W$: \ ${sci(d['jac_entries'], 1)}$ numbers, \ "
                  rf"${d['jac_bytes'] / 1e12:.0f}$ terabytes", font_size=26, color=C.SURPRISE),
            label(rf"the product $X^\top G$: \ ${sci(d['vjp_flops'], 1)}$ multiplications and additions", font_size=26,
                  color=GRAD),
            label(rf"checked against our library: \ largest difference ${gap_tex(d['mm_diff'])}$", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real layers first. The most common one is a matrix product: inputs X, one row per token, times weights "
            "W. <bookmark mark='a'/> A weight in row j and column k touches only column k of the output, so its "
            "gradient collects the gradient arriving from above, G, times the inputs it multiplied. "
            "<bookmark mark='b'/> That sum is itself a matrix product: X transposed times G. <bookmark mark='c'/> "
            "And the gradient for the inputs, which flows on to the layer below, is G times W transposed. "
            "<bookmark mark='d'/> Notice what we never wrote down: the Jacobian itself. For one of GPT-2's matrices "
            f"over {T:,} tokens it would hold {d['jac_entries'] / 1e12:.1f} trillion numbers. Backpropagation needs "
            "only its product with G, which costs about as much as the layer did on the way forward."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cost], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def softmax(self):
        d = load("jacobians")
        p = np.asarray(d["p"])
        J = np.asarray(d["J_sm"])
        eig = np.asarray(d["eig_sm"])
        assert d["sm_diff"] < 1e-12 and eig.min() > -1e-12 and d["sm_null"] < 1e-12
        rows = [
            cmath(r"p_i", r"=", r"\frac{e^{z_i}}{S}, \quad S = \textstyle\sum_k e^{z_k}", font_size=34, colors={r"p_i": C.PROB}),
            cmath(r"\frac{\partial p_i}{\partial z_j}", r"=", r"\frac{\delta_{ij}\, e^{z_i} S - e^{z_i} e^{z_j}}{S^2}",
                  font_size=34),
            cmath(r"\frac{\partial p_i}{\partial z_j}", r"=", r"p_i\, \delta_{ij} - p_i\, p_j", font_size=34),
            cmath(r"J", r"=", r"\operatorname{diag}(p) - p\, p^\top", font_size=38, colors={r"J": GRAD}),
        ]
        whys = [why(r"the softmax", font_size=22), why(r"quotient rule; \ $\partial S / \partial z_j = e^{z_j}$", font_size=22),
                why(r"split the fraction", font_size=22), why(r"as a matrix", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-4.2, buff=0.42, edge=6.9)
        heat = matrix_heat(J, cell=0.6, numbers=True, fmt="{:.2f}", font_size=16).move_to([4.6, -1.75, 0])
        hl = label(rf"computed: \ $5$ scores; \ library: \ difference ${gap_tex(d['sm_diff'])}$", font_size=20,
                   color=GREY_B).next_to(heat, UP, buff=0.15)
        props = VGroup(
            label(r"rows add to $0$: \ $J\,\mathbf 1 = 0$", font_size=25, color=GREY_A),
            label(r"symmetric, \ eigenvalues $\ge 0$:", font_size=25, color=GREY_A),
            MathTex(r",\ ".join(f"{max(v, 0):.3f}" for v in eig), font_size=28, color=GRAD),
            label(r"$J^\top g = p \odot (g - p\cdot g)$: \ $n$ steps, \ not $n^2$", font_size=25, color=GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-3.6, -2.3, 0])
        with self.voiceover(
            "Next, the softmax, which turns scores into probabilities. <bookmark mark='a'/> Differentiate with the "
            "quotient rule. <bookmark mark='b'/> Split the fraction, and every entry is p i times delta i j, minus p i "
            "times p j. <bookmark mark='c'/> As a matrix: the probabilities on the diagonal, minus the outer product "
            "of p with itself. <bookmark mark='d'/> Here it is for five scores, computed, and matching our library. "
            "Its rows add to zero, because adding the same number to every score changes nothing; and it is "
            "symmetric with no negative eigenvalues, one of them zero. <bookmark mark='e'/> Again we never need the "
            "matrix: its product with a vector takes n steps instead of n squared, which matters with GPT-2's "
            "fifty thousand tokens in the vocabulary. Joined with the cross-entropy, it collapses to Part 1's q "
            "minus p."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(heat), FadeIn(hl))
            self.play(FadeIn(props[0]), FadeIn(props[1]), FadeIn(props[2]))
            vo.wait_until("e")
            self.play(FadeIn(props[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layernorm(self):
        d = load("jacobians")
        J = np.asarray(d["J_ln"])
        eig = np.asarray(d["eig_ln"])
        assert d["ln_diff"] < 1e-10
        n_small = int((np.abs(eig) < 1e-3).sum())
        rows = [
            cmath(r"y", r"=", r"\frac{x - \mu\,\mathbf 1}{\sigma}, \quad \sigma = \sqrt{v + \epsilon}", font_size=36),
            cmath(r"J", r"=", r"\frac{1}{\sigma}\Big(I - \tfrac1n \mathbf 1 \mathbf 1^\top - \tfrac1n\, y\, y^\top\Big)",
                  font_size=36, colors={r"J": GRAD}),
        ]
        whys = [why(r"layer norm: \ subtract the mean $\mu$, \\ divide by the spread ($v$: the variance)", font_size=22),
                why(r"$\mu$ and $\sigma$ move with $x$ too: \\ two corrections", font_size=22)]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-3.0, buff=0.6, edge=6.9)
        heat = matrix_heat(J, cell=0.45, numbers=False).move_to([-3.6, -1.6, 0])
        hl = label(rf"computed: \ $6$ numbers; \ library: \ difference ${gap_tex(d['ln_diff'])}$", font_size=20,
                   color=GREY_B).next_to(heat, UP, buff=0.15)
        ev = VGroup(label(r"eigenvalues:", font_size=24, color=GREY_A),
                    MathTex(r",\ ".join(sci(abs(v), 0) if abs(v) < 1e-3 else f"{v:.3f}" for v in eig), font_size=28,
                            color=GRAD),
                    label(r"mean: \ eigenvalue $0$; \ scale: \ $\epsilon/\sigma^3$", font_size=24, color=GRAD),
                    label(r"mean is removed; \ scale sensitivity is suppressed", font_size=24, color=GREY_A))
        ev.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([2.8, -1.6, 0])
        with self.voiceover(
            "Last, layer norm: subtract the mean of the vector, divide by its spread, before any learned scale and "
            "shift. <bookmark mark='a'/> The mean "
            "and the spread move when x moves, so the Jacobian has two corrections: a projection that removes the "
            "direction of all ones, and another that suppresses the radial direction, all divided by sigma. "
            f"<bookmark mark='b'/> Computed for six numbers, {n_small} eigenvalues have magnitude below one "
            "thousandth, and the rest are equal. Mean shifts are removed exactly; scale changes are strongly "
            "suppressed, with a small remaining sensitivity from epsilon."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(heat), FadeIn(hl))
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in ev], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
