from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, PART, REAL, TAIL, day_text, load, real_data, sci


class Hook(VoiceoverScene):
    def construct(self):
        g = load("game")
        self.title_card()
        panels = self.game(g)
        self.reveal(g, panels)
        self.objectives()
        self.house()

    # ------------------------------------------------------------------
    def title_card(self):
        card = part_title(PART, r"Which one is real?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part one. The fair game. A price moves every day, and every day millions of people try to guess where "
            "it goes next. For more than a century the best description of those moves has been a game of pure "
            "chance, a coin tossed again and again. This part asks how good that description is, measured on "
            "ninety-four years of the American stock market and on Bitcoin, and what it means for anyone who "
            "hopes to win."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    # ------------------------------------------------------------------
    def _panel(self, levels, rets, name, lo, hi, rlim):
        n = len(rets)
        top = axes([0, n], [lo, hi], x_length=5.6, y_length=1.75, yticks=[100, 120], font_size=16)
        ax = top.ax
        line = curve(ax, np.arange(n + 1), levels, WHITE, stroke_width=2.2)
        tag = label(name, font_size=30, color=QC.IDEA).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
        bot = axes([0, n], [-rlim, rlim], x_length=5.6, y_length=0.95, font_size=14)
        bot.next_to(top, DOWN, buff=0.12).align_to(top, LEFT)
        bx = bot.ax
        strip = VGroup()
        w = bx.x_length / n
        for i, v in enumerate(rets):
            y0, y1 = bx.c2p(i, 0)[1], bx.c2p(i, float(np.clip(v, -rlim, rlim)))[1]
            strip.add(Line([bx.c2p(i + 0.5, 0)[0], y0, 0], [bx.c2p(i + 0.5, 0)[0], y1, 0], stroke_width=max(w * 40, 1.2),
                           color=GREY_B))
        return VGroup(top, line, tag), VGroup(bot, strip)

    def game(self, g):
        L, R = g["levels"], g["returns"]
        lo = float(np.floor(L.min() / 10) * 10) - 5
        hi = float(np.ceil(L.max() / 10) * 10) + 5
        rlim = 0.07
        names = ["A", "B", "C", "D"]
        tops, bots = VGroup(), VGroup()
        for i in range(4):
            t, b = self._panel(L[i], R[i], names[i], lo, hi, rlim)
            tops.add(t)
            bots.add(b)
        cells = VGroup(*[VGroup(t, b) for t, b in zip(tops, bots)])
        cells.arrange_in_grid(2, 2, buff=(0.7, 0.45)).move_to(DOWN * 0.15)
        start = MathTex(r"100", font_size=18, color=GREY_B)
        q = label(r"Three are coin flips. One is the US stock market. Which?", font_size=30)
        q.to_edge(UP, buff=0.18)
        with self.voiceover(
            "Here is a game. Four charts, each one year of a price, each starting at a hundred. Three of them are a "
            "computer tossing coins: every day it draws a random return from a bell curve with the same average and "
            "the same spread as the real thing, and adds it on. One of them is the American stock market, in a real "
            "year. <bookmark mark='a'/> Which one is real? Take a moment. They wander, they trend, they reverse, "
            "they look like charts that people draw lines on and tell stories about. <bookmark mark='b'/> If you "
            "can't tell, you're in good company: in 1953 the statistician Maurice Kendall showed price charts to "
            "economists, who could not tell them from chance either."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t[0]) for t in tops], lag_ratio=0.15), FadeIn(q))
            self.play(LaggedStart(*[Create(t[1]) for t in tops], lag_ratio=0.2, run_time=6), *[FadeIn(t[2]) for t in tops])
            vo.wait_until("a")
            boxes = VGroup(*[SurroundingRectangle(t, buff=0.08, color=QC.IDEA, stroke_width=2, corner_radius=0.08)
                             for t in tops])
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3, run_time=3))
            self.play(FadeOut(boxes))
            vo.wait_until("b")
        self.q = q
        return tops, bots

    def reveal(self, g, panels):
        tops, bots = panels
        ri = g["real_index"]
        with self.voiceover(
            "Now look underneath each chart, at the daily returns: how much the price moved each day. "
            "<bookmark mark='a'/> Three of the strips are steady static, every day the same kind of day. One has "
            "a spike. <bookmark mark='b'/> Chart C is the market in 1997, and the spike is the 27th of October, "
            f"when the market fell {abs(100 * g['worst']):.1f} percent, as Asia's currency crisis reached Wall "
            f"Street. Measured against that year's own volatility, it was a move of {abs(g['worst_z']):.1f} standard "
            "deviations. If daily returns really came from a bell curve, a day like that would come about once "
            f"every {g['worst_gauss_years'] / 1e6:.0f} million years. <bookmark mark='c'/> So the coin-flip picture "
            "is good enough to fool the eye, and wrong in the place that matters most: the extremes. This part "
            "measures exactly where the fair game holds, and where it breaks."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b[0]) for b in bots], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b[1], lag_ratio=0.0) for b in bots], lag_ratio=0.25, run_time=4))
            vo.wait_until("b")
            others = VGroup(*[VGroup(tops[i], bots[i]) for i in range(4) if i != ri])
            real = VGroup(tops[ri], bots[ri])
            spike_i = int(np.argmin(g["returns"][ri]))
            bx = bots[ri][0].ax
            spike = bots[ri][1][spike_i]
            ring = Circle(radius=0.22, color=TAIL, stroke_width=3).move_to(spike.get_bottom())
            bgc = self.camera.background_color
            veils = VGroup(*[Rectangle(width=o.width + 0.2, height=o.height + 0.2, stroke_width=0, fill_color=bgc,
                                       fill_opacity=0.78).move_to(o) for o in others])
            self.play(FadeIn(veils), bots[ri][1].animate.set_color(REAL), tops[ri][1].animate.set_color(REAL))
            self.play(spike.animate.set_color(TAIL), Create(ring))
            info = VGroup(
                label(rf"C: the US market, {g['year']}", font_size=26, color=REAL),
                label(day_text(g["worst_date"]) + rf": ${100 * g['worst']:.1f}\%$", font_size=24, color=TAIL),
                MathTex(rf"{abs(g['worst_z']):.1f}\,\sigma", font_size=40, color=TAIL),
                label(rf"a bell curve: once in ${sci(g['worst_gauss_years'])}$ years", font_size=22, color=GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            bg = BackgroundRectangle(info, buff=0.2, fill_opacity=0.92, color="#0b0f17")
            panel = VGroup(bg, info)
            panel.next_to(real, RIGHT if ri % 2 == 0 else LEFT, buff=0.15)
            if panel.get_right()[0] > 7.0:
                panel.shift((6.9 - panel.get_right()[0]) * RIGHT)
            self.play(FadeIn(panel, shift=LEFT * 0.2))
            src = real_data(r"US market: Ken French's daily value-weighted returns; the others: Gaussian, same mean and "
                            r"volatility", corner=DR)
            self.play(FadeIn(src))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def objectives(self):
        card = objectives_card([
            r"Returns and their arithmetic: log returns, the geometric mean, and the drag that volatility puts on growth",
            r"The random walk and the martingale: Samuelson's proof that well-anticipated prices are unpredictable",
            r"Test it: Lo and MacKinlay's variance ratio, replicated, then followed for 35 more years",
            r"Measure the stylized facts: heavy tails and the cubic law, volatility clustering, the leverage effect",
            r"Efficient markets, and why in-sample predictability can fool you; two worlds, $\mathbb P$ and $\mathbb Q$",
            r"Who trades, who wins, and the first rule of the House: point in time, and a sealed envelope",
        ], color=QC.IDEA)
        with self.voiceover(
            "Here is the plan. The arithmetic of returns, and the drag that volatility puts on growth. The random "
            "walk, and Samuelson's proof that well-anticipated prices must be unpredictable. A real test of it, "
            "replicated and then followed for thirty-five more years. The stylized facts, each one measured. "
            "Efficient markets, and a modern result on how in-sample tests can fool you. The two worlds of finance, "
            "the real one and the risk-neutral one. And who is on the other side of every trade."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "And this is the House: the quant firm this series builds, one part at a time. Every desk you see will "
            "be written, tested and used to trade, price or hedge. Today it is an empty building with one desk "
            "being set up. <bookmark mark='a'/> Data and technology: before anyone trades, someone has to decide "
            "what the firm is allowed to know, and when. That desk's first rule comes at the end of this part."
        ) as vo:
            self.play(FadeIn(chart.title), LaggedStart(*[FadeIn(r) for r in chart.rows], lag_ratio=0.3, run_time=3),
                      FadeIn(chart.flows))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
