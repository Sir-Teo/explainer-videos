from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403

PAL_OWN = ["#7EC8F5", "#4FA3F7", "#2F6FB0", "#3A4560"]
SHORT = {"Tickets and miles sold, not yet used": "tickets, miles", "Data centres and property": "data centres",
         "Stock on the shelves": "stock", "Owed to suppliers": "suppliers", "Power plants and wires": "plants, wires",
         "Aircraft and property": "aircraft", "Paid in advance by customers": "prepaid", "Long-term debt": "debt",
         "Other borrowing": "borrowing", "Everything else": "other", "Owner's money and kept profit": "owner",
         "Oven, after a year's wear": "oven", "Owed to the miller": "miller", "Owed by cafes": "cafes owe"}
PAL_OWE = ["#F2A65A", "#C07A3A", "#7BD88F"]


def pair(owns, owes, total, h=4.3, w=0.95, x=0.0, top=2.0, size=12):
    """Two columns, what a business has and who paid for it, each slice labelled inside when it fits."""
    g = VGroup()
    for side, items, pal in ((0, owns, PAL_OWN), (1, owes, PAL_OWE)):
        y = top
        col = VGroup()
        for k, (lab, v) in enumerate(items):
            hh = h * v / total
            c = pal[-1] if (side == 1 and lab in ("Owners", "Owner's money and kept profit")) else pal[min(k, len(pal) - 2)
                                                                                                      if side == 1 else k]
            rr = Rectangle(width=w, height=max(hh, 0.01), fill_color=c, fill_opacity=0.92, stroke_color=BACKGROUND,
                           stroke_width=1.2).move_to(np.array([x + (side - 0.5) * (w + 0.06), y - hh / 2, 0]))
            txt = VGroup()
            if hh > 0.34:
                txt = VGroup(TB(f"{100 * v / total:.0f}%", size + 3, "#0E1117"),
                             T(SHORT.get(lab, lab).lower(), size, "#0E1117")).arrange(DOWN, buff=0.02)
                if txt.width > w - 0.08:
                    txt.scale_to_fit_width(w - 0.08)
                if txt.height > hh - 0.06:
                    txt.scale_to_fit_height(hh - 0.06)
                txt.move_to(rr)
            col.add(VGroup(rr, txt))
            y -= hh
        g.add(col)
    return g


class Balance(VoiceoverScene):
    def construct(self):
        card(self, 4, "The balance sheet", "What does a business own, and who paid for it?",
             "Chapter four. The balance sheet.", lit=("make", "moat"))
        self.bakery()
        self.companies()

    def bakery(self):
        b = R["bakery_year"]["balance"]
        inc = R["bakery_year"]["income"]
        owns = [("Cash", b["cash"]), ("Owed by cafes", b["receivables"]), ("Flour", b["inventory"]),
                ("Oven, after a year's wear", b["ppe"])]
        owes = [("Owed to the miller", b["payables"]), ("Bank loan", b["debt"]),
                ("Owner's money and kept profit", b["equity"])]
        total = sum(v for _, v in owns)
        g = pair(owns, owes, total, h=4.6, w=2.6, x=-1.2, top=2.2, size=15)
        lab = VGroup(TB("Assets", 22, OWN).next_to(g[0], UP, buff=0.12),
                     TB("Liabilities and equity", 22, OWE).next_to(g[1], UP, buff=0.12))
        side = VGroup(*[T(f"{n}: ${v:,.0f}", 18, I.TEXT) for n, v in owns + owes]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.5)
        tot = TB(f"Both sides: ${total:,.0f}", 24, I.ACCENT).next_to(side, DOWN, buff=0.35, aligned_edge=LEFT)
        src = estimate_tag("illustrative: the model bakery at the end of its first year", corner=DR)
        # a snapshot: the bakery on one day
        shop = draw.shop(2.2, color="#F2A65A").move_to([0, 0.2, 0])
        frame = VGroup(RoundedRectangle(corner_radius=0.1, width=4.4, height=3.6, stroke_color=WHITE, stroke_width=3,
                                        fill_opacity=0).move_to(shop))
        corners = VGroup()
        for k_, c_ in enumerate((DL, DR, UR, UL)):
            L_ = VGroup(Line(ORIGIN, RIGHT * 0.4), Line(ORIGIN, UP * 0.4)).set_stroke(I.ACCENT, 5).rotate(
                k_ * PI / 2, about_point=ORIGIN)
            corners.add(L_.shift(frame[0].get_corner(c_) + (-c_) * 0.1))
        stamp = TB("31 December", 22, I.ACCENT).next_to(frame[0], DOWN, buff=0.2)
        flash = frame[0].copy().set_fill(WHITE, 0.6).set_stroke(width=0)
        with self.voiceover(
            "At the end of the year the accountant draws the two sides of the book as a picture of the business on "
            "one day: the balance sheet. <bookmark mark='a'/> On the left, what the bakery has: "
            f"{say_usd(b['cash'])} of cash; {say_usd(b['receivables'])} that cafes owe it, because they pay twenty "
            "days after delivery; a little flour; and the oven, now worth less after a year's wear. <bookmark "
            "mark='b'/> On the right, who paid for it all: the miller, who has not been paid yet; the bank; and the "
            f"owner, whose forty thousand is now {say_usd(b['equity'])}, because the year's profit of "
            f"{say_usd(inc['net'])} was kept in the business. <bookmark mark='c'/> Every company's balance sheet is "
            "this picture, and the right-hand side is the interesting one: whose money is the business running on?"
        ) as vo:
            self.play(FadeIn(src), FadeIn(shop, shift=UP * 0.2))
            self.play(Create(frame[0]), FadeIn(corners), FadeIn(stamp, shift=UP * 0.1))
            self.play(FadeIn(flash, run_time=0.15))
            self.play(FadeOut(flash, run_time=0.5))
            vo.wait_until("a")
            self.play(FadeOut(VGroup(shop, frame, corners, stamp), scale=0.6), run_time=0.6)
            self.play(FadeIn(lab[0]), LaggedStart(*[FadeIn(s) for s in g[0]], lag_ratio=0.2), FadeIn(side[:4]))
            vo.wait_until("b")
            self.play(FadeIn(lab[1]), LaggedStart(*[FadeIn(s) for s in g[1]], lag_ratio=0.2), FadeIn(side[4:]))
            vo.wait_until("c")
            self.play(FadeIn(tot))
        self.clear_scene()

    def companies(self):
        B = R["balance"]
        six = R["six"]
        order = ["jpm", "nee", "cost", "dal", "msft"]
        groups = VGroup()
        for i, k in enumerate(order):
            x = -5.2 + i * 2.6
            g = pair(B[k]["owns"], B[k]["owes"], six[k]["assets"], h=4.3, w=1.08, x=x, top=1.75, size=13)
            nm = TB(name(k), 18, CO[k]).next_to(g, UP, buff=0.12)
            amt = T(f"assets {bn(six[k]['assets'], 0) if six[k]['assets'] < 1000 else '$' + format(six[k]['assets'] / 1e3, '.1f') + 'tn'}",
                    14, I.DIM).next_to(g, DOWN, buff=0.1)
            groups.add(VGroup(nm, g, amt))
        key = VGroup(VGroup(Square(0.2, fill_color=OWN, fill_opacity=0.9, stroke_width=0), T("what it has", 16, I.TEXT)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, fill_color=OWE, fill_opacity=0.9, stroke_width=0), T("what it owes", 16, I.TEXT)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, fill_color=OWNER, fill_opacity=0.9, stroke_width=0), T("its owners' money", 16,
                            I.TEXT)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.45)
        head = T("Balance sheets, as shares of everything each company has", 22, I.TEXT).to_edge(UP, buff=0.3)
        src = source("Forms 10-K, year-end balance sheets: JPMorgan, NextEra, Delta 2025; Costco, Microsoft fiscal "
                     "2026", corner=DR, size=12)
        J, N, C, Dl, M = (B[k] for k in order)
        with self.voiceover(
            "Now five real ones, each drawn the same height. <bookmark mark='a'/> JPMorgan Chase, a bank: of 4.4 "
            "trillion dollars of assets, a third is loans to its customers. And on the right, almost six dollars in "
            "ten are deposits: the bank's biggest supplier of money is the people who keep their savings there. Its "
            "owners' money is eight cents in the dollar. Everything else is borrowed. <bookmark mark='b'/> NextEra: "
            "almost three quarters of what it has is power plants, turbines, solar farms and wires, paid for largely "
            "with long-term debt. <bookmark mark='c'/> Costco: a fifth of what it has is the stock on its shelves, "
            "and the money it owes its suppliers is larger than that stock. Its suppliers are paying for the "
            "shelves. <bookmark mark='d'/> Delta: a fifth of its balance sheet is money from customers for tickets "
            "not yet flown and SkyMiles not yet spent, more than 16 billion dollars, held before a seat is "
            "used. <bookmark mark='e'/> And Microsoft: mostly its owners' money, and its biggest single asset now is "
            "data centres. Who funds a business, and in what form, tells you a great deal about the business."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(src))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                g = groups[i]
                self.play(FadeIn(g[0]), LaggedStart(*[FadeIn(s) for s in g[1][0]], lag_ratio=0.15),
                          LaggedStart(*[FadeIn(s) for s in g[1][1]], lag_ratio=0.15), FadeIn(g[2]), run_time=1.6)
        self.clear_scene()
        assert J and N and C and Dl and M
