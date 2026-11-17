from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403

ROWS = [
    ("minimal_group",
     "Eight new rows today. The first: assigning people to groups by a trivial criterion is enough for them to favour "
     "their own group. <bookmark mark='a'/> The original: Tajfel and colleagues' schoolboys, in 1971. "
     "<bookmark mark='b'/> The record: Balliet, Wu and De Dreu's two hundred and twelve studies. <bookmark mark='c'/> "
     "Robust but modest when groups are mere labels, and mostly warmth for us rather than hostility to them. "
     "<bookmark mark='d'/> Replicated."),
    ("iat_group",
     "The second: on average, people sort faster when categories are paired as common associations pair them. "
     "<bookmark mark='a'/> The original: Greenwald, McGhee and Schwartz, 1998. <bookmark mark='b'/> The record: "
     "Greenwald and Lai's review, with internal consistency near point eight and retest near point five. "
     "<bookmark mark='c'/> The average effect is robust; what it means for one person is the next row. "
     "<bookmark mark='d'/> Replicated."),
    ("iat_individual",
     "The third: a person's IAT score predicts their discriminatory behaviour well enough to judge individuals, and "
     "changing it changes behaviour. <bookmark mark='a'/> The original: Greenwald and colleagues' meta-analysis of "
     "2009. <bookmark mark='b'/> The record: Oswald and colleagues' reanalysis, and Forscher and colleagues' four "
     "hundred and ninety-two studies. <bookmark mark='c'/> The score is a weak guide to one person, and changing it "
     "doesn't change behaviour. <bookmark mark='d'/> Failed."),
    ("hiring_audits",
     "The fourth: identical applications get fewer callbacks when the name signals a Black applicant. "
     "<bookmark mark='a'/> The original: Bertrand and Mullainathan, 2004. <bookmark mark='b'/> The record: "
     "Quillian and colleagues' twenty-eight studies. <bookmark mark='c'/> Consistent, measured as behaviour, and "
     "unchanged in a quarter century. <bookmark mark='d'/> Replicated."),
    ("stereotype_threat",
     "The fifth: reminding people of a negative stereotype about their group lowers their test performance. "
     "<bookmark mark='a'/> The original: Steele and Aronson, 1995. <bookmark mark='b'/> The record: Sackett and "
     "colleagues on the adjustment, and the Dutch registered study. <bookmark mark='c'/> Its size and reach are "
     "unsettled. <bookmark mark='d'/> Contested."),
    ("intergroup_contact",
     "The sixth: contact between groups reduces prejudice. <bookmark mark='a'/> The original evidence: Pettigrew and "
     "Tropp's meta-analysis of 2006. <bookmark mark='b'/> The record: the twenty-seven randomized studies. "
     "<bookmark mark='c'/> The average holds, but the causal evidence is thin where it matters most. "
     "<bookmark mark='d'/> Replicated."),
    ("deep_canvassing",
     "The seventh: a single conversation at the door can durably reduce prejudice. <bookmark mark='a'/> The "
     "original: LaCour and Green's paper of 2014, fabricated and retracted. <bookmark mark='b'/> The record: "
     "Broockman and Kalla's real experiment of 2016. <bookmark mark='c'/> Replicated by the people who exposed the "
     "fake. <bookmark mark='d'/> Replicated."),
    ("robbers_cave",
     "And the eighth: competition at a summer camp produced hostility, and shared goals removed it. "
     "<bookmark mark='a'/> The original: Sherif and colleagues, 1954. <bookmark mark='b'/> The record: Perry's "
     "archives, with a failed first run left out of the report. <bookmark mark='c'/> A demonstration with the "
     "conditions arranged. <bookmark mark='d'/> Story and record."),
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
        head = heading(r"Part 36 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 5, "failed": 1, "contested": 1, "story and record": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ favouritism for a mere label, \ the average implicit association, \ discrimination in "
             r"hiring audits, \ contact, \ and deep canvassing", GOOD),
            (r"what failed: \ the IAT as a guide to one person, \ or as a lever on behaviour", AUTH),
            (r"what is argued: \ stereotype threat", YOU),
            (r"a story set against its record: \ Robbers Cave", P.ACCENT),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: favouritism for a mere label, the average implicit "
            "association, discrimination in hiring audits, contact, and deep canvassing. <bookmark mark='b'/> What "
            "failed: the IAT as a guide to one person, or as a lever on behaviour. <bookmark mark='c'/> What's "
            "argued: stereotype threat. <bookmark mark='d'/> And one story set against its record, Robbers Cave. "
            "The strongest evidence in this part measures behaviour, at scale, with random assignment."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
