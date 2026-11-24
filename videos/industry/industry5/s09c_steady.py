from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

LINES = (("V", "Visa", "#F6C453"), ("COST", "Costco", "#7EC8F5"), ("DAL", "Delta Air Lines", ENTRANT))


class Steady(VoiceoverScene):
    def construct(self):
        card(self, 12, "A moat in the accounts", "What does a moat look like in a company's figures?",
             "Chapter twelve. A moat in the accounts.", lit=("moat", "dollar"))
        M = R["margins"]
        ax = CornerAxes(x_range=[2008.5, 2026.5, 1], y_range=[-0.3, 0.7, 0.1], x_length=10.0, y_length=5.0,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-0.4, -0.35, 0])
        zero = DashedLine(ax.c2p(2008.5, 0), ax.c2p(2026.5, 0), stroke_color=GREY_C, stroke_width=1.5)
        xt = VGroup(*[tx(f"{y}", 15, GREY_B).next_to(ax.c2p(y, -0.3), DOWN, buff=0.08) for y in (2010, 2014, 2018, 2022, 2026)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(2008.5, v), LEFT, buff=0.08)
                      for v in (-0.2, 0.2, 0.4, 0.6)])
        yl = tx("operating profit per dollar of sales, each fiscal year", 17, GREY_B).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)

        def clip(v):
            return max(v, -0.29)
        paths, labels = {}, {}
        for tic, name, col in LINES:
            pts = [ax.c2p(y, clip(v)) for y, v in M[tic]["points"]]
            paths[tic] = VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(pts)
            labels[tic] = tx(name, 19, col, bold=True).next_to(pts[-1], RIGHT, buff=0.12)
        crash = tx("2020: -73%", 16, ENTRANT).next_to(ax.c2p(2020, -0.29), RIGHT, buff=0.1)
        legal = tx("2012: a one-time legal charge", 15, "#F6C453").next_to(ax.c2p(2012, 0.2), DOWN, buff=0.12)
        src = source("SEC company facts: Forms 10-K of Visa, Costco and Delta, fiscal 2009-2026", size=13)
        sd = {k: M[k]["sd"] for k in M}
        with self.voiceover(
            "What does a moat look like in a company's own accounts? Not, as you might think, a high margin. "
            "<bookmark mark='a'/> Here is the operating profit Visa kept from each dollar of sales, every year since "
            "2009. Apart from one year with a large legal charge, it has stayed between about half and two thirds. "
            "<bookmark mark='b'/> Here is Costco. It keeps less than four cents of each dollar, a margin most "
            "businesses would call a disaster. But look at the line: it has hardly moved in seventeen years, and it "
            "has edged up. Buffett named Costco, with GEICO, as the kind of low-cost producer that has a moat: "
            "its prices are so low that a rival cannot undercut them. <bookmark mark='c'/> And here is Delta: "
            "a healthy margin in good years, then minus seventy-three percent in 2020. "
            f"<bookmark mark='d'/> Measure how far each line wanders, and Costco's moves by less than half a point "
            f"a year, Visa's by about {100 * sd['V']:.0f}, Delta's by {100 * sd['DAL']:.0f}. A moat shows up as a "
            "margin that rivals and recessions cannot push around, whatever its height."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(paths["V"]), run_time=2.4)
            self.play(FadeIn(labels["V"]), FadeIn(legal))
            vo.wait_until("b")
            self.play(Create(paths["COST"]), run_time=2.4)
            self.play(FadeIn(labels["COST"]))
            vo.wait_until("c")
            self.play(Create(paths["DAL"]), run_time=2.4)
            self.play(FadeIn(labels["DAL"]), FadeIn(crash))
            vo.wait_until("d")
            self.play(Indicate(paths["COST"], color=WHITE), Indicate(labels["COST"], color=WHITE))
        self.clear_scene()
