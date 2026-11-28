from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.day1()
        self.ouch()
        self.growth()
        self.mix()
        self.profit()
        self.title()

    def day1(self):
        H = R["hook"]
        lap = draw.laptop(2.4).move_to([-4.2, 1.4, 0])
        q = quote(["'But this is Day 1 for the Internet and, if we execute well, for Amazon.com.'",
                   "'When forced to choose between optimizing the appearance of our GAAP accounting and maximizing the",
                   "present value of future cash flows, we'll take the cash flows.'"],
                  "Amazon.com, letter to shareholders, 1997", size=17).move_to([1.2, 1.4, 0])
        c = stat_cards([(f"{H['cust97']:.1f}m", "customers served by the end of 1997", SHOP),
                        (f"${H['l97']:.1f}m", "revenue in 1997, up 838%", MARKET)], y=-1.6, size=38, span=10)
        src = source("Amazon.com, 1997 letter to shareholders, reprinted with the 2008 letter (Form 8-K)", size=12)
        beat(self,
             "In early 1998 an online bookshop wrote to its shareholders. <bookmark mark='a'/> It said it was Day 1 for "
             "the internet, and that when it had to choose between looking profitable and building cash flow for the long "
             "run, it would take the cash flow. <bookmark mark='b'/> It had served "
             f"{H['cust97']:.1f} million customers. <bookmark mark='c'/> And it had sold {H['l97']:.0f} million dollars of "
             "books in a year: a rounding error for a big chain of bookshops.",
             base=[lap, src], steps=[q, c[0], c[1]])

    def ouch(self):
        H = R["hook"]
        q = quote(["'Ouch. It's been a brutal year for many in the capital markets and certainly for Amazon.com",
                   "shareholders. As of this writing, our shares are down more than 80% from when I wrote you last year.'"],
                  "Amazon.com, letter to shareholders, 2000", size=18).move_to([0, 1.4, 0])
        c = stat_cards([(f"-{H['down00']:.0f}%", "the share price, in a year", BAD), ("$2.76bn", "sales in 2000", SHOP),
                        ("20m", "customers in 2000", SHOP)], y=-1.3, size=38, span=11)
        src = source("Amazon.com, 2000 letter to shareholders (Form 8-K, April 2001)", size=12)
        beat(self,
             "Three years later the letter began with one word. <bookmark mark='a'/> Ouch. The shares had fallen by more "
             "than four-fifths in a year, and many of the online shops born in the same boom were gone. "
             "<bookmark mark='b'/> Yet sales had reached 2.76 billion dollars, <bookmark mark='c'/> from twenty million "
             "customers. The shop was growing; what nobody could see was how it would ever make money.",
             base=[src], steps=[q, c[0], VGroup(c[1], c[2])])

    def growth(self):
        H = R["hook"]
        ch = line_chart({"revenue": (H["hist"], SHOP)}, x=(2009, 2025), y=(0, 800), xticks=[2009, 2013, 2017, 2021, 2025],
                        yticks=[0, 200, 400, 600, 800], yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon's revenue, $bn a year",
                        width=8.8, height=4.4, center=(-1.0, -0.45), label_end=False)
        m0 = marker(ch.ax, 2009, H["hist"][2009], f"2009: ${H['hist'][2009]:.0f}bn", SHOP, side=UP)
        m1 = marker(ch.ax, 2025, H["rev"], f"2025: ${H['rev']:.0f}bn", SHOP, side=LEFT)
        src = source("Amazon.com, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Here is what happened next. <bookmark mark='a'/> By 2009 Amazon's revenue was "
             f"{H['hist'][2009]:.0f} billion dollars a year. <bookmark mark='b'/> By 2025 it was {H['rev']:.0f} billion, "
             f"from a company with about {H['emp'] / 1e6:.1f} million employees: as large as Walmart, the biggest shop on "
             "earth, from Part 31.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["revenue"], m0), m1])

    def mix(self):
        M = R["hook"]["mix"]
        tot = sum(M[k][2025] for k, _, _ in MIX)
        parts = [(name, M[k][2025], col) for k, name, col in MIX]
        bar = viz.bar_split(parts, tot, width=12.6, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup()
        for i, (name, v, col) in enumerate(parts):
            if v / tot < 0.03:
                continue
            labs.add(VGroup(tx(f"${v:.0f}bn", 19, col, bold=True), tx(name, 13, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2))
        hd = tx("Amazon's revenue in 2025, $717bn, by what was sold", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        brace = BraceBetweenPoints(bar[0].get_corner(UL), bar[1].get_corner(UR), direction=UP, color=SHOP)
        bt = tx("the shop: goods it bought and resold", 15, SHOP).next_to(brace, UP, buff=0.08)
        src = source("Amazon.com, Form 10-K for 2025: net sales by groups of similar products and services", size=12)
        beat(self,
             "But look at what that revenue is made of. <bookmark mark='a'/> About forty per cent is the shop you might "
             "picture: goods Amazon buys and sells to you, online and in its stores. <bookmark mark='b'/> A quarter is "
             "fees from other people's sales on its site. <bookmark mark='c'/> Then advertising, subscriptions like Prime, "
             "and a cloud computing business, AWS, that has nothing to do with shopping at all.",
             base=[hd, src], steps=[VGroup(bar[0], bar[1], labs[0], labs[1], brace, bt), VGroup(bar[2], labs[2]),
                                    VGroup(bar[3:], labs[3:])])

    def profit(self):
        H = R["hook"]
        O = H["op"]
        items = [("North America (shops)", O["na"][2025], SHOP, f"${O['na'][2025]:.1f}bn"),
                 ("International (shops)", O["intl"][2025], SHOP, f"${O['intl'][2025]:.1f}bn"),
                 ("AWS (the cloud)", O["aws"][2025], CLOUD, f"${O['aws'][2025]:.1f}bn")]
        rows = hbars(items, max_value=50, x0=-0.8, top=1.4, row=1.0, length=6.0, size=18, bar_h=0.55)
        hd = tx("Amazon's operating income in 2025, by segment", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"AWS: {100 * get('am32.aws') / H['rev']:.0f}% of revenue, "
                  f"{100 * H['aws_share']:.0f}% of operating income", 20, CLOUD, bold=True).move_to([0, -1.9, 0])
        src = source("Amazon.com, Form 10-K for 2025: segment information", size=12)
        beat(self,
             "And the profit. <bookmark mark='a'/> Amazon's shops in North America earned "
             f"{O['na'][2025]:.1f} billion dollars of operating income in 2025, <bookmark mark='b'/> and abroad "
             f"{O['intl'][2025]:.1f} billion. <bookmark mark='c'/> The cloud earned {O['aws'][2025]:.1f} billion. "
             f"<bookmark mark='d'/> A business that is {100 * get('am32.aws') / H['rev']:.0f} per cent of the revenue made "
             f"{100 * H['aws_share']:.0f} per cent of the profit. So what exactly is the online shop?",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2], note])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-two: e-commerce. Is selling online a shop, a toll road, or an "
                            "advertising business?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
