from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Schools(VoiceoverScene):
    def construct(self):
        card(self, 8, r"School choice", r"How should a city give out places at its public schools?",
             "Chapter eight. School choice.",
             lit={2003: r"Abdulkadiroğlu and Sönmez", 2004: r"New York's new match", 2017: r"Chen and Kesten"},
             scale=("city", "nation"), horizon=("a year",))
        self.boston()
        self.newyork()
        self.china()

    def boston(self):
        rows = VGroup(
            label(r"2003: \ Atila Abdulkadiroğlu and Tayfun Sönmez look at how cities assign school places",
                  font_size=23),
            label(r"many used the Boston rule: \ it tries to give as many families as possible their first choice",
                  font_size=23, color=SCHOOL),
            label(r"but listing a popular school first, \ and missing, \ can cost you your second choice too",
                  font_size=23, color=REJECT),
            label(r"so families who know the game list safe schools first; \ families who don't, \ lose",
                  font_size=23, color=REJECT),
            label(r"their proposal: \ deferred acceptance with students asking: \ the truth is safe, \ and no "
                  r"student envies a place they had the better claim to", font_size=22, color=STABLE),
            label(r"Boston adopted it, \ and other cities followed", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Abdulkadiroğlu and Sönmez, AER 93(3) (2003)", corner=DR, font_size=13)
        with self.voiceover(
            "School places are the largest matching market most people ever meet. <bookmark mark='a'/> In 2003 "
            "Atila Abdulkadiroğlu and Tayfun Sönmez looked at how American cities were giving them out. "
            "<bookmark mark='b'/> Many used the Boston rule from Play it, which tries to give as many families as "
            "possible their first choice. That sounds good. <bookmark mark='c'/> But as you found, listing a "
            "popular school first and missing it can cost you your second choice as well. "
            "<bookmark mark='d'/> So families who understood the game listed safer schools first, and families who "
            "did not paid for their honesty. <bookmark mark='e'/> They proposed deferred acceptance with students "
            "asking: the truth is safe, and no student loses a place to someone with a weaker claim to it. "
            "<bookmark mark='f'/> Boston adopted it, and other cities followed."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def newyork(self):
        n = load("roth")["nyc"]
        base_y, sc = -2.2, 3.6 / 32000
        bars = VGroup()
        for i, (v, c) in enumerate(((n["unassigned_before"], REJECT), (n["unassigned_after"], STABLE))):
            h = v * sc
            r = Rectangle(width=1.6, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [-3.6 + 3.0 * i, base_y + h / 2, 0])
            bars.add(r)
        base = Line([-5.2, base_y, 0], [0.4, base_y, 0], color=GREY_B, stroke_width=2)
        labs = VGroup(label(r"before", font_size=21, color=GREY_A).next_to(bars[0], DOWN, buff=0.2),
                      label(r"after", font_size=21, color=GREY_A).next_to(bars[1], DOWN, buff=0.2))
        vals = VGroup(label(rf"about {n['unassigned_before']:,}".replace(",", "{,}"), font_size=24,
                            color=REJECT).next_to(bars[0], UP, buff=0.1),
                      label(rf"about {n['unassigned_after']:,}".replace(",", "{,}"), font_size=24,
                            color=STABLE).next_to(bars[1], UP, buff=0.1))
        head = label(r"New York's high schools: \ students placed by the administration at schools they never chose",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.4)
        side = VGroup(
            label(rf"about {n['entering']:,} students \\ start high school each year".replace(",", "{,}"),
                  font_size=21),
            label(r"the old system: \ offers and waiting \\ lists by post, \ one round at a time", font_size=21,
                  color=REJECT),
            label(r"a congested market: \\ the waiting lists couldn't move", font_size=21, color=GREY_A),
            label(r"from 2003--04: \ one stable \\ clearinghouse, \ students asking", font_size=21, color=STABLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        tag = published_tag(r"Abdulkadiroğlu, Pathak and Roth, AER 95(2) (2005); \ Roth, Nobel lecture (2012)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "New York's problem was different. <bookmark mark='a'/> Almost ninety thousand students start high "
            "school there each year. <bookmark mark='b'/> Under the old system, schools sent offers by post, and "
            "a student holding two offers had to send one back before anyone on a waiting list could be admitted. "
            "<bookmark mark='c'/> It was the congestion of the 1940s hospitals again: the waiting lists could not "
            "move fast enough, and just before school began about thirty thousand students had no place at all, "
            "and were assigned by the administration to schools they had never listed. "
            "<bookmark mark='d'/> From 2003, with Abdulkadiroğlu, Parag Pathak and Roth, the city ran one stable "
            "clearinghouse with students asking. Almost at once, the thirty thousand fell to about three thousand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(base), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), GrowFromEdge(bars[0], DOWN), FadeIn(labs[0]), FadeIn(vals[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), GrowFromEdge(bars[1], DOWN), FadeIn(labs[1]), FadeIn(vals[1]))
        self.clear_scene()

    def china(self):
        rows = VGroup(
            label(r"China's university places: \ millions of students, \ one exam, \ province by province",
                  font_size=24),
            label(r"the old sequential rule: \ like Boston's, \ a missed first choice could sink a strong student",
                  font_size=23, color=REJECT),
            label(r"the ``parallel'' rule: \ several choices treated together, \ then the next group",
                  font_size=23, color=HELD),
            label(r"Yan Chen and Onur Kesten (2017): \ it lies between Boston's rule and deferred acceptance",
                  font_size=23, color=STABLE),
            label(r"safer to tell the truth, \ more stable, \ than the rule it replaced", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Chen and Kesten, JPE 125(1) (2017)", corner=DR, font_size=13)
        with self.voiceover(
            "The largest school match of all is for China's universities. <bookmark mark='a'/> Millions of "
            "students sit the national examination each year and are placed province by province. "
            "<bookmark mark='b'/> Under the old sequential rule, much like Boston's, a strong student who aimed too "
            "high with a first choice could end up with nothing good. <bookmark mark='c'/> Many provinces have "
            "moved to a parallel rule, which treats a student's first several choices together, deferring "
            "acceptance among them, before moving on to the next group. <bookmark mark='d'/> Yan Chen and Onur "
            "Kesten showed that it lies between Boston's rule and deferred acceptance: <bookmark mark='e'/> safer "
            "to be honest under, and more stable, than the rule it replaced."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                if mk == "a":
                    continue
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
