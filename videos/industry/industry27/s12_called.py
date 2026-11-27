from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Can anyone forecast freight?",
             "Chapter ten. Called it? A line's forecast of its own year, the market's forecast of the cycle, and our own call.",
             lit=("change",))
        self.zim()
        self.cycle()
        self.ours()

    def zim(self):
        C = R["called"]
        pa = viz.plot_axes([1.5, 4.0], [0, 3], x_length=9.6, y_length=3.0, xticks=[2.0, 2.5, 3.0, 3.5],
                           xfmt=lambda v: f"${v:.1f}bn", grid=False, size=13).move_to([0.4, 0.0, 0])
        ax = pa.ax
        bars, labs = VGroup(), VGroup()
        for i, (when, lo, hi) in enumerate(C["g"]):
            yy = 2.5 - i
            b = Line(ax.c2p(lo, yy), ax.c2p(hi, yy), stroke_color=[RATE, BOX, BAD][i], stroke_width=16)
            bars.add(b)
            labs.add(tx(f"{when} 2026: ${lo:.1f}-{hi:.1f}bn", 16, [RATE, BOX, BAD][i], bold=True).next_to(b, UP, buff=0.12))
        lab = tx("ZIM's forecast of its own adjusted EBITDA for 2026, as it changed", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("ZIM, Forms 6-K of 19 August, 6 October and 18 November 2026", size=12)
        a, b, c = C["g"]
        beat(self,
             "ZIM first. In March 2026, with its sale to Hapag-Lloyd agreed, it gave no forecast for the year at all. "
             f"<bookmark mark='a'/> In August it expected adjusted earnings before interest, tax, depreciation and amortization "
             f"of {a[1]:.1f} to {a[2]:.1f} billion dollars. <bookmark mark='b'/> Seven weeks later, {b[1]:.1f} to {b[2]:.1f}. "
             f"<bookmark mark='c'/> Six weeks after that, {c[1]:.1f} to {c[2]:.1f}: half as much again as in August, for a year "
             "already three-quarters over. If a line cannot forecast its own year from inside it, nobody outside can forecast "
             "freight.",
             base=[pa, lab, src], steps=[[bars[0], labs[0]], [bars[1], labs[1]], [bars[2], labs[2]]])

    def cycle(self):
        C = R["called"]
        B = R["box"]["g"]
        rows = table([["", "the view at the end of 2021", "what followed"],
                      ["fleet growth", f"+{B['g21']:.1f}% in 2021", f"+{B['g24']:.1f}% in 2024, +{B['g25']:.1f}% in 2025"],
                      ["demand growth", f"+{C['d21']:.1f}% projected", f"+{B['d25']:.1f}% in 2025, +{B['d26']:.1f}% projected for 2026"],
                      ["ZIM's freight a TEU", f"${R['cycle']['rate'][2021]:,.0f} in 2021", f"${R['cycle']['rate'][2023]:,.0f} in 2023"]],
                     col_x=[-6.2, -2.8, 1.6], top=1.6, row_h=0.8, size=18, colors=[None] + [[WHITE, RATE, BAD]] * 3)
        src = source("Alphaliner, as quoted in ZIM's Forms 20-F for 2021 and 2025; ZIM's Forms 20-F", size=12)
        beat(self,
             "Then the market's own forecast, at the top of the boom. <bookmark mark='a'/> At the end of 2021 ZIM, citing "
             f"Alphaliner, reported that the fleet had grown only {B['g21']:.1f} per cent that year, <bookmark mark='b'/> while "
             f"demand was projected to grow {C['d21']:.1f}: more cargo than ships, for a second year. <bookmark mark='c'/> The "
             "lines ordered accordingly. The ships arrived in 2024 and 2025, when the fleet grew ten and seven per cent; and "
             f"ZIM's freight fell from {R['cycle']['rate'][2021]:,.0f} dollars a TEU to {R['cycle']['rate'][2023]:,.0f}. It was "
             "Run it, exactly.",
             base=[rows[0], src], steps=[rows[1], rows[2], rows[3]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, RATE, bold=True),
                       tx("Hapag-Lloyd's purchase of ZIM will be completed", 22, WHITE, bold=True),
                       tx("by 30 June 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, RATE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets(["for: agreed in February 2026 and approved by ZIM's shareholders in April; aimed to close in early 2027",
                       "for: the close is targeted for the first quarter, leaving a quarter to spare",
                       "against: Israel's golden share; the original application was terminated and must be filed again"],
                      size=18).move_to([0, -0.5, 0])
        rule = tx("scored on the companies' announcements of completion, or of a lapse, by 30 June 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours, and not on freight. <bookmark mark='a'/> We say Hapag-Lloyd's purchase of ZIM will be completed by 30 "
             f"June 2027, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: the companies agreed it in "
             "February 2026, ZIM's shareholders approved it in April, and the target is the first quarter of 2027, leaving a "
             "quarter to spare. Against: the State of Israel holds a golden share in ZIM, its original application was "
             "terminated, and a new one had still to be filed in November. <bookmark mark='c'/> The companies' announcements "
             "will settle it, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
