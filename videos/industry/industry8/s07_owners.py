from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403

NAMES = {"USA": "United States", "RUS": "Russia", "SAU": "Saudi Arabia", "CAN": "Canada", "IRQ": "Iraq", "CHN": "China",
         "ARE": "UAE", "IRN": "Iran", "BRA": "Brazil", "KWT": "Kuwait", "KAZ": "Kazakhstan", "NOR": "Norway",
         "MEX": "Mexico", "NGA": "Nigeria", "QAT": "Qatar", "LBY": "Libya", "AGO": "Angola", "DZA": "Algeria",
         "VEN": "Venezuela", "GBR": "UK", "GUY": "Guyana"}
OPEC_MEMBERS = {"SAU", "IRQ", "IRN", "ARE", "KWT", "VEN", "NGA", "LBY", "DZA"}


class Owners(VoiceoverScene):
    def construct(self):
        card(self, 6, "Who owns the oil", "When a barrel costs three dollars and sells for sixty-nine, who keeps the rest?",
             "Chapter six. Who owns the oil.", lit=("dollar", "moat"))
        self.producers()
        self.giants()
        self.take()

    def producers(self):
        W = R["world"]
        top = W["top"]
        u = 0.36
        bars = VGroup()
        for k, (a, v) in enumerate(top):
            col = OPEC if a in OPEC_MEMBERS else BRENT
            b = Rectangle(width=v / 1000 * u, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.9)
            b.move_to([-2.6, 2.3 - 0.47 * k, 0], aligned_edge=LEFT)
            n = tx(NAMES.get(a, a), 17, WHITE).next_to(b, LEFT, buff=0.15).align_to([-2.75, 0, 0], RIGHT)
            v_ = tx(f"{v / 1000:.1f}m", 16, GREY_A).next_to(b, RIGHT, buff=0.1)
            bars.add(VGroup(n, b, v_))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=OPEC, fill_opacity=1), tx("OPEC member", 15, OPEC)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=BRENT, fill_opacity=1), tx("not in OPEC", 15, BRENT)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.85)
        head = tx(f"Crude oil produced, 2025: million barrels a day (world: {W['world'][-1] / 1000:.1f}m)", 20, GREY_A).to_edge(
            UP, buff=0.35)
        share = tx(f"OPEC: {100 * W['opec_share'][2025]:.0f}% of the world's crude", 20, OPEC, bold=True).move_to([4.6, -1.4, 0])
        src = source("US Energy Information Administration, International Energy Statistics (crude oil including lease "
                     "condensate)", size=13)
        with self.voiceover(
            "Start with who produces it. <bookmark mark='a'/> In 2025 the world produced about eighty-four and a half "
            "million barrels of crude oil a day. The largest producer was the United States, then Russia, then "
            "Saudi Arabia, Canada and Iraq. <bookmark mark='b'/> The countries in red belong to OPEC, the "
            f"Organization of the Petroleum Exporting Countries, which together produced {100 * W['opec_share'][2025]:.0f} "
            "percent of it. But the bigger difference is who owns the oil. In America, much of it belongs to whoever "
            "owns the land, and is produced by thousands of private companies. In most other places, the oil under "
            "the ground belongs to the state."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2])) for g in bars],
                                  lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(key), FadeIn(share))
        self.clear_scene()

    def giants(self):
        a_res, x_res = get("aramco.reserves"), get("xom.reserves.2025")
        unit = 2.5  # bn boe per barrel icon
        ab = VGroup(*[draw.barrel(0.32, color=GAS) for _ in range(int(round(a_res / unit)))]).arrange_in_grid(
            cols=14, buff=(0.06, 0.06))
        xb = VGroup(*[draw.barrel(0.32, color=BRENT) for _ in range(int(round(x_res / unit)))]).arrange_in_grid(
            cols=14, buff=(0.06, 0.06))
        ab.move_to([-2.4, -0.3, 0])
        xb.next_to(ab, RIGHT, buff=1.0).align_to(ab, DOWN)
        al = VGroup(tx("Saudi Aramco", 24, GAS, bold=True), tx(f"{a_res:.0f}bn barrels of oil equivalent", 17, GREY_A),
                    tx(f"{get('aramco.production'):.1f}m barrels a day produced", 17, GREY_A)).arrange(DOWN, buff=0.05).next_to(
            ab, UP, buff=0.3)
        xl = VGroup(tx("ExxonMobil", 24, BRENT, bold=True), tx(f"{x_res:.1f}bn proved", 17, GREY_A)).arrange(
            DOWN, buff=0.05).next_to(xb, UP, buff=0.3)
        key = tx("each barrel: 2.5 billion barrels", 15, GREY_B).to_edge(DOWN, buff=0.7)
        src = source("Saudi Aramco, Annual Report 2025 (reserves under the Concession); ExxonMobil, Form 10-K for 2025",
                     size=13)
        with self.voiceover(
            "Compare two companies. <bookmark mark='a'/> Saudi Aramco holds, under its concession from the Saudi "
            f"state, about {a_res:.0f} billion barrels of oil and gas, counted as oil equivalent. <bookmark mark='b'/> "
            f"ExxonMobil, the largest American oil company, reported {x_res:.1f} billion of proved reserves at the end "
            "of 2025. The two numbers are not measured under the same rules, but the difference in scale is not in "
            "doubt: the biggest oil companies in the world are mostly owned by states."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(al), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in ab], lag_ratio=0.01), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(xl), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in xb], lag_ratio=0.05), run_time=1.2)
        self.clear_scene()

    def take(self):
        roy, tax, net, div, gov = (get(k) for k in ("aramco.royalties", "aramco.tax", "aramco.net", "aramco.dividends",
                                                    "aramco.gov"))
        to_gov_div = div * gov / 100
        items = [("royalties and other taxes", roy, STATE), ("income taxes and zakat", tax, STATE),
                 ("dividends to the Government (81.48%)", to_gov_div, "#F28B82"),
                 ("dividends to the state's fund and the public", div - to_gov_div, GREY_B)]
        bars = VGroup()
        x = -5.6
        for k, (lab, v, col) in enumerate(items):
            b = Rectangle(width=v * 11.2 / (roy + tax + div), height=0.8, stroke_color="#0E1117", stroke_width=2, fill_color=col,
                          fill_opacity=0.95).move_to([x, 0.6, 0], aligned_edge=LEFT)
            x += b.width
            t = VGroup(tx(f"${v:.0f}bn", 20, WHITE, bold=True), tx(lab, 14, GREY_A)).arrange(DOWN, buff=0.04)
            t.next_to(b, DOWN if k % 2 == 0 else UP, buff=0.2)
            bars.add(VGroup(b, t))
        total = roy + tax + to_gov_div
        brace = BraceBetweenPoints(bars[0][0].get_corner(DL) + DOWN * 1.0, bars[2][0].get_corner(DR) + DOWN * 1.0, DOWN,
                                   color=STATE)
        bt = tx(f"to the Saudi state, 2025: about ${total:.0f}bn", 22, STATE, bold=True).next_to(brace, DOWN, buff=0.1)
        cmp_ = tx(f"Aramco's net income: ${net:.0f}bn", 18, GREY_A).to_edge(UP, buff=0.5)
        src = source("Saudi Aramco, Annual Report 2025 (dividends SAR 320.4bn at 3.75 riyals to the dollar); this "
                     "film's shares", size=13)
        with self.voiceover(
            "And when a barrel costs a few dollars to lift and sells for seventy, most of the difference goes to the "
            f"owner of the rock. <bookmark mark='a'/> In 2025 Aramco paid the Saudi state {roy:.0f} billion dollars in "
            f"royalties and other taxes, <bookmark mark='b'/> and {tax:.0f} billion in income tax and zakat. "
            f"<bookmark mark='c'/> It then paid {div:.0f} billion dollars in dividends, and the Government, which owns "
            f"{gov:.0f} percent of the company directly, received about {to_gov_div:.0f} billion of them. "
            "<bookmark mark='d'/> Much of the rest went to the state's own investment fund. "
            f"<bookmark mark='e'/> All told, something like {total:.0f} billion dollars went from one company's "
            "barrels to one government in one year. That is why oil is as much about states as about companies, "
            "and why the chapters on OPEC and on war are in a film about an industry."
        ) as vo:
            self.play(FadeIn(src), FadeIn(cmp_))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(GrowFromEdge(bars[k][0], LEFT), FadeIn(bars[k][1]), run_time=1.0)
            vo.wait_until("e")
            self.play(GrowFromCenter(brace), FadeIn(bt))
        self.clear_scene()
