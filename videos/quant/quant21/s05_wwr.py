from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, GOOD, PART, ask, fit_right, illustration, load


class WWR(VoiceoverScene):
    def construct(self):
        w = load("wwr")
        self.card()
        self.idea()
        self.curve_(w)
        self.examples()

    def card(self):
        c = chapter_card(4, r"Wrong-way risk", r"What if they fail exactly when they owe you most?", part=PART)
        with self.voiceover("Chapter four. Wrong-way risk: when the counterparty fails exactly when it owes you most."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"\text{CVA}", r"=", r"(1 - R)\sum_i \mathbb{E}\big[\max(V(t_i), 0)\,\big|\,\tau \in (t_{i-1}, "
                      r"t_i]\big]\,P(0, t_i)\,\mathbb{P}(\tau \in \cdot)", font_size=32, colors={r"\text{CVA}": CVA_C}),
                cmath(r"U_\tau", r"=", r"\rho\,Z_x + \sqrt{1 - \rho^2}\,\varepsilon,\quad \tau = Q^{-1}\big(N(U_\tau)\big)",
                      font_size=36, colors={r"U_\tau": BAD})]
        whys = [why(r"the formula of chapter 3 used the unconditional exposure; the right one is the exposure given "
                    r"that the counterparty is defaulting. If the two are dependent, they differ"),
                why(r"a simple model: the default time and the rate factor share a Gaussian copula with correlation "
                    r"$\rho$; positive $\rho$ makes default likelier on the paths where the bank is owed the most")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The formula so far assumed that a counterparty's default has nothing to do with how much it owes. The "
            "correct formula uses the exposure on the paths where it defaults. <bookmark mark='a'/> Tie the two "
            "together with a copula, Part twenty's tool: a correlation between the counterparty's default time and "
            "the rate that drives the trade's value."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def curve_(self, w):
        r_, c_ = np.asarray(w["rhos"]), np.asarray(w["cva"]) * 1e3
        g = axes([-0.7, 1.0], [0, 750], x_length=7.4, y_length=4.4, xlabel=r"correlation of default with the rate factor",
                 ylabel=r"CVA, \$ thousand", xticks=[-0.6, -0.3, 0, 0.3, 0.6, 0.9], yticks=[0, 250, 500, 750],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        k0 = int(np.argmin(np.abs(r_)))
        base = DashedLine(ax.c2p(-0.7, c_[k0]), ax.c2p(1.0, c_[k0]), color=GREY_B, stroke_width=1.5)
        line = VGroup(curve(ax, r_, c_, CVA_C, stroke_width=3.5), *[Dot(ax.c2p(a, b), color=CVA_C) for a, b in zip(r_, c_)])
        side = VGroup(
            MathTex(rf"\rho = 0:\ {c_[k0]:.0f}\text{{k}}", font_size=28),
            MathTex(rf"\rho = 0.9:\ {c_[-1]:.0f}\text{{k}}\ (\times {c_[-1] / c_[k0]:.1f})", font_size=28, color=BAD),
            MathTex(rf"\rho = -0.6:\ {c_[0]:.0f}\text{{k}}\ (\text{{right-way}})", font_size=26, color=GOOD),
            wrapped_label(r"same exposure, same default probability, only the dependence changes. The hard part is "
                          r"that $\rho$ cannot be estimated from calm data", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The netting set again, with the counterparty's default probability unchanged and only the dependence "
            f"varied. <bookmark mark='a'/> Independent, the CVA is {c_[k0]:.0f} thousand. <bookmark mark='b'/> With "
            f"default strongly tied to the paths where the bank is owed most, it is {c_[-1]:.0f}, "
            f"{c_[-1] / c_[k0]:.1f} times as much. In the other direction, right-way risk, it shrinks. Nothing about "
            "the counterparty's rating or the trade's average exposure changed."
        ) as vo:
            self.play(FadeIn(g), Create(base))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def examples(self):
        cards = VGroup(
            desk_question(r"general wrong-way risk", r"a counterparty whose credit worsens with the same market move that "
                          r"raises your exposure: an oil producer that sold you oil forwards, an emerging-market bank "
                          r"that owes you dollars against its own currency", width=12.0, font_size=21),
            desk_question(r"specific wrong-way risk", r"exposure tied to the counterparty itself: protection bought from a "
                          r"seller whose default is correlated with the reference name's, as banks found with the "
                          r"monoline insurers that had sold them protection on mortgage securities in 2007--08",
                          width=12.0, font_size=21),
            desk_question(r"Archegos (chapter 13)", r"the collateral was the same few stocks whose fall caused the "
                          r"default: margin that disappears exactly when it is needed", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Where does it happen? General wrong-way risk: a counterparty whose credit falls with the same market "
            "move that raises your exposure, like an oil producer that sold you oil forward. <bookmark mark='a'/> "
            "Specific: protection bought from a seller whose fate is tied to what it insures, as banks learned with "
            "the bond insurers that had sold them protection on mortgage securities. <bookmark mark='b'/> And "
            "collateral that is the counterparty's own risk, the story of Archegos at the end of this part."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"you buy CDS protection on a bank from another bank in the same country. What kind of risk is that, "
                r"and how would you price it?")
        with self.voiceover("You buy protection on one bank from another bank in the same country. What kind of risk is "
                            "that, and how would you price it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
