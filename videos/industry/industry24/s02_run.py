from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403

CH = {"0.02": ("add 2%", BAD), "0.08": ("add 8%, like the rivals", PRICE), "0.15": ("add 15%", MAKE)}


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: five tenders",
             "Five jobs come up for bid against four rivals. How much do you add to your estimate?",
             "Chapter one. Run it. You run a building contractor. Five jobs come up for tender this year, and for each "
             "one, you and four rivals will hand in a sealed price. The lowest price wins. How much should you add?",
             lit=("dollar", "moat"))
        self.setup_()
        self.example()
        self.curse()
        self.three()
        self.curve()
        self.answer()

    def setup_(self):
        U = R["run"]
        bp = draw.blueprint(1.8).move_to([-4.6, 1.5, 0])
        hats = VGroup(draw.hardhat(0.8, color=YOU), *[draw.hardhat(0.8, color=RIVAL) for _ in range(U["rivals"])]
                      ).arrange(RIGHT, buff=0.35).move_to([1.6, 1.8, 0])
        names = VGroup(*[tx(n, 13, YOU if i == 0 else GREY_B).next_to(h, DOWN, buff=0.1) for i, (h, n) in
                         enumerate(zip(hats, ["you", "rival", "rival", "rival", "rival"]))])
        facts = VGroup(tx(f"the job really costs ${U['cost']:.0f}m to build, but nobody knows that exactly", 17, WHITE),
                       tx(f"each bidder's estimate is off by about {100 * U['sd']:.0f}% either way", 17, GREY_A),
                       tx(f"the rivals add {100 * U['rival_markup']:.0f}% to their estimates", 17, RIVAL),
                       tx("the lowest sealed price wins, and is paid that price", 17, PRICE)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.4, -1.3, 0])
        est = estimate_tag("the Works: an illustrative tender", size=12)
        beat(self,
             f"Here is a job: a building that will really cost {U['cost']:.0f} million dollars to put up. "
             "<bookmark mark='a'/> Nobody knows that number exactly. Each bidder prices the drawings, the steel, the "
             f"concrete and the hours, and each estimate is off by about {100 * U['sd']:.0f} per cent, sometimes high, "
             f"sometimes low. <bookmark mark='b'/> Your four rivals add {100 * U['rival_markup']:.0f} per cent to their "
             "estimates for profit and risk. <bookmark mark='c'/> The client opens the envelopes and the lowest price "
             "wins, and is paid what it bid.",
             base=[bp, hats, names, est], steps=[facts[:2], facts[2], facts[3]])

    def example(self):
        ests = [96.0, 99.0, 101.0, 103.0, 106.0]
        order = [2, 0, 3, 1, 4]  # which bidder made which estimate (you have the 101)
        bids = {i: ests[k] * 1.08 for i, k in enumerate(order)}
        items = [("you" if i == 0 else f"rival {i}", bids[i], YOU if i == 0 else RIVAL, f"${bids[i]:.1f}m") for i in range(5)]
        rows = hbars(items, max_value=120, x0=-1.6, top=1.8, row=0.62, length=6.6, size=16, bar_h=0.36)
        true = DashedLine([-1.6 + 6.6 * 100 / 120, 2.2, 0], [-1.6 + 6.6 * 100 / 120, -1.0, 0], stroke_color=GOOD, stroke_width=2)
        tl = tx("true cost $100m", 14, GOOD, bold=True).next_to(true, UP, buff=0.08)
        win = min(bids, key=bids.get)
        note = tx(f"winner: the rival who estimated ${ests[order[win]]:.0f}m. It bid ${bids[win]:.1f}m and makes "
                  f"${bids[win] - 100:.1f}m, not the $8m it added", 18, PRICE, bold=True).move_to([0, -1.9, 0])
        est = estimate_tag("the Works: one tender, with illustrative estimates", size=12)
        beat(self,
             "Watch one tender. <bookmark mark='a'/> Everyone adds eight per cent to their own estimate. You estimated "
             "101 million and bid 109. <bookmark mark='b'/> The rival who estimated 96, four per cent too low, bids "
             f"{bids[win]:.1f} and wins. <bookmark mark='c'/> It meant to add eight million dollars of profit, and it will "
             f"make {bids[win] - 100:.1f}, because its estimate was the lowest, and the lowest estimate is usually too low. "
             "The tender does not pick the best builder; it picks the most optimistic estimate.",
             base=[rows.axis, est], steps=[rows, [true, tl], note])

    def curse(self):
        C = R["curse"]
        allp = {100 * e: v / 10 for e, v in zip(C["e"], C["all"])}
        wonp = {100 * e: v / 10 for e, v in zip(C["e"], C["won"])}
        ch = line_chart({"every bidder's estimate": (allp, RIVAL), "the winning estimate": (wonp, PRICE)}, x=(-20, 20),
                        y=(0, 1.3), xticks=[-20, -10, 0, 10, 20], yticks=[0], xfmt=lambda v: f"{v:+.0f}%",
                        yfmt=lambda v: "", ylabel="how often", width=9.4, height=4.2, center=(-0.6, -0.5), label_end=False)
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(0, 1.25), stroke_color=GOOD, stroke_width=2)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(n, 14, c)).arrange(RIGHT, buff=0.12)
                       for n, c in (("every bidder's estimate", RIVAL), ("the winning estimate", PRICE))]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 1.6, 0])
        xl = tx("estimate against the true cost", 14, GREY_B).next_to(ch.ax, DOWN, buff=0.45)
        m = marker(ch.ax, 100 * C["mean_won"], 0.05, f"on average {100 * C['mean_won']:.1f}%", PRICE, side=DOWN)
        est = estimate_tag("the Works: five bidders, estimates off by 5%, all adding 8%", size=12)
        beat(self,
             "Now every tender at once. <bookmark mark='a'/> Each bidder's estimate is right on average: as often too "
             "high as too low. <bookmark mark='b'/> But the estimates that win are not. They sit to the left, too low, "
             f"by {abs(100 * C['mean_won']):.1f} per cent on average. Economists call this the winner's curse: whoever "
             "wins an auction for something of uncertain value has probably overestimated what it is worth, or here, "
             "underestimated what it will cost.",
             base=[ch.frame, zero, key, xl, est], steps=[ch.lines["every bidder's estimate"], [ch.lines["the winning estimate"], m]])

    def three(self):
        Ch = R["run"]["choices"]
        rows = [["", "jobs won of five", "profit, five tenders", "margin on work won"]]
        cols = []
        for k in ("0.02", "0.08", "0.15"):
            v = Ch[k]
            rows.append([CH[k][0], f"{v['wins']:.1f}", ("-" if v["profit"] < 0 else "+") + f"${abs(v['profit']):.1f}m",
                         f"{100 * v['margin']:+.1f}%"])
            cols.append([CH[k][1]] * 4)
        tbl = table(rows, col_x=[-5.8, -1.6, 1.4, 4.2], top=1.4, row_h=0.8, size=19, colors=[None] + cols)
        est = estimate_tag("the Works: five tenders, expected values", size=12)
        beat(self,
             "So, how much to add? Three choices over the year's five tenders. <bookmark mark='a'/> Add two per cent and "
             f"you win about {Ch['0.02']['wins']:.1f} of the five jobs, but lose {abs(Ch['0.02']['profit']):.1f} million "
             f"dollars: on the work you win, a margin of {100 * Ch['0.02']['margin']:.1f} per cent. You win because you "
             "are cheapest, and you are cheapest because you guessed low. <bookmark mark='b'/> Add eight, like everyone "
             f"else, and you win one job in five on average and make {Ch['0.08']['profit']:.1f} million: a margin of "
             f"{100 * Ch['0.08']['margin']:.1f} per cent on what you won, not eight. <bookmark mark='c'/> Add fifteen and "
             f"you keep {100 * Ch['0.15']['margin']:.1f} per cent on the rare job you win, but most years you win "
             "nothing at all.",
             base=[tbl[0], est], steps=[tbl[1], tbl[2], tbl[3]])

    def curve(self):
        C = R["run"]["curve"]
        pts = {100 * float(k): v["profit"] for k, v in C.items()}
        win = {100 * float(k): v["win"] for k, v in C.items()}
        ch = line_chart({"profit per tender": (pts, PRICE)}, x=(0, 20), y=(-1.6, 0.6), xticks=[0, 4, 8, 12, 16, 20],
                        yticks=[-1.5, -1.0, -0.5, 0, 0.5], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: ("-" if v < 0 else "") + f"${abs(v):.1f}m",
                        ylabel="expected profit per tender", width=9.0, height=4.2, center=(-0.6, -0.4), label_end=False)
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(20, 0), stroke_color=GREY_B, stroke_width=1.5)
        B = R["run"]["best"]
        m = marker(ch.ax, 100 * B["markup"], B["profit"], f"best: add {100 * B['markup']:.0f}%, win {100 * B['win']:.0f}% of tenders",
                   GOOD, side=UP)
        xl = tx("what you add to your estimate", 14, GREY_B).next_to(ch.ax, DOWN, buff=0.45)
        est = estimate_tag("the Works' tender", size=12)
        beat(self,
             "The whole curve. <bookmark mark='a'/> Below about four per cent you lose money on average, however many "
             "jobs you win. <bookmark mark='b'/> The best markup here is about "
             f"{100 * B['markup']:.0f} per cent, winning {100 * B['win']:.0f} per cent of tenders and keeping "
             f"{100 * B['margin']:.1f} per cent of the revenue. Above it, you win too rarely to make up for the margin. "
             f"At {100 * B['markup']:.0f} per cent, about a third of the jobs you do win still lose money.",
             base=[ch.frame, zero, xl, est], steps=[ch.lines["profit per tender"], m])

    def answer(self):
        Ch = R["run"]["choices"]
        G = R["chain"]
        c = stat_cards([(f"{100 * Ch['0.02']['margin']:+.1f}%", "add 2%: win often, lose money", BAD),
                        (f"{100 * Ch['0.08']['margin']:+.1f}%", "add 8%: the margin you actually keep", PRICE),
                        (f"{100 * G['general']:.1f}%", "real general contractors' median net margin", GOOD)],
                       y=0.9, size=40, span=12)
        note = tx("The lowest bid wins, so the winner is usually the one who guessed lowest.", 20, WHITE, bold=True).move_to([0, -1.4, 0])
        est = estimate_tag("the Works' tender; SEC company facts for the real contractors", size=12)
        beat(self,
             "So the answer. <bookmark mark='a'/> Bid low and you fill your order book with losses. <bookmark mark='b'/> "
             f"Bid like everyone else and the eight per cent you add becomes about {100 * Ch['0.08']['margin']:.0f} per "
             f"cent in your accounts. <bookmark mark='c'/> And real American general contractors have kept about "
             f"{100 * G['general']:.0f} cents of each dollar of revenue as profit over the last five years. "
             "<bookmark mark='d'/> That is the first answer to this film's question: a sealed-bid business keeps very "
             "little, and much of what it keeps depends on how the contract is written. The next chapters follow the money.",
             base=[est], steps=[c[0], c[1], c[2], note])
