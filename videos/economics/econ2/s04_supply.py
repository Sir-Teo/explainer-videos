from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Supply(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Supply, and the scissors", r"Which cards set the price?", "Chapter three. Supply, and the "
             "scissors.", lit={1890: r"Marshall's \emph{Principles}"}, scale=("firm", "market"), horizon=("a day",))
        self.farm()
        self.scissors()
        self.marginal()
        self.both()

    # ------------------------------------------------------------------
    def farm(self):
        d = load("supply")
        costs = d["farm"]
        ax = price_axes(5, (0, 4), x_length=6.4, y_length=4.4, qticks=[0, 1, 2, 3, 4, 5], pticks=[0, 1, 2, 3, 4],
                        qlabel=r"sacks of coffee this week", plabel=r"cost of one more sack",
                        center=LEFT * 2.8 + DOWN * 0.5)
        a = ax.ax
        bars = VGroup(*[Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0] - 0.06, height=a.c2p(0, c)[1] - a.c2p(0, 0)[1],
                                  stroke_width=0, fill_color=E.SUPPLY, fill_opacity=0.55)
                        .move_to((a.c2p(k, 0) + a.c2p(k + 1, c)) / 2) for k, c in enumerate(costs)])
        vals = VGroup(*[label(dollars(c), font_size=22, color=WHITE).next_to(b, UP, buff=0.08)
                        for b, c in zip(bars, costs)])
        why = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (
            r"the first sacks: \ the best trees, \ near the road",
            r"then the hillside, \ and more pickers",
            r"the last: \ overtime, \ and the worst land",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        stairs = step_curve(a, [(k, k + 1, c) for k, c in enumerate(costs)], E.SUPPLY)
        price = 2.00
        n = sum(1 for c in costs if c <= price)
        pl = DashedLine(a.c2p(0, price), a.c2p(5, price), color=E.ACCENT, stroke_width=2.5)
        plab = label(rf"price {dollars(price)}", font_size=22, color=E.ACCENT).next_to(a.c2p(0.1, price), UP, buff=0.1)
        plab.align_to(pl, LEFT)
        sells = label(rf"the farm sells {n} sacks", font_size=28, color=E.ACCENT).next_to(why, DOWN, buff=0.5)
        sells.align_to(why, LEFT)
        tag = illustrative_tag(corner=DR, font_size=17)
        with self.voiceover(
            "Supply is built the same way, from the other side of the market. <bookmark mark='a'/> Here is a "
            "coffee farm, and the cost of picking and drying one more sack this week. <bookmark mark='b'/> The "
            "first sacks are cheap: the best trees, near the road. Then the hillside, and more pickers to hire. "
            "The last sacks need overtime, and the worst land on the farm. Each sack costs more than the one "
            "before. That's marginal cost, and it usually rises. <bookmark mark='c'/> If coffee fetches two dollars "
            f"a sack, the farm sells every sack that costs less than that: {n} of them. <bookmark mark='d'/> Draw "
            "the costs as steps and you have the farm's supply curve, rising. Add up every farm sideways, as we "
            "added the drinkers, and you have the market's supply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            for b, v in zip(bars, vals):
                self.play(GrowFromEdge(b, DOWN), FadeIn(v), run_time=0.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w, shift=LEFT * 0.1) for w in why], lag_ratio=0.6), run_time=4)
            vo.wait_until("c")
            self.play(Create(pl), FadeIn(plab))
            self.play(*[b.animate.set_fill(E.ACCENT if c <= price else GREY_D, 0.7 if c <= price else 0.35)
                        for b, c in zip(bars, costs)])
            self.play(FadeIn(sells, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Create(stairs), bars.animate.set_fill(opacity=0.15), run_time=1.5)
        self.clear_scene()

    def scissors(self):
        hc = history_card(1890, r"Alfred Marshall, \ \emph{Principles of Economics}",
                          r"the book that taught demand and supply to the world for half a century", color=E.ACCENT,
                          width=8.0, font_size=25).to_edge(UP, buff=0.45)
        q1 = quote_card(r"The `cost of production principle' and the `final utility' principle are undoubtedly "
                        r"component parts of the one all-ruling law of supply and demand; each may be compared to one "
                        r"blade of a pair of scissors.", r"Marshall, \emph{Principles} (1890)", width=11.6,
                        font_size=27).next_to(hc, DOWN, buff=0.35)
        q2 = quote_card(r"We might as reasonably dispute whether it is the upper or the under blade of a pair of "
                        r"scissors that cuts a piece of paper, as whether value is governed by utility or cost of "
                        r"production.", r"Marshall, \emph{Principles}, Book V, ch.~3 (5th ed., 1907)", width=11.6,
                        font_size=27, color=E.ACCENT).next_to(q1, DOWN, buff=0.3)
        src = published_tag(r"Marshall, \emph{Principles} (1890; 3rd ed. 1895; 5th ed. 1907): Internet Archive scans",
                            corner=DR, font_size=16)
        with self.voiceover(
            "In 1890 Alfred Marshall, at Cambridge, put the two halves together in the book that taught economics "
            "to the world for the next fifty years. <bookmark mark='a'/> The cost of production principle and the "
            "final utility principle, he wrote, are both parts of the one law of supply and demand; each may be "
            "compared to one blade of a pair of scissors. <bookmark mark='b'/> In later editions he put it more "
            "sharply. We might as reasonably dispute whether it is the upper or the under blade of a pair of "
            "scissors that cuts a piece of paper, as whether value is governed by utility or cost of production."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(q1.animate.set_opacity(0.4), FadeIn(q2, shift=UP * 0.2))
        self.clear_scene()

    def marginal(self):
        d = load("supply")
        v, c, q = d["values"], d["costs"], d["q"]
        m = Market(tuple(v), tuple(c))
        ax = price_axes(10, (1, 3.5), x_length=7.4, y_length=4.8, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price",
                        center=LEFT * 2.4 + DOWN * 0.4)
        a = ax.ax
        st = market_steps(a, m.steps())
        band = Rectangle(width=a.c2p(10, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, d["hi"])[1] - a.c2p(0, d["lo"])[1],
                         stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.22)
        band.move_to((a.c2p(0, d["lo"]) + a.c2p(10, d["hi"])) / 2)

        def mark(k, val, color):
            return Dot(a.c2p(k + 0.5, val), radius=0.09, color=color)

        dots = VGroup(mark(q - 1, d["v_last_in"], E.DEMAND), mark(q - 1, d["c_last_in"], E.SUPPLY),
                      mark(q, d["v_first_out"], E.DEMAND), mark(q, d["c_first_out"], E.SUPPLY))
        notes = VGroup(*[label(t, font_size=22, color=col) for t, col in (
            (rf"the {q}th buyer, \ {dollars(d['v_last_in'])}: \ the last one in", E.DEMAND),
            (rf"the {q}th seller, \ {dollars(d['c_last_in'])}: \ the last one in", E.SUPPLY),
            (rf"the {q + 1}th buyer, \ {dollars(d['v_first_out'])}: \ the first one out", GREY_A),
            (rf"the {q + 1}th seller, \ {dollars(d['c_first_out'])}: \ the first one out", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35).shift(UP * 0.9)
        bl = label(rf"the band: \ {dollars(d['lo'])} to {dollars(d['hi'])}", font_size=28, color=E.ACCENT)
        bl.next_to(notes, DOWN, buff=0.45).align_to(notes, LEFT)
        # the top buyer's card rises and the bottom seller's falls: the band does not move
        top = Line(a.c2p(0, v[0]), a.c2p(1, v[0]), color=E.DEMAND, stroke_width=6)
        top_hi = Line(a.c2p(0, 3.5), a.c2p(1, 3.5), color=E.DEMAND, stroke_width=6)
        bot = Line(a.c2p(0, c[0]), a.c2p(1, c[0]), color=E.SUPPLY, stroke_width=6)
        bot_lo = Line(a.c2p(0, 1.0), a.c2p(1, 1.0), color=E.SUPPLY, stroke_width=6)
        same = label(r"the keenest buyer's card rises, \ the cheapest seller's falls: \ the band stays put",
                     font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        tag = published_tag(r"the pit of Part 1: \ its twenty cards", corner=DR, font_size=17)
        with self.voiceover(
            "Now go back to the pit from Part one, with its twenty cards, and ask which of them set the price. "
            "<bookmark mark='a'/> The curves cross at six units. <bookmark mark='b'/> Four cards decide where. The "
            f"sixth buyer, whose card says {money_words(d['v_last_in'])}, and the sixth seller, at "
            f"{money_words(d['c_last_in'])}, are the last ones in: they trade, but only just. "
            f"<bookmark mark='c'/> The seventh buyer, at {money_words(d['v_first_out'])}, and the seventh seller, at "
            f"{money_words(d['c_first_out'])}, are the first ones out. <bookmark mark='d'/> The price has to keep "
            "the last ones in and the first ones out, and that pins it between "
            f"{money_words(d['lo'])} and {money_words(d['hi'])}. <bookmark mark='e'/> Every other card could "
            "change a great deal without moving it. Let the keenest buyer's card rise as high as you like, or the "
            "cheapest seller's cost fall to a dollar: they still trade, and the band doesn't move. The price is set "
            "at the margin, by the traders who are only just in and only just out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(st.demand), Create(st.supply), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(band))
            vo.wait_until("b")
            self.play(FadeIn(dots[0], scale=0.5), FadeIn(dots[1], scale=0.5), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots[2], scale=0.5), FadeIn(dots[3], scale=0.5), FadeIn(notes[2]), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(bl, shift=UP * 0.1), Indicate(band, color=E.ACCENT, scale_factor=1.02))
            vo.wait_until("e")
            self.add(top, bot)
            self.play(Transform(top, top_hi), Transform(bot, bot_lo), run_time=1.5)
            self.play(FadeIn(same), Indicate(bl, color=E.ACCENT))
        self.clear_scene()

    def both(self):
        logo = scissors_logo(2.0).move_to(UP * 0.6)
        lt = VGroup(label(r"what one more unit is worth", font_size=26, color=E.DEMAND),
                    label(r"the buyers' blade", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.12)
        rt = VGroup(label(r"what one more unit costs", font_size=26, color=E.SUPPLY),
                    label(r"the sellers' blade", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.12)
        lt.next_to(logo, LEFT, buff=0.5)
        rt.next_to(logo, RIGHT, buff=0.5)
        bottom = VGroup(
            label(r"water: \ the last litre costs little to bring, \ and is worth little", font_size=26, color=WATER),
            label(r"diamonds: \ the next carat is costly to find, \ and still wanted", font_size=26, color=DIAMOND),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So here is the answer to the question of the part, in one picture. <bookmark mark='a'/> A price is "
            "where what one more unit is worth to the last buyer meets what one more unit costs the last seller. "
            "Neither blade cuts alone. <bookmark mark='b'/> Water is cheap because the last litre costs little to "
            "bring to you and is worth little when it arrives. Diamonds are dear because the next carat is costly "
            "to find and still badly wanted. Smith's paradox was a paradox only for as long as people looked at "
            "the whole instead of the margin."
        ) as vo:
            self.play(Create(logo.demand), Create(logo.supply), run_time=1.2)
            self.play(FadeIn(logo.price, scale=0.3))
            vo.wait_until("a")
            self.play(FadeIn(lt, shift=RIGHT * 0.1), FadeIn(rt, shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bottom], lag_ratio=0.5), run_time=2)
        self.clear_scene()
