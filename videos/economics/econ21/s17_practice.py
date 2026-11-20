from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ R\&D policy and productivity analysis", r"How do governments pay for research, "
             r"\ and who measures productivity?", "Chapter fifteen. In practice: R and D policy and productivity "
             "analysis.", lit={2019: r"a toolkit", 2023: r"the UK's threshold"}, scale=("firm", "nation"),
             horizon=("a year", "a decade"))
        self.credits()
        self.jobs()

    def credits(self):
        rows = VGroup(
            label(r"R\&D tax credits: \ cut the cost of research for every firm that does it", font_size=23,
                  color=IDEA),
            label(r"a regression discontinuity: \ the UK changed the size threshold for its generous small-firm scheme",
                  font_size=21, color=GREY_A),
            label(r"firms just below the new threshold did more R\&D and filed more patents, \ for up to seven years",
                  font_size=21, color=CONS),
            label(r"the effects were largest for firms short of finance, \ and spilled over to technologically close "
                  r"firms", font_size=21, color=CONS),
            label(r"the toolkit \ (Bloom, \ Van Reenen and Williams, \ 2019): \ tax credits and public research work; "
                  r"\ more scientists help most", font_size=21, color=INST),
            label(r"but subsidies raise scientists' pay as well as their number, \ if the supply of scientists is "
                  r"fixed", font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Dechezlepr\^etre, Einio, Martin, Nguyen and Van Reenen, AEJ: Policy 15(4) (2023); \ "
                            r"Bloom, Van Reenen and Williams, JEP 33(3) (2019)", corner=DR, font_size=11)
        with self.voiceover(
            "Governments act on the dial mostly through taxes. <bookmark mark='a'/> An R and D tax credit cuts the "
            "cost of research for any firm that does it. Does it work? <bookmark mark='b'/> Britain offered a more "
            "generous scheme to small and medium-sized firms, and in 2008 raised the size threshold for it, a "
            "natural experiment that Antoine Dechezleprêtre and his co-authors analysed as a regression "
            "discontinuity. <bookmark mark='c'/> Firms just below the new threshold did more research and filed "
            "more patents, for up to seven years. <bookmark mark='d'/> The effects were largest for firms short of "
            "finance, and the research spilled over to technologically close firms. <bookmark mark='e'/> Bloom, "
            "Van Reenen and Williams's survey of the tools concludes that tax credits and direct public research "
            "both work, and that expanding the supply of scientists, through universities and immigration, helps "
            "most in the long run, <bookmark mark='f'/> because when the number of scientists is fixed, subsidies "
            "mainly raise their pay."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def jobs(self):
        cards = point_cards([
            (r"statistical agencies", r"productivity statistics: \\ multifactor productivity, \\ by industry", OUTPUT),
            (r"finance ministries", r"R\&D tax credits: \\ cost, \ take-up, \ evaluation", IDEA),
            (r"competition authorities", r"misallocation, \ market power \\ and the spread of firms' productivity",
             WEDGE),
            (r"firms and consultancies", r"management practices, \\ technology adoption", INST),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who does this work? <bookmark mark='a'/> Statistical agencies, which publish multifactor productivity, "
            "the residual, industry by industry. <bookmark mark='b'/> Finance ministries, which design and evaluate "
            "R and D tax credits. <bookmark mark='c'/> Competition authorities, who watch the spread of productivity "
            "and markups across firms, the subject of part forty-three. <bookmark mark='d'/> And firms and "
            "consultancies, measuring management practices and how fast new technology is adopted, part sixty-two's "
            "subject."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
