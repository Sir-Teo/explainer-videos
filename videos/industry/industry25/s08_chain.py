from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Chain(VoiceoverScene):
    def construct(self):
        card(self, 6, "Between the buyer and the house", "What do the brokers and the portals earn?",
             "Chapter six. Between the buyer and the house. Most homes that change hands are not new: they are sold by "
             "one family to another, through agents, listings and websites.", lit=("dollar", "moat"))
        self.nar()
        self.portals()
        self.lender()
        self.ibuyer()

    def nar(self):
        sign = draw.sale_sign(1.6).move_to([-5.0, 0.8, 0])
        q = quote(["'NAR agreed to implement certain industry-wide practice changes, including ... prohibiting buyer",
                   "brokers' offers of compensation from being included in listings on Multiple Listing Services and",
                   "requiring a buyer to enter into a written agreement with their agent that would set forth the buyer",
                   "broker's fee before showing the buyer a property. These changes went into effect in August of 2024.'"],
                  "Compass, Inc., Form 10-K for 2025", size=16).move_to([1.2, 1.2, 0])
        note = tx(f"Anywhere, now part of Compass, settled for ${R['trade']['nar']:.1f}m and five years of practice changes",
                  17, PRICE, bold=True).move_to([1.2, -1.2, 0])
        src = source("Compass, Inc., Form 10-K for 2025", size=12)
        beat(self,
             "For decades an American seller's agent offered part of the commission to whichever agent brought the "
             "buyer, and the offer sat in the shared listing service that every agent searched. <bookmark mark='a'/> "
             "Sellers sued, arguing that this kept commissions high. To settle, the National Association of Realtors "
             "agreed to change the rules from August 2024: no offers of buyer-agent pay in the listings, and a written "
             "agreement on the buyer's agent's fee before any viewing. <bookmark mark='b'/> The large brokerages settled "
             f"too: Anywhere, now owned by Compass, for {R['trade']['nar']:.1f} million dollars and five years of changed "
             "practices.",
             base=[sign, src], steps=[q, note])

    def portals(self):
        T = R["trade"]
        ys = list(range(2021, 2026))
        series = {"Zillow": ({y: 100 * T["Zillow"][y][1] for y in ys}, BAD), "Compass": ({y: 100 * T["Compass"][y][1] for y in ys}, PRICE)}
        ch = line_chart(series, x=(2021, 2025), y=(-30, 5), xticks=ys, yticks=[-30, -20, -10, 0], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="net income per dollar of revenue", width=9.0, height=4.2, center=(-0.8, -0.45))
        zero = DashedLine(ch.ax.c2p(2021, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5)
        src = source("Zillow Group and Compass, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "The businesses around the transaction have found it hard to make money. <bookmark mark='a'/> Zillow, the "
             f"listings website, lost {abs(100 * T['Zillow'][2021][1]):.0f} cents on each dollar of revenue in 2021, "
             f"and only reached a small profit, {100 * T['Zillow'][2025][1]:.1f} cents, in 2025. Compass, a large "
             f"brokerage, lost money every year from 2021 to 2025, though less each year: "
             f"{100 * T['Compass'][2025][1]:.1f} cents in 2025. Agents are paid commissions; the firms around them keep "
             "little.",
             base=[ch.frame, zero, src], steps=[[ch.lines[k] for k in ch.lines] + [ch.labels[k] for k in ch.labels]])

    def ibuyer(self):
        T = R["trade"]["Opendoor"]
        items = [(str(y), T[y][0], BAD if y in (2022,) else GREY_B, f"${T[y][0]:.1f}bn") for y in range(2021, 2026)]
        bars_ = vbars(items, base_y=-2.2, height=3.4, width=1.1, gap=0.6, size=17, max_value=16.5)
        lab = tx("Opendoor's revenue: buying homes, fixing them up and reselling them", 16, GREY_A).to_edge(UP, buff=0.7)
        note = tx(f"net loss in every year; {abs(100 * T[2025][1]):.0f} cents per dollar in 2025", 18, BAD, bold=True).move_to([0, 1.6, 0])
        src = source("Opendoor Technologies, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And one company tried to replace the whole chain with an algorithm. <bookmark mark='a'/> Opendoor buys "
             "homes directly from sellers, fixes them up and resells them. Its revenue jumped to "
             f"{T[2022][0]:.1f} billion dollars in 2022, then fell to {T[2025][0]:.1f} billion by 2025, as the market "
             "slowed. <bookmark mark='b'/> It lost money in every one of those years. A house is a costly thing "
             "to hold in inventory when prices can fall, the same lesson as the builders' land.",
             base=[lab, src], steps=[bars_, note])

    def lender(self):
        U = R["extra"]["uwm"]
        items = [(str(y), 100 * m, GOOD if m > 0 else BAD, f"{100 * m:+.1f}%") for y, (rv, m) in U.items()]
        bars_ = VGroup()
        for i, (lab, v, col, t) in enumerate(items):
            h = abs(v) * 0.5
            x = -3.0 + i * 1.5
            rect = Rectangle(width=1.0, height=max(h, 0.03), stroke_width=0, fill_color=col, fill_opacity=0.9)
            rect.move_to([x, -0.4 + (h / 2 if v > 0 else -h / 2), 0])
            bars_.add(VGroup(rect, tx(t, 16, col, bold=True).next_to(rect, UP if v > 0 else DOWN, buff=0.08),
                             tx(lab, 15, GREY_A).move_to([x, -1.4 if v > 0 else 0.4, 0])))
        axis = Line([-3.8, -0.4, 0], [3.8, -0.4, 0], stroke_color=GREY_B, stroke_width=2)
        lab = tx("UWM, a large mortgage lender: net income per dollar of revenue", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("UWM Holdings, Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"The lenders who make the loans keep little too. <bookmark mark='a'/> UWM, a large wholesale lender, kept {100 * U[2021][1]:.1f} cents of each dollar of revenue in 2021, when refinancing "
             f"boomed, <bookmark mark='b'/> lost money in 2023, and kept under one cent in 2024 and 2025. The lender earns "
             "on the volume of loans it makes and sells on; when rates rise, the volume goes.",
             base=[axis, lab, src], steps=[bars_[0], bars_[1:]])
