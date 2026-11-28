from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Agents(VoiceoverScene):
    def construct(self):
        card(self, 6, "The online agents", "Who sits between the traveller and the hotel, and what does it charge?",
             "Chapter six. The online agents. Between the traveller and the hotel sit a few websites that between them sell "
             "billions of nights a year.", lit=("dollar", "moat"))
        self.booking()
        self.models()
        self.marketing()
        self.supply()
        self.rules()
        self.airbnb()

    def booking(self):
        B = R["agents"]["bk"]
        c = stat_cards([(f"{B['nights'] / 1e3:.2f}bn", "room nights booked, 2025", AGENT),
                        (bn(B["gb"], 0), "of travel booked", AGENT),
                        (bn(B["rev"]), f"revenue: {100 * B['rev'] / B['gb']:.1f}% of bookings", BRAND),
                        (bn(B["op"]), "operating income", GOOD)], y=1.9, size=32, span=12.4)
        page = draw.web_page(4.6, cols=4, rows=2, sponsored=(0, 5), accent=AGENT).move_to([0, -1.2, 0])
        src = source("Booking Holdings, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Booking Holdings, the owner of Booking.com, Agoda, Priceline and KAYAK, booked "
             f"{B['nights'] / 1e3:.2f} billion room nights in 2025. <bookmark mark='b'/> With flights and car hire, travellers "
             f"booked {B['gb']:.0f} billion dollars of travel through it. <bookmark mark='c'/> It kept {B['rev']:.1f} billion "
             f"as revenue, {100 * B['rev'] / B['gb']:.1f} per cent, <bookmark mark='d'/> and its operating income was "
             f"{B['op']:.1f} billion: more than Marriott's and Hilton's put together.",
             base=[page, src], steps=list(c))

    def models(self):
        B = R["agents"]["bk"]
        items = [("agency: the hotel takes payment, pays a commission", B["gba"], AGENT, bn(B["gba"], 0) + " (-8.7%)"),
                 ("merchant: Booking takes payment, pays the hotel", B["gbm"], BRAND, bn(B["gbm"], 0) + " (+24.8%)")]
        rows = hbars(items, max_value=140, x0=1.0, top=1.0, row=1.3, length=4.2, size=17, bar_h=0.65)
        hd = tx("Booking Holdings' gross bookings in 2025, by who collects the money", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("the merchant model keeps the traveller's payment, and the card fees and timing that come with it", 16, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Booking Holdings, Form 10-K for 2025", size=12)
        beat(self,
             "There are two ways to sell someone else's room. <bookmark mark='a'/> In the agency model the guest pays the hotel "
             f"at the stay, and the hotel sends the agent its commission: {B['gba']:.0f} billion dollars of Booking's bookings, "
             f"falling. <bookmark mark='b'/> In the merchant model the agent takes the guest's money when they book and pays "
             f"the hotel later: {B['gbm']:.0f} billion, up a quarter in a year. <bookmark mark='c'/> Handling the payment lets "
             "the agent earn on the card fees and the money's timing, and holds the customer more tightly.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], note])

    def marketing(self):
        B, E, A = R["agents"]["bk"], R["agents"]["ex"], R["agents"]["ab"]
        items = [("Booking: marketing", 100 * B["mkt"] / B["rev"], AGENT, f"{bn(B['mkt'])}, {100 * B['mkt'] / B['rev']:.0f}% of revenue"),
                 ("Expedia: selling and marketing", 100 * E["mkt"] / E["rev"], AGENT, f"{bn(E['mkt'])}, {100 * E['mkt'] / E['rev']:.0f}% of revenue"),
                 ("Airbnb: sales and marketing", 100 * A["mkt"] / A["rev"], AGENT, f"{bn(A['mkt'])}, {100 * A['mkt'] / A['rev']:.0f}% of revenue")]
        rows = hbars(items, max_value=60, x0=0.6, top=1.2, row=1.0, length=4.2, size=17, bar_h=0.55)
        hd = tx("what the agents spend to be found, 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Booking Holdings, Expedia Group and Airbnb, Forms 10-K for 2025; SEC company facts", size=12)
        beat(self,
             "Where does the commission go? Much of it goes to being found. <bookmark mark='a'/> Booking spent "
             f"{B['mkt']:.1f} billion dollars on marketing in 2025, nearly a third of its revenue, most of it on search "
             "engines, chiefly Google, and on the price-comparison sites. "
             f"<bookmark mark='b'/> Expedia, which booked {E['gb']:.0f} billion dollars of travel, spent "
             f"{E['mkt']:.1f} billion on selling and marketing, half of its revenue. <bookmark mark='c'/> Airbnb, which aims to "
             f"attract guests through direct and unpaid channels, spent {100 * A['mkt'] / A['rev']:.0f} per cent. In this series' reading, an "
             "online agent is a buyer of attention that resells it to hotels at a mark-up.",
             base=[rows.axis, hd, src], steps=list(rows))

    def supply(self):
        B = R["agents"]["bk"]
        parts = [("hotels, motels and resorts", B["hotels"] / B["props"], BRAND), ("homes, apartments and other places", 1 - B["hotels"] / B["props"], AGENT)]
        bar = viz.bar_split(parts, 1.0, width=11.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n_, 14, GREY_A)).arrange(DOWN, buff=0.05).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n_, v, c) in enumerate(parts)])
        hd = tx(f"the {B['props']:.1f} million places to stay on Booking.com, end of 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Booking Holdings, Form 10-K for 2025", size=12)
        beat(self,
             f"And what it sells. <bookmark mark='a'/> Of the {B['props']:.1f} million places offered on Booking.com at the "
             f"end of 2025, about {B['hotels'] * 1e3:.0f} thousand were hotels, motels and resorts. <bookmark mark='b'/> The "
             "other 3.9 million were homes, apartments and other places to stay. The agent's catalogue is mostly the long tail "
             "that no hotel brand reaches: one flat, one guest house, one family hotel at a time.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0]), VGroup(bar[1], labs[1])])

    def rules(self):
        q = quote(["'In 2024, the Comisión Nacional de los Mercados y la Competencia in Spain", "imposed a fine and restricted certain of Booking.com's business practices", "such as those relating to contractual parity provisions and the ranking criteria'"],
                  "Booking Holdings, Form 10-K for 2025", size=20)
        note = tx("and in the EU, Booking Holdings is designated a 'gatekeeper' under the Digital Markets Act", 18, BRAND).move_to([0, -2.1, 0])
        src = source("Booking Holdings, Form 10-K for 2025", size=12)
        beat(self,
             "Hotels resent the commission, and for years many contracts with the agents carried parity clauses: the hotel "
             "promised not to sell the same room more cheaply elsewhere, including on its own website. <bookmark mark='a'/> "
             "Competition authorities have chipped away at them. In 2024 Spain's competition authority fined Booking.com and "
             "restricted its parity provisions and the way it ranks hotels. <bookmark mark='b'/> And the European Union has "
             "designated Booking Holdings a gatekeeper under its Digital Markets Act, the same rules it applies to the largest "
             "technology platforms.",
             base=[src], steps=[q, note])

    def airbnb(self):
        A = R["agents"]["ab"]
        houses = VGroup(*[draw.house(0.7, color=c) for c in ("#C9D3E0", "#F2C14E", "#9FE0D0", "#FF8FB1", "#B58CFF")]).arrange(RIGHT, buff=0.35).move_to([0, 1.6, 0])
        c = stat_cards([(bn(A["gbv"]), "booked on Airbnb, 2025", AGENT), (f"{A['nights']}m", "nights and seats booked", AGENT),
                        (f"{100 * A['rev'] / A['gbv']:.1f}%", f"kept as revenue: {bn(A['rev'])}", BRAND),
                        (f"{A['hosts']}m+", "hosts", GOOD)], y=-0.6, size=30, span=12.4)
        note = tx("'New York City passed regulations in 2023, which resulted in a de facto ban of short-term rental activities'", 15, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Airbnb, Form 10-K for 2025", size=12)
        beat(self,
             "And the platform that sells nights in other people's homes. <bookmark mark='a'/> Guests booked "
             f"{A['gbv']:.0f} billion dollars of stays and experiences on Airbnb in 2025, <bookmark mark='b'/> {A['nights']} "
             f"million nights and seats. <bookmark mark='c'/> Airbnb kept {100 * A['rev'] / A['gbv']:.1f} per cent, "
             f"{A['rev']:.1f} billion dollars, and made {A['ni']:.1f} billion of profit, <bookmark mark='d'/> with more than "
             f"{A['hosts']} million hosts. It owns no homes at all: an even lighter version of the hotel brand. "
             "<bookmark mark='e'/> Its risk is the city council: New York's rules of 2023, Airbnb says, amount to a de facto ban.",
             base=[houses, src], steps=list(c) + [note])
