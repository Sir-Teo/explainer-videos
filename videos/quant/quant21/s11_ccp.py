from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, COLL, GOOD, IM_C, PART, ask, fit_right, illustration, load


class CCP(VoiceoverScene):
    def construct(self):
        c = load("ccp")
        self.card()
        self.novation()
        self.waterfall(c)
        self.sim(c)

    def card(self):
        c = chapter_card(10, r"Central clearing", r"What happens when a clearing member fails?", part=PART)
        with self.voiceover("Chapter ten. Central clearing, and the waterfall that absorbs a member's default."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def novation(self):
        names = ["A", "B", "C", "D", "E"]
        ang = np.linspace(0, 2 * np.pi, 6)[:-1] + np.pi / 2
        left = VGroup(*[Circle(radius=0.32, color=GREY_B).move_to([-4.0 + 1.6 * np.cos(a_), 0.4 + 1.6 * np.sin(a_), 0])
                        for a_ in ang])
        llab = VGroup(*[MathTex(n_, font_size=26).move_to(c_) for n_, c_ in zip(names, left)])
        ledges = VGroup(*[Line(left[i].get_center(), left[j].get_center(), color=GREY_C, stroke_width=1.5, buff=0.32)
                          for i in range(5) for j in range(i + 1, 5)])
        right = VGroup(*[Circle(radius=0.32, color=GREY_B).move_to([3.6 + 1.8 * np.cos(a_), 0.4 + 1.8 * np.sin(a_), 0])
                         for a_ in ang])
        rlab = VGroup(*[MathTex(n_, font_size=26).move_to(c_) for n_, c_ in zip(names, right)])
        hub = Circle(radius=0.5, color=COLL, fill_opacity=0.25).move_to([3.6, 0.4, 0])
        hl = label(r"CCP", font_size=20).move_to(hub)
        redges = VGroup(*[Line(hub.get_center(), r_.get_center(), color=COLL, stroke_width=2, buff=0.45) for r_ in right])
        foot = wrapped_label(r"novation: the clearing house becomes the buyer to every seller and the seller to every "
                             r"buyer. Ten bilateral exposures become five, netted across everyone; since 2009's G20 "
                             r"commitments, standard swaps must be cleared. The largest: LCH, CME, ICE", 12.0, 19,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "After 2008, the G20 required standard derivatives to be cleared. <bookmark mark='a'/> Bilaterally, five "
            "dealers have ten relationships, each with its own exposure. <bookmark mark='b'/> With a clearing house, "
            "every trade is replaced by two, one with the clearing house on each side, and each dealer has one "
            "exposure, netted across all its trades with everyone. The clearing house has none, as long as everyone "
            "pays. The question is what happens when someone does not."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(llab), Create(ledges))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rlab), FadeIn(hub), FadeIn(hl), Create(redges), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def waterfall(self, c):
        layers = [("defaulter's initial margin", IM_C), ("defaulter's default-fund contribution", QC.SPOT),
                  ("CCP's own capital: skin in the game", QC.IMPLIED), ("survivors' default-fund contributions", BAD),
                  ("assessments on survivors", QC.LOSS), ("recovery and resolution tools", GREY_B)]
        blocks = VGroup()
        for i, (t, c_) in enumerate(layers):
            r_ = Rectangle(width=6.0, height=0.7, stroke_color=WHITE, stroke_width=1.5, fill_color=c_, fill_opacity=0.35)
            r_.move_to([-2.0, 2.2 - 0.82 * i, 0])
            blocks.add(VGroup(r_, label(t, font_size=19).move_to(r_)))
        arrow = Arrow([2.0, 2.6, 0], [2.0, -2.2, 0], buff=0, color=BAD, stroke_width=4)
        side = wrapped_label(r"each layer is used only when the one above is exhausted. The default fund is sized to "
                             rf"'Cover 2' (CPMI--IOSCO, 2012): the default of the two members with the largest exposures in "
                             r"extreme but plausible conditions. Here: {c['df_total']:.0f} against total margin of 100",
                             4.2, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "If a member defaults, its losses run down a waterfall. <bookmark mark='a'/> First its own initial margin, "
            "then its contribution to the default fund, then a slice of the clearing house's own capital, skin in the "
            "game, then the default-fund contributions of the members who did nothing wrong, then calls on them for "
            "more. <bookmark mark='b'/> The fund is sized so that the default of the two largest members, in extreme "
            "but plausible markets, stays within it: the Cover 2 standard."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.1) for b_ in blocks], lag_ratio=0.3), GrowArrow(arrow))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def sim(self, c):
        hit = c["hit_given_default"]
        names = [("defaulter fund", r"defaulter's fund"), ("CCP capital", r"CCP capital"),
                 ("survivors' fund", r"survivors' fund"), ("assessments", r"assessments"), ("uncovered", r"uncovered")]
        g = axes([0.4, 5.6], [0, 100], x_length=7.2, y_length=4.2, xlabel=r"", ylabel=r"\% of default scenarios reaching it",
                 xticks=[], yticks=[0, 25, 50, 75, 100], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (k, n_) in enumerate(names):
            v = 100 * hit[k]
            b_ = Rectangle(width=0.7, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                           fill_color=BAD if i >= 2 else QC.SPOT, fill_opacity=0.8).move_to(
                [ax.c2p(i + 1, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(rf"{v:.1f}" if v >= 1 else rf"{v:.2f}", font_size=22).next_to(b_, UP, buff=0.08),
                            wrapped_label(n_, 1.3, 15, GREY_A).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.15)))
        one_in = 1 / max(hit["survivors' fund"], 1e-9)
        side = VGroup(
            MathTex(rf"\mathbb{{P}}(\text{{any default in a year}}) = {100 * c['p_any_default']:.1f}\%", font_size=24),
            MathTex(rf"\mathbb{{P}}(\text{{two or more}}) = {100 * c['p_two']:.1f}\%", font_size=24),
            wrapped_label(r"20 members of unequal size, defaults correlated through one stress factor, close-out losses "
                          r"heavier in stress; illustrative. Most defaults stop at the defaulter's own resources; the "
                          r"survivors pay in about one in eight", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Simulate a clearing house with twenty members of unequal size, defaults that cluster in stress, and "
            "close-out losses that are worse when they do. <bookmark mark='a'/> In the years with a default, most "
            "losses stop at the defaulter's own margin and fund contribution. <bookmark mark='b'/> In about one in "
            f"{one_in:.0f} the surviving members' money is used, "
            "and only rarely is anything left uncovered. The design moves the tail from the clearing house to its "
            "members, which is why members watch each other's risk so closely."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(bars[1]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(bars[3]), FadeIn(bars[4]), FadeIn(side[2]))
        q = ask(r"a clearing house lowers its margin to win business from a rival. Who bears the risk it no longer "
                r"collects?")
        with self.voiceover("A clearing house lowers its margins to win business from a rival. Who bears the risk it no "
                            "longer collects?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
