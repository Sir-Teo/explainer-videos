from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry5.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        card(self, 12, "Buyers and suppliers", "Who wins when one firm's customer is another firm?",
             "Chapter twelve. Buyers and suppliers.", lit=("moat", "who"))
        tsmc, fox, apple, qcom = (get("tsmc.gm.q4_2025"), get("foxconn.gm.2025"), get("apple.gm_products.fy2025"),
                                  get("qcom.qtl_ebt.fy2026"))
        xs = (-4.8, -1.6, 1.6, 4.8)
        glyphs = VGroup(draw.chip(0.9, color="#B58CFF"), draw.factory(1.3, color="#8C929B"),
                        viz.phone(1.2, back=True, body="#3B2F2A"), draw.chip(0.9, color="#E9A0C9"))
        names = VGroup(tx("TSMC", 22, "#B58CFF", bold=True), tx("Foxconn", 22, "#8C929B", bold=True),
                       tx("Apple's products", 22, WHITE, bold=True), tx("Qualcomm's patents", 22, "#E9A0C9", bold=True))
        roles = VGroup(tx("makes the processor; the only maker", 15, GREY_B),
                       tx("assembles the phone; one of several", 15, GREY_B),
                       tx("the buyer of both", 15, GREY_B), tx("licensed by every phone maker", 15, GREY_B))
        for g_, n_, r_, x in zip(glyphs, names, roles, xs):
            g_.move_to([x, 2.2, 0])
            n_.move_to([x, 1.25, 0])
            r_.move_to([x, 0.9, 0])
        base = -2.7
        u = 3.3
        vals = (tsmc, fox, apple, qcom)
        cols = ("#B58CFF", "#8C929B", WHITE, "#E9A0C9")
        bars = VGroup()
        for v, x, c in zip(vals, xs, cols):
            b = Rectangle(width=1.1, height=v * u, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [x, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{100 * v:.0f}%", 22, c, bold=True).next_to(b, UP, buff=0.08)))
        what = tx("kept of each dollar of sales (gross margin; Qualcomm's licensing: before tax)", 16, GREY_A).to_edge(
            DOWN, buff=0.15)
        arrows = VGroup(Arrow([xs[0] + 0.6, 2.2, 0], [xs[2] - 0.6, 2.2, 0], buff=0.1, color="#B58CFF", stroke_width=3,
                              path_arc=-0.5),
                        Arrow([xs[1] + 0.7, 2.0, 0], [xs[2] - 0.6, 2.0, 0], buff=0.1, color="#8C929B", stroke_width=3))
        src = source("Part 1's Register: TSMC Q4 2025, Foxconn 2025, Apple FY2025, Qualcomm FY2026 results", corner=UL,
                     size=13)
        with self.voiceover(
            "Two of Porter's forces are other companies: the customers who buy from an industry and the suppliers "
            "who sell to it. Part 1 of this series met them inside a phone. <bookmark mark='a'/> Apple buys its "
            "processors from TSMC, and its assembly from Foxconn. Both are giants. Both sell to the same customer. "
            "<bookmark mark='b'/> TSMC is the only company that can make Apple's processors at the scale and "
            f"precision Apple needs. It keeps {100 * tsmc:.0f} cents of each dollar of sales after the direct cost "
            "of making them. <bookmark mark='c'/> Foxconn assembles phones, and Apple could move that work to "
            f"Luxshare, Pegatron or Tata. Foxconn keeps {100 * fox:.0f} cents. <bookmark mark='d'/> Apple, the buyer, "
            f"keeps {100 * apple:.0f} cents on its products. <bookmark mark='e'/> And Qualcomm, whose patents every "
            f"phone maker must license, keeps {100 * qcom:.0f} cents of its licensing revenue before tax. "
            "<bookmark mark='f'/> Same chain, same phones: the companies that cannot be replaced keep the "
            "money, and the ones that can be replaced work for a sliver. Buyer power is a moat drained by your own "
            "customer."
        ) as vo:
            big = glyphs[2].copy().scale(2.2).move_to([0, 0.6, 0])
            self.play(FadeIn(src), FadeIn(what), FadeIn(big, shift=UP * 0.3))
            self.play(Rotate(big, 0.15, rate_func=there_and_back), run_time=1.2)
            vo.wait_until("a")
            self.play(ReplacementTransform(big, glyphs[2]), FadeIn(names[2]), FadeIn(roles[2]),
                      FadeIn(glyphs[0]), FadeIn(names[0]), FadeIn(glyphs[1]), FadeIn(names[1]))
            self.play(*[GrowArrow(a) for a in arrows])
            vo.wait_until("b")
            self.play(FadeIn(roles[0]), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]))
            vo.wait_until("c")
            self.play(FadeIn(roles[1]), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]))
            vo.wait_until("e")
            self.play(FadeIn(glyphs[3]), FadeIn(names[3]), FadeIn(roles[3]), GrowFromEdge(bars[3][0], DOWN),
                      FadeIn(bars[3][1]))
            vo.wait_until("f")
            self.play(Indicate(bars[0], color=WHITE), Indicate(bars[3], color=WHITE))
            self.play(Indicate(bars[1], color=COST_, scale_factor=1.3))
        self.clear_scene()
