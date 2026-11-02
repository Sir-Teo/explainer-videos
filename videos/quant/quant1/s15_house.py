from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, PART, REAL, load


class House(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.desk()
        self.rule()
        self.envelope(e)
        self.counter(e)

    def card(self):
        c = chapter_card(14, r"The House opens", r"What is the firm allowed to know, and when?", part=PART)
        with self.voiceover("Chapter fourteen. The House opens."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def desk(self):
        chart = house_chart(PART, lit=("data",)).scale(0.8).to_edge(UP, buff=0.3)
        items = VGroup(
            label(r"the data layer: every dataset fetched from a free public source, piece by piece, resumable", font_size=23),
            label(r"each piece's SHA-256 recorded on first fetch and checked on every later one", font_size=23),
            label(r"so every render, on any machine, sees the same numbers", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(chart, DOWN, buff=0.45)
        if items.width > 13.0:
            items.scale_to_fit_width(13.0)
        with self.voiceover(
            "The House now has its first desk: data and technology. Everything this part measured came through it. "
            "Each dataset is fetched from a free public source, piece by piece, so an interrupted download resumes "
            "where it stopped. <bookmark mark='a'/> The fingerprint of every piece is recorded the first time it "
            "arrives, and checked every time after, so if a source quietly revises its history, the House notices, "
            "and every render of this series, on any machine, sees the same numbers."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.04))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    def rule(self):
        r1 = theorem_card(r"Rule 1: point in time", r"A number used at time $t$ may depend only on data stamped at or "
                          r"before $t$, as it was known then. No revised figures, no survivors-only lists, no "
                          r"tomorrow's close.", width=11.0, font_size=26, kind=r"The House").to_edge(UP, buff=0.6)
        why_ = VGroup(
            label(r"chapter 4: an echo in stale prices is not a profit", font_size=24, color=GREY_A),
            label(r"chapter 9: in-sample predictability appears even in efficient markets", font_size=24, color=GREY_A),
            label(r"Part 26: every backtest that looked too good, and why", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(r1, DOWN, buff=0.6)
        with self.voiceover(
            "The desk's first rule is the most important rule in quantitative finance, and the one most often "
            "broken by accident. Point in time: a number used at a moment may depend only on what was known at that "
            "moment, as it was known then. Not the revised figure, not today's list of companies that survived, "
            "not tomorrow's closing price. <bookmark mark='a'/> This part has already shown why. An echo in stale "
            "prices that no one could have traded on. Predictability that appears in hindsight even in a market "
            "that is efficient by construction. Part twenty-six is a museum of backtests that broke this rule."
        ) as vo:
            self.play(FadeIn(r1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w) for w in why_], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    def envelope(self, e):
        y0, y1, ys = 1926, 2026, 2021
        W = 11.6
        bar = VGroup()
        x = lambda yr: -W / 2 + W * (yr - y0) / (y1 - y0)
        res = Rectangle(width=x(ys) - x(y0), height=0.8, stroke_width=0, fill_color=REAL, fill_opacity=0.55)
        res.move_to([(x(y0) + x(ys)) / 2, 1.9, 0])
        hold = Rectangle(width=x(y1) - x(ys), height=0.8, stroke_color=QC.HOUSE, stroke_width=3, fill_color=GREY_D,
                         fill_opacity=0.9).move_to([(x(ys) + x(y1)) / 2, 1.9, 0])
        lr = label(r"research: 1926 to 31 December 2020", font_size=24).move_to(res)
        lh = label(r"sealed: 2021--2025", font_size=22, color=QC.HOUSE).next_to(hold, UP, buff=0.12).align_to(hold, RIGHT)
        ticks = VGroup(*[label(str(yr), font_size=18, color=GREY_B).next_to([x(yr), 1.5, 0], DOWN, buff=0.05)
                         for yr in (1926, 1950, 1975, 2000, 2021)])
        bar.add(res, hold, lr, lh, ticks)
        rows = VGroup()
        for name, rec in e["records"].items():
            rows.add(VGroup(label(name, font_size=22, color=GREY_A),
                            label(rf"{rec['first'] // 10000}--{rec['last'] // 10000}, {rec['n']:,} days".replace(",", "{,}"),
                                  font_size=22),
                            data_text(rec["digest"][:24] + "...", font_size=18, color=QC.HOUSE)))
        cells = VGroup(*[c for r_ in rows for c in r_]).arrange_in_grid(len(rows), 3, buff=(0.5, 0.25),
                                                                        col_alignments="lll")
        cells.next_to(bar, DOWN, buff=0.7)
        if cells.width > 13.2:
            cells.scale_to_fit_width(13.2)
        rule2 = wrapped_label(r"Rule 2: a strategy is registered first (the hash of its code, its parameters, the "
                              r"number of things tried), then the envelope is opened for it, once. Whatever it says is "
                              r"shown.", 12.4, 23, WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The second rule is a sealed envelope. Every statistic of stocks and Bitcoin in this part used data up "
            "to the last day of 2020, and so will every piece of research in this series. <bookmark mark='a'/> The "
            "five years since, 2021 to 2025, are sealed. Their fingerprints were recorded today, so no one, "
            "including the author, can quietly look and adjust. <bookmark mark='b'/> When a strategy is ready, in "
            "Parts twenty-four to forty-three, it is registered first: the fingerprint of its code, its "
            "parameters, and how many things were tried to find it. Then the envelope is opened for it, once, and "
            "the result is shown, whatever it is."
        ) as vo:
            self.play(FadeIn(res), FadeIn(lr), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(hold), FadeIn(lh))
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule2))
        self.wait(0.3)
        self.clear_scene()

    def counter(self, e):
        big = MathTex(str(e["trials"]), font_size=160, color=QC.HOUSE)
        cap = label(r"the trial counter: configurations tried so far, across the whole series", font_size=28,
                    color=GREY_A)
        grp = VGroup(big, cap).arrange(DOWN, buff=0.3).shift(UP * 0.8)
        nxt = wrapped_label(r"Part 26 explains why the count matters: the more things you try, the higher the bar a "
                            r"result must clear. The finale deflates every result by it.", 11.0, 24, WHITE)
        nxt.next_to(grp, DOWN, buff=0.6)
        surf = note(r"also frozen: the Surface, Deribit's BTC options on 10--11 December 2025 (Parts 10--17)",
                    font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And the third device: a counter. Every backtest in this series declares how many configurations it "
            "tried, in code, so the count can be regenerated. Today it reads zero. <bookmark mark='a'/> Part "
            "twenty-six explains why it matters: the more things you try, the higher the bar a result must clear "
            "before you believe it. By the finale the counter will be large, and every result will be judged "
            "against it."
        ) as vo:
            self.play(FadeIn(big, scale=1.3), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(nxt), FadeIn(surf))
        self.wait(0.4)
        self.clear_scene()
