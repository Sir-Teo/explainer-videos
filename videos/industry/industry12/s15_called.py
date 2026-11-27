from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "Will Germany's chemical industry come back?", "Chapter thirteen. Called it?",
             lit=("change",))
        self.theirs()
        self.ours()

    def panel(self, x, title, unit, proj, actual, plab, alab, lo, hi, fmt):
        h = 3.2
        base_y = -1.0
        sc = h / (hi - lo)
        zero_y = base_y + (0 - lo) * sc - h / 2
        axis = Line([x - 1.4, zero_y, 0], [x + 1.4, zero_y, 0], stroke_color=GREY_B, stroke_width=1.2)
        bars = VGroup()
        for j, (v, col, lab) in enumerate(((proj, PRICE, plab), (actual, GOOD if j_ok(proj, actual) else BAD, alab))):
            r_ = Rectangle(width=0.9, height=max(abs(v) * sc, 0.03), stroke_color=col, stroke_width=2, fill_color=col,
                           fill_opacity=0.35 if j == 0 else 0.9)
            r_.move_to([x - 0.6 + 1.2 * j, zero_y, 0], aligned_edge=DOWN if v >= 0 else UP)
            val = tx(fmt(v), 17, col, bold=True).next_to(r_, UP if v >= 0 else DOWN, buff=0.08)
            nm = VGroup(*[tx(s_, 12, GREY_A) for s_ in lab.split("\n")]).arrange(DOWN, buff=0.02)
            nm.next_to(val, UP if v >= 0 else DOWN, buff=0.06)
            bars.add(VGroup(r_, val, nm))
        head = VGroup(tx(title, 17, WHITE, bold=True), tx(unit, 12, GREY_B)).arrange(DOWN, buff=0.04).move_to([x, 2.6, 0])
        return VGroup(head, axis, bars)

    def theirs(self):
        C = R["called"]
        p1 = self.panel(-4.6, "Liquefied natural gas, 2025", "trillion cubic feet", C["lng_proj"], -C["lng_exports_2025"],
                        "projected:\nnet imports", "actual:\nexports", -7, 7.5, lambda v: f"{abs(v):.1f}")
        p2 = self.panel(0.0, "Nitrogen fertilizer, 2003-2025", "growth a year", C["ag_proj"], C["n_actual"],
                        "projected:\nfarm chemicals", "actual:\nammonia (USGS)", -0.5, 3.0, lambda v: f"{v:+.1f}%")
        p3 = self.panel(4.6, "Bulk chemicals, 2003-2025", "growth a year", C["chem_proj"], C["basic_actual"],
                        "projected:\nbulk chemicals", "actual: basic\nchemicals (Fed)", -0.5, 3.0, lambda v: f"{v:+.1f}%")
        verdict = VGroup(tx("Wrong about the gas, and so wrong about fertilizer;", 19, BAD, bold=True),
                         tx("right that bulk chemicals would grow slowly.", 19, GOOD, bold=True)).arrange(DOWN, buff=0.06).to_edge(
            DOWN, buff=0.6)
        head = tx("The government's outlook of February 2005, against what happened", 20, WHITE, bold=True).to_edge(UP, buff=0.25)
        src = source("EIA, Annual Energy Outlook 2005; EIA LNG exports; USGS (ammonia); Federal Reserve G.17 via FRED", size=12)
        with self.voiceover(
            "Part twelve's forecast to test is the American government's own. <bookmark mark='a'/> In February 2005, "
            "the Energy Information Administration published its outlook to 2025. Gas was dear and getting dearer, so "
            f"it expected America to import more and more of it as liquefied natural gas: {C['lng_proj']:.1f} trillion "
            f"cubic feet a year by 2025, up from {C['lng_2003']:.1f}. <bookmark mark='b'/> In 2025 America did the "
            f"opposite. It exported {C['lng_exports_2025']:.1f} trillion cubic feet. <bookmark mark='c'/> Expecting dear "
            "gas, it cut its forecast for farm chemicals, nitrogen fertilizer among them, to growth of "
            f"{C['ag_proj']:.1f} per cent a year, because of foreign competition. American ammonia grew "
            f"{C['n_actual']:.1f} per cent a year instead. <bookmark mark='d'/> For bulk chemicals it expected "
            f"{C['chem_proj']:.0f} per cent a year. The Federal Reserve's index of basic chemicals grew about "
            f"{C['basic_actual']:.1f} per cent, and plastics and resins about {C['resin_actual']:.0f}. "
            "<bookmark mark='e'/> Called it? On chemicals, roughly, and even a little high. On gas, the input that "
            "decides everything else, completely wrong: the outlook had not priced in shale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(p_[0]) for p_ in (p1, p2, p3)], *[Create(p_[1]) for p_ in (p1, p2, p3)])
            vo.wait_until("a")
            self.play(GrowFromEdge(p1[2][0][0], DOWN), FadeIn(p1[2][0][1:]), run_time=1.0)
            vo.wait_until("b")
            self.play(GrowFromEdge(p1[2][1][0], UP), FadeIn(p1[2][1][1:]), run_time=1.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(p2[2][0][0], DOWN), FadeIn(p2[2][0][1:]), run_time=0.8)
            self.play(GrowFromEdge(p2[2][1][0], DOWN), FadeIn(p2[2][1][1:]), run_time=0.8)
            vo.wait_until("d")
            self.play(GrowFromEdge(p3[2][0][0], DOWN), FadeIn(p3[2][0][1:]), run_time=0.8)
            self.play(GrowFromEdge(p3[2][1][0], DOWN), FadeIn(p3[2][1][1:]), run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        E = R["europe"]
        de = E["de"]
        ms = sorted(m for m in de if m >= "2019-01")
        pa = viz.plot_axes([2019, 2028.05], [60, 110], x_length=7.6, y_length=4.0, xticks=[2019, 2021, 2023, 2025, 2027],
                           yticks=[70, 80, 90, 100, 110], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}",
                           ylabel="Germany's chemical output, 2021 = 100", size=13).move_to([-2.8, -0.6, 0])
        line = VMobject(stroke_color=EUROPE, stroke_width=3).set_points_as_corners([pa.ax.c2p(mx(m), de[m]) for m in ms])
        thr = DashedLine(pa.ax.c2p(2019, C["threshold"]), pa.ax.c2p(2028.05, C["threshold"]), stroke_color=PRICE, stroke_width=2,
                         dash_length=0.08)
        tl = tx(f"{C['threshold']:.1f}: 20% below 2021", 13, PRICE).next_to(pa.ax.c2p(2019.1, C["threshold"]), UP, buff=0.05).align_to(
            pa.ax.c2p(2019.1, 0), LEFT)
        box = Rectangle(width=pa.ax.c2p(2028, 0)[0] - pa.ax.c2p(2027, 0)[0], height=4.0, stroke_color=GOLD, stroke_width=1.5,
                        fill_color=GOLD, fill_opacity=0.08).move_to([(pa.ax.c2p(2028, 0)[0] + pa.ax.c2p(2027, 0)[0]) / 2,
                                                                    pa.ax.c2p(0, 85)[1], 0])
        q = tx("?", 40, GOLD, bold=True).move_to(box)
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("Germany's chemical output in 2027", 17, WHITE),
                       tx("will average below 79.8 (2021 = 100):", 17, WHITE),
                       tx("still at least 20% below 2021.", 17, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked against Eurostat in early 2028", 14, GREY_A)).arrange(DOWN, buff=0.12).move_to([4.2, 1.0, 0])
        why = VGroup(tx("For: gas about eight times America's", 14, GOOD), tx(f"(Sep 2026); the index at {E['de_last']:.0f};", 14, GOOD),
                     tx("closures announced", 14, GOOD), tx("Against: cheaper gas, a demand recovery,", 14, BAD),
                     tx("revisions", 14, BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.2, -2.0, 0])
        src = source("Eurostat, sts_inpr_m (C20, Germany, seasonally and calendar adjusted, 2021 = 100)", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> Germany's chemical output "
            f"averaged {C['de25']:.1f} in 2025, on an index where 2021 is a hundred, and about {C['de26']:.0f} in the "
            "first nine months of 2026. <bookmark mark='b'/> We think that in 2027 it will still average below "
            f"{C['threshold']:.1f}, at least twenty per cent below 2021. European gas was still about eight times "
            "America's price in September 2026, and the closures already announced take capacity out for good. "
            "Against us: gas could fall, demand could recover, and the figures get revised. <bookmark mark='c'/> We give "
            f"it {100 * C['prob']:.0f} per cent, and we will check it against Eurostat's figures in early 2028, right or "
            "wrong."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(card_[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(thr), FadeIn(tl), FadeIn(box), FadeIn(q), FadeIn(card_[1:4]))
            self.play(FadeIn(why, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(card_[4:], scale=1.1))
        self.clear_scene()


def j_ok(proj, actual) -> bool:
    """Green when the outcome landed on the projection's side of zero and within a percentage point of it."""
    return (proj >= 0) == (actual >= 0) and abs(proj - actual) <= 1.0
