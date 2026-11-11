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
        self.tools(load("apc"))
        self.backtest(load("imbacktest"))

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
        self.wait(0.4)
        self.clear_scene()

    def tools(self, a):
        t = np.asarray(a["t"])
        g = axes([2017, 2026], [0, 8], x_length=8.0, y_length=4.4, xlabel=r"year",
                 ylabel=r"margin per \$100 of 10-year notes, \$", xticks=[2017, 2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6, 8],
                 font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"ewma": BAD, "buffer": QC.IMPLIED, "floor": IM_C}
        lines = {k: curve(ax, t, np.asarray(a[k]), c_, stroke_width=2.4) for k, c_ in cols.items()}
        j, cl = a["jump"], a["calm_level"]
        side = VGroup(
            legend([(BAD, r"EWMA alone"), (QC.IMPLIED, r"with a 25\% buffer, released in stress"),
                    (IM_C, r"floored at a 10-year look-back")], font_size=16),
            *[MathTex(rf"\times {j[k]:.1f}\ \text{{in March 2020; calm level}}\ \${cl[k]:.2f}", font_size=21, color=c_)
              for k, c_ in cols.items()],
            wrapped_label(r"the tools Europe's clearing rules (EMIR) require of CCPs: a buffer of at least 25\% that can be "
                          r"drawn down in stress, or a floor from a ten-year window. Smaller jumps, paid for with more "
                          r"margin every calm day", 3.8, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.25)
        fit_right(side, 6.85)
        with self.voiceover(
            "Europe's clearing rules make the remedies concrete. A clearing house must use one of a few "
            "anti-procyclicality tools. <bookmark mark='a'/> The responsive model alone jumped "
            f"{j['ewma']:.1f} times in March 2020. <bookmark mark='b'/> A buffer of twenty-five percent, collected in calm "
            f"times and released in a stress, makes the jump {j['buffer']:.1f} times. <bookmark mark='c'/> A floor at the "
            f"level of a ten-year look-back makes it {j['floor']:.1f} times. <bookmark mark='d'/> The price is paid "
            f"every quiet day: before the crisis, the floored margin was {cl['floor']:.2f} dollars against "
            f"{cl['ewma']:.2f}, about {100 * (cl['floor'] / cl['ewma'] - 1):.0f} percent more. Stability is bought with "
            "collateral that sits idle in good times."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines["ewma"]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["buffer"]), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines["floor"]), FadeIn(side[3]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def backtest(self, b):
        rows = [cmath(r"\text{LR}", r"=", r"-2\ln\frac{(1-p)^{n-x}p^{x}}{(1-\hat p)^{n-x}\hat p^{x}} \sim \chi^2_1",
                      font_size=36, colors={r"\text{LR}": IM_C})]
        whys = [why(f"Kupiec's test: with $p$ = 1\\%, $n$ = {b['n']:,} days and $x$ = {b['exceptions']} exceptions, $\\hat p$ = {100 * b['rate']:.2f}\\%, LR = {b['lr']:.2f}, p-value {b['pval']:.2f}: iid reference only; overlapping windows"
                    .replace(",", "{,}", 1))]
        step = ladder(self, rows, whys, keep=1, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        yrs = sorted(b["by_year"], key=int)
        vals = [100 * b["by_year"][y] for y in yrs]
        g = axes([-0.6, len(yrs) - 0.4], [0, 6], x_length=7.6, y_length=2.6, xlabel=r"", ylabel=r"exceptions, \%",
                 xticks=[], yticks=[0, 1, 3, 5], font_size=13).to_edge(DOWN, buff=0.6).shift(LEFT * 1.4)
        ax = g.ax
        one = DashedLine(ax.c2p(-0.6, 1), ax.c2p(len(yrs) - 0.4, 1), color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for i, (y, v_) in enumerate(zip(yrs, vals)):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v_)[1]
            bars.add(VGroup(Rectangle(width=0.5, height=max(y1 - y0, 0.01), stroke_width=0,
                                      fill_color=BAD if v_ > 2 else IM_C, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), label(str(y), font_size=15).next_to(ax.c2p(i, 0), DOWN, buff=0.1)))
        side = wrapped_label('Descriptive two-sided 10-day exceedances overlap and are dependent. The iid Kupiec p-value is only a diagnostic, not coverage certification; year-level clustering is descriptive', 3.4, 17, GREY_A).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.6)
        with self.voiceover(
            f"This is a historical diagnostic of absolute ten-day yield moves, with a two-sided normal threshold of two point five seven six standard deviations, rather than the earlier one-sided margin rule. <bookmark mark='a'/> There are {b['exceptions']} exceptions in {b['n']:,} overlapping windows, {100 * b['rate']:.2f} percent. The reported iid Kupiec reference p-value is {b['pval']:.2f}. <bookmark mark='b'/> Overlap creates dependence even under independent daily moves, so that p-value cannot certify coverage. Year-level rates reveal concentration of exceptions; formal testing needs a method accounting for overlap and model estimation. This is not a full margin-system backtest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(one))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.15), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a margin model with a 10-year look-back barely moved in March 2020. Why might a regulator still "
                r"dislike it?")
        with self.voiceover("A margin model with a ten-year look-back barely moved in March 2020. Why might a regulator "
                            "still dislike it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
