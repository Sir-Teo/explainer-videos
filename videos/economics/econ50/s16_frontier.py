from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ what remains unidentified", r"Which studies would change the memo?",
             "Chapter fourteen. Frontier: what remains unidentified.", lit={2025: r"Baby's First Years"},
             scale=("household", "nation"), horizon=("a decade", "a generation"))
        self.trial()
        self.open_questions()

    def trial(self):
        F = tables.FRONTIER50.data
        groups = VGroup()
        for amt, col, txt in ((F["high"], NEW, r"a high gift"), (F["low"], OLD, r"a low gift")):
            g = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=col, fill_opacity=0.9) for _ in range(40)])
            g.arrange_in_grid(rows=4, cols=10, buff=0.08)
            lab = label(rf"{txt}: \ \${amt} a month", font_size=19, color=col).next_to(g, UP, buff=0.15)
            groups.add(VGroup(g, lab))
        groups.arrange(DOWN, buff=0.5).move_to(LEFT * 3.6 + UP * 0.4)
        head = label(rf"Baby's First Years: \ {F['mothers']:,} mothers below the poverty line, \ from birth"
                     .replace(",", "{,}"), font_size=22, color=WHITE).to_edge(UP, buff=0.45)
        outs = VGroup(*[VGroup(label(o, font_size=18, color=WHITE),
                               label(r"no significant difference", font_size=15, color=HOLD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06) for o in (r"language", r"executive function",
                                                          r"social-emotional problems", r"brain activity (EEG)")])
        outs.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.2 + UP * 0.2)
        oh = label(r"at age four:", font_size=20, color=GREY_A).next_to(outs, UP, buff=0.3).align_to(outs, LEFT)
        note_ = label(r"randomized; \ effects may yet appear later in life", font_size=18,
                      color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Noble, Magnuson, Duncan, Gennetian et al., \ NBER WP 33844 (2025)", corner=DR,
                            font_size=12)
        sch = label(r"dots: \ schematic", font_size=12, color=GREY_B).to_corner(DL, buff=0.3)
        with self.voiceover(
            "The frontier for this memo is defined by its weakest page, the long run. The best new evidence is a "
            f"randomized trial, Baby's First Years. <bookmark mark='a'/> From 2018, {F['mothers']:,} mothers with "
            "incomes below the poverty line were recruited in maternity wards and assigned by lottery to receive "
            f"either {F['high']} dollars a month, <bookmark mark='b'/> or {F['low']} dollars a month, for the "
            "first years of their children's lives. <bookmark mark='c'/> In 2025 the researchers reported the "
            "results at age four: no statistically significant effect on any of the four outcomes they had named "
            "in advance, language, executive function, social and emotional problems, and brain activity. "
            "<bookmark mark='d'/> That is not proof of no effect: the gains of Mothers' Pensions appeared in "
            "adulthood, and effects may yet appear later in these children's lives. But it is the most direct modern "
            "evidence, and an honest memo "
            "must give it the same weight it would give a positive result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(oh), LaggedStart(*[FadeIn(o, shift=LEFT * 0.1) for o in outs], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(note_, shift=UP * 0.1))
        self.clear_scene()

    def open_questions(self):
        cards = point_cards([
            (r"permanent behaviour", r"how parents respond when the allowance is expected to last: \ a staggered "
                                     r"start would measure it", WORK),
            (r"the long run", r"children's earnings and health as adults: \ the trials of today report in the 2040s",
             EVIDENCE),
            (r"births and families", r"whether a lasting allowance changes fertility, \ marriage or living "
                                     r"arrangements", CHILD),
            (r"delivery", r"paying the poorest automatically, \ from records, \ without a tax return", HOLD),
            (r"at scale", r"rents and local prices where many families gain at once", NEW),
            (r"the weights", r"how much societies value children's incomes: \ revealed in their budgets, \ "
                             r"and argued about in their elections", GREY_A),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what would change the memo", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What else remains unidentified? <bookmark mark='a'/> How parents respond to an allowance they expect "
            "to last, which a staggered start could measure within a few years. <bookmark mark='b'/> Children's "
            "earnings and health as adults: the trials running today will report in the 2040s. <bookmark "
            "mark='c'/> Whether a lasting allowance changes births, marriage or who lives with whom. <bookmark "
            "mark='d'/> How to pay the poorest families automatically, from records the government already "
            "holds. <bookmark mark='e'/> What happens to rents and local prices where many families gain at once. "
            "<bookmark mark='f'/> And the weights themselves, which no study identifies: societies reveal them in "
            "their budgets and argue about them in their elections. The economist's job is to make that argument "
            "about values, and not about facts that could have been measured."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
