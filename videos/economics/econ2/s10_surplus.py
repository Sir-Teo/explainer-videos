from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Surplus(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Surplus", r"How much does a market make for the people in it?", "Chapter eight. Surplus.",
             lit={1844: r"Dupuit's bridges"}, scale=("person", "market"), horizon=("a day",))
        self.dupuit()
        self.pit()
        self.best()

    # ------------------------------------------------------------------
    def dupuit(self):
        hc = history_card(1844, r"Jules Dupuit, \ engineer of the Ponts et Chauss\'ees",
                          r"``On the measurement of the utility of public works'': \ what is a bridge worth?",
                          color=E.CS, width=7.4, font_size=24).to_corner(UL, buff=0.45)
        ax = price_axes(10, (0, 10), x_length=6.6, y_length=3.8, qticks=None, pticks=None,
                        qlabel=r"crossings a day", plabel=r"what a crossing is worth to each traveller",
                        center=LEFT * 2.6 + DOWN * 0.95)
        a = ax.ax
        dem = line_on(a, 0, 10, 10, 0, E.DEMAND)
        toll = 3.0
        q = 10 - toll
        rev = Polygon(a.c2p(0, 0), a.c2p(0, toll), a.c2p(q, toll), a.c2p(q, 0), stroke_width=0, fill_color=E.ACCENT,
                      fill_opacity=0.35)
        cs = Polygon(a.c2p(0, toll), a.c2p(0, 10), a.c2p(q, toll), stroke_width=0, fill_color=E.CS, fill_opacity=0.45)
        lost = Polygon(a.c2p(q, 0), a.c2p(q, toll), a.c2p(10, 0), stroke_width=0, fill_color=E.MISS, fill_opacity=0.45)
        tl = DashedLine(a.c2p(0, toll), a.c2p(10, toll), color=E.ACCENT, stroke_width=2)
        tlab = label(r"the toll", font_size=22, color=E.ACCENT).next_to(a.c2p(10, toll), UP, buff=0.1).shift(LEFT * 0.4)
        rows = VGroup(
            label(r"the tolls collected", font_size=24, color=E.ACCENT),
            label(r"what crossers would have paid, \ above the toll", font_size=24, color=E.CS),
            label(r"crossings the toll prevents, \ worth something to someone", font_size=24, color=E.MISS),
            label(r"the bridge's utility: \ all three, \ not the first alone", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.6)
        tag = illustrative_tag(corner=DR, font_size=17)
        src = published_tag(r"Dupuit (1844), \emph{Annales des ponts et chauss\'ees}", corner=UR, font_size=16)
        with self.voiceover(
            "How much good does a market do? The first person to answer properly was a French engineer, Jules "
            "Dupuit, in 1844. <bookmark mark='a'/> His question was practical: is a bridge worth building? The "
            "obvious answer was to count the tolls it would collect. <bookmark mark='b'/> Dupuit saw that the tolls "
            "miss most of it. Line up the travellers by what a crossing is worth to each of them. "
            "<bookmark mark='c'/> The tolls are this rectangle. <bookmark mark='d'/> But everyone who crosses would "
            "have paid more than the toll, some of them much more, and that difference is a gain that nobody "
            "collects. <bookmark mark='e'/> And the travellers the toll turns away, whose crossing would have cost "
            "the bridge nothing, lose this triangle. <bookmark mark='f'/> The bridge's real value is all of it. "
            "Marshall named the middle area: he called it consumer's rent at first, and then consumer's surplus, "
            "the name that stuck."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(dem), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(tl), FadeIn(tlab), FadeIn(rev), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(cs), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(lost), FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def pit(self):
        d = load("surplus")["pit"]
        v, c, q, p = d["values"], d["costs"], d["q"], d["p"]
        m = Market(tuple(v), tuple(c))
        ax = price_axes(10, (1, 3.5), x_length=7.2, y_length=4.8, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price", center=LEFT * 2.5 + DOWN * 0.35)
        a = ax.ax
        st = market_steps(a, m.steps())
        w = a.c2p(1, 0)[0] - a.c2p(0, 0)[0]
        cs = VGroup(*[Rectangle(width=w, height=a.c2p(0, x)[1] - a.c2p(0, p)[1], stroke_width=0, fill_color=E.CS,
                                fill_opacity=0.5).move_to((a.c2p(k, p) + a.c2p(k + 1, x)) / 2) for k, x in enumerate(v[:q])])
        ps = VGroup(*[Rectangle(width=w, height=a.c2p(0, p)[1] - a.c2p(0, x)[1], stroke_width=0, fill_color=E.PS,
                                fill_opacity=0.4).move_to((a.c2p(k, x) + a.c2p(k + 1, p)) / 2) for k, x in enumerate(c[:q])])
        pl = DashedLine(a.c2p(0, p), a.c2p(10, p), color=E.ACCENT, stroke_width=2)
        # one pair too many: the seventh buyer and the seventh seller trade at a loss to the market
        extra = Rectangle(width=w, height=a.c2p(0, c[q])[1] - a.c2p(0, v[q])[1], stroke_width=0, fill_color=E.MISS,
                          fill_opacity=0.6).move_to((a.c2p(q, v[q]) + a.c2p(q + 1, c[q])) / 2)
        short = Rectangle(width=w, height=a.c2p(0, v[q - 1])[1] - a.c2p(0, c[q - 1])[1], stroke_width=0,
                          fill_color=E.MISS, fill_opacity=0.6).move_to((a.c2p(q - 1, c[q - 1]) + a.c2p(q, v[q - 1])) / 2)
        rows = VGroup(
            label(rf"at {dollars(p)}: \ buyers keep {dollars(d['cs'])}", font_size=25, color=E.CS),
            label(rf"sellers keep {dollars(d['ps'])}", font_size=25, color=E.PS),
            label(rf"together: \ {dollars(d['surplus'])}, \ the most possible", font_size=27, color=WHITE),
            label(rf"one pair fewer: \ lose {dollars(v[q - 1] - c[q - 1])}", font_size=23, color=E.MISS),
            label(rf"one pair more: \ lose {dollars(c[q] - v[q])}", font_size=23, color=E.MISS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45).shift(UP * 0.3)
        tag = published_tag(r"the pit of Part 1", corner=DR, font_size=17)
        with self.voiceover(
            "Dupuit's idea measures any market. Here is Part one's pit again. <bookmark mark='a'/> At a price of "
            f"{money_words(p)}, each buyer who trades keeps the difference between her card and the price: the "
            f"blue steps, {money_words(d['cs'])} in all. <bookmark mark='b'/> Each seller keeps the price less his "
            f"cost: the amber steps, {money_words(d['ps'])}. <bookmark mark='c'/> Together that's "
            f"{money_words(d['surplus'])}, and no other arrangement of these twenty people can make more. "
            "<bookmark mark='d'/> Drop the last pair, and the market loses the thin step between them. "
            "<bookmark mark='e'/> Add one more pair, the seventh buyer and the seventh seller, and the unit costs "
            "more to make than it's worth to the person who gets it: that loses money too. The competitive "
            "quantity is exactly the one that makes the most."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), FadeIn(tag), run_time=1.5)
            self.play(Create(pl))
            vo.wait_until("a")
            self.play(FadeIn(cs, lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ps, lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(short), FadeIn(rows[3]))
            self.play(FadeOut(short))
            vo.wait_until("e")
            self.play(FadeIn(extra), FadeIn(rows[4]))
        self.clear_scene()

    def best(self):
        s = load("surplus")
        L = Linear(**s["line"])
        e = s["fish"]
        ax = price_axes(400, (0, 6), x_length=7.0, y_length=4.6, qticks=[0, 100, 200, 300, 400], pticks=[0, 1, 2, 3, 4, 5, 6],
                        qlabel=r"fish a day", plabel=r"price", center=LEFT * 2.6 + DOWN * 0.35)
        a = ax.ax
        dem = line_on(a, 0, L.choke, L.a, 0, E.DEMAND)
        sup = line_on(a, 0, L.reservation, float(L.qs(6.0)), 6.0, E.SUPPLY)
        cs = Polygon(a.c2p(0, e["p"]), a.c2p(0, L.choke), a.c2p(e["q"], e["p"]), stroke_width=0, fill_color=E.CS,
                     fill_opacity=0.45)
        ps = Polygon(a.c2p(0, L.reservation), a.c2p(0, e["p"]), a.c2p(e["q"], e["p"]), stroke_width=0, fill_color=E.PS,
                     fill_opacity=0.4)
        q1 = 150.0
        tri = Polygon(a.c2p(q1, float(L.pd(q1))), a.c2p(q1, float(L.ps(q1))), a.c2p(e["q"], e["p"]), stroke_width=0,
                      fill_color=E.MISS, fill_opacity=0.6)
        cut = DashedLine(a.c2p(q1, 0), a.c2p(q1, float(L.pd(q1))), color=E.MISS, stroke_width=2.5)
        rows = VGroup(
            label(rf"buyers' surplus: \ {dollars(e['cs'], 0)} a day", font_size=25, color=E.CS),
            label(rf"sellers' surplus: \ {dollars(e['ps'], 0)} a day", font_size=25, color=E.PS),
            label(rf"if only {q1:.0f} fish could be sold:", font_size=24, color=GREY_A),
            label(r"the triangle is lost: \ a deadweight loss", font_size=25, color=E.MISS),
            label(r"taxes and price controls cut here: \ chapters 9 and 10", font_size=23, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        tag = island_tag(r"simulated: the Island's fish market (planted lines)", corner=DR, font_size=16)
        with self.voiceover(
            "With many traders the steps become areas. <bookmark mark='a'/> On the Island's fish market, the "
            f"villagers' surplus is this triangle, about {e['cs']:.0f} dollars a day, and the fishers' is this one, "
            f"about {e['ps']:.0f}. <bookmark mark='b'/> Now suppose something stops the market at {q1:.0f} fish a day. "
            "<bookmark mark='c'/> Every fish between there and the competitive quantity was worth more to some "
            "buyer than it cost some fisher to catch, and none of them is caught. That triangle of gains is simply "
            "gone; it doesn't move to anyone. Economists call it a deadweight loss, and Arnold Harberger made a "
            "career of measuring it. <bookmark mark='d'/> Taxes and price controls both cut a market off short of "
            "its competitive quantity. The next two chapters measure what that costs, and who pays."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), Create(sup), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(cs), FadeIn(rows[0]))
            self.play(FadeIn(ps), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(tri), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
