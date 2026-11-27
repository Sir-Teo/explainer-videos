from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Mortgage(VoiceoverScene):
    def construct(self):
        card(self, 5, "The thirty-year loan", "How does the loan set the price?",
             "Chapter five. The thirty-year loan. Most homes are bought with borrowed money, and in America most of it is "
             "lent at a rate fixed for thirty years.", lit=("dollar", "change"))
        self.rate()
        self.share()
        self.amort()
        self.fannie()
        self.lock()
        self.delinq()
        self.debt()

    def rate(self):
        M = R["mortgage"]
        ch = line_chart({"30-year rate": (M["rate"], LOAN)}, x=(1971, 2025), y=(0, 18), xticks=[1971, 1980, 1990, 2000, 2010, 2020, 2025],
                        yticks=[0, 3, 6, 9, 12, 15, 18], yfmt=lambda v: f"{v:.0f}%", ylabel="30-year fixed mortgage rate, yearly average",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = max(M["rate"], key=M["rate"].get)
        lo = min(M["rate"], key=M["rate"].get)
        m1 = marker(ch.ax, pk, M["rate"][pk], f"{pk}: {M['rate'][pk]:.1f}%", BAD, side=RIGHT)
        m2 = marker(ch.ax, lo, M["rate"][lo], f"{lo}: {M['rate'][lo]:.1f}%", GOOD, side=DOWN)
        m3 = marker(ch.ax, 2025, M["rate"][2025], f"2025: {M['rate'][2025]:.1f}%", LOAN, side=UP)
        src = source("Freddie Mac, Primary Mortgage Market Survey, via FRED", size=12)
        beat(self,
             f"The price of the loan has swung more than the price of the house. <bookmark mark='a'/> In {pk} a thirty-year "
             f"mortgage cost {M['rate'][pk]:.1f} per cent. <bookmark mark='b'/> In {lo}, {M['rate'][lo]:.1f} per cent. "
             f"<bookmark mark='c'/> In 2025, {M['rate'][2025]:.1f}, and by November 2026 it was back above seven.",
             base=[ch.frame, src], steps=[[ch.lines["30-year rate"], m1], m2, m3])

    def share(self):
        M = R["mortgage"]["pay_share"]
        ch = line_chart({"payment share": ({y: 100 * v for y, v in M.items()}, PRICE)}, x=(1984, 2025), y=(15, 50),
                        xticks=[1984, 1990, 2000, 2006, 2012, 2020, 2025], yticks=[20, 30, 40, 50], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="mortgage payments on a median new house as a share of median household income",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        lo = min(M, key=M.get)
        m1 = marker(ch.ax, 1984, 100 * M[1984], f"1984: {100 * M[1984]:.0f}%", BAD, side=RIGHT)
        m2 = marker(ch.ax, lo, 100 * M[lo], f"{lo}: {100 * M[lo]:.0f}%", GOOD, side=DOWN)
        m3 = marker(ch.ax, 2025, 100 * M[2025], f"2025: {100 * M[2025]:.0f}%", PRICE, side=UP)
        tag = estimate_tag("this series' arithmetic: 10% down, 30 years, principal and interest only", size=12)
        src = source("Census and HUD; Freddie Mac; Census median household income; via FRED", size=12)
        beat(self,
             "Put price and rate together, and compare with income. <bookmark mark='a'/> In 1984, with rates in the "
             f"teens, the payments on a median new house took {100 * M[1984]:.0f} per cent of a median household's income. "
             f"<bookmark mark='b'/> In {lo}, with cheap money, {100 * M[lo]:.0f} per cent. <bookmark mark='c'/> In 2025, "
             f"{100 * M[2025]:.0f}. The house got dearer and the loan got cheaper for thirty years; since 2021 both have "
             "moved against the buyer at once.",
             base=[ch.frame, tag, src], steps=[[ch.lines["payment share"], m1], m2, m3])

    def fannie(self):
        M = R["mortgage"]
        c = stat_cards([(f"${M['debt_total']:.1f}tn", "of American residential mortgage debt, September 2025", LOAN),
                        (f"{M['share']}%", "of it owned or guaranteed by Fannie Mae", PRICE),
                        (f"${M['book']:.1f}tn", "Fannie Mae's guaranty book", GOOD)], y=1.0, size=40, span=12)
        chain = VGroup(tx("buyer", 18, HOUSE, bold=True), tx("lender", 18, LOAN, bold=True), tx("Fannie or Freddie", 18, PRICE, bold=True),
                       tx("bond investors", 18, GOOD, bold=True)).arrange(RIGHT, buff=1.0).move_to([0, -1.5, 0])
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.1, stroke_width=3, stroke_color=GREY_B,
                                max_tip_length_to_length_ratio=0.3) for i in range(3)])
        src = source("Fannie Mae, Form 10-K for 2025", size=12)
        beat(self,
             "Who lends thirty years at a fixed rate? Often not the bank that signs the loan. <bookmark mark='a'/> Of the "
             f"{M['debt_total']:.0f} trillion dollars Americans owed on homes in September 2025, <bookmark mark='b'/> "
             f"Fannie Mae alone owned or guaranteed {M['share']} per cent, <bookmark mark='c'/> a guaranty book of "
             f"{M['book']:.1f} trillion dollars. <bookmark mark='d'/> The chain: a lender makes the loan, sells it to Fannie "
             "Mae or Freddie Mac, which guarantee it against default and pool it into bonds that investors around the "
             "world buy. The investor takes the interest-rate risk; the government-sponsored guarantor takes the risk of "
             "default; the borrower gets a fixed rate for thirty years.",
             base=[src], steps=[c[0], c[1], c[2], [chain, arrows]])

    def lock(self):
        M = R["mortgage"]
        q = quote(["'most of our single-family conventional guaranty book of business as of December 31, 2025 had an",
                   "interest rate lower than the U.S. weekly average 30-year fixed-rate mortgage rate ... even if interest",
                   "rates decline to 5%, most of the borrowers ... still would not be incentivized to refinance.'"],
                  "Fannie Mae, Form 10-K for 2025", size=17).move_to([0, 1.3, 0])
        key = draw.house_key(1.6).move_to([0, -1.3, 0])
        note = tx("a cheap fixed loan cannot move house with its owner", 19, PRICE, bold=True).next_to(key, DOWN, buff=0.3)
        src = source("Fannie Mae, Form 10-K for 2025", size=12)
        beat(self,
             "The thirty-year fixed loan has a side effect. <bookmark mark='a'/> Fannie Mae's report says most of the "
             f"loans it guarantees carry rates below the {M['lock']} per cent of December 2025, and that even if rates fell "
             "to five, most of those borrowers would have no reason to refinance. <bookmark mark='b'/> An owner who sells "
             "gives up a cheap loan and takes a dear one on the next house. In this series' reading, that is why many stay "
             "put, fewer existing homes come up for sale, and more buyers turn to builders, who can buy down the rate.",
             base=[src], steps=[q, [key, note]])

    def debt(self):
        M = R["mortgage"]
        a, b = M["orig"]
        ra, rb = M["refi"]
        c = stat_cards([(f"${M['hh_debt']:.1f}tn", "owed by households on homes of one to four families, 2026", LOAN),
                        (f"${a:.2f}tn", "new single-family mortgages made in 2025 (Fannie Mae's estimate)", GOOD),
                        (f"${b:.2f}tn", "its forecast for 2026, made in February", PRICE)], y=0.6, size=38, span=12.4)
        src = source("Federal Reserve, Financial Accounts (Z.1), via FRED; Fannie Mae, Form 10-K for 2025", size=12)
        beat(self,
             "And the size of the trade. <bookmark mark='a'/> American households owed "
             f"{M['hh_debt']:.1f} trillion dollars on their homes in 2026. <bookmark mark='b'/> In 2025 lenders made about "
             f"{a:.2f} trillion dollars of new home loans, {ra:.0f} billion of them refinancings. <bookmark mark='c'/> In "
             f"February 2026 Fannie Mae forecast {b:.2f} trillion for 2026, with refinancing up to {rb:.0f} billion, on "
             "the expectation of lower rates. Rates went up instead; chapter nine comes back to that forecast.",
             base=[src], steps=[c[0], c[1], c[2]])

    def amort(self):
        E = R["extra"]
        L = E["loan"]
        a, b = E["bal5"][2.735], E["bal5"][7.328]
        items = [("at 2.7%", L - a, GOOD, f"${(L - a) / 1e3:.0f}k repaid"), ("at 7.3%", L - b, BAD, f"${(L - b) / 1e3:.0f}k repaid")]
        rows = hbars(items, max_value=45000, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx(f"a ${L / 1e3:.0f}k thirty-year loan: how much is paid off in the first five years", 16, GREY_A).move_to([0, 2.1, 0])
        tag = estimate_tag("this series' arithmetic: level monthly payments", size=12)
        beat(self,
             f"A thirty-year loan also pays off slowly, and more slowly when rates are high. Take a {L / 1e3:.0f} thousand "
             "dollar loan, ninety per cent of the median new house in 2026. <bookmark mark='a'/> At the 2021 rate, five "
             f"years of payments would pay off about {(L - a) / 1e3:.0f} thousand dollars of it. <bookmark mark='b'/> At "
             f"the 2026 rate, about {(L - b) / 1e3:.0f} thousand: the rest of a much larger payment is interest. A buyer at "
             "today's rates pays down the loan at about half the speed.",
             base=[rows.axis, lab, tag], steps=[rows[0], rows[1]])

    def delinq(self):
        D = R["extra"]["delinq"]
        ch = line_chart({"delinquency": ({y: v for y, v in D.items() if y <= 2025}, BAD)}, x=(1991, 2025), y=(0, 12),
                        xticks=[1991, 1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 3, 6, 9, 12], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="single-family mortgages at commercial banks that are delinquent", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        pk = max(D, key=D.get)
        m1 = marker(ch.ax, pk, D[pk], f"{pk}: {D[pk]:.1f}%", BAD, side=UP)
        m2 = marker(ch.ax, 2025, D[2025], f"2025: {D[2025]:.1f}%", GOOD, side=UP)
        src = source("Federal Reserve, delinquency rate on single-family residential mortgages, all commercial banks, via FRED", size=12)
        beat(self,
             "And the loans are being paid. <bookmark mark='a'/> After the crash, in "
             f"{pk}, {D[pk]:.1f} per cent of single-family mortgages at American banks were delinquent. "
             f"<bookmark mark='b'/> In 2025, {D[2025]:.1f} per cent. A borrower with a fixed rate pays the same when "
             "rates rise; only those who need a new loan pay more. In this series' reading, the squeeze of 2026 falls on "
             "buyers and builders, not on owners.",
             base=[ch.frame, src], steps=[[ch.lines["delinquency"], m1], m2])
