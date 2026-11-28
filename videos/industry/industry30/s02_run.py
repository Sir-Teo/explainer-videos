from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


def value_table(U, highlight=None):
    rows = [["", "1st block", "2nd", "3rd", "4th"]]
    for n, vals in zip(U["names"], U["values"]):
        rows.append([n] + [f"${v:.1f}bn" for v in vals])
    cols = [None] + [[YOU if i == 0 else RIVALS[i - 1]] + [WHITE] * 4 for i in range(4)]
    t = table(rows, col_x=[-4.6, -2.2, -0.6, 1.0, 2.6], top=2.0, row_h=0.55, size=17, colors=cols)
    return t


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: bid for spectrum", "Eight blocks of airwaves, four bidders. How many do you bid for?",
             "Chapter one. Run it. The government is auctioning eight identical blocks of airwaves. You and three rivals "
             "want them. The price rises until nobody wants more blocks than there are. How do you bid?",
             lit=("unit", "moat"))
        self.rules()
        self.values()
        self.why()
        self.sincere()
        self.rounds()
        self.reduce()
        self.everyone()
        self.seller()
        self.lesson()

    def rules(self):
        U = R["run"]
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.1, height=0.7, stroke_width=2, stroke_color=WIRELESS,
                                           fill_color="#1B2433", fill_opacity=1) for _ in range(U["supply"])]).arrange(RIGHT, buff=0.18)
        labs = VGroup(*[tx(f"block {i + 1}", 13, GREY_A).move_to(b) for i, b in enumerate(blocks)])
        g = VGroup(blocks, labs).move_to([0, 1.6, 0])
        clock = VGroup(Circle(radius=0.8, stroke_color=TOWER, stroke_width=4), Line(ORIGIN, UP * 0.6, stroke_color=TOWER, stroke_width=4),
                       tx("the price per block rises", 16, TOWER)).arrange(DOWN, buff=0.2).move_to([0, -1.3, 0])
        clock[1].move_to(clock[0].get_center() + UP * 0.3)
        rule = tx("each bidder says how many blocks it wants at this price; when demand is no more than 8, everyone pays the same price",
                  15, GREY_A).to_edge(DOWN, buff=0.8)
        if rule.width > 13:
            rule.scale_to_fit_width(13)
        tag = estimate_tag("the Works: an ascending clock auction with one price for all, as many spectrum auctions are run", size=12)
        beat(self,
             f"Here are the {U['supply']} blocks. <bookmark mark='a'/> The auctioneer calls out a price per block, and "
             "raises it round by round. <bookmark mark='b'/> At each price, every bidder says how many blocks it wants. "
             "When the blocks wanted are no more than the blocks on offer, the auction stops, and every winner pays that "
             "last price for every block it wins.",
             base=[g, tag], steps=[clock, rule])

    def values(self):
        U = R["run"]
        t = value_table(U)
        note = tx("what each block is worth to each bidder, in the Works: the first is worth most, the fourth least", 16, GREY_A).to_edge(DOWN, buff=1.0)
        tag = estimate_tag("the Works: every value is this series' illustration", size=12)
        v = U["values"]
        beat(self,
             "Each bidder knows what a block is worth to it, from its own business case: more airwaves mean more traffic "
             "carried without building more towers. <bookmark mark='a'/> To you, the first block is worth "
             f"{v[0][0]:.1f} billion dollars, the second {v[0][1]:.1f}, the third {v[0][2]:.1f}, the fourth {v[0][3]:.1f}. "
             "<bookmark mark='b'/> Rival A is small and values blocks less. Rival B wants two badly. Rival C wants three. "
             "You do not know their numbers; they do not know yours.",
             base=[tag], steps=[VGroup(t[0], t[1]), VGroup(t[2:], note)])

    def why(self):
        tw = VGroup(*[draw.cell_tower(1.3) for _ in range(6)]).arrange(RIGHT, buff=0.35).move_to([-2.6, 1.4, 0])
        tw2 = VGroup(*[draw.cell_tower(1.3) for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to([3.6, 1.4, 0])
        l1 = tx("traffic carried with little spectrum: many towers", 16, BAD).next_to(tw, DOWN, buff=0.25)
        l2 = tx("the same traffic with more: fewer towers", 16, GOOD).next_to(tw2, DOWN, buff=0.25)
        g = bullets(["the first block lets you serve customers you would otherwise lose", "the second saves building some towers",
                     "the third and fourth save less: you value each extra block less"], size=17).move_to([0, -1.6, 0])
        tag = estimate_tag("this series' reading of where a bidder's values come from", size=12)
        beat(self,
             "Where do the values come from? In this series' reading, from towers you will not have to build. "
             "<bookmark mark='a'/> With little spectrum, carrying more traffic means more towers, closer together. "
             "<bookmark mark='b'/> With more, the same towers carry more. <bookmark mark='c'/> The first block lets you keep "
             "customers you would otherwise lose to slow service, the second saves a lot of building, and each block after "
             "that saves less. That is why every bidder's values fall from the first block to the fourth.",
             base=[tag], steps=[VGroup(tw, l1), VGroup(tw2, l2), g])

    def sincere(self):
        U = R["run"]
        r = U["runs"][4]
        path = {p: d for p, d in r["path"]}
        ch = line_chart({"blocks wanted": (path, WIRELESS)}, x=(0, 7), y=(0, 16), xticks=[0, 1, 2, 3, 4, 5, 6, 7],
                        yticks=[0, 4, 8, 12, 16], xfmt=lambda v: f"${v:.0f}bn", yfmt=lambda v: f"{v:.0f}",
                        ylabel="the Works: blocks wanted by all four bidders, as the price per block rises", width=8.6, height=3.6,
                        center=(-1.2, 0.4), label_end=False)
        sup = DashedLine(ch.ax.c2p(0, U["supply"]), ch.ax.c2p(7, U["supply"]), stroke_color=GREY_B, stroke_width=2)
        sl = tx("8 blocks on offer", 13, GREY_B).next_to(ch.ax.c2p(0.1, U["supply"]), DOWN, buff=0.08, aligned_edge=LEFT)
        m = marker(ch.ax, r["price"], sum(r["won"]), f"stops at ${r['price']:.2f}bn", BAD, side=UP)
        c = stat_cards([(f"{r['won'][0]}", "blocks you win", YOU), (f"${r['price']:.2f}bn", "price per block", ALL),
                        (f"${r['surplus'][0]:.2f}bn", "value less price, for you", GOOD)], y=-2.6, size=30, span=11)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "First, bid honestly: ask for every block worth more to you than the price. <bookmark mark='a'/> At low "
             "prices everyone wants more than there is. As the price climbs, bidders drop the blocks they value least. "
             f"<bookmark mark='b'/> The demand falls to eight at {r['price']:.2f} billion dollars a block. "
             f"<bookmark mark='c'/> You win {r['won'][0]} blocks, worth {sum(U['values'][0][:r['won'][0]]):.1f} billion to "
             f"you, and pay {r['price'] * r['won'][0]:.2f} billion: <bookmark mark='d'/> you are {r['surplus'][0]:.2f} billion "
             "better off.",
             base=[ch.frame, sup, sl, tag], steps=[ch.lines["blocks wanted"], m, VGroup(c[0], c[1]), c[2]])

    def rounds(self):
        U = R["run"]
        K = U["clock"]
        rows = [["price per block", "you", "rival A", "rival B", "rival C", "wanted"]]
        for p, d in K.items():
            rows.append([f"${p:.2f}bn"] + [str(x) for x in d] + [str(sum(d))])
        cols = [None] + [[WHITE, YOU, RIVALS[0], RIVALS[1], RIVALS[2], (GOOD if sum(d) <= U["supply"] else BAD)] for d in K.values()]
        t = table(rows, col_x=[-5.0, -2.6, -1.0, 0.6, 2.2, 4.0], top=2.2, row_h=0.6, size=17, colors=cols)
        tag = estimate_tag("the Works: blocks each bidder wants, bidding honestly, round by round", size=12)
        beat(self,
             "Here are the rounds, bidding honestly. <bookmark mark='a'/> At three billion dollars a block, fourteen "
             "blocks are wanted for eight on offer. <bookmark mark='b'/> At four, every rival sheds a block; at five, rival "
             "A is down to one and rival B to two. <bookmark mark='c'/> At six you still want all four, and at six and a "
             "half rival A is gone. <bookmark mark='d'/> Only at six and three-quarters do you drop your fourth block, and "
             "demand falls to eight.",
             base=[tag, t[0]], steps=[t[1], VGroup(t[2], t[3]), VGroup(t[4], t[5]), t[6]])

    def reduce(self):
        U = R["run"]
        a, b = U["runs"][4], U["runs"][2]
        items = [("bid for every block you value", a["surplus"][0], BAD, f"{a['won'][0]} blocks at ${a['price']:.2f}bn: ${a['surplus'][0]:.2f}bn"),
                 ("bid for two blocks only", b["surplus"][0], GOOD, f"{b['won'][0]} blocks at ${b['price']:.2f}bn: ${b['surplus'][0]:.2f}bn")]
        rows = hbars(items, max_value=11, x0=-0.6, top=0.9, row=1.3, length=4.6, size=17, bar_h=0.6)
        lab = tx("the Works: what you are left with, value less price", 17, GREY_A).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "Now try the other way. <bookmark mark='a'/> You said you wanted three blocks, and that third block kept the "
             f"price rising: you paid {a['price']:.2f} on all three. <bookmark mark='b'/> Instead, ask for just two from the "
             f"start. The rivals' demand alone falls to six at {b['price']:.2f}, so the auction stops there. You win one "
             f"block fewer, but pay {a['price'] - b['price']:.0f} billion less on each of the two you win, and end "
             f"{b['surplus'][0]:.2f} billion better off instead of {a['surplus'][0]:.2f}.",
             base=[rows.axis, lab, tag], steps=[rows[0], rows[1]])

    def everyone(self):
        U = R["run"]
        a, b = U["runs"][4], U["runs"][2]
        rows = [["", "you", "rival A", "rival B", "rival C", "the government"],
                ["honest bidding"] + [f"${x:.2f}" for x in a["surplus"]] + [f"${a['revenue']:.0f}bn"],
                ["you ask for two"] + [f"${x:.2f}" for x in b["surplus"]] + [f"${b['revenue']:.0f}bn"]]
        t = table(rows, col_x=[-4.8, -2.4, -0.8, 0.8, 2.4, 4.6], top=1.4, row_h=0.8, size=18,
                  colors=[None, [WHITE, BAD, BAD, BAD, BAD, GOOD], [WHITE, GOOD, GOOD, GOOD, GOOD, BAD]])
        lab = tx("the Works: each bidder's value less what it paid ($bn), and what the auction raised", 16, GREY_A).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "And look who else gains. <bookmark mark='a'/> With honest bidding the auction raised "
             f"{a['revenue']:.0f} billion dollars for the government. <bookmark mark='b'/> When you hold back, the price "
             f"stops lower for everyone: every rival is better off too, and the auction raises only {b['revenue']:.0f} "
             "billion. Auction designers spend careers on rules that make this harder, because the bidders have every "
             "reason to find it.",
             base=[lab, tag, t[0]], steps=[t[1], t[2]])

    def seller(self):
        g = VGroup(tx("What a government auctioneer can do, in this series' reading", 21, WHITE, bold=True),
                   tx("set a reserve price below which no block is sold", 18, TOWER),
                   tx("cap how much any one bidder may win, to keep more networks alive", 18, WIRELESS),
                   tx("sell more blocks at once, so holding back gains less", 18, GOOD),
                   tx("and remember it is not maximising revenue alone: it wants the airwaves used", 18, ALL)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading; Economics, Built's auction part works through the designs", size=12)
        beat(self,
             "The seller is not helpless. In this series' reading, <bookmark mark='a'/> it can set a reserve price, below "
             "which nothing sells. <bookmark mark='b'/> It can cap how much one bidder may win, to keep more networks in "
             "the market. <bookmark mark='c'/> It can offer more blocks at once, so that holding back gains less. "
             "<bookmark mark='d'/> And it has to remember that the point is not the money alone: an airwave sold for a "
             "fortune to a company that cannot afford to build on it is wasted.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])

    def lesson(self):
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx("airwaves are sold like land, at whatever the bidders will pay", 18, WIRELESS),
                   tx("one price for all means each bidder's demand raises what everyone pays", 18, TOWER),
                   tx("so wanting less can leave a bidder richer, and the seller poorer", 18, GOOD),
                   tx("the operator pays for the spectrum before it has earned a cent from it", 18, BAD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' auction; Economics, Built covers auction design", size=12)
        beat(self,
             "So: <bookmark mark='a'/> the airwaves a phone network needs are sold like land, at whatever bidders will "
             "pay. <bookmark mark='b'/> With one price for all, your own demand raises what you pay, <bookmark mark='c'/> "
             "so asking for less can leave you richer. <bookmark mark='d'/> And whatever the price, the operator pays it "
             "before it has earned a cent, often tens of billions, then must build the network to use it.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
