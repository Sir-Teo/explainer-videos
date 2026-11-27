from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "Will America keep using more electricity?", "Chapter thirteen. Called it?", lit=("change",))
        self.theirs()
        self.ours()

    def theirs(self):
        C = R["called"]
        H = R["history"]
        eu = H["end_use"]
        ys = [y for y in sorted(eu) if y >= 1995]
        pa = viz.plot_axes([1994.5, 2026.5], [0, 6000], x_length=9.2, y_length=4.6, xticks=[1995, 2003, 2010, 2015, 2020, 2025],
                           yticks=[1500, 3000, 4500, 6000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="US electricity use, billion kWh", size=14).move_to([-1.6, -0.4, 0])
        actual = poly(pa, [(y, eu[y]) for y in ys], WHITE, 3.5)
        proj = DashedLine(pa.ax.c2p(2003, C["base"]), pa.ax.c2p(2025, C["proj"]), stroke_color=PRICE, stroke_width=3.5, dash_length=0.1)
        d1 = Dot(pa.ax.c2p(2025, C["proj"]), radius=0.08, color=PRICE)
        d2 = Dot(pa.ax.c2p(2025, C["actual"]), radius=0.08, color=WHITE)
        l1 = tx(f"projected for 2025: {C['proj']:,.0f}", 15, PRICE, bold=True).next_to(d1, LEFT, buff=0.15)
        l2 = tx(f"actual: {C['actual']:,.0f}", 15, WHITE, bold=True).next_to(d2, DOWN + LEFT, buff=0.1)
        quote = VGroup(tx("'Rapid growth in electricity use for", 15, WHITE), tx("computers, office equipment, and a variety", 15, WHITE),
                       tx("of electrical appliances'", 15, WHITE), tx("EIA, Annual Energy Outlook 2005", 13, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, 1.8, 0])
        verdict = VGroup(tx(f"projected: {C['growth_proj']:.1f}% a year", 17, PRICE, bold=True),
                         tx(f"actual: {C['growth_actual']:.1f}% a year", 17, WHITE, bold=True),
                         tx(f"the projection: {100 * (C['proj'] / C['actual'] - 1):.0f}% too high", 17, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, -1.2, 0])
        src = source("EIA, Annual Energy Outlook 2005; Monthly Energy Review, Table 7.6 (electricity end use)", size=13)
        with self.voiceover(
            "Part thirteen's forecast to test is the government's own, again: the Energy Information Administration's "
            "outlook of February 2005. <bookmark mark='a'/> It expected America's electricity use to grow from about "
            f"{C['base']:,.0f} billion kilowatt-hours in 2003 to {C['proj']:,.0f} billion in 2025, {C['growth_proj']:.1f} "
            "per cent a year, led, it said, by rapid growth in electricity use for computers and office equipment. "
            f"<bookmark mark='b'/> What happened: about {C['actual']:,.0f} billion in 2025, growth of {C['growth_actual']:.1f} "
            f"per cent a year. <bookmark mark='c'/> Called it? No: the projection was about {100 * (C['proj'] / C['actual'] - 1):.0f} "
            "per cent too high. The growth it expected never came, and for fifteen years the line was flat. And the irony: "
            "twenty years later, the computers it named are back, in data centres."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(proj), FadeIn(d1), FadeIn(l1), FadeIn(quote), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(actual), run_time=2.5)
            self.play(FadeIn(d2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        D = R["demand"]
        g = D["growth"]
        rows = VGroup(*[tx(f"{y}: {g[y]:+.1f}%", 18, GOOD if g[y] >= 0 else BAD, bold=True) for y in (2022, 2023, 2024, 2025)],
                      tx(f"{D['ytd_year']}, January-August: {D['ytd']:+.1f}%", 18, GOOD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.move_to([-4.2, 0.6, 0])
        rl = tx("US electricity sales, change on the year before", 14, GREY_B).next_to(rows, UP, buff=0.25)
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("America's retail sales of electricity", 17, WHITE),
                       tx("in 2027 will be more than 1.5% above 2026's.", 17, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked against the EIA's figures in early 2028", 14, GREY_A)).arrange(DOWN, buff=0.12).move_to([3.0, 1.0, 0])
        why = VGroup(tx("For: 2024, 2025 and 2026 so far grew about 2%; data centres", 14, GOOD),
                     tx("projected at 325-580 TWh by 2028; utilities building", 14, GOOD),
                     tx("Against: a mild year, a slowdown, efficiency,", 14, BAD),
                     tx("and delays in connecting the new load", 14, BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.0, -1.8, 0])
        src = source("EIA, Monthly Energy Review, Table 7.6; DOE on LBNL's data center report (2024)", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> American electricity sales grew "
            f"{g[2024]:.1f} per cent in 2024, {g[2025]:.1f} per cent in 2025, and about {D['ytd']:.0f} per cent in the "
            "first eight months of 2026. <bookmark mark='b'/> We think 2027 will be more of the same: sales more than one "
            "and a half per cent above 2026. Data centres are being built, and utilities are spending to serve them. "
            "Against us: a mild summer, a slowdown, and delays in connecting the new load to the grid. "
            f"<bookmark mark='c'/> We give it {100 * C['prob']:.0f} per cent, and we will check it against the government's "
            "figures in early 2028, right or wrong."
        ) as vo:
            self.play(FadeIn(src), FadeIn(rl), FadeIn(card_[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(card_[1:3]), FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(card_[3:], scale=1.1))
        self.clear_scene()
