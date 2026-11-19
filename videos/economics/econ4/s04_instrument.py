from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class Instrument(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The instrument", r"What could separate the two curves?",
             "Chapter three. The instrument.", scale=("market",), horizon=("a season",))
        self.storms()
        self.wald()
        self.wright()
        self.feasts()

    def storms(self):
        s = load("season")
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        calm = VGroup()
        stormy = VGroup()
        for p, q, st in zip(s["p"], s["q"], s["storm"]):
            (stormy if st else calm).add(Dot(a.c2p(q, p), radius=0.04, color=STORM if st else ORDINARY,
                                             fill_opacity=0.8))
        rows = VGroup(
            label(r"what we need: \ something that moves \\ \emph{supply} and not demand", font_size=26),
            label(r"the weather: \ a storm keeps boats in, \\ and does not change how much \\ anyone wants fish",
                  font_size=24, color=STORM),
            label(rf"{s['n_storm']} stormy days, \ {s['days'] - s['n_storm']} calm", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        tag = island_tag(r"simulated: the Island's season, coloured by the weather", corner=DR, font_size=15)
        with self.voiceover(
            "To find demand, we need days on which only supply moved: something that shifts supply, and has nothing "
            "to do with demand. <bookmark mark='a'/> The Island has one: the weather. A storm keeps boats in "
            "harbour. It doesn't make anyone hungrier for fish, or less hungry. <bookmark mark='b'/> Colour the "
            f"season by the weather: {s['n_storm']} stormy days, and the rest calm."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(calm), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in stormy], lag_ratio=0.05), FadeIn(rows[2]))
        self.clear_scene()

    def wald(self):
        s, ins = load("season"), load("instrument")
        st = ins["storm"]
        m = st["means"]
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        dots = day_dots(ax, s, radius=0.035).set_opacity(0.3)
        pc = a.c2p(m["y0"], m["x0"])
        ps = a.c2p(m["y1"], m["x1"])
        mc = VGroup(Dot(pc, radius=0.13, color=ORDINARY), label(r"calm days", font_size=21, color=ORDINARY).next_to(
            pc, DOWN, buff=0.15))
        ms = VGroup(Dot(ps, radius=0.13, color=STORM), label(r"stormy days", font_size=21, color=STORM).next_to(
            ps, LEFT, buff=0.15))
        through = line_qp(ax, st["estimate"], m["y0"], m["x0"], IVC, width=4)
        truth = line_qp(ax, -s["b"], s["groups"]["ordinary"]["q"], s["groups"]["ordinary"]["p"], E.TRUTH,
                        dashed=True)
        eq = MathTex(r"\hat\beta_{\text{Wald}} = \frac{\bar q_{\text{storm}} - \bar q_{\text{calm}}}"
                     r"{\bar p_{\text{storm}} - \bar p_{\text{calm}}}", font_size=40).to_corner(UR, buff=0.5)
        num = MathTex(rf"= \frac{{{m['y1']:.1f} - {m['y0']:.1f}}}{{{m['x1']:.2f} - {m['x0']:.2f}}} = "
                      rf"{st['estimate']:.1f}", font_size=36, color=IVC).next_to(eq, DOWN, buff=0.3).align_to(eq, LEFT)
        rows = VGroup(
            label(rf"planted demand: \ ${-s['b']:.1f}$", font_size=24, color=E.TRUTH),
            label(rf"two-stage least squares: \ ${ins['iv_storm']['estimate']:.1f}$ \ (s.e.\ "
                  rf"{ins['iv_storm']['se']:.1f})", font_size=22, color=IVC),
            label(rf"first stage: \ a storm raises the price \\ by {money_words(ins['first_stage_storm']['slope'])}",
                  font_size=22, color=STORM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(num, DOWN, buff=0.45).align_to(eq, LEFT)
        tag = island_tag(r"simulated: the Island; truth planted", corner=DR, font_size=15)
        with self.voiceover(
            "Now compare. <bookmark mark='a'/> On the calm days, the average price and catch sit here. "
            "<bookmark mark='b'/> On the stormy days, here: fewer fish, at a higher price. Between the two, only "
            "supply has moved, so the step from one to the other runs along the demand curve. "
            "<bookmark mark='c'/> Divide the change in the catch by the change in the price, and you have demand's "
            f"slope: about {abs(st['estimate']):.0f} fish for every dollar. <bookmark mark='d'/> The planted truth is "
            f"{s['b']:.1f}. The storm has done what no amount of data could: it separated the curves. "
            "<bookmark mark='e'/> This ratio is the Wald estimator, and the storm is called an instrument. It "
            "works on two conditions. It must move the price, which it does: a storm adds about "
            f"{money_words(ins['first_stage_storm']['slope'])} to the price of fish. And it must have no other "
            "route to the catch, except through supply. That second condition can't be checked in the data. It's "
            "an argument about the world."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(mc, scale=0.6))
            vo.wait_until("b")
            self.play(FadeIn(ms, scale=0.6))
            vo.wait_until("c")
            self.play(Create(through), Write(eq))
            self.play(Write(num))
            vo.wait_until("d")
            self.play(Create(truth), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def wright(self):
        who = history_card(r"1928", r"Philip G.\ Wright, \emph{The Tariff on Animal and Vegetable Oils}",
                           r"Appendix B: the elasticities of demand and supply for butter and flaxseed, found with "
                           r"factors that move one curve and not the other", color=IVC, width=7.4, font_size=25)
        who.to_corner(UL, buff=0.5)
        son = history_card(r"2003", r"James Stock and Francesco Trebbi",
                           r"who wrote Appendix B, Philip or his son Sewall, the geneticist? \ Word counts say: "
                           r"Philip", color=GREY_B, width=5.4, font_size=23)
        son.to_corner(UR, buff=0.5)
        dag = VGroup()
        z = label(r"weather", font_size=28, color=STORM)
        p = label(r"supply", font_size=28, color=E.SUPPLY)
        q = label(r"price and quantity", font_size=28, color=WHITE)
        d = label(r"demand", font_size=28, color=E.DEMAND)
        z.move_to(LEFT * 4.8 + DOWN * 1.9)
        p.move_to(LEFT * 2.0 + DOWN * 1.9)
        q.move_to(RIGHT * 1.6 + DOWN * 1.9)
        d.move_to(RIGHT * 1.6 + DOWN * 0.5)
        arrows = VGroup(Arrow(z.get_right(), p.get_left(), buff=0.15, color=STORM),
                        Arrow(p.get_right(), q.get_left(), buff=0.15, color=E.SUPPLY),
                        Arrow(d.get_bottom(), q.get_top(), buff=0.15, color=E.DEMAND))
        no = VGroup(DashedLine(z.get_top() + UP * 0.1, d.get_left() + LEFT * 0.15, color=E.MISS),
                    label(r"no arrow", font_size=22, color=E.MISS)).arrange(RIGHT, buff=0.1)
        no[1].move_to(LEFT * 1.8 + DOWN * 0.7)
        dag.add(z, p, q, d, arrows, no)
        tag = published_tag(r"P.\ G.\ Wright (1928), Appendix B; Stock and Trebbi, JEP 17(3) (2003)", corner=DR,
                            font_size=15)
        with self.voiceover(
            "The idea is almost a hundred years old. <bookmark mark='a'/> In 1928 Philip Wright published a book "
            "on the tariff on animal and vegetable oils, and at the back of it, in Appendix B, he solved Moore's "
            "problem. To find the demand for butter and for flaxseed, he used factors that move one curve and not "
            "the other, <bookmark mark='w'/> such as the weather where the crop was grown. It was the first instrumental variable "
            "estimator. <bookmark mark='b'/> The picture he had in mind was this: the weather has an arrow into "
            "supply, supply and demand together make the price and quantity, <bookmark mark='c'/> and there is no "
            "arrow from the weather to demand. <bookmark mark='d'/> For decades people wondered whether the "
            "appendix was really written by his son, Sewall Wright, a famous geneticist who had invented a method "
            "of drawing just such arrows. In 2003 James Stock and Francesco Trebbi compared its style with both "
            "men's writing, and concluded it was the father's."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(who, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(who, color=IVC, scale_factor=1.02))
            vo.wait_until("w")
            self.play(FadeIn(z, shift=UP * 0.2), FadeIn(p, shift=UP * 0.2), FadeIn(q, shift=UP * 0.2),
                      FadeIn(d, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Create(no[0]), FadeIn(no[1]))
            vo.wait_until("d")
            self.play(FadeIn(son, shift=LEFT * 0.2))
        self.clear_scene()

    def feasts(self):
        s, ins = load("season"), load("instrument")
        fe = ins["feast"]
        m = fe["means"]
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        dots = day_dots(ax, s, radius=0.035).set_opacity(0.3)
        p0 = a.c2p(m["y0"], m["x0"])
        p1 = a.c2p(m["y1"], m["x1"])
        mk = VGroup(Dot(p0, radius=0.13, color=ORDINARY), Dot(p1, radius=0.13, color=FEAST))
        through = line_qp(ax, fe["estimate"], m["y0"], m["x0"], IVC, width=4)
        truth = line_qp(ax, s["d"], s["groups"]["ordinary"]["q"], s["groups"]["ordinary"]["p"], E.TRUTH, dashed=True)
        rows = VGroup(
            label(r"feasts move demand, \ not supply", font_size=26, color=FEAST),
            label(rf"so they trace supply: \ $+{fe['estimate']:.1f}$", font_size=26, color=IVC),
            label(rf"planted supply: \ $+{s['d']:.1f}$", font_size=24, color=E.TRUTH),
            label(r"one instrument per curve", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        tag = island_tag(r"simulated: the Island; truth planted", corner=DR, font_size=15)
        with self.voiceover(
            "The same trick finds the other curve. <bookmark mark='a'/> Feasts move the islanders' demand and do "
            "nothing to the boats. <bookmark mark='b'/> So the step from ordinary days to feast days runs along "
            f"supply, and its slope is about {fe['estimate']:.0f} fish per dollar, <bookmark mark='c'/> against a "
            f"planted {s['d']:.0f}. <bookmark mark='d'/> Each curve needs its own instrument: something that moves "
            "the other curve, and only the other curve."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dots), FadeIn(tag), FadeIn(mk[0]))
            vo.wait_until("a")
            self.play(FadeIn(mk[1], scale=0.6), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(through), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(truth), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
