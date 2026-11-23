from __future__ import annotations

import math

from videos.industry.industry3.common import *  # noqa: F403


class DuPont(VoiceoverScene):
    def construct(self):
        card(self, 7, "Margin, speed and borrowing", "How can a grocer earn as much on its money as a software company?",
             "Chapter seven. Margin, speed and borrowing.", lit=("dollar", "moat"))
        self.identity()
        self.map()
        self.leverage()

    def identity(self):
        def box(top, bottom, color):
            t = VGroup(TB(top, 22, color), T(bottom, 16, I.DIM)).arrange(DOWN, buff=0.08)
            b = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=1.25, fill_color=I.PANEL,
                                 fill_opacity=1, stroke_color=color, stroke_width=2)
            return VGroup(b, t.move_to(b))
        roe = box("Return on equity", "profit per $ the owners put in", I.ACCENT)
        m = box("Margin", "profit per $ of sales", "#4FA3F7")
        t = box("Speed", "sales per $ of assets", "#7BD88F")
        lv = box("Borrowing", "assets per $ of owners' money", "#F2A65A")
        row = VGroup(roe, TB("=", 40, I.TEXT), m, TB("×", 40, I.TEXT), t, TB("×", 40, I.TEXT), lv).arrange(
            RIGHT, buff=0.22)
        if row.width > 13.2:
            row.scale_to_fit_width(13.2)
        row.move_to(UP * 0.9)
        r = R["bakery_year"]["ratios"]
        ex = VGroup(T("The bakery:", 22, I.DIM), TB(f"{100 * r['roe']:.0f}%", 26, I.ACCENT), T("=", 24, I.TEXT),
                    TB(f"{100 * r['net_margin']:.1f}%", 26, "#4FA3F7"), T("×", 24, I.TEXT),
                    TB(f"{r['turnover']:.2f}", 26, "#7BD88F"), T("×", 24, I.TEXT),
                    TB(f"{r['leverage']:.2f}", 26, "#F2A65A")).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.3)
        with self.voiceover(
            "Donaldson Brown's split, extended by one more step, is the most useful formula in this part. "
            "<bookmark mark='a'/> What the owners care about is the return on their money: the year's profit for "
            "every dollar they have in the business. <bookmark mark='b'/> It is the product of three things. The "
            "margin: how much profit each dollar of sales leaves. <bookmark mark='c'/> The speed: how many dollars "
            "of sales each dollar of assets produces in a year. <bookmark mark='d'/> And the borrowing: how many "
            "dollars of assets each dollar of the owners' money supports, the rest coming from lenders and "
            f"suppliers. <bookmark mark='e'/> For the bakery: a margin of {100 * r['net_margin']:.1f} percent, "
            f"times {r['turnover']:.1f} dollars of sales per dollar of assets, times {r['leverage']:.1f}, gives "
            f"{say_pct(r['roe'])} on the owner's money. There are three ways to a good return, and each industry "
            "takes a different one."
        ) as vo:
            self.play(FadeIn(row[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(row[0], color=I.ACCENT, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(row[1]), FadeIn(row[2]))
            vo.wait_until("c")
            self.play(FadeIn(row[3]), FadeIn(row[4]))
            vo.wait_until("d")
            self.play(FadeIn(row[5]), FadeIn(row[6]))
            vo.wait_until("e")
            self.play(FadeIn(ex, shift=UP * 0.1))
        self.clear_scene()

    def map(self):
        S = R["six"]
        lx = lambda v: math.log10(v)  # noqa: E731
        ax = Axes(x_range=[lx(0.025), lx(6), 1], y_range=[lx(0.008), lx(0.8), 1], x_length=7.8, y_length=5.2,
                  axis_config=dict(color=I.EDGE, include_ticks=False, include_tip=False)).shift(LEFT * 1.7 + DOWN * 0.3)
        xt = VGroup(*[T(f"${v:g}", 14, I.DIM).next_to(ax.c2p(lx(v), lx(0.008)), DOWN, buff=0.1)
                      for v in (0.03, 0.1, 0.3, 1, 3)])
        yt = VGroup(*[T(f"{100 * v:g}¢", 14, I.DIM).next_to(ax.c2p(lx(0.025), lx(v)), LEFT, buff=0.1)
                      for v in (0.01, 0.03, 0.1, 0.3)])
        xl = T("speed: sales per $ of assets (log scale)", 16, "#7BD88F").next_to(ax, DOWN, buff=0.45)
        yl = T("margin: net profit per $ of sales", 16, "#4FA3F7").rotate(PI / 2).next_to(ax, LEFT, buff=0.75)
        curves = VGroup()
        for roa in (0.01, 0.03, 0.1, 0.3):
            xs = np.linspace(lx(max(0.025, roa / 0.8)), lx(min(6, roa / 0.008)), 60)
            pts = [ax.c2p(x, lx(roa) - x) for x in xs]
            c = VMobject(stroke_color=I.FAINT, stroke_width=1.5).set_points_smoothly(pts)
            lab = T(f"{100 * roa:g}% on assets", 13, I.FAINT).move_to(pts[-1] + np.array([0.05, 0.2, 0])).shift(
                LEFT * 0.5)
            curves.add(VGroup(DashedVMobject(c, num_dashes=40), lab))
        dots = VGroup()
        for k, d in S.items():
            p = ax.c2p(lx(d["turnover"]), lx(d["net_margin"]))
            dot = Dot(p, radius=0.11, color=CO[k])
            lab = T(name(k), 16, CO[k]).next_to(dot, UR if k != "lly" else DR, buff=0.06)
            dots.add(VGroup(dot, lab))
        keys = list(S)
        head = T("Two ways to the same return on assets", 22, I.TEXT).to_corner(UL, buff=0.35)
        side = VGroup(*[T(f"{name(k)}: {100 * S[k]['roa']:.1f}% on assets", 16, CO[k]) for k in keys]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(RIGHT, buff=0.35)
        src = source("Forms 10-K (Costco, Microsoft FY2026; others 2025); net income over year-end assets", size=13)
        c, m, j = S["cost"], S["msft"], S["jpm"]
        with self.voiceover(
            "Put the six companies on a map of the first two. <bookmark mark='a'/> Across, the speed: dollars of "
            "sales per dollar of assets. Up, the margin. The dashed curves join points with the same return on "
            "assets, margin times speed. <bookmark mark='b'/> Costco is far to the right: it sells "
            f"{c['turnover']:.1f} dollars of goods a year for every dollar it owns, at a margin of "
            f"{100 * c['net_margin']:.0f} cents. <bookmark mark='c'/> Microsoft is far up: {100 * m['net_margin']:.0f} "
            f"cents of profit on each dollar, but only {100 * m['turnover']:.0f} cents of sales a year from each "
            "dollar of data centres and everything else. Opposite businesses; both earn ten percent or more on "
            "their assets. <bookmark mark='d'/> Lilly is high and fairly fast. The airline is in the middle. "
            "The power company and the bank sit low and slow: NextEra needs a dollar of assets for every thirteen "
            f"cents of yearly sales, and JPMorgan earns {100 * j['roa']:.1f} cents a year on each dollar of assets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cv) for cv in curves], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(dots[keys.index("cost")], scale=1.5), FadeIn(side[keys.index("cost")]))
            vo.wait_until("c")
            self.play(FadeIn(dots[keys.index("msft")], scale=1.5), FadeIn(side[keys.index("msft")]))
            vo.wait_until("d")
            rest = [keys.index(k) for k in ("lly", "dal", "nee", "jpm")]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i], scale=1.5), FadeIn(side[i])) for i in rest],
                                  lag_ratio=0.3), run_time=2)
        self.clear_scene()

    def leverage(self):
        S = R["six"]
        order = sorted(S, key=lambda k: S[k]["roe"])
        rows = VGroup()
        hdr = VGroup(T("", 18), TB("on assets", 18, "#7BD88F"), T("", 18), TB("borrowing", 18, "#F2A65A"), T("", 18),
                     TB("on equity", 18, I.ACCENT))
        xs = [-5.6, -1.6, -0.3, 1.0, 2.4, 3.9]
        for c, x in zip(hdr, xs):
            c.move_to(np.array([x, 2.3, 0]), aligned_edge=LEFT)
        rows.add(hdr)
        for r_, k in enumerate(order):
            d = S[k]
            y = 1.65 - r_ * 0.62
            cells = [TB(name(k), 20, CO[k]), T(f"{100 * d['roa']:.1f}%", 22, "#7BD88F"), T("×", 22, I.TEXT),
                     T(f"{d['leverage']:.1f}", 22, "#F2A65A"), T("=", 22, I.TEXT), TB(f"{100 * d['roe']:.0f}%", 24,
                                                                                   I.ACCENT)]
            row = VGroup()
            for c, x in zip(cells, xs):
                row.add(c.move_to(np.array([x, y, 0]), aligned_edge=LEFT))
            rows.add(row)
        j = S["jpm"]
        warn = VGroup(T(f"JPMorgan: owners' money is {100 / j['leverage']:.1f}¢ of each $ of assets", 18, I.COST),
                      T("a loss that size on its assets would wipe it out", 18, I.COST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).to_edge(DOWN, buff=0.85)
        head = T("The third lever: borrowing multiplies the return on assets", 22, I.TEXT).to_corner(UL, buff=0.35)
        src = source("Forms 10-K; return on equity here is net income over year-end equity", corner=DR, size=13)
        lly = S["lly"]
        with self.voiceover(
            "Now the third lever. <bookmark mark='a'/> Multiply the return on assets by how far the owners' money "
            "is stretched, and you get the return on the owners' money. <bookmark mark='b'/> The bank earns only "
            f"{100 * j['roa']:.1f} percent on its assets, but it holds {j['leverage']:.0f} dollars of assets for "
            f"every dollar of its owners' money, so its owners earn about {say_pct(j['roe'])}. Borrowing is the "
            "bank's business. <bookmark mark='c'/> It cuts both ways. With eight cents of owners' money behind each "
            "dollar of assets, a loss of eight cents in the dollar on what it has lent and invested would wipe the "
            "owners out. That is why regulators watch banks' capital so closely. <bookmark mark='d'/> And at the top, "
            f"Lilly's {say_pct(lly['roe'])} is partly the drug business and partly arithmetic: years of buying back "
            "its own shares shrank the owners' money on the balance sheet, so every dollar of profit is divided by "
            "less. A high return on equity can mean a great business, or a lot of borrowing, or both. The formula "
            "tells you which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.15), run_time=2.2)
            vo.wait_until("b")
            self.play(Indicate(rows[1 + order.index("jpm")], color="#B58CFF", scale_factor=1.04))
            vo.wait_until("c")
            self.play(FadeIn(warn))
            vo.wait_until("d")
            self.play(Indicate(rows[-1], color=I.ACCENT, scale_factor=1.04))
        self.clear_scene()
