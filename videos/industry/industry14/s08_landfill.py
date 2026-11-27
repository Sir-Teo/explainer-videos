from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Landfill(VoiceoverScene):
    def construct(self):
        card(self, 7, "The hole in the ground", "Why is a landfill permit worth more than the land?",
             "Chapter seven. The hole in the ground.", lit=("make", "moat"))
        self.rule()
        self.fewer()
        self.airspace()
        self.integrate()

    def rule(self):
        L = R["landfill"]
        lf = draw.landfill_section(7.0, 3.2, fill=1.0).move_to([-2.0, -1.0, 0])
        for c in lf.cells:
            c.set_opacity(0)
        lf.cap.set_opacity(0)
        lf.wells.set_opacity(0)
        lf.pipes.set_opacity(0)
        lf.drain.set_opacity(0)
        anchors = [lf.clay.point_from_proportion(0.9), lf.liner.point_from_proportion(0.75), lf.drain.get_right() + LEFT * 0.3,
                   lf.cells[2].get_center() + RIGHT * 1.2, lf.wells[2].get_top(), lf.cap.point_from_proportion(0.6)]
        notes = [(f"compacted clay, at least {L['clay']:.0f} feet", LANDFILL, -2.75),
                 (f"a plastic membrane: {L['liner']:.0f} thousandths\nof an inch, if polyethylene", "#C9D3E0", -1.75),
                 (f"leachate pipes: no more than\n{L['leachate']:.0f} cm may pool on the liner", BURN, -0.8),
                 ("the waste, in cells,\ncovered with soil each day", WASTE, 0.2),
                 ("wells that draw off the gas", PRICE, 1.25),
                 (f"a final cap; then {L['postclosure']:.0f} years\nof care after it closes", GOOD, 2.2)]
        labs, leads = VGroup(), VGroup()
        for (text, col, y), pt in zip(notes, anchors):
            lab = tx(text, 15, col, bold=True).move_to([3.1, y, 0], aligned_edge=LEFT)
            labs.add(lab)
            leads.add(Line(lab.get_left() + LEFT * 0.08, pt, stroke_color=col, stroke_width=1.5, stroke_opacity=0.8))
        head = tx("A landfill under America's 1991 rules", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("40 CFR Part 258, criteria for municipal solid waste landfills (56 FR 51016, 9 October 1991)", size=13)
        with self.voiceover(
            "Every truck ends at a hole in the ground, and the hole is the most valuable thing in the business. A "
            "modern landfill is not a dump. Since 1991, the standard design for a new American landfill looks like this. "
            f"<bookmark mark='a'/> At the bottom, at least {L['clay']:.0f} feet of compacted clay. <bookmark mark='b'/> On "
            f"top of it, a plastic membrane, {L['liner']:.0f} thousandths of an inch thick if it is polyethylene. "
            "<bookmark mark='c'/> Above that, pipes to collect the leachate, the liquid that drains through rubbish, so "
            f"that no more than {L['leachate']:.0f} centimetres of it ever pools on the liner. <bookmark mark='d'/> Then "
            "the rubbish itself, compacted in cells and covered with soil at the end of every day. <bookmark mark='e'/> "
            "Wells to draw off the gas it gives off as it rots. <bookmark mark='f'/> And when it is full, a cap, and "
            f"{L['postclosure']:.0f} years of monitoring and repairs afterwards, paid for by the owner."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(lf.soil), FadeIn(lf.pit), FadeIn(lf.ground))
            vo.wait_until("a")
            self.play(Create(lf.clay), FadeIn(labs[0]), Create(leads[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lf.liner), FadeIn(labs[1]), Create(leads[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(lf.drain.animate.set_opacity(0.9), lf.pipes.animate.set_opacity(1), FadeIn(labs[2]), Create(leads[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[c.animate.set_opacity(1) for c in lf.cells], lag_ratio=0.35), FadeIn(labs[3]), Create(leads[3]), run_time=3.5)
            vo.wait_until("e")
            self.play(lf.wells.animate.set_opacity(1), FadeIn(labs[4]), Create(leads[4]))
            vo.wait_until("f")
            self.play(lf.cap.animate.set_opacity(1), FadeIn(labs[5]), Create(leads[5]))
        self.clear_scene()

    def fewer(self):
        L = R["landfill"]
        n88, n09 = L["count"]
        per = 50
        dots88 = VGroup(*[Dot(radius=0.06, color=LANDFILL) for _ in range(int(round(n88 / per)))]).arrange_in_grid(cols=16, buff=0.07)
        dots88.move_to([-4.6, 0.3, 0])
        dots09 = VGroup(*[Dot(radius=0.06, color=PRICE) for _ in range(int(round(n09 / per)))]).arrange_in_grid(cols=16, buff=0.07)
        dots09.move_to([-4.6, 0.3, 0]).align_to(dots88, UP)
        l88 = tx(f"{n88:,.0f} landfills in 1988", 18, LANDFILL, bold=True).next_to(dots88, UP, buff=0.15)
        l09 = tx(f"{n09:,.0f} in 2009", 18, PRICE, bold=True).next_to(dots88, DOWN, buff=0.15)
        key = tx(f"each dot: {per} landfills", 13, GREY_B).next_to(l09, DOWN, buff=0.08)
        tons = L["tons"]
        pa = viz.plot_axes([1960, 2018], [0, 160], x_length=5.6, y_length=3.6, xticks=[1960, 1980, 2000, 2018], yticks=[50, 100, 150],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}m", ylabel="tons landfilled a year (US, municipal waste)", size=12).move_to([3.0, 0.2, 0])
        ln = poly(pa, sorted(tons.items()), WASTE, 4)
        sz = VGroup(tx(f"the average landfill took about {L['per_landfill'][0]:.0f} thousand tons a year in 1988,", 15, WHITE),
                    tx(f"and about {L['per_landfill'][1]:.0f} thousand in 2009", 15, WHITE)).arrange(DOWN, buff=0.04).to_edge(DOWN, buff=0.75)
        src = source("US EPA, MSW in the United States: 2009 Facts and Figures; EPA, Facts and Figures history 1960-2018", size=13)
        with self.voiceover(
            "Rules like that are expensive to meet, and small dumps could not meet them. "
            f"<bookmark mark='a'/> In 1988 America had {n88:,.0f} municipal landfills. <bookmark mark='b'/> By 2009 it "
            f"had {n09:,.0f}. <bookmark mark='c'/> Yet the tonnage going into them hardly changed: about "
            f"{tons[1990]:.0f} million tons in 1990, about {tons[2018]:.0f} million in 2018, the last year the EPA "
            "counted. <bookmark mark='d'/> Small town dumps closed; big, engineered regional landfills took their place. "
            f"The average landfill went from about {L['per_landfill'][0]:.0f} thousand tons a year to about "
            f"{L['per_landfill'][1]:.0f} thousand: four times the size."
        ) as vo:
            ghost = VGroup(dots88.copy().set_opacity(0.3), tx("Fewer, bigger landfills", 22, WHITE, bold=True).to_edge(UP, buff=0.35))
            self.play(FadeIn(src), FadeIn(ghost), FadeIn(pa))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots88], lag_ratio=0.005), FadeIn(l88), run_time=2.0)
            self.remove(ghost)
            vo.wait_until("b")
            keep = dots88[:len(dots09)]
            gone = dots88[len(dots09):]
            self.play(FadeOut(gone, lag_ratio=0.01), keep.animate.set_color(PRICE), FadeIn(l09), FadeIn(key), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(sz, shift=UP * 0.1))
        self.clear_scene()

    def airspace(self):
        L = R["landfill"]
        W = L["wm_life"]
        buckets = [("0-5", W["0_5"]), ("6-10", W["6_10"]), ("11-20", W["11_20"]), ("21-40", W["21_40"]), ("41+", W["41"])]
        sc = 3.0 / 100
        bars = VGroup()
        for i, (k, v) in enumerate(buckets):
            b = Rectangle(width=0.7, height=v * sc, stroke_width=0, fill_color=LANDFILL if i < 2 else "#B08A5A", fill_opacity=0.95).move_to(
                [-5.8 + 0.95 * i, -1.9, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{v:.0f}", 16, WHITE, bold=True).next_to(b, UP, buff=0.06), tx(k, 13, GREY_A).next_to(b, DOWN, buff=0.08)))
        bh = VGroup(tx(f"Waste Management's {L['wm_landfills']:.0f} landfills", 17, WHITE, bold=True),
                    tx("by years of room left", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(bars, UP, buff=0.35)
        avg = tx(f"weighted average: about {L['wm_avg']:.0f} years", 15, PRICE, bold=True).next_to(bars, DOWN, buff=0.45)
        Rg = L["rsg"]
        sc2 = 3.0 / 500
        floor_ = 4500
        x0 = 0.8
        steps = [("end of 2024", Rg["start"], None, "#9AA3B2"), ("bought", Rg["acq"], +1, GOOD), ("permits won", Rg["permits"], +1, GOOD),
                 ("used up", Rg["used"], -1, BAD), ("end of 2025", Rg["end"], None, "#9AA3B2")]
        level = 0.0
        wf = VGroup()
        base_y = -1.9
        for i, (nm, v, sign, col) in enumerate(steps):
            x = x0 + 1.25 * i
            if sign is None:
                b = Rectangle(width=0.8, height=(v - floor_) * sc2, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x, base_y, 0], aligned_edge=DOWN)
                level = v
                lab = f"{v:,.0f}"
            else:
                lo = level if sign > 0 else level - v
                hi = level + v if sign > 0 else level
                b = Rectangle(width=0.8, height=max((hi - lo) * sc2, 0.04), stroke_width=0, fill_color=col, fill_opacity=0.95).move_to(
                    [x, base_y + (lo - floor_) * sc2, 0], aligned_edge=DOWN)
                level = hi if sign > 0 else lo
                lab = f"{'+' if sign > 0 else '-'}{v:,.0f}"
            wf.add(VGroup(b, tx(lab, 15, WHITE, bold=True).next_to(b, UP, buff=0.06), tx(nm, 12, GREY_A).next_to([x, base_y, 0], DOWN, buff=0.1)))
        wh = VGroup(tx("Republic's permitted airspace, 2025", 17, WHITE, bold=True), tx("million cubic yards; bars start at 4,500", 14, GREY_A)).arrange(
            DOWN, buff=0.04).move_to([x0 + 2.5, 2.4, 0])
        yrs = tx(f"with probable expansions, {Rg['total']:,.0f}m at both ends: about {Rg['years_left']:.0f} years at 2025's pace", 15, PRICE, bold=True).to_edge(DOWN, buff=0.7).shift(RIGHT * 2.6)
        src = source("Waste Management, Form 10-K 2025 (landfills by remaining life); Republic Services, Form 10-K 2025 (available airspace)", size=13)
        with self.voiceover(
            "For the owners, a landfill's room is an inventory, counted in years. <bookmark mark='a'/> Waste "
            f"Management has {L['wm_landfills']:.0f} landfills. A few dozen have less than ten years of room left; most "
            f"have more than twenty. Weighted by size, about {L['wm_avg']:.0f} years. <bookmark mark='b'/> Republic "
            f"Services counts its airspace in cubic yards. It began 2025 with {Rg['start']:,.0f} million of permitted "
            f"space. <bookmark mark='c'/> It bought landfills with another {Rg['acq']:.0f} million and won permits for "
            f"{Rg['permits']:.0f} million more. <bookmark mark='d'/> It filled {Rg['used']:.0f} million. "
            f"<bookmark mark='e'/> It ended the year with more room than it started with. Counting the expansions it "
            f"expects, it has about {Rg['years_left']:.0f} years at the rate it fills today. The inventory is not running "
            "out; it is being replaced, one hard-won permit at a time."
        ) as vo:
            ghost = VGroup(*[b_[0].copy().set_fill(opacity=0.15) for b_ in bars], *[b_[0].copy().set_fill(opacity=0.15) for b_ in wf])
            self.play(FadeIn(src), FadeIn(ghost))
            vo.wait_until("a")
            self.play(FadeIn(bh), LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(avg))
            vo.wait_until("b")
            self.play(FadeIn(wh), GrowFromEdge(wf[0][0], DOWN), FadeIn(wf[0][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(wf[1][0], DOWN), FadeIn(wf[1][1:]))
            self.play(GrowFromEdge(wf[2][0], DOWN), FadeIn(wf[2][1:]))
            vo.wait_until("d")
            self.play(GrowFromEdge(wf[3][0], UP), FadeIn(wf[3][1:]))
            vo.wait_until("e")
            self.play(GrowFromEdge(wf[4][0], DOWN), FadeIn(wf[4][1:]))
            self.play(FadeIn(yrs, shift=UP * 0.1))
        self.clear_scene()

    def integrate(self):
        L = R["landfill"]
        W = R["collection"]["wm"]
        Rg = L["rsg"]
        lorry = draw.bin_lorry(1.4).move_to([-5.6, 0.6, 0])
        transfer = VGroup(Rectangle(width=1.6, height=0.9, stroke_width=0, fill_color="#5D6B82", fill_opacity=1),
                          Polygon([-0.9, 0.45, 0], [0.9, 0.45, 0], [0, 0.85, 0], stroke_width=0, fill_color="#4A5568", fill_opacity=1)).move_to([-1.6, 0.85, 0])
        transfer_l = tx("transfer station", 14, GREY_A).next_to(transfer, DOWN, buff=0.1)
        trailer = draw.truck(1.5, "#9AA3B2").move_to([-1.6, -0.55, 0])
        lf = draw.landfill_section(3.4, 1.4, fill=0.9).move_to([3.6, 0.3, 0])
        lf.cap.set_opacity(0)
        lf_l = tx("its own landfill", 14, GREY_A).next_to(lf, DOWN, buff=0.1)
        arrow1 = Arrow([-4.7, 0.7, 0], [-2.5, 0.8, 0], color=GREY_B, stroke_width=3, buff=0.05)
        arrow2 = Arrow([-0.6, 0.6, 0], [1.8, 0.6, 0], color=GREY_B, stroke_width=3, buff=0.05)
        stat = VGroup(tx(f"Republic: about {Rg['internal']:.0f}% of what its trucks collect goes to its own landfills", 17, WHITE, bold=True),
                      tx(f"Waste Management: ${W['landfill_gross']:.1f}bn of landfill revenue, ${W['landfill_gross'] - W['landfill']:.1f}bn of it from its own trucks", 17, WHITE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -2.1, 0])
        tip = L["tip"]
        tipbox = VGroup(tx("average US tipping fee, in 2013 dollars a ton", 14, GREY_A),
                        tx(f"1985: ${tip[1985]:.2f}   1995: ${tip[1995]:.2f}   2013: ${tip[2013]:.2f}", 17, PRICE, bold=True)).arrange(
            DOWN, buff=0.06).to_edge(UP, buff=0.4)
        src = source("Republic Services and Waste Management, Forms 10-K 2025; US EPA, Historic Tipping Fees and Commodity Values (2015)", size=13)
        with self.voiceover(
            "So the big haulers own the whole chain. <bookmark mark='a'/> The truck collects; <bookmark mark='b'/> a "
            "transfer station packs the rubbish into big trailers for the long haul; <bookmark mark='c'/> and the trailer "
            "unloads at a landfill the same company owns. <bookmark mark='d'/> About two-thirds of what Republic's trucks "
            f"collect goes into Republic's own landfills. Waste Management's landfills took in ${W['landfill_gross']:.1f} "
            f"billion in 2025, and ${W['landfill_gross'] - W['landfill']:.1f} billion of that came from its own trucks. "
            "<bookmark mark='e'/> And the price of tipping rose: the national average fee went from about "
            f"${tip[1985]:.0f} a ton in 1985 to about ${tip[1995]:.0f} in 1995, in 2013 dollars, and then stayed there. Owning the hole means a rival hauler, however efficient its trucks, still pays you "
            "to tip."
        ) as vo:
            ghost = VGroup(transfer.copy().set_opacity(0.15), lf.copy().set_opacity(0.15))
            self.play(FadeIn(src), FadeIn(ghost), FadeIn(lorry, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Indicate(lorry, scale_factor=1.1))
            vo.wait_until("b")
            self.play(GrowArrow(arrow1), FadeIn(transfer), FadeIn(transfer_l), FadeIn(trailer))
            vo.wait_until("c")
            self.play(GrowArrow(arrow2), FadeIn(lf), FadeIn(lf_l))
            self.play(trailer.animate.move_to([0.9, -0.55, 0]), run_time=1.5)
            self.play(FadeOut(trailer, shift=RIGHT * 0.4), lf.cells[-1].animate.set_opacity(1), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(stat, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(tipbox, shift=DOWN * 0.1))
        self.clear_scene()
