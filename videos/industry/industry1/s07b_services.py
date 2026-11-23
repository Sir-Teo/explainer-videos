from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Services(VoiceoverScene):
    def construct(self):
        card(self, 8, "After the sale", "Does the money stop when the phone is sold?",
             "Chapter eight. After the sale.", lit=("dollar", "moat"))
        self.split()
        self.what()

    def split(self):
        S = R["services"]
        rev, gp = get("apple.revenue.fy2026"), get("apple.gross_profit.fy2026")
        L = 8.4
        def row(total, part, y, title, unit):
            sc = L / rev
            prod = Rectangle(width=sc * (total - part), height=0.75, fill_color=I.BRAND, fill_opacity=0.55,
                             stroke_width=0)
            serv = Rectangle(width=sc * part, height=0.75, fill_color=I.PROFIT, fill_opacity=0.9, stroke_width=0)
            g = VGroup(prod, serv).arrange(RIGHT, buff=0).move_to(np.array([0, y, 0])).align_to(LEFT * 5.0, LEFT)
            t = VGroup(TB(title, 22, I.TEXT), T(money_short(total), 18, I.DIM)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.04)
            t.next_to(g, UP, buff=0.12).align_to(g, LEFT)
            lp = T(f"products {money_short(total - part)}", 17, "#0E1117").move_to(prod)
            ls = VGroup(TB(f"services {money_short(part)}", 18, I.PROFIT), T(unit, 16, I.PROFIT)
                        ).arrange(DOWN, buff=0.03).next_to(serv, RIGHT, buff=0.15)
            return VGroup(g, t, lp, ls)
        r1 = row(rev, S["sales"], 1.3, "Apple's sales, fiscal 2026", f"{pct(S['share_sales'])} of sales")
        r2 = row(gp, S["gp"], -1.2, "Apple's gross profit, fiscal 2026", f"{pct(S['share_gp'])} of gross profit")
        src = source("Apple Form 10-K FY2026")
        with self.voiceover(
            "When you buy an iPhone, Apple is not done with you. <bookmark mark='a'/> In its last fiscal year Apple "
            "sold 479 billion dollars of goods and services. A quarter of it, 123 billion, was services: the App "
            "Store, iCloud storage, AppleCare, music and video subscriptions, advertising, payments. <bookmark "
            "mark='b'/> But look at what Apple kept. Services cost little to provide once the software is written, so "
            "they keep 76 cents of each dollar. That made them 40 percent of Apple's gross profit: 94 billion "
            "dollars."
        ) as vo:
            self.play(FadeIn(src), FadeIn(r1[1]))
            vo.wait_until("a")
            self.play(GrowFromEdge(r1[0], LEFT), FadeIn(r1[2]), FadeIn(r1[3]), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(r2[1]), GrowFromEdge(r2[0], LEFT), FadeIn(r2[2]), FadeIn(r2[3]), run_time=1.4)
        self.clear_scene()

    def what(self):
        S = R["services"]
        ph = viz.phone(3.2, body=BODY_17, glow=I.PROFIT).shift(LEFT * 4.6)
        streams = [("App Store: up to 30% of what is spent in apps", I.PROFIT),
                   ("iCloud, Music, TV+, AppleCare: monthly fees", I.PROFIT),
                   (f"Google: about {money_short(S['google'], 0)} in 2022 to be the default search", I.RF),
                   ("advertising and payments", I.PROFIT)]
        items = VGroup()
        for text, c in streams:
            dot = viz.coin(0.1, c)
            items.add(VGroup(dot, T(text, 22, I.TEXT)).arrange(RIGHT, buff=0.2))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 1.2 + UP * 0.9)
        per = VGroup(T("Per active Apple device, per year:", 22, I.DIM),
                     TB(f"about {money(S['per_device'])} of services, {money(S['gp_per_device'])} of gross profit", 26,
                        I.PROFIT),
                     T(f"{S['base']:.1f} billion active devices (Apple, January 2026)", 18, I.DIM)
                     ).arrange(DOWN, buff=0.08).move_to(RIGHT * 1.2 + DOWN * 1.6)
        arrows = VGroup(*[Arrow(ph.get_right(), it.get_left(), buff=0.15, color=I.PROFIT, stroke_width=2,
                                max_tip_length_to_length_ratio=0.08) for it in items])
        src = source("Apple Newsroom (2026-01-29); App Store guidelines; United States v. Google (2024), via NPR;"
                     " Apple 10-K FY2026", size=14)
        with self.voiceover(
            "Every iPhone sold is also a toll booth. <bookmark mark='a'/> Apple takes up to 30 percent of what people "
            "spend inside apps, 15 percent for small developers. It charges monthly for storage, music, television "
            "and repairs. <bookmark mark='b'/> And other companies pay to reach iPhone users. In the antitrust case "
            "against Google, the judge found that Google paid Apple an estimated 20 billion dollars in 2022 to be the "
            "default search engine in Safari. <bookmark mark='c'/> Spread over the more than two and a half billion "
            "Apple devices in use, services bring in about 49 dollars of revenue and 38 dollars of gross profit per "
            "device, every year. <bookmark mark='d'/> That changes how to read the Dollar of chapter five. The 244 "
            "dollars of profit on the sale is not the end of the money; for as long as the phone is used, more "
            "keeps coming. It is one more reason the brand at the end of the chain keeps the most."
        ) as vo:
            self.play(FadeIn(ph, shift=UP * 0.1), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(items[0]), GrowArrow(arrows[1]), FadeIn(items[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[2]), FadeIn(items[2]), GrowArrow(arrows[3]), FadeIn(items[3]))
            vo.wait_until("c")
            self.play(FadeIn(per, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(per[1], color=I.PROFIT, scale_factor=1.05))
        self.clear_scene()
