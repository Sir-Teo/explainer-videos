from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403

SHOW = ("USA", "CHN", "DEU", "JPN", "MEX", "CAN", "KOR", "GBR")


class Formula(VoiceoverScene):
    def construct(self):
        card(self, 8, r"One formula, \ and a counterfactual", r"What if America and China traded less?",
             "Chapter eight. One formula, and a counterfactual.",
             lit={2008: r"Dekle, \ Eaton and Kortum", 2012: r"Arkolakis, \ Costinot and Rodr\'iguez-Clare"},
             scale=("nation", "world"), horizon=("a decade",))
        self.autarky()
        self.counterfactual()

    def autarky(self):
        H = load("hat")
        idx = [H["regions"].index(c) for c in SHOW]
        ax = plane([0.4, len(SHOW) + 0.6], [0, 12], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[], yticks=[0, 3, 6, 9, 12], ylabel=r"loss from autarky, \ \% of real income",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars, nms = VGroup(), VGroup()
        for k, i in enumerate(idx):
            v = 100 * H["acr"][i]
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=GAIN, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            nms.add(VGroup(label(SHOW[k], font_size=15, color=WHITE), label(f"{v:.1f}", font_size=14, color=GAIN))
                    .arrange(DOWN, buff=0.04).next_to(ax.ax.c2p(k + 1, 0), DOWN, buff=0.1))
        eq = MathTex(r"1 - \lambda^{1/\theta}", font_size=38).to_edge(UP, buff=0.3).shift(RIGHT * 3.5)
        us = H["regions"].index("USA")
        big = MathTex(r"\text{loss from autarky} = 1 - \lambda^{1/\theta}", font_size=54).move_to(UP * 0.9)
        work = MathTex(rf"\text{{America, 2019:}} \quad 1 - {H['lambda'][us]:.3f}^{{1/{H['theta']:.0f}}} = "
                       rf"{100 * H['acr'][us]:.1f}\%", font_size=40, color=GAIN).next_to(big, DOWN, buff=0.6)
        keys = label(r"$\lambda$: \ the share of spending on home goods; \ $\theta$: \ the trade elasticity",
                     font_size=22, color=GREY_A).next_to(work, DOWN, buff=0.5)
        side = VGroup(
            label(rf"$\theta$ = {H['theta']:.0f}; \\ $\lambda$: \ spending \\ on home goods", font_size=18,
                  color=GREY_A),
            label(r"large, \ closed \\ economies gain least; \\ small, \ open ones most", font_size=18,
                  color=WHITE),
            label(r"Krugman, \ Melitz \\ and Eaton-Kortum \\ all give this formula", font_size=18, color=ARCH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"CEPII Gravity (BACI), \ 2019; \ Arkolakis, \ Costinot and Rodr\'iguez-Clare (2012)",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Part thirty-five's formula for the gains from trade has a remarkable property. Arkolakis, Costinot "
            "and Rodriguez-Clare showed that Krugman's model, Melitz's and Eaton and Kortum's all give the same "
            "answer from the same two numbers: the share of spending on home goods, and the trade elasticity. "
            "<bookmark mark='a'/> Here it is computed from 2019 trade data with an elasticity of four, for eight "
            "economies, counting domestic spending as GDP less goods exports. <bookmark mark='b'/> Large economies "
            "that trade little relative to their size, like America and China, would lose under three percent in "
            "autarky; open ones like Germany, Korea and Mexico around nine or ten. <bookmark mark='c'/> The models "
            "differ in how trade works, but not, at this level, in how much it is worth."
        ) as vo:
            self.play(FadeIn(big), FadeIn(tag))
            self.play(FadeIn(keys), FadeIn(work, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(work), FadeOut(keys), ReplacementTransform(big, eq), FadeIn(ax))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), FadeIn(nms),
                      FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def counterfactual(self):
        H = load("hat")
        idx = [H["regions"].index(c) for c in SHOW]
        ax = plane([0.4, len(SHOW) + 0.6], [-0.4, 0.2], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[], yticks=[-0.4, -0.2, 0, 0.2], ylabel=r"change in real income, \ \%",
                   yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=14)
        zero = seg(ax, 0.4, 0, len(SHOW) + 0.6, 0, GREY_B, 1.5)
        bars, nms = VGroup(), VGroup()
        for k, i in enumerate(idx):
            v = 100 * H["welfare"][i]
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01),
                               fill_color=GAIN if v > 0 else TARIFF, fill_opacity=0.85, stroke_width=0).move_to(
                (p0 + p1) / 2))
            nms.add(VGroup(label(SHOW[k], font_size=15, color=WHITE), label(f"{v:+.2f}", font_size=14,
                                                                            color=GAIN if v > 0 else TARIFF))
                    .arrange(DOWN, buff=0.04).next_to(ax.ax.c2p(k + 1, -0.4), DOWN, buff=0.1))
        u, c = H["regions"].index("USA"), H["regions"].index("CHN")
        side = VGroup(
            label(rf"trade costs between \\ America and China \\ +{100 * (H['rise'] - 1):.0f}\%", font_size=18,
                  color=TARIFF),
            label(rf"America's spending \\ on Chinese goods: \\ {100 * H['us_china_share_before']:.1f}\% $\to$ "
                  rf"{100 * H['us_china_share_after']:.1f}\%", font_size=18, color=WHITE),
            label(r"both lose; \\ Mexico and Canada gain \\ from diversion", font_size=18, color=GAIN),
            label(r"exact hat algebra: \\ only today's shares \\ and $\theta$ are needed", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"CEPII Gravity (BACI), \ 2019; \ Dekle, \ Eaton and Kortum (2008); \ this film", corner=DR,
                       font_size=12)
        dek = VGroup(
            MathTex(r"\hat\pi_{ni} = \frac{(\hat w_i\,\hat d_{ni})^{-\theta}}{\sum_k \pi_{nk}\,(\hat w_k\,"
                    r"\hat d_{nk})^{-\theta}}", font_size=40),
            MathTex(r"\hat w_i\,Y_i = \sum_n \pi_{ni}\,\hat\pi_{ni}\,(\hat w_n Y_n + D_n)", font_size=40),
            label(r"hats: \ ratios of new to old; \ $\pi$: \ today's trade shares; \ $D$: \ deficits, \ held fixed",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(LEFT * 1.5 + UP * 0.2)
        small = VGroup(dek[0].copy(), dek[1].copy()).arrange(RIGHT, buff=0.6).scale(0.6).to_edge(UP, buff=0.25)
        with self.voiceover(
            "The same models answer what-if questions. Robert Dekle, Jonathan Eaton and Samuel Kortum showed in 2008 "
            "that a counterfactual needs only today's trade shares and the elasticity, solved in proportional "
            "changes: exact hat algebra. <bookmark mark='a'/> Suppose trade costs between America and China rose "
            f"by {100 * (H['rise'] - 1):.0f} percent, about the size of a broad tariff. Solving for the new wages "
            "and prices in all sixteen regions of the 2019 data: <bookmark mark='b'/> America's spending on "
            f"Chinese goods falls from {100 * H['us_china_share_before']:.1f} percent to "
            f"{100 * H['us_china_share_after']:.1f}. <bookmark mark='c'/> America loses "
            f"{abs(100 * H['welfare'][u]):.2f} percent of real income and China {abs(100 * H['welfare'][c]):.2f}; "
            "Mexico and Canada gain, as trade diverts to them. <bookmark mark='d'/> The numbers are small "
            "because the model is static and has no inputs crossing borders; Part sixty-six returns with richer "
            "versions."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(dek[0]))
            self.play(FadeIn(dek[1]), FadeIn(dek[2]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(dek[2]), ReplacementTransform(VGroup(dek[0], dek[1]), small), FadeIn(ax), FadeIn(zero),
                      FadeIn(nms))
            self.play(LaggedStart(*[GrowFromEdge(b, UP if H["welfare"][i] < 0 else DOWN) for b, i in zip(bars, idx)],
                                  lag_ratio=0.12), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
