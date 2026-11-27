from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 12, "Called it?", "How well does a drug company forecast its own year?",
             "Chapter twelve. Called it? How well does a drug company in a boom forecast its own year?", lit=("change",))
        self.lilly()
        self.ours()

    def lilly(self):
        C = R["called"]
        pa = viz.plot_axes([50, 100], [0, 2], x_length=10.0, y_length=2.6, xticks=[50, 60, 70, 80, 90, 100],
                           xfmt=lambda v: f"${int(v)}bn", grid=False, size=13).move_to([0.4, 0.3, 0])
        ax = pa.ax
        y25, y26 = 1.5, 0.5
        r25 = Line(ax.c2p(C["g2025"][0], y25), ax.c2p(C["g2025"][1], y25), stroke_color=PRICE, stroke_width=12)
        l25 = tx("February 2025: 2025 revenue $58.0-61.0bn", 14, PRICE).next_to(r25, UP, buff=0.12)
        a25 = marker(ax, C["a2025"], y25, f"actual: ${C['a2025']:.1f}bn", GOOD, side=RIGHT)
        r26 = Line(ax.c2p(C["g2026"][0], y26), ax.c2p(C["g2026"][1], y26), stroke_color=PRICE, stroke_width=12)
        l26 = tx("February 2026: 2026 revenue $80-83bn", 14, PRICE).next_to(r26, DOWN, buff=0.12)
        r26b = Line(ax.c2p(C["g2026_oct"][0], y26), ax.c2p(C["g2026_oct"][1], y26), stroke_color=GOOD, stroke_width=12)
        l26b = tx("October 2026: raised to $91-92bn", 14, GOOD, bold=True).next_to(r26b, UP, buff=0.12)
        nm = VGroup(tx("2025", 20, WHITE, bold=True).next_to(ax.c2p(50, y25), LEFT, buff=0.3),
                    tx("2026", 20, WHITE, bold=True).next_to(ax.c2p(50, y26), LEFT, buff=0.3))
        src = source("Eli Lilly and Company, Forms 8-K of 6 February 2025, 4 February 2026 and 29 October 2026; Form 10-K 2025",
                     size=12)
        beat(self,
             "Drug companies publish forecasts of their own year. Here are Lilly's. <bookmark mark='a'/> In February "
             "2025 it expected revenue of fifty-eight to sixty-one billion dollars. <bookmark mark='b'/> It reported "
             f"{C['a2025']:.1f} billion, seven per cent above the top of its own range. <bookmark mark='c'/> In February "
             "2026 it expected eighty to eighty-three billion for 2026, <bookmark mark='d'/> and in October it raised that "
             "to ninety-one to ninety-two billion. In a boom, even the company inside it keeps underestimating. A company "
             "sets its own forecast, and beating one reads better than missing it, so the numbers it publishes tend to "
             "lean low.",
             base=[pa, nm, src], steps=[[r25, l25], a25, [r26, l26], [r26b, l26b]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx(f"Lilly's 2026 revenue will come in at or above ${C['g2026_oct'][1]:.0f}bn, the top of its raised range.", 21, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets(["for: it beat the top of its range by 7% in 2025, and it raised again in October",
                       "against: a raise in late October leaves only one quarter to surprise, and prices are falling",
                       f"third quarter of 2026: ${C['q3']:.1f}bn, up 39%"], size=18).move_to([0, -0.4, 0])
        rule = tx("scored on Lilly's fourth-quarter results or Form 10-K for 2026, due February 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Lilly's 2026 revenue will reach at least {C['g2026_oct'][1]:.0f} "
             f"billion dollars, the top of its raised range, and give it {100 * C['prob']:.0f} per cent. "
             "<bookmark mark='b'/> For: it beat its range comfortably last year and has kept raising. Against: by late "
             "October most of the year is known, so there is little room left to surprise, and its prices are falling. "
             "<bookmark mark='c'/> Lilly's report in February will settle it. Fifty-five per cent is only a little better "
             "than a coin: we think the company is still leaning low, but not by much. If revenue lands inside its range, "
             "we were wrong, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
