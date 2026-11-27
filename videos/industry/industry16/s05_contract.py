from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

COLS = {"JBL": "#F2A65A", "FLEX": "#F6C453", "SANM": "#E8554E", "PLXS": "#B58CFF", "BHE": "#9AA3B2", "CLS": "#7EC8F5"}


class Contract(VoiceoverScene):
    def construct(self):
        card(self, 4, "Contract manufacturing", "How does a business survive on three cents in the dollar?",
             "Chapter four. Contract manufacturing.", lit=("make", "dollar"))
        self.margins()
        self.turnkey()
        self.dupont()
        self.people()

    def margins(self):
        C = R["contract"]
        M = C["margins"]
        pa = viz.plot_axes([2010, 2025], [-0.04, 0.08], x_length=8.6, y_length=4.4, xticks=[2010, 2013, 2016, 2019, 2022, 2025],
                           yticks=[-0.02, 0, 0.02, 0.04, 0.06, 0.08], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue", size=13).move_to([-1.4, -0.4, 0])
        zero = DashedLine(pa.ax.c2p(2010, 0), pa.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.2, dash_length=0.08)
        band = Polygon(pa.ax.c2p(2010, 0), pa.ax.c2p(2025, 0), pa.ax.c2p(2025, 0.05), pa.ax.c2p(2010, 0.05), stroke_width=0,
                       fill_color=ASSEMBLER, fill_opacity=0.08)
        lines, labs = VGroup(), VGroup()
        for tk, col in COLS.items():
            pts = sorted((y, max(min(v, 0.08), -0.04)) for y, v in M[tk].items())
            lines.add(poly(pa, pts, col, 3))
            labs.add(tx(NAMES[tk], 13, col, bold=True))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 0.6, 0])
        hh = VGroup(*[Dot(pa.ax.c2p(y, M["HONHAI"][y]), radius=0.1, color=WHITE) for y in (2024, 2025)])
        hhl = tx("Hon Hai", 14, WHITE, bold=True).next_to(hh, DOWN, buff=0.15)
        src = source("SEC EDGAR: Forms 10-K of Jabil, Flex, Sanmina, Plexus, Benchmark and Celestica (fiscal years); Hon Hai, audited "
                     "statements 2025", size=12)
        with self.voiceover(
            "These are the contract manufacturers that file accounts in America: Jabil, Flex, Sanmina, Plexus, Benchmark and "
            "Celestica. <bookmark mark='a'/> Here is the profit each kept from a dollar of revenue, year by year since "
            "2010. <bookmark mark='b'/> Fifteen years, booms and busts, and they have stayed almost entirely between zero and "
            "five cents. <bookmark mark='c'/> Hon Hai, the biggest of them all, kept about two cents. How does a business "
            "live on so little?"
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(src), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(band))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in hh], lag_ratio=0.3), FadeIn(hhl))
        self.clear_scene()

    def turnkey(self):
        C = R["contract"]
        t, c = C["turnkey"], C["consigned"]
        sc = 9.0 / t["revenue"]
        def pair(y, d, name, sub):
            rev = Rectangle(width=d["revenue"] * sc, height=0.8, stroke_width=0, fill_color=ASSEMBLER, fill_opacity=0.3).move_to([-5.4, y, 0], aligned_edge=LEFT)
            prof = Rectangle(width=max(d["profit"] * sc, 0.04), height=0.8, stroke_width=0, fill_color=ASSEMBLER, fill_opacity=1).move_to([-5.4, y, 0], aligned_edge=LEFT)
            lab = VGroup(tx(name, 18, WHITE, bold=True), tx(sub, 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(rev, UP, buff=0.1).align_to(rev, LEFT)
            num = tx(f"revenue ${d['revenue'] / 1e9:.1f}bn, profit ${d['profit'] / 1e6:.0f}m: a margin of {100 * d['margin']:.0f}%", 16, ASSEMBLER, bold=True)
            num.next_to(rev, DOWN, buff=0.12).align_to(rev, LEFT)
            return VGroup(rev, prof, lab, num)
        a = pair(1.4, t, "Turnkey: the assembler buys the parts and resells them", "revenue = parts + fee")
        b = pair(-1.6, c, "Consigned: the brand supplies the parts", "revenue = fee only")
        tag = estimate_tag("the Works' assembler: 20 million devices a year", corner=DR, size=12)
        with self.voiceover(
            "Part of the answer is in the bookkeeping. <bookmark mark='a'/> Most assemblers buy the parts themselves and "
            "sell the finished device to the brand. Their revenue includes every chip and screen, so the Works' assembler "
            f"books about ${t['revenue'] / 1e9:.1f} billion of revenue for {20} million devices, and its profit of "
            f"${t['profit'] / 1e6:.0f} million is a margin of about {100 * t['margin']:.0f} per cent. <bookmark mark='b'/> If the "
            "brand supplied the parts instead and paid only for the work, the same profit would be "
            f"{100 * c['margin']:.0f} per cent of a much smaller revenue. Nothing about the business changed, only what "
            "counts as revenue. The thin margin is partly an illusion of passing other people's parts through the books."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(a[2]), FadeIn(b[2]), FadeIn(ghost(a[0], b[0], opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(a[0], LEFT), run_time=1.5)
            self.play(GrowFromEdge(a[1], LEFT), FadeIn(a[3]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], LEFT), GrowFromEdge(b[1], LEFT), FadeIn(b[3]))
        self.clear_scene()

    def dupont(self):
        C = R["contract"]
        H = R["hook"]
        m, tv, lev, roe = H["hh_kept"], C["hh_turnover"], C["hh_leverage"], C["hh_roe"]
        def term(top, val, sub, col):
            return VGroup(tx(top, 15, GREY_A), tx(val, 34, col, bold=True), tx(sub, 13, GREY_B)).arrange(DOWN, buff=0.1)
        t1 = term("profit per dollar of sales", f"{100 * m:.1f}%", "thin", ASSEMBLER)
        t2 = term("sales per dollar of assets", f"{tv:.2f}", "fast", PARTS)
        t3 = term("assets per dollar of equity", f"{lev:.2f}", "borrowed and owed", GREY_A)
        t4 = term("return on equity", f"{100 * roe:.1f}%", "Hon Hai, 2025", GOOD)
        x_ = tx("x", 30, WHITE)
        row = VGroup(t1, x_.copy(), t2, x_.copy(), t3, tx("=", 30, WHITE), t4).arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
        inv = VGroup(tx(f"inventory: about {C['hh_inv_days']:.0f} days of costs", 16, WHITE, bold=True),
                     tx(f"research and development: {100 * C['hh_rd']:.1f}% of revenue", 16, WHITE, bold=True)).arrange(DOWN, buff=0.1).move_to([0, -2.0, 0])
        head = tx("How three cents becomes a return", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("Hon Hai, audited consolidated statements 2025 (revenue, profit to owners, total assets, equity, inventories, R&D)", size=13)
        with self.voiceover(
            "The other part is speed. <bookmark mark='a'/> Hon Hai kept about "
            f"{100 * m:.1f} cents of each dollar of sales in 2025. <bookmark mark='b'/> But each dollar of its assets turned "
            f"over about {tv:.1f} times a year in sales. <bookmark mark='c'/> And it finances its assets partly with what it "
            f"owes suppliers and lenders. <bookmark mark='d'/> Multiply them and its owners earned about {100 * roe:.0f} per "
            f"cent on their equity. <bookmark mark='e'/> Its inventory was about {C['hh_inv_days']:.0f} days of costs, and it "
            f"spent {100 * C['hh_rd']:.1f} per cent of revenue on research. An assembler is a machine for turning capital over "
            "fast, not for keeping much of each turn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(row, opacity=0.2)))
            for mk, part in zip("abcd", (t1, VGroup(row[1], t2), VGroup(row[3], t3), VGroup(row[5], t4))):
                vo.wait_until(mk)
                self.play(FadeIn(part, shift=UP * 0.1))
            self.play(Indicate(t4, color=GOOD, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeIn(inv, shift=UP * 0.1))
        self.clear_scene()

    def people(self):
        C = R["contract"]
        reg = C["flex_regions"]
        per = 2000
        names = {"am": "the Americas", "asia": "Asia", "eu": "Europe"}
        cols = {"am": "#B58CFF", "asia": "#F2A65A", "eu": "#7EC8F5"}
        groups = VGroup()
        for i, k in enumerate(("am", "asia", "eu")):
            n = int(round(reg[k] / per))
            g = VGroup(*[draw.person(0.3, cols[k]) for _ in range(n)]).arrange_in_grid(cols=8, buff=(0.06, 0.08))
            lab = VGroup(tx(names[k], 18, cols[k], bold=True), tx(f"{reg[k]:,.0f} people", 15, WHITE)).arrange(DOWN, buff=0.04)
            groups.add(VGroup(g, lab).arrange(DOWN, buff=0.2))
        groups.arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.1, 0])
        key = tx(f"each figure: {per:,} employees of Flex, 31 March 2026", 13, GREY_B).to_edge(DOWN, buff=0.75)
        head = tx("Where a contract manufacturer's people are", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Flex Ltd., Form 10-K for the year to 31 March 2026 (employees by region; net sales by region)", size=13)
        with self.voiceover(
            "And it is a business of people as well as plants. <bookmark mark='a'/> Flex counted about "
            f"{reg['am']:,.0f} people in the Americas, <bookmark mark='b'/> {reg['asia']:,.0f} in Asia, "
            f"<bookmark mark='c'/> and {reg['eu']:,.0f} in Europe. Only {C['flex_china']:.0f} per cent of its sales were "
            "made in China. Flex builds for many industries, not just phones, and spreads its plants across about thirty "
            "countries, close to the customers it builds for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(ghost(*[g_[0] for g_ in groups], opacity=0.2)))
            for mk, g_ in zip("abc", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(p_, scale=0.6) for p_ in g_[0]], lag_ratio=0.02), FadeIn(g_[1]), run_time=1.5)
        self.clear_scene()
