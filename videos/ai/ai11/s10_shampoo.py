from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, lag, takeaway_card

SH, SO, MU, AD = OPT_COLORS["shampoo"], OPT_COLORS["soap"], OPT_COLORS["muon"], OPT_COLORS["adam"]


def grid_picture(M, center, size=1.6, cmap=(C.TRUE_P, C.MODEL_Q)):
    """A small matrix as an image, blue for negative, orange for positive."""
    M = np.asarray(M, float)
    v = M / (np.abs(M).max() + 1e-12)
    c0, c1 = np.array(ManimColor(cmap[0]).to_rgb()), np.array(ManimColor(cmap[1]).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    pos, neg = np.clip(v, 0, 1)[..., None], np.clip(-v, 0, 1)[..., None]
    rgb = bg * (1 - pos - neg) + c1 * pos + c0 * neg
    img = ImageMobject((255 * rgb).astype(np.uint8)).set_height(size).move_to(center)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return Group(img, SurroundingRectangle(img, color=GREY_C, buff=0.0, stroke_width=1.5))


class Shampoo(VoiceoverScene):
    def construct(self):
        self.card()
        self.shampoo()
        self.bridge()
        self.practice()
        self.soap()
        self.takeaway()

    def card(self):
        c = chapter_card(9, r"Shampoo and SOAP", r"What if the preconditioner saw a whole matrix?", part=PART)
        with self.voiceover("Chapter nine. Shampoo, and SOAP."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def shampoo(self):
        hist = history_card(2018, r"Vineet Gupta, Tomer Koren \& Yoram Singer \ (Google)", r"\textit{Shampoo: \ "
                            r"Preconditioned Stochastic Tensor Optimization}", width=5.6).to_corner(UR, buff=0.3)
        head = label(r"a layer's weights $W$ \ ($m \times n$), \ its gradient $G_t$", font_size=28).to_corner(UL, buff=0.4)
        cl = {r"L_t": SH, r"R_t": SH}
        rows = [
            cmath(r"\Big(\sum_t g_t g_t^\top\Big)^{-1/2} g", r",\quad", r"g = \mathrm{vec}(G)", font_size=32),
            cmath(r"L_t", "=", r"\sum_{s \le t} G_s G_s^\top", r",\quad", r"R_t", "=", r"\sum_{s \le t} G_s^\top G_s",
                  font_size=32, colors=cl),
            cmath(r"\sum_t g_t g_t^\top", r"\preceq", r"r\, L_t^{1/2} \otimes R_t^{1/2}", font_size=32, colors=cl),
            cmath(r"W", r"\leftarrow", r"W - \eta\, L_t^{-1/4}\, G_t\, R_t^{-1/4}", font_size=36,
                  colors={r"W - \eta\, L_t^{-1/4}\, G_t\, R_t^{-1/4}": SH}),
        ]
        whys = [why(r"full-matrix AdaGrad: \ an $mn \times mn$ matrix"), why(r"two small ones: \ $m \times m$ and $n \times n$"),
                why(r"Gupta et al.'s bound, \ $r$ the rank"), why(r"$(A \otimes B)^{-1/2} = A^{-1/2} \otimes B^{-1/2}$, \ in matrix form")]
        step = ladder(self, rows, whys, keep=4, top=1.9, x=-2.0, buff=0.45, edge=6.9)
        kn = label(r"the Kronecker trick of K-FAC, \ with factors built from the gradient alone", font_size=22, color=SH)
        kn.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Adam and AdaGrad treat each weight on its own. The full version of AdaGrad would precondition by a "
            "matrix with a row and a column for every pair of weights, which no one can store. "
            "<bookmark mark='a'/> In 2018 Vineet Gupta, Tomer Koren and Yoram Singer, at Google, used the shape of "
            "a layer. <bookmark mark='b'/> Keep two small running sums instead: G G transpose, over the rows, and G "
            "transpose G, over the columns. <bookmark mark='c'/> They proved that the big matrix is bounded by a "
            "Kronecker product of the two. <bookmark mark='d'/> So precondition the gradient matrix from both "
            "sides, by the inverse fourth roots of L and R. They called it Shampoo: <bookmark mark='e'/> K-FAC's "
            "Kronecker trick, with both factors taken from the gradient itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hist, shift=LEFT * 0.2))
            step(0)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                step(k + 1)
            vo.wait_until("e")
            self.play(FadeIn(kn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bridge(self):
        head = label(r"Shampoo with no memory: \ one gradient, \ $L = GG^\top$, \ $R = G^\top G$", font_size=30).to_edge(UP, buff=0.35)
        cl = {r"U V^\top": MU}
        rows = [
            cmath(r"G", "=", r"U \Sigma V^\top", font_size=36),
            cmath(r"L^{-1/4}\, G\, R^{-1/4}", "=", r"(U \Sigma^{-1/2} U^\top)\,(U \Sigma V^\top)\,(V \Sigma^{-1/2} V^\top)",
                  font_size=34),
            cmath(r"L^{-1/4}\, G\, R^{-1/4}", "=", r"U V^\top", font_size=40, colors=cl),
        ]
        whys = [why(r"the SVD (Part 3)"), why(r"$GG^\top = U\Sigma^2 U^\top$, \ $G^\top G = V \Sigma^2 V^\top$"),
                why(r"every singular value set to $1$")]
        step = ladder(self, rows, whys, keep=3, top=2.0, x=-1.0, buff=0.6, edge=6.9)
        res = label(r"the gradient, \ orthogonalized: \ Muon's step \ (Chapter 10)", font_size=28, color=MU).to_edge(DOWN, buff=0.9)
        cite_ = cite(r"J.~Bernstein \& L.~Newhouse, \textit{Old Optimizer, New Norm: An Anthology} (2024)", corner=DR)
        with self.voiceover(
            "Here is a surprise hidden in Shampoo. Switch off its memory, so the two factors come from the current "
            "gradient alone. <bookmark mark='a'/> Write the gradient by its singular value decomposition, from part "
            "three. <bookmark mark='b'/> Then L to the minus a quarter, and R to the minus a quarter, are built from "
            "the same singular vectors, with the singular values raised to minus a half. <bookmark mark='c'/> "
            "Multiply out, and every singular value cancels: what is left is U V transpose, the gradient with all "
            "its singular values set to one. Jeremy Bernstein and Laker Newhouse pointed this out in 2024. "
            "<bookmark mark='d'/> Remember that matrix: it is Muon's step."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        probs = VGroup(
            label(r"inverse fourth roots: \ eigendecompositions, \ every few steps", font_size=24, color=WHITE),
            label(r"badly conditioned factors: \ damping, \ high precision", font_size=24, color=WHITE),
            label(r"an awkward step size: \ \textit{grafting}, \ Adam's size with Shampoo's direction", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=0.5)
        hdr = label(r"why Shampoo took years to catch on", font_size=28, color=SH).next_to(probs, UP, buff=0.3).align_to(probs, LEFT)
        algo = theorem_card(r"AlgoPerf, \ 2024", r"Eight workloads, \ fixed hardware, \ time to a target. \ External "
                            r"tuning: \ won by Distributed Shampoo, \ about $28\%$ faster than the baseline (NAdamW). \ "
                            r"Self-tuning: \ won by schedule-free AdamW, \ about $8\%$.",
                            who=r"Kasimbeg et al., \textit{Accelerating Neural Network Training} (2025)", width=7.4,
                            font_size=22, kind=r"Benchmark", color=SH).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Shampoo was hard to use. <bookmark mark='a'/> Inverse fourth roots need eigendecompositions, which are "
            "slow, so they are refreshed only every few steps; the factors are badly conditioned and need damping; "
            "and the size of its step is awkward, so practical versions graft on Adam's size and keep only "
            "Shampoo's direction. <bookmark mark='b'/> Engineers at Meta and Google made it practical as Distributed "
            "Shampoo, and in 2024 it won the external-tuning track of AlgoPerf, a benchmark that times training "
            "algorithms to a target on eight workloads with fixed hardware: about twenty-eight percent faster than "
            "the baseline, counting its extra cost per step."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(lag([FadeIn(p, shift=RIGHT * 0.2) for p in probs], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(algo, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def soap(self):
        rng_ = np.random.default_rng(4)
        A = rng_.normal(size=(12, 12)) @ np.diag(np.geomspace(3, 0.1, 12)) @ rng_.normal(size=(12, 12)) / 4
        U, S, Vt = np.linalg.svd(A)
        rot = U.T @ A @ Vt.T
        cx = [-5.2, -2.1, 1.0, 4.1]
        pics = Group(grid_picture(A, [cx[0], 0.8, 0]), grid_picture(rot, [cx[1], 0.8, 0]),
                     grid_picture(np.sign(rot) * np.minimum(np.abs(rot), 0.25 * np.abs(rot).max()), [cx[2], 0.8, 0]),
                     grid_picture(U @ (np.sign(rot) * np.minimum(np.abs(rot), 0.25 * np.abs(rot).max())) @ Vt, [cx[3], 0.8, 0]))
        caps = VGroup(label(r"the gradient $G$", font_size=20, color=GREY_A),
                      label(r"$Q_L^\top G\, Q_R$: \ in Shampoo's \\ eigenbases", font_size=20, color=SO),
                      label(r"Adam, \\ coordinate by coordinate", font_size=20, color=AD),
                      label(r"rotated back", font_size=20, color=SO))
        for c_, p_ in zip(caps, pics):
            c_.next_to(p_, DOWN, buff=0.15)
        arrows = VGroup(*[Arrow(pics[i].get_right(), pics[i + 1].get_left(), buff=0.15, color=GREY_B, stroke_width=3,
                                max_tip_length_to_length_ratio=0.25) for i in range(3)])
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        hist = history_card(2024, r"Nikhil Vyas, Depen Morwani, \dots, Sham Kakade \ (Harvard)",
                            r"SOAP: \ ShampoO with Adam in the Preconditioner's eigenbasis. \ Reported: \ over $40\%$ fewer "
                            r"steps and $35\%$ less time than AdamW, \ at $360$M and $660$M parameters", width=8.4)
        hist.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2024 a group at Harvard simplified it. <bookmark mark='a'/> Shampoo's two factors have "
            "eigenvectors: a rotation of the rows, and one of the columns. <bookmark mark='b'/> Rotate the gradient "
            "into those bases, run plain Adam there, coordinate by coordinate, <bookmark mark='c'/> and rotate the "
            "step back. The rotation is refreshed every few steps; Adam does the rest. They called it SOAP, and "
            "reported reaching AdamW's loss in over forty percent fewer steps on language models of up to six hundred "
            "and sixty million parameters. Shampoo, it turns out, is close to a cheap form of Adam in its own "
            "eigenbasis. SOAP runs in our race too."
        ) as vo:
            self.play(FadeIn(pics[0]), FadeIn(caps[0]), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(pics[1]), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(pics[2]), FadeIn(caps[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(pics[3]), FadeIn(caps[3]))
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Precondition the whole matrix",
                          r"Shampoo: \ $L^{-1/4} G R^{-1/4}$, \ two small factors per layer. \ Without memory it is "
                          r"$U V^\top$. \ SOAP: \ Adam in Shampoo's eigenbasis.",
                          r"Next: \ $UV^\top$, derived as the steepest step")
        with self.voiceover(
            "So Shampoo preconditions a whole matrix with two small factors, SOAP runs Adam in their eigenbasis, "
            "and Shampoo without memory is the orthogonalized gradient. Next, why that matrix is the steepest step "
            "of all."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
