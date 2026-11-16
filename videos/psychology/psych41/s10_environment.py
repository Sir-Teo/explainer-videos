from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Environment(VoiceoverScene):
    def construct(self):
        self.card()
        self.ratpark()
        self.vietnam()
        self.vouchers()

    def card(self):
        card = chapter_card(9, r"Cages, \ wars and vouchers", r"How much is addiction about the setting?",
                            lit={1974: r"Robins", 1978: r"Alexander et al.", 1991: r"Higgins et al."}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter nine. Cages, wars and vouchers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ratpark(self):
        head = heading(r"Rat Park")
        cage = Square(side_length=1.2, color=GREY_B).move_to([-5.0, 0.6, 0])
        rat1 = Dot(cage.get_center(), radius=0.1, color=PERSON)
        park = RoundedRectangle(width=3.4, height=2.2, corner_radius=0.2, color=GOOD).move_to([-2.4, 0.6, 0])
        rng = np.random.default_rng(1)
        rats = VGroup(*[Dot(park.get_center() + np.array([rng.uniform(-1.4, 1.4), rng.uniform(-0.8, 0.8), 0]),
                            radius=0.08, color=PERSON) for _ in range(14)])
        l1 = label(r"alone in a cage", font_size=15, color=GREY_A).next_to(cage, DOWN, buff=0.15)
        l2 = label(r"a large, \ social colony", font_size=15, color=GOOD).next_to(park, DOWN, buff=0.15)
        rows = rows_of([
            (r"Alexander, \ Coambs and Hadaway, \ 1978: \ rats alone in cages drank far more morphine solution than "
             r"rats in a large colony with company and space", WHITE),
            (r"the lesson drawn: \ addiction is a response to a barren life, \ not to the drug", GOOD),
            (r"Petrie, \ 1996: \ a replication found housing made little difference; \ later enrichment studies are "
             r"mixed", AUTH),
            (r"the Ledger: \ contested; \ a story told far more often than it has been tested", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Alexander, \ Coambs \& Hadaway (1978); \ Petrie (1996)")
        with self.voiceover(
            "How much is addiction about the setting? <bookmark mark='a'/> In 1978 Bruce Alexander and colleagues "
            "reported that rats alone in cages drank far more morphine solution than rats in a large colony, with "
            "company and space to roam. They called it Rat Park. <bookmark mark='b'/> The lesson drawn was that "
            "addiction is a response to a barren life, not to the drug. <bookmark mark='c'/> But a 1996 replication "
            "by Bruce Petrie found housing made little difference, and later studies of enrichment are mixed. "
            "<bookmark mark='d'/> The Ledger marks it contested: a story told far more often than it's been tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cage), FadeIn(rat1), FadeIn(park), FadeIn(rats), FadeIn(l1),
                      FadeIn(l2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def vietnam(self):
        head = heading(r"Coming home")
        rows = rows_of([
            (r"Robins, \ 1974: \ heroin was cheap and pure in Vietnam, \ and many soldiers used it; \ a large "
             r"minority became addicted there", WHITE),
            (r"after coming home, \ only about 5\% of those addicted in Vietnam were addicted again within a year", GOOD),
            (r"what changed was the setting: \ the cues, \ the supply, \ the stress and the company", PERSON),
            (r"one cohort, \ in unusual conditions: \ it shows recovery without treatment is common, \ not that "
             r"setting is everything", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Robins (1974)")
        with self.voiceover(
            "A larger natural experiment came from a war. <bookmark mark='a'/> In Vietnam, heroin was cheap and pure, "
            "and many American soldiers used it. The sociologist Lee Robins followed them home. A large minority had "
            "become addicted in Vietnam. <bookmark mark='b'/> After coming home, only about five percent of those "
            "addicted in Vietnam were addicted again within a year. <bookmark mark='c'/> What changed was the "
            "setting: the cues, the supply, the stress and the company. <bookmark mark='d'/> It's one cohort, in "
            "unusual conditions. It shows that recovery without treatment is common, not that setting is everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def vouchers(self):
        head = heading(r"Paying for clean samples")
        steps = VGroup()
        for t, c in ((r"a drug-free urine sample", GOOD), (r"a voucher or a prize draw", PERSON),
                     (r"the value rises with each clean sample in a row", MODEL), (r"a positive sample resets it", AUTH)):
            steps.add(word_chip(t, color=c, font_size=18, width=5.4))
        steps.arrange(DOWN, buff=0.25).move_to([-3.6, 0.3, 0])
        rows = rows_of([
            (r"contingency management: \ Part 16's operant conditioning, \ applied", WHITE),
            (r"Higgins and colleagues, \ 1991: \ vouchers for cocaine-free samples kept more patients in treatment and "
             r"abstinent than counselling alone", GOOD),
            (r"Prendergast and colleagues, \ 2006: \ across trials, \ a moderate effect on abstinence during "
             r"treatment, \ one of the best in the field", MODEL),
            (r"the effect fades after the incentives stop, \ and it is used far less than the evidence supports", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Higgins et al.\ (1991); \ Prendergast et al.\ (2006)")
        with self.voiceover(
            "If addiction is learning, learning can be used against it. <bookmark mark='a'/> Contingency management "
            "is Part 16's operant conditioning, applied. A drug-free urine sample earns a voucher or a prize draw, the "
            "value rises with each clean sample in a row, and a positive sample resets it. <bookmark mark='b'/> In "
            "1991 Stephen Higgins and colleagues showed that vouchers for cocaine-free samples kept more patients in "
            "treatment, and abstinent, than counselling alone. <bookmark mark='c'/> In 2006 a meta-analysis led by "
            "Michael Prendergast found a moderate effect on abstinence across trials, one of the best in the field. "
            "<bookmark mark='d'/> The effect fades after the incentives stop. And it's used far less than the "
            "evidence supports."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
