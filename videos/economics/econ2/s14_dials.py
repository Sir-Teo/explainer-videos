from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The Dials: how much do people respond?", r"What do the studies say about real elasticities?",
             "Chapter twelve. The Dials: how much do people respond?", scale=("market", "nation"),
             horizon=("a year", "a decade"))
        self.first()
        self.board()

    def first(self):
        dial = dials.DIALS["elasticity_staples"]
        short = [r"petrol, \ a year or less", r"petrol, \ the long run", r"cigarettes", r"beer", r"wine", r"spirits"]
        dc = dial_card(dial, -1.0, 0.0, width=12.8, font_size=22, ticks=[-1.0, -0.75, -0.5, -0.25, 0.0],
                       short=short).move_to(UP * 0.2)
        src = published_tag(r"Havranek, Irsova and Janda (2012); \ Gallet and List (2003); \ Wagenaar, Salois and "
                            r"Komro (2009): \ meta-analyses", corner=DR, font_size=15)
        g = dial.estimates
        with self.voiceover(
            "Every part enters what it has learned into the Dials, the numbers economics runs on, each with its "
            "range of estimates and how they were measured. This part fills the first one: the price elasticity of "
            "demand for staples. <bookmark mark='a'/> For petrol, the corrected averages we met earlier: "
            f"{say_num(g[0].value)} within a year, {say_num(g[1].value)} in the long run. <bookmark mark='b'/> For cigarettes, "
            f"a meta-analysis by Craig Gallet and John List averaged {say_num(g[2].value)} over more than five hundred "
            "estimates. <bookmark mark='c'/> For alcohol, Alexander Wagenaar and his co-authors pooled more than a "
            f"thousand: about {say_num(g[3].value)} for beer, {say_num(g[4].value)} for wine and {say_num(g[5].value)} for spirits. "
            "<bookmark mark='d'/> Every one is below one in size. That's why taxes on these goods raise so much "
            "revenue: people keep buying. It's also why, as health policy, such taxes work, but slowly, and the "
            "long-run numbers matter more than the short."
        ) as vo:
            self.play(FadeIn(dc.card), FadeIn(dc.head), FadeIn(dc.axis), FadeIn(dc.marks), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(dc.dots[0], scale=0.6), FadeIn(dc.dots[1], scale=0.6))
            vo.wait_until("b")
            self.play(FadeIn(dc.dots[2], scale=0.6))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, scale=0.6) for x in dc.dots[3:]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(dc.meaning))
        self.clear_scene()

    def board(self):
        rows = dials.board()
        b = dial_board(rows[:16], cols=8, radius=0.48, width=13.2, font_size=14).move_to(DOWN * 0.2)
        head = heading(r"The Dials: \ one filled, \ the rest waiting for their parts")
        with self.voiceover(
            "Here are the first sixteen of the Dials. <bookmark mark='a'/> One is lit. The rest are drawn empty, "
            "each with the part that will fill it: the elasticity of intertemporal substitution in Part seven, "
            "markups in Part ten, the multipliers of government spending in Part thirty-two. By the end of the "
            "series every one of them will have its estimates, its designs, and a verdict on how settled it is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, scale=0.9) for f in b.faces], lag_ratio=0.06), run_time=2.5)
        self.clear_scene()
