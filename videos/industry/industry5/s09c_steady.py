from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

LINES = (("V", "Visa", "#F6C453"), ("COST", "Costco", "#7EC8F5"), ("DAL", "Delta Air Lines", ENTRANT))


class Steady(VoiceoverScene):
    def construct(self):
        card(self, 13, "A moat in the accounts", "What does a moat look like in a company's figures?",
             "Chapter thirteen. A moat in the accounts.", lit=("moat", "dollar"))
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
            labels[tic] = tx(name, 19, col, bold=True).next_to(pts[-1], RIGHT, buff=0.12).shift(
                {"COST": DOWN * 0.14, "DAL": UP * 0.14}.get(tic, ORIGIN))
        crash = tx("2020: -73%", 16, ENTRANT).next_to(ax.c2p(2020, -0.29), RIGHT, buff=0.1)
        legal = tx("2012: a one-time legal charge", 15, "#F6C453").next_to(ax.c2p(2012, 0.2), DOWN, buff=0.12)
        src = source("SEC company facts: Forms 10-K of Visa, Costco and Delta, fiscal 2009-2026", size=13)
        cardg = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.95, stroke_width=0, fill_color="#2B4C9B",
                                        fill_opacity=1),
                       Rectangle(width=1.5, height=0.16, stroke_width=0, fill_color="#0E1117", fill_opacity=1).shift(
                           UP * 0.18),
                       Rectangle(width=0.3, height=0.22, stroke_width=0, fill_color="#F6C453", fill_opacity=1).shift(
                           LEFT * 0.45 + DOWN * 0.15))
        icons = VGroup(VGroup(cardg, tx("Visa", 20, "#F6C453", bold=True)).arrange(DOWN, buff=0.15),
                       VGroup(draw.shop(1.3, color="#7EC8F5"), tx("Costco", 20, "#7EC8F5", bold=True)).arrange(DOWN, buff=0.15),
                       VGroup(draw.plane(1.8), tx("Delta", 20, ENTRANT, bold=True)).arrange(DOWN, buff=0.15)
                       ).arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to([0.2, 0.6, 0])
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
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl), Create(zero), FadeIn(src),
                      LaggedStart(*[FadeIn(i_, shift=UP * 0.2) for i_ in icons], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("a")
            self.play(FadeOut(icons), run_time=0.6)
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
        self.map()

    def map(self):
        Mm = R["margin_map"]
        pa = viz.plot_axes([0, 0.65], [0, 0.28], x_length=9.0, y_length=4.6, xticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                           yticks=[0.1, 0.2], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"{100 * v:.0f} pts",
                           xlabel="average operating margin, fiscal 2009 to the latest year",
                           ylabel="how far it wanders from year to year (standard deviation)", size=15)
        pa.move_to([0.3, -0.2, 0])
        steady = Rectangle(width=pa.ax.c2p(0.65, 0)[0] - pa.ax.c2p(0, 0)[0],
                           height=pa.ax.c2p(0, 0.12)[1] - pa.ax.c2p(0, 0)[1], stroke_width=0, fill_color=RET,
                           fill_opacity=0.10).move_to(pa.ax.c2p(0, 0), aligned_edge=DL)
        st = tx("steady", 17, RET).next_to(steady, LEFT, buff=0.1).shift(UP * 0.05)
        dots, labs = VGroup(), VGroup()
        for d in Mm:
            p_ = pa.ax.c2p(d["mean"], d["sd"])
            col = RET if d["sd"] < 0.12 else COST_
            dots.add(glow_dot(p_, color=col, radius=0.09))
            labs.add(tx(d["name"], 16, WHITE).next_to(p_, UR if d["tic"] not in ("WMT",) else DR, buff=0.05))
        src = source("SEC company facts: Forms 10-K, fiscal 2009 to 2025 or 2026", size=13)
        with self.voiceover(
            "Put every company in this series' filings on one chart. <bookmark mark='a'/> Along the bottom, each "
            "company's average operating margin since 2009. Up the side, how far that margin wanders from year to "
            "year. <bookmark mark='b'/> The steady ones sit along the bottom, at every height: Costco and Walmart "
            "with thin margins, NextEra and Microsoft in the middle, Mastercard and Visa at the top; Visa sits a "
            "little higher only because of its one-time legal charge in 2012. "
            "<bookmark mark='c'/> The wanderers sit above: Delta, Intel and Micron, whose margins swing with fuel, "
            "with chip prices and with the cycle that Part 6 is about. <bookmark mark='d'/> The height of a margin "
            "and its steadiness are different things. A moat shows up in the second."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa))
            vo.wait_until("a")
            self.play(FadeIn(steady), FadeIn(st))
            vo.wait_until("b")
            low = [i for i, d in enumerate(Mm) if d["sd"] < 0.12]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i], scale=2), FadeIn(labs[i])) for i in low],
                                  lag_ratio=0.25), run_time=2.4)
            vo.wait_until("c")
            high = [i for i, d in enumerate(Mm) if d["sd"] >= 0.12]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i], scale=2), FadeIn(labs[i])) for i in high],
                                  lag_ratio=0.3), run_time=1.8)
            vo.wait_until("d")
            self.play(Indicate(steady, color=RET, scale_factor=1.0))
        self.clear_scene()
