from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.moore()
        self.wright()
        self.cloud()
        self.question()
        self.title()
        self.objectives()

    # ------------------------------------------------------------------
    def moore(self):
        m = tables.MOORE_1914.data
        who = history_card(r"1914", r"Henry Ludwell Moore, Columbia University",
                           r"\emph{Economic Cycles: Their Law and Cause}: ``statistical laws of demand'' fitted to the "
                           r"prices and quantities of crops, and of pig iron", color=E.DEMAND, width=6.6, font_size=25)
        who.to_corner(UL, buff=0.5)
        q = quote_card(m["moore"], r"Moore (1914), p.\ 126", width=11.6, font_size=30, color=E.DEMAND)
        q.to_edge(DOWN, buff=0.6)
        cax = axes([0, 4], [0, 4], x_length=2.6, y_length=2.3, xlabel=r"corn supplied", ylabel=r"price",
                   font_size=18, center=RIGHT * 2.1 + UP * 1.7)
        down = Line(cax.ax.c2p(0.5, 3.4), cax.ax.c2p(3.6, 0.7), color=E.DEMAND, stroke_width=4)
        dl = label(r"crops: \\ sloping down", font_size=20, color=E.DEMAND).next_to(cax, DOWN, buff=0.15)
        ax = axes([0, 4], [0, 4], x_length=2.6, y_length=2.3, xlabel=r"pig iron supplied", ylabel=r"price",
                  font_size=18, center=RIGHT * 5.4 + UP * 1.7)
        up = Line(ax.ax.c2p(0.5, 0.7), ax.ax.c2p(3.6, 3.4), color=E.MISS, stroke_width=4)
        ul = label(r"pig iron: \\ Moore's ``law of demand''", font_size=20, color=E.MISS).next_to(ax, DOWN,
                                                                                               buff=0.15)
        tag = published_tag(r"H.\ L.\ Moore, Economic Cycles (1914), as quoted in The Econometrics Journal (2025)",
                            corner=DR, font_size=15)
        with self.voiceover(
            "In 1914 an economist at Columbia University, Henry Moore, did something new. He took the actual "
            "prices and quantities of goods, year by year, and fitted lines through them, which he called "
            "statistical laws of demand. <bookmark mark='x'/> For crops like corn and potatoes, his lines sloped "
            "down, as demand curves should. <bookmark mark='a'/> For pig iron, the raw material of steel, his line sloped up. "
            "<bookmark mark='b'/> Moore didn't flinch. Unlike the law of demand for the crops, he wrote, the law of "
            "demand for a producers' good is such that as the supply increases the price rises. A new kind of "
            "demand curve, discovered in the data."
        ) as vo:
            self.play(FadeIn(who, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("x")
            self.play(FadeIn(cax), Create(down), FadeIn(dl))
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(up), FadeIn(ul))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def wright(self):
        who = history_card(r"1915", r"Philip Wright, reviewing Moore",
                           r"rainfall moves the supply of crops; but through business conditions it moves the "
                           r"\emph{demand} for pig iron", color=E.SUPPLY, width=6.6, font_size=25)
        who.to_corner(UL, buff=0.5)

        def panel(title, move, color, center):
            ax = axes([0, 4], [0, 4], x_length=3.6, y_length=2.8, xlabel=r"quantity", ylabel=r"price", font_size=18,
                      center=center)
            a = ax.ax
            d = Line(a.c2p(0.4, 3.6), a.c2p(3.6, 0.4), color=E.DEMAND, stroke_width=3)
            s = Line(a.c2p(0.4, 0.6), a.c2p(3.6, 3.4), color=E.SUPPLY, stroke_width=3)
            g = VGroup(ax, d, s)
            shifted = VGroup()
            pts = VGroup()
            for k in (-0.6, 0.0, 0.6):
                if move == "supply":
                    ln = Line(a.c2p(0.4 + k, 0.6), a.c2p(3.6 + k, 3.4), color=E.SUPPLY, stroke_width=2,
                              stroke_opacity=0.5)
                    x = 2.0 + k / 2
                    pt = a.c2p(x, 4.0 - x)
                else:
                    ln = Line(a.c2p(0.4 + k, 3.6), a.c2p(3.6 + k, 0.4), color=E.DEMAND, stroke_width=2,
                              stroke_opacity=0.5)
                    x = 2.0 + k / 2
                    pt = a.c2p(x, x)
                shifted.add(ln)
                pts.add(Dot(pt, radius=0.08, color=WHITE))
            t = label(title, font_size=22, color=color).next_to(ax, UP, buff=0.15)
            return VGroup(g, shifted, pts, t)

        crops = panel(r"crops: \ rain moves supply", "supply", E.SUPPLY, LEFT * 1.6 + DOWN * 1.2)
        iron = panel(r"pig iron: \ booms move demand", "demand", E.DEMAND, RIGHT * 3.6 + DOWN * 1.2)
        trace1 = label(r"the points trace demand", font_size=21, color=E.DEMAND).next_to(crops, DOWN, buff=0.15)
        trace2 = label(r"the points trace supply", font_size=21, color=E.SUPPLY).next_to(iron, DOWN, buff=0.15)
        tag = published_tag(r"P.\ G.\ Wright, ``Moore's Economic Cycles'', QJE 29 (1915)", corner=DR, font_size=15)
        with self.voiceover(
            "A year later an economist named Philip Wright reviewed Moore's book and saw the trouble. "
            "<bookmark mark='a'/> Rain moves the supply of crops, so a crop's prices and quantities slide along "
            "its demand curve. <bookmark mark='b'/> But the same weather, through the whole state of business, "
            "moves the demand for pig iron, so iron's points slide along its supply curve. <bookmark mark='c'/> "
            "Moore's upward-sloping law of demand was a supply curve. The data had answered a different question "
            "from the one he asked."
        ) as vo:
            self.play(FadeIn(who, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(crops[0]), FadeIn(crops[3]))
            self.play(LaggedStart(*[FadeIn(x) for x in crops[1]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(x, scale=0.5) for x in crops[2]], lag_ratio=0.3), FadeIn(trace1))
            vo.wait_until("b")
            self.play(FadeIn(iron[0]), FadeIn(iron[3]))
            self.play(LaggedStart(*[FadeIn(x) for x in iron[1]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(x, scale=0.5) for x in iron[2]], lag_ratio=0.3), FadeIn(trace2))
            vo.wait_until("c")
            self.play(Indicate(trace2, color=E.SUPPLY))
        self.clear_scene()

    def cloud(self):
        s = load("season")
        ax = fish_axes(center=LEFT * 2.0 + DOWN * 0.2)
        dots = day_dots(ax, s)
        a = ax.ax
        ols = line_qp(ax, s["ols_slope"], s["q_mean"], s["p_mean"], OLSC)
        rows = VGroup(
            label(rf"the Island's fish market: \ {s['days']} days", font_size=26),
            label(r"each dot: \ one day's price and catch sold", font_size=22, color=GREY_A),
            label(rf"a line through them: \ slope $+{s['ols_slope']:.1f}$ fish per dollar", font_size=24, color=OLSC),
            label(r"higher prices, \ more fish sold?", font_size=26, color=OLSC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45).shift(UP * 0.6)
        working = label(r"Elmer Working, 1927: \ ``What do statistical `demand curves' show?''", font_size=24,
                        color=E.ACCENT).to_edge(DOWN, buff=0.4)
        tag = island_tag(r"simulated: the Island, a season of the fish market", corner=UR, font_size=15)
        with self.voiceover(
            "The Island can make the same mistake. <bookmark mark='a'/> Here is a season of the fish market, two "
            "hundred and forty days, each dot one day's price and the number of fish sold. <bookmark mark='b'/> Put "
            f"the best straight line through them, and it slopes upward: about {s['ols_slope']:.0f} more fish sold "
            "for every dollar on the price. <bookmark mark='c'/> Do the islanders want more fish when fish is dearer? "
            "Of course not. In 1927 an agricultural economist, Elmer Working, asked the question in its general "
            "form: what do statistical demand curves show? The answer turned out to be the foundation of modern "
            "empirical economics."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.006), FadeIn(rows[0]),
                      FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ols), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(working))
        self.clear_scene()

    def question(self):
        q = label(ASK, font_size=58, color=E.ACCENT).to_edge(UP, buff=0.9)
        subs = VGroup(
            label(r"a cloud of prices and quantities: \ which curve is it?", font_size=30, color=E.DEMAND),
            label(r"a training programme: \ did it work, \ or were its trainees different?", font_size=30,
                  color=EXP),
            label(r"a pattern in the past: \ will it hold once policy leans on it?", font_size=30, color=OLSC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part is about one question: when can data answer an economic question? <bookmark mark='a'/> "
            "When does a cloud of prices and quantities tell you about demand? <bookmark mark='b'/> When can you "
            "tell whether a programme worked, rather than that the people in it were different? <bookmark mark='c'/> "
            "And when will a pattern found in the past survive a government that tries to use it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", subs):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = magnifier(0.8)
        t = label(SERIES_EN, font_size=72)
        sub = label(r"Part 4 \ \textperiodcentered\ \ The Evidence", font_size=40, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part four: the evidence."):
            self.play(Create(logo.ring), Create(logo.handle), LaggedStart(*[FadeIn(d, scale=0.3) for d in logo.dots],
                                                                          lag_ratio=0.1), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(0.8)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 4", font_size=34, color=GREY_B), label(r"The Evidence", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"find the demand curve in a cloud of prices yourself, \ and see why the obvious line fails",
            r"the instrument: \ weather that moves supply alone, \ from Philip Wright in 1928",
            r"omitted variables and selection, \ and LaLonde's test of the methods against an experiment",
            r"the credibility revolution: \ lotteries, birthdays, borders, \ and experiments in the field",
            r"the Lucas critique, \ structure against design, \ and the return to a year of school",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Part four: the evidence. <bookmark mark='a'/> You'll try to find the demand curve in the Island's cloud, "
            "and see why the obvious line fails. <bookmark mark='b'/> Then the fix that Philip Wright found in 1928: "
            "an instrument, something like the weather that moves one curve and not the other. "
            "<bookmark mark='c'/> We'll meet omitted variables and self-selection, and a famous test in which the "
            "methods of the day were checked against an experiment. <bookmark mark='d'/> Then the credibility "
            "revolution: draft lotteries, birthdays, state borders and experiments in the field. "
            "<bookmark mark='e'/> And we'll finish with the Lucas critique, the argument between structure and "
            "design, and what a year of school is worth."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
