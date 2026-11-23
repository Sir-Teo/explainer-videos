from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

NAICS = [("11", "Farms, forestry, fishing"), ("21", "Mining, oil and gas"), ("22", "Utilities"), ("23", "Construction"),
         ("31-33", "Manufacturing"), ("42", "Wholesale trade"), ("44-45", "Retail trade"),
         ("48-49", "Transportation"), ("51", "Information"), ("52", "Finance and insurance"), ("53", "Real estate"),
         ("54", "Professional services"), ("55", "Head offices"), ("56", "Admin and waste"), ("61", "Education"),
         ("62", "Health care"), ("71", "Arts and recreation"), ("72", "Hotels and restaurants"),
         ("81", "Other services"), ("92", "Government")]


class Industry(VoiceoverScene):
    def construct(self):
        card(self, 3, "What is an industry?", "Is Amazon a shop or a cloud company?",
             "Chapter three. What is an industry?", lit=("unit",))
        self.codes()
        self.amazon()

    def codes(self):
        cells = VGroup()
        for code, name in NAICS:
            box = RoundedRectangle(corner_radius=0.08, width=2.4, height=0.78, fill_color=I.PANEL, fill_opacity=1,
                                   stroke_color=I.EDGE, stroke_width=1.2)
            body = VGroup(TB(code, 17, I.ACCENT), T(name, 15, I.TEXT)).arrange(DOWN, buff=0.04)
            if body.width > 2.25:
                body.scale_to_fit_width(2.25)
            cells.add(VGroup(box, body.move_to(box)))
        cells.arrange_in_grid(rows=4, cols=5, buff=(0.15, 0.15)).move_to(DOWN * 0.3)
        head = T("The North American Industry Classification System: twenty sectors", 24, I.TEXT).to_edge(UP, buff=0.5)
        note = T("Each factory, office, store or warehouse is classified by what it does", 20, I.DIM).to_edge(DOWN,
                                                                                                             buff=0.4)
        src = source("US Census Bureau, NAICS 2022", corner=UR)
        with self.voiceover(
            "To measure industries you first have to say what they are. <bookmark mark='a'/> America, Canada and "
            "Mexico share a list of twenty sectors, each with a code: 11 for farming, 31 to 33 for manufacturing, 51 "
            "for information, 62 for health care, and so on down to about a thousand detailed industries. "
            "<bookmark mark='b'/> The statisticians do not classify companies. They classify each factory, office, "
            "store or warehouse by what it does, and add them up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.95) for c in cells], lag_ratio=0.06), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def amazon(self):
        A = R["companies"]["aws"]
        retail_s, retail_oi = A["amzn_sales"] - A["sales"], A["amzn_oi"] - A["oi"]
        L = 9.0

        def row(y, total, part, title, fmt):
            r1 = Rectangle(width=L * (total - part) / total, height=0.7, fill_color="#F2A65A", fill_opacity=0.85,
                           stroke_width=0)
            r2 = Rectangle(width=L * part / total, height=0.7, fill_color="#B58CFF", fill_opacity=0.95, stroke_width=0)
            g = VGroup(r1, r2).arrange(RIGHT, buff=0).move_to(np.array([0.2, y, 0]))
            t = TB(title, 22, I.TEXT).next_to(g, UP, buff=0.12).align_to(g, LEFT)
            l1 = T(f"shops and advertising {fmt(total - part)}", 17, "#0E1117").move_to(r1)
            l2 = T(f"AWS {fmt(part)}", 17, "#0E1117").move_to(r2)
            if l2.width > r2.width - 0.1:
                l2.next_to(r2, RIGHT, buff=0.1).set_color("#B58CFF")
            return VGroup(g, t, l1, l2)
        s = row(1.2, A["amzn_sales"], A["sales"], "Amazon's sales, 2025", lambda v: f"${v:.0f}bn")
        p = row(-1.0, A["amzn_oi"], A["oi"], "Amazon's operating profit, 2025", lambda v: f"${v:.0f}bn")
        q = T(f"AWS: {100 * A['sales'] / A['amzn_sales']:.0f}% of the sales, {100 * A['oi'] / A['amzn_oi']:.0f}% of "
              "the profit", 26, "#B58CFF").to_edge(DOWN, buff=0.6)
        src = source("Amazon Form 10-K 2025, segment information")
        with self.voiceover(
            "Companies do not fit the boxes so neatly. <bookmark mark='a'/> Amazon is counted by most people as a "
            "shop, and most of its sales are: of its 717 billion dollars in 2025, 588 billion came from its North "
            "American and international segments: the shops, the marketplace, advertising and subscriptions. <bookmark mark='b'/> But look at its profit. Amazon Web "
            "Services, which rents computing power to other companies, made 129 billion dollars of sales, eighteen "
            "percent of the total, <bookmark mark='c'/> and 46 billion of the company's 80 billion dollars of "
            "operating profit: more than half. <bookmark mark='d'/> By sales Amazon is a retailer. By profit it is a "
            "cloud company that also runs shops. In the statistics, its warehouses are counted in one industry and "
            "its data centres in another, which is why industry figures and company figures never quite match."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(s[1]), GrowFromEdge(s[0][0], LEFT), FadeIn(s[2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(s[0][1], LEFT), FadeIn(s[3]))
            vo.wait_until("c")
            self.play(FadeIn(p[1]), GrowFromEdge(p[0], LEFT), FadeIn(p[2]), FadeIn(p[3]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()
