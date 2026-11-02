from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, LOSS, PART, TRADE, load, ro

MARKETS = [
    (r"United States", r"the largest stock market; T+1 since May 2024; most retail orders filled by wholesalers; many "
                       r"exchanges and dark pools, wired together by Reg NMS (Parts 35--38)", TRADE),
    (r"Europe and the UK", r"many national exchanges and venues under MiFID II; T+1 on 11 October 2027 (EU regulation "
                           r"of October 2025; the UK confirmed the same date in February 2025)", CASH),
    (r"Japan", r"the Tokyo Stock Exchange; the yen is the world's funding currency, which is why its carry trade "
               r"matters (Part 22)", QC.IDEA),
    (r"India", r"NSE has been the world's largest derivatives exchange by contracts since 2019. SEBI: 93\% of "
               r"individual F\&O traders lost money in FY22--24 (over Rs\,1.8 lakh crore); 91\% in FY25 (Rs\,1,05,603 "
               r"crore, July 2025 study). From 20 November 2024: bigger contracts (at least Rs\,15 lakh) and one weekly "
               r"expiry per exchange", QC.GAMMA),
    (r"China (A-shares)", r"shares bought today can be sold only tomorrow (T+1); daily limits of $\pm$10\% on the main "
                          r"boards and $\pm$20\% on STAR and ChiNext; Stock Connect from Hong Kong. July 2024: "
                          r"securities refinancing for short sales suspended; exchange rules treat 300 orders a second "
                          r"or 20,000 a day from one account as high-frequency (as reported)", LOSS),
]


class World(VoiceoverScene):
    def construct(self):
        lm = load("limits")
        self.card()
        self.markets()
        self.spring(lm)
        self.measure(lm)

    def card(self):
        c = chapter_card(16, r"Markets around the world", r"Does the machine work the same everywhere?",
                         lit=(2015,), part=PART)
        with self.voiceover("Chapter sixteen. Markets around the world."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def markets(self):
        rows = VGroup()
        for name, what, col in MARKETS:
            rows.add(VGroup(label(name, font_size=24, color=col), wrapped_label(what, 9.6, 19, WHITE))
                     .arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(ORIGIN)
        names_w = max(r_[0].width for r_ in rows)
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.4 + names_w - r_[0].width).align_to(r_[0], UP)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.9:
            rows.scale_to_fit_height(6.9)
        rows.move_to(ORIGIN)
        src = note(r"FCA; EU T+1 regulation (2025); FIA volume reports; SEBI studies (September 2024, July 2025) and "
                   r"circular (October 2024); CSRC (July 2024)", font_size=15).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "The machine is built differently in each country, and the differences matter. The United States settles in a "
            "day, routes most retail orders to wholesalers, and splits trading across many venues. <bookmark mark='a'/> "
            "Europe and Britain move to one-day settlement together on the eleventh of October 2027. <bookmark mark='b'/> "
            "Japan's yen is the currency the world borrows in, which is why its carry trade, Part twenty-two, matters "
            "everywhere. <bookmark mark='c'/> India's National Stock Exchange has been the world's largest derivatives "
            "exchange by contracts since 2019, much of it weekly index options bought by individuals. Its regulator found "
            "ninety-three percent of them lost money over three years, and ninety-one percent in the year to March 2025, then "
            "made contracts bigger and cut weekly expiries to one per exchange. <bookmark mark='d'/> In China a share bought "
            "today can't be sold until tomorrow, prices may move at most ten percent a day, twenty on STAR and ChiNext, and "
            "in 2024 the regulator suspended lending shares for short sales and set rules for high-frequency trading."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(src))
            for i, mk in enumerate("abcd", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i], shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def spring(self, lm):
        tp = np.asarray(lm["true_path"], float)
        op = np.asarray(lm["obs_path"], float)
        n = len(tp)
        g = axes([0, n - 1], [-0.1, 0.45], x_length=8.0, y_length=4.4, xlabel=r"trading days",
                 ylabel=r"cumulative log return", yticks=[0, 0.2, 0.4], font_size=17).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        k = ValueTracker(0)
        lt = tracing(ax, np.arange(n), tp, k, GREY_B, stroke_width=2.5)
        lo = tracing(ax, np.arange(n), op, k, LOSS, stroke_width=3.5)

        def spring_m():
            i = at_index(np.arange(n), k)
            a, b = ax.c2p(i, at_index(op, k)), ax.c2p(i, at_index(tp, k))
            if abs(a[1] - b[1]) < 0.05:
                return VGroup(Dot(a, radius=0.07, color=LOSS))
            pts = [a + (b - a) * s + RIGHT * 0.08 * np.sin(14 * np.pi * s) for s in np.linspace(0, 1, 40)]
            return VGroup(VMobject(color=QC.IDEA, stroke_width=2.5).set_points_smoothly(pts),
                          Dot(a, radius=0.07, color=LOSS), Dot(b, radius=0.07, color=GREY_B))
        sp = always_redraw(spring_m)
        rows = [
            MathTex(r"r^o_t = \operatorname{clip}(r_t + c_{t-1},\ \pm L)", font_size=32),
            MathTex(r"c_t = r_t + c_{t-1} - r^o_t", font_size=32),
            MathTex(r"\Rightarrow\ \operatorname{Cov}(r^o_t, r^o_{t+1}) > 0", font_size=32, color=QC.IDEA),
        ]
        whys = [why(r"the observed move is capped at the limit $L$", font_size=19),
                why(r"the part that couldn't trade rolls into tomorrow", font_size=19),
                why(r"so a limit day is followed by more of the same", font_size=19)]
        stack = VGroup(*[VGroup(r_, w).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for r_, w in zip(rows, whys)])
        stack.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        for s in stack:
            if s.width > 4.8:
                s.scale_to_fit_width(4.8)
        stack.to_edge(RIGHT, buff=0.3)
        leg = legend([(GREY_B, r"the price the news says"), (LOSS, r"the price that trades ($\pm$10\% a day)")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        with self.voiceover(
            "Price limits change Part one's statistics. A stock hit by big news twice in forty days: grey where the news says "
            "the price should be, red the price that can trade, capped at ten percent a day, a spring between them. "
            "<bookmark mark='a'/> On a limit day the true price runs ahead; next day the spring drags the traded price after "
            "it. <bookmark mark='b'/> The observed return is the true one plus yesterday's remainder, clipped; what's clipped "
            "rolls over, so a limit day predicts more of the same."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.add(lt, lo, sp)
            vo.wait_until("a")
            self.play(k.animate.set_value(n - 1), run_time=8, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in stack], lag_ratio=0.4))
        for m in (lt, lo, sp):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def measure(self, lm):
        res = lm["res"]
        bars = VGroup()
        g = axes([-0.5, 2.5], [0, 0.16], x_length=5.0, y_length=3.6, ylabel=r"lag-1 autocorrelation, observed",
                 yticks=[0, 0.05, 0.1, 0.15], font_size=16).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ax = g.ax
        items = [(r"no limit", float(np.mean(res["0.10"]["ac1_true"])), GREY_B, None),
                 (r"$\pm$20\%", float(np.mean(res["0.20"]["ac1"])), QC.IDEA, res["0.20"]["ac1"]),
                 (r"$\pm$10\%", float(np.mean(res["0.10"]["ac1"])), LOSS, res["0.10"]["ac1"])]
        for i, (name, v, col, seeds) in enumerate(items):
            h = max(ax.c2p(0, max(v, 0))[1] - ax.c2p(0, 0)[1], 0.01)
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(ax.c2p(i, 0),
                                                                                                         aligned_edge=DOWN)
            grp = VGroup(b, label(name, font_size=19, color=col).next_to(ax.c2p(i, 0), DOWN, buff=0.15))
            if seeds is not None:
                grp.add(*[Dot(ax.c2p(i + 0.25 * (j / 7 - 0.5), s), radius=0.035, color=WHITE) for j, s in enumerate(seeds)])
            bars.add(grp)
        txt = VGroup(
            MathTex(rf"\pm 10\%:\ \text{{AC1}} = {np.mean(res['0.10']['ac1']):.2f},\ \text{{at the limit on}}\ "
                    rf"{100 * np.mean(res['0.10']['at_limit']):.1f}\%\ \text{{of days}}", font_size=26, color=LOSS),
            MathTex(rf"\pm 20\%:\ \text{{AC1}} = {np.mean(res['0.20']['ac1']):.2f},\ "
                    rf"{100 * np.mean(res['0.20']['at_limit']):.1f}\%\ \text{{of days}}", font_size=26, color=QC.IDEA),
            label(r"a signal no one could trade: at the limit, the queue doesn't clear", font_size=21, color=GREY_A),
            label(r"the House's data desk stores each market's rules beside its prices", font_size=21, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        q = desk_question(r"A stock closes limit-up with buyers queued. What is tomorrow's expected return, and can you "
                          r"trade it?", width=6.0, font_size=19).to_corner(DR, buff=0.3)
        src = note(r"simulated: daily vol 3\%, jumps on 5\% of days (12\% s.d.), 5,000 days, 8 seeds", font_size=15)
        src.to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "Measure it: five thousand simulated days, eight seeds, no limit, twenty and ten percent. <bookmark mark='a'/> "
            f"Without limits, no autocorrelation; with ten percent limits, {np.mean(res['0.10']['ac1']):.2f}, from a stock at "
            f"its limit on only {100 * np.mean(res['0.10']['at_limit']):.0f} percent of days. A backtest sees momentum, but at "
            "limit-up the buy queue doesn't clear. <bookmark mark='b'/> So the House stores each market's rules beside its "
            "prices. Predict: limit-up close, buyers queued. Tomorrow's return, and can you trade it?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.4))
            self.play(FadeIn(txt[:3]))
            vo.wait_until("b")
            self.play(FadeIn(txt[3]), FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
