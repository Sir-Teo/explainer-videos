from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403

COLS = {"MSFT": "#7EC8F5", "GOOGL": "#7BD88F", "AMZN": "#F2A65A", "META": "#B58CFF"}


class Ai(VoiceoverScene):
    def construct(self):
        card(self, 14, "A boom you can watch", "What do the gauges say about the data centres being built today?",
             "Chapter fourteen. A boom you can watch.", lit=("change",))
        self.spend()
        self.gauges()

    def spend(self):
        H = R["hyperscale"]
        yrs = H["years"]
        pa = viz.plot_axes([2014.4, 2025.6], [0, 380], x_length=8.4, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[100, 200, 300], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([1.4, -0.6, 0])
        stacks = VGroup()
        for y in yrs:
            base = 0.0
            col = VGroup()
            for t in H["names"]:
                v = H["capex"][t][yrs.index(y)] or 0.0
                p0, p1 = pa.ax.c2p(y, base), pa.ax.c2p(y, base + v)
                col.add(Rectangle(width=0.55, height=max(p1[1] - p0[1], 0.003), stroke_width=0, fill_color=COLS[t],
                                  fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
                base += v
            stacks.add(col)
        tops = VGroup(*[tx(f"${H['total'][y]:.0f}bn", 15, WHITE).next_to(stacks[k], UP, buff=0.06)
                        for k, y in enumerate(yrs) if y in (2015, 2020, 2025)])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=COLS[t], fill_opacity=1), tx(n, 16, COLS[t])).arrange(
            RIGHT, buff=0.1) for t, n in H["names"].items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-5.2, 1.2, 0])
        head = tx("capital spending each fiscal year: data centres, chips, power, and (for Amazon) warehouses", 16,
                  GREY_A).next_to(pa, UP, buff=0.15)
        racks = VGroup(*[draw.server_rack(0.9) for _ in range(6)]).arrange(RIGHT, buff=0.1).move_to([-4.6, -1.6, 0])
        racks.scale_to_fit_width(3.2)
        src = source("Forms 10-K of Microsoft (fiscal years to June), Alphabet, Amazon and Meta (SEC company facts)", size=13)
        m26 = H["msft26"]
        with self.voiceover(
            "Everything in this part says you cannot know when a cycle will turn. But you can watch one being built. "
            "<bookmark mark='a'/> Here are four of the companies spending most on data centres for artificial "
            "intelligence: Microsoft, Alphabet, Amazon and Meta. <bookmark mark='b'/> In 2015, between them, they "
            f"spent {H['total'][2015]:.0f} billion dollars on buildings and equipment. <bookmark mark='c'/> By 2020, "
            f"{H['total'][2020]:.0f} billion. <bookmark mark='d'/> In 2025, {H['total'][2025]:.0f} billion: more "
            "than fifteen times as much in ten years. Amazon's figure includes its warehouses. And Microsoft's next "
            f"year, to June 2026, "
            f"came in at {m26['capex']:.0f} billion on its own."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in racks], lag_ratio=0.1),
                      FadeIn(pa), FadeIn(head), run_time=1.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k_, shift=RIGHT * 0.15) for k_ in key], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in stacks[0]], lag_ratio=0.1), FadeIn(tops[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in col]) for col in stacks[1:6]],
                                  lag_ratio=0.3), FadeIn(tops[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in col]) for col in stacks[6:]],
                                  lag_ratio=0.3), run_time=2.4)
            self.play(FadeIn(tops[2], scale=1.3))
        self.clear_scene()

    def gauges(self):
        H = R["hyperscale"]
        r25, s25 = H["ratio"][2025], H["share_of_cash"][2025]
        r23 = H["ratio"][2023]
        t1, t2 = ValueTracker(0.0), ValueTracker(0.0)
        g1 = draw.gauge(t1, 0, 4, r=1.2, bands=((BOOM, 0.4), (ORDER, 0.7), (BUST, 1.0))).move_to([-3.3, 0.9, 0])
        g2 = draw.gauge(t2, 0, 1, r=1.2, bands=((BOOM, 0.4), (ORDER, 0.7), (BUST, 1.0))).move_to([3.3, 0.9, 0])
        n1 = draw.number(lambda: t1.get_value(), 1, suffix="×", size=34, color=WHITE)
        n2 = draw.number(lambda: 100 * t2.get_value(), 0, suffix="%", size=34, color=WHITE)
        n1.add_updater(lambda g: g.next_to(g1, DOWN, buff=0.25))
        n2.add_updater(lambda g: g.next_to(g2, DOWN, buff=0.25))
        l1 = VGroup(tx("spending against wear", 20, WHITE, bold=True),
                    tx(f"2023: {r23:.1f}×   2025: {r25:.1f}×", 16, GREY_B)).arrange(DOWN, buff=0.06).move_to([-3.3, -1.7, 0])
        l2 = VGroup(tx("share of their operating cash spent on it", 20, WHITE, bold=True),
                    tx(f"2023: {100 * H['share_of_cash'][2023]:.0f}%   2025: {100 * s25:.0f}%", 16, GREY_B)).arrange(
            DOWN, buff=0.06).move_to([3.3, -1.7, 0])
        q = VGroup(tx("What the gauges cannot say:", 20, GOLD, bold=True),
                   tx("whether the customers' spending on AI grows as fast as the plant built for it.", 18, GREY_A)
                   ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.45)
        src = source("Forms 10-K (SEC company facts); this film's sums of the four", size=13)
        with self.voiceover(
            "Now read the gauges from chapter thirteen. <bookmark mark='a'/> Spending against wear: in 2025 the four "
            f"spent {r25:.1f} times their depreciation, up from {r23:.1f} in 2023. They are not replacing plant; they "
            "are building a new layer of it. <bookmark mark='b'/> And they are paying for it with their own cash: "
            f"about {100 * s25:.0f} cents of every dollar their businesses brought in went back into building, up from "
            f"{100 * H['share_of_cash'][2023]:.0f} two years earlier. <bookmark mark='c'/> Those readings look like the "
            "top of a capital cycle. They are also what the start of a long build-out looks like, when a new "
            "technology really does need new plant, as railways and electricity once did. The gauges cannot tell "
            "the two apart. What decides it is whether what customers spend on artificial intelligence grows as fast "
            "as the plant being built for it. And that, unlike the spending, is not yet in anyone's accounts. The "
            "memory chips of chapter seven are the same boom, seen from a supplier's side."
        ) as vo:
            self.play(FadeIn(src), FadeIn(g1), FadeIn(n1), FadeIn(g2.copy().set_opacity(0.25)))
            vo.wait_until("a")
            self.play(FadeIn(l1), t1.animate.set_value(r25), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(n2))
            self.play(FadeIn(l2), t2.animate.set_value(s25), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.1))
        n1.clear_updaters()
        n2.clear_updaters()
        self.clear_scene()
