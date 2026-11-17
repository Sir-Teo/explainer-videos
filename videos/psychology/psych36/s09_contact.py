from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Contact(VoiceoverScene):
    def construct(self):
        self.card()
        self.allport()
        self.evidence()

    def card(self):
        card = chapter_card(8, r"Contact", r"Does meeting the other group reduce prejudice?",
                            lit={1954: r"Allport", 2006: r"Pettigrew \& Tropp", 2019: r"Paluck, \ Green \& Green"},
                            part=PART, scale=("group",), marr=("what",))
        with self.voiceover("Chapter eight. Contact."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def allport(self):
        head = heading(r"Allport's conditions")
        conds = VGroup(*[word_chip(t, color=c, font_size=20, width=4.6) for t, c in (
            (r"equal status in the situation", IN), (r"common goals", GOOD), (r"cooperation, \ not competition", MODEL),
            (r"support from authorities, \ law or custom", PERSON))]).arrange(DOWN, buff=0.3).move_to([-3.6, 0.0, 0])
        rows = rows_of([
            (r"Gordon Allport, \ \emph{The Nature of Prejudice}, \ 1954: \ contact between groups reduces "
             r"prejudice, \ under four conditions", WHITE),
            (r"Robbers Cave's shared goals fit the second and third", MODEL),
            (r"Pettigrew and Tropp, \ 2006: \ a meta-analysis of more than 500 studies: \ contact was associated "
             r"with less prejudice, \ and the conditions helped without being necessary", CROWD),
            (r"but most of those studies were correlations: \ people who are less prejudiced may seek out contact", AUTH),
        ], 6.2, 20, 0.36).move_to([3.2, -0.2, 0])
        tag = historical_tag(r"Allport (1954); \ Pettigrew \& Tropp (2006)")
        with self.voiceover(
            "The oldest idea for reducing prejudice is contact. <bookmark mark='a'/> In 1954 Gordon Allport's book "
            "The Nature of Prejudice proposed that contact between groups reduces prejudice under four "
            "conditions: equal status in the situation, common goals, cooperation rather than competition, and "
            "support from authorities, law or custom. <bookmark mark='b'/> Robbers Cave's shared goals fit two of "
            "them. <bookmark mark='c'/> In 2006 Thomas Pettigrew and Linda Tropp pooled more than five hundred "
            "studies. Contact was associated with less prejudice, and Allport's conditions helped without being "
            "necessary. <bookmark mark='d'/> But most of those studies were correlations, and people who are less "
            "prejudiced may be the ones who seek out contact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(c_) for c_ in conds], lag_ratio=0.4), run_time=3.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def evidence(self):
        head = heading(r"Only the randomized studies")
        funnel = VGroup(
            Polygon([-6.0, 1.6, 0], [-1.4, 1.6, 0], [-2.8, -1.2, 0], [-4.6, -1.2, 0], color=GREY_B, stroke_width=2),
            label(r"more than 500 studies", font_size=17, color=GREY_A).move_to([-3.7, 1.2, 0]),
            label(r"randomized, \ with outcomes", font_size=15, color=CROWD).move_to([-3.7, 0.2, 0]),
            label(r"measured a day or more later", font_size=15, color=CROWD).move_to([-3.7, -0.2, 0]),
            label(r"27", font_size=34, color=GOOD).move_to([-3.7, -1.7, 0]))
        rows = rows_of([
            (r"Paluck, \ Green and Green, \ 2019: \ only 27 contact studies assigned contact at random and measured "
             r"prejudice at least a day later", WHITE),
            (r"they are consistent with contact reducing prejudice, \ on average", GOOD),
            (r"but effects varied, \ and were substantially weaker for ethnic and racial prejudice", AUTH),
            (r"their verdict on contact as a policy tool: \ the jury is still out; \ a famous idea, \ thinly "
             r"tested where it matters most", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = published_tag(r"Paluck, \ Green \& Green (2019)")
        with self.voiceover(
            "So look only at experiments. <bookmark mark='a'/> In 2019 Elizabeth Levy Paluck, Seth Green and "
            "Donald Green found that only twenty-seven contact studies had assigned contact at random and measured "
            "prejudice at least a day later. <bookmark mark='b'/> Those studies are consistent with contact "
            "reducing prejudice, on average. <bookmark mark='c'/> But the effects varied, and were substantially "
            "weaker for ethnic and racial prejudice. <bookmark mark='d'/> Their verdict on contact as a policy tool: "
            "the jury is still out. It's a famous idea, thinly tested where it matters most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(funnel[:2]))
            vo.wait_until("a")
            self.play(FadeIn(funnel[2:]), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
