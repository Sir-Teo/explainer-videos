from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ the scorekeepers", r"Who does this work, \ and what does a week of it look "
             r"like?", "Chapter fourteen. In practice: the scorekeepers.", lit={1957: r"Sydney's estimate",
                                                                               1975: r"CBO"},
             scale=("nation",), horizon=("a day", "a decade"))
        self.jobs()
        self.called()

    def jobs(self):
        cards = point_cards([
            (r"budget offices", r"CBO and the JCT, \ the OBR, \ the CPB: \ baselines, \ scores, \ the record "
             r"published", CBO),
            (r"finance ministries", r"appraisal guidance, \ the Green Book's checks, \ distribution tables at each "
             r"budget", RATE),
            (r"regulators", r"impact assessments for every significant rule, \ reviewed centrally", BEN),
            (r"development banks", r"an economic rate of return for each loan, \ and evaluation offices that "
             r"check it later", SAFE),
            (r"think tanks", r"the IFS, \ the Tax Policy Center, \ the Penn Wharton Budget Model: \ scores that "
             r"check the official ones", TRAV),
            (r"consultancies", r"traffic and demand forecasts, \ business cases: \ where optimism is paid for",
             COST),
        ], width=12.8, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where cost-benefit analysis and scoring are done", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        with self.voiceover(
            "This is a large trade. <bookmark mark='a'/> The budget offices produce baselines and scores, and the "
            "good ones publish their own record, as CBO does. <bookmark mark='b'/> Finance ministries write the "
            "appraisal guidance and check the business cases that come to them, and in Britain publish a "
            "distribution table with every budget. <bookmark mark='c'/> Regulators write an impact assessment for "
            "every significant rule, and a central office reviews it. <bookmark mark='d'/> Development banks compute "
            "an economic rate of return for each loan, and their evaluation offices check it years later. <bookmark "
            "mark='e'/> Think tanks such as the Institute for Fiscal Studies, the Tax Policy Center and the Penn "
            "Wharton Budget Model score bills independently. <bookmark mark='f'/> And consultancies forecast the "
            "traffic and write the business cases, which is where the optimism of chapter ten is paid for. The "
            "skills are this part's: surplus, discounting, a survey and its weights, a model of behaviour, and the "
            "habit of checking the forecast afterwards."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["sydney_1957"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.0)
        lesson = VGroup(
            label(r"an estimate made before anyone knew how to build it", font_size=21, color=SAFE),
            label(r"the building is now loved; \ the estimate was still wrong", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.6)
        tag = published_tag(r"Sydney Opera House; \ National Museum of Australia; \ Guinness World Records",
                            corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1957 the government of New South Wales expected its new opera house "
            "to cost about seven million Australian dollars and to be finished by January 1963. The design, by Jørn "
            "Utzon, had just won a competition as a sketch; no one yet knew how to build its shells. <bookmark "
            "mark='b'/> It opened in October 1973, ten years late, at a cost of a hundred and two million: about "
            "fourteen times the estimate, which Guinness records as the largest proportional increase in the cost "
            "of any building. <bookmark "
            "mark='c'/> The verdict: wrong. <bookmark mark='d'/> The estimate was made before the problem was "
            "understood, <bookmark mark='e'/> and the fact that the building is now loved does not make the "
            "estimate right. It is why appraisals of new kinds of project need the widest ranges of all."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson[0]))
            vo.wait_until("e")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
