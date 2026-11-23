from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403

# colours for kinds of cost, the same in every company's column
KC = {"goods": "#8B95A7", "people": "#7EC8F5", "research": "#B58CFF", "wear": "#4FD1C5", "fuel": "#F2A65A",
      "other": "#5B6578", "tax": "#E8554E", "profit": "#7BD88F", "bad": "#F2C14E"}
LINE_KIND = {"Merchandise": "goods", "Stores, staff, overheads": "people", "Operating profit": "profit",
             "Cost of revenue": "goods", "Research": "research", "Selling and admin": "people", "Labour": "people",
             "Fuel": "fuel", "Everything else": "other", "Making the medicines": "goods", "Other charges": "other",
             "Fuel and power bought": "fuel", "Running the plants": "people", "Depreciation": "wear",
             "Taxes and other": "other"}


class Income(VoiceoverScene):
    def construct(self):
        card(self, 3, "The income statement", "Of every dollar a company takes in, how much does it keep?",
             "Chapter three. The income statement.", lit=("dollar",))
        self.bakery()
        self.five()

    def bakery(self):
        inc = R["bakery_year"]["income"]
        steps = [("Sales", inc["revenue"], "total", I.MONEY), ("Flour and fillings", -inc["cogs"], "step", KC["goods"]),
                 ("Gross profit", inc["gross"], "total", I.TEXT),
                 ("Staff and rent", -inc["fixed"], "step", KC["people"]),
                 ("The oven's wear", -inc["depreciation"], "step", KC["wear"]),
                 ("Operating profit", inc["ebit"], "total", I.TEXT), ("Interest", -inc["interest"], "step", KC["other"]),
                 ("Tax", -inc["tax"], "step", KC["tax"]), ("Net profit", inc["net"], "total", KC["profit"])]
        s = 4.4 / inc["revenue"]
        base = -2.2
        x0, dx = -5.6, 1.4
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        level = 0.0
        for k, (lab, v, kind, col) in enumerate(steps):
            x = x0 + k * dx
            if kind == "total":
                lo, hi = 0.0, v
                level = v
            else:
                lo, hi = level + v, level
                level = level + v
            h = max((hi - lo) * s, 0.02)
            r = Rectangle(width=1.0, height=h, fill_color=col, fill_opacity=0.9 if kind == "step" else 0.75,
                          stroke_width=0).move_to(np.array([x, base + (lo + hi) / 2 * s, 0]))
            bars.add(r)
            t = T(lab, 15, I.TEXT)
            if t.width > 1.3:
                t = VGroup(*[T(w, 15, I.TEXT) for w in lab.split(" ", 1)]).arrange(DOWN, buff=0.04)
            labs.add(t.next_to(np.array([x, base, 0]), DOWN, buff=0.15))
            vals.add(TB(f"{'-' if kind == 'step' else ''}${abs(v):,.0f}", 16, col if kind == "step" else I.TEXT
                        ).next_to(r, UP, buff=0.06))
        axis = Line(np.array([-6.3, base, 0]), np.array([6.3, base, 0]), color=I.EDGE)
        head = T("The bakery's first year: its income statement", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = estimate_tag("illustrative: a model bakery, 60,000 loaves at $3.60", corner=DR)
        r = R["bakery_year"]["ratios"]
        with self.voiceover(
            "Now a whole year. The bakery sells sixty thousand loaves and cakes at three dollars sixty: "
            f"<bookmark mark='a'/> {say_usd(inc['revenue'])} of sales. <bookmark mark='b'/> Take off what went into "
            f"them, the flour, butter and fillings, and {say_usd(inc['gross'])} is left: the gross profit, "
            f"{say_pct(r['gross_margin'])} of sales. <bookmark mark='c'/> Then the costs of being open at all: the "
            "staff, the owner's own pay and the rent, a hundred and fifteen thousand. <bookmark mark='d'/> And one "
            "cost that is never paid in the year at all. The oven cost forty-five thousand and should last ten "
            "years, so each year carries a tenth of it, four thousand five hundred dollars. Accountants call it "
            f"depreciation. <bookmark mark='e'/> What is left is the operating profit, {say_usd(inc['ebit'])}: what "
            "the business itself earns. <bookmark mark='f'/> Interest to the bank and tax to the government come "
            f"off, and the net profit, the bottom line, is {say_usd(inc['net'])}: about six cents on each dollar of "
            "sales."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            marks = {"a": [0], "b": [1, 2], "c": [3], "d": [4], "e": [5], "f": [6, 7, 8]}
            for m, idx in marks.items():
                vo.wait_until(m)
                self.play(*[AnimationGroup(GrowFromEdge(bars[i], DOWN if steps[i][2] == "total" else UP),
                                           FadeIn(labs[i]), FadeIn(vals[i])) for i in idx], run_time=0.9)
        self.clear_scene()

    def five(self):
        D = R["dollar"]
        order = ["cost", "msft", "dal", "lly", "nee"]
        H, W = 5.0, 1.45
        cols = VGroup()
        for i, k in enumerate(order):
            x = -5.4 + i * 2.7
            y = 2.35
            g = VGroup()
            for lab, v in D[k]:
                h = H * v
                kind = LINE_KIND[lab]
                rr = Rectangle(width=W, height=max(h, 0.01), fill_color=KC[kind], fill_opacity=0.92,
                               stroke_color=BACKGROUND, stroke_width=1.2).move_to(np.array([x, y - h / 2, 0]))
                txt = VGroup()
                if h > 0.42:
                    txt = VGroup(TB(f"{100 * v:.0f}¢", 17, "#0E1117"), T(lab.lower(), 12, "#0E1117")).arrange(
                        DOWN, buff=0.02)
                    if txt.width > W - 0.1:
                        txt.scale_to_fit_width(W - 0.1)
                    txt.move_to(rr)
                elif h > 0.18:
                    txt = TB(f"{100 * v:.0f}¢ {lab.lower()}", 12, "#0E1117")
                    if txt.width > W - 0.08:
                        txt.scale_to_fit_width(W - 0.08)
                    txt.move_to(rr)
                g.add(VGroup(rr, txt))
                y -= h
            nm = TB(name(k), 19, CO[k]).next_to(np.array([x, 2.35, 0]), UP, buff=0.15)
            gl = _glyph(k)
            gl.scale_to_fit_height(min(gl.height, 0.5)).next_to(nm, UP, buff=0.12)
            cols.add(VGroup(VGroup(nm, gl), g))
        head = T("Where each dollar of sales goes", 22, I.TEXT).to_corner(UL, buff=0.3)
        src = source("Forms 10-K: Costco and Microsoft fiscal 2026, Delta, Lilly and NextEra 2025", size=13)
        J = dict(D["jpm"])
        with self.voiceover(
            "The income statement of a real company has the same shape, and the shape is the business. Here is one "
            "dollar of sales at five companies. <bookmark mark='a'/> Costco: 87 cents pays for the goods on its "
            "shelves, nine for the warehouses, staff and overheads, and less than four cents is left as operating "
            "profit. <bookmark mark='b'/> Microsoft: the copies of its software cost almost nothing, so most of its "
            "costs are people and data centres, and it keeps 47 cents. <bookmark mark='c'/> Delta: 28 cents to its "
            "people, 15 for fuel, 48 for everything else an airline needs, from aircraft to airports, and nine cents "
            "of profit. <bookmark mark='d'/> Eli Lilly: 17 cents to make its medicines, 20 on research for the next "
            "ones, 17 to sell them, and 40 cents of profit. <bookmark mark='e'/> NextEra, the power company: its "
            "largest cost is depreciation, the wear on its power plants and wires, 24 cents of every dollar, a cost "
            "that, like the bakery's oven, was paid for years ago. A bank's statement looks different again: of "
            f"JPMorgan's dollar, {100 * J['Staff and overheads']:.0f} cents goes on its people and offices and about "
            f"{100 * J['Loans gone bad (provision)']:.0f} on loans expected to go bad."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                c = cols[i]
                dollar = draw.coin(0.16).move_to(c[1].get_top() + UP * 0.05)
                self.play(FadeIn(c[0], shift=DOWN * 0.1), FadeIn(dollar, scale=1.5), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.05) for s in c[1]], lag_ratio=0.15),
                          dollar.animate.move_to(c[1].get_bottom() + DOWN * 0.15), run_time=1.3, rate_func=linear)
                self.play(FadeOut(dollar, scale=0.3), run_time=0.3)
            self.play(Indicate(VGroup(*[c[1][-1] for c in cols]), color=KC["profit"], scale_factor=1.04))
        self.clear_scene()


def _glyph(k: str) -> VGroup:
    """A small picture of each of the five businesses."""
    if k == "cost":  # a shopping cart
        basket = Polygon([-0.3, 0.15, 0], [0.3, 0.15, 0], [0.22, -0.12, 0], [-0.22, -0.12, 0], stroke_color="#C9D3E0",
                         stroke_width=3, fill_color="#C9D3E0", fill_opacity=0.25)
        handle = Line([-0.3, 0.15, 0], [-0.42, 0.28, 0], stroke_color="#C9D3E0", stroke_width=3)
        wheels = VGroup(*[Circle(radius=0.05, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([x, -0.2, 0])
                          for x in (-0.16, 0.16)])
        return VGroup(basket, handle, wheels)
    if k == "msft":
        return draw.server_rack(0.6)
    if k == "dal":
        return draw.plane(1.1, windows=False)
    if k == "lly":  # a capsule
        a = RoundedRectangle(corner_radius=0.12, width=0.3, height=0.24, stroke_width=0, fill_color="#E8554E",
                             fill_opacity=1).shift(LEFT * 0.12)
        b = RoundedRectangle(corner_radius=0.12, width=0.3, height=0.24, stroke_width=0, fill_color="#E8EAED",
                             fill_opacity=1).shift(RIGHT * 0.12)
        return VGroup(a, b).rotate(0.5)
    return draw.wind_turbine(0.6)
