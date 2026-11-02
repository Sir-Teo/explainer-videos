from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import control as C
from videos.quant.quant8.common import BAD, GOOD, KELLY, PART, VALUE


class Utility(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.gamma()

    def card(self):
        c = chapter_card(1, r"Utility and risk aversion", r"What is a gamble worth to you?", part=PART)
        with self.voiceover("Chapter one. Utility, and risk aversion."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curves(self):
        g = axes([0, 200], [-1.6, 0.8], x_length=6.6, y_length=4.6, xlabel=r"wealth", ylabel=r"utility (log)",
                 xticks=[50, 100, 150, 200], yticks=[], font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = g.ax
        w = np.linspace(20, 200, 200)
        u = np.log(w / 100)
        line = curve(ax, w, u, VALUE, stroke_width=4)
        a, b = (50, np.log(0.5)), (150, np.log(1.5))
        pa, pb = Dot(ax.c2p(*a), color=GOOD), Dot(ax.c2p(*b), color=GOOD)
        chord = Line(ax.c2p(*a), ax.c2p(*b), color=GREY_B, stroke_width=2)
        eu = 0.5 * (a[1] + b[1])
        mid = Dot(ax.c2p(100, eu), color=WHITE)
        ce = C.certainty_equivalent([50, 150], [0.5, 0.5], 1.0)
        cedot = Dot(ax.c2p(ce, eu), color=KELLY)
        hline = DashedLine(ax.c2p(ce, eu), ax.c2p(100, eu), color=KELLY, stroke_width=2)
        vline = DashedLine(ax.c2p(ce, eu), ax.c2p(ce, -1.6), color=KELLY, stroke_width=2)
        cel = MathTex(rf"CE = {ce:.1f}", font_size=26, color=KELLY).next_to(cedot, LEFT, buff=0.15).shift(UP * 0.25)
        side = VGroup(
            label(r"a coin flip: 50 or 150, from 100", font_size=24, color=GREY_A),
            MathTex(r"\mathbb{E}[u(W)] = \tfrac12 u(50) + \tfrac12 u(150)", font_size=30),
            MathTex(r"u(CE) = \mathbb{E}[u(W)]", font_size=30, color=KELLY),
            wrapped_label(r"Daniel Bernoulli (1738): value a gamble by the logarithm of wealth, not by its money "
                          r"average; von Neumann and Morgenstern (1944): any consistent ranking of gambles is an "
                          r"expected utility", 4.6, 20, GREY_A),
            wrapped_label(r"concave $u$ means a sure amount below the average is worth as much as the gamble; the gap "
                          r"is the risk premium", 4.6, 20, VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In 1738 Daniel Bernoulli proposed that a gamble should be valued not by its average payoff in money but "
            "by the average of a utility, and he chose the logarithm of wealth. In 1944 John von Neumann and Oskar "
            "Morgenstern showed that anyone whose choices among gambles obey a few consistency axioms behaves as if "
            "maximizing an expected utility. <bookmark mark='a'/> Take a coin flip that leaves you with fifty or one "
            "hundred and fifty, from a hundred. Its average is a hundred. Its expected log utility sits on the chord, "
            "below the curve, because the curve bends. <bookmark mark='b'/> The sure amount with the same utility, "
            f"the certainty equivalent, is {ce:.1f}. You would pay up to {100 - ce:.1f} to avoid a fair gamble: that "
            "gap is the risk premium, and the bend of the curve is risk aversion."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), Create(chord), FadeIn(mid), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(cedot), Create(hline), Create(vline), FadeIn(cel), FadeIn(side[2]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def gamma(self):
        gam = [0.5, 1, 2, 3, 5, 10, 30]
        ces = [C.certainty_equivalent([50, 150], [0.5, 0.5], g_) for g_ in gam]
        rows = [cmath(r"u(W)", r"=", r"\frac{W^{1-\gamma}}{1-\gamma}", font_size=38, colors={r"u(W)": VALUE}),
                cmath(r"\pi", r"\approx", r"\tfrac12\,\gamma\,\frac{\sigma^2}{W}", font_size=38, colors={r"\pi": KELLY})]
        whys = [why(r"constant relative risk aversion $\gamma$: you take the same gambles in percent at any wealth; "
                    r"$\gamma = 1$ is the log"),
                why(r"Arrow (1965) and Pratt (1964): for small gambles the premium is half of $\gamma$ times the "
                    r"variance, relative to wealth")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-2.4, buff=0.9, edge=6.9)
        tab = VGroup()
        head = VGroup(MathTex(r"\gamma", font_size=28, color=GREY_B), label(r"certainty equivalent of 50 or 150",
                                                                           font_size=20, color=GREY_B))
        cells = [head] + [VGroup(MathTex(f"{g_:g}", font_size=28, color=VALUE),
                                 MathTex(f"{c_:.1f}", font_size=28, color=KELLY)) for g_, c_ in zip(gam, ces)]
        tab = VGroup(*[m for r_ in cells for m in r_]).arrange_in_grid(rows=len(cells), cols=2, buff=(0.8, 0.12),
                                                                    col_alignments="cc")
        tab.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        side = wrapped_label(r"what $\gamma$ do people have? Surveys and lab choices: about 1 to 10. Part 6's "
                             r"consumption Euler equation needed about 400 to explain the equity premium.", 5.0, 21,
                             GREY_A).next_to(tab, RIGHT, buff=1.0).align_to(tab, DOWN)
        with self.voiceover(
            "Economists usually work with constant relative risk aversion: utility is wealth to the power one minus "
            "gamma, divided by one minus gamma, and gamma equal to one is the logarithm. Someone with this utility "
            "takes the same gambles, in percentages, whether rich or poor. <bookmark mark='a'/> Kenneth Arrow and "
            "John Pratt showed that for a small gamble the premium you would pay to avoid it is about half of gamma "
            "times its variance, relative to your wealth. <bookmark mark='b'/> Here is the coin flip's certainty "
            f"equivalent as gamma rises: from {ces[0]:.0f} at a half, through the log's {ces[1]:.0f}, to {ces[-1]:.0f} "
            "at thirty, barely above the worst outcome. <bookmark mark='c'/> Surveys and laboratory choices put most people's gamma between one and ten. "
            "Part six found that the consumption data needed a gamma of about four hundred to explain the equity "
            "premium: one reason economists still argue about what gamma is."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.2, run_time=3))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
