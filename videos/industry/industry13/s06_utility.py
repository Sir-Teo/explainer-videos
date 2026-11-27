from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Utility(VoiceoverScene):
    def construct(self):
        card(self, 5, "The regulated utility", "Who decides what the wires earn?", "Chapter five. The regulated utility.",
             lit=("dollar", "moat", "state"))
        self.dollar()
        self.requirement()
        self.cases()

    def dollar(self):
        U = R["utility"]
        sp = U["split"]
        tot = U["total_c"]
        parts = [("generation", sp["generation"], GAS, draw.gas_plant(0.9)), ("transmission", sp["transmission"], WIND, draw.pylon(1.1)),
                 ("distribution", sp["distribution"], STORE, VGroup(Line(DOWN * 0.5, UP * 0.5, stroke_color="#8C929B", stroke_width=5),
                                                                     Line(LEFT * 0.3 + UP * 0.4, RIGHT * 0.3 + UP * 0.4, stroke_color="#8C929B",
                                                                          stroke_width=4), draw.house(0.5).shift(RIGHT * 0.7 + DOWN * 0.3)))]
        x = -4.8
        bars, pics, labs = VGroup(), VGroup(), VGroup()
        for name, v, col, ic in parts:
            w = v / tot * 10.0
            b = Rectangle(width=w, height=1.0, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=0.88).move_to(
                [x, -0.4, 0], aligned_edge=LEFT)
            bars.add(b)
            ic.scale_to_fit_height(min(ic.height, 1.1)).next_to(b, UP, buff=0.3)
            pics.add(ic)
            labs.add(VGroup(tx(name, 18, col, bold=True), tx(f"{v:.2f}¢ ({100 * v / tot:.0f}%)", 16, WHITE)).arrange(
                DOWN, buff=0.04).next_to(b, DOWN, buff=0.2))
            x += w
        head = tx(f"A kilowatt-hour in America, 2020: {tot:.2f} cents on average", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("EIA, Annual Energy Outlook 2021, Table 8 (end-use prices by service category, 2020)", size=13)
        note = tx("the wires: almost half of the bill", 18, PRICE, bold=True).move_to([2.6, -2.6, 0])
        with self.voiceover(
            "Follow a customer's dollar. In 2020, the average kilowatt-hour in America cost about "
            f"{tot:.0f} cents, and the government's energy agency splits it three ways. <bookmark mark='a'/> About "
            f"{sp['generation']:.1f} cents paid for making the power. <bookmark mark='b'/> About {sp['transmission']:.1f} "
            "for the high-voltage lines that carry it across the country. <bookmark mark='c'/> And about "
            f"{sp['distribution']:.1f} for the local poles, wires and transformers that bring it to your door. "
            "<bookmark mark='d'/> The wires take almost half the bill, and they are a natural monopoly: no one builds a "
            "second set of poles down your street. So in America they are owned by regulated utilities, and the state "
            "decides what they may earn."
        ) as vo:
            for b_ in bars:
                b_.set_fill(opacity=0.15)
            coin = VGroup(Circle(0.55, stroke_color=PRICE, stroke_width=4, fill_color=PRICE, fill_opacity=0.2),
                          tx("1 kWh", 16, PRICE, bold=True)).move_to([-5.9, -0.4, 0])
            self.play(FadeIn(head), FadeIn(src), FadeIn(bars), FadeIn(coin))
            for m_, i in zip("abc", range(3)):
                vo.wait_until(m_)
                self.play(bars[i].animate.set_fill(opacity=0.88), FadeIn(pics[i], shift=DOWN * 0.1), FadeIn(labs[i]), run_time=1.0)
            vo.wait_until("d")
            self.play(Indicate(VGroup(bars[1], bars[2]), color=PRICE, scale_factor=1.03), FadeIn(note))
        self.clear_scene()

    def requirement(self):
        U = R["utility"]
        q = U["req"]
        items = [("operations and maintenance", q["om"], GREY_B), ("depreciation", q["depreciation"], WIND),
                 ("income taxes", q["tax"], COAL), ("the allowed return", q["return"], PRICE)]
        sc = 4.6 / q["total"]
        y = -2.6
        blocks = VGroup()
        for name, v, col in items:
            b = Rectangle(width=2.0, height=v * sc, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=0.88).move_to(
                [-2.0, y, 0], aligned_edge=DOWN)
            lab = tx(f"{name}: ${v / 1000:.2f}bn", 15, col, bold=True).next_to(b, LEFT, buff=0.2)
            blocks.add(VGroup(b, lab))
            y += v * sc
        tot = tx(f"revenue requirement: ${q['total'] / 1000:.2f}bn a year", 19, WHITE, bold=True).next_to(blocks, UP, buff=0.15)
        rb = VGroup(tx(f"rate base: ${U['rate_base'] / 1000:.0f}bn of plant and wires", 17, WHITE, bold=True),
                    tx(f"financed {100 * U['equity']:.0f}% by shareholders, allowed {100 * U['roe']:.0f}%", 15, GREY_A),
                    tx(f"the rest by lenders, at about 5%", 15, GREY_A),
                    tx(f"÷ {U['sales']:.0f} billion kWh sold", 17, WHITE, bold=True),
                    tx(f"= {q['cents']:.1f} cents a kWh", 24, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.6, 0.4, 0])
        aj = VGroup(tx("one point more on the allowed return:", 15, GREY_A),
                    tx(f"+${(U['roe_hi']['total'] - q['total']):,.0f}m a year from customers", 17, BAD, bold=True),
                    tx("and the more you invest, the more you earn", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.6, -2.2, 0])
        tag = estimate_tag("the Works (power.py): an illustrative utility, not any company's numbers", corner=DR, size=12)
        with self.voiceover(
            "How does the state decide? With a formula, set in a rate case. Play it with an imaginary utility. "
            f"<bookmark mark='a'/> It owns {U['rate_base'] / 1000:.0f} billion dollars of plant and wires: its rate base. "
            "<bookmark mark='b'/> Customers pay its running costs, and the wear on its assets, depreciation, and its "
            "taxes. <bookmark mark='c'/> And on top, a return on the rate base: interest for the lenders, and an allowed "
            f"return on equity for the shareholders, here {100 * U['roe']:.0f} per cent. Add it up and divide by the "
            f"kilowatt-hours it sells, and you have the price: about {q['cents']:.0f} cents. <bookmark mark='d'/> Notice "
            "what the formula rewards. The profit is a percentage of the rate base, so the way to earn more is to build "
            "more: economists call it the Averch-Johnson effect. And every point on the allowed return is worth "
            f"hundreds of millions of dollars a year, so both sides fight over it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rb[0]))
            vo.wait_until("a")
            self.play(Indicate(rb[0], color=PRICE))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in blocks[:3]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b_[1]) for b_ in blocks[:3]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(blocks[3][0], DOWN), FadeIn(blocks[3][1]), FadeIn(rb[1:3]))
            self.play(FadeIn(tot), FadeIn(rb[3:]))
            vo.wait_until("d")
            self.play(FadeIn(aj, shift=UP * 0.1))
        self.clear_scene()

    def cases(self):
        U = R["utility"]
        cases, pend = U["cases"], U["pending"]
        names = {"dec_nc_2023": "Carolinas, N.C. 2023", "dep_nc_2022": "Progress, N.C. 2022", "dei_2024": "Indiana 2024",
                 "def_2024": "Florida 2024", "dec_sc_2024": "Carolinas, S.C. 2024", "dek_2024": "Kentucky 2024",
                 "dek_2022": "Kentucky 2022", "dep_sc_2025": "Progress, S.C. 2025", "dep_sc_2022": "Progress, S.C. 2022",
                 "dec_sc_2025": "Carolinas, S.C. 2025", "deo_2021": "Ohio 2021", "dec_nc_2025": "Carolinas, N.C. 2025",
                 "dep_nc_2025": "Progress, N.C. 2025"}
        rows = sorted(cases, key=lambda c: -c[1])
        pa = viz.plot_axes([9.3, 11.1], [0, len(rows) + 3], x_length=6.4, y_length=5.2, xticks=[9.5, 10.0, 10.5, 11.0], yticks=[],
                           xfmt=lambda v: f"{v:.1f}%", size=14, grid=False).move_to([0.6, -0.3, 0])
        dots = VGroup()
        for i, (k, rev, roe) in enumerate(rows):
            y = len(rows) + 2 - i
            d_ = Dot(pa.ax.c2p(roe, y), radius=0.06 + 0.10 * (rev / 1000) ** 0.5, color=GOOD, fill_opacity=0.85)
            lab = tx(f"{names[k]}: ${rev:,.0f}m", 12, GREY_A).next_to(pa.ax.c2p(9.3, y), LEFT, buff=0.1)
            dots.add(VGroup(d_, lab))
        pdots = VGroup()
        for j, (k, rev, roe) in enumerate(pend):
            y = 1.5 - j
            d_ = Dot(pa.ax.c2p(roe, y), radius=0.06 + 0.10 * (rev / 1000) ** 0.5, color=BAD, fill_opacity=0.85)
            lab = tx(f"{names[k]}, asked: ${rev:,.0f}m", 12, BAD).next_to(pa.ax.c2p(9.3, y), LEFT, buff=0.1)
            pdots.add(VGroup(d_, lab))
        xl = tx("return on equity", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        head = tx("Duke Energy's electric rate cases, approved and pending", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        note = VGroup(tx("approved: 9.5% to 10.3%", 16, GOOD, bold=True), tx("asked, North Carolina, 2025:", 15, BAD),
                      tx("10.95%, $1.7bn more a year", 16, BAD, bold=True), tx("dot size: the revenue increase", 13, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.4, 1.0, 0])
        src = source("Duke Energy Corporation, Form 10-K 2025 (approved and pending electric rate cases)", size=13)
        with self.voiceover(
            "Here are real rate cases, from the annual report of Duke Energy, one of the largest American utilities. "
            "<bookmark mark='a'/> Each dot is a state commission's decision in the last three years: the extra revenue "
            "it allowed, and the return on equity it set. They cluster tightly, between about nine and a half and ten "
            "and a third per cent. <bookmark mark='b'/> And here is what Duke asked for in North Carolina in 2025: "
            "almost eleven per cent, and about 1.7 billion dollars a year more from customers. <bookmark mark='c'/> The "
            "commission will decide. Rate cases are long, public and adversarial, and the answer is usually somewhere "
            "in between. It is the price of a monopoly: steady profits, decided in a hearing room rather than a market."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.08), FadeIn(note[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in pdots], lag_ratio=0.3), FadeIn(note[1:]), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Indicate(d_[0], color=BAD) for d_ in pdots])
        self.clear_scene()
