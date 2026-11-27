from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Biotech(VoiceoverScene):
    def construct(self):
        card(self, 10, "Biotech: the small companies", "What happens to a company with one great idea?",
             "Chapter ten. Biotech. Many new medicines start in small companies with one idea, a laboratory and "
             "investors' money. What happens to them?", lit=("change", "moat"))
        self.moderna()
        self.winners()
        self.bought()

    def moderna(self):
        B = R["biotech"]
        m = B["mrna"]
        items = [(str(y), v, BIO if y in (2021, 2022) else GREY_B, f"${v:.1f}bn") for y, v in sorted(m.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=0.9, gap=0.4, size=14)
        vl = draw.vial(1.2, BIO).move_to([-5.6, 1.6, 0])
        src = source("Moderna, Inc., Forms 10-K via SEC company facts: revenue", size=12)
        beat(self,
             "Moderna shows the whole arc. <bookmark mark='a'/> In 2019 it was a research company with "
             f"{m[2019] * 1e3:.0f} million dollars of revenue and no product on sale. <bookmark mark='b'/> With its Covid "
             f"vaccine it sold {m[2021]:.1f} billion dollars in 2021 and {m[2022]:.1f} billion in 2022. "
             f"<bookmark mark='c'/> By 2025 it was down to {m[2025]:.1f} billion, and losing more than it sold. One "
             "product can make a biotech company, and its decline can leave the company searching for the next one, "
             "spending the cash the good years left behind on trials that may or may not succeed.",
             base=[vl, head("Moderna's revenue"), src], steps=[VGroup(*bars_[:2]), VGroup(*bars_[2:4]), VGroup(*bars_[4:])])

    def winners(self):
        B = R["biotech"]
        mg, rd = B["margins"], B["rnd"]
        rows = VGroup()
        for i, k in enumerate(("Vertex", "Regeneron", "Amgen", "Gilead")):
            y = 1.4 - 0.85 * i
            rows.add(VGroup(tx(k, 19, BIO, bold=True).move_to([-4.0, y, 0], aligned_edge=RIGHT),
                            tx(f"research: {100 * rd[k]:.0f}% of revenue", 17, WHITE).move_to([-1.0, y, 0]),
                            tx(f"kept: {100 * mg[k]:.0f}% (median, 2021-2025)", 17, GOOD, bold=True).move_to([3.2, y, 0])))
        src = source("Forms 10-K via SEC company facts: research and development and net income over revenue", size=12)
        beat(self,
             "The biotech companies that found protected products are among the most profitable companies in this series. "
             f"<bookmark mark='a'/> Vertex, which sells medicines for cystic fibrosis, spends {100 * rd['Vertex']:.0f} per "
             f"cent of its revenue on research and keeps {100 * mg['Vertex']:.0f} per cent as profit. "
             f"<bookmark mark='b'/> Regeneron spends {100 * rd['Regeneron']:.0f} per cent on research and keeps "
             f"{100 * mg['Regeneron']:.0f}. <bookmark mark='c'/> Amgen and Gilead, the older biotech companies, spend about "
             "a fifth and keep about a fifth. <bookmark mark='d'/> Research is their biggest cost, and the protected "
             "product pays for it with room to spare.",
             base=[head("Biotech companies that made it"), src], steps=list(rows))

    def bought(self):
        B = R["biotech"]
        big = VGroup(draw.factory(1.8, BRAND), tx("a large company with a patent date", 16, BRAND, bold=True)).arrange(DOWN, buff=0.1).move_to([-4.0, 0.6, 0])
        small = VGroup(draw.flask(1.2, BIO), tx("a biotech with a promising drug", 16, BIO, bold=True)).arrange(DOWN, buff=0.1).move_to([4.0, 0.6, 0])
        arr = Arrow(small.get_left(), big.get_right(), buff=0.3, stroke_width=4, color=PRICE)
        al = tx("bought, for its pipeline", 16, PRICE, bold=True).next_to(arr, UP, buff=0.1)
        ex = tx(f"January 2026: Merck acquires Cidara for about ${B['cidara']:.1f}bn", 18, WHITE, bold=True).move_to([0, -1.8, 0])
        src = source("Merck & Co., Inc., Form 10-K 2025", size=12)
        beat(self,
             "And many small companies end up inside big ones. <bookmark mark='a'/> A large company facing a patent date "
             "needs new drugs; <bookmark mark='b'/> a small company with a promising one needs money for Phase three and "
             "a sales force. <bookmark mark='c'/> So the large company buys it. <bookmark mark='d'/> Merck, with Keytruda's "
             f"date approaching, acquired Cidara for about {B['cidara']:.1f} billion dollars in January 2026. Much of the "
             "industry's invention happens in small companies; much of its selling, in large ones.",
             base=[src], steps=[big, small, [arr, al], ex])
