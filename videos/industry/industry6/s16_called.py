from __future__ import annotations

from explainer.industry.calls import calls
from videos.industry.industry6.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 16, "Called it?", "Can you see a peak while you are standing on it?",
             "Chapter sixteen. Called it?", lit=("change",))
        self.intel()
        self.ours()

    def intel(self):
        I_ = R["intel"]
        yrs = I_["years"]
        pa = viz.plot_axes([2018.4, 2025.6], [-15, 30], x_length=7.6, y_length=4.2, xticks=yrs, yticks=[-10, 0, 10, 20],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([2.0, -0.7, 0])
        zero = DashedLine(pa.ax.c2p(2018.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_C, stroke_width=1.5)
        bars = VGroup()
        for y, v in zip(yrs, I_["capex"]):
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, v)
            bars.add(Rectangle(width=0.5, height=p1[1] - p0[1], stroke_width=0, fill_color=ORDER, fill_opacity=0.85
                               ).move_to([p0[0] - 0.14, (p0[1] + p1[1]) / 2, 0]))
        oi = VGroup()
        for y, v in zip(yrs, I_["oi"]):
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, v)
            h = abs(p1[1] - p0[1])
            oi.add(Rectangle(width=0.28, height=max(h, 0.02), stroke_width=0, fill_color=BOOM if v > 0 else BUST,
                             fill_opacity=0.95).move_to([p0[0] + 0.2, (p0[1] + p1[1]) / 2, 0]))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=ORDER, fill_opacity=1),
                            tx("spending on plant", 16, ORDER)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=BOOM, fill_opacity=1),
                            tx("operating profit", 16, BOOM)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.5).next_to(
            pa, UP, buff=0.15).align_to(pa, LEFT)
        rel = VGroup(RoundedRectangle(corner_radius=0.06, width=3.6, height=2.0, stroke_width=0, fill_color="#E8E4DA",
                                      fill_opacity=1),
                     tx("23 March 2021", 15, "#4A4F5A").shift(UP * 0.62),
                     tx("IDM 2.0", 28, "#1B1F27", bold=True).shift(UP * 0.18),
                     tx(f"about ${R['intel']['announced']:.0f} billion for", 17, "#1B1F27").shift(DOWN * 0.3),
                     tx("two new factories in Arizona", 17, "#1B1F27").shift(DOWN * 0.62)).move_to([-5.0, 2.2, 0])
        fabs = VGroup(draw.factory(1.0, color="#7EC8F5"), draw.factory(1.0, color="#7EC8F5")).arrange(RIGHT, buff=0.15)
        fabs.next_to(rel, DOWN, buff=0.35)
        i21, i24 = yrs.index(2021), yrs.index(2024)
        src = source("Intel press release, 23 March 2021; Intel Forms 10-K, 2019-2025 (SEC company facts)", size=13)
        with self.voiceover(
            "Every part ends with a forecast. This one is a decision made at a peak. <bookmark mark='a'/> In March "
            "2021, in the middle of a worldwide shortage of chips, Intel's new chief executive, Pat Gelsinger, "
            "announced a plan to build its way back to the front of the industry, starting with about twenty "
            "billion dollars for two new factories in Arizona. <bookmark mark='b'/> Intel's "
            f"spending on plant rose from {I_['capex'][yrs.index(2020)]:.1f} billion dollars in 2020 to "
            f"{I_['capex'][yrs.index(2023)]:.1f} billion in 2023. <bookmark mark='c'/> Its operating profit went the "
            f"other way: from {I_['oi'][i21]:.1f} billion in 2021 to a loss of {-I_['oi'][i24]:.1f} billion in "
            "2024. The shortage passed, and the new factories were costs long before they were "
            f"revenue. <bookmark mark='d'/> In 2025 Intel cut its spending to {I_['capex'][-1]:.1f} billion. A plan "
            "drawn up at a peak, with the peak's numbers, met the trough."
        ) as vo:
            self.play(FadeIn(src), FadeIn(rel, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f_, shift=UP * 0.2) for f_ in fabs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(pa), Create(zero), FadeIn(key))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(o_) for o_ in oi], lag_ratio=0.15), run_time=2.0)
            self.play(Indicate(oi[i24], color=BUST, scale_factor=1.3), fabs.animate.set_opacity(0.4))
            vo.wait_until("d")
            self.play(Indicate(bars[-1], color=WHITE))
        self.clear_scene()

    def ours(self):
        c = calls(6, ours=True)[0]
        m = R["micron"]
        br = R["base_rate"]
        box = RoundedRectangle(corner_radius=0.15, width=12.4, height=2.6, fill_color="#141A24", fill_opacity=1,
                               stroke_color=GOLD, stroke_width=2).move_to(UP * 2.0)
        body = VGroup(tx("This series' call, made 24 November 2026", 22, GOLD, bold=True),
                      tx("Before the end of 2028, Micron will report a quarter whose revenue is at least 25% below", 19),
                      tx(f"its highest earlier quarter (so far ${m['q4_26']['revenue']:.1f}bn, the quarter to "
                         f"3 September 2026).", 19),
                      tx("Probability: 55%. Scored on Micron's Forms 10-Q and 10-K, January 2029.", 18, GOLD)).arrange(
            DOWN, buff=0.14).move_to(box)
        # the evidence: each past peak and its fall
        falls = VGroup()
        for p in br["peaks"]:
            h1, h2 = 1.8, 1.8 * (1 + p["fall"])
            a_ = Rectangle(width=0.5, height=h1, stroke_width=0, fill_color=CAP, fill_opacity=0.85)
            b_ = Rectangle(width=0.5, height=h2, stroke_width=0, fill_color=BUST, fill_opacity=0.85)
            pair = VGroup(a_, b_).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            falls.add(VGroup(pair, tx(f"{100 * p['fall']:.0f}%", 20, BUST, bold=True).next_to(pair, UP, buff=0.1),
                             tx(p["end"][:4], 15, GREY_B).next_to(pair, DOWN, buff=0.1)))
        falls.arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to([-2.6, -1.8, 0])
        ft = tx("Micron's past peaks, and the lowest quarter within two years", 16, GREY_A).next_to(falls, UP, buff=0.5)
        rd = dict(R["reading"]["micron"])
        why = VGroup(tx("For: spending 3.2× depreciation;", 17, WHITE), tx("every past peak fell 20% or more", 17, WHITE),
                     tx("Against: demand from AI data centres", 17, GREY_B),
                     tx("may grow faster than the new plants", 17, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        why.move_to([4.3, -1.6, 0])
        with self.voiceover(
            "And this series' own call, logged today. <bookmark mark='a'/> Before the end of 2028, Micron will "
            "report a quarter whose revenue is at least a quarter below the best quarter before it. So far that is "
            f"{m['q4_26']['revenue']:.1f} billion dollars, the quarter to September 2026. <bookmark mark='b'/> The "
            "case for: after every one of its four earlier peaks, Micron's quarterly revenue fell by a fifth or "
            f"more within two years, and in three of the four by more than a quarter. And it is spending "
            f"{rd[2026]:.1f} times its depreciation. <bookmark mark='c'/> The case against: the demand from data "
            "centres for artificial intelligence may keep growing faster than the new factories can be built. We "
            "put it at fifty-five percent, and will score it from Micron's own reports in January 2029."
        ) as vo:
            self.play(FadeIn(box), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(ft), LaggedStart(*[FadeIn(f_, shift=UP * 0.15) for f_ in falls], lag_ratio=0.3),
                      FadeIn(why[:2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(why[2:]), FadeIn(body[3]))
        self.clear_scene()
        assert "Micron" in c.claim
