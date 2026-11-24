from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

SIMON, EHRLICH = "#7EC8F5", STATE


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "Who was right about scarcity: the biologist or the economist?",
             "Chapter fourteen. Called it?", lit=("change",))
        self.bet()
        self.windows()
        self.ours()

    def bet(self):
        B = R["bet"]
        metals = B["metals"]
        cols = [STONE, COPPER, "#7EC8F5", "#C9D3E0", "#9C6B9E"]
        stacks = VGroup()
        ends = VGroup()
        labs = VGroup()
        for k, (m, c) in enumerate(zip(metals, cols)):
            x = -4.6 + 1.25 * k
            s0 = Rectangle(width=0.8, height=2.0, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [x, -1.2, 0], aligned_edge=DOWN)
            h1 = 2.0 * (1 + B["change"][m])
            s1 = Rectangle(width=0.8, height=h1, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [x, -1.2, 0], aligned_edge=DOWN)
            stacks.add(s0)
            ends.add(s1)
            labs.add(VGroup(tx(m, 16, WHITE, bold=True).next_to(s0, DOWN, buff=0.12),
                            tx(f"{100 * B['change'][m]:+.0f}%", 15, EHRLICH if B["change"][m] > 0 else SIMON,
                               bold=True).next_to(s0, DOWN, buff=0.45)))
        t1 = tx("$200 of each, September 1980", 18, WHITE, bold=True).move_to([-2.1, 1.4, 0])
        t2 = tx("the same metals in 1990, after inflation", 18, WHITE, bold=True).move_to([-2.1, 1.4, 0])
        people = VGroup(
            VGroup(draw.person(0.9, EHRLICH), tx("Paul Ehrlich, biologist", 16, EHRLICH, bold=True),
                   tx("bet the metals would grow scarcer", 14, GREY_A), tx("and dearer", 14, GREY_A)).arrange(DOWN, buff=0.06),
            VGroup(draw.person(0.9, SIMON), tx("Julian Simon, economist", 16, SIMON, bold=True),
                   tx("bet that ingenuity would", 14, GREY_A), tx("make them cheaper", 14, GREY_A)).arrange(DOWN, buff=0.06)
        ).arrange(RIGHT, buff=0.6).move_to([3.9, 1.3, 0])
        cheque = VGroup(Rectangle(width=3.6, height=1.3, stroke_color=GREEN_C, stroke_width=2, fill_color="#14241A",
                                  fill_opacity=1),
                        VGroup(tx("Pay to Julian Simon", 15, WHITE), tx(f"${B['cheque']:.2f}", 26, GREEN_C, bold=True),
                               tx("October 1990", 13, GREY_A)).arrange(DOWN, buff=0.06)).move_to([3.9, -1.3, 0])
        cheque[1].move_to(cheque[0])
        redo = VGroup(tx("Our check, on the Survey's yearly prices:", 15, GREY_A),
                      tx(f"the $1,000 basket fell to about ${B['basket_real']:,.0f}", 16, WHITE, bold=True)).arrange(
            DOWN, buff=0.04).next_to(cheque, DOWN, buff=0.25)
        src = source("Paul Sabin, The Bet (Yale, 2013); US Geological Survey, Data Series 140 (unit values in 1998 dollars)",
                     size=13)
        with self.voiceover(
            "Part nine's forecast to test is the most famous bet in economics. <bookmark mark='a'/> In 1980 the "
            "biologist Paul Ehrlich, who had warned that a growing population would exhaust the Earth's resources, "
            "accepted a challenge from the economist Julian Simon, who believed that human ingenuity would always find "
            "more. <bookmark mark='b'/> On the twenty-ninth of September 1980 they agreed on a notional basket: two "
            "hundred dollars each of chromium, copper, nickel, tin and tungsten, chosen by Ehrlich and his colleagues. "
            "If the basket was worth more after inflation in 1990, Simon would pay the difference; if less, Ehrlich "
            "would. <bookmark mark='c'/> All five fell. Tin and tungsten lost more than two-thirds of their real value. "
            f"<bookmark mark='d'/> In October 1990 Ehrlich mailed Simon a cheque for {B['cheque']:.2f} dollars. Using "
            "the Geological Survey's yearly average prices, we get the same verdict: the thousand-dollar basket fell to "
            f"about {B['basket_real']:,.0f} dollars."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(people[0], shift=UP * 0.1))
            self.play(FadeIn(people[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(t1), LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in stacks], lag_ratio=0.15),
                      FadeIn(VGroup(*[l_[0] for l_ in labs])), run_time=1.8)
            vo.wait_until("c")
            self.play(ReplacementTransform(t1, t2), *[Transform(a, b) for a, b in zip(stacks, ends)],
                      FadeIn(VGroup(*[l_[1] for l_ in labs])), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(cheque, shift=UP * 0.15))
            self.play(FadeIn(redo))
        self.clear_scene()

    def windows(self):
        B = R["bet"]
        W = B["windows"]
        n = len(W)
        cols_ = 22
        cells = VGroup()
        for k, (y, ratio) in enumerate(W):
            c = Square(0.42, stroke_width=1, stroke_color=BACKGROUND, fill_color=EHRLICH if ratio > 1 else SIMON,
                       fill_opacity=0.9)
            cells.add(VGroup(c, tx(f"{y % 100:02d}", 10, BACKGROUND).move_to(c)))
        cells.arrange_in_grid(rows=int(np.ceil(n / cols_)), cols=cols_, buff=0.04).move_to([0, -0.2, 0])
        k80 = [y for y, _ in W].index(1980)
        ring = SurroundingRectangle(cells[k80], color=WHITE, buff=0.03, stroke_width=3)
        rl = tx("1980-1990: the real bet", 15, WHITE, bold=True).next_to(ring, DOWN, buff=0.12)
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=EHRLICH, fill_opacity=1),
                            tx(f"Ehrlich wins: the basket rose ({B['ehrlich']} windows)", 16, WHITE)).arrange(RIGHT,
                                                                                                             buff=0.12),
                     VGroup(Square(0.22, stroke_width=0, fill_color=SIMON, fill_opacity=1),
                            tx(f"Simon wins: the basket fell ({n - B['ehrlich']} windows)", 16, WHITE)).arrange(
                         RIGHT, buff=0.12)).arrange(RIGHT, buff=0.7).next_to(cells, DOWN, buff=0.7)
        head = tx(f"The same bet, for every ten-year window from {B['first']}-{B['first'] + 10} to "
                  f"{B['last']}-{B['last'] + 10}", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        sub = tx("each square is the window's first year", 15, GREY_A).next_to(head, DOWN, buff=0.12)
        big = tx(f"Ehrlich would have won {100 * B['ehrlich_share']:.0f}% of the time", 26, EHRLICH, bold=True
                 ).next_to(cells, UP, buff=0.35)
        src = source("computed: the Works (mine.py), US Geological Survey Data Series 140 real unit values", size=13)
        with self.voiceover(
            "Simon won. But was he right, or lucky? We can check, because the Geological Survey publishes a price for "
            "each of these metals for every year since 1900. <bookmark mark='a'/> So run the same bet, with the same "
            f"five metals, for every ten-year window: 1900 to 1910, 1901 to 1911, and so on, {n} windows in all. "
            "Red means the basket rose in real terms and Ehrlich would have won; blue means it fell and Simon would "
            "have won. <bookmark mark='b'/> Here is 1980, the real bet: blue. <bookmark mark='c'/> But over the whole "
            f"century, Ehrlich would have won {B['ehrlich']} of the {n} windows, {100 * B['ehrlich_share']:.0f} "
            "percent. Simon picked a decade in which metal prices fell. Over the long run, the honest answer is the one "
            "from the intermission: prices swing in long cycles around a level that barely moves, because each boom "
            "brings new mines and new methods. Neither man's theory beats the cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.02), run_time=4.0)
            self.play(FadeIn(key))
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(big, shift=DOWN * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["call"]
        E = R["esc"]
        lo, hi = C["fy26"]
        pa = viz.plot_axes([2023.4, 2028.6], [0, 1500], x_length=6.4, y_length=4.4, xticks=[2024, 2025, 2026, 2027, 2028],
                           yticks=[500, 1000, 1500], xfmt=lambda v: f"FY{int(v) % 100}", yfmt=lambda v: f"{v:,.0f} kt",
                           size=14).move_to([-3.0, -0.4, 0])
        bars = VGroup(
            Rectangle(width=0.55, height=pa.ax.c2p(0, get("esc.output.2024"))[1] - pa.ax.c2p(0, 0)[1], stroke_width=0, fill_color=COPPER,
                      fill_opacity=0.85).move_to(pa.ax.c2p(2024, 0), aligned_edge=DOWN),
            Rectangle(width=0.55, height=pa.ax.c2p(0, C["fy25"])[1] - pa.ax.c2p(0, 0)[1], stroke_width=0,
                      fill_color=COPPER, fill_opacity=0.85).move_to(pa.ax.c2p(2025, 0), aligned_edge=DOWN))
        rng26 = Rectangle(width=0.55, height=pa.ax.c2p(0, hi)[1] - pa.ax.c2p(0, lo)[1], stroke_color=COPPER,
                          stroke_width=2, fill_color=COPPER, fill_opacity=0.3).move_to(
            [pa.ax.c2p(2026, 0)[0], (pa.ax.c2p(0, lo)[1] + pa.ax.c2p(0, hi)[1]) / 2, 0])
        mlo, mhi = span("esc.medium")
        rngm = Rectangle(width=pa.ax.c2p(2028.4, 0)[0] - pa.ax.c2p(2026.6, 0)[0],
                         height=pa.ax.c2p(0, mhi)[1] - pa.ax.c2p(0, mlo)[1], stroke_color=GREY_A, stroke_width=1.5,
                         fill_color=GREY_A, fill_opacity=0.15).move_to(
            [(pa.ax.c2p(2026.6, 0)[0] + pa.ax.c2p(2028.4, 0)[0]) / 2, (pa.ax.c2p(0, mlo)[1] + pa.ax.c2p(0, mhi)[1]) / 2, 0])
        rml = tx("BHP's outlook, FY27-31", 13, GREY_A).next_to(rngm, UP, buff=0.06)
        thr = DashedLine(pa.ax.c2p(2023.4, C["threshold"]), pa.ax.c2p(2028.6, C["threshold"]), stroke_color=PRICE,
                         stroke_width=2.5)
        thl = tx(f"{C['threshold']:,} kt", 15, PRICE, bold=True).next_to(thr, RIGHT, buff=0.1)
        q = pa.ax.c2p(2027, 1000)
        qm = tx("?", 40, PRICE, bold=True).move_to(q)
        card_ = VGroup(
            tx("Our call", 26, PRICE, bold=True),
            tx("Escondida will produce less than", 18, WHITE), tx(f"{C['threshold']:,} thousand tonnes of copper", 18, WHITE,
                                                                  bold=True),
            tx("in BHP's year to June 2027.", 18, WHITE),
            tx(f"Probability: {100 * C['prob']:.0f}%", 24, PRICE, bold=True),
            tx("Checked against BHP's results, August 2027", 14, GREY_A)).arrange(DOWN, buff=0.1).move_to([3.7, 0.6, 0])
        why = VGroup(tx("For: the grade falls to about 0.85%; BHP guides 900-1,000 kt from FY27.", 14, GREY_A),
                     tx("Against: leaching and throughput beat expectations in FY25.", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.7, -2.2, 0])
        src = source("BHP, results for the year to June 2025 (FY24 1,125 kt; FY25 1,305 kt; guidance and outlook)", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> Escondida produced "
            f"{C['fy25']:,} thousand tonnes in the year to June 2025. BHP's guidance for the year to June 2026 is "
            f"{lo:,} to {hi:,}. <bookmark mark='b'/> Its outlook for the five years after that is nine hundred "
            "thousand to a million tonnes a year. <bookmark mark='c'/> Our call: in the year to June 2027, Escondida "
            f"will produce less than {C['threshold']:,} thousand tonnes. We give it a "
            f"{100 * C['prob']:.0f} percent chance. The grade is falling, and BHP's own outlook sits below the line. "
            "What could make us wrong: the mine beat expectations in 2025 with more leaching and faster milling, and "
            "BHP has strong reasons to push throughput while copper is at a record. <bookmark mark='d'/> BHP will "
            "report the number in August 2027, and we will put it here, right or wrong."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN))
            self.play(FadeIn(rng26))
            vo.wait_until("b")
            self.play(FadeIn(rngm), FadeIn(rml))
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(thl), FadeIn(qm, scale=1.5))
            self.play(LaggedStart(*[FadeIn(m) for m in card_], lag_ratio=0.25), run_time=2.0)
            self.play(FadeIn(why))
            vo.wait_until("d")
            self.play(Indicate(card_[4], color=PRICE, scale_factor=1.06))
        self.clear_scene()
