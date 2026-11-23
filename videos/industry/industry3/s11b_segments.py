from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403

SEG = [("Productivity and\nBusiness Processes", "Office, LinkedIn, Dynamics", get("msft.pbp_rev"), get("msft.pbp_oi"),
        120.810, "#4FA3F7"),
       ("Intelligent Cloud", "Azure, server products", get("msft.ic_rev"), get("msft.ic_oi"), 106.265, "#7EC8F5"),
       ("More Personal\nComputing", "Windows, devices, Xbox, search ads", get("msft.mpc_rev"), get("msft.mpc_oi"),
        54.649, "#8B95A7")]


class Segments(VoiceoverScene):
    def construct(self):
        card(self, 10, "The businesses inside", "What do a company's totals hide?",
             "Chapter ten. The businesses inside.", lit=("unit", "moat", "change"))
        self.microsoft()
        self.lilly()

    def microsoft(self):
        s = 3.6 / 140
        groups = VGroup()
        for i, (nm, what, rev, oi, rev25, col) in enumerate(SEG):
            x = -4.3 + i * 4.3
            r = Rectangle(width=1.5, height=rev * s, fill_color=col, fill_opacity=0.45, stroke_color=col,
                          stroke_width=2).move_to(np.array([x - 0.42, -2.2 + rev * s / 2, 0]))
            o = Rectangle(width=1.5, height=oi * s, fill_color=col, fill_opacity=0.95, stroke_width=0).move_to(
                np.array([x + 0.42, -2.2 + oi * s / 2, 0]))
            o.set_z_index(1)
            rv = TB(f"${rev:.0f}bn", 18, col).next_to(r, UP, buff=0.06).shift(LEFT * 0.25)
            ov = TB(f"{100 * oi / rev:.0f}% margin", 17, I.PROFIT).next_to(o, UP, buff=0.06).shift(RIGHT * 0.3)
            g = 100 * (rev / rev25 - 1)
            gr = T(f"sales {g:+.0f}% on a year before", 15, I.PROFIT if g > 0 else I.COST)
            name_t = VGroup(*[TB(t, 18, I.TEXT) for t in nm.split("\n")]).arrange(DOWN, buff=0.03)
            lab = VGroup(name_t, T(what, 14, I.DIM), gr).arrange(DOWN, buff=0.06).next_to(
                np.array([x, -2.2, 0]), DOWN, buff=0.15)
            groups.add(VGroup(r, o, rv, ov, lab))
        key = VGroup(VGroup(Square(0.2, fill_color="#4FA3F7", fill_opacity=0.45, stroke_color="#4FA3F7"),
                            T("revenue", 15, I.TEXT)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, fill_color="#4FA3F7", fill_opacity=0.95, stroke_width=0),
                            T("operating income", 15, I.TEXT)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.4).to_corner(UR, buff=0.4)
        axis = Line(np.array([-6.5, -2.2, 0]), np.array([6.5, -2.2, 0]), color=I.EDGE)
        head = T("Microsoft's three segments, fiscal 2026", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = source("Microsoft Form 10-K FY2026, segment results of operations", size=13)
        with self.voiceover(
            "A company's totals can hide several different businesses, and the notes break them out as segments. "
            "Microsoft reports three. <bookmark mark='a'/> Productivity and Business Processes: Office, LinkedIn and "
            f"Dynamics. {say_bn(SEG[0][2])} of revenue in fiscal 2026, and an operating margin of "
            f"{100 * SEG[0][3] / SEG[0][2]:.0f} percent: subscriptions to software hundreds of millions of people "
            f"already use. <bookmark mark='b'/> Intelligent Cloud: Azure and the server business, "
            f"{say_bn(SEG[1][2])}, up thirty percent, with Azure itself up 41 percent. Its margin is lower, "
            f"{100 * SEG[1][3] / SEG[1][2]:.0f} percent, and its costs rose 44 percent, which Microsoft says was "
            "driven by its investment in AI infrastructure: the data centres of the last chapters show up here. "
            f"<bookmark mark='c'/> More Personal Computing: Windows, Surface, Xbox and search advertising, "
            f"{say_bn(SEG[2][2])}, slightly smaller than a year before, at {100 * SEG[2][3] / SEG[2][2]:.0f} percent. "
            "<bookmark mark='d'/> So the profit is in Office, the growth is in the cloud, and the spending is for "
            "the cloud's future. One set of totals; three businesses with different economics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis), FadeIn(key))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                g = groups[i]
                self.play(GrowFromEdge(g[0], DOWN), GrowFromEdge(g[1], DOWN), FadeIn(g[2]), FadeIn(g[3]),
                          FadeIn(g[4]), run_time=1.2)
            vo.wait_until("d")
            self.play(Indicate(groups[0][3], color=I.PROFIT), Indicate(groups[1][4][2], color=I.PROFIT))
        self.clear_scene()

    def lilly(self):
        rev = get("lly.rev")
        items = [("Mounjaro", get("lly.mounjaro"), "#F2C14E"), ("Zepbound", get("lly.zepbound"), "#F2A65A"),
                 ("Everything else", rev - get("lly.mounjaro") - get("lly.zepbound"), "#5B6578")]
        bar = viz.bar_split(items, rev, width=11.0, height=0.95).move_to(UP * 0.4)
        labs = VGroup()
        for (nm, v, c), r in zip(items, bar[:3] if len(bar) >= 3 else bar):
            labs.add(VGroup(TB(f"${v:.1f}bn", 22, c), T(nm, 17, I.TEXT), T(f"{100 * v / rev:.0f}% of revenue", 15,
                                                                         I.DIM)).arrange(DOWN, buff=0.04).next_to(
                r, DOWN, buff=0.25))
        head = T(f"Eli Lilly's revenue, 2025: ${rev:.1f}bn", 24, I.TEXT).to_edge(UP, buff=0.6)
        note = T("both are tirzepatide: one medicine, sold for diabetes and for weight loss", 19, I.ACCENT).to_edge(
            DOWN, buff=0.8)
        src = source("Eli Lilly Form 10-K 2025, revenue by product", size=13)
        share = (get("lly.mounjaro") + get("lly.zepbound")) / rev
        with self.voiceover(
            "Segments can also be products. <bookmark mark='a'/> Of Eli Lilly's 65 billion dollars of revenue in "
            f"2025, {say_pct(share)} came from two names, Mounjaro and Zepbound, <bookmark mark='b'/> which are the "
            "same medicine, tirzepatide, sold for diabetes and for weight loss. That one molecule explains most of "
            "Lilly's growth, its margin and its return on capital. It also tells you the risk: the accounts of a "
            "drug maker are as strong as its patents, and every patent expires."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()
