from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Tools(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Redistribution and pre-distribution", r"What can a society do about it?",
             "Chapter thirteen. Redistribution and pre-distribution.", lit={},
             scale=("household", "nation"), horizon=("a year", "a decade"))
        self.flow()
        self.pre()

    def flow(self):
        P = load("practice")
        steps = flow_chain([(r"market \\ income", TOP), (r"less taxes", LOSS), (r"plus cash \\ transfers", GAIN),
                            (r"plus services \\ in kind", MIDDLE)],
                           notes=[r"wages, \ profits, \\ interest, \ rents", r"income, \ payroll, \\ sales "
                                  r"(Part 41)", r"pensions, \ credits, \\ benefits (Part 42)", r"health care, \\ "
                                  r"schools"], box_w=2.6, font_size=20, note_size=15).move_to(UP * 1.2)
        isl = VGroup(
            label(rf"the Island: \ a flat tax of {100 * P['tax']:.0f}\%, \ paid back as an equal "
                  rf"transfer of \${P['transfer']:,.0f}", font_size=20, color=WHITE),
            label(rf"Gini: \ {P['gini_pre']:.3f} before, \ {P['gini_post']:.3f} after", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        two = VGroup(
            label(r"redistribution: \ changes incomes after the market has set them", font_size=21, color=WHITE),
            label(r"pre-distribution: \ changes what the market pays \ (next)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 0.7)
        tag = island_tag(corner=DR, font_size=14)
        head = label(r"redistribution: \ from market income to what people can spend", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What can a society do? The textbook distinction is between redistribution and pre-distribution. "
            "Redistribution changes incomes after the market has set them. <bookmark mark='a'/> Start with market "
            "income: wages, profits, interest and rents. <bookmark mark='b'/> Subtract taxes, the subject of Part "
            "forty-one. <bookmark mark='c'/> Add cash transfers, the subject of Part forty-two. "
            "<bookmark mark='d'/> Add services in kind, such as health care and schools. <bookmark mark='e'/> Even "
            f"the simplest scheme is powerful: on the Island, a flat tax of {100 * P['tax']:.0f} percent paid back "
            f"equally to everyone lowers the Gini from {P['gini_pre']:.2f} to {P['gini_post']:.2f}. What it costs "
            "in work and saving is Part forty-one's question."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head), FadeIn(two[0]), FadeIn(two[1]))
            vo.wait_until("a")
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(isl, shift=UP * 0.1))
        self.clear_scene()

    def pre(self):
        cards = point_cards([
            (r"skills", r"schooling and early \\ childhood: \ the race \\ of Part 39", TOP),
            (r"wage setting", r"minimum wages \\ (Part 38), \ unions \\ (Part 39)", MIDDLE),
            (r"competition", r"monopoly and \\ monopsony power \\ (Parts 10 and 38)", WEALTH),
            (r"places", r"where children grow \\ up: \ housing, \\ schools, \ moves", CHILD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"pre-distribution: \ changing market incomes themselves", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Pre-distribution changes what the market pays in the first place. <bookmark mark='a'/> Skills, through "
            "schools and early childhood, the race of Part thirty-nine. <bookmark mark='b'/> How wages are set: "
            "minimum wages and unions. <bookmark mark='c'/> Competition, against the market power of Parts ten and "
            "thirty-eight. <bookmark mark='d'/> And places, which this part found matter most for children. Each has "
            "its own costs and evidence, and each later part weighs them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
