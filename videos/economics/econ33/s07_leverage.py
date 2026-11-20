from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Leverage(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Leverage, \ margins and fire sales", r"Why does borrowing make prices rise so high, and "
             r"fall so far?", "Chapter six. Leverage, margins and fire sales.",
             lit={1992: r"Shleifer and Vishny", 2009: r"Brunnermeier and Pedersen", 2010: r"Geanakoplos"},
             scale=("market",), horizon=("a day", "a year"))
        self.optimists()
        self.tree()
        self.spirals()

    def optimists(self):
        L = load("leverage")
        w, wo = L["with"], L["without"]
        line = NumberLine(x_range=[0, 1, 0.1], length=11.0, include_numbers=False, color=GREY_B).move_to(UP * 0.6)
        ends = VGroup(label(r"pessimists: \ $h = 0$", font_size=18, color=GREY_B).next_to(line, DOWN, buff=0.2)
                      .align_to(line, LEFT),
                      label(r"optimists: \ $h = 1$", font_size=18, color=GREY_B).next_to(line, DOWN, buff=0.2)
                      .align_to(line, RIGHT))

        def marker(h, col, txt):
            x = line.n2p(h)
            tick = Line(x + DOWN * 0.25, x + UP * 0.25, color=col, stroke_width=5)
            lab = label(txt, font_size=19, color=col).next_to(tick, UP, buff=0.1)
            return VGroup(tick, lab)

        m0 = marker(wo["h1"], CALM, rf"no borrowing: \ price {wo['p']:.2f}")
        m1 = marker(w["h1"], CRISIS, rf"with leverage: \ price {w['p']:.2f}")
        m1[1].shift(UP * 0.5)
        buyers = Line(line.n2p(w["h1"]), line.n2p(1), color=CRISIS, stroke_width=10, stroke_opacity=0.5)
        rows = VGroup(
            label(r"an asset pays 1 if the news is good, \ 0.2 if it is bad; \ each person $h$ believes good news "
                  r"with probability $h$", font_size=22, color=WHITE),
            label(rf"the average opinion values it at {w['average']:.2f}", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.5)
        foot = VGroup(
            label(r"with leverage, \ fewer and keener buyers own everything, \ borrowing 0.2 a unit, \ all a "
                  r"lender will lend safely", font_size=21, color=CRISIS),
            label(rf"the margin: \ {100 * w['margin']:.0f}\% down; \ the price is set by the person at "
                  rf"$h = {w['h1']:.2f}$", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Geanakoplos, \ ``The Leverage Cycle'', \ \emph{NBER Macroeconomics Annual} 24 (2010)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "John Geanakoplos asked what borrowing does to prices when people disagree. <bookmark mark='a'/> An "
            "asset pays one if the news is good and point two if it is bad. People differ in how likely they think "
            "good news is, from zero to one, and each has one unit of cash and one unit of the asset. "
            f"<bookmark mark='b'/> The average opinion values it at {w['average']:.1f}. <bookmark mark='c'/> "
            "Without borrowing, the optimists buy from the pessimists until their cash runs out, and the price is "
            f"set by the person at the margin: {wo['p']:.2f}. <bookmark mark='d'/> Now let buyers borrow, as much "
            "as a lender can lend with no risk, point two per unit, the asset's worst value. Fewer and keener "
            f"buyers can now own the whole supply, the marginal buyer is more optimistic, and the price rises to "
            f"{w['p']:.2f}. <bookmark mark='e'/> Leverage does not change anyone's opinion. It changes whose opinion "
            "sets the price."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(ends))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(m0, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(m1, shift=DOWN * 0.1), Create(buyers), FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def tree(self):
        C = load("leverage")["cycle"]
        d = load("leverage")["d"]

        def node(txt, col, pos):
            c = Circle(radius=0.5, color=col, stroke_width=3, fill_color=col, fill_opacity=0.12).move_to(pos)
            return VGroup(c, label(txt, font_size=24, color=col).move_to(pos))

        n0 = node(rf"{C['p0']:.2f}", WHITE, LEFT * 4.6 + DOWN * 0.2)
        nU = node(r"1", CALM, LEFT * 0.8 + UP * 1.6)
        nD = node(rf"{C['pD']:.2f}", CRISIS, LEFT * 0.8 + DOWN * 2.0)
        nDU = node(r"1", CALM, RIGHT * 2.8 + DOWN * 0.8)
        nDD = node(rf"{d:.1f}", CRISIS, RIGHT * 2.8 + DOWN * 3.0)
        edges = VGroup(*[Line(a[0].get_center(), b[0].get_center(), color=GREY_C, stroke_width=2.5, buff=0.5)
                         for a, b in ((n0, nU), (n0, nD), (nD, nDU), (nD, nDD))])
        e_lab = VGroup(label(r"good news", font_size=17, color=CALM).next_to(edges[0].get_center(), UL, buff=0.05),
                       label(r"bad news", font_size=17, color=CRISIS).next_to(edges[1].get_center(), DL, buff=0.05))
        side = VGroup(
            label(rf"today: \ margin {100 * C['margin0']:.0f}\%, \ leverage {C['leverage0']:.1f} to 1", font_size=21,
                  color=WHITE),
            label(r"bad news: \ the leveraged optimists are wiped out", font_size=21, color=CRISIS),
            label(rf"the new buyers are less sure: \ margin {100 * C['marginD']:.0f}\%, \ leverage "
                  rf"{C['leverageD']:.1f}", font_size=21, color=CRISIS),
            label(rf"price: \ {C['p0']:.2f} \ $\to$ \ {C['pD']:.2f}, \ a fall of {100 * (1 - C['pD'] / C['p0']):.0f}\%",
                  font_size=23, color=HOUSE),
            label(rf"to the old marginal buyer, \ the news cut the value by only "
                  rf"{100 * (1 - C['h0_value_at_D'] / C['fund0']):.0f}\%", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_corner(UR, buff=0.4)
        tag = published_tag(r"Geanakoplos (2010); \ computed here: \ two periods, \ agents uniform on $[0, 1]$",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Now let news arrive in two steps. The asset pays one unless the news is bad twice. "
            "<bookmark mark='a'/> Today the optimists buy with borrowed money, and lenders, looking one step ahead, "
            "lend up to the price after bad news, so buyers put down only "
            f"{100 * C['margin0']:.0f} percent: leverage of {C['leverage0']:.1f} to one. Solving for both prices at "
            f"once, the asset trades at {C['p0']:.2f}. <bookmark mark='b'/> Then the first piece of bad news "
            "arrives. The optimists who bought on credit lose everything they put down; they were the natural "
            "buyers, and they are gone. <bookmark mark='c'/> The asset must be held by the next most optimistic, "
            "who are less sure, and lenders, now facing more risk, ask for "
            f"{100 * C['marginD']:.0f} percent down. <bookmark mark='d'/> The price falls to {C['pD']:.2f}, "
            f"{100 * (1 - C['pD'] / C['p0']):.0f} percent. <bookmark mark='e'/> Yet for the person who set the "
            "price before, the news lowered the asset's worth by only "
            f"{100 * (1 - C['h0_value_at_D'] / C['fund0']):.0f} percent. The rest of the fall is the leverage cycle: "
            "the margins and the buyers changed together."
        ) as vo:
            self.play(FadeIn(n0), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(edges[0]), Create(edges[1]), FadeIn(nU), FadeIn(nD), FadeIn(e_lab))
            vo.wait_until("b")
            self.play(Indicate(nD, color=CRISIS), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(edges[2]), Create(edges[3]), FadeIn(nDU), FadeIn(nDD), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def spirals(self):
        chain = flow_chain([(r"prices fall", HOUSE), (r"losses on positions bought on credit", CRISIS),
                            (r"lenders raise margins", RATE), (r"holders must sell", CREDIT),
                            (r"the natural buyers are short of cash too", HOLD)], box_w=2.35, box_h=1.3, buff=0.42,
                           font_size=20).move_to(UP * 0.6)
        back = CurvedArrow(chain.boxes[-1].get_bottom() + DOWN * 0.1, chain.boxes[0].get_bottom() + DOWN * 0.1,
                           angle=-TAU / 6, color=CRISIS, stroke_width=3)
        notes = VGroup(
            label(r"Shleifer and Vishny (1992): \ fire sales: \ the best buyers are in the same trouble", font_size=20,
                  color=HOLD),
            label(r"Brunnermeier and Pedersen (2009): \ the margin spiral and the loss spiral", font_size=20,
                  color=RATE),
            label(r"2007--08: \ the haircuts lenders took on collateral rose sharply (Gorton and Metrick)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In markets this becomes a spiral. <bookmark mark='a'/> Prices fall; <bookmark mark='b'/> those who "
            "bought on credit take losses; <bookmark mark='c'/> lenders, seeing more risk, raise the margins they "
            "demand; <bookmark mark='d'/> holders must sell to meet them; <bookmark mark='e'/> and the natural "
            "buyers, the specialists who know the asset, are in the same trouble, so the asset goes to outsiders "
            "at a discount. Andrei Shleifer and Robert Vishny called these fire sales. <bookmark mark='f'/> Markus "
            "Brunnermeier and Lasse Pedersen showed how funding and market liquidity drain together, through the "
            "margin spiral and the loss spiral. <bookmark mark='g'/> In 2007 and 2008 the haircuts that repo "
            "lenders took on mortgage collateral rose sharply, the run on repo of Part twenty-six."
        ) as vo:
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            self.play(Create(back))
            self.play(FadeIn(notes[0]))
            vo.wait_until("f")
            self.play(FadeIn(notes[1]))
            vo.wait_until("g")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
