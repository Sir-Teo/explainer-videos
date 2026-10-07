from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import TimeChart, label, last, show_chapter_card, source, tagged, ts

SAVERS = GREY_A  # supply of savings (local to this chapter)


class Savings(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 6, r"Force 3: from savings glut to savings shortage")
        self.market()
        self.capex()

    # ------------------------------------------------------------------
    def market(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=6.6, y_length=5.0, tips=False,
                  axis_config={"color": GREY_B, "stroke_width": 2, "include_ticks": False}).move_to(LEFT * 2.6 + DOWN * 0.3)
        xl = label(r"amount of savings lent and borrowed", font_size=26, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = label(r"real interest rate", font_size=28, color=C.REAL_RATE).next_to(ax.y_axis, UP, buff=0.15).align_to(ax.y_axis, LEFT)
        sch = label(r"(schematic)", font_size=24, color=GREY_B).next_to(xl, DOWN, buff=0.1)
        s_shift, d_shift = ValueTracker(0.0), ValueTracker(0.0)

        def supply_y(x):  # savers lend more when paid more
            return 0.9 * (x - s_shift.get_value()) + 0.5

        def demand_y(x):  # borrowers borrow more when it's cheap
            return 9.5 - 0.9 * (x - d_shift.get_value())

        supply = always_redraw(lambda: ax.plot(supply_y, x_range=[max(0.2, s_shift.get_value()), 9.8], color=SAVERS,
                                               stroke_width=5))
        demand = always_redraw(lambda: ax.plot(demand_y, x_range=[max(0.2, d_shift.get_value() - 0.5), 9.8], color=C.DEBT,
                                               stroke_width=5))

        def eq_point():
            a, b = s_shift.get_value(), d_shift.get_value()
            x = (9.5 + 0.9 * b - 0.5 + 0.9 * a) / 1.8
            return x, supply_y(x)

        dot = always_redraw(lambda: Dot(ax.c2p(*eq_point()), radius=0.11, color=YELLOW))
        level = always_redraw(lambda: DashedLine(ax.c2p(0, eq_point()[1]), ax.c2p(*eq_point()), color=C.REAL_RATE,
                                                 stroke_width=3))
        rate_l = always_redraw(lambda: label(r"the real rate", font_size=24, color=C.REAL_RATE).next_to(
            ax.c2p(0, eq_point()[1]), UR, buff=0.08))
        s_l = always_redraw(lambda: label(r"savers", font_size=30, color=SAVERS).next_to(ax.c2p(9.8, supply_y(9.8)), RIGHT,
                                                                                     buff=0.12))
        d_l = always_redraw(lambda: label(r"borrowers", font_size=30, color=C.DEBT).next_to(
            ax.c2p(9.8, demand_y(9.8)), RIGHT, buff=0.12))
        with self.voiceover(
            "Force number three is about the world's supply of savings. Think of interest rates as a price: the price "
            "of borrowing savings. <bookmark mark='s'/> Savers lend more when they're paid more. <bookmark mark='d'/> "
            "Borrowers, governments and companies, borrow more when money is cheap. <bookmark mark='e'/> Where the two "
            "curves cross sets the real interest rate."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch))
            vo.wait_until("s")
            self.add(supply)
            self.play(FadeIn(s_l))
            vo.wait_until("d")
            self.add(demand)
            self.play(FadeIn(d_l))
            vo.wait_until("e")
            self.play(FadeIn(dot), FadeIn(level), FadeIn(rate_l))

        notes = VGroup(label(r"2000s--2010s: the ``savings glut''", font_size=30, color=SAVERS),
                       label(r"Asia, oil exporters, aging rich societies", font_size=24, color=GREY_A),
                       label(r"$\Rightarrow$ a flood of savings, low rates", font_size=26, color=GREY_A),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 4.3 + UP * 2.0)
        with self.voiceover(
            "Through the 2000s and 2010s, the world had what Ben Bernanke called a savings glut: <bookmark mark='g'/> "
            "a flood of savings from fast-growing Asian economies, oil exporters, and aging rich societies, all looking for "
            "safe places to go. <bookmark mark='s'/> The supply curve shifted out, and the price of money fell. That glut "
            "is a big part of why bond yields stayed so low for so long."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(notes, shift=LEFT * 0.2))
            vo.wait_until("s")
            self.play(s_shift.animate.set_value(2.2), run_time=2.5)

        now = VGroup(label(r"2020s: a savings shortage", font_size=30, color=C.DEBT),
                     label(r"governments: deficits near 6\% of GDP", font_size=24, color=GREY_A),
                     label(r"companies: the AI build-out", font_size=24, color=GREY_A),
                     label(r"$\Rightarrow$ more borrowing chasing less saving", font_size=26, color=GREY_A),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 4.3 + DOWN * 0.6)
        with self.voiceover(
            "Timmer argues that glut has turned into a savings shortage. <bookmark mark='a'/> On the borrowing side, "
            "governments are running big deficits, and companies are pouring money into building out artificial "
            "intelligence. <bookmark mark='b'/> Demand for savings shifts out, <bookmark mark='c'/> while, in his telling, "
            "the surplus savings that once flooded in have dried up. <bookmark mark='r'/> The crossing point moves up: a higher "
            "real interest rate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(now, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(d_shift.animate.set_value(2.0), run_time=2)
            vo.wait_until("c")
            self.play(s_shift.animate.set_value(0.6), run_time=2)
            vo.wait_until("r")
            self.play(Flash(dot, color=YELLOW))
        for m in (supply, demand, dot, level, rate_l, s_l, d_l):
            m.clear_updaters()
        self.clear_scene()

        classic = VGroup(label(r"classic crowding out", font_size=34, color=GREY_A),
                         label(r"government borrowing $\to$ higher rates $\to$ companies cancel projects", font_size=28,
                               color=GREY_A)).arrange(DOWN, buff=0.2).move_to(UP * 1.8)
        rev = VGroup(label(r"reverse crowding out", font_size=38, color=YELLOW),
                     label(r"AI investment $\to$ higher rates $\to$ the government must pay up", font_size=30)).arrange(DOWN, buff=0.2)
        rev.move_to(DOWN * 0.2)
        why = label(r"AI builders expect returns far above their borrowing costs,\\so they keep borrowing", font_size=28,
                    color=C.EARNINGS).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Economists have long worried about crowding out: <bookmark mark='c'/> heavy government borrowing pushes up "
            "rates, and private companies cancel projects that no longer pay. Timmer's twist is <bookmark mark='r'/> "
            "reverse crowding out. Today it's the private sector competing with the government for savings. <bookmark "
            "mark='w'/> The companies building AI expect returns far above what they pay to borrow, so higher rates don't "
            "stop them. Someone has to give way, and it's the price the Treasury pays to borrow."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(classic, shift=DOWN * 0.2))
            vo.wait_until("r")
            self.play(FadeIn(rev, shift=UP * 0.2))
            vo.wait_until("w")
            self.play(FadeIn(why))
        self.clear_scene()

    # ------------------------------------------------------------------
    def capex(self):
        t, v = ts("ai_capex_pct_gdp")
        dot_com = float(v[(t > 1999) & (t < 2001.5)].max())
        assert v[-1] > dot_com and 4.3 < dot_com < 4.6 and 4.9 < v[-1] < 5.2
        level = last("ai_capex")
        assert 1.55 < level < 1.75
        ch = TimeChart((1990, 2026.6), (2.0, 5.5), width=10.4, height=4.7, x_ticks=range(1990, 2030, 5),
                       y_ticks=[2, 3, 4, 5], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.35)
        yl = ch.y_title(r"business investment in computers, equipment and software, \% of GDP", color=C.EARNINGS)
        line = ch.line(t, v, C.EARNINGS, 4)
        k = int(np.argmax(np.where((t > 1999) & (t < 2001.5), v, 0)))
        dc = tagged(rf"dot-com peak: {dot_com:.1f}\%", font_size=26).next_to(ch.c2p(t[k], v[k]), UP, buff=0.15)
        nw = tagged(rf"2026: {v[-1]:.1f}\%\\(\${level:.2f} trillion a year)", font_size=26, color=C.EARNINGS)
        nw.next_to(ch.c2p(t[-1], v[-1]), LEFT, buff=0.2).shift(UP * 0.35)
        ref = ch.hline(dot_com, GREY_B)
        src = source(r"FRED (A679RC1Q027SBEA, GDP); a broad proxy for AI investment")
        with self.voiceover(
            "How big is that build-out? <bookmark mark='a'/> Here's American business investment in information "
            "processing equipment and software, as a share of the economy. It's a broad measure, but it's where the "
            "servers, chips and software of the AI boom show up. <bookmark mark='p'/> At the height of the dot-com boom it "
            "reached about four and a half percent of GDP. <bookmark mark='n'/> It's now above five percent: about 1.6 "
            "trillion dollars a year, competing for the same pool of savings as the Treasury."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            self.play(Create(line), run_time=2.5, rate_func=linear)
            vo.wait_until("p")
            self.play(FadeIn(dc), Create(ref))
            vo.wait_until("n")
            self.play(FadeIn(nw))
        self.clear_scene()
