from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Hazard(VoiceoverScene):
    def construct(self):
        card(self, 9, "Waste the law creates", "What is a market made by regulation worth?",
             "Chapter nine. Waste the law creates.", lit=("moat", "change"))
        self.law()
        self.growth()
        self.pfas()

    def law(self):
        inc = int(get("clh.incinerators"))
        lfs = int(get("clh.landfills"))
        kilns = VGroup(*[draw.rotary_kiln(1.3) for _ in range(inc)]).arrange_in_grid(rows=2, buff=(0.25, 0.4))
        kilns.scale_to_fit_width(6.6).move_to([-3.0, 0.9, 0])
        kl = tx(f"{inc} commercial hazardous waste incinerators", 17, BURN, bold=True).next_to(kilns, UP, buff=0.25)
        pits = VGroup(*[draw.landfill_section(1.1, 0.5, fill=0.8) for _ in range(lfs)]).arrange(RIGHT, buff=0.15)
        pits.scale_to_fit_width(6.6).move_to([-3.0, -1.7, 0])
        for p_ in pits:
            p_.cap.set_opacity(0)
        pl = tx(f"{lfs} commercial landfills, {lfs - 1} of them for hazardous waste", 17, LANDFILL, bold=True).next_to(pits, UP, buff=0.2)
        side = VGroup(tx("Clean Harbors, 2025", 22, WHITE, bold=True),
                      tx(f"over {get('clh.facilities'):.0f} disposal facilities", 16, GREY_A),
                      tx(f"{get('clh.airspace'):.0f} million cubic yards left", 16, GREY_A),
                      tx("in its hazardous waste landfills", 16, GREY_A),
                      tx("permits it calls 'hard-to-come-by'", 16, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.4, 0.2, 0])
        src = source("Clean Harbors, Form 10-K 2025 (facilities; RCRA Part B permits, corrective action and financial assurance)", size=13)
        with self.voiceover(
            "Some waste markets exist only because the law forbids the cheap alternative. Under America's main waste "
            "law, anyone who treats, stores or disposes of hazardous waste needs a special permit, and each one comes "
            "with clean-up duties and proof that the owner can pay for them. <bookmark mark='a'/> So the "
            "places that can legally burn a drum of solvent or bury contaminated soil are few. Clean Harbors, the largest "
            f"such network in North America by its own account, runs {inc} commercial hazardous waste incinerators. "
            f"<bookmark mark='b'/> And {lfs} commercial landfills, {lfs - 1} of them licensed for hazardous waste, with "
            f"about {get('clh.airspace'):.0f} million cubic yards of room left. <bookmark mark='c'/> It describes its "
            "permits as hard to come by. A permit that is hard to get is a moat that is hard to cross."
        ) as vo:
            ghost = VGroup(kilns.copy().set_opacity(0.15), pits.copy().set_opacity(0.15))
            self.play(FadeIn(src), FadeIn(ghost))
            vo.wait_until("a")
            self.play(FadeIn(kl), LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kilns], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in pits], lag_ratio=0.1), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()

    def growth(self):
        H = R["hazard"]
        C = H["clh"]
        ys = sorted(C)
        pa = viz.plot_axes([ys[0] - 0.7, ys[-1] + 0.7], [0, 7], x_length=8.6, y_length=4.4, xticks=[2009, 2013, 2017, 2021, 2025],
                           yticks=[2, 4, 6], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn", ylabel="Clean Harbors, revenue a year",
                           size=13).move_to([-1.4, -0.4, 0])
        bars = VGroup()
        for y in ys:
            rev, oi = C[y]
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            y1 = pa.ax.c2p(y, rev)[1]
            bars.add(Rectangle(width=0.36, height=y1 - y0, stroke_width=0, fill_color=HAZ, fill_opacity=0.85).move_to([x0, y0, 0], aligned_edge=DOWN))
        l1 = tx(f"${C[ys[0]][0]:.1f}bn", 16, WHITE, bold=True).next_to(bars[0], UP, buff=0.08)
        l2 = tx(f"${C[ys[-1]][0]:.1f}bn", 16, WHITE, bold=True).next_to(bars[-1], UP, buff=0.08)
        med = VGroup(tx("medical waste", 18, WHITE, bold=True),
                     tx(f"Waste Management's healthcare arm:", 15, GREY_A),
                     tx(f"${H['wm_health']:.1f}bn of revenue in 2025,", 15, GREY_A),
                     tx("bought with Stericycle in November 2024", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([5.0, 0.2, 0])
        src = source("SEC EDGAR: Clean Harbors, Forms 10-K 2009-2025 (revenue); Waste Management, Form 10-K 2025", size=13)
        with self.voiceover(
            "And it has grown. <bookmark mark='a'/> Clean Harbors' revenue was about "
            f"${C[ys[0]][0]:.1f} billion in {ys[0]}. <bookmark mark='b'/> By {ys[-1]}, about ${C[ys[-1]][0]:.0f} billion. <bookmark mark='c'/> Medical waste works the same way: "
            "rules about how a hospital must get rid of needles and tissue create a business. Waste Management bought "
            f"Stericycle, a medical waste company, in 2024; in 2025 that arm brought in about "
            f"${H['wm_health']:.1f} billion. In waste, the regulator does not just police the market. It draws it."
        ) as vo:
            ghost = VGroup(*[b.copy().set_fill(opacity=0.15) for b in bars])
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(l1))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:]], lag_ratio=0.08), run_time=3.0)
            self.play(FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(med, shift=LEFT * 0.1))
        self.clear_scene()

    def pfas(self):
        mcl = get("epa.pfas.mcl")
        years = 1e12 / (365.25 * 24 * 3600)
        glass = VGroup(Polygon([-0.7, 1.0, 0], [0.7, 1.0, 0], [0.55, -1.0, 0], [-0.55, -1.0, 0], stroke_color="#C9D3E0", stroke_width=3,
                               fill_color=WATER, fill_opacity=0.25)).move_to([-4.6, 0.4, 0])
        dots = VGroup(*[Dot(radius=0.035, color=BAD).move_to(glass.get_center() + np.array([0.3 * np.cos(k), 0.4 * np.sin(2 * k), 0])) for k in range(4)])
        rule = VGroup(tx("America's PFAS rule, April 2024", 20, WHITE, bold=True),
                      tx(f"PFOA and PFOS: no more than {mcl:.0f} parts per trillion", 17, BAD, bold=True),
                      tx(f"{mcl:.0f} seconds in about {years / 1000:.0f} thousand years", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.3, -2.0, 0])
        lo, hi = span("mmm.pfas")
        cols = VGroup(VGroup(tx("who caused it pays", 15, GREY_A), tx(f"3M: ${lo:.1f}-{hi:.1f}bn", 22, PRICE, bold=True),
                             tx("to US public water suppliers (2023)", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05),
                      VGroup(tx("who removes it", 15, GREY_A), tx(f"American Water: ${get('awk.quality5'):.1f}bn", 22, WATER, bold=True),
                             tx(f"over five years on water quality, ${1000 * get('awk.quality26'):.0f}m in 2026", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05),
                      VGroup(tx("and when", 15, GREY_A), tx(f"by April {get('awk.pfas_deadline'):.0f}", 22, WHITE, bold=True),
                             tx("the EPA has said it intends to allow until 2031", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.0, 0.3, 0])
        src = source("US EPA, PFAS National Primary Drinking Water Regulation (89 FR 32532, 2024); 3M, Form 8-K (22 June 2023); "
                     "American Water Works, Form 10-K 2025", size=13)
        with self.voiceover(
            "The law makes costs for water companies too, and this is the newest. <bookmark mark='a'/> In April 2024 "
            "America set its first national limits on 'forever chemicals' in drinking water: for the two best known, "
            f"PFOA and PFOS, {mcl:.0f} parts per trillion. Four parts per trillion is about four seconds in "
            f"{years / 1000:.0f} thousand years. <bookmark mark='b'/> The chemical makers have been paying: 3M agreed to "
            f"pay America's public water suppliers {lo:.1f} to {hi:.1f} billion dollars. <bookmark mark='c'/> The water "
            f"companies must build the treatment. American Water plans about ${get('awk.quality5'):.1f} billion over five "
            "years on water quality, most of it to comply with environmental rules. <bookmark mark='d'/> Under the rule as "
            f"written, the deadline is April {get('awk.pfas_deadline'):.0f}; the EPA has said it intends to extend it to "
            "2031. Either way, the cost goes into the asset base, and from there into the bill."
        ) as vo:
            self.play(FadeIn(src), FadeIn(glass), FadeIn(cols.copy().set_opacity(0.12)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.3), FadeIn(rule), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cols[0], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cols[1], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cols[2], shift=LEFT * 0.1))
        self.clear_scene()
