from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403

ROWS = [
    ("asch_conformity",
     "Ten new rows today. The first: people often give an answer they can see is wrong when a unanimous group gives it "
     "first. <bookmark mark='a'/> The original: Asch's monograph of 1956. <bookmark mark='b'/> The record: Bond and "
     "Smith's meta-analysis of a hundred and thirty-three studies, and Franzen and Mader's replication in 2023, at "
     "thirty-three percent. <bookmark mark='c'/> Robust and durable, though smaller in later and individualist "
     "samples, and one ally removes most of it. <bookmark mark='d'/> Replicated, smaller."),
    ("milgram_obedience",
     "The second: most ordinary people will give apparently dangerous shocks when an experimenter tells them to. "
     "<bookmark mark='a'/> The original: Milgram's twenty-six of forty, in 1963. <bookmark mark='b'/> The record: "
     "Burger's partial replication; the synthesis of twenty-one conditions at forty-four percent; and the archive "
     "reanalysis, in which only about half had fully believed. <bookmark mark='c'/> Never run in full again. Milder "
     "versions replicate the willingness to go on, while what it means is contested. <bookmark mark='d'/> Not "
     "directly tested."),
    ("stanford_prison",
     "The third: randomly assigned guards spontaneously became abusive, because a role takes over the person. "
     "<bookmark mark='a'/> The original: Stanford, 1971. <bookmark mark='b'/> The record: the BBC prison study, "
     "where the guards never took to their role, and Le Texier's archives, which show the guards were coached. "
     "<bookmark mark='c'/> It was not an experiment on what a role does by itself. <bookmark mark='d'/> Story and "
     "record."),
    ("genovese_witnesses",
     "The fourth: thirty-eight neighbours watched Kitty Genovese's murder and none called the police. "
     "<bookmark mark='a'/> The original: the New York Times, 1964. <bookmark mark='b'/> The record: Manning, Levine "
     "and Collins, who found about a dozen partial witnesses and at least one call to the police. "
     "<bookmark mark='c'/> The effect it inspired is real; the story that launched it wasn't. <bookmark mark='d'/> "
     "Story and record."),
    ("bystander_effect",
     "The fifth: the more bystanders there are, the less likely each one is to help. <bookmark mark='a'/> The "
     "original: Darley and Latané's intercom seizure, in 1968. <bookmark mark='b'/> The record: Fischer and "
     "colleagues' meta-analysis, and Philpot and colleagues' cameras, where someone helped in nine of ten conflicts. "
     "<bookmark mark='c'/> True of each person in the laboratory; on the street a larger crowd still means help is "
     "more likely. <bookmark mark='d'/> Replicated."),
    ("social_facilitation",
     "The sixth: an audience improves simple tasks and impairs complex ones. <bookmark mark='a'/> The original: "
     "Zajonc's cockroaches, in 1969. <bookmark mark='b'/> The record: the preregistered replication of 2020, which "
     "found slowing on both tasks. <bookmark mark='c'/> Social inhibition replicates; the facilitation half of the "
     "famous interaction did not. <bookmark mark='d'/> Contested."),
    ("social_loafing",
     "The seventh: people work less hard on a collective task. <bookmark mark='a'/> The original: Latané, Williams "
     "and Harkins's shouting students, in 1979. <bookmark mark='b'/> The record: Karau and Williams's seventy-eight "
     "studies. <bookmark mark='c'/> One of the steadier group effects. <bookmark mark='d'/> Replicated."),
    ("groupthink",
     "The eighth: cohesive, insulated groups under directive leaders seek consensus and decide badly. "
     "<bookmark mark='a'/> The original: Janis's case studies, in 1972. <bookmark mark='b'/> The record: a quarter "
     "century of research, found virtually devoid of support. <bookmark mark='c'/> Case studies fit it; experiments "
     "rarely confirm its causal model. <bookmark mark='d'/> Contested."),
    ("hotel_towel_norms",
     "The ninth: telling hotel guests that most guests reuse their towels works better than an environmental appeal. "
     "<bookmark mark='a'/> The original: Goldstein, Cialdini and Griskevicius, 2008. <bookmark mark='b'/> The record: "
     "two German hotels, where the norm did no better than the standard appeal. <bookmark mark='c'/> Norm messages "
     "help, but their edge depends on the setting. <bookmark mark='d'/> Contested."),
    ("crowd_influence",
     "And the tenth: seeing others' estimates reduces a crowd's diversity without making it more accurate. "
     "<bookmark mark='a'/> The original: Lorenz and colleagues, 2011. <bookmark mark='b'/> The record: Becker, "
     "Brackbill and Centola, who found that in decentralized networks influence improved accuracy. "
     "<bookmark mark='c'/> Whether influence helps or harms a crowd depends on who is listened to. "
     "<bookmark mark='d'/> Contested."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("group",), marr=("what",))
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
        head = heading(r"Part 34 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 2, "replicated, smaller": 1, "contested": 4, "story and record": 2,
                          "not directly tested": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ conformity to a unanimous group, \ less help from each bystander, \ and loafing in "
             r"groups", GOOD),
            (r"what was never tested in full: \ Milgram's obedience", STATUS_COLOR["not directly tested"]),
            (r"two stories that outran their records: \ the prison study and the 38 witnesses", P.ACCENT),
            (r"what is argued: \ audiences, \ groupthink, \ norm messages and influence on crowds", YOU),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: conformity to a unanimous group, less help from each "
            "bystander, and loafing in groups. <bookmark mark='b'/> What was never tested in full: Milgram's "
            "obedience. <bookmark mark='c'/> Two stories that outran their records: the prison study and the "
            "thirty-eight witnesses. <bookmark mark='d'/> And what's argued: audiences, groupthink, norm messages, "
            "and influence on crowds. The most famous studies in this part are the weakest; the dull ones held."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
