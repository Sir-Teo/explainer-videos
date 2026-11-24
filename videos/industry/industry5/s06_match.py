from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

SHORT = {"Retail (Building Supply)": "Home centers", "Beverage (Soft)": "Soft drinks",
         "Household Products": "Soap and detergent", "Air Transport": "Airlines", "Restaurant/Dining": "Restaurants",
         "Auto & Truck": "Carmakers", "Trucking": "Trucking", "Tobacco": "Tobacco"}


class Match(VoiceoverScene):
    def construct(self):
        card(self, 7, "Few castles, high walls?", "Do concentrated industries earn more?",
             "Chapter seven. Few castles, high walls?", lit=("moat",))
        M = R["match"]
        ax = CornerAxes(x_range=[0, 100, 25], y_range=[0, 0.7, 0.1], x_length=7.2, y_length=5.0,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-1.3, -0.3, 0])
        xt = VGroup(*[tx(f"{v}%", 15, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (25, 50, 75, 100)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0.2, 0.4, 0.6)])
        xl = tx("share of sales of the four largest firms (Census, 2022)", 17, GREY_B).next_to(ax, DOWN, buff=0.4)
        yl = tx("return on capital, 2025 (Damodaran)", 17, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        pts, labs = VGroup(), VGroup()
        for m in M:
            good = m["roc"] > 0.2
            p_ = ax.c2p(m["cr4"], m["roc"])
            pts.add(glow_dot(p_, color=RET if good else (COST_ if m["cr4"] > 50 else GREY_B), radius=0.1))
            t_ = tx(SHORT.get(m["industry"], m["industry"]), 17, WHITE).next_to(p_, UR, buff=0.06)
            labs.add(t_)
        nm = [m["industry"] for m in M]
        good = [nm.index(k) for k in ("Tobacco", "Retail (Building Supply)")]
        bad = [nm.index(k) for k in ("Air Transport", "Auto & Truck")]
        rest = [i for i in range(len(M)) if i not in good + bad]
        labs[nm.index("Auto & Truck")].next_to(pts[nm.index("Auto & Truck")], DR, buff=0.04)
        side = VGroup(tx("Few firms help only if", 22, GOLD, bold=True),
                      tx("1. something stops new ones coming in", 19, WHITE),
                      tx("2. the few do not fight each other", 19, WHITE),
                      tx("   to the cost of one more (Part 4)", 19, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        side.move_to([4.6, 1.2, 0])
        note = tx("eight industries matched by hand between two sources: this film's pairing", 15, GREY_C).to_corner(
            DR, buff=0.28)
        src = source("Census 2022 Economic Census; Damodaran, Excess Returns by industry, 2025", corner=DL)
        with self.voiceover(
            "If an industry has only a few castles, do they earn more? Put the two measures side by side. "
            "<bookmark mark='a'/> Along the bottom, the share of sales held by an industry's four largest firms, from "
            "the Census. Up the side, the return on capital, from Damodaran. The two sources group industries "
            "differently, so these are eight that can be matched by hand. <bookmark mark='b'/> Tobacco and home "
            "centers sit top right: a few firms, and very high returns. <bookmark mark='c'/> But look at the "
            "airlines and the carmakers. The four largest airlines take nearly three quarters of their industry's "
            "sales, and the four largest carmakers more than half, yet both earn less than ten percent, near or "
            "below what their capital costs. <bookmark mark='d'/> And restaurants, where the four largest firms have six "
            "percent of sales, earn more than either. <bookmark mark='e'/> Concentration is not a moat. A small "
            "number of firms earns high returns only if something stops new firms coming in, and only if the few "
            "do not fight each other down to the cost of one more unit, as memory makers did in Part 4. The "
            "rest of this part is about what that something is."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(src), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(pts[i], scale=2) for i in rest], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(labs[i]) for i in rest], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            self.play(*[FadeIn(pts[i], scale=2) for i in good], *[FadeIn(labs[i]) for i in good])
            vo.wait_until("c")
            self.play(*[FadeIn(pts[i], scale=2) for i in bad], *[FadeIn(labs[i]) for i in bad])
            self.play(*[Indicate(labs[i], color=COST_) for i in bad])
            vo.wait_until("d")
            r_ = nm.index("Restaurant/Dining")
            self.play(Indicate(pts[r_], scale_factor=2.0), Indicate(labs[r_]))
            vo.wait_until("e")
            self.play(FadeIn(side, shift=LEFT * 0.2))
        self.clear_scene()
