from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403

ROWS = [
    ("ultimatum_rejection",
     "Seven new rows today. The first: in the ultimatum game proposers offer far more than the minimum, and "
     "responders reject low offers at a cost to themselves. <bookmark mark='a'/> The original: Güth and colleagues, "
     "1982. <bookmark mark='b'/> The record: a meta-analysis of thirty-seven papers, and fifteen small-scale "
     "societies. <bookmark mark='c'/> One of the most reproducible results in experimental economics. "
     "<bookmark mark='d'/> Replicated."),
    ("punishment_cooperation",
     "The second: when people can punish free riders, cooperation holds up instead of decaying. "
     "<bookmark mark='a'/> The original: Fehr and Gächter, 2002. <bookmark mark='b'/> The record: sixteen "
     "participant pools, where antisocial punishment removed the benefit in some. <bookmark mark='c'/> Robust where "
     "punishment targets free riders. <bookmark mark='d'/> Replicated."),
    ("mere_exposure",
     "The third: repeated exposure increases liking. <bookmark mark='a'/> The original: Zajonc, 1968. "
     "<bookmark mark='b'/> The record: two hundred and eight experiments, and an inverted U across eighty-one "
     "articles. <bookmark mark='c'/> Reliable, with limits. <bookmark mark='d'/> Replicated."),
    ("stated_preferences",
     "The fourth: the partner qualities people say they want predict whom they desire when they meet. "
     "<bookmark mark='a'/> The original: Buss's thirty-seven cultures, 1989. <bookmark mark='b'/> The record: "
     "Eastwick and Finkel's speed dating, and Joel and colleagues' machine learning. <bookmark mark='c'/> As "
     "statements they replicate; as predictions of desire they fail. <bookmark mark='d'/> Failed."),
    ("divorce_prediction",
     "The fifth: watching a couple argue predicts divorce with about ninety percent accuracy. <bookmark mark='a'/> "
     "The original: Gottman and colleagues, 1998. <bookmark mark='b'/> The record: Heyman and Slep on "
     "cross-validation, and eleven thousand couples whose changes were largely unpredictable. <bookmark mark='c'/> "
     "The headline accuracy was never shown on new couples. <bookmark mark='d'/> Contested."),
    ("mate_preferences",
     "The sixth: across cultures, men say they value attractiveness and youth more, and women earning prospects. "
     "<bookmark mark='a'/> The original: Buss, 1989. <bookmark mark='b'/> The record: forty-five countries in 2020. "
     "<bookmark mark='c'/> Replicated, as stated preferences. <bookmark mark='d'/> Replicated."),
    ("isolation_mortality",
     "And the seventh: people with stronger social relationships are more likely to survive. <bookmark mark='a'/> "
     "The original: Holt-Lunstad and colleagues' hundred and forty-eight studies, 2010. <bookmark mark='b'/> The "
     "record: their 2015 meta-analysis of isolation and loneliness. <bookmark mark='c'/> A robust association; the "
     "cause is not established. <bookmark mark='d'/> Replicated."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def row(self, key, text):
        card = ledger_card(self._get(key), width=12.8, font_size=21)
        with self.voiceover(text) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 37 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 5, "failed": 1, "contested": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ fair offers and costly rejections, \ punishment sustaining cooperation, \ mere "
             r"exposure, \ stated mate preferences, \ and the link between relationships and survival", GOOD),
            (r"what failed: \ stated preferences as a guide to whom people desire", AUTH),
            (r"what is argued: \ predicting divorce", YOU),
            (r"the games replicate as behaviour; \ the predictions about particular people do not", MODEL),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: fair offers and costly rejections, punishment sustaining "
            "cooperation, mere exposure, stated mate preferences, and the link between relationships and survival. "
            "<bookmark mark='b'/> What failed: stated preferences as a guide to whom people desire. "
            "<bookmark mark='c'/> What's argued: predicting divorce. <bookmark mark='d'/> The games replicate as "
            "behaviour, across thousands of players. Predictions about particular people, and particular pairs, do "
            "not."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
