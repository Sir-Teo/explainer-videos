from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data


class Correlation(VoiceoverScene):
    def construct(self):
        w = load("worstof")
        self.card()
        self.worst(w)

    def card(self):
        c = chapter_card(7, r"Worst-of, and correlation", r"Why does a two-index note pay more than either alone?",
                         part=PART)
        with self.voiceover("Chapter seven. Worst-of, and correlation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def worst(self, w):
        rh = np.asarray(w["rhos"])
        pr = np.asarray(w["prices"])
        g = axes([-0.2, 1.0], [0.1, 0.18], x_length=6.4, y_length=4.2, xlabel=r"correlation between the two indices",
                 ylabel=r"worst-of put, at the money, one year", xticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yticks=[0.10, 0.12, 0.14, 0.16, 0.18], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, rh, pr, OPT, stroke_width=3)
        s1, s2 = w["single"]
        h1 = DashedLine(ax.c2p(-0.2, s2), ax.c2p(1.0, s2), stroke_color=GREY_B, stroke_width=1.5)
        h1l = label(r"a put on the HSCEI alone", font_size=16, color=GREY_B).next_to(ax.c2p(-0.2, s2), UR, buff=0.05)
        mk = DashedLine(ax.c2p(w["rho_measured"], 0.1), ax.c2p(w["rho_measured"], 0.18), stroke_color=IV, stroke_width=2)
        mkl = label(rf"measured, 2021--2023: {w['rho_measured']:.2f}", font_size=17, color=IV).next_to(
            ax.c2p(w["rho_measured"], 0.18), DOWN, buff=0.1)
        side = VGroup(
            wrapped_label(r"a worst-of note pays on whichever of several underlyings does worst: the investor is short "
                          r"a put on the worst performer, so the coupon is higher", 4.4, 19, GREY_A),
            wrapped_label(r"the lower the correlation, the likelier one of them falls: the put is worth more, and the "
                          r"buyer is paid more for selling it", 4.4, 19, WHITE),
            wrapped_label(r"the dealer, long that put, is short correlation: in a crash correlations jump toward one "
                          r"(Part 11), the dealer gains on the move but must re-mark a correlation input no market quotes "
                          r"directly. The correlation skew, implied correlation higher on the downside, prices that",
                          4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = real_data(rf"vols from 2021--2023: CSI 500 ETF {100 * w['sig1']:.0f}\%, HSCEI {100 * w['sig2']:.0f}\%; "
                        r"200{,}000 paths")
        with self.voiceover(
            "Structurers have a trick for raising the coupon: link the note to the worst of two or three indices. "
            "The buyer is now short a put on whichever falls furthest. <bookmark mark='a'/> How much is that worth? "
            "It depends on how the indices move together. If they moved as one, the put would be a put on the "
            "riskier index alone. The lower the correlation, the more likely one of them falls, and the dearer the "
            f"put. Between the CSI 500 and the HSCEI, the measured correlation over 2021 to 2023 was "
            f"{w['rho_measured']:.2f}. <bookmark mark='b'/> So the dealer, long that put, is short correlation, an "
            "input no market quotes directly. Correlations jump toward one in crashes, and desks charge for it with a "
            "correlation skew: higher implied correlation on the downside."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), Create(h1), FadeIn(h1l), Create(mk), FadeIn(mkl), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
