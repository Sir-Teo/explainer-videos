from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Variance(VoiceoverScene):
    def construct(self):
        card(self, 5, "Industry or company?", "How much of a firm's profit is just the industry it is in?",
             "Chapter five. Industry or company?", lit=("moat",))
        V = R["variance"]
        items = [("the business itself", V["business"], RET, f"{100 * V['business']:.0f}%"),
                 ("its industry", V["industry"], MOAT, f"{100 * V['industry']:.0f}%"),
                 ("the parent company", V["parent"], GOLD, f"{100 * V['parent']:.0f}%"),
                 ("the year", V["year"], ENTRANT, f"{100 * V['year']:.0f}%"),
                 ("not explained", V["unexplained"], "#4A5568", f"{100 * V['unexplained']:.0f}%")]
        tm = viz.treemap(items, width=8.2, height=4.6, size=20).move_to([1.6, -0.35, 0])
        whole = Rectangle(width=8.2, height=4.6, stroke_color=GREY_B, stroke_width=2, fill_color="#141A24",
                          fill_opacity=1).move_to(tm)
        whole_t = tx("all the differences in profitability\nbetween American business units, 1981-1994", 24, GREY_A
                     ).move_to(whole)
        # businesses as castles of different heights, in landscapes of different heights
        lands = VGroup()
        for k, (lh, hs) in enumerate(((0.9, (0.9, 1.3, 0.7)), (0.35, (0.8, 0.5, 1.1)))):
            ground = Rectangle(width=2.6, height=lh, stroke_width=0, fill_color=MOAT if k == 0 else "#3E4A3A",
                               fill_opacity=0.5).move_to([-5.0, 1.0 - 2.6 * k, 0], aligned_edge=DOWN)
            cs = VGroup(*[draw.castle(0.55 * h + 0.25, color=STONE) for h in hs]).arrange(RIGHT, buff=0.12,
                                                                                         aligned_edge=DOWN)
            cs.next_to(ground, UP, buff=0)
            lands.add(VGroup(ground, cs))
        lt = VGroup(tx("a rich industry", 17, GREY_B).next_to(lands[0], DOWN, buff=0.12),
                    tx("a poor one", 17, GREY_B).next_to(lands[1], DOWN, buff=0.12))
        src = source("McGahan and Porter, 'How much does industry matter, really?', Strategic Management Journal, 1997")
        with self.voiceover(
            "Is a high return the industry's doing, or the company's? <bookmark mark='a'/> Picture every business as "
            "a castle on a hill. Some hills are higher than others: that is the industry. Some castles are taller "
            "than their neighbours: that is the company. <bookmark mark='b'/> In 1997 Anita McGahan and Michael "
            "Porter measured the two. They took the profitability of the business units of American public "
            "companies, from 1981 to 1994, and asked how much of the differences between them each thing explained. "
            f"<bookmark mark='c'/> The year explained {100 * V['year']:.0f} percent, the parent company "
            f"{100 * V['parent']:.0f}. <bookmark mark='d'/> The industry explained {100 * V['industry']:.0f} percent. "
            f"<bookmark mark='e'/> The business itself, {100 * V['business']:.0f}. And {100 * V['unexplained']:.0f} "
            "percent they could not explain at all. <bookmark mark='f'/> So the hill matters: about a fifth of the "
            "differences in profit come from the industry a business is in. But the castle matters more. The rest "
            "of this part is about both: the barriers that protect a whole industry, and the advantages that "
            "protect one company from its neighbours."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(l_, shift=UP * 0.2) for l_ in lands], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(lt), Indicate(VGroup(lands[0][0], lands[1][0]), color=WHITE, scale_factor=1.03))
            self.play(Indicate(VGroup(lands[0][1][1], lands[1][1][2]), color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(whole), FadeIn(whole_t))
            order = {"c": (3, 2), "d": (1,), "e": (0, 4)}
            shown = []
            for m in "cde":
                vo.wait_until(m)
                if m == "c":
                    self.play(FadeOut(whole_t))
                self.play(*[FadeIn(tm[i], scale=0.92) for i in order[m]], run_time=1.0)
                shown += order[m]
            vo.wait_until("f")
            self.play(Indicate(tm[1], color=WHITE, scale_factor=1.04), Indicate(lands[0][0], color=WHITE))
            self.play(Indicate(tm[0], color=WHITE, scale_factor=1.04), Indicate(lands[0][1][1], color=WHITE))
        self.clear_scene()
