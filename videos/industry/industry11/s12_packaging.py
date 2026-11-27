from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Packaging(VoiceoverScene):
    def construct(self):
        card(self, 10, "Boxes, cans and bottles", "Why do a few companies make most of the world's packaging?",
             "Chapter ten. Boxes, cans and bottles.", lit=("make", "moat"))
        self.few()
        self.merge()
        self.paper()

    def few(self):
        P = R["packaging"]
        items = [("corrugated boxes", P["cr4_box"], draw.carton(0.7)), ("containerboard mills", P["cr4_board"], draw.coil(0.3, PACK)),
                 ("metal cans", P["cr4_cans"], draw.can(0.7)), ("glass containers", P["cr4_glass"], draw.bottle(0.6, "#7BD88F", 0.8))]
        rows = VGroup()
        for i, (n, (cr, firms), ic) in enumerate(items):
            y = 1.6 - 1.15 * i
            ic.scale_to_fit_height(0.7)
            ic.move_to([-5.2, y, 0])
            bg = Rectangle(width=6.0, height=0.42, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to([-3.8, y, 0],
                                                                                                         aligned_edge=LEFT)
            fg = Rectangle(width=6.0 * cr / 100, height=0.42, stroke_width=0, fill_color=PACK, fill_opacity=0.95).move_to(
                [-3.8, y, 0], aligned_edge=LEFT)
            lab = VGroup(tx(n, 17, WHITE, bold=True), tx(f"{firms:,.0f} firms", 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.02).next_to(
                bg, UP, buff=0.05).align_to(bg, LEFT)
            val = tx(f"{cr:.0f}%", 18, WHITE, bold=True).next_to(fg, RIGHT, buff=0.1)
            rows.add(VGroup(ic, bg, fg, lab, val))
        head = tx("Share of US sales made by the four largest firms, 2022", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        why = VGroup(tx("Continuous processes", 20, PACK, bold=True),
                     tx("a paper machine, a glass furnace and a can line", 15, GREY_A),
                     tx("run day and night, for years: huge, costly,", 15, GREY_A),
                     tx("and cheapest per unit when big and full", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(
            [4.6, 0.2, 0])
        src = source("US Census Bureau, 2022 Economic Census: concentration of largest firms (NAICS 322211, 322130, 332431, "
                     "327213)", size=13)
        with self.voiceover(
            "The heavy-materials family has a lighter branch: packaging. The boxes, cans and bottles that everything "
            "else is shipped and sold in. <bookmark mark='a'/> In the United States, the four largest firms make about "
            f"half of all corrugated boxes, <bookmark mark='b'/> two thirds of the containerboard they are made from, "
            f"<bookmark mark='c'/> {P['cr4_cans'][0]:.0f} per cent of metal cans, <bookmark mark='d'/> and "
            f"{P['cr4_glass'][0]:.0f} per cent of glass bottles and jars, which come from just "
            f"{P['cr4_glass'][1]:.0f} firms. <bookmark mark='e'/> Like steel, these are continuous processes: a paper "
            "machine, a glass furnace, a can line, running day and night, cheapest per box or per can when they are big "
            "and full. That pushes the industry into fewer, larger hands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(VGroup(r_[0], r_[1], r_[3])) for r_ in rows])
            for m_, r_ in zip("abcd", rows):
                vo.wait_until(m_)
                self.play(GrowFromEdge(r_[2], LEFT), FadeIn(r_[4]), run_time=0.9)
            vo.wait_until("e")
            self.play(FadeIn(why, shift=LEFT * 0.2))
        self.clear_scene()

    def merge(self):
        L = {c["ticker"]: c for c in R["landscape"]["companies"]}
        sec = R["packaging"]["companies"]
        a = VGroup(draw.carton(0.8), tx("Smurfit Kappa", 18, WHITE, bold=True), tx("Ireland", 13, GREY_A)).arrange(DOWN, buff=0.08)
        b = VGroup(draw.carton(0.8), tx("WestRock", 18, WHITE, bold=True), tx("United States", 13, GREY_A)).arrange(DOWN, buff=0.08)
        VGroup(a, b).arrange(RIGHT, buff=1.4).move_to([-3.6, 1.2, 0])
        sw = VGroup(draw.carton(1.1), tx("Smurfit Westrock", 22, PACK, bold=True),
                    tx(f"5 July 2024; revenue ${sec['SW']['revenue']:.1f}bn in {sec['SW']['year']}", 15, GREY_A)).arrange(
            DOWN, buff=0.08).move_to([-3.6, -1.6, 0])
        c = VGroup(draw.carton(0.8), tx("International Paper", 18, WHITE, bold=True), tx("United States", 13, GREY_A)).arrange(
            DOWN, buff=0.08)
        d = VGroup(draw.carton(0.8), tx("DS Smith", 18, WHITE, bold=True), tx("Britain", 13, GREY_A)).arrange(DOWN, buff=0.08)
        VGroup(c, d).arrange(RIGHT, buff=1.4).move_to([3.4, 1.2, 0])
        ip = VGroup(draw.carton(1.1), tx("International Paper", 22, PACK, bold=True),
                    tx(f"31 January 2025; revenue ${sec['IP']['revenue']:.1f}bn in {sec['IP']['year']}", 15, GREY_A)).arrange(
            DOWN, buff=0.08).move_to([3.4, -1.6, 0])
        ar1 = VGroup(Arrow(a.get_bottom(), sw.get_top(), buff=0.15, color=GREY_B, stroke_width=2.5, tip_length=0.12),
                     Arrow(b.get_bottom(), sw.get_top(), buff=0.15, color=GREY_B, stroke_width=2.5, tip_length=0.12))
        ar2 = VGroup(Arrow(c.get_bottom(), ip.get_top(), buff=0.15, color=GREY_B, stroke_width=2.5, tip_length=0.12),
                     Arrow(d.get_bottom(), ip.get_top(), buff=0.15, color=GREY_B, stroke_width=2.5, tip_length=0.12))
        marg = tx(f"Profit kept per dollar of sales, five-year average: Smurfit Westrock {100 * sec['SW']['margin5']:.0f}%, "
                  f"International Paper {100 * sec['IP']['margin5']:.0f}%, Packaging Corp. {100 * sec['PKG']['margin5']:.0f}%",
                  15, GREY_A).to_edge(DOWN, buff=0.55)
        src = source("Smurfit Westrock and International Paper, Forms 10-K 2025; SEC company facts", size=13)
        with self.voiceover(
            "And the hands keep getting fewer. <bookmark mark='a'/> In July 2024, Ireland's Smurfit Kappa and America's "
            "WestRock closed their combination, <bookmark mark='b'/> making Smurfit Westrock, with about "
            f"{sec['SW']['revenue']:.0f} billion dollars of sales in 2025, one of the largest box makers in the world. "
            "<bookmark mark='c'/> Six months later, in January 2025, International Paper bought Britain's DS Smith. "
            "<bookmark mark='d'/> Bigger, though, has not meant richer. Over the last five years Smurfit Westrock kept "
            f"about {100 * sec['SW']['margin5']:.0f} cents of every dollar of sales as profit, International Paper about "
            f"{100 * sec['IP']['margin5']:.0f}, after losses on what it sold and closed. The best of the group, "
            f"Packaging Corporation of America, North America's third-largest containerboard maker, about "
            f"{100 * sec['PKG']['margin5']:.0f}."
        ) as vo:
            self.play(FadeIn(src), FadeIn(a), FadeIn(b), FadeIn(c), FadeIn(d))
            vo.wait_until("a")
            self.play(GrowArrow(ar1[0]), GrowArrow(ar1[1]))
            vo.wait_until("b")
            self.play(FadeIn(sw, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(GrowArrow(ar2[0]), GrowArrow(ar2[1]), FadeIn(ip, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(marg, shift=UP * 0.1))
        self.clear_scene()

    def paper(self):
        P = R["packaging"]
        ip = P["ip_paper"]
        ys = sorted(ip)
        box = P["ppi"]["PCU322211322211"]
        pa = viz.plot_axes([1971, 2026.5], [60, 180], x_length=10.0, y_length=4.2, xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                           yticks=[80, 120, 160], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}",
                           ylabel="output of US pulp, paper and paperboard mills (2017 = 100)", size=13).move_to([-0.6, -0.4, 0])
        ln = VMobject(stroke_color=PACK, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, ip[y]) for y in ys])
        pk = max(ys, key=lambda y: ip[y])
        mk = VGroup(Dot(pa.ax.c2p(pk, ip[pk]), radius=0.06, color=WHITE),
                    tx(f"{pk}: {ip[pk]:.0f}", 14, WHITE).next_to(pa.ax.c2p(pk, ip[pk]), UP, buff=0.08))
        ys_last = ys[-1]
        mk2 = VGroup(Dot(pa.ax.c2p(ys_last, ip[ys_last]), radius=0.06, color=WHITE),
                     tx(f"{ys_last}: {ip[ys_last]:.0f}", 14, WHITE).next_to(pa.ax.c2p(ys_last, ip[ys_last]), DOWN, buff=0.08))
        side = VGroup(tx("The price of a box", 16, WHITE, bold=True), tx("producer price index", 13, GREY_A),
                      tx(f"2000: {box[2000]:.0f}", 15, GREY_A), tx(f"2025: {box[2025]:.0f}", 15, PACK, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.5)
        src = source("Federal Reserve G.17, industrial production: pulp, paper and paperboard mills (IPG3221S); BLS PPI, "
                     "corrugated and solid fiber boxes (PCU322211322211); via FRED", size=12)
        with self.voiceover(
            "There is a reason for the mergers. <bookmark mark='a'/> Here is the output of America's pulp, paper and "
            f"board mills since 1972. It peaked in {pk}, <bookmark mark='b'/> and by {ys_last} it had fallen by "
            f"{100 * (1 - ip[ys_last] / ip[pk]):.0f} per cent. Newspapers, magazines, letters and office paper moved to "
            "screens, and many of the mills that made paper for them closed. <bookmark mark='c'/> Boxes held up "
            "better, and the producer price of a box more than doubled between 2000 and 2025. A shrinking industry "
            "with a sturdier corner consolidates: the survivors buy each other, close the weakest mills, and try to "
            "keep the rest full."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            self.play(FadeIn(mk))
            vo.wait_until("b")
            self.play(FadeIn(mk2))
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.2))
        self.clear_scene()
