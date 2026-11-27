from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Defence(VoiceoverScene):
    def construct(self):
        card(self, 10, "Defence: one buyer", "What happens to a business with one customer?",
             "Chapter ten. Defence. Here the airliner's logic turns over: instead of many airlines and two makers, a "
             "handful of makers and, for each country, one buyer.", lit=("unit", "dollar", "moat"))
        self.buyer()
        self.contracts()
        self.margins()
        self.spending()

    def buyer(self):
        D = R["defence"]
        jet = draw.fighter(3.4, DEFENCE).move_to([-4.2, 0.8, 0])
        W = 7.0
        x0 = -1.2
        segs = [(D["usg"] - 63, "rest of the US government", "#4E9A5E"), (63, "the Department of Defense", DEFENCE),
                (100 - D["usg"], "other countries and commercial", GREY_B)]
        segs = [segs[1], segs[0], segs[2]]
        bar = VGroup()
        x = x0
        for v, lab, col in segs:
            r_ = Rectangle(width=W * v / 100, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([x + W * v / 200, 1.2, 0])
            r_.grow = LEFT
            bar.add(VGroup(r_, tx(f"{v:.0f}%", 16, "#0E1117", bold=True).move_to(r_)))
            x += W * v / 100
        keys = VGroup(*[tx(f"{lab}", 14, col) for v, lab, col in segs]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bar, DOWN, buff=0.25).align_to(bar, LEFT)
        f35 = VGroup(tx(f"the F-35 alone: {D['f35']}% of Lockheed's sales", 20, DEFENCE, bold=True),
                     tx("seven partner countries and twelve foreign military sales customers", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.3, -1.6, 0])
        head_ = tx("Lockheed Martin's sales, 2025", 20, WHITE, bold=True).next_to(bar, UP, buff=0.25).align_to(bar, LEFT)
        src = source("Lockheed Martin, Form 10-K 2025", size=12)
        beat(self,
             "Take Lockheed Martin, the maker of the F-35 fighter. <bookmark mark='a'/> In 2025, sixty-three per cent of "
             "its sales went to one customer, the US Department of Defense, which the filing now calls the Department of "
             f"War, and {D['usg']} per cent to the US government as a whole. <bookmark mark='b'/> The rest came from "
             "other countries and commercial customers. <bookmark mark='c'/> And one programme, the "
             f"F-35, was {D['f35']} per cent of everything Lockheed sold. A company like this does not compete for "
             "customers. It competes for contracts, years apart, from a buyer who also writes the rules.",
             base=[jet, head_, src], steps=[bar[0], [bar[1], bar[2], keys], f35])

    def contracts(self):
        D = R["defence"]

        def box(x, title, col, lines):
            b = RoundedRectangle(corner_radius=0.15, width=5.6, height=2.6, stroke_color=col, stroke_width=2, fill_opacity=0).move_to([x, 0.6, 0])
            t = VGroup(tx(title, 20, col, bold=True), *[tx(l, 15, WHITE) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(b)
            return VGroup(b, t)
        cp = box(-3.1, f"cost-reimbursable: {D['costplus']}% of Lockheed's sales", GOOD,
                 ["the buyer pays the costs, plus a fee", "overruns are mostly the buyer's problem", "low margin, low risk"])
        fp = box(3.1, f"fixed-price: the other {100 - D['costplus']}%", BAD,
                 ["the maker agrees a price up front", "overruns are the maker's problem", "more margin, if it goes well"])
        warn = VGroup(tx(f"Boeing's defence arm, 2024: ${D['bds']:.1f}bn of extra losses", 18, BOEING, bold=True),
                      tx("on five fixed-price development programmes: the KC-46A tanker, the T-7A trainer, Starliner,", 15, GREY_A),
                      tx("the new Air Force One and the MQ-25 drone", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([0, -1.9, 0])
        src = source("Lockheed Martin, Form 10-K 2025; The Boeing Company, Form 10-K 2025", size=12)
        beat(self,
             "How the buyer pays matters as much as how much. <bookmark mark='a'/> Under a cost-reimbursable contract "
             "the government pays what the work costs plus a fee: little risk, and a modest margin. About "
             f"{D['costplus']} per cent of Lockheed's sales are like that. <bookmark mark='b'/> Under a fixed-price "
             "contract the maker names its price up front and keeps whatever is left, or pays for the overrun. "
             "<bookmark mark='c'/> Fixed prices on work that has never been done before can be ruinous. In 2024 Boeing's "
             f"defence arm booked {D['bds']:.1f} billion dollars of extra losses on five fixed-price development "
             "programmes, among them a tanker, a trainer jet, the Starliner space capsule and the new Air Force One.",
             base=[src], steps=[cp, fp, warn])

    def margins(self):
        D = R["defence"]
        names = {"LMT": "Lockheed Martin", "RTX": "RTX (Raytheon, Pratt & Whitney)", "NOC": "Northrop Grumman",
                 "GD": "General Dynamics", "LHX": "L3Harris", "HII": "Huntington Ingalls (warships)"}
        order = sorted(D["margins"], key=lambda k: -D["margins"][k])
        items = [(names[k], 100 * D["margins"][k], DEFENCE, f"{100 * D['margins'][k]:.1f}% on ${D['rev'][k]:.0f}bn") for k in order]
        rows = hbars(items, max_value=12, x0=0.2, top=1.6, row=0.7, length=4.6, size=16)
        avg = R["suppliers"]["avg"]
        note = tx(f"their averages 2015-2025 run from {100 * min(avg[k] for k in D['margins']):.1f}% to "
                  f"{100 * max(avg[k] for k in D['margins']):.1f}%: modest, and steady", 15, GREY_A).to_edge(DOWN, buff=0.75)
        src = source("Forms 10-K of the six companies (net income over revenue, latest fiscal year), via SEC company facts",
                     size=12)
        beat(self,
             "So what does a defence prime earn? <bookmark mark='a'/> Here are six of America's largest defence "
             "contractors in their latest year: profit margins between five and ten per cent. <bookmark mark='b'/> Over "
             "the decade they stayed in a narrow band, mostly between five and eleven per cent, while Boeing's swung from "
             "plus ten to minus twenty. Their buyer's budget does not follow the business cycle. The price of that "
             "steadiness is a ceiling: a buyer who pays costs plus a fee, and can see those costs, does not let the "
             "margin run far.",
             base=[rows.axis, head("Defence primes: net income as a share of revenue"), src], steps=[rows, note])

    def spending(self):
        D = R["defence"]
        real = {y: v for y, v in D["real"].items()}
        ch = line_chart({"US defence": (real, DEFENCE)}, x=(1947, 2025), y=(0, 1300),
                        xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2025], yticks=[0, 250, 500, 750, 1000, 1250],
                        yfmt=lambda v: f"${v:,.0f}bn", ylabel="US federal defence spending, $bn a year in 2025 prices",
                        width=9.8, height=4.5, center=(-0.4, -0.45), label_end=False)
        ax = ch.ax
        ms = VGroup(*[marker(ax, y, real[y], lab, DEFENCE if y != 2025 else PRICE, side=UP, size=13) for y, lab in
                      ((1953, "Korea"), (1968, "Vietnam"), (1987, "the 1980s build-up"), (2010, "Iraq and Afghanistan"))])
        m25 = marker(ax, 2025, real[2025], f"2025: ${real[2025]:,.0f}bn", PRICE, side=LEFT)
        lo = marker(ax, 1998, real[1998], f"after the Cold War: ${real[1998]:,.0f}bn", BAD, side=DOWN)
        src = source("US Bureau of Economic Analysis, national defense consumption expenditures and gross investment (via "
                     "FRED, FDEFX), deflated by the CPI-U (BLS, via FRED)", size=12)
        beat(self,
             "And the budget itself. <bookmark mark='a'/> Here is America's federal defence spending since 1947, in "
             "today's dollars. It rises in waves: Korea, Vietnam, the build-up of the 1980s, the wars in Iraq and "
             "Afghanistan. <bookmark mark='b'/> After the Cold War it fell by about a third. <bookmark mark='c'/> In "
             f"2025 it was about {real[2025]:,.0f} billion dollars a year, within a tenth of its post-war peak of 2010. For the makers, the waves are slow and visible "
             "years ahead, in budgets argued over in public.",
             base=[ch.frame, src], steps=[[ch.lines["US defence"], ms], lo, m25])
