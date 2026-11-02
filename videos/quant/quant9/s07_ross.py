from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, PUT, Q_C, illustration, load


def heat(M, size=0.36, lo=None, hi=None, color_lo=None, color_hi=None):
    M = np.asarray(M)
    lo = M.min() if lo is None else lo
    hi = M.max() if hi is None else hi
    g = VGroup()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = float(np.clip((M[i, j] - lo) / (hi - lo + 1e-12), 0, 1))
            g.add(Square(size, stroke_width=0.5, stroke_color=BACKGROUND,
                         fill_color=interpolate_color(ManimColor(color_lo or BACKGROUND), ManimColor(color_hi or Q_C), v),
                         fill_opacity=1).move_to([j * size, -i * size, 0]))
    return g


class Ross(VoiceoverScene):
    def construct(self):
        r = load("ross")
        self.card()
        self.theorem()
        self.economies(r)

    def card(self):
        c = chapter_card(6, r"Ross recovery, and its critique", r"Can option prices reveal real probabilities?",
                         lit=(2015,), part=PART)
        with self.voiceover("Chapter six. Ross recovery, and its critique."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        rows = [cmath(r"P_{ij}", r"=", r"\pi_{ij}\, m_{ij}", font_size=38, colors={r"P_{ij}": Q_C}),
                cmath(r"m_{ij}", r"=", r"\delta\,\frac{\phi(j)}{\phi(i)}", font_size=38, colors={r"m_{ij}": ALT}),
                cmath(r"P\,z", r"=", r"\delta\, z,\qquad \pi_{ij} = \frac{P_{ij}\, z_j}{\delta\, z_i}", font_size=36,
                      colors={r"P\,z": CALL})]
        whys = [why(r"state prices for moving from state $i$ to $j$: the real probability times the discount factor"),
                why(r"Ross's assumption (2015): the discount factor depends only on where you start and end, like a "
                    r"representative investor's marginal utility"),
                why(r"then Perron--Frobenius: the positive eigenvector of the state-price matrix recovers $\pi$, the "
                    r"market's real probabilities, from prices alone")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Option prices give us Q. Can they give us P, the probabilities the market really believes? Stephen "
            "Ross claimed in 2015 that they can. Write the state prices for moving between states as the real "
            "transition probability times the discount factor. <bookmark mark='a'/> Assume, as with a "
            "representative investor, that the discount factor depends only on where you start and where you end, "
            "through a single function of the state. <bookmark mark='b'/> Then a theorem of Oskar Perron and Georg "
            "Frobenius does the rest: the state-price matrix has one positive eigenvector, and it unlocks the real "
            "probabilities. Prices alone, no history needed."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def economies(self, r):
        pi, rec, rec2 = (np.asarray(r[k]) for k in ("pi", "recovered", "recovered2"))
        hi = max(pi.max(), rec2.max())
        h1, h2, h3 = (heat(M, size=0.3, lo=0, hi=hi) for M in (pi, rec, rec2))
        tl = [label(t, font_size=20, color=c) for t, c in ((r"the truth", GREY_A), (r"recovered: Ross's world", CALL),
                                                          (r"recovered: with permanent shocks", ARB))]
        blocks = VGroup(*[VGroup(t_, h).arrange(DOWN, buff=0.15) for t_, h in zip(tl, (h1, h2, h3))])
        blocks.arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.6)
        sub = label(r"transition probabilities between 9 states of the economy (rows: today, columns: tomorrow)",
                    font_size=19, color=GREY_B).next_to(blocks, DOWN, buff=0.2)
        side = VGroup(
            MathTex(rf"\text{{Ross's world: largest error }} {r['err1']:.0e}", font_size=28, color=CALL),
            MathTex(rf"\text{{with permanent shocks: }} {r['err2']:.3f}", font_size=28, color=ARB),
            MathTex(rf"\text{{long-run consumption vs trend: true }} {100 * r['mean_true']:+.1f}\%,\ \text{{recovered }} "
                    rf"{100 * r['mean_rec2']:+.1f}\%", font_size=28, color=ARB),
            wrapped_label(r"Borovi\v{c}ka, Hansen and Scheinkman (2016): when the discount factor has a permanent part, as "
                          r"it does with growing consumption, the eigenvector recovers a long-run risk-adjusted measure, "
                          r"not $P$; the assumption cannot be tested from prices alone", 11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        src = illustration(r"two synthetic economies with a known truth")
        with self.voiceover(
            "Test it where we know the truth. A synthetic economy with nine states, and a representative investor "
            "with constant relative risk aversion: exactly Ross's assumption. <bookmark mark='a'/> From state "
            "prices alone, the recovered probabilities match the truth to the last digit. <bookmark mark='b'/> Now "
            "add what real economies have: a permanent component in the discount factor, shocks to wealth that do "
            "not wash out. The recovery still returns a clean answer, but the wrong one. It is pessimistic: it puts "
            f"the economy's long-run level {100 * abs(r['mean_rec2']):.1f} percent below trend when the truth is "
            f"{100 * r['mean_true']:.1f} percent above. <bookmark mark='c'/> Jaroslav Borovička, Lars Hansen and José Scheinkman "
            "showed in 2016 that this is general: the eigenvector recovers a risk-adjusted long-run measure, not the "
            "real probabilities, and nothing in prices alone can tell you which world you are in."
        ) as vo:
            self.play(FadeIn(blocks[0]), FadeIn(sub), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(blocks[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(blocks[2]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
