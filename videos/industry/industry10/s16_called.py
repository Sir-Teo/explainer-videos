from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "Was the battle to feed humanity lost?",
             "Chapter fourteen. Called it?", lit=("change",))
        self.bomb()
        self.ours()

    def bomb(self):
        cal = R["calories"]
        book = VGroup(Rectangle(width=2.0, height=2.8, stroke_color=WHITE, stroke_width=2, fill_color="#7A1E1E", fill_opacity=1),
                      VGroup(tx("THE", 14, WHITE, bold=True), tx("POPULATION", 18, WHITE, bold=True), tx("BOMB", 26, WHITE, bold=True),
                             tx("Paul R. Ehrlich, 1968", 12, GREY_A)).arrange(DOWN, buff=0.08)).move_to([-4.6, 0.6, 0])
        book[1].move_to(book[0])
        quote = VGroup(tx("\"The battle to feed all of humanity is over.\"", 22, WHITE, bold=True),
                       tx("It predicted that hundreds of millions would starve", 17, GREY_A),
                       tx("in the coming decades, whatever was done.", 17, GREY_A)).arrange(DOWN, buff=0.08).move_to([1.6, 2.2, 0])
        ys = [1961, 1968, 1980, 2000, 2024]
        bars = VGroup()
        for i, y in enumerate(ys):
            v = cal["World"][y]
            b = Rectangle(width=0.9, height=(v - 1500) / 1600 * 3.0, stroke_width=0, fill_color=FARM, fill_opacity=0.9).move_to(
                [-0.6 + 1.35 * i, -2.6, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{v:,.0f}", 15, WHITE, bold=True).next_to(b, UP, buff=0.05),
                            tx(str(y), 14, GREY_A).next_to(b, DOWN, buff=0.06)))
        bt = tx("food per person on Earth, kilocalories a day", 15, GREY_A).next_to(bars, UP, buff=0.55)
        verdict = VGroup(tx("Wrong, by a wide margin.", 22, STATE, bold=True),
                         tx("Famines still came, mostly from war and politics,", 15, GREY_A),
                         tx("but nothing on the scale foretold.", 15, GREY_A)).arrange(DOWN, buff=0.05).move_to([-4.6, -2.1, 0])
        src = source("Paul R. Ehrlich, The Population Bomb (Ballantine, 1968); FAO food balances via Our World in Data", size=13)
        with self.voiceover(
            "Part ten's forecast to test is one of the most famous of the twentieth century. "
            "<bookmark mark='a'/> In 1968 the biologist Paul Ehrlich, the same man who would later lose the metals bet "
            "of Part nine, published The Population Bomb. It opened: the battle to feed all of humanity is over. "
            "<bookmark mark='b'/> It predicted that hundreds of millions of people would starve to death in the coming "
            "decades, whatever crash programmes were launched. India, it argued, could not feed itself. "
            "<bookmark mark='c'/> As the book went to press, Borlaug's dwarf wheat was already spreading across India "
            f"and Pakistan. Here is the world's food supply per person: about {cal['World'][1961]:,.0f} kilocalories a "
            f"day in 1961, about {cal['World'][1968]:,.0f} when the book appeared, and about {cal['World'][2024]:,.0f} "
            "in 2024, for a population more than twice as large. <bookmark mark='d'/> Called it? No. Famines still "
            "came, in Bangladesh, in Ethiopia, in North Korea, mostly through war and misrule. But the mass starvation "
            "foretold did not come, because the farmers, the seed breeders and the fertilizer makers, the whole industry "
            "of this film, grew the food."
        ) as vo:
            self.play(FadeIn(src), FadeIn(book, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(quote[0]))
            vo.wait_until("b")
            self.play(FadeIn(quote[1:]))
            vo.wait_until("c")
            self.play(FadeIn(bt), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars],
                                              lag_ratio=0.35), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        D = R["dollar"]
        C = R["call"]
        S = D["series"]["All"]
        ys = sorted(S)
        pa = viz.plot_axes([2006.5, 2026.8], [10, 17], x_length=6.6, y_length=3.8, xticks=[2007, 2011, 2016, 2021, 2026],
                           yticks=[11, 13, 15, 17], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}c", size=13).move_to(
            [-2.8, -0.4, 0])
        ln = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, S[y]) for y in ys])
        last = Dot(pa.ax.c2p(ys[-1], S[ys[-1]]), color=PRICE, radius=0.07)
        q = tx("?", 40, PRICE, bold=True).move_to(pa.ax.c2p(2026, S[ys[-1]] + 0.9))
        arr = Arrow(pa.ax.c2p(2025.1, S[ys[-1]]), pa.ax.c2p(2026, S[ys[-1]] + 0.6), buff=0.05, stroke_width=3, color=PRICE,
                    tip_length=0.14)
        pt = tx("the farm share of a US food dollar, cents", 15, GREY_A).next_to(pa, UP, buff=0.1)
        pc = C["price_change"]
        card_ = VGroup(tx("Our call", 26, PRICE, bold=True),
                       tx("In USDA's next food dollar, the farm share", 17, WHITE),
                       tx("for 2026 will be higher than for 2025", 17, WHITE, bold=True),
                       tx("(compared within the same release).", 15, GREY_A),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 24, PRICE, bold=True),
                       tx("Checked when the release comes out, late 2027", 13, GREY_A)).arrange(DOWN, buff=0.1).move_to([3.8, 0.7, 0])
        why = VGroup(tx("Jan-Sep 2026 against a year before:", 14, WHITE),
                     tx(f"maize {100 * pc['maize']:+.0f}%, wheat {100 * pc['wheat']:+.0f}%, soybeans {100 * pc['soybeans']:+.0f}%, "
                        f"beef {100 * pc['beef']:+.0f}%", 14, GREY_A),
                     tx("Against: more of each dollar spent in restaurants.", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.05).move_to([3.8, -2.1, 0])
        src = source("USDA ERS Food Dollar Series (November 2026); IMF prices via FRED", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> The farm share of an American "
            f"food dollar was {C['last']:.1f} cents in {C['year']}. Since 2016 it has stayed between "
            f"{C['since2016'][0]:.1f} and {C['since2016'][1]:.1f}, rising when farm prices rise. "
            "<bookmark mark='b'/> In the first nine months of 2026, the world prices of maize, wheat, soybeans and beef "
            "all averaged more than a year earlier, by between five and eighteen percent. <bookmark mark='c'/> So our "
            "call: when the Department of Agriculture next publishes the food dollar, the farm share for 2026 will be "
            "higher than for 2025, comparing the two years in the same release, since the department revises its "
            f"figures. We give it {100 * C['prob']:.0f} percent. What could make us wrong: Americans moving still more of "
            "their food spending to restaurants, where the farm share is small, or margins further down the chain "
            "widening faster than farm prices. We will report the answer, right or wrong."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(pt), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            self.play(FadeIn(last, scale=2))
            vo.wait_until("b")
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(q))
            self.play(LaggedStart(*[FadeIn(m) for m in card_], lag_ratio=0.25), run_time=2.0)
        self.clear_scene()
