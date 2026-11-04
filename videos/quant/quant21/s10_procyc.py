from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, IM_C, PART, ask, fit_right, illustration, load


class Procyc(VoiceoverScene):
    def construct(self):
        p = load("procyc")
        self.card()
        self.chart(p)
        self.loop()

    def card(self):
        c = chapter_card(9, r"Margin procyclicality", r"Why does margin rise exactly when cash is scarce?", lit=(2020,),
                         part=PART)
        with self.voiceover("Chapter nine. Procyclicality: why margin calls arrive exactly when cash is scarcest."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def chart(self, p):
        t, h, e = np.asarray(p["t"]), np.asarray(p["hist"]), np.asarray(p["ewma"])
        g = axes([2017, 2026], [0, 8], x_length=8.4, y_length=4.4, xlabel=r"year",
                 ylabel=r"margin per \$100 of 10-year notes, \$", xticks=[2017, 2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6, 8],
                 font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lh = curve(ax, t, h, IM_C, stroke_width=2.6)
        le = curve(ax, t, e, BAD, stroke_width=2.6)
        side = VGroup(
            legend([(IM_C, r"99\% of the last year's moves"), (BAD, r"EWMA volatility ($\lambda$ = 0.97)")], font_size=17),
            MathTex(rf"\text{{early 2020}}: \${p['pre']['ewma']:.2f}", font_size=24),
            MathTex(rf"\text{{March 2020}}: \${p['peak2020']['ewma']:.2f}\ (\times {p['peak2020']['ewma'] / p['pre']['ewma']:.1f})",
                    font_size=24, color=BAD),
            wrapped_label(r"a 10-day, 99\% margin on a 10-year Treasury position, from the daily moves in its yield. "
                          r"The responsive model doubled in weeks; the one-year window rose more slowly and stayed high "
                          r"for a year", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Margin models scale with volatility. Here are two simple ones, computed from the daily moves of the "
            "ten-year Treasury yield since 2017: one uses the worst one percent of the last year's moves, the other "
            "an exponentially weighted volatility that reacts within days. <bookmark mark='a'/> In March 2020 the "
            f"responsive model's margin rose from {p['pre']['ewma']:.1f} to {p['peak2020']['ewma']:.1f} dollars per "
            "hundred of notes in a few weeks. <bookmark mark='b'/> The slower model rose less, and then stayed high for "
            "a year after the danger had passed. Every holder of a margined position was asked for more cash at the "
            "same moment, and the fastest way to raise cash was to sell."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(le), FadeIn(side[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lh), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"FRED: DGS10, daily; DV01 of a 10-year note about \$0.085 per \$100 per bp"))
        self.wait(0.4)
        self.clear_scene()

    def loop(self):
        steps = [r"volatility rises", r"margin models ask for more", r"holders sell assets to raise cash",
                 r"prices fall, volatility rises further"]
        nodes = VGroup(*[RoundedRectangle(corner_radius=0.15, width=4.2, height=0.9, stroke_color=BAD, stroke_width=2,
                                          fill_opacity=0) for _ in steps])
        pos = [UP * 1.6, RIGHT * 3.4, DOWN * 1.6, LEFT * 3.4]
        for n_, p_, s_ in zip(nodes, pos, steps):
            n_.move_to(p_ + UP * 0.2)
            n_.add(wrapped_label(s_, 3.8, 19).move_to(n_))
        arrows = VGroup(*[CurvedArrow(nodes[i].get_center() + (pos[(i + 1) % 4] - pos[i]) * 0.28,
                                      nodes[(i + 1) % 4].get_center() - (pos[(i + 1) % 4] - pos[i]) * 0.28,
                                      angle=-PI / 4, color=GREY_B, stroke_width=3) for i in range(4)])
        foot = wrapped_label(r"the same loop drove Part 18's LDI spiral in September 2022. Remedies in use: margin floors "
                             r"and buffers in calm times, longer look-back windows that include stress, and more "
                             r"transparent, predictable calls", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "That is a loop. <bookmark mark='a'/> Volatility rises, so margin models ask for more; "
            "<bookmark mark='b'/> holders sell to raise the cash, <bookmark mark='c'/> prices fall further, and "
            "volatility rises again. It drove the gilt crisis of Part eighteen as well. <bookmark mark='d'/> The "
            "remedies trade efficiency in calm times for stability in storms: margin floors and buffers built up "
            "when markets are quiet, and look-back windows long enough to remember the last crisis."
        ) as vo:
            self.play(FadeIn(nodes[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(arrows[i]), FadeIn(nodes[i + 1]))
            self.play(Create(arrows[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        q = ask(r"a margin model with a 10-year look-back barely moved in March 2020. Why might a regulator still "
                r"dislike it?")
        with self.voiceover("A margin model with a ten-year look-back barely moved in March 2020. Why might a regulator "
                            "still dislike it?"):
            self.play(FadeOut(foot), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
