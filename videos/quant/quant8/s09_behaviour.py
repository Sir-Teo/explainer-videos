from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE

ALPHA, LAM, GAM_G = 0.88, 2.25, 0.61  # Tversky and Kahneman (1992)


def v(x):
    x = np.asarray(x, float)
    return np.where(x >= 0, np.abs(x) ** ALPHA, -LAM * np.abs(x) ** ALPHA)


def w(p, g=GAM_G):
    p = np.asarray(p, float)
    return p ** g / (p ** g + (1 - p) ** g) ** (1 / g)


class Behaviour(VoiceoverScene):
    def construct(self):
        self.card()
        self.prospect()
        self.ambiguity()

    def card(self):
        c = chapter_card(8, r"How people decide: prospect theory and ambiguity", r"What do real decisions look like?",
                         part=PART)
        with self.voiceover("Chapter eight. How people really decide: prospect theory, and ambiguity."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def prospect(self):
        g1 = axes([-100, 100], [-150, 70], x_length=5.4, y_length=4.0, xlabel=r"gain or loss", ylabel=r"value",
                  xticks=[-100, 0, 100], yticks=[], font_size=17)
        g2 = axes([0, 1], [0, 1], x_length=4.0, y_length=4.0, xlabel=r"probability", ylabel=r"decision weight",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=17)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.8)
        x = np.linspace(-100, 100, 201)
        lv = curve(g1.ax, x, v(x), VALUE, stroke_width=4)
        ref = DashedLine(g1.ax.c2p(0, -150), g1.ax.c2p(0, 70), color=GREY_C, stroke_width=1.5)
        p = np.linspace(0.001, 0.999, 200)
        diag = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        lw = curve(g2.ax, p, w(p), KELLY, stroke_width=4)
        notes = VGroup(
            MathTex(r"v(x) = x^{0.88}\ (x \ge 0),\quad -2.25\,(-x)^{0.88}\ (x < 0)", font_size=28, color=VALUE),
            wrapped_label(r"measured from a reference point, not from wealth; losses hurt about twice as much as gains "
                          r"please; small probabilities overweighted, large ones underweighted (Kahneman and Tversky "
                          r"1979; Tversky and Kahneman 1992)", 11.6, 21, GREY_A),
            wrapped_label(r"in markets: the disposition effect, selling winners and holding losers (Shefrin and Statman "
                          r"1985); lottery-like stocks overpriced (Barberis and Huang 2008)", 11.6, 21, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Expected utility describes how a consistent investor should choose. Daniel Kahneman and Amos Tversky "
            "studied how people do choose, and in 1979 proposed prospect theory. <bookmark mark='a'/> People value "
            "gains and losses from a reference point, usually where they started, not their total wealth; and a loss "
            "hurts about two and a quarter times as much as an equal gain pleases. <bookmark mark='b'/> They also "
            "weigh probabilities unevenly: a one percent chance feels larger than it is, a ninety-nine percent "
            "chance smaller. <bookmark mark='c'/> These shapes leave fingerprints in markets: investors sell winners "
            "too early and hold losers too long, and stocks that look like lottery tickets are overpriced."
        ) as vo:
            self.play(FadeIn(g1), Create(ref))
            vo.wait_until("a")
            self.play(Create(lv), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(diag), Create(lw), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def ambiguity(self):
        rows = [cmath(r"\max_{\pi}\ \min_{Q \in \mathcal{P}}", r"\ ", r"\mathbb{E}_Q[u(W)]", font_size=36,
                      colors={r"\max_{\pi}\ \min_{Q \in \mathcal{P}}": ALT}),
                cmath(r"\pi^*", r"=", r"\frac{\mu - r}{(\gamma + \theta)\,\sigma^2}", font_size=38,
                      colors={r"\pi^*": KELLY})]
        whys = [why(r"Gilboa and Schmeidler (1989): when you do not know the probabilities, choose the action whose "
                    r"worst plausible model is best"),
                why(r"Hansen and Sargent's robust control; for Merton, Maenhout (2004): doubt about the mean acts like "
                    r"extra risk aversion $\theta$")]
        step = ladder(self, rows, whys, keep=2, top=0.7, x=-1.4, buff=0.9, edge=6.9)
        urn = VGroup(
            label(r"Ellsberg (1961): an urn of 90 balls, 30 red, 60 black or yellow in unknown proportion", font_size=26,
                  color=GREY_A),
            wrapped_label(r"most people prefer to bet on red rather than black, and on black-or-yellow rather than "
                          r"red-or-yellow: no single probability makes both choices consistent", 12.0, 23, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.6)
        with self.voiceover(
            "A second departure: people dislike not knowing the odds, separately from disliking risk. Daniel "
            "Ellsberg's urn of 1961 holds thirty red balls and sixty black or yellow, in unknown proportion. Most "
            "people would rather bet on red than on black, and on black-or-yellow than on red-or-yellow. No single "
            "probability for black makes both choices consistent. <bookmark mark='a'/> Itzhak Gilboa and David "
            "Schmeidler made this a theory in 1989: when the model is uncertain, choose the action whose worst "
            "plausible model is best. <bookmark mark='b'/> Lars Hansen and Thomas Sargent built robust control on the "
            "same idea. Applied to Merton's problem by Pascal Maenhout in 2004, doubt about the expected return acts "
            "like extra risk aversion: the robust investor holds less, which is one honest answer to chapter three's "
            "uncertain inputs."
        ) as vo:
            self.play(FadeIn(urn))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.4)
        self.clear_scene()
