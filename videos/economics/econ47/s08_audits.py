from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Audits(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Audits from above, \ meetings from below", r"What cut the theft, and what did not?",
             "Chapter seven. Audits from above, meetings from below.", lit={2007: r"Olken"}, scale=("village",),
             horizon=("a year",))
        self.results()
        self.why()
        self.perceptions()

    def results(self):
        T = tables.OLKEN_2007.data
        rows = [(r"projects without \\ the audit", T["missing_control"], CONTROL),
                (r"projects told they \\ would be audited", T["missing_audit"], AUDIT)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            y = 1.3 - 1.2 * i
            w = v / 30 * 7.0
            r = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.0 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=20, color=col).next_to(np.array([-2.2, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{v}\%", font_size=24, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(r"Indonesia: \ the share of road spending missing", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        notes = VGroup(
            label(rf"audits: \ the chance raised from {T['audit_from']}\% to {T['audit_to']}\%, \ announced before "
                  rf"construction: \ about {T['effect']} points less missing", font_size=21, color=AUDIT),
            label(r"more than enough to pay for the audits", font_size=21, color=GAIN),
            label(r"meetings and anonymous comment forms: \ little effect on average", font_size=21, color=VOTER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.OLKEN_2007.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Here is what Olken found in Indonesia. <bookmark mark='a'/> In projects that faced the usual small "
            f"chance of an audit, {T['missing_control']} percent of the money was missing, by J-PAL's summary of "
            "the study. <bookmark mark='b'/> In projects told, before construction began, that they would "
            f"certainly be audited, {T['missing_audit']} percent. <bookmark mark='c'/> About {T['effect']} "
            "points less, and the money saved was more than the audits cost. <bookmark mark='d'/> Village meetings "
            "and anonymous comment forms did little on average. They reduced missing wages, which villagers could "
            "see because they or their neighbours had worked on the road, but not missing materials, which they "
            "could not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b[0]) for b in bars])
            for mk, b in zip("ab", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"free riding", r"each villager gains \\ little from going \\ to a meeting: \\ chapter one", FEW),
            (r"what is visible", r"wages paid to \\ neighbours, \ yes; \\ gravel in the \\ road, \ no", VOTER),
            (r"elite capture", r"meetings can be \\ dominated by those \\ being watched", ELITE),
            (r"credible threat", r"auditors can \\ prosecute; \\ neighbours can \\ only complain", AUDIT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"why the cure from below did so little", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.OLKEN_2007.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Why did monitoring from below fail? <bookmark mark='a'/> Free riding: every villager gains from a "
            "well-built road, but each gains little from spending an evening checking the accounts, chapter one's "
            "logic at the scale of a village. <bookmark mark='b'/> Visibility: villagers can see who was paid, but "
            "not how much gravel lies under the asphalt. <bookmark mark='c'/> Capture: meetings can be dominated by "
            "the same village elite who manage the money; participation reduced theft only where free riding and "
            "elite capture were limited. <bookmark mark='d'/> And credibility: an auditor's report can lead to "
            "prosecution, while a "
            "neighbour can only complain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def perceptions(self):
        R = load("roads")
        T = tables.OLKEN_2007.data
        rows = VGroup(
            label(rf"Olken, \ 2009: \ 10\% more money missing \ $\rightarrow$ \ {T['perception']}\% more likely "
                  r"that a villager \\ thinks there is any corruption", font_size=22, color=WHITE),
            label(r"in ethnically mixed villages: \ more corruption perceived, \ less found", font_size=22,
                  color=HOLD),
            label(rf"on the Island: \ the correlation of perceived and actual theft is "
                  rf"{R['perception_corr']:.2f}", font_size=22, color=VOTER),
            label(r"surveys of perceptions measure something, \ but not the theft itself", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"perception against reality", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.OLKEN_2007.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Olken also asked the villagers how corrupt they thought their road project was. <bookmark mark='a'/> "
            f"Their answers tracked the truth only faintly: ten percent more money missing made a villager "
            f"{T['perception']} percent more likely to think there was any corruption at all, partly because "
            "officials hid the theft where villagers could not see it. <bookmark mark='b'/> In ethnically mixed "
            "villages people perceived more corruption, and there was less. <bookmark mark='c'/> The Island's "
            f"villagers are planted the same way: the correlation between what they perceive and what is stolen is "
            f"{R['perception_corr']:.2f}. <bookmark mark='d'/> That matters, because most of what the world knows "
            "about corruption comes from surveys of perceptions. The next chapters measure it four ways."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
