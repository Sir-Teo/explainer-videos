from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403


def traders(b):
    return (ge.Trader((b["aA"], 1 - b["aA"]), b["eA"]), ge.Trader((b["aB"], 1 - b["aB"]), b["eB"]))


class Prices(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Prices: \ offer curves, \ equilibrium, \ Walras's law", r"Is there a price at which both "
             r"traders want exactly what the other offers?", "Chapter three. Prices: offer curves, equilibrium, and "
             "Walras's law.", lit={1874: r"Walras's \emph{\'El\'ements}"})
        self.wrong_price()
        self.offer_curves()
        self.walras()
        self.fact()

    def wrong_price(self):
        b = load("box")
        A, B = traders(b)
        X = np.array(b["X"])
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        p = 1.5
        line = price_line(box, b["eA"], p)
        da = A.demand([p, 1.0])
        db = B.demand([p, 1.0])
        Pa = Dot(box.c2p(*da), radius=0.09, color=ANA)
        Pb = Dot(box.c2p(*(X - db)), radius=0.09, color=BO)
        sell = A.e[0] - da[0]
        buy = db[0] - B.e[0]
        side = VGroup(
            label(r"a price: \ 1.5 baskets for a fish", font_size=24),
            label(r"the budget line through $\omega$, \ slope $-1.5$: \\ everything each can reach by trading at "
                  r"that price", font_size=22, color=GREY_A),
            label(rf"Ana's best point: \ she sells {sell:.2f} fish", font_size=23, color=ANA),
            label(rf"Bo's best point: \ he buys {buy:.2f} fish", font_size=23, color=BO),
            label(rf"too many fish offered, \ too few wanted: \\ excess supply of {sell - buy:.2f} fish; \ "
                  r"the price of fish is too high", font_size=22, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now add a price. Suppose anyone can swap fish for coconuts at a basket and a half for a fish. "
            "<bookmark mark='a'/> Then the points Ana can reach by trading lie on a straight line through the "
            "starting point, with slope minus one and a half: her budget line. Bo faces the same line, seen from his corner. "
            "<bookmark mark='b'/> Ana picks the point on it she likes best, where it just touches one of her "
            "curves. At this price fish are dear, so she sells a lot of them: four point four. "
            "<bookmark mark='c'/> Bo picks his best point on the same line. At this price he wants to buy far "
            "fewer: two point six. <bookmark mark='d'/> So at this price the two plans don't fit: more "
            "fish offered than wanted, one point eight too many. The price of fish is too high."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(Pa, scale=0.5), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(Pb, scale=0.5), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), Indicate(VGroup(Pa, Pb), color=HOLD))
        self.clear_scene()

    def offer_curves(self):
        b = load("box")
        X = np.array(b["X"])
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        oa = box.curve(b["offer_A"][0], b["offer_A"][1], color=ANA, width=3.5)
        ob = box.curve(b["offer_B"][0], b["offer_B"][1], color=BO, width=3.5)
        E_ = Dot(box.c2p(*b["xA"]), radius=0.1, color=CC)
        line = price_line(box, b["eA"], b["p"])
        A, B = traders(b)
        ua = A.utility(b["xA"])
        ub = B.utility(b["xB"])
        xs = np.linspace(0.05, X[0], 300)
        ia = box.curve(xs, ge.cd_indifference(b["aA"], ua, xs), color=ANA, width=2.2).set_stroke(opacity=0.7)
        xs2 = np.linspace(0.0, X[0] - 0.05, 300)
        ib = box.curve(xs2, X[1] - ge.cd_indifference(b["aB"], ub, X[0] - xs2), color=BO, width=2.2
                       ).set_stroke(opacity=0.7)
        side = VGroup(
            label(r"turn the price: \ each best point traces \\ an \emph{offer curve}", font_size=23),
            label(rf"they cross at {b['p']:.3f} baskets a fish:", font_size=24, color=CC),
            label(rf"Ana sells {b['trade_fish']:.2f} fish \\ for {b['trade_coco']:.2f} baskets, \ "
                  r"just what Bo wants", font_size=23, color=CC),
            label(r"a competitive equilibrium: \\ prices at which every market clears", font_size=23,
                  color=E.ACCENT),
            label(r"both curves touch the line, \ so they touch each other: \\ the equilibrium is on the contract "
                  r"curve", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "So lower the price, and keep lowering it, and watch where each of them would choose to be. "
            "<bookmark mark='a'/> Ana's best points trace out a curve, her offer curve, and Bo's best points trace "
            "out his. <bookmark mark='b'/> They cross at one place: a price of one point oh one eight baskets a "
            "fish. <bookmark mark='c'/> At that price Ana wants to sell four point two one fish for four point two "
            "nine baskets, and Bo wants to buy exactly that: four point two one fish, paying four point two nine "
            "baskets. <bookmark mark='d'/> This is a competitive equilibrium, in Leon Walras's sense: a price at "
            "which each trader does the best they can, taking the price as given, and every market clears. "
            "<bookmark mark='e'/> And look where it is. Both curves touch the same price line there, so they touch "
            "each other. The equilibrium is on the contract curve. It's trade B, the one from Play it."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w))
            vo.wait_until("a")
            self.play(Create(oa), Create(ob), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(E_, scale=0.5), Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(ia), Create(ib), FadeIn(side[4]))
        self.clear_scene()

    def walras(self):
        b = load("box")
        A, B = traders(b)
        p = 1.5
        z = ge.excess([A, B], [p, 1.0])
        rows = VGroup(
            label(r"every trader's plan is affordable: \ spending equals the value of what they own", font_size=25),
            MathTex(r"p_{\text{fish}}\, z_{\text{fish}} + p_{\text{coco}}\, z_{\text{coco}} = 0", font_size=42,
                    color=E.ACCENT),
            label(rf"at 1.5 baskets a fish: \ $1.5 \times ({z[0]:.2f}) + 1 \times ({z[1]:+.2f}) = "
                  rf"{abs(p * z[0] + z[1]):.2f}$", font_size=26),
            label(r"so if the fish market clears, \ the coconut market clears too", font_size=26, color=CC),
            label(r"with $n$ goods: \ $n - 1$ conditions, \ $n - 1$ relative prices \ (only ratios matter)",
                  font_size=25, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        hc = history_card(1874, r"L\'eon Walras, \ Lausanne", r"\emph{\'El\'ements d'\'economie politique pure}: \ "
                          r"all markets at once, \ cleared by an auctioneer who calls out prices", color=E.ACCENT,
                          width=10.6, font_size=23)
        VGroup(hc, rows).arrange(DOWN, buff=0.45)
        with self.voiceover(
            "Leon Walras, in Lausanne in 1874, was the first to write down a whole economy of markets clearing at "
            "once. <bookmark mark='a'/> One identity makes it manageable. Each trader's plan is affordable: what "
            "they spend equals the value of what they own. Add up everyone's plans and the value of all the "
            "excess demands is zero, at any prices whatever. <bookmark mark='b'/> At a basket and a half for a "
            "fish, the excess supply of fish, valued at one and a half, exactly matches the excess demand for "
            "coconuts. "
            "<bookmark mark='c'/> So if one market clears, the other must. This is Walras's law. "
            "<bookmark mark='d'/> With many goods it says that if all markets but one clear, the last one does too; "
            "and since only relative prices matter, an economy of n goods has n minus one prices to find, and n "
            "minus one markets to clear."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Write(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def fact(self):
        f = load("fact")
        fa = facts.BY_KEY["one_price"]
        v = f["villages"]
        guess = label(r"(yours)", font_size=26, color=E.ACCENT)
        data_col = VGroup(
            label(rf"oil, 1987--2010: \ Brent $-$ WTI \\ averaged {signed(f['mean_before'])} \$ a barrel",
                  font_size=24),
            label(rf"a basket of output costs \\ {f['level_poorest20']:.2f} of America's price \\ in the 20 "
                  rf"poorest countries", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ag = VGroup(
            label(rf"fish, \ carried at \${v['cost']:.0f}: \\ \${v['fish'][0]:.2f} and \${v['fish'][1]:.2f}",
                  font_size=24, color=E.AGORA),
            label(rf"haircuts, \ not carried: \\ \${v['haircuts'][0]:.0f} and \${v['haircuts'][1]:.0f}",
                  font_size=24, color=E.AGORA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fc = fact_card(fa.statement, columns=((r"your guess", guess), (r"the data", data_col), (r"Agora", ag)),
                       width=12.6).move_to(UP * 0.9)
        rows = VGroup(
            label(r"equilibrium has one price for each good, \ for everyone: \ the law of one price", font_size=24,
                  color=CC),
            label(r"it holds where traders can carry goods across: \ the gap shrinks to the cost of carrying",
                  font_size=23),
            label(r"it fails for what can't be carried: \ the haircut stays where it is", font_size=23,
                  color=HOLD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        tag = data_tag(r"FRED (EIA): MCOILBRENTEU, MCOILWTICO; World Bank WDI, 2023; Radford (1945)", corner=DL,
                       font_size=13)
        with self.voiceover(
            "In the equilibrium of the box, Ana and Bo face the same price. That's a prediction about every market: "
            "one price for each good, for everyone. It's the second of this series' Facts. <bookmark mark='a'/> "
            "Make a guess before the data: where would you expect it to hold, and where to fail? "
            "<bookmark mark='b'/> Crude oil is about as uniform a good as there is. From 1987 to 2010 the North Sea "
            "crude called Brent and the American crude called West Texas Intermediate differed by about a dollar "
            "and a half a barrel, the American usually the dearer, on prices that ranged from about ten dollars to "
            "well over a hundred. But a haircut can't be shipped. In the "
            "twenty poorest countries, the same basket of goods and services costs about a third of what it costs "
            "in America. <bookmark mark='c'/> Agora shows why. Two villages with the same demand: fish can be "
            "carried between them for a dollar, haircuts can't. Before any trade, fish cost three dollars in one "
            "and nine in the other. Once fish are carried, the prices are five fifty and six fifty: a gap of "
            "exactly the dollar it costs to carry one. The haircuts stay eight dollars and four. "
            "<bookmark mark='d'/> Radford saw the same thing: one price across his permanent camp, where everyone "
            "could read the boards, and two cigarettes in twenty across a single hut in a transit camp, where "
            "nobody could."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc.head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
