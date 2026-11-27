from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Regulated(VoiceoverScene):
    def construct(self):
        card(self, 3, "The regulated water company", "How is a monopoly's price set, and who gets the return?",
             "Chapter three. The regulated water company.", lit=("dollar", "moat"))
        self.blocks()
        self.grow()
        self.gearing()

    def blocks(self):
        G = R["regulated"]
        f = G["first"]
        rcv_box = Rectangle(width=3.0, height=3.0, stroke_width=0, fill_color=WATER, fill_opacity=0.35).move_to([-4.6, -0.2, 0])
        rcv_l = VGroup(tx("the asset base", 20, WHITE, bold=True), tx(f"£{f['rcv'] / 1000:.0f}bn", 40, WATER, bold=True),
                       tx("pipes, works, reservoirs,", 13, GREY_A), tx("at what was paid for them", 13, GREY_A)).arrange(DOWN, buff=0.06).move_to(rcv_box)
        sc = 4.4 / f["revenue"]
        segs = [("return on the base", f["ret"], f"{100 * G['wacc']:.0f}% x £{f['rcv'] / 1000:.0f}bn", PRICE),
                ("the base, run off", f["dep"], f"{100 * G['run_off']:.0f}% of it a year", "#8B95A7"),
                ("running costs", G["opex"], "staff, power, chemicals", COST)]
        stack_ = VGroup()
        y = -2.4
        for name, v, how, col in segs:
            b = Rectangle(width=1.6, height=v * sc, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=0.85).move_to(
                [0.4, y, 0], aligned_edge=DOWN)
            lab = VGroup(tx(f"{name}: £{v:,.0f}m", 16, col, bold=True), tx(how, 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).next_to(b, RIGHT, buff=0.2)
            stack_.add(VGroup(b, lab))
            y += v * sc
        total = VGroup(tx(f"allowed revenue: £{f['revenue']:,.0f}m a year", 20, WHITE, bold=True)).next_to(stack_[-1][0], UP, buff=0.15).align_to(stack_[0][0], LEFT)
        bill = VGroup(tx(f"÷ {G['customers']:.0f} million households", 16, GREY_A), tx(f"= £{f['bill']:.0f} a year each", 30, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.3, 1.0, 0])
        arrow = Arrow(rcv_box.get_right(), [-0.5, -0.2, 0], color=GREY_B, stroke_width=3, buff=0.1)
        tag = estimate_tag("the Works' water company: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "Because nobody can compete on the street, someone has to set the price. Regulators do it in different ways; "
            "England's is the cleanest to draw. Here is the Works' water company, in round numbers. "
            "<bookmark mark='a'/> Its pipes, works and reservoirs are counted in a regulatory asset base: "
            f"£{f['rcv'] / 1000:.0f} billion. <bookmark mark='b'/> Each year the regulator lets it earn a return on that "
            f"base, here {100 * G['wacc']:.0f} per cent after inflation: £{f['ret']:,.0f} million. <bookmark mark='c'/> It "
            f"lets it recover a slice of the base itself, as if the pipes were wearing out: another £{f['dep']:,.0f} "
            f"million. <bookmark mark='d'/> And it allows the running costs it thinks an efficient company would have: "
            f"£{G['opex']:,.0f} million. <bookmark mark='e'/> Add them up and divide by the households: "
            f"£{f['bill']:.0f} a year each. That is the bill."
        ) as vo:
            head = tx("A water company's bill, built in blocks", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
            ghost = VGroup(rcv_box.copy().set_fill(opacity=0.12), *[seg[0].copy().set_fill(opacity=0.12) for seg in stack_])
            self.play(FadeIn(tag), FadeIn(head), FadeIn(ghost))
            vo.wait_until("a")
            self.play(GrowFromCenter(rcv_box), FadeIn(rcv_l))
            for m_, seg in zip("bcd", stack_):
                vo.wait_until(m_)
                if m_ == "b":
                    self.play(GrowArrow(arrow))
                self.play(GrowFromEdge(seg[0], DOWN), FadeIn(seg[1], shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(total), FadeIn(bill, shift=LEFT * 0.1))
        self.clear_scene()

    def grow(self):
        G = R["regulated"]
        path = G["path"]
        pa = viz.plot_axes([0, 25], [0, 20000], x_length=5.6, y_length=3.8, xticks=[0, 5, 10, 15, 20, 25], yticks=[5000, 10000, 15000, 20000],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"£{v / 1000:.0f}bn", ylabel="the asset base (real terms)", size=12).move_to([-3.4, -0.4, 0])
        pb = viz.plot_axes([0, 25], [0, 400], x_length=5.6, y_length=3.8, xticks=[0, 5, 10, 15, 20, 25], yticks=[100, 200, 300, 400],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"£{v:.0f}", ylabel="the bill, a year (real terms)", size=12).move_to([3.4, -0.4, 0])
        xl = VGroup(tx("years", 13, GREY_B).next_to(pa, DOWN, buff=0.08), tx("years", 13, GREY_B).next_to(pb, DOWN, buff=0.08))
        t = ValueTracker(0)

        def upto(key, ax):
            k = int(t.get_value())
            pts = [(p_["t"], p_[key]) for p_ in path[:k + 1]]
            if len(pts) < 2:
                pts = pts + pts
            return VMobject(stroke_color=WATER if key == "rcv" else PRICE, stroke_width=4).set_points_as_corners([ax.ax.c2p(x, y) for x, y in pts])
        l1 = always_redraw(lambda: upto("rcv", pa))
        l2 = always_redraw(lambda: upto("bill", pb))
        flow = VGroup(tx(f"in: £{G['capex']:,.0f}m a year of new pipes and works", 16, GOOD),
                      tx(f"out: {100 * G['run_off']:.0f}% of the base run off", 16, "#8B95A7")).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_edge(UP, buff=0.4)
        end = VGroup(tx(f"£{path[0]['rcv'] / 1000:.0f}bn to £{path[-1]['rcv'] / 1000:.0f}bn", 18, WATER, bold=True).next_to(pa.ax.c2p(25, path[-1]["rcv"]), UP, buff=0.12),
                     tx(f"£{path[0]['bill']:.0f} to £{path[-1]['bill']:.0f}", 18, PRICE, bold=True).next_to(pb.ax.c2p(25, path[-1]["bill"]), UP, buff=0.12))
        end[0].shift(LEFT * 0.9)
        end[1].shift(LEFT * 0.7)
        tag = estimate_tag("the Works' water company: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "Now let the company invest. <bookmark mark='a'/> Each year it spends "
            f"£{G['capex']:,.0f} million on new pipes and works, which are added to the base, while "
            f"{100 * G['run_off']:.0f} per cent of the base is run off. <bookmark mark='b'/> Spending more than runs off, "
            f"the base grows: from £{path[0]['rcv'] / 1000:.0f} billion to about £{path[-1]['rcv'] / 1000:.0f} billion in "
            f"twenty-five years. <bookmark mark='c'/> And because the bill is built on the base, the bill grows too, from "
            f"£{path[0]['bill']:.0f} to about £{path[-1]['bill']:.0f}, before any inflation. <bookmark mark='d'/> This is the "
            "engine of every regulated water company: it earns a return on what it has invested, so it grows by "
            "investing, and the customers pay for the growth through their bills."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(flow))
            self.add(l1, l2)
            vo.wait_until("b")
            self.play(t.animate.set_value(25), run_time=6.0, rate_func=linear)
            self.play(FadeIn(end[0]))
            vo.wait_until("c")
            self.play(FadeIn(end[1]), Indicate(end[1], color=PRICE))
        self.clear_scene()

    def gearing(self):
        G = R["regulated"]
        cheap, dear = G["lev_cheap"], G["lev_dear"]
        gs = sorted(cheap)
        pa = viz.plot_axes([0, 0.85], [-0.02, 0.13], x_length=7.6, y_length=4.4, xticks=[0, 0.2, 0.4, 0.55, 0.7, 0.8],
                           yticks=[0, 0.04, 0.08, 0.12], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="the shareholders' return a year", size=13).move_to([-2.0, -0.3, 0])
        xl = tx("share of the asset base paid for with debt (gearing)", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        base = DashedLine(pa.ax.c2p(0, 0.04), pa.ax.c2p(0.85, 0.04), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        base_l = tx("the base earns 4%", 13, GREY_B).next_to(pa.ax.c2p(0.85, 0.04), RIGHT, buff=0.1)
        lc = poly(pa, [(g, cheap[g]) for g in gs], GOOD, 4)
        ld = poly(pa, [(g, dear[g]) for g in gs], BAD, 4)
        lcl = tx("debt at 2%", 16, GOOD, bold=True).next_to(pa.ax.c2p(0.8, cheap[0.8]), RIGHT, buff=0.1)
        ldl = tx("debt at 5%", 16, BAD, bold=True).next_to(pa.ax.c2p(0.8, dear[0.8]), RIGHT, buff=0.1)
        dots = VGroup(*[Dot(pa.ax.c2p(0.55, v[0.55]), radius=0.07, color=c) for v, c in ((cheap, GOOD), (dear, BAD))])
        eng = VGroup(tx("England's water and sewerage companies", 18, WHITE, bold=True),
                     tx(f"average gearing, 1991: {G['gear91']:.0f}%", 17, UK),
                     tx(f"average gearing, 2009: {G['gear09']:.0f}%", 17, UK),
                     tx("regulator's assumption for 2025-30: 55%", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 1.9, 0])
        tag = estimate_tag("the Works' water company: an illustration", corner=DR, size=12)
        src = source("Independent Water Commission, Final Report (July 2025): gearing of the water and sewerage companies", size=13)
        with self.voiceover(
            "Who gets that return depends on how the base was paid for. <bookmark mark='a'/> Suppose the base earns "
            "four per cent a year. If the shareholders paid for all of it, they earn four per cent. <bookmark mark='b'/> "
            "Now borrow part of it at two per cent. The lenders get their two, and the shareholders keep the rest of "
            f"the four on a smaller stake: at 55 per cent debt they earn about {100 * cheap[0.55]:.1f} per cent, at 80 "
            f"per cent about {100 * cheap[0.8]:.0f}. <bookmark mark='c'/> But if debt costs five per cent, the same "
            f"borrowing works in reverse: at 80 per cent debt, the shareholders earn about nothing. <bookmark mark='d'/> "
            "When England's water companies were privatized, they had little debt. Between 1991 and 2009, their "
            f"average gearing went from {G['gear91']:.0f} per cent to {G['gear09']:.0f} per cent. While debt is cheap, "
            "borrowing turns a steady return into a much larger one for the owners. When it becomes dear, the same "
            "borrowing eats the owners' return, and then the company's ability to pay."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(base), FadeIn(base_l))
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(lcl), run_time=2.0)
            self.play(FadeIn(dots[0]))
            vo.wait_until("c")
            self.play(Create(ld), FadeIn(ldl), FadeIn(dots[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(eng, shift=LEFT * 0.1))
        self.clear_scene()
