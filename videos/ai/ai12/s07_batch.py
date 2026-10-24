from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, PART, load

LEVEL_COLORS = ["#7FD3FF", C.BITS, C.MODEL_Q]


class Batch(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.tradeoff()
        self.noise()

    def card(self):
        card = chapter_card(6, r"How big a batch?", r"When does a bigger batch stop saving time?", part=PART)
        with self.voiceover("Chapter six. How big a batch?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"one step of gradient descent, \ with a batch of $B$ examples", font_size=30).to_edge(UP, buff=0.35)
        colors = {r"B_{\text{noise}}": C.ADVANTAGE, r"\epsilon": C.BITS}
        rows = [
            cmath(r"\mathbb{E}\,\Delta L", r"\approx", r"-\epsilon\, |G|^2 + \tfrac{\epsilon^2}{2}\Big(G^\top H G + "
                  r"\tfrac{\operatorname{tr}(H\Sigma)}{B}\Big)", font_size=32, colors=colors),
            cmath(r"\epsilon^*", r"=", r"\frac{|G|^2}{G^\top H G + \operatorname{tr}(H\Sigma)/B}", font_size=32, colors=colors),
            cmath(r"\mathbb{E}\,\Delta L^*", r"=", r"\frac{\Delta L_{\max}}{1 + B_{\text{noise}}/B}", r",\quad",
                  r"B_{\text{noise}}", r"= \frac{\operatorname{tr}(H\Sigma)}{G^\top H G} \approx \frac{\operatorname{tr}\Sigma}{|G|^2}",
                  font_size=32, colors=colors),
            cmath(r"S = S_{\min}\big(1 + \tfrac{B_{\text{noise}}}{B}\big)", r",\quad",
                  r"E = BS = E_{\min}\big(1 + \tfrac{B}{B_{\text{noise}}}\big)", font_size=32, colors=colors),
            cmath(r"\Big(\frac{S}{S_{\min}} - 1\Big)\Big(\frac{E}{E_{\min}} - 1\Big)", r"=", r"1", font_size=34),
        ]
        whys = [why(r"Taylor to second order; \ the batch's noise $\Sigma/B$"), why(r"the best step: \ minimize in $\epsilon$"),
                why(r"substitute; \ $H \propto I$ for the last step"), why(r"steps and examples to a target, \ per step's gain"),
                why(r"eliminate $B$")]
        step = ladder(self, rows, whys, keep=5, top=2.4, x=-2.4, buff=0.4, edge=6.9)
        cite_ = cite(r"S.~McCandlish, J.~Kaplan, D.~Amodei \& the OpenAI Dota team, \textit{An Empirical Model of "
                     r"Large-Batch Training} (2018)", corner=DL)
        with self.voiceover(
            "Part eleven showed that a small batch gives a noisy gradient. How big should the batch be? In 2018, Sam "
            "McCandlish and colleagues at OpenAI answered with one step of algebra. <bookmark mark='a'/> Expand the "
            "loss after one step to second order: the gradient helps, the curvature and the batch's noise hurt. "
            "<bookmark mark='b'/> Choose the best step size. <bookmark mark='c'/> The best gain is the noise-free "
            "gain divided by one plus a ratio, the noise scale over the batch: how many examples it takes for the "
            "gradient's signal to beat its noise. <bookmark mark='d'/> So the number of steps to reach a loss "
            "falls as the batch grows, and the number of examples rises. <bookmark mark='e'/> Eliminate the batch, "
            "and steps and examples trade off along a hyperbola. Far below the noise scale, doubling the batch "
            "halves the steps for free; far above it, it only wastes examples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tradeoff(self):
        b = load("batch")
        Bs = np.asarray(b["batches"], float)
        S, Ex = np.asarray(b["S"], float), np.asarray(b["E"], float)
        levels = [float(v) for v in b["levels"]]
        smin, bcrit = np.asarray(b["Smin"], float), np.asarray(b["Bcrit"], float)
        lS, lE = np.log10(S[np.isfinite(S)]), np.log10(Ex[np.isfinite(Ex)])
        x0, x1 = math.floor(lE.min() * 2) / 2 - 0.1, math.ceil(lE.max() * 2) / 2 + 0.1
        y0, y1 = math.floor(lS.min() * 2) / 2 - 0.1, math.ceil(lS.max() * 2) / 2 + 0.1
        ax = CornerAxes(x_range=[x0, x1, 0.5], y_range=[y0, y1, 0.5], x_length=6.6, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.6, -0.5, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                      for v in range(math.ceil(y0), math.floor(y1) + 1)])
        xn = label(r"characters read, \ $E$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"optimizer steps, \ $S$", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        groups = VGroup()
        for i, (lv, col) in enumerate(zip(levels, LEVEL_COLORS)):
            ok = np.isfinite(S[i])
            pts = VGroup(*[Dot(ax.c2p(math.log10(e), math.log10(s)), radius=0.07, color=col)
                           for e, s in zip(Ex[i][ok], S[i][ok])])
            bb = np.geomspace(Bs.min() / 2, Bs.max() * 2, 80)
            ss = smin[i] * (1 + bcrit[i] / bb)
            ee = bb * ss
            keep = (np.log10(ee) > x0) & (np.log10(ee) < x1) & (np.log10(ss) > y0) & (np.log10(ss) < y1)
            hyp = curve(ax, np.log10(ee[keep]), np.log10(ss[keep]), col, 2.5, smooth=True)
            knee = Dot(ax.c2p(math.log10(2 * bcrit[i] * smin[i]), math.log10(2 * smin[i])), radius=0.09, color=WHITE)
            groups.add(VGroup(hyp, pts, knee))
        bl = VGroup(*[label(f"{int(v):,}".replace(",", "{,}"), font_size=16, color=GREY_B)
                      .next_to(ax.c2p(math.log10(Ex[0][j]), math.log10(S[0][j])), UR, buff=0.04)
                      for j, v in enumerate(Bs) if np.isfinite(S[0][j]) and j % 2 == 0])
        lg = VGroup(*[label(rf"to {lv:.1f} bits: \ $B_{{\text{{crit}}}} \approx {bc:,.0f}$".replace(",", "{,}"), font_size=22,
                            color=col) for lv, bc, col in zip(levels, bcrit, LEVEL_COLORS)])
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, 1.4, 0])
        kn = label(r"white: \ the knee, \ $B = B_{\text{crit}}$: \\ twice the fewest steps, \\ twice the fewest examples",
                   font_size=20, color=GREY_A).next_to(lg, DOWN, buff=0.35).align_to(lg, LEFT)
        tag = note(rf"computed: \ width ${int(b['width'])}$, \ batches ${int(Bs[0])}$ to ${int(Bs[-1]):,}$, \ the best of "
                   r"three learning rates at each".replace(",", "{,}")).to_corner(DL, buff=0.2)
        grows = bcrit[-1] > bcrit[0] * 1.3
        said1 = (
            f"the hyperbola moves out, and the critical batch grows: {bcrit[1]:,.0f}, then {bcrit[2]:,.0f}. The "
            "closer a model gets to the end of training, the larger the batch it can use."
            if grows else
            f"the critical batch is {bcrit[1]:,.0f} and {bcrit[2]:,.0f}: at our scale it barely changes."
        )
        with self.voiceover(
            f"Measure it. Train our character model with batches from {int(Bs[0])} to {int(Bs[-1]):,} characters, "
            "each at the best of three learning rates, and count the steps and the characters it takes to reach a "
            f"loss. <bookmark mark='a'/> To reach {levels[0]:.1f} bits, the points fall on a hyperbola, with a "
            f"critical batch of about {bcrit[0]:,.0f}. <bookmark mark='b'/> To reach lower losses, "
            + said1
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(groups[0][1]), FadeIn(bl))
            self.play(Create(groups[0][0]), FadeIn(groups[0][2]), FadeIn(lg[0]), FadeIn(kn))
            vo.wait_until("b")
            for g, l_ in zip(groups[1:], lg[1:]):
                self.play(FadeIn(g[1]), Create(g[0]), FadeIn(g[2]), FadeIn(l_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def noise(self):
        b = load("batch")
        levels = [float(v) for v in b["levels"]]
        bcrit, noise = np.asarray(b["Bcrit"], float), np.asarray(b["noise"], float)
        rows = VGroup(label(r"loss reached", font_size=22, color=GREY_A), label(r"$B_{\text{crit}}$, \ from the hyperbola",
                                                                              font_size=22, color=GREY_A),
                      label(r"noise scale, \ measured", font_size=22, color=GREY_A))
        grid = VGroup()
        for lv, bc, ns, col in zip(levels, bcrit, noise, LEVEL_COLORS):
            grid.add(VGroup(label(f"{lv:.1f} bits", font_size=24, color=col),
                            MathTex(f"{bc:,.0f}".replace(",", "{,}"), font_size=28, color=col),
                            MathTex(f"{ns:,.0f}".replace(",", "{,}") if np.isfinite(ns) else r"\text{--}", font_size=28, color=col)))
        tab = VGroup(rows, *grid)
        for j in range(3):
            col = VGroup(rows[j], *[g[j] for g in grid]).arrange(DOWN, buff=0.25)
            col.move_to([-4.6 + 3.0 * j, 0.9, 0])
        hd = label(r"two ways to the same number", font_size=30).to_edge(UP, buff=0.4)
        how = label(r"noise scale: \ $\operatorname{tr}\Sigma / |G|^2$ \ from gradients at batches $64$ and $4{,}096$ \ "
                    r"(McCandlish et al., Appendix A)", font_size=20, color=GREY_B).next_to(tab, DOWN, buff=0.35).set_x(-1.6)
        cards = VGroup(
            history_card(2020, r"Kaplan et al.", r"the critical batch grows as the loss falls: \ "
                         r"$B_{\text{crit}} \propto L^{-1/0.21}$", width=5.8, color=HIST),
            history_card(2024, r"Zhang et al.; \ Bergsma et al.\ (2025)", r"it grows with the data, \ not with the model's "
                         r"size", width=5.8, color=HIST),
            history_card(2024, r"DeepSeek-V3", r"batch raised from $3{,}072$ to $15{,}360$ sequences over the first "
                         r"$469$ billion tokens", width=5.8, color=HIST)).arrange(DOWN, buff=0.15).move_to([3.6, -1.7, 0])
        ratio = noise / bcrit
        agree = np.all(np.isfinite(ratio)) and np.all((ratio > 0.2) & (ratio < 5))
        said2 = (
            f"They agree to within a factor of {max(ratio.max(), 1 / ratio.min()):.1f}: rough, as McCandlish and "
            "colleagues found too, but the same order, from a single measurement instead of a sweep. "
            if agree else
            "Here they disagree by more than a factor of five: the simple noise scale ignores the curvature, and "
            "Adam reshapes the noise. "
        )
        with self.voiceover(
            "Is the critical batch really the noise scale? We can measure the noise scale directly, from the sizes "
            "of gradients at two batch sizes, as the loss passes each level. <bookmark mark='a'/> "
            + said2
            + "<bookmark mark='b'/> Kaplan's laws found the critical batch growing as the loss falls, and later work "
            "found that it grows with the amount of data, not the size of the model. So large runs raise their batch "
            "as they go: DeepSeek-V3 grew its batch fivefold, from 3,072 sequences to 15,360, over its first 469 "
            "billion tokens."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(rows), *[FadeIn(g[:2]) for g in grid])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g[2]) for g in grid], lag_ratio=0.3), FadeIn(how))
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
